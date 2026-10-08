"""Transactional dedicated-schema initialization on disposable PostgreSQL only."""
import pytest
from sqlalchemy import inspect, text
from sqlalchemy.exc import DBAPIError
from pathlib import Path
from database import engine, Base
from test_postgres_initializer import initializer
initialize, IncompatibleSchema = initializer.initialize, initializer.IncompatibleSchema

pytestmark = pytest.mark.skipif(engine.dialect.name != 'postgresql', reason='Real PostgreSQL schema verification')


def test_exported_sql_creates_exact_schema_and_refuses_reapplication():
    schema = 'ats'
    assert not inspect(engine).has_schema(schema)
    sql = (Path(__file__).resolve().parents[1] / 'deploy/postgres_schema.sql').read_text()
    try:
        with engine.begin() as connection:
            connection.exec_driver_sql(sql)
            connection.execute(text("INSERT INTO ats.users (id, username, email, password_hash, status) VALUES ('export-sentinel', 'export-sentinel', 'sentinel@example.com', 'synthetic', true)"))
        assert len(inspect(engine).get_table_names(schema=schema)) == 82
        assert initialize(False, schema=schema, connection_engine=engine, metadata=Base.metadata)['createTables'] == []
        with pytest.raises(DBAPIError):
            with engine.begin() as connection:
                connection.exec_driver_sql(sql)
        with engine.connect() as connection:
            assert connection.execute(text('SELECT id FROM ats.users')).scalar_one() == 'export-sentinel'
    finally:
        with engine.begin() as connection:
            connection.execute(text('DROP SCHEMA IF EXISTS ats CASCADE'))


def test_all_models_initialize_idempotently_and_preserve_rows():
    schema = 'ats_initializer_regression'
    assert not inspect(engine).has_schema(schema)
    try:
        preview = initialize(False, schema=schema, connection_engine=engine, metadata=Base.metadata)
        assert preview['createSchema'] and len(preview['createTables']) == len(Base.metadata.tables)
        assert not inspect(engine).has_schema(schema)
        initialize(True, schema=schema, connection_engine=engine, metadata=Base.metadata)
        with engine.begin() as connection:
            connection.execute(text(f"INSERT INTO {schema}.users (id, username, email, password_hash, status) VALUES ('sentinel', 'sentinel', 'sentinel@test.invalid', 'synthetic', true)"))
        assert initialize(False, schema=schema, connection_engine=engine, metadata=Base.metadata)['createTables'] == []
        initialize(True, schema=schema, connection_engine=engine, metadata=Base.metadata)
        with engine.connect() as connection:
            assert connection.execute(text(f'SELECT id FROM {schema}.users')).scalar_one() == 'sentinel'
        with engine.begin() as connection:
            connection.execute(text(f'ALTER TABLE {schema}.users ADD COLUMN unexpected INTEGER'))
        with pytest.raises(IncompatibleSchema):
            initialize(True, schema=schema, connection_engine=engine, metadata=Base.metadata)
        with engine.connect() as connection:
            assert connection.execute(text(f'SELECT id FROM {schema}.users')).scalar_one() == 'sentinel'
    finally:
        # This module only runs under the guarded loopback synthetic test DB.
        with engine.begin() as connection:
            connection.execute(text(f'DROP SCHEMA IF EXISTS {schema} CASCADE'))
