"""Independent Node pools on synthetic databases; no new Agent or service."""

from copy import deepcopy
import httpx
import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from test_plan_native_workspace import native_workspace
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from models import (
    User,
    Project,
    Environment,
    Permission,
    Role,
    UserRole,
    RolePermission,
)
from models.global_resource_pool import (
    GlobalResourcePool as Pool,
    GlobalResourcePoolMember as Member,
    GlobalResourcePoolProject as Scope,
)
from schemas.global_resource_pool import PoolInput, PoolEnable
from services import global_resource_pool as pools
from api.v1.case_governance import transact


@pytest.fixture
def pool_lab(native_workspace):
    db, app, identity = native_workspace
    permission = Permission(
        id="pool-management",
        code="system:manage",
        name="Synthetic pool authority",
        resource="system",
        action="manage",
    )
    role = Role(
        id="pool-manager", name="synthetic-pool-manager", display_name="Synthetic"
    )
    db.add_all([permission, role])
    db.flush()
    db.add_all(
        [
            UserRole(user_id="owner", role_id=role.id),
            RolePermission(role_id=role.id, permission_id=permission.id),
        ]
    )
    db.add(Project(id="unshared", name="Unshared", owner_id="stranger"))
    db.add(
        Environment(
            id="alternate",
            name="Alternate",
            status=True,
            is_online=True,
            max_concurrent_tasks=2,
            token="never-return-this-synthetic-token",
        )
    )
    db.commit()
    from api.v1.global_resource_pool import router

    app.include_router(router, prefix="/pools")
    return db, app, identity


def body(**values):
    defaults = dict(
        name="Shared Node pool",
        description="Synthetic",
        applications=["api", "scenario"],
        allProjects=False,
        projectIds=["project"],
        environmentIds=["node", "alternate"],
        expectedRevision=0,
        requestId="create-pool",
    )
    return {**defaults, **values}


def saved(db, user=None, **values):
    user = user or db.get(User, "owner")
    return transact(
        db, lambda: pools.save(db, user, PoolInput.model_validate(body(**values)))
    )


@pytest.mark.asyncio
async def test_http_crud_scopes_permissions_capacity_and_keyed_receipt(pool_lab):
    db, app, identity = pool_lab
    base = "/pools/resource-pools"
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as http:
        create = await http.post(base, json=body())
        assert create.status_code == 200, create.text
        receipt = create.json()["data"]
        pid = receipt["id"]
        assert (await http.post(base, json=body())).json()["data"] == receipt
        catalog = (await http.get(base)).json()["data"]
        entry = catalog["items"][0]
        assert catalog["canEdit"] and entry["capacity"] == dict(
            configured=5, online=5, running=0, available=5
        )
        assert "never-return" not in str(catalog) and "token" not in str(catalog)
        assert (await http.get(base + "/nodes", params={"size": 1})).json()["data"][
            "total"
        ] == 2
        identity["id"] = "stranger"
        assert (await http.get(base)).status_code == 403
        assert (await http.get(base, params={"projectId": "unshared"})).json()["data"][
            "total"
        ] == 0
        assert (await http.post(base, json=body())).status_code == 403
        assert (await http.get(base + "/nodes")).status_code == 403
        identity["id"] = "owner"
        edited = {**body(), "name": "Later edit", "expectedRevision": 1}
        assert (await http.put(base + "/" + pid, json=edited)).json()["data"][
            "revision"
        ] == 2
        assert (await http.post(base, json=body())).json()["data"] == receipt
        assert (await http.put(base + "/" + pid, json=edited)).status_code == 409
        assert (
            await http.post(base, json={**body(), "name": "different retry"})
        ).status_code == 409
        assert (
            await http.put(
                base + "/" + pid + "/enabled",
                json={"enabled": False, "expectedRevision": 2},
            )
        ).json()["data"]["revision"] == 3
        assert (await http.get(base)).json()["data"]["items"][0]["capacity"][
            "available"
        ] == 0
        assert (
            await http.request("DELETE", base + "/" + pid, json={"expectedRevision": 2})
        ).status_code == 409
        assert (
            await http.request("DELETE", base + "/" + pid, json={"expectedRevision": 3})
        ).status_code == 200
    assert (
        db.query(Pool).count()
        == db.query(Member).count()
        == db.query(Scope).count()
        == 0
    )


