"""Real single-process production entrypoint against disposable PostgreSQL."""
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

import httpx
import psutil
import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import engine, Base
from test_postgres_initializer import initializer

pytestmark = pytest.mark.skipif(engine.dialect.name != 'postgresql', reason='Real isolated PostgreSQL controller smoke')


def test_protected_controller_login_readiness_and_idle_memory(tmp_path):
    from models import User
    from core.security import get_password_hash
    schema = 'ats_render_smoke'
    root = Path(__file__).resolve().parents[1]
    key = 'synthetic-origin-for-loopback-only-' * 2
    environment = dict(os.environ, DATABASE_URL=os.environ['ATS_POSTGRES_TEST_URL'],
                       DATABASE_SCHEMA=schema, JWT_SECRET_KEY='synthetic-jwt-for-loopback-only-' * 2,
                       ATS_ORIGIN_SERVICE_KEY=key, PORT='17400', TASK_SCHEDULER_ENABLED='false',
                       LOG_FILE=str(tmp_path / 'controller.log'))
    process = None
    try:
        initializer.initialize(True, schema=schema, connection_engine=engine, metadata=Base.metadata)
        with engine.connect() as connection:
            with Session(bind=connection.execution_options(schema_translate_map={None: schema})) as db:
                db.add(User(id=str(uuid.uuid4()), username='smoke', email='smoke@example.com',
                            password_hash=get_password_hash('synthetic-login-only')))
                db.commit()
        with (tmp_path / 'stdout.log').open('w') as log:
            process = subprocess.Popen([sys.executable, str(root / 'scripts/start_render.py')],
                                       cwd=root, env=environment, stdout=log, stderr=subprocess.STDOUT)
            with httpx.Client(base_url='http://127.0.0.1:17400', trust_env=False, timeout=5) as client:
                deadline = time.monotonic() + 30
                while True:
                    try:
                        response = client.get('/health')
                        break
                    except httpx.TransportError:
                        assert process.poll() is None, (tmp_path / 'stdout.log').read_text()
                        assert time.monotonic() < deadline
                        time.sleep(0.1)
                assert response.status_code == 403
                client.headers['X-ATS-Origin-Authorization'] = 'Bearer ' + key
                assert client.get('/health').status_code == 200
                assert client.get('/ready').json() == {'status': 'ready'}
                response = client.post('/api/v1/auth/login', json={'username': 'smoke', 'password': 'synthetic-login-only'})
                assert response.status_code == 200, response.text
                token = response.json()['data']['access_token']
                client.headers['Authorization'] = 'Bearer ' + token
                for _ in range(10):
                    assert client.get('/ready').status_code == 200
                rss = psutil.Process(process.pid).memory_info().rss
                print(f'Controller idle/login RSS: {rss / 1024**2:.1f} MiB')
                assert rss < 400 * 1024**2, '512MB tier needs headroom even at idle/login'
        logs = (tmp_path / 'stdout.log').read_text()
        assert key not in logs and token not in logs
    finally:
        if process is not None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        with engine.begin() as connection:
            connection.execute(text(f'DROP SCHEMA IF EXISTS {schema} CASCADE'))
