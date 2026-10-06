"""规划整体草稿的事务、默认集和真实冻结顺序，均为隔离软件验收。"""

from uuid import uuid4
import httpx
import pytest
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab, finish
from models import (
    TestPlan as Plan,
    TestCase as Case,
    PlanCaseRelation,
    TestSuite as Suite,
)
from models.plan_workspace import PlanNode, PlanWorkspace
from models.plan_execution_config import PlanExecutionConfig
from models.plan_orchestration import PlanRun, PlanRunItem
from models.task_queue import TaskQueue
from services.plan_tree import save_node
from services.plan_execution_config import (
    ExecutionConfig,
    ConfigSave,
    save as save_config,
)
from services.plan_orchestration import start_plan_run, advance_plan_runs

BASE = "/orchestration/plans/plan/minder-workspace"


def point(name, category="functional", **changes):
    return dict(
        id=str(uuid4()),
        name=name,
        category=category,
        parentId=None,
        position=0,
        **changes,
    )


def payload(snapshot, **changes):
    return dict(
        expectedFingerprint=snapshot["fingerprint"],
        points=[
            {
                key: n.get(key)
                for key in ("id", "name", "category", "parentId", "position")
            }
            for n in snapshot["nodes"]
            if n["nodeType"] == "point"
        ],
        **changes,
    )


async def snapshot(client):
    result = await client.get(BASE)
    assert result.status_code == 200, result.text
    return result.json()["data"]


@pytest.mark.asyncio
async def test_atomic_new_points_name_and_configuration_then_stale_rejected(
    workspace_http,
):
    db, app, _ = workspace_http
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        initial = await snapshot(client)
        one, two = point("接口集", "api"), point("场景集", "scenario")
        body = payload(
            initial,
            configurations={
                f"node:api:{one['id']}": dict(
                    config=ExecutionConfig(
                        extended=False, retryOnFailure=True, retryTimes=2
                    ).model_dump(),
                    expectedRevision=0,
                )
            },
        )
        body["points"] += [one, two]
        # 整体草稿尚未提交时无节点、配置或任务。
        assert (
            db.query(PlanNode).count()
            == db.query(PlanExecutionConfig).count()
            == db.query(TaskQueue).count()
            == 0
        )
        result = await client.put(BASE, json=body)
        assert result.status_code == 200, result.text
        saved = result.json()["data"]
        assert saved["fingerprint"] != initial["fingerprint"]
        assert (
            saved["executionCatalog"]["configurations"][f"node:api:{one['id']}"][
                "effectiveConfig"
            ]["retryTimes"]
            == 2
        )
        assert (await client.put(BASE, json=body)).status_code == 409
        update = payload(saved)
        next(p for p in update["points"] if p["id"] == one["id"])["name"] = "改名后"
        assert (await client.put(BASE, json=update)).status_code == 200
        assert db.get(PlanNode, one["id"]).name == "改名后"
        assert db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_duplicate_names_cross_category_and_configuration_rollback(
    workspace_http,
):
    db, app, _ = workspace_http
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        initial = await snapshot(client)
        body = payload(initial)
        body["points"] = [point("同名"), point("同名")]
        assert (await client.put(BASE, json=body)).status_code == 422
        assert db.query(PlanNode).count() == 0
        body["points"][1]["category"] = "api"
        body["configurations"] = {
            "root:api": dict(
                config=ExecutionConfig(
                    extended=False, requestEnvironmentId="outside"
                ).model_dump(),
                expectedRevision=0,
            )
        }
        assert (await client.put(BASE, json=body)).status_code == 422
        assert db.query(PlanNode).count() == db.query(PlanExecutionConfig).count() == 0
        body["configurations"] = {}
        assert (await client.put(BASE, json=body)).status_code == 200
        assert db.query(PlanNode).count() == 2


