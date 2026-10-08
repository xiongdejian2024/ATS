"""Single-controller socket/session ownership, never a distributed lease."""

import asyncio
import time
import uuid
from dataclasses import dataclass, field

from core.agent_protocol import (
    CLOSE_TIMEOUT,
    HEARTBEAT_TIMEOUT,
    PROTOCOL_VERSION,
    SEND_TIMEOUT,
)
from core.logger import logger


@dataclass(eq=False)
class AgentSession:
    environment_id: str
    websocket: object
    token: str | None
    protocol_version: int
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    last_seen: float = field(default_factory=time.monotonic)
    last_status_write: float = 0.0
    capabilities: frozenset = field(default_factory=frozenset)
    auth_received: bool = False
    send_lock: asyncio.Lock = field(default_factory=asyncio.Lock)


class ConnectionManager:
    """Fence callbacks by socket identity and an unguessable per-connect generation.

    Inbound handlers and replacement registration share an environment lock. A
    handler already admitted finishes before replacement; every subsequent frame
    and ACK must belong to the current session. DB writes use this same process,
    not a database lease: run ONE controller worker, including API dispatch.
    """

    def __init__(self):
        self.active_connections = {}
        self.token_to_env = {}
        self.sessions = {}
        self._locks = {}
        self._closing = set()
        self.heartbeat_timeout = HEARTBEAT_TIMEOUT
        self.send_timeout = SEND_TIMEOUT

    def session_lock(self, environment_id):
        return self._locks.setdefault(environment_id, asyncio.Lock())

    def is_current(self, session):
        return bool(
            session
            and self.sessions.get(session.environment_id) is session
            and self.active_connections.get(session.environment_id) is session.websocket
        )

    def is_live(self, session):
        return (
            self.is_current(session)
            and time.monotonic() - session.last_seen < self.heartbeat_timeout
        )

    async def connect(
        self, websocket, environment_id, token=None, protocol_version=1, authorize=None
    ):
        async with self.session_lock(environment_id):
            # Authentication may have waited behind an admitted handler while
            # an administrator revoked the token. Recheck before registration.
            if authorize is not None and not authorize():
                return None
            previous = self.sessions.get(environment_id)
            session = AgentSession(environment_id, websocket, token, protocol_version)
            self.sessions[environment_id] = session
            self.active_connections[environment_id] = websocket
            self.token_to_env = {
                k: v for k, v in self.token_to_env.items() if v != environment_id
            }
            if token:
                self.token_to_env[token] = environment_id
            if previous:
                self._close_later(previous, 4001, "Agent session replaced")
            logger.info(
                "[WebSocket] Agent session connected: {} / {}",
                environment_id,
                session.session_id,
            )
            return session

    def disconnect(self, environment_id, session):
        """Compare-and-remove only; stale finalizers must not change DB or mapping."""
        if (
            not session
            or session.environment_id != environment_id
            or not self.is_current(session)
        ):
            return False
        del self.sessions[environment_id]
        self.active_connections.pop(environment_id, None)
        self.token_to_env = {
            k: v for k, v in self.token_to_env.items() if v != environment_id
        }
        # No await between ownership check, removal and the DB status write.
        from database import SessionLocal
        from services.environment_service import EnvironmentService

        with SessionLocal() as db:
            try:
                EnvironmentService.mark_node_offline(db, environment_id)
                from services.script_jobs import mark_disconnected
                mark_disconnected(db, environment_id)
            except Exception:
                db.rollback()
                logger.exception(
                    "Failed to persist Agent offline status: {}", environment_id
                )
        return True

    def _close_later(self, session, code, reason):
        async def close():
            try:
                await asyncio.wait_for(
                    session.websocket.close(code=code, reason=reason), CLOSE_TIMEOUT
                )
            except Exception:
                logger.debug(
                    "Agent socket close did not finish: {}", session.session_id
                )

        task = asyncio.create_task(close())
        self._closing.add(task)
        task.add_done_callback(self._closing.discard)

    async def disconnect_and_notify(
        self, environment_id, reason="Token已失效，请重新连接"
    ):
        session = self.sessions.get(environment_id)
        if not session:
            return
        if not self.disconnect(environment_id, session):
            return
        try:
            await asyncio.wait_for(
                session.websocket.send_json(
                    {
                        "type": "token_invalid",
                        "message": reason,
                        "reason": "token_regenerated",
                        "session_id": session.session_id,
                        "protocol_version": PROTOCOL_VERSION,
                    }
                ),
                self.send_timeout,
            )
        except Exception:
            logger.debug("Could not notify invalidated Agent session")
        finally:
            self._close_later(session, 1008, reason)

    async def send_session(self, session, message):
        if not self.is_live(session):
            if self.disconnect(session.environment_id, session):
                self._close_later(session, 4000, "Agent heartbeat timeout")
            return False
        try:
            async with session.send_lock:
                if not self.is_live(session):
                    return False
                payload = dict(
                    message,
                    session_id=session.session_id,
                    protocol_version=PROTOCOL_VERSION,
                )
                await asyncio.wait_for(
                    session.websocket.send_json(payload), self.send_timeout
                )
                return self.is_current(session)
        except Exception:
            logger.exception("Agent send failed: {}", session.environment_id)
            if self.disconnect(session.environment_id, session):
                self._close_later(session, 1011, "Agent send failed")
            return False

    async def send_message(self, environment_id, message):
        session = self.sessions.get(environment_id)
        return await self.send_session(session, message) if session else False

    async def broadcast(self, message):
        for session in list(self.sessions.values()):
            await self.send_session(session, message)

    def touch(self, db, session, node_info=None):
        """Called only for a validated frame while holding the admission lock."""
        if not self.is_live(session):
            return False
        from services.environment_service import EnvironmentService

        now = time.monotonic()
        if node_info is not None or now - session.last_status_write >= 5:
            EnvironmentService.update_node_info(
                db, session.environment_id, node_info or {}
            )
            session.last_status_write = now
        session.last_seen = time.monotonic()
        return True

    async def aclose(self):
        for session in list(self.sessions.values()):
            if self.disconnect(session.environment_id, session):
                self._close_later(session, 1001, "Controller stopping")
        if self._closing:
            await asyncio.gather(*list(self._closing), return_exceptions=True)
        self._locks.clear()

    @staticmethod
    def reset_online_status():
        """Crash/restart recovery for the supported single-controller deployment."""
        from database import SessionLocal
        from models.environment import Environment

        with SessionLocal() as db:
            db.query(Environment).filter(Environment.is_online.is_(True)).update(
                {"is_online": False}
            )
            from models.script_job import ScriptJobRun
            from models.task_queue import TaskQueue
            active = db.query(TaskQueue.execution_id).filter_by(kind="script", status="running")
            db.query(ScriptJobRun).filter(ScriptJobRun.execution_id.in_(active), ScriptJobRun.result.is_(None)).update(
                {"delivery_state": "unknown", "error_message": "控制器已重启，执行状态待核对；系统不会自动重派"}, synchronize_session=False)
            db.commit()
