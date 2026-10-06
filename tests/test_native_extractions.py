"""提取规则、变量生存期、真实Agent传递与历史响应权限验收。"""

import base64
import json
import httpx
import pytest
from pydantic import ValidationError
from framework.native_http.models import RequestSpec, FrozenRequest, FrozenCase
from framework.native_http.extraction_models import Extractor, PostProcessorConfig
from framework.native_http.extractions import (
    evaluate,
    matches,
    sample_values,
    scope_text,
    resolve_request,
)
from framework.native_http.engine import execute
from test_native_http_agent_e2e import native_lab, dispatch, finished, scope
from test_http_agent_e2e import lab


def rule(**kw):
    return Extractor(id="row", variableName="token", expression="$.values[*]", **kw)


def config(*rows):
    return PostProcessorConfig(
        processors=[dict(id="post", extractors=[r.model_dump() for r in rows])]
    )


def response(content='{"values":["甲","乙"]}'.encode("utf-8"), **kw):
    return httpx.Response(
        201,
        content=content,
        headers={"content-type": "application/json", "X-Lab": "value"},
        request=httpx.Request(
            "POST", "http://owned.test/echo", headers={"X-Input": "source"}
        ),
        **kw,
    )


@pytest.mark.parametrize(
    "value",
    [
        dict(variableType="ENVIRONMENT"),
        dict(variableName="${evil}"),
        dict(resultMatchingRuleNum=True),
        dict(resultMatchingRuleNum=0),
        dict(extractScope="UNKNOWN"),
        dict(expression=" "),
        dict(expression="x" * 201),
    ],
)
def test_contract_rejects_unconnected_environment_and_invalid_fields(value):
    with pytest.raises(ValidationError):
        Extractor.model_validate({**rule().model_dump(), **value})


def test_config_identity_budget_disabled_and_duplicate_names():
    with pytest.raises(ValidationError):
        config(rule(), rule())
    cfg = config(
        rule(),
        Extractor(id="other", variableName="token", expression="bad", enable=False),
    )
    variables = {}
    rows = evaluate(cfg, response(), variables)
    assert len(rows) == 1 and variables["token"] in {"甲", "乙"}
    cfg.processors[0].enable = False
    assert evaluate(cfg, response(), variables) == []
    assert RequestSpec().postProcessorConfig.processors == []


def test_json_modes_suffixes_cleanup_null_values_single_value_and_out_of_range():
    variables = {}
    r = rule(resultMatchingRule="ALL")
    rows = evaluate(config(r), response(), variables)
    assert rows[0]["matched"] and rows[0]["value"] == "甲,乙"
    assert variables == {
        "token": "",
        "token_1": "甲",
        "token_2": "乙",
        "token_matchNr": "2",
        "token_ALL": "甲,乙",
    }
    evaluate(config(r), response(b'{"values":[7]}'), variables)
    assert variables["token_1"] == "7" and "token_2" not in variables
    evaluate(config(r), response(b'{"values":[]}'), variables)
    assert (
        variables["token"] == variables["token_ALL"] == ""
        and variables["token_matchNr"] == "0"
        and "token_1" not in variables
    )
    r.resultMatchingRule = "SPECIFIC"
    r.resultMatchingRuleNum = 2
    evaluate(config(r), response(), variables)
    assert variables["token"] == "乙"
    r.resultMatchingRuleNum = 100
    evaluate(config(r), response(), variables)
    assert variables["token"] == ""
    evaluate(config(r), response(b'{"values":[false]}'), variables)
    assert variables["token"] == "false"  # JMeter单值分支忽略指定序号。
    r.expression = "$.values"
    assert sample_values(r, matches(r, response())) == ['["甲","乙"]']


@pytest.mark.parametrize(
    "scope,expression,expected",
    [
        ("BODY", r"<p>(.*?)</p>", "A&amp;B"),
        ("UNESCAPED_BODY", r"<p>(.*?)</p>", "A&B"),
        ("BODY_AS_DOCUMENT", r"(A&amp;B|A&B)", "A&B"),
        ("URL", r"/(echo)", "echo"),
        ("REQUEST_HEADERS", r"X-Input: (\w+)", "source"),
        ("RESPONSE_HEADERS", r"X-Lab: (\w+)", "value"),
        ("RESPONSE_CODE", r"(201)", "201"),
        ("RESPONSE_MESSAGE", r"(Created)", "Created"),
    ],
)
def test_regex_all_scope_values_and_first_group(scope, expression, expected):
    value = response(b"<p>A&amp;B</p>")
    value.headers["content-type"] = "text/html"
    value.request.headers["Cookie"] = "private=hidden"
    r = rule(
        extractType="REGEX",
        extractScope=scope,
        expressionMatchingRule="GROUP",
        resultMatchingRule="SPECIFIC",
    )
    r.expression = expression
    if scope == "RESPONSE_HEADERS":
        header_text = scope_text(r, value)
        assert header_text.startswith("HTTP/1.1 201 Created\n")
        assert header_text.endswith("\n") and "\r" not in header_text
    elif scope == "REQUEST_HEADERS":
        header_text = scope_text(r, value)
        assert "Cookie" not in header_text and "private=hidden" not in header_text
        assert header_text.endswith("\n") and "\r" not in header_text
    variables = {}
    out = evaluate(config(r), value, variables)
    assert out[0]["matched"] and variables["token"] == expected
    assert variables["token_g"] == "1" and variables["token_g1"] == expected


