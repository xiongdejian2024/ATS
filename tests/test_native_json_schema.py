"""Schema 是编辑元数据：预览、生成、权限和真实Agent正文冻结各自验收。"""

import json
import re
import base64
import pytest
from pydantic import ValidationError
from framework.native_http.models import RequestSpec
from framework.native_http.schema_models import JsonSchemaItem, JsonBodySchema
from services.native_json_schema import convert_schema
from test_native_http_agent_e2e import native_lab, dispatch, finished, scope
from test_http_agent_e2e import lab


def schema(**properties):
    return JsonSchemaItem(type="object", properties=properties)


def test_preview_examples_and_generation_priority_preserve_disabled_required():
    item = schema(
        text={
            "type": "string",
            "defaultValue": "默认",
            "enumValues": ["枚举"],
            "enable": False,
        },
        example={
            "type": "string",
            "example": "示例",
            "enumValues": ["另一值"],
            "maxLength": 1,
        },
        integer={"type": "integer", "defaultValue": 12},
        number={"type": "number", "example": "2.75"},
        flag={"type": "boolean", "defaultValue": True},
        empty={"type": "null"},
        nested={
            "type": "object",
            "properties": {
                "list": {
                    "type": "array",
                    "items": [{"type": "boolean", "example": "true"}],
                }
            },
        },
    )
    preview = json.loads(convert_schema(item, preview=True))
    assert preview == {
        "text": "string",
        "example": "示例",
        "integer": 0,
        "number": 2.75,
        "flag": False,
        "empty": None,
        "nested": {"list": [True]},
    }
    generated = json.loads(convert_schema(item, preview=False))
    assert generated == {**preview, "text": "枚举", "integer": 12}


def test_array_preview_ignores_bounds_generate_truncates_and_pads_strings():
    item = JsonSchemaItem(
        type="array",
        items=[
            {"type": "integer", "example": "7"},
            {"type": "string", "example": "second"},
        ],
        maxItems=1,
    )
    assert json.loads(convert_schema(item, preview=True)) == [7, "second"]
    assert json.loads(convert_schema(item, preview=False)) == [7]
    item.maxItems = 3
    item.minItems = 3
    result = json.loads(convert_schema(item, preview=False))
    assert result[:2] == [7, "second"] and len(result[2]) == 8


def test_generation_bounds_regex_defaults_enums_and_format_metadata():
    item = schema(
        trimmed={"type": "string", "enumValues": ["ABCDE"], "maxLength": 2},
        padded={"type": "string", "defaultValue": "X", "minLength": 4, "maxLength": 4},
        random={"type": "string", "minLength": 5, "maxLength": 5, "format": "email"},
        pattern={
            "type": "string",
            "pattern": "[A-Z]{3}[0-9]{2}",
            "defaultValue": "不能优先",
        },
        integer={"type": "integer", "minimum": 4, "maximum": 5},
        fixed={"type": "integer", "minimum": 9, "maximum": 9},
        number={"type": "number", "minimum": 1.2, "maximum": 2.5},
        enumNumber={"type": "number", "enumValues": ["12.25"]},
        large={"type": "number"},
    )
    result = json.loads(convert_schema(item, preview=False))
    assert result["trimmed"] == "AB"
    assert result["padded"].startswith("X") and len(result["padded"]) == 4
    assert len(result["random"]) == 5 and re.fullmatch(
        "[A-Z]{3}[0-9]{2}", result["pattern"]
    )
    assert (
        result["integer"] == 4
        and result["fixed"] == 9
        and 1.2 <= result["number"] <= 2.5
    )
    assert result["enumNumber"] == 12.25 and isinstance(result["large"], float)


@pytest.mark.parametrize(
    "value",
    [
        {"type": "string"},
        {"type": "object", "properties": {"": {"type": "string"}}},
        {"type": "object", "required": ["missing"]},
        {"type": "array", "items": {"type": "string"}},
        {"type": "array", "minItems": 3, "maxItems": 2},
        {
            "type": "object",
            "properties": {"bad": {"type": "string", "minLength": True}},
        },
        {
            "type": "object",
            "properties": {"bad": {"type": "string", "$ref": "http://external.test/"}},
        },
        {
            "type": "object",
            "properties": {"bad": {"type": "number", "minimum": float("nan")}},
        },
        {
            "type": "object",
            "properties": {"bad": {"type": "integer", "enumValues": []}},
        },
    ],
)
def test_schema_contract_rejects_bad_tree_and_unknown_external_references(value):
    with pytest.raises(ValidationError):
        JsonBodySchema(jsonSchema=value)


