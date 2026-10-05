"""模块组合覆盖父子范围、跨页排除、无模块用例、当前归属和整批回滚。"""
import httpx
import pytest
from datetime import datetime
from test_plan_candidate_selection import candidate_range
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from models import TestCase as Case, Module, PlanCaseRelation, TestPlan as Plan, User
from models.case_governance import CaseVersion
from models.task_queue import TaskQueue
from schemas.plan_candidate_selection import Association
from services.plan_candidate_selection import preview
from services.plan_case_workspace import associate
from api.v1.case_governance import transact
from fastapi import HTTPException

BASE = '/orchestration/plans/plan/case-workspace'
full = lambda *excluded: dict(selectAll=True, excludeIds=list(excluded))
partial = lambda *ids: dict(selectIds=list(ids))


@pytest.fixture
def module_range(candidate_range):
    db, app, identity = candidate_range
    db.add(Module(id='sibling', name='另一个模块', project_id='project')); db.flush()
    for cid, module in [('parent-case', 'parent'), ('sibling-case', 'sibling'), ('no-module', None)]:
        db.add(Case(id=cid, project_id='project', name=cid, case_code=cid, type='functional', steps=[],
            is_automated=False, created_by='owner', priority='P1', module_id=module))
    db.commit()
    return db, app, identity


@pytest.mark.asyncio
async def test_parent_child_exact_union_cross_page_exclusion_and_real_association(module_range):
    db, app, _ = module_range
    body = dict(moduleMaps=dict(parent=full(), child=full('range-0', 'range-22'), sibling=partial('sibling-case')),
        condition=dict(priority='P1'))
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        response = await client.post(BASE+'/candidates/selection', json=body)
        assert response.status_code == 200, response.text
        data = response.json()['data']
        assert data['count'] == 23 and data['excludedCount'] == 2
        assert data['moduleCounts'] == dict(parent=dict(total=1, selected=1), child=dict(total=23, selected=21),
            sibling=dict(total=1, selected=1), unassigned=dict(total=1, selected=0))
        assert data['eligibleCount'] == 26 and db.query(CaseVersion).count() == 0
        response = await client.post(BASE+'/associate', json=body)
        assert response.status_code == 200 and response.json()['data']['added'] == 23, response.text
        actual = {row.case_id for row in db.query(PlanCaseRelation).filter_by(plan_id='plan')}
        assert actual == {'case-0', 'case-1', 'parent-case', 'sibling-case'} | {f'range-{i}' for i in range(1, 22)}
        assert (await client.post(BASE+'/candidates/selection', json=body)).json()['data']['count'] == 0
        assert (await client.post(BASE+'/associate', json=body)).status_code == 409
    assert db.query(TaskQueue).count() == db.query(CaseVersion).count() == 0


@pytest.mark.asyncio
async def test_global_selection_override_unassigned_and_filter_literal(module_range):
    db, app, _ = module_range
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        async def count(maps, condition=None):
            response = await client.post(BASE+'/candidates/selection', json=dict(moduleMaps=maps, condition=condition or dict(priority='P1')))
            assert response.status_code == 200, response.text
            return response.json()['data']
        assert (await count(dict(all=full(), child=dict(selectAll=False))))['count'] == 3
        assert (await count(dict(all=full(), unassigned=dict(selectAll=False))))['count'] == 25
        assert (await count(dict(all=full('no-module'), sibling=partial('sibling-case'))))['excludedCount'] == 1
        assert (await count(dict(child=full()), dict(search='%_')))['count'] == 23
        assert (await count(dict(parent=full()), dict(search='%_')))['count'] == 0
        assert (await count(dict(child=full('foreign', 'no-module'))))['excludedCount'] == 0
        assert (await count(dict(unassigned=full())))['count'] == 1
        db.get(Case, 'no-module').priority = 'P0'; db.commit()
        assert (await count(dict(unassigned=full()), dict(priority='P1')))['count'] == 0


