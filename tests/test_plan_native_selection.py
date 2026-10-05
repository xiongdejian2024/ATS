"""原生关联实例跨页范围，使用隔离数据库，绝不创建执行队列。"""
import pytest
import httpx
from test_plan_native_workspace import native_workspace, c, frozen_run
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from models import TestCase as Case, TestPlan as Plan, PlanCaseRelation, TestSuite as Suite, Module, ProjectMember
from models.native_case import NativeCaseConfig
from models.plan_workspace import PlanWorkspace, PlanNode
from models.task_queue import TaskQueue
from services.plan_tree import save_node
from services import plan_case_workspace as service
BASE = '/orchestration/plans/plan/case-workspace'


def seed(db, count=24, category='api'):
    for i in range(count):
        case = Case(id=f'extra-{i}',project_id='project',case_code=f'RANGE-{i:04}',name=f'范围用例{i}',type=category,is_automated=True,priority='P1' if i%2 else 'P2',created_by='owner',steps=[])
        db.add(case);db.flush()
        db.add(NativeCaseConfig(case_id=case.id,state='PROCESSING' if category=='api' else 'UNDERWAY',api_definition_id='definition' if category=='api' else None,parameters={},updated_by='owner'))
        db.add(PlanCaseRelation(plan_id='plan',case_id=case.id,execution_order=i+2))
    db.commit()


def client(app): return httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test')
async def rows(http, **params):
    response=await http.get(BASE,params=dict(category='api',sort='caseCode',direction='asc',size=20,**params))
    assert response.status_code==200,response.text
    return response.json()['data']
async def preview(http, body):
    response=await http.post(BASE+'/selection',json=body)
    assert response.status_code==200,response.text
    return response.json()['data']
async def apply(http, body, action='unlink', **extra): return await http.post(BASE+'/batch-range',json=dict(body,action=action,**extra))


