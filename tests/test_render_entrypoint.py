"""Deployment configuration checks use synthetic secrets and never bind ports."""
import os
import subprocess
import sys
from pathlib import Path
import pytest


def run(overrides=None):
    root = Path(__file__).resolve().parents[1]
    environment = dict(os.environ, DATABASE_URL='postgresql://synthetic@127.0.0.1/unused',
                       DATABASE_SCHEMA='ats', JWT_SECRET_KEY='synthetic-jwt-only-' * 3,
                       ATS_ORIGIN_SERVICE_KEY='synthetic-origin-only-' * 3, PORT='17400')
    environment.update(overrides or {})
    source = '''
import runpy, sys, types
def verify(app, **kwargs):
    assert app == 'main:app'
    assert kwargs == dict(host='0.0.0.0', port=17400, workers=1, access_log=False, log_level='warning')
sys.modules['uvicorn'] = types.SimpleNamespace(run=verify)
runpy.run_path(sys.argv[1], run_name='__main__')
'''
    return subprocess.run([sys.executable, '-c', source, str(root / 'scripts/start_render.py')],
                          env=environment, capture_output=True, text=True)


def test_single_worker_and_no_token_url_access_logging():
    result = run()
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize('overrides', [
    {'ATS_ORIGIN_SERVICE_KEY': ''}, {'JWT_SECRET_KEY': 'your-super-secret-jwt-key-change-in-production'},
    {'ATS_ORIGIN_SERVICE_KEY': 'REPLACE_WITH_SEPARATE_APPROVED_SERVICE_SECRET'},
    {'DATABASE_URL': 'sqlite:///ephemeral.db'}, {'DATABASE_SCHEMA': ''},
    {'JWT_SECRET_KEY': 'synthetic-origin-only-' * 3},
])
def test_missing_or_unsafe_deployment_configuration_refuses_start(overrides):
    assert run(overrides).returncode != 0
