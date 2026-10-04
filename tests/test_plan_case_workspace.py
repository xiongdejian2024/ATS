"""分类工作区：导航、旧数据兼容、事务隔离和空树执行边界。"""
import httpx
import pytest
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from models import TestPlan as Plan, TestCase as Case, Module, PlanCaseRelation, Project, ProjectMember
from models.plan_workspace import PlanNode, PlanWorkspace
from models.case_features import CaseIssue, CaseIssueLink
from models.task_queue import TaskQueue
from services.plan_tree import save_node
from services.plan_orchestration import start_plan_run


@pytest.mark.asyncio
async def test_legacy_columns_filters_tree_counts_move_assign_and_clone(workspace_http):
    db,app,identity=workspace_http
    db.add(Module(id='parent',project_id='project',name='父模块'))
    db.flush();db.add(Module(id='child',project_id='project',name='子模块',parent_id='parent'))
    case=db.get(Case,'case-0');case.module_id='child';case.tags=['回归'];case.priority='P1'
    other=db.get(Case,'case-1');other.priority='P3'
    point=save_node(db,db.get(Plan,'plan'),dict(name='新测试集',nodeType='point'))
    db.add(CaseIssue(id='bug',project_id='project',kind='defect',title='实际缺陷',created_by='owner',updated_by='owner'))
    db.flush();db.add(CaseIssueLink(issue_id='bug',case_id='case-0',created_by='owner'));db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        base='/orchestration/plans/plan/case-workspace'
        data=(await client.get(base)).json()['data']
        assert data['total']==2 and not data['usesTree']
        row=next(item for item in data['items'] if item['caseId']=='case-0')
        assert row['moduleName']=='子模块' and row['bugCount']==1 and row['tags']==['回归'] and row['executorName']=='未分配'
        assert next(module for module in data['modules'] if module['id']=='parent')['count']==1
        assert (await client.get(base,params={'tree_type':'MODULE','folder':'parent'})).json()['data']['total']==1
        assert (await client.get(base,params={'tree_type':'MODULE','folder':'parent','include_descendants':False})).json()['data']['total']==0
        assert (await client.get(base,params={'priority':'P1','tag':'回归','search':'code-0'})).json()['data']['total']==1
        assert (await client.get(base,params={'size':1,'page':2,'sort':'caseCode','direction':'asc'})).json()['data']['items'][0]['caseId']=='case-1'
        assert len((await client.get(base,params={'size':1,'view':'mind'})).json()['data']['items'])==2
        selected=[dict(source=row['source'],id=row['associationId'])]
        assert (await client.post(base+'/batch',json=dict(action='move',selections=selected,collectionId=point.id))).status_code==200
        assert (await client.get(base,params={'folder':point.id})).json()['data']['items'][0]['collectionName']=='新测试集'
        assert (await client.post(base+'/batch',json=dict(action='assign',selections=selected,assignedTo='owner'))).status_code==200
        assert (await client.get(base,params={'executor':'owner'})).json()['data']['items'][0]['executorName']=='计划负责人'
        clone=(await client.post('/test-plans/plan/clone',json={'project_id':'project'})).json()['data']
        clone_data=(await client.get(f"/orchestration/plans/{clone['id']}/case-workspace")).json()['data']
        cloned=next(item for item in clone_data['items'] if item['caseId']=='case-0')
        assert cloned['collectionName']=='新测试集' and cloned['collectionId']!=point.id and cloned['assignedTo']=='owner'
        assert not clone_data['usesTree'] and cloned['result']=='pending'
    assert db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_rejected_batches_do_not_partially_write_and_member_is_readonly(workspace_http):
    db,app,identity=workspace_http
    db.add(Project(id='other',name='另项目',owner_id='owner'));db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        base='/orchestration/plans/plan/case-workspace'
        row=(await client.get(base)).json()['data']['items'][0]
        selection=dict(source=row['source'],id=row['associationId'])
        for payload in (dict(action='unlink',selections=[selection,dict(source='legacy',id='not-current')]),dict(action='move',selections=[selection],collectionId='outside'),dict(action='assign',selections=[selection],assignedTo='stranger')):
            assert (await client.post(base+'/batch',json=payload)).status_code in (403,404,422)
        assert db.query(PlanCaseRelation).filter_by(plan_id='plan').count()==2
        assert all(item.assigned_to is None for item in db.query(PlanCaseRelation).filter_by(plan_id='plan'))
        assert (await client.post(base+'/associate',json={'caseIds':['case-2','missing']})).status_code==404
        assert db.query(PlanCaseRelation).filter_by(plan_id='plan').count()==2
        assert (await client.post(base+'/associate',json={'caseIds':['case-2']})).json()['data']['added']==1
        assert (await client.post(base+'/associate',json={'caseIds':['case-2']})).json()['data']['added']==0
        identity['id']='stranger'
        assert (await client.get(base)).status_code==403
        db.add(ProjectMember(project_id='project',user_id='stranger',role='member'));db.commit()
        assert (await client.get(base)).status_code==200
        assert (await client.post(base+'/batch',json=dict(action='unlink',selections=[selection]))).status_code==403
        assert (await client.post(base+'/associate',json={'caseIds':['case-2']})).status_code==403
    assert db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_last_tree_unlink_stays_empty_and_does_not_reactivate_legacy_suites(workspace_http):
    db,app,identity=workspace_http
    node=save_node(db,db.get(Plan,'plan'),dict(name='手工独立范围',nodeType='case',category='functional',caseId='case-2'));db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        base='/orchestration/plans/plan/case-workspace'
        data=(await client.get(base)).json()['data'];assert data['total']==1 and data['usesTree']
        assert (await client.post(base+'/batch',json=dict(action='unlink',selections=[dict(source='node',id=node.id)]))).status_code==200
        data=(await client.get(base)).json()['data'];assert data['total']==0 and data['usesTree']
        detail=(await client.get('/test-plans/plan')).json()['data']
        assert detail['totalCases']==0 and detail['usesTestPointTree'] and detail['categoryCounts']['functional']==0
        assert (await client.get('/orchestration/plans/plan/defects')).json()['data']['cases']==[]
        with pytest.raises(ValueError,match='请先为计划关联用例'):
            await start_plan_run(db,'plan','owner')
        assert (await client.post(base+'/associate',json={'caseIds':['case-2']})).status_code==200
        assert (await client.get(base)).json()['data']['total']==1
        assert db.query(PlanCaseRelation).filter_by(plan_id='plan').count()==2  # 旧关联仍保存，但不再参与树执行范围
    assert db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_legacy_unlink_prunes_future_suite_scope_but_keeps_templates_and_blocks_active_runs(workspace_http):
    from models import TestSuite as Suite
    from models.plan_orchestration import PlanRun
    db,app,identity=workspace_http
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        base='/orchestration/plans/plan/case-workspace'
        data=(await client.get(base)).json()['data']
        row=next(item for item in data['items'] if item['caseId']=='case-0')
        payload=dict(action='unlink',selections=[dict(source='legacy',id=row['associationId'])])
        run=await start_plan_run(db,'plan','owner')
        assert (await client.post(base+'/batch',json=payload)).status_code==409
        assert db.get(Suite,'suite-0').case_ids==['case-0']
        from services.plan_orchestration import cancel_plan_run, advance_plan_runs
        await cancel_plan_run(db,run.id,'owner')
        await advance_plan_runs(db)
        assert (await client.post(base+'/batch',json=payload)).status_code==200
        assert db.get(Suite,'suite-0').case_ids==[] and db.query(Suite).count()==2
        next_run=await start_plan_run(db,'plan','owner')
        assert {item['id'] for item in next_run.case_snapshot}=={'case-1'}
        assert {item['id'] for item in db.get(PlanRun,run.id).case_snapshot}=={'case-0','case-1'}
