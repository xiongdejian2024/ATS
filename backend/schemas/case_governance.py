"""用例治理请求约束。"""

from typing import Literal, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator
from pydantic import model_validator
from datetime import date, datetime


class StrictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class RestoreVersion(StrictRequest):
    expectedVersion: int = Field(ge=1)
    reason: str = Field(min_length=1, max_length=500)


class ReviewHeader(StrictRequest):
    """创建与基本信息编辑共享字段，不携带用例或结论写入字段。"""

    name: str = Field(min_length=1, max_length=255)
    reviewerIds: list[str] = Field(min_length=1, max_length=50)
    mode: Literal["single", "multiple"] | None = None
    description: str = Field(default="", max_length=10000)
    startDate: date | None = None
    endDate: date | None = None
    startTime: datetime | None = None
    endTime: datetime | None = None
    moduleId: str | None = None
    tags: list[str] = Field(default_factory=list, max_length=50)

    @field_validator("startTime", "endTime")
    @classmethod
    def local_period(cls, value):
        from utils.datetime_utils import BEIJING_TZ

        if value is None:
            return None
        return (
            value.replace(tzinfo=BEIJING_TZ)
            if value.tzinfo is None
            else value.astimezone(BEIJING_TZ)
        )

    @field_validator("tags")
    @classmethod
    def normalized_tags(cls, values):
        values = [v.strip() for v in values]
        if any(not v or len(v) > 100 for v in values) or len(set(values)) != len(
            values
        ):
            raise ValueError("标签必须不重复且长度为1至100个字符")
        return values

    @field_validator("reviewerIds")
    @classmethod
    def unique_ids(cls, values):
        if any(not value.strip() for value in values) or len(set(values)) != len(
            values
        ):
            raise ValueError("ID 不能为空或重复")
        return values

    @model_validator(mode="after")
    def period_order(self):
        if bool(self.startTime) != bool(self.endTime):
            raise ValueError("评审周期开始时间和结束时间必须同时填写")
        if self.startTime and self.endTime < self.startTime:
            raise ValueError("评审结束时间不能早于开始时间")
        if self.startDate and self.endDate and self.endDate < self.startDate:
            raise ValueError("评审结束日期不能早于开始日期")
        return self


class ReviewCreate(ReviewHeader):
    caseIds: list[str] = Field(default_factory=list, max_length=10000)
    policy: Literal["all", "any"] = "all"
    itemReviewers: dict[str, list[str]] = Field(default_factory=dict)

    @field_validator("caseIds")
    @classmethod
    def unique_cases(cls, values):
        return ReviewHeader.unique_ids(values)

    @model_validator(mode="after")
    def assignments(self):
        if set(self.itemReviewers) - set(self.caseIds):
            raise ValueError("逐条评审人仅可指定本评审用例")
        if any(
            not ids
            or len(ids) > 50
            or len(set(ids)) != len(ids)
            or any(not i.strip() for i in ids)
            for ids in self.itemReviewers.values()
        ):
            raise ValueError("每条用例必须有不重复的评审人")
        return self


class ReviewVote(StrictRequest):
    decision: Literal["approved", "rejected", "suggestion"]
    comment: str = Field(default="", max_length=10000)

    @model_validator(mode="after")
    def required_reason(self):
        from utils.rich_text import has_visible_content

        if self.decision != "approved" and not has_visible_content(self.comment):
            raise ValueError("不通过或建议必须填写评审理由")
        return self


class ReviewBatchVote(ReviewVote):
    itemIds: list[str] = Field(min_length=1, max_length=10000)


class ReviewResubmit(StrictRequest):
    caseIds: list[str] | None = None
    name: str | None = Field(default=None, min_length=1, max_length=255)
    reviewerIds: list[str] | None = None
    mode: Literal["single", "multiple"] | None = None
    description: str | None = Field(default=None, max_length=10000)
    itemReviewers: dict[str, list[str]] | None = None
    startDate: date | None = None
    endDate: date | None = None
    startTime: datetime | None = None
    endTime: datetime | None = None
    moduleId: str | None = None
    tags: list[str] | None = None


class ReviewCommentCreate(StrictRequest):
    content: str = Field(min_length=1, max_length=10000)
    itemId: str | None = None


class SavedViewRename(StrictRequest):
    name: str = Field(min_length=1, max_length=255)

    @field_validator("name")
    @classmethod
    def nonblank_name(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("视图名称不能为空")
        return value


class SavedViewCreate(SavedViewRename):
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
        from services.case_query import parse_filters
        from fastapi import HTTPException

        try:
            parse_filters(
                {
                    "conditions": values.get("filterConditions", []),
                    "logic": values.get("filterLogic", "and"),
                }
            )
        except HTTPException as exc:
            raise ValueError(exc.detail) from exc
        return values


class SavedViewUpdate(SavedViewRename):
    filters: dict[str, Any] | None = None

    @field_validator("filters")
    @classmethod
    def valid_filters(cls, values):
        if values is None:
            raise ValueError("视图筛选不能为null，请使用空对象清空")
        return SavedViewCreate.bounded_filters(values)


class CaseBatchUpdate(StrictRequest):
    caseIds: list[str] = Field(min_length=1, max_length=200)
    priority: Literal["P0", "P1", "P2", "P3"] | None = None
    tags: list[str] | None = Field(default=None, max_length=50)
    isAutomated: bool | None = None
    moduleId: str | None = None


class CaseBatchCopy(StrictRequest):
    caseIds: list[str] = Field(min_length=1, max_length=200)
    moduleId: str | None
