"""复用httpx发请求；报告包含真实请求耗时、响应概要和断言结果。"""

import asyncio
from copy import deepcopy
import json
import time
import httpx
import logging

logger = logging.getLogger("XAT原生HTTP")
from .models import FrozenCase
from .legacy_assertions import equal, check
from .response_assertions import evaluate
from .parameters import arguments as request_arguments, request_url


async def execute(case: FrozenCase, *, transport=None):
    started = time.monotonic()
    rows = []
    async with httpx.AsyncClient(transport=transport, trust_env=False) as client:
        for index, request in enumerate(case.requests):
            attempts = []
            step_started = time.monotonic()
            for attempt in range(case.retryTimes + 1):
                if attempt:
                    logger.info(
                        "等待原生HTTP步骤重试：用例=%s，步骤=%s，重试=%s，间隔毫秒=%s",
                        case.id,
                        index + 1,
                        attempt,
                        case.retryInterval,
                    )
                    try:
                        await asyncio.sleep(case.retryInterval / 1000)
                    except asyncio.CancelledError:
                        logger.info(
                            "原生HTTP重试等待已取消：用例=%s，步骤=%s",
                            case.id,
                            index + 1,
                            exc_info=True,
                        )
                        raise
                before = time.monotonic()
                row = dict(
                    index=index,
                    name=request.name,
                    method=request.method,
                    result="error",
                    statusCode=None,
                    assertions=[],
                )
                try:
                    arguments = request_arguments(request)
                    if request.bodyType == "json":
                        arguments["json"] = deepcopy(request.body)
                    elif request.bodyType == "text":
                        if not isinstance(request.body, str):
                            raise ValueError("文本请求体须为字符串")
                        arguments["content"] = request.body
                    elif request.bodyType == "form" and request.formParams is None:
                        if not isinstance(request.body, dict) or any(
                            not isinstance(v, str) for v in request.body.values()
                        ):
                            raise ValueError("表单请求体须为字符串键值对象")
                        arguments["data"] = request.body
                    logger.info(
                        "原生HTTP请求开始：用例=%s，步骤=%s，方法=%s",
                        case.id,
                        index + 1,
                        request.method,
                    )
                    response = await asyncio.wait_for(
                        client.request(
                            request.method, request_url(request), **arguments
                        ),
                        timeout=(
                            request.timeoutMs / 1000
                            if request.connectTimeoutMs is None
                            and request.responseTimeoutMs is None
                            else None
                        ),
                    )
                    row["statusCode"] = response.status_code
                    elapsed_ms = (time.monotonic() - before) * 1000
                    row["assertions"] = [
                        check(assertion, response) for assertion in request.assertions
                    ]
                    row["assertions"].extend(
                        await asyncio.to_thread(
                            evaluate,
                            request.responseAssertions,
                            response,
                            elapsed_ms,
                        )
                    )
                    # 未指定有效断言时采用真实HTTP状态；显式断言沿已有预期错误状态语义。
                    passed = (
                        all(v["passed"] for v in row["assertions"])
                        if row["assertions"]
                        else 200 <= response.status_code < 400
                    )
                    row["result"] = "passed" if passed else "failed"
                    if not passed:
                        row["error"] = "响应未满足预期状态或断言"
                except asyncio.CancelledError:
                    logger.info(
                        "原生HTTP执行已取消：用例=%s，步骤=%s",
                        case.id,
                        index + 1,
                        exc_info=True,
                    )
                    raise
                except Exception as exception:
                    logger.exception(
                        "原生HTTP请求失败：用例=%s，步骤=%s", case.id, index + 1
                    )
                    row["error"] = "请求执行失败：" + type(exception).__name__
                row["duration"] = round(time.monotonic() - before, 6)
                logger.info(
                    "原生HTTP步骤结束：用例=%s，步骤=%s，结果=%s，HTTP状态=%s",
                    case.id,
                    index + 1,
                    row["result"],
                    row["statusCode"],
                )
                attempts.append(deepcopy(row))
                if row["result"] == "passed":
                    break
            if case.retryTimes:
                row["attempts"] = attempts
                row["duration"] = round(time.monotonic() - step_started, 6)
            rows.append(row)
            if row["result"] != "passed" and case.stopOnFailure:
                rows.extend(
                    dict(
                        index=i,
                        name=r.name,
                        method=r.method,
                        result="skipped",
                        duration=0,
                        statusCode=None,
                        assertions=[],
                        error="前序步骤失败，场景停止",
                    )
                    for i, r in enumerate(case.requests[index + 1 :], index + 1)
                )
                break
    result = (
        "error"
        if any(r["result"] == "error" for r in rows)
        else "failed" if any(r["result"] == "failed" for r in rows) else "passed"
    )
    return dict(
        case_id=case.id,
        status=result,
        duration=time.monotonic() - started,
        steps=rows,
        error=None if result == "passed" else "原生HTTP请求或断言未通过",
        log=json.dumps(dict(步骤=rows), ensure_ascii=False),
    )
