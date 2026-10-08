"""All claim entrances wait for current Agent capability without consuming a slot."""

from copy import deepcopy
from uuid import uuid4
from datetime import datetime
import pytest
from models import User, TestSuite as Suite, TaskQueue, Environment
from models.plan_orchestration import PlanRunItem
from models.task_schedule import TaskSchedule, TaskScheduleRun
from models.native_case import NativeCaseConfig
from services.task_queue_service import TaskQueueService
from services import native_variable_delivery as delivery
from services.agent_connections import AgentSession
from test_plan_orchestration import plan_lab
from test_plan_native_workspace import native_workspace
from test_plan_workspace import workspace_http
from test_native_http_execution import configure
from services.plan_orchestration import start_plan_run, advance_plan_runs


def payload():
    return dict(
        id="case-0",
        category="api",
        requests=[
            dict(
                url="http://fixture.test/",
                name="request",
                initialVariables=[dict(name="token", value="literal")],
            )
        ],
    )


def capable(monkeypatch):
    from api.v1.websocket import manager

    class Socket:
        def __init__(self):
            self.sent = []

        async def send_json(self, value):
            self.sent.append(value)

    socket = Socket()
    session = AgentSession(
        "node",
        socket,
        None,
        2,
        auth_received=True,
        capabilities=frozenset({delivery.CAPABILITY}),
    )
    monkeypatch.setattr(manager, "sessions", {"node": session})
    monkeypatch.setattr(manager, "active_connections", {"node": socket})
    return socket


@pytest.mark.asyncio
@pytest.mark.parametrize("entrance", ["ordinary", "queued", "schedule"])
async def test_three_suite_entrances_wait_before_claim_and_send_same_session(
    plan_lab, monkeypatch, entrance
):
    from api.v1.websocket import manager
    from api.v1.test_suites import execute_test_suite
    from services.queued_dispatch import dispatch_pending_suites
    from services.task_scheduler import dispatch_pending

    db, legacy_sent = plan_lab
    from utils.datetime_utils import beijing_now

    db.get(Environment, "node").last_heartbeat = beijing_now()
    monkeypatch.setattr(manager, "sessions", {})
    suite = db.get(Suite, "suite-0")
    suite.execution_command = "ats-native-http"
    suite.native_cases = [payload()]
    db.commit()
    if entrance == "ordinary":
        await execute_test_suite(
            suite_id=suite.id, db=db, current_user=db.get(User, "owner")
        )
        task = db.query(TaskQueue).one()
    else:
        task = TaskQueueService.add_to_queue(
            db, "node", suite.id, "variables-" + entrance, "owner"
        )
    if entrance == "schedule":
        schedule = TaskSchedule(
            id="variable-schedule",
            project_id="project",
            target_type="suite",
            target_id=suite.id,
            name="synthetic",
            timezone="UTC",
            created_by="owner",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db.add(schedule)
        db.flush()
        db.add(
            TaskScheduleRun(
                id="variable-schedule-run",
                schedule_id=schedule.id,
                execution_id=task.execution_id,
                status="queued",
                trigger_type="manual",
                trigger_key="variable-trigger",
                scheduled_for=datetime.now(),
                executor_id="owner",
                created_at=datetime.now(),
            )
        )
        db.commit()
        await dispatch_pending(db)
    elif entrance == "queued":
        await dispatch_pending_suites(db, "node")
    assert task.status == "pending" and task.started_at is None and not legacy_sent
    socket = capable(monkeypatch)
    if entrance == "schedule":
        await dispatch_pending(db)
    else:
        await dispatch_pending_suites(db, "node")
    db.refresh(task)
    assert task.status == "running" and len(socket.sent) == 1 and not legacy_sent
    assert (
        socket.sent[0]["native_cases"][0]["requests"][0]["initialVariables"][0]["value"]
        == "literal"
    )


@pytest.mark.asyncio
async def test_plan_entrance_keeps_pending_until_capable(native_workspace, monkeypatch):
    from api.v1.websocket import manager

    db, _, _ = native_workspace
    configure(db)
    row = db.get(NativeCaseConfig, "case-0")
    row.parameters = {
        **row.parameters,
        "request": {
            **row.parameters["request"],
            "initialVariables": [dict(name="x", value="literal")],
        },
    }
    db.commit()
    monkeypatch.setattr(manager, "sessions", {})
    run = await start_plan_run(db, "plan", "owner")
    await advance_plan_runs(db)
    item = db.query(PlanRunItem).filter_by(run_id=run.id, sequence=0).one()
    task = db.query(TaskQueue).filter_by(execution_id=item.execution_id).one()
    assert item.status == task.status == "pending" and task.started_at is None
    socket = capable(monkeypatch)
    await advance_plan_runs(db)
    db.refresh(task)
    assert task.status == "running" and len(socket.sent) == 1
