"""声明式请求/断言模型；拒绝未知配置，不执行脚本或shell。"""

from typing import Literal
from .response_assertion_models import ResponseAssertion
from urllib.parse import urlsplit
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictInt,
    JsonValue,
    field_validator,
    model_validator,
)


class NativeModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, hide_input_in_errors=True)


class RequestParam(NativeModel):
    key: str = Field(min_length=1, max_length=255)
    value: str = Field(default="", max_length=20000)
    enable: StrictBool = True
    paramType: Literal["string", "integer", "number", "boolean", "array"] = "string"
    required: StrictBool = False
    encode: StrictBool = True
    description: str = Field(default="", max_length=1000)
    lengthRange: list[StrictInt] = Field(default_factory=list, max_length=2)

    @field_validator("lengthRange")
    @classmethod
    def valid_range(cls, value):
        if value and (len(value) != 2 or value[0] < 0 or value[1] < value[0]):
            raise ValueError("参数长度范围须为非负、递增的两个整数")
        return value


class AuthCredentials(NativeModel):
    userName: str = Field(default="", max_length=255)
    password: str = Field(default="", max_length=20000, repr=False)


class RequestAuth(NativeModel):
    authType: Literal["NONE", "BASIC", "DIGEST"] = "NONE"
    basicAuth: AuthCredentials = Field(default_factory=AuthCredentials)
    digestAuth: AuthCredentials = Field(default_factory=AuthCredentials)


class Assertion(NativeModel):
    source: Literal["status", "json", "text", "header"] = "status"
    path: list[str | StrictInt] = Field(default_factory=list, max_length=50)
    name: str | None = Field(None, max_length=100)
    operator: Literal["equals", "not_equals", "contains", "exists", "not_exists"] = (
        "equals"
    )
    expected: JsonValue = None

    @model_validator(mode="after")
    def valid_target(self):
        if self.source == "header" and not self.name:
            raise ValueError("响应头断言需要名称")
        if self.source != "header" and self.name is not None:
            raise ValueError("只有响应头断言可以指定名称")
        if self.source != "json" and self.path:
            raise ValueError("只有JSON断言可以指定路径")
        if any(isinstance(segment, int) and segment < 0 for segment in self.path):
            raise ValueError("JSON数组下标不能为负数")
        return self


class RequestSpec(NativeModel):
    method: Literal[
        "GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "CONNECT"
    ] = "GET"
    headers: dict[str, str] = Field(default_factory=dict)
    query: dict[str, str] = Field(default_factory=dict)
    body: JsonValue = None
    bodyType: Literal["none", "json", "text", "form"] = "none"
    timeoutMs: StrictInt = Field(10000, ge=1, le=300000)
    followRedirects: StrictBool = False
    assertions: list[Assertion] = Field(default_factory=list, max_length=100)
    responseAssertions: list[ResponseAssertion] = Field(
        default_factory=list, max_length=4
    )
    headerParams: list[RequestParam] | None = Field(None, max_length=200)
    queryParams: list[RequestParam] | None = Field(None, max_length=200)
    restParams: list[RequestParam] = Field(default_factory=list, max_length=200)
    formParams: list[RequestParam] | None = Field(None, max_length=200)
    authConfig: RequestAuth | None = None
    connectTimeoutMs: StrictInt | None = Field(None, ge=0, le=600000)
    responseTimeoutMs: StrictInt | None = Field(None, ge=0, le=600000)

    @model_validator(mode="after")
    def valid_body(self):
        groups = self.responseAssertions
        if len({g.id for g in groups}) != len(groups) or len(
            {g.assertionType for g in groups}
        ) != len(groups):
            raise ValueError("响应断言分类及ID不能重复")
        for rows, legacy, is_header in (
            (self.headerParams, self.headers, True),
            (self.queryParams, self.query, False),
            (self.formParams, self.body if self.bodyType == "form" else {}, False),
            (self.restParams, {}, False),
        ):
            if rows is None:
                continue
            if legacy:
                raise ValueError("参数表格不能与旧键值配置混用")
            keys = [
                row.key.casefold() if is_header else row.key
                for row in rows
                if row.enable
            ]
            if len(keys) != len(set(keys)):
                raise ValueError("启用的参数名称不能重复")
        if self.formParams is not None and self.bodyType != "form":
            raise ValueError("表单参数只用于表单请求体")
        if self.bodyType == "none" and self.body is not None:
            raise ValueError("无请求体时不能保存正文")
        if self.bodyType == "text" and not isinstance(self.body, str):
            raise ValueError("文本请求体须为字符串")
        if self.bodyType == "form" and (
            not isinstance(self.body, dict)
            or any(not isinstance(v, str) for v in self.body.values())
        ):
            raise ValueError("表单请求体须为字符串键值对象")
        return self

    @field_validator("headers", "query")
    @classmethod
    def bounded_pairs(cls, value):
        if len(value) > 200 or any(
            not key or len(key) > 255 or len(item) > 20000
            for key, item in value.items()
        ):
            raise ValueError("请求键值最多200项，名称及值超过长度限制")
        return value


class FrozenRequest(RequestSpec):
    url: str = Field(min_length=1, max_length=2000)
    name: str = Field(min_length=1, max_length=255)

    @field_validator("url")
    @classmethod
    def http_url(cls, value):
        parsed = urlsplit(value)
        if (
            parsed.scheme not in {"http", "https"}
            or not parsed.hostname
            or parsed.username
            or parsed.password
            or parsed.fragment
        ):
            raise ValueError("请求地址须为无用户信息及片段的HTTP/HTTPS地址")
        # 解析端口同样校验范围，不接受结构错误的地址。
        _ = parsed.port
        return value


class ScenarioStep(NativeModel):
    apiCaseId: str = Field(min_length=1, max_length=36)
    enabled: StrictBool = True


class ScenarioSpec(NativeModel):
    steps: list[ScenarioStep] = Field(min_length=1, max_length=1000)
    stopOnFailure: StrictBool = True


class FrozenCase(NativeModel):
    id: str = Field(min_length=1, max_length=36)
    category: Literal["api", "scenario"]
    requests: list[FrozenRequest] = Field(min_length=1, max_length=1000)
    stopOnFailure: StrictBool = True
    retryTimes: StrictInt = Field(0, ge=0, le=10)
    retryInterval: StrictInt = Field(0, ge=0, le=2147483647)
