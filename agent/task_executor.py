"""任务执行器模块"""
import asyncio
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Callable, Awaitable
from loguru import logger as default_logger

# 支持直接运行和作为模块运行
try:
    from .utils import ensure_dir
    from .bounded_output import OutputTail, append_local_log
    from .script_runtime import positive_timeout, text_chunks, stop_script_process
except ImportError:
    from utils import ensure_dir
    from bounded_output import OutputTail, append_local_log
    from script_runtime import positive_timeout, text_chunks, stop_script_process


class TaskExecutor:
    """任务执行器类"""
    
    def __init__(
        self,
        work_dir: Path,
        on_log: Optional[Callable[[str, str, str], Awaitable[None]]] = None,
        logger=None,
        default_timeout: float = 3600,
        max_log_bytes=16 * 1024 * 1024,
        total_log_bytes=64 * 1024 * 1024,
    ):
        """
        初始化任务执行器
        
        Args:
            work_dir: 工作目录
            on_log: 日志回调函数 (task_id, level, message)
            logger: 日志器
        """
        self.work_dir = work_dir
        self.max_log_bytes = max_log_bytes
        self.total_log_bytes = total_log_bytes
        self.on_log = on_log
        self.logger = logger or default_logger
        self.default_timeout = default_timeout
        self.cancelled = set()
        self.runners = {}
        self.finalizing = set()
        self.tasks: Dict[str, asyncio.subprocess.Process] = {}  # task_id -> process
        self.task_logs: Dict[str, Path] = {}  # task_id -> log_file_path
    
    def _get_task_dir(self, task_id: str) -> Path:
        """
        获取任务目录
        
        Args:
            task_id: 任务ID
        
        Returns:
            任务目录路径
        """
        return self.work_dir / "tasks" / task_id
    
    def _get_task_log_file(self, task_id: str) -> Path:
        """
        获取任务日志文件路径
        
        Args:
            task_id: 任务ID
        
        Returns:
            日志文件路径
        """
        log_dir = self.work_dir / "logs" / "tasks"
        ensure_dir(log_dir)
        return log_dir / f"{task_id}.log"
    
    async def _log(self, task_id: str, level: str, message: str) -> None:
        """
        记录日志
        
        Args:
            task_id: 任务ID
            level: 日志级别
            message: 日志内容
        """
        # A quota/error must reach execute_task so it terminates the child and
        # reports evidence-storage failure, rather than silently dropping logs.
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        append_local_log(self._get_task_log_file(task_id),
                         f"[{timestamp}] [{level.upper()}] {message}\n",
                         self.max_log_bytes, self.total_log_bytes)
        if self.on_log:
            await self.on_log(task_id, level, message)

    async def execute_task(self, task_config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute asynchronously so silent commands cannot block heartbeat/cancel."""
        task_id, command = task_config.get("task_id"), task_config.get("command")
        started, output, process = datetime.now(), OutputTail(), None
        status, error = "error", None
        timeout = task_config.get("timeout", self.default_timeout)
        self.runners[task_id] = asyncio.current_task()
        try:
            timeout = positive_timeout(timeout)
            if not task_id or not command:
                raise ValueError("task_id和command是必需的")
            if task_id in self.cancelled:
                raise asyncio.CancelledError
            async with asyncio.timeout(timeout):
                task_dir = Path(task_config["work_dir"]).expanduser().resolve() if task_config.get("work_dir") else self._get_task_dir(task_id)
                ensure_dir(task_dir)
                env = os.environ.copy()
                env.update(task_config.get("env_vars", {}))
                options = dict(cwd=str(task_dir), env=env, stdout=asyncio.subprocess.PIPE,
                               stderr=asyncio.subprocess.STDOUT, start_new_session=(os.name == "posix"))
                if isinstance(command, str):
                    process = await asyncio.create_subprocess_shell(command, **options)
                else:
                    process = await asyncio.create_subprocess_exec(*command, **options)
                self.tasks[task_id] = process
                if task_id in self.cancelled:
                    raise asyncio.CancelledError
                async for text in text_chunks(process.stdout):
                    output.append(text)
                    await self._log(task_id, "info", text)
                code = await process.wait()
            status = "cancelled" if task_id in self.cancelled else "success" if code == 0 else "failed"
            error = None if code == 0 else f"进程退出码: {code}"
        except asyncio.TimeoutError:
            status, error = "timeout", f"任务执行超时（{timeout}秒）"
        except asyncio.CancelledError:
            status, error = "cancelled", "任务已取消"
        except Exception as exc:
            error = str(exc)
            self.logger.exception("任务执行失败：{}", task_id)
        finally:
            self.finalizing.add(task_id)
            try:
                if process:
                    await stop_script_process(process)
            finally:
                self.tasks.pop(task_id, None)
                self.cancelled.discard(task_id)
                self.runners.pop(task_id, None)
                self.finalizing.discard(task_id)
        return {"task_id": task_id, "status": status,
                "exit_code": process.returncode if process else -1,
                "output": output.render(), "error": error,
                "duration": (datetime.now() - started).total_seconds()}

    async def cancel_task(self, task_id: str) -> bool:
        try:
            from .sat_runner import terminate_process
        except ImportError:
            from sat_runner import terminate_process
        self.cancelled.add(task_id)
        runner = self.runners.get(task_id)
        if runner and task_id not in self.finalizing and not runner.cancelling():
            runner.cancel()
        process = self.tasks.get(task_id)
        if process is None:
            return False
        await terminate_process(process)
        return True

    def get_task_status(self, task_id: str) -> Optional[str]:
        """
        获取任务状态
        
        Args:
            task_id: 任务ID
        
        Returns:
            任务状态 (running/completed/not_found)
        """
        if task_id not in self.tasks:
            return "not_found"
        
        process = self.tasks[task_id]
        if process.returncode is None:
            return "running"
        else:
            return "completed"

