"""Permanent regressions promoted from independent review and API acceptance.

Only synthetic isolated databases and queued/deferred execution are used.
"""

import pytest
from conftest import isolated_database
from test_plan_orchestration import plan_lab
from test_plan_workspace import workspace_http
from test_plan_native_workspace import native_workspace
from schemas.request_environment_group import EnvironmentGroupInput
from services import request_environment_group as groups
from models import User, Project, ProjectMember, TestPlan as Plan, TestCase as Case
from models.native_case import ApiDefinition, ApiTestEnvironment, NativeCaseConfig
from models.request_environment_group import (
    RequestEnvironmentGroup,
    RequestEnvironmentMapping,
)
from api.v1.case_governance import transact


def save_group(db, actor, mappings, group=None, revision=0):
    body = EnvironmentGroupInput(
        name="group",
        expectedRevision=revision,
        mappings=[{"projectId": p, "environmentId": e} for p, e in mappings],
    )
    return transact(db, lambda: groups.save(db, actor, "project", body, group))


@pytest.mark.asyncio
async def test_multi_source_requests_freeze_group_mapping_and_revision(
    native_workspace,
):
    from copy import deepcopy
    from test_native_http_execution import configure
    from test_plan_execution_configuration import store
    from services.plan_tree import save_node
    from services.plan_orchestration import start_plan_run
    from models.plan_orchestration import PlanRunItem

    db, app, identity = native_workspace
    configure(db)
    db.add(
        ApiTestEnvironment(
            id="mapped-local",
            project_id="project",
            name="local",
            address="http://local.test/a/",
            updated_by="owner",
        )
    )
    db.add(Project(id="foreign", name="foreign", owner_id="owner"))
    db.flush()
    db.add(
        Case(
            id="foreign-case",
            project_id="foreign",
            name="foreign case",
            case_code="FOREIGN",
            type="api",
            is_automated=True,
            steps=[],
            created_by="owner",
        )
    )
    db.add(
        ApiDefinition(
            id="foreign-def",
            project_id="foreign",
            name="foreign",
            protocol="HTTP",
            path="endpoint",
            parameters={},
            updated_by="owner",
        )
    )
    db.add(
        ApiTestEnvironment(
            id="mapped-foreign",
            project_id="foreign",
            name="foreign",
            address="http://foreign.test/b/",
            updated_by="owner",
        )
    )
    db.flush()
    db.add(
        NativeCaseConfig(
            case_id="foreign-case",
            state="PROCESSING",
            api_definition_id="foreign-def",
            parameters={"request": {}},
            updated_by="owner",
        )
    )
    db.commit()
    actor = db.get(User, "owner")
    group = save_group(
        db, actor, [("project", "mapped-local"), ("foreign", "mapped-foreign")]
    )
    plan = db.get(Plan, "plan")
    for cid in ["case-0", "foreign-case"]:
        save_node(
            db,
            plan,
            {"name": cid, "nodeType": "case", "category": "api", "caseId": cid},
            source_project_id="foreign" if cid == "foreign-case" else None,
        )
    db.commit()
    store(db, "root:api", extended=False, requestEnvironmentGroupId=group.id)
    run = await start_plan_run(db, "plan", "owner", defer=True)
    items = (
        db.query(PlanRunItem)
        .filter_by(run_id=run.id)
        .order_by(PlanRunItem.sequence)
        .all()
    )
    requests = {
        i.suite_snapshot["caseIds"][0]: i.suite_snapshot["nativeCases"][0]["requests"][
            0
        ]["url"]
        for i in items
    }
    assert requests == {
        "case-0": "http://local.test/a/endpoint",
        "foreign-case": "http://foreign.test/b/endpoint",
    }
    assert all(
        i.suite_snapshot["executionConfig"]["requestEnvironmentGroupRevision"] == 1
        for i in items
    )
    original = deepcopy([i.suite_snapshot for i in items])
    db.get(ApiTestEnvironment, "mapped-local").address = "http://changed.test/"
    db.add(
        ApiTestEnvironment(
            id="new-local",
            project_id="project",
            name="new",
            address="http://new.test/",
            updated_by="owner",
        )
    )
    db.commit()
    save_group(
        db,
        actor,
        [("project", "new-local"), ("foreign", "mapped-foreign")],
        group.id,
        1,
    )
    db.expire_all()
    assert [i.suite_snapshot for i in items] == original


