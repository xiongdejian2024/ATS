"""测试点编排与协作，全部使用隔离软件环境。"""
import base64
from datetime import datetime, timedelta, timezone
import httpx
import pytest
from fastapi import HTTPException
from test_plan_orchestration import plan_lab, finish
from test_plan_workspace import workspace_http
from models import TestPlan as Plan, TestCase as Case, Environment, User, Project
from models.plan_workspace import PlanNode, PlanRunAttachment, PlanReportShare
from models.plan_orchestration import PlanRunItem, PlanRun
from models.task_queue import TaskQueue
from models.case_features import CaseIssue
from services.plan_tree import save_node, effective_config
from services.plan_orchestration import start_plan_run, release_plan_run, advance_plan_runs, build_report, record_manual_result, save_policy, cancel_plan_run
from schemas.plan_orchestration import PlanPolicy, ManualResultInput


def node(db, **kwargs):
    data=dict(name='测试节点',nodeType='case',category='functional',caseId='case-2')
    data.update(kwargs)
    row=save_node(db,db.get(Plan,'plan'),data)
    db.commit()
    return row


@pytest.mark.asyncio
async def test_duplicate_manual_instances_and_full_copy(plan_lab):
    from services.test_plan_service import TestPlanService
    db,sent=plan_lab
    first=node(db,name='白天步骤')
    second=node(db,name='夜间步骤')
    run=await start_plan_run(db,'plan','owner')
    assert len(run.case_snapshot)==2 and build_report(db,run)['total']==2
    record_manual_result(db,run.id,first.id,ManualResultInput(result='passed'),'owner')
    assert build_report(db,run)['counts']['pending']==1
    record_manual_result(db,run.id,second.id,ManualResultInput(result='failed'),'owner')
    await advance_plan_runs(db)
    assert run.status=='failed' and run.report['counts']['passed']==1
    clone=TestPlanService.clone_plan(db,'plan','project','owner')
    assert db.query(PlanNode).filter_by(plan_id=clone.id).count()==2
    assert db.query(PlanRun).filter_by(plan_id=clone.id).count()==0
    assert not sent


@pytest.mark.asyncio
async def test_nested_parallel_then_serial_and_repeated_suite_instances(plan_lab):
    db,sent=plan_lab
    root=node(db,name='并行检查',nodeType='point',caseId=None,config={'executionMode':'parallel','environmentId':'node'})
    a=node(db,name='接口一',category='api',caseId='case-0',suiteId='suite-0',parentId=root.id)
    b=node(db,name='接口二同用例重复',category='api',caseId='case-0',suiteId='suite-0',parentId=root.id)
    c=node(db,name='收尾场景',nodeType='suite',caseId=None,category='scenario',suiteId='suite-1',position=1)
    run=await start_plan_run(db,'plan','owner')
    items=db.query(PlanRunItem).filter_by(run_id=run.id).order_by(PlanRunItem.sequence).all()
    assert [item.status for item in items]==['pending','pending','waiting']
    await advance_plan_runs(db)
    assert len(sent)==2 and sent[0][1]['execution_id']!=sent[1][1]['execution_id']
    finish(db,items[0]);await advance_plan_runs(db)
    assert len(sent)==2
    finish(db,items[1]);await advance_plan_runs(db)
    assert len(sent)==3
    finish(db,items[2]);await advance_plan_runs(db)
    assert run.status=='completed' and run.report['total']==3
    assert {row['associationId'] for row in run.report['cases']}=={a.id,b.id,c.id}


@pytest.mark.asyncio
async def test_resource_pool_switch_and_automatic_result_updates_functional(plan_lab,monkeypatch):
    from api.v1.websocket import manager
    db,sent=plan_lab
    db.add(Environment(id='spare',name='备用软件节点',is_online=True,max_concurrent_tasks=1));db.commit()
    point=node(db,nodeType='point',caseId=None,config={'resourcePool':['node','spare']})
    manual=node(db,parentId=point.id,name='功能校验')
    auto=node(db,parentId=point.id,name='API自动校验',category='api',caseId='case-0',suiteId='suite-0',linkedFunctionalId=manual.id)
    assert effective_config(db,auto)['resourcePool']==['node','spare']
    run=await start_plan_run(db,'plan','owner')
    monkeypatch.setattr(manager,'active_connections',{'spare':object()})
    await advance_plan_runs(db)
    assert len(sent)==1 and sent[0][0]=='spare'
    item=db.query(PlanRunItem).filter_by(run_id=run.id).one()
    assert item.environment_id=='spare'
    from services.suite_results import handle_run_result
    assert handle_run_result(db,'spare',dict(suite_id=item.suite_id,execution_id=item.execution_id,case_id='case-0',result='passed'))
    db.query(TaskQueue).filter_by(execution_id=item.execution_id).update({'status':'completed'});db.commit()
    await advance_plan_runs(db)
    assert run.status=='completed' and run.report['counts']['passed']==2
    assert next(row for row in run.report['cases'] if row['associationId']==manual.id)['linkedAutomation']


