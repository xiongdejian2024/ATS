"""关联全范围、排除、原生字段、事务回滚及旧接口兼容。"""
from datetime import datetime, timedelta
import json
import httpx
import pytest
from fastapi import HTTPException
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from test_native_case_filters import native, prepare, config, c
from models import TestCase as Case, TestPlan as Plan, TestSuite as Suite, PlanCaseRelation, Module, Project, ProjectMember
from models.plan_workspace import PlanNode, PlanWorkspace
from models.case_governance import CaseVersion
from models.task_queue import TaskQueue
from services.plan_tree import save_node

BASE = '/orchestration/plans/plan/case-workspace'


@pytest.fixture
def candidate_range(workspace_http):
    db, app, identity = workspace_http
    db.add(Module(id='parent', project_id='project', name='父目录')); db.flush()
    db.add(Module(id='child', project_id='project', name='子目录', parent_id='parent')); db.flush()
    db.add_all([Case(id=f'range-{i}', project_id='project', name=f'范围%_用例{i}', case_code=f'RANGE-{i}',
        type='functional', steps=[], is_automated=False, created_by='owner', priority='P1', tags=['回归'],
        module_id='child', created_at=datetime(2026, 10, 6) + timedelta(minutes=i)) for i in range(23)])
    db.add(Project(id='other', name='外部项目', owner_id='owner')); db.flush()
    db.add(Case(id='foreign', project_id='other', name='范围%_外部', case_code='FOREIGN', type='functional', steps=[], created_by='owner'))
    db.commit()
    return db, app, identity


@pytest.mark.asyncio
async def test_full_range_pages_exclusions_legacy_links_and_exact_commit(candidate_range):
    db, app, _ = candidate_range
    body = dict(selectAll=True, condition=dict(search='%_', folder='parent', priority='P1'), excludeIds=['range-0', 'range-22'])
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        first = (await client.get(BASE+'/candidates', params=dict(search='%_', folder='parent', size=20))).json()['data']
        second = (await client.get(BASE+'/candidates', params=dict(search='%_', folder='parent', size=20, page=2))).json()['data']
        assert first['total'] == second['total'] == 23 and len(first['items']) == 20 and len(second['items']) == 3
        response = await client.post(BASE+'/candidates/selection', json=body)
        assert response.status_code == 200, response.text
        assert response.json()['data'] == dict(count=21, excludedCount=2, automatedCount=0, usesTree=False, compatibleSuiteIds=['suite-0', 'suite-1'], canAssociate=True)
        assert db.query(PlanCaseRelation).count() == 2 and db.query(CaseVersion).count() == 0
        response = await client.post(BASE+'/associate', json=body)
        assert response.status_code == 200, response.text
        assert response.json()['data']['added'] == 21
        actual = {r.case_id for r in db.query(PlanCaseRelation).filter_by(plan_id='plan')}
        assert actual == {'case-0', 'case-1'} | {f'range-{i}' for i in range(1, 22)}
        assert (await client.post(BASE+'/candidates/selection', json=body)).json()['data']['count'] == 0
        assert (await client.post(BASE+'/associate', json=body)).status_code == 409
        assert (await client.post(BASE+'/associate', json=dict(caseIds=['range-1']))).json()['data']['added'] == 0
    assert db.query(TaskQueue).count() == 0 and db.query(CaseVersion).count() == 0


