"""Fault injection for overlapping sockets, stale frames and bounded liveness."""

import asyncio
import json
from datetime import timedelta

import httpx
import pytest
import pytest_asyncio
from fastapi import WebSocketDisconnect

from agent.websocket_client import WebSocketClient
from test_http_agent_e2e import until


class Socket:
    def __init__(self, version="2"):
        self.query_params = {} if version is None else {"protocol_version": version}
        self.incoming = asyncio.Queue()
        self.sent = []
        self.closed = []
        self.sending = asyncio.Event()
        self.release_send = None
        self.fail_send = False

    async def accept(self):
        pass

    async def receive_text(self):
        value = await self.incoming.get()
        if isinstance(value, Exception):
            raise value
        return value if isinstance(value, str) else json.dumps(value)

    async def send_json(self, payload):
        self.sending.set()
        if self.release_send:
            await self.release_send.wait()
        if self.fail_send:
            raise OSError("injected lost transport")
        self.sent.append(payload)

    async def close(self, code=1000, reason=""):
        # Deliberately keep receive half-open after close: an old buffered frame
        # and its late finalizer can arrive after the new socket is established.
        self.closed.append((code, reason))

    def frame(self, payload, session=None):
        if session:
            payload = dict(payload, session_id=session.session_id, protocol_version=2)
        self.incoming.put_nowait(payload)


@pytest_asyncio.fixture
async def controller(monkeypatch):
    import main  # noqa: F401; initialize routes before replacing the manager
    import api.v1.websocket as endpoint
    from database import SessionLocal
    from models.environment import Environment
    from services.agent_connections import ConnectionManager

    with SessionLocal() as db:
        db.add(
            Environment(
                id="node", name="fenced node", token="node-token", os_type="Linux"
            )
        )
        db.commit()
    manager = ConnectionManager()
    monkeypatch.setattr(endpoint, "manager", manager)
    tasks = []

    async def connect(version="2"):
        socket = Socket(version)
        task = asyncio.create_task(endpoint.websocket_endpoint(socket, "node-token"))
        tasks.append((task, socket))
        if version not in {None, "1", "2"}:
            await task
            return socket, None, task
        await until(lambda: len(socket.sent) >= 2)
        return socket, manager.sessions["node"], task

    yield endpoint, manager, connect
    for task, socket in tasks:
        socket.incoming.put_nowait(WebSocketDisconnect())
    await asyncio.gather(*(task for task, _ in tasks), return_exceptions=True)
    await manager.aclose()


def node():
    from database import SessionLocal
    from models.environment import Environment

    with SessionLocal() as db:
        value = db.get(Environment, "node")
        return value.is_online, value.node_ip, value.os_type, value.last_heartbeat


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "kind", ["heartbeat", "test_suite_result", "test_suite_completed", "test_suite_log"]
)
@pytest.mark.parametrize("version", ["2", None])
async def test_replaced_socket_cannot_mutate_ack_or_mark_new_offline(
    controller, monkeypatch, kind, version
):
    endpoint, manager, connect = controller
    calls = []

    async def handler(*args):
        calls.append(args)
        return True

    for name in [
        "handle_test_suite_result",
        "handle_test_suite_completed",
        "handle_test_suite_log",
    ]:
        monkeypatch.setattr(endpoint, name, handler)
    old, old_session, old_task = await connect(version)
    new, new_session, _ = await connect()
    assert new_session.session_id != old_session.session_id
    assert not manager.disconnect("node", old_session)
    before = node()
    old.frame(
        {"type": kind, "data": {"node_ip": "stale"}, "event_id": "old-event"},
        old_session if version else None,
    )
    await asyncio.wait_for(old_task, 2)
    assert manager.sessions["node"] is new_session
    assert manager.active_connections["node"] is new
    assert manager.token_to_env == {"node-token": "node"}
    assert node() == before and node()[0] is True
    assert calls == []
    assert [p["type"] for p in old.sent] == ["welcome", "auth_success"]
    new.frame({"type": "heartbeat", "data": {"node_ip": "fresh"}}, new_session)
    await until(lambda: node()[1] == "fresh")
    assert node()[2] == "Linux"  # liveness-only updates preserve inventory
    await until(lambda: new.sent[-1]["type"] == "heartbeat_ack")


@pytest.mark.asyncio
async def test_failed_old_send_cannot_remove_replacement(controller):
    _, manager, connect = controller
    old, old_session, _ = await connect()
    old.sending.clear()
    old.release_send = asyncio.Event()
    old.fail_send = True
    sending = asyncio.create_task(manager.send_session(old_session, {"type": "task"}))
    await old.sending.wait()
    new, new_session, _ = await connect()
    old.release_send.set()
    assert await sending is False
    assert manager.is_current(new_session) and manager.active_connections["node"] is new
    assert node()[0] is True


