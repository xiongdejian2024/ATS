"""官方变量比较、执行上下文、实际Agent可靠回传与项目权限验收。"""

import httpx
import pytest
from pydantic import ValidationError
from framework.native_http.models import RequestSpec, FrozenRequest, FrozenCase
from framework.native_http.response_assertions import evaluate
from framework.native_http.variable_assertions import compare_variable, java_double
from framework.native_http.engine import execute
from test_native_http_agent_e2e import native_lab, dispatch, finished, scope
from test_http_agent_e2e import lab


def group(rows, **options):
    return dict(id="vars", name="变量断言", assertionType="VARIABLE", variableAssertionItems=rows, **options)


def row(name="token", condition="EQUALS", expected="7", **options):
    return dict(variableName=name, condition=condition, expectedValue=expected, **options)


@pytest.mark.parametrize("actual,condition,expected,passed", [
    ("7", "EQUALS", "7", True), ("7", "EQUALS", "7.0", False),
    (None, "EQUALS", "", False), (None, "NOT_EQUALS", "", True),
    (None, "REGEX", ".*", False), ("7", "NOT_EQUALS", "8", True),
    ("1e3", "GT", "999", True), ("0x1.0p3", "GT_OR_EQUALS", "8", True),
    ("1f", "LT", "2D", True), ("-2", "LT_OR_EQUALS", "-2.0", True),
    ("中文", "CONTAINS", "文", True), ("中文", "NOT_CONTAINS", "空", True),
    ("开头结尾", "START_WITH", "开头", True), ("开头结尾", "END_WITH", "结尾", True),
    ("", "EMPTY", "", True), ("  ", "EMPTY", "", False),
    ("  ", "NOT_EMPTY", "", True), ("", "NOT_EMPTY", "", False),
    ("123", "REGEX", "[0-9]+", True), ("xx123xx", "REGEX", "[0-9]+", False),
    ("😀", "LENGTH_EQUALS", "2", True), ("abc", "LENGTH_GT", "2.5", True),
    ("abc", "LENGTH_GT_OR_EQUALS", "3.0", True), ("abc", "LENGTH_LT", "3.5", True),
    ("abc", "LENGTH_LT_OR_EQUALS", "3D", True),
    ("NaN", "GT", "0", False), ("Infinity", "GT", "1", True),
])
def test_official_groovy_variable_comparisons(actual, condition, expected, passed):
    assert compare_variable(actual, condition, expected) is passed


@pytest.mark.parametrize("value", ["1_000", "１２", "nan", "inf", "1 2", "", "\u00a01", "0x1"])
def test_java_double_rejects_python_only_or_invalid_formats(value):
    with pytest.raises(ValueError):
        java_double(value)


def test_java_double_hex_overflow_and_signed_zero():
    assert java_double(" +0x1.8p2F ") == 6
    assert java_double("0x1p99999") == float("inf")
    assert java_double("-0x1p99999") == -float("inf")
    assert java_double("-0") == 0


@pytest.mark.parametrize("options", [
    dict(variableName=" "), dict(variableName="a\nb"), dict(condition="UNKNOWN"),
    dict(enable=1), dict(expectedValue=None), dict(extra="错误"), dict(variableName="x" * 256),
])
def test_strict_variable_rule_validation(options):
    with pytest.raises(ValidationError):
        RequestSpec(responseAssertions=[group([{**row(), **options}])])


def test_five_group_contract_limits_and_duplicate_guard():
    spec = RequestSpec(responseAssertions=[
        dict(id="code", name="状态", assertionType="RESPONSE_CODE"),
        dict(id="header", name="头", assertionType="RESPONSE_HEADER"),
        dict(id="body", name="正文", assertionType="RESPONSE_BODY"),
        dict(id="time", name="时间", assertionType="RESPONSE_TIME"), group([row()]),
    ])
    assert len(spec.responseAssertions) == 5
    with pytest.raises(ValidationError):
        RequestSpec(responseAssertions=[group([row()]), group([row()], enable=False)])
    with pytest.raises(ValidationError):
        RequestSpec(responseAssertions=[group([row()] * 101)])


def test_missing_variable_is_not_empty_and_records_errors_with_stack(caplog):
    rules = [row(condition=c, expected="") for c in ["EQUALS", "NOT_EQUALS", "REGEX", "EMPTY", "NOT_EMPTY", "CONTAINS"]]
    details = []
    result = evaluate(RequestSpec(responseAssertions=[group(rules)]).responseAssertions, httpx.Response(200), 0, details, {})
    assert [r["passed"] for r in result] == [False, True, False, False, False, False]
    assert all(not d["actualPresent"] for d in details)
    assert all(d["actualValue"] == "null" for d in details)
    assert "变量未定义" in caplog.text and "Traceback" in caplog.text
    assert "评估失败" in details[3]["message"]


def test_disabled_and_uncheck_skip_empty_regex_errors_and_timeouts(caplog):
    rules = [row(condition="UNCHECK"), row(enable=False), row(condition="REGEX", expected="["), row(condition="REGEX", expected="(a+)+$")]
    groups = RequestSpec(responseAssertions=[group(rules)]).responseAssertions
    assert evaluate(RequestSpec(responseAssertions=[group(rules, enable=False)]).responseAssertions, httpx.Response(200), 0, variables={"token":"7"}) == []
    result = evaluate(groups, httpx.Response(200), 0, variables={"token": "a" * 30000 + "!"})
    assert len(result) == 2 and all(not r["passed"] for r in result)
    assert "TimeoutError" in caplog.text and "Traceback" in caplog.text


