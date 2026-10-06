"""脑图临时集关联：真实解析、保存点回滚、整图原子保存及权限重查。"""

import httpx
import pytest
from test_plan_minder_edit import BASE, point, payload, snapshot
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from test_plan_candidate_projects import cross
from test_plan_candidate_sync import sync_lab
from models import (
    TestPlan as Plan,
    TestCase as Case,
    TestSuite as Suite,
    PlanCaseRelation,
)
from models.plan_workspace import PlanNode
from models.plan_execution_config import PlanExecutionConfig
from models.task_queue import TaskQueue
from services.plan_tree import save_node

PREVIEW = BASE + "/candidates/selection"


@pytest.mark.asyncio
async def test_new_collection_preview_never_persists_and_whole_save_links(
    workspace_http,
):
    db, app, _ = workspace_http
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        initial = await snapshot(client)
        target = point("临时功能集")
        body = payload(initial)
        body["points"] = [target]
        chosen = dict(
            category="functional", caseIds=["case-2"], collectionId=target["id"]
        )
        preview = await client.post(
            PREVIEW,
            json=dict(
                draft=body, selection=dict(category="functional", caseIds=["case-2"])
            ),
        )
        assert preview.status_code == 200, preview.text
        assert preview.json()["data"]["count"] == 1
        assert (await snapshot(client))["fingerprint"] == initial["fingerprint"]
        assert (
            db.query(PlanNode).count()
            == db.query(PlanExecutionConfig).count()
            == db.query(TaskQueue).count()
            == 0
        )
        body["associations"] = [chosen]
        saved = await client.put(BASE, json=body)
        assert saved.status_code == 200, saved.text
        linked = db.query(PlanCaseRelation).filter_by(case_id="case-2").one()
        assert linked.collection_id == target["id"]
        assert db.query(Case).count() == 3 and db.query(TaskQueue).count() == 0
        assert (await client.put(BASE, json=body)).status_code == 409


@pytest.mark.asyncio
async def test_pending_range_preview_excludes_earlier_batch_and_rolls_back(
    workspace_http,
):
    db, app, _ = workspace_http
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        initial = await snapshot(client)
        body = payload(initial, associations=[dict(caseIds=["case-2"])])
        body["points"] = [point("先前待关联")]
        selected = dict(selectAll=True, condition=dict(folder="all"))
        result = await client.post(PREVIEW, json=dict(draft=body, selection=selected))
        assert result.status_code == 200, result.text
        assert result.json()["data"]["count"] == 0
        assert (
            db.query(PlanCaseRelation).count() == 2 and db.query(PlanNode).count() == 0
        )
        assert (await snapshot(client))["fingerprint"] == initial["fingerprint"]
        body["associations"][0]["caseIds"] = ["missing"]
        assert (
            await client.post(PREVIEW, json=dict(draft=body, selection=selected))
        ).status_code == 404
        assert (await snapshot(client))["fingerprint"] == initial["fingerprint"]


@pytest.mark.asyncio
async def test_late_invalid_association_rolls_back_points_mode_configs_and_prior_batch(
    workspace_http,
):
    db, app, _ = workspace_http
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        initial = await snapshot(client)
        target = point("回滚新增")
        body = payload(
            initial,
            executionMode="parallel",
            associations=[
                dict(caseIds=["case-2"], collectionId=target["id"]),
                dict(caseIds=["missing"]),
            ],
        )
        body["points"] = [target]
        assert (await client.put(BASE, json=body)).status_code == 404
        assert (await snapshot(client))["fingerprint"] == initial["fingerprint"]
        assert db.query(PlanNode).count() == db.query(PlanExecutionConfig).count() == 0
        assert (
            db.query(PlanCaseRelation).count() == 2 and db.query(TaskQueue).count() == 0
        )


