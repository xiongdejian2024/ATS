"""隔离软件验收：声明式配置、真实结果范围、冻结与请求语义。"""

import asyncio
import json
from copy import deepcopy
from uuid import uuid4
import httpx
import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from framework.native_http.models import (
    RequestSpec,
    Assertion,
    FrozenRequest,
    FrozenCase,
)
from framework.native_http.engine import execute, check
from test_plan_native_workspace import native_workspace
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from models import (
    TestCase as Case,
    TestPlan as Plan,
    TestSuite as Suite,
    User,
    Environment,
)
from models.native_case import NativeCaseConfig, ApiTestEnvironment, ApiDefinition
from models.plan_orchestration import PlanRunItem, PlanRun
from models.task_queue import TaskQueue
from services.native_http_execution import freeze, COMMAND
from services.plan_orchestration import start_plan_run, advance_plan_runs
from services.plan_tree import save_node


@pytest.mark.parametrize(
    "value",
    [
        dict(timeoutMs=True),
        dict(timeoutMs=0),
        dict(bodyType="text", body={}),
        dict(bodyType="form", body={"x": 1}),
        dict(body="多余正文"),
        dict(method="TRACE"),
        dict(assertions=[dict(source="header")]),
        dict(assertions=[dict(source="json", path=[-1])]),
        dict(assertions=[dict(source="status", path=["x"])]),
        dict(unknown=True),
    ],
)
def test_invalid_http_configuration_rejected(value):
    with pytest.raises(ValidationError):
        RequestSpec.model_validate(value)


def test_json_assertion_missing_null_bool_and_numeric_semantics():
    response = httpx.Response(
        200, json={"rows": [{"number": 1, "flag": True, "null": None}]}
    )
    for path, op, expected, success in [
        (["rows", 0, "number"], "equals", 1.0, True),
        (["rows", 0, "flag"], "equals", 1, False),
        (["rows", 0, "null"], "exists", None, True),
        (["missing"], "equals", None, False),
        (["missing"], "not_exists", None, True),
        (["rows"], "contains", {"number": True, "flag": True, "null": None}, False),
    ]:
        assert (
            check(
                Assertion(source="json", path=path, operator=op, expected=expected),
                response,
            )["passed"]
            is success
        )
    assert not check(
        Assertion(source="json", path=["missing"], operator="not_exists"),
        httpx.Response(200, text="不是JSON"),
    )["passed"]


@pytest.mark.asyncio
async def test_request_actual_headers_query_body_and_explicit_error_status():
    seen = []

    def target(request):
        seen.append(request)
        return httpx.Response(
            422,
            json={"accepted": False},
            headers={"X-Result": "软件校验".encode().hex()},
        )

    case = FrozenCase(
        id="api",
        category="api",
        requests=[
            FrozenRequest(
                name="实际请求",
                url="http://loopback.test/target?existing=keep",
                method="POST",
                query={"q": "中文"},
                headers={"X-Test": "value"},
                bodyType="json",
                body={"number": 1},
                assertions=[
                    Assertion(expected=422),
                    Assertion(source="json", path=["accepted"], expected=False),
                    Assertion(
                        source="header",
                        name="x-result",
                        expected="软件校验".encode().hex(),
                    ),
                ],
            )
        ],
    )
    row = await execute(case, transport=httpx.MockTransport(target))
    assert row["status"] == "passed" and row["steps"][0]["statusCode"] == 422
    assert (
        seen[0].url.params["q"] == "中文"
        and seen[0].headers["X-Test"] == "value"
        and json.loads(seen[0].content) == {"number": 1}
    )
    assert seen[0].url.params["existing"] == "keep"
    assert "X-Test" not in row["log"] and "accepted" not in row["log"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "stop,count,result",
    [(True, 1, ["failed", "skipped"]), (False, 2, ["failed", "passed"])],
)
async def test_scenario_failure_controls_real_request_count(stop, count, result):
    seen = []

    def target(request):
        seen.append(request)
        return httpx.Response(500 if len(seen) == 1 else 200)

    case = FrozenCase(
        id="scenario",
        category="scenario",
        stopOnFailure=stop,
        requests=[
            FrozenRequest(url="http://loopback.test/", name=f"步骤{i}")
            for i in range(2)
        ],
    )
    row = await execute(case, transport=httpx.MockTransport(target))
    assert (
        row["status"] == "failed"
        and len(seen) == count
        and [step["result"] for step in row["steps"]] == result
    )


@pytest.mark.asyncio
async def test_total_timeout_and_cancellation_do_not_generate_passed():
    async def target(request):
        await asyncio.sleep(1)
        return httpx.Response(200)

    case = FrozenCase(
        id="api",
        category="api",
        requests=[FrozenRequest(url="http://loopback.test/", name="超时", timeoutMs=5)],
    )
    assert (await execute(case, transport=httpx.MockTransport(target)))[
        "status"
    ] == "error"
    task = asyncio.create_task(execute(case, transport=httpx.MockTransport(target)))
    await asyncio.sleep(0)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task


