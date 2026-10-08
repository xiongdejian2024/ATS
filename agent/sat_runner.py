"""SAT runner using existing suite protocol and an isolated directory per execution."""

import asyncio
import json
import math
import os
import shlex
import signal
import sys
import time
import uuid
from pathlib import Path
from loguru import logger

try:
    from .script_runtime import positive_timeout, text_chunks, stop_script_process
except ImportError:
    from script_runtime import positive_timeout, text_chunks, stop_script_process


def parse_command(command):
    import argparse

    class Parser(argparse.ArgumentParser):
        def error(self, message):
            raise ValueError(message)

    parser = Parser(prog="xat")
    parser.add_argument("--mode", choices=["offline", "sat", "hardware"], default="offline")
    parser.add_argument("--tests", default="cases/src/xat_cases/legacy")
    parser.add_argument("--bench-config")
    parser.add_argument("--case-config")
    parser.add_argument("--timeout", type=float)
    parts = shlex.split(command)
    if not parts or parts[0] not in {"xat", "ats-sat"}:
        raise ValueError("执行命令需要以 xat 或 ats-sat 开头")
    try:
        return parser.parse_args(parts[1:])
    except (SystemExit, argparse.ArgumentError) as exc:
        raise ValueError("XAT 执行选项无效") from exc


def build_invocation(config, options, directory, selection):
    """Agent 负责进程控制；SAT/ECU 的配置与执行由 XAT 统一处理。"""
    ats_root = Path(__file__).resolve().parents[1]
    xat_root = ats_root / "xat"
    if str(xat_root) not in sys.path:
        sys.path.insert(0, str(xat_root))
    from framework.integrations.runtime import IntegrationSettings

    settings = IntegrationSettings(
        mode=options.mode,
        sat_root=config.sat_root,
        ecu_root=config.ecu_root,
        allow_hardware=config.sat_allow_hardware,
    )
    settings.prepare()
    if options.mode in {"sat", "hardware"}:
        settings.sat_path(options.tests)
    for value in (options.bench_config, options.case_config):
        if value:
            settings.sat_path(value)
    selection_path = directory / "selection.json"
    selection_path.write_text(json.dumps(selection), encoding="utf-8")
    env = os.environ.copy()
    env.update(
        {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONUNBUFFERED": "1",
            "XAT_ALLOW_HARDWARE": "true" if settings.allow_hardware else "false",
            "XAT_PROJECT_ROOT": str(settings.sat_root),
            "PYTHONPATH": os.pathsep.join(
                [
                    str(xat_root),
                    str(xat_root / "packages/ecu/src"),
                    str(xat_root / "cases/src"),
                    str(ats_root),
                ]
            ),
        }
    )
    # 明确传入本次选择和输出目录，不继承别的任务的选择文件。
    for key in ("ATS_CASE_SELECTION", "ATS_RESULT_FILE"):
        env.pop(key, None)
    command = [
        config.sat_python or sys.executable,
        "-m",
        "framework",
        "--mode",
        options.mode,
        "--sat-root",
        str(settings.sat_root),
        "--ecu-root",
        str(settings.ecu_root),
        "--selection",
        str(selection_path),
        "--output-dir",
        str(directory),
    ]
    if settings.allow_hardware:
        command.append("--allow-hardware")
    if options.mode in {"sat", "hardware"}:
        command += ["--tests", options.tests]
    for flag, value in [
        ("--bench-config", options.bench_config),
        ("--case-config", options.case_config),
    ]:
        if value:
            command += [flag, value]
    return command, env


def read_results(path, case_ids):
    """Read only complete, selected case rows from XAT's atomic checkpoint."""
    if not path.exists():
        return []
    with path.open("rb") as source:
        contents = source.read(16 * 1024 * 1024 + 1)
    if len(contents) > 16 * 1024 * 1024:
        raise ValueError("XAT 结果文件超过16MiB，已拒绝读取")
    rows = json.loads(contents)
    if not isinstance(rows, list):
        raise ValueError("XAT 结果必须为列表")
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("XAT 结果行格式无效")
        case_id, duration = row.get("case_id"), row.get("duration")
        if (
            not isinstance(case_id, str)
            or case_id not in case_ids
            or case_id in seen
            or row.get("status") not in ("passed", "failed", "skipped", "error")
            or isinstance(duration, bool)
            or not isinstance(duration, (int, float))
            or not math.isfinite(duration)
            or duration < 0
        ):
            raise ValueError("XAT 结果包含无效或重复的用例数据")
        seen.add(case_id)
    return rows


