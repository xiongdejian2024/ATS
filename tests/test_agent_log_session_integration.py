"""Durable log replay retains the authenticated session boundary."""

import asyncio
import json
import uuid

import pytest
from loguru import logger

from agent.log_spool import LogDelivery, LogSpool
from agent.websocket_client import WebSocketClient
from test_agent_session_fencing import ClientSocket, controller
from test_http_agent_e2e import until


@pytest.mark.asyncio
async def test_log_batch_replacement_fences_writes_and_ack(controller):
    from database import SessionLocal
    from models.agent_log import AgentLogCursor, AgentTaskLog

    _, _, connect = controller
    old, old_session, old_task = await connect()
    current, session, _ = await connect()
    assert all("log_batch_v1" in frame["capabilities"] for frame in current.sent[:2])
    batch = {
        "type": "log_batch",
        "stream_id": str(uuid.uuid4()),
        "records": [
            {
                "sequence": 1,
                "payload": {
                    "type": "task_log",
                    "task_id": "direct",
                    "message": "raw  \n\t",
                    "raw": True,
                },
            }
        ],
    }
    old.frame(batch, old_session)
    await asyncio.wait_for(old_task, 2)
    with SessionLocal() as db:
        assert db.query(AgentTaskLog).count() == db.query(AgentLogCursor).count() == 0
    assert not any(row["type"].startswith("log_batch_") for row in old.sent)
    for replay in range(2):
        current.frame(batch, session)
        await until(
            lambda: len([row for row in current.sent if row["type"] == "log_batch_ack"])
            == replay + 1
        )
    ack = current.sent[-1]
    assert ack["session_id"] == session.session_id and ack["protocol_version"] == 2
    assert ack["through_sequence"] == 1
    with SessionLocal() as db:
        assert db.query(AgentTaskLog).one().message == "raw  \n\t"
        assert db.query(AgentLogCursor).one().through_sequence == 1


@pytest.mark.asyncio
async def test_offline_logs_spool_before_readiness_and_stale_ack_cannot_reclaim(
    tmp_path, monkeypatch
):
    socket = ClientSocket("current")

    async def dial(*args, **kwargs):
        return socket

    monkeypatch.setattr("agent.websocket_client.websockets.connect", dial)
    client = WebSocketClient("ws://localhost", "token")
    spool = LogSpool(tmp_path / "offline.sqlite")
    delivery = LogDelivery(spool, client, logger, retry_seconds=0.01)
    client.on_log_message = delivery.enqueue

    async def message(payload):
        if payload["type"] in {"log_batch_ack", "log_batch_nack"}:
            delivery.acknowledge(payload)

    client.on_message = message
    try:
        assert await client.send_task_log("direct", "info", "offline evidence")
        assert spool.usage()["records"] == 1
        assert await client.connect()
        delivery.negotiate({"capabilities": ["log_batch_v1"]})
        await until(lambda: any(row["type"] == "log_batch" for row in socket.sent))
        batch = next(row for row in socket.sent if row["type"] == "log_batch")
        assert batch["session_id"] == "current" and batch["protocol_version"] == 2
        socket.incoming.put_nowait(
            json.dumps(
                {
                    "type": "log_batch_ack",
                    "stream_id": spool.stream_id,
                    "through_sequence": 1,
                    "session_id": "stale",
                    "protocol_version": 2,
                }
            )
        )

        async def pause():
            client._should_reconnect = False

        monkeypatch.setattr(client, "_start_reconnect", pause)
        await asyncio.wait_for(client.receive_messages(), 1)
        assert spool.usage()["records"] == 1
    finally:
        await delivery.close()
        await client.close()


@pytest.mark.asyncio
async def test_legacy_capability_replay_keeps_session_envelope(monkeypatch):
    socket = ClientSocket("current")

    async def dial(*args, **kwargs):
        return socket

    async def must_not_enqueue(payload):
        raise AssertionError("replay must not re-enqueue its own payload")

    monkeypatch.setattr("agent.websocket_client.websockets.connect", dial)
    client = WebSocketClient("ws://localhost", "token")
    client.on_log_message = must_not_enqueue
    assert await client.connect()
    try:
        assert await client.send_log_legacy(
            {"type": "task_log", "task_id": "direct", "message": "legacy"}
        )
        assert socket.sent[-1]["session_id"] == "current"
        assert socket.sent[-1]["protocol_version"] == 2
    finally:
        await client.close()