@pytest.mark.asyncio
async def test_default_materialization_keeps_association_identity_and_config(
    workspace_http,
):
    db, app, _ = workspace_http
    db.get(Case, "case-0").type = "api"
    save_config(
        db,
        db.get(Plan, "plan"),
        "default:api",
        ConfigSave(
            config=ExecutionConfig(extended=False, retryOnFailure=True, retryTimes=3),
            expectedRevision=0,
        ),
    )
    db.commit()
    before = db.query(PlanCaseRelation).filter_by(case_id="case-0").one().id
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        initial = await snapshot(client)
        body = payload(initial)
        new = point("自定义默认集", "api", materializeDefault="api")
        body["points"].append(new)
        result = await client.put(BASE, json=body)
        assert result.status_code == 200, result.text
        relation = db.get(PlanCaseRelation, before)
        assert relation.collection_id == new["id"] and relation.case_id == "case-0"
        assert db.query(PlanCaseRelation).count() == 2
        migrated = db.get(PlanExecutionConfig, ("plan", f"node:api:{new['id']}"))
        assert (
            migrated and migrated.config["retryTimes"] == 3 and migrated.revision == 1
        )
        assert db.get(PlanExecutionConfig, ("plan", "default:api")) is None
        assert not result.json()["data"]["usesTree"]
        assert result.json()["data"]["entries"]["api"][0]["associationId"] == before


@pytest.mark.asyncio
async def test_delete_collection_unlinks_instead_of_moving_default_and_preserves_history(
    workspace_http,
):
    db, app, _ = workspace_http
    plan = db.get(Plan, "plan")
    collection = save_node(db, plan, dict(name="删除目标"))
    relation = db.query(PlanCaseRelation).filter_by(case_id="case-0").one()
    relation.collection_id = collection.id
    history = PlanRun(
        id="history",
        plan_id="plan",
        executor_id="owner",
        status="completed",
        plan_name="旧计划",
        config_snapshot={},
        case_snapshot=[dict(caseId="case-0")],
        report={"冻结": True, "cases": []},
    )
    db.add(history)
    db.commit()
    relation_id, collection_id = relation.id, collection.id
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        initial = await snapshot(client)
        body = payload(initial)
        body["points"] = []
        result = await client.put(BASE, json=body)
        assert result.status_code == 200, result.text
        assert (
            db.get(PlanCaseRelation, relation_id) is None
            and db.get(PlanNode, collection_id) is None
        )
        assert db.get(Case, "case-0") and db.get(Suite, "suite-0").case_ids == []
        assert db.get(PlanRun, "history").report == {"冻结": True, "cases": []}
        assert [
            item["caseId"] for item in result.json()["data"]["entries"]["functional"]
        ] == ["case-1"]
        assert db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_default_delete_only_requested_category_and_tree_remains_tree(
    workspace_http,
):
    db, app, _ = workspace_http
    plan = db.get(Plan, "plan")
    api = save_node(
        db,
        plan,
        dict(
            name="独立API",
            nodeType="case",
            category="api",
            caseId="case-0",
            suiteId="suite-0",
        ),
    )
    functional = save_node(
        db,
        plan,
        dict(name="独立手工", nodeType="case", category="functional", caseId="case-2"),
    )
    db.commit()
    ids = api.id, functional.id
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        initial = await snapshot(client)
        result = await client.put(BASE, json=payload(initial, deleteDefaults=["api"]))
        assert result.status_code == 200, result.text
        assert db.get(PlanNode, ids[0]) is None and db.get(PlanNode, ids[1])
        saved = result.json()["data"]
        assert saved["usesTree"] and not saved["entries"]["api"]
        assert len(saved["entries"]["functional"]) == 1
        assert db.query(PlanCaseRelation).count() == 2
        result = await client.put(
            BASE, json=payload(saved, deleteDefaults=["functional"])
        )
        assert result.status_code == 200 and result.json()["data"]["usesTree"]
        assert db.get(PlanWorkspace, "plan").uses_tree