@pytest.mark.asyncio
async def test_replacement_waits_for_already_admitted_handler(controller, monkeypatch):
    endpoint, manager, connect = controller
    entered, finish = asyncio.Event(), asyncio.Event()

    async def result(*args):
        entered.set()
        await finish.wait()
        return True

    monkeypatch.setattr(endpoint, "handle_test_suite_result", result)
    old, old_session, _ = await connect()
    old.frame(
        {"type": "test_suite_result", "event_id": "committed-before-replace"},
        old_session,
    )
    await entered.wait()
    replacing = asyncio.create_task(connect())
    await asyncio.sleep(0.02)
    assert manager.sessions["node"] is old_session
    finish.set()
    _, new_session, _ = await replacing
    assert manager.sessions["node"] is new_session
    assert old.sent[-1]["event_id"] == "committed-before-replace"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "frame",
    [
        "not json",
        "[]",
        "null",
        '{"type":{}}',
        {"type": "unknown"},
        {"type": "heartbeat", "data": []},
        {
            "type": "test_suite_result",
            "event_id": "bad-session",
            "session_id": "stale",
            "protocol_version": 2,
        },
    ],
)
async def test_invalid_or_wrong_session_frames_never_ack(controller, frame):
    _, manager, connect = controller
    socket, session, task = await connect()
    if isinstance(frame, dict) and "session_id" not in frame:
        socket.frame(frame, session)
    else:
        socket.frame(frame)
    await asyncio.wait_for(task, 2)
    assert not manager.sessions
    assert node()[0] is False
    assert not any(p["type"] == "sat_event_ack" for p in socket.sent)
    assert socket.closed


@pytest.mark.asyncio
async def test_unsupported_protocol_does_not_evict_current(controller):
    _, manager, connect = controller
    _, session, _ = await connect()
    bad, _, _ = await connect("999")
    assert manager.is_current(session) and node()[0] is True
    assert bad.closed == [(1002, "Unsupported Agent protocol")]


@pytest.mark.asyncio
async def test_unresponsive_agent_expires_even_when_ping_send_succeeds(
    controller, monkeypatch
):
    endpoint, manager, connect = controller
    manager.heartbeat_timeout = 0.5
    monkeypatch.setattr(endpoint, "PING_INTERVAL", 0.02)
    socket, _, task = await connect()
    await asyncio.wait_for(task, 1)
    assert any(p["type"] == "ping" for p in socket.sent)
    assert not manager.sessions and node()[0] is False


@pytest.mark.asyncio
async def test_pong_keeps_online_until_socket_ends(controller, monkeypatch):
    endpoint, manager, connect = controller
    manager.heartbeat_timeout = 0.5
    monkeypatch.setattr(endpoint, "PING_INTERVAL", 0.02)
    socket, session, task = await connect()
    for _ in range(5):
        await asyncio.sleep(0.15)
        socket.frame({"type": "pong"}, session)
    assert not task.done() and manager.is_live(session) and node()[0]
    socket.incoming.put_nowait(WebSocketDisconnect())
    await task
    assert node()[0] is False


@pytest.mark.asyncio
async def test_http_heartbeat_requires_current_token_and_session(controller):
    from main import app

    _, manager, connect = controller
    socket, session, _ = await connect()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        path = "/api/v1/environments/node/heartbeat"
        for headers, status in [
            ({}, 401),
            ({"Authorization": "Bearer wrong"}, 401),
            ({"Authorization": "Bearer node-token"}, 409),
            (
                {"Authorization": "Bearer node-token", "X-Agent-Session-ID": "stale"},
                409,
            ),
        ]:
            response = await client.post(path, headers=headers, json={"node_ip": "bad"})
            assert response.status_code == status
            assert node()[1] is None
        response = await client.post(
            path,
            headers={
                "Authorization": "Bearer node-token",
                "X-Agent-Session-ID": session.session_id,
            },
            json={"node_ip": "valid"},
        )
        assert response.status_code == 200 and node()[1] == "valid"
        manager.disconnect("node", session)
        response = await client.post(
            path,
            headers={
                "Authorization": "Bearer node-token",
                "X-Agent-Session-ID": session.session_id,
            },
            json={"node_ip": "bad"},
        )
        assert response.status_code == 401 and not node()[0]