async def terminate_process(process, *, blocking=False):
    """Stop an owned session, including children outliving its shell leader."""
    async def wait():
        # asyncio.Process.wait() may also wait for EOF on inherited pipes. An
        # escaped descendant can hold those pipes after the owned leader exits.
        # Wait for OS child exit here; stop_script_process bounds pipe draining
        # separately. Popen.poll() also reaps blocking subprocess children.
        while (process.poll() if blocking else process.returncode) is None:
            await asyncio.sleep(0.02)

    alive = process.poll() is None if blocking else process.returncode is None
    try:
        if os.name == "posix":
            # Even an exited leader can leave a live background child/group.
            os.killpg(process.pid, signal.SIGTERM)
        elif alive:
            process.terminate()
        if alive:
            try:
                await asyncio.wait_for(wait(), timeout=3)
            except asyncio.TimeoutError:
                if os.name != "posix":
                    process.kill()
    except ProcessLookupError:
        logger.opt(exception=True).debug("子进程组已退出，无需再次终止")
    finally:
        if os.name == "posix":
            try:
                # Shell exit is not proof that descendants honored SIGTERM.
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        if alive:
            await wait()
        if os.name == "posix":
            import psutil

            # Zombies have exited and no longer own execution resources. Keep
            # the slot if an OS-level process has not yet actually stopped.
            while True:
                running = False
                for child in psutil.process_iter():
                    try:
                        if os.getpgid(child.pid) == process.pid and child.status() not in (
                            psutil.STATUS_ZOMBIE, psutil.STATUS_DEAD
                        ):
                            running = True
                            break
                    except (ProcessLookupError, PermissionError, psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                if not running:
                    break
                await asyncio.sleep(0.02)


class SATRunner:
    def __init__(self, agent):
        self.agent = agent
        self.runs = {}
        self.suites = {}
        self.executed = set()
        self.started = set()
        self.cancel_requested = set()
        self.finalizing = set()
        self.delivery_lock = asyncio.Lock()

    @property
    def outbox(self):
        return self.agent.work_dir / "sat-outbox"

    async def deliver(self, payload):
        delivery = getattr(self.agent, "log_delivery", None)
        if delivery and payload.get("type") in {"test_suite_completed", "script_job_completed"}:
            diagnostic = delivery.diagnostics()
            if diagnostic["blocked_reason"] or diagnostic["backpressured"]:
                payload["log_delivery"] = diagnostic
                reason = diagnostic["blocked_reason"] or "spool_quota_backpressure"
                payload["message"] = (payload.get("message") or "") + f"；日志传输受阻：{reason}，未确认记录保留在 Agent"
        self.outbox.mkdir(parents=True, exist_ok=True)
        key = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                payload["execution_id"] + ":" + (payload.get("case_id") or "completed"),
            )
        )
        payload["event_id"] = key
        path = self.outbox / (key + ".json")
        temporary = path.with_suffix(".tmp")
        with open(
            temporary,
            "w",
            encoding="utf-8",
            opener=lambda path, flags: os.open(path, flags, 0o600),
        ) as output:
            os.fchmod(output.fileno(), 0o600)
            output.write(json.dumps(payload))
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
        await self.flush()

    async def flush(self):
        if not self.agent.work_dir or not self.agent.ws_client:
            return
        async with self.delivery_lock:
            if not self.outbox.exists():
                return
            # Results must reach the backend before completion releases the queue.
            pending = []
            for path in self.outbox.glob("*.json"):
                try:
                    payload = json.loads(path.read_text(encoding="utf-8"))
                    if not isinstance(payload, dict) or "type" not in payload:
                        raise ValueError("待回传消息必须包含 type 字段")
                    pending.append((path, payload))
                except (ValueError, OSError):
                    logger.exception("读取待回传消息失败，保留损坏文件供排查：{}", path)
                    path.rename(path.with_suffix(".invalid"))
            pending.sort(
                key=lambda entry: (
                    entry[1]["type"] == "test_suite_completed",
                    entry[0].name,
                )
            )
            for path, payload in pending:
                if payload["type"] == "script_job_completed" and "script_jobs_v1" not in getattr(self.agent.ws_client, "server_capabilities", ()):
                    continue
                if not await self.agent.ws_client.send_message(payload):
                    break

    def acknowledge(self, event_id):
        try:
            uuid.UUID(event_id)
        except (ValueError, TypeError, AttributeError):
            return
        (self.outbox / (event_id + ".json")).unlink(missing_ok=True)

    def has_suite(self, suite_id):
        return suite_id in self.suites.values()

    def start(self, message):
        execution_id = message["execution_id"]
        if execution_id in self.runs or execution_id in self.executed:
            return
        try:
            from .execution_admission import admission_for
        except ImportError:
            from execution_admission import admission_for
        admission = admission_for(self.agent)
        if not admission.register(execution_id):
            return
        self.executed.add(execution_id)
        self.suites[execution_id] = message["suite_id"]
        self.runs[execution_id] = asyncio.create_task(self._execute_admitted(message))

    async def _execute_admitted(self, message):
        execution_id = message["execution_id"]
        admission = self.agent.execution_admission
        try:
            if not await admission.wait(execution_id):
                self.cancel_requested.add(execution_id)
            await self.execute(message)
        finally:
            # Also covers failures before the runner enters its own try/finally.
            self.started.discard(execution_id)
            self.cancel_requested.discard(execution_id)
            self.finalizing.discard(execution_id)
            self.runs.pop(execution_id, None)
            self.suites.pop(execution_id, None)
            admission.release(execution_id)
            if execution_id not in admission.seen:
                self.executed.discard(execution_id)

    async def cancel(self, suite_id, execution_id=None):
        tasks = [
            (key, task)
            for key, task in self.runs.items()
            if self.suites[key] == suite_id and (execution_id is None or key == execution_id)
        ]
        for key, task in tasks:
            self.cancel_requested.add(key)
            self.agent.execution_admission.cancel_waiting(key)
            # A task cancelled before its first turn never enters its finally.
            # Let execute consume that request; once finalizing, cancellation
            # waits for durable results/completion instead of interrupting them.
            if key in self.started and key not in self.finalizing and not task.cancelling():
                task.cancel()
        await asyncio.gather(*(asyncio.shield(task) for _, task in tasks), return_exceptions=True)

    async def log(self, message, text, *, raw=False):
        await self.agent.ws_client.send_message(
            {
                "type": "test_suite_log",
                "suite_id": message["suite_id"],
                "execution_id": message["execution_id"],
                "level": "info",
                "message": text,
                "raw": raw,
            }
        )

    async def execute(self, message):
        suite_id, execution_id = message["suite_id"], message["execution_id"]
        process, rows, error, status = None, [], None, "failed"
        exit_code = None
        started = time.monotonic()
        directory = self.agent.work_dir / "suites" / suite_id / "executions" / execution_id
        directory.mkdir(parents=True, exist_ok=True)
        self.started.add(execution_id)
        try:
            if execution_id in self.cancel_requested:
                raise asyncio.CancelledError
            options = parse_command(message["execution_command"])
            ids, codes = message["case_ids"], message.get("case_codes", [])
            if len(ids) != len(codes) or len(set(codes)) != len(codes) or not all(codes):
                raise ValueError("每个所选 ATS 用例需要唯一的 XAT 用例编号")
            timeout = (
                options.timeout
                if options.timeout is not None
                else self.agent.config.default_timeout
            )
            timeout = positive_timeout(timeout)
            command, env = build_invocation(
                self.agent.config, options, directory, dict(zip(codes, ids))
            )
            logger.info(
                "开始 XAT/SAT 执行：执行ID={}，模式={}，用例数={}",
                execution_id,
                options.mode,
                len(ids),
            )
            async with asyncio.timeout(timeout):
                await self.log(message, "开始 XAT/SAT 执行，模式：" + options.mode)
                process = await asyncio.create_subprocess_exec(
                    *command,
                    cwd=str(directory),
                    env=env,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT,
                    start_new_session=(os.name == "posix"),
                )

                async def read_output():
                    try:
                        from .bounded_output import append_local_log
                    except ImportError:
                        from bounded_output import append_local_log
                    async for text in text_chunks(process.stdout):
                        append_local_log(
                            directory / "output.log", text,
                            getattr(self.agent.config, "task_log_max_bytes", 16 * 1024 * 1024),
                            getattr(self.agent.config, "task_logs_total_bytes", 64 * 1024 * 1024),
                            quota_root=self.agent.work_dir,
                            quota_pattern="suites/*/executions/*/output.log",
                        )
                        await self.log(message, text, raw=True)
                    return await process.wait()

                exit_code = await read_output()
            if exit_code:
                error = f"XAT pytest 退出码为 {exit_code}，详情见 output.log"
        except asyncio.CancelledError:
            status, error = "cancelled", "执行已取消"
            logger.opt(exception=True).info("XAT/SAT 执行已取消：{}", execution_id)
        except asyncio.TimeoutError:
            error = "XAT 执行超时"
            logger.exception("XAT/SAT 执行超时：{}", execution_id)
        except Exception as exc:
            error = str(exc)
            logger.exception("XAT/SAT 执行失败：{}", execution_id)
        finally:
            self.finalizing.add(execution_id)
            try:
                if process:
                    await stop_script_process(process)
                # XAT checkpoints each completed teardown atomically. Stop the
                # writer first, then recover the last checkpoint on every exit.
                if process:
                    try:
                        rows = read_results(directory / "results.json", message["case_ids"])
                    except (ValueError, OSError) as exc:
                        error = error or f"读取 XAT 结果失败：{exc}"
                        logger.exception("读取 XAT 执行结果失败：{}", execution_id)
                if status != "cancelled":
                    status = (
                        "completed"
                        if exit_code == 0
                        and error is None
                        and len(rows) == len(message["case_ids"])
                        and all(row["status"] in {"passed", "skipped"} for row in rows)
                        else "failed"
                    )
                row_by_id = {row["case_id"]: row for row in rows}
                for case_id in message["case_ids"]:
                    # Cancellation is intentional: retain finished cases without
                    # synthesizing failures for work that never completed.
                    if status == "cancelled" and case_id not in row_by_id:
                        continue
                    row = row_by_id.get(
                        case_id,
                        {
                            "status": "error",
                            "duration": 0,
                            "error": error or "XAT 未产生对应结果",
                        },
                    )
                    await self.deliver(
                        {
                            "type": "test_suite_result",
                            "suite_id": suite_id,
                            "execution_id": execution_id,
                            "case_id": case_id,
                            "result": row["status"],
                            "duration": f'{row["duration"]:.3f}s',
                            "error_message": row.get("error"),
                            "log_output": row.get("log") or row.get("error"),
                            "executor_id": message.get("executor_id", "system"),
                        }
                    )
                (directory / "run.json").write_text(
                    json.dumps(
                        {
                            "execution_id": execution_id,
                            "status": status,
                            "error": error,
                            "exit_code": process.returncode if process else None,
                            "outcome": (
                                "cancelled"
                                if status == "cancelled"
                                else ("timeout" if error == "XAT 执行超时" else status)
                            ),
                        }
                    ),
                    encoding="utf-8",
                )
                await self.deliver(
                    {
                        "type": "test_suite_completed",
                        "suite_id": suite_id,
                        "execution_id": execution_id,
                        "status": status,
                        "message": error or "XAT/SAT 执行已结束",
                        "duration": f"{time.monotonic() - started:.3f}s",
                        "total_case_count": len(message["case_ids"]),
                        "reported_case_count": len(rows),
                        "exit_code": process.returncode if process else None,
                        "outcome": (
                            "cancelled"
                            if status == "cancelled"
                            else ("timeout" if error == "XAT 执行超时" else status)
                        ),
                    }
                )
                logger.info(
                    "XAT/SAT 执行结束：执行ID={}，状态={}，结果数={}",
                    execution_id,
                    status,
                    len(rows),
                )
            finally:
                self.started.discard(execution_id)
                self.cancel_requested.discard(execution_id)
                self.finalizing.discard(execution_id)
                if self.runs.get(execution_id) is asyncio.current_task():
                    self.runs.pop(execution_id, None)
                    self.suites.pop(execution_id, None)
