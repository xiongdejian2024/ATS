"""官方四类响应断言的真实判定及配置冻结；全程MockTransport。"""

import asyncio
from types import SimpleNamespace
import logging
import httpx
import pytest
from pydantic import ValidationError
from framework.native_http.models import RequestSpec, FrozenCase, FrozenRequest
from framework.native_http.response_assertions import evaluate, compare
from framework.native_http.engine import execute
from test_native_http_execution import (
    native_workspace,
    workspace_http,
    plan_lab,
    configure,
)
from models import User, TestCase as Case
from models.native_case import NativeCaseConfig
from services.native_http_execution import freeze


def group(kind, **options):
    return {
        "id": kind,
        "name": "响应校验",
        "enable": True,
        "assertionType": kind,
        **options,
    }


def body(mode, rows, **options):
    key = {
        "JSON_PATH": "jsonPathAssertion",
        "XPATH": "xpathAssertion",
        "REGEX": "regexAssertion",
    }[mode]
    return group(
        "RESPONSE_BODY",
        assertionBodyType=mode,
        **{key: dict(assertions=rows, **options)}
    )


def checked(config, response, elapsed=0):
    return evaluate(
        RequestSpec(responseAssertions=config).responseAssertions, response, elapsed
    )


@pytest.mark.parametrize(
    "actual,condition,expected,result",
    [
        (1, "EQUALS", "1", True),
        (True, "EQUALS", "1", False),
        (1, "EQUALS", "1.0", False),
        ("1", "EQUALS", "1", True),
        ({"b": [1, True]}, "EQUALS", '{"b":[1,true]}', True),
        (None, "EQUALS", "null", True),
        ([1, 2], "NOT_EQUALS", "[1,2]", False),
        (2.5, "GT", "2", True),
        ("3", "GT_OR_EQUALS", "3", True),
        (-2, "LT", "-1", True),
        (2, "LT_OR_EQUALS", "2", True),
        ("中文值", "CONTAINS", "文", True),
        ("中文值", "NOT_CONTAINS", "空", True),
        ("开头结尾", "START_WITH", "开头", True),
        ("开头结尾", "END_WITH", "结尾", True),
        ("  ", "EMPTY", "", True),
        ([], "EMPTY", "", False),
        (False, "NOT_EMPTY", "", True),
        ("xx123xx", "REGEX", "[0-9]+", False),
        ("123", "REGEX", "[0-9]+", True),
        ("😀", "LENGTH_EQUALS", "2", True),
        ([1, 2], "LENGTH_EQUALS", "5", True),
        ("abc", "LENGTH_GT", "2", True),
        ("abc", "LENGTH_GT_OR_EQUALS", "3", True),
        ("abc", "LENGTH_LT", "4", True),
        ("abc", "LENGTH_LT_OR_EQUALS", "3", True),
    ],
)
def test_official_json_value_comparisons(actual, condition, expected, result):
    assert compare(actual, condition, expected) is result


@pytest.mark.parametrize(
    "config",
    [
        [group("UNKNOWN")],
        [group("RESPONSE_TIME", expectedValue=True)],
        [group("RESPONSE_TIME", expectedValue=-1)],
        [group("RESPONSE_CODE", condition="GT")],
        [group("RESPONSE_CODE"), group("RESPONSE_CODE", id="second")],
        [body("JSON_PATH", [dict(expression="$.a", enable=1)])],
        [body("XPATH", [dict(expression="")])],
    ],
)
def test_invalid_groups_rejected_without_input(config):
    with pytest.raises(ValidationError):
        RequestSpec(responseAssertions=config)


def test_actual_status_header_regex_and_negative_missing_header():
    response = httpx.Response(422, headers={"X-Result": "value-123"})
    rows = checked(
        [
            group("RESPONSE_CODE", condition="EQUALS", expectedValue="4[0-9]{2}"),
            group(
                "RESPONSE_HEADER",
                assertions=[
                    dict(
                        header="X-Result",
                        condition="EQUALS",
                        expectedValue="value-[0-9]+",
                    ),
                    dict(
                        header="X-Other",
                        condition="NOT_CONTAINS",
                        expectedValue="missing",
                    ),
                    dict(
                        header="X-Result",
                        condition="EQUALS",
                        expectedValue="",
                        enable=False,
                    ),
                ],
            ),
        ],
        response,
    )
    assert len(rows) == 3 and all(r["passed"] for r in rows)
    assert not checked(
        [group("RESPONSE_CODE", condition="NOT_EQUALS", expectedValue="4..")], response
    )[0]["passed"]
    assert (
        checked(
            [group("RESPONSE_HEADER", assertions=[dict(header="X", expectedValue="")])],
            response,
        )
        == []
    )


def test_jsonpath_filters_arrays_missing_null_and_full_regex():
    response = httpx.Response(
        200,
        json={"items": [{"id": 1}, {"id": 2}], "null": None, "text": "prefix42suffix"},
    )
    rows = checked(
        [
            body(
                "JSON_PATH",
                [
                    dict(expression="$.items[*].id", expectedValue="[1,2]"),
                    dict(expression="$.items[?(@.id>1)].id", expectedValue="[2]"),
                    dict(expression="$.null", expectedValue="null"),
                    dict(expression="$.text", condition="REGEX", expectedValue="42"),
                    dict(expression="$.missing", condition="EMPTY"),
                    dict(expression="$.missing", condition="UNCHECK"),
                    dict(expression="$.missing", enable=False),
                ],
            )
        ],
        response,
    )
    assert [r["passed"] for r in rows] == [True, True, True, False, False]
    assert all("actual" not in r and "expectedValue" not in r for r in rows)


