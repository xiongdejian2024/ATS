"""用例治理请求约束。"""

from typing import Literal, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator


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

    @field_validator("caseIds", "reviewerIds")
    @classmethod
    def unique_ids(cls, values):
        if any(not value.strip() for value in values) or len(set(values)) != len(
            values
        ):
            raise ValueError("ID 不能为空或重复")
        return values


class ReviewVote(StrictRequest):
    decision: Literal["approved", "rejected"]
    comment: str = Field(min_length=1, max_length=10000)


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
