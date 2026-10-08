"""Additive MySQL migration after prior CI fixtures, with no existing data removal."""

import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from migrations.add_native_environment_variables import upgrade


def test_real_mysql_native_variable_sidecar_preserves_legacy_queue():
    source = os.environ.get("ATS_MYSQL_TEST_URL")
    if not source:
        pytest.skip("Dedicated disposable MySQL CI service is not configured")
    url = make_url(source)
    if (
        os.environ.get("CI") != "true"
        or os.environ.get("ATS_MYSQL_ISOLATED") != "1"
        or url.host not in {"127.0.0.1", "localhost"}
        or url.database != "ats_migration_test"
        or url.get_backend_name() != "mysql"
        or url.query
    ):
        pytest.fail("Refusing any database other than the explicit loopback CI fixture")
    engine = create_engine(url, pool_pre_ping=True)
    try:
        with engine.begin() as conn:
            queue = (
                conn.execute(text("SELECT * FROM task_queue ORDER BY id"))
                .mappings()
                .all()
            )
            conn.execute(
                text(
                    "CREATE TABLE IF NOT EXISTS native_api_environments (id VARCHAR(36) PRIMARY KEY)"
                )
            )
        assert upgrade(engine) == ["native_environment_variables"]
        assert upgrade(engine, apply=True) == ["native_environment_variables"]
        assert upgrade(engine, apply=True) == []
        with engine.connect() as conn:
            assert (
                conn.execute(text("SELECT * FROM task_queue ORDER BY id"))
                .mappings()
                .all()
                == queue
            )
    finally:
        engine.dispose()
