"""计划关联候选范围；分页和身份由服务端决定。"""
from typing import Any, Literal
from pydantic import Field, StrictBool, field_validator, model_validator
from schemas.case_selection import ScopeRequest

Category = Literal['functional', 'api', 'scenario']


class CandidateCondition(ScopeRequest):
    search: str = Field('', max_length=255)
    folder: str = Field('all', min_length=1, max_length=36)
    priority: Literal['P0', 'P1', 'P2', 'P3'] | None = None
    filters: dict[str, Any] | None = None
    mine: StrictBool = False


class CandidateSelection(ScopeRequest):
    category: Category = 'functional'
    selectAll: StrictBool = False
    caseIds: list[str] = Field(default_factory=list, max_length=10000)
    excludeIds: list[str] = Field(default_factory=list, max_length=10000)
    condition: CandidateCondition = Field(default_factory=CandidateCondition)

    @field_validator('caseIds', 'excludeIds')
    @classmethod
    def unique_ids(cls, values):
        if any(not value.strip() or value != value.strip() or len(value) > 36 for value in values):
            raise ValueError('用例ID须为1到36字符且不含首尾空白')
        if len(values) != len(set(values)):
            raise ValueError('用例ID不能重复')
        return values

    @model_validator(mode='after')
    def selection_mode(self):
        if self.selectAll:
            if self.caseIds:
                raise ValueError('范围全选不能混用逐条用例ID')
            from fastapi import HTTPException
            from services.plan_candidate_filter import parse_candidate_filters
            try:
                parse_candidate_filters(self.condition.filters, self.category)
            except HTTPException as exc:
                from core.logger import logger
                logger.exception('计划关联范围高级筛选校验失败')
                raise ValueError(exc.detail) from exc
        elif not self.caseIds or self.excludeIds or self.condition.model_fields_set:
            raise ValueError('逐条选择必须指定ID，不能混用筛选条件或排除项')
        return self


class Association(CandidateSelection):
    collectionId: str | None = Field(None, min_length=1, max_length=36)
    suiteId: str | None = Field(None, min_length=1, max_length=36)
