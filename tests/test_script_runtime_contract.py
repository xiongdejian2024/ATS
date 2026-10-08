"""Trusted scripts keep shell/argv compatibility and bounded, cancellable lifetimes."""

import asyncio
import json
import os
import shlex
import sys
from pathlib import Path

import psutil
import pytest
from loguru import logger

from agent.script_runtime import positive_timeout, prepare_command, text_chunks
from agent.task_executor import TaskExecutor
from test_agent_capacity_admission import make_agent, message
from test_http_agent_e2e import until
from test_plan_orchestration import plan_lab


BAD_TIMEOUTS = [None, True, False, 0, -1, "1", float("nan"), float("inf"), float("-inf"), 10**400]


def stopped(pid):
    try:
        return psutil.Process(pid).status() in (psutil.STATUS_ZOMBIE, psutil.STATUS_DEAD)
    except psutil.NoSuchProcess:
        return True


def script_command(source):
    return f"{shlex.quote(sys.executable)} -c {shlex.quote(source)}"


@pytest.mark.parametrize("value", BAD_TIMEOUTS)
@pytest.mark.asyncio
async def test_invalid_timeout_reports_error_without_launch(tmp_path, monkeypatch, value):
    called = []

    async def unexpected(*args, **kwargs):
        called.append(True)
        raise AssertionError("invalid timeout must not start a child")

    monkeypatch.setattr(asyncio, "create_subprocess_exec", unexpected)
    monkeypatch.setattr(asyncio, "create_subprocess_shell", unexpected)
    with pytest.raises(ValueError, match="有限正数"):
        positive_timeout(value)
    executor = TaskExecutor(tmp_path)
    result = await executor.execute_task(dict(task_id="invalid", command="echo never", timeout=value))
    assert result["status"] == "error" and "有限正数" in result["error"]
    assert not called and not executor.tasks


@pytest.mark.asyncio
@pytest.mark.parametrize("shell", [False, True])
async def test_raw_shell_and_argv_keep_cwd_env_and_no_newline_output(tmp_path, shell):
    directory = tmp_path / "custom cwd"
    source = "import os,sys;sys.stdout.write(os.environ['VALUE']+'|'+os.path.basename(os.getcwd()))"
    command = script_command(source) if shell else [sys.executable, "-c", source]
    result = await TaskExecutor(tmp_path).execute_task(dict(
        task_id="argv", command=command, work_dir=str(directory), env_vars={"VALUE": "中文"}, timeout=3,
    ))
    assert result["status"] == "success"
    assert result["output"] == "中文|custom cwd"


@pytest.mark.asyncio
async def test_split_utf8_chunks_keep_exact_text():
    class Stream:
        chunks = iter([b"\xe4", b"\xb8\xad\xf0", b"\x9f\x98\x80", b""])

        async def read(self, size):
            assert size == 4096
            return next(self.chunks)

    assert "".join([chunk async for chunk in text_chunks(Stream())]) == "中😀"


@pytest.mark.asyncio
async def test_raw_default_timeout_and_invalid_environment_still_return_results(tmp_path):
    executor = TaskExecutor(tmp_path, default_timeout=0.15)
    result = await executor.execute_task(dict(task_id="silent", command=[sys.executable, "-c", "import time;time.sleep(60)"]))
    assert result["status"] == "timeout" and not executor.tasks
    invalid = await executor.execute_task(dict(task_id="bad-env", command="echo never", env_vars=None))
    assert invalid["status"] == "error" and invalid["exit_code"] == -1


