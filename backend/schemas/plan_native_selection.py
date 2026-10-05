"""原生计划关联实例范围，身份和分页均由服务端确定。"""
import re
from typing import Any, Literal
from pydantic import Field, StrictBool, field_validator, model_validator
from fastapi import HTTPException
from schemas.case_selection import ScopeRequest
from services.plan_case_filter import parse_plan_filters
from core.logger import logger


class NativeWorkspaceCondition(ScopeRequest):
    tree_type: Literal['COLLECTION', 'MODULE'] = 'COLLECTION'
    folder: str = Field('all', min_length=1, max_length=80)
    search: str = Field('', max_length=255)
    include_descendants: StrictBool = True
    protocols: str | None = Field(None, max_length=1000)
    priority: str | None = Field(None, max_length=100)
    result: str | None = Field(None, max_length=100)
    executor: str | None = Field(None, max_length=36)
    tag: str | None = Field(None, max_length=255)
    filters: dict[str, Any] | None = None
    mine: StrictBool = False


class NativeWorkspaceSelection(ScopeRequest):
    category: Literal['api', 'scenario']
    selectAll: StrictBool = False
    selectIds: list[str] = Field(default_factory=list, max_length=10000)
    excludeIds: list[str] = Field(default_factory=list, max_length=10000)
    condition: NativeWorkspaceCondition = Field(default_factory=NativeWorkspaceCondition)

    @field_validator('selectIds', 'excludeIds')
    @classmethod
    def identities(cls, values):
        if len(values) != len(set(values)) or any(not re.fullmatch(r'(legacy|node):[^:\s]{1,36}:[^:\s]{1,36}', value) for value in values):
            raise ValueError('关联实例ID格式无效或重复')
        return values

    @model_validator(mode='after')
    def selection_mode(self):
        if self.selectAll:
            if self.selectIds:
                raise ValueError('全范围选择不能混用逐条实例ID')
            if self.category != 'api' and self.condition.protocols is not None:
                raise ValueError('协议筛选只适用于API用例')
            try:
                parse_plan_filters(self.condition.filters, self.category)
            except HTTPException as exc:
                logger.exception('原生计划范围高级条件校验失败')
                raise ValueError(exc.detail) from exc
        elif not self.selectIds or self.excludeIds or self.condition.model_fields_set:
            raise ValueError('逐条选择必须指定实例ID，不能混用条件或排除项')
        return self


class NativeWorkspaceBatch(NativeWorkspaceSelection):
    action: Literal['move', 'unlink']
    collectionId: str | None = Field(None, min_length=1, max_length=36)