@pytest.mark.asyncio
async def test_advanced_current_user_or_and_empty_and_dynamic_requery(candidate_range):
    db, app, _ = candidate_range
    conditions = [c('createdBy', 'equals', 'CURRENT_USER'), c('tags', 'belongs_to', ['回归']), c('priority', 'equals', 'P1')]
    body = dict(selectAll=True, excludeIds=['range-22'], condition=dict(filters=dict(conditions=conditions, logic='and'), mine=True))
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        assert (await client.post(BASE+'/candidates/selection', json=body)).json()['data']['count'] == 22
        db.get(Case, 'range-0').priority = 'P0'
        db.get(Case, 'range-1').deleted_at = datetime.now(); db.commit()
        result = await client.post(BASE+'/associate', json=body)
        assert result.status_code == 200, result.text
        assert result.json()['data']['added'] == 20
        assert {r.case_id for r in db.query(PlanCaseRelation).filter_by(plan_id='plan')} == {'case-0', 'case-1'} | {f'range-{i}' for i in range(2, 22)}
        alternate = dict(selectAll=True, condition=dict(filters=dict(conditions=[c('id', 'equals', 'RANGE-0'), c('name', 'contains', '用例22'), c('name', 'contains', '')], logic='or')))
        assert (await client.post(BASE+'/candidates/selection', json=alternate)).json()['data']['count'] == 2
        empty = dict(selectAll=True, condition=dict(search='不存在的范围'))
        assert (await client.post(BASE+'/candidates/selection', json=empty)).json()['data']['count'] == 0
        assert (await client.post(BASE+'/associate', json=empty)).status_code == 409
    assert db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
