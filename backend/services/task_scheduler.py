"""用现有 Celery cron 解析器与数据库事务调度，复用 Agent 执行通道。"""

import asyncio
from datetime import datetime, timezone as dt_timezone, timedelta
import uuid
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from celery.schedules import crontab
from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

from core.logger import logger
from core.project_access import require_project_access
from database import SessionLocal
from models import User, TestPlan, TestSuite, Environment
from models.task_queue import TaskQueue
from models.task_schedule import TaskSchedule, TaskScheduleRun
from services.suite_dispatch import build_suite_message, load_dispatch_suite
from utils.datetime_utils import beijing_now

TERMINAL = {"completed", "failed", "cancelled"}


def utc_now():
    """调度字段统一存 UTC 无时区值，展示时带 UTC 标识。"""
    return datetime.now(dt_timezone.utc).replace(tzinfo=None)


def next_fire_time(expression, timezone, now=None):
    """五段 cron；复用 Celery 的日历计算，不自行实现 cron 解析。"""
    try:
        zone = ZoneInfo(timezone)
        parts = (expression or "").split()
        if len(parts) != 5:
            raise ValueError("请输入五段 Cron：分 时 日 月 周")
        now = now or utc_now()
        aware = now.replace(tzinfo=dt_timezone.utc).astimezone(zone)
        schedule = crontab(
            minute=parts[0], hour=parts[1], day_of_month=parts[2],
            month_of_year=parts[3], day_of_week=parts[4], nowfun=lambda: aware,
        )
        due = aware + schedule.remaining_estimate(aware)
        return due.astimezone(dt_timezone.utc).replace(tzinfo=None)
    except (ValueError, KeyError, ZoneInfoNotFoundError) as exc:
        raise ValueError("Cron 或时区无效：" + str(exc)) from exc


def check_target(db, user, project_id, target_type, target_id):
    require_project_access(db, user, project_id, "test_plan:execute")
    if target_type == "group":
        from models.plan_orchestration import PlanGroup
        group = db.get(PlanGroup, target_id)
        if not group or group.project_id != project_id:
            raise HTTPException(400, "计划组必须属于当前项目")
        return group
    if target_type == "suite":
        suite = db.get(TestSuite, target_id)
        plan = db.get(TestPlan, suite.plan_id) if suite else None
        if not suite or not plan or plan.project_id != project_id:
            raise HTTPException(400, "测试套必须属于当前项目")
        # 仅校验引用完整性；这里不会运行命令或读取台架。
        build_suite_message(db, suite, "validation", str(user.id))
        return suite
    plan = db.get(TestPlan, target_id)
    if not plan or plan.project_id != project_id:
        raise HTTPException(400, "测试计划必须属于当前项目")
    return plan


def create_schedule(db, user, data):
    check_target(db, user, data.project_id, data.target_type, data.target_id)
    expression = (data.cron_expression or "").strip() or None
    if expression:
        next_fire_time(expression, data.timezone)
    else:
        try:
            ZoneInfo(data.timezone)
        except ZoneInfoNotFoundError as exc:
            raise ValueError("时区无效") from exc
    now = utc_now()
    row = TaskSchedule(
        id=str(uuid.uuid4()), project_id=data.project_id, name=data.name.strip(),
        target_type=data.target_type, target_id=data.target_id,
        cron_expression=expression, timezone=data.timezone, enabled=False,
        created_by=str(user.id), created_at=now, updated_at=now,
    )
    if not row.name:
        raise ValueError("任务名称不能为空")
    db.add(row)
    db.commit()
    logger.info("任务定义已创建且保持停用：任务={}，项目={}", row.id, row.project_id)
    return row


def set_enabled(db, user, row, enabled):
    require_project_access(db, user, row.project_id, "test_plan:execute")
    if enabled:
        check_target(db, user, row.project_id, row.target_type, row.target_id)
        row.next_run_at = next_fire_time(row.cron_expression, row.timezone)
        # 以最后一次显式启用者身份执行，并在每次触发时重新检查权限。
        row.created_by = str(user.id)
    else:
        row.next_run_at = None
    row.enabled = enabled
    row.updated_at = utc_now()
    db.commit()
    logger.info("任务定时开关已更新：任务={}，启用={}", row.id, enabled)
    return row


