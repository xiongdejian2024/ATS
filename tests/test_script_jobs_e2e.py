"""Real HTTP + session-v2 sockets + Agent + Python/shell processes, no fake cases."""
import asyncio
import uuid
import pytest
import pytest_asyncio
import websockets
import httpx
from loguru import logger
from starlette.websockets import WebSocket, WebSocketDisconnect
from agent.log_spool import LogSpool, LogDelivery
from test_http_agent_e2e import lab, until, queue_states


@pytest.fixture(autouse=True)
def local_http_client(monkeypatch):
    # Loopback integration traffic must never instantiate an unrelated external
    # proxy transport. This affects only this test's explicit local base URL.
    original = httpx.AsyncClient
    def local(*args, **kwargs):
        if str(kwargs.get("base_url", "")).startswith("http://127.0.0.1:"):
            kwargs["trust_env"] = False
        return original(*args, **kwargs)
    monkeypatch.setattr(httpx, "AsyncClient", local)


@pytest_asyncio.fixture
async def scripts(lab):
    from database import SessionLocal
    from models import TestPlan as Plan
    agent = lab["agent"]
    agent.log_delivery = LogDelivery(LogSpool(agent.work_dir / "script-logs.sqlite"), agent.ws_client, logger, retry_seconds=0.03)
    agent.ws_client.on_log_message = agent.log_delivery.enqueue
    agent.log_delivery.negotiate({"capabilities": list(agent.ws_client.server_capabilities)})
    await until(lambda: lab["manager"].sessions[lab["environment"]["id"]].auth_received)
    with SessionLocal() as db:
        project = db.get(Plan, lab["plan"]["id"]).project_id
    async def create(source="print('plain脚本😀')", **kwargs):
        body = dict(projectId=project, name="plain script", environmentId=lab["environment"]["id"],
                    mode="python", script=source, command="", args=[], workDir="", timeoutSeconds=5)
        body.update(kwargs)
        response = await lab["client"].post("/api/v1/script-jobs", json=body)
        assert response.status_code == 200, response.text
        return response.json()["data"]
    async def run(job, request=None):
        response = await lab["client"].post(f'/api/v1/script-jobs/{job["id"]}/runs', json={"requestId":request or str(uuid.uuid4())})
        assert response.status_code == 200, response.text
        return response.json()["data"]
    lab.update(create_script=create, run_script=run)
    yield lab


def run_state(execution_id):
    from database import SessionLocal
    from models import TaskQueue
    from models.script_job import ScriptJobRun
    with SessionLocal() as db:
        run = db.get(ScriptJobRun, execution_id)
        task = db.query(TaskQueue).filter_by(execution_id=execution_id).one()
        return task.status, run.result


@pytest.mark.asyncio
async def test_plain_python_lost_log_and_terminal_ack_replay_raw_export(scripts, monkeypatch):
    from database import SessionLocal
    from models.script_job import ScriptJobLog, ScriptJobRun
    from models import TestSuiteExecution as Execution, TestExecution as CaseExecution
    value, agent = scripts, scripts["agent"]
    original = WebSocket.send_json
    dropped_log, dropped_result = False, False
    async def drop(self, payload, *args, **kwargs):
        nonlocal dropped_log, dropped_result
        if payload.get("type") == "log_batch_ack" and not dropped_log:
            dropped_log = True
            await self.close(code=1000)
            raise WebSocketDisconnect(code=1000)
        if payload.get("type") == "sat_event_ack" and not dropped_result:
            dropped_result = True
            await self.close(code=1000)
            raise WebSocketDisconnect(code=1000)
        return await original(self, payload, *args, **kwargs)
    monkeypatch.setattr(WebSocket, "send_json", drop)
    job = await value["create_script"]("import sys; sys.stdout.write('精确  空白\\r\\n😀')")
    run = await value["run_script"](job, "same-request")
    execution_id = run["executionId"]
    await until(lambda: run_state(execution_id) == ("completed", "success"), timeout=20)
    await until(lambda: dropped_log and dropped_result and not list(agent.sat_runner.outbox.glob("*.json")), timeout=20)
    await until(lambda: agent.log_delivery.spool.usage()["records"] == 0)
    response = await value["client"].post(f'/api/v1/script-jobs/{job["id"]}/runs', json={"requestId":"same-request"})
    assert response.json()["data"]["executionId"] == execution_id
    with SessionLocal() as db:
        log = db.query(ScriptJobLog).one()
        assert log.message == "精确  空白\r\n😀"
        assert db.query(ScriptJobRun).count() == 1
        assert not db.query(Execution).count() and not db.query(CaseExecution).count()
    base = f'/api/v1/script-jobs/{job["id"]}/runs/{execution_id}'
    response = await value["client"].get(base + "/logs")
    assert response.status_code == 200 and response.json()["data"]["items"][0]["message"] == "精确  空白\r\n😀"
    export = (await value["client"].post(base + "/logs/export", json={})).json()["data"]
    assert export["complete"] and "精确  空白\r\n😀" in export["content"]
    token = value["client"].headers["Authorization"].removeprefix("Bearer ")
    url = str(value["client"].base_url).rstrip("/").replace("http://", "ws://")
    async with websockets.connect(f'{url}/ws/script-jobs?token={token}&job_id={job["id"]}&execution_id={execution_id}') as socket:
        assert __import__('json').loads(await socket.recv())["type"] == "connected"


