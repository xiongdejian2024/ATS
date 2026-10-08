"""Retain atomically persisted XAT case results when the process is interrupted."""

import asyncio
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from agent.sat_runner import SATRunner


@pytest.mark.asyncio
@pytest.mark.parametrize("interruption", ["timeout", "cancel"])
async def test_interruption_preserves_completed_pytest_case(
    tmp_path, monkeypatch, interruption
):
    source = tmp_path / "test_partial.py"
    ready = tmp_path / "slow-case-started"
    source.write_text(
        "import time\nfrom pathlib import Path\n"
        "def test_caseid_finished(): assert True\n"
        f"def test_caseid_slow():\n    Path({str(ready)!r}).touch()\n    time.sleep(60)\n"
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
    events = []

    async def send_message(payload):
        events.append(dict(payload))
        if payload.get("event_id"):
            runner.acknowledge(payload["event_id"])
        return True

    runner = SATRunner(
        SimpleNamespace(
            work_dir=tmp_path / "agent",
            config=SimpleNamespace(
                default_timeout=3 if interruption == "timeout" else 20
            ),
            ws_client=SimpleNamespace(send_message=send_message),
        )
    )
    message = dict(
        suite_id="suite",
        execution_id="run",
        case_ids=["done", "pending"],
        case_codes=["finished", "slow"],
        execution_command="xat --mode offline",
    )
    runner.start(message)
    task = runner.runs["run"]

    async def wait_for_slow_case():
        while not ready.exists():
            if task.done():
                await task
                pytest.fail("Runner stopped before the second case started")
            await asyncio.sleep(0.01)

    await asyncio.wait_for(wait_for_slow_case(), 10)
    if interruption == "cancel":
        await runner.cancel("suite", "run")
    await asyncio.wait_for(task, 10)
    results = {
        event["case_id"]: event
        for event in events
        if event["type"] == "test_suite_result"
    }
    assert results["done"]["result"] == "passed"
    assert "teardown: passed" in results["done"]["log_output"]
    if interruption == "cancel":
        assert "pending" not in results
    else:
        assert results["pending"]["result"] == "error"
        assert results["pending"]["error_message"] == "XAT 执行超时"
    completed = [event for event in events if event["type"] == "test_suite_completed"]
    assert len(completed) == 1
    assert completed[0]["reported_case_count"] == 1
    assert completed[0]["outcome"] == (
        "cancelled" if interruption == "cancel" else "timeout"
    )
    assert events[-1]["type"] == "test_suite_completed"
    assert not runner.runs and not runner.suites
    assert not list(runner.outbox.glob("*.json"))
    report = json.loads(
        (tmp_path / "agent/suites/suite/executions/run/run.json").read_text()
    )
    assert report["outcome"] == completed[0]["outcome"]


@pytest.mark.parametrize(
    "contents",
    [
        "{broken",
        "{}",
        "[null]",
        json.dumps([{"case_id": "other", "status": "passed", "duration": 1}]),
        json.dumps([{"case_id": "done", "status": "passed", "duration": -1}]),
        json.dumps([{"case_id": "done", "status": [], "duration": 1}]),
        json.dumps([{"case_id": "done", "status": "passed", "duration": True}]),
        json.dumps([{"case_id": "done", "status": "passed", "duration": float("nan")}]),
        json.dumps([{"case_id": "done", "status": "passed", "duration": 1}] * 2),
    ],
)
def test_invalid_checkpoint_is_rejected(tmp_path, contents):
    from agent.sat_runner import read_results

    checkpoint = tmp_path / "results.json"
    checkpoint.write_text(contents)
    with pytest.raises(ValueError):
        read_results(checkpoint, ["done"])


@pytest.mark.asyncio
async def test_corrupt_checkpoint_still_delivers_terminal_event(tmp_path, monkeypatch):
    events = []

    async def send_message(payload):
        events.append(dict(payload))
        if payload.get("event_id"):
            runner.acknowledge(payload["event_id"])
        return True

    monkeypatch.setattr(
        "agent.sat_runner.build_invocation",
        lambda *args: (
            [
                sys.executable,
                "-c",
                "from pathlib import Path; Path('results.json').write_text('{broken')",
            ],
            os.environ.copy(),
        ),
    )
    runner = SATRunner(
        SimpleNamespace(
            work_dir=tmp_path,
            config=SimpleNamespace(default_timeout=10),
            ws_client=SimpleNamespace(send_message=send_message),
        )
    )
    runner.start(
        dict(
            suite_id="suite",
            execution_id="run",
            case_ids=["done"],
            case_codes=["finished"],
            execution_command="xat --mode offline",
        )
    )
    await asyncio.wait_for(runner.runs["run"], 10)
    result = next(event for event in events if event["type"] == "test_suite_result")
    assert result["result"] == "error"
    assert "读取 XAT 结果失败" in result["error_message"]
    assert events[-1]["type"] == "test_suite_completed"
    assert events[-1]["status"] == "failed"
    assert events[-1]["reported_case_count"] == 0
    assert not runner.runs and not runner.suites