@pytest.mark.asyncio
async def test_preserve_old_nested_and_cross_category_projection_disallow_reparent(
    workspace_http,
):
    db, app, _ = workspace_http
    plan = db.get(Plan, "plan")
    parent = save_node(db, plan, dict(name="公共父集"))
    child = save_node(db, plan, dict(name="旧嵌套", category="api", parentId=parent.id))
    db.commit()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        initial = await snapshot(client)
        body = payload(initial)
        nested = next(p for p in body["points"] if p["id"] == child.id)
        nested["parentId"] = None
        assert (await client.put(BASE, json=body)).status_code == 422
        body = payload(initial)
        body["points"] = [p for p in body["points"] if p["id"] == child.id]
        assert (await client.put(BASE, json=body)).status_code == 422
        body = payload(initial)
        body["points"].append(point("新一级集", "api"))
        assert (await client.put(BASE, json=body)).status_code == 200
        assert db.get(PlanNode, child.id).parent_id == parent.id


@pytest.mark.asyncio
async def test_other_page_association_change_rejects_stale_full_structure(
    workspace_http,
):
    db, app, _ = workspace_http
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        initial = await snapshot(client)
        db.add(PlanCaseRelation(plan_id="plan", case_id="case-2"))
        db.commit()
        body = payload(initial)
        body["points"].append(point("旧页面新增"))
        assert (await client.put(BASE, json=body)).status_code == 409
        assert (
            db.query(PlanNode).count() == 0 and db.query(PlanCaseRelation).count() == 3
        )


@pytest.mark.asyncio
async def test_archive_active_plan_and_stale_configuration_reject_all_changes(
    workspace_http,
):
    db, app, _ = workspace_http
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        initial = await snapshot(client)
        body = payload(initial)
        body["points"].append(point("事务草稿"))
        db.add(PlanWorkspace(plan_id="plan", archived=True))
        db.commit()
        assert (await client.put(BASE, json=body)).status_code == 409
        db.get(PlanWorkspace, "plan").archived = False
        db.commit()
        active = PlanRun(
            id="active",
            plan_id="plan",
            executor_id="owner",
            status="queued",
            plan_name="排队",
            config_snapshot={"passThreshold": 100},
            case_snapshot=[],
        )
        db.add(active)
        db.commit()
        body["expectedFingerprint"] = (await snapshot(client))["fingerprint"]
        assert (await client.put(BASE, json=body)).status_code == 409
        db.delete(active)
        db.commit()
        body["expectedFingerprint"] = (await snapshot(client))["fingerprint"]
        body["configurations"] = {
            "root:api": dict(
                config=ExecutionConfig(extended=False).model_dump(), expectedRevision=1
            )
        }
        assert (await client.put(BASE, json=body)).status_code == 409
        assert db.query(PlanNode).count() == db.query(PlanExecutionConfig).count() == 0


@pytest.mark.asyncio
async def test_actual_api_execution_follows_saved_collection_order_and_history_frozen(
    workspace_http,
):
    db, app, _ = workspace_http
    plan = db.get(Plan, "plan")
    plan.environment_id = "node"
    for identifier in ("case-0", "case-1"):
        db.get(Case, identifier).type = "api"
    first = save_node(db, plan, dict(name="第一集", category="api", position=0))
    second = save_node(db, plan, dict(name="第二集", category="api", position=1))
    db.query(PlanCaseRelation).filter_by(case_id="case-0").one().collection_id = (
        first.id
    )
    db.query(PlanCaseRelation).filter_by(case_id="case-1").one().collection_id = (
        second.id
    )
    db.commit()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        initial = await snapshot(client)
        body = payload(initial)
        for p in body["points"]:
            p["position"] = 0 if p["id"] == second.id else 1
        result = await client.put(BASE, json=body)
        assert result.status_code == 200, result.text
        run = await start_plan_run(db, "plan", "owner")
        items = (
            db.query(PlanRunItem)
            .filter_by(run_id=run.id)
            .order_by(PlanRunItem.sequence)
            .all()
        )
        assert [item.suite_snapshot["caseIds"] for item in items] == [
            ["case-1"],
            ["case-0"],
        ]
        assert items[1].suite_snapshot["prerequisites"] == [
            items[0].suite_snapshot["nodeId"]
        ]
        await advance_plan_runs(db)
        finish(db, items[0])
        await advance_plan_runs(db)
        finish(db, items[1])
        await advance_plan_runs(db)
        assert run.status == "completed"
        saved = await snapshot(client)
        body = payload(saved)
        body["points"] = []
        assert (await client.put(BASE, json=body)).status_code == 200
        assert run.report["counts"]["passed"] == 2 and db.query(Case).count() == 3
        assert db.query(PlanCaseRelation).count() == 0


