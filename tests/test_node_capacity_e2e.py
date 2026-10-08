"""Capacity across real loopback HTTP, WebSocket, Agent, native HTTP and XAT."""

import pytest

from test_http_agent_e2e import lab, queue_states, until
from test_native_http_agent_e2e import native_lab, scope, dispatch


@pytest.mark.asyncio
async def test_agent_limit_below_backend_limit_queues_xat_behind_real_native_http(
    native_lab,
):
    from database import SessionLocal
    from models import Environment, TestSuite as Suite
    from models.plan_orchestration import PlanRunItem
    from models.task_queue import TaskQueue
    from models.test_suite import TestSuiteExecution
    from services.suite_dispatch import build_suite_message

    value = native_lab
    agent = value["agent"]
    assert agent.config.max_concurrent_tasks == 1
    with SessionLocal() as db:
        db.get(Environment, value["environment"]["id"]).max_concurrent_tasks = 2
        db.commit()
    value["block"]()
    native_run = await scope(value, "api")
    await dispatch(native_run)
    await until(value["entered"].is_set)
    with SessionLocal() as db:
        native = db.query(PlanRunItem).filter_by(run_id=native_run).one()
        native_id, native_suite_id = native.execution_id, native.suite_id
    response = await value["client"].post(
        f'/api/v1/test-plans/suites/{value["suite"]["id"]}/execute'
    )
    assert response.status_code == 200, response.text
    xat_id = next(iter(queue_states(value["suite"]["id"])))
    await until(lambda: xat_id in agent.sat_runner.runs)
    assert xat_id not in agent.sat_runner.started
    assert native_id in agent.native_http_runner.started
    with SessionLocal() as db:
        running = db.query(TaskQueue).filter_by(status="running").all()
        assert len(running) == 2  # Backend reservations; Agent executes only one.
        task = db.query(TaskQueue).filter_by(execution_id=xat_id).one()
        duplicate = build_suite_message(
            db, db.get(Suite, task.suite_id), xat_id, task.executor_id
        )
    # Replayed dispatch while waiting must not create another workload.
    assert await value["manager"].send_message(value["environment"]["id"], duplicate)
    response = await value["client"].post(
        f"/api/v1/test-plans/suites/{native_suite_id}/cancel",
        json={"executionId": native_id},
    )
    assert response.status_code == 200, response.text
    await until(lambda: queue_states(native_suite_id).get(native_id) == "cancelled")
    value["release"].set()
    await until(lambda: queue_states(value["suite"]["id"]).get(xat_id) == "completed")
    await until(lambda: not agent.execution_admission.tickets)
    with SessionLocal() as db:
        rows = (
            db.query(TestSuiteExecution).filter_by(suite_id=value["suite"]["id"]).all()
        )
        assert len(rows) == 4 and all(row.result == "passed" for row in rows)
    assert not agent.sat_runner.runs and not agent.native_http_runner.runs


@pytest.mark.asyncio
async def test_never_delivered_direct_dispatch_recovers_through_scoped_cancel(
    lab, monkeypatch
):
    from database import SessionLocal
    from models.task_queue import TaskQueue

    manager = lab["manager"]
    original_send = manager.send_message
    dropped = []

    async def drop_execute(environment_id, payload):
        if payload["type"] == "execute_test_suite":
            dropped.append(payload["execution_id"])
            return False
        return await original_send(environment_id, payload)

    monkeypatch.setattr(manager, "send_message", drop_execute)
    path = f'/api/v1/test-plans/suites/{lab["suite"]["id"]}'
    response = await lab["client"].post(path + "/execute")
    assert response.status_code == 503
    execution_id = dropped[0]
    assert queue_states(lab["suite"]["id"])[execution_id] == "running"
    assert execution_id not in lab["agent"].execution_admission.seen
    response = await lab["client"].post(
        path + "/cancel", json={"executionId": execution_id}
    )
    assert response.status_code == 200
    await until(lambda: queue_states(lab["suite"]["id"])[execution_id] == "cancelled")
    monkeypatch.setattr(manager, "send_message", original_send)
    response = await lab["client"].post(path + "/execute")
    assert response.status_code == 200
    await until(lambda: "completed" in queue_states(lab["suite"]["id"]).values())
    with SessionLocal() as db:
        assert db.query(TaskQueue).filter_by(status="running").count() == 0
    marker = lab["agent"].work_dir / "execution-admission" / (execution_id + ".json")
    assert marker.exists()
