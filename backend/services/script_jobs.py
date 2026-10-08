"""Formal script queues: frozen execution identity, current authority, durable results."""
import math
import uuid
from copy import deepcopy
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from models import User, Environment, TaskQueue
from models.script_job import ScriptJob, ScriptJobRun
from core.project_access import require_project_access
from core.permissions import has_global_permission
from services.task_queue_service import TaskQueueService
from utils.datetime_utils import beijing_now

TERMINAL = {"completed", "failed", "cancelled"}
CAPABILITY = "script_jobs_v1"


def capable(session, manager):
    return bool(session and manager.is_live(session) and session.protocol_version >= 2
                and getattr(session, "auth_received", False)
                and CAPABILITY in getattr(session, "capabilities", frozenset()))


def stamp(value):
    return value.isoformat() + "+08:00" if value and value.tzinfo is None else value.isoformat() if value else None


def job_json(job):
    return dict(deepcopy(job.config), id=job.id, projectId=job.project_id, name=job.name,
                environmentId=job.environment_id, revision=job.revision,
                createdAt=stamp(job.created_at), updatedAt=stamp(job.updated_at))


def run_json(db, run):
    task = db.query(TaskQueue).filter_by(execution_id=run.execution_id, kind="script").one()
    return dict(executionId=run.execution_id, jobId=run.job_id, projectId=run.project_id,
                environmentId=run.environment_id, executorId=run.executor_id,
                status=task.status, deliveryState=run.delivery_state,
                cancelRequested=run.cancel_requested_at is not None, result=run.result,
                exitCode=run.exit_code, durationSeconds=run.duration_seconds,
                errorMessage=run.error_message, configSnapshot=deepcopy(run.config_snapshot),
                createdAt=stamp(run.created_at), startedAt=stamp(task.started_at),
                completedAt=stamp(task.completed_at), closedBy=run.closed_by,
                closedAt=stamp(run.closed_at), logDelivery=run.log_delivery)


def require_node(db, user, environment_id, *, current_read=False):
    node = (db.query(Environment).filter_by(id=environment_id).populate_existing().with_for_update().first()
            if current_read else db.get(Environment, environment_id))
    if not node:
        raise HTTPException(404, "节点不存在")
    if node.created_by != str(user.id) and not has_global_permission(db, user.id, "system", "manage", current_read=current_read):
        raise HTTPException(403, "仅节点创建人或系统管理员可以运行脚本作业")
    return node


def find_job(db, user, job_id, action="read", *, current_read=False):
    job = (db.query(ScriptJob).filter_by(id=job_id).populate_existing().with_for_update().first()
           if current_read else db.get(ScriptJob, job_id))
    if not job:
        raise HTTPException(404, "脚本作业不存在")
    require_project_access(db, user, job.project_id, "test_plan:" + action, current_read=current_read)
    return job


def find_run(db, user, job_id, execution_id, action="read"):
    find_job(db, user, job_id, action)
    run = db.get(ScriptJobRun, execution_id)
    if not run or run.job_id != job_id:
        raise HTTPException(404, "脚本执行不存在")
    if action != "read":
        require_node(db, user, run.environment_id, current_read=True)
    return run


def create_job(db, user, data):
    require_project_access(db, user, data.project_id, "test_plan:execute")
    require_node(db, user, data.environment_id)
    now = beijing_now()
    config = data.model_dump(by_alias=True, exclude={"project_id"})
    job = ScriptJob(id=str(uuid.uuid4()), project_id=data.project_id, name=data.name,
                    environment_id=data.environment_id, config=config, revision=1,
                    created_by=user.id, updated_by=user.id, created_at=now, updated_at=now)
    db.add(job); db.commit(); return job


def update_job(db, user, job_id, data):
    require_node(db, user, data.environment_id, current_read=True)
    job = find_job(db, user, job_id, "execute", current_read=True)
    require_node(db, user, job.environment_id, current_read=True)
    job.name, job.environment_id = data.name, data.environment_id
    job.config = data.model_dump(by_alias=True)
    job.revision += 1
    job.updated_by, job.updated_at = user.id, beijing_now()
    db.commit(); return job