@pytest.mark.asyncio
@pytest.mark.parametrize("command", ["echo legacy", "xat --mode offline", "xat --mode offline --timeout nan"])
async def test_suite_invalid_timeout_has_terminal_event_without_launch(sat_config, monkeypatch, command):
    sat_config.default_timeout = float("inf")
    agent, events = make_agent(sat_config)
    spawned = []

    async def forbidden(*args, **kwargs):
        spawned.append(True)
        raise AssertionError("invalid deadline must fail before launch")

    monkeypatch.setattr(asyncio, "create_subprocess_shell", forbidden)
    monkeypatch.setattr(asyncio, "create_subprocess_exec", forbidden)
    await agent._handle_execute_test_suite(message("invalid", command))
    tasks = [*agent.legacy_runs.values(), *agent.sat_runner.runs.values()]
    await asyncio.gather(*tasks)
    assert not spawned
    assert events[-1]["type"] == "test_suite_completed" and events[-1]["status"] == "failed"
    assert "有限正数" in events[-1]["message"]
    assert not agent.execution_admission.tickets


@pytest.mark.asyncio
@pytest.mark.parametrize("partial_output", [False, True])
async def test_legacy_silent_and_unterminated_line_timeout_without_blocking_loop(sat_config, partial_output):
    sat_config.default_timeout = 0.3
    agent, events = make_agent(sat_config)
    agent.logger = logger
    marker = sat_config.work_dir / "script.pid"
    source = (
        "import os,sys,time;from pathlib import Path;"
        f"Path({str(marker)!r}).write_text(str(os.getpid()));"
        + ("sys.stdout.write('partial-without-newline');sys.stdout.flush();" if partial_output else "")
        + "time.sleep(60)"
    )
    await agent._handle_execute_test_suite(message("legacy", script_command(source)))
    task = agent.legacy_runs["legacy"]
    ticks = 0

    async def heartbeat():
        nonlocal ticks
        while not task.done():
            ticks += 1
            await asyncio.sleep(0.01)

    timer = asyncio.create_task(heartbeat())
    try:
        async with asyncio.timeout(6):
            await task
        assert ticks >= 5
        assert marker.exists() and stopped(int(marker.read_text()))
        completion = [event for event in events if event["type"] == "test_suite_completed"]
        assert completion and completion[-1]["status"] == "failed"
        assert "超时" in completion[-1]["message"]
        if partial_output:
            assert any("partial-without-newline" in event.get("message", "") for event in events)
        assert not agent.execution_admission.tickets and not agent.running_suites
    finally:
        timer.cancel()
        await asyncio.gather(timer, return_exceptions=True)
        await agent._cancel_legacy("suite")


@pytest.mark.asyncio
async def test_legacy_cancel_during_unterminated_line_retains_finished_case(sat_config):
    agent, events = make_agent(sat_config)
    agent.logger = logger
    marker = sat_config.work_dir / "cancel.pid"
    row = dict(test_name="finished", case_id="case", status="passed", duration=0.01)
    source = (
        "import os,sys,time;from pathlib import Path;"
        f"Path({str(marker)!r}).write_text(str(os.getpid()));"
        f"Path('xat/test_results.json').write_text({json.dumps([row])!r});"
        "sys.stdout.write('still running');sys.stdout.flush();time.sleep(60)"
    )
    await agent._handle_execute_test_suite(message("cancel-run", script_command(source)))
    task = agent.legacy_runs["cancel-run"]
    try:
        await until(lambda: any(event["type"] == "test_suite_result" for event in events))
        async with asyncio.timeout(6):
            await agent._handle_cancel_test_suite(dict(suite_id="suite", execution_id="cancel-run"))
        assert stopped(int(marker.read_text()))
        assert any(event["type"] == "test_suite_result" and event["result"] == "passed" for event in events)
        assert events[-1]["type"] == "test_suite_completed" and events[-1]["status"] == "cancelled"
        assert not agent.execution_admission.tickets
    finally:
        if not task.done():
            await agent._cancel_legacy("suite")


