"""原生范围执行软件验收：隔离库、消息替身，不连接台架。"""
from uuid import uuid4
import pytest
import httpx
from test_plan_native_workspace import native_workspace
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab, finish
from models import TestPlan as Plan, TestCase as Case, TestSuite as Suite, PlanCaseRelation, ProjectMember, Environment
from models.plan_workspace import PlanWorkspace
from models.plan_orchestration import PlanRun, PlanRunItem
from models.task_queue import TaskQueue
from models.case_governance import CaseVersion
from services.plan_tree import save_node
from services.plan_orchestration import advance_plan_runs, save_policy, build_report
from schemas.plan_orchestration import PlanPolicy
BASE='/orchestration/plans/plan/case-workspace'


def client(app): return httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test')
def body(category='api', **kwargs): return dict(category=category,requestId=str(uuid4()),**kwargs)
async def ids(http, category='api'):
    response=await http.get(BASE,params=dict(category=category));assert response.status_code==200,response.text
    return [r['id'] for r in response.json()['data']['items']]
async def execute(http, request): return await http.post(BASE+'/run-range',json=request)


@pytest.mark.asyncio
async def test_single_legacy_filters_suite_and_excludes_manual_and_scene(native_workspace):
    db,app,_=native_workspace
    db.get(Suite,'suite-0').case_ids=['case-0','case-1'];db.commit()
    async with client(app) as http:
        selected=await ids(http);response=await execute(http,body(selectIds=selected));assert response.status_code==200,response.text
        run=db.get(PlanRun,response.json()['data']['id'])
        assert len(run.case_snapshot)==1 and run.case_snapshot[0]['id']=='case-0'
        item=db.query(PlanRunItem).filter_by(run_id=run.id).one()
        assert item.suite_snapshot['caseIds']==['case-0'] and item.suite_snapshot['nodeId']==selected[0].split(':')[1]
        assert run.manual_results=={} and db.query(TaskQueue).count()==1
        rows=(await http.get(BASE,params={'category':'api'})).json()['data']['items'];assert rows[0]['runId']==run.id
        scene=(await http.get(BASE,params={'category':'scenario'})).json()['data']['items'];assert scene[0]['runId'] is None
    await advance_plan_runs(db)
    from api.v1.websocket import manager
    # plan_lab的消息替身实际接收冻结过滤范围。
    finish(db,item,'passed');await advance_plan_runs(db)
    assert build_report(db,run)['cases'][0]['associationId']==selected[0].split(':')[1]
    assert run.report['total']==1 and run.status=='completed'


@pytest.mark.asyncio
async def test_duplicate_instances_all_exclusion_versions_and_dispatch(native_workspace,plan_lab):
    db,app,_=native_workspace;_,sent=plan_lab
    plan=db.get(Plan,'plan')
    group=save_node(db,plan,dict(name='并行集',nodeType='point',category='api',config=dict(executionMode='parallel')))
    leaves=[save_node(db,plan,dict(name=f'实例{i}',nodeType='case',category='api',caseId='case-0',suiteId='suite-0',parentId=group.id)) for i in range(3)]
    db.commit()
    async with client(app) as http:
        all_ids=await ids(http);excluded=f'node:{leaves[1].id}:case-0'
        response=await execute(http,body(selectAll=True,excludeIds=[excluded],condition=dict(folder=group.id)));assert response.status_code==200,response.text
        run=db.get(PlanRun,response.json()['data']['id']);items=db.query(PlanRunItem).filter_by(run_id=run.id).all()
        assert {c['associationId'] for c in run.case_snapshot}=={leaves[0].id,leaves[2].id}
        assert len(items)==2 and len({i.execution_id for i in items})==2 and db.query(TaskQueue).count()==2
        assert len({c['versionId'] for c in run.case_snapshot})==1
        assert all(i.suite_snapshot['prerequisites']==[] for i in items)
    await advance_plan_runs(db)
    assert len(sent)==2 and all(message['case_ids']==['case-0'] for _,message in sent)
    finish(db,items[0],'passed');finish(db,items[1],'failed');await advance_plan_runs(db)
    assert run.report['total']==2 and {r['result'] for r in run.report['cases']}=={'passed','failed'}
    assert {r['associationId'] for r in run.report['cases']}=={leaves[0].id,leaves[2].id}


@pytest.mark.asyncio
async def test_serial_prunes_unselected_predecessors_and_inherits_environment(native_workspace,plan_lab):
    db,app,_=native_workspace;_,sent=plan_lab;plan=db.get(Plan,'plan')
    db.add(Environment(id='override',name='继承节点',is_online=True,max_concurrent_tasks=3));db.flush()
    group=save_node(db,plan,dict(name='串行集',nodeType='point',category='api',config=dict(environmentId='override',executionMode='serial')))
    leaves=[save_node(db,plan,dict(name=f'实例{i}',nodeType='case',category='api',caseId='case-0',suiteId='suite-0',parentId=group.id)) for i in range(3)]
    db.commit()
    async with client(app) as http:
        response=await execute(http,body(selectIds=[f'node:{n.id}:case-0' for n in leaves[1:]]));assert response.status_code==200,response.text
        run=db.get(PlanRun,response.json()['data']['id']);items=db.query(PlanRunItem).filter_by(run_id=run.id).order_by(PlanRunItem.sequence).all()
        assert items[0].suite_snapshot['prerequisites']==[] and items[1].suite_snapshot['prerequisites']==[leaves[1].id]
        assert [i.status for i in items]==['pending','waiting'] and all(i.environment_id=='override' for i in items)
        assert db.get(Suite,'suite-0').environment_id=='node'
        from services.suite_results import handle_run_result
        assert handle_run_result(db, 'override', dict(suite_id=items[0].suite_id, execution_id=items[0].execution_id, case_id='case-0', result='passed', duration='0.1s'))
        db.query(TaskQueue).filter_by(execution_id=items[0].execution_id).one().status='completed';db.commit()
        await advance_plan_runs(db)
        assert db.query(TaskQueue).count()==2 and items[1].status=='pending'
        assert sent==[] # 新节点无连接，任务排队而非虚报成功。


