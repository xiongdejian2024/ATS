"""计划工作区隔离验收，不连接台架或生产库。"""
from datetime import date
import pytest
import httpx
from fastapi import FastAPI
from test_plan_orchestration import plan_lab
from database import get_db
from models import User, TestPlan as Plan, TestCase as Case, TestSuite as Suite
from models.plan_workspace import PlanModule, PlanWorkspace, PlanFollow
from models.plan_orchestration import PlanSettings
from services.test_plan_service import TestPlanService
from services.plan_orchestration import start_plan_run, advance_plan_runs, build_report
from services.plan_workspace import update_metadata
from api.deps import get_current_user


@pytest.fixture
def workspace_http(plan_lab):
    from api.v1.test_plans import router as plans
    from api.v1.plan_orchestration import router as orchestration
    from api.v1.test_suites import router as suites
    db, sent = plan_lab
    db.add(User(id="stranger", username="项目外用户", email="stranger@example.test", password_hash="隔离测试"))
    db.commit()
    app = FastAPI()
    app.include_router(plans, prefix="/test-plans")
    app.include_router(orchestration, prefix="/orchestration")
    app.include_router(suites, prefix="/test-plans")
    identity = {"id": "owner"}
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user] = lambda: db.get(User, identity["id"])
    return db, app, identity


@pytest.mark.asyncio
async def test_module_hierarchy_metadata_follow_batch_and_dates(workspace_http):
    db, app, identity = workspace_http
    plan = db.get(Plan, "plan")
    plan.start_date, plan.end_date = date(2026, 10, 2), date(2026, 10, 8)
    db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        root = (await client.post('/orchestration/projects/project/modules',json={"name":"发布"})).json()['data']['id']
        child = (await client.post('/orchestration/projects/project/modules',json={"name":"回归","parentId":root})).json()['data']['id']
        assert (await client.put(f'/orchestration/modules/{root}',json={"parentId":child})).status_code == 400
        assert (await client.delete(f'/orchestration/modules/{root}')).status_code == 409
        assert (await client.put('/orchestration/plans/plan/workspace',json={"moduleId":child,"tags":["回归","发布"]})).status_code == 200
        await client.put('/orchestration/plans/plan/follow',json={"followed":True})
        response = await client.get('/test-plans',params={"project_id":"project","module_id":child,"tag":"发布","followed":True,"start_date":"2026-10-07","end_date":"2026-10-10"})
        assert response.status_code == 200, response.text
        assert response.json()['data']['total'] == 1 and response.json()['data']['items'][0]['followed']
        assert (await client.get('/test-plans',params={"project_id":"project","start_date":"2026-10-09"})).json()['data']['total'] == 0
        assert (await client.get('/test-plans',params={"project_id":"project","start_date":"invalid"})).status_code == 422
        response = await client.post('/orchestration/projects/project/plans/batch',json={"planIds":["plan"],"changes":{"archived":True}})
        assert response.status_code == 200
        assert (await client.get('/test-plans',params={"project_id":"project"})).json()['data']['total'] == 0
        assert (await client.get('/test-plans',params={"project_id":"project","archived":True})).json()['data']['total'] == 1
        with pytest.raises(ValueError, match="归档"):
            await start_plan_run(db,"plan","owner")
        identity['id']='stranger'
        assert (await client.put('/orchestration/plans/plan/follow',json={"followed":True})).status_code == 403
        assert (await client.post('/orchestration/projects/project/plans/batch',json={"planIds":["plan"],"changes":{"archived":False}})).status_code == 403


