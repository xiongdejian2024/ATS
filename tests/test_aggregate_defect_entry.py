from uuid import uuid4
import httpx
import pytest
from models import TaskQueue, ProjectMember
from models.plan_workspace import PlanWorkspace
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab


@pytest.mark.asyncio
async def test_aggregate_entry_capabilities_use_plan_instance_authority(workspace_http):
    db, app, identity = workspace_http
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        base = '/orchestration/plans/plan/case-workspace'
        before = (await client.get(base + '/defects/aggregate')).json()['data']
        assert before['canCreate'] and before['canAssociate']
        rows = (await client.get(base, params={'category': 'functional'})).json()['data']['items']
        first = rows[0]['id']
        created = await client.post(base + '/defects', json=dict(selectIds=[first], title='聚合页实例缺陷', description='', requestId=str(uuid4())))
        assert created.status_code == 200, created.text
        output = (await client.get(base + '/defects/aggregate')).json()['data']
        assert output['items'][0]['cases'][0]['associationKey'] == first
        db.add(PlanWorkspace(plan_id='plan', archived=True)); db.commit()
        archived = (await client.get(base + '/defects/aggregate')).json()['data']
        assert not archived['canCreate'] and not archived['canAssociate']
        identity['id'] = 'stranger'
        assert (await client.get(base + '/defects/aggregate')).status_code == 403
    assert db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_aggregate_execute_only_capability(workspace_http):
    from models.role import Permission, ProjectPermission
    db, app, identity = workspace_http
    db.add(ProjectMember(project_id='project', user_id='stranger', role='member'))
    db.add(Permission(id='aggregate-execute', code='test_plan:execute', resource='test_plan', action='execute', name='execute'))
    db.flush()
    db.add(ProjectPermission(project_id='project', user_id='stranger', permission_id='aggregate-execute'))
    db.commit(); identity['id'] = 'stranger'
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        data = (await client.get('/orchestration/plans/plan/case-workspace/defects/aggregate')).json()['data']
        assert data['canAssociate'] and not data['canCreate']
        assert not data['canEdit']
