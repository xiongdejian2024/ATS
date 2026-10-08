"""Raw evidence survives large logs without unbounded server/browser JSON paths."""
import gc
import hashlib
import tracemalloc
from datetime import datetime

import httpx
import pytest
from sqlalchemy import event, update
from sqlalchemy.dialects import mysql

from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from models import ProjectMember
from models.test_suite import TestSuiteLog as Log
from models.plan_orchestration import PlanRun, PlanRunItem
from services.raw_log_export import (
    LogExportRequest, export_log_chunk, character_length, MAX_CHUNK_CHARS,
    LEGACY_MAX_CHARS, MAX_SNAPSHOT_RECORDS,
)


STAMP = datetime(2026, 10, 8, 1, 2, 3)
SUITE_PATH = '/test-plans/suites/suite-0/logs'


def put(db, id='log', body='原始\n\t空格  \r\n', execution='execution', suite='suite-0'):
    db.add(Log(id=id, suite_id=suite, execution_id=execution, message=body, timestamp=STAMP))
    db.commit()


def record_text(id, body, execution='execution', suite='suite-0'):
    return f'[{STAMP}] [suite={suite} execution={execution or "-"} log={id}]\n{body}\n'


def run(db):
    db.add(PlanRun(id='run', plan_id='plan', executor_id='owner', plan_name='计划', config_snapshot={}, case_snapshot=[], manual_results={}))
    db.flush()
    for i in range(2):
        db.add(PlanRunItem(id=f'item-{i}', run_id='run', suite_id=f'suite-{i}', execution_id=f'exec-{i}',
                          environment_id='node', sequence=i, suite_snapshot={}))
    db.commit()


@pytest.mark.asyncio
async def test_unicode_whitespace_no_newline_chunks_freeze_membership_and_end(workspace_http):
    db, app, _ = workspace_http
    body = ' \t' + '😀中文e\u0301' * 35000 + '\r\n \t'
    put(db, 'a', body, 'old-execution')
    put(db, 'b', '\tsecond record  ', 'second-execution')
    expected = record_text('a', body, 'old-execution') + record_text('b', '\tsecond record  ', 'second-execution')
    chunks = []
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        first = (await client.post(SUITE_PATH + '/export', json={})).json()['data']
        assert first['recordCount'] == 2 and not first['complete']
        # Subsequent appends and a new execution cannot extend this export.
        db.execute(update(Log).where(Log.id == 'a').values(message=body + 'NOT IN SNAPSHOT'))
        db.commit()
        put(db, 'c', 'NEW EXECUTION MUST NOT APPEAR', 'later-execution')
        chunk = first
        while True:
            assert len(chunk['content']) <= MAX_CHUNK_CHARS
            assert len(chunk['content'].encode()) <= 256 * 1024
            assert '\ufffd' not in chunk['content']
            assert chunk['part'] == len(chunks) + 1
            chunks.append(chunk['content'])
            if chunk['complete']:
                assert chunk['nextCursor'] is None
                break
            response = await client.post(SUITE_PATH + '/export', json={'cursor': chunk['nextCursor']})
            assert response.status_code == 200, response.text
            chunk = response.json()['data']
        assert ''.join(chunks) == expected
        assert (await client.post(SUITE_PATH + '/export', json={'executionId': 'second-execution'})).json()['data']['content'] == record_text('b', '\tsecond record  ', 'second-execution')
        assert (await client.post(SUITE_PATH + '/export', json={'logId': 'b'})).json()['data']['recordCount'] == 1


def test_giant_log_memory_and_database_projection_are_bounded(plan_lab):
    db, _ = plan_lab
    body = '😀中e\u0301' * 500000  # 2 million scalars, 5 MiB, no newline.
    expected = hashlib.sha256(record_text('giant', body).encode()).hexdigest()
    put(db, 'giant', body)
    db.expunge_all(); del body; gc.collect()
    statements = []
    def capture(_connection, _cursor, statement, parameters, _context, _many):
        statements.append((statement, parameters))
    event.listen(db.bind, 'before_cursor_execute', capture)
    tracemalloc.start()
    try:
        cursor, digest, parts = None, hashlib.sha256(), 0
        while True:
            result = export_log_chunk(db.query(Log).filter_by(suite_id='suite-0'), 'suite:suite-0', 'owner', LogExportRequest(cursor=cursor))
            digest.update(result['content'].encode())
            parts += 1
            cursor = result['nextCursor']
            if result['complete']:
                break
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop(); event.remove(db.bind, 'before_cursor_execute', capture)
    assert digest.hexdigest() == expected and parts > 20
    assert peak < 3 * 1024 * 1024, f'Python export peak {peak} must not scale with the full LONGTEXT'
    assert not any(isinstance(value, Log) for value in db.identity_map.values())
    reads = [sql for sql, _ in statements if 'test_suite_logs' in sql]
    assert all('test_suite_logs.message AS' not in sql for sql in reads)
    assert all('length(' in sql or 'substr(' in sql for sql in reads)
    assert all('LIMIT' in sql for sql in reads)
    for sql, parameters in statements:
        if 'substr(' in sql:
            assert parameters[1] <= MAX_CHUNK_CHARS
    # Production must count characters, not MySQL LENGTH's byte count.
    class MySQLSession:
        class bind:
            dialect = mysql.dialect()
    class Query:
        session = MySQLSession()
    assert str(character_length(Query()).compile(dialect=mysql.dialect())).startswith('char_length(')


