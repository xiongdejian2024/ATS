"""Slow log subscribers cannot hold up Agent handling or other subscribers."""

import asyncio
import json

import pytest
import pytest_asyncio

from services.frontend_log_stream import FrontendConnectionManager
from test_http_agent_e2e import until
from test_plan_orchestration import plan_lab


class Socket:
    def __init__(self, *, blocked=False, broken=False, blocked_close=False):
        self.entered = asyncio.Event()
        self.release = asyncio.Event()
        self.closed = asyncio.Event()
        self.cancelled = asyncio.Event()
        self.blocked = blocked
        self.broken = broken
        self.blocked_close = blocked_close
        self.frames = []
        self.closes = []
        self.sending = False

    async def send_text(self, payload):
        assert not self.sending, "Concurrent socket writes are not allowed"
        self.sending = True
        self.entered.set()
        try:
            if self.blocked:
                await self.release.wait()
            if self.broken:
                raise OSError("transport failed")
            self.frames.append(json.loads(payload))
        except asyncio.CancelledError:
            self.cancelled.set()
            raise
        finally:
            self.sending = False

    async def close(self, code, reason):
        assert not self.sending, "Close must wait for the sender's cancellation"
        self.closes.append((code, reason))
        self.closed.set()
        if self.blocked_close:
            await asyncio.Event().wait()


@pytest_asyncio.fixture
async def stream():
    manager = FrontendConnectionManager(send_timeout=1, close_timeout=0.05)
    yield manager
    await manager.aclose()
    assert not manager.frontend_connections
    assert not manager._subscribers
    assert not manager._tasks
    assert not manager._retiring


@pytest.mark.asyncio
async def test_blocked_subscriber_does_not_delay_healthy_subscriber(stream):
    slow, healthy = Socket(blocked=True), Socket()
    await stream.connect(slow, "suite")
    await stream.connect(healthy, "suite")
    for index in range(5):
        await asyncio.wait_for(stream.broadcast_log("suite", {"message": str(index)}), 0.1)
        await until(lambda: len(healthy.frames) == index + 1, timeout=0.3)
    assert slow.entered.is_set() and not slow.frames and not slow.release.is_set()
    assert [frame["data"]["message"] for frame in healthy.frames] == list(map(str, range(5)))


@pytest.mark.asyncio
async def test_message_budget_includes_inflight_and_isolates_overload():
    stream = FrontendConnectionManager(max_pending_messages=3, close_timeout=0.05)
    slow, healthy, other_suite = Socket(blocked=True), Socket(), Socket()
    try:
        await stream.connect(slow, "suite")
        await stream.connect(healthy, "suite")
        await stream.connect(other_suite, "other")
        state = stream._subscribers[slow]
        for index in range(3):
            await stream.broadcast_log("suite", {"message": str(index)})
            await until(lambda: len(healthy.frames) == index + 1)
        assert state.pending_messages == 3 and state.queue.qsize() == 2
        await stream.broadcast_log("suite", {"message": "overload"})
        assert not stream.is_connected(slow, "suite")
        assert state.queue.empty()
        await asyncio.wait_for(slow.closed.wait(), 0.3)
        assert slow.closes[0][0] == 1013 and "reload history" in slow.closes[0][1]
        assert slow.cancelled.is_set() and not slow.frames
        assert state.pending_messages == state.pending_bytes == 0
        await asyncio.wait_for(state.queue.join(), 0.1)
        await until(lambda: len(healthy.frames) == 4)
        assert stream.is_connected(other_suite, "other") and not other_suite.frames
    finally:
        await stream.aclose()


