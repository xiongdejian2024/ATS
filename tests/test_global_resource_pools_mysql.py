"""Actual additive MySQL pool migration on prior disposable CI legacy fixtures."""

import os
import pytest
from sqlalchemy import create_engine, inspect, text, event
from sqlalchemy.engine import make_url
from sqlalchemy.exc import IntegrityError


def test_real_mysql_independent_pool_migration_preserves_legacy_and_node_foreign_keys():
    source = os.environ.get("ATS_MYSQL_TEST_URL")
    if not source:
        pytest.skip("Dedicated disposable MySQL CI service is not configured")
    url = make_url(source)
    if (
        os.environ.get("CI") != "true"
        or os.environ.get("ATS_MYSQL_ISOLATED") != "1"
        or url.database != "ats_migration_test"
        or url.host not in {"127.0.0.1", "localhost"}
        or url.get_backend_name() != "mysql"
        or url.query
    ):
        pytest.fail("Refusing any database other than the explicit loopback CI fixture")
    engine = create_engine(url, pool_pre_ping=True)
    from migrations.add_global_resource_pools import upgrade
    from models.global_resource_pool import (
        GlobalResourcePool as Pool,
        GlobalResourcePoolProject as Scope,
        GlobalResourcePoolMember as Member,
    )

    try:
        with engine.connect() as conn:
            retained = (
                conn.execute(text("SELECT * FROM task_queue ORDER BY id"))
                .mappings()
                .all()
            )
        statements = []

        def capture(_conn, _cursor, sql, _parameters, _context, _many):
            statements.append(sql)

        event.listen(engine, "before_cursor_execute", capture)
        try:
            assert len(upgrade(engine)) == 3
        finally:
            event.remove(engine, "before_cursor_execute", capture)
        assert not any(
            s.lstrip()
            .upper()
            .startswith(("CREATE ", "ALTER ", "DROP ", "INSERT ", "UPDATE ", "DELETE "))
            for s in statements
        )
        upgrade(engine, apply=True)
        assert upgrade(engine, apply=True) == []
        with engine.begin() as conn:
            conn.execute(
                Pool.__table__.insert().values(
                    id="migration-pool",
                    name="Synthetic pool",
                    updated_by="owner",
                    revision=1,
                    creation_key="synthetic-pool-create",
                    creation_fingerprint="b" * 64,
                )
            )
            conn.execute(
                Scope.__table__.insert().values(
                    pool_id="migration-pool", project_id="project"
                )
            )
            conn.execute(
                text("INSERT INTO environments(id) VALUES('migration-pool-node')")
            )
            conn.execute(
                Member.__table__.insert().values(
                    pool_id="migration-pool",
                    environment_id="migration-pool-node",
                    position=0,
                )
            )
        with pytest.raises(IntegrityError):
            with engine.begin() as conn:
                conn.execute(
                    text("DELETE FROM environments WHERE id='migration-pool-node'")
                )
        with engine.connect() as conn:
            assert (
                conn.execute(text("SELECT * FROM task_queue ORDER BY id"))
                .mappings()
                .all()
                == retained
            )
            assert (
                conn.execute(
                    text(
                        "SELECT COUNT(*) FROM environments WHERE id='migration-pool-node'"
                    )
                ).scalar_one()
                == 1
            )
            assert (
                conn.execute(
                    text(
                        "SELECT revision FROM global_resource_pools WHERE id='migration-pool'"
                    )
                ).scalar_one()
                == 1
            )
        fks = inspect(engine).get_foreign_keys("global_resource_pool_members")
        assert any(
            f["referred_table"] == "environments"
            and f.get("options", {}).get("ondelete", "RESTRICT").upper()
            in {"RESTRICT", "NO ACTION"}
            for f in fks
        )
    finally:
        engine.dispose()
