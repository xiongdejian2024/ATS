"""Persist bounded Agent batches and cursor atomically, then emit an ACK.

Raw suite logs retain the existing history/export API. SQL append avoids loading
an execution's ever-growing history into Python on every new chunk.
"""

import json
import os
import uuid
from datetime import datetime

from sqlalchemy import func, update
from sqlalchemy.orm import load_only
from models.agent_log import AgentLogCursor, AgentTaskLog
from models.task_queue import TaskQueue
from models.test_suite import TestSuiteLog
from models.script_job import ScriptJobLog
from utils.datetime_utils import beijing_now

MAX_BATCH_RECORDS = 64
MAX_BATCH_BYTES = 64 * 1024
MAX_RECORD_BYTES = 16 * 1024
# Explicit raw-storage ceiling, independently configurable by operator. No
# truncation: over-quota batches are rejected and remain on the Agent spool.
MAX_EXECUTION_LOG_BYTES = int(
    os.environ.get("ATS_MAX_EXECUTION_LOG_BYTES", 256 * 1024 * 1024)
)


def _identifier(value, max_length=36):
    return isinstance(value, str) and 0 < len(value) <= max_length


def _timestamp(value):
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            pass
    return beijing_now()


def _byte_length(db, column):
    # SQLite length(TEXT) counts codepoints, not stored UTF-8 bytes.
    from sqlalchemy import LargeBinary, cast

    return (
        func.length(cast(column, LargeBinary))
        if db.bind.dialect.name == "sqlite"
        else func.octet_length(column)
    )


def _char_length(db, column):
    return (
        func.length(column)
        if db.bind.dialect.name == "sqlite"
        else func.char_length(column)
    )


def validate_batch(message):
    try:
        stream_id = message.get("stream_id", "")
        if not isinstance(stream_id, str) or str(uuid.UUID(stream_id)) != stream_id:
            raise ValueError("invalid_stream")
    except (ValueError, TypeError, AttributeError):
        raise ValueError("invalid_stream")
    records = message.get("records")
    if not isinstance(records, list) or not 1 <= len(records) <= MAX_BATCH_RECORDS:
        raise ValueError("invalid_batch_size")
    total, previous = 0, None
    for record in records:
        if (
            not isinstance(record, dict)
            or type(record.get("sequence")) is not int
            or not 1 <= record["sequence"] < 2**63
        ):
            raise ValueError("invalid_sequence")
        if previous is not None and record["sequence"] != previous + 1:
            raise ValueError("noncontiguous_batch")
        previous = record["sequence"]
        payload = record.get("payload")
        if (
            not isinstance(payload, dict)
            or payload.get("type") not in {"test_suite_log", "task_log", "script_job_log"}
            or not isinstance(payload.get("message"), str)
        ):
            raise ValueError("invalid_payload")
        if "\x00" in payload["message"]:
            # SQLite text length/substr stop at NUL; never pretend its browser
            # offsets preserve binary output. Keep rejected evidence on Agent.
            raise ValueError("unsupported_nul")
        if (
            type(payload.get("continuation", False)) is not bool
            or type(payload.get("raw", False)) is not bool
        ):
            raise ValueError("invalid_continuation")
        if payload["type"] == "test_suite_log":
            if not _identifier(payload.get("suite_id")) or not _identifier(
                payload.get("execution_id")
            ):
                raise ValueError("invalid_execution")
        elif payload["type"] == "script_job_log":
            if not _identifier(payload.get("script_job_id")) or not _identifier(payload.get("execution_id")):
                raise ValueError("invalid_execution")
        elif not _identifier(payload.get("task_id"), 255):
            raise ValueError("invalid_task")
        size = len(
            json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode(
                "utf-8"
            )
        )
        total += size
        if size > MAX_RECORD_BYTES or total > MAX_BATCH_BYTES:
            raise ValueError("batch_quota")
    return records


