"""HTTP实际交换详情，独立于日志；保存字节、重复响应头及截断标志。"""

import base64
import json
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictInt,
    model_validator,
)
from typing import Literal

BODY_LIMIT = 256 * 1024
DETAIL_LIMIT = 8 * 1024 * 1024


def text(value, limit=4096):
    raw = str(value).encode("utf-8")
    return raw[:limit].decode("utf-8", errors="ignore"), len(raw) > limit


def body(content, content_type, charset="utf-8"):
    captured = content[:BODY_LIMIT]
    return dict(
        base64=base64.b64encode(captured).decode("ascii"),
        byteLength=len(content),
        capturedBytes=len(captured),
        truncated=len(content) > len(captured),
        contentType=text(content_type, 255)[0],
        charset=text(charset or "utf-8", 80)[0],
    )


def headers(value):
    return [
        [text(name.decode("latin-1"), 255)[0], text(item.decode("latin-1"), 20000)[0]]
        for name, item in value.raw[:200]
    ]


def headers_truncated(value):
    return len(value.raw) > 200 or any(
        len(k.decode("latin-1").encode("utf-8")) > 255
        or len(v.decode("latin-1").encode("utf-8")) > 20000
        for k, v in value.raw
    )


def exchange(response, elapsed_ms):
    request = response.request
    return dict(
        request=request_detail(request),
        response=dict(
            statusCode=response.status_code,
            reason=text(response.reason_phrase, 255)[0],
            httpVersion=text(response.http_version, 80)[0],
            headers=headers(response.headers),
            headersTruncated=headers_truncated(response.headers),
            body=body(
                response.content,
                response.headers.get("content-type", ""),
                response.encoding,
            ),
            responseTimeMs=round(elapsed_ms, 6) if elapsed_ms is not None else None,
        ),
    )


def request_detail(request):
    return dict(
        method=request.method,
        url=text(str(request.url), 20000)[0],
        headers=headers(request.headers),
        headersTruncated=headers_truncated(request.headers),
        body=body(request.content, request.headers.get("content-type", "")),
    )


def assertion_detail(row, *, actual, expected, name, expression="", present=True):
    actual_value, actual_cut = text(actual)
    expected_value, expected_cut = text(expected)
    return dict(
        name=text(name, 255)[0],
        assertionType=row.get("assertionType", row["source"]),
        condition=row["operator"],
        expression=text(expression, 255)[0],
        actualValue=actual_value,
        expectedValue=expected_value,
        actualTruncated=actual_cut,
        expectedTruncated=expected_cut,
        actualPresent=present,
        passed=row["passed"],
        message=row["description"],
        groupId=row.get("groupId"),
        rowIndex=row.get("rowIndex"),
    )


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, hide_input_in_errors=True)


