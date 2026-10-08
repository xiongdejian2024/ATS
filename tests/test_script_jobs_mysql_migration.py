"""Opt-in real MySQL migration qualification on an empty, disposable CI database."""
import importlib.util
import os
from datetime import datetime
from pathlib import Path

import pytest
from sqlalchemy import create_engine, event, inspect, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import DBAPIError


def test_real_mysql_preserves_legacy_queue_and_accepts_independent_script_jobs():
    source = os.environ.get('ATS_MYSQL_TEST_URL')
    if not source:
        pytest.skip('Dedicated disposable MySQL CI service is not configured')
    url = make_url(source)
    if (os.environ.get('CI') != 'true' or os.environ.get('ATS_MYSQL_ISOLATED') != '1'
            or url.database != 'ats_migration_test' or url.host not in {'127.0.0.1', 'localhost'}
            or url.get_backend_name() != 'mysql'):
        pytest.fail('Refusing any database other than the explicit loopback CI fixture')
    engine = create_engine(url, pool_pre_ping=True)
    try:
        if inspect(engine).get_table_names():
            pytest.fail('MySQL fixture must start empty; this test never drops existing tables')
        with engine.begin() as connection:
            for name in ['users', 'projects', 'environments', 'test_suites']:
                connection.execute(text(f'CREATE TABLE {name} (id VARCHAR(36) NOT NULL PRIMARY KEY) ENGINE=InnoDB'))
            connection.execute(text('''CREATE TABLE task_queue (
                id VARCHAR(36) NOT NULL PRIMARY KEY,
                environment_id VARCHAR(36) NOT NULL, suite_id VARCHAR(36) NOT NULL,
                execution_id VARCHAR(36) NOT NULL, executor_id VARCHAR(36) NOT NULL,
                status VARCHAR(50) NOT NULL, priority INTEGER NOT NULL DEFAULT 0,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, started_at DATETIME NULL, completed_at DATETIME NULL,
                CONSTRAINT fk_legacy_node FOREIGN KEY (environment_id) REFERENCES environments(id) ON DELETE CASCADE,
                CONSTRAINT fk_legacy_suite FOREIGN KEY (suite_id) REFERENCES test_suites(id) ON DELETE CASCADE,
                CONSTRAINT fk_legacy_executor FOREIGN KEY (executor_id) REFERENCES users(id),
                INDEX ix_legacy_execution (execution_id), INDEX ix_legacy_state (status)
            ) ENGINE=InnoDB'''))
            for name, value in [('users', 'owner'), ('projects', 'project'), ('environments', 'node'), ('test_suites', 'suite')]:
                connection.execute(text(f'INSERT INTO {name}(id) VALUES (:id)'), {'id': value})
            connection.execute(text('''INSERT INTO task_queue
                (id,environment_id,suite_id,execution_id,executor_id,status,priority,created_at)
                VALUES ('legacy-row','node','suite','legacy-execution','owner','pending',7,'2026-10-08 00:00:00')'''))
        with engine.connect() as connection:
            before = dict(connection.execute(text('SELECT * FROM task_queue')).mappings().one())
        legacy_fks = inspect(engine).get_foreign_keys('task_queue')
        root = Path(__file__).resolve().parents[1]
        spec = importlib.util.spec_from_file_location('ats_mysql_script_migration', root / 'scripts/upgrade_script_jobs.py')
        migration = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migration)
        statements = []
        def capture(_connection, _cursor, sql, _parameters, _context, _many):
            statements.append(sql)
        event.listen(engine, 'before_cursor_execute', capture)
        try:
            planned = migration.upgrade(engine, apply=False)
        finally:
            event.remove(engine, 'before_cursor_execute', capture)
        assert planned
        assert not any(sql.lstrip().upper().startswith(('CREATE ', 'ALTER ', 'DROP ', 'INSERT ', 'UPDATE ', 'DELETE ')) for sql in statements)
        assert 'script_jobs' not in inspect(engine).get_table_names()
        migration.upgrade(engine, apply=True)
        assert migration.upgrade(engine, apply=True) == []
        schema = inspect(engine)
        columns = {column['name']: column for column in schema.get_columns('task_queue')}
        assert columns['suite_id']['nullable'] is True
        assert columns['kind']['default'].strip("'\"") == 'suite'
        assert {'ix_legacy_execution', 'ix_legacy_state', 'ix_task_queue_script_job_id'} <= {i['name'] for i in schema.get_indexes('task_queue')}
        actual_fks = {f['name']: f for f in schema.get_foreign_keys('task_queue')}
        for previous in legacy_fks:
            assert actual_fks[previous['name']] == previous
        with engine.connect() as connection:
            retained = dict(connection.execute(text("SELECT * FROM task_queue WHERE id='legacy-row'")).mappings().one())
        assert {key: retained[key] for key in before} == before
        assert retained['kind'] == 'suite' and retained['script_job_id'] is None

        from models.script_job import ScriptJob, ScriptJobRun
        from models.task_queue import TaskQueue
        config = {'mode': 'python', 'script': 'print("synthetic")', 'args': [], 'workDir': '', 'timeoutSeconds': 10}
        now = datetime(2026, 10, 8)
        with engine.begin() as connection:
            connection.execute(ScriptJob.__table__.insert().values(id='job', project_id='project', name='Synthetic job',
                environment_id='node', config=config, revision=1, created_by='owner', updated_by='owner', created_at=now, updated_at=now))
            connection.execute(ScriptJobRun.__table__.insert().values(execution_id='script-execution', job_id='job',
                project_id='project', environment_id='node', executor_id='owner', request_id='synthetic-request',
                config_snapshot=config, delivery_state='queued', created_at=now))
            connection.execute(TaskQueue.__table__.insert().values(id='script-row', environment_id='node', suite_id=None,
                script_job_id='job', kind='script', execution_id='script-execution', executor_id='owner', status='pending', priority=0))
        with pytest.raises(DBAPIError) as violation:
            with engine.begin() as connection:
                connection.execute(text("INSERT INTO task_queue (id,environment_id,suite_id,script_job_id,kind,execution_id,executor_id,status,priority,created_at) VALUES ('bad-row','node','suite','job','script','bad','owner','pending',0,NOW())"))
        assert violation.value.orig.args[0] == 3819  # MySQL CHECK constraint rejection
        with engine.connect() as connection:
            assert connection.execute(text('SELECT COUNT(*) FROM task_queue')).scalar_one() == 2
        assert migration.migration_plan(engine) == []
    finally:
        engine.dispose()
