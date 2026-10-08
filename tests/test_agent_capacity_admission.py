"""Agent-local capacity is shared across XAT, native and legacy execution."""

import asyncio
from types import SimpleNamespace

import pytest

from agent.agent import Agent


@pytest.mark.asyncio
async def test_mixed_runners_share_one_agent_slot(sat_config, monkeypatch):
    sat_config.max_concurrent_tasks = 1
    agent = Agent(sat_config)
    agent.work_dir = sat_config.work_dir
    agent.ws_client = SimpleNamespace()
    release = asyncio.Event()
    entered = []

    async def execute(message):
        entered.append(message["execution_id"])
        await release.wait()

    monkeypatch.setattr(agent.sat_runner, "execute", execute)
    monkeypatch.setattr(agent.native_http_runner, "execute", execute)
    base = dict(suite_id="suite", case_ids=["case"], case_codes=["code"])
    agent.sat_runner.start(dict(base, execution_id="xat", execution_command="xat"))
    agent.native_http_runner.start(
        dict(base, execution_id="native", execution_command="ats-native-http")
    )
    tasks = [*agent.sat_runner.runs.values(), *agent.native_http_runner.runs.values()]
    try:
        await asyncio.sleep(0.02)
        assert len(entered) == 1
    finally:
        release.set()
        await asyncio.gather(*tasks)


def message(execution_id, command="xat", suite_id="suite"):
    return dict(
        suite_id=suite_id,
        execution_id=execution_id,
        case_ids=["case"],
        case_codes=["code"],
        execution_command=command,
    )


def make_agent(sat_config):
    agent = Agent(sat_config)
    agent.work_dir = sat_config.work_dir
    events = []

    async def send_message(payload):
        events.append(dict(payload))
        return True

    async def send_task_result(**payload):
        events.append(dict(type="task_result", **payload))

    async def close():
        pass

    agent.ws_client = SimpleNamespace(
        send_message=send_message, send_task_result=send_task_result, close=close
    )
    return agent, events


@pytest.mark.asyncio
async def test_duplicate_ids_across_runners_and_legacy_startup_are_deduplicated(
    sat_config, monkeypatch
):
    agent, _ = make_agent(sat_config)
    entered, release = [], asyncio.Event()

    async def execute(payload):
        entered.append(payload["execution_id"])
        await release.wait()

    async def legacy(**kwargs):
        await execute(kwargs)

    monkeypatch.setattr(agent.sat_runner, "execute", execute)
    monkeypatch.setattr(agent.native_http_runner, "execute", execute)
    monkeypatch.setattr(agent, "_execute_test_suite_async", legacy)
    await agent.on_message(dict(message("same"), type="execute_test_suite"))
    await agent.on_message(
        dict(message("same", "ats-native-http"), type="execute_test_suite")
    )
    await agent.on_message(
        dict(message("same", "echo legacy"), type="execute_test_suite")
    )
    assert len(agent.sat_runner.runs) == 1
    assert not agent.native_http_runner.runs and not agent.legacy_runs
    release.set()
    await asyncio.gather(*agent.sat_runner.runs.values())
    await agent.on_message(
        dict(message("same", "echo legacy"), type="execute_test_suite")
    )
    assert entered == ["same"]
    assert not agent.execution_admission.tickets


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["xat", "native", "legacy"])
async def test_cancel_waiting_runner_does_not_wait_for_active_slot(
    sat_config, monkeypatch, kind
):
    agent, events = make_agent(sat_config)
    release = asyncio.Event()

    async def block(_):
        await release.wait()

    monkeypatch.setattr(agent.sat_runner, "execute", block)
    agent.sat_runner.start(message("blocker", suite_id="other"))
    blocker = agent.sat_runner.runs["blocker"]
    await asyncio.sleep(0)
    if kind == "xat":
        from agent.sat_runner import SATRunner

        monkeypatch.setattr(
            agent.sat_runner, "execute", SATRunner.execute.__get__(agent.sat_runner)
        )
    command = {"xat": "xat", "native": "ats-native-http", "legacy": "echo never-run"}[
        kind
    ]
    await agent._handle_execute_test_suite(message("waiting", command))
    try:
        await asyncio.wait_for(
            agent._handle_cancel_test_suite(
                dict(suite_id="suite", execution_id="waiting")
            ),
            2,
        )
        terminals = [
            event
            for event in events
            if event["type"] == "test_suite_completed"
            and event["execution_id"] == "waiting"
        ]
        assert terminals and terminals[-1]["status"] == "cancelled"
        assert not blocker.done()
        assert len(agent.execution_admission.tickets) == 1
    finally:
        release.set()
        await blocker


