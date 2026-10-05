"""真实本地HTTP目标、后端WebSocket、Agent和冻结计划报告的端到端验收。"""

import asyncio
import json
import socket
import time
from uuid import uuid4
import pytest
import pytest_asyncio
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from test_http_agent_e2e import lab, until, queue_states


@pytest_asyncio.fixture
async def native_lab(lab):
    from database import SessionLocal
    from models import TestPlan as Plan

    target = FastAPI()
    hits = []
    entered = asyncio.Event()
    release = asyncio.Event()
    blocked = False
    response_statuses = []
    hit_times = []

    @target.post("/echo")
    async def echo(request: Request):
        hit_times.append(time.monotonic())
        hits.append(
            {
                "query": dict(request.query_params),
                "body": await request.json(),
                "header": request.headers.get("X-Frozen"),
            }
        )
        entered.set()
        if blocked:
            await release.wait()
        return JSONResponse(
            {"accepted": True, "rows": [{"value": 7}]},
            status_code=response_statuses.pop(0) if response_statuses else 201,
            headers={"X-Lab": "owned-loopback"},
        )

    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    server = uvicorn.Server(
        uvicorn.Config(
            target, host="127.0.0.1", port=port, log_level="error", lifespan="off"
        )
    )
    serving = asyncio.create_task(server.serve(sockets=[sock]))
    await until(lambda: server.started)
    project_id = lab["cases"][0]["projectId"]
    base = f"/projects/{project_id}/native-cases"
    request = {
        "method": "POST",
        "query": {"q": "中文参数"},
        "headers": {"X-Frozen": "original"},
        "bodyType": "json",
        "body": {"number": 7},
        "assertions": [
            {"expected": 201},
            {"source": "json", "path": ["rows", 0, "value"], "expected": 7},
            {"source": "header", "name": "X-Lab", "expected": "owned-loopback"},
        ],
    }
    post = lab["post"]
    catalog = await post(
        base + "/definitions",
        {"name": "自建回环接口", "protocol": "HTTP", "path": "/echo", "parameters": {}},
    )
    definition = catalog["definitions"][0]
    catalog = await post(
        base + "/environments",
        {"name": "自建HTTP目标", "address": f"http://127.0.0.1:{port}"},
    )
    environment = catalog["environments"][0]
    api = await post(
        "/test-cases",
        {
            "project_id": project_id,
            "case_code": "OWN_HTTP",
            "name": "自建HTTP请求",
            "type": "api",
            "is_automated": False,
        },
    )
    scene = await post(
        "/test-cases",
        {
            "project_id": project_id,
            "case_code": "OWN_SCENE",
            "name": "自建场景",
            "type": "scenario",
            "is_automated": False,
        },
    )

    async def config(case, parameters, revision=0):
        response = await lab["client"].put(
            "/api/v1" + base + "/cases/" + case["id"],
            json={
                "state": "DONE" if case["type"] == "api" else "COMPLETED",
                "apiDefinitionId": definition["id"] if case["type"] == "api" else None,
                "environmentId": environment["id"],
                "parameters": parameters,
                "expectedRevision": revision,
                "expectedDefinitionRevision": (
                    definition["revision"] if case["type"] == "api" else None
                ),
            },
        )
        assert response.status_code == 200, response.text
        return response.json()["data"]

    await config(api, {"request": request})
    await config(
        scene,
        {
            "scenario": {
                "steps": [
                    {"apiCaseId": api["id"], "enabled": True},
                    {"apiCaseId": api["id"], "enabled": False},
                    {"apiCaseId": api["id"], "enabled": True},
                ],
                "stopOnFailure": True,
            }
        },
    )
    plan = await post(
        "/test-plans",
        {
            "project_id": project_id,
            "name": "原生HTTP软件验收",
            "startDate": "2026-10-06",
            "testCaseIds": [api["id"], scene["id"]],
        },
    )
    with SessionLocal() as db:
        db.get(Plan, plan["id"]).environment_id = lab["environment"]["id"]
        db.commit()

    def block():
        nonlocal blocked
        blocked = True
        entered.clear()

    value = {
        **lab,
        "native_plan": plan,
        "api": api,
        "scene": scene,
        "request": request,
        "config": config,
        "hits": hits,
        "entered": entered,
        "release": release,
        "block": block,
        "response_statuses": response_statuses,
        "hit_times": hit_times,
        "request_environment": environment,
    }
    try:
        yield value
    finally:
        release.set()
        server.should_exit = True
        await asyncio.wait_for(serving, 5)


