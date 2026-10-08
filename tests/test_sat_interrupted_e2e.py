"""Real HTTP cancellation, WebSocket delivery, XAT checkpoint and database recovery."""

import json
import os
import sys
from pathlib import Path

import pytest

from test_http_agent_e2e import lab, queue_states, until


@pytest.mark.asyncio
@pytest.mark.parametrize("interruption", ["timeout", "execution-id", "suite-wide"])
async def test_interrupted_pytest_rows_reach_backend(
    lab, tmp_path, monkeypatch, interruption
):
    from database import SessionLocal
    from models.test_suite import TestSuiteExecution
    from models import TestExecution
    from services.suite_results import result_id

    ready = tmp_path / "slow-started"
    source = tmp_path / "test_partial.py"
    completed_case = lab["cases"][0]
    next_case = lab["cases"][1]
    source.write_text(
        "import time\nimport pytest\nfrom pathlib import Path\n"
        f"@pytest.mark.ats_case({completed_case['caseCode']!r})\n"
        "def test_completed(): assert True\n"
        f"@pytest.mark.ats_case({next_case['caseCode']!r})\n"
        f"def test_slow():\n    Path({str(ready)!r}).touch()\n    time.sleep(60)\n"
    )

    def invocation(config, options, directory, selection):
        selected = directory / "selection.json"
        selected.write_text(json.dumps(selection))
        env = dict(
            os.environ,
            ATS_CASE_SELECTION=str(selected),
            ATS_RESULT_FILE=str(directory / "results.json"),
            PYTHONPATH=str(Path(__file__).resolve().parents[1]),
            PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
        )
        return [
            sys.executable,
            "-m",
            "pytest",
            "--noconftest",
            "-p",
            "integrations.sat_pytest",
            str(source),
        ], env

    monkeypatch.setattr("agent.sat_runner.build_invocation", invocation)
    client, suite_id = lab["client"], lab["suite"]["id"]
    base = f"/api/v1/test-plans/suites/{suite_id}"
    timeout = 3 if interruption == "timeout" else 20
    response = await client.put(
        base, json={"execution_command": f"xat --mode offline --timeout {timeout}"}
    )
    assert response.status_code == 200, response.text
    response = await client.post(base + "/execute")
    assert response.status_code == 200, response.text
    await until(ready.exists)
    execution_id = next(
        key for key, status in queue_states(suite_id).items() if status == "running"
    )
    if interruption != "timeout":
        body = {"executionId": execution_id} if interruption == "execution-id" else {}
        response = await client.post(base + "/cancel", json=body)
        assert response.status_code == 200, response.text
    expected_status = "failed" if interruption == "timeout" else "cancelled"
    await until(lambda: queue_states(suite_id).get(execution_id) == expected_status)
    await until(lambda: not list(lab["agent"].sat_runner.outbox.glob("*.json")))
    with SessionLocal() as db:
        identifier = result_id(execution_id, completed_case["id"])
        row = db.get(TestSuiteExecution, identifier)
        assert row is not None and row.result == "passed"
        assert "teardown: passed" in row.log_output
        assert db.get(TestExecution, identifier).result == "passed"
        all_rows = db.query(TestSuiteExecution).all()
        if interruption == "timeout":
            assert len(all_rows) == 4
            assert sum(item.result == "error" for item in all_rows) == 3
        else:
            assert len(all_rows) == 1
    run = (
        lab["agent"].work_dir
        / "suites"
        / suite_id
        / "executions"
        / execution_id
        / "run.json"
    )
    assert json.loads(run.read_text())["outcome"] == (
        "timeout" if interruption == "timeout" else "cancelled"
    )
