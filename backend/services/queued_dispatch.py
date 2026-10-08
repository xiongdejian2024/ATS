"""Dispatch ordinary suite jobs through the same slot claim as plans/schedules."""

from core.logger import logger
from models.task_queue import TaskQueue
from services.suite_dispatch import build_suite_message, load_dispatch_suite
from services.task_queue_service import TaskQueueService


async def dispatch_pending_suites(db, environment_id):
    from api.v1.websocket import manager

    while environment_id in manager.active_connections:
        from services import script_jobs
        session = manager.sessions.get(environment_id)
        kinds = ("suite", "script") if script_jobs.capable(session, manager) else ("suite",)
        pending = TaskQueueService.get_next_pending_task(db, environment_id, kinds=kinds)
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
            if pending.kind == "script":
                prepared = script_jobs.prepare_dispatch(db, pending)
                if prepared is None:
                    db.rollback()
                    return
                run, session, payload = prepared
            else:
                suite = load_dispatch_suite(db, pending.suite_id, pending.executor_id)
                if suite.environment_id != pending.environment_id:
                    raise ValueError("测试套节点在排队后已改变，拒绝跨节点派发")
                payload = build_suite_message(
                    db, suite, execution_id, pending.executor_id, current_read=True
                )
        except Exception:
            logger.exception("排队测试套派发前校验失败：执行={}", execution_id)
            if pending.kind == "script":
                script_jobs.fail_pending(db, pending)
            else:
                TaskQueueService.complete_task(db, execution_id, "failed")
            continue
        claimed = TaskQueueService.start_task(
            db, execution_id, environment_id=environment_id, commit=False
        )
        if not claimed:
            db.rollback()
            return
        if pending.kind == "script":
            from utils.datetime_utils import beijing_now
            run.delivery_state, run.dispatch_attempted_at = "dispatching", beijing_now()
            run.dispatch_session_id = session.session_id
        else:
            suite.status = "running"
        db.commit()
        try:
            sent = (await manager.send_session(session, payload) if pending.kind == "script"
                    else await manager.send_message(environment_id, payload))
        except Exception:
            logger.exception("排队测试套派发异常：执行={}", execution_id)
            sent = False
        if pending.kind == "script":
            from models.script_job import ScriptJobRun
            db.query(ScriptJobRun).filter_by(execution_id=execution_id, delivery_state="dispatching").update(
                {"delivery_state": "sent" if sent else "unknown"}, synchronize_session=False)
            db.commit()
        else:
            from services.suite_delivery import dispatched
            dispatched(db, execution_id, sent)
        if not sent:
            # As with plans/schedules, a write failure is an uncertain delivery,
            # never permission to release the slot or automatically resend.
            logger.warning("派发结果未知，保留运行槽且不重发：执行={}", execution_id)
            return
        logger.info("排队测试套已派发：执行={}", execution_id)