def test_complete_clone_copies_suites_policy_metadata_without_results(plan_lab):
    db, sent = plan_lab
    db.get(Plan,"plan").environment_id='node'
    db.add(PlanSettings(plan_id='plan',execution_mode='parallel',stop_on_failure=True,pass_threshold=80,suite_order=['suite-1','suite-0']))
    db.add(PlanWorkspace(plan_id='plan',tags=['发布'],archived=True))
    db.add(PlanFollow(plan_id='plan',user_id='owner'))
    db.commit()
    clone=TestPlanService.clone_plan(db,'plan','project','owner')
    assert clone.environment_id=='node' and clone.status=='not_started'
    suites=db.query(Suite).filter_by(plan_id=clone.id).all()
    assert len(suites)==2 and {s.name for s in suites}=={'测试套 0','测试套 1'}
    assert all(s.status=='pending' for s in suites)
    policy=db.get(PlanSettings,clone.id)
    assert policy.execution_mode=='parallel' and policy.pass_threshold==80
    assert db.get(Suite,policy.suite_order[0]).name=='测试套 1'
    assert db.get(PlanWorkspace,clone.id).tags==['发布'] and not db.get(PlanWorkspace,clone.id).archived
    assert db.query(PlanFollow).filter_by(plan_id=clone.id).count()==0


@pytest.mark.asyncio
async def test_case_snapshot_steps_and_code_are_frozen_and_recycle_excluded(plan_lab):
    db,sent=plan_lab
    case=db.get(Case,'case-0');case.precondition='前置条件';case.steps=[{'action':'打开界面','expected':'显示首页'}]
    db.commit()
    run=await start_plan_run(db,'plan','owner')
    case.steps=[{'action':'之后修改','expected':'新值'}];case.case_code='CHANGED'
    db.commit()
    await advance_plan_runs(db)
    assert sent[0][1]['case_codes']==['CODE-0']
    row=build_report(db,run)['cases'][0]
    assert row['snapshot']['steps']==[{'action':'打开界面','expected':'显示首页'}]
    assert run.case_snapshot[0]['versionId']


@pytest.mark.asyncio
async def test_all_suite_endpoints_enforce_project_access(workspace_http):
    db,app,identity=workspace_http
    identity['id']='stranger'
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        for path in ['/test-plans/plan/suites','/test-plans/suites/suite-0','/test-plans/suites/suite-0/executions','/test-plans/suites/suite-0/logs','/test-plans/suites/suite-0/suite-executions']:
            response=await client.get(path)
            assert response.status_code==403,(path,response.text)
        for path in ['/test-plans/suites/suite-0/execute','/test-plans/suites/suite-0/cancel']:
            response=await client.post(path,json={})
            assert response.status_code==403,(path,response.text)
        assert (await client.delete('/test-plans/suites/suite-0')).status_code==403


@pytest.mark.asyncio
async def test_navigation_module_filter_includes_descendants_and_group_location(workspace_http):
    """左树模块范围与组成员位置一致，仍保留旧的精确模块过滤语义。"""
    from models.plan_orchestration import PlanGroup
    from models.plan_workspace import PlanGroupWorkspace
    db,app,identity=workspace_http
    db.add(PlanModule(id='parent',project_id='project',name='父模块'))
    db.flush()
    db.add(PlanModule(id='child',project_id='project',name='子模块',parent_id='parent'))
    db.add(PlanGroup(id='group',project_id='project',name='计划组'))
    db.flush()
    db.add(PlanGroupWorkspace(group_id='group',module_id='child'))
    db.add(PlanSettings(plan_id='plan',group_id='group'))
    # 组内计划自身模块为空，导航应遵循组所在模块。
    db.add(PlanWorkspace(plan_id='plan',module_id=None))
    db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        params={'project_id':'project','module_id':'parent','include_descendants':True}
        response=await client.get('/test-plans',params=params)
        assert response.status_code==200,response.text
        assert response.json()['data']['total']==1
        params['group_id']='group'
        assert (await client.get('/test-plans',params=params)).json()['data']['total']==1
        assert (await client.get('/test-plans',params={'project_id':'project','module_id':'parent'})).json()['data']['total']==0
        params['module_id']='outside'
        assert (await client.get('/test-plans',params=params)).json()['data']['total']==0
