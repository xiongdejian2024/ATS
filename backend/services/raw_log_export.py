"""Bounded, authenticated raw-log exports with frozen record IDs and end offsets.

Cursors are integrity-protected state, never an authentication credential. Every
request must still authorize the suite/run and constrain reads to that selection.
No log body, export file, credential or retention policy is stored by this API.
"""
import base64
import hashlib
import hmac
import json
import time
from datetime import datetime, timezone

from fastapi import HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func

from config import settings
from models.test_suite import TestSuiteLog

MAX_SNAPSHOT_RECORDS = 1000
MAX_CHUNK_CHARS = 65536  # At most 256 KiB of UTF-8, independent of newline count.
MAX_CHUNK_RECORDS = 32
MAX_CURSOR_CHARS = 512 * 1024
CURSOR_LIFETIME_SECONDS = 3600
LEGACY_MAX_CHARS = 512 * 1024


class LogExportRequest(BaseModel):
    cursor: str | None = Field(None, max_length=MAX_CURSOR_CHARS)
    execution_id: str | None = Field(None, alias="executionId", max_length=36)
    log_id: str | None = Field(None, alias="logId", max_length=36)


def character_length(query):
    return (func.length(TestSuiteLog.message) if query.session.bind.dialect.name == "sqlite"
            else func.char_length(TestSuiteLog.message))


def run_log_query(db, run_id):
    from models.plan_orchestration import PlanRunItem
    membership = db.query(PlanRunItem.id).filter(
        PlanRunItem.run_id == run_id,
        PlanRunItem.suite_id == TestSuiteLog.suite_id,
        PlanRunItem.execution_id == TestSuiteLog.execution_id,
    ).exists()
    return db.query(TestSuiteLog).filter(membership)


def _nul_position(query):
    # SQLite text LENGTH/SUBSTR stop at NUL. MySQL supports the full string.
    return (func.instr(TestSuiteLog.message, "\x00") if query.session.bind.dialect.name == "sqlite"
            else func.coalesce(None, 0))


def _check_nul(position):
    if position:
        raise HTTPException(409, {"code": "LOG_UNSUPPORTED_NUL",
            "message": "SQLite 中的旧日志含 NUL 字符，无法安全分段；请通过数据库原始备份提取。日志未截断或删除。"})


def check_legacy_log_budget(query, skip=0, limit=MAX_SNAPSHOT_RECORDS + 1):
    """Capture bounded metadata before bodies; an aggregate alone has a read race."""
    columns = [c for c in TestSuiteLog.__table__.columns if c.name != 'message']
    rows = query.with_entities(*columns, character_length(query).label('_chars'),
        _nul_position(query).label('_nul')).offset(skip).limit(min(limit, MAX_SNAPSHOT_RECORDS + 1)).all()
    for row in rows:
        _check_nul(row._mapping['_nul'])
    if len(rows) > MAX_SNAPSHOT_RECORDS or sum(row._mapping['_chars'] for row in rows) > LEGACY_MAX_CHARS:
        raise HTTPException(413, {
            "code": "LOG_EXPORT_REQUIRED",
            "message": "日志超出完整 JSON 上限，请使用同一路径 /export 分段下载，或使用 tailChars 查看有界尾部。原始日志未截断。",
            "maxRecords": MAX_SNAPSHOT_RECORDS, "maxChars": LEGACY_MAX_CHARS,
        })
    return rows


def legacy_log_rows(query, skip=0, limit=MAX_SNAPSHOT_RECORDS + 1):
    rows = check_legacy_log_budget(query, skip, limit)
    result = []
    for metadata in rows:
        item = dict(metadata._mapping)
        end = item.pop('_chars'); item.pop('_nul')
        row = query.filter(TestSuiteLog.id == item['id']).with_entities(character_length(query),
            func.substr(TestSuiteLog.message, 1, end), _nul_position(query)).first()
        if row is None or row[0] != end or len(row[1]) != end:
            raise HTTPException(409, "日志在读取期间发生变化，请重试或使用 /export 冻结快照下载。")
        _check_nul(row[2])
        item['message'] = row[1]
        result.append(item)
    return result


def _sign(payload):
    encoded = base64.urlsafe_b64encode(json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode()).decode()
    signature = hmac.new(settings.JWT_SECRET_KEY.encode(), b"ats-raw-log-v1:" + encoded.encode(), hashlib.sha256).hexdigest()
    cursor = encoded + "." + signature
    if len(cursor) > MAX_CURSOR_CHARS:
        raise HTTPException(413, "日志索引过大，请按单次测试套执行下载；原始日志未截断。")
    return cursor


