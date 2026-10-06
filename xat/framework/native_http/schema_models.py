"""MS 请求 Schema 编辑元数据；执行仍使用独立 JSON 正文。"""

from typing import Literal
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictInt,
    StrictStr,
    model_validator,
)


class JsonSchemaItem(BaseModel):
    model_config = ConfigDict(extra="forbid", hide_input_in_errors=True)
    type: Literal["object", "array", "string", "number", "integer", "boolean", "null"]
    enable: StrictBool = True
    description: StrictStr = Field("", max_length=20000)
    example: StrictStr = Field("", max_length=20000)
    defaultValue: StrictStr | StrictInt | float | StrictBool = ""
    properties: dict[str, "JsonSchemaItem"] | None = None
    items: list["JsonSchemaItem"] | None = Field(None, max_length=200)
    required: list[StrictStr] = Field(default_factory=list, max_length=200)
    enumValues: list[StrictStr] | None = Field(None, max_length=200)
    pattern: StrictStr | None = Field(None, max_length=512)
    format: (
        Literal["date", "date-time", "email", "hostname", "ipv4", "ipv6", "url"] | None
    ) = None
    minLength: StrictInt | None = Field(None, ge=0, le=20000)
    maxLength: StrictInt | None = Field(None, ge=0, le=20000)
    minimum: float | None = Field(None, allow_inf_nan=False)
    maximum: float | None = Field(None, allow_inf_nan=False)
    minItems: StrictInt | None = Field(None, ge=0, le=200)
    maxItems: StrictInt | None = Field(None, ge=0, le=200)

    @model_validator(mode="after")
    def valid_structure(self):
        if self.type == "object":
            if self.items is not None:
                raise ValueError("对象不能包含数组项")
            names = self.properties or {}
            if len(names) > 200 or any(not k.strip() or len(k) > 255 for k in names):
                raise ValueError("Schema 属性名称不能为空或超过255字符，每层最多200项")
            if (
                len(set(self.required)) != len(self.required)
                or not set(self.required) <= names.keys()
            ):
                raise ValueError("必填名称须对应唯一的对象属性")
        elif self.type == "array":
            if self.properties is not None or self.required:
                raise ValueError("数组不能包含对象属性或必填名称")
        elif self.properties is not None or self.items is not None or self.required:
            raise ValueError("基础类型不能包含子节点")
        for lo, hi in [
            (self.minLength, self.maxLength),
            (self.minimum, self.maximum),
            (self.minItems, self.maxItems),
        ]:
            if lo is not None and hi is not None and lo > hi:
                raise ValueError("Schema 最小值不能大于最大值")
        if self.enumValues is not None and (
            not self.enumValues
            or any(not v.strip() or len(v) > 20000 for v in self.enumValues)
        ):
            raise ValueError("枚举须为非空值列表")
        if isinstance(self.defaultValue, float):
            import math

            if not math.isfinite(self.defaultValue):
                raise ValueError("默认值不能为非有限数字")
        return self


def validate_schema_budget(node: JsonSchemaItem):
    """整个草稿最多1000节点、20层，防止嵌套或生成资源失控。"""
    count = 0

    def walk(item, depth):
        nonlocal count
        count += 1
        if depth > 20 or count > 1000:
            raise ValueError("Schema 最多20层、1000节点")
        for child in (item.properties or {}).values():
            walk(child, depth + 1)
        for child in item.items or []:
            walk(child, depth + 1)

    walk(node, 1)
    return node


class JsonBodySchema(BaseModel):
    model_config = ConfigDict(extra="forbid", hide_input_in_errors=True)
    enableJsonSchema: StrictBool = False
    jsonSchema: JsonSchemaItem = Field(
        default_factory=lambda: JsonSchemaItem(type="object", properties={})
    )

    @model_validator(mode="after")
    def valid_root(self):
        if self.jsonSchema.type not in {"object", "array"}:
            raise ValueError("Schema 根节点只能为object或array")
        validate_schema_budget(self.jsonSchema)
        return self
