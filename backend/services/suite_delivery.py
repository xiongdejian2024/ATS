"""Never rerun an uncertain suite. Release its slot only after operator proof."""
from fastapi import HTTPException
from pydantic import BaseModel, Field, StrictBool, ConfigDict
from models import TaskQueue, SuiteDelivery, User
from models.plan_orchestration import PlanRunItem
from models.task_schedule import TaskScheduleRun
from services.task_queue_service import TaskQueueService
from utils.datetime_utils import beijing_now


class ResolveSuiteInput(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    confirmed_stopped: StrictBool = Field(alias="confirmedStopped")
    reason: str = Field(min_length=1, max_length=2000)


def ordinary(db, execution_id):
    return not (db.query(PlanRunItem.id).filter_by(execution_id=execution_id).first()
                or db.query(TaskScheduleRun.id).filter_by(execution_id=execution_id).first())


def state_json(db, task):
    from api.v1.websocket import manager
    delivery = db.get(SuiteDelivery, task.execution_id)
    session = manager.sessions.get(task.environment_id)
    if task.status in {"completed", "failed", "cancelled"}:
        state = "terminal"
    elif task.status == "pending":
        state = "queued"
    elif (not manager.is_live(session) or not delivery or delivery.state == "unknown"
          or delivery.session_id != session.session_id):
        state = "unknown"
    else:
        state = delivery.state
    is_ordinary = ordinary(db, task.execution_id)
    return dict(executionId=task.execution_id, suiteId=task.suite_id,
                environmentId=task.environment_id, status=task.status,
                deliveryState=state, canResolve=state == "unknown" and is_ordinary,
                managedBy="suite" if is_ordinary else "plan-or-schedule",
                result="unknown" if delivery and delivery.closed_by else None,
                closedBy=delivery.closed_by if delivery else None,
                closedAt=delivery.closed_at.isoformat() if delivery and delivery.closed_at else None,
                reason=delivery.reason if delivery else None)


def find_task(db, suite_id, execution_id):
    task = db.query(TaskQueue).filter_by(kind="suite", suite_id=suite_id, execution_id=execution_id).first()
    if task is None:
        raise HTTPException(404, "此测试套中不存在该执行")
    return task


def reserve(db, task):
    from api.v1.websocket import manager
    session = manager.sessions.get(task.environment_id)
    row = SuiteDelivery(execution_id=task.execution_id, suite_id=task.suite_id,
                        environment_id=task.environment_id,
                        session_id=session.session_id if session else None, state="dispatching")
    db.add(row)


def dispatched(db, execution_id, sent):
    db.query(SuiteDelivery).filter_by(execution_id=execution_id, state="dispatching").update(
        {"state": "sent" if sent else "unknown"}, synchronize_session=False)
    db.commit()


def resolve(db, user, suite_id, execution_id, data):
    from api.v1.test_suites import require_suite_access
    from services.script_jobs import require_node
    require_suite_access(db, user, suite_id, "execute")
    task = find_task(db, suite_id, execution_id)
    # Closing a slot admits later workloads. It requires node ownership/admin
    # as well as project execution permission, just like standalone scripts.
    require_node(db, user, task.environment_id, current_read=True)
    if data.confirmed_stopped is not True or not data.reason.strip():
        raise HTTPException(400, "必须核对节点并确认未启动或所有相关进程已停止，填写核对说明")
    TaskQueueService.lock_environment(db, task.environment_id)
    db.refresh(task, with_for_update=True)
    delivery = db.get(SuiteDelivery, execution_id)
    if delivery and delivery.closed_by:
        return state_json(db, task)
    if not state_json(db, task)["canResolve"] or task.status != "running":
        raise HTTPException(409, "只有普通测试套的未知执行可以在此关闭；计划/定时批次请到原入口核对")
    if delivery is None:
        delivery = SuiteDelivery(execution_id=execution_id, suite_id=suite_id, environment_id=task.environment_id, state="unknown")
        db.add(delivery)
    delivery.closed_by, delivery.closed_at = str(user.id), beijing_now()
    delivery.reason = data.reason.strip()
    delivery.state = "terminal"
    task.status, task.completed_at = "failed", beijing_now()
    db.flush()  # SessionLocal disables autoflush; exclude our closed slot now.
    from models import TestSuite
    suite = db.get(TestSuite, suite_id)
    active = db.query(TaskQueue.status).filter(TaskQueue.suite_id == suite_id, TaskQueue.status.in_(("running", "pending"))).all()
    suite.status = "running" if any(row[0] == "running" for row in active) else "pending" if active else "failed"
    db.commit()
    return state_json(db, task)
