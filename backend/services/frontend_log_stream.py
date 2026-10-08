"""Bounded, ordered best-effort live delivery; SQL history remains authoritative."""

import asyncio
import json
from dataclasses import dataclass
from typing import Dict, List

from fastapi import WebSocket

from core.logger import logger


@dataclass
class _Subscriber:
    websocket: WebSocket
    suite_id: str
    queue: asyncio.Queue
    pending_bytes: int = 0
    pending_messages: int = 0
    sender: asyncio.Task | None = None


class FrontendConnectionManager:
    """One FIFO/sender per socket, including connection and heartbeat frames.

    Enqueueing never waits for socket I/O and does not acknowledge delivery. Limits
    include the in-flight frame. An overloaded/failed subscriber is detached before
    asynchronous cleanup, without trimming or altering persisted logs. Reconnect
    with a new socket and fetch HTTP log history to recover any missed live data.
    """

    def __init__(
        self,
        *,
        max_pending_messages: int = 64,
        max_pending_bytes: int = 1024 * 1024,
        send_timeout: float = 5.0,
        close_timeout: float = 1.0,
    ):
        if min(max_pending_messages, max_pending_bytes, send_timeout, close_timeout) <= 0:
            raise ValueError("Log stream limits and timeouts must be positive")
        self.max_pending_messages = max_pending_messages
        self.max_pending_bytes = max_pending_bytes
        self.send_timeout = send_timeout
        self.close_timeout = close_timeout
        self.frontend_connections: Dict[str, List[WebSocket]] = {}
        self._subscribers: Dict[WebSocket, _Subscriber] = {}
        self._tasks: set[asyncio.Task] = set()
        self._retiring: Dict[WebSocket, asyncio.Task] = {}

    def _track(self, coroutine, name):
        task = asyncio.create_task(coroutine, name=name)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return task

    async def connect(self, websocket: WebSocket, suite_id: str):
        """Register an already accepted, authorized socket; no network I/O."""
        if websocket in self._retiring:
            raise ValueError("Reconnect using a new WebSocket")
        if websocket in self._subscribers:
            if self._subscribers[websocket].suite_id != suite_id:
                raise ValueError("WebSocket already subscribed to another suite")
            return
        subscriber = _Subscriber(
            websocket, suite_id, asyncio.Queue(maxsize=self.max_pending_messages)
        )
        self._subscribers[websocket] = subscriber
        connections = self.frontend_connections.setdefault(suite_id, [])
        connections.append(websocket)
        subscriber.sender = self._track(self._send(subscriber), "ats-log-sender")
        logger.info(
            "[Frontend WebSocket] 订阅测试套 {} 日志，当前连接数: {}",
            suite_id,
            len(connections),
        )

    def disconnect(self, websocket: WebSocket, suite_id: str):
        """Detach immediately; return bounded cleanup to await at route teardown."""
        subscriber = self._subscribers.get(websocket)
        if subscriber is None:
            return self._retiring.get(websocket)
        if subscriber.suite_id != suite_id:
            return None
        return self._stop(subscriber)

    def is_connected(self, websocket: WebSocket, suite_id: str) -> bool:
        subscriber = self._subscribers.get(websocket)
        return subscriber is not None and subscriber.suite_id == suite_id

    def _stop(self, subscriber, *, code=None, reason=""):
        websocket, suite_id = subscriber.websocket, subscriber.suite_id
        if self._subscribers.get(websocket) is not subscriber:
            return self._retiring.get(websocket)
        del self._subscribers[websocket]
        connections = self.frontend_connections[suite_id]
        connections.remove(websocket)
        if not connections:
            del self.frontend_connections[suite_id]
        # Release queued payloads immediately. The sender owns any in-flight frame
        # and releases its accounting in finally before the close is attempted.
        while not subscriber.queue.empty():
            _, size = subscriber.queue.get_nowait()
            subscriber.queue.task_done()
            subscriber.pending_bytes -= size
            subscriber.pending_messages -= 1
        sender = subscriber.sender
        if sender is not asyncio.current_task():
            sender.cancel()
        cleanup = self._track(self._retire(subscriber, code, reason), "ats-log-cleanup")
        self._retiring[websocket] = cleanup
        cleanup.add_done_callback(lambda _: self._retiring.pop(websocket, None))
        logger.info("[Frontend WebSocket] 取消订阅测试套 {} 日志", suite_id)
        return cleanup

    async def _retire(self, subscriber, code, reason):
        # Even cancellation before the sender starts must still run cleanup.
        await asyncio.gather(subscriber.sender, return_exceptions=True)
        if code is not None:
            try:
                async with asyncio.timeout(self.close_timeout):
                    await subscriber.websocket.close(code=code, reason=reason)
            except Exception as exc:
                logger.warning("[Frontend WebSocket] 关闭日志连接失败: {}", exc)

    async def _send(self, subscriber):
        try:
            while True:
                payload, size = await subscriber.queue.get()
                try:
                    async with asyncio.timeout(self.send_timeout):
                        await subscriber.websocket.send_text(payload)
                finally:
                    subscriber.queue.task_done()
                    subscriber.pending_bytes -= size
                    subscriber.pending_messages -= 1
        except asyncio.CancelledError:
            raise
        except TimeoutError:
            logger.warning(
                "[Frontend WebSocket] 测试套 {} 日志发送超时；断开慢订阅，完整日志保留在历史记录",
                subscriber.suite_id,
            )
            self._stop(
                subscriber, code=1013, reason="Log stream too slow; reconnect and reload history"
            )
        except Exception as exc:
            logger.warning("[Frontend WebSocket] 日志发送失败: {}", exc)
            self._stop(
                subscriber, code=1011, reason="Log delivery failed; reconnect and reload history"
            )

    def _enqueue(self, subscriber, payload, size) -> bool:
        if (
            subscriber.pending_messages >= self.max_pending_messages
            or subscriber.pending_bytes + size > self.max_pending_bytes
        ):
            logger.warning(
                "[Frontend WebSocket] 测试套 {} 日志缓冲达到上限 ({} 条 / {} 字节)；"
                "断开订阅，须重新读取历史记录",
                subscriber.suite_id,
                subscriber.pending_messages,
                subscriber.pending_bytes,
            )
            self._stop(
                subscriber, code=1013, reason="Log buffer full; reconnect and reload history"
            )
            return False
        subscriber.queue.put_nowait((payload, size))
        subscriber.pending_messages += 1
        subscriber.pending_bytes += size
        return True

    def enqueue_message(self, websocket: WebSocket, suite_id: str, message: dict) -> bool:
        """Return queue acceptance only, never a network delivery confirmation."""
        subscriber = self._subscribers.get(websocket)
        if subscriber is None or subscriber.suite_id != suite_id:
            return False
        payload = json.dumps(message, ensure_ascii=False, separators=(",", ":"))
        return self._enqueue(subscriber, payload, len(payload.encode("utf-8")))

    async def broadcast_log(self, suite_id: str, log_data: dict):
        """Snapshot and enqueue in order without waiting for any subscriber."""
        connections = self.frontend_connections.get(suite_id)
        if not connections:
            return
        payload = json.dumps(
            ({"type": "script_job_log", "job_id": log_data["script_job_id"], "execution_id": log_data["execution_id"], "data": log_data}
             if "script_job_id" in log_data else {"type": "test_suite_log", "suite_id": suite_id, "data": log_data}),
            ensure_ascii=False,
            separators=(",", ":"),
        )
        size = len(payload.encode("utf-8"))
        for websocket in tuple(connections):
            self._enqueue(self._subscribers[websocket], payload, size)
        # A producer may already have many Agent messages buffered. Give healthy
        # senders a scheduling turn without waiting for any socket or its timeout.
        await asyncio.sleep(0)

    async def aclose(self):
        """Drain task ownership at server shutdown; do not flush stale live logs."""
        for subscriber in list(self._subscribers.values()):
            self._stop(
                subscriber, code=1001, reason="Server shutdown; reconnect and reload history"
            )
        if self._tasks:
            await asyncio.gather(*tuple(self._tasks), return_exceptions=True)
            # gather may finish synchronously when all tasks are already done;
            # let their registered ownership-cleanup callbacks run before return.
            await asyncio.sleep(0)