@pytest.mark.asyncio
async def test_frozen_global_members_revision_and_dispatch_survive_pool_edit(
    pool_lab, monkeypatch
):
    from test_native_http_execution import configure
    from test_plan_execution_configuration import store
    from services.plan_orchestration import start_plan_run, advance_plan_runs
    from models.plan_orchestration import PlanRunItem
    from services.plan_collaboration import enriched_report

    db, _, _ = pool_lab
    configure(db)
    pid = saved(db)["id"]
    store(
        db,
        "root:api",
        extended=False,
        testResourcePoolId=pid,
        testResourcePoolScope="global",
    )
    run = await start_plan_run(db, "plan", "owner", suite_ids=["suite-0"], defer=True)
    item = db.query(PlanRunItem).filter_by(run_id=run.id).one()
    snapshot = deepcopy(item.suite_snapshot)
    assert (
        snapshot["executionConfig"]["testResourcePoolScope"] == "global"
        and snapshot["executionConfig"]["testResourcePoolRevision"] == 1
    )
    assert snapshot["resourcePool"] == ["node", "alternate"]
    input = PoolInput.model_validate(
        {**body(), "expectedRevision": 1, "environmentIds": ["alternate"]}
    )
    transact(db, lambda: pools.save(db, db.get(User, "owner"), input, pid))
    transact(
        db,
        lambda: pools.set_enabled(
            db,
            db.get(User, "owner"),
            pid,
            PoolEnable(enabled=False, expectedRevision=2),
        ),
    )
    db.expire_all()
    assert item.suite_snapshot == snapshot
    with pytest.raises(HTTPException):
        transact(db, lambda: pools.remove(db, db.get(User, "owner"), pid, 3))
    monkeypatch.setattr(
        pools,
        "resolve",
        lambda *args: pytest.fail("Dispatch must not re-read current global pool"),
    )
    from services.plan_orchestration import release_plan_run

    release_plan_run(db, run)
    db.commit()
    await advance_plan_runs(db)
    report = enriched_report(db, run)["reportDetails"]["configuration"]["items"][0]
    assert report["executionConfig"]["testResourcePoolRevision"] == 1 and report[
        "resourcePool"
    ] == ["node", "alternate"]


def test_current_authority_invalid_members_and_scope_are_atomic(pool_lab):
    from database import SessionLocal

    db, _, _ = pool_lab
    user = db.get(User, "owner")
    pid = saved(db)["id"]
    original = pools.catalog(db, user)["items"][0]
    invalid = PoolInput.model_validate(
        {**body(), "expectedRevision": 1, "environmentIds": ["node", "missing"]}
    )
    with pytest.raises(HTTPException) as invalid_member:
        transact(db, lambda: pools.save(db, user, invalid, pid))
    assert (
        invalid_member.value.status_code == 422
        and pools.catalog(db, user)["items"][0] == original
    )
    # End the catalog request before simulating a permission change from
    # another connection. Its current-read locks live until request teardown.
    db.rollback()
    with SessionLocal() as fresh:
        fresh.query(UserRole).filter_by(user_id="owner").delete()
        fresh.commit()
    with pytest.raises(HTTPException) as revoked:
        transact(
            db,
            lambda: pools.save(
                db,
                user,
                PoolInput.model_validate({**body(), "expectedRevision": 1}),
                pid,
            ),
        )
    assert revoked.value.status_code == 403 and db.get(Pool, pid).revision == 1
    assert {x["id"] for x in pools.choices(db, "project")} == {pid}
    assert pools.choices(db, "unshared") == []


@pytest.mark.parametrize(
    "invalid",
    [
        {"enabled": 1},
        {"type": "Kubernetes"},
        {"projectIds": []},
        {"allProjects": True},
        {"environmentIds": ["node", "node"]},
        {"applications": ["api", "api"]},
        {"expectedRevision": True},
        {"extra": "x"},
    ],
)
def test_strict_pool_input_rejects_unsupported_or_ambiguous_scope(invalid):
    with pytest.raises(ValidationError):
        PoolInput.model_validate({**body(), **invalid})


