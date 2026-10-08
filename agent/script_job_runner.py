"""Plain scripts using formal execution IDs, shared admission and durable delivery."""
import asyncio
import json
import math
import os
import re
import sys
import uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
try:
    from .execution_admission import admission_for
    from .task_executor import TaskExecutor
except ImportError:
    from execution_admission import admission_for
    from task_executor import TaskExecutor


def identifier(value):
    return isinstance(value, str) and re.fullmatch(r"[a-zA-Z0-9_-]{1,36}", value)


def validate_config(config):
    if not isinstance(config, dict):
        raise ValueError("脚本配置无效")
    mode = config.get("mode")
    source, command, args = config.get("script", ""), config.get("command", ""), config.get("args", [])
    cwd, timeout = config.get("workDir", ""), config.get("timeoutSeconds", 3600)
    if (mode not in {"shell", "python", "command"} or not isinstance(source, str)
            or not isinstance(command, str) or not isinstance(cwd, str)
            or not isinstance(args, list) or len(args) > 128
            or any(not isinstance(arg, str) or len(arg) > 8192 for arg in args)):
        raise ValueError("脚本配置类型无效")
    if (len(command) > 4096 or len(cwd) > 500 or len(source.encode()) > 65536
            or any("\x00" in v for v in [source, command, cwd, *args])
            or len(json.dumps([source, command, cwd, *args], ensure_ascii=False).encode()) > 128 * 1024):
        raise ValueError("脚本配置超出上限或包含NUL")
    if (mode == "command" and (not command.strip() or source)
            or mode != "command" and (not source.strip() or command)):
        raise ValueError("脚本内容与运行模式不一致")
    if type(timeout) not in (int, float) or not math.isfinite(timeout) or not 1 <= timeout <= 86400:
        raise ValueError("脚本超时必须为1至86400秒的有限数值")
    for path in (PurePosixPath(cwd), PureWindowsPath(cwd)):
        if path.is_absolute() or path.drive or ".." in path.parts:
            raise ValueError("工作目录必须为工作空间内的相对路径")
    return mode, source, command, args, cwd, timeout


