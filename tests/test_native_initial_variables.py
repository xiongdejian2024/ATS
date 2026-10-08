"""Literal declarations, request-local scope and backwards-compatible frozen wire."""

import asyncio
import importlib.util
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import httpx
import pytest
from pydantic import ValidationError
from framework.native_http.models import RequestSpec, FrozenRequest, FrozenCase
from framework.native_http.variable_models import wire_case
from framework.native_http.engine import execute
from framework.native_http.extraction_models import PostProcessorConfig
from framework.native_http.extractions import evaluate
from services import native_variable_delivery as delivery
from services.agent_connections import ConnectionManager, AgentSession


def declaration(name, value="", **kw):
    return dict(name=name, value=value, **kw)


@pytest.mark.parametrize(
    "rows",
    [
        [declaration(" ")],
        [declaration("${bad}")],
        [declaration("a\nb")],
        [declaration("a", 1)],
        [declaration("a", enable=1)],
        [declaration("a"), declaration("a", enable=False)],
        [declaration(str(i)) for i in range(101)],
        [declaration(str(i), "中" * 20000) for i in range(2)],
    ],
)
def test_invalid_bounded_declarations(rows):
    with pytest.raises(ValidationError):
        RequestSpec(initialVariables=rows)


@pytest.mark.asyncio
async def test_precedence_empty_values_local_isolation_and_equal_extraction():
    hits = []

    def handler(request):
        hits.append(dict(request.url.params))
        return httpx.Response(200, json={"value": "same"})

    request = dict(
        url="http://fixture.test/echo",
        name="first",
        query={"token": "${token}", "empty": "${empty}", "local": "${local}"},
        environmentVariables=[declaration("token", "env"), declaration("empty", "env")],
        initialVariables=[
            declaration("token", "same"),
            declaration("empty", ""),
            declaration("local", "request-only"),
        ],
        postProcessorConfig=dict(
            processors=[
                dict(
                    id="processor",
                    extractors=[
                        dict(id="extract", variableName="token", expression="$.value")
                    ],
                )
            ]
        ),
    )
    second = deepcopy(request)
    second.update(
        name="second",
        initialVariables=[
            declaration("token", "second"),
            declaration("local", "second-local"),
        ],
        postProcessorConfig={"processors": []},
    )
    third = deepcopy(second)
    third.update(name="third", initialVariables=[])
    result = await execute(
        FrozenCase(
            id="case",
            category="scenario",
            initialVariables=[declaration("token", "scenario")],
            requests=[request, second, third],
        ),
        transport=httpx.MockTransport(handler),
    )
    assert result["status"] == "passed"
    assert hits == [
        dict(token="same", empty="", local="request-only"),
        dict(token="same", empty="env", local="second-local"),
        dict(token="same", empty="env", local="${local}"),
    ]


@pytest.mark.asyncio
async def test_retry_rebuilds_local_scope_and_preserves_extracted_only():
    hits = []

    def handler(request):
        hits.append(dict(request.url.params))
        return httpx.Response(
            503 if len(hits) == 1 else 200, json={"value": "from-first-attempt"}
        )

    case = FrozenCase(
        id="retry",
        category="api",
        retryTimes=1,
        requests=[
            dict(
                url="http://fixture.test/",
                name="retry",
                query={"v": "${v}", "local": "${local}"},
                initialVariables=[
                    declaration("v", "initial"),
                    declaration("local", "private"),
                ],
                postProcessorConfig=dict(
                    processors=[
                        dict(
                            id="p",
                            extractors=[
                                dict(id="e", variableName="v", expression="$.value")
                            ],
                        )
                    ]
                ),
            )
        ],
    )
    result = await execute(case, transport=httpx.MockTransport(handler))
    assert result["status"] == "passed"
    assert hits == [
        dict(v="initial", local="private"),
        dict(v="from-first-attempt", local="private"),
    ]


def test_extractor_alias_cleanup_updates_temporary_without_carrying_defaults():
    config = PostProcessorConfig(
        processors=[
            dict(
                id="p",
                extractors=[
                    dict(
                        id="e",
                        variableName="v",
                        expression="$.values[*]",
                        resultMatchingRule="ALL",
                    )
                ],
            )
        ]
    )
    scope, temporary = {"local": "private"}, {}
    evaluate(config, httpx.Response(200, json={"values": ["a", "b"]}), scope, temporary)
    assert temporary["v_2"] == "b" and "local" not in temporary
    evaluate(config, httpx.Response(200, json={"values": ["c"]}), scope, temporary)
    assert "v_2" not in temporary and temporary["v_1"] == "c"


def test_wire_preserves_legacy_strict_model_and_disabled_rows_require_capability():
    from framework.native_http import models

    # Load the committed pre-variable strict parser, not a permissive current model.
    path = Path(__file__).parent / "fixtures/native_http_prevariables_models.py"
    spec = importlib.util.spec_from_file_location(
        "framework.native_http.prevariables_test", path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    case = FrozenCase(
        id="old",
        category="api",
        requests=[dict(url="http://fixture.test/", name="old")],
    )
    old = wire_case(case)
    assert module.FrozenCase.model_validate(old).id == "old"
    assert not delivery.requires_variables({"native_cases": [old]})
    case.requests[0].initialVariables = RequestSpec(
        initialVariables=[declaration("disabled", enable=False)]
    ).initialVariables
    payload = {"native_cases": [wire_case(case)]}
    assert delivery.requires_variables(payload)
    with pytest.raises(ValidationError):
        module.FrozenCase.model_validate(payload["native_cases"][0])


@pytest.mark.asyncio
async def test_replacement_session_does_not_receive_new_protocol():
    class Socket:
        def __init__(self):
            self.sent = []

        async def send_json(self, payload):
            self.sent.append(payload)

    manager = ConnectionManager()
    first, second = Socket(), Socket()
    session = AgentSession(
        "node",
        first,
        None,
        2,
        auth_received=True,
        capabilities=frozenset({delivery.CAPABILITY}),
    )
    manager.sessions["node"], manager.active_connections["node"] = session, first
    payload = {
        "native_cases": [{"initialVariables": [declaration("a")], "requests": []}]
    }
    captured = delivery.session_for(manager, "node", payload)
    manager.sessions["node"] = AgentSession("node", second, None, 2, auth_received=True)
    manager.active_connections["node"] = second
    assert delivery.session_for(manager, "node", payload) is None
    assert await delivery.send(manager, "node", payload, captured) is False
    assert first.sent == second.sent == []


def test_wire_budget_rejects_final_message():
    with pytest.raises(ValueError, match="12MiB"):
        delivery.validate_budget(
            {"native_cases": [], "oversize": "x" * delivery.WIRE_LIMIT}
        )
