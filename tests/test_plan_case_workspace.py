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
        assert row['projectName']==db.get(Project,'project').name
        assert row['moduleName']=='子模块' and row['bugCount']==0 and row['caseBugCount']==1 and row['tags']==['回归'] and row['executorName']=='未分配'
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


@pytest.mark.asyncio
async def test_associate_candidates_pagination_literals_module_counts_and_project_scope(workspace_http):
    from datetime import datetime
    db,app,identity=workspace_http
    db.add(Module(id='parent',project_id='project',name='父模块'));db.flush()
    db.add(Module(id='child',project_id='project',name='子模块',parent_id='parent'));db.flush()
    db.get(Case,'case-0').module_id='child'
    db.get(Case,'case-2').name='百分%_用例'
    db.add(Case(id='deleted',project_id='project',name='已回收',case_code='DELETED',type='functional',steps=[],created_by='owner',deleted_at=datetime.now()))
    db.add(Case(id='api',project_id='project',name='API验收',case_code='API',type='api',steps=[],created_by='owner',is_automated=True))
    db.add(Case(id='bad-api',project_id='project',name='不可执行API',case_code='BAD-API',type='api',steps=[],created_by='owner',is_automated=False))
    db.add(Project(id='other',name='另项目',owner_id='owner'));db.flush()
    db.add(Module(id='outside',project_id='other',name='外部目录'))
    db.add(Case(id='outside-case',project_id='other',name='外部用例',case_code='OUTSIDE',type='functional',steps=[],created_by='owner'))
    db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        base='/orchestration/plans/plan/case-workspace'
        data=(await client.get(base+'/candidates',params={'size':1})).json()['data']
        assert data['total']==3 and len(data['items'])==1 and data['counts']['all']==3
        assert next(row for row in data['modules'] if row['id']=='parent')['count']==1
        first=data['items'][0]['id']
        second=(await client.get(base+'/candidates',params={'size':1,'page':2})).json()['data']['items'][0]['id']
        assert first!=second
        assert (await client.get(base+'/candidates',params={'folder':'parent'})).json()['data']['items'][0]['id']=='case-0'
        literal=(await client.get(base+'/candidates',params={'search':'%_'})).json()['data']
        assert literal['total']==1 and literal['items'][0]['id']=='case-2' and not literal['items'][0]['alreadyLinked']
        assert (await client.get(base+'/candidates',params={'folder':'outside'})).status_code==404
        api=(await client.get(base+'/candidates',params={'category':'api'})).json()['data']
        assert [row['id'] for row in api['items']]==['api']
        assert (await client.post(base+'/associate',json={'category':'api','caseIds':['api','case-2']})).status_code==422
        assert (await client.post(base+'/associate',json={'category':'api','caseIds':['bad-api']})).status_code==422
        assert db.query(PlanCaseRelation).filter_by(plan_id='plan').count()==2
        assert (await client.post(base+'/associate',json={'category':'api','caseIds':['api']})).json()['data']['added']==1
        assert (await client.get(base+'/candidates',params={'category':'api'})).json()['data']['items'][0]['alreadyLinked']
        identity['id']='stranger'
        assert (await client.get(base+'/candidates')).status_code==403
    assert db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_tree_association_validates_full_selection_suite_and_preserves_duplicates(workspace_http):
    db,app,identity=workspace_http
    node=save_node(db,db.get(Plan,'plan'),dict(name='原手工范围',nodeType='case',category='functional',caseId='case-2'));db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        base='/orchestration/plans/plan/case-workspace'
        original=db.query(PlanNode).count()
        assert (await client.post(base+'/associate',json={'caseIds':['case-0','case-2']})).status_code==422
        assert (await client.post(base+'/associate',json={'caseIds':['case-0','case-1'],'suiteId':'suite-0'})).status_code==422
        assert (await client.post(base+'/associate',json={'caseIds':['case-2'],'suiteId':'missing'})).status_code==422
        assert db.query(PlanNode).count()==original
        assert (await client.post(base+'/associate',json={'caseIds':['case-0','case-2'],'suiteId':'suite-0'})).json()['data']['added']==2
        rows=(await client.get(base)).json()['data']['items']
        assert len(rows)==3 and len({row['associationId'] for row in rows if row['caseId']=='case-2'})==2
        assert (await client.get(base+'/candidates')).json()['data']['usesTree']
    assert db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_node_configuration_archived_and_batch_validation_roll_back(workspace_http,monkeypatch):
    from fastapi import HTTPException
    import services.plan_tree as tree
    db,app,identity=workspace_http
    plan=db.get(Plan,'plan')
    point=save_node(db,plan,dict(name='配置测试集',nodeType='point'))
    first=save_node(db,plan,dict(name='实例甲',nodeType='case',category='functional',caseId='case-2',parentId=point.id))
    second=save_node(db,plan,dict(name='实例乙',nodeType='case',category='functional',caseId='case-2',parentId=point.id))
    db.get(PlanWorkspace,'plan').archived=True;db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        base='/orchestration/plans/plan/nodes'
        assert (await client.post(base,json={'name':'归档后创建'})).status_code==409
        assert (await client.put('/orchestration/nodes/'+point.id,json={'name':'归档后编辑'})).status_code==409
        assert (await client.delete('/orchestration/nodes/'+point.id)).status_code==409
        assert (await client.post(base+'/assign',json={'nodeIds':[first.id],'assignedTo':'owner'})).status_code==409
        assert (await client.get(base)).status_code==200
        db.get(PlanWorkspace,'plan').archived=False;db.commit()
        original=tree.save_node;calls=[]
        def rejected_second(db,plan,data,existing=None):
            calls.append(existing.id)
            if len(calls)==2:raise HTTPException(422,'模拟第二项校验失败')
            return original(db,plan,data,existing)
        monkeypatch.setattr(tree,'save_node',rejected_second)
        assert (await client.post(base+'/assign',json={'nodeIds':[first.id,second.id],'assignedTo':'owner'})).status_code==422
        assert len(calls)==2 and db.get(PlanNode,first.id).assigned_to is None and db.get(PlanNode,second.id).assigned_to is None
        monkeypatch.setattr(tree,'save_node',original)
        assert (await client.post(base+'/assign',json={'nodeIds':[first.id,first.id],'assignedTo':'owner'})).status_code==422
    assert db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_node_create_commit_failure_rolls_back_insert(workspace_http,monkeypatch):
    db,app,identity=workspace_http
    original=db.commit
    def broken_commit():raise RuntimeError('模拟提交失败')
    monkeypatch.setattr(db,'commit',broken_commit)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app,raise_app_exceptions=False),base_url='http://test') as client:
        assert (await client.post('/orchestration/plans/plan/nodes',json={'name':'提交失败不残留','nodeType':'point'})).status_code==500
    monkeypatch.setattr(db,'commit',original)
    assert db.query(PlanNode).count()==0 and db.query(TaskQueue).count()==0