@pytest.mark.asyncio
async def test_legacy_deadline_includes_preparation(sat_config, monkeypatch):
    sat_config.default_timeout = 0.1
    agent, events = make_agent(sat_config)
    called = []

    async def blocked_preparation(*args, **kwargs):
        called.append(True)
        await asyncio.sleep(60)

    monkeypatch.setattr("agent.agent.prepare_command", blocked_preparation)
    payload = dict(message("preparation", "echo must-not-start"), git_repo_url="https://example.invalid/repo", git_branch="main")
    await agent._handle_execute_test_suite(payload)
    async with asyncio.timeout(6):
        await agent.legacy_runs["preparation"]
    assert called and not agent.running_suites
    assert events[-1]["type"] == "test_suite_completed" and "超时" in events[-1]["message"]


@pytest.mark.asyncio
@pytest.mark.parametrize("timeout", [0.3, 0.9], ids=["checkpoint-only", "already-reported"])
async def test_legacy_timeout_preserves_completed_checkpoint_without_error_replacement(sat_config, timeout):
    sat_config.default_timeout = timeout
    agent, events = make_agent(sat_config)
    agent.logger = logger
    row = dict(test_name="finished", case_id="case", status="passed", duration=0.01)
    source = (
        "import time;from pathlib import Path;time.sleep(0.08);"
        f"Path('xat/test_results.json').write_text({json.dumps([row])!r});time.sleep(60)"
    )
    await agent._handle_execute_test_suite(message("partial", script_command(source)))
    async with asyncio.timeout(6):
        await agent.legacy_runs["partial"]
    rows = [event for event in events if event["type"] == "test_suite_result"]
    assert rows and all(event["result"] == "passed" for event in rows)
    assert events[-1]["type"] == "test_suite_completed" and events[-1]["status"] == "failed"


@pytest.mark.asyncio
@pytest.mark.parametrize("cancel", [False, True])
async def test_preparation_subprocess_timeout_and_cancel_reap_child(tmp_path, cancel):
    marker = tmp_path / "prepare.pid"
    source = "import os,time;from pathlib import Path;" + f"Path({str(marker)!r}).write_text(str(os.getpid()));time.sleep(60)"
    task = asyncio.create_task(prepare_command([sys.executable, "-c", source], timeout=10 if cancel else 0.2))
    try:
        await until(marker.exists)
        if cancel:
            task.cancel()
        with pytest.raises(asyncio.CancelledError if cancel else TimeoutError):
            await task
        assert stopped(int(marker.read_text()))
    finally:
        if not task.done():
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)


@pytest.mark.asyncio
async def test_preparation_drains_both_pipes_but_keeps_only_explicit_tail():
    result = await prepare_command([
        sys.executable, "-c",
        "import os;os.write(1,b'A'*(2*1024*1024)+b'OUT-END');os.write(2,b'B'*(2*1024*1024)+b'ERR-END')",
    ], timeout=5)
    assert result.returncode == 0
    assert result.stdout.endswith("OUT-END") and result.stderr.endswith("ERR-END")
    assert len(result.stdout.encode()) < 66 * 1024 and len(result.stderr.encode()) < 66 * 1024
    assert "截断" in result.stdout and "截断" in result.stderr


@pytest.mark.asyncio
@pytest.mark.parametrize("command", ["echo legacy", "xat --mode offline"])
async def test_start_log_backpressure_cannot_disable_suite_timeout(sat_config, monkeypatch, command):
    sat_config.default_timeout = 0.1
    agent, events = make_agent(sat_config)
    never = asyncio.Event()

    async def send(payload):
        if payload["type"] == "test_suite_log":
            await never.wait()
        events.append(dict(payload))
        return True

    agent.ws_client.send_message = send
    monkeypatch.setattr("agent.sat_runner.build_invocation", lambda *args: ([sys.executable, "-c", "pass"], os.environ.copy()))
    await agent._handle_execute_test_suite(message("backpressure", command))
    tasks = [*agent.legacy_runs.values(), *agent.sat_runner.runs.values()]
    async with asyncio.timeout(5):
        await asyncio.gather(*tasks)
    assert events[-1]["type"] == "test_suite_completed" and events[-1]["status"] == "failed"
    assert "超时" in events[-1]["message"]
    assert not agent.execution_admission.tickets


