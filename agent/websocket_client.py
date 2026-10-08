"""WebSocket客户端模块"""

import asyncio
import json
import random
import time
from datetime import datetime
from typing import Dict, Any, Optional, Callable, Awaitable
from urllib.parse import urlparse, parse_qs, urlencode
import websockets
from websockets.exceptions import ConnectionClosed
from loguru import logger as default_logger


class WebSocketClient:
    """WebSocket客户端类"""

    def __init__(
        self,
        server_url: str,
        token: str,
        on_message: Optional[Callable[[Dict[str, Any]], Awaitable[None]]] = None,
        on_connect: Optional[Callable[[], Awaitable[None]]] = None,
        on_disconnect: Optional[Callable[[], Awaitable[None]]] = None,
        logger=None,
    ):
        """
        初始化WebSocket客户端

        Args:
            server_url: WebSocket服务器地址
            token: 认证Token
            on_message: 消息处理回调函数
            on_connect: 连接成功回调函数
            on_disconnect: 断开连接回调函数
            logger: 日志器
        """
        self.server_url = server_url
        self.token = token
        self.on_message = on_message
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.logger = logger or default_logger

        self.websocket: Optional[Any] = None  # websockets.WebSocketClientProtocol
        self.connected = False
        self.reconnect_interval = 1  # 初始重连间隔（秒）
        self.max_reconnect_interval = 60  # 最大重连间隔（秒）
        self.reconnect_delay = 3  # 重连延迟时间（秒），从服务器配置获取
        self._reconnect_task: Optional[asyncio.Task] = None
        self._should_reconnect = True
        self.on_log_message = None
        self.session_id: Optional[str] = None
        self.protocol_version = 2
        self.server_capabilities = frozenset()
        self.handshake_timeout = 10.0
        self.heartbeat_timeout = 90.0
        self.send_timeout = 5.0
        self._connect_lock = asyncio.Lock()
        self._send_lock = asyncio.Lock()
        self._connected_at = 0.0
        self._generation = 0
        self._healthy_after = 30.0

    def _build_url(self) -> str:
        """
        构建带Token的WebSocket URL

        Returns:
            完整的WebSocket URL
        """
        parsed = urlparse(self.server_url)
        query_params = parse_qs(parsed.query)
        query_params["token"] = [self.token]
        query_params["protocol_version"] = [str(self.protocol_version)]
        new_query = urlencode(query_params, doseq=True)

        # 重建URL
        if parsed.scheme == "wss":
            scheme = "wss"
        else:
            scheme = "ws"

        netloc = parsed.netloc
        path = parsed.path

        return f"{scheme}://{netloc}{path}?{new_query}"

    async def connect(self) -> bool:
        """Become ready only after the controller authenticates a v2 session.

        Upgraded agents fail closed against older controllers. The controller
        continues to accept legacy agents with socket-identity fencing.
        """
        async with self._connect_lock:
            if self.connected:
                return True
            connection = None
            try:
                connection = await websockets.connect(
                    self._build_url(),
                    ping_interval=20,
                    ping_timeout=10,
                    close_timeout=1,
                    open_timeout=self.handshake_timeout,
                    max_size=16 * 1024 * 1024,
                )

                async def handshake():
                    welcome = json.loads(await connection.recv())
                    authenticated = json.loads(await connection.recv())
                    if (
                        not isinstance(welcome, dict)
                        or not isinstance(authenticated, dict)
                        or welcome.get("type") != "welcome"
                        or authenticated.get("type") != "auth_success"
                        or not isinstance(welcome.get("session_id"), str)
                        or not welcome["session_id"]
                        or authenticated.get("session_id") != welcome["session_id"]
                        or type(welcome.get("protocol_version")) is not int
                        or welcome["protocol_version"] != self.protocol_version
                        or type(authenticated.get("protocol_version")) is not int
                        or authenticated["protocol_version"] != self.protocol_version
                    ):
                        raise ValueError(
                            "Controller does not support the Agent v2 session protocol"
                        )
                    return welcome, authenticated

                welcome, authenticated = await asyncio.wait_for(
                    handshake(), self.handshake_timeout
                )
                if not self._should_reconnect:
                    await connection.close()
                    return False
                self._generation += 1
                self.websocket = connection
                self.session_id = welcome["session_id"]
                self.server_capabilities = frozenset(welcome.get("capabilities", []))
                self.heartbeat_timeout = max(
                    1.0, min(300.0, float(welcome.get("heartbeat_timeout", 90)))
                )
                self.connected = True
                self._connected_at = time.monotonic()
                self.set_reconnect_delay(welcome.get("reconnect_delay", 3))
                await self.send_auth_message()
                if not self.connected:
                    return False
                if self.on_message:
                    await self.on_message(welcome)
                    await self.on_message(authenticated)
                if self.on_connect:
                    await self.on_connect()
                return self.connected and self.websocket is connection
            except asyncio.CancelledError:
                if connection:
                    await connection.close()
                raise
            except Exception:
                if self.websocket is connection:
                    self.connected = False
                    self.websocket = None
                    self.session_id = None
                if connection:
                    await connection.close()
                self.logger.exception(
                    "Agent WebSocket connection/authentication failed"
                )
                return False

    async def send_auth_message(self) -> None:
        """发送认证消息"""
        try:
            from .utils import get_platform_info
        except ImportError:
            from utils import get_platform_info

        platform_info = get_platform_info()
        auth_message = {
            "type": "auth",
            "capabilities": ["log_batch_v1", "script_jobs_v1", "native_http_variables_v1", "native_http_processors_v1"],
            "token": self.token,
            "agent_info": {
                "version": "1.0.0",
                "platform": platform_info["platform"],
                "python_version": platform_info["python_version"],
            },
        }
        await self.send_message(auth_message)

    async def _retire(self, connection) -> None:
        """An old send/receiver failure must never clear a newer socket."""
        if self.websocket is connection:
            self.connected = False
            self.websocket = None
            self.session_id = None
        try:
            await asyncio.wait_for(connection.close(), 1.0)
        except Exception:
            self.logger.debug("Agent socket close timed out or failed")

    async def send_message(self, message: Dict[str, Any], *, _log_replay=False) -> bool:
        # Commit logs even while disconnected; only replay uses the live socket.
        if (
            not _log_replay
            and self.on_log_message
            and message.get("type") in {"test_suite_log", "task_log", "script_job_log"}
        ):
            return await self.on_log_message(message)
        connection, session_id = self.websocket, self.session_id
        if not self.connected or connection is None or not session_id:
            return False
        try:
            async with self._send_lock:
                if (
                    not self.connected
                    or self.websocket is not connection
                    or self.session_id != session_id
                    or connection is None
                ):
                    return False
                # Rebind durable outbox events on replay. Never mutate the saved
                # payload or pin an execution/event ID to a dead transport.
                payload = dict(
                    message,
                    session_id=session_id,
                    protocol_version=self.protocol_version,
                )
                await asyncio.wait_for(
                    connection.send(json.dumps(payload, ensure_ascii=False)),
                    self.send_timeout,
                )
            return self.connected and self.websocket is connection
        except Exception:
            self.logger.exception("Agent WebSocket send failed")
            await self._retire(connection)
            return False

    async def send_log_legacy(self, message):
        """Legacy log capability compatibility; preserve the session envelope."""
        return await self.send_message(message, _log_replay=True)

    async def send_heartbeat(self, system_info: Dict[str, Any]) -> bool:
        """
        发送心跳消息

        Args:
            system_info: 系统信息字典

        Returns:
            是否发送成功
        """
        # 后端期望的格式: {"type": "heartbeat", "data": {...}}
        # 需要将system_info转换为后端期望的格式
        node_info = {
            "node_ip": system_info.get("network", {}).get("ip", ""),
            "os_type": system_info.get("os", {}).get("type", ""),
            "os_version": system_info.get("os", {}).get("version", ""),
            "cpu_info": system_info.get("cpu", {}),
            "memory_info": system_info.get("memory", {}),
            "disk_info": system_info.get("disk", {}),
        }

        message = {"type": "heartbeat", "data": node_info}
        return await self.send_message(message)

    async def send_task_result(
        self,
        task_id: str,
        status: str,
        exit_code: int,
        output: str,
        error: Optional[str],
        duration: float,
    ) -> bool:
        """
        发送任务执行结果

        Args:
            task_id: 任务ID
            status: 任务状态 (success/failed/error/timeout)
            exit_code: 退出码
            output: 标准输出
            error: 错误信息
            duration: 执行时长（秒）

        Returns:
            是否发送成功
        """
        message = {
            "type": "task_result",
            "task_id": task_id,
            "status": status,
            "exit_code": exit_code,
            "output": output,
            "error": error,
            "duration": duration,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        return await self.send_message(message)

    async def send_task_log(self, task_id: str, level: str, message: str) -> bool:
        """
        发送任务日志

        Args:
            task_id: 任务ID
            level: 日志级别 (info/warning/error)
            message: 日志内容

        Returns:
            是否发送成功
        """
        log_message = {
            "type": "task_log",
            "raw": True,
            "task_id": task_id,
            "level": level,
            "message": message,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        return await self.send_message(log_message)

    async def receive_messages(self) -> None:
        """Reconnect after normal close, network failure or missing controller liveness."""
        while self._should_reconnect:
            if not self.connected or not self.websocket:
                await self._start_reconnect()
                if self._reconnect_task:
                    await self._reconnect_task
                continue
            connection, session_id = self.websocket, self.session_id
            generation = self._generation
            try:
                while (
                    self._should_reconnect
                    and self.websocket is connection
                    and self.connected
                ):
                    raw = await asyncio.wait_for(
                        connection.recv(), self.heartbeat_timeout
                    )
                    if self.websocket is not connection or not self.connected:
                        break
                    data = json.loads(raw)
                    if (
                        not isinstance(data, dict)
                        or not isinstance(data.get("type"), str)
                        or data.get("session_id") != session_id
                        or type(data.get("protocol_version")) is not int
                        or data["protocol_version"] != self.protocol_version
                    ):
                        raise ValueError("Invalid controller session frame")
                    if time.monotonic() - self._connected_at >= self._healthy_after:
                        self.reconnect_interval = 1
                    if self.on_message:
                        await self.on_message(data)
            except ConnectionClosed:
                pass
            except asyncio.CancelledError:
                raise
            except Exception:
                self.logger.exception("Agent WebSocket receive failed")
            finally:
                was_current = self.websocket is connection
                await self._retire(connection)
                if (
                    was_current
                    and self._generation == generation
                    and self.on_disconnect
                ):
                    await self.on_disconnect()

    async def _start_reconnect(self) -> None:
        if not self._reconnect_task or self._reconnect_task.done():
            self._reconnect_task = asyncio.create_task(self._reconnect_loop())

    def set_reconnect_delay(self, delay: int) -> None:
        try:
            self.reconnect_delay = max(1, min(60, int(delay)))
        except (ValueError, TypeError):
            self.logger.warning("Invalid Agent reconnect delay")

    async def _reconnect_loop(self) -> None:
        while self._should_reconnect and not self.connected:
            # Quick connect/disconnect loops retain backoff, avoiding a retry
            # storm. Jitter spreads multiple agents reconnecting after restart.
            delay = min(
                self.max_reconnect_interval,
                max(self.reconnect_delay, self.reconnect_interval),
            )
            await asyncio.sleep(random.uniform(delay * 0.8, delay))
            if not self._should_reconnect:
                return
            self.reconnect_interval = min(
                max(delay, self.reconnect_interval) * 2, self.max_reconnect_interval
            )
            if await self.connect():
                return

    async def close(self) -> None:
        self._should_reconnect = False
        if self._reconnect_task and not self._reconnect_task.done():
            self._reconnect_task.cancel()
            await asyncio.gather(self._reconnect_task, return_exceptions=True)
        connection = self.websocket
        if connection:
            await self._retire(connection)
        self.connected = False
