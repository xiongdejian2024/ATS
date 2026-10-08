import gzip
import hashlib
import json
from dataclasses import replace
from datetime import datetime, timezone, timedelta

import pytest
from sqlalchemy import event
from test_plan_orchestration import plan_lab
from models.test_suite import TestSuiteLog
from services.log_archive import ArchivePolicy, capacity, archive_record, archive_expired, CHUNK_CHARS


def put(db, body, identifier="evidence", stamp=None):
    db.add(TestSuiteLog(id=identifier, suite_id="suite-0", execution_id="execution",
                       message=body, timestamp=stamp or datetime(2020, 1, 1)))
    db.commit()


def test_capacity_counts_utf8_without_materializing_bodies_and_default_no_deletion(plan_lab):
    db, _ = plan_lab
    put(db, "😀中文")
    put(db, "new", "new", datetime.now(timezone.utc))
    statements = []
    def capture(_conn, _cursor, statement, *_args): statements.append(statement)
    event.listen(db.bind, "before_cursor_execute", capture)
    try:
        report = capacity(db, ArchivePolicy(warning_bytes=1))
    finally:
        event.remove(db.bind, "before_cursor_execute", capture)
    assert report["utf8Bytes"] == len("😀中文new".encode())
    assert report["tables"]["suite"]["olderRecords"] == 1
    assert report["warning"] and not report["automaticDeletion"] and not report["archiveEnabled"]
    assert all("sum(" in statement.lower() for statement in statements)


def test_atomic_archive_large_unicode_preserves_evidence_and_fixed_read_budget(plan_lab, tmp_path):
    db, _ = plan_lab
    body = "😀中\t\r\n " * 100000
    put(db, body)
    policy = ArchivePolicy(enabled=True, directory=str(tmp_path))
    report = archive_record(db, "suite", "evidence", policy=policy)
    with gzip.open(report["path"], "rt", encoding="utf-8") as source:
        rows = [json.loads(line) for line in source]
    assert rows[0]["characters"] == len(body)
    assert all(len(row["text"]) <= CHUNK_CHARS for row in rows[1:-1])
    assert "".join(row["text"] for row in rows[1:-1]) == body
    assert rows[-1]["sha256"] == hashlib.sha256(body.encode()).hexdigest()
    assert db.get(TestSuiteLog, "evidence").message == body
    assert not report["sourceDeleted"]
    assert len(list(tmp_path.iterdir())) == 1


def test_disabled_quota_and_binary_rejection_never_modify_evidence(plan_lab, tmp_path):
    db, _ = plan_lab
    put(db, "large body")
    policy = ArchivePolicy(directory=str(tmp_path))
    with pytest.raises(ValueError, match="disabled"):
        archive_expired(db, policy=policy)
    with pytest.raises(ValueError, match="budget"):
        archive_record(db, "suite", "evidence", policy=replace(policy, enabled=True, max_archive_bytes=1))
    assert list(tmp_path.iterdir()) == []
    assert db.get(TestSuiteLog, "evidence").message == "large body"
    if db.get_bind().dialect.name == "sqlite":
        put(db, "a\x00b", "binary")
        with pytest.raises(ValueError, match="binary"):
            archive_record(db, "suite", "binary", policy=replace(policy, enabled=True))


def test_expired_selection_bounded_and_failed_copy_leaves_previous_archive(plan_lab, tmp_path, monkeypatch):
    db, _ = plan_lab
    put(db, "old")
    put(db, "recent", "new", datetime.now(timezone.utc) + timedelta(days=1))
    policy = ArchivePolicy(enabled=True, directory=str(tmp_path))
    result = archive_expired(db, policy=policy, limit=1)
    assert len(result) == 1
    previous = list(tmp_path.iterdir())[0].read_bytes()
    monkeypatch.setattr("services.log_archive.os.replace", lambda *_: (_ for _ in ()).throw(OSError("disk full")))
    with pytest.raises(OSError): archive_record(db, "suite", "evidence", policy=policy)
    assert list(tmp_path.iterdir())[0].read_bytes() == previous
    assert len(list(tmp_path.iterdir())) == 1
    assert db.query(TestSuiteLog).count() == 2