@pytest.mark.asyncio
async def test_cancel_same_suite_targets_correct_runner_and_releases_capacity(
    sat_config, monkeypatch
):
    sat_config.max_concurrent_tasks = 2
    agent, _ = make_agent(sat_config)
    release = asyncio.Event()
    started = asyncio.Event()

    async def xat(payload):
        agent.sat_runner.started.add(payload["execution_id"])
        started.set()
        await release.wait()

    async def native(payload):
        agent.native_http_runner.started.add(payload["execution_id"])
        await release.wait()

    monkeypatch.setattr(agent.sat_runner, "execute", xat)
    monkeypatch.setattr(agent.native_http_runner, "execute", native)
    agent.sat_runner.start(message("xat"))
    agent.native_http_runner.start(message("native", "ats-native-http"))
    xat_task, native_task = (
        agent.sat_runner.runs["xat"],
        agent.native_http_runner.runs["native"],
    )
    await started.wait()
    await agent._handle_cancel_test_suite(dict(suite_id="suite", execution_id="xat"))
    assert xat_task.done() and not native_task.done()
    assert list(agent.execution_admission.tickets) == ["native"]
    release.set()
    await native_task
    assert not agent.execution_admission.tickets


@pytest.mark.asyncio
async def test_legacy_same_suite_serializes_without_wasting_other_slots(
    sat_config, monkeypatch
):
    sat_config.max_concurrent_tasks = 2
    agent, _ = make_agent(sat_config)
    entered, release = [], asyncio.Event()

    async def legacy(**payload):
        entered.append(payload["execution_id"])
        await release.wait()

    async def native(payload):
        entered.append(payload["execution_id"])
        await release.wait()

    monkeypatch.setattr(agent, "_execute_test_suite_async", legacy)
    monkeypatch.setattr(agent.native_http_runner, "execute", native)
    await agent._handle_execute_test_suite(message("first", "echo first"))
    await agent._handle_execute_test_suite(message("second", "echo second"))
    agent.native_http_runner.start(
        message("native", "ats-native-http", suite_id="other")
    )
    tasks = [*agent.legacy_runs.values(), *agent.native_http_runner.runs.values()]
    try:
        await asyncio.sleep(0)
        assert entered == ["first", "native"]
    finally:
        release.set()
        await asyncio.gather(*tasks)
    assert entered == ["first", "native", "second"]
    assert not agent.execution_admission.tickets


@pytest.mark.asyncio
async def test_exception_and_reconnect_preserve_slot_ownership(sat_config, monkeypatch):
    agent, _ = make_agent(sat_config)
    release, entered = asyncio.Event(), []

    async def failure(payload):
        await release.wait()
        raise OSError("isolated runner failure")

    async def succeeding(payload):
        entered.append(payload["execution_id"])

    monkeypatch.setattr(agent.sat_runner, "execute", failure)
    monkeypatch.setattr(agent.native_http_runner, "execute", succeeding)
    agent.sat_runner.start(message("first"))
    agent.native_http_runner.start(message("second", "ats-native-http"))
    tasks = [*agent.sat_runner.runs.values(), *agent.native_http_runner.runs.values()]
    await agent._setup_work_dir(str(sat_config.work_dir))
    executor = agent.task_executor
    await agent._setup_work_dir(str(sat_config.work_dir))
    assert agent.task_executor is executor
    await asyncio.sleep(0)
    assert entered == []
    release.set()
    results = await asyncio.gather(*tasks, return_exceptions=True)
    assert isinstance(results[0], OSError)
    assert entered == ["second"]
    assert not agent.execution_admission.tickets


@pytest.mark.asyncio
async def test_real_legacy_subprocess_cancel_stops_before_successor(
    sat_config, monkeypatch
):
    import shlex
    import sys
    from loguru import logger
    from test_http_agent_e2e import until

    agent, events = make_agent(sat_config)
    agent.logger = logger
    command = f"{shlex.quote(sys.executable)} -c 'import time; time.sleep(60)'"
    await agent._handle_execute_test_suite(message("legacy", command))
    await until(lambda: "suite" in agent.running_suites)
    process = agent.running_suites["suite"]
    entered = []

    async def successor(payload):
        assert process.poll() is not None
        entered.append(payload["execution_id"])

    monkeypatch.setattr(agent.native_http_runner, "execute", successor)
    agent.native_http_runner.start(message("next", "ats-native-http", suite_id="other"))
    successor_task = agent.native_http_runner.runs["next"]
    await asyncio.wait_for(
        agent._handle_cancel_test_suite(dict(suite_id="suite", execution_id="legacy")),
        5,
    )
    await successor_task
    assert entered == ["next"]
    assert process.poll() is not None
    assert not agent.execution_admission.tickets and not agent.running_suites
    assert any(
        event["type"] == "test_suite_completed" and event["status"] == "cancelled"
        for event in events
    )


