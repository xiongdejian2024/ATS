"""Cancellation cannot bypass startup or interrupt durable finalization."""

import asyncio
import json
import os
import sys
from types import SimpleNamespace

import pytest

from agent.sat_runner import SATRunner


def make_runner(
    tmp_path, monkeypatch, *, sleep=False, pause_result=False, native=False
):
    events = []
    sending, release = asyncio.Event(), asyncio.Event()
    checkpoint = [dict(case_id="done", status="passed", duration=0.1)]
    command = (
        "import json,time; from pathlib import Path; "
        f"Path('results.json').write_text({json.dumps(checkpoint)!r}); "
        + ("time.sleep(60)" if sleep else "pass")
    )
    monkeypatch.setattr(
        "agent.sat_runner.build_invocation",
        lambda *args: ([sys.executable, "-c", command], os.environ.copy()),
    )

    async def send_message(payload):
        events.append(dict(payload))
        if pause_result and payload["type"] == "test_suite_result":
            sending.set()
            await release.wait()
        return True  # Keep the durable outbox for assertions, without ACKs.

    agent = SimpleNamespace(
        work_dir=tmp_path,
        config=SimpleNamespace(default_timeout=20),
        ws_client=SimpleNamespace(send_message=send_message),
    )
    agent.sat_runner = SATRunner(agent)
    if native:
        # Native execution adds XAT to sys.path; keep this unit test isolated
        # from subsequent backend fixtures that import their own main module.
        monkeypatch.setattr(sys, "path", sys.path.copy())
        from agent.native_http_runner import NativeHTTPRunner

        runner = NativeHTTPRunner(agent)
    else:
        runner = agent.sat_runner
    message = dict(
        suite_id="suite",
        execution_id="run",
        case_ids=["done", "pending"],
        case_codes=["finished", "later"],
        execution_command="xat --mode offline",
    )
    return runner, message, events, sending, release


def terminal_events(runner):
    return [
        json.loads(path.read_text())
        for path in runner.outbox.glob("*.json")
        if json.loads(path.read_text())["type"] == "test_suite_completed"
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize("native", [False, True])
async def test_immediate_cancel_before_execute_first_yield(
    tmp_path, monkeypatch, native
):
    runner, message, _, _, _ = make_runner(
        tmp_path, monkeypatch, sleep=True, native=native
    )
    runner.start(message)
    task = runner.runs["run"]
    await asyncio.wait_for(runner.cancel("suite", "run"), 10)
    assert not task.cancelled()
    assert not runner.runs and not runner.suites
    assert not runner.started and not runner.cancel_requested and not runner.finalizing
    assert len(terminal_events(runner)) == 1
    assert terminal_events(runner)[0]["status"] == "cancelled"


@pytest.mark.asyncio
@pytest.mark.parametrize("cancel_waiter", [False, True])
async def test_late_cancel_waits_for_result_and_completion_delivery(
    tmp_path, monkeypatch, cancel_waiter
):
    runner, message, _, sending, release = make_runner(
        tmp_path, monkeypatch, pause_result=True
    )
    runner.start(message)
    task = runner.runs["run"]
    await asyncio.wait_for(sending.wait(), 10)
    cancelling = asyncio.create_task(runner.cancel("suite", "run"))
    await asyncio.sleep(0.02)
    if cancel_waiter:
        cancelling.cancel()
        with pytest.raises(asyncio.CancelledError):
            await cancelling
    release.set()
    if not cancel_waiter:
        await asyncio.wait_for(cancelling, 10)
    await asyncio.wait_for(task, 10)
    assert not task.cancelled()
    assert not runner.runs and not runner.suites
    assert not runner.started and not runner.cancel_requested and not runner.finalizing
    stored = [json.loads(path.read_text()) for path in runner.outbox.glob("*.json")]
    results = {
        row["case_id"]: row for row in stored if row["type"] == "test_suite_result"
    }
    assert results["done"]["result"] == "passed"
    assert results["pending"]["result"] == "error"
    assert len(terminal_events(runner)) == 1
    assert (
        terminal_events(runner)[0]["status"] == "failed"
    )  # Natural exit has already won.


@pytest.mark.asyncio
async def test_repeated_cancel_during_process_termination_is_idempotent(
    tmp_path, monkeypatch
):
    from agent.sat_runner import terminate_process

    runner, message, _, _, _ = make_runner(tmp_path, monkeypatch, sleep=True)
    terminating, release = asyncio.Event(), asyncio.Event()
    processes = []

    async def paused_terminate(process):
        processes.append(process)
        terminating.set()
        await release.wait()
        await terminate_process(process)

    monkeypatch.setattr("agent.sat_runner.terminate_process", paused_terminate)
    runner.start(message)
    task = runner.runs["run"]
    checkpoint = tmp_path / "suites/suite/executions/run/results.json"

    async def wait_for_checkpoint():
        while not checkpoint.exists():
            await asyncio.sleep(0.01)

    await asyncio.wait_for(wait_for_checkpoint(), 10)
    first = asyncio.create_task(runner.cancel("suite", "run"))
    await asyncio.wait_for(terminating.wait(), 10)
    second = asyncio.create_task(runner.cancel("suite", "run"))
    await asyncio.sleep(0.02)
    release.set()
    try:
        await asyncio.wait_for(asyncio.gather(first, second), 10)
        assert not task.cancelled()
        assert not runner.runs and not runner.suites
        assert (
            not runner.started and not runner.cancel_requested and not runner.finalizing
        )
        assert len(terminal_events(runner)) == 1
        assert terminal_events(runner)[0]["status"] == "cancelled"
        assert processes[0].returncode is not None
    finally:
        for process in processes:
            await terminate_process(process)


@pytest.mark.asyncio
async def test_native_finalization_cannot_be_interrupted(tmp_path, monkeypatch):
    runner, message, _, sending, release = make_runner(
        tmp_path, monkeypatch, pause_result=True, native=True
    )
    # Invalid native input enters error finalization without issuing any HTTP request.
    runner.start(message)
    task = runner.runs["run"]
    await asyncio.wait_for(sending.wait(), 10)
    cancelling = asyncio.create_task(runner.cancel("suite", "run"))
    await asyncio.sleep(0.02)
    release.set()
    await asyncio.wait_for(cancelling, 10)
    assert not task.cancelled()
    assert not runner.runs and not runner.suites
    assert not runner.started and not runner.cancel_requested and not runner.finalizing
    assert len(terminal_events(runner)) == 1
    assert terminal_events(runner)[0]["status"] == "failed"
    record = tmp_path / "suites/suite/executions/run/native-run.json"
    assert json.loads(record.read_text())["status"] == "failed"