@pytest.mark.asyncio
async def test_byte_budget_counts_serialized_utf8_and_inflight():
    message = {"type": "test_suite_log", "suite_id": "suite", "data": {"message": "中😀"}}
    size = len(json.dumps(message, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
    stream = FrontendConnectionManager(max_pending_bytes=size * 2, close_timeout=0.05)
    slow = Socket(blocked=True)
    try:
        await stream.connect(slow, "suite")
        state = stream._subscribers[slow]
        await stream.broadcast_log("suite", message["data"])
        await slow.entered.wait()
        await stream.broadcast_log("suite", message["data"])
        assert state.pending_bytes == size * 2 and state.pending_messages == 2
        await stream.broadcast_log("suite", message["data"])
        await slow.closed.wait()
        assert slow.closes[0][0] == 1013
        assert state.pending_bytes == state.pending_messages == 0
    finally:
        await stream.aclose()


@pytest.mark.asyncio
async def test_oversized_frame_closes_even_before_sender_started():
    stream = FrontendConnectionManager(max_pending_bytes=1, close_timeout=0.05)
    socket = Socket()
    await stream.connect(socket, "suite")
    await stream.broadcast_log("suite", {"message": "oversized"})
    assert not stream.frontend_connections
    await asyncio.wait_for(stream.aclose(), 0.3)
    assert not socket.frames and socket.closes[0][0] == 1013
    assert not stream._tasks and not stream._retiring


@pytest.mark.asyncio
async def test_fifo_snapshot_control_frames_and_suite_isolation(stream):
    socket, other = Socket(), Socket()
    await stream.connect(socket, "suite")
    await stream.connect(other, "other")
    assert stream.enqueue_message(socket, "suite", {"type": "connected"})
    data = {"message": "original", "endOffset": 8}
    await stream.broadcast_log("suite", data)
    data["message"] = "mutated after enqueue"
    assert stream.enqueue_message(socket, "suite", {"type": "pong"})
    await stream.broadcast_log("suite", {"message": "next", "endOffset": 13})
    await until(lambda: len(socket.frames) == 4)
    assert [frame["type"] for frame in socket.frames] == [
        "connected",
        "test_suite_log",
        "pong",
        "test_suite_log",
    ]
    assert socket.frames[1]["data"] == {"message": "original", "endOffset": 8}
    assert not other.frames
    assert not stream.enqueue_message(socket, "other", {"type": "ping"})


@pytest.mark.asyncio
@pytest.mark.parametrize("broken, expected_code", [(False, 1013), (True, 1011)])
async def test_timeout_and_send_failure_retire_only_failed_socket(broken, expected_code):
    stream = FrontendConnectionManager(send_timeout=0.02, close_timeout=0.02)
    socket, healthy = Socket(blocked=not broken, broken=broken), Socket()
    try:
        await stream.connect(socket, "suite")
        await stream.connect(healthy, "suite")
        await stream.broadcast_log("suite", {"message": "before"})
        await asyncio.wait_for(socket.closed.wait(), 0.3)
        assert socket.closes[0][0] == expected_code
        assert not stream.is_connected(socket, "suite")
        await stream.broadcast_log("suite", {"message": "after"})
        await until(lambda: len(healthy.frames) == 2)
    finally:
        await stream.aclose()


@pytest.mark.asyncio
async def test_disconnect_is_idempotent_and_reconnect_uses_fresh_fifo(stream):
    old, fresh = Socket(blocked=True), Socket()
    await stream.connect(old, "suite")
    await stream.connect(old, "suite")
    assert len(stream.frontend_connections["suite"]) == 1
    with pytest.raises(ValueError, match="another suite"):
        await stream.connect(old, "other")
    await stream.broadcast_log("suite", {"message": "old"})
    await old.entered.wait()
    await stream.broadcast_log("suite", {"message": "queued old"})
    state = stream._subscribers[old]
    cleanup = stream.disconnect(old, "suite")
    assert stream.disconnect(old, "suite") is cleanup
    assert not stream.enqueue_message(old, "suite", {"type": "ping"})
    await stream.connect(fresh, "suite")
    await stream.broadcast_log("suite", {"message": "fresh"})
    await cleanup
    await until(lambda: len(fresh.frames) == 1)
    assert not old.frames and not old.closes
    assert state.pending_messages == state.pending_bytes == 0
    await asyncio.wait_for(state.queue.join(), 0.1)
    assert fresh.frames[0]["data"]["message"] == "fresh"


@pytest.mark.asyncio
async def test_shutdown_reaps_blocked_senders_and_bounds_close():
    stream = FrontendConnectionManager(send_timeout=10, close_timeout=0.02)
    socket = Socket(blocked=True, blocked_close=True)
    await stream.connect(socket, "suite")
    await stream.broadcast_log("suite", {"message": "blocked"})
    await socket.entered.wait()
    await asyncio.wait_for(stream.aclose(), 0.3)
    assert socket.cancelled.is_set() and socket.closes[0][0] == 1001
    assert not stream._tasks and not stream._retiring and not stream._subscribers
    assert not stream.frontend_connections
    await stream.aclose()


@pytest.mark.parametrize(
    "options",
    [
        {"max_pending_messages": 0},
        {"max_pending_bytes": -1},
        {"send_timeout": 0},
        {"close_timeout": -1},
    ],
)
def test_invalid_bounds_are_rejected(options):
    with pytest.raises(ValueError):
        FrontendConnectionManager(**options)


@pytest.mark.asyncio
async def test_overload_keeps_full_persistent_logs(plan_lab, monkeypatch):
    import api.v1.websocket as routes
    from models.test_suite import TestSuiteLog

    db, _ = plan_lab
    stream = FrontendConnectionManager(max_pending_messages=1, close_timeout=0.05)
    monkeypatch.setattr(routes, "frontend_manager", stream)
    slow, healthy = Socket(blocked=True), Socket()
    parts = ["first😀", "完整中间" * 10000, "最后日志😀"]
    try:
        await stream.connect(slow, "suite-0")
        await stream.connect(healthy, "suite-0")
        for index, text in enumerate(parts):
            await asyncio.wait_for(
                routes.handle_test_suite_log(
                    db,
                    "node",
                    {
                        "suite_id": "suite-0",
                        "execution_id": "persisted",
                        "message": text,
                    },
                ),
                0.3,
            )
            await until(lambda: len(healthy.frames) == index + 1)
        await asyncio.wait_for(slow.closed.wait(), 0.3)
        assert slow.closes[0][0] == 1013 and not slow.frames
        saved = db.query(TestSuiteLog).filter_by(execution_id="persisted").one()
        assert saved.message == "\n".join(parts)
        assert healthy.frames[1]["data"]["truncated"]
        assert healthy.frames[-1]["data"]["endOffset"] == len(saved.message)
    finally:
        await stream.aclose()


@pytest.mark.asyncio
async def test_burst_producer_gives_healthy_senders_fair_scheduling():
    stream = FrontendConnectionManager(max_pending_messages=3, close_timeout=0.05)
    slow, healthy = Socket(blocked=True), Socket()
    try:
        await stream.connect(slow, "suite")
        await stream.connect(healthy, "suite")
        # No test-provided sleep/wait between enqueues: broadcast itself must
        # let an immediately writable socket drain rather than reject a burst.
        for index in range(100):
            await stream.broadcast_log("suite", {"message": str(index)})
        assert stream.is_connected(healthy, "suite")
        assert [frame["data"]["message"] for frame in healthy.frames] == list(map(str, range(100)))
        assert not stream.is_connected(slow, "suite")
        await asyncio.wait_for(slow.closed.wait(), 0.3)
        assert slow.closes[0][0] == 1013
    finally:
        await stream.aclose()