def _append(db, environment_id, payload):
    """Return bounded live delta after SQL append, without fetching raw history."""
    is_suite = payload["type"] == "test_suite_log"
    is_script = payload["type"] == "script_job_log"
    model = ScriptJobLog if is_script else TestSuiteLog if is_suite else AgentTaskLog
    if is_script:
        task = db.query(TaskQueue).filter_by(kind="script", script_job_id=payload["script_job_id"],
            execution_id=payload["execution_id"], environment_id=environment_id).first()
        if not task:
            raise ValueError("execution_not_owned")
        from models.script_job import ScriptJobRun
        run = db.get(ScriptJobRun, payload["execution_id"])
        if not run or run.job_id != payload["script_job_id"] or run.environment_id != environment_id:
            raise ValueError("execution_not_owned")
        log_id = str(uuid.uuid5(uuid.NAMESPACE_URL, "ats-script-log:" + payload["execution_id"]))
        row = db.query(model).options(load_only(model.id, model.timestamp)).filter_by(id=log_id).first()
        if not row:
            row = model(id=log_id, script_job_id=payload["script_job_id"], execution_id=payload["execution_id"], message="", timestamp=beijing_now())
            db.add(row); db.flush()
    elif is_suite:
        task = (
            db.query(TaskQueue.id)
            .filter_by(
                execution_id=payload["execution_id"], kind="suite",
                suite_id=payload["suite_id"],
                environment_id=environment_id,
            )
            .first()
        )
        if not task:
            raise ValueError("execution_not_owned")
        row = (
            db.query(model)
            .options(load_only(model.id, model.timestamp))
            .filter_by(
                suite_id=payload["suite_id"],
                execution_id=payload["execution_id"],
            )
            .first()
        )
        if not row:
            log_id = str(
                uuid.uuid5(
                    uuid.NAMESPACE_URL,
                    f"ats-log:{environment_id}:{payload['suite_id']}:{payload['execution_id']}",
                )
            )
            sequence = (
                db.query(func.max(model.sequence_number))
                .filter_by(suite_id=payload["suite_id"])
                .scalar()
                or 0
            ) + 1
            row = model(
                id=log_id,
                suite_id=payload["suite_id"],
                execution_id=payload["execution_id"],
                sequence_number=sequence,
                message="",
            )
            db.add(row)
            db.flush()
    else:
        log_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                f"ats-task-log:{environment_id}:{payload['task_id']}",
            )
        )
        row = (
            db.query(model)
            .options(load_only(model.id, model.timestamp))
            .filter_by(id=log_id)
            .first()
        )
        if not row:
            row = model(
                id=log_id,
                environment_id=environment_id,
                task_id=payload["task_id"],
                message="",
            )
            db.add(row)
            db.flush()
    size, length = (
        db.query(_byte_length(db, model.message), _char_length(db, model.message))
        .filter_by(id=row.id)
        .one()
    )
    text = payload["message"]
    suffix = (
        "\n"
        if length and not payload.get("continuation") and not payload.get("raw")
        else ""
    ) + text
    if size + len(suffix.encode("utf-8")) > MAX_EXECUTION_LOG_BYTES:
        raise ValueError("execution_log_quota")
    timestamp = _timestamp(payload.get("timestamp"))
    db.execute(
        update(model)
        .where(model.id == row.id)
        .values(message=model.message + suffix, timestamp=timestamp),
        execution_options={"synchronize_session": False},
    )
    if is_script:
        return ("script:" + payload["execution_id"], dict(id=row.id, message=suffix[-32768:],
            timestamp=timestamp.isoformat(), execution_id=payload["execution_id"],
            script_job_id=payload["script_job_id"], endOffset=length + len(suffix), truncated=len(suffix) > 32768))
    if is_suite:
        return (
            payload["suite_id"],
            dict(
                id=row.id,
                message=suffix[-32768:],
                timestamp=timestamp.isoformat(),
                execution_id=payload["execution_id"],
                endOffset=length + len(suffix),
                truncated=len(suffix) > 32768,
            ),
        )
    return None