def configure(db):
    db.get(ApiTestEnvironment, "native-env").address = "http://127.0.0.1:12345/base/"
    db.get(ApiDefinition, "definition").path = "endpoint"
    db.get(NativeCaseConfig, "case-0").parameters = {
        "request": {"assertions": [{"expected": 200}]}
    }
    db.get(NativeCaseConfig, "case-1").parameters = {
        "scenario": {
            "steps": [
                {"apiCaseId": "case-0", "enabled": True},
                {"apiCaseId": "case-0", "enabled": False},
            ]
        }
    }
    db.get(Plan, "plan").environment_id = "node"
    db.commit()


def test_freeze_scene_requests_environment_and_disabled_steps(native_workspace):
    db, _, _ = native_workspace
    configure(db)
    actor = db.get(User, "owner")
    value = freeze(db, db.get(Case, "case-1"), actor)
    assert (
        len(value["requests"]) == 1
        and value["requests"][0]["url"] == "http://127.0.0.1:12345/base/endpoint"
    )
    db.get(ApiDefinition, "definition").path = "http://127.0.0.1:12346/wrong"
    db.commit()
    with pytest.raises(HTTPException):
        freeze(db, db.get(Case, "case-0"), actor)


@pytest.mark.asyncio
async def test_native_whole_plan_freezes_without_duplicate_xat_cases(
    native_workspace, plan_lab
):
    db, _, _ = native_workspace
    _, sent = plan_lab
    configure(db)
    originals = {suite.id: deepcopy(suite.case_ids) for suite in db.query(Suite)}
    run = await start_plan_run(db, "plan", "owner")
    items = (
        db.query(PlanRunItem)
        .filter_by(run_id=run.id)
        .order_by(PlanRunItem.sequence)
        .all()
    )
    assert len(items) == 2 and all(
        item.suite_snapshot["executionCommand"] == COMMAND for item in items
    )
    assert [c["id"] for c in run.case_snapshot] == ["case-0", "case-1"]
    assert all(db.get(Suite, key).case_ids == value for key, value in originals.items())
    db.get(ApiTestEnvironment, "native-env").address = "http://127.0.0.1:12346/changed"
    db.commit()
    await advance_plan_runs(db)
    assert len(sent) == 1 and sent[0][1]["execution_command"] == COMMAND
    assert (
        sent[0][1]["native_cases"][0]["requests"][0]["url"]
        == "http://127.0.0.1:12345/base/endpoint"
    )


@pytest.mark.asyncio
async def test_native_tree_no_user_suite_duplicate_instances_and_resource_pool(
    native_workspace,
):
    db, _, _ = native_workspace
    configure(db)
    db.add(Environment(id="disabled", name="已停用资源", status=False))
    db.flush()
    parent = save_node(
        db,
        db.get(Plan, "plan"),
        dict(
            name="原生请求",
            nodeType="point",
            category="api",
            config={"executionMode": "parallel", "resourcePool": ["disabled", "node"]},
        ),
    )
    leaves = [
        save_node(
            db,
            db.get(Plan, "plan"),
            dict(
                name=f"实例{i}",
                nodeType="case",
                category="api",
                caseId="case-0",
                parentId=parent.id,
            ),
        )
        for i in range(2)
    ]
    db.commit()
    run = await start_plan_run(db, "plan", "owner")
    items = db.query(PlanRunItem).filter_by(run_id=run.id).all()
    assert (
        len(items) == 2
        and len({i.execution_id for i in items}) == 2
        and {i.environment_id for i in items} == {"node"}
    )
    assert {i.suite_snapshot["nodeId"] for i in items} == {n.id for n in leaves}
    assert len({i.suite_id for i in items}) == 1 and db.query(TaskQueue).count() == 2


@pytest.mark.asyncio
async def test_scope_rejects_unselected_original_suite_member(native_workspace):
    from services.suite_results import handle_run_result
    from test_plan_native_run import client, body, ids, execute as run_scope

    db, app, _ = native_workspace
    db.get(Suite, "suite-0").case_ids = ["case-0", "case-1"]
    db.commit()
    async with client(app) as http:
        response = await run_scope(http, body(selectIds=await ids(http)))
        assert response.status_code == 200, response.text
    item = db.query(PlanRunItem).one()
    task = db.query(TaskQueue).one()
    task.status = "running"
    db.commit()
    assert not handle_run_result(
        db,
        "node",
        {
            "suite_id": item.suite_id,
            "execution_id": item.execution_id,
            "case_id": "case-1",
            "result": "passed",
        },
    )
    assert handle_run_result(
        db,
        "node",
        {
            "suite_id": item.suite_id,
            "execution_id": item.execution_id,
            "case_id": "case-0",
            "result": "passed",
        },
    )
