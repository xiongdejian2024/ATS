"""WebSocket服务器 - 用于Agent连接和前端连接"""
from fastapi import WebSocket, WebSocketDisconnect
from services.environment_service import EnvironmentService
from core.logger import logger
from typing import Dict
from services.frontend_log_stream import FrontendConnectionManager
from sqlalchemy.orm import Session
import json
import asyncio
from datetime import datetime
from utils.datetime_utils import beijing_now


class ConnectionManager:
    """WebSocket连接管理器"""
    
    def __init__(self):
        # 存储活跃连接: {environment_id: websocket}
        self.active_connections: Dict[str, WebSocket] = {}
        # 存储token到environment_id的映射: {token: environment_id}
        self.token_to_env: Dict[str, str] = {}
    
    async def connect(self, websocket: WebSocket, environment_id: str, token: str = None):
        """注册WebSocket连接（连接已在外部accept）"""
        self.active_connections[environment_id] = websocket
        # 存储token映射
        if token:
            self.token_to_env[token] = environment_id
        logger.info(f"[WebSocket] 环境 {environment_id} 已连接")
    
    def disconnect(self, environment_id: str):
        """断开WebSocket连接"""
        if environment_id in self.active_connections:
            del self.active_connections[environment_id]
        # 清理token映射
        self.token_to_env = {k: v for k, v in self.token_to_env.items() if v != environment_id}
        logger.info(f"[WebSocket] 环境 {environment_id} 已断开")
    
    async def disconnect_and_notify(self, environment_id: str, reason: str = "Token已失效，请重新连接"):
        """断开连接并发送通知消息"""
        if environment_id in self.active_connections:
            websocket = self.active_connections[environment_id]
            try:
                # 发送token失效通知
                await websocket.send_json({
                    "type": "token_invalid",
                    "message": reason,
                    "reason": "token_regenerated"
                })
                # 关闭连接
                await websocket.close(code=1008, reason=reason)
            except Exception as e:
                logger.error(f"[WebSocket] 断开连接时出错 {environment_id}: {e}")
            finally:
                self.disconnect(environment_id)
    
    async def send_message(self, environment_id: str, message: dict):
        """向指定环境发送消息"""
        if environment_id in self.active_connections:
            try:
                await self.active_connections[environment_id].send_json(message)
                return True
            except Exception as e:
                logger.error(f"[WebSocket] 发送消息失败 {environment_id}: {e}")
                self.disconnect(environment_id)
                return False
        return False
    
    async def broadcast(self, message: dict):
        """广播消息到所有连接"""
        disconnected = []
        for environment_id, websocket in self.active_connections.items():
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"[WebSocket] 广播失败 {environment_id}: {e}")
                disconnected.append(environment_id)
        
        # 清理断开的连接
        for env_id in disconnected:
            self.disconnect(env_id)


# 全局连接管理器
manager = ConnectionManager()


# 全局前端连接管理器
frontend_manager = FrontendConnectionManager()