def _notify_blocked(db, environment_id, message, reason):
    """Persist one visible inbox diagnostic per stream/reason and recipient.

    This separate transaction never ACKs or changes raw logs/cursors. Include
    identifiers and the bounded reason only, never untrusted raw log contents.
    """
    from services.inbox import notify
    from models.environment import Environment

    stream = str(message.get("stream_id", ""))[:36]
    recipients = {}
    records = message.get("records")
    for record in records[:MAX_BATCH_RECORDS] if isinstance(records, list) else []:
        entry = record.get("payload") if isinstance(record, dict) else None
        if not isinstance(entry, dict):
            continue
        task = (
            db.query(TaskQueue)
            .filter_by(
                execution_id=entry.get("execution_id"),
                suite_id=entry.get("suite_id"),
                environment_id=environment_id,
            )
            .first()
            if entry.get("type") == "test_suite_log"
            and _identifier(entry.get("suite_id"))
            and _identifier(entry.get("execution_id"))
            else None
        )
        if entry.get("type") == "script_job_log" and _identifier(entry.get("script_job_id")) and _identifier(entry.get("execution_id")):
            task = db.query(TaskQueue).filter_by(kind="script", script_job_id=entry["script_job_id"],
                execution_id=entry["execution_id"], environment_id=environment_id).first()
        if task:
            recipients[task.executor_id] = (task.suite_id or task.script_job_id, task.execution_id)
    if not recipients:
        environment = db.get(Environment, environment_id)
        if environment and environment.created_by:
            recipients[environment.created_by] = (environment_id, None)
    for user_id, (related_id, execution_id) in recipients.items():
        notify(
            db,
            user_id,
            f"log-blocked:{environment_id}:{stream}:{reason}",
            "log_delivery_blocked",
            "执行日志传输受阻",
            f"节点 {environment_id}，执行 {execution_id or 'direct-task'}：{reason}。"
            "未确认日志保留在 Agent，后续日志已反压。请核对日志配额或不支持的输出，处理后重启 Agent；不要删除未确认队列。",
            related_id,
        )
    db.commit()


def persist_log_batch(db, environment_id, message):
    """Returns (response, post-commit live deltas). No ACK on validation/DB error."""
    stream_id = message.get("stream_id")
    expected = 1
    try:
        records = validate_batch(message)
        cursor_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL, f"ats-log-cursor:{environment_id}:{stream_id}"
            )
        )
        cursor = (
            db.query(AgentLogCursor).filter_by(id=cursor_id).with_for_update().first()
        )
        if not cursor:
            cursor = AgentLogCursor(
                id=cursor_id,
                environment_id=environment_id,
                stream_id=stream_id,
                through_sequence=0,
            )
            db.add(cursor)
            db.flush()
        expected = cursor.through_sequence + 1
        if records[0]["sequence"] > expected:
            raise ValueError("gap")
        deltas = []
        for record in records:
            if record["sequence"] <= cursor.through_sequence:
                continue
            delta = _append(db, environment_id, record["payload"])
            if delta:
                deltas.append(delta)
            cursor.through_sequence = record["sequence"]
        through_sequence = cursor.through_sequence
        db.commit()  # Both raw evidence and cursor durable before ACK is formed.
        return (
            dict(
                type="log_batch_ack",
                stream_id=stream_id,
                through_sequence=through_sequence,
            ),
            deltas,
        )
    except ValueError as exc:
        db.rollback()
        _notify_blocked(db, environment_id, message, str(exc))
        return (
            dict(
                type="log_batch_nack",
                stream_id=stream_id,
                expected_sequence=expected,
                reason=str(exc),
            ),
            [],
        )
    except Exception:
        db.rollback()
        raise
