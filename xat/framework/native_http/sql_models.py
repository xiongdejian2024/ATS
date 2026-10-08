"""Synthetic in-memory SQLite fixtures and bound, read-only queries."""
import json
import re
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, model_validator, field_validator


class Model(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True, hide_input_in_errors=True, allow_inf_nan=False)


class SqlColumn(Model):
    name: str = Field(min_length=1, max_length=64, pattern=r'^[A-Za-z_][A-Za-z0-9_]*$')
    type: Literal['TEXT', 'INTEGER', 'REAL'] = 'TEXT'


class SqlTable(Model):
    name: str = Field(min_length=1, max_length=64, pattern=r'^[A-Za-z_][A-Za-z0-9_]*$')
    columns: list[SqlColumn] = Field(min_length=1, max_length=20)
    rows: list[dict[str, str | StrictInt | float | StrictBool | None]] = Field(default_factory=list, max_length=1000)

    @model_validator(mode='after')
    def consistent_rows(self):
        columns={c.name for c in self.columns}
        if len({c.name.casefold() for c in self.columns})!=len(self.columns) or any(set(r)!=columns for r in self.rows):
            raise ValueError('合成SQL表列重复或行结构不一致')
        return self


class SqlBinding(Model):
    name: str = Field(min_length=1, max_length=255)
    column: str = Field(min_length=1, max_length=255)
    row: StrictInt = Field(default=0, ge=0, le=999)

    @field_validator('name')
    @classmethod
    def valid_name(cls, value):
        from .variable_models import InitialVariable
        return InitialVariable(name=value).name


class SqlProcessor(Model):
    type: Literal['sql'] = 'sql'
    id: str = Field(min_length=1, max_length=36)
    name: str = Field(default='只读合成SQL', max_length=255)
    enable: StrictBool = True
    query: str = Field(min_length=1, max_length=8192)
    parameters: dict[str, str | StrictInt | float | StrictBool | None] = Field(default_factory=dict)
    tables: list[SqlTable] = Field(default_factory=list, max_length=10)
    bindings: list[SqlBinding] = Field(default_factory=list, max_length=100)
    maxRows: StrictInt = Field(default=100, ge=1, le=1000)
    timeoutMs: StrictInt = Field(default=1000, ge=50, le=2000)

    @model_validator(mode='after')
    def bounded(self):
        if (len({t.name.casefold() for t in self.tables})!=len(self.tables)
                or len({b.name for b in self.bindings})!=len(self.bindings)
                or len(self.parameters)>100
                or any(not k or len(k)>255 for k in self.parameters)
                or len(json.dumps(self.model_dump(),ensure_ascii=False,allow_nan=False).encode())>256*1024):
            raise ValueError('SQL处理器、表、绑定名称重复或配置超过限制')
        return self