def test_xml_xpath2_html_tolerant_and_regex_search():
    xml = httpx.Response(200, content=b"<root><item>one</item><item>two</item></root>")
    rows = checked(
        [
            body(
                "XPATH",
                [
                    dict(expression='exists(/root/item[text()="two"])'),
                    dict(expression="count(/root/item) eq 2"),
                    dict(expression="/root/missing"),
                ],
            )
        ],
        xml,
    )
    assert [r["passed"] for r in rows] == [True, True, False]
    html = httpx.Response(200, text="<html><body><p>open<b>bold")
    assert checked(
        [body("XPATH", [dict(expression="//p/b")], responseFormat="HTML")], html
    )[0]["passed"]
    assert checked([body("REGEX", [dict(expression="bold")])], html)[0]["passed"]
    assert not checked(
        [body("XPATH", [dict(expression="doc('http://127.0.0.1:1/no-send')")])], xml
    )[0]["passed"]
    entity = httpx.Response(
        200,
        content=b'<!DOCTYPE root [<!ENTITY x SYSTEM "file:///etc/passwd">]><root>&x;</root>',
    )
    assert not checked([body("XPATH", [dict(expression="/root")])], entity)[0]["passed"]


def test_time_boundary_bad_expression_and_regex_timeout(caplog):
    response = httpx.Response(200, text="a" * 10000 + "!")
    assert checked([group("RESPONSE_TIME", expectedValue=200)], response, 200)[0][
        "passed"
    ]
    assert not checked([group("RESPONSE_TIME", expectedValue=200)], response, 200.01)[
        0
    ]["passed"]
    with caplog.at_level(logging.ERROR, logger="XAT响应断言"):
        rows = checked(
            [body("REGEX", [dict(expression="("), dict(expression="(a|aa)+$")])],
            response,
        )
    assert [r["passed"] for r in rows] == [False, False]
    assert rows[1]["description"].endswith("TimeoutError")
    assert "Traceback" in caplog.text


@pytest.mark.asyncio
async def test_groups_execute_legacy_preserved_disabled_falls_back_and_retry():
    count = 0

    def target(request):
        nonlocal count
        count += 1
        return httpx.Response(200, json={"accepted": count > 1})

    config = [body("JSON_PATH", [dict(expression="$.accepted", expectedValue="true")])]
    request = FrozenRequest(
        url="http://loopback.test/",
        name="四类断言",
        responseAssertions=config,
        assertions=[dict(expected=200)],
    )
    result = await execute(
        FrozenCase(id="case", category="api", requests=[request], retryTimes=1),
        transport=httpx.MockTransport(target),
    )
    assert (
        count == 2
        and result["status"] == "passed"
        and len(result["steps"][0]["attempts"]) == 2
    )
    assert len(result["steps"][0]["assertions"]) == 2
    disabled = FrozenRequest(
        url="http://loopback.test/",
        name="停用",
        responseAssertions=[group("RESPONSE_CODE", enable=False, expectedValue="500")],
    )
    result = await execute(
        FrozenCase(id="off", category="api", requests=[disabled]),
        transport=httpx.MockTransport(lambda _: httpx.Response(500)),
    )
    assert result["status"] == "failed" and not result["steps"][0]["assertions"]


@pytest.mark.asyncio
async def test_response_time_excludes_legacy_assertion_evaluation(monkeypatch):
    from framework.native_http import engine

    clock = [0.0]
    original = engine.check
    monkeypatch.setattr(engine, "time", SimpleNamespace(monotonic=lambda: clock[0]))

    def legacy(assertion, response):
        clock[0] = 1.0
        return original(assertion, response)

    monkeypatch.setattr(engine, "check", legacy)
    request = FrozenRequest(
        name="网络耗时独立测量",
        url="http://loopback.test/",
        assertions=[dict(expected=200)],
        responseAssertions=[group("RESPONSE_TIME", expectedValue=5)],
    )
    result = await execute(
        FrozenCase(id="time", category="api", requests=[request]),
        transport=httpx.MockTransport(lambda _: httpx.Response(200)),
    )
    assert result["status"] == "passed"
    assert result["steps"][0]["duration"] == 1


def test_group_config_freeze_preserves_order_modes_and_disabled_rows(native_workspace):
    db, _, _ = native_workspace
    configure(db)
    groups = [
        group("RESPONSE_TIME", expectedValue=500),
        body(
            "XPATH",
            [dict(expression="/root/item", enable=False)],
            responseFormat="HTML",
        ),
    ]
    db.get(NativeCaseConfig, "case-0").parameters = {
        "request": {"responseAssertions": groups, "assertions": [{"expected": 200}]}
    }
    db.commit()
    result = freeze(db, db.get(Case, "case-0"), db.get(User, "owner"))["requests"][0]
    assert [g["assertionType"] for g in result["responseAssertions"]] == [
        "RESPONSE_TIME",
        "RESPONSE_BODY",
    ]
    assert result["responseAssertions"][1]["xpathAssertion"] == {
        "responseFormat": "HTML",
        "assertions": [{"expression": "/root/item", "enable": False}],
    }
    assert result["assertions"][0]["expected"] == 200
