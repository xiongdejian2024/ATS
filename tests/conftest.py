"""All regression state lives in a fresh SQLite database and temporary workspace."""

import os
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))
TEST_DIRECTORY = Path(tempfile.mkdtemp(prefix="ats-software-regression-"))
postgres_test_url = os.environ.get("ATS_POSTGRES_TEST_URL")
if postgres_test_url:
    from sqlalchemy.engine import make_url
    test_url = make_url(postgres_test_url)
    if (test_url.get_backend_name() != "postgresql"
            or test_url.host not in {"127.0.0.1", "localhost"}
            or test_url.database != "ats_pg_regression"
            or test_url.query
            or any(name.startswith("PG") for name in os.environ)):
        raise RuntimeError("Destructive regression tests require loopback ats_pg_regression")
    os.environ["DATABASE_URL"] = postgres_test_url
    os.environ["DATABASE_SCHEMA"] = ""
else:
    os.environ["DATABASE_URL"] = "sqlite:///" + str(TEST_DIRECTORY / "test.sqlite")
os.environ["ENVIRONMENT"] = "test"
os.environ["LOG_FILE"] = str(TEST_DIRECTORY / "backend.log")


@pytest.fixture(autouse=True)
def isolated_database():
    from database import engine, Base
    import models

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    try:
        yield
    finally:
        # SQLite caches schema per connection. A pooled handle that observed a
        # DROP can report missing auto-indexes after another handle recreates the
        # table. Close idle handles after test fixtures release their sessions,
        # before the next test's destructive schema reset. Production is untouched.
        engine.dispose()


@pytest.fixture
def sat_config(tmp_path):
    from agent.config import Config

    config = Config()
    config.work_dir = tmp_path / "agent"
    config.work_dir.mkdir()
    config.default_timeout = 20
    return config
