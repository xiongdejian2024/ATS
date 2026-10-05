"""声明式请求/断言模型；拒绝未知配置，不执行脚本或shell。"""

from typing import Literal
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
    model_config = ConfigDict(extra="forbid", strict=True)


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
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"] = "GET"
    headers: dict[str, str] = Field(default_factory=dict)
    query: dict[str, str] = Field(default_factory=dict)
    body: JsonValue = None
    bodyType: Literal["none", "json", "text", "form"] = "none"
    timeoutMs: StrictInt = Field(10000, ge=1, le=300000)
    followRedirects: StrictBool = False
    assertions: list[Assertion] = Field(default_factory=list, max_length=100)

    @model_validator(mode="after")
    def valid_body(self):
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
