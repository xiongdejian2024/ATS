"""Script HTTP/WS reads share project authority; writers also need node ownership."""
import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect
from core.security import create_access_token
from models import User, ProjectMember
from models.script_job import ScriptJobLog
from services import script_jobs as jobs
from test_script_jobs import script_lab, create
from test_plan_orchestration import plan_lab
from utils.datetime_utils import beijing_now


def headers(user):
    return {"Authorization": "Bearer " + create_access_token({"sub": user})}


@pytest.mark.asyncio
async def test_script_http_ws_export_permissions_and_live_revocation(script_lab):
    import main
    db, user, manager, _, _ = script_lab
    job = create(script_lab)
    manager.active_connections.clear()
    run = await jobs.trigger(db, user, job.id, "permission")
    for identity in ["reader", "stranger"]:
        db.add(User(id=identity, username=identity, email=identity+"@test.local", password_hash="unused"))
    db.flush()
    db.add(ProjectMember(project_id="project", user_id="reader", role="member"))
    db.add(ScriptJobLog(id="raw", script_job_id=job.id, execution_id=run.execution_id, message="private", timestamp=beijing_now()))
    db.commit()
    base = f"/api/v1/script-jobs/{job.id}/runs/{run.execution_id}"
    client = TestClient(main.app)
    for identity, status in [("owner", 200), ("reader", 200), ("stranger", 403)]:
        assert client.get(base, headers=headers(identity)).status_code == status
        assert client.get(base+"/logs", headers=headers(identity)).status_code == status
        assert client.post(base+"/logs/export", headers=headers(identity), json={}).status_code == status
        token = create_access_token({"sub":identity})
        with client.websocket_connect(f"/ws/script-jobs?token={token}&job_id={job.id}&execution_id={run.execution_id}") as socket:
            if status != 200:
                with pytest.raises(WebSocketDisconnect) as error:
                    socket.receive_json()
                assert error.value.code == 1008
            else:
                assert socket.receive_json()["type"] == "connected"
    assert client.post(base+"/cancel", headers=headers("reader"), json={}).status_code == 403
    assert client.post(base+"/resolve", headers=headers("owner"), json={"confirmedStopped":1}).status_code == 422
    token = create_access_token({"sub":"reader"})
    with client.websocket_connect(f"/ws/script-jobs?token={token}&job_id={job.id}&execution_id={run.execution_id}") as socket:
        assert socket.receive_json()["type"] == "connected"
        db.query(ProjectMember).filter_by(project_id="project", user_id="reader").delete(); db.commit()
        socket.send_json({"type":"ping"})
        # The in-flight heartbeat may have been admitted already; no later turn
        # keeps the old identity-map authority after the fresh check.
        with pytest.raises(WebSocketDisconnect) as error:
            first = socket.receive_json()
            assert first["type"] == "pong"
            socket.receive_json()
        assert error.value.code == 1008


@pytest.mark.asyncio
async def test_same_project_foreign_job_run_pair_cannot_read(script_lab):
    import main
    db, user, manager, _, _ = script_lab
    first, second = create(script_lab), create(script_lab)
    manager.active_connections.clear()
    run = await jobs.trigger(db, user, first.id, "pair")
    client = TestClient(main.app)
    base = f"/api/v1/script-jobs/{second.id}/runs/{run.execution_id}"
    assert client.get(base, headers=headers("owner")).status_code == 404
    assert client.post(base+"/logs/export", headers=headers("owner"), json={}).status_code == 404