@pytest.mark.parametrize('category', ['api', 'scenario'])
async def test_native_scope_is_real_and_category_and_suite_are_checked(native, category):
    db, app, _ = native
    db.query(PlanCaseRelation).delete(); db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        definition, env = await prepare(client)
        if category == 'api':
            assert (await client.put('/projects/project/native-cases/cases/case-0', json=config(definition, env))).status_code == 200
            conditions = [c('protocol', 'equals', 'HTTP'), c('apiChange', 'equals', False), c('path', 'contains', '诊断')]
            target = 'case-0'
        else:
            assert (await client.put('/projects/project/native-cases/cases/case-2', json=dict(state='UNDERWAY', environmentId=env['id']))).status_code == 200
            conditions = [c('nativeState', 'equals', 'UNDERWAY'), c('environmentName', 'equals', env['id']), c('stepTotal', 'equals', 3)]
            target = 'case-2'
        body = dict(category=category, selectAll=True, condition=dict(filters=dict(conditions=conditions)))
        preview = (await client.post(BASE+'/candidates/selection', json=body)).json()['data']
        assert preview['count'] == preview['automatedCount'] == 1
        result = await client.post(BASE+'/associate', json=body)
        assert result.status_code == 200, result.text
        assert {r.case_id for r in db.query(PlanCaseRelation)} == {target}
        assert (await client.post(BASE+'/candidates/selection', json={**body, 'category':'functional'})).status_code == 422
    assert db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_tree_suite_full_scope_duplicates_and_failed_second_write_roll_back(candidate_range, monkeypatch):
    db, app, _ = candidate_range
    save_node(db, db.get(Plan, 'plan'), dict(name='原关联', nodeType='case', caseId='case-2'))
    db.get(Suite, 'suite-0').case_ids = ['case-0', 'case-1']; db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        body = dict(selectAll=True, condition={})
        preview = (await client.post(BASE+'/candidates/selection', json=body)).json()['data']
        assert preview['count'] == 26 and preview['automatedCount'] == 2 and preview['usesTree']
        assert preview['compatibleSuiteIds'] == ['suite-0']
        assert (await client.post(BASE+'/associate', json=body)).status_code == 422
        assert (await client.post(BASE+'/associate', json={**body, 'suiteId':'suite-1'})).status_code == 422
        assert db.query(PlanNode).count() == 1
        import services.plan_case_workspace as service
        original = service.save_node
        calls = []
        def fail_second(*args, **kwargs):
            calls.append(1)
            if len(calls) == 2: raise HTTPException(422, '模拟第二条关联失败')
            return original(*args, **kwargs)
        monkeypatch.setattr(service, 'save_node', fail_second)
        assert (await client.post(BASE+'/associate', json={**body, 'suiteId':'suite-0'})).status_code == 422
        assert db.query(PlanNode).count() == 1
        monkeypatch.setattr(service, 'save_node', original)
        result = await client.post(BASE+'/associate', json={**body, 'suiteId':'suite-0'})
        assert result.status_code == 200, result.text
        assert result.json()['data']['added'] == 26 and db.query(PlanNode).count() == 27
        # 树中同一个用例可以有多个关联实例，不能按主用例ID去掉已有实例。
        assert (await client.post(BASE+'/associate', json=dict(caseIds=['case-2']))).json()['data']['added'] == 1
        assert db.query(PlanNode).filter_by(case_id='case-2').count() == 3
    assert db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_schema_permissions_archived_foreign_and_commit_failure(candidate_range, monkeypatch):
    db, app, identity = candidate_range
    body = dict(selectAll=True, condition=dict(search='%_'))
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app, raise_app_exceptions=False), base_url='http://test') as client:
        for invalid in [{}, dict(selectAll=True, caseIds=['range-0']), dict(caseIds=['range-0'], excludeIds=['range-1']), dict(caseIds=['range-0'], condition={'search':'范围'}), dict(caseIds=['range-0', 'range-0']), dict(caseIds=['']), dict(selectAll=1), dict(selectAll=True, condition={'page':1}), dict(selectAll=True, condition={'userId':'stranger'}), dict(selectAll=True, condition={'filters':{'conditions':[c('不存在字段','equals',1)]}})]:
            assert (await client.post(BASE+'/candidates/selection', json=invalid)).status_code == 422, invalid
        assert (await client.post(BASE+'/associate', json=dict(caseIds=['range-0', 'foreign']))).status_code == 404
        assert (await client.post(BASE+'/candidates/selection', json=dict(selectAll=True, condition={'folder':'foreign'}))).status_code == 404
        identity['id'] = 'stranger'
        assert (await client.post(BASE+'/candidates/selection', json=body)).status_code == 403
        db.add(ProjectMember(project_id='project', user_id='stranger', role='member')); db.commit()
        assert not (await client.post(BASE+'/candidates/selection', json=body)).json()['data']['canAssociate']
        assert (await client.post(BASE+'/associate', json=body)).status_code == 403
        identity['id'] = 'owner'
        db.add(PlanWorkspace(plan_id='plan', archived=True)); db.commit()
        assert not (await client.post(BASE+'/candidates/selection', json=body)).json()['data']['canAssociate']
        assert (await client.post(BASE+'/associate', json=body)).status_code == 409
        db.get(PlanWorkspace, 'plan').archived = False; db.commit()
        original = db.commit
        def failed_commit(): raise RuntimeError('模拟关联提交失败')
        monkeypatch.setattr(db, 'commit', failed_commit)
        assert (await client.post(BASE+'/associate', json=body)).status_code == 500
        monkeypatch.setattr(db, 'commit', original)
        assert db.query(PlanCaseRelation).count() == 2
    assert db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_more_than_old_500_and_real_limit_with_matching_exclusions(workspace_http):
    db, app, _ = workspace_http
    db.bulk_insert_mappings(Case, [dict(id=f'large-{i}', project_id='project', name=f'大范围{i}', case_code=f'LARGE-{i}', type='functional', steps=[], is_automated=False, created_by='owner') for i in range(10001)])
    db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        body = dict(selectAll=True, condition=dict(search='大范围'))
        assert (await client.post(BASE+'/candidates/selection', json=body)).status_code == 422
        assert (await client.post(BASE+'/candidates/selection', json={**body, 'excludeIds':['missing']})).status_code == 422
        assert (await client.post(BASE+'/candidates/selection', json={**body, 'excludeIds':['large-0']})).json()['data']['count'] == 10000
        explicit = dict(caseIds=[f'large-{i}' for i in range(501)])
        assert (await client.post(BASE+'/candidates/selection', json=explicit)).json()['data']['count'] == 501
        assert (await client.post(BASE+'/associate', json=explicit)).json()['data']['added'] == 501
        assert db.query(PlanCaseRelation).count() == 503
    assert db.query(TaskQueue).count() == 0 and db.query(CaseVersion).count() == 0
