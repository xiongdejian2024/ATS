"""评审目录和列表操作约束。"""

from typing import Literal

from pydantic import Field, field_validator, model_validator
from schemas.case_governance import StrictRequest, ReviewVote


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


class ReviewItemFilter(StrictRequest):
    """与关联列表共用的筛选范围，不接受分页或其他项目标识。"""

    search: str = Field(default="", max_length=255)
    folder: str = Field(default="all", max_length=255)
    includeDescendants: bool = True
    priority: Literal["P0", "P1", "P2", "P3"] | None = None
    state: (
        Literal["approved", "rejected", "under_review", "un_review", "re_review"] | None
    ) = None
    states: list[
        Literal["approved", "rejected", "under_review", "un_review", "re_review"]
    ] = Field(default_factory=list, max_length=5)
    reviewerId: str | None = Field(default=None, max_length=255)
    creatorId: str | None = Field(default=None, max_length=255)
    onlyMine: bool = False


class ReviewItemSelection(StrictRequest):
    itemIds: list[str] = Field(default_factory=list, max_length=10000)
    selectAll: bool = False
    excludeIds: list[str] = Field(default_factory=list, max_length=10000)
    condition: ReviewItemFilter = Field(default_factory=ReviewItemFilter)

    @field_validator("itemIds", "excludeIds")
    @classmethod
    def valid_items(cls, values):
        return ReviewAssociate.unique_nonempty_ids(values)

    @model_validator(mode="after")
    def selection_mode(self):
        if self.selectAll:
            if self.itemIds:
                raise ValueError("全部筛选范围不能同时指定条目编号")
        elif not self.itemIds or self.excludeIds or self.condition.model_fields_set:
            raise ValueError("逐条选择必须指定条目编号，不能混用筛选范围和排除项")
        return self


class ReviewItemVote(ReviewItemSelection, ReviewVote):
    pass


class ReviewItemReviewers(ReviewItemSelection):
    reviewerIds: list[str] = Field(min_length=1, max_length=50)
    append: bool = False

    @field_validator("reviewerIds")
    @classmethod
    def valid_reviewers(cls, values):
        return ReviewAssociate.unique_nonempty_ids(values)


class ReviewItemReReview(ReviewItemSelection):
    comment: str = Field(default="", max_length=10000)
