"""响应与变量断言独立契约；保留各正文方式草稿及启停，不接受脚本。"""

from typing import Literal, Annotated
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictInt,
    field_validator,
)

Condition = Literal[
    "UNCHECK",
    "EQUALS",
    "NOT_EQUALS",
    "GT",
    "GT_OR_EQUALS",
    "LT",
    "LT_OR_EQUALS",
    "CONTAINS",
    "NOT_CONTAINS",
    "START_WITH",
    "END_WITH",
    "EMPTY",
    "NOT_EMPTY",
    "REGEX",
    "LENGTH_GT",
    "LENGTH_GT_OR_EQUALS",
    "LENGTH_LT",
    "LENGTH_LT_OR_EQUALS",
    "LENGTH_EQUALS",
]
MatchCondition = Literal["CONTAINS", "NOT_CONTAINS", "EQUALS", "NOT_EQUALS"]


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, hide_input_in_errors=True)


class Group(Model):
    id: str = Field(min_length=1, max_length=36)
    name: str = Field(min_length=1, max_length=255)
    enable: StrictBool = True


class CodeAssertion(Group):
    assertionType: Literal["RESPONSE_CODE"]
    condition: MatchCondition | Literal["UNCHECK"] = "EQUALS"
    expectedValue: str = Field(default="200", max_length=20000)


class HeaderRule(Model):
    header: str = Field(min_length=1, max_length=255)
    condition: MatchCondition = "EQUALS"
    expectedValue: str = Field(default="", max_length=20000)
    enable: StrictBool = True


class HeaderAssertion(Group):
    assertionType: Literal["RESPONSE_HEADER"]
    assertions: list[HeaderRule] = Field(default_factory=list, max_length=100)


class JsonPathRule(Model):
    expression: str = Field(min_length=1, max_length=255)
    condition: Condition = "EQUALS"
    expectedValue: str = Field(default="", max_length=20000)
    enable: StrictBool = True


class ExpressionRule(Model):
    expression: str = Field(min_length=1, max_length=255)
    enable: StrictBool = True


class JsonPathSection(Model):
    assertions: list[JsonPathRule] = Field(default_factory=list, max_length=100)


class XPathSection(Model):
    responseFormat: Literal["XML", "HTML"] = "XML"
    assertions: list[ExpressionRule] = Field(default_factory=list, max_length=100)


class RegexSection(Model):
    assertions: list[ExpressionRule] = Field(default_factory=list, max_length=100)


class BodyAssertion(Group):
    assertionType: Literal["RESPONSE_BODY"]
    assertionBodyType: Literal["JSON_PATH", "XPATH", "REGEX"] = "JSON_PATH"
    jsonPathAssertion: JsonPathSection = Field(default_factory=JsonPathSection)
    xpathAssertion: XPathSection = Field(default_factory=XPathSection)
    regexAssertion: RegexSection = Field(default_factory=RegexSection)


class TimeAssertion(Group):
    assertionType: Literal["RESPONSE_TIME"]
    expectedValue: StrictInt = Field(default=200, ge=0, le=2147483647)


class VariableRule(Model):
    variableName: str = Field(min_length=1, max_length=255)
    condition: Condition = "EQUALS"
    expectedValue: str = Field(default="", max_length=20000)
    enable: StrictBool = True

    @field_validator("variableName")
    @classmethod
    def valid_name(cls, value):
        if not value.strip() or any(c in value for c in "\r\n\0"):
            raise ValueError("变量断言名称不能为空或包含控制字符")
        return value


class VariableAssertion(Group):
    assertionType: Literal["VARIABLE"]
    variableAssertionItems: list[VariableRule] = Field(default_factory=list, max_length=100)


ResponseAssertion = Annotated[
    CodeAssertion | HeaderAssertion | BodyAssertion | TimeAssertion | VariableAssertion,
    Field(discriminator="assertionType"),
]