async def _prepare_run(db, row, user, trigger_key, trigger_type, scheduled_for):
    existing = db.query(TaskScheduleRun).filter_by(trigger_key=trigger_key).first()
    if existing:
        return existing
    target = check_target(db, user, row.project_id, row.target_type, row.target_id)
    identifier = str(uuid.uuid5(uuid.NAMESPACE_URL, "ats-task:" + trigger_key))
    run = TaskScheduleRun(
        id=identifier, schedule_id=row.id, trigger_key=trigger_key,
        trigger_type=trigger_type, scheduled_for=scheduled_for,
        executor_id=str(user.id), status="queued", created_at=utc_now(),
    )
    db.add(run)
    # 唯一触发键先落入事务，竞争请求只能有一个继续创建执行批次。
    db.flush()
    if row.target_type == "group":
        from services.plan_group_execution import start_group_run
        group_run = await start_group_run(db, target.id, str(user.id), idempotency_key=trigger_key, commit=False)
        run.group_run_id = group_run.id
    elif row.target_type == "plan":
        from services.plan_orchestration import start_plan_run
        plan_run = await start_plan_run(
            db, target.id, str(user.id), idempotency_key=trigger_key, commit=False,
        )
        run.plan_run_id = plan_run.id
    else:
        execution_id = str(uuid.uuid5(uuid.NAMESPACE_URL, "ats-task-execution:" + trigger_key))
        run.execution_id = execution_id
        db.add(TaskQueue(
            id=str(uuid.uuid4()), environment_id=target.environment_id,
            suite_id=target.id, execution_id=execution_id,
            executor_id=str(user.id), status="pending", priority=0, created_at=beijing_now(),
        ))
    db.flush()
    return run


async def trigger_schedule(db, user, row, request_id):
    require_project_access(db, user, row.project_id, "test_plan:execute")
    key = f"{row.id}:manual:{request_id}"
    try:
        run = await _prepare_run(db, row, user, key, "manual", utc_now())
        db.commit()
    except IntegrityError:
        db.rollback()
        logger.exception("重复手动触发已由唯一键拦截：任务={}", row.id)
        run = db.query(TaskScheduleRun).filter_by(trigger_key=key).first()
        if run is None:
            raise
    logger.info("手动任务已持久化：任务={}，触发={}", row.id, run.id)
    return run


async def enqueue_due(db, now=None):
    """CAS 领取到期记录；每次恢复只合并一次错过的周期。"""
    now = now or utc_now()
    due = db.query(TaskSchedule).filter(
        TaskSchedule.enabled.is_(True), TaskSchedule.next_run_at <= now,
    ).order_by(TaskSchedule.next_run_at).limit(100).all()
    created = 0
    for row in due:
        scheduled_for = row.next_run_at
        next_at = next_fire_time(row.cron_expression, row.timezone, now)
        claimed = db.execute(update(TaskSchedule).where(
            TaskSchedule.id == row.id, TaskSchedule.enabled.is_(True),
            TaskSchedule.next_run_at == scheduled_for,
        ).values(next_run_at=next_at, last_run_at=now, updated_at=now))
        if claimed.rowcount != 1:
            db.rollback()
            continue
        key = f"{row.id}:cron:{scheduled_for.isoformat()}"
        try:
            with db.begin_nested():
                user = db.get(User, row.created_by)
                if not user or not user.status:
                    raise ValueError("定时任务执行人不存在或已被禁用")
                await _prepare_run(db, row, user, key, "cron", scheduled_for)
            db.commit()
            created += 1
            logger.info("到期任务已入队：任务={}，计划时间={}", row.id, scheduled_for)
        except Exception:
            logger.exception("到期任务创建失败：任务={}", row.id)
            # 不把配置/命令中的凭证写进可见错误；完整诊断保留于后端堆栈。
            if not db.query(TaskScheduleRun).filter_by(trigger_key=key).first():
                db.add(TaskScheduleRun(
                    id=str(uuid.uuid4()), schedule_id=row.id, trigger_key=key,
                    trigger_type="cron", scheduled_for=scheduled_for,
                    executor_id=row.created_by, status="failed", created_at=now,
                    completed_at=now, error_message="创建执行失败，请检查目标、执行人权限及服务日志",
                ))
            db.commit()
    return created