@pytest.mark.asyncio
async def test_unknown_cancel_tombstone_survives_restart_and_prevents_all_runner_replays(
    sat_config, monkeypatch
):
    agent, events = make_agent(sat_config)
    cancel = dict(suite_id="suite", execution_id="never-delivered")
    await agent._handle_cancel_test_suite(cancel)
    terminal = next(row for row in events if row["type"] == "test_suite_completed")
    assert terminal["status"] == "cancelled"
    agent.sat_runner.acknowledge(terminal["event_id"])
    assert not list(agent.sat_runner.outbox.glob("*.json"))
    marker = agent.work_dir / "execution-admission/never-delivered.json"
    assert marker.is_file()

    restarted, replayed = make_agent(sat_config)
    for command in ("xat", "ats-native-http", "echo legacy"):
        await restarted._handle_execute_test_suite(message("never-delivered", command))
    assert not restarted.sat_runner.runs and not restarted.native_http_runner.runs
    assert not restarted.legacy_runs and not restarted.execution_admission.tickets
    await restarted._handle_cancel_test_suite(cancel)
    assert replayed[-1]["type"] == "test_suite_completed"
    assert replayed[-1]["status"] == "cancelled"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "evidence",
    ["directory", "legacy", "corrupt", "accepted", "other-legacy", "empty-legacy"],
)
async def test_unknown_cancel_never_acknowledges_potential_orphan_work(
    sat_config, evidence
):
    import json

    agent, events = make_agent(sat_config)
    suite = agent.work_dir / "suites/suite"
    if evidence == "directory":
        (suite / "executions/unknown").mkdir(parents=True)
    elif evidence in ("legacy", "corrupt", "other-legacy", "empty-legacy"):
        path = suite / "xat/test_cases.json"
        path.parent.mkdir(parents=True)
        if evidence != "empty-legacy":
            path.write_text(
                json.dumps(
                    {"execution_id": "unknown" if evidence == "legacy" else "different"}
                )
                if evidence != "corrupt"
                else "{"
            )
    else:
        assert agent.execution_admission.register("unknown")
        agent, events = make_agent(sat_config)  # Previous owner/process is gone.
    await agent._handle_cancel_test_suite(
        dict(suite_id="suite", execution_id="unknown")
    )
    assert not events


@pytest.mark.asyncio
async def test_raw_task_shares_capacity_and_cancel_before_start_reports_without_execution(
    sat_config, monkeypatch
):
    from agent.task_executor import TaskExecutor

    agent, events = make_agent(sat_config)
    agent.task_executor = TaskExecutor(agent.work_dir)
    release, executed = asyncio.Event(), []

    async def blocking(_):
        await release.wait()

    async def unexpected(_):
        executed.append(True)
        raise AssertionError("cancelled task must not execute")

    monkeypatch.setattr(agent.sat_runner, "execute", blocking)
    monkeypatch.setattr(agent.task_executor, "execute_task", unexpected)
    agent.sat_runner.start(message("blocking"))
    blocker = agent.sat_runner.runs["blocking"]
    await agent._handle_task(dict(task_id="raw", command="echo never"))
    raw = agent.task_runs["raw"]
    await agent._handle_cancel_task(dict(task_id="raw"))
    await asyncio.wait_for(raw, 2)
    assert not executed
    assert any(
        row["type"] == "task_result" and row["status"] == "cancelled" for row in events
    )
    assert not blocker.done()
    release.set()
    await blocker
    assert not agent.execution_admission.tickets


@pytest.mark.asyncio
@pytest.mark.parametrize("leader_exits", [False, True])
async def test_process_group_cleanup_kills_child_ignoring_term(tmp_path, leader_exits):
    import os
    import shlex
    import sys
    import psutil
    from agent.sat_runner import terminate_process
    from test_http_agent_e2e import until

    if os.name != "posix":
        pytest.skip("POSIX process-group regression")
    marker = tmp_path / "child.pid"
    source = tmp_path / "child.py"
    source.write_text(
        "import os,signal,time\nfrom pathlib import Path\n"
        "signal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
        f"Path({str(marker)!r}).write_text(str(os.getpid()))\n"
        "time.sleep(60)\n"
    )
    # Keep the pipe open in the normal leader case; in the background case the
    # parent exits before cleanup while the same-group child remains alive.
    command = f"{shlex.quote(sys.executable)} {shlex.quote(str(source))} & " + (
        "exit 0" if leader_exits else "wait"
    )
    process = await asyncio.create_subprocess_shell(command, start_new_session=True)
    try:
        await until(marker.exists)
        child = psutil.Process(int(marker.read_text()))
        if leader_exits:
            await process.wait()
        await asyncio.wait_for(terminate_process(process), 5)
        assert process.returncode is not None
        assert not child.is_running() or child.status() in (
            psutil.STATUS_ZOMBIE,
            psutil.STATUS_DEAD,
        )
    finally:
        try:
            os.killpg(process.pid, 9)
        except ProcessLookupError:
            pass
        await process.wait()