async def dispatch(run_id):
    from database import SessionLocal
    from services.plan_orchestration import advance_plan_runs

    with SessionLocal() as db:
        await advance_plan_runs(db)


async def finished(run_id):
    from database import SessionLocal
    from models.plan_orchestration import PlanRunItem
    from models.task_queue import TaskQueue

    def done():
        with SessionLocal() as db:
            ids = [
                i.execution_id for i in db.query(PlanRunItem).filter_by(run_id=run_id)
            ]
            return bool(ids) and all(
                t.status in {"completed", "failed", "cancelled"}
                for t in db.query(TaskQueue).filter(TaskQueue.execution_id.in_(ids))
            )

    await until(done)
    await dispatch(run_id)


async def scope(value, category):
    base = (
        f'/api/v1/plan-orchestration/plans/{value["native_plan"]["id"]}/case-workspace'
    )
    response = await value["client"].get(base, params={"category": category})
    assert response.status_code == 200, response.text
    rows = response.json()["data"]["items"]
    response = await value["client"].post(
        base + "/run-range",
        json={
            "category": category,
            "selectIds": [rows[0]["id"]],
            "requestId": str(uuid4()),
        },
    )
    assert response.status_code == 200, response.text
    return response.json()["data"]["id"]


@pytest.mark.asyncio
async def test_whole_plan_real_native_http_scene_freeze_ack_and_report(native_lab):
    from database import SessionLocal
    from models.plan_orchestration import PlanRun, PlanRunItem
    from models.test_suite import TestSuiteExecution

    value = native_lab
    path = f'/api/v1/test-plans/{value["native_plan"]["id"]}'
    response = await value["client"].post(path + "/execute", json={})
    assert response.status_code == 200, response.text
    run_id = response.json()["data"]["id"]
    changed = {**value["request"], "headers": {"X-Frozen": "changed"}}
    await value["config"](value["api"], {"request": changed}, revision=1)
    await dispatch(run_id)
    # 串行计划需要调度循环在第一条真实完成后释放场景。
    with SessionLocal() as db:
        first = (
            db.query(PlanRunItem).filter_by(run_id=run_id, sequence=0).one().suite_id
        )
    await until(
        lambda: bool(queue_states(first))
        and set(queue_states(first).values()) == {"completed"}
    )
    await dispatch(run_id)
    await finished(run_id)
    assert len(value["hits"]) == 3 and all(
        h == {"query": {"q": "中文参数"}, "body": {"number": 7}, "header": "original"}
        for h in value["hits"]
    )
    with SessionLocal() as db:
        run = db.get(PlanRun, run_id)
        items = db.query(PlanRunItem).filter_by(run_id=run_id).all()
        assert (
            run.status == "completed"
            and run.report["total"] == 2
            and run.report["counts"]["passed"] == 2
        )
        assert {row['category'] for row in run.report['cases']} == {'api', 'scenario'}
        from services.suite_results import result_id

        rows = (
            db.query(TestSuiteExecution)
            .filter(
                TestSuiteExecution.id.in_(
                    [
                        result_id(i.execution_id, cid)
                        for i in items
                        for cid in i.suite_snapshot["caseIds"]
                    ]
                )
            )
            .all()
        )
        assert len(rows) == 2 and sorted(
            len(json.loads(r.log_output)["步骤"]) for r in rows
        ) == [1, 2]
        assert all(
            json.loads(r.log_output)["步骤"][0]["statusCode"] == 201 for r in rows
        )
        assert all(
            (
                value["agent"].work_dir
                / "suites"
                / i.suite_id
                / "executions"
                / i.execution_id
                / "native-run.json"
            ).exists()
            for i in items
        )
    await until(lambda: not list(value["agent"].sat_runner.outbox.glob("*.json")))
    print(
        "原生端到端验收通过：真实本地HTTP三次请求；冻结配置不受入队后修改影响；两条真实报告及可靠ACK。"
    )


