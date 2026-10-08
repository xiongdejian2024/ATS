"""Agent WebSocket endpoint. Handler admission is fenced to one live session."""

import asyncio
import json
import time
from datetime import datetime

from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from core.agent_protocol import (
    AGENT_MESSAGE_TYPES,
    MAX_FRAME_BYTES,
    PING_INTERVAL,
    PROTOCOL_VERSION,
)
from core.logger import logger
from services.agent_connections import ConnectionManager
from services.environment_service import EnvironmentService
from services.frontend_log_stream import FrontendConnectionManager
from utils.datetime_utils import beijing_now

manager = ConnectionManager()
frontend_manager = FrontendConnectionManager()


async def websocket_endpoint(websocket: WebSocket, token: str):
    from database import SessionLocal
    from services.queued_dispatch import dispatch_pending_suites

    db = SessionLocal()
    session = None
    try:
        await websocket.accept()
        environment = EnvironmentService.get_environment_by_token(db, token)
        if not environment:
            await websocket.close(code=1008, reason="Invalid environment token")
            return
        requested = websocket.query_params.get("protocol_version", "1")
        if requested not in {"1", str(PROTOCOL_VERSION)}:
            await websocket.close(code=1002, reason="Unsupported Agent protocol")
            return
        environment_id = environment["id"]

        def still_authorized():
            db.rollback()
            current = EnvironmentService.get_environment_by_token(db, token)
            return current is not None and current["id"] == environment_id

        session = await manager.connect(
            websocket, environment_id, token, int(requested), authorize=still_authorized
        )
        if session is None:
            await websocket.close(code=1008, reason="Environment token revoked")
            return
        async with manager.session_lock(environment_id):
            if not manager.touch(db, session, {}):
                return
            try:
                reconnect_delay = max(
                    1,
                    min(
                        60,
                        int(
                            environment.get("reconnect_delay")
                            or environment.get("reconnectDelay")
                            or 30
                        ),
                    ),
                )
            except (ValueError, TypeError):
                reconnect_delay = 30
            config = {
                "environment_id": environment_id,
                "environment_name": environment.get("name"),
                "work_dir": environment.get("remote_work_dir")
                or environment.get("remoteWorkDir")
                or "",
                "reconnect_delay": reconnect_delay,
                "heartbeat_timeout": manager.heartbeat_timeout,
                "capabilities": ["log_batch_v1"],
            }
            if not await manager.send_session(session, dict(config, type="welcome")):
                return
            if not await manager.send_session(
                session, dict(config, type="auth_success")
            ):
                return
            await dispatch_pending_suites(db, environment_id)
            db.rollback()  # release read transactions before idle socket waits

        while manager.is_live(session):
            remaining = manager.heartbeat_timeout - (
                time.monotonic() - session.last_seen
            )
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(), min(PING_INTERVAL, remaining)
                )
            except asyncio.TimeoutError:
                if not manager.is_live(session):
                    break
                if not await manager.send_session(session, {"type": "ping"}):
                    break
                continue
            if len(data.encode("utf-8")) > MAX_FRAME_BYTES:
                await websocket.close(code=1009, reason="Agent frame too large")
                break
            try:
                message = json.loads(data)
            except (ValueError, RecursionError):
                await websocket.close(code=1002, reason="Invalid Agent JSON")
                break
            if (
                not isinstance(message, dict)
                or not isinstance(message.get("type"), str)
                or message["type"] not in AGENT_MESSAGE_TYPES
            ):
                await websocket.close(code=1002, reason="Invalid Agent message type")
                break
            if session.protocol_version >= 2 and (
                message.get("session_id") != session.session_id
                or type(message.get("protocol_version")) is not int
                or message["protocol_version"] != PROTOCOL_VERSION
            ):
                await websocket.close(
                    code=1002, reason="Agent session or protocol mismatch"
                )
                break
            if message["type"] == "heartbeat" and not isinstance(
                message.get("data", {}), dict
            ):
                await websocket.close(code=1002, reason="Invalid Agent heartbeat")
                break
            # Replacement cannot interleave with an admitted handler's DB writes.
            # A stale waiting frame does not reach persistence, task release, or ACK.
            async with manager.session_lock(environment_id):
                if not manager.touch(
                    db,
                    session,
                    message.get("data", {}) if message["type"] == "heartbeat" else None,
                ):
                    break
                message_type = message["type"]
                if message_type == "heartbeat":
                    await manager.send_session(
                        session,
                        {
                            "type": "heartbeat_ack",
                            "timestamp": beijing_now().isoformat(),
                        },
                    )
                elif message_type in {"auth", "pong"}:
                    pass
                elif message_type in {"task_result", "task_log"}:
                    logger.debug("Received legacy Agent task frame: {}", message_type)
                elif message_type == "test_suite_result":
                    accepted = await handle_test_suite_result(
                        db, environment_id, message
                    )
                    db.rollback()
                    if accepted and message.get("event_id"):
                        await manager.send_session(
                            session,
                            {"type": "sat_event_ack", "event_id": message["event_id"]},
                        )
                elif message_type == "log_batch":
                    from services.agent_log_ingest import persist_log_batch

                    response, deltas = persist_log_batch(db, environment_id, message)
                    # Persistence and ACK are fenced to this authenticated session.
                    await manager.send_session(session, response)
                    for suite_id, delta in deltas:
                        await frontend_manager.broadcast_log(suite_id, delta)
                elif message_type == "test_suite_log":
                    await handle_test_suite_log(db, environment_id, message)
                elif message_type == "test_suite_completed":
                    accepted = await handle_test_suite_completed(
                        db, environment_id, message
                    )
                    db.rollback()
                    if accepted and message.get("event_id"):
                        await manager.send_session(
                            session,
                            {"type": "sat_event_ack", "event_id": message["event_id"]},
                        )
                elif message_type.startswith("workspace_"):
                    from api.v1.workspace import handle_workspace_response

                    handle_workspace_response(message)
                db.rollback()  # handlers commit accepted events; never hold a DB lease while idle
    except WebSocketDisconnect:
        pass
    except Exception:
        db.rollback()
        logger.exception("Agent connection failed")
    finally:
        if session and manager.disconnect(session.environment_id, session):
            manager._close_later(session, 1001, "Agent session ended")
        db.close()


