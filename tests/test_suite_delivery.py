import pytest
from fastapi import HTTPException
from models import User, Environment, SuiteDelivery, TaskQueue
from models.plan_orchestration import PlanRun, PlanRunItem
from services.task_queue_service import TaskQueueService
from services.suite_delivery import dispatched, resolve, state_json, ResolveSuiteInput
from test_plan_orchestration import plan_lab


def start(db):
    db.get(Environment, "node").created_by = "owner"
    db.commit()
    TaskQueueService.add_to_queue(db, "node", "suite-0", "unknown-execution", "owner")
    return TaskQueueService.start_task(db, "unknown-execution")


def confirmation(): return ResolveSuiteInput(confirmedStopped=True, reason="隔离节点核对：全部相关进程已停止")


def test_failed_dispatch_requires_explicit_proof_and_preserves_results(plan_lab):
    db, _ = plan_lab
    task = start(db)
    dispatched(db, task.execution_id, False)
    user = db.get(User, "owner")
    assert state_json(db, task)["canResolve"]
    with pytest.raises(HTTPException) as error:
        resolve(db, user, "suite-0", task.execution_id, ResolveSuiteInput(confirmedStopped=False, reason="尚未核对"))
    assert error.value.status_code == 400
    assert task.status == "running"
    output = resolve(db, user, "suite-0", task.execution_id, confirmation())
    assert output["result"] == "unknown" and output["closedBy"] == "owner"
    assert task.status == "failed" and task.completed_at is not None
    assert resolve(db, user, "suite-0", task.execution_id, confirmation()) == output
    assert TaskQueueService.complete_task(db, task.execution_id, "completed") is None


def test_node_ownership_and_frozen_environment_are_required(plan_lab):
    db, _ = plan_lab
    task = start(db)
    db.get(Environment, "node").created_by = "different-owner"
    db.commit()
    with pytest.raises(HTTPException) as error:
        resolve(db, db.get(User, "owner"), "suite-0", task.execution_id, confirmation())
    assert error.value.status_code == 403
    assert task.status == "running"


def test_plan_batch_cannot_be_closed_through_ordinary_suite_entrance(plan_lab):
    db, _ = plan_lab
    task = start(db)
    db.add(PlanRun(id="active", plan_id="plan", executor_id="owner", plan_name="frozen", config_snapshot={}, case_snapshot=[], manual_results={}))
    db.flush()
    db.add(PlanRunItem(id="item", run_id="active", suite_id="suite-0", execution_id=task.execution_id,
                       environment_id="node", sequence=1, suite_snapshot={}))
    db.commit()
    assert not state_json(db, task)["canResolve"]
    with pytest.raises(HTTPException) as error:
        resolve(db, db.get(User, "owner"), "suite-0", task.execution_id, confirmation())
    assert error.value.status_code == 409


def test_live_current_session_cannot_be_closed_until_uncertainty(plan_lab, monkeypatch):
    from types import SimpleNamespace
    from api.v1.websocket import manager
    db, _ = plan_lab
    session = SimpleNamespace(session_id="current-session")
    monkeypatch.setattr(manager, "sessions", {"node": session})
    monkeypatch.setattr(manager, "is_live", lambda value: value is session)
    task = start(db)
    dispatched(db, task.execution_id, True)
    assert not state_json(db, task)["canResolve"]
    with pytest.raises(HTTPException): resolve(db, db.get(User, "owner"), "suite-0", task.execution_id, confirmation())
    db.rollback()
    monkeypatch.setattr(manager, "sessions", {"node": SimpleNamespace(session_id="replacement")})
    assert state_json(db, task)["canResolve"]


@pytest.mark.asyncio
async def test_late_completion_and_results_cannot_replace_operator_unknown(plan_lab):
    from api.v1.websocket import handle_test_suite_completed
    from services.suite_results import handle_run_result
    from models import TestSuite as Suite, Notification
    from models.test_suite import TestSuiteExecution as Result
    db, _ = plan_lab
    task = start(db)
    resolve(db, db.get(User, "owner"), "suite-0", task.execution_id, confirmation())
    assert await handle_test_suite_completed(db, "node", dict(suite_id="suite-0", execution_id=task.execution_id, status="completed"))
    assert handle_run_result(db, "node", dict(suite_id="suite-0", execution_id=task.execution_id, case_id="case-0", result="passed"))
    assert db.get(Suite, "suite-0").status == "failed"
    assert db.query(Result).count() == 0
    assert db.query(Notification).count() == 0


@pytest.mark.asyncio
async def test_completion_losing_terminal_compare_and_swap_has_no_success_effect(plan_lab, monkeypatch):
    from api.v1.websocket import handle_test_suite_completed
    from models import TestSuite as Suite, Notification
    db, _ = plan_lab
    task = start(db)
    original = TaskQueueService.complete_task
    def interleaved(session, execution_id, status="completed"):
        resolve(session, session.get(User, "owner"), "suite-0", execution_id, confirmation())
        return original(session, execution_id, status)
    monkeypatch.setattr(TaskQueueService, "complete_task", interleaved)
    assert await handle_test_suite_completed(db, "node", dict(suite_id="suite-0", execution_id=task.execution_id, status="completed"))
    assert db.get(Suite, "suite-0").status == "failed"
    assert db.query(Notification).count() == 0
