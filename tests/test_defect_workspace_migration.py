"""Additive defect migration preserves prior identities and does not grant access."""

import pytest
from sqlalchemy import create_engine, event, inspect, text
from migrations.add_defect_workspace import upgrade
from models import Permission
from models.case_features import CaseIssue


def seed(engine):
    with engine.begin() as conn:
        for name in ["users", "projects"]:
            conn.execute(text(f"CREATE TABLE {name}(id VARCHAR(36) PRIMARY KEY)"))
        conn.execute(text("INSERT INTO users VALUES ('owner')"))
        conn.execute(text("INSERT INTO projects VALUES ('project')"))
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


def check(engine):
    with engine.connect() as conn:
        retained = dict(
            conn.execute(text("SELECT * FROM case_issues WHERE id='retained'"))
            .mappings()
            .one()
        )
    statements = []

    def capture(_conn, _cursor, sql, _params, _context, _many):
        statements.append(sql)

    event.listen(engine, "before_cursor_execute", capture)
    try:
        planned = upgrade(engine)
    finally:
        event.remove(engine, "before_cursor_execute", capture)
    assert len(planned) == 8
    assert not any(
        s.lstrip()
        .upper()
        .startswith(("CREATE ", "ALTER ", "DROP ", "INSERT ", "UPDATE ", "DELETE "))
        for s in statements
    )
    assert "defect_profiles" not in inspect(engine).get_table_names()
    assert upgrade(engine, apply=True) == planned
    assert upgrade(engine, apply=True) == []
    with engine.connect() as conn:
        assert (
            dict(
                conn.execute(text("SELECT * FROM case_issues WHERE id='retained'"))
                .mappings()
                .one()
            )
            == retained
        )
        assert set(
            conn.execute(
                text("SELECT code FROM permissions WHERE resource='defect'")
            ).scalars()
        ) == {"defect:read", "defect:create", "defect:update", "defect:delete"}
        for name in [
            "defect_profiles",
            "defect_comments",
            "defect_events",
            "defect_templates",
        ]:
            assert conn.execute(text(f"SELECT COUNT(*) FROM {name}")).scalar_one() == 0
    assert not {"project_permissions", "role_permissions", "user_roles"} & set(
        inspect(engine).get_table_names()
    )


def test_preview_apply_idempotence_and_preserved_legacy(tmp_path):
    engine = create_engine("sqlite:///" + str(tmp_path / "legacy.sqlite"))
    try:
        seed(engine)
        check(engine)
    finally:
        engine.dispose()


def test_incompatible_existing_sidecar_is_refused_before_any_mutation(tmp_path):
    engine = create_engine("sqlite:///" + str(tmp_path / "bad.sqlite"))
    try:
        seed(engine)
        with engine.begin() as conn:
            conn.execute(
                text("CREATE TABLE defect_profiles(issue_id VARCHAR(36) PRIMARY KEY)")
            )
        original = set(inspect(engine).get_table_names())
        with pytest.raises(ValueError, match="Incompatible"):
            upgrade(engine, apply=True)
        assert set(inspect(engine).get_table_names()) == original
        with engine.connect() as conn:
            assert (
                conn.execute(text("SELECT COUNT(*) FROM permissions")).scalar_one() == 0
            )
    finally:
        engine.dispose()
