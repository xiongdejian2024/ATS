"""Actual loopback controller/Agent/XAT uses frozen environment and initial values."""

from copy import deepcopy
from uuid import uuid4
import pytest
from test_http_agent_e2e import lab, until
from test_native_http_agent_e2e import native_lab, dispatch, finished, scope


@pytest.mark.asyncio
async def test_controller_agent_xat_frozen_environment_and_initial_values(native_lab):
    value = native_lab
    client = value["client"]
    environment = value["request_environment"]
    base = f"/api/v1/projects/{value['api']['projectId']}/native-cases"
    body = dict(
        name=environment["name"],
        address=environment["address"],
        expectedRevision=environment["revision"],
        variables=[
            dict(name="q", value="frozen-environment"),
            dict(name="header", value="environment-header"),
        ],
    )
    response = await client.put(base + "/environments/" + environment["id"], json=body)
    assert response.status_code == 200, response.text
    environment = response.json()["data"]["environments"][0]
    request = {
        **value["request"],
        "query": {"q": "${q}"},
        "headers": {"X-Frozen": "${header}"},
        "initialVariables": [dict(name="header", value="request-header")],
    }
    await value["config"](value["api"], {"request": request}, revision=1)
    run_id = await scope(value, "api")
    body.update(
        expectedRevision=environment["revision"],
        variables=[dict(name="q", value="changed-after-freeze")],
    )
    response = await client.put(base + "/environments/" + environment["id"], json=body)
    assert response.status_code == 200, response.text
    await dispatch(run_id)
    await finished(run_id)
    assert value["hits"] == [
        dict(
            query={"q": "frozen-environment"},
            body={"number": 7},
            header="request-header",
        )
    ]