def test_regex_groups_all_cleanup_invalid_expression_timeout_and_bounded_matches():
    r = rule(
        extractType="REGEX", resultMatchingRule="ALL", expressionMatchingRule="GROUP"
    )
    r.expression = r"(\d+)"
    variables = {"token": "previous"}
    evaluate(config(r), response(b"11 22"), variables)
    assert (
        variables["token"] == "previous"
        and variables["token_1"] == "11"
        and variables["token_2_g1"] == "22"
    )
    evaluate(config(r), response(b"33"), variables)
    assert "token_2" not in variables and "token_2_g1" not in variables
    r.expression = "["
    out = evaluate(config(r), response(), variables)
    assert not out[0]["matched"] and "提取失败" in out[0]["message"]
    r.expression = r"(a+)+$"
    out = evaluate(config(r), response(b"a" * 30000 + b"!"), variables)
    assert "TimeoutError" in out[0]["message"]
    r.expression = "x"
    out = evaluate(config(r), response(b"x" * 1001), variables)
    assert "ValueError" in out[0]["message"]
    r.expression = "x"
    r.expressionMatchingRule = "GROUP"
    out = evaluate(config(r), response(b"x"), variables)
    assert "IndexError" in out[0]["message"]


def test_xpath_xml_html_scalar_and_external_resource_rejection():
    r = rule(extractType="X_PATH", resultMatchingRule="ALL")
    r.expression = "//v/text()"
    variables = {}
    evaluate(config(r), response(b"<root><v>7</v><v>8</v></root>"), variables)
    assert (
        variables["token"] == "7"
        and variables["token_2"] == "8"
        and variables["token_matchNr"] == "2"
    )
    r.resultMatchingRule = "SPECIFIC"
    r.resultMatchingRuleNum = 2
    evaluate(config(r), response(b"<root><v>7</v><v>8</v></root>"), variables)
    assert (
        variables["token"] == "8"
        and variables["token_1"] == "8"
        and "token_2" not in variables
    )
    r.responseFormat = "HTML"
    r.expression = "//p"
    assert sample_values(r, matches(r, response("<p>中文".encode("utf-8"))))
    r.responseFormat = "XML"
    r.expression = "count(//v)"
    assert sample_values(r, matches(r, response(b"<root><v/></root>"))) == ["1"]
    r.expression = "doc('file:///tmp/private')"
    assert (
        "ValueError"
        in evaluate(config(r), response(b"<root/>"), variables)[0]["message"]
    )
    r.expression = "//v"
    assert (
        "ValueError"
        in evaluate(
            config(r),
            response(
                b'<!DOCTYPE r [<!ENTITY x SYSTEM "file:///tmp/private">]><r><v>&x;</v></r>'
            ),
            variables,
        )[0]["message"]
    )


def test_resolve_request_keeps_frozen_template_and_file_identity_and_rest_encoding():
    frozen = FrozenRequest(
        name="输入",
        url="http://owned.test/{id}",
        method="POST",
        restParams=[dict(key="id", value="${token}")],
        query={"x": "前${token}"},
        headerParams=[dict(key="X-Value", value="${token}")],
        bodyType="json",
        body={"v": "${token}", "n": 7},
    )
    resolved = resolve_request(frozen, {"token": "中文/7"})
    assert resolved.url == "http://owned.test/%E4%B8%AD%E6%96%87%2F7"
    assert (
        resolved.body == {"v": "中文/7", "n": 7} and resolved.query["x"] == "前中文/7"
    )
    assert (
        frozen.body == {"v": "${token}", "n": 7}
        and frozen.restParams[0].value == "${token}"
    )
    assert resolve_request(frozen, {}).body["v"] == "${token}"
    frozen.body = {"${token}": {"${token}": "${token}"}}
    assert resolve_request(frozen, {"token": "key"}).body == {"key": {"key": "key"}}
    frozen.body = {"${token}": 1, "key": 2}
    with pytest.raises(ValueError, match="重复"):
        resolve_request(frozen, {"token": "key"})
    frozen.body = {str(i): "${token}" for i in range(9)}
    frozen.query = {}
    frozen.headerParams = []
    frozen.restParams = None
    frozen.url = "http://owned.test/echo"
    with pytest.raises(ValueError, match="总量"):
        resolve_request(frozen, {"token": "x" * (1024 * 1024)})