@pytest.mark.asyncio
async def test_cursor_scope_user_tampering_expiry_and_permission_recheck(workspace_http, monkeypatch):
    import services.raw_log_export as module
    db, app, identity = workspace_http
    put(db, body='😀' * (MAX_CHUNK_CHARS * 2))
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        result = await client.post(SUITE_PATH + '/export', json={})
        cursor = result.json()['data']['nextCursor']
        assert (await client.post(SUITE_PATH + '/export', json={'cursor': cursor[:-1] + ('0' if cursor[-1] != '0' else '1')})).status_code == 400
        assert (await client.post('/test-plans/suites/suite-1/logs/export', json={'cursor': cursor})).status_code == 400
        assert (await client.post(SUITE_PATH + '/export', json={'cursor': cursor, 'executionId': 'changed'})).status_code == 400
        assert (await client.post(SUITE_PATH + '/export', json={'cursor': 'broken'})).status_code == 400
        identity['id'] = 'stranger'
        assert (await client.post(SUITE_PATH + '/export', json={'cursor': cursor})).status_code == 403
        db.add(ProjectMember(project_id='project', user_id='stranger', role='member')); db.commit()
        assert (await client.post(SUITE_PATH + '/export', json={'cursor': cursor})).status_code == 400
        identity['id'] = 'owner'
        monkeypatch.setattr(module.time, 'time', lambda: 99999999999)
        assert (await client.post(SUITE_PATH + '/export', json={'cursor': cursor})).status_code == 410


@pytest.mark.asyncio
@pytest.mark.parametrize('remove', [False, True])
async def test_deleted_or_shortened_snapshot_is_explicit_gap(workspace_http, remove):
    db, app, _ = workspace_http
    put(db, body='x' * (MAX_CHUNK_CHARS * 2))
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        cursor = (await client.post(SUITE_PATH + '/export', json={})).json()['data']['nextCursor']
        if remove:
            db.query(Log).delete()
        else:
            db.execute(update(Log).where(Log.id == 'log').values(message='shortened'))
        db.commit()
        result = await client.post(SUITE_PATH + '/export', json={'cursor': cursor})
        assert result.status_code == 409 and result.json()['detail']['code'] == 'LOG_EXPORT_GAP'


@pytest.mark.asyncio
async def test_plan_export_uses_exact_run_suite_execution_pairs_and_bounded_preview(workspace_http):
    db, app, identity = workspace_http
    run(db)
    put(db, 'first', 'a' * (MAX_CHUNK_CHARS + 20), 'exec-0')
    put(db, 'second', 'B\n\n  ', 'exec-1', 'suite-1')
    put(db, 'unrelated', 'NOT THIS RUN', 'next-execution')
    put(db, 'wrong-suite', 'NOT THIS SUITE', 'exec-0', 'suite-1')
    paths = ['/test-plans/plan/executions/run/logs', '/orchestration/runs/run/logs']
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        for path in paths:
            preview = await client.get(path, params={'tailChars': 10})
            assert preview.status_code == 200
            assert preview.json()['data']['total'] == 2
            assert all(len(r['message']) <= 10 for r in preview.json()['data']['items'])
            response = await client.post(path + '/export', json={})
            data = response.json()['data']; output = data['content']
            assert data['recordCount'] == 2
            while data['nextCursor']:
                data = (await client.post(path + '/export', json={'cursor': data['nextCursor']})).json()['data']
                output += data['content']
            assert output == record_text('first', 'a' * (MAX_CHUNK_CHARS + 20), 'exec-0') + record_text('second', 'B\n\n  ', 'exec-1', 'suite-1')
            identity['id'] = 'stranger'
            assert (await client.post(path + '/export', json={})).status_code == 403
            identity['id'] = 'owner'
        assert (await client.post('/test-plans/other/executions/run/logs/export', json={})).status_code == 404


