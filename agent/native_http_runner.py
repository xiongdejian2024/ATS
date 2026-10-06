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
except ImportError:
    from sat_runner import SATRunner
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
            logger.info("原生HTTP执行已结束，忽略重复派发：执行={}", message["execution_id"])
            return
        super().start(message)

    async def execute(self, message):
        suite_id, execution_id = message["suite_id"], message["execution_id"]
        started, rows, status, error = time.monotonic(), [], "failed", None
        directory = self.agent.work_dir / "suites" / suite_id / "executions" / execution_id
        directory.mkdir(parents=True, exist_ok=True)
        try:
            # 与现有SAT适配器同样从工作区加载自有XAT，httpx/Pydantic均为XAT已有依赖。
            xat_path = str(Path(__file__).resolve().parents[1] / "xat")
            if xat_path not in sys.path:
                sys.path.insert(0, xat_path)
            from framework.native_http.models import FrozenCase
            from framework.native_http.engine import execute

            cases = [FrozenCase.model_validate(value) for value in message.get("native_cases", [])]
            if (
                not cases
                or [case.id for case in cases] != message["case_ids"]
                or len({c.id for c in cases}) != len(cases)
            ):
                raise ValueError("冻结原生用例与本次选择范围不一致")
            await self.log(message, f"开始原生HTTP执行，实际用例数：{len(cases)}")
            for case in cases:
                row = await execute(case)
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
            status = "completed" if all(row["status"] == "passed" for row in rows) else "failed"
        except asyncio.CancelledError:
            status, error = "cancelled", "原生HTTP执行已取消"
            logger.opt(exception=True).info("原生HTTP执行已取消：执行={}", execution_id)
        except Exception as exception:
            error = "原生HTTP执行失败：" + type(exception).__name__
            logger.exception("原生HTTP执行失败：执行={}", execution_id)
        finally:
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
                record = dict(execution_id=execution_id, status=status, error=error, rows=rows)
                self.runs.pop(execution_id, None)
                self.suites.pop(execution_id, None)
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
                if self.runs.get(execution_id) is asyncio.current_task():
                    self.runs.pop(execution_id, None)
                    self.suites.pop(execution_id, None)