async def dispatch_pending(db):
    """仅派发任务中心创建的测试套；计划批次由计划编排器派发。"""
    from api.v1.websocket import manager
    rows = db.query(TaskQueue).join(
        TaskScheduleRun, TaskScheduleRun.execution_id == TaskQueue.execution_id,
    ).filter(TaskQueue.kind == "suite", TaskQueue.status == "pending", TaskScheduleRun.status != "cancelling").order_by(
        TaskQueue.priority.desc(), TaskQueue.created_at,
    ).all()
    for task in rows:
        # 同环境串行锁覆盖容量检查与领取；条件更新防止重叠tick重复发送。
        from services.task_queue_service import TaskQueueService
        environment = TaskQueueService.lock_environment(db, task.environment_id)
        if not environment:
            db.rollback()
            continue
        if not environment.status or task.environment_id not in manager.active_connections:
            db.rollback()
            continue
        task = db.query(TaskQueue).filter_by(id=task.id).populate_existing().with_for_update().one()
        run = db.query(TaskScheduleRun).filter_by(execution_id=task.execution_id).populate_existing().with_for_update().first()
        if task.status != "pending" or not run or run.status in (*TERMINAL, "cancelling", "needs_confirmation"):
            db.rollback()
            continue
        try:
            schedule = db.query(TaskSchedule).filter_by(id=run.schedule_id).populate_existing().with_for_update().first()
            suite = load_dispatch_suite(db, task.suite_id, task.executor_id)
            plan = db.query(TestPlan).filter_by(id=suite.plan_id).populate_existing().with_for_update().one()
            if not schedule or plan.project_id != schedule.project_id:
                raise ValueError("定时任务与测试套项目不一致")
            payload = build_suite_message(db, suite, task.execution_id, task.executor_id, current_read=True)
        except Exception:
            logger.exception("派发前校验失败：执行={}", task.execution_id)
            task.status, run.status = "failed", "failed"
            task.completed_at, run.completed_at = beijing_now(), utc_now()
            run.error_message = "派发前校验失败，请检查目标和执行人权限"
            db.commit()
            continue
        eligible_runs = db.query(TaskScheduleRun.execution_id).filter(
            TaskScheduleRun.status.notin_((*TERMINAL, "cancelling", "needs_confirmation"))
        )
        claimed = TaskQueueService.start_task(
            db, task.execution_id, environment_id=task.environment_id, commit=False,
            eligibility=(TaskQueue.execution_id.in_(eligible_runs),),
        )
        if not claimed:
            db.rollback()
            continue
        suite.status, run.status = "running", "running"
        run.delivery_state, run.dispatch_attempted_at = "dispatching", utc_now()
        db.commit()
        try:
            sent = await manager.send_message(task.environment_id, payload)
        except Exception:
            logger.exception("派发消息异常：执行={}", task.execution_id)
            sent = False
        if not sent:
            # 已通过在线检查并尝试发送，异常不能证明节点未收到，保留运行槽。
            run.status = "needs_confirmation"
            run.delivery_state = "uncertain"
            run.error_message = "派发已尝试但未确认交付，请核对节点执行状态；系统不会自动重发。"
            db.commit()
            logger.warning("任务派发结果待核对，保留运行槽：执行={}", task.execution_id)
        else:
            run.delivery_state = "delivered"
            run.error_message = None
            db.commit()
            logger.info("任务已派发至 Agent：执行={}", task.execution_id)


async def cancel_run(db, user, run):
    schedule = db.get(TaskSchedule, run.schedule_id)
    require_project_access(db, user, schedule.project_id, "test_plan:execute")
    if run.status in TERMINAL:
        return run
    if run.group_run_id:
        from models.plan_group_execution import PlanGroupRun
        from services.plan_group_execution import cancel_group_run
        group = db.get(PlanGroupRun, run.group_run_id)
        await cancel_group_run(db, group, user)
        run.status = group.status
    elif run.plan_run_id:
        from services.plan_orchestration import cancel_plan_run
        await cancel_plan_run(db, run.plan_run_id, user_id=str(user.id))
        run.status = "cancelling"
    else:
        task = db.query(TaskQueue).filter_by(execution_id=run.execution_id).first()
        if task and task.status == "pending":
            # CAS防止恰好被另一派发器领取时假装取消成功。
            changed = db.execute(update(TaskQueue).where(
                TaskQueue.id == task.id, TaskQueue.status == "pending",
            ).values(status="cancelled", completed_at=beijing_now()))
            run.status = "cancelled" if changed.rowcount == 1 else "cancelling"
        else:
            run.status = "cancelling"
    if run.status == "cancelled":
        run.completed_at = utc_now()
    db.commit()
    logger.info("任务取消意图已保存：触发={}，状态={}", run.id, run.status)
    await reconcile_runs(db)
    return run