@pytest.mark.asyncio
async def test_explicit_caps_before_body_loading_and_legacy_small_contract(workspace_http):
    db, app, _ = workspace_http
    run(db)
    put(db, body='大' * (LEGACY_MAX_CHARS + 1), execution='exec-0')
    statements = []
    def capture(_connection, _cursor, statement, _parameters, _context, _many): statements.append(statement)
    event.listen(db.bind, 'before_cursor_execute', capture)
    try:
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
            for path in [SUITE_PATH, '/test-plans/plan/executions/run/logs', '/orchestration/runs/run/logs']:
                result = await client.get(path)
                assert result.status_code == 413, result.text
                assert result.json()['detail']['code'] == 'LOG_EXPORT_REQUIRED'
            assert all('test_suite_logs.message AS' not in sql for sql in statements)
            db.execute(update(Log).values(message='  full legacy\n\t')); db.commit()
            assert (await client.get(SUITE_PATH)).json()['data']['items'][0]['message'] == '  full legacy\n\t'
            assert 'full legacy' in (await client.get('/orchestration/runs/run/logs')).json()['data']['executionLog']
            db.add_all([Log(id=f'cap-{i:04d}', suite_id='suite-0', execution_id=f'e-{i}', message='', timestamp=STAMP) for i in range(MAX_SNAPSHOT_RECORDS)])
            db.commit()
            result = await client.post(SUITE_PATH + '/export', json={})
            assert result.status_code == 413 and result.json()['detail']['code'] == 'LOG_SELECTION_TOO_LARGE'
            result = await client.post(SUITE_PATH + '/export', json={'executionId': 'exec-0'})
            assert result.status_code == 200 and result.json()['data']['recordCount'] == 1
    finally:
        event.remove(db.bind, 'before_cursor_execute', capture)


@pytest.mark.asyncio
async def test_legacy_growth_after_preflight_is_bounded_and_explicit(workspace_http, monkeypatch):
    import services.raw_log_export as module
    db, app, _ = workspace_http
    put(db, body='small')
    check = module.check_legacy_log_budget
    def grow_after_snapshot(*args, **kwargs):
        rows = check(*args, **kwargs)
        db.execute(update(Log).values(message='巨' * (LEGACY_MAX_CHARS + 100)))
        db.commit()
        return rows
    monkeypatch.setattr(module, 'check_legacy_log_budget', grow_after_snapshot)
    statements = []
    def capture(_connection, _cursor, statement, parameters, _context, _many):
        if 'substr(' in statement: statements.append((statement, parameters))
    event.listen(db.bind, 'before_cursor_execute', capture)
    try:
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
            response = await client.get(SUITE_PATH)
            assert response.status_code == 409
        assert statements and statements[-1][1][1] == len('small')
        assert 'test_suite_logs.message AS' not in statements[-1][0]
    finally:
        event.remove(db.bind, 'before_cursor_execute', capture)


@pytest.mark.asyncio
async def test_legacy_sqlite_nul_is_rejected_without_claiming_complete(workspace_http):
    db, app, _ = workspace_http
    put(db, body='before\x00after')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        for method, path in [('get', SUITE_PATH), ('post', SUITE_PATH + '/export')]:
            response = await getattr(client, method)(path, **({'json': {}} if method == 'post' else {}))
            assert response.status_code == 409 and response.json()['detail']['code'] == 'LOG_UNSUPPORTED_NUL'
        assert db.query(Log.message).scalar() == 'before\x00after'


@pytest.mark.asyncio
async def test_empty_records_and_record_work_limit_never_skip_tied_timestamps(workspace_http):
    db, app, _ = workspace_http
    for i in range(65):
        db.add(Log(id=f'empty-{i:03d}', suite_id='suite-0', execution_id=None, message='', timestamp=STAMP))
    db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        response = await client.post(SUITE_PATH + '/export', json={})
        data = response.json()['data']; output = data['content']; part = 1
        while data['nextCursor']:
            data = (await client.post(SUITE_PATH + '/export', json={'cursor': data['nextCursor']})).json()['data']
            output += data['content']; part += 1
        assert part == 3 and data['complete']
        assert output == ''.join(record_text(f'empty-{i:03d}', '', None) for i in range(65))


@pytest.mark.asyncio
async def test_plan_log_authorization_does_not_load_report_or_case_snapshot(workspace_http):
    db, app, _ = workspace_http
    run(db); put(db, execution='exec-0')
    statements = []
    def capture(_connection, _cursor, statement, _parameters, _context, _many): statements.append(statement)
    event.listen(db.bind, 'before_cursor_execute', capture)
    try:
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
            for path in ['/test-plans/plan/executions/run/logs', '/orchestration/runs/run/logs']:
                assert (await client.post(path + '/export', json={})).status_code == 200
                assert (await client.get(path, params={'tailChars': 20})).status_code == 200
        assert any('plan_runs.id' in statement for statement in statements)
        assert not any('plan_runs.case_snapshot' in statement or 'plan_runs.report' in statement for statement in statements)
    finally:
        event.remove(db.bind, 'before_cursor_execute', capture)
