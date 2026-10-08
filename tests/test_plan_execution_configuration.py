"""隔离数据库验证完整继承、真实资源池和分类停止范围，不连接台架。"""

from copy import deepcopy
import httpx
import pytest
from pydantic import ValidationError
from models import TestPlan as Plan, TestCase as Case, User, Environment
from models.native_case import ApiTestEnvironment, NativeCaseConfig
from models.plan_orchestration import PlanRunItem
from services.plan_execution_config import (
    ExecutionConfig,
    ConfigSave,
    PoolSave,
    save,
    save_pool,
    ConfigurationTree,
)
from services.plan_orchestration import get_policy, start_plan_run, advance_plan_runs
from services.plan_tree import save_node, nodes
from test_native_http_execution import native_workspace, configure
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab, finish


@pytest.mark.parametrize(
    "invalid",
    [
        {"retryTimes": 0},
        {"retryTimes": 11},
        {"retryTimes": True},
        {"retryTimes": 1.1},
        {"retryInterval": -1},
        {"retryInterval": True},
        {"retryOnFailure": 1},
        {"extra": True},
    ],
)
def test_strict_configuration_rejects_invalid_retry(invalid):
    with pytest.raises(ValidationError):
        ExecutionConfig.model_validate(invalid)


def store(db, scope, **fields):
    plan = db.get(Plan, "plan")
    tree = ConfigurationTree(db, plan, get_policy(db, plan.id), nodes(db, plan.id))
    current = tree.data(scope)
    save(
        db,
        plan,
        scope,
        ConfigSave(
            config=ExecutionConfig(**{**current["config"], **fields}),
            expectedRevision=current["revision"],
        ),
    )
    db.commit()


@pytest.mark.asyncio
async def test_catalog_dynamic_inheritance_overrides_versions_and_project_access(
    native_workspace,
):
    db, app, identity = native_workspace
    configure(db)
    plan = db.get(Plan, "plan")
    point = save_node(db, plan, dict(name="API测试集", category="api"))
    db.commit()
    base = "/orchestration/plans/plan"
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        result = await client.post(
            base + "/resource-pools",
            json=dict(name="自建软件池", environmentIds=["node"], expectedRevision=0),
        )
        assert result.status_code == 200, result.text
        pool = result.json()["data"]["pools"][0]
        config = ExecutionConfig(
            extended=False,
            testResourcePoolId=pool["id"],
            requestEnvironmentId="native-env",
            executionMode="parallel",
            retryOnFailure=True,
            retryTimes=2,
            retryInterval=100,
        ).model_dump()
        result = await client.put(
            base + "/execution-configurations/root:api",
            json=dict(config=config, expectedRevision=0),
        )
        assert result.status_code == 200, result.text
        scope = f"node:api:{point.id}"
        inherited = result.json()["data"]["configurations"][scope]
        assert inherited["revision"] == 0 and inherited["effectiveConfig"] == dict(
            config, extended=True
        )
        config.update(retryTimes=3, requestEnvironmentId="NONE")
        result = await client.put(
            base + "/execution-configurations/root:api",
            json=dict(config=config, expectedRevision=1),
        )
        assert result.json()["data"]["configurations"][scope][
            "effectiveConfig"
        ] == dict(config, extended=True)
        assert (
            await client.put(
                base + "/execution-configurations/root:api",
                json=dict(config=config, expectedRevision=1),
            )
        ).status_code == 409
        child = dict(
            config, extended=False, retryOnFailure=False, executionMode="serial"
        )
        result = await client.put(
            base + f"/execution-configurations/{scope}",
            json=dict(
                config=child,
                expectedRevision=0,
                name="单独配置",
                expectedName="API测试集",
            ),
        )
        assert result.status_code == 200
        assert db.get(type(point), point.id).name == "单独配置"
        assert (
            result.json()["data"]["configurations"][scope]["effectiveConfig"] == child
        )
        config["executionMode"] = "serial"
        await client.put(
            base + "/execution-configurations/root:api",
            json=dict(config=config, expectedRevision=2),
        )
        result = await client.get(base + "/execution-configurations")
        assert (
            result.json()["data"]["configurations"][scope]["effectiveConfig"] == child
        )
        # 脏名称的条件保存不能覆盖其他页面已提交的名称，也不能推进配置版本。
        assert (
            await client.put(
                base + f"/execution-configurations/{scope}",
                json=dict(
                    config=child,
                    expectedRevision=1,
                    name="覆盖名称",
                    expectedName="API测试集",
                ),
            )
        ).status_code == 409
        identity["id"] = "stranger"
        assert (await client.get(base + "/execution-configurations")).status_code == 403
        assert (
            await client.post(
                base + "/resource-pools",
                json=dict(name="越权", environmentIds=["node"]),
            )
        ).status_code == 403