async def handle_test_suite_result(db: Session, environment_id: str, message: dict):
    """处理测试套执行结果"""
    from services.test_suite_service import TestSuiteService
    from models.test_suite import TestSuite
    
    if message.get("execution_id"):
        from services.suite_results import handle_run_result
        try:
            return handle_run_result(db, environment_id, message)
        except Exception:
            db.rollback()
            logger.exception("Failed to persist SAT result")
            return False

    logger.info(f"[WebSocket] 开始处理测试套执行结果: {message}")
    try:
        suite_id = message.get("suite_id")
        case_id = message.get("case_id")
        result = message.get("result")  # passed, failed, error, skipped
        duration = message.get("duration")
        log_output = message.get("log_output")
        error_message = message.get("error_message")
        executor_id = message.get("executor_id")
        
        logger.info(f"[WebSocket] 解析后的参数: suite_id={suite_id}, case_id={case_id}, result={result}, duration={duration}")
        
        if not suite_id or not case_id:
            logger.warning(f"[WebSocket] 测试套执行结果缺少必要字段: suite_id={suite_id}, case_id={case_id}, message={message}")
            return
        
        # 创建执行记录
        TestSuiteService.create_suite_execution(
            db=db,
            suite_id=suite_id,
            case_id=case_id,
            environment_id=environment_id,
            executor_id=executor_id or "system",
            result=result,
            duration=duration,
            log_output=log_output,
            error_message=error_message
        )
        
        logger.info(f"[WebSocket] 测试套执行记录已保存: suite_id={suite_id}, case_id={case_id}, result={result}")
        
        # 获取测试套信息
        suite = db.query(TestSuite).filter(TestSuite.id == suite_id).first()
        logger.info(f"suite plan id is {suite.plan_id}")
        # 如果测试套关联了测试计划，更新 plan_case_relations 表的 execution_status
        if suite and suite.plan_id:
            try:
                from models.test_plan import PlanCaseRelation
                
                # 状态映射：TestSuiteExecution 的状态 -> plan_case_relations 的状态
                status_map = {
                    "passed": "pass",
                    "failed": "fail",
                    "error": "error",
                    "skipped": "skip"
                }
                plan_status = status_map.get(result, "error")
                
                # 更新 plan_case_relations 表的 execution_status
                relation = db.query(PlanCaseRelation).filter(
                    PlanCaseRelation.plan_id == suite.plan_id,
                    PlanCaseRelation.case_id == case_id
                ).first()
                
                if relation:
                    relation.execution_status = plan_status
                    relation.execution_updated_at = beijing_now()
                    db.commit()
                    logger.info(f"[WebSocket] 已更新计划用例执行状态: plan_id={suite.plan_id}, case_id={case_id}, status={plan_status}")
                else:
                    logger.warning(f"[WebSocket] 未找到计划用例关联: plan_id={suite.plan_id}, case_id={case_id}")
            except Exception as e:
                logger.error(f"[WebSocket] 更新计划用例执行状态失败: {e}", exc_info=True)
                db.rollback()
        
        # A last case row does not prove process teardown has finished.
        # Only test_suite_completed releases its execution slot. Legacy rows
        # lacking execution_id must not guess an owner from the latest log.

    except Exception as e:
        logger.exception(f"[WebSocket] 处理测试套执行结果时出错: {e}")