async def trigger(db, user, job_id, request_id):
    from api.v1.websocket import manager
    job = find_job(db, user, job_id, "execute", current_read=True)
    existing = db.query(ScriptJobRun).filter_by(request_id=request_id).first()
    if existing:
        if existing.job_id != job_id or existing.executor_id != str(user.id):
            raise HTTPException(409, "requestId已被其他执行使用")
        require_node(db, user, existing.environment_id, current_read=True)
        return existing
    node = require_node(db, user, job.environment_id, current_read=True)
    if not node.status:
        raise HTTPException(409, "节点已禁用")
    session = manager.sessions.get(node.id)
    # No session means a durable pending intent. An authenticated old Agent is
    # explicitly unsupported; an auth frame still in flight is simply pending.
    if session and manager.is_live(session) and getattr(session, "auth_received", False) and not capable(session, manager):
        raise HTTPException(409, "当前Agent不支持脚本作业，请升级Agent")
    execution_id, now = str(uuid.uuid4()), beijing_now()
    run = ScriptJobRun(execution_id=execution_id, job_id=job.id, project_id=job.project_id,
                      environment_id=node.id, executor_id=user.id, request_id=request_id,
                      config_snapshot=dict(deepcopy(job.config), revision=job.revision), created_at=now)
    db.add(run)
    db.add(TaskQueue(id=str(uuid.uuid4()), kind="script", script_job_id=job.id,
                     environment_id=node.id, execution_id=execution_id, executor_id=user.id,
                     status="pending", priority=0, created_at=now))
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = db.query(ScriptJobRun).filter_by(request_id=request_id).first()
        if not existing or existing.job_id != job_id or existing.executor_id != str(user.id):
            raise HTTPException(409, "requestId冲突")
        return existing
    from services.queued_dispatch import dispatch_pending_suites
    await dispatch_pending_suites(db, node.id)
    db.refresh(run)
    return run


def prepare_dispatch(db, task):
    from api.v1.websocket import manager
    session = manager.sessions.get(task.environment_id)
    if not capable(session, manager):
        return None
    run = db.query(ScriptJobRun).filter_by(execution_id=task.execution_id).populate_existing().with_for_update().one()
    user = db.query(User).filter_by(id=task.executor_id).populate_existing().with_for_update(read=True).first()
    if not user or not user.status:
        raise ValueError("执行人已停用")
    if (run.job_id != task.script_job_id or run.environment_id != task.environment_id
            or run.executor_id != task.executor_id or run.result is not None):
        raise ValueError("脚本执行身份不一致")
    require_project_access(db, user, run.project_id, "test_plan:execute", current_read=True)
    node = require_node(db, user, run.environment_id, current_read=True)
    if not node.status:
        raise ValueError("节点已禁用")
    return run, session, dict(type="execute_script_job", script_job_id=run.job_id,
                             execution_id=run.execution_id, dispatch_session_id=session.session_id, config=deepcopy(run.config_snapshot))


def fail_pending(db, task):
    run = db.get(ScriptJobRun, task.execution_id)
    task.status, task.completed_at = "failed", beijing_now()
    if run:
        run.result, run.delivery_state = "error", "terminal"
        run.error_message = "派发前校验失败，请核对执行人权限和节点归属"
    db.commit()


async def cancel(db, user, job_id, execution_id):
    from api.v1.websocket import manager
    run = find_run(db, user, job_id, execution_id, "execute")
    TaskQueueService.lock_environment(db, run.environment_id)
    task = db.query(TaskQueue).filter_by(execution_id=execution_id, kind="script", script_job_id=job_id).populate_existing().with_for_update().one()
    db.refresh(run)
    if task.status in TERMINAL:
        return run
    run.cancel_requested_at = beijing_now()
    if task.status == "pending":
        task.status, task.completed_at = "cancelled", beijing_now()
        run.result, run.delivery_state = "cancelled", "terminal"
        run.error_message = "任务在派发前已取消"
        db.commit()
    else:
        # Persist the intention first. Retry the cancellation after reconnect,
        # never release on successful socket send alone.
        db.commit()
        session = manager.sessions.get(run.environment_id)
        sent = capable(session, manager) and await manager.send_session(session, dict(
            type="cancel_script_job", script_job_id=job_id, execution_id=execution_id, dispatch_session_id=run.dispatch_session_id))
        if not sent:
            db.query(ScriptJobRun).filter(ScriptJobRun.execution_id == execution_id,
                ScriptJobRun.result.is_(None), ScriptJobRun.delivery_state != "terminal").update(
                {"delivery_state": "unknown", "error_message": "取消尚未确认；请核对节点，运行槽保留"}, synchronize_session=False)
            db.commit()
            db.refresh(run)
    from services.queued_dispatch import dispatch_pending_suites
    await dispatch_pending_suites(db, run.environment_id)
    return run