@pytest.mark.asyncio
async def test_new_cross_project_sync_targets_preview_and_save_atomic(sync_lab):
    db, app, _ = sync_lab
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        initial = await snapshot(client)
        functional, api, scene = (
            point("新功能集"),
            point("新接口集", "api"),
            point("新场景集", "scenario"),
        )
        body = payload(initial)
        body["points"] += [functional, api, scene]
        selection = dict(
            projectId="source",
            moduleMaps={"all": dict(selectAll=True, excludeIds=["foreign-2"])},
            syncCase=True,
            apiCaseCollectionId=api["id"],
            apiScenarioCollectionId=scene["id"],
        )
        result = await client.post(PREVIEW, json=dict(draft=body, selection=selection))
        assert result.status_code == 200, result.text
        assert result.json()["data"]["sync"]["api"]["count"] == 2
        assert result.json()["data"]["sync"]["scenario"]["count"] == 1
        assert (await snapshot(client))["fingerprint"] == initial["fingerprint"]
        body["associations"] = [{**selection, "collectionId": functional["id"]}]
        result = await client.put(BASE, json=body)
        assert result.status_code == 200, result.text
        actual = {r.case_id: r.collection_id for r in db.query(PlanCaseRelation)}
        assert actual["foreign-0"] == actual["foreign-1"] == functional["id"]
        assert (
            actual["api-0"] == actual["api-1"] == api["id"]
            and actual["scenario-0"] == scene["id"]
        )
        assert "foreign-2" not in actual and "recycled" not in actual
        assert db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_cross_project_permission_revoked_after_preview_rejects_complete_save(
    sync_lab,
):
    from models import ProjectMember

    db, app, identity = sync_lab
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        initial = await snapshot(client)
        target = point("来源撤权回滚集")
        body = payload(initial)
        body["points"].append(target)
        selection = dict(projectId="source", caseIds=["foreign-0"])
        result = await client.post(PREVIEW, json=dict(draft=body, selection=selection))
        assert result.status_code == 200, result.text
        db.query(ProjectMember).filter_by(project_id="source", user_id="owner").delete()
        db.commit()
        body["associations"] = [{**selection, "collectionId": target["id"]}]
        assert (
            await client.post(PREVIEW, json=dict(draft=body, selection=selection))
        ).status_code == 403
        assert (await client.put(BASE, json=body)).status_code == 403
        assert (await snapshot(client))["fingerprint"] == initial["fingerprint"]
        assert (
            db.get(PlanNode, target["id"]) is None
            and db.query(PlanCaseRelation).count() == 2
        )


@pytest.mark.asyncio
async def test_tree_repeated_case_instances_and_suite_binding_in_single_save(
    workspace_http,
):
    db, app, _ = workspace_http
    plan = db.get(Plan, "plan")
    db.query(PlanCaseRelation).delete()
    save_node(db, plan, dict(name="原手工", nodeType="case", caseId="case-2"))
    db.get(Case, "case-0").type = "api"
    db.commit()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        initial = await snapshot(client)
        first, second = point("接口新集一", "api"), point("接口新集二", "api")
        second["position"] = 1
        body = payload(initial)
        body["points"] += [first, second]
        body["associations"] = [
            dict(
                category="api",
                caseIds=["case-0"],
                collectionId=p["id"],
                suiteId="suite-0",
            )
            for p in [first, second]
        ]
        body["associations"][1]["suiteId"] = "suite-1"
        assert (await client.put(BASE, json=body)).status_code == 422
        assert (await snapshot(client))["fingerprint"] == initial["fingerprint"]
        body["associations"][1]["suiteId"] = "suite-0"
        result = await client.put(BASE, json=body)
        assert result.status_code == 200, result.text
        nodes = db.query(PlanNode).filter_by(case_id="case-0").all()
        assert len(nodes) == 2 and {n.parent_id for n in nodes} == {
            first["id"],
            second["id"],
        }
        assert (
            all(n.suite_id == "suite-0" for n in nodes)
            and db.query(TaskQueue).count() == 0
        )