@pytest.mark.asyncio
async def test_execute_two_requests_pass_variables_without_cross_case_state():
    sent = []

    def handler(req):
        sent.append(json.loads(req.content))
        return response(b'{"values":[7]}')

    first = FrozenRequest(
        name="提取",
        url="http://owned.test/first",
        method="POST",
        bodyType="json",
        body={},
        postProcessorConfig=config(rule(resultMatchingRule="SPECIFIC")),
        responseAssertions=[
            dict(
                id="body",
                name="当前提取值断言",
                assertionType="RESPONSE_BODY",
                assertionBodyType="JSON_PATH",
                jsonPathAssertion={
                    "assertions": [
                        dict(
                            expression="$.values[0]",
                            condition="EQUALS",
                            expectedValue="${token}",
                            enable=True,
                        )
                    ]
                },
            )
        ],
    )
    second = FrozenRequest(
        name="引用",
        url="http://owned.test/second",
        method="POST",
        bodyType="json",
        body={"value": "${token}"},
    )
    out = await execute(
        FrozenCase(id="case", category="scenario", requests=[first, second]),
        transport=httpx.MockTransport(handler),
    )
    assert out["status"] == "passed" and sent == [{}, {"value": "7"}]
    assert (
        out["native_detail"]["steps"][0]["attempts"][0]["extractResults"][0]["value"]
        == "7"
    )
    await execute(
        FrozenCase(id="other", category="api", requests=[second]),
        transport=httpx.MockTransport(handler),
    )
    assert sent[-1] == {"value": "${token}"}


@pytest.mark.asyncio
async def test_real_agent_frozen_extraction_response_permissions_preview_and_following_step(
    native_lab,
):
    from database import SessionLocal
    from models.native_case import NativeCaseConfig
    from models.plan_orchestration import PlanRunItem
    from models import User, ProjectMember
    from core.security import create_access_token

    v = native_lab
    client = v["client"]
    project = v["api"]["projectId"]
    case = v["api"]["id"]
    endpoint = f"/api/v1/projects/{project}/native-cases/cases/{case}"
    assert (await client.get(endpoint + "/extraction-response")).json()["data"][
        "available"
    ] is False
    value = {
        "method": "POST",
        "bodyType": "json",
        "body": {"previous": "${token}"},
        "postProcessorConfig": config(rule(resultMatchingRule="SPECIFIC")).model_dump(),
    }
    value["postProcessorConfig"]["processors"][0]["extractors"][0][
        "expression"
    ] = "$.rows[0].value"
    await v["config"](v["api"], {"request": value}, revision=1)
    run = await scope(v, "scenario")
    with SessionLocal() as db:
        item = db.query(PlanRunItem).filter_by(run_id=run).one()
        assert (
            item.suite_snapshot["nativeCases"][0]["requests"][0]["postProcessorConfig"]
            == value["postProcessorConfig"]
        )
        row = db.get(NativeCaseConfig, case)
        row.parameters = {
            "request": {"method": "POST", "bodyType": "json", "body": {"changed": True}}
        }
        db.commit()
    await dispatch(run)
    await finished(run)
    assert v["hits"][-2]["body"] == {"previous": "${token}"} and v["hits"][-1][
        "body"
    ] == {"previous": "7"}
    # 单API实际执行后，读取该用例的历史响应；不把场景报告冒充单API响应。
    await v["config"](v["api"], {"request": value}, revision=2)
    run = await scope(v, "api")
    await dispatch(run)
    await finished(run)
    source = (await client.get(endpoint + "/extraction-response")).json()["data"]
    assert (
        source["available"] and source["response"]["extractResults"][0]["value"] == "7"
    )
    preview = {
        **value["postProcessorConfig"]["processors"][0]["extractors"][0],
        "expectedExecutionId": source["executionId"],
    }
    result = await client.post(endpoint + "/extraction-preview", json=preview)
    assert result.status_code == 200 and result.json()["data"]["values"] == ["7"]
    assert (
        await client.post(
            endpoint + "/extraction-preview",
            json={**preview, "expectedExecutionId": "stale"},
        )
    ).status_code == 409
    assert (
        await client.post(
            endpoint + "/extraction-preview", json={**preview, "expression": "["}
        )
    ).status_code == 422
    before = len(v["hits"])
    with SessionLocal() as db:
        for identifier in ["extract-reader", "extract-outsider"]:
            db.add(
                User(
                    id=identifier,
                    username=identifier,
                    email=identifier + "@example.test",
                    password_hash="隔离",
                )
            )
        db.flush()
        db.add(
            ProjectMember(project_id=project, user_id="extract-reader", role="viewer")
        )
        db.commit()
    auth = lambda who: {"Authorization": "Bearer " + create_access_token({"sub": who})}
    assert (
        await client.get(
            endpoint + "/extraction-response", headers=auth("extract-reader")
        )
    ).status_code == 200
    assert (
        await client.post(
            endpoint + "/extraction-preview",
            json=preview,
            headers=auth("extract-reader"),
        )
    ).status_code == 200
    assert (
        await client.get(
            endpoint + "/extraction-response", headers=auth("extract-outsider")
        )
    ).status_code == 403
    assert (
        await client.post(
            endpoint + "/extraction-preview",
            json=preview,
            headers=auth("extract-outsider"),
        )
    ).status_code == 403
    assert len(v["hits"]) == before
