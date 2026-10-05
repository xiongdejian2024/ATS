"""主用例的筛选范围选择，不接受分页、用户或其他项目身份。"""

from typing import Any
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ScopeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class CaseQueryScope(ScopeRequest):
    search: str | None = Field(default=None, max_length=500)
    module_id: str | None = Field(default=None, alias="moduleId")
    module_ids: str | None = Field(default=None, alias="moduleIds", max_length=30000)
    priority: str | None = None
    status: str | None = None
    type: str | None = None
    tags: str | None = Field(default=None, max_length=10000)
    review_status: str | None = None
    is_automated: bool | None = None
    mine: bool = False
    followed: bool = False
    filters: dict[str, Any] | None = None

    @field_validator("filters")
    @classmethod
    def valid_filters(cls, value):
        from services.case_query import parse_filters
        from fastapi import HTTPException

        try:
            parse_filters(value)
        except HTTPException as exc:
            raise ValueError(exc.detail) from exc
        return value


class CaseSelection(ScopeRequest):
    selectAll: bool = False
    caseIds: list[str] = Field(default_factory=list, max_length=10000)
    excludeIds: list[str] = Field(default_factory=list, max_length=10000)
    # 独立评审表单允许在范围之外继续明确关联用例，使用同一范围计数。
    includeIds: list[str] = Field(default_factory=list, max_length=10000)
    condition: CaseQueryScope = Field(default_factory=CaseQueryScope)

    @field_validator("caseIds", "excludeIds", "includeIds")
    @classmethod
    def unique_ids(cls, values):
        if any(not value.strip() or value != value.strip() for value in values):
            raise ValueError("用例ID不能为空或包含空白")
        if len(values) != len(set(values)):
            raise ValueError("用例ID不能重复")
        return values

    @model_validator(mode="after")
    def selection_mode(self):
        if self.selectAll:
            if self.caseIds:
                raise ValueError("全范围选择不能混用逐条用例ID")
        elif not self.caseIds or self.excludeIds or self.includeIds or self.condition.model_fields_set:
            raise ValueError("逐条选择必须指定ID，不能混用筛选条件或排除项")
        return self


class CaseSelectionIssue(CaseSelection):
    issueId: str = Field(min_length=1)


class CaseSelectionMembership(CaseSelection):
    candidateIds: list[str] = Field(max_length=200)


class CaseSelectionExport(CaseSelection):
    format: str = "xlsx"
    layout: str = "case"
    fields: str | None = None
    sortBy: str = "created_at"
    sortOrder: str = "desc"
