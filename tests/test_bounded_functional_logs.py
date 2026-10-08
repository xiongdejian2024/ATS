"""功能测试执行日志：隔离库尾部查询、权限、实际pytest子进程实时输出。"""
import asyncio
import sys
from datetime import datetime, timedelta
from types import SimpleNamespace
import httpx
import pytest
from sqlalchemy import event
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from models.test_suite import TestSuiteLog as SuiteLog
from services.bounded_logs import live_log_window


@pytest.mark.asyncio
async def test_history_tail_database_projection_and_latest_order(workspace_http):
    db, app, _ = workspace_http
    text = '完整前段' * 100000 + '\n中文😀末尾'
    for i in range(25):
        db.add(SuiteLog(id=f'日志{i:02d}', suite_id='suite-0', execution_id=f'执行{i}', message=text,
                            timestamp=datetime(2026, 10, 6) + timedelta(seconds=i)))
    db.commit()
    statements = []
    def capture(_connection, _cursor, statement, _parameters, _context, _many): statements.append(statement)
    event.listen(db.bind, 'before_cursor_execute', capture)
    try:
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://隔离') as client:
            response = await client.get('/test-plans/suites/suite-0/logs', params=dict(limit=10000, tailChars=7, latest=True))
            assert response.status_code == 200, response.text
            data = response.json()['data']
            assert data['total'] == 25 and data['limit'] == 20
            assert [r['id'] for r in data['items']] == [f'日志{i:02d}' for i in range(5,25)]
            assert all(r['message'] == text[-7:] and r['totalChars'] == len(text) and r['truncated'] for r in data['items'])
            tail_function = 'right(' if db.bind.dialect.name == 'postgresql' else 'substr('
            sql = [s for s in statements if tail_function in s.lower()]
            assert len(sql) == 1
            assert 'test_suite_logs.message,' not in sql[0].split(tail_function)[0]
            assert not any(isinstance(o, SuiteLog) for o in db.identity_map.values())
            assert db.query(SuiteLog.message).filter_by(id='日志24').scalar() == text
            result = await client.get('/test-plans/suites/suite-0/logs', params=dict(executionId='执行3', tailChars=3, latest=True))
            assert result.json()['data']['items'][0]['message'] == '😀末尾'
            full = await client.get('/test-plans/suites/suite-0/logs', params=dict(logId='日志24'))
            assert full.json()['data']['items'][0]['message'] == text
    finally:
        event.remove(db.bind, 'before_cursor_execute', capture)


@pytest.mark.asyncio
async def test_tail_read_permissions_and_invalid_bounds(workspace_http):
    db, app, identity = workspace_http
    db.add(SuiteLog(id='日志', suite_id='suite-0', execution_id='执行', message='未截断')); db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://隔离') as client:
        result = await client.get('/test-plans/suites/suite-0/logs', params={'tailChars':32768})
        assert result.status_code == 200 and result.json()['data']['items'][0]['truncated'] is False
        for params in [dict(tailChars=0), dict(tailChars=32769), dict(skip=-1), dict(limit=0), dict(limit=10001)]:
            assert (await client.get('/test-plans/suites/suite-0/logs', params=params)).status_code == 422
        identity['id'] = 'stranger'
        assert (await client.get('/test-plans/suites/suite-0/logs', params={'tailChars':10})).status_code == 403
        assert (await client.get('/test-plans/suites/missing/logs', params={'tailChars':10})).status_code == 404


@pytest.mark.asyncio
async def test_central_log_handler_persists_full_and_pushes_bounded_delta(plan_lab, monkeypatch):
    from api.v1.websocket import handle_test_suite_log, frontend_manager
    db, _ = plan_lab; messages = []
    async def broadcast(suite_id, data): messages.append(data)
    monkeypatch.setattr(frontend_manager, 'broadcast_log', broadcast)
    for text in ['开头😀', '中' * 100000 + '尾😀']:
        await handle_test_suite_log(db, 'node', dict(suite_id='suite-0', execution_id='执行', message=text))
    saved = db.query(SuiteLog).filter_by(execution_id='执行').one()
    assert saved.message == '开头😀\n' + '中' * 100000 + '尾😀'
    assert len(messages[1]['message']) == 32768 and messages[1]['message'].endswith('尾😀') and messages[1]['truncated']
    assert messages[1]['endOffset'] == len(saved.message)
    assert live_log_window(saved, '最新')['message'] == '最新'


@pytest.mark.asyncio
async def test_actual_functional_pytest_outputs_before_completion(tmp_path, monkeypatch, sat_config):
    from agent.sat_runner import SATRunner
    import agent.sat_runner as runner_module
    script = tmp_path / 'test_functional.py'
    script.write_text('import time\ndef test_caseid_FUNCTIONAL():\n print("功能用例实时开始", flush=True)\n time.sleep(0.8)\n print("功能用例实时结束", flush=True)\n assert 1 + 1 == 2\n')
    started = asyncio.Event(); messages = []
    class Client:
        async def send_message(self, message):
            messages.append(message)
            if message.get('type') == 'test_suite_log' and '功能用例实时开始' in message.get('message', ''): started.set()
            return True
    original = runner_module.build_invocation
    def invocation(config, options, directory, selection):
        options.tests = str(script)
        old_path = sys.path[:]
        try:
            command, env = original(config, options, directory, selection)
        finally:
            sys.path[:] = old_path
        env.update(ATS_CASE_SELECTION=str(directory/'selection.json'), ATS_RESULT_FILE=str(directory/'results.json'), PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
        return [sys.executable, '-m', 'pytest', '-s', '--noconftest', '-p', 'integrations.sat_pytest', str(script)], env
    monkeypatch.setattr(runner_module, 'build_invocation', invocation)
    runner = SATRunner(SimpleNamespace(work_dir=tmp_path/'agent', ws_client=Client(), config=sat_config))
    task = asyncio.create_task(runner.execute(dict(suite_id='suite-0', execution_id='实际功能执行', case_ids=['case-0'], case_codes=['FUNCTIONAL'], execution_command='xat --mode offline', git_enabled=False)))
    await asyncio.wait_for(started.wait(), 15)
    assert not task.done(), '开始日志必须在执行完成前到达'
    await asyncio.wait_for(task, 20)
    assert any('功能用例实时结束' in m.get('message','') for m in messages)
    assert any(m.get('type') == 'test_suite_result' and m.get('result') == 'passed' for m in messages), messages
    assert all(m['execution_id'] == '实际功能执行' for m in messages if m.get('type') == 'test_suite_log')