def test_database_expiry_and_controller_restart_reset():
    from database import SessionLocal
    from models.environment import Environment
    from services.agent_connections import ConnectionManager
    from services.environment_service import EnvironmentService
    from core.agent_protocol import HEARTBEAT_TIMEOUT
    from utils.datetime_utils import beijing_now

    with SessionLocal() as db:
        item = Environment(
            id="node",
            name="node",
            is_online=True,
            last_heartbeat=beijing_now() - timedelta(seconds=HEARTBEAT_TIMEOUT + 1),
        )
        db.add(item)
        db.commit()
        assert not EnvironmentService.check_node_status(db, "node")["is_online"]
        item.is_online = True
        item.last_heartbeat = beijing_now()
        db.commit()
    ConnectionManager.reset_online_status()
    assert node()[0] is False


class ClientSocket:
    def __init__(self, session="one"):
        self.session = session
        self.incoming = asyncio.Queue()
        for kind in ["welcome", "auth_success"]:
            self.incoming.put_nowait(
                json.dumps({"type": kind, "session_id": session, "protocol_version": 2})
            )
        self.sent = []
        self.closed = 0
        self.fail = False
        self.sending = asyncio.Event()
        self.release = None

    async def recv(self):
        return await self.incoming.get()

    async def send(self, text):
        self.sending.set()
        if self.release:
            await self.release.wait()
        if self.fail:
            raise OSError("lost socket")
        self.sent.append(json.loads(text))

    async def close(self):
        self.closed += 1


@pytest.mark.asyncio
async def test_client_connect_requires_authenticated_session_and_binds_replay(
    monkeypatch,
):
    socket = ClientSocket()

    async def dial(*args, **kwargs):
        return socket

    monkeypatch.setattr("agent.websocket_client.websockets.connect", dial)
    calls = []

    async def ready():
        calls.append("ready")

    client = WebSocketClient("ws://localhost/ws/agent", "token", on_connect=ready)
    assert "protocol_version=2" in client._build_url()
    assert await client.connect()
    assert calls == ["ready"]
    event = {
        "type": "test_suite_result",
        "event_id": "durable-id",
        "session_id": "dead",
    }
    assert await client.send_message(event)
    assert socket.sent[-1]["session_id"] == "one"
    assert event["session_id"] == "dead"
    await client.close()


@pytest.mark.asyncio
async def test_client_handshake_failure_keeps_outbox_callback_unrun(monkeypatch):
    socket = ClientSocket()
    socket.incoming = asyncio.Queue()
    socket.incoming.put_nowait(json.dumps({"type": "welcome"}))
    socket.incoming.put_nowait(json.dumps({"type": "auth_success"}))

    async def dial(*args, **kwargs):
        return socket

    monkeypatch.setattr("agent.websocket_client.websockets.connect", dial)

    async def forbidden():
        pytest.fail("Outbox flush ran before authentication")

    client = WebSocketClient("ws://localhost", "token", on_connect=forbidden)
    assert await client.connect() is False
    assert not client.connected and client.session_id is None and socket.closed


@pytest.mark.asyncio
async def test_client_old_send_failure_does_not_clear_new_session(monkeypatch):
    old, new = ClientSocket("old"), ClientSocket("new")
    sockets = iter([old, new])

    async def dial(*args, **kwargs):
        return next(sockets)

    monkeypatch.setattr("agent.websocket_client.websockets.connect", dial)
    client = WebSocketClient("ws://localhost", "token")
    assert await client.connect()
    old.sending.clear()
    old.release = asyncio.Event()
    old.fail = True
    sending = asyncio.create_task(client.send_message({"type": "test_suite_result"}))
    await old.sending.wait()
    client.connected = False
    reconnect = asyncio.create_task(client.connect())
    await until(lambda: client.websocket is new)
    old.release.set()
    assert await sending is False
    assert await reconnect
    assert client.connected and client.websocket is new and client.session_id == "new"
    await client.close()


@pytest.mark.asyncio
@pytest.mark.parametrize("wrong", [False, True])
async def test_client_missing_liveness_or_stale_ack_cannot_reach_handler(
    monkeypatch, wrong
):
    socket = ClientSocket()

    async def dial(*args, **kwargs):
        return socket

    monkeypatch.setattr("agent.websocket_client.websockets.connect", dial)
    received = []

    async def message(payload):
        received.append(payload)

    client = WebSocketClient("ws://localhost", "token", on_message=message)
    assert await client.connect()
    received.clear()
    client.heartbeat_timeout = 0.03
    if wrong:
        socket.incoming.put_nowait(
            json.dumps(
                {
                    "type": "sat_event_ack",
                    "event_id": "keep-outbox",
                    "session_id": "dead",
                    "protocol_version": 2,
                }
            )
        )

    async def pause():
        client._should_reconnect = False

    monkeypatch.setattr(client, "_start_reconnect", pause)
    await asyncio.wait_for(client.receive_messages(), 1)
    assert not received and not client.connected and socket.closed


