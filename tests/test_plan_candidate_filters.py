"""关联筛选读取主记录；计划关系、分类与视图不得互相污染。"""

import json
from datetime import datetime
import httpx
import pytest
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from models import TestCase as Case, TestPlan as Plan, Project, ProjectMember, Module, TestSuite as Suite, CaseAttachment
from models.case_features import CaseIssue, CaseIssueLink, CaseTemplate
from models.plan_workspace import PlanNode, PlanWorkspace
from models.plan_case_view import PlanCaseSavedView
from models.case_governance import CaseVersion
from models.task_queue import TaskQueue
from services.plan_tree import save_node
from services.plan_candidate_filter import plan_membership

BASE = '/orchestration/plans/plan/case-workspace'


def c(field, op, value=None):
    return dict(field=field, operator=op, value=value)


def params(*conditions, logic='and', **other):
    return dict(filters=json.dumps(dict(conditions=list(conditions), logic=logic)), **other)


@pytest.mark.asyncio
async def test_advanced_candidate_categories_mine_and_foreign_project_are_isolated(workspace_http):
    db, app, _ = workspace_http
    db.add(Project(id='other', name='不可混入项目', owner_id='owner')); db.flush()
    db.add(Plan(id='foreign-plan', project_id='other', name='不可混入计划', plan_number='FOREIGN', owner_id='owner'))
    for cid, category, automated, creator, project in [
        ('api', 'api', True, 'owner', 'project'),
        ('api-other', 'api', True, 'stranger', 'project'),
        ('api-manual', 'api', False, 'owner', 'project'),
        ('scenario', 'scenario', True, 'owner', 'project'),
        ('foreign', 'api', True, 'owner', 'other'),
    ]:
        db.add(Case(id=cid, project_id=project, name='分类验收', case_code=cid,
                    type=category, is_automated=automated, created_by=creator, steps=[], status='failed'))
    db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        for category, expected in [('api', {'api', 'api-other'}), ('scenario', {'scenario'})]:
            query = params(c('status', 'equals', 'failed'), category=category)
            data = (await client.get(BASE+'/candidates', params=query)).json()['data']
            assert {row['id'] for row in data['items']} == expected
            assert data['counts']['all'] == len(expected)
            assert 'foreign-plan' not in [p['id'] for p in data['plans']]
            mine = (await client.get(BASE+'/candidates', params={**query, 'mine': True})).json()['data']
            assert {row['id'] for row in mine['items']} == {category}
        assert (await client.get(BASE+'/candidates', params=params(c('planIds', 'equals', 'foreign-plan')))).json()['data']['total'] == 0
    assert db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_candidate_status_scope_related_fields_pages_counts_and_current_user(workspace_http):
    db, app, identity = workspace_http
    db.add(Module(id='parent', project_id='project', name='父模块')); db.flush()
    db.add(Module(id='child', project_id='project', name='子模块', parent_id='parent')); db.flush()
    case = db.get(Case, 'case-0'); case.module_id='child'; case.status='failed'; case.tags=['回归', '诊断']
    case.created_at = datetime(2026, 10, 5, 0); case.updated_by='owner'
    case.custom_fields={'deadline':'2026-10-05', 'zero':0, 'enabled':False}; case.template_id='typed'
    db.add(CaseTemplate(id='typed', project_id='project', name='类型模板', created_by='owner',
                        fields=[dict(key='deadline', type='date'), dict(key='zero',type='number'), dict(key='enabled',type='boolean')]))
    db.add(CaseAttachment(case_id=case.id,file_name='诊断.pdf',file_path='隔离占位'))
    db.add(CaseIssue(id='need',project_id='project',kind='requirement',title='诊断需求',created_by='owner',updated_by='owner'));db.flush()
    db.add(CaseIssueLink(issue_id='need',case_id=case.id,created_by='owner'))
    db.get(Case, 'case-1').created_by='stranger'; db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        query=params(c('status','equals','failed'),c('attachment','contains','诊断'),c('requirementRef','contains','诊断'),
            c('createdBy','belongs_to',['CURRENT_USER']),c('updatedBy','belongs_to',['CURRENT_USER']),c('tags','count_gt',1),
            c('createdAt','between',['2026-10-05T00:00:00Z','2026-10-05T01:00:00Z']),
            c('customFields.deadline','between',['2026-10-05','2026-10-05']),c('customFields.zero','equals',0),c('customFields.enabled','equals',False),
            c('reviewResult','equals','not_reviewed'),folder='别的目录',search='旧搜索',priority='P3',size=1)
        response=await client.get(BASE+'/candidates',params=query)
        assert response.status_code==200,response.text
        data=response.json()['data'];assert data['total']==1 and data['items'][0]['id']=='case-0' and data['items'][0]['alreadyLinked']
        assert data['counts']=={'all':1,'unassigned':0}
        assert next(m['count'] for m in data['modules'] if m['id']=='parent')==1
        assert data['projectId']=='project' and [p['id'] for p in data['plans']]==['plan']
        two=params(c('name','contains','用例 0'),c('id','contains','CODE-2'),c('name','contains',''),logic='or',size=1)
        first=(await client.get(BASE+'/candidates',params=two)).json()['data']
        second=(await client.get(BASE+'/candidates',params={**two,'page':2})).json()['data']
        assert first['total']==second['total']==2 and first['items'][0]['id']!=second['items'][0]['id']
        assert (await client.get(BASE+'/candidates',params=params(c('name','contains','用例'),mine=True))).json()['data']['total']==2
        for invalid in ['{','[]',json.dumps({'conditions':[c('result','equals','passed')]}),json.dumps({'conditions':[c('collectionId','equals','id')]}),json.dumps({'logic':'错误'})]:
            assert (await client.get(BASE+'/candidates',params={'filters':invalid})).status_code==422
        db.get(Case,'case-0').deleted_at=datetime.now();db.commit()
        assert (await client.get(BASE+'/candidates',params=query)).json()['data']['total']==0
        identity['id']='stranger'
        assert (await client.get(BASE+'/candidates',params=two)).status_code==403
    assert db.query(CaseVersion).count()==0 and db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_membership_legacy_points_tree_duplicates_suites_and_empty_tree(workspace_http):
    db, app, _ = workspace_http
    plan=db.get(Plan,'plan')
    point=save_node(db,plan,dict(name='仅目录',nodeType='point'));db.commit()
    assert plan_membership(db,'project')[0]['case-0']=={'plan'}  # 只有测试点时旧关联仍有效。
    db.get(Case,'case-2').is_automated=False
    first=save_node(db,plan,dict(name='手工关联',nodeType='case',category='functional',caseId='case-2'))
    second=save_node(db,plan,dict(name='重复实例',nodeType='case',category='functional',caseId='case-2',parentId=point.id))
    suite=save_node(db,plan,dict(name='测试套',nodeType='suite',category='functional',suiteId='suite-0'))
    db.commit()
    membership,_=plan_membership(db,'project')
    assert membership['case-2']=={'plan'} and membership['case-0']=={'plan'} and not membership['case-1']
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        data=(await client.get(BASE+'/candidates',params=params(c('planIds','equals','plan')))).json()['data']
        assert data['total']==2 and {r['id'] for r in data['items']}=={'case-0','case-2'}
        assert (await client.get(BASE+'/candidates',params=params(c('planIds','not_equals','plan')))).json()['data']['total']==1
        for node in [first,second,suite]:db.delete(node)
        db.get(PlanWorkspace,'plan').uses_tree=True;db.commit()
        assert (await client.get(BASE+'/candidates',params=params(c('planIds','equals','plan')))).json()['data']['total']==0
        assert (await client.get(BASE+'/candidates',params=params(c('planIds','is_empty')))).json()['data']['total']==3
    assert db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_drawer_views_crud_owners_categories_limits_and_workspace_isolation(workspace_http):
    db,app,identity=workspace_http
    db.add(ProjectMember(project_id='project',user_id='stranger',role='member'));db.commit()
    url=BASE+'/candidates/views';filters=dict(filterConditions=[c('planIds','equals','plan')],filterLogic='and')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        first=(await client.post(url,json=dict(name='同名视图',filters=filters))).json()['data']
        assert (await client.get(BASE+'/views')).json()['data']==[]
        assert (await client.post(BASE+'/views',json=dict(name='同名视图',filters={}))).status_code==200
        assert (await client.get(url,params={'category':'api'})).json()['data']==[]
        assert (await client.put(url+'/'+first['id'],json=dict(name='改名'))).json()['data']['filters']==filters
        for invalid in [None,{'mine':True},{'filterConditions':[c('result','equals','passed')]}]:
            assert (await client.put(url+'/'+first['id'],json=dict(name='非法',filters=invalid))).status_code==422
        identity['id']='stranger'
        assert (await client.get(url)).json()['data']==[]
        assert (await client.put(url+'/'+first['id'],json=dict(name='越权'))).status_code==404
        assert (await client.delete(url+'/'+first['id'])).status_code==404
        assert (await client.post(url,json=dict(name='我的只读视图',filters={}))).status_code==200
        identity['id']='owner'
        for i in range(9):assert (await client.post(url,json=dict(name=f'视图{i}',filters={}))).status_code==200
        assert (await client.post(url,json=dict(name='超限',filters={}))).status_code==409
        assert (await client.post(url,params={'category':'api'},json=dict(name='独立分类',filters={}))).status_code==200
        assert (await client.post(url,params={'category':'scenario'},json=dict(name='独立分类',filters={}))).status_code==200
        assert (await client.delete(url+'/'+first['id'])).status_code==200
        assert (await client.post(url,json=dict(name='补充',filters={}))).status_code==200
    assert db.query(PlanCaseSavedView).count()==14 and db.query(TaskQueue).count()==0