@pytest.mark.asyncio
async def test_current_extraction_derived_values_templates_and_case_isolation():
    extract = dict(processors=[dict(id="post", extractors=[dict(id="e", variableName="token", expression="$.values[*]", resultMatchingRule="ALL")])])
    assertions = [group([row("token_ALL", expected="7,8"), row("token_2", expected="${token_2}"), row("token_matchNr", expected="2")])]
    first = FrozenRequest(name="提取并校验", url="http://owned.test/first", postProcessorConfig=extract, responseAssertions=assertions)
    second = FrozenRequest(name="继承变量", url="http://owned.test/second", responseAssertions=[group([row("token_1", expected="7")])])
    original = first.model_dump()
    transport = httpx.MockTransport(lambda _: httpx.Response(200, json={"values":[7,8]}))
    result = await execute(FrozenCase(id="scene", category="scenario", requests=[first,second]), transport=transport)
    assert result["status"] == "passed" and first.model_dump() == original
    detail = result["native_detail"]["steps"][0]["attempts"][0]["assertions"]
    assert all(d["actualPresent"] and d["assertionType"] == "VARIABLE" for d in detail)
    assert detail[1]["actualValue"] == detail[1]["expectedValue"] == "8"
    isolated = await execute(FrozenCase(id="other", category="api", requests=[second]), transport=transport)
    assert isolated["status"] == "failed"
    assert not isolated["native_detail"]["steps"][0]["attempts"][0]["assertions"][0]["actualPresent"]


@pytest.mark.asyncio
async def test_real_agent_frozen_variable_assertions_report_failure_and_permissions(native_lab):
    from database import SessionLocal
    from models.native_case import NativeCaseConfig
    from models.plan_orchestration import PlanRunItem
    from models import User, ProjectMember
    from core.security import create_access_token

    v = native_lab;client=v["client"];project=v["api"]["projectId"];case=v["api"]["id"]
    endpoint=f"/api/v1/projects/{project}/native-cases/cases/{case}"
    config={"request":{"method":"POST","bodyType":"json","body":{"previous":"${token}"},"postProcessorConfig":{"processors":[{"id":"post","extractors":[{"id":"e","variableName":"token","expression":"$.rows[0].value"}]}]},"responseAssertions":[group([row(expected="${token}"),row("missing",condition="NOT_EQUALS",expected="")])]}}
    await v["config"](v["api"],config,revision=1)
    run=await scope(v,"scenario")
    with SessionLocal() as db:
        item=db.query(PlanRunItem).filter_by(run_id=run).one();frozen=item.suite_snapshot["nativeCases"][0]["requests"][0]
        assert frozen["responseAssertions"][0]["variableAssertionItems"][0]["expectedValue"]=="${token}"
        stored=db.get(NativeCaseConfig,case);stored.parameters={"request":{"responseAssertions":[group([row(expected="错误")])]}};db.commit()
    await dispatch(run);await finished(run)
    with SessionLocal() as db:
        item=db.query(PlanRunItem).filter_by(run_id=run).one();assert item.status=="completed";execution=item.execution_id
    report=(await client.get(f"/api/v1/plan-orchestration/runs/{run}/native-cases/{execution}/{v['scene']['id']}/detail")).json()["data"]
    assert report["result"] == "passed"
    assert report["detail"]["steps"][0]["attempts"][0]["assertions"][0]["actualValue"]=="7"
    assert v["hits"][-1]["body"]=={"previous":"7"}
    config["request"]["responseAssertions"]=[group([row(expected="8")])]
    await v["config"](v["api"],config,revision=2);run=await scope(v,"api");await dispatch(run);await finished(run)
    with SessionLocal() as db:
        item=db.query(PlanRunItem).filter_by(run_id=run).one();assert item.status=="failed";execution=item.execution_id
    report=(await client.get(f"/api/v1/plan-orchestration/runs/{run}/native-cases/{execution}/{case}/detail")).json()["data"]
    assert report["result"] == "failed"
    assertion=report["detail"]["steps"][0]["attempts"][0]["assertions"][0]
    assert assertion["actualValue"]=="7" and assertion["expectedValue"]=="8" and not assertion["passed"]
    with SessionLocal() as db:
        db.add_all([User(id=i,username=i,email=i+"@example.test",password_hash="隔离") for i in ["var-reader","var-outsider"]]);db.flush();db.add(ProjectMember(project_id=project,user_id="var-reader",role="viewer"));db.commit()
    auth=lambda who:{"Authorization":"Bearer "+create_access_token({"sub":who})}
    assert (await client.get(endpoint,headers=auth("var-reader"))).status_code==200
    payload={"state":"DONE","expectedRevision":3,"parameters":config}
    assert (await client.put(endpoint,json=payload,headers=auth("var-reader"))).status_code==403
    assert (await client.get(endpoint,headers=auth("var-outsider"))).status_code==403
    invalid={**payload,"parameters":{"request":{"responseAssertions":[group([row(name=" ")])]}}}
    assert (await client.put(endpoint,json=invalid)).status_code==422
