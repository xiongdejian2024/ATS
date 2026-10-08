"""One environment slot is shared by every backend dispatch source."""

import pytest

from models import Environment
from services.task_queue_service import TaskQueueService
from test_plan_orchestration import plan_lab


def test_start_task_rechecks_capacity_after_stale_advisory_check(plan_lab):
    db, _ = plan_lab
    db.get(Environment, "node").max_concurrent_tasks = 1
    db.commit()
    # Two requests can both observe capacity before either inserts its queue row.
    assert TaskQueueService.can_execute_immediately(db, "node")
    assert TaskQueueService.can_execute_immediately(db, "node")
    for execution_id in ("first", "second"):
        TaskQueueService.add_to_queue(db, "node", "suite-0", execution_id, "owner")
    assert TaskQueueService.start_task(db, "first")
    assert TaskQueueService.start_task(db, "second") is None
    assert TaskQueueService.get_running_task_count(db, "node") == 1


def test_overlapping_sessions_and_duplicate_claims_share_slot(plan_lab):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    from database import SessionLocal

    db, _ = plan_lab
    db.get(Environment, "node").max_concurrent_tasks = 1
    db.commit()
    for execution_id in ("first", "second"):
        TaskQueueService.add_to_queue(db, "node", "suite-0", execution_id, "owner")
    barrier = Barrier(4)

    def claim(execution_id):
        with SessionLocal() as session:
            assert TaskQueueService.can_execute_immediately(session, "node")
            barrier.wait(timeout=5)
            row = TaskQueueService.start_task(session, execution_id)
            return row.execution_id if row else None

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(claim, ["first", "second", "first", "second"]))
    assert len([value for value in results if value]) == 1
    assert TaskQueueService.get_running_task_count(db, "node") == 1
    winner = next(value for value in results if value)
    loser = "first" if winner == "second" else "second"
    TaskQueueService.complete_task(db, winner, "completed")
    assert TaskQueueService.start_task(db, loser)
    assert TaskQueueService.start_task(db, winner) is None


def test_stale_completion_cannot_overwrite_terminal_state(plan_lab):
    from database import SessionLocal
    from models.task_queue import TaskQueue

    db, _ = plan_lab
    TaskQueueService.add_to_queue(db, "node", "suite-0", "first", "owner")
    TaskQueueService.start_task(db, "first")
    with SessionLocal() as stale:
        old = stale.query(TaskQueue).filter_by(execution_id="first").one()
        assert old.status == "running"
        TaskQueueService.complete_task(db, "first", "completed")
        assert TaskQueueService.complete_task(stale, "first", "cancelled") is None
        assert old.status == "completed"


@pytest.mark.asyncio
async def test_failed_delivery_keeps_slot_and_reconnect_does_not_replay(
    plan_lab, monkeypatch
):
    from api.v1.websocket import manager
    from models.task_queue import TaskQueue
    from services.queued_dispatch import dispatch_pending_suites

    db, _ = plan_lab
    db.get(Environment, "node").max_concurrent_tasks = 1
    db.commit()
    for execution_id in ("first", "second"):
        TaskQueueService.add_to_queue(db, "node", "suite-0", execution_id, "owner")
    attempted = []

    async def uncertain(environment_id, message):
        attempted.append(message["execution_id"])
        return False

    monkeypatch.setattr(manager, "send_message", uncertain)
    await dispatch_pending_suites(db, "node")
    await dispatch_pending_suites(db, "node")  # reconnect/callback retry
    assert attempted == ["first"]
    assert db.query(TaskQueue).filter_by(execution_id="first").one().status == "running"
    assert (
        db.query(TaskQueue).filter_by(execution_id="second").one().status == "pending"
    )
    TaskQueueService.complete_task(db, "first", "cancelled")
    await dispatch_pending_suites(db, "node")
    assert attempted == ["first", "second"]


@pytest.mark.asyncio
async def test_lost_queue_claim_never_sends(plan_lab, monkeypatch):
    from services.queued_dispatch import dispatch_pending_suites

    db, sent = plan_lab
    TaskQueueService.add_to_queue(db, "node", "suite-0", "first", "owner")
    monkeypatch.setattr(TaskQueueService, "start_task", lambda *args, **kwargs: None)
    await dispatch_pending_suites(db, "node")
    assert not sent


@pytest.mark.asyncio
async def test_queued_job_rechecks_revoked_executor_before_dispatch(plan_lab):
    from models import User
    from models.task_queue import TaskQueue
    from services.queued_dispatch import dispatch_pending_suites

    db, sent = plan_lab
    TaskQueueService.add_to_queue(db, "node", "suite-0", "first", "owner")
    db.get(User, "owner").status = False
    db.commit()
    await dispatch_pending_suites(db, "node")
    assert not sent
    assert db.query(TaskQueue).filter_by(execution_id="first").one().status == "failed"


