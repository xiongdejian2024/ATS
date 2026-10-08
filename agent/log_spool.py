"""Bounded, crash-durable log outbox. Only committed controller ACKs reclaim it.

A full spool backpressures the producer; it never evicts unacknowledged records.
SQLite DELETE journals + FULL sync bound the DB and transient journal separately.
"""

import asyncio
import json
import os
import sqlite3
import time
import uuid
from pathlib import Path

MAX_RECORD_BYTES = 16 * 1024
MAX_BATCH_BYTES = 64 * 1024
MAX_BATCH_RECORDS = 64


class SpoolFull(Exception):
    pass


class LogSpool:
    def __init__(self, path, max_bytes=64 * 1024 * 1024, max_records=8192):
        if max_bytes < MAX_RECORD_BYTES or max_records < 1:
            raise ValueError("log spool quota must fit at least one 16 KiB record")
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.max_bytes, self.max_records = max_bytes, max_records
        descriptor = os.open(self.path, os.O_CREAT | os.O_WRONLY, 0o600)
        os.close(descriptor)
        self.db = sqlite3.connect(self.path, timeout=1)
        self.db.execute("PRAGMA journal_mode=DELETE")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.execute("PRAGMA auto_vacuum=FULL")
        # Logical quota counts UTF-8 serialized bytes; physical cap also covers
        # B-tree/index/metadata overhead. Rollback journal is at most DB-sized.
        self.page_limit = (2 * max_bytes + 2 * 1024 * 1024 + 4095) // 4096
        self.page_limit = self.db.execute(
            f"PRAGMA max_page_count={self.page_limit}"
        ).fetchone()[0]
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS state (
                id INTEGER PRIMARY KEY CHECK(id=1), stream_id TEXT NOT NULL,
                next_sequence INTEGER NOT NULL, acknowledged INTEGER NOT NULL,
                pending_bytes INTEGER NOT NULL, pending_records INTEGER NOT NULL,
                legacy_advanced INTEGER NOT NULL DEFAULT 0);
            CREATE TABLE IF NOT EXISTS records (
                sequence INTEGER PRIMARY KEY, payload TEXT NOT NULL, size INTEGER NOT NULL);
        """)
        with self.db:
            self.db.execute(
                "INSERT OR IGNORE INTO state VALUES (1, ?, 1, 0, 0, 0, 0)",
                (str(uuid.uuid4()),),
            )
        self.stream_id = self.db.execute("SELECT stream_id FROM state").fetchone()[0]

    def usage(self):
        size, count = self.db.execute(
            "SELECT pending_bytes, pending_records FROM state"
        ).fetchone()
        return {
            "bytes": size,
            "records": count,
            "max_bytes": self.max_bytes,
            "max_records": self.max_records,
        }

    def append(self, payload):
        text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        size = len(text.encode("utf-8"))
        if size > MAX_RECORD_BYTES:
            raise ValueError("log record exceeds wire limit")
        try:
            with self.db:
                sequence, used, count = self.db.execute(
                    "SELECT next_sequence, pending_bytes, pending_records FROM state"
                ).fetchone()
                if used + size > self.max_bytes or count >= self.max_records:
                    raise SpoolFull(
                        "durable log spool quota reached; execution output is backpressured"
                    )
                self.db.execute(
                    "INSERT INTO records VALUES (?, ?, ?)", (sequence, text, size)
                )
                self.db.execute(
                    "UPDATE state SET next_sequence=?, pending_bytes=pending_bytes+?, pending_records=pending_records+1",
                    (sequence + 1, size),
                )
            return sequence
        except sqlite3.OperationalError as exc:
            # Includes SQLITE_FULL / disk full. Existing records remain intact.
            raise SpoolFull(f"cannot persist log evidence: {exc}") from exc

    def batch(self):
        records, total = [], 0
        for sequence, payload, size in self.db.execute(
            "SELECT sequence, payload, size FROM records ORDER BY sequence LIMIT ?",
            (MAX_BATCH_RECORDS,),
        ):
            if total + size > MAX_BATCH_BYTES:
                break
            records.append({"sequence": sequence, "payload": json.loads(payload)})
            total += size
        return {"type": "log_batch", "stream_id": self.stream_id, "records": records}

    def acknowledge(self, sequence, *, legacy=False):
        if type(sequence) is not int:
            return False
        with self.db:
            next_sequence, acknowledged = self.db.execute(
                "SELECT next_sequence, acknowledged FROM state"
            ).fetchone()
            if sequence <= acknowledged or sequence >= next_sequence:
                return False
            size, count = self.db.execute(
                "SELECT coalesce(sum(size), 0), count(*) FROM records WHERE sequence<=?",
                (sequence,),
            ).fetchone()
            self.db.execute("DELETE FROM records WHERE sequence<=?", (sequence,))
            self.db.execute(
                "UPDATE state SET acknowledged=?, pending_bytes=pending_bytes-?, pending_records=pending_records-?, legacy_advanced=max(legacy_advanced, ?)",
                (sequence, size, count, int(legacy)),
            )
        return True

    def prepare_durable_stream(self):
        """Legacy socket sends have no controller cursor. Give the remaining
        evidence a fresh stream identity on upgrade, atomically and explicitly.
        """
        acknowledged, legacy = self.db.execute(
            "SELECT acknowledged, legacy_advanced FROM state"
        ).fetchone()
        if not legacy:
            return False
        stream_id = str(uuid.uuid4())
        with self.db:
            self.db.execute("UPDATE records SET sequence=-sequence")
            self.db.execute("UPDATE records SET sequence=-sequence-?", (acknowledged,))
            self.db.execute(
                "UPDATE state SET stream_id=?, next_sequence=next_sequence-?, acknowledged=0, legacy_advanced=0",
                (stream_id, acknowledged),
            )
        self.stream_id = stream_id
        return True

    def close(self):
        self.db.close()


class LogDelivery:
    """One bounded in-flight batch; retries survive lost sends, ACKs and restart."""

    def __init__(self, spool, client, logger, retry_seconds=1):
        self.spool, self.client, self.logger = spool, client, logger
        self.retry_seconds = retry_seconds
        self.capable = None
        self.blocked_reason = None
        self.backpressured = False
        self.changed = asyncio.Event()
        self.ack_changed = asyncio.Event()
        self.worker = None
        self.closed = False
        self.sent_through = 0
        self._last_warning = 0
        self._append_lock = asyncio.Lock()

    def wake(self):
        self.changed.set()
        if not self.closed and (self.worker is None or self.worker.done()):
            self.worker = asyncio.create_task(self._run())

    def negotiate(self, message):
        self.capable = "log_batch_v1" in message.get("capabilities", [])
        if not self.capable and self.logger:
            self.logger.warning(
                "Controller has no durable log ACK capability; legacy delivery is best-effort after socket send"
            )
        self.wake()

    async def enqueue(self, payload):
        # Bound even a no-newline message; preserve every character in order.
        # JSON control escapes use up to 6 bytes/codepoint; leave metadata room.
        metadata = {
            key: payload[key]
            for key in (
                "type",
                "suite_id",
                "execution_id",
                "task_id",
                "level",
                "timestamp",
                "raw",
            )
            if key in payload
        }
        if len(json.dumps(metadata).encode()) > 2048:
            raise ValueError("log metadata exceeds 2 KiB")
        text = payload.get("message", "")
        if not isinstance(text, str):
            raise ValueError("log message must be text")
        async with self._append_lock:
            for offset in range(0, max(1, len(text)), 2000):
                record = dict(metadata, message=text[offset : offset + 2000])
                # Continuation is part of the original message, not a new line.
                record["continuation"] = offset > 0
                while True:
                    if self.closed:
                        raise RuntimeError(
                            "log delivery closed before evidence was persisted"
                        )
                    try:
                        self.spool.append(record)
                        self.backpressured = False
                        self.wake()
                        # Keep receiver/heartbeat/cancel runnable during a large
                        # multi-chunk payload even when disk quota has room.
                        await asyncio.sleep(0)
                        break
                    except SpoolFull as exc:
                        self.backpressured = True
                        if self.logger and time.monotonic() - self._last_warning > 10:
                            self.logger.error(
                                "{}; awaiting durable ACK, cancellation remains available",
                                exc,
                            )
                            self._last_warning = time.monotonic()
                        self.changed.clear()
                        await self._wait()
        return True

    def acknowledge(self, message):
        if message.get("stream_id") != self.spool.stream_id:
            return
        if message.get("type") == "log_batch_nack":
            expected = message.get("expected_sequence")
            batch = self.spool.batch()["records"]
            if (
                message.get("reason") != "gap"
                or not batch
                or expected != batch[0]["sequence"]
            ):
                reason = message.get("reason", "rejected")
                changed = reason != self.blocked_reason
                self.blocked_reason = reason
                if self.logger and changed:
                    self.logger.error(
                        "Controller rejected durable logs: {} expected_sequence={}; spool retained, operator reconciliation required",
                        self.blocked_reason,
                        expected,
                    )
            self.wake()
            return
        sequence = message.get("through_sequence")
        if (
            type(sequence) is int
            and sequence <= self.sent_through
            and self.spool.acknowledge(sequence)
        ):
            self.ack_changed.set()
            self.wake()

    async def _wait(self):
        try:
            await asyncio.wait_for(self.changed.wait(), timeout=self.retry_seconds)
        except asyncio.TimeoutError:
            pass

    async def _run(self):
        while not self.closed:
            self.changed.clear()
            if self.capable is None or not self.client.connected or self.blocked_reason:
                await self._wait()
                continue
            if self.capable and self.spool.prepare_durable_stream():
                self.sent_through = 0
                if self.logger:
                    self.logger.warning(
                        "Starting durable stream after legacy delivery; prior socket-sent logs have no persistence guarantee"
                    )
            batch = self.spool.batch()
            if not batch["records"]:
                await self._wait()
                continue
            try:
                if self.capable:
                    self.sent_through = max(
                        self.sent_through, batch["records"][-1]["sequence"]
                    )
                    self.ack_changed.clear()
                    await self.client.send_message(batch)
                    try:
                        await asyncio.wait_for(
                            self.ack_changed.wait(), timeout=self.retry_seconds
                        )
                    except asyncio.TimeoutError:
                        pass
                else:
                    for record in batch["records"]:
                        # Bypass only the local log interception; transport still
                        # supplies its session fence and socket send behavior.
                        if not await self.client.send_log_legacy(record["payload"]):
                            break
                        self.spool.acknowledge(record["sequence"], legacy=True)
                        self.changed.set()
            except Exception:
                if self.logger:
                    self.logger.exception(
                        "Log delivery failed; durable records retained for replay"
                    )
                await asyncio.sleep(self.retry_seconds)
            if not self.capable:
                await self._wait()

    def diagnostics(self):
        return dict(
            self.spool.usage(),
            blocked_reason=self.blocked_reason,
            backpressured=self.backpressured,
        )

    async def close(self):
        self.closed = True
        self.changed.set()
        if self.worker:
            self.worker.cancel()
            await asyncio.gather(self.worker, return_exceptions=True)
        self.spool.close()
