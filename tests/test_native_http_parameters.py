"""参数编辑与真实HTTP协议验收；只使用MockTransport，不连接外部目标。"""

import base64
import json
import httpx
import pytest
from pydantic import ValidationError
from framework.native_http.models import RequestSpec, FrozenRequest, FrozenCase
from framework.native_http.engine import execute
from framework.native_http.parameters import path_parameters, arguments
from test_native_http_execution import (
    native_workspace,
    workspace_http,
    plan_lab,
    configure,
)
from models import TestCase as Case, User
from models.native_case import NativeCaseConfig, ApiDefinition
from services.native_http_execution import freeze


@pytest.mark.parametrize(
    "config",
    [
        {"queryParams": [{"key": "same"}, {"key": "same"}]},
        {"headerParams": [{"key": "X-Test"}, {"key": "x-test"}]},
        {"queryParams": [{"key": ""}]},
        {"queryParams": [{"key": "q", "lengthRange": [3, 2]}]},
        {"queryParams": [{"key": "q", "enable": 1}]},
        {"queryParams": [{"key": "q"}], "query": {"q": "legacy"}},
        {"formParams": [{"key": "q"}]},
        {
            "authConfig": {
                "authType": "UNKNOWN",
                "basicAuth": {"password": "不得出现在错误里"},
            }
        },
        {"connectTimeoutMs": True},
        {"responseTimeoutMs": 600001},
    ],
)
def test_invalid_parameter_table_does_not_leak_input(config):
    with pytest.raises(ValidationError) as failure:
        RequestSpec.model_validate(config)
    assert "不得出现在错误里" not in str(failure.value)


@pytest.mark.asyncio
async def test_enabled_tables_actual_encoding_headers_form_and_basic_auth():
    seen = []

    def target(request):
        seen.append(request)
        return httpx.Response(200)

    request = FrozenRequest(
        url="http://loopback.test/target?existing=keep&q=old",
        name="参数表请求",
        method="POST",
        queryParams=[
            {"key": "q", "value": "中文 空格"},
            {"key": "plain", "value": "/keep", "encode": False},
            {"key": "unicode", "value": "中文 空格", "encode": False},
            {"key": "disabled", "value": "never", "enable": False},
        ],
        headerParams=[
            {"key": "X-Enabled", "value": "yes"},
            {"key": "X-Disabled", "value": "never", "enable": False},
        ],
        bodyType="form",
        body={},
        formParams=[
            {"key": "field", "value": "中文"},
            {"key": "hidden", "value": "never", "enable": False},
        ],
        authConfig={
            "authType": "BASIC",
            "basicAuth": {"userName": "reader", "password": "local-only"},
        },
    )
    result = await execute(
        FrozenCase(id="case", category="api", requests=[request]),
        transport=httpx.MockTransport(target),
    )
    assert result["status"] == "passed"
    sent = seen[0]
    assert sent.url.params["existing"] == "keep" and sent.url.params.get_list("q") == [
        "中文 空格"
    ]
    assert b"plain=/keep" in sent.url.query and "disabled" not in sent.url.params
    assert sent.url.params["unicode"] == "中文 空格" and b"%20" in sent.url.query
    assert sent.headers["X-Enabled"] == "yes" and "X-Disabled" not in sent.headers
    assert (
        sent.headers["Authorization"]
        == "Basic " + base64.b64encode(b"reader:local-only").decode()
    )
    assert httpx.QueryParams(sent.content.decode()) == httpx.QueryParams(
        {"field": "中文"}
    )
    assert all(
        secret not in result["log"]
        for secret in ["local-only", "Authorization", "X-Enabled", "never"]
    )


@pytest.mark.asyncio
async def test_digest_handshake_is_per_request_and_no_auth_is_empty():
    seen = []

    def target(request):
        # httpx摘要握手复用请求对象；观察时复制头部，避免事后变更覆盖首次请求证据。
        seen.append(dict(request.headers))
        if len(seen) == 1:
            return httpx.Response(
                401,
                headers={
                    "WWW-Authenticate": 'Digest realm="lab", nonce="abc", qop="auth", algorithm=MD5'
                },
            )
        return httpx.Response(200)

    config = {
        "authType": "DIGEST",
        "digestAuth": {"userName": "reader", "password": "digest-local"},
    }
    requests = [
        FrozenRequest(url="http://loopback.test/", name="摘要认证", authConfig=config),
        FrozenRequest(
            url="http://loopback.test/other",
            name="无认证",
            authConfig={"authType": "NONE"},
        ),
    ]
    result = await execute(
        FrozenCase(id="case", category="scenario", requests=requests),
        transport=httpx.MockTransport(target),
    )
    assert result["status"] == "passed" and len(seen) == 3
    assert "authorization" not in seen[0] and seen[1]["authorization"].startswith(
        "Digest "
    )
    assert (
        'username="reader"' in seen[1]["authorization"]
        and "authorization" not in seen[2]
    )
    assert "digest-local" not in result["log"]


def test_rest_parameters_freeze_and_timeouts(native_workspace):
    db, _, _ = native_workspace
    configure(db)
    definition = db.get(ApiDefinition, "definition")
    definition.path = "items/{id}"
    config = db.get(NativeCaseConfig, "case-0")
    config.parameters = {
        "request": {
            "restParams": [
                {"key": "id", "value": "中文/a"},
                {"key": "unused", "enable": False},
            ],
            "connectTimeoutMs": 0,
            "responseTimeoutMs": 600000,
        }
    }
    db.commit()
    frozen = freeze(db, db.get(Case, "case-0"), db.get(User, "owner"))
    assert (
        frozen["requests"][0]["url"]
        == "http://127.0.0.1:12345/base/items/%E4%B8%AD%E6%96%87%2Fa"
    )
    options = arguments(FrozenRequest.model_validate(frozen["requests"][0]))
    assert options["timeout"].connect is None and options["timeout"].read == 600
    with pytest.raises(ValueError, match="REST"):
        path_parameters(
            "/target",
            RequestSpec(restParams=[{"key": "absent", "value": "v"}]).restParams,
        )
    assert (
        arguments(FrozenRequest(url="http://loopback.test/", name="旧配置"))["timeout"]
        == 10
    )
