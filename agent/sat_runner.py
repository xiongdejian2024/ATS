"""SAT runner using existing suite protocol and an isolated directory per execution."""

import asyncio
import json
import os
import shlex
import signal
import sys
import time
import uuid
from pathlib import Path
from loguru import logger


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


async def terminate_process(process):
    """Terminate the runner and its children without blocking the event loop."""
    if process.returncode is not None:
        return
    try:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGTERM)
        else:
            process.terminate()
        await asyncio.wait_for(process.wait(), timeout=3)
    except asyncio.TimeoutError:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
        await process.wait()
    except ProcessLookupError:
        logger.opt(exception=True).debug("子进程已退出，无需再次终止")


class SATRunner:
    def __init__(self, agent):
        self.agent = agent
        self.runs = {}
        self.suites = {}
        self.executed = set()
        self.delivery_lock = asyncio.Lock()

    @property
    def outbox(self):
        return self.agent.work_dir / "sat-outbox"

    async def deliver(self, payload):
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
            temporary, "w", encoding="utf-8", opener=lambda path, flags: os.open(path, flags, 0o600)
        ) as output:
            os.fchmod(output.fileno(), 0o600)
            output.write(json.dumps(payload))
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
        self.executed.add(execution_id)
        self.suites[execution_id] = message["suite_id"]
        self.runs[execution_id] = asyncio.create_task(self.execute(message))

    async def cancel(self, suite_id, execution_id=None):
        tasks = [
            task
            for key, task in self.runs.items()
            if self.suites[key] == suite_id and (execution_id is None or key == execution_id)
        ]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    async def log(self, message, text):
        await self.agent.ws_client.send_message(
            {
                "type": "test_suite_log",
                "suite_id": message["suite_id"],
                "execution_id": message["execution_id"],
                "level": "info",
                "message": text,
            }
        )

    async def execute(self, message):
        suite_id, execution_id = message["suite_id"], message["execution_id"]
        process, rows, error, status = None, [], None, "failed"
        started = time.monotonic()
        directory = self.agent.work_dir / "suites" / suite_id / "executions" / execution_id
        directory.mkdir(parents=True, exist_ok=True)
        try:
            options = parse_command(message["execution_command"])
            ids, codes = message["case_ids"], message.get("case_codes", [])
            if len(ids) != len(codes) or len(set(codes)) != len(codes) or not all(codes):
                raise ValueError("每个所选 ATS 用例需要唯一的 XAT 用例编号")
            timeout = (
                options.timeout
                if options.timeout is not None
                else self.agent.config.default_timeout
            )
            if timeout <= 0:
                raise ValueError("XAT 超时时间必须大于零")
            command, env = build_invocation(
                self.agent.config, options, directory, dict(zip(codes, ids))
            )
            logger.info(
                "开始 XAT/SAT 执行：执行ID={}，模式={}，用例数={}",
                execution_id,
                options.mode,
                len(ids),
            )
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
                with (directory / "output.log").open("w", encoding="utf-8") as log:
                    while True:
                        chunk = await process.stdout.read(4096)
                        if not chunk:
                            break
                        text = chunk.decode("utf-8", errors="replace")
                        log.write(text)
                        log.flush()
                        await self.log(message, text)
                return await process.wait()

            exit_code = await asyncio.wait_for(read_output(), timeout=timeout)
            result_file = directory / "results.json"
            if result_file.exists():
                rows = json.loads(result_file.read_text(encoding="utf-8"))
            status = (
                "completed"
                if exit_code == 0
                and len(rows) == len(ids)
                and all(row["status"] in ["passed", "skipped"] for row in rows)
                else "failed"
            )
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
            if process:
                await terminate_process(process)
            try:
                if status != "cancelled":
                    row_by_id = {row["case_id"]: row for row in rows}
                    for case_id in message["case_ids"]:
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
                self.runs.pop(execution_id, None)
                self.suites.pop(execution_id, None)
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
                if self.runs.get(execution_id) is asyncio.current_task():
                    self.runs.pop(execution_id, None)
                    self.suites.pop(execution_id, None)
