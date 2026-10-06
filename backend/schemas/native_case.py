"""原生配置校验；参数变更由定义结构比较，客户端不得直接指定。"""
import json
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict, field_validator


class NativeBody(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
    expectedRevision: int = Field(0, ge=0)


class DefinitionInput(NativeBody):
    name: str = Field(min_length=1, max_length=255)
    protocol: str = Field(min_length=1, max_length=50, pattern=r'^[A-Z0-9_-]+$')
    path: str = Field(min_length=1, max_length=500)
    parameters: dict = Field(default_factory=dict)
    module_id: str | None = Field(None, min_length=1, max_length=36)
    state: Literal['PROCESSING', 'DEPRECATED', 'DONE'] | None = None
    tags: list[str] = Field(default_factory=list, max_length=100)

    @field_validator('tags')
    @classmethod
    def valid_tags(cls, values):
        if any(not v.strip() or len(v) > 100 for v in values) or len(values) != len(set(values)):
            raise ValueError('接口标签须为不重复的1到100字符文本')
        return values

    @field_validator('parameters')
    @classmethod
    def parameters_size(cls, value):
        if len(json.dumps(value, ensure_ascii=False)) > 20000:
            raise ValueError('请求参数最多20000字符')
        return value


class EnvironmentInput(NativeBody):
    name: str = Field(min_length=1, max_length=255)
    address: str = Field(min_length=1, max_length=500)


class ConfigInput(NativeBody):
    state: str = Field(min_length=1, max_length=30)
    environmentId: str | None = Field(None, min_length=1, max_length=36)
    apiDefinitionId: str | None = Field(None, min_length=1, max_length=36)
    parameters: dict = Field(default_factory=dict)
    syncDefinition: bool = False
    expectedDefinitionRevision: int | None = Field(None, ge=1)

    @field_validator('parameters')
    @classmethod
    def parameters_size(cls, value):
        return DefinitionInput.parameters_size(value)