def resolve(db, user, job_id, execution_id, data):
    run = find_run(db, user, job_id, execution_id, "execute")
    if data.confirmed_stopped is not True:
        raise HTTPException(400, "必须明确确认本次执行未启动或所有相关进程已停止")
    TaskQueueService.lock_environment(db, run.environment_id)
    task = db.query(TaskQueue).filter_by(execution_id=execution_id, kind="script").populate_existing().with_for_update().one()
    db.refresh(run)
    if run.result == "unknown" and run.closed_by:
        return run
    if task.status != "running" or run.delivery_state != "unknown":
        raise HTTPException(409, "只有结果待核对的执行可以人工关闭")
    run.result, run.delivery_state = "unknown", "terminal"
    run.exit_code = None
    run.closed_by, run.closed_at = user.id, beijing_now()
    run.error_message = "用户已确认未启动或进程已停止；未知结果人工关闭" + ("：" + data.reason if data.reason else "")
    task.status, task.completed_at = "failed", beijing_now()
    db.commit(); return run


def owned_run(db, environment_id, message):
    task = db.query(TaskQueue).filter_by(execution_id=message.get("execution_id"), kind="script",
                                         script_job_id=message.get("script_job_id"), environment_id=environment_id).with_for_update().first()
    run = db.get(ScriptJobRun, message.get("execution_id"))
    if not task or not run or run.environment_id != environment_id or run.job_id != task.script_job_id:
        return None
    return task, run


def complete(db, environment_id, message):
    pair = owned_run(db, environment_id, message)
    if not pair:
        return False
    task, run = pair
    result, code, duration = message.get("result"), message.get("exit_code"), message.get("duration_seconds")
    if (result not in {"success", "failed", "timeout", "error", "cancelled"}
            or code is not None and (type(code) is not int or not -(2**31) <= code < 2**31)
            or type(duration) not in (int, float) or not math.isfinite(duration) or duration < 0
            or result == "success" and code != 0):
        return False
    if task.status in TERMINAL:
        return True
    if task.status != "running":
        return False
    run.result, run.exit_code, run.duration_seconds = result, code, duration
    run.delivery_state = "terminal"
    run.error_message = str(message.get("error") or "")[:4096] or None
    diagnostic = message.get("log_delivery")
    if isinstance(diagnostic, dict):
        run.log_delivery = {k: diagnostic[k] for k in ("bytes", "records", "max_bytes", "max_records")
                            if type(diagnostic.get(k)) is int and 0 <= diagnostic[k] < 2**63}
        if isinstance(diagnostic.get("blocked_reason"), str):
            run.log_delivery["blocked_reason"] = diagnostic["blocked_reason"][:256]
        if type(diagnostic.get("backpressured")) is bool:
            run.log_delivery["backpressured"] = diagnostic["backpressured"]
    task.status = "completed" if result == "success" else "cancelled" if result == "cancelled" else "failed"
    task.completed_at = beijing_now()
    db.commit()
    return True


def accept_state(db, environment_id, message):
    pair = owned_run(db, environment_id, message)
    if not pair:
        return False
    task, run = pair
    if task.status in TERMINAL:
        return True
    state = message.get("state")
    if task.status != "running" or state not in {"running", "terminal_pending", "unknown", "never_started"}:
        return False
    run.delivery_state = "running" if state == "running" else "unknown"
    run.error_message = None if state == "running" else "执行结果尚未确认，槽位保留；请取消或核对节点后人工关闭"
    db.commit(); return True


async def reconcile_session(db, session):
    from api.v1.websocket import manager
    if not capable(session, manager):
        return
    rows = db.query(ScriptJobRun).join(TaskQueue, TaskQueue.execution_id == ScriptJobRun.execution_id).filter(
        TaskQueue.kind == "script", TaskQueue.environment_id == session.environment_id, TaskQueue.status == "running").all()
    for run in rows:
        run.delivery_state = "unknown"
        run.error_message = "连接已恢复，正在核对节点执行状态；系统不会自动重派"
    db.commit()
    for run in rows:
        await manager.send_session(session, dict(type="query_script_job", script_job_id=run.job_id, execution_id=run.execution_id, dispatch_session_id=run.dispatch_session_id))
        if run.cancel_requested_at:
            await manager.send_session(session, dict(type="cancel_script_job", script_job_id=run.job_id, execution_id=run.execution_id, dispatch_session_id=run.dispatch_session_id))


def mark_disconnected(db, environment_id):
    rows = db.query(ScriptJobRun).join(TaskQueue, TaskQueue.execution_id == ScriptJobRun.execution_id).filter(
        TaskQueue.kind == "script", TaskQueue.environment_id == environment_id, TaskQueue.status == "running").all()
    for run in rows:
        run.delivery_state = "unknown"
        run.error_message = "节点连接中断，执行状态待核对；系统不会自动重派"
    db.commit()