@pytest.mark.asyncio
async def test_native_scene_failed_assertion_stops_actual_next_request(native_lab):
    from database import SessionLocal
    from models.plan_orchestration import PlanRun

    value = native_lab
    changed = {**value["request"], "assertions": [{"expected": 200}]}
    await value["config"](value["api"], {"request": changed}, revision=1)
    run_id = await scope(value, "scenario")
    await dispatch(run_id)
    await finished(run_id)
    assert len(value["hits"]) == 1
    with SessionLocal() as db:
        run = db.get(PlanRun, run_id)
        assert (
            run.status == "failed"
            and run.report["total"] == 1
            and run.report["counts"]["failed"] == 1
        )
    print("场景失败验收通过：真实201响应与200断言不符，仅请求一次，后续步骤未发送。")


@pytest.mark.asyncio
async def test_native_http_cancel_real_inflight_request(native_lab):
    from database import SessionLocal
    from models.plan_orchestration import PlanRun

    value = native_lab
    value["block"]()
    run_id = await scope(value, "api")
    await dispatch(run_id)
    await asyncio.wait_for(value["entered"].wait(), 5)
    response = await value["client"].post(
        f"/api/v1/plan-orchestration/runs/{run_id}/cancel"
    )
    assert response.status_code == 200, response.text
    await finished(run_id)
    with SessionLocal() as db:
        run = db.get(PlanRun, run_id)
        assert run.status == "cancelled" and run.report["counts"]["passed"] == 0
    assert not value["agent"].native_http_runner.runs and len(value["hits"]) == 1
    print("原生取消验收通过：取消正在等待真实HTTP响应的请求，报告没有虚构成功结果。")


@pytest.mark.asyncio
async def test_native_reconnect_durable_ack_and_duplicate_does_not_repeat_http(
    native_lab,
):
    from database import SessionLocal
    from models.plan_orchestration import PlanRunItem
    from agent.native_http_runner import NativeHTTPRunner

    value = native_lab
    value["block"]()
    run_id = await scope(value, "api")
    await dispatch(run_id)
    await asyncio.wait_for(value["entered"].wait(), 5)
    await value["agent"].ws_client.websocket.close(code=1000)
    await until(lambda: not value["agent"].ws_client.connected)
    value["release"].set()
    await until(lambda: bool(list(value["agent"].sat_runner.outbox.glob("*.json"))))
    await finished(run_id)
    await until(lambda: not list(value["agent"].sat_runner.outbox.glob("*.json")))
    with SessionLocal() as db:
        item = db.query(PlanRunItem).filter_by(run_id=run_id).one()
        message = {
            "type": "execute_test_suite",
            "suite_id": item.suite_id,
            "execution_id": item.execution_id,
            "plan_id": value["native_plan"]["id"],
            "execution_command": "ats-native-http",
            "case_ids": item.suite_snapshot["caseIds"],
            "native_cases": item.suite_snapshot["nativeCases"],
        }
    runner = NativeHTTPRunner(value["agent"])
    runner.start(message)
    assert not runner.runs and len(value["hits"]) == 1
    print(
        "断网回传验收通过：结果保留在本地，重连后ACK清空；重新创建执行器后重复派发未重复HTTP请求。"
    )


@pytest.mark.asyncio
async def test_scoped_xat_actual_completion_ignores_unselected_suite_members(lab):
    from database import SessionLocal
    from models import TestCase as Case
    from models.plan_orchestration import PlanRun

    value = {**lab, "native_plan": lab["plan"]}
    with SessionLocal() as db:
        db.get(Case, lab["cases"][0]["id"]).type = "api"
        db.commit()
    run_id = await scope(value, "api")
    await dispatch(run_id)
    await finished(run_id)
    with SessionLocal() as db:
        run = db.get(PlanRun, run_id)
        assert (
            run.status == "completed"
            and run.report["total"] == 1
            and run.report["counts"]["passed"] == 1
        )
    assert len(lab["suite"]["caseIds"]) == 4
    print(
        "范围完成校验验收通过：四成员XAT测试套只执行所选一条，真实WebSocket回传后仍正确完成。"
    )


