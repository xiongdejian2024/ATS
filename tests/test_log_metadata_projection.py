import httpx
import pytest
from sqlalchemy import event
from sqlalchemy.exc import InvalidRequestError
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from models.test_suite import TestSuiteLog as SuiteLog
from services.bounded_logs import log_metadata_query

@pytest.mark.asyncio
async def test_history_metadata_never_loads_raw_body(workspace_http):
    db, app, _ = workspace_http
    db.add(SuiteLog(id='large-body', suite_id='suite-0', execution_id='run-large', message='日志取消\n' * 200000))
    db.commit()
    db.expunge_all()
    statements = []
    def capture(_c, _cursor, sql, _p, _ctx, _many):
        statements.append(sql)
    event.listen(db.bind, 'before_cursor_execute', capture)
    try:
        row = log_metadata_query(db).filter(SuiteLog.message.like('%取消%')).first()
        assert row.id == 'large-body'
        with pytest.raises(InvalidRequestError):
            _ = row.message
        db.expunge_all()
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://local') as client:
            response = await client.get('/test-plans/suites/suite-0/suite-executions')
            assert response.status_code == 200, response.text
        selected = [sql.split('FROM')[0] for sql in statements if sql.lstrip().upper().startswith('SELECT')]
        assert not any('test_suite_logs.message' in sql for sql in selected)
    finally:
        event.remove(db.bind, 'before_cursor_execute', capture)
