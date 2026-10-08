"""Real HTTP/WS/Agent/XAT run with a controller-committed, lost log ACK."""

import asyncio

import pytest
from starlette.websockets import WebSocket, WebSocketDisconnect
from loguru import logger

from agent.log_spool import LogSpool, LogDelivery
from test_http_agent_e2e import lab, until, queue_states


@pytest.mark.asyncio
async def test_real_run_replays_persisted_log_after_lost_ack(lab, monkeypatch):
    from database import SessionLocal
    from models.test_suite import TestSuiteLog
    from models.agent_log import AgentLogCursor

    agent, client = lab["agent"], lab["client"]
    agent.log_delivery = LogDelivery(
        LogSpool(agent.work_dir / "logs-e2e.sqlite"),
        agent.ws_client,
        logger,
        retry_seconds=0.03,
    )
    agent.ws_client.on_log_message = agent.log_delivery.enqueue
    # Re-authenticate to negotiate capability from the real controller welcome.
    await agent.ws_client.websocket.close(code=1000)
    await until(
        lambda: agent.log_delivery.capable is True and agent.ws_client.connected
    )
    release = asyncio.Event()
    original_connect = agent.ws_client.connect

    async def controlled_reconnect():
        await release.wait()
        return await original_connect()

    monkeypatch.setattr(agent.ws_client, "connect", controlled_reconnect)
    original_send = WebSocket.send_json
    dropped = asyncio.Event()

    async def drop_first_ack(self, message, *args, **kwargs):
        if message.get("type") == "log_batch_ack" and not dropped.is_set():
            dropped.set()
            await self.close(code=1000)
            raise WebSocketDisconnect(code=1000)
        return await original_send(self, message, *args, **kwargs)

    monkeypatch.setattr(WebSocket, "send_json", drop_first_ack)
    suite_id = lab["suite"]["id"]
    result = await client.post(f"/api/v1/test-plans/suites/{suite_id}/execute")
    assert result.status_code == 200, result.text
    await asyncio.wait_for(dropped.wait(), 10)
    await until(lambda: not agent.ws_client.connected)
    assert agent.log_delivery.spool.usage()["records"] > 0
    with SessionLocal() as db:
        assert db.query(AgentLogCursor).one().through_sequence > 0
        committed = db.query(TestSuiteLog.message).filter_by(suite_id=suite_id).scalar()
        assert committed and "开始 XAT/SAT 执行" in committed
    # Output produced during this outage is queued durably too.
    await until(lambda: bool(list(agent.sat_runner.outbox.glob("*.json"))))
    release.set()
    await until(
        lambda: bool(queue_states(suite_id))
        and set(queue_states(suite_id).values()) == {"completed"}
    )
    await until(lambda: agent.log_delivery.spool.usage()["records"] == 0)
    response = await client.get(f"/api/v1/test-plans/suites/{suite_id}/logs")
    assert response.status_code == 200
    records = response.json()["data"]["items"]
    assert len(records) == 1
    text = records[0]["message"]
    assert text.count("开始 XAT/SAT 执行") == 1
    assert "XAT测试框架启动" in text
    assert "passed" in text
    tail = await client.get(
        f"/api/v1/test-plans/suites/{suite_id}/logs",
        params={"tailChars": 100, "latest": True},
    )
    item = tail.json()["data"]["items"][0]
    assert item["totalChars"] == len(text) and len(item["message"]) <= 100