@pytest.mark.asyncio
async def test_repeated_quick_flaps_increase_backoff(monkeypatch):
    client = WebSocketClient("ws://localhost", "token")
    client.reconnect_delay = 1
    delays = []

    async def sleep(delay):
        delays.append(delay)

    async def failing_connect():
        if len(delays) == 4:
            client._should_reconnect = False
        return False

    monkeypatch.setattr("agent.websocket_client.asyncio.sleep", sleep)
    monkeypatch.setattr("agent.websocket_client.random.uniform", lambda low, high: high)
    monkeypatch.setattr(client, "connect", failing_connect)
    await client._reconnect_loop()
    assert delays == [1, 2, 4, 8]


@pytest.mark.asyncio
async def test_waiting_registration_rechecks_revoked_token(controller):
    endpoint, manager, connect = controller
    from database import SessionLocal
    from models.environment import Environment

    old, session, _ = await connect()
    async with manager.session_lock("node"):
        socket = Socket()
        pending = asyncio.create_task(endpoint.websocket_endpoint(socket, "node-token"))
        await asyncio.sleep(0.02)
        with SessionLocal() as db:
            db.get(Environment, "node").token = "new-token"
            db.commit()
    await asyncio.wait_for(pending, 2)
    assert socket.sent == [] and socket.closed == [(1008, "Environment token revoked")]
    assert manager.is_current(session)


@pytest.mark.asyncio
async def test_token_invalidation_retires_before_notification_io(controller):
    _, manager, connect = controller
    old, session, old_task = await connect()
    old.sending.clear()
    old.release_send = asyncio.Event()
    notifying = asyncio.create_task(manager.disconnect_and_notify("node"))
    await old.sending.wait()
    assert not manager.is_current(session) and not node()[0]
    new, replacement, _ = await connect()
    old.release_send.set()
    await notifying
    assert manager.is_current(replacement) and node()[0]


@pytest.mark.asyncio
async def test_outbox_replay_does_not_block_receive_readiness(sat_config, monkeypatch):
    from agent.agent import Agent

    agent = Agent(sat_config)
    entered, ack = asyncio.Event(), asyncio.Event()

    async def replay():
        entered.set()
        await ack.wait()

    monkeypatch.setattr(agent.sat_runner, "flush", replay)
    await asyncio.wait_for(agent.on_connect(), 0.2)
    await entered.wait()
    assert not agent._result_replay_task.done()
    ack.set()
    await agent._result_replay_task
    await agent.stop()


@pytest.mark.asyncio
async def test_idle_agent_does_not_reserve_database_pool_connection(controller):
    from database import engine

    _, _, connect = controller
    before = engine.pool.checkedout()
    _, _, _ = await connect()
    await asyncio.sleep(0.02)
    assert engine.pool.checkedout() == before


@pytest.mark.asyncio
async def test_agent_initial_controller_outage_enters_retry_path(
    sat_config, monkeypatch
):
    import agent.agent as module

    entered, stop = asyncio.Event(), asyncio.Event()

    class UnavailableClient:
        connected = False

        def __init__(self, **kwargs):
            pass

        async def connect(self):
            return False

        async def receive_messages(self):
            entered.set()
            await stop.wait()

        async def close(self):
            stop.set()

    monkeypatch.setattr(module, "WebSocketClient", UnavailableClient)
    agent = module.Agent(sat_config)
    starting = asyncio.create_task(agent.start())
    await asyncio.wait_for(entered.wait(), 1)
    assert agent.running and not starting.done()
    await agent.stop()
    await starting


@pytest.mark.asyncio
async def test_live_session_deadline_wins_over_throttled_db_timestamp(controller):
    from database import SessionLocal
    from models.environment import Environment
    from services.environment_service import EnvironmentService
    from utils.datetime_utils import beijing_now

    _, manager, connect = controller
    _, session, _ = await connect()
    with SessionLocal() as db:
        item = db.get(Environment, "node")
        item.last_heartbeat = beijing_now() - timedelta(seconds=91)
        db.commit()
        assert manager.is_live(session)
        assert EnvironmentService.check_node_status(db, "node")["is_online"]