@pytest.mark.asyncio
async def test_explicit_two_pages_and_composite_identity_are_atomic(native_workspace):
    db,app,_=native_workspace;seed(db)
    async with client(app) as http:
        first=await rows(http);second=await rows(http,page=2)
        assert first['total']==first['selectableTotal']==25 and len(second['items'])==5
        selected=[first['items'][0]['id'],second['items'][0]['id']]
        body=dict(category='api',selectIds=selected)
        assert (await preview(http,body))['count']==2
        invalid=dict(body,selectIds=[selected[0],selected[1].rsplit(':',1)[0]+':wrong-case'])
        assert (await apply(http,invalid)).status_code==404
        assert (await rows(http))['total']==25
        response=await apply(http,body);assert response.status_code==200,response.text
        assert response.json()['data']['updated']==2 and (await rows(http))['total']==23
        assert (await apply(http,body)).status_code==404
    assert db.query(Case).count()==27 and db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_all_pages_exclusions_and_submit_reparse_changed_scope(native_workspace):
    db,app,_=native_workspace;seed(db)
    point=save_node(db,db.get(Plan,'plan'),dict(name='范围目标',nodeType='point',category='api'));db.commit()
    async with client(app) as http:
        first=await rows(http);second=await rows(http,page=2)
        excluded=[first['items'][0]['id'],second['items'][0]['id']]
        body=dict(category='api',selectAll=True,excludeIds=excluded,condition=dict(protocols='HTTP',folder='all'))
        summary=await preview(http,body);assert summary['count']==23 and summary['excludedCount']==2
        db.get(NativeCaseConfig,'extra-23').api_definition_id=None;db.commit()
        response=await apply(http,body,'move',collectionId=point.id);assert response.status_code==200,response.text
        assert response.json()['data']['updated']==22
        moved=await rows(http,folder=point.id);assert moved['total']==22
        assert not set(excluded)&{r['id'] for r in moved['items']}
        assert (await apply(http,dict(category='api',selectAll=True,condition=dict(protocols='')))).status_code==409
    assert db.query(Case).count()==27 and db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_filter_module_descendants_mine_and_frozen_instance_result(native_workspace):
    db,app,_=native_workspace;seed(db,3)
    db.add(Module(id='root',project_id='project',name='父模块'));db.flush()
    db.add(Module(id='child',project_id='project',name='子模块',parent_id='root'));db.flush()
    db.get(Case,'extra-0').module_id='root';db.get(Case,'extra-1').module_id='child';db.get(Case,'extra-2').created_by='stranger';db.commit()
    frozen_run(db,'scope-report',[('extra-0','extra-0','passed'),('extra-1','extra-1','failed')])
    async with client(app) as http:
        scope=dict(category='api',selectAll=True,condition=dict(tree_type='MODULE',folder='root',include_descendants=True))
        assert (await preview(http,scope))['count']==2
        scope['condition']['include_descendants']=False;assert (await preview(http,scope))['count']==1
        scope['condition']=dict(mine=True);assert (await preview(http,scope))['count']==3
        scope['condition']=dict(filters=dict(conditions=[c('result','equals','SUCCESS'),c('executorId','equals','CURRENT_USER')],logic='and'))
        assert (await preview(http,scope))['count']==1
        frozen_run(db,'scope-report-new',[('extra-0','extra-0','failed')],2)
        assert (await apply(http,scope)).status_code==409
        assert (await rows(http))['total']==4
    assert db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_duplicate_tree_instances_remain_distinct_and_grouped_rows_are_excluded(native_workspace):
    db,app,_=native_workspace;plan=db.get(Plan,'plan')
    point=save_node(db,plan,dict(name='目标',nodeType='point',category='api'))
    nodes=[save_node(db,plan,dict(name=f'实例{i}',nodeType='case',category='api',caseId='case-0',suiteId='suite-0')) for i in range(2)]
    grouped=save_node(db,plan,dict(name='整套',nodeType='suite',category='api',suiteId='suite-0'));db.commit()
    frozen_run(db,'different-results',[('case-0',nodes[0].id,'passed'),('case-0',nodes[1].id,'failed')])
    async with client(app) as http:
        data=await rows(http);assert data['total']==3 and data['selectableTotal']==2
        keys={r['associationId']:r['id'] for r in data['items']}
        assert (await http.post(BASE+'/selection',json=dict(category='api',selectIds=[keys[grouped.id]]))).status_code==404
        body=dict(category='api',selectAll=True,excludeIds=[keys[nodes[1].id]])
        assert (await preview(http,body))['count']==1
        response=await apply(http,body,'move',collectionId=point.id);assert response.status_code==200,response.text
        assert db.get(PlanNode,nodes[0].id).parent_id==point.id and db.get(PlanNode,nodes[1].id).parent_id is None
        response=await apply(http,dict(category='api',selectAll=True,condition=dict(result='SUCCESS')));assert response.status_code==200,response.text
        assert db.get(PlanNode,nodes[0].id) is None and db.get(PlanNode,nodes[1].id) and db.get(PlanNode,grouped.id)
        assert db.get(Case,'case-0') and db.get(PlanWorkspace,'plan').uses_tree
    assert db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_scenario_range_is_independent_and_target_category_is_checked(native_workspace):
    db,app,_=native_workspace;seed(db,22,'scenario')
    point=save_node(db,db.get(Plan,'plan'),dict(name='错误目标分类',nodeType='point',category='api'));db.commit()
    async with client(app) as http:
        body=dict(category='scenario',selectAll=True,condition=dict(filters=dict(conditions=[c('nativeState','equals','UNDERWAY')],logic='and')))
        assert (await preview(http,body))['count']==23
        assert (await apply(http,body,'move',collectionId=point.id)).status_code==422
        response=await apply(http,body);assert response.status_code==200,response.text
        assert response.json()['data']['updated']==23 and (await rows(http))['total']==1
    assert db.query(Case).count()==25 and db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_more_than_old_500_limit_and_10000_boundary_no_truncation(native_workspace):
    db,app,_=native_workspace;seed(db,500)
    async with client(app) as http:
        body=dict(category='api',selectAll=True)
        assert (await preview(http,body))['count']==501
        response=await apply(http,body);assert response.status_code==200,response.text
        assert response.json()['data']['updated']==501
    assert db.query(Case).count()==503 and db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_limit_uses_actual_selected_count_after_exclusions(native_workspace,monkeypatch):
    db,app,_=native_workspace
    originals=service.listing
    items=[dict(id=f'legacy:r{i}:c{i}',grouped=False) for i in range(10001)]
    monkeypatch.setattr(service,'listing',lambda *args,**kwargs:dict(items=items))
    async with client(app) as http:
        assert (await http.post(BASE+'/selection',json=dict(category='api',selectAll=True))).status_code==422
        summary=await preview(http,dict(category='api',selectAll=True,excludeIds=[items[0]['id']]))
        assert summary['count']==10000 and summary['eligibleCount']==10001 and summary['excludedCount']==1
    monkeypatch.setattr(service,'listing',originals)
    assert db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_permissions_archive_and_active_suite_rechecked_on_submit(native_workspace):
    db,app,identity=native_workspace
    async with client(app) as http:
        body=dict(category='api',selectAll=True)
        assert (await preview(http,body))['canModify']
        db.add(PlanWorkspace(plan_id='plan',archived=True));db.commit()
        assert not (await preview(http,body))['canModify']
        assert (await apply(http,body)).status_code==409
        db.get(PlanWorkspace,'plan').archived=False;db.commit()
        db.add(TaskQueue(id='active-sample',suite_id='suite-0',environment_id='node',execution_id='sample-only',executor_id='owner',status='running'));db.commit()
        assert (await apply(http,body)).status_code==409
        assert (await rows(http))['total']==1 and db.get(Suite,'suite-0').case_ids==['case-0']
        db.delete(db.get(TaskQueue,'active-sample'));db.commit()
        identity['id']='stranger';assert (await http.post(BASE+'/selection',json=body)).status_code==403
        db.add(ProjectMember(project_id='project',user_id='stranger',role='tester'));db.commit()
        assert not (await preview(http,body))['canModify'] and (await apply(http,body)).status_code==403
    assert db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_mid_batch_failure_rolls_back_all_instances(native_workspace,monkeypatch):
    db,app,_=native_workspace;plan=db.get(Plan,'plan')
    point=save_node(db,plan,dict(name='目标',nodeType='point',category='api'))
    nodes=[save_node(db,plan,dict(name=f'实例{i}',nodeType='case',category='api',caseId='case-0',suiteId='suite-0')) for i in range(2)];db.commit()
    original=service.save_node;calls=[]
    def fail_second(*args,**kwargs):
        calls.append(1)
        if len(calls)==2:raise ValueError('隔离模拟第二实例写入失败')
        return original(*args,**kwargs)
    monkeypatch.setattr(service,'save_node',fail_second)
    async with client(app) as http:
        with pytest.raises(ValueError,match='第二实例'):
            await apply(http,dict(category='api',selectAll=True),'move',collectionId=point.id)
        assert all(db.get(PlanNode,n.id).parent_id is None for n in nodes)
    assert db.query(TaskQueue).count()==0


@pytest.mark.asyncio
@pytest.mark.parametrize('body',[
    dict(category='functional',selectAll=True), dict(category='api',selectAll='true'),
    dict(category='api',selectIds=['not-composite']), dict(category='api',selectIds=['legacy:a:b']*2),
    dict(category='api',selectAll=True,selectIds=['legacy:a:b']), dict(category='api',selectIds=['legacy:a:b'],excludeIds=['legacy:c:d']),
    dict(category='api',selectIds=['legacy:a:b'],condition=dict(search='x')),
    dict(category='api',selectAll=True,condition=dict(page=2)),dict(category='api',selectAll=True,condition=dict(user_id='stranger')),
    dict(category='scenario',selectAll=True,condition=dict(protocols='HTTP')),
    dict(category='scenario',selectAll=True,condition=dict(filters=dict(conditions=[c('protocol','equals','HTTP')],logic='and'))),
])
async def test_invalid_scope_schema_is_rejected_without_changes(native_workspace,body):
    db,app,_=native_workspace
    async with client(app) as http:
        assert (await http.post(BASE+'/selection',json=body)).status_code==422
        assert (await apply(http,body)).status_code==422
    assert db.query(PlanCaseRelation).count()==2 and db.query(TaskQueue).count()==0