async def execution_config(value, category, **changes):
    from services.plan_execution_config import ExecutionConfig
    base = f'/api/v1/plan-orchestration/plans/{value["native_plan"]["id"]}'
    response = await value["client"].post(base + "/resource-pools", json={"name": "自建回环验收池", "environmentIds": [value["environment"]["id"]]})
    assert response.status_code == 200, response.text
    pool = response.json()["data"]["pools"][-1]
    config = ExecutionConfig(extended=False, testResourcePoolId=pool["id"], requestEnvironmentId=value["request_environment"]["id"], **changes).model_dump()
    response = await value["client"].put(base + f"/execution-configurations/root:{category}", json={"config": config, "expectedRevision": 0})
    assert response.status_code == 200, response.text
    return base, config


@pytest.mark.asyncio
async def test_real_scene_retries_only_failed_step_and_reports_one_final_case(native_lab):
    from database import SessionLocal
    from models.plan_orchestration import PlanRun, PlanRunItem
    from models.test_suite import TestSuiteExecution
    from services.suite_results import result_id

    value = native_lab
    value["response_statuses"].extend([201, 500, 201])
    base, config = await execution_config(value, "scenario", retryOnFailure=True, retryTimes=2, retryInterval=100)
    run_id = await scope(value, "scenario")
    # 排队后修改重试配置，Agent仍使用入队时冻结的步骤重试。
    response = await value["client"].put(base + "/execution-configurations/root:scenario", json={"config": dict(config, retryOnFailure=False), "expectedRevision": 1})
    assert response.status_code == 200
    await dispatch(run_id)
    await finished(run_id)
    assert len(value["hits"]) == 3
    assert value["hit_times"][2] - value["hit_times"][1] >= 0.09
    with SessionLocal() as db:
        run = db.get(PlanRun, run_id)
        item = db.query(PlanRunItem).filter_by(run_id=run_id).one()
        row = db.get(TestSuiteExecution, result_id(item.execution_id, value["scene"]["id"]))
        steps = json.loads(row.log_output)["步骤"]
        assert [len(step["attempts"]) for step in steps] == [1, 2]
        assert [attempt["statusCode"] for attempt in steps[1]["attempts"]] == [500, 201]
        assert run.status == "completed" and run.report["total"] == run.report["counts"]["passed"] == 1
    print("真实步骤重试验收通过：成功步骤一次、失败步骤两次；等待实际100毫秒；冻结重试配置生效，最终报告仅一条通过。")


@pytest.mark.asyncio
async def test_real_retry_exhaustion_then_stops_scene(native_lab):
    value = native_lab
    value["response_statuses"].extend([500, 500, 500])
    await execution_config(value, "scenario", retryOnFailure=True, retryTimes=2, retryInterval=0)
    run_id = await scope(value, "scenario")
    await dispatch(run_id)
    await finished(run_id)
    assert len(value["hits"]) == 3
    from database import SessionLocal
    from models.plan_orchestration import PlanRun
    with SessionLocal() as db:
        run = db.get(PlanRun, run_id)
        assert run.status == "failed" and run.report["total"] == run.report["counts"]["failed"] == 1
    print("重试耗尽验收通过：首次及两次重试均为真实500，后续场景步骤未发送，报告只有一条失败。")


@pytest.mark.asyncio
async def test_real_retry_delay_is_cancellable(native_lab):
    value = native_lab
    value["response_statuses"].append(500)
    await execution_config(value, "api", retryOnFailure=True, retryTimes=2, retryInterval=30000)
    run_id = await scope(value, "api")
    await dispatch(run_id)
    await asyncio.wait_for(value["entered"].wait(), 5)
    await asyncio.sleep(0.05)
    response = await value["client"].post(f"/api/v1/plan-orchestration/runs/{run_id}/cancel")
    assert response.status_code == 200, response.text
    await finished(run_id)
    assert len(value["hits"]) == 1 and not value["agent"].native_http_runner.runs
    print("重试等待取消验收通过：首个真实请求失败后取消30秒等待，没有继续重发请求。")