@pytest.mark.asyncio
async def test_resource_pool_and_target_environment_are_independent_frozen_inputs(
    native_workspace,
):
    db, _, _ = native_workspace
    configure(db)
    plan = db.get(Plan, "plan")
    db.add(
        Environment(
            id="software-node", name="另一个软件节点", status=True, is_online=True
        )
    )
    db.add(
        ApiTestEnvironment(
            id="second-target",
            project_id="project",
            name="第二请求环境",
            address="http://127.0.0.1:54321/alternate/",
            updated_by="owner",
        )
    )
    db.commit()
    pool = save_pool(
        db, plan, PoolSave(name="独立执行池", environmentIds=["software-node"])
    )
    db.commit()
    store(
        db,
        "root:api",
        extended=False,
        testResourcePoolId=pool.id,
        requestEnvironmentId="second-target",
        retryOnFailure=True,
        retryTimes=2,
        retryInterval=100,
    )
    run = await start_plan_run(db, "plan", "owner")
    api_item = next(
        item
        for item in db.query(PlanRunItem).filter_by(run_id=run.id)
        if item.suite_snapshot["category"] == "api"
    )
    assert api_item.environment_id == "software-node"
    frozen = api_item.suite_snapshot["nativeCases"][0]
    assert frozen["requests"][0]["url"] == "http://127.0.0.1:54321/alternate/endpoint"
    assert frozen["retryTimes"] == 2 and frozen["retryInterval"] == 100
    assert api_item.suite_snapshot["resourcePool"] == ["software-node"]
    store(db, "root:api", retryTimes=5, requestEnvironmentId="NONE")
    pool.environment_ids = ["node"]
    db.commit()
    assert api_item.suite_snapshot["nativeCases"][0] == frozen
    assert api_item.suite_snapshot["resourcePool"] == ["software-node"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "root_stop,collection_stop,second_state,last_state",
    [(True, False, "running", "skipped"), (False, True, "skipped", "running")],
)
async def test_failure_stop_obeys_collection_and_category_boundaries(
    native_workspace, root_stop, collection_stop, second_state, last_state
):
    db, _, _ = native_workspace
    configure(db)
    plan = db.get(Plan, "plan")
    for index in (2, 3):
        db.add(
            Case(
                id=f"api-{index}",
                project_id="project",
                name=f"接口 {index}",
                case_code=f"API-{index}",
                type="api",
                is_automated=True,
                steps=[],
                created_by="owner",
            )
        )
        # No ORM relationship declares this dependency: persist the parent
        # before its native config so PostgreSQL's immediate FK is respected.
        db.flush()
        original = db.get(NativeCaseConfig, "case-0")
        db.add(
            NativeCaseConfig(
                case_id=f"api-{index}",
                state="DONE",
                environment_id=original.environment_id,
                api_definition_id=original.api_definition_id,
                parameters=deepcopy(original.parameters),
                updated_by="owner",
            )
        )
    db.flush()
    group_a = save_node(db, plan, dict(name="测试集A", category="api"))
    group_b = save_node(db, plan, dict(name="测试集B", category="api"))
    leaf_a = save_node(
        db,
        plan,
        dict(
            name="A第一条",
            nodeType="case",
            category="api",
            caseId="case-0",
            parentId=group_a.id,
        ),
    )
    leaf_b = save_node(
        db,
        plan,
        dict(
            name="A第二条",
            nodeType="case",
            category="api",
            caseId="api-2",
            parentId=group_a.id,
        ),
    )
    leaf_c = save_node(
        db,
        plan,
        dict(
            name="B用例",
            nodeType="case",
            category="api",
            caseId="api-3",
            parentId=group_b.id,
        ),
    )
    scene = save_node(
        db,
        plan,
        dict(name="独立场景", nodeType="case", category="scenario", caseId="case-1"),
    )
    db.commit()
    store(
        db, "root:api", extended=False, executionMode="serial", stopOnFailure=root_stop
    )
    store(
        db,
        f"node:api:{group_a.id}",
        extended=False,
        executionMode="serial",
        stopOnFailure=collection_stop,
    )
    run = await start_plan_run(db, "plan", "owner")
    await advance_plan_runs(db)
    items = {
        item.suite_snapshot["nodeId"]: item
        for item in db.query(PlanRunItem).filter_by(run_id=run.id)
    }
    assert items[leaf_a.id].status == items[scene.id].status == "running"
    finish(db, items[leaf_a.id], "failed")
    finish(db, items[scene.id])
    await advance_plan_runs(db)
    assert items[leaf_b.id].status == second_state
    if second_state == "running":
        finish(db, items[leaf_b.id])
        await advance_plan_runs(db)
    assert items[leaf_c.id].status == last_state
    if last_state == "running":
        finish(db, items[leaf_c.id])
        await advance_plan_runs(db)
    assert (
        run.status == "failed"
        and run.report["counts"]["skipped"] == 1
        and run.report["counts"]["passed"] == 2
    )


@pytest.mark.asyncio
async def test_clone_remaps_collection_configuration_and_node_delete_removes_it(
    native_workspace,
):
    from models.plan_execution_config import PlanExecutionConfig
    from models.plan_workspace import PlanNode
    from services.test_plan_service import TestPlanService

    db, app, unused = native_workspace
    configure(db)
    point = save_node(db, db.get(Plan, "plan"), dict(name="独立测试集", category="api"))
    db.commit()
    store(db, "root:api", extended=False, retryTimes=4)
    store(
        db,
        f"node:api:{point.id}",
        extended=False,
        executionMode="parallel",
        retryTimes=2,
    )
    cloned = TestPlanService.clone_plan(db, "plan", "project", "owner")
    cloned_point = db.query(PlanNode).filter_by(plan_id=cloned.id).one()
    tree = ConfigurationTree(
        db, cloned, get_policy(db, cloned.id), nodes(db, cloned.id)
    )
    assert tree.effective("root:api")["retryTimes"] == 4
    assert tree.effective(f"node:api:{cloned_point.id}")["retryTimes"] == 2
    assert f"node:api:{point.id}" not in tree.rows
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        assert (
            await client.delete(f"/orchestration/nodes/{cloned_point.id}")
        ).status_code == 200
    assert db.query(PlanExecutionConfig).filter_by(plan_id=cloned.id).count() == 1
    assert db.query(PlanExecutionConfig).filter_by(plan_id="plan").count() == 2