@pytest.mark.asyncio
async def test_raw_cancel_interrupts_log_callback_and_cleans_process(tmp_path):
    entered = asyncio.Event()

    async def blocked_log(*args):
        entered.set()
        await asyncio.Event().wait()

    executor = TaskExecutor(tmp_path, on_log=blocked_log)
    task = asyncio.create_task(executor.execute_task(dict(
        task_id="blocked", command=[sys.executable, "-c", "import time;print('ready',flush=True);time.sleep(60)"], timeout=60,
    )))
    try:
        async with asyncio.timeout(5):
            await entered.wait()
            await executor.cancel_task("blocked")
            result = await task
        assert result["status"] == "cancelled"
        assert not executor.tasks and not executor.runners and not executor.finalizing
    finally:
        if not task.done():
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)


@pytest.mark.asyncio
async def test_legacy_stdout_preserves_whitespace_and_marks_raw(sat_config):
    agent, events = make_agent(sat_config)
    text = "spaces  \n\nno-newline\t "
    command = script_command(f"import sys;sys.stdout.write({text!r})")
    await agent._handle_execute_test_suite(message("whitespace", command))
    await agent.legacy_runs["whitespace"]
    assert "".join(row["message"] for row in events if row.get("raw")) == text


@pytest.mark.asyncio
async def test_legacy_result_preview_is_bounded_without_truncating_raw_logs(sat_config):
    agent, events = make_agent(sat_config)
    row = dict(test_name="finished", case_id="case", status="passed", duration=0.01)
    source = (
        "import sys;from pathlib import Path;"
        "sys.stdout.write('x' * 200000 + 'TAIL-END');sys.stdout.flush();"
        f"Path('xat/test_results.json').write_text({json.dumps([row])!r})"
    )
    await agent._handle_execute_test_suite(message("preview", script_command(source)))
    await agent.legacy_runs["preview"]
    raw = "".join(event["message"] for event in events if event.get("raw"))
    result = next(event for event in events if event["type"] == "test_suite_result")
    assert raw == "x" * 200000 + "TAIL-END"
    assert len(result["log_output"]) < 66000
    assert result["log_output"].endswith("TAIL-END")
    assert "characters omitted" in result["log_output"]
    assert result["result"] == "passed" and events[-1]["status"] == "completed"


@pytest.mark.asyncio
async def test_oversized_checkpoint_fails_explicitly_without_loading_json(sat_config):
    agent, events = make_agent(sat_config)
    source = "from pathlib import Path;f=Path('xat/test_results.json').open('wb');f.truncate(16*1024*1024+1);f.close()"
    await agent._handle_execute_test_suite(message("too-large", script_command(source)))
    await agent.legacy_runs["too-large"]
    assert events[-1]["type"] == "test_suite_completed" and events[-1]["status"] == "failed"
    assert "超过16MiB" in events[-1]["message"]


