"""实际HTTP详情采集、迁移及冻结身份读取；MockTransport和隔离数据库。"""

import base64
import importlib.util
from pathlib import Path
import httpx
import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import create_engine, text, inspect
from framework.native_http.engine import execute
from framework.native_http.models import FrozenCase, FrozenRequest
from framework.native_http.result_details import NativeDetail, BODY_LIMIT


@pytest.mark.asyncio
async def test_actual_exchange_assertions_retry_and_no_sensitive_log():
    hits = []

    def target(request):
        hits.append(request)
        return httpx.Response(
            500 if len(hits) == 1 else 200,
            headers=[
                ("X-Test", "real-header"),
                ("Set-Cookie", "one=1"),
                ("Set-Cookie", "two=2"),
            ],
            json={"value": len(hits), "actual": "实际响应"},
        )

    req = FrozenRequest(
        name="实际交换",
        url="http://loopback.test/item?q=real",
        method="POST",
        headers={"Authorization": "Bearer report-secret"},
        bodyType="json",
        body={"input": "真实请求"},
        assertions=[{"expected": 200}],
        responseAssertions=[
            {
                "id": "body",
                "name": "响应体",
                "assertionType": "RESPONSE_BODY",
                "jsonPathAssertion": {
                    "assertions": [{"expression": "$.value", "expectedValue": "2"}]
                },
            }
        ],
    )
    result = await execute(
        FrozenCase(id="case", category="api", requests=[req], retryTimes=1),
        transport=httpx.MockTransport(target),
    )
    details = result["native_detail"]
    assert details["totalSteps"] == 1 and details["omittedSteps"] == 0
    step = details["steps"][0]
    assert [a["result"] for a in step["attempts"]] == ["failed", "passed"]
    first, last = step["attempts"]
    assert (
        first["response"]["statusCode"] == 500 and last["response"]["statusCode"] == 200
    )
    assert [h for h in last["response"]["headers"] if h[0].lower() == "set-cookie"] == [
        ["Set-Cookie", "one=1"],
        ["Set-Cookie", "two=2"],
    ]
    assert b"input" in base64.b64decode(last["request"]["body"]["base64"])
    assert (
        last["assertions"][1]["actualValue"] == "2"
        and last["assertions"][1]["expectedValue"] == "2"
    )
    assert any(
        h == ["Authorization", "Bearer report-secret"]
        for h in last["request"]["headers"]
    )
    assert all(
        v not in result["log"]
        for v in [
            "report-secret",
            "真实请求",
            "实际响应",
            "real-header",
            "Authorization",
        ]
    )
    assert (
        NativeDetail.model_validate(details)
        .steps[0]
        .attempts[1]
        .response.body.byteLength
        > 0
    )


