"""原生HTTP执行适配器；复用已有可靠结果回传和按执行ID取消机制。"""

import asyncio
import json
import os
import re
import sys
import time
from pathlib import Path

try:
    from .sat_runner import SATRunner
    from .script_runtime import positive_timeout
except ImportError:
    from sat_runner import SATRunner
    from script_runtime import positive_timeout
from loguru import logger


class NativeHTTPRunner(SATRunner):
    def __init__(self, agent):
        super().__init__(agent)
        self.delivery_lock = agent.sat_runner.delivery_lock

    def start(self, message):
        # 后端发出UUID；路径验证也保护独立Agent免受畸形消息影响。
        if any(
            not re.fullmatch(r"[a-zA-Z0-9_-]{1,36}", str(message.get(key, "")))
            for key in ("suite_id", "execution_id")
        ):
            logger.error("原生HTTP请求缺少有效的测试套或执行ID")
            return
        directory = (
            self.agent.work_dir
            / "suites"
            / message["suite_id"]
            / "executions"
            / message["execution_id"]
        )
        if (directory / "native-run.json").exists():
            logger.info(
                "原生HTTP执行已结束，忽略重复派发：执行={}", message["execution_id"]
            )
            return
        super().start(message)

    async def execute(self, message):
        suite_id, execution_id = message["suite_id"], message["execution_id"]
        started, rows, status, error = time.monotonic(), [], "failed", None
        directory = (
            self.agent.work_dir / "suites" / suite_id / "executions" / execution_id
        )
        directory.mkdir(parents=True, exist_ok=True)
        self.started.add(execution_id)
        try:
            if execution_id in self.cancel_requested:
                raise asyncio.CancelledError
            # 与现有SAT适配器同样从工作区加载自有XAT，httpx/Pydantic均为XAT已有依赖。
            xat_path = str(Path(__file__).resolve().parents[1] / "xat")
            if xat_path not in sys.path:
                sys.path.insert(0, xat_path)
            from framework.native_http.models import FrozenCase
            from framework.native_http.engine import execute
            import httpx
            from urllib.parse import urlsplit, urlunsplit

            async def load_file(meta):
                address = urlsplit(self.agent.ws_client.server_url)
                scheme = {"ws": "http", "wss": "https"}[address.scheme]
                prefix = address.path.removesuffix("/ws/agent").rstrip("/")
                url = urlunsplit(
                    (
                        scheme,
                        address.netloc,
                        prefix
                        + "/api/v1/native-http/executions/"
                        + execution_id
                        + "/files/"
                        + meta.fileId,
                        "",
                        "",
                    )
                )
                async with httpx.AsyncClient(trust_env=False, timeout=60) as client:
                    response = await client.get(
                        url, headers={"X-Agent-Token": self.agent.ws_client.token}
                    )
                    response.raise_for_status()
                logger.info(
                    "冻结请求文件读取完成：执行={}，文件={}，字节={}",
                    execution_id,
                    meta.fileId,
                    len(response.content),
                )
                return response.content

            cases = [
                FrozenCase.model_validate(value)
                for value in message.get("native_cases", [])
            ]
            if (
                not cases
                or [case.id for case in cases] != message["case_ids"]
                or len({c.id for c in cases}) != len(cases)
            ):
                raise ValueError("冻结原生用例与本次选择范围不一致")
            # Logging backpressure is not covered by the HTTP engine's request
            # timeouts. Bound this startup await before invoking any request.
            async with asyncio.timeout(positive_timeout(self.agent.config.default_timeout)):
                await self.log(message, f"开始原生HTTP执行，实际用例数：{len(cases)}")
            hook_sequence = 0
            for case in cases:
                extended = 'native_http_processors_v1' in getattr(self.agent.ws_client, 'server_capabilities', ())
                requested = case.globalPreProcessors or case.globalPostProcessors or any(r.reportPhases or r.preProcessors or r.postProcessors or (r.mockResponse and r.mockResponse.enable) for r in case.requests)
                if not extended and requested:
                    raise ValueError('Controller未协商原生处理器和高级报告能力')
                async def execute_hook(hook):
                    nonlocal hook_sequence
                    hook_sequence += 1
                    try:
                        from .native_hook_runtime import execute as run_hook
                    except ImportError:
                        from native_hook_runtime import execute as run_hook
                    return await run_hook(self,message,hook,directory/'hooks'/str(hook_sequence))
                row = await execute(case, file_loader=load_file, extended_details=bool(extended and requested),hook_executor=execute_hook)
                rows.append(row)
                await self.deliver(
                    dict(
                        type="test_suite_result",
                        suite_id=suite_id,
                        execution_id=execution_id,
                        case_id=case.id,
                        result=row["status"],
                        duration=f"{row['duration']:.3f}s",
                        error_message=row["error"],
                        log_output=row["log"],
                        native_detail=row["native_detail"],
                        executor_id=message.get("executor_id", "system"),
                    )
                )
            status = (
                "completed"
                if all(row["status"] == "passed" for row in rows)
                else "failed"
            )
        except asyncio.CancelledError:
            status, error = "cancelled", "原生HTTP执行已取消"
            logger.opt(exception=True).info("原生HTTP执行已取消：执行={}", execution_id)
        except asyncio.TimeoutError:
            error = "原生HTTP启动日志超时"
            logger.exception("原生HTTP启动日志超时：执行={}", execution_id)
        except Exception as exception:
            error = "原生HTTP执行失败：" + type(exception).__name__
            logger.exception("原生HTTP执行失败：执行={}", execution_id)
        finally:
            self.finalizing.add(execution_id)
            try:
                if status != "cancelled":
                    reported = {row["case_id"] for row in rows}
                    for case_id in message.get("case_ids", []):
                        if case_id not in reported:
                            await self.deliver(
                                dict(
                                    type="test_suite_result",
                                    suite_id=suite_id,
                                    execution_id=execution_id,
                                    case_id=case_id,
                                    result="error",
                                    duration="0.000s",
                                    error_message=error or "原生HTTP未产生对应结果",
                                    log_output=error,
                                    executor_id=message.get("executor_id", "system"),
                                )
                            )
                record = dict(
                    execution_id=execution_id, status=status, error=error, rows=rows
                )
                await self.deliver(
                    dict(
                        type="test_suite_completed",
                        suite_id=suite_id,
                        execution_id=execution_id,
                        status=status,
                        message=error or "原生HTTP执行已结束",
                        duration=f"{time.monotonic() - started:.3f}s",
                        total_case_count=len(message.get("case_ids", [])),
                        reported_case_count=len(rows),
                        outcome=status,
                    )
                )
                # 先持久化可靠完成消息，再写终态标记，避免标记成功却丢失完成事件。
                temporary = directory / "native-run.tmp"
                with open(
                    temporary,
                    "w",
                    encoding="utf-8",
                    opener=lambda path, flags: os.open(path, flags, 0o600),
                ) as output:
                    os.fchmod(output.fileno(), 0o600)
                    output.write(json.dumps(record, ensure_ascii=False))
                temporary.replace(directory / "native-run.json")
                logger.info(
                    "原生HTTP执行结束：执行={}，状态={}，实际结果数={}",
                    execution_id,
                    status,
                    len(rows),
                )
            except Exception:
                logger.exception("原生HTTP终态持久化或回传失败：执行={}", execution_id)
                raise
            finally:
                self.started.discard(execution_id)
                self.cancel_requested.discard(execution_id)
                self.finalizing.discard(execution_id)
                if self.runs.get(execution_id) is asyncio.current_task():
                    self.runs.pop(execution_id, None)
                    self.suites.pop(execution_id, None)
