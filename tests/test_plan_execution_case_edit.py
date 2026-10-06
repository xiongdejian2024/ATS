"""执行页主用例编辑：来源授权、历史冻结和脱离/归档边界，零节点任务。"""
from copy import deepcopy
from datetime import datetime
from uuid import uuid4
import httpx
import pytest
from api.v1.test_cases import router as cases
from models import TestCase as Case, ProjectMember
from models.case_governance import CaseVersion
from models.plan_case_execution import PlanCaseExecution
from models.plan_workspace import PlanWorkspace
from models.task_queue import TaskQueue
from test_plan_candidate_projects import cross
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab

BASE = '/orchestration/plans/plan/case-workspace'


def query(row):
    return dict(source=row['source'], associationId=row['associationId'], caseId=row['caseId'])


@pytest.mark.asyncio
async def test_source_edit_permission_is_independent_and_revoked_write_fails(cross):
    db, app, identity = cross
    app.include_router(cases, prefix='/test-cases')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        assert (await client.post(BASE+'/associate', json=dict(projectId='source',caseIds=['foreign-1']))).status_code == 200
        row = next(r for r in (await client.get(BASE)).json()['data']['items'] if r['caseId']=='foreign-1')
        data = (await client.get(BASE+'/execution', params=query(row))).json()['data']
        assert data['canExecute'] and data['canReadCase'] and not data['canEditCase']
        assert (await client.put('/test-cases/foreign-1',json={'name':'不应更新'})).status_code == 403
        member = db.query(ProjectMember).filter_by(project_id='source',user_id='owner').one()
        member.role='maintainer';db.commit()
        data = (await client.get(BASE+'/execution', params=query(row))).json()['data']
        assert data['canEditCase'] and data['entry']['projectId']=='source'
        assert (await client.get('/test-cases/foreign-1',params={'project_id':'source'})).status_code == 200
        assert (await client.get('/test-cases/foreign-1',params={'project_id':'project'})).status_code == 404
        # 已取得可编辑标记后撤权，原写接口仍拒绝，不能依靠隐藏按钮代替鉴权。
        db.delete(member);db.commit()
        data = (await client.get(BASE+'/execution', params=query(row))).json()['data']
        assert data['canExecute'] and not data['canReadCase'] and not data['canEditCase']
        assert (await client.put('/test-cases/foreign-1',json={'name':'撤权后写入'})).status_code == 403
        assert db.get(Case,'foreign-1').name=='来源用例1'
        assert db.query(CaseVersion).count()==db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_edit_updates_current_source_keeps_step_and_text_history(cross):
    db, app, _ = cross
    app.include_router(cases, prefix='/test-cases')
    db.query(ProjectMember).filter_by(project_id='source',user_id='owner').one().role='maintainer'
    case=db.get(Case,'foreign-1');case.steps=[dict(step=1,action='旧步骤中文😀',expected='旧预期')];db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        await client.post(BASE+'/associate', json=dict(projectId='source',caseIds=['foreign-1']))
        row = next(r for r in (await client.get(BASE)).json()['data']['items'] if r['caseId']=='foreign-1')
        payload=dict(requestId=str(uuid4()),selections=[dict(source=row['source'],id=row['associationId'])], result='passed',description='<p>旧执行中文😀</p>',stepResults=[dict(index=0,result='passed',actual='旧实际')])
        response=await client.post(BASE+'/execute',json=payload)
        assert response.status_code==200,response.text
        previous=deepcopy((await client.get(BASE+'/execution',params=query(row))).json()['data']['history'])
        response=await client.put('/test-cases/foreign-1',json=dict(name='更新后主用例',case_edit_type='TEXT',text_description='<p>新文本</p>',expected_result='<p>新预期</p>',steps=[],priority='P0'))
        assert response.status_code==200,response.text
        current=(await client.get(BASE+'/execution',params=query(row))).json()['data']
        assert current['entry']['name']=='更新后主用例' and current['entry']['caseEditType']=='TEXT'
        assert current['history']==previous and current['history'][0]['caseSnapshot']['steps'][0]['action']=='旧步骤中文😀'
        payload.update(requestId=str(uuid4()),description='新文本执行',stepResults=[])
        assert (await client.post(BASE+'/execute',json=payload)).status_code==200
        history=(await client.get(BASE+'/execution',params=query(row))).json()['data']['history']
        assert len(history)==2 and history[0]['caseSnapshot']['caseEditType']=='TEXT'
        assert history[1]==previous[0] and db.query(PlanCaseExecution).count()==2
        versions=db.query(CaseVersion).filter_by(case_id='foreign-1').order_by(CaseVersion.version).all()
        assert len(versions)==2 and versions[0].snapshot['name']=='来源用例1' and versions[1].snapshot['name']=='更新后主用例'
        assert db.get(Case,'foreign-1').project_id=='source' and db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_archived_recycled_and_detached_editor_flags_preserve_history(workspace_http):
    db, app, _ = workspace_http
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        row=(await client.get(BASE)).json()['data']['items'][0]
        async def detail(): return (await client.get(BASE+'/execution',params=query(row))).json()['data']
        assert (await detail())['canEditCase']
        await client.post(BASE+'/execute',json=dict(requestId=str(uuid4()),selections=[dict(source=row['source'],id=row['associationId'])],result='blocked',description='保留执行历史'))
        history=(await detail())['history']
        workspace=PlanWorkspace(plan_id='plan',archived=True);db.add(workspace);db.commit()
        data=await detail();assert data['canReadCase'] and not data['canEditCase'] and not data['canExecute']
        workspace.archived=False;db.get(Case,row['caseId']).deleted_at=datetime.now();db.commit()
        data=await detail();assert not data['canReadCase'] and not data['canEditCase'] and data['history']==history
        db.get(Case,row['caseId']).deleted_at=None;db.commit()
        await client.post(BASE+'/batch',json=dict(action='unlink',selections=[dict(source=row['source'],id=row['associationId'])]))
        data=await detail();assert data['detached'] and not data['canReadCase'] and not data['canEditCase'] and data['history']==history
        assert db.query(TaskQueue).count()==0
