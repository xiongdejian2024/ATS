"""MS 后置提取协议；当前临时参数的生存期是一次用例/场景执行。"""

from typing import Literal
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictInt,
    model_validator,
)


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, hide_input_in_errors=True)


class Extractor(Model):
    id: str = Field(min_length=1, max_length=36)
    enable: StrictBool = True
    variableName: str = Field(min_length=1, max_length=100)
    variableType: Literal["TEMPORARY"] = "TEMPORARY"
    description: str = Field(default="", max_length=1000)
    extractType: Literal["JSON_PATH", "X_PATH", "REGEX"] = "JSON_PATH"
    expression: str = Field(min_length=1, max_length=200)
    extractScope: Literal[
        "BODY",
        "UNESCAPED_BODY",
        "BODY_AS_DOCUMENT",
        "URL",
        "REQUEST_HEADERS",
        "RESPONSE_HEADERS",
        "RESPONSE_CODE",
        "RESPONSE_MESSAGE",
    ] = "BODY"
    expressionMatchingRule: Literal["EXPRESSION", "GROUP"] = "EXPRESSION"
    resultMatchingRule: Literal["RANDOM", "SPECIFIC", "ALL"] = "RANDOM"
    resultMatchingRuleNum: StrictInt = Field(default=1, ge=1, le=2147483647)
    responseFormat: Literal["XML", "HTML"] = "XML"

    @model_validator(mode="after")
    def valid_names(self):
        if not self.variableName.strip() or any(
            c in self.variableName for c in "${}\r\n\x00"
        ):
            raise ValueError("变量名不能为空或含模板分隔符及控制字符")
        if not self.expression.strip():
            raise ValueError("提取表达式不能为空")
        return self


class ExtractProcessor(Model):
    id: str = Field(min_length=1, max_length=36)
    name: str = Field(default="参数提取", min_length=1, max_length=255)
    processorType: Literal["EXTRACT"] = "EXTRACT"
    enable: StrictBool = True
    extractors: list[Extractor] = Field(default_factory=list, max_length=200)

    @model_validator(mode="after")
    def unique_rows(self):
        if len({r.id for r in self.extractors}) != len(self.extractors):
            raise ValueError("提取行标识不能重复")
        active = [r.variableName for r in self.extractors if r.enable]
        if len(active) != len(set(active)):
            raise ValueError("同一提取器中的启用变量名不能重复")
        return self


class PostProcessorConfig(Model):
    processors: list[ExtractProcessor] = Field(default_factory=list, max_length=100)

    @model_validator(mode="after")
    def bounded_rows(self):
        if len({p.id for p in self.processors}) != len(self.processors):
            raise ValueError("后置条件标识不能重复")
        if sum(len(p.extractors) for p in self.processors) > 200:
            raise ValueError("每个请求最多200个提取参数")
        return self