@pytest.mark.asyncio
async def test_retry_same_request_is_one_batch_and_mismatched_payload_rejected(native_workspace):
    db,app,_=native_workspace
    async with client(app) as http:
        request=body(selectIds=await ids(http));first=await execute(http,request);assert first.status_code==200,first.text
        second=await execute(http,request);assert second.status_code==200 and first.json()['data']['id']==second.json()['data']['id']
        changed=dict(request,selectIds=await ids(http,'scenario'),category='scenario');assert (await execute(http,changed)).status_code==409
        assert (await execute(http,body(selectIds=await ids(http)))).status_code==409
    assert db.query(PlanRun).count()==1 and db.query(PlanRunItem).count()==1 and db.query(TaskQueue).count()==1


@pytest.mark.asyncio
@pytest.mark.parametrize('failure',['missing-suite','ambiguous-suite','generic-command','disabled-env','recycled','active-task','archived'])
async def test_invalid_selection_rolls_back_everything(native_workspace,failure):
    db,app,_=native_workspace
    async with client(app) as http:
        selected=await ids(http)
        if failure=='missing-suite':db.get(Suite,'suite-0').case_ids=[]
        if failure=='ambiguous-suite':db.get(Suite,'suite-1').case_ids.append('case-0');db.get(Suite,'suite-1').case_ids=['case-1','case-0']
        if failure=='generic-command':db.get(Suite,'suite-0').execution_command='python execute_all.py'
        if failure=='disabled-env':db.get(Environment,'node').status=False
        if failure=='recycled':
            from utils.datetime_utils import beijing_now
            db.get(Case,'case-0').deleted_at=beijing_now()
        if failure=='active-task':db.add(TaskQueue(id='occupied',suite_id='suite-0',environment_id='node',executor_id='owner',execution_id='old',status='pending'))
        if failure=='archived':db.add(PlanWorkspace(plan_id='plan',archived=True))
        db.commit();response=await execute(http,body(selectIds=selected));assert response.status_code in (404,409),response.text
    assert db.query(PlanRun).count()==0 and db.query(PlanRunItem).count()==0 and db.query(CaseVersion).count()==0
    assert db.query(TaskQueue).count()==(1 if failure=='active-task' else 0)


@pytest.mark.asyncio
async def test_scene_scope_and_execute_permission_do_not_require_edit(native_workspace):
    db,app,identity=native_workspace
    member=ProjectMember(project_id='project',user_id='stranger',role='viewer')
    from models.role import ProjectPermission, Permission
    permission=Permission(id='scope-execute',name='范围执行',code='test_plan:execute',resource='test_plan',action='execute');db.add(permission);db.flush()
    grant=ProjectPermission(project_id='project',user_id='stranger',permission_id=permission.id,granted_by='owner')
    db.add(grant)
    db.add(member);db.commit();identity['id']='stranger'
    async with client(app) as http:
        selected=await ids(http,'scenario')
        preview=(await http.post(BASE+'/selection',json=dict(category='scenario',selectIds=selected))).json()['data']
        assert preview['canExecute'] and not preview['canModify']
        response=await execute(http,body('scenario',selectIds=selected));assert response.status_code==200,response.text
        assert response.json()['data']['report']['total']==1 and response.json()['data']['report']['cases'][0]['category']=='scenario'
        assert (await http.post(BASE+'/batch-range',json=dict(category='scenario',selectIds=selected,action='unlink'))).status_code==403
        db.delete(grant);db.commit()
        assert (await execute(http,body('scenario',selectIds=selected))).status_code==403


@pytest.mark.asyncio
async def test_enqueue_failure_rolls_back_versions_batch_and_queue(native_workspace,monkeypatch):
    db,app,_=native_workspace
    from services import plan_native_run
    original=plan_native_run._enqueue
    def fail(db,run,item):
        original(db,run,item)
        raise RuntimeError('隔离范围入队故障')
    monkeypatch.setattr(plan_native_run,'_enqueue',fail)
    async with client(app) as http:
        with pytest.raises(RuntimeError,match='隔离范围入队故障'):
            await execute(http,body(selectIds=await ids(http)))
    assert db.query(PlanRun).count()==db.query(PlanRunItem).count()==db.query(TaskQueue).count()==db.query(CaseVersion).count()==0

@pytest.mark.asyncio
async def test_later_whole_plan_batch_overrides_legacy_scope_result(native_workspace):
    db,app,_=native_workspace
    async with client(app) as http:
        response=await execute(http,body(selectIds=await ids(http)));assert response.status_code==200,response.text
        run=db.get(PlanRun,response.json()['data']['id']);item=db.query(PlanRunItem).filter_by(run_id=run.id).one()
        finish(db,item,'passed');await advance_plan_runs(db)
        assert (await http.get(BASE,params={'category':'api'})).json()['data']['items'][0]['nativeResult']=='SUCCESS'
        from services.plan_orchestration import start_plan_run
        later=await start_plan_run(db,'plan','owner')
        latest=(await http.get(BASE,params={'category':'api'})).json()['data']['items'][0]
        assert latest['runId']==later.id and latest['nativeResult']=='PENDING'
        assert run.status=='completed' and run.report['counts']['passed']==1