def test_crud_revision_revoke_disabled_cache_and_atomic_invalid_mapping(
    native_workspace,
):
    from database import SessionLocal
    from fastapi import HTTPException

    db, app, identity = native_workspace
    actor = db.get(User, "owner")
    group = save_group(db, actor, [("project", "native-env")])
    gid = group.id
    with pytest.raises(HTTPException) as stale:
        save_group(db, actor, [("project", "native-env")], gid, 0)
    assert stale.value.status_code == 409
    before = groups.catalog(db, actor, "project")["items"]
    with pytest.raises(HTTPException) as invalid:
        save_group(db, actor, [("project", "missing-env")], gid, 1)
    assert invalid.value.status_code == 422
    assert groups.catalog(db, actor, "project")["items"] == before
    assert "address" not in str(groups.source_catalog(db, actor, "project"))
    with SessionLocal() as fresh:
        fresh.query(User).filter_by(id="owner").update({"status": False})
        fresh.commit()
    with pytest.raises(HTTPException) as disabled:
        save_group(db, actor, [("project", "native-env")], gid, 1)
    assert disabled.value.status_code == 403


@pytest.mark.asyncio
async def test_write_response_keeps_revision_of_its_own_write(
    native_workspace, monkeypatch
):
    import httpx
    from database import SessionLocal
    from api.v1.request_environment_group import router

    db, app, identity = native_workspace
    app.include_router(router, prefix="/groups")
    original_commit = db.commit
    fired = False

    def raced_commit():
        nonlocal fired
        original_commit()
        if not fired:
            fired = True
            with SessionLocal() as fresh:
                row = fresh.query(RequestEnvironmentGroup).one()
                row.revision = 2
                row.description = "concurrent update"
                fresh.commit()

    monkeypatch.setattr(db, "commit", raced_commit)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as c:
        response = await c.post(
            "/groups/projects/project/request-environment-groups",
            json={
                "name": "first",
                "expectedRevision": 0,
                "mappings": [{"projectId": "project", "environmentId": "native-env"}],
            },
        )
        assert response.status_code == 200, response.text
        assert response.json()["data"]["revision"] == 1, response.text


@pytest.mark.asyncio
async def test_selected_suite_entry_honors_configured_environment_group(
    native_workspace,
):
    from test_native_http_execution import configure
    from test_plan_execution_configuration import store
    from services.plan_orchestration import start_plan_run
    from models.plan_orchestration import PlanRunItem

    db, app, identity = native_workspace
    configure(db)
    db.add(
        ApiTestEnvironment(
            id="mapped",
            project_id="project",
            name="mapped",
            address="http://selected.test/",
            updated_by="owner",
        )
    )
    db.commit()
    group = save_group(db, db.get(User, "owner"), [("project", "mapped")])
    store(db, "root:api", extended=False, requestEnvironmentGroupId=group.id)
    run = await start_plan_run(db, "plan", "owner", suite_ids=["suite-0"], defer=True)
    item = db.query(PlanRunItem).filter_by(run_id=run.id).one()
    url = item.suite_snapshot["nativeCases"][0]["requests"][0]["url"]
    assert url == "http://selected.test/endpoint", url
    assert (
        item.suite_snapshot["executionConfig"]["requestEnvironmentGroupRevision"] == 1
    )
    assert {case["id"] for case in run.case_snapshot} == {"case-0"}


def test_delete_reference_guard_and_invalid_mappings_are_atomic(native_workspace):
    from fastapi import HTTPException
    from test_plan_execution_configuration import store

    db, app, _ = native_workspace
    actor = db.get(User, "owner")
    group = save_group(db, actor, [("project", "native-env")])
    gid = group.id
    store(db, "root:api", extended=False, requestEnvironmentGroupId=gid)
    before = groups.catalog(db, actor, "project")["items"]
    with pytest.raises(HTTPException) as blocked:
        transact(db, lambda: groups.remove(db, actor, "project", gid, 1))
    assert blocked.value.status_code == 409
    assert groups.catalog(db, actor, "project")["items"] == before
    assert db.query(RequestEnvironmentMapping).filter_by(group_id=gid).count() == 1


