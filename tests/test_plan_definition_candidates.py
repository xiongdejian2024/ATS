"""接口双模式按真实定义展开；覆盖分页、排除、权限、模块、视图及草稿回滚。"""

import importlib.util
from pathlib import Path
import httpx
import pytest
from sqlalchemy import create_engine, text, inspect
from test_plan_candidate_modules import module_range
from test_plan_candidate_selection import candidate_range
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from test_plan_minder_edit import point, payload, snapshot, BASE as MINDER
from models import (
    TestCase as Case,
    PlanCaseRelation,
    TestSuite as Suite,
    TestPlan as Plan,
)
from models.native_case import ApiDefinition, NativeCaseConfig
from models.plan_workspace import PlanNode
from models.case_governance import CaseVersion
from models.task_queue import TaskQueue
from services.plan_tree import save_node
from test_plan_candidate_projects import cross

BASE = "/orchestration/plans/plan/case-workspace"


@pytest.mark.asyncio
async def test_cross_project_definition_fresh_children_and_revoked_access(cross):
    from models import ProjectMember

    db, app, _ = cross
    db.add(
        ApiDefinition(
            id="source-definition",
            project_id="source",
            name="来源接口",
            protocol="HTTP",
            path="/source",
            parameters={},
            updated_by="owner",
        )
    )
    db.flush()
    case = db.get(Case, "foreign-0")
    case.type = "api"
    case.is_automated = True
    db.add(
        NativeCaseConfig(
            case_id=case.id,
            api_definition_id="source-definition",
            state="DONE",
            parameters={},
            updated_by="owner",
        )
    )
    db.commit()
    chosen = dict(
        projectId="source",
        category="api",
        resourceType="API",
        definitionIds=["source-definition"],
    )
    before = db.query(Case).count()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(BASE + "/candidates/selection", json=chosen)
        assert (
            response.status_code == 200 and response.json()["data"]["count"] == 1
        ), response.text
        # 保存重新读取定义下的当前子用例；预览后新增引用也被纳入，不使用旧浏览器快照。
        second = db.get(Case, "foreign-1")
        second.type = "api"
        second.is_automated = True
        db.add(
            NativeCaseConfig(
                case_id=second.id,
                api_definition_id="source-definition",
                state="DONE",
                parameters={},
                updated_by="owner",
            )
        )
        db.commit()
        response = await client.post(BASE + "/associate", json=chosen)
        assert (
            response.status_code == 200 and response.json()["data"]["added"] == 2
        ), response.text
        assert {
            row.case_id
            for row in db.query(PlanCaseRelation)
            if row.case_id.startswith("foreign-")
        } == {"foreign-0", "foreign-1"}
        db.query(ProjectMember).filter_by(project_id="source", user_id="owner").delete()
        db.commit()
        assert (await client.post(BASE + "/associate", json=chosen)).status_code == 403
        assert (
            await client.get(
                BASE + "/candidates",
                params=dict(category="api", resourceType="API", projectId="source"),
            )
        ).status_code == 403
    assert db.query(Case).count() == before and db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_definition_metadata_versions_foreign_module_and_old_client_preservation(
    definitions,
):
    from api.v1.native_case import router
    from models import Module

    db, app, _ = definitions
    app.include_router(router)
    db.add(
        Module(id="foreign-definition-module", project_id="other", name="外部接口模块")
    )
    db.commit()
    endpoint = "/projects/project/native-cases/definitions/def-0"
    body = dict(
        name="编辑接口",
        protocol="HTTP",
        path="/definition",
        parameters={"request": {"method": "GET"}},
        expectedRevision=1,
        module_id="child",
        state="DONE",
        tags=["真实标签"],
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.put(endpoint, json=body)
        assert response.status_code == 200, response.text
        old = {
            key: value
            for key, value in body.items()
            if key not in {"module_id", "state", "tags"}
        }
        old.update(expectedRevision=2, name="旧客户端改名")
        response = await client.put(endpoint, json=old)
        assert response.status_code == 200, response.text
        row = next(
            row
            for row in response.json()["data"]["definitions"]
            if row["id"] == "def-0"
        )
        assert (
            row["module_id"] == "child"
            and row["tags"] == ["真实标签"]
            and row["state"] == "DONE"
            and row["created_by"] == "owner"
        )
        assert row["revision"] == 3
        assert (await client.put(endpoint, json=old)).status_code == 409
        assert (
            await client.put(
                endpoint,
                json={
                    **body,
                    "expectedRevision": 3,
                    "module_id": "foreign-definition-module",
                },
            )
        ).status_code == 404
        assert db.get(ApiDefinition, "def-0").revision == 3
        assert (
            await client.put(endpoint, json={**body, "tags": ["重复", "重复"]})
        ).status_code == 422
    assert db.query(TaskQueue).count() == 0


@pytest.fixture
def definitions(module_range):
    db, app, identity = module_range
    for index in range(24):
        definition = ApiDefinition(
            id=f"def-{index}",
            project_id="project",
            name=f"接口%_{index}",
            module_id="child" if index < 23 else None,
            protocol="HTTP",
            path=f"/items/{index}",
            parameters={"request": {"method": "GET"}},
            state="DONE",
            tags=["回归"],
            created_by="owner",
            updated_by="owner",
        )
        db.add(definition)
    db.add(
        ApiDefinition(
            id="foreign-def",
            project_id="other",
            name="外部",
            protocol="HTTP",
            path="/外部",
            parameters={},
            updated_by="owner",
        )
    )
    db.flush()
    for index in range(23):
        for child in range(2 if index == 0 else 1):
            case = Case(
                id=f"def-case-{index}-{child}",
                project_id="project",
                name="接口子用例",
                case_code=f"D-{index}-{child}",
                type="api",
                is_automated=True,
                created_by="owner",
                steps=[],
                module_id="sibling",
            )
            db.add(case)
            db.flush()
            db.add(
                NativeCaseConfig(
                    case_id=case.id,
                    state="DONE",
                    api_definition_id=f"def-{index}",
                    parameters={},
                    updated_by="owner",
                )
            )
    db.commit()
    return db, app, identity


@pytest.mark.asyncio
async def test_definition_pages_real_children_selection_and_no_case_creation(
    definitions,
):
    db, app, _ = definitions
    before = db.query(Case).count()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        first = (
            await client.get(
                BASE + "/candidates",
                params=dict(category="api", resourceType="API", search="%_", size=20),
            )
        ).json()["data"]
        second = (
            await client.get(
                BASE + "/candidates",
                params=dict(
                    category="api", resourceType="API", search="%_", size=20, page=2
                ),
            )
        ).json()["data"]
        assert first["total"] == second["total"] == 24
        rows = first["items"] + second["items"]
        assert next(row for row in rows if row["id"] == "def-0")["caseTotal"] == 2
        assert next(row for row in rows if row["id"] == "def-23")["caseTotal"] == 0
        selected = dict(
            category="api", resourceType="API", definitionIds=["def-0", "def-23"]
        )
        result = await client.post(BASE + "/candidates/selection", json=selected)
        assert result.status_code == 200, result.text
        assert (
            result.json()["data"]["selectedDefinitionCount"]
            == result.json()["data"]["count"]
            == 2
        )
        result = await client.post(BASE + "/associate", json=selected)
        assert (
            result.status_code == 200 and result.json()["data"]["added"] == 2
        ), result.text
        assert {
            r.case_id
            for r in db.query(PlanCaseRelation)
            if r.case_id.startswith("def-")
        } == {"def-case-0-0", "def-case-0-1"}
        assert (
            await client.post(BASE + "/candidates/selection", json=selected)
        ).json()["data"]["count"] == 0
        assert (
            await client.post(
                BASE + "/associate", json={**selected, "definitionIds": ["def-23"]}
            )
        ).json()["data"]["added"] == 0
        # 旧CASE模式的ID不能误传为接口ID，双模式也不能混用。
        for invalid in [
            dict(category="functional", resourceType="API", definitionIds=["def-0"]),
            dict(category="api", resourceType="API", caseIds=["def-case-0-0"]),
            dict(category="api", definitionIds=["def-0"]),
            {**selected, "caseIds": ["def-case-0-0"]},
        ]:
            assert (
                await client.post(BASE + "/associate", json=invalid)
            ).status_code == 422
        assert (
            await client.post(
                BASE + "/associate", json={**selected, "definitionIds": ["foreign-def"]}
            )
        ).status_code == 404
        assert (
            await client.post(
                BASE + "/associate", json=dict(category="api", caseIds=["def-case-1-0"])
            )
        ).json()["data"]["added"] == 1
    assert db.query(Case).count() == before
    assert db.query(TaskQueue).count() == db.query(CaseVersion).count() == 0


@pytest.mark.asyncio
async def test_definition_modules_cross_page_exclusion_and_fresh_move(definitions):
    db, app, _ = definitions
    selected = dict(
        category="api",
        resourceType="API",
        moduleMaps={
            "all": dict(selectAll=True),
            "child": dict(selectAll=True, excludeIds=["def-0", "def-22"]),
        },
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        result = await client.post(BASE + "/candidates/selection", json=selected)
        assert result.status_code == 200, result.text
        data = result.json()["data"]
        assert (
            data["selectedDefinitionCount"] == 22
            and data["count"] == 21
            and data["excludedCount"] == 2
        )
        assert data["moduleCounts"]["child"] == dict(total=23, selected=21)
        assert data["moduleCounts"]["unassigned"] == dict(total=1, selected=1)
        assert data["moduleCounts"]["sibling"] == dict(total=0, selected=0)
        moved = {**selected, "moduleMaps": {"child": dict(selectIds=["def-0"])}}
        db.get(ApiDefinition, "def-0").module_id = "parent"
        db.commit()
        assert (await client.post(BASE + "/associate", json=moved)).status_code == 409
        assert db.query(PlanCaseRelation).count() == 2
        result = await client.post(BASE + "/associate", json=selected)
        assert (
            result.status_code == 200 and result.json()["data"]["added"] == 23
        ), result.text
        # def-0移出被排除的child后，由all范围重新包含，其两个子用例均关联。
        assert db.query(PlanCaseRelation).count() == 25


@pytest.mark.asyncio
async def test_definition_filters_view_isolation_and_permissions(definitions):
    from api.v1.plan_case_workspace import candidate_view_scope
    from models.plan_case_view import PlanCaseSavedView

    assert (
        len(candidate_view_scope("api", "API"))
        <= PlanCaseSavedView.__table__.c.category.type.length
    )
    db, app, identity = definitions
    fields = dict(
        conditions=[
            dict(field="method", operator="equals", value="GET"),
            dict(field="caseTotal", operator="gte", value=2),
            dict(field="createdBy", operator="equals", value="CURRENT_USER"),
        ]
    )
    selected = dict(
        category="api",
        resourceType="API",
        selectAll=True,
        condition=dict(filters=fields, mine=True),
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        result = await client.post(BASE + "/candidates/selection", json=selected)
        assert (
            result.status_code == 200 and result.json()["data"]["count"] == 2
        ), result.text
        response = await client.post(
            BASE + "/candidates/views",
            params=dict(category="api", resourceType="API"),
            json=dict(
                name="接口用例数", filters={"filterConditions": fields["conditions"]}
            ),
        )
        assert response.status_code == 200, response.text
        identifier = response.json()["data"]["id"]
        assert (
            len(
                (
                    await client.get(
                        BASE + "/candidates/views",
                        params=dict(category="api", resourceType="API"),
                    )
                ).json()["data"]
            )
            == 1
        )
        assert (
            await client.get(BASE + "/candidates/views", params=dict(category="api"))
        ).json()["data"] == []
        assert (
            await client.delete(
                BASE + "/candidates/views/" + identifier, params=dict(category="api")
            )
        ).status_code == 404
        for field in ["priority", "apiChange", "environmentName", "customFields.any"]:
            invalid = {
                **selected,
                "condition": dict(
                    filters={
                        "conditions": [dict(field=field, operator="equals", value="P0")]
                    }
                ),
            }
            assert (
                await client.post(BASE + "/candidates/selection", json=invalid)
            ).status_code == 422
        for value in (None, [], ""):
            invalid = {
                **selected,
                "condition": dict(
                    filters={
                        "conditions": [
                            dict(field="caseTotal", operator="between", value=value)
                        ]
                    }
                ),
            }
            response = await client.post(BASE + "/candidates/selection", json=invalid)
            assert (
                response.status_code == 200 and response.json()["data"]["count"] == 24
            ), response.text
        invalid = {
            **selected,
            "condition": dict(
                filters={
                    "conditions": [
                        dict(field="caseTotal", operator="between", value=[1, None])
                    ]
                }
            ),
        }
        assert (
            await client.post(BASE + "/candidates/selection", json=invalid)
        ).status_code == 422
        identity["id"] = "stranger"
        assert (
            await client.get(
                BASE + "/candidates", params=dict(category="api", resourceType="API")
            )
        ).status_code == 403
        assert (
            await client.post(BASE + "/associate", json=selected)
        ).status_code == 403


@pytest.mark.asyncio
async def test_minder_definition_preview_and_late_failure_rollback(definitions):
    db, app, _ = definitions
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        original = await snapshot(client)
        target = point("接口选择新测试集", "api")
        draft = payload(original)
        draft["points"].append(target)
        chosen = dict(category="api", resourceType="API", definitionIds=["def-0"])
        response = await client.post(
            MINDER + "/candidates/selection", json=dict(draft=draft, selection=chosen)
        )
        assert response.status_code == 200, response.text
        assert (
            response.json()["data"]["count"] == 2
            and response.json()["data"]["selectedDefinitionCount"] == 1
        )
        assert (
            db.get(PlanNode, target["id"]) is None
            and db.query(PlanCaseRelation).count() == 2
        )
        draft["associations"] = [
            {**chosen, "collectionId": target["id"]},
            {**chosen, "definitionIds": ["missing"]},
        ]
        assert (await client.put(MINDER, json=draft)).status_code == 404
        assert (await snapshot(client))["fingerprint"] == original["fingerprint"]
        assert (
            db.get(PlanNode, target["id"]) is None
            and db.query(PlanCaseRelation).count() == 2
        )
        draft["associations"].pop()
        assert (await client.put(MINDER, json=draft)).status_code == 200
        assert {
            r.case_id
            for r in db.query(PlanCaseRelation).filter_by(collection_id=target["id"])
        } == {"def-case-0-0", "def-case-0-1"}
        assert db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_definition_tree_repeated_instances_and_suite_compatibility(definitions):
    db, app, _ = definitions
    db.query(PlanCaseRelation).delete()
    save_node(
        db,
        db.get(Plan, "plan"),
        dict(name="原树用例", nodeType="case", caseId="case-2"),
    )
    db.get(Suite, "suite-0").case_ids = ["def-case-0-0", "def-case-0-1"]
    db.commit()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        selected = dict(category="api", resourceType="API", definitionIds=["def-0"])
        response = await client.post(BASE + "/candidates/selection", json=selected)
        assert response.json()["data"]["compatibleSuiteIds"] == ["suite-0"]
        assert (
            await client.post(BASE + "/associate", json=selected)
        ).status_code == 422
        for _ in range(2):
            response = await client.post(
                BASE + "/associate", json={**selected, "suiteId": "suite-0"}
            )
            assert (
                response.status_code == 200 and response.json()["data"]["added"] == 2
            ), response.text
        assert (
            db.query(PlanNode)
            .filter(PlanNode.case_id.in_(["def-case-0-0", "def-case-0-1"]))
            .count()
            == 4
        )
        assert db.query(TaskQueue).count() == 0


def test_metadata_incremental_upgrade_preserves_legacy_unknown_values():
    spec = importlib.util.spec_from_file_location(
        "definition_upgrade",
        Path(__file__).resolve().parents[1]
        / "scripts/upgrade_api_definition_metadata.py",
    )
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)
    engine = create_engine("sqlite://")
    with engine.begin() as connection:
        connection.execute(
            text(
                "CREATE TABLE native_api_definitions (id VARCHAR(36) PRIMARY KEY, name VARCHAR(255), parameters JSON)"
            )
        )
        connection.execute(
            text(
                "INSERT INTO native_api_definitions VALUES ('history','历史接口','{}')"
            )
        )
    assert migration.upgrade(connection_engine=engine) == list(migration.COLUMNS)
    migration.upgrade(True, engine)
    assert migration.upgrade(True, engine) == []
    with engine.connect() as connection:
        assert tuple(
            connection.execute(
                text(
                    "SELECT id,name,parameters,module_id,state,tags,created_by FROM native_api_definitions"
                )
            ).one()
        ) == ("history", "历史接口", "{}", None, None, None, None)
    assert {
        tuple(f["constrained_columns"])
        for f in inspect(engine).get_foreign_keys("native_api_definitions")
    } == {("module_id",), ("created_by",)}
