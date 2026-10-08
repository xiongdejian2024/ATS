"""PostgreSQL row locks serialize replay without duplicating stored evidence."""
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import pytest
from database import engine, SessionLocal
from models.test_suite import TestSuiteLog as SuiteLog
from services.agent_log_ingest import persist_log_batch
from test_plan_orchestration import plan_lab
from test_agent_log_delivery import add_task, batch

pytestmark = pytest.mark.skipif(engine.dialect.name != 'postgresql', reason='Real PostgreSQL row-lock test')


def test_concurrent_cursor_replay_appends_once(plan_lab):
    db, _ = plan_lab
    add_task(db)
    first = batch('first😀')
    assert persist_log_batch(db, 'node', first)[0]['through_sequence'] == 1
    replay = batch('second中文', stream_id=first['stream_id'], first=2)
    barrier = Barrier(4)

    def append(_):
        with SessionLocal() as session:
            barrier.wait(timeout=5)
            return persist_log_batch(session, 'node', replay)

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(append, range(4)))
    assert all(response['type'] == 'log_batch_ack' and response['through_sequence'] == 2 for response, _ in results)
    assert sum(len(deltas) for _, deltas in results) == 1
    db.expire_all()
    assert db.query(SuiteLog.message).scalar() == 'first😀\nsecond中文'


def test_session_setup_survives_filtered_startup_options_and_rollback(monkeypatch):
    from sqlalchemy import text
    # connect_args are merged later by SQLAlchemy, so intercept the DBAPI
    # connection itself to emulate a pooler discarding all startup options.
    connect = engine.dialect.dbapi.connect
    def without_options(*args, **kwargs):
        kwargs.pop('options', None)
        return connect(*args, **kwargs)
    monkeypatch.setattr(engine.dialect.dbapi, 'connect', without_options)
    engine.dispose()
    try:
        with engine.connect() as connection:
            assert connection.execute(text('SHOW TimeZone')).scalar_one() == 'Asia/Shanghai'
            connection.rollback()
            assert connection.execute(text('SHOW TimeZone')).scalar_one() == 'Asia/Shanghai'
    finally:
        engine.dispose()