@pytest.mark.asyncio
async def test_pending_cancel_losing_to_dispatch_keeps_slot_and_sends_cancel(
    plan_lab, monkeypatch
):
    from api.v1.test_suites import cancel_test_suite
    from database import SessionLocal
    from models import User
    from models.task_queue import TaskQueue
    from schemas.test_suite import TestSuiteCancelRequest
    from utils.datetime_utils import beijing_now

    db, sent = plan_lab
    db.get(Environment, "node").last_heartbeat = beijing_now()
    db.commit()
    TaskQueueService.add_to_queue(db, "node", "suite-0", "first", "owner")
    original_lock = TaskQueueService.lock_environment
    moved = False

    def concurrent_dispatch(session, environment_id):
        nonlocal moved
        if not moved:
            moved = True
            with SessionLocal() as other:
                # Model a completed competing claim before this cancellation
                # obtains the environment lock; no foreign process is launched.
                other.query(TaskQueue).filter_by(execution_id="first").update(
                    {"status": "running"}
                )
                other.commit()
        return original_lock(session, environment_id)

    monkeypatch.setattr(TaskQueueService, "lock_environment", concurrent_dispatch)
    await cancel_test_suite(
        "suite-0",
        TestSuiteCancelRequest(executionId="first"),
        db,
        db.get(User, "owner"),
    )
    row = db.query(TaskQueue).filter_by(execution_id="first").one()
    assert row.status == "running" and row.completed_at is None
    assert [payload["type"] for _, payload in sent] == ["cancel_test_suite"]


@pytest.mark.asyncio
async def test_legacy_last_case_row_does_not_release_running_slot(plan_lab):
    from api.v1.websocket import handle_test_suite_result
    from models import TestSuite as Suite
    from models.test_suite import TestSuiteLog
    from models.task_queue import TaskQueue
    from utils.datetime_utils import beijing_now

    db, sent = plan_lab
    suite = db.get(Suite, "suite-0")
    suite.execution_command = "echo legacy"
    suite.status = "running"
    db.get(Environment, "node").max_concurrent_tasks = 1
    db.add(
        TestSuiteLog(
            suite_id=suite.id,
            execution_id="legacy",
            message="started",
            timestamp=beijing_now(),
        )
    )
    db.commit()
    TaskQueueService.add_to_queue(db, "node", "suite-0", "legacy", "owner")
    TaskQueueService.start_task(db, "legacy")
    TaskQueueService.add_to_queue(db, "node", "suite-0", "next", "owner")
    await handle_test_suite_result(
        db,
        "node",
        dict(
            suite_id=suite.id,
            case_id="case-0",
            executor_id="owner",
            result="passed",
            duration="0.1s",
        ),
    )
    assert (
        db.query(TaskQueue).filter_by(execution_id="legacy").one().status == "running"
    )
    assert db.query(TaskQueue).filter_by(execution_id="next").one().status == "pending"
    assert not sent


@pytest.mark.asyncio
async def test_simultaneous_direct_plan_scheduler_and_reconnect_dispatch_share_capacity(
    plan_lab,
):
    import asyncio
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    from types import SimpleNamespace
    from database import SessionLocal
    from models import User
    from models.task_queue import TaskQueue
    from services.plan_orchestration import start_plan_run, advance_plan_runs
    from services.task_scheduler import (
        create_schedule,
        trigger_schedule,
        dispatch_pending,
    )
    from services.queued_dispatch import dispatch_pending_suites
    from api.v1.test_suites import execute_test_suite
    from utils.datetime_utils import beijing_now

    db, sent = plan_lab
    environment = db.get(Environment, "node")
    environment.max_concurrent_tasks = 1
    environment.last_heartbeat = beijing_now()
    db.commit()
    await start_plan_run(db, "plan", "owner")
    user = db.get(User, "owner")
    schedule = create_schedule(
        db,
        user,
        SimpleNamespace(
            project_id="project",
            name="capacity test",
            target_type="suite",
            target_id="suite-0",
            cron_expression=None,
            timezone="UTC",
        ),
    )
    await trigger_schedule(db, user, schedule, "first")
    TaskQueueService.add_to_queue(db, "node", "suite-0", "reconnect", "owner")
    barrier = Barrier(4)

    def dispatch(kind):
        with SessionLocal() as session:
            barrier.wait(timeout=5)
            if kind == "direct":
                asyncio.run(
                    execute_test_suite("suite-0", session, session.get(User, "owner"))
                )
            elif kind == "plan":
                asyncio.run(advance_plan_runs(session))
            elif kind == "scheduler":
                asyncio.run(dispatch_pending(session))
            else:
                asyncio.run(dispatch_pending_suites(session, "node"))

    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(dispatch, ["direct", "plan", "scheduler", "reconnect"]))
    db.expire_all()
    running = db.query(TaskQueue).filter_by(status="running").all()
    assert len(running) == 1
    assert len(sent) == 1
    assert sent[0][1]["execution_id"] == running[0].execution_id
    assert db.query(TaskQueue).filter_by(status="pending").count() == 3
