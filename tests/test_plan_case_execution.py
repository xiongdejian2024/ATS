"""MS功能用例独立回填：权限、批量原子性、重复实例与冻结历史。"""
import uuid
import httpx
import pytest
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from models import TestCase as Case, TestPlan as Plan, Project, ProjectMember, PlanCaseRelation
from models.plan_workspace import PlanWorkspace
from models.plan_case_execution import PlanCaseExecution
from models.plan_orchestration import PlanRun
from models.task_queue import TaskQueue
from services.plan_tree import save_node
from services.plan_orchestration import start_plan_run, cancel_plan_run, advance_plan_runs
BASE = '/orchestration/plans/plan/case-workspace'

def body(rows, result='passed', **kwargs):
    return dict(requestId=str(uuid.uuid4()), selections=[dict(source=row['source'],id=row['associationId']) for row in rows], result=result, **kwargs)

@pytest.mark.asyncio
async def test_independent_result_history_replay_stats_and_frozen_run(workspace_http):
    db,app,identity=workspace_http
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        row=(await client.get(BASE)).json()['data']['items'][0]
        run=await start_plan_run(db,'plan','owner');await cancel_plan_run(db,run.id,'owner');await advance_plan_runs(db)
        frozen=dict(db.get(PlanRun,run.id).report)
        task_count=db.query(TaskQueue).count()
        payload=body([row],description='<p>软件检查通过</p>')
        response=await client.post(BASE+'/execute',json=payload)
        assert response.status_code==200,response.text
        assert (await client.post(BASE+'/execute',json=payload)).json()['data']['replayed']
        current=(await client.get(BASE)).json()['data']
        assert next(item for item in current['items'] if item['id']==row['id'])['result']=='passed'
        details=(await client.get(BASE+'/execution',params=dict(source=row['source'],associationId=row['associationId'],caseId=row['caseId']))).json()['data']
        assert details['total']==1 and details['history'][0]['description']=='<p>软件检查通过</p>'
        changed=dict(payload,result='failed')
        assert (await client.post(BASE+'/execute',json=changed)).status_code==409
        plan=(await client.get('/test-plans/plan')).json()['data']
        assert plan['executedCases']==2 and plan['caseStatusCounts']['pass']==1
        assert db.get(PlanRun,run.id).report==frozen and db.query(TaskQueue).count()==task_count
        assert (await client.post(BASE+'/execute',json=body([row],'blocked'))).status_code==200
        plan=(await client.get('/test-plans/plan')).json()['data']
        assert plan['caseStatusCounts']['blocked']==1 and plan['caseStatusCounts']['pass']==0
        # 后创建的整计划批次重置当前状态，但不删除独立历史。
        next_run=await start_plan_run(db,'plan','owner')
        assert next(item for item in (await client.get(BASE)).json()['data']['items'] if item['id']==row['id'])['result']=='pending'
        assert db.query(PlanCaseExecution).count()==2

@pytest.mark.asyncio
async def test_duplicate_tree_instances_batch_atomicity_unlink_keeps_history(workspace_http):
    db,app,identity=workspace_http
    case=db.get(Case,'case-2');case.type='functional';case.is_automated=False;db.commit()
    first=save_node(db,db.get(Plan,'plan'),dict(name='实例一',nodeType='case',category='functional',caseId=case.id))
    second=save_node(db,db.get(Plan,'plan'),dict(name='实例二',nodeType='case',category='functional',caseId=case.id));db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        rows=(await client.get(BASE)).json()['data']['items']
        invalid=body([rows[0]]);invalid['selections'].append(dict(source='node',id='other-project'))
        assert (await client.post(BASE+'/execute',json=invalid)).status_code==404
        assert db.query(PlanCaseExecution).count()==0
        duplicate=body([rows[0],rows[0]])
        assert (await client.post(BASE+'/execute',json=duplicate)).status_code==422
        assert (await client.post(BASE+'/execute',json=body([rows[0]],'failed'))).status_code==200
        statuses={item['associationId']:item['result'] for item in (await client.get(BASE)).json()['data']['items']}
        assert set(statuses.values())=={'pending','failed'}
        assert (await client.get(BASE,params={'result':'failed,pending'})).json()['data']['total']==2
        assert (await client.get(BASE,params={'result':'failed'})).json()['data']['total']==1
        payload=body(rows,'blocked',description='统一阻塞原因')
        assert (await client.post(BASE+'/execute',json=payload)).status_code==200
        assert {item['result'] for item in (await client.get(BASE)).json()['data']['items']}=={'blocked'}
        target=rows[0]
        assert (await client.post(BASE+'/batch',json=dict(action='unlink',selections=[dict(source=target['source'],id=target['associationId'])]))).status_code==200
        detail=(await client.get(BASE+'/execution',params=dict(source=target['source'],associationId=target['associationId'],caseId=target['caseId']))).json()['data']
        assert detail['detached'] and not detail['canExecute'] and detail['total']==2
        assert db.query(PlanCaseExecution).count()==3 and db.query(TaskQueue).count()==0

