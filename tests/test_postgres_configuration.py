"""Configuration validation never needs a database or real credentials."""
import os
import subprocess
import sys
from pathlib import Path
import pytest


@pytest.mark.parametrize('scheme', ['postgres', 'postgresql', 'postgresql+psycopg'])
def test_postgres_driver_schema_and_pool_configuration(scheme):
    root = Path(__file__).resolve().parents[1]
    environment = dict(os.environ, PYTHONPATH=str(root / 'backend'),
                       DATABASE_URL=f'{scheme}://synthetic@127.0.0.1/unused',
                       DATABASE_SCHEMA='ats', DATABASE_POOL_SIZE='3',
                       DATABASE_MAX_OVERFLOW='2')
    result = subprocess.run([sys.executable, '-c', '''
from database import engine, connect_args
assert engine.url.drivername == 'postgresql+psycopg'
assert connect_args['prepare_threshold'] is None
assert connect_args['options'] == '-c timezone=Asia/Shanghai -c search_path=ats'
assert engine.pool.size() == 3
'''], env=environment, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize('schema', ['auth', 'public', 'storage', 'pg_catalog', 'pg_bad', 'ats;DROP SCHEMA auth'])
def test_reserved_or_unsafe_schema_rejected(schema):
    root = Path(__file__).resolve().parents[1]
    environment = dict(os.environ, PYTHONPATH=str(root / 'backend'),
                       DATABASE_URL='postgresql://synthetic@127.0.0.1/unused', DATABASE_SCHEMA=schema)
    result = subprocess.run([sys.executable, '-c', 'import database'], env=environment,
                            capture_output=True, text=True)
    assert result.returncode != 0


@pytest.mark.parametrize('suffix, extra', [
    ('?host=example.invalid', {}), ('?hostaddr=192.0.2.1', {}),
    ('?dbname=production', {}), ('?service=production', {}),
    ('', {'PGHOSTADDR': '192.0.2.1'}), ('', {'PGSERVICE': 'production'}),
])
def test_destructive_test_guard_rejects_destination_overrides(suffix, extra):
    root = Path(__file__).resolve().parents[1]
    environment = dict(os.environ, ATS_POSTGRES_TEST_URL=
                       'postgresql+psycopg://synthetic@127.0.0.1/ats_pg_regression' + suffix, **extra)
    result = subprocess.run([sys.executable, str(root / 'tests/conftest.py')],
                            env=environment, capture_output=True, text=True)
    assert result.returncode != 0
    assert 'Destructive regression tests require loopback' in result.stderr
