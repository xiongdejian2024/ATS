import httpx
import pytest
from models.plan_orchestration import PlanRun
from test_plan_orchestration import plan_lab
from test_plan_workspace import workspace_http


@pytest.mark.asyncio
async def test_active_context_matches_frozen_instance_and_preserves_terminal_reports(workspace_http):
    db, app, identity = workspace_http
    for name, phase in [('active', 'running'), ('closed', 'completed')]:
        db.add(PlanRun(id=name, plan_id='plan', executor_id='owner', plan_name='freeze', status=phase,
                       config_snapshot={}, manual_results={}, case_snapshot=[
                           dict(id='case-0', associationId='first-copy', name='frozen first'),
                           dict(id='case-0', associationId='second-copy', name='frozen second')]))
    db.commit()
    base = '/orchestration/plans/plan/active-execution-context'
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        response = await client.get(base, params=dict(source='node', associationId='second-copy', caseId='case-0'))
        data = response.json()['data']
        assert data['total'] == 1 and data['items'][0]['associationId'] == 'second-copy'
        assert data['items'][0]['caseName'] == 'frozen second'
        absent = (await client.get(base, params=dict(source='node', associationId='new-copy', caseId='case-0'))).json()['data']
        assert not absent['items'][0]['frozenSelection']
        identity['id'] = 'stranger'
        assert (await client.get(base)).status_code == 403
    assert db.get(PlanRun, 'closed').status == 'completed'


@pytest.mark.asyncio
async def test_active_context_legacy_fallback_and_bounded_paging(workspace_http):
    db, app, _ = workspace_http
    for index in range(21):
        db.add(PlanRun(id=f'active-{index:02}', plan_id='plan', executor_id='owner', plan_name='frozen',
                       status='queued', config_snapshot={}, manual_results={},
                       case_snapshot=[dict(id='case-0', name='legacy frozen')]))
    db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        base = '/orchestration/plans/plan/active-execution-context'
        legacy = (await client.get(base, params=dict(source='legacy', caseId='case-0', associationId='old'))).json()['data']
        assert legacy['total'] == 21 and len(legacy['items']) == 20
        assert all(row['associationId'] == 'case-0' and row['frozenSelection'] for row in legacy['items'])
        second = (await client.get(base, params=dict(page=2))).json()['data']
        assert len(second['items']) == 1 and not second['items'][0]['frozenSelection']
        tree = (await client.get(base, params=dict(source='node', caseId='case-0', associationId='copy'))).json()['data']
        assert all(not row['frozenSelection'] for row in tree['items'])
        assert (await client.get(base, params=dict(page=0))).status_code == 422
        assert (await client.get(base, params=dict(source='invalid'))).status_code == 422