@pytest.mark.asyncio
async def test_plan_root_mode_atomic_preserves_policy_and_rejects_stale(workspace_http):
    from models.plan_orchestration import PlanSettings

    db, app, _ = workspace_http
    db.add(
        PlanSettings(
            plan_id="plan",
            execution_mode="serial",
            stop_on_failure=True,
            pass_threshold=88,
            suite_order=[],
        )
    )
    db.commit()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        old = await snapshot(client)
        body = payload(old, executionMode="parallel")
        body["points"] = [point("根方式原子新增集", "api")]
        result = await client.put(BASE, json=body)
        assert result.status_code == 200, result.text
        saved = result.json()["data"]
        assert saved["policy"]["executionMode"] == "parallel"
        assert (
            saved["policy"]["stopOnFailure"] and saved["policy"]["passThreshold"] == 88
        )
        assert (
            saved["executionCatalog"]["configurations"]["root:api"]["effectiveConfig"][
                "executionMode"
            ]
            == "parallel"
        )
        assert (
            saved["executionCatalog"]["configurations"]["root:scenario"][
                "effectiveConfig"
            ]["executionMode"]
            == "parallel"
        )
        assert (
            await client.put(BASE, json=payload(old, executionMode="serial"))
        ).status_code == 409
        assert (await snapshot(client))["policy"] == saved["policy"]


@pytest.mark.asyncio
async def test_plan_root_mode_rolls_back_with_invalid_configuration(workspace_http):
    db, app, _ = workspace_http
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        old = await snapshot(client)
        body = payload(
            old,
            executionMode="parallel",
            configurations={
                "missing:api": dict(
                    config=ExecutionConfig().model_dump(), expectedRevision=0
                )
            },
        )
        result = await client.put(BASE, json=body)
        assert result.status_code == 404, result.text
        saved = await snapshot(client)
        assert saved["fingerprint"] == old["fingerprint"]
        assert saved["policy"] == old["policy"]
        assert (
            await client.put(BASE, json=payload(old, executionMode="wrong"))
        ).status_code == 422


@pytest.mark.asyncio
async def test_minder_root_parallel_drives_actual_queue_and_frozen_policy(plan_lab):
    from models import User
    from services.plan_minder_edit import load, save, MinderSave

    db, sent = plan_lab
    user = db.get(User, "owner")
    current = load(db, user, "plan")
    saved = save(
        db,
        user,
        "plan",
        MinderSave(
            expectedFingerprint=current["fingerprint"],
            points=[],
            executionMode="parallel",
        ),
    )
    db.commit()
    assert saved["policy"]["executionMode"] == "parallel"
    run = await start_plan_run(db, "plan", "owner")
    assert run.config_snapshot["executionMode"] == "parallel"
    assert db.query(TaskQueue).filter_by(status="pending").count() == 2
    assert not sent
    await advance_plan_runs(db)
    items = (
        db.query(PlanRunItem)
        .filter_by(run_id=run.id)
        .order_by(PlanRunItem.sequence)
        .all()
    )
    assert len(sent) == 2 and all(item.status == "running" for item in items)
    for item in items:
        finish(db, item)
    await advance_plan_runs(db)
    assert run.status == "completed" and run.report["counts"]["passed"] == 2


@pytest.mark.asyncio
async def test_provisional_default_name_cannot_duplicate_virtual_default_and_rolls_back(
    workspace_http,
):
    db, app, _ = workspace_http
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        old = await snapshot(client)
        assert old["entries"]["functional"]
        body = payload(old, executionMode="parallel")
        temporary = point("默认测试集")
        body["points"].append(temporary)
        result = await client.put(BASE, json=body)
        assert result.status_code == 422 and "默认测试集" in result.text
        assert (await snapshot(client))["fingerprint"] == old["fingerprint"]
        temporary["name"] = "直接插入后改名"
        saved = await client.put(BASE, json=body)
        assert saved.status_code == 200, saved.text
        assert saved.json()["data"]["entries"] == old["entries"]
