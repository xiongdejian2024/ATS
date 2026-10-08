"""Environment revision/legacy update and frozen declarations use synthetic data."""

from copy import deepcopy
import httpx
import pytest
from sqlalchemy import create_engine, inspect, text
from test_native_case_filters import native, prepare, config, BASE
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from models.native_case import NativeCaseConfig, ApiDefinition, ApiTestEnvironment
from models.native_environment_variables import NativeEnvironmentVariables
from models import TestCase as Case, User
from services.native_http_execution import freeze
from migrations.add_native_environment_variables import upgrade


@pytest.mark.asyncio
async def test_legacy_update_preserves_variables_explicit_empty_clears_and_freeze(
    native,
):
    db, app, _ = native
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://fixture"
    ) as client:
        definition, env = await prepare(client)
        url = BASE + "/environments/" + env["id"]
        payload = dict(
            name=env["name"],
            address=env["address"],
            expectedRevision=env["revision"],
            variables=[
                dict(name="literal", value="  kept  "),
                dict(name="empty", value=""),
            ],
        )
        response = await client.put(url, json=payload)
        assert response.status_code == 200, response.text
        saved = response.json()["data"]["environments"][0]
        assert saved["variables"][0]["value"] == "  kept  "
        assert saved["variables"][1]["value"] == ""
        assert (await client.put(url, json=payload)).status_code == 409
        legacy = dict(
            name=env["name"], address=env["address"], expectedRevision=saved["revision"]
        )
        saved = (await client.put(url, json=legacy)).json()["data"]["environments"][0]
        assert saved["variables"][0]["value"] == "  kept  "
        case_payload = config(definition, env)
        case_payload["parameters"] = {"request": {}}
        response = await client.put(BASE + "/cases/case-0", json=case_payload)
        assert response.status_code == 200, response.text
        frozen = freeze(db, db.get(Case, "case-0"), db.get(User, "owner"))
        assert frozen["requests"][0]["environmentVariables"][0]["value"] == "  kept  "
        legacy.update(expectedRevision=saved["revision"], variables=[])
        cleared = (await client.put(url, json=legacy)).json()["data"]["environments"][0]
        assert cleared["variables"] == []
        assert frozen["requests"][0]["environmentVariables"][0]["value"] == "  kept  "
        assert (
            freeze(db, db.get(Case, "case-0"), db.get(User, "owner"))["requests"][0][
                "environmentVariables"
            ]
            == []
        )


def migration_check(engine):
    assert upgrade(engine) == ["native_environment_variables"]
    assert not inspect(engine).has_table("native_environment_variables")
    assert upgrade(engine, apply=True) == ["native_environment_variables"]
    assert upgrade(engine, apply=True) == []


def test_additive_migration_preview_and_apply():
    engine = create_engine("sqlite://")
    with engine.begin() as conn:
        conn.execute(
            text(
                "CREATE TABLE native_api_environments (id VARCHAR(36) PRIMARY KEY, name VARCHAR(255))"
            )
        )
        conn.execute(
            text("INSERT INTO native_api_environments VALUES ('retained', 'retained')")
        )
    migration_check(engine)
    with engine.connect() as conn:
        assert (
            conn.execute(text("SELECT name FROM native_api_environments")).scalar_one()
            == "retained"
        )
    engine.dispose()


def test_incompatible_migration_refuses_mutation():
    engine = create_engine("sqlite://")
    with engine.begin() as conn:
        conn.execute(
            text("CREATE TABLE native_api_environments (id VARCHAR(36) PRIMARY KEY)")
        )
        conn.execute(
            text("CREATE TABLE native_environment_variables (unknown INTEGER)")
        )
    with pytest.raises(ValueError, match="Incompatible"):
        upgrade(engine, apply=True)
    assert [
        c["name"] for c in inspect(engine).get_columns("native_environment_variables")
    ] == ["unknown"]
    engine.dispose()


from test_plan_native_workspace import native_workspace
from test_native_initial_variables import declaration


def test_disabled_cached_actor_cannot_save_request_initial_variables(native_workspace):
    from test_native_http_execution import configure
    from database import SessionLocal
    from models import User
    from models.native_case import NativeCaseConfig, ApiDefinition
    from schemas.native_case import ConfigInput
    from services.native_case import save_config
    from fastapi import HTTPException

    db, _, _ = native_workspace
    configure(db)
    actor = db.get(User, "owner")
    assert actor.status
    row = db.get(NativeCaseConfig, "case-0")
    definition = db.get(ApiDefinition, "definition")
    body = ConfigInput(
        state=row.state,
        environmentId=row.environment_id,
        apiDefinitionId=row.api_definition_id,
        expectedRevision=row.revision,
        expectedDefinitionRevision=definition.revision,
        parameters={"request": {"initialVariables": [declaration("new", "literal")]}},
    )
    with SessionLocal() as other:
        other.get(User, "owner").status = False
        other.commit()
    with pytest.raises(HTTPException) as caught:
        save_config(db, actor, "project", "case-0", body)
    assert caught.value.status_code == 403
    db.rollback()


def test_request_variable_write_rechecks_grant_after_project_lock(
    native_workspace, monkeypatch
):
    from test_native_http_execution import configure
    from database import SessionLocal
    from models import User, Permission, ProjectPermission
    from models.native_case import NativeCaseConfig, ApiDefinition
    from schemas.native_case import ConfigInput
    from services import native_case as service
    from fastapi import HTTPException

    db, _, _ = native_workspace
    configure(db)
    permission = Permission(
        code="test_case:update", name="用例编辑", resource="test_case", action="update"
    )
    db.add(permission)
    db.flush()
    db.add(
        ProjectPermission(
            project_id="project", user_id="stranger", permission_id=permission.id
        )
    )
    db.commit()
    actor = db.get(User, "stranger")
    row = db.get(NativeCaseConfig, "case-0")
    definition = db.get(ApiDefinition, "definition")
    before = row.revision
    body = ConfigInput(
        state=row.state,
        environmentId=row.environment_id,
        apiDefinitionId=row.api_definition_id,
        expectedRevision=before,
        expectedDefinitionRevision=definition.revision,
        parameters={"request": {"initialVariables": [declaration("new", "literal")]}},
    )
    lock = service.lock_project

    def revoke_then_lock(db_arg, project_id):
        with SessionLocal() as other:
            other.query(ProjectPermission).filter_by(
                project_id="project", user_id="stranger"
            ).delete()
            other.commit()
        return lock(db_arg, project_id)

    monkeypatch.setattr(service, "lock_project", revoke_then_lock)
    with pytest.raises(HTTPException) as caught:
        service.save_config(db, actor, "project", "case-0", body)
    assert caught.value.status_code == 403
    db.rollback()
    db.refresh(row)
    assert row.revision == before
