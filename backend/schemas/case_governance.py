"""用例治理请求约束。"""

from typing import Literal, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator
from pydantic import model_validator
from datetime import date


class StrictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class RestoreVersion(StrictRequest):
    expectedVersion: int = Field(ge=1)
    reason: str = Field(min_length=1, max_length=500)


class ReviewCreate(StrictRequest):
    name: str = Field(min_length=1, max_length=200)
    caseIds: list[str] = Field(min_length=1, max_length=200)
    reviewerIds: list[str] = Field(min_length=1, max_length=50)
    policy: Literal["all", "any"] = "all"
    mode: Literal["single", "multiple"] | None = None
    description: str = Field(default="", max_length=10000)
    itemReviewers: dict[str, list[str]] = Field(default_factory=dict)
    startDate: date | None = None
    endDate: date | None = None

    @model_validator(mode="after")
    def period_and_assignments(self):
        if self.startDate and self.endDate and self.endDate < self.startDate:
            raise ValueError("评审结束日期不能早于开始日期")
        if set(self.itemReviewers) - set(self.caseIds):
            raise ValueError("逐条评审人仅可指定本评审用例")
        if any(
            not ids or len(ids) > 50 or len(set(ids)) != len(ids)
            for ids in self.itemReviewers.values()
        ):
            raise ValueError("每条用例必须有不重复的评审人")
        return self

    @field_validator("caseIds", "reviewerIds")
    @classmethod
    def unique_ids(cls, values):
        if any(not value.strip() for value in values) or len(set(values)) != len(
            values
        ):
            raise ValueError("ID 不能为空或重复")
        return values


class ReviewVote(StrictRequest):
    decision: Literal["approved", "rejected", "suggestion"]
    comment: str = Field(min_length=1, max_length=10000)


class ReviewBatchVote(ReviewVote):
    itemIds: list[str] = Field(min_length=1, max_length=200)


class ReviewResubmit(StrictRequest):
    caseIds: list[str] | None = None
    name: str | None = Field(default=None, min_length=1, max_length=200)
    reviewerIds: list[str] | None = None
    mode: Literal["single", "multiple"] | None = None
    description: str | None = Field(default=None, max_length=10000)
    itemReviewers: dict[str, list[str]] | None = None
    startDate: date | None = None
    endDate: date | None = None


class ReviewCommentCreate(StrictRequest):
    content: str = Field(min_length=1, max_length=10000)
    itemId: str | None = None


class SavedViewCreate(StrictRequest):
    name: str = Field(min_length=1, max_length=100)
    filters: dict[str, Any]

    @field_validator("filters")
    @classmethod
    def bounded_filters(cls, values):
        import json

        allowed = {
            "search",
            "moduleKeys",
            "filterConditions",
            "filterLogic",
            "level",
            "executionResult",
            "reviewResult",
            "sortBy",
            "sortOrder",
            "mine",
            "followed",
            "viewMode",
        }
        if set(values) - allowed or len(json.dumps(values, ensure_ascii=False)) > 20000:
            raise ValueError("筛选视图字段或大小不符合要求")
        if "moduleKeys" in values and (
            not isinstance(values["moduleKeys"], list)
            or not all(isinstance(v, str) for v in values["moduleKeys"])
        ):
            raise ValueError("模块筛选必须是字符串数组")
        if "filterConditions" in values and not isinstance(
            values["filterConditions"], list
        ):
            raise ValueError("筛选条件必须是数组")
        return values


class CaseBatchUpdate(StrictRequest):
    caseIds: list[str] = Field(min_length=1, max_length=200)
    priority: Literal["P0", "P1", "P2", "P3"] | None = None
    tags: list[str] | None = Field(default=None, max_length=50)
    isAutomated: bool | None = None
    moduleId: str | None = None


class CaseBatchCopy(StrictRequest):
    caseIds: list[str] = Field(min_length=1, max_length=200)
    moduleId: str | None
