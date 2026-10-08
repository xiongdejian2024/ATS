"""Opt-in real MySQL RR interleaving on disposable loopback CI fixtures.

The production remove service runs against small, prefixed test mappings.
Existing migration fixtures are retained; no table or legacy row is dropped.
"""

import os
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    JSON,
    create_engine,
    event,
    inspect,
    text,
)
from sqlalchemy.engine import make_url
from sqlalchemy.orm import declarative_base, sessionmaker


def test_real_mysql_concurrent_configuration_prevents_group_delete(monkeypatch):
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
    engine = create_engine(url, isolation_level="REPEATABLE READ", pool_pre_ping=True)
    base = declarative_base()

    class Project(base):
        __tablename__ = "ats_env_rr_projects"
        id = Column(String(36), primary_key=True)

    class User(base):
        __tablename__ = "ats_env_rr_users"
        id = Column(String(36), primary_key=True)
        status = Column(Boolean, nullable=False)

    class Group(base):
        __tablename__ = "ats_env_rr_groups"
        id = Column(String(36), primary_key=True)
        project_id = Column(String(36), nullable=False)
        revision = Column(Integer, nullable=False)

    class Mapping(base):
        __tablename__ = "ats_env_rr_mappings"
        group_id = Column(String(36), primary_key=True)
        source_project_id = Column(String(36), primary_key=True)
        environment_id = Column(String(36), nullable=False)

    class Plan(base):
        __tablename__ = "ats_env_rr_plans"
        id = Column(String(36), primary_key=True)
        project_id = Column(String(36), nullable=False)

    class Configuration(base):
        __tablename__ = "ats_env_rr_configs"
        plan_id = Column(String(36), primary_key=True)
        scope = Column(String(80), primary_key=True)
        config = Column(JSON, nullable=False)

    try:
        if set(base.metadata.tables) & set(inspect(engine).get_table_names()):
            pytest.fail(
                "Prefixed concurrency fixtures must start absent; never replace existing tables"
            )
        base.metadata.create_all(engine)
        sessions = sessionmaker(bind=engine)
        with sessions.begin() as seed:
            seed.add_all(
                [
                    Project(id="rr-project"),
                    User(id="rr-owner", status=True),
                    Group(id="rr-group", project_id="rr-project", revision=1),
                    Mapping(
                        group_id="rr-group",
                        source_project_id="rr-project",
                        environment_id="rr-env",
                    ),
                    Plan(id="rr-plan", project_id="rr-project"),
                ]
            )
        from services import request_environment_group as groups
        from models import plan_execution_config

        for name, value in [
            ("Project", Project),
            ("User", User),
            ("TestPlan", Plan),
            ("RequestEnvironmentGroup", Group),
            ("RequestEnvironmentMapping", Mapping),
        ]:
            monkeypatch.setattr(groups, name, value)
        monkeypatch.setattr(plan_execution_config, "PlanExecutionConfig", Configuration)

        # Authorization itself is covered with actual ATS models in the PG/API
        # suite. This fixture isolates the exact RR snapshot/locking sequence.
        def access(db, actor, project_id, permission, *, current_read=False):
            query = db.query(Project).filter_by(id=project_id)
            return (
                query.populate_existing().with_for_update() if current_read else query
            ).one()

        monkeypatch.setattr(groups, "require_project_access", access)
        snapshot_ready, lock_attempted = Event(), Event()
        statements = []

        def observed(_connection, _cursor, sql, _parameters, _context, _many):
            if "ats_env_rr_projects" in sql and sql.lstrip().upper().startswith(
                "SELECT"
            ):
                if "FOR UPDATE" in sql.upper():
                    lock_attempted.set()
                else:
                    snapshot_ready.set()
            if "ats_env_rr_configs" in sql:
                statements.append(sql)

        actor = SimpleNamespace(id="rr-owner", status=True)
        with sessions() as writer:
            writer.query(Project).filter_by(id="rr-project").with_for_update().one()
            event.listen(engine, "before_cursor_execute", observed)

            def delete():
                with sessions() as deleting:
                    try:
                        groups.remove(deleting, actor, "rr-project", "rr-group", 1)
                        deleting.commit()
                        return 200
                    except HTTPException as error:
                        deleting.rollback()
                        return error.status_code

            with ThreadPoolExecutor(max_workers=1) as workers:
                pending = workers.submit(delete)
                try:
                    assert snapshot_ready.wait(5) and lock_attempted.wait(5)
                    writer.add(
                        Configuration(
                            plan_id="rr-plan",
                            scope="root:api",
                            config={"requestEnvironmentGroupId": "rr-group"},
                        )
                    )
                    writer.commit()  # Deleter resumes with a now-stale RR view.
                finally:
                    writer.rollback()  # Release lock even if synchronization fails.
                assert pending.result(timeout=10) == 409
            event.remove(engine, "before_cursor_execute", observed)
        with sessions() as retained:
            assert retained.get(Group, "rr-group").revision == 1
            assert retained.query(Mapping).count() == 1
        assert any(
            "FOR UPDATE" in sql.upper()
            for sql in statements
            if sql.lstrip().upper().startswith("SELECT")
        )

        # Exercise the actual two-table migration against the existing synthetic
        # legacy fixture, including foreign keys and keyed-create columns.
        from models.native_case import ApiTestEnvironment
        from models.request_environment_group import (
            RequestEnvironmentGroup,
            RequestEnvironmentMapping,
        )
        from migrations.add_request_environment_groups import upgrade

        ApiTestEnvironment.__table__.create(engine, checkfirst=True)
        with engine.connect() as connection:
            legacy = connection.execute(
                text("SELECT COUNT(*) FROM task_queue")
            ).scalar_one()
        assert len(upgrade(engine)) == 2
        upgrade(engine, apply=True)
        assert upgrade(engine, apply=True) == []
        with engine.begin() as connection:
            connection.execute(
                ApiTestEnvironment.__table__.insert().values(
                    id="migration-target",
                    project_id="project",
                    name="Synthetic",
                    address="http://synthetic.test/",
                    updated_by="owner",
                )
            )
            connection.execute(
                RequestEnvironmentGroup.__table__.insert().values(
                    id="migration-group",
                    project_id="project",
                    name="Synthetic",
                    updated_by="owner",
                    creation_key="synthetic-create",
                    creation_fingerprint="a" * 64,
                )
            )
            connection.execute(
                RequestEnvironmentMapping.__table__.insert().values(
                    group_id="migration-group",
                    source_project_id="project",
                    environment_id="migration-target",
                )
            )
        with engine.connect() as connection:
            assert (
                connection.execute(text("SELECT COUNT(*) FROM task_queue")).scalar_one()
                == legacy
            )
            assert (
                connection.execute(
                    text(
                        "SELECT revision FROM request_environment_groups WHERE id='migration-group'"
                    )
                ).scalar_one()
                == 1
            )
    finally:
        engine.dispose()
