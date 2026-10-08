"""Actual Agent re-creation, same-workspace durable replay, current-session ACK."""

import asyncio

import pytest

from agent.agent import Agent
from agent.websocket_client import WebSocketClient
from test_http_agent_e2e import lab, queue_states, until  # noqa: F401 (pytest fixture)


@pytest.mark.asyncio
async def test_restart_replays_outbox_on_new_session(lab):  # noqa: F811
    from database import SessionLocal
    from models.test_suite import TestSuiteExecution

    old = lab["agent"]
    suite_id = lab["suite"]["id"]
    response = await lab["client"].post(f"/api/v1/test-plans/suites/{suite_id}/execute")
    assert response.status_code == 200
    await until(lambda: set(queue_states(suite_id).values()) == {"completed"})
    await until(lambda: not list(old.sat_runner.outbox.glob("*.json")))
    old_session = old.ws_client.session_id
    server_url, token = old.ws_client.server_url, old.ws_client.token
    await old.stop()
    await old.sat_runner.deliver(
        {
            "type": "test_suite_result",
            "suite_id": suite_id,
            "execution_id": next(iter(queue_states(suite_id))),
            "case_id": lab["cases"][0]["id"],
            "result": "passed",
            "duration": "0.001s",
        }
    )
    assert list(old.sat_runner.outbox.glob("*.json"))
    restarted = Agent(old.config)
    restarted.work_dir = old.work_dir
    restarted.ws_client = WebSocketClient(
        server_url,
        token,
        on_message=restarted.on_message,
        on_connect=restarted.on_connect,
        on_disconnect=restarted.on_disconnect,
    )
    receiving = None
    try:
        assert await restarted.ws_client.connect()
        assert restarted.ws_client.session_id != old_session
        receiving = asyncio.create_task(restarted.ws_client.receive_messages())
        await until(lambda: not list(restarted.sat_runner.outbox.glob("*.json")))
        with SessionLocal() as db:
            assert db.query(TestSuiteExecution).count() == 4
        assert not restarted.execution_admission.tickets
    finally:
        await restarted.stop()
        if receiving:
            receiving.cancel()
            await asyncio.gather(receiving, return_exceptions=True)