class ScriptJobRunner:
    def __init__(self, agent):
        self.agent = agent
        self.runs, self.jobs, self.executors = {}, {}, {}
        self.finalizing = set()
        self.cancel_requested = set()

    def directory(self, job_id, execution_id):
        return Path(self.agent.work_dir) / "script-jobs" / job_id / "executions" / execution_id

    def start(self, message):
        execution_id, job_id = message.get("execution_id"), message.get("script_job_id")
        if (not identifier(execution_id) or not identifier(job_id)
                or not message.get("dispatch_session_id")
                or message["dispatch_session_id"] != getattr(self.agent.ws_client, "session_id", None)):
            return False
        if not admission_for(self.agent).register(execution_id):
            return False
        self.jobs[execution_id] = job_id
        self.runs[execution_id] = asyncio.create_task(self.execute(message))
        return True

    async def log(self, execution_id, level, text):
        await self.agent.ws_client.send_message(dict(type="script_job_log", script_job_id=self.jobs[execution_id],
            execution_id=execution_id, level=level, message=text, raw=True))

    async def execute(self, message):
        execution_id, job_id = message["execution_id"], message["script_job_id"]
        result = dict(status="error", exit_code=None, duration=0, error="脚本未执行")
        try:
            if not await admission_for(self.agent).wait(execution_id) or execution_id in self.cancel_requested:
                result.update(status="cancelled", error="执行在启动前已取消")
            else:
                await self.agent.ws_client.send_message(dict(type="script_job_state", script_job_id=job_id,
                    execution_id=execution_id, state="running"))
                mode, source, command, args, relative, timeout = validate_config(message.get("config"))
                directory = self.directory(job_id, execution_id)
                directory.mkdir(parents=True, exist_ok=True)
                root = Path(self.agent.work_dir).resolve()
                cwd = (root / relative).resolve() if relative else directory.resolve()
                cwd.relative_to(root)  # Reject traversal through a workspace symlink.
                cwd.mkdir(parents=True, exist_ok=True)
                if mode != "command":
                    filename = directory / ("script.py" if mode == "python" else "script.cmd" if os.name == "nt" else "script.sh")
                    with open(filename, "w", encoding="utf-8", newline="", opener=lambda p, flags: os.open(p, flags, 0o600)) as output:
                        output.write(source)
                    command = ([sys.executable, "-u", str(filename)] if mode == "python" else
                               [os.environ.get("COMSPEC", "cmd.exe"), "/D", "/C", str(filename)] if os.name == "nt" else ["/bin/sh", str(filename)]) + args
                else:
                    command = [command, *args]
                config = self.agent.config
                executor = TaskExecutor(root, on_log=self.log, logger=self.agent.logger,
                    max_log_bytes=getattr(config, "task_log_max_bytes", 16 * 1024 * 1024),
                    total_log_bytes=getattr(config, "task_logs_total_bytes", 64 * 1024 * 1024))
                if execution_id in self.cancel_requested:
                    raise asyncio.CancelledError
                self.executors[execution_id] = executor
                result = await executor.execute_task(dict(task_id=execution_id, command=command, work_dir=str(cwd), timeout=timeout))
        except asyncio.CancelledError:
            result.update(status="cancelled", error="脚本执行已取消")
        except Exception as exc:
            result.update(status="error", error=str(exc))
        finally:
            self.finalizing.add(execution_id)
            try:
                # TaskExecutor returns only after its process-group teardown.
                # Persist terminal evidence before releasing the admission slot.
                await self.agent.sat_runner.deliver(dict(type="script_job_completed", script_job_id=job_id,
                    execution_id=execution_id, result=result["status"], exit_code=result["exit_code"],
                    duration_seconds=result["duration"], error=result.get("error")))
            finally:
                self.runs.pop(execution_id, None); self.jobs.pop(execution_id, None)
                self.executors.pop(execution_id, None); self.finalizing.discard(execution_id)
                self.cancel_requested.discard(execution_id)
                admission_for(self.agent).release(execution_id)

    async def state(self, job_id, execution_id, dispatch_session_id=None):
        if not identifier(job_id) or not identifier(execution_id):
            return
        if execution_id in self.runs:
            if self.jobs[execution_id] != job_id:
                return
            state = "running"
        else:
            event = str(uuid.uuid5(uuid.NAMESPACE_URL, execution_id + ":completed"))
            pending = self.agent.sat_runner.outbox / (event + ".json")
            if pending.is_file():
                try:
                    payload = json.loads(pending.read_text())
                    state = "terminal_pending" if payload.get("script_job_id") == job_id else "unknown"
                except (ValueError, OSError):
                    state = "unknown"
            else:
                marker = admission_for(self.agent)._marker(execution_id)
                same_session = bool(dispatch_session_id and dispatch_session_id == getattr(self.agent.ws_client, "session_id", None))
                state = "never_started" if same_session and not marker.exists() and not self.directory(job_id, execution_id).exists() else "unknown"
        await self.agent.ws_client.send_message(dict(type="script_job_state", script_job_id=job_id,
            execution_id=execution_id, state=state))
        if state == "terminal_pending":
            await self.agent.sat_runner.flush()

    async def cancel(self, job_id, execution_id, dispatch_session_id=None):
        if not identifier(job_id) or not identifier(execution_id):
            return
        task = self.runs.get(execution_id)
        if task:
            if self.jobs[execution_id] != job_id:
                return
            self.cancel_requested.add(execution_id)
            admission_for(self.agent).cancel_waiting(execution_id)
            executor = self.executors.get(execution_id)
            if executor:
                await executor.cancel_task(execution_id)
            elif execution_id not in self.finalizing and not task.cancelling():
                # A task that has not entered execute must run its finalizer.
                # Waiting admission was signalled above; no cancellation needed.
                pass
            await asyncio.shield(task)
            return
        admission = admission_for(self.agent)
        marker = admission._marker(execution_id)
        cancelled = False
        if marker.exists():
            try:
                cancelled = json.loads(marker.read_text()).get("state") == "cancelled-before-start"
            except (OSError, ValueError):
                pass
        elif (dispatch_session_id and dispatch_session_id == getattr(self.agent.ws_client, "session_id", None)
              and not self.directory(job_id, execution_id).exists()):
            cancelled = admission._persist(execution_id, "cancelled-before-start")
        if cancelled:
            await self.agent.sat_runner.deliver(dict(type="script_job_completed", script_job_id=job_id,
                execution_id=execution_id, result="cancelled", exit_code=None, duration_seconds=0,
                error="已持久记录禁止启动，本次执行已取消"))
        else:
            await self.state(job_id, execution_id, dispatch_session_id)

    async def close(self):
        for execution_id, job_id in list(self.jobs.items()):
            await self.cancel(job_id, execution_id)