async def handle_test_suite_log(db: Session, environment_id: str, message: dict):
    """处理测试套实时日志"""
    from models.test_suite import TestSuite, TestSuiteLog
    
    try:
        suite_id = message.get("suite_id")
        log_message = message.get("message", "")
        timestamp = message.get("timestamp")
        execution_id = message.get("execution_id")  # Agent发送的执行ID
        
        logger.debug(f"[WebSocket] 处理测试套日志: suite_id={suite_id}, execution_id={execution_id}, message_length={len(log_message) if log_message else 0}")
        
        if not suite_id:
            logger.warning(f"[WebSocket] 测试套日志缺少suite_id: {message}")
            return
        
        # 验证测试套存在
        suite = db.query(TestSuite).filter(TestSuite.id == suite_id).first()
        if not suite:
            logger.warning(f"[WebSocket] 测试套不存在: suite_id={suite_id}")
            return
        
        # 解析时间戳
        log_timestamp = beijing_now()
        if timestamp:
            try:
                # 处理ISO格式时间戳，支持带Z和不带Z的格式
                if timestamp.endswith('Z'):
                    log_timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                else:
                    log_timestamp = datetime.fromisoformat(timestamp)
            except Exception:
                logger.opt(exception=True).warning("解析日志时间戳失败，使用当前时间")
                log_timestamp = beijing_now()
        
        # 查找或创建日志记录（每个execution_id只创建一条记录）
        if execution_id:
            log_entry = db.query(TestSuiteLog).filter(
                TestSuiteLog.suite_id == suite_id,
                TestSuiteLog.execution_id == execution_id
            ).first()
            
            if log_entry:
                # 如果已存在，追加日志消息（换行分隔）
                if log_entry.message:
                    log_entry.message += ("" if message.get("raw") else "\n") + log_message
                else:
                    log_entry.message = log_message
                log_entry.timestamp = log_timestamp  # 更新最后时间戳
            else:
                # 如果不存在，创建新记录
                # 计算序号：获取该测试套的最大序号，然后+1
                from sqlalchemy import func
                max_sequence = db.query(func.max(TestSuiteLog.sequence_number)).filter(
                    TestSuiteLog.suite_id == suite_id,
                ).scalar() or 0
                sequence_number = max_sequence + 1
                
                log_entry = TestSuiteLog(
                    suite_id=suite_id,
                    execution_id=execution_id,
                    sequence_number=sequence_number,
                    message=log_message,
                    timestamp=log_timestamp
                )
                db.add(log_entry)
        else:
            # 如果没有execution_id，记录警告并创建新记录
            # 注意：正常情况下应该有execution_id，如果没有可能是旧版本Agent或配置问题
            logger.warning(f"[WebSocket] 测试套日志缺少execution_id: suite_id={suite_id}, message={log_message[:50]}")
            # 创建新记录（不追加到旧记录，确保每次执行都有独立记录）
            log_entry = TestSuiteLog(
                suite_id=suite_id,
                execution_id=None,
                message=log_message,
                timestamp=log_timestamp
            )
            db.add(log_entry)
        
        db.commit()
        db.refresh(log_entry)
        
        # 构建日志数据（用于实时推送）
        from services.bounded_logs import live_log_window
        log_data = live_log_window(log_entry, log_message)
        
        # 推送给所有订阅该测试套日志的前端
        await frontend_manager.broadcast_log(suite_id, log_data)
        
        # 如果日志消息包含"测试套执行已取消"或"执行完成"，计算执行耗时并保存到日志记录
        if execution_id and ("测试套执行已取消" in log_message or "测试套执行完成" in log_message or "执行完成" in log_message):
            # 从日志消息中解析时间戳来计算执行耗时
            import re
            
            duration_seconds = 0
            if log_entry.message:
                # 匹配时间戳格式：[YYYY-MM-DD HH:mm:ss.SSS]
                timestamp_pattern = r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})\]'
                timestamps = re.findall(timestamp_pattern, log_entry.message)
                
                if len(timestamps) >= 2:
                    # 解析第一条和最后一条日志的时间戳
                    try:
                        first_ts_str = timestamps[0]
                        last_ts_str = timestamps[-1]
                        first_ts = datetime.strptime(first_ts_str, "%Y-%m-%d %H:%M:%S.%f")
                        last_ts = datetime.strptime(last_ts_str, "%Y-%m-%d %H:%M:%S.%f")
                        duration_seconds = (last_ts - first_ts).total_seconds()
                    except (ValueError, AttributeError):
                        logger.opt(exception=True).warning("解析执行耗时失败，使用记录时间")
                        # 如果解析失败，使用created_at和timestamp的差值作为备选
                        if log_entry.created_at and log_entry.timestamp:
                            duration_seconds = (log_entry.timestamp - log_entry.created_at).total_seconds()
                elif len(timestamps) == 1:
                    # 如果只有一条日志，使用created_at和timestamp的差值
                    if log_entry.created_at and log_entry.timestamp:
                        duration_seconds = (log_entry.timestamp - log_entry.created_at).total_seconds()
                else:
                    # 如果没有时间戳，使用created_at和timestamp的差值
                    if log_entry.created_at and log_entry.timestamp:
                        duration_seconds = (log_entry.timestamp - log_entry.created_at).total_seconds()
            
            # 格式化总耗时并保存到日志记录
            if duration_seconds > 0:
                hours = int(duration_seconds // 3600)
                minutes = int((duration_seconds % 3600) // 60)
                seconds = duration_seconds % 60
                log_entry.duration = f"{hours}:{minutes:02d}:{seconds:05.2f}"
                
                # 如果是取消，更新测试套状态
                if "测试套执行已取消" in log_message or "已取消" in log_message:
                    suite.status = "pending"  # 取消后状态设为pending
                
                db.commit()
                logger.info(f"[WebSocket] 测试套执行耗时已保存到日志: suite_id={suite_id}, execution_id={execution_id}, duration={log_entry.duration}, status={suite.status}")
        
        logger.debug(f"[WebSocket] 测试套日志已存储并提交实时队列（非送达确认）: suite_id={suite_id}, execution_id={execution_id}, message={log_message[:50]}")
        
    except Exception as e:
        logger.exception(f"[WebSocket] 处理测试套日志时出错: {e}")
        db.rollback()


async def handle_test_suite_completed(db: Session, environment_id: str, message: dict):
    """处理测试套执行完成消息"""
    from services.task_queue_service import TaskQueueService
    from models.task_queue import TaskQueue
    from models.test_suite import TestSuite
    
    try:
        suite_id = message.get("suite_id")
        execution_id = message.get("execution_id")
        status = message.get("status")  # completed, failed, cancelled
        reported_case_count = message.get("reported_case_count")
        total_case_count = message.get("total_case_count")
        duration = message.get("duration")
        completion_message = message.get("message", "")
        
        if not suite_id or not execution_id:
            logger.warning(f"[WebSocket] 测试套完成消息缺少必要字段: {message}")
            return
        
        task = db.query(TaskQueue).filter(TaskQueue.execution_id == execution_id).first()
        if not task or task.suite_id != suite_id or task.environment_id != environment_id:
            return False
        if task.status in ["completed", "failed", "cancelled"]:
            return True
        if status not in ["completed", "failed", "cancelled"]:
            return False
        if message.get("event_id") and status == "completed":
            from services.suite_results import result_id, dispatch_case_ids
            from models.test_suite import TestSuiteExecution
            expected_suite = db.query(TestSuite).filter(TestSuite.id == suite_id).first()
            records = [db.get(TestSuiteExecution, result_id(execution_id, cid)) for cid in dispatch_case_ids(db, task, expected_suite)]
            if any(row is None or row.result in ["failed", "error"] for row in records):
                status = "failed"

        logger.info(f"[WebSocket] 收到测试套完成消息: suite_id={suite_id}, execution_id={execution_id}, status={status}")
        
        # 更新任务队列中的任务状态
        task_status_map = {
            "completed": "completed",
            "failed": "failed",
            "cancelled": "cancelled"
        }
        task_status = task_status_map.get(status, "completed")
        from services.inbox import notify
        notify(db, task.executor_id, execution_id, 'execution_completed', '测试任务已结束',
            f'执行 {execution_id}：{status}' + (f'。{completion_message}' if message.get('log_delivery') else ''), suite_id)
        TaskQueueService.complete_task(db, execution_id, task_status)
        
        # 获取测试套
        suite = db.query(TestSuite).filter(TestSuite.id == suite_id).first()
        if not suite:
            logger.warning(f"[WebSocket] 测试套不存在: suite_id={suite_id}")
            db.commit()
            return
        
        # 检查是否还有其他正在运行或等待的任务
        running_tasks = db.query(TaskQueue).filter(
            TaskQueue.suite_id == suite_id,
            TaskQueue.status == "running"
        ).count()
        pending_tasks = db.query(TaskQueue).filter(
            TaskQueue.suite_id == suite_id,
            TaskQueue.status == "pending"
        ).count()
        
        # 根据任务队列状态更新测试套状态
        if running_tasks > 0:
            suite.status = "running"
        elif pending_tasks > 0:
            suite.status = "pending"
        else:
            # 所有任务都完成了，根据完成消息的状态设置测试套状态
            if status == "cancelled":
                suite.status = "pending"  # 取消后设为pending
            elif status == "failed":
                suite.status = "failed"
            else:
                # completed状态，需要检查是否有失败的用例
                from models.test_suite import TestSuiteExecution
                from sqlalchemy import func
                
                if message.get("event_id"):
                    suite.status = "completed"
                else:
                    # 获取最近一次执行的记录
                    latest_execution_time = db.query(func.max(TestSuiteExecution.executed_at)).filter(
                        TestSuiteExecution.suite_id == suite_id
                    ).scalar()

                    if latest_execution_time:
                        latest_executions = db.query(TestSuiteExecution).filter(
                            TestSuiteExecution.suite_id == suite_id,
                            TestSuiteExecution.executed_at == latest_execution_time
                        ).all()

                        has_failed = any(e.result in ["failed", "error"] for e in latest_executions)
                        suite.status = "failed" if has_failed else "completed"
                    else:
                        # 如果没有执行记录，根据状态设置
                        suite.status = "completed"
        db.commit()
        logger.info(f"[WebSocket] 测试套状态已更新: suite_id={suite_id}, status={suite.status}, 任务状态={task_status}, 运行中任务={running_tasks}, 等待中任务={pending_tasks}")
        
        from services.queued_dispatch import dispatch_pending_suites
        await dispatch_pending_suites(db, environment_id)

        return True

    except Exception as e:
        logger.exception(f"[WebSocket] 处理测试套完成消息时出错: {e}")
        db.rollback()
        return False