async def reconcile_runs(db):
    from api.v1.websocket import manager
    from models.plan_orchestration import PlanRun
    for run in db.query(TaskScheduleRun).filter(TaskScheduleRun.status.notin_(TERMINAL)).all():
        if run.group_run_id:
            from models.plan_group_execution import PlanGroupRun
            group = db.get(PlanGroupRun, run.group_run_id)
            if group:
                run.status = group.status
        elif run.plan_run_id:
            plan = db.get(PlanRun, run.plan_run_id)
            if plan:
                run.status = plan.status
        else:
            task = db.query(TaskQueue).filter_by(execution_id=run.execution_id).first()
            if task:
                if task.status in TERMINAL:
                    run.status = task.status
                elif run.status == "cancelling":
                    if task.status == "pending":
                        changed = db.execute(update(TaskQueue).where(
                            TaskQueue.id == task.id, TaskQueue.status == "pending",
                        ).values(status="cancelled", completed_at=beijing_now()))
                        if changed.rowcount == 1:
                            run.status = "cancelled"
                    else:
                        await manager.send_message(task.environment_id, {
                            "type": "cancel_test_suite", "suite_id": task.suite_id,
                            "execution_id": task.execution_id,
                        })
                elif run.delivery_state == "dispatching" and run.dispatch_attempted_at and (
                    utc_now() - run.dispatch_attempted_at > timedelta(seconds=30)
                ):
                    run.status = "needs_confirmation"
                    run.error_message = "服务中断时派发结果未确认，请核对节点执行状态；系统不会自动重派。"
                elif run.status != "needs_confirmation":
                    run.status = "queued" if task.status == "pending" else "running"
        if run.status in TERMINAL:
            run.completed_at = utc_now()
    db.commit()


def resolve_uncertain_run(db, user, run):
    """仅用于用户已核对节点后的人工结束，不能把未知执行结果标为成功。"""
    schedule = db.get(TaskSchedule, run.schedule_id)
    require_project_access(db, user, schedule.project_id, "test_plan:execute")
    if run.status != "needs_confirmation" or not run.execution_id:
        raise HTTPException(409, "该记录不属于待确认的测试套执行")
    task = db.query(TaskQueue).filter_by(execution_id=run.execution_id).first()
    if task and task.status not in TERMINAL:
        task.status, task.completed_at = "failed", beijing_now()
    run.status, run.completed_at = "failed", utc_now()
    run.error_message = "用户已确认节点未执行或已停止，未知结果按异常结束处理"
    db.commit()
    logger.warning("用户人工结束未确认的派发：触发={}，操作人={}", run.id, user.id)
    return run


async def scheduler_tick(db, now=None):
    from services.plan_orchestration import advance_plan_runs
    from services.plan_group_execution import advance_group_runs
    await enqueue_due(db, now)
    await reconcile_runs(db)
    await advance_group_runs(db)
    await advance_plan_runs(db)
    await advance_group_runs(db)
    await dispatch_pending(db)
    await reconcile_runs(db)


async def scheduler_loop(interval=2):
    """由 FastAPI 生命周期启动；数据库保存状态，进程本身没有调度真相。"""
    logger.info("任务调度循环启动，仅执行用户已启用的到期任务")
    while True:
        try:
            with SessionLocal() as db:
                await scheduler_tick(db)
        except asyncio.CancelledError:
            logger.info("任务调度循环停止，已持久化的任务留待恢复")
            raise
        except Exception:
            logger.exception("任务调度轮询失败，下一轮重试")
        await asyncio.sleep(interval)