class Body(Model):
    base64: str = Field(max_length=(BODY_LIMIT + 2) // 3 * 4)
    byteLength: StrictInt = Field(ge=0)
    capturedBytes: StrictInt = Field(ge=0, le=BODY_LIMIT)
    truncated: StrictBool
    contentType: str = Field(max_length=255)
    charset: str = Field(max_length=80)

    @model_validator(mode="after")
    def consistent_bytes(self):
        data = base64.b64decode(self.base64, validate=True)
        if (
            len(data) != self.capturedBytes
            or self.byteLength < len(data)
            or self.truncated != (self.byteLength > len(data))
        ):
            raise ValueError("捕获正文大小或截断标志不一致")
        return self


class Request(Model):
    method: str = Field(max_length=20)
    url: str = Field(max_length=20000)
    headers: list[tuple[str, str] | list[str]] = Field(max_length=200)
    headersTruncated: StrictBool = False
    body: Body

    @model_validator(mode="after")
    def valid_headers(self):
        if any(
            len(h) != 2 or len(h[0]) > 255 or len(h[1]) > 20000 for h in self.headers
        ):
            raise ValueError("实际请求头结构无效")
        return self


class Response(Model):
    statusCode: StrictInt = Field(ge=100, le=999)
    reason: str = Field(max_length=255)
    httpVersion: str = Field(max_length=80)
    headers: list[tuple[str, str] | list[str]] = Field(max_length=200)
    headersTruncated: StrictBool = False
    body: Body
    responseTimeMs: float | None = Field(default=None, ge=0, allow_inf_nan=False)

    @model_validator(mode="after")
    def valid_headers(self):
        if any(
            len(h) != 2 or len(h[0]) > 255 or len(h[1]) > 20000 for h in self.headers
        ):
            raise ValueError("实际响应头结构无效")
        return self


class Redirect(Model):
    request: Request
    response: Response


class Assertion(Model):
    name: str = Field(max_length=255)
    assertionType: str = Field(max_length=40)
    condition: str = Field(max_length=40)
    expression: str = Field(max_length=255)
    actualValue: str = Field(max_length=4096)
    expectedValue: str = Field(max_length=4096)
    actualTruncated: StrictBool
    expectedTruncated: StrictBool
    actualPresent: StrictBool
    passed: StrictBool
    message: str = Field(max_length=1000)
    groupId: str | None = Field(default=None, max_length=36)
    rowIndex: StrictInt | None = Field(default=None, ge=0, le=1000)


class Extraction(Model):
    name: str = Field(max_length=100)
    type: Literal["TEMPORARY"]
    expression: str = Field(max_length=200)
    processorId: str = Field(max_length=36)
    extractorId: str = Field(max_length=36)
    matched: StrictBool
    matchCount: StrictInt = Field(ge=0, le=1000)
    value: str = Field(max_length=4096)
    truncated: StrictBool
    message: str = Field(max_length=1000)


class Timings(Model):
    preProcessorsMs: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    postProcessorsMs: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    preparationMs: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    httpMs: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    extractionMs: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    assertionMs: float | None = Field(default=None, ge=0, allow_inf_nan=False)


class ProcessorBinding(Model):
    name: str = Field(max_length=255)
    value: str = Field(max_length=4096)
    truncated: StrictBool = False


class ProcessorResult(Model):
    id: str = Field(max_length=36)
    name: str = Field(max_length=255)
    type: Literal['sql','script']
    phase: Literal['pre','post','global_pre','global_post']
    result: Literal['passed','error','skipped']
    durationMs: float = Field(ge=0,allow_inf_nan=False)
    error: str | None = Field(default=None,max_length=1000)
    rowCount: StrictInt | None = Field(default=None,ge=0,le=1000)
    bindings: list[ProcessorBinding] = Field(default_factory=list,max_length=100)


class Attempt(Model):
    processorResults: list[ProcessorResult] | None = Field(default=None,max_length=20)
    source: Literal['http', 'mock'] | None = None
    timings: Timings | None = None
    attempt: StrictInt = Field(ge=1, le=11)
    result: Literal["passed", "failed", "error", "skipped"]
    duration: float = Field(ge=0, allow_inf_nan=False)
    request: Request | None = None
    response: Response | None = None
    assertions: list[Assertion] = Field(default_factory=list, max_length=500)
    extractResults: list[Extraction] = Field(default_factory=list, max_length=200)
    error: str | None = Field(default=None, max_length=1000)
    redirects: list[Redirect] = Field(default_factory=list, max_length=20)
    console: list[str] = Field(default_factory=list, max_length=100)


class Step(Model):
    index: StrictInt = Field(ge=0, le=999)
    name: str = Field(max_length=255)
    method: str = Field(max_length=20)
    result: Literal["passed", "failed", "error", "skipped"]
    duration: float = Field(ge=0, allow_inf_nan=False)
    attempts: list[Attempt] = Field(max_length=11)
    error: str | None = Field(default=None, max_length=1000)


class NativeDetail(Model):
    globalProcessorResults: list[ProcessorResult] = Field(default_factory=list,max_length=20)
    omittedGlobalProcessors: StrictInt = Field(default=0,ge=0,le=20)
    version: Literal[1, 2] = 1
    totalSteps: StrictInt = Field(ge=0, le=1000)
    omittedSteps: StrictInt = Field(ge=0, le=1000)
    steps: list[Step] = Field(max_length=1000)

    @model_validator(mode="after")
    def consistent_steps(self):
        if self.totalSteps != len(self.steps) + self.omittedSteps or [
            s.index for s in self.steps
        ] != list(range(len(self.steps))):
            raise ValueError("捕获步骤数量或顺序不一致")
        for step in self.steps:
            if [a.attempt for a in step.attempts] != list(
                range(1, len(step.attempts) + 1)
            ):
                raise ValueError("实际尝试顺序不一致")
        return self


def bounded_detail(steps, *, extended=False, global_processors=None):
    """实际捕获量超过协议上限时明确标记，绝不伪装成完整内容。"""
    selected, size = [], 256
    global_selected=[]
    for row in global_processors or []:
        row=ProcessorResult.model_validate(row).model_dump()
        needed=len(json.dumps(row,ensure_ascii=True).encode())+2
        if size+needed>DETAIL_LIMIT: break
        global_selected.append(row);size+=needed
    for step in steps:
        step = Step.model_validate(step).model_dump()
        for attempt in step['attempts']:
            if not extended or attempt['processorResults'] is None:
                attempt.pop('processorResults')
            if not extended or attempt['source'] is None:
                attempt.pop('source')
            if not extended or attempt['timings'] is None:
                attempt.pop('timings')
        # 可靠回传沿现有JSON协议转义非ASCII，按实际线上编码计量。
        needed = len(json.dumps(step, ensure_ascii=True).encode("utf-8")) + 2
        if size + needed > DETAIL_LIMIT:
            break
        selected.append(step)
        size += needed
    payload = NativeDetail(
        version=2 if extended else 1,
        totalSteps=len(steps), omittedSteps=len(steps) - len(selected), steps=selected
        ,globalProcessorResults=global_selected,omittedGlobalProcessors=len(global_processors or [])-len(global_selected)
    ).model_dump()
    for step in payload['steps']:
        for attempt in step['attempts']:
            for field in ('source', 'timings', 'processorResults'):
                if not extended or attempt[field] is None:
                    attempt.pop(field)
    if not extended:
        payload.pop('globalProcessorResults');payload.pop('omittedGlobalProcessors')
    return payload