def test_schema_budget_and_request_keeps_independent_json_body():
    value = {"type": "object", "properties": {}}
    current = value
    for _ in range(22):
        child = {"type": "object", "properties": {}}
        current["properties"]["next"] = child
        current = child
    with pytest.raises(ValidationError):
        JsonBodySchema(jsonSchema=value)
    req = RequestSpec(
        bodyType="json",
        body={"send": "原正文"},
        jsonBody={
            "enableJsonSchema": True,
            "jsonSchema": {
                "type": "object",
                "properties": {"other": {"type": "string", "example": "预览"}},
            },
        },
    )
    assert req.body == {"send": "原正文"}
    with pytest.raises(ValueError):
        convert_schema(
            schema(bad={"type": "integer", "example": "${value}"}), preview=False
        )


@pytest.mark.asyncio
async def test_schema_permissions_preview_generation_version_freeze_and_real_agent(
    native_lab,
):
    from database import SessionLocal
    from models import User, ProjectMember
    from models.plan_orchestration import PlanRunItem
    from models.native_case import NativeCaseConfig
    from core.security import create_access_token

    v = native_lab
    client = v["client"]
    project = v["api"]["projectId"]
    endpoint = f"/api/v1/projects/{project}/native-cases/json-schema/convert"
    value = {
        "type": "object",
        "properties": {
            "value": {"type": "integer", "defaultValue": 7},
            "label": {
                "type": "string",
                "defaultValue": "中文正文",
                "minLength": 4,
                "maxLength": 4,
            },
        },
    }
    preview = await client.post(
        endpoint, json={"jsonSchema": value, "action": "preview"}
    )
    generated = await client.post(
        endpoint, json={"jsonSchema": value, "action": "generate"}
    )
    assert preview.status_code == generated.status_code == 200
    assert json.loads(preview.json()["data"]["jsonValue"]) == {
        "value": 0,
        "label": "string",
    }
    body = json.loads(generated.json()["data"]["jsonValue"])
    assert body == {"value": 7, "label": "中文正文"}
    assert (
        await client.post(
            endpoint,
            json={"jsonSchema": {"type": "object", "$ref": "file:///tmp/private"}},
        )
    ).status_code == 422
    with SessionLocal() as db:
        for identifier in ["schema-reader", "schema-outsider"]:
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
            ProjectMember(project_id=project, user_id="schema-reader", role="viewer")
        )
        db.commit()
    headers = lambda sub: {
        "Authorization": "Bearer " + create_access_token({"sub": sub})
    }
    assert (
        await client.post(
            endpoint, json={"jsonSchema": value}, headers=headers("schema-reader")
        )
    ).status_code == 200
    assert (
        await client.post(
            endpoint, json={"jsonSchema": value}, headers=headers("schema-outsider")
        )
    ).status_code == 403
    config = {
        "request": {
            "method": "POST",
            "bodyType": "json",
            "body": body,
            "jsonBody": {"enableJsonSchema": True, "jsonSchema": value},
            "assertions": [{"expected": 201}],
        }
    }
    await v["config"](v["api"], config, revision=1)
    stored = (
        await client.get(
            f'/api/v1/projects/{project}/native-cases/cases/{v["api"]["id"]}'
        )
    ).json()["data"]
    assert stored["parameters"]["request"]["jsonBody"]["jsonSchema"] == value
    run_id = await scope(v, "api")
    with SessionLocal() as db:
        frozen = (
            db.query(PlanRunItem)
            .filter_by(run_id=run_id)
            .one()
            .suite_snapshot["nativeCases"][0]["requests"][0]
        )
        assert frozen.get("jsonBody") is None and frozen["body"] == body
        row = db.get(NativeCaseConfig, v["api"]["id"])
        row.parameters = {
            "request": {"bodyType": "json", "body": {"after": "不能覆盖已冻结正文"}}
        }
        db.commit()
    await dispatch(run_id)
    await finished(run_id)
    with SessionLocal() as db:
        item = db.query(PlanRunItem).filter_by(run_id=run_id).one()
        assert item.status == "completed"
        from models.test_suite import TestSuiteExecution
        from services.suite_results import result_id

        execution = db.get(
            TestSuiteExecution, result_id(item.execution_id, v["api"]["id"])
        )
        assert execution.result == "passed"
        detail = execution.native_detail["steps"][0]["attempts"][0]["request"]["body"]
        assert json.loads(base64.b64decode(detail["base64"])) == body
