"""实例缺陷不传播到重复主用例，跨项目、权限、批量范围与历史软件验收。"""
from uuid import uuid4
from datetime import datetime
import httpx
import pytest
from sqlalchemy import create_engine, inspect
from models import TestPlan as Plan, TestCase as Case, ProjectMember, Module, PlanCaseRelation
from models.case_features import CaseIssue, CaseIssueLink
from models.plan_workspace import PlanNode, PlanWorkspace
from models.plan_case_defect import PlanCaseDefect
from models.role import Permission, ProjectPermission
from models.task_queue import TaskQueue
from services.plan_tree import save_node
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from test_plan_candidate_projects import cross
BASE = '/orchestration/plans/plan/case-workspace'


@pytest.mark.asyncio
async def test_cross_project_duplicate_bindings_replay_cancel_and_legacy_preserved(cross):
    db, app, _ = cross
    plan = db.get(Plan, 'plan')
    for _ in range(2): save_node(db, plan, dict(name='来源重复实例', nodeType='case', caseId='foreign-1'), source_project_id='source')
    db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        rows = (await client.get(BASE)).json()['data']['items']; assert len(rows) == 2
        payload = dict(selectIds=[rows[0]['id']], title='  本计划实例缺陷😀  ', description='功能执行发现问题', requestId=str(uuid4()))
        response = await client.post(BASE+'/defects', json=payload); assert response.status_code == 200, response.text
        issue_id = response.json()['data']['issueId']
        assert (await client.post(BASE+'/defects', json=payload)).json()['data']['replayed']
        assert (await client.post(BASE+'/defects', json=dict(payload, title='不同内容'))).status_code == 409
        assert db.get(CaseIssue, issue_id).project_id == 'project'
        assert db.query(CaseIssueLink).count() == 1  # 原来源缺陷保持，不写主用例关系
        counts = {r['id']: r['bugCount'] for r in (await client.get(BASE)).json()['data']['items']}
        assert counts == {rows[0]['id']: 1, rows[1]['id']: 0}
        import json
        filtered=(await client.get(BASE, params={'filters':json.dumps({'conditions':[{'field':'bugCount','operator':'equals','value':1}]})})).json()['data']['items']
        assert [row['id'] for row in filtered] == [rows[0]['id']]
        candidates = (await client.get(BASE+'/defects/candidates')).json()['data']['items']
        assert {i['id'] for i in candidates} == {issue_id}
        assert (await client.post(BASE+'/defects/associate', json=dict(selectIds=[rows[1]['id']], issueIds=['source-bug']))).status_code == 404
        association = dict(selectIds=[rows[1]['id']], issueIds=[issue_id])
        assert (await client.post(BASE+'/defects/associate', json=association)).json()['data']['updated'] == 1
        assert (await client.post(BASE+'/defects/associate', json=association)).json()['data']['updated'] == 0
        link = (await client.get(BASE+'/defects', params={'associationKey': rows[0]['id']})).json()['data']['items'][0]
        assert (await client.delete(BASE+'/defects/'+link['linkId'])).status_code == 200
        assert db.get(CaseIssue, issue_id) and db.query(PlanCaseDefect).filter_by(active=True).count() == 1
        assert (await client.post(BASE+'/defects/associate', json=dict(selectIds=[rows[0]['id']], issueIds=[issue_id]))).json()['data']['updated'] == 1
        frozen = db.query(PlanCaseDefect).filter_by(association_key=rows[0]['id']).one().case_snapshot.copy()
        db.get(Case, 'foreign-1').name = '主用例后来改名'; db.commit()
        assert (await client.post(BASE+'/minder-batch', json=dict(selectIds=[rows[0]['id']], action='unlink'))).status_code == 200
        history = (await client.get(BASE+'/defects', params={'associationKey': rows[0]['id']})).json()['data']
        assert history['detached'] and not history['canAssociate'] and history['items'][0]['caseName'] == frozen['name']
        assert (await client.delete(BASE+'/defects/'+link['linkId'])).status_code == 404
        aggregate = (await client.get('/orchestration/plans/plan/defects')).json()['data']['items']
        assert aggregate[0]['cases'][0].get('associationKey')
    assert db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_execute_permission_can_associate_without_plan_update_or_issue_create(workspace_http):
    db, app, identity = workspace_http
    db.add(ProjectMember(project_id='project', user_id='stranger', role='member'))
    db.add(Permission(id='execute-grant', code='test_plan:execute', resource='test_plan', action='execute', name='计划执行'))
    db.flush(); db.add(ProjectPermission(project_id='project', user_id='stranger', permission_id='execute-grant'))
    db.add(CaseIssue(id='bug', project_id='project', kind='defect', title='既有缺陷', created_by='owner', updated_by='owner')); db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        row = (await client.get(BASE)).json()['data']['items'][0]; selection = dict(selectIds=[row['id']]); identity['id'] = 'stranger'
        caps = (await client.post(BASE+'/defects/preview', json=selection)).json()['data']
        assert caps['canAssociate'] and not caps['canCreate']
        assert (await client.post(BASE+'/defects', json=dict(**selection, title='禁止创建', requestId=str(uuid4())))).status_code == 403
        assert (await client.post(BASE+'/defects/associate', json=dict(**selection, issueIds=['bug']))).status_code == 200
        assert (await client.post(BASE+'/minder-batch', json=dict(**selection, action='assign'))).status_code == 403
        link = db.query(PlanCaseDefect).one()
        assert (await client.delete(BASE+'/defects/'+link.id)).status_code == 200
        db.add(PlanWorkspace(plan_id='plan', archived=True)); db.commit()
        caps = (await client.post(BASE+'/defects/preview', json=selection)).json()['data']; assert not caps['canAssociate']
        assert (await client.post(BASE+'/defects/associate', json=dict(**selection, issueIds=['bug']))).status_code == 409
        identity['id'] = 'owner'
        assert (await client.post('/orchestration/plans/plan/defects', json={'caseId':row['caseId'], 'title':'归档禁止'})).status_code == 409
    assert db.query(CaseIssue).count() == 1 and db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_multi_folder_union_full_scope_deduplicates_and_filters_intersect(workspace_http):
    db, app, _ = workspace_http
    db.add_all([Module(id='parent', project_id='project', name='父目录'), Module(id='other', project_id='project', name='另目录')]); db.flush()
    db.add(Module(id='child', project_id='project', parent_id='parent', name='子目录')); db.flush()
    for i in range(101):
        db.add(Case(id=f'union-{i}', project_id='project', module_id='child', name='批量未加载功能'+str(i), case_code=f'UNION{i:03}', type='functional', steps=[], priority='P1', created_by='owner'))
    db.flush(); db.add_all([PlanCaseRelation(plan_id='plan', case_id=f'union-{i}') for i in range(101)])
    db.add(CaseIssue(id='bug', project_id='project', kind='defect', title='批量绑定', created_by='owner', updated_by='owner')); db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        page = (await client.get(BASE, params=dict(view='minder-page', search='批量未加载', size=100))).json()['data']; assert page['total'] == 101 and len(page['items']) == 100
        scope = dict(selectAll=True, condition=dict(tree_type='MODULE', folderIds=['parent','child','other'], entryIds=[page['items'][0]['id']], search='批量未加载'))
        preview = await client.post(BASE+'/defects/preview', json=scope); assert preview.status_code == 200, preview.text; assert preview.json()['data']['count'] == 101
        association = dict(**scope, issueIds=['bug'])
        assert (await client.post(BASE+'/defects/associate', json=association)).json()['data']['updated'] == 101
        assert (await client.post(BASE+'/defects/associate', json=association)).json()['data']['updated'] == 0
        assert (await client.post(BASE+'/minder-batch', json=dict(**scope, action='assign', assignedTo='owner'))).json()['data']['updated'] == 101
        scope['condition']['search']='不存在'
        assert (await client.post(BASE+'/minder-batch', json=dict(**scope, action='unlink'))).status_code == 409
        scope['condition']['search']='批量未加载'
        scope['condition']['entryIds']=['node:foreign:case-0']
        assert (await client.post(BASE+'/defects/associate', json=dict(**scope, issueIds=['bug']))).status_code == 404
        assert db.query(PlanCaseDefect).count() == 101
        aggregate=(await client.get(BASE+'/defects/aggregate',params={'size':1})).json()['data']
        assert aggregate['total']==1 and len(aggregate['items'])==1 and len(aggregate['items'][0]['cases'])==20 and aggregate['items'][0]['caseCount']==101
        assert aggregate['cases']==[]
        assert (await client.get(BASE+'/defects/candidates', params={'size':101})).status_code == 422
    assert db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_recycled_unlink_and_commit_failure_roll_back_issue_and_binding(workspace_http, monkeypatch):
    db, app, _ = workspace_http
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        row = (await client.get(BASE)).json()['data']['items'][0]
        payload = dict(selectIds=[row['id']], title='失败不残留缺陷', requestId=str(uuid4()))
        def fail(): raise RuntimeError('模拟缺陷事务提交失败，验证完整回滚')
        with monkeypatch.context() as patch:
            patch.setattr(db, 'commit', fail)
            with pytest.raises(RuntimeError): await client.post(BASE+'/defects', json=payload)
        assert db.query(CaseIssue).count() == db.query(PlanCaseDefect).count() == 0
        assert (await client.post(BASE+'/defects', json=dict(payload, caseId=row['caseId']))).status_code == 422
        db.get(Case, row['caseId']).deleted_at = datetime.now(); db.commit()
        assert (await client.post(BASE+'/defects', json=payload)).status_code == 404
        selection = dict(selectIds=[row['id']], action='unlink')
        assert (await client.post(BASE+'/minder-batch/preview', json=selection)).json()['data']['count'] == 1
        assert (await client.post(BASE+'/minder-batch', json=selection)).status_code == 200
    assert db.query(TaskQueue).count() == 0


def test_incremental_schema_validates_unique_foreign_keys_and_dry_run(workspace_http):
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
    from upgrade_plan_case_defects import upgrade
    db, _, _ = workspace_http
    assert upgrade(True, db.bind) == []
    engine = create_engine('sqlite:///:memory:')
    assert upgrade(False, engine) == ['plan_case_defects']
    assert 'plan_case_defects' not in inspect(engine).get_table_names()
    upgrade(True, engine)
    assert upgrade(True, engine) == []