@pytest.mark.asyncio
async def test_real_suite_script_capacity_cancel_then_timeout_and_exit_code(scripts):
    value, agent = scripts, scripts["agent"]
    job = await value["create_script"]("import time; print('started', flush=True); time.sleep(60)")
    run = await value["run_script"](job)
    execution_id = run["executionId"]
    await until(lambda: execution_id in agent.script_job_runner.executors)
    suite_id = value["suite"]["id"]
    response = await value["client"].post(f"/api/v1/test-plans/suites/{suite_id}/execute")
    assert response.status_code == 200
    suite_run = next(iter(queue_states(suite_id)))
    assert queue_states(suite_id)[suite_run] == "pending"
    assert len([ticket for ticket in agent.execution_admission.tickets.values() if ticket.admitted]) == 1
    result = await value["client"].post(f'/api/v1/script-jobs/{job["id"]}/runs/{execution_id}/cancel', json={})
    assert result.status_code == 200, result.text
    await until(lambda: run_state(execution_id) == ("cancelled", "cancelled"))
    await until(lambda: queue_states(suite_id)[suite_run] == "completed")
    timeout = await value["create_script"]("import time;time.sleep(60)", timeoutSeconds=1)
    timed_run = await value["run_script"](timeout)
    await until(lambda: run_state(timed_run["executionId"]) == ("failed", "timeout"))
    shell = await value["create_script"]("printf 'shell-output'; exit 7", mode="shell")
    shell_run = await value["run_script"](shell)
    await until(lambda: run_state(shell_run["executionId"]) == ("failed", "failed"))
    response = await value["client"].get(f'/api/v1/script-jobs/{shell["id"]}/runs/{shell_run["executionId"]}')
    assert response.json()["data"]["exitCode"] == 7
    await until(lambda: not agent.execution_admission.tickets)


@pytest.mark.asyncio
async def test_same_process_reconnect_can_cancel_owned_active_script(scripts):
    value, agent = scripts, scripts["agent"]
    job = await value["create_script"]("import time; print('alive', flush=True); time.sleep(60)", timeoutSeconds=20)
    run = await value["run_script"](job)
    execution_id = run["executionId"]
    await until(lambda: execution_id in agent.script_job_runner.executors)
    original_session = agent.ws_client.session_id
    await agent.ws_client.websocket.close(code=1000)
    await until(lambda: agent.ws_client.connected and agent.ws_client.session_id != original_session)
    response = await value["client"].post(f'/api/v1/script-jobs/{job["id"]}/runs/{execution_id}/cancel', json={})
    assert response.status_code == 200, response.text
    await until(lambda: run_state(execution_id) == ("cancelled", "cancelled"))
    assert execution_id not in agent.script_job_runner.runs
