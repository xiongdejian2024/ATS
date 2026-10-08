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
from .extractions import evaluate as extract, resolve_request, render_value
from .result_details import exchange, bounded_detail, request_detail
from .parameters import arguments as request_arguments, request_url
from .request_bodies import load_files, arguments as body_arguments
from .variable_models import values
from .processor_runtime import evaluate as process


class ProcessorFailure(Exception):
    pass


async def execute(case: FrozenCase, *, transport=None, file_loader=None, extended_details=False, hook_executor=None):
    started = time.monotonic()
    rows = []
    details = []
    temporary = {}
    global_variables = {**values(case.requests[0].environmentVariables), **values(case.initialVariables)}
    if case.category == 'api':
        global_variables.update(values(case.requests[0].initialVariables))
    global_rows, global_success = await process('global_pre',case.globalPreProcessors,global_variables,temporary,hook_executor=hook_executor)

    async def capture_request(value):
        await value.aread()
        actual["request"] = request_detail(value)

    async def send_request(client, request, arguments):
        async def mock_handler(value):
            mock = request.mockResponse
            await asyncio.sleep(mock.delayMs / 1000)
            return httpx.Response(mock.statusCode, headers=mock.headers, content=mock.body.encode('utf-8'), request=value)
        if request.mockResponse and request.mockResponse.enable:
            async with httpx.AsyncClient(transport=httpx.MockTransport(mock_handler), trust_env=False, event_hooks={"request": [capture_request]}) as mocked:
                return await mocked.request(request.method, request_url(request), **arguments)
        return await client.request(request.method, request_url(request), **arguments)

    async with httpx.AsyncClient(
        transport=transport, trust_env=False, event_hooks={"request": [capture_request]}
    ) as client:
        for index, template in enumerate(case.requests):
            if not global_success:
                row = dict(index=index,name=template.name,method=template.method,result='skipped',duration=0,statusCode=None,assertions=[],error='全局前置处理器失败')
                rows.append(row)
                details.append(dict(index=index,name=template.name,method=template.method,result='skipped',duration=0,attempts=[],error=row['error']))
                continue
            request = template
            attempts = []
            detail_attempts = []
            step_started = time.monotonic()
            for attempt in range(case.retryTimes + 1):
                variables = {
                    **values(template.environmentVariables),
                    **values(case.initialVariables),
                    **values(template.initialVariables),
                    **temporary,
                }
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
                actual = dict(attempt=attempt + 1, assertions=[], console=[])
                timings = {}
                phase, phase_started = None, None
                retry_allowed = True
                if extended_details:
                    actual['source'] = 'mock' if template.mockResponse and template.mockResponse.enable else 'http'
                    actual['timings'] = timings
                    actual['processorResults'] = []
                try:
                    if template.preProcessors:
                        phase, phase_started = 'preProcessorsMs', time.monotonic()
                        processor_rows, succeeded = await process('pre', template.preProcessors, variables, temporary, hook_executor=hook_executor)
                        if extended_details: actual['processorResults'].extend(processor_rows)
                        timings[phase] = (time.monotonic() - phase_started) * 1000
                        if not succeeded:
                            retry_allowed = False
                            raise ProcessorFailure('前置处理器失败')
                    preparation_started = time.monotonic()
                    phase, phase_started = 'preparationMs', preparation_started
                    request = resolve_request(template, variables)
                    arguments = request_arguments(request)
                    arguments.update(
                        body_arguments(request, await load_files(request, file_loader))
                    )
                    if request.bodyType in {"xml", "binary"} and not any(
                        k.casefold() == "content-type" for k in arguments["headers"]
                    ):
                        arguments["headers"] = dict(
                            arguments["headers"],
                            **{
                                "Content-Type": (
                                    "application/xml"
                                    if request.bodyType == "xml"
                                    else "application/octet-stream"
                                )
                            },
                        )
                    if request.bodyType == "json":
                        arguments["json"] = deepcopy(request.body)
                    elif request.bodyType in {"text", "xml"}:
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
                    actual["console"].append(
                        f"原生HTTP请求开始：步骤={index + 1}，方法={request.method}，尝试={attempt + 1}"
                    )
                    timings['preparationMs'] = (time.monotonic() - preparation_started) * 1000
                    network_started = time.monotonic()
                    phase, phase_started = 'httpMs', network_started
                    response = await asyncio.wait_for(
                        send_request(client, request, arguments),
                        timeout=(
                            ((request.timeoutMs if request.responseTimeoutMs is None else request.responseTimeoutMs) / 1000 or None)
                            if request.mockResponse and request.mockResponse.enable
                            else request.timeoutMs / 1000
                            if request.connectTimeoutMs is None
                            and request.responseTimeoutMs is None
                            else None
                        ),
                    )
                    row["statusCode"] = response.status_code
                    elapsed_ms = (time.monotonic() - network_started) * 1000
                    timings['httpMs'] = elapsed_ms
                    actual.update(exchange(response, elapsed_ms))
                    extraction_started = time.monotonic()
                    phase, phase_started = 'extractionMs', extraction_started
                    actual["extractResults"] = await asyncio.to_thread(
                        extract, request.postProcessorConfig, response, variables, temporary
                    )
                    timings['extractionMs'] = (time.monotonic() - extraction_started) * 1000
                    if template.postProcessors:
                        phase, phase_started = 'postProcessorsMs', time.monotonic()
                        processor_rows, succeeded = await process('post', template.postProcessors, variables, temporary, hook_executor=hook_executor)
                        if extended_details: actual['processorResults'].extend(processor_rows)
                        timings[phase] = (time.monotonic() - phase_started) * 1000
                        if not succeeded:
                            retry_allowed = False
                            raise ProcessorFailure('后置处理器失败，HTTP已经完成，不自动重发')
                    logger.info(
                        "后置参数提取完成：用例=%s，步骤=%s，执行项数=%s",
                        case.id,
                        index + 1,
                        len(actual["extractResults"]),
                    )
                    actual["console"].append(
                        f"后置参数提取完成：执行{len(actual['extractResults'])}项"
                    )
                    assertion_started = time.monotonic()
                    phase, phase_started = 'assertionMs', assertion_started
                    request.assertions = [
                        type(a).model_validate(render_value(a.model_dump(), variables))
                        for a in template.assertions
                    ]
                    request.responseAssertions = [
                        type(a).model_validate(render_value(a.model_dump(), variables))
                        for a in template.responseAssertions
                    ]
                    actual["redirects"] = [exchange(r, None) for r in response.history]
                    row["assertions"] = [
                        check(assertion, response, actual["assertions"])
                        for assertion in request.assertions
                    ]
                    row["assertions"].extend(
                        await asyncio.to_thread(
                            evaluate,
                            request.responseAssertions,
                            response,
                            elapsed_ms,
                            actual["assertions"],
                            variables,
                        )
                    )
                    # 未指定有效断言时采用真实HTTP状态；显式断言沿已有预期错误状态语义。
                    passed = (
                        all(v["passed"] for v in row["assertions"])
                        if row["assertions"]
                        else 200 <= response.status_code < 400
                    )
                    row["result"] = "passed" if passed else "failed"
                    timings['assertionMs'] = (time.monotonic() - assertion_started) * 1000
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
                if phase is not None and phase not in timings:
                    timings[phase] = (time.monotonic() - phase_started) * 1000
                row["duration"] = round(time.monotonic() - before, 6)
                actual.update(
                    result=row["result"],
                    duration=row["duration"],
                    error=row.get("error"),
                )
                actual["console"].append(
                    f"原生HTTP步骤结束：结果={row['result']}，HTTP状态={row['statusCode']}，耗时={row['duration']}s"
                )
                if row.get("error"):
                    actual["console"].append(row["error"])
                detail_attempts.append(actual)
                logger.info(
                    "原生HTTP步骤结束：用例=%s，步骤=%s，结果=%s，HTTP状态=%s",
                    case.id,
                    index + 1,
                    row["result"],
                    row["statusCode"],
                )
                attempts.append(deepcopy(row))
                if row["result"] == "passed" or not retry_allowed:
                    break
            if case.retryTimes:
                row["attempts"] = attempts
                row["duration"] = round(time.monotonic() - step_started, 6)
            rows.append(row)
            details.append(
                dict(
                    index=index,
                    name=request.name,
                    method=request.method,
                    result=row["result"],
                    duration=row["duration"],
                    attempts=detail_attempts,
                    error=row.get("error"),
                )
            )
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
                details.extend(
                    dict(
                        index=i,
                        name=r.name,
                        method=r.method,
                        result="skipped",
                        duration=0,
                        attempts=[],
                        error="前序步骤失败，场景停止",
                    )
                    for i, r in enumerate(case.requests[index + 1 :], index + 1)
                )
                break
    global_after, after_success = await process('global_post',case.globalPostProcessors,{**global_variables,**temporary},temporary,hook_executor=hook_executor,skip_reason=None if global_success else '全局前置处理器失败')
    global_rows.extend(global_after)
    result = (
        "error"
        if not global_success or not after_success or any(r["result"] == "error" for r in rows)
        else "failed" if any(r["result"] == "failed" for r in rows) else "passed"
    )
    return dict(
        case_id=case.id,
        status=result,
        duration=time.monotonic() - started,
        steps=rows,
        error=None if result == "passed" else "原生HTTP请求或断言未通过",
        log=json.dumps(dict(步骤=rows), ensure_ascii=False),
        native_detail=bounded_detail(details, extended=extended_details, global_processors=global_rows),
    )