@pytest.mark.asyncio
async def test_deferred_group_batch_freezes_and_release_enqueues_once(plan_lab):
    db,sent=plan_lab
    run=await start_plan_run(db,'plan','owner',defer=True)
    assert run.status=='group_waiting' and db.query(TaskQueue).count()==0
    await advance_plan_runs(db)
    assert not sent
    with pytest.raises(ValueError,match='已有执行'):
        await start_plan_run(db,'plan','owner')
    assert release_plan_run(db,run)
    assert not release_plan_run(db,run)
    db.commit();await advance_plan_runs(db)
    assert len(sent)==1


def test_tree_validation_cross_project_cycle_and_assignment(plan_lab):
    db,sent=plan_lab
    first=node(db,nodeType='point',caseId=None)
    child=node(db,nodeType='point',caseId=None,parentId=first.id)
    with pytest.raises(HTTPException,match='循环'):
        save_node(db,db.get(Plan,'plan'),{'parentId':child.id},first)
    db.rollback()
    with pytest.raises(HTTPException,match='自动化'):
        node(db,category='api')
    db.rollback()
    db.add(User(id='outside',username='外部人员',email='out@example.test',password_hash='无效'));db.commit()
    with pytest.raises(HTTPException):
        node(db,assignedTo='outside')


@pytest.mark.asyncio
async def test_steps_evidence_defects_comments_pdf_summary_share(workspace_http):
    db,app,identity=workspace_http
    db.get(Case,'case-2').steps=[{'action':'检查界面','expected':'正常显示'}]
    db.add(CaseIssue(id='defect',project_id='project',kind='defect',title='显示异常',created_by='owner',updated_by='owner'));db.commit()
    association=node(db,name='手工界面检查')
    run=await start_plan_run(db,'plan','owner')
    base=f'/orchestration/runs/{run.id}'
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        attach=await client.post(f'{base}/cases/{association.id}/attachments',json={'name':'证据.txt','contentBase64':base64.b64encode('实际证据'.encode()).decode()})
        assert attach.status_code==200,attach.text
        attachment=attach.json()['data']['id']
        assert (await client.get(f'/orchestration/attachments/{attachment}')).content=='实际证据'.encode()
        assert (await client.post(f'{base}/cases/{association.id}/comments',json={'content':'等待修复后复测'})).status_code==200
        steps=[{'index':0,'result':'failed','actual':'未显示','defectIds':['defect'],'attachments':[attachment]}]
        result=await client.put(f'{base}/cases/{association.id}/result',json={'result':'passed','stepResults':steps})
        assert result.status_code==400
        result=await client.put(f'{base}/cases/{association.id}/result',json={'result':'failed','stepResults':steps,'notes':'发现缺陷'})
        assert result.status_code==200,result.text
        await advance_plan_runs(db)
        assert run.status=='failed'
        await client.put(f'{base}/summary',json={'conclusion':'不通过','risk':'界面缺陷','notes':'软件验证'})
        report=(await client.get(f'{base}/report')).json()['data']
        assert report['report']['cases'][0]['stepResults'][0]['defectIds']==['defect']
        assert report['report']['categories']['functional']['counts']['failed']==1
        pdf=await client.get(f'{base}/pdf')
        assert pdf.status_code==200 and pdf.content.startswith(b'%PDF-'),pdf.text[:200]
        shared=await client.post(f'{base}/shares',json={'expiresHours':1})
        token=shared.json()['data']['token']; share_id=shared.json()['data']['id']
        identity['id']='stranger'
        assert (await client.get(f'{base}/report')).status_code==403
        assert (await client.get(f'/orchestration/attachments/{attachment}')).status_code==403
        public=await client.get(f'/orchestration/shared/{token}')
        assert public.status_code==200 and 'configSnapshot' not in public.json()['data']
        db.get(PlanReportShare,share_id).expires_at=datetime.now(timezone.utc).replace(tzinfo=None)-timedelta(seconds=1);db.commit()
        assert (await client.get(f'/orchestration/shared/{token}/pdf')).status_code==404


@pytest.mark.asyncio
async def test_manual_dependencies_progress_and_failure_stop(plan_lab):
    db,sent=plan_lab
    first=node(db,name='第一步')
    second=node(db,name='第二步',position=1)
    save_policy(db,'plan',PlanPolicy(stopOnFailure=True))
    run=await start_plan_run(db,'plan','owner')
    with pytest.raises(ValueError,match='前序'):
        record_manual_result(db,run.id,second.id,ManualResultInput(result='passed'),'owner')
    record_manual_result(db,run.id,first.id,ManualResultInput(result='pending',notes='正在检查'),'owner')
    assert build_report(db,run)['counts']['pending']==2
    record_manual_result(db,run.id,first.id,ManualResultInput(result='failed'),'owner')
    await advance_plan_runs(db)
    assert run.status=='failed' and run.report['counts']['skipped']==1 and not sent


