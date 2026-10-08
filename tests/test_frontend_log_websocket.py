"""Real route authorization plus loopback HTTP/WS/Agent/XAT log isolation."""

import asyncio
import json

import pytest
import websockets
from fastapi.testclient import TestClient
from starlette.websockets import WebSocket, WebSocketDisconnect

from core.security import create_access_token
from services.frontend_log_stream import FrontendConnectionManager
from test_http_agent_e2e import lab, queue_states, until
from test_plan_orchestration import plan_lab


@pytest.mark.parametrize(
    "identity, suite_id, expected_http",
    [
        ("owner", "suite-0", 200),
        ("reader", "suite-0", 200),
        ("stranger", "suite-0", 403),
        ("writer", "suite-0", 403),
        ("foreign-reader", "suite-0", 403),
        ("disabled", "suite-0", 401),
        ("owner", "missing", 404),
    ],
)
def test_frontend_subscription_matches_http_log_read_policy(
    plan_lab, monkeypatch, identity, suite_id, expected_http
):
    import main
    from models import Permission, Project, ProjectPermission, User

    db, _ = plan_lab
    for user_id in ["reader", "stranger", "writer", "foreign-reader", "disabled"]:
        db.add(
            User(
                id=user_id,
                username=user_id,
                email=f"{user_id}@example.test",
                password_hash="unused",
                status=user_id != "disabled",
            )
        )
    db.add(Project(id="foreign", name="Other project", owner_id="owner"))
    db.add(
        Permission(
            id="read", code="test_plan:read", resource="test_plan", action="read", name="Read plan"
        )
    )
    db.add(
        Permission(
            id="write",
            code="test_plan:update",
            resource="test_plan",
            action="update",
            name="Update plan",
        )
    )
    db.flush()
    for user_id, project_id, permission_id in [
        ("reader", "project", "read"),
        ("writer", "project", "write"),
        ("foreign-reader", "foreign", "read"),
    ]:
        db.add(
            ProjectPermission(user_id=user_id, project_id=project_id, permission_id=permission_id)
        )
    db.commit()
    stream = FrontendConnectionManager()
    monkeypatch.setattr(main, "frontend_manager", stream)
    token = create_access_token({"sub": identity})
    with TestClient(main.app) as client:
        response = client.get(
            f"/api/v1/test-plans/suites/{suite_id}/logs",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == expected_http, response.text
        with client.websocket_connect(f"/ws/client?token={token}&suite_id={suite_id}") as socket:
            if expected_http == 200:
                assert socket.receive_json()["type"] == "connected"
                socket.send_json({"type": "ping"})
                assert socket.receive_json() == {"type": "pong"}
            else:
                with pytest.raises(WebSocketDisconnect) as closed:
                    socket.receive_json()
                assert closed.value.code == 1008
                assert not stream.frontend_connections and not stream._subscribers
    assert not stream.frontend_connections and not stream._tasks


@pytest.mark.parametrize(
    "query",
    [
        "suite_id=suite-0",
        "token=bad&suite_id=suite-0",
        "token=valid",
        "token=deleted&suite_id=suite-0",
    ],
)
def test_invalid_auth_or_subscription_never_registers(plan_lab, monkeypatch, query):
    import main

    stream = FrontendConnectionManager()
    monkeypatch.setattr(main, "frontend_manager", stream)
    query = query.replace("token=valid", "token=" + create_access_token({"sub": "owner"}))
    query = query.replace("token=deleted", "token=" + create_access_token({"sub": "deleted"}))
    with TestClient(main.app) as client:
        with client.websocket_connect("/ws/client?" + query) as socket:
            with pytest.raises(WebSocketDisconnect) as closed:
                socket.receive_json()
            assert closed.value.code == 1008
        assert not stream.frontend_connections and not stream._tasks


@pytest.mark.asyncio
async def test_real_agent_completes_with_stalled_frontend_and_history_recovers(lab, monkeypatch):
    """Only the slow socket send is fault-injected; execution/HTTP/WS/SQL are real."""
    import main
    import api.v1.websocket as routes
    from database import SessionLocal
    from models.test_suite import TestSuiteExecution, TestSuiteLog

    stream = FrontendConnectionManager(send_timeout=0.1, close_timeout=0.1)
    monkeypatch.setattr(main, "frontend_manager", stream)
    monkeypatch.setattr(routes, "frontend_manager", stream)
    blocked = asyncio.Event()
    never_release = asyncio.Event()
    original_send = WebSocket.send_text

    async def send(self, payload):
        if (
            self.scope["path"] == "/ws/client"
            and b"stall=yes" in self.scope["query_string"]
            and json.loads(payload).get("type") == "test_suite_log"
        ):
            blocked.set()
            await never_release.wait()
        await original_send(self, payload)

    monkeypatch.setattr(WebSocket, "send_text", send)
    suite_id = lab["suite"]["id"]
    token = lab["client"].headers["Authorization"].removeprefix("Bearer ")
    base = str(lab["client"].base_url).rstrip("/").replace("http://", "ws://")
    url = f"{base}/ws/client?token={token}&suite_id={suite_id}"
    seen = []

    async def collect(socket):
        async for payload in socket:
            seen.append(json.loads(payload))

    try:
        async with websockets.connect(url + "&stall=yes") as slow, websockets.connect(
            url
        ) as healthy:
            assert json.loads(await slow.recv())["type"] == "connected"
            assert json.loads(await healthy.recv())["type"] == "connected"
            receiving = asyncio.create_task(collect(healthy))
            try:
                response = await lab["client"].post(f"/api/v1/test-plans/suites/{suite_id}/execute")
                assert response.status_code == 200, response.text
                await asyncio.wait_for(blocked.wait(), 5)
                await until(
                    lambda: bool(queue_states(suite_id))
                    and set(queue_states(suite_id).values()) == {"completed"}
                )
                await until(lambda: not list(lab["agent"].sat_runner.outbox.glob("*.json")))
                assert not never_release.is_set()
                with pytest.raises(websockets.exceptions.ConnectionClosedError) as closed:
                    await asyncio.wait_for(slow.recv(), 2)
                assert (
                    closed.value.rcvd.code == 1013 and "reload history" in closed.value.rcvd.reason
                )
                execution_id = next(iter(queue_states(suite_id)))
                with SessionLocal() as db:
                    rows = db.query(TestSuiteExecution).filter_by(suite_id=suite_id).all()
                    assert len(rows) == 4 and all(row.result == "passed" for row in rows)
                    saved = (
                        db.query(TestSuiteLog)
                        .filter_by(suite_id=suite_id, execution_id=execution_id)
                        .one()
                    )
                    saved_id, saved_text = saved.id, saved.message
                await until(
                    lambda: any(
                        event.get("data", {}).get("endOffset") == len(saved_text) for event in seen
                    )
                )
                live = [event["data"] for event in seen if event["type"] == "test_suite_log"]
                offsets = [event["endOffset"] for event in live]
                assert offsets == sorted(offsets) and len(offsets) == len(set(offsets))
                assert "XAT测试框架启动" in saved_text and "执行完成" in saved_text
                # New connection is accepted after retirement, and complete history
                # is fetched explicitly rather than pretending lost frames arrived.
                async with websockets.connect(url) as recovered:
                    assert json.loads(await recovered.recv())["type"] == "connected"
                    history = await lab["client"].get(
                        f"/api/v1/test-plans/suites/{suite_id}/logs", params={"logId": saved_id}
                    )
                    assert history.status_code == 200, history.text
                    assert history.json()["data"]["items"][0]["message"] == saved_text
                    await recovered.send(json.dumps({"type": "ping"}))
                    assert json.loads(await recovered.recv())["type"] == "pong"
            finally:
                receiving.cancel()
                await asyncio.gather(receiving, return_exceptions=True)
        await until(lambda: not stream._tasks and not stream.frontend_connections)
    finally:
        await stream.aclose()
