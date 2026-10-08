"""Cancellation keeps XAT result delivery open until the Agent completes."""

import pytest
from fastapi import HTTPException

from api.v1.test_suites import cancel_test_suite
from api.v1.websocket import handle_test_suite_completed, manager
from models import Environment, Notification, TestExecution as Execution, User
from models.task_queue import TaskQueue
from models.test_suite import TestSuite as Suite, TestSuiteExecution as SuiteExecution
from schemas.test_suite import TestSuiteCancelRequest as CancelRequest
from services.suite_results import handle_run_result, result_id
from services.task_queue_service import TaskQueueService
from test_plan_orchestration import plan_lab
from utils.datetime_utils import beijing_now


def running_task(db, execution_id="interrupted", command="xat --mode offline"):
    environment = db.get(Environment, "node")
    environment.is_online = True
    environment.last_heartbeat = beijing_now()
    suite = db.get(Suite, "suite-0")
    suite.execution_command = command
    suite.case_ids = ["case-0", "case-1"]
    suite.status = "running"
    task = TaskQueue(
        environment_id="node",
        suite_id=suite.id,
        execution_id=execution_id,
        executor_id="owner",
        status="running",
    )
    db.add(task)
    db.commit()
    return suite, task


def result_message(execution_id):
    return dict(
        type="test_suite_result",
        suite_id="suite-0",
        execution_id=execution_id,
        case_id="case-0",
        result="passed",
        duration="0.125s",
        log_output="Completed before cancellation",
    )


def completion_message(execution_id):
    return dict(
        type="test_suite_completed",
        suite_id="suite-0",
        execution_id=execution_id,
        status="cancelled",
        event_id="completion-" + execution_id,
        reported_case_count=1,
        total_case_count=2,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("command", ["xat --mode offline", "ats-sat --mode offline"])
@pytest.mark.parametrize("scoped", [False, True], ids=["suite-wide", "execution-id"])
async def test_cancel_preserves_rows_before_completion_and_then_resumes_queue(
    plan_lab, command, scoped
):
    db, sent = plan_lab
    db.get(Environment, "node").max_concurrent_tasks = 1
    suite, task = running_task(db, command=command)
    successor = TaskQueue(
        environment_id="node",
        suite_id=suite.id,
        execution_id="successor",
        executor_id="owner",
        status="pending",
    )
    db.add(successor)
    db.commit()
    request = CancelRequest(executionId=task.execution_id if scoped else None)

    await cancel_test_suite(suite.id, request, db, db.get(User, "owner"))

    db.refresh(task)
    db.refresh(successor)
    db.refresh(suite)
    assert task.status == "running"
    assert successor.status == "pending"
    assert suite.status == "running"
    assert not TaskQueueService.can_execute_immediately(db, "node")
    assert [message["type"] for _, message in sent] == ["cancel_test_suite"]

    message = result_message(task.execution_id)
    assert handle_run_result(db, "node", message)
    identifier = result_id(task.execution_id, "case-0")
    assert db.get(SuiteExecution, identifier).result == "passed"
    assert db.get(Execution, identifier).result == "passed"
    assert db.get(SuiteExecution, result_id(task.execution_id, "case-1")) is None

    completion = completion_message(task.execution_id)
    assert await handle_test_suite_completed(db, "node", completion)
    db.refresh(task)
    db.refresh(successor)
    assert task.status == "cancelled"
    assert successor.status == "running"
    assert sent[-1][1]["type"] == "execute_test_suite"
    assert sent[-1][1]["execution_id"] == successor.execution_id
    assert db.get(SuiteExecution, identifier).result == "passed"
    assert db.get(SuiteExecution, result_id(task.execution_id, "case-1")) is None

    # Replayed results and completion remain idempotent after cancellation.
    assert handle_run_result(db, "node", message)
    assert await handle_test_suite_completed(db, "node", completion)
    assert db.query(SuiteExecution).count() == db.query(Execution).count() == 1
    assert db.query(Notification).count() == 1
    assert len(sent) == 2


@pytest.mark.asyncio
async def test_suite_wide_cancel_waits_for_each_running_xat_execution(plan_lab):
    db, sent = plan_lab
    suite, first = running_task(db, "first")
    _, second = running_task(db, "second")

    await cancel_test_suite(suite.id, CancelRequest(), db, db.get(User, "owner"))

    assert {message["execution_id"] for _, message in sent} == {"first", "second"}
    for task in (first, second):
        db.refresh(task)
        assert task.status == "running"
        assert handle_run_result(db, "node", result_message(task.execution_id))
        assert await handle_test_suite_completed(db, "node", completion_message(task.execution_id))
        db.refresh(task)
        assert task.status == "cancelled"
    assert db.query(SuiteExecution).count() == db.query(Execution).count() == 2


@pytest.mark.asyncio
@pytest.mark.parametrize("scoped", [False, True], ids=["suite-wide", "execution-id"])
async def test_failed_cancel_delivery_keeps_running_slot(plan_lab, monkeypatch, scoped):
    db, _ = plan_lab
    suite, task = running_task(db)

    async def disconnected(environment_id, message):
        return False

    monkeypatch.setattr(manager, "send_message", disconnected)
    request = CancelRequest(executionId=task.execution_id if scoped else None)
    with pytest.raises(HTTPException) as error:
        await cancel_test_suite(suite.id, request, db, db.get(User, "owner"))

    assert error.value.status_code == 503
    assert "无法发送取消指令到Agent" in error.value.detail
    db.refresh(task)
    db.refresh(suite)
    assert task.status == suite.status == "running"
    assert task.completed_at is None


@pytest.mark.asyncio
async def test_suite_cancel_does_not_overwrite_completion_during_send(plan_lab, monkeypatch):
    db, _ = plan_lab
    suite, task = running_task(db)

    async def complete_while_sending(environment_id, message):
        assert message["type"] == "cancel_test_suite"
        assert handle_run_result(db, environment_id, result_message(task.execution_id))
        assert await handle_test_suite_completed(
            db, environment_id, completion_message(task.execution_id)
        )
        return True

    monkeypatch.setattr(manager, "send_message", complete_while_sending)
    await cancel_test_suite(suite.id, CancelRequest(), db, db.get(User, "owner"))

    db.refresh(task)
    db.refresh(suite)
    assert task.status == "cancelled"
    assert suite.status == "pending"
    assert db.get(SuiteExecution, result_id(task.execution_id, "case-0")).result == "passed"


@pytest.mark.asyncio
@pytest.mark.parametrize("command", ["pytest test_legacy.py", "ats-native-http"])
async def test_all_running_runners_wait_for_terminal_ack(plan_lab, command):
    db, sent = plan_lab
    suite, task = running_task(db, command=command)

    await cancel_test_suite(suite.id, CancelRequest(), db, db.get(User, "owner"))

    db.refresh(task)
    assert task.status == "running"
    assert task.completed_at is None
    assert sent[-1][1]["type"] == "cancel_test_suite"
    assert await handle_test_suite_completed(db, "node", completion_message(task.execution_id))
    db.refresh(task)
    assert task.status == "cancelled"
    assert task.completed_at is not None
