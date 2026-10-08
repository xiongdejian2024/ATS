"""Independent HTTP regression cases promoted after review; synthetic fixtures."""

import pytest
from conftest import isolated_database
from test_plan_orchestration import plan_lab
from test_plan_workspace import workspace_http
from test_plan_native_workspace import native_workspace
from test_global_resource_pools import pool_lab, saved
from models import User, Permission, ProjectPermission, ProjectMember
from models.plan_execution_config import PlanExecutionConfig
from models.plan_orchestration import PlanRun


def grant(db, action):
    code = "test_plan:" + action
    db.add(
        Permission(
            id="grant-" + action,
            code=code,
            name=code,
            resource="test_plan",
            action=action,
        )
    )
    db.flush()
    db.add(
        ProjectPermission(
            project_id="project", user_id="stranger", permission_id="grant-" + action
        )
    )
    db.commit()


def revoke(action):
    from database import SessionLocal

    with SessionLocal() as fresh:
        fresh.query(ProjectPermission).filter_by(
            project_id="project", user_id="stranger", permission_id="grant-" + action
        ).delete()
        fresh.commit()


@pytest.mark.asyncio
async def test_revoke_update_after_api_precheck_does_not_commit_global_reference(
    pool_lab, monkeypatch
):
    import httpx
    from services import plan_execution_config as configuration

    db, app, identity = pool_lab
    pid = saved(db)["id"]
    db.add(ProjectMember(project_id="project", user_id="stranger", role="tester"))
    db.commit()
    grant(db, "update")
    original = configuration.lock_project
    fired = False

    def locked(db, pid):
        nonlocal fired
        if not fired:
            fired = True
            revoke("update")
        return original(db, pid)

    monkeypatch.setattr(configuration, "lock_project", locked)
    identity["id"] = "stranger"
    body = dict(
        config=dict(
            extended=False, testResourcePoolScope="global", testResourcePoolId=pid
        ),
        expectedRevision=0,
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as http:
        response = await http.put(
            "/orchestration/plans/plan/execution-configurations/root:api", json=body
        )
        assert response.status_code == 403, response.text
    db.rollback()
    assert db.query(PlanExecutionConfig).count() == 0


@pytest.mark.asyncio
async def test_revoke_execute_after_api_precheck_does_not_create_frozen_global_run(
    pool_lab, monkeypatch
):
    import httpx
    from services import plan_candidate_project
    from test_native_http_execution import configure
    from test_plan_execution_configuration import store

    db, app, identity = pool_lab
    configure(db)
    pid = saved(db)["id"]
    store(
        db,
        "root:api",
        extended=False,
        testResourcePoolScope="global",
        testResourcePoolId=pid,
    )
    db.add(ProjectMember(project_id="project", user_id="stranger", role="tester"))
    db.commit()
    grant(db, "execute")
    original = plan_candidate_project.lock_run_sources
    fired = False

    def locked(db, planid, **kwargs):
        nonlocal fired
        if not fired:
            fired = True
            revoke("execute")
        return original(db, planid, **kwargs)

    monkeypatch.setattr(plan_candidate_project, "lock_run_sources", locked)
    identity["id"] = "stranger"
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as http:
        response = await http.post(
            "/test-plans/plan/execute", json={"suiteIds": ["suite-0"]}
        )
        assert response.status_code == 403, response.text
    db.rollback()
    assert db.query(PlanRun).count() == 0


@pytest.mark.asyncio
async def test_pool_catalog_exact_project_scope_no_unshared_project_or_secrets(
    pool_lab,
):
    import httpx
    from services import global_resource_pool as pools
    from api.v1.case_governance import transact
    from schemas.global_resource_pool import PoolInput
    from test_global_resource_pools import body

    db, app, identity = pool_lab
    restricted = saved(db)["id"]
    public = transact(
        db,
        lambda: pools.save(
            db,
            db.get(User, "owner"),
            PoolInput.model_validate(
                {
                    **body(),
                    "name": "all",
                    "requestId": "all",
                    "allProjects": True,
                    "projectIds": [],
                }
            ),
        ),
    )["id"]
    db.add(ProjectMember(project_id="project", user_id="stranger", role="tester"))
    db.commit()
    identity["id"] = "stranger"
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as http:
        own = await http.get("/pools/resource-pools", params={"projectId": "unshared"})
        assert own.status_code == 200, own.text
        data = own.json()["data"]
        assert {p["id"] for p in data["items"]} == {public}
        assert not data["canEdit"] and not data["canDelete"]
        assert all(p["projectIds"] == [] for p in data["items"])
        assert "never-return" not in own.text and "token" not in own.text
        other = await http.get("/pools/resource-pools", params={"projectId": "project"})
        assert {p["id"] for p in other.json()["data"]["items"]} == {restricted, public}
        assert (await http.get("/pools/resource-pools/nodes")).status_code == 403
        assert (
            await http.request(
                "DELETE",
                "/pools/resource-pools/" + public,
                json={"expectedRevision": 1},
            )
        ).status_code == 403


def test_pool_application_current_member_order_and_disabled_cache_are_safe(pool_lab):
    from database import SessionLocal
    from fastapi import HTTPException
    from services import global_resource_pool as pools
    from models import Environment
    from test_global_resource_pools import body
    from schemas.global_resource_pool import PoolInput
    from api.v1.case_governance import transact

    db, app, identity = pool_lab
    pid = transact(
        db,
        lambda: pools.save(
            db,
            db.get(User, "owner"),
            PoolInput.model_validate(
                {
                    **body(),
                    "applications": ["api"],
                    "environmentIds": ["alternate", "node"],
                }
            ),
        ),
    )["id"]
    assert pools.resolve(db, "project", "api", pid)[1] == ["alternate", "node"]
    with pytest.raises(HTTPException) as wrong_application:
        pools.resolve(db, "project", "scenario", pid)
    assert wrong_application.value.status_code == 409
    db.rollback()
    cached = db.get(Environment, "node")
    assert cached.status
    with SessionLocal() as fresh:
        fresh.query(Environment).filter_by(id="node").update({"status": False})
        fresh.commit()
    with pytest.raises(HTTPException) as invalid:
        transact(
            db,
            lambda: pools.save(
                db,
                db.get(User, "owner"),
                PoolInput.model_validate({**body(), "expectedRevision": 1}),
                pid,
            ),
        )
    assert invalid.value.status_code == 422
    pool, members = pools.resolve(db, "project", "api", pid)
    assert pool.revision == 1 and members == ["alternate", "node"]


@pytest.mark.asyncio
@pytest.mark.parametrize("foreign_keys", [True, False])
async def test_existing_node_delete_used_by_global_pool_returns_conflict_without_damage(
    pool_lab, foreign_keys
):
    import httpx
    from sqlalchemy import text
    from api.v1.environments import router
    from models import Environment
    from models.global_resource_pool import GlobalResourcePool, GlobalResourcePoolMember

    db, app, identity = pool_lab
    saved(db)
    app.include_router(router, prefix="/env")
    if db.bind.dialect.name == "sqlite":
        db.execute(text("PRAGMA foreign_keys=" + ("ON" if foreign_keys else "OFF")))
        db.commit()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app, raise_app_exceptions=False),
        base_url="http://test",
    ) as http:
        response = await http.delete("/env/alternate")
        assert response.status_code == 409, response.text
    db.rollback()
    assert db.get(Environment, "alternate") is not None
    assert (
        db.query(GlobalResourcePool).count() == 1
        and db.query(GlobalResourcePoolMember).count() == 2
    )


@pytest.mark.asyncio
async def test_pool_delete_ignores_configuration_for_deleted_plan_on_supported_sqlite(
    pool_lab,
):
    import httpx
    from test_plan_execution_configuration import store
    from models import TestPlan as Plan
    from models.global_resource_pool import GlobalResourcePool

    db, app, identity = pool_lab
    pid = saved(db)["id"]
    store(
        db,
        "root:api",
        extended=False,
        testResourcePoolScope="global",
        testResourcePoolId=pid,
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as http:
        removed = await http.delete("/test-plans/plan")
        assert removed.status_code == 200, removed.text
        assert db.get(Plan, "plan") is None
        response = await http.request(
            "DELETE", "/pools/resource-pools/" + pid, json={"expectedRevision": 1}
        )
        assert response.status_code == 200, response.text
    assert db.get(GlobalResourcePool, pid) is None