def test_current_source_permission_revocation_rejects_resolve_and_update(
    native_workspace,
):
    from database import SessionLocal
    from fastapi import HTTPException

    db, app, _ = native_workspace
    db.add(Project(id="foreign", name="foreign", owner_id="stranger"))
    db.flush()
    db.add(ProjectMember(project_id="foreign", user_id="owner", role="tester"))
    db.add(
        ApiTestEnvironment(
            id="foreign-env",
            project_id="foreign",
            name="foreign",
            address="http://foreign.test/",
            updated_by="stranger",
        )
    )
    db.commit()
    actor = db.get(User, "owner")
    group = save_group(
        db, actor, [("project", "native-env"), ("foreign", "foreign-env")]
    )
    gid = group.id
    assert (
        groups.resolve(db, actor, "project", "foreign", gid)["environmentId"]
        == "foreign-env"
    )
    db.rollback()
    with SessionLocal() as fresh:
        fresh.query(ProjectMember).filter_by(
            project_id="foreign", user_id="owner"
        ).delete()
        fresh.commit()
    with pytest.raises(HTTPException) as revoked:
        groups.resolve(db, actor, "project", "foreign", gid)
    db.rollback()
    assert revoked.value.status_code == 403
    with pytest.raises(HTTPException) as revoked_update:
        save_group(
            db, actor, [("project", "native-env"), ("foreign", "foreign-env")], gid, 1
        )
    assert revoked_update.value.status_code == 403
    assert db.get(RequestEnvironmentGroup, gid).revision == 1


@pytest.mark.asyncio
async def test_native_range_freezes_group_mapping_without_external_dispatch(
    native_workspace,
):
    from test_native_http_execution import configure
    from test_plan_execution_configuration import store
    from test_plan_native_run import client, ids, execute, body
    from models.plan_orchestration import PlanRunItem

    db, app, _ = native_workspace
    configure(db)
    db.add(
        ApiTestEnvironment(
            id="mapped",
            project_id="project",
            name="mapped",
            address="http://range.test/",
            updated_by="owner",
        )
    )
    db.commit()
    group = save_group(db, db.get(User, "owner"), [("project", "mapped")])
    store(db, "root:api", extended=False, requestEnvironmentGroupId=group.id)
    async with client(app) as http:
        response = await execute(http, body(selectIds=await ids(http)))
        assert response.status_code == 200, response.text
        item = (
            db.query(PlanRunItem).filter_by(run_id=response.json()["data"]["id"]).one()
        )
        assert (
            item.suite_snapshot["nativeCases"][0]["requests"][0]["url"]
            == "http://range.test/endpoint"
        )
        assert (
            item.suite_snapshot["executionConfig"]["requestEnvironmentGroupRevision"]
            == 1
        )


@pytest.mark.asyncio
async def test_missing_source_mapping_leaves_no_partial_batch_or_tasks(
    native_workspace,
):
    import httpx
    from test_native_http_execution import configure
    from test_plan_execution_configuration import store
    from models.plan_orchestration import PlanRun, PlanRunItem
    from models.task_queue import TaskQueue

    db, app, _ = native_workspace
    configure(db)
    db.add(Project(id="foreign", name="foreign", owner_id="owner"))
    db.flush()
    db.add(
        ApiTestEnvironment(
            id="foreign-env",
            project_id="foreign",
            name="foreign",
            address="http://foreign.test/",
            updated_by="owner",
        )
    )
    db.commit()
    group = save_group(db, db.get(User, "owner"), [("foreign", "foreign-env")])
    store(db, "root:api", extended=False, requestEnvironmentGroupId=group.id)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as c:
        response = await c.post("/test-plans/plan/execute", json={})
        assert response.status_code == 409, response.text
    db.rollback()
    assert (
        db.query(PlanRun).count() == 0
        and db.query(PlanRunItem).count() == 0
        and db.query(TaskQueue).count() == 0
    )
    assert db.get(Plan, "plan").status != "running"


def test_schemas_are_strict_and_old_config_is_compatible():
    from pydantic import ValidationError
    from services.plan_execution_config import ExecutionConfig

    base = dict(
        name="group",
        expectedRevision=0,
        mappings=[dict(projectId="project", environmentId="env")],
    )
    for delta in [
        dict(expectedRevision=True),
        dict(unexpected="x"),
        dict(name="   "),
        dict(mappings=base["mappings"] * 2),
        dict(
            mappings=[dict(projectId="project", environmentId="env", address="secret")]
        ),
    ]:
        with pytest.raises(ValidationError):
            EnvironmentGroupInput.model_validate(dict(base, **delta))
    assert (
        ExecutionConfig.model_validate(
            dict(requestEnvironmentId="legacy-env")
        ).requestEnvironmentGroupId
        == "NONE"
    )
    with pytest.raises(ValidationError):
        ExecutionConfig.model_validate(
            dict(requestEnvironmentId="legacy-env", requestEnvironmentGroupId="group")
        )