@pytest.mark.asyncio
async def test_redirect_binary_capture_and_timeout_request_are_actual():
    def target(req):
        return (
            httpx.Response(302, headers={"location": "/binary"})
            if req.url.path == "/start"
            else httpx.Response(
                200,
                content=bytes(range(256)) * (BODY_LIMIT // 256 + 1),
                headers={"content-type": "application/octet-stream"},
            )
        )

    req = FrozenRequest(
        name="重定向", url="http://loopback.test/start", followRedirects=True
    )
    result = await execute(
        FrozenCase(id="case", category="api", requests=[req]),
        transport=httpx.MockTransport(target),
    )
    attempt = result["native_detail"]["steps"][0]["attempts"][0]
    assert (
        attempt["request"]["url"].endswith("/binary") and len(attempt["redirects"]) == 1
    )
    assert (
        attempt["redirects"][0]["response"]["statusCode"] == 302
        and attempt["redirects"][0]["response"]["responseTimeMs"] is None
    )
    capture = attempt["response"]["body"]
    assert (
        capture["truncated"]
        and capture["capturedBytes"] == BODY_LIMIT
        and capture["byteLength"] > BODY_LIMIT
    )
    assert base64.b64decode(capture["base64"]) == bytes(range(256)) * (
        BODY_LIMIT // 256
    )

    def timeout(req):
        raise httpx.ReadTimeout("local-only", request=req)

    failed = await execute(
        FrozenCase(id="failed", category="api", requests=[req]),
        transport=httpx.MockTransport(timeout),
    )
    attempt = failed["native_detail"]["steps"][0]["attempts"][0]
    assert (
        attempt["request"]["url"].endswith("/start")
        and attempt["response"] is None
        and attempt["result"] == "error"
    )


@pytest.mark.asyncio
async def test_missing_json_and_parse_failure_keep_failed_detail():
    req = FrozenRequest(
        name="缺失值",
        url="http://loopback.test/",
        assertions=[{"source": "json", "path": ["missing"], "expected": None}],
    )
    result = await execute(
        FrozenCase(id="case", category="api", requests=[req]),
        transport=httpx.MockTransport(lambda _: httpx.Response(200, text="not-json")),
    )
    assertion = result["native_detail"]["steps"][0]["attempts"][0]["assertions"][0]
    assert (
        not assertion["passed"]
        and not assertion["actualPresent"]
        and assertion["message"] == "响应不是有效JSON"
    )


def test_legacy_sqlite_upgrade_preserves_data_and_is_idempotent(tmp_path):
    spec = importlib.util.spec_from_file_location(
        "http_detail_upgrade",
        Path(__file__).resolve().parents[1] / "scripts/upgrade_native_http_detail.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    engine = create_engine("sqlite:///" + str(tmp_path / "old.db"))
    with engine.begin() as conn:
        conn.execute(
            text(
                "CREATE TABLE test_suite_executions (id VARCHAR(36) PRIMARY KEY, log_output TEXT, result VARCHAR(50))"
            )
        )
        conn.execute(
            text("INSERT INTO test_suite_executions VALUES ('old','原日志','passed')")
        )
    assert module.upgrade(False, engine) == [
        "native_detail"
    ] and "native_detail" not in {
        c["name"] for c in inspect(engine).get_columns("test_suite_executions")
    }
    assert (
        module.upgrade(True, engine) == ["native_detail"]
        and module.upgrade(True, engine) == []
    )
    with engine.connect() as conn:
        assert conn.execute(
            text("SELECT id,log_output,result,native_detail FROM test_suite_executions")
        ).one() == ("old", "原日志", "passed", None)
    engine.dispose()


def test_details_reject_inconsistent_body_and_steps():
    from framework.native_http.result_details import body, Body

    capture = body(b"actual", "text/plain")
    capture["capturedBytes"] = 1
    with pytest.raises(ValidationError):
        Body.model_validate(capture)
    with pytest.raises(ValidationError):
        NativeDetail(totalSteps=2, omittedSteps=0, steps=[])


def test_missing_header_and_capture_budget_are_explicit(monkeypatch):
    from framework.native_http import result_details
    from framework.native_http.response_assertions import evaluate
    from framework.native_http.response_assertion_models import HeaderAssertion

    sink = []
    group = HeaderAssertion(
        id="missing",
        name="缺失响应头",
        assertionType="RESPONSE_HEADER",
        assertions=[{"header": "X-Missing", "expectedValue": "expected"}],
    )
    evaluate([group], httpx.Response(200), 1, sink)
    assert not sink[0]["actualPresent"] and not sink[0]["passed"]
    assert result_details.headers_truncated(
        httpx.Headers({"X-Value": "é" * 11000}, encoding="latin-1")
    )
    steps = [
        dict(
            index=i,
            name="响应",
            method="GET",
            result="skipped",
            duration=0.0,
            attempts=[],
        )
        for i in range(20)
    ]
    monkeypatch.setattr(result_details, "DETAIL_LIMIT", 700)
    value = result_details.bounded_detail(steps)
    assert (
        value["omittedSteps"] > 0 and len(value["steps"]) + value["omittedSteps"] == 20
    )
    import json

    assert len(json.dumps(value, ensure_ascii=False).encode()) <= 700


from test_native_http_agent_e2e import native_lab, lab, dispatch, finished, scope


@pytest.mark.asyncio
async def test_real_center_detail_permission_frozen_identity_legacy_and_deleted(
    native_lab,
):
    from database import SessionLocal
    from models.plan_orchestration import PlanRunItem
    from models.test_suite import TestSuiteExecution
    from services.suite_results import result_id

    value = native_lab
    run_id = await scope(value, "api")
    from api.v1.websocket import handle_test_suite_result

    with SessionLocal() as db:
        item = db.query(PlanRunItem).filter_by(run_id=run_id).one()
        malformed = dict(
            execution_id=item.execution_id,
            suite_id=item.suite_id,
            case_id=value["api"]["id"],
            result="passed",
            native_detail={
                "version": 1,
                "totalSteps": 1,
                "omittedSteps": 0,
                "steps": [],
            },
        )
        assert (
            await handle_test_suite_result(db, item.environment_id, malformed) is False
        )
        assert (
            db.get(TestSuiteExecution, result_id(item.execution_id, value["api"]["id"]))
            is None
        )
    await dispatch(run_id)
    await finished(run_id)
    with SessionLocal() as db:
        item = db.query(PlanRunItem).filter_by(run_id=run_id).one()
        execution_id = item.execution_id
        suite_id = item.suite_id
        identifier = result_id(execution_id, value["api"]["id"])
        row = db.get(TestSuiteExecution, identifier)
        assert (
            row.native_detail
            and row.native_detail["steps"][0]["attempts"][0]["response"]["statusCode"]
            == 201
        )
        original_detail = row.native_detail
        malformed["native_detail"] = None
        assert (
            await handle_test_suite_result(db, item.environment_id, malformed) is True
        )
        db.refresh(row)
        assert row.native_detail == original_detail
    record = (
        value["agent"].work_dir
        / "suites"
        / suite_id
        / "executions"
        / execution_id
        / "native-run.json"
    )
    assert record.stat().st_mode & 0o777 == 0o600
    path = f'/api/v1/plan-orchestration/runs/{run_id}/native-cases/{execution_id}/{value["api"]["id"]}/detail'
    response = await value["client"].get(path)
    assert response.status_code == 200, response.text
    data = response.json()["data"]
    assert (
        data["available"]
        and len(data["detail"]["steps"][0]["attempts"][0]["assertions"]) == 7
    )
    assert (
        base64.b64decode(
            data["detail"]["steps"][0]["attempts"][0]["request"]["body"]["base64"]
        )
        == b'{"number":7}'
    )
    async with httpx.AsyncClient(base_url=value["client"].base_url) as anonymous:
        response = await anonymous.get(path)
        assert response.status_code == 401
    from models import User
    from core.security import create_access_token
    from uuid import uuid4

    outsider_id = str(uuid4())
    with SessionLocal() as db:
        db.add(
            User(
                id=outsider_id,
                username="报告外部用户",
                email="report-outsider@example.test",
                password_hash="测试",
            )
        )
        db.commit()
    async with httpx.AsyncClient(
        base_url=value["client"].base_url,
        headers={
            "Authorization": "Bearer " + create_access_token({"sub": outsider_id})
        },
    ) as outsider:
        assert (await outsider.get(path)).status_code == 403
    bad = await value["client"].get(path.replace(execution_id, "unselected-execution"))
    assert bad.status_code == 404
    bad = await value["client"].get(
        path.replace(value["api"]["id"], value["scene"]["id"])
    )
    assert bad.status_code == 404
    with SessionLocal() as db:
        row = db.get(TestSuiteExecution, identifier)
        row.native_detail = None
        db.commit()
    response = await value["client"].get(path)
    assert (
        response.status_code == 200
        and response.json()["data"]["available"] is False
        and response.json()["data"]["native"] is True
    )
    response = await value["client"].delete(
        f'/api/v1/plan-orchestration/projects/{value["api"]["projectId"]}/reports/PLAN/{run_id}'
    )
    assert response.status_code == 200, response.text
    assert (await value["client"].get(path)).status_code == 404
    with SessionLocal() as db:
        assert db.get(TestSuiteExecution, identifier)
