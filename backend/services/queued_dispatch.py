"""Dispatch ordinary suite jobs through the same slot claim as plans/schedules."""

from core.logger import logger
from models.task_queue import TaskQueue
from services.suite_dispatch import build_suite_message, load_dispatch_suite
from services.task_queue_service import TaskQueueService


async def dispatch_pending_suites(db, environment_id):
    from api.v1.websocket import manager

    while environment_id in manager.active_connections:
        pending = TaskQueueService.get_next_pending_task(db, environment_id)
        if not pending:
            return
        execution_id = pending.execution_id
        # All pre-dispatch reads/validation share the Environment lock with the
        # final claim. No network await occurs while the transaction is locked.
        environment = TaskQueueService.lock_environment(db, environment_id)
        if not environment or not environment.status:
            db.rollback()
            return
        pending = (
            db.query(TaskQueue)
            .filter_by(execution_id=execution_id)
            .populate_existing()
            .with_for_update()
            .one()
        )
        if pending.status != "pending" or pending.environment_id != environment_id:
            db.rollback()
            continue
        try:
            suite = load_dispatch_suite(db, pending.suite_id, pending.executor_id)
            payload = build_suite_message(
                db, suite, execution_id, pending.executor_id, current_read=True
            )
        except Exception:
            logger.exception("排队测试套派发前校验失败：执行={}", execution_id)
            TaskQueueService.complete_task(db, execution_id, "failed")
            continue
        claimed = TaskQueueService.start_task(
            db, execution_id, environment_id=environment_id, commit=False
        )
        if not claimed:
            db.rollback()
            return
        suite.status = "running"
        db.commit()
        try:
            sent = await manager.send_message(environment_id, payload)
        except Exception:
            logger.exception("排队测试套派发异常：执行={}", execution_id)
            sent = False
        if not sent:
            # As with plans/schedules, a write failure is an uncertain delivery,
            # never permission to release the slot or automatically resend.
            logger.warning("派发结果未知，保留运行槽且不重发：执行={}", execution_id)
            return
        logger.info("排队测试套已派发：执行={}", execution_id)
