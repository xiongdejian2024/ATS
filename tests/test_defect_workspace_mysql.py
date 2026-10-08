"""Actual defect migration follows prior synthetic MySQL CI migrations."""

import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from test_defect_workspace_migration import check
from models.case_features import CaseIssue
from models import Permission


def test_real_mysql_defect_sidecars_preserve_legacy_queue_and_identity():
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
        with engine.connect() as conn:
            queue = (
                conn.execute(text("SELECT * FROM task_queue ORDER BY id"))
                .mappings()
                .all()
            )
        CaseIssue.__table__.create(engine, checkfirst=True)
        Permission.__table__.create(engine, checkfirst=True)
        with engine.begin() as conn:
            conn.execute(
                CaseIssue.__table__.insert().values(
                    id="retained",
                    project_id="project",
                    kind="defect",
                    title="Old identity",
                    description="<b>literal</b>",
                    status="open",
                    created_by="owner",
                    updated_by="owner",
                )
            )
        check(engine)
        with engine.connect() as conn:
            assert (
                conn.execute(text("SELECT * FROM task_queue ORDER BY id"))
                .mappings()
                .all()
                == queue
            )
    finally:
        engine.dispose()
