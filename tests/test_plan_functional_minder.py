"""功能脑图按实例回填、完整目录范围及结果筛选重试；仅隔离软件库。"""
from copy import deepcopy
from uuid import uuid4
import httpx
import pytest
from models import TestCase as Case, PlanCaseRelation
from models.plan_workspace import PlanNode, PlanWorkspace
from models.plan_case_execution import PlanCaseExecution
from models.task_queue import TaskQueue
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab

BASE='/orchestration/plans/plan/case-workspace'

@pytest.mark.asyncio
async def test_duplicate_instances_keep_independent_result_and_snapshot(workspace_http):
    db,app,_=workspace_http
    db.add_all([PlanNode(id='root',plan_id='plan',node_type='ROOT',name='计划'),PlanCaseRelation(plan_id='plan',case_id='case-2')]);db.flush()
    db.add_all([PlanNode(id='a',plan_id='plan',parent_id='root',node_type='CASE',name='同一用例A',case_id='case-2'),PlanNode(id='b',plan_id='plan',parent_id='root',node_type='CASE',name='同一用例B',case_id='case-2')]);db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        data=(await client.get(BASE)).json()['data'];rows=[row for row in data['items'] if row['caseId']=='case-2'];assert len(rows)>=2
        row=rows[0];body=dict(selectIds=[row['id']],requestId=str(uuid4()),result='failed',description='实例独立中文😀')
        response=await client.post(BASE+'/minder-execute',json=body);assert response.status_code==200,response.text
        assert response.json()['data']['updated']==1
        all_rows=(await client.get(BASE)).json()['data']['items'];assert sum(r['result']=='failed' for r in all_rows)==1
        history=deepcopy(db.query(PlanCaseExecution).one().case_snapshot)
        db.get(Case,'case-2').name='主用例之后更新';db.commit()
        assert db.query(PlanCaseExecution).one().case_snapshot==history
        assert (await client.post(BASE+'/minder-execute',json=body)).json()['data']['replayed']
        body['result']='passed';assert (await client.post(BASE+'/minder-execute',json=body)).status_code==409
        assert db.query(TaskQueue).count()==0

@pytest.mark.asyncio
async def test_complete_scope_exceeds_page_and_result_filter_retries(workspace_http):
    db,app,_=workspace_http
    for index in range(101):
        db.add(Case(id=f'm-{index}',project_id='project',name=f'脑图分页{index}',case_code=f'M{index:03}',type='functional',steps=[],is_automated=False,created_by='owner'))
    db.flush()
    db.add_all([PlanCaseRelation(plan_id='plan',case_id=f'm-{index}') for index in range(101)]);db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        condition=dict(search='脑图分页',result='pending')
        page=(await client.get(BASE,params=dict(view='minder-page',size=100,**condition))).json()['data']
        assert page['total']==101 and len(page['items'])==100
        selection=dict(selectAll=True,condition=condition)
        response=await client.post(BASE+'/minder-preview',json=selection);assert response.status_code==200,response.text
        assert response.json()['data']['count']==101
        body=dict(**selection,requestId=str(uuid4()),result='passed',description='全范围分页独立回填')
        result=await client.post(BASE+'/minder-execute',json=body);assert result.status_code==200,result.text
        assert result.json()['data']['updated']==101
        assert db.query(PlanCaseExecution).count()==101 and db.query(TaskQueue).count()==0
        assert (await client.get(BASE,params=condition)).json()['data']['total']==0
        replay=await client.post(BASE+'/minder-execute',json=body);assert replay.status_code==200,replay.text
        assert replay.json()['data']==dict(updated=101,replayed=True)
        assert db.query(PlanCaseExecution).count()==101
        body['description']='不得覆盖';assert (await client.post(BASE+'/minder-execute',json=body)).status_code==409

@pytest.mark.asyncio
async def test_archived_and_recycled_and_strict_scope_do_not_write(workspace_http):
    db,app,identity=workspace_http
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        rows=(await client.get(BASE)).json()['data']['items'];row=rows[0]
        body=dict(selectIds=[row['id']],requestId=str(uuid4()),result='blocked')
        for changes in [dict(category='api'),dict(selectAll=True),dict(stepResults=[dict(index=0,result='passed')]),dict(condition={'protocols':'HTTP'})]:
            assert (await client.post(BASE+'/minder-execute',json=dict(body,**changes))).status_code==422
        db.add(PlanWorkspace(plan_id='plan',archived=True));db.commit()
        preview=await client.post(BASE+'/minder-preview',json=dict(selectIds=[row['id']]));assert not preview.json()['data']['canExecute']
        assert (await client.post(BASE+'/minder-execute',json=body)).status_code==409
        db.get(PlanWorkspace,'plan').archived=False
        from datetime import datetime
        db.get(Case,row['caseId']).deleted_at=datetime.now();db.commit()
        assert (await client.post(BASE+'/minder-execute',json=body)).status_code==404
        identity['id']='stranger';assert (await client.post(BASE+'/minder-execute',json=body)).status_code==403
        assert db.query(PlanCaseExecution).count()==db.query(TaskQueue).count()==0

@pytest.mark.asyncio
async def test_folder_and_advanced_filters_intersect_and_descendants(workspace_http):
    from models import Module
    from test_plan_native_workspace import c
    db,app,_=workspace_http
    db.add(Module(id='parent-m',project_id='project',name='父模块'));db.flush()
    db.add(Module(id='child-m',project_id='project',name='子模块',parent_id='parent-m'))
    db.get(Case,'case-0').module_id='parent-m';db.get(Case,'case-0').priority='P1'
    db.get(Case,'case-1').module_id='child-m';db.get(Case,'case-1').priority='P1';db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        condition=dict(tree_type='MODULE',folder='parent-m',include_descendants=False,filters=dict(conditions=[c('priority','equals','P1')],logic='and'))
        selection=dict(selectAll=True,condition=condition)
        response=await client.post(BASE+'/minder-preview',json=selection);assert response.status_code==200,response.text
        assert response.json()['data']['count']==1
        condition['include_descendants']=True
        assert (await client.post(BASE+'/minder-preview',json=selection)).json()['data']['count']==2
        condition['folder']='child-m'
        response=await client.post(BASE+'/minder-execute',json=dict(**selection,requestId=str(uuid4()),result='blocked'))
        assert response.status_code==200,response.text
        assert response.json()['data']['updated']==1
        assert db.query(PlanCaseExecution).one().case_id=='case-1' and db.query(TaskQueue).count()==0