@pytest.mark.asyncio
async def test_readonly_archived_recycled_active_and_commit_failure(workspace_http,monkeypatch):
    db,app,identity=workspace_http
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        row=(await client.get(BASE)).json()['data']['items'][0];payload=body([row])
        identity['id']='stranger'
        db.add(ProjectMember(project_id='project',user_id='stranger',role='member'));db.commit()
        assert not (await client.get(BASE)).json()['data']['canExecute']
        assert (await client.post(BASE+'/execute',json=payload)).status_code==403
        identity['id']='owner'
        db.add(PlanWorkspace(plan_id='plan',archived=True));db.commit()
        assert (await client.post(BASE+'/execute',json=payload)).status_code==409
        db.get(PlanWorkspace,'plan').archived=False;db.commit()
        run=await start_plan_run(db,'plan','owner')
        assert (await client.post(BASE+'/execute',json=payload)).status_code==409
        await cancel_plan_run(db,run.id,'owner');await advance_plan_runs(db)
        from datetime import datetime
        db.get(Case,row['caseId']).deleted_at=datetime.now();db.commit()
        assert (await client.post(BASE+'/execute',json=payload)).status_code==409
        db.get(Case,row['caseId']).deleted_at=None;db.commit()
        old=db.get(PlanCaseRelation,row['associationId']).execution_status
        def failure(): raise RuntimeError('软件回归模拟提交失败')
        with monkeypatch.context() as patch:
            patch.setattr(db,'commit',failure)
            # 应用处理异常转500；验证同一事务没有结果或部分主状态残留。
            with pytest.raises(RuntimeError): await client.post(BASE+'/execute',json=payload)
        assert db.query(PlanCaseExecution).count()==0
        assert db.get(PlanCaseRelation,row['associationId']).execution_status==old

@pytest.mark.asyncio
async def test_step_validation_and_history_project_scope(workspace_http):
    db,app,identity=workspace_http
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        row=(await client.get(BASE)).json()['data']['items'][0]
        db.get(Case,row['caseId']).steps=[dict(action='检查',expected='通过')];db.get(Case,row['caseId']).case_edit_type='STEP';db.commit()
        assert (await client.post(BASE+'/execute',json=body([row],stepResults=[dict(index=1,result='passed')]))).status_code==422
        assert (await client.post(BASE+'/execute',json=body([row],stepResults=[dict(index=0,result='failed')]))).status_code==422
        assert (await client.post(BASE+'/execute',json=body([row],stepResults=[dict(index=0,result='passed',actual='正常')]))).status_code==200
        db.add(Project(id='other',name='另一项目',owner_id='owner'));db.add(Plan(id='other-plan',project_id='other',plan_number='OTHER',name='另一计划',owner_id='owner'));db.commit()
        response=await client.get(BASE.replace('/plan/','/other-plan/')+'/execution',params=dict(source=row['source'],associationId=row['associationId'],caseId=row['caseId']))
        assert response.status_code==404
        identity['id']='stranger'
        assert (await client.get(BASE+'/execution',params=dict(source=row['source'],associationId=row['associationId'],caseId=row['caseId']))).status_code==403
