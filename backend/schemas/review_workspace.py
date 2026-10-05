"""评审目录和列表操作约束。"""

from typing import Literal

from pydantic import Field, field_validator
from schemas.case_governance import StrictRequest


class ModuleSave(StrictRequest):
    name: str = Field(min_length=1, max_length=100)
    parentId: str | None = None
    position: int = Field(default=0, ge=0, le=100000)


class ConfirmDelete(StrictRequest):
    name: str = Field(min_length=1, max_length=255)


class ReviewMove(StrictRequest):
    reviewIds: list[str] = Field(min_length=1, max_length=255)
    moduleId: str | None = None

    @field_validator("reviewIds")
    @classmethod
    def unique_ids(cls, values):
        if len(values) != len(set(values)) or any(
            not value.strip() for value in values
        ):
            raise ValueError("评审编号不能为空或重复")
        return values


class ReviewCandidateSelection(StrictRequest):
    search: str = Field(default="", max_length=255)
    folder: str = "all"
    priority: Literal["P0", "P1", "P2", "P3"] | None = None
    excludeIds: list[str] = Field(default_factory=list, max_length=10000)


class ReviewAssociate(StrictRequest):
    caseIds: list[str] = Field(min_length=1, max_length=10000)
    reviewerIds: list[str] = Field(min_length=1, max_length=50)

    @field_validator("caseIds", "reviewerIds")
    @classmethod
    def unique_nonempty_ids(cls, values):
        if any(not value.strip() for value in values) or len(values) != len(
            set(values)
        ):
            raise ValueError("编号不能为空或重复")
        return values


class ReviewItemSelection(StrictRequest):
    itemIds: list[str] = Field(min_length=1, max_length=10000)

    @field_validator("itemIds")
    @classmethod
    def valid_items(cls, values):
        return ReviewAssociate.unique_nonempty_ids(values)


class ReviewItemReviewers(ReviewItemSelection):
    reviewerIds: list[str] = Field(min_length=1, max_length=50)
    append: bool = False

    @field_validator("reviewerIds")
    @classmethod
    def valid_reviewers(cls, values):
        return ReviewAssociate.unique_nonempty_ids(values)
