"""独立详情分类、旧关联、缺陷事务和项目权限：仅隔离数据库。"""
import httpx
import pytest
from test_plan_orchestration import plan_lab
from test_plan_workspace import workspace_http
from models import Project, ProjectMember, TestCase as Case
from models.case_features import CaseIssue, CaseIssueLink
from models.task_queue import TaskQueue
from services.plan_tree import save_node


@pytest.mark.asyncio
async def test_legacy_detail_project_scope_and_readonly_capabilities(workspace_http):
    db, app, identity = workspace_http
    db.add(Project(id='other', name='另一个项目', owner_id='owner'))
    db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        response = await client.get('/test-plans/plan', params={'project_id':'project'})
        assert response.status_code == 200, response.text
        data = response.json()['data']
        assert data['categoryCounts'] == dict(functional=2, api=0, scenario=0)
        assert all(data['capabilities'].values())
        assert data['testCases'][0]['type'] == 'functional'
        cases = await client.get('/test-plans/plan/cases')
        assert cases.status_code == 200, cases.text
        assert len(cases.json()['data']) == 2
        assert (await client.get('/test-plans/plan',params={'project_id':'other'})).status_code == 404
        identity['id']='stranger'
        assert (await client.get('/test-plans/plan')).status_code == 403
        db.add(ProjectMember(project_id='project',user_id='stranger',role='member'));db.commit()
        data=(await client.get('/test-plans/plan')).json()['data']
        assert not any(data['capabilities'].values())
        assert (await client.put('/orchestration/plans/plan/follow',json={'followed':True})).status_code == 200
        assert (await client.get('/orchestration/plans/plan/workspace')).json()['data']['followed']
        assert (await client.get('/orchestration/plans/plan/defects')).json()['data']['canEdit'] is False
        assert (await client.post('/orchestration/plans/plan/defects',json={'caseId':'case-0','title':'只读禁止'})).status_code == 403
    assert db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_category_instances_defect_scope_and_rejected_write_are_atomic(workspace_http):
    from models import TestPlan as Plan
    db,app,identity=workspace_http
    plan=db.get(Plan,'plan')
    point=save_node(db,plan,dict(name='测试点',nodeType='point',category='functional'))
    db.flush()
    for data in (dict(name='功能实例',nodeType='case',category='functional',caseId='case-2'),
                 dict(name='API 一',nodeType='case',category='api',caseId='case-0',suiteId='suite-0'),
                 dict(name='API 二',nodeType='case',category='api',caseId='case-0',suiteId='suite-0'),
                 dict(name='场景',nodeType='suite',category='scenario',suiteId='suite-1')):
        save_node(db,plan,dict(data,parentId=point.id))
    db.add(Case(id='unrelated',project_id='project',name='不属于计划',case_code='UNRELATED',type='functional',steps=[],created_by='owner'))
    db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        data=(await client.get('/test-plans/plan')).json()['data']
        assert data['usesTestPointTree'] and data['categoryCounts']==dict(functional=1,api=2,scenario=1)
        assert data['totalCases']==4
        base='/orchestration/plans/plan/defects'
        for payload in (dict(caseId='unrelated',title='不应创建'),dict(caseId='case-2',title='   ')):
            assert (await client.post(base,json=payload)).status_code==422
        assert db.query(CaseIssue).count()==db.query(CaseIssueLink).count()==0
        response=await client.post(base,json=dict(caseId='case-2',title='  隔离缺陷  ',description='详情与关联原子保存'))
        assert response.status_code==200,response.text
        issue_id=response.json()['data']['id']
        listing=(await client.get(base)).json()['data']
        assert listing['canEdit'] and len(listing['items'])==1
        assert listing['items'][0]['id']==issue_id and listing['items'][0]['title']=='隔离缺陷'
        assert listing['items'][0]['cases'][0]['id']=='case-2'
        assert {case['id'] for case in listing['cases']}=={'case-0','case-1','case-2'}
        identity['id']='stranger'
        assert (await client.get(base)).status_code==403
    assert db.query(TaskQueue).count()==0
