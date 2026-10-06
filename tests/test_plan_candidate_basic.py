"""接口基础条件必须约束分页、目录、排除和当前读；排序不能改变关联身份。"""

import httpx
import pytest
from test_plan_definition_candidates import definitions
from test_plan_candidate_modules import module_range
from test_plan_candidate_selection import candidate_range
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from models import TestCase as Case, PlanCaseRelation, User, ProjectMember
from models.native_case import ApiDefinition
from models.task_queue import TaskQueue

BASE = "/orchestration/plans/plan/case-workspace"


@pytest.fixture
def basic(definitions):
    db, app, identity = definitions
    db.add(
        User(
            id="writer",
            username="接口创建人",
            email="writer@example.test",
            password_hash="不用登录",
        )
    )
    db.flush()
    db.add(ProjectMember(project_id="project", user_id="writer", role="member"))
    for i in range(24):
        row = db.get(ApiDefinition, f"def-{i}")
        row.protocol = "HTTP" if i < 12 else "TCP"
        row.parameters = {"request": {"method": "POST" if i < 6 else "GET"}}
        row.created_by = "owner" if i % 2 == 0 else "writer"
    db.commit()
    return db, app, identity


@pytest.mark.asyncio
async def test_basic_definition_page_module_counts_sort_and_cross_page_exclusion(basic):
    db, app, _ = basic
    before = db.query(Case).count()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        params = dict(
            category="api",
            resourceType="API",
            protocols="HTTP",
            methods="POST",
            createdBy="owner",
            size=2,
            sort="id",
            direction="asc",
        )
        first = await client.get(BASE + "/candidates", params=params)
        assert first.status_code == 200, first.text
        first = first.json()["data"]
        second = (
            await client.get(BASE + "/candidates", params={**params, "page": 2})
        ).json()["data"]
        assert first["total"] == second["total"] == first["counts"]["all"] == 3
        assert [r["id"] for r in first["items"] + second["items"]] == [
            "def-0",
            "def-2",
            "def-4",
        ]
        assert first["basicOptions"]["protocols"] == ["HTTP", "TCP"]
        assert {r["value"] for r in first["basicOptions"]["creators"]} == {
            "owner",
            "writer",
        }
        assert next(m for m in first["modules"] if m["id"] == "child")["count"] == 3
        desc = (
            await client.get(
                BASE + "/candidates", params={**params, "direction": "desc"}
            )
        ).json()["data"]
        assert [r["id"] for r in desc["items"]] == ["def-4", "def-2"]
        chosen = dict(
            category="api",
            resourceType="API",
            moduleMaps={"all": dict(selectAll=True, excludeIds=["def-4"])},
            condition=dict(protocols=["HTTP"], methods=["POST"], createdBy=["owner"]),
        )
        summary = (
            await client.post(BASE + "/candidates/selection", json=chosen)
        ).json()["data"]
        assert (
            summary["selectedDefinitionCount"] == 2
            and summary["count"] == 3
            and summary["excludedCount"] == 1
        )
        assert summary["moduleCounts"]["child"] == dict(total=3, selected=2)
        saved = await client.post(BASE + "/associate", json=chosen)
        assert (
            saved.status_code == 200 and saved.json()["data"]["added"] == 3
        ), saved.text
    assert {
        r.case_id
        for r in db.query(PlanCaseRelation)
        if r.case_id.startswith("def-case")
    } == {"def-case-0-0", "def-case-0-1", "def-case-2-0"}
    assert db.query(Case).count() == before and db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_empty_protocols_explicit_scope_stale_and_advanced_reject(basic):
    db, app, _ = basic
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        params = dict(category="api", resourceType="API", protocols="")
        empty = (await client.get(BASE + "/candidates", params=params)).json()["data"]
        assert empty["items"] == [] and empty["total"] == empty["counts"]["all"] == 0
        chosen = dict(
            category="api",
            resourceType="API",
            definitionIds=["def-0"],
            condition=dict(protocols=["HTTP"], methods=["POST"]),
        )
        assert (await client.post(BASE + "/candidates/selection", json=chosen)).json()[
            "data"
        ]["count"] == 2
        db.get(ApiDefinition, "def-0").protocol = "TCP"
        db.commit()
        assert (await client.post(BASE + "/associate", json=chosen)).status_code == 404
        module = {
            **chosen,
            "definitionIds": [],
            "moduleMaps": {"child": dict(selectIds=["def-0"])},
        }
        assert (await client.post(BASE + "/associate", json=module)).status_code == 409
        for condition in [
            dict(protocols=["HTTP", "HTTP"]),
            dict(protocols=[" HTTP"]),
            dict(methods=["x" * 51]),
            dict(protocols=["HTTP"], mine=True),
            dict(protocols=["HTTP"], filters={"conditions": []}),
        ]:
            assert (
                await client.post(
                    BASE + "/candidates/selection",
                    json={**chosen, "condition": condition},
                )
            ).status_code == 422
        assert (
            await client.get(
                BASE + "/candidates",
                params={**params, "methods": "GET", "resourceType": "CASE"},
            )
        ).status_code == 422
        assert (
            await client.get(
                BASE + "/candidates",
                params={**params, "category": "scenario", "resourceType": "CASE"},
            )
        ).status_code == 422
        assert (
            await client.get(
                BASE + "/candidates", params={**params, "filters": '{"conditions":[]}'}
            )
        ).status_code == 422
    assert db.query(PlanCaseRelation).count() == 2 and db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_case_protocol_sql_counts_and_explicit_selection(basic):
    db, app, _ = basic
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        params = dict(
            category="api", protocols="TCP", size=5, sort="id", direction="desc"
        )
        data = (await client.get(BASE + "/candidates", params=params)).json()["data"]
        assert data["total"] == data["counts"]["all"] == 11
        assert all(
            row["protocol"] == "TCP"
            and row["createdByName"] == db.get(User, "owner").username
            for row in data["items"]
        )
        advanced = await client.get(
            BASE + "/candidates",
            params=dict(category="api", filters='{"conditions":[]}', size=5, sort="name", direction="asc"),
        )
        assert advanced.status_code == 200, advanced.text
        assert all(
            row["createdByName"] == db.get(User, "owner").username
            for row in advanced.json()["data"]["items"]
        )
        asc_names = [row["name"] for row in advanced.json()["data"]["items"]]
        assert asc_names == sorted(asc_names)
        advanced_desc = await client.get(
            BASE + "/candidates",
            params=dict(category="api", filters='{"conditions":[]}', size=50, sort="name", direction="desc"),
        )
        names = [row["name"] for row in advanced_desc.json()["data"]["items"]]
        assert len(names) == 24 and names == sorted(names, reverse=True)
        assert (
            await client.get(BASE + "/candidates", params={**params, "protocols": ""})
        ).json()["data"]["total"] == 0
        chosen = dict(
            category="api", caseIds=["def-case-12-0"], condition=dict(protocols=["TCP"])
        )
        assert (await client.post(BASE + "/associate", json=chosen)).status_code == 200
        invalid = {**chosen, "caseIds": ["def-case-0-0"]}
        assert (await client.post(BASE + "/associate", json=invalid)).status_code == 404
        scope = dict(
            category="api",
            selectAll=True,
            excludeIds=["def-case-13-0"],
            condition=dict(protocols=["TCP"]),
        )
        summary = (
            await client.post(BASE + "/candidates/selection", json=scope)
        ).json()["data"]
        assert summary["count"] == 9 and summary["excludedCount"] == 1
    assert db.query(TaskQueue).count() == 0