def _read(cursor, scope, user_id):
    try:
        encoded, signature = cursor.rsplit(".", 1)
        expected = hmac.new(settings.JWT_SECRET_KEY.encode(), b"ats-raw-log-v1:" + encoded.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            raise ValueError("signature")
        payload = json.loads(base64.urlsafe_b64decode(encoded))
        if payload["scope"] != scope or payload["user"] != str(user_id) or payload["v"] != 1:
            raise ValueError("selection")
        if payload["expires"] < time.time():
            raise HTTPException(410, "日志下载快照已过期，请重新开始下载。")
        return payload
    except (ValueError, KeyError, TypeError, UnicodeError) as exc:
        raise HTTPException(400, "日志下载游标无效或不属于当前用户/选择。") from exc


def export_log_chunk(query, scope, user_id, request):
    """At most 1001 metadata rows at start and 32 SUBSTR reads per response.

    A fixed manifest avoids time-based pagination skipping tied timestamps or
    mixing in a later execution. Appends after capture are intentionally excluded.
    The log writer is append-only; deleted/shortened rows fail instead of creating
    a seemingly complete file with a gap. Metadata over the explicit limit asks
    the caller to split by execution, never silently drops evidence.
    """
    if request.cursor:
        state = _read(request.cursor, scope, user_id)
        if ((request.execution_id and request.execution_id != state["execution"])
                or (request.log_id and request.log_id != state["log"])):
            raise HTTPException(400, "下载过程中不能改变执行选择，请重新开始。")
    else:
        selected = query
        if request.execution_id:
            selected = selected.filter(TestSuiteLog.execution_id == request.execution_id)
        if request.log_id:
            selected = selected.filter(TestSuiteLog.id == request.log_id)
        rows = selected.with_entities(TestSuiteLog.id, TestSuiteLog.suite_id,
            TestSuiteLog.execution_id, TestSuiteLog.timestamp, character_length(selected), _nul_position(selected)).order_by(
                TestSuiteLog.timestamp, TestSuiteLog.id).limit(MAX_SNAPSHOT_RECORDS + 1).all()
        if len(rows) > MAX_SNAPSHOT_RECORDS:
            raise HTTPException(413, {
                "code": "LOG_SELECTION_TOO_LARGE", "maxRecords": MAX_SNAPSHOT_RECORDS,
                "message": "选择超过 1000 条日志，请按单次测试套执行或 logId 分别下载；没有日志被截断或删除。",
            })
        for row in rows:
            _check_nul(row[5])
        state = dict(v=1, scope=scope, user=str(user_id), expires=int(time.time()) + CURSOR_LIFETIME_SECONDS,
            captured=datetime.now(timezone.utc).isoformat(), execution=request.execution_id,
            log=request.log_id, records=[[r[0], r[1], r[2], str(r[3]), r[4]] for r in rows], index=0, offset=0, part=1)

    pieces, remaining, visited = [], MAX_CHUNK_CHARS, 0
    records = state["records"]
    while state["index"] < len(records) and remaining and visited < MAX_CHUNK_RECORDS:
        log_id, suite_id, execution_id, timestamp, end = records[state["index"]]
        header = f"[{timestamp}] [suite={suite_id} execution={execution_id or '-'} log={log_id}]\n"
        offset = state["offset"]
        prefix = header[offset:offset + remaining] if offset < len(header) else ""
        offset += len(prefix)
        body_start = max(0, offset - len(header))
        take = min(remaining - len(prefix), max(0, end - body_start))
        # This scalar projection never constructs a TestSuiteLog ORM entity.
        row = query.filter(TestSuiteLog.id == log_id, TestSuiteLog.suite_id == suite_id,
            TestSuiteLog.execution_id == execution_id).with_entities(character_length(query),
                func.substr(TestSuiteLog.message, body_start + 1, take), _nul_position(query)).first()
        if row is None or row[0] < end or len(row[1]) != take:
            raise HTTPException(409, {"code": "LOG_EXPORT_GAP", "logId": log_id,
                "message": "快照中的日志已删除或缩短，下载中止。请保留已下载部分并重新选择日志。"})
        _check_nul(row[2])
        pieces.extend((prefix, row[1]))
        consumed = len(prefix) + take
        offset += take
        if offset == len(header) + end and remaining > consumed:
            pieces.append("\n")
            consumed += 1
            state["index"] += 1
            offset = 0
        state["offset"] = offset
        remaining -= consumed
        visited += 1

    complete = state["index"] == len(records)
    part = state["part"]
    state["part"] += 1
    return dict(content="".join(pieces), complete=complete,
        nextCursor=None if complete else _sign(state), part=part, recordCount=len(records),
        snapshotAt=state["captured"], maxChunkBytes=MAX_CHUNK_CHARS * 4)