@pytest.mark.asyncio
async def test_legacy_offline_results_and_lost_ack_replay_before_completion(sat_config, plan_lab):
    from api.v1.websocket import handle_test_suite_completed
    from models import TestExecution as Execution, Notification
    from models.test_suite import TestSuiteExecution as SuiteExecution
    from services.suite_results import handle_run_result
    from services.task_queue_service import TaskQueueService

    db, _ = plan_lab
    TaskQueueService.add_to_queue(db, "node", "suite-0", "offline", "owner")
    assert TaskQueueService.start_task(db, "offline")
    agent, _ = make_agent(sat_config)
    online, lost_ack = False, False
    delivered = []

    async def send(payload):
        nonlocal lost_ack
        if payload["type"] == "test_suite_log":
            return True
        if not online:
            return False
        delivered.append(payload["type"])
        if payload["type"] == "test_suite_result":
            accepted = handle_run_result(db, "node", payload)
            if not lost_ack:
                lost_ack = True
                return True
        else:
            accepted = await handle_test_suite_completed(db, "node", payload)
        if accepted:
            agent.sat_runner.acknowledge(payload["event_id"])
        return True

    agent.ws_client.send_message = send
    row = dict(test_name="finished", case_id="case-0", status="passed", duration=0.01)
    command = script_command(f"from pathlib import Path;Path('xat/test_results.json').write_text({json.dumps([row])!r})")
    payload = dict(message("offline", command, suite_id="suite-0"), case_ids=["case-0"], case_codes=["CODE-0"])
    await agent._handle_execute_test_suite(payload)
    await agent.legacy_runs["offline"]
    assert len(list(agent.sat_runner.outbox.glob("*.json"))) == 2
    online = True
    await agent.sat_runner.flush()
    assert delivered == ["test_suite_result", "test_suite_completed"]
    await agent.sat_runner.flush()
    assert delivered[-1] == "test_suite_result"
    assert not list(agent.sat_runner.outbox.glob("*.json"))
    assert db.query(SuiteExecution).count() == db.query(Execution).count() == 1
    assert db.query(Notification).count() == 1


@pytest.mark.asyncio
async def test_native_start_log_backpressure_has_deadline_before_request(sat_config, monkeypatch):
    sat_config.default_timeout = 0.1
    agent, events = make_agent(sat_config)
    monkeypatch.setattr(sys, "path", sys.path.copy())

    async def send(payload):
        if payload["type"] == "test_suite_log":
            await asyncio.Event().wait()
        events.append(dict(payload))
        return True

    agent.ws_client.send_message = send
    payload = dict(message("native-block", "ats-native-http"), native_cases=[{
        "id": "case", "category": "api", "requests": [{"name": "never sent", "url": "http://127.0.0.1:1"}],
    }])
    await agent._handle_execute_test_suite(payload)
    async with asyncio.timeout(5):
        await agent.native_http_runner.runs["native-block"]
    assert events[-1]["type"] == "test_suite_completed" and events[-1]["status"] == "failed"
    assert "启动日志超时" in events[-1]["message"]
    assert not agent.execution_admission.tickets


@pytest.mark.asyncio
@pytest.mark.parametrize("leader_mode", ["exited", "live", "ignore-term"])
async def test_detached_descendant_inherited_pipe_cannot_pin_cleanup(tmp_path, leader_mode):
    from agent.script_runtime import stop_script_process

    if os.name != "posix":
        pytest.skip("POSIX session/pipe regression")
    marker = tmp_path / "detached.pid"
    source = (
        "import subprocess,sys,signal;from pathlib import Path;"
        + ("signal.signal(signal.SIGTERM,signal.SIG_IGN);" if leader_mode == "ignore-term" else "")
        + "p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)'],start_new_session=True);"
        f"Path({str(marker)!r}).write_text(str(p.pid));"
        + ("import time;time.sleep(60)" if leader_mode != "exited" else "pass")
    )
    process = await asyncio.create_subprocess_exec(
        sys.executable, "-c", source, stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE, start_new_session=True,
    )
    child_pid = None
    try:
        await until(marker.exists)
        child_pid = int(marker.read_text())
        if leader_mode != "exited":
            assert process.returncode is None
        else:
            await until(lambda: process.returncode is not None)
        async with asyncio.timeout(6):
            await stop_script_process(process)
        assert process.returncode is not None
        assert stopped(process.pid)
        # Detached sessions are outside the owned process group. Do not claim
        # cleanup killed that child; this test remains responsible for it.
        assert not stopped(child_pid)
    finally:
        if child_pid is not None:
            try:
                os.kill(child_pid, 9)
            except ProcessLookupError:
                pass
        if process.returncode is None:
            os.killpg(process.pid, 9)
        await process.wait()