@pytest.mark.parametrize(
    "failure", ["disabled", "other-project", "other-application", "missing-member"]
)
@pytest.mark.asyncio
async def test_invalid_pool_is_refused_before_new_queue(pool_lab, failure):
    from test_native_http_execution import configure
    from test_plan_execution_configuration import store
    from models.plan_orchestration import PlanRun, PlanRunItem
    from models.task_queue import TaskQueue

    db, app, _ = pool_lab
    configure(db)
    pid = saved(db)["id"]
    store(
        db,
        "root:api",
        extended=False,
        testResourcePoolId=pid,
        testResourcePoolScope="global",
    )
    row = db.get(Pool, pid)
    if failure == "disabled":
        row.enabled = False
    if failure == "other-application":
        row.api_enabled = False
    if failure == "other-project":
        db.query(Scope).filter_by(pool_id=pid).delete()
    if failure == "missing-member":
        db.query(Member).filter_by(pool_id=pid).delete()
    db.commit()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as http:
        response = await http.post(
            "/test-plans/plan/execute", json={"suiteIds": ["suite-0"]}
        )
        assert response.status_code == 409, response.text
    assert (
        db.query(PlanRun).count()
        == db.query(PlanRunItem).count()
        == db.query(TaskQueue).count()
        == 0
    )


def test_additive_pool_migration_preview_idempotence_and_legacy_rows(tmp_path):
    from sqlalchemy import create_engine, inspect, text
    from migrations.add_global_resource_pools import upgrade

    engine = create_engine("sqlite:///" + str(tmp_path / "legacy.sqlite"))
    with engine.begin() as connection:
        for table in ["users", "projects", "environments"]:
            connection.execute(
                text(f"CREATE TABLE {table}(id VARCHAR(36) PRIMARY KEY)")
            )
            connection.execute(text(f"INSERT INTO {table} VALUES('retained')"))
    assert len(upgrade(engine)) == 3 and len(inspect(engine).get_table_names()) == 3
    upgrade(engine, apply=True)
    assert upgrade(engine, apply=True) == []
    with engine.connect() as connection:
        for table in ["users", "projects", "environments"]:
            assert (
                connection.execute(text(f"SELECT id FROM {table}")).scalar_one()
                == "retained"
            )
    engine.dispose()


@pytest.mark.asyncio
@pytest.mark.parametrize("entrance", ["whole-plan", "selected-suite", "native-range"])
async def test_all_three_execution_entrances_freeze_global_pool(pool_lab, entrance):
    from test_native_http_execution import configure
    from test_plan_execution_configuration import store
    from models.plan_orchestration import PlanRun, PlanRunItem
    from services.plan_orchestration import start_plan_run

    db, app, _ = pool_lab
    configure(db)
    pid = saved(db)["id"]
    store(
        db,
        "root:api",
        extended=False,
        testResourcePoolScope="global",
        testResourcePoolId=pid,
    )
    if entrance == "native-range":
        from test_plan_native_run import ids, body as range_body, execute

        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as http:
            response = await execute(http, range_body(selectIds=await ids(http)))
            assert response.status_code == 200, response.text
            run = db.get(PlanRun, response.json()["data"]["id"])
    else:
        run = await start_plan_run(
            db,
            "plan",
            "owner",
            suite_ids=["suite-0"] if entrance == "selected-suite" else None,
            defer=True,
        )
    items = db.query(PlanRunItem).filter_by(run_id=run.id).all()
    api_items = [i for i in items if i.suite_snapshot["category"] == "api"]
    assert api_items
    for item in api_items:
        assert item.suite_snapshot["resourcePool"] == ["node", "alternate"]
        frozen = item.suite_snapshot["executionConfig"]
        assert (
            frozen["testResourcePoolScope"] == "global"
            and frozen["testResourcePoolId"] == pid
            and frozen["testResourcePoolRevision"] == 1
        )


def test_global_scope_default_is_rejected_and_legacy_scope_remains_project():
    from services.plan_execution_config import ExecutionConfig

    with pytest.raises(ValidationError):
        ExecutionConfig(testResourcePoolScope="global")
    assert (
        ExecutionConfig(testResourcePoolId="legacy").testResourcePoolScope == "project"
    )
