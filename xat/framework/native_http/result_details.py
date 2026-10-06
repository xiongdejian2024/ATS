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


class Attempt(Model):
    attempt: StrictInt = Field(ge=1, le=11)
    result: Literal["passed", "failed", "error", "skipped"]
    duration: float = Field(ge=0, allow_inf_nan=False)
    request: Request | None = None
    response: Response | None = None
    assertions: list[Assertion] = Field(default_factory=list, max_length=500)
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
    version: Literal[1] = 1
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


def bounded_detail(steps):
    """实际捕获量超过协议上限时明确标记，绝不伪装成完整内容。"""
    selected, size = [], 256
    for step in steps:
        step = Step.model_validate(step).model_dump()
        needed = len(json.dumps(step, ensure_ascii=False).encode("utf-8")) + 2
        if size + needed > DETAIL_LIMIT:
            break
        selected.append(step)
        size += needed
    return NativeDetail(
        totalSteps=len(steps), omittedSteps=len(steps) - len(selected), steps=selected
    ).model_dump()