@pytest.mark.asyncio
@pytest.mark.parametrize('category', ['api', 'scenario'])
async def test_native_category_and_explicit_module_move_reject_atomic(module_range, category):
    db, app, _ = module_range
    db.add_all([Case(id=f'{category}-{i}', project_id='project', name='原生候选', case_code=f'N-{i}', type=category,
        steps=[], is_automated=True, module_id='child' if i < 2 else 'sibling', created_by='owner') for i in range(3)])
    db.commit()
    body = dict(category=category, moduleMaps=dict(child=full(f'{category}-0'), sibling=partial(f'{category}-2')))
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        response = await client.post(BASE+'/candidates/selection', json=body)
        assert response.status_code == 200, response.text
        assert response.json()['data']['count'] == response.json()['data']['automatedCount'] == 2
        db.get(Case, f'{category}-2').module_id = 'parent'; db.commit()
        assert (await client.post(BASE+'/associate', json=body)).status_code == 409
        assert db.query(PlanCaseRelation).filter_by(plan_id='plan').count() == 2
        db.get(Case, f'{category}-2').module_id = 'sibling'; db.commit()
        assert (await client.post(BASE+'/associate', json=body)).json()['data']['added'] == 2
        assert db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_schema_foreign_modules_permissions_and_no_partial_write(module_range):
    db, app, identity = module_range
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        for body in [dict(moduleMaps={}), dict(moduleMaps=dict(child=full()), selectAll=True),
            dict(moduleMaps=dict(child=full()), caseIds=['range-1']), dict(moduleMaps=dict(child=full()), condition=dict(folder='child')),
            dict(moduleMaps=dict(child=full()), condition=dict(filters=dict(conditions=[]))),
            dict(moduleMaps=dict(child=full()), condition=dict(mine=True)), dict(moduleMaps=dict(all=partial('range-1'))),
            dict(moduleMaps=dict(child=dict(selectAll='true'))), dict(moduleMaps=dict(child=full('range-1'), parent=partial('range-1'))),
            dict(moduleMaps=dict(child=dict(selectAll=True, selectIds=['range-1']))),
            dict(moduleMaps=dict(child=dict(selectIds=['range-1'], count=1)))]:
            assert (await client.post(BASE+'/associate', json=body)).status_code == 422, body
        for maps, expected in [(dict(child=full(), other=full()),404), (dict(child=full(), sibling=partial('foreign')),404),
            (dict(child=full(), sibling=partial('range-1')),409), (dict(child=partial('case-0')),409)]:
            assert (await client.post(BASE+'/associate', json=dict(moduleMaps=maps))).status_code == expected
            assert db.query(PlanCaseRelation).filter_by(plan_id='plan').count() == 2
        identity['id'] = 'stranger'
        assert (await client.post(BASE+'/candidates/selection', json=dict(moduleMaps=dict(child=full())))).status_code == 403
        assert (await client.post(BASE+'/associate', json=dict(moduleMaps=dict(child=full())))).status_code == 403


def test_new_case_current_scope_deleted_module_and_transaction_failure(module_range, monkeypatch):
    db, _, _ = module_range
    owner, plan = db.get(User, 'owner'), db.get(Plan, 'plan')
    body = Association(moduleMaps=dict(child=full('range-22')))
    assert preview(db, plan, owner, body)['count'] == 22
    db.add(Case(id='late', project_id='project', name='预览后新增', case_code='LATE', type='functional', steps=[],
        is_automated=False, module_id='child', created_by='owner')); db.commit()
    db.get(Case, 'range-0').module_id = 'sibling'; db.commit()
    assert preview(db, plan, owner, body)['count'] == 22
    original = db.commit
    def failed_commit():
        raise RuntimeError('模拟模块组合提交失败')
    monkeypatch.setattr(db, 'commit', failed_commit)
    with pytest.raises(RuntimeError, match='模拟模块组合提交失败'):
        transact(db, lambda: associate(db, plan, owner, body))
    assert db.query(PlanCaseRelation).count() == 2
    monkeypatch.setattr(db, 'commit', original)
    db.query(Case).filter_by(module_id='child').update({'module_id': None}); db.delete(db.get(Module, 'child')); db.commit()
    with pytest.raises(HTTPException) as error:
        transact(db, lambda: associate(db, plan, owner, body))
    assert error.value.status_code == 404 and db.query(PlanCaseRelation).count() == 2


def test_module_limit_uses_entire_range_and_exclusion_boundary(module_range):
    db, _, _ = module_range
    db.bulk_save_objects([Case(id=f'cap-{i}', project_id='project', name='完整模块上限', case_code=f'CAP-{i}',
        type='functional', steps=[], module_id='child', created_by='owner', is_automated=False) for i in range(9978)])
    db.commit()
    owner, plan = db.get(User, 'owner'), db.get(Plan, 'plan')
    with pytest.raises(HTTPException) as error:
        preview(db, plan, owner, Association(moduleMaps=dict(child=full())))
    assert error.value.status_code == 422 and db.query(PlanCaseRelation).count() == 2
    result = preview(db, plan, owner, Association(moduleMaps=dict(child=full('cap-0'))))
    assert result['count'] == 10000 and result['excludedCount'] == 1
    assert result['moduleCounts']['child'] == dict(total=10001, selected=10000)
    assert db.query(TaskQueue).count() == 0
