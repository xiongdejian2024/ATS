from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest
from fastapi import HTTPException
from agent.workspace_manager import WorkspaceManager

@pytest.mark.parametrize('path', ['', '.', '/', 'child/..'])
def test_workspace_root_cannot_be_deleted(tmp_path, path):
    (tmp_path / 'child').mkdir()
    evidence = tmp_path / 'keep.txt'
    evidence.write_text('keep')
    with pytest.raises(Exception, match='根目录'):
        WorkspaceManager(tmp_path).delete_file(path)
    assert evidence.read_text() == 'keep'

def test_workspace_child_can_be_deleted(tmp_path):
    (tmp_path / 'child').mkdir()
    assert WorkspaceManager(tmp_path).delete_file('child')['success']
    assert tmp_path.exists()

@pytest.mark.asyncio
@pytest.mark.parametrize('name', ['list_workspace_files', 'read_workspace_file', 'delete_workspace_file', 'create_workspace_directory'])
async def test_workspace_commands_reject_non_owner_before_forwarding(monkeypatch, name):
    from api.v1 import workspace
    import core.permissions
    monkeypatch.setattr(workspace.EnvironmentService, 'get_environment', lambda *a: {'createdBy':'owner', 'isOnline':True})
    monkeypatch.setattr(core.permissions, 'has_global_permission', lambda *a: False)
    forward = AsyncMock(return_value={})
    monkeypatch.setattr(workspace, 'send_workspace_request', forward)
    with pytest.raises(HTTPException) as error:
        await getattr(workspace, name)(environment_id='node', path='file', db=object(), current_user=SimpleNamespace(id='outsider'))
    assert error.value.status_code == 403
    forward.assert_not_awaited()

@pytest.mark.parametrize('owner, admin', [('owner', False), ('admin', True)])
def test_workspace_owner_and_system_admin_allowed(monkeypatch, owner, admin):
    from api.v1.workspace import require_workspace_owner
    import core.permissions
    monkeypatch.setattr(core.permissions, 'has_global_permission', lambda *a: admin)
    require_workspace_owner(object(), SimpleNamespace(id=owner), {'createdBy':'owner'})