async def websocket_endpoint(
    websocket: WebSocket,
    token: str
):
    """
    WebSocket端点 - Agent连接入口
    
    连接URL: ws://host:port/ws/agent?token=xxx
    """
    from database import SessionLocal
    db = SessionLocal()
    environment_id = None
    
    try:
        # 必须先accept连接，然后才能关闭或使用
        try:
            await websocket.accept()
        except Exception as e:
            logger.error(f"[WebSocket] 接受连接失败: {e}")
            db.close()
            return
        
        # 根据token查找环境
        environment = EnvironmentService.get_environment_by_token(db, token)
        
        if not environment:
            # 记录token信息用于调试
            token_preview = token[:20] + "..." if token and len(token) > 20 else (token or "None")
            logger.warning(f"[WebSocket] 无效的token: {token_preview} (token长度: {len(token) if token else 0})")
            logger.warning(f"[WebSocket] 提示: Agent应使用环境管理页面生成的token，而不是JWT token")
            # 已accept，可以关闭连接
            try:
                await websocket.close(code=1008, reason="Invalid token - Please use environment token, not JWT token")
            except Exception as e:
                logger.error(f"[WebSocket] 关闭连接时出错: {e}")
            db.close()
            return
        
        environment_id = environment.get("id")
        if not environment_id:
            logger.warning(f"[WebSocket] 环境ID不存在")
            try:
                await websocket.close(code=1008, reason="Environment not found")
            except Exception as e:
                logger.error(f"[WebSocket] 关闭连接时出错: {e}")
            db.close()
            return
        
        # 建立连接（已经accept了，这里只是注册连接）
        await manager.connect(websocket, environment_id, token)
        
        # 更新在线状态
        EnvironmentService.update_node_info(
            db,
            environment_id,
            {"is_online": True}  # 仅更新在线状态，其他信息通过心跳更新
        )
        
        try:
            # 获取重连延迟配置（默认30秒）
            reconnect_delay = environment.get("reconnect_delay") or environment.get("reconnectDelay") or "30"
            try:
                reconnect_delay_int = int(reconnect_delay)
            except (ValueError, TypeError):
                reconnect_delay_int = 30
            
            # 获取工作目录
            work_dir = environment.get("remote_work_dir") or environment.get("remoteWorkDir") or ""
            
            # 发送欢迎消息（包含配置信息）
            logger.info(f"[WebSocket] 准备发送欢迎消息，环境ID: {environment_id}")
            try:
                await websocket.send_json({
                    "type": "welcome",
                    "message": "连接成功",
                    "environment_id": environment_id,
                    "environment_name": environment.get("name"),
                    "work_dir": work_dir,
                    "reconnect_delay": reconnect_delay_int  # 重连延迟时间（秒）
                })
                logger.debug(f"[WebSocket] 欢迎消息已发送")
            except Exception as e:
                logger.error(f"[WebSocket] 发送欢迎消息失败: {e}", exc_info=True)
                raise
            
            # 发送认证成功消息（兼容旧版本agent）
            try:
                await websocket.send_json({
                    "type": "auth_success",
                    "environment_id": environment_id,
                    "work_dir": work_dir,
                    "reconnect_delay": reconnect_delay_int  # 重连延迟时间（秒）
                })
                logger.debug(f"[WebSocket] 认证成功消息已发送")
            except Exception as e:
                logger.error(f"[WebSocket] 发送认证成功消息失败: {e}", exc_info=True)
                raise
            
            from services.queued_dispatch import dispatch_pending_suites
            await dispatch_pending_suites(db, environment_id)

            # 保持连接，接收消息
            logger.info(f"[WebSocket] 进入消息接收循环，环境ID: {environment_id}")
            while True:
                try:
                    # 接收消息（超时30秒）
                    logger.debug(f"[WebSocket] 等待接收消息...")
                    data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                    logger.debug("[WebSocket] 收到消息字节数={}", len(data))
                    message = json.loads(data)
                    message_type = message.get('type', 'unknown')
                    logger.info("[WebSocket] 收到消息：类型={}，执行={}，用例={}", message_type, message.get("execution_id"), message.get("case_id"))
                    
                    # 特别记录test_suite_result消息
                    if message_type == "test_suite_result":
                        logger.info(f"[WebSocket] ===== 收到test_suite_result消息 ===== suite_id={message.get('suite_id')}, case_id={message.get('case_id')}, result={message.get('result')}")
                    
                    # 处理心跳消息
                    if message.get("type") == "heartbeat":
                        node_info = message.get("data", {})
                        # 更新节点信息
                        EnvironmentService.update_node_info(db, environment_id, node_info)
                        # 回复心跳确认
                        try:
                            await websocket.send_json({
                                "type": "heartbeat_ack",
                                "timestamp": beijing_now().isoformat()
                            })
                        except (WebSocketDisconnect, Exception) as e:
                            logger.warning(f"[WebSocket] 发送心跳确认失败，连接可能已断开: {e}")
                            break  # 退出循环
                    
                    # 处理任务结果
                    elif message.get("type") == "task_result":
                        # TODO: 处理任务执行结果
                        logger.info(f"[WebSocket] 收到任务结果: {message}")
                    
                    # 处理测试套执行结果
                    elif message.get("type") == "test_suite_result":
                        logger.info(f"[WebSocket] 收到测试套执行结果消息: suite_id={message.get('suite_id')}, case_id={message.get('case_id')}, result={message.get('result')}")
                        accepted = await handle_test_suite_result(db, environment_id, message)
                        if accepted and message.get("event_id"):
                            await websocket.send_json({"type": "sat_event_ack", "event_id": message["event_id"]})
                    
                    # 处理测试套实时日志
                    elif message.get("type") == "test_suite_log":
                        await handle_test_suite_log(db, environment_id, message)
                    
                    # 处理测试套执行完成消息
                    elif message.get("type") == "test_suite_completed":
                        accepted = await handle_test_suite_completed(db, environment_id, message)
                        if accepted and message.get("event_id"):
                            await websocket.send_json({"type": "sat_event_ack", "event_id": message["event_id"]})
                    
                    # 处理工作空间响应（从Agent返回）
                    elif message.get("type") in [
                        "workspace_list_response",
                        "workspace_read_response",
                        "workspace_write_response",
                        "workspace_delete_response",
                        "workspace_mkdir_response"
                    ]:
                        # 转发响应到workspace API模块
                        logger.debug(f"[WebSocket] 收到工作空间响应: {message.get('type')}, request_id: {message.get('request_id')}")
                        from api.v1.workspace import handle_workspace_response
                        try:
                            handle_workspace_response(message)
                        except Exception as e:
                            logger.exception(f"[WebSocket] 处理工作空间响应时出错: {e}")
                    
                    else:
                        logger.warning(f"[WebSocket] 收到未知消息类型: {message.get('type')}")
                        
                except asyncio.TimeoutError:
                    # 超时，发送ping保持连接
                    logger.debug(f"[WebSocket] 接收消息超时，发送ping保持连接")
                    try:
                        await websocket.send_json({"type": "ping"})
                    except Exception as e:
                        logger.warning(f"[WebSocket] 发送ping失败，连接可能已断开: {e}")
                        break  # 退出循环
                except json.JSONDecodeError as e:
                    logger.warning(f"[WebSocket] 收到无效JSON: {data}, 错误: {e}")
                except WebSocketDisconnect:
                    # WebSocket断开连接，重新抛出让外层处理
                    logger.info(f"[WebSocket] 检测到WebSocket断开连接")
                    raise
                except Exception as e:
                    error_msg = str(e)
                    # 检查是否是断开连接相关的错误
                    if "disconnect" in error_msg.lower() or "receive" in error_msg.lower():
                        logger.info(f"[WebSocket] 连接已断开: {error_msg}")
                        break  # 退出循环
                    else:
                        logger.error(f"[WebSocket] 处理消息时出错: {e}", exc_info=True)
                        # 继续循环，不中断连接
                    
        except WebSocketDisconnect:
            logger.info(f"[WebSocket] 客户端断开连接: {environment_id}")
        except Exception as e:
            logger.exception(f"[WebSocket] 连接错误: {e}")
    except Exception as e:
        # 处理外层异常（如数据库错误）
        logger.exception(f"[WebSocket] 初始化连接错误: {e}")
        try:
            await websocket.close(code=1011, reason=f"Server error: {str(e)}")
        except:
            pass
    finally:
        # 断开连接，更新离线状态
        if environment_id:
            try:
                manager.disconnect(environment_id)
                EnvironmentService.mark_node_offline(db, environment_id)
            except Exception as e:
                logger.error(f"[WebSocket] 清理连接时出错: {e}")
        try:
            db.close()
        except:
            pass


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
                    log_entry.message += "\n" + log_message
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
            f'执行 {execution_id}：{status}', suite_id)
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