def test_dialect_delete_guard_compiles_current_json_read(native_workspace, monkeypatch):
    from sqlalchemy.orm import Query
    from sqlalchemy.dialects import postgresql, mysql, sqlite
    from fastapi import HTTPException
    from test_plan_execution_configuration import store

    db, app, _ = native_workspace
    actor = db.get(User, "owner")
    group = save_group(db, actor, [("project", "native-env")])
    gid = group.id
    store(db, "root:api", extended=False, requestEnvironmentGroupId=gid)
    original_first = Query.first
    captured = []

    def first(query):
        text = str(query.statement)
        if "plan_execution_configs" in text:
            captured.append(query.statement)
        return original_first(query)

    monkeypatch.setattr(Query, "first", first)
    with pytest.raises(HTTPException):
        transact(db, lambda: groups.remove(db, actor, "project", gid, 1))
    assert len(captured) == 1
    for dialect in [postgresql.dialect(), mysql.dialect(), sqlite.dialect()]:
        sql = str(
            captured[0].compile(dialect=dialect, compile_kwargs={"literal_binds": True})
        )
        assert "requestEnvironmentGroupId" in sql
        if dialect.name != "sqlite":
            assert "FOR UPDATE" in sql


@pytest.mark.asyncio
async def test_http_crud_pagination_readonly_and_strict_mapping(native_workspace):
    import httpx
    from api.v1.request_environment_group import router

    db, app, identity = native_workspace
    app.include_router(router, prefix="/groups")
    base = "/groups/projects/project/request-environment-groups"
    create = dict(
        name="百分号%原样",
        description="draft",
        expectedRevision=0,
        mappings=[dict(projectId="project", environmentId="native-env")],
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as http:
        first = await http.post(base, json=create)
        assert first.status_code == 200, first.text
        gid = first.json()["data"]["id"]
        assert (
            await http.post(base, json={**create, "name": "second"})
        ).status_code == 200
        page = (await http.get(base, params=dict(page=1, size=1, search="%"))).json()[
            "data"
        ]
        assert (
            page["total"] == 1
            and len(page["items"]) == 1
            and page["canEdit"]
            and page["canDelete"]
        )
        assert page["items"][0]["id"] == gid and "address" not in str(page)
        assert (await http.get(base, params=dict(page=0))).status_code == 422
        assert (await http.get(base, params=dict(size=101))).status_code == 422
        bad = {
            **create,
            "expectedRevision": 1,
            "mappings": [dict(projectId="project", environmentId="missing")],
        }
        assert (await http.put(base + "/" + gid, json=bad)).status_code == 422
        assert db.get(RequestEnvironmentGroup, gid).revision == 1
        assert (
            await http.put(
                base + "/" + gid,
                json={**create, "expectedRevision": 1, "name": "renamed"},
            )
        ).json()["data"]["revision"] == 2
        assert (
            await http.put(base + "/" + gid, json={**create, "expectedRevision": 1})
        ).status_code == 409
        db.add(ProjectMember(project_id="project", user_id="stranger", role="viewer"))
        db.commit()
        identity["id"] = "stranger"
        readonly = (await http.get(base)).json()["data"]
        assert not readonly["canEdit"] and not readonly["canDelete"]
        assert (await http.get(base + "/source-environments")).status_code == 200
        assert (await http.post(base, json=create)).status_code == 403
        assert (
            await http.request("DELETE", base + "/" + gid, json={"expectedRevision": 2})
        ).status_code == 403
        identity["id"] = "owner"
        assert (
            await http.request("DELETE", base + "/" + gid, json={"expectedRevision": 1})
        ).status_code == 409
        assert (
            await http.request("DELETE", base + "/" + gid, json={"expectedRevision": 2})
        ).status_code == 200
        assert db.query(RequestEnvironmentMapping).filter_by(group_id=gid).count() == 0


@pytest.mark.asyncio
async def test_keyed_create_retry_never_duplicates_or_grants_later_revision(
    native_workspace,
):
    import httpx
    from api.v1.request_environment_group import router

    db, app, _ = native_workspace
    app.include_router(router, prefix="/groups")
    base = "/groups/projects/project/request-environment-groups"
    create = dict(
        name="keyed",
        requestId="original-create",
        expectedRevision=0,
        mappings=[dict(projectId="project", environmentId="native-env")],
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as http:
        first = (await http.post(base, json=create)).json()["data"]
        gid = first["id"]
        assert (await http.post(base, json=create)).json()["data"] == first
        update = {**create, "name": "later writer", "expectedRevision": 1}
        assert (await http.put(base + "/" + gid, json=update)).json()["data"][
            "revision"
        ] == 2
        replay = await http.post(base, json=create)
        assert replay.status_code == 200 and replay.json()["data"] == first
        assert db.query(RequestEnvironmentGroup).count() == 1
        assert db.get(RequestEnvironmentGroup, gid).name == "later writer"
        assert (
            await http.put(base + "/" + gid, json={**create, "expectedRevision": 1})
        ).status_code == 409
        assert (
            await http.post(base, json={**create, "name": "changed retry"})
        ).status_code == 409


@pytest.mark.asyncio
async def test_selected_suite_honors_collection_override_keeps_manual_and_excludes_unselected(
    native_workspace,
):
    from test_native_http_execution import configure
    from test_plan_execution_configuration import store
    from services.plan_tree import save_node
    from services.plan_orchestration import start_plan_run
    from models import PlanCaseRelation
    from models.plan_orchestration import PlanRunItem

    db, _, _ = native_workspace
    configure(db)
    actor = db.get(User, "owner")
    db.add(
        ApiTestEnvironment(
            id="mapped-collection",
            project_id="project",
            name="mapped",
            address="http://collection.test/",
            updated_by="owner",
        )
    )
    db.commit()
    root_group = save_group(db, actor, [("project", "native-env")])
    root_id = root_group.id
    child_group = save_group(db, actor, [("project", "mapped-collection")])
    child_id = child_group.id
    point = save_node(
        db,
        db.get(Plan, "plan"),
        dict(name="selected collection", nodeType="point", category="api"),
    )
    db.query(PlanCaseRelation).filter_by(
        plan_id="plan", case_id="case-0"
    ).one().collection_id = point.id
    db.add(PlanCaseRelation(plan_id="plan", case_id="case-2", execution_order=2))
    db.commit()
    store(db, "root:api", extended=False, requestEnvironmentGroupId=root_id)
    store(
        db, "node:api:" + point.id, extended=False, requestEnvironmentGroupId=child_id
    )
    run = await start_plan_run(db, "plan", "owner", suite_ids=["suite-0"], defer=True)
    item = db.query(PlanRunItem).filter_by(run_id=run.id).one()
    assert (
        item.suite_snapshot["nativeCases"][0]["requests"][0]["url"]
        == "http://collection.test/endpoint"
    )
    assert (
        item.suite_snapshot["executionConfig"]["requestEnvironmentGroupId"] == child_id
    )
    assert {c["id"] for c in run.case_snapshot} == {"case-0", "case-2"}
    assert item.suite_snapshot["testSet"]["id"] == point.id


@pytest.mark.asyncio
async def test_selected_configured_generic_command_rejected_before_queue(
    native_workspace,
):
    from test_plan_execution_configuration import store
    from models import TestSuite as Suite
    from models.plan_orchestration import PlanRun, PlanRunItem
    from models.task_queue import TaskQueue
    import httpx

    db, app, _ = native_workspace
    db.query(NativeCaseConfig).filter_by(case_id="case-0").delete()
    db.get(Suite, "suite-0").execution_command = "python execute_all.py"
    db.commit()
    store(db, "root:api", extended=False, executionMode="parallel")
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as http:
        response = await http.post(
            "/test-plans/plan/execute", json={"suiteIds": ["suite-0"]}
        )
        assert response.status_code == 409, response.text
    assert (
        db.query(PlanRun).count() == 0
        and db.query(PlanRunItem).count() == 0
        and db.query(TaskQueue).count() == 0
    )


def test_additive_migration_preserves_existing_rows_and_is_idempotent(tmp_path):
    from sqlalchemy import create_engine, text, inspect
    from migrations.add_request_environment_groups import upgrade

    engine = create_engine("sqlite:///" + str(tmp_path / "existing.sqlite"))
    with engine.begin() as connection:
        for table in ["users", "projects", "native_api_environments"]:
            connection.execute(
                text(f"CREATE TABLE {table} (id VARCHAR(36) PRIMARY KEY)")
            )
            connection.execute(text(f"INSERT INTO {table}(id) VALUES ('retained')"))
    assert upgrade(engine) == [
        "request_environment_groups",
        "request_environment_group_mappings",
    ]
    assert set(inspect(engine).get_table_names()) == {
        "users",
        "projects",
        "native_api_environments",
    }
    upgrade(engine, apply=True)
    assert upgrade(engine, apply=True) == []
    assert set(inspect(engine).get_table_names()) == {
        "users",
        "projects",
        "native_api_environments",
        "request_environment_groups",
        "request_environment_group_mappings",
    }
    with engine.connect() as connection:
        for table in ["users", "projects", "native_api_environments"]:
            assert (
                connection.execute(text(f"SELECT id FROM {table}")).scalar_one()
                == "retained"
            )
    engine.dispose()