@pytest.mark.asyncio
async def test_group_complete_copy_and_active_delete_protection(workspace_http):
    from models.plan_orchestration import PlanGroup,PlanSettings
    from models.plan_group_execution import PlanGroupPolicy,PlanGroupRun
    from models.plan_workspace import PlanGroupWorkspace,PlanModule
    db,app,identity=workspace_http
    db.add(PlanGroup(id='group',project_id='project',name='发布组'))
    db.add(PlanModule(id='module',project_id='project',name='版本一'));db.flush()
    db.add(PlanSettings(plan_id='plan',group_id='group',suite_order=['suite-0','suite-1']))
    db.add(PlanGroupPolicy(group_id='group',execution_mode='parallel',stop_on_failure=True,pass_threshold=80,plan_order=['plan']))
    db.add(PlanGroupWorkspace(group_id='group',module_id='module',tags=['回归'],archived=False));db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        response=await client.post('/orchestration/groups/group/clone')
        assert response.status_code==200,response.text
        group_id=response.json()['data']['id']
        copied=db.query(PlanSettings).filter_by(group_id=group_id).one()
        assert copied.plan_id!='plan'
        policy=db.get(PlanGroupPolicy,group_id)
        assert policy.plan_order==[copied.plan_id] and policy.execution_mode=='parallel'
        assert db.get(PlanGroupWorkspace,group_id).tags==['回归']
        db.add(PlanGroupRun(id='group-run',group_id='group',active_group_id='group',project_id='project',group_name='发布组',executor_id='owner',config_snapshot={}));db.commit()
        assert (await client.delete('/orchestration/groups/group')).status_code==409
        assert (await client.put('/orchestration/groups/group',json={'name':'发布组','archived':True})).status_code==409


@pytest.mark.asyncio
async def test_assigned_project_member_can_fill_only_assigned_instance(workspace_http):
    from models import ProjectMember
    db,app,identity=workspace_http
    db.add(ProjectMember(project_id='project',user_id='stranger',role='member'));db.commit()
    assigned=node(db,name='分配给成员',assignedTo='stranger')
    other=node(db,name='未分配',position=1)
    run=await start_plan_run(db,'plan','owner')
    identity['id']='stranger'
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        response=await client.put(f'/orchestration/runs/{run.id}/cases/{assigned.id}/result',json={'result':'passed'})
        assert response.status_code==200,response.text
        assert (await client.put(f'/orchestration/runs/{run.id}/cases/{other.id}/result',json={'result':'passed'})).status_code==403
        assert (await client.post(f'/orchestration/runs/{run.id}/cases/{assigned.id}/comments',json={'content':'成员执行完成'})).status_code==200


@pytest.mark.asyncio
async def test_empty_resource_pool_preserves_explicit_and_inherited_environment(plan_lab):
    from services.plan_tree import compile_tree
    db, sent = plan_lab
    db.add(Environment(id="spare", name="继承验证软件节点", is_online=True, max_concurrent_tasks=1)); db.commit()
    parent = node(db, nodeType="point", caseId=None, category="api", config={"executionMode": "parallel", "environmentId": "spare", "resourcePool": []})
    child = node(db, nodeType="point", caseId=None, category="api", parentId=parent.id, config={"executionMode": None, "environmentId": None, "resourcePool": []})
    auto = node(db, category="api", caseId="case-0", suiteId="suite-0", parentId=child.id)
    assert effective_config(db, child) == {"executionMode": "parallel", "environmentId": "spare"}
    assert effective_config(db, auto)["environmentId"] == "spare"
    compiled = compile_tree(db, db.get(Plan, "plan"), {"executionMode": "serial"})
    assert compiled[0]["suite"].environment_id == "spare"
    run = await start_plan_run(db, "plan", "owner")
    assert db.query(PlanRunItem).filter_by(run_id=run.id).one().environment_id == "spare"
    assert not sent
    save_node(db, db.get(Plan, "plan"), {"config": {"environmentId": None, "resourcePool": ["node"]}}, child); db.commit()
    assert effective_config(db, auto) == {"executionMode": "parallel", "resourcePool": ["node"]}
    save_node(db, db.get(Plan, "plan"), {"config": {}}, child); db.commit()
    assert effective_config(db, auto)["environmentId"] == "spare"
    # 已创建批次继续采用原配置快照，不跟随修改后的测试集。
    assert db.query(PlanRunItem).filter_by(run_id=run.id).one().environment_id == "spare"


@pytest.mark.parametrize("config", [{"environmentId": ["node"]}, {"resourcePool": "node"}, {"resourcePool": ["node", "node"]}, {"resourcePool": [False]}, {"resourcePool": ""}])
def test_invalid_node_environment_config_rejected_before_database_lookup(plan_lab, config):
    db, sent = plan_lab
    with pytest.raises(HTTPException) as caught:
        node(db, nodeType="point", caseId=None, config=config)
    assert caught.value.status_code == 422
    db.rollback()
    assert db.query(PlanNode).count() == 0 and not sent
