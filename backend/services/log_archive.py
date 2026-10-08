"""Non-destructive global log accounting and bounded, atomic gzip archives.

Archives copy a frozen prefix. They never delete rows, advance delivery cursors,
or claim to free database space. An operator must explicitly enable archival.
"""
import gzip
import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import func, cast, LargeBinary
from models.test_suite import TestSuiteLog
from models.agent_log import AgentTaskLog
from models.script_job import ScriptJobLog

MODELS = {"suite": TestSuiteLog, "task": AgentTaskLog, "script": ScriptJobLog}
CHUNK_CHARS = 65536


@dataclass(frozen=True)
class ArchivePolicy:
    enabled: bool = False
    retention_days: int = 30
    warning_bytes: int = 10 * 1024**3
    max_archive_bytes: int = 1024**3
    directory: str = ""

    def __post_init__(self):
        if any(type(value) is not int or value <= 0 for value in
               (self.retention_days, self.warning_bytes, self.max_archive_bytes)):
            raise ValueError("Log archive limits must be positive integers")

    @classmethod
    def from_env(cls):
        flag = os.environ.get("ATS_LOG_ARCHIVE_ENABLED", "false").lower()
        if flag not in {"true", "false"}:
            raise ValueError("ATS_LOG_ARCHIVE_ENABLED must be true or false")
        return cls(enabled=flag == "true",
                   retention_days=int(os.environ.get("ATS_LOG_RETENTION_DAYS", "30")),
                   warning_bytes=int(os.environ.get("ATS_LOG_WARNING_BYTES", str(10 * 1024**3))),
                   max_archive_bytes=int(os.environ.get("ATS_LOG_ARCHIVE_MAX_BYTES", str(1024**3))),
                   directory=os.environ.get("ATS_LOG_ARCHIVE_DIR", ""))


def byte_length(db, column):
    return func.length(cast(column, LargeBinary)) if db.get_bind().dialect.name == "sqlite" else func.octet_length(column)


def capacity(db, policy=None, now=None):
    policy = policy or ArchivePolicy.from_env()
    cutoff = (now or datetime.now(timezone.utc)) - timedelta(days=policy.retention_days)
    tables = {}
    for name, model in MODELS.items():
        query = db.query(func.count(model.id), func.coalesce(func.sum(byte_length(db, model.message)), 0))
        records, size = query.one()
        old_records, old_size = query.filter(model.timestamp < cutoff).one()
        tables[name] = dict(records=records, utf8Bytes=int(size), olderRecords=old_records, olderBytes=int(old_size))
    total = sum(item["utf8Bytes"] for item in tables.values())
    return dict(tables=tables, utf8Bytes=total, warning=total >= policy.warning_bytes,
                warningBytes=policy.warning_bytes, retentionDays=policy.retention_days,
                archiveEnabled=policy.enabled, automaticDeletion=False,
                cutoff=cutoff.isoformat(), measurement="log text only; excludes indexes, WAL and backups")


def archive_record(db, kind, identifier, *, policy=None):
    policy = policy or ArchivePolicy.from_env()
    if not policy.enabled or not policy.directory:
        raise ValueError("Archival is disabled or ATS_LOG_ARCHIVE_DIR is unset")
    model = MODELS[kind]
    query = db.query(model).filter(model.id == identifier)
    chars = func.length(model.message) if db.get_bind().dialect.name == "sqlite" else func.char_length(model.message)
    columns = [column for column in model.__table__.columns if column.name != "message"]
    snapshot = query.with_entities(*columns, chars.label("_chars"), byte_length(db, model.message).label("_bytes")).first()
    if snapshot is None:
        raise ValueError("Log record does not exist")
    metadata = dict(snapshot._mapping)
    end, raw_size = metadata.pop("_chars"), metadata.pop("_bytes")
    if raw_size > policy.max_archive_bytes:
        raise ValueError("Log record exceeds archive byte budget")
    # SQLite text functions stop at NUL. Fail without replacing a previous copy.
    if db.get_bind().dialect.name == "sqlite" and query.with_entities(func.instr(model.message, "\x00")).scalar():
        raise ValueError("Legacy SQLite binary log requires a database backup")
    root = Path(policy.directory).resolve()
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    # Identifiers never become paths. Use one atomic artifact containing its
    # manifest and body, so interruption cannot publish an incomplete pair.
    name = kind + "-" + hashlib.sha256(identifier.encode()).hexdigest() + ".jsonl.gz"
    target = root / name
    descriptor, temporary = tempfile.mkstemp(dir=root, prefix=".ats-archive-")
    digest, copied = hashlib.sha256(), 0
    try:
        with os.fdopen(descriptor, "wb") as output:
            with gzip.GzipFile(fileobj=output, mode="wb", mtime=0) as compressed:
                header = dict(version=1, kind=kind, metadata=metadata, characters=end,
                              capturedAt=datetime.now(timezone.utc).isoformat(), format="utf8-json-chunks")
                compressed.write((json.dumps(header, default=str, ensure_ascii=False) + "\n").encode())
                for offset in range(0, end, CHUNK_CHARS):
                    piece = query.with_entities(func.substr(model.message, offset + 1, min(CHUNK_CHARS, end - offset))).scalar()
                    if piece is None or len(piece) != min(CHUNK_CHARS, end - offset):
                        raise ValueError("Log changed during archival")
                    data = piece.encode("utf-8")
                    digest.update(data); copied += len(data)
                    if copied > policy.max_archive_bytes:
                        raise ValueError("Archive byte budget exceeded")
                    compressed.write((json.dumps(dict(offset=offset, text=piece), ensure_ascii=False) + "\n").encode())
                compressed.write((json.dumps(dict(complete=True, utf8Bytes=copied, sha256=digest.hexdigest())) + "\n").encode())
            output.flush(); os.fsync(output.fileno())
        os.replace(temporary, target)
        directory_fd = os.open(root, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise
    return dict(path=str(target), characters=end, utf8Bytes=copied, sha256=digest.hexdigest(), sourceDeleted=False)


def archive_expired(db, *, policy=None, limit=100, now=None):
    policy = policy or ArchivePolicy.from_env()
    if not policy.enabled:
        raise ValueError("Archival is disabled")
    if type(limit) is not int or not 1 <= limit <= 1000:
        raise ValueError("Archive batch limit must be 1..1000")
    cutoff = (now or datetime.now(timezone.utc)) - timedelta(days=policy.retention_days)
    result = []
    for kind, model in MODELS.items():
        ids = db.query(model.id).filter(model.timestamp < cutoff).order_by(model.timestamp, model.id).limit(limit - len(result)).all()
        for (identifier,) in ids:
            result.append(archive_record(db, kind, identifier, policy=policy))
        if len(result) == limit:
            break
    return result
