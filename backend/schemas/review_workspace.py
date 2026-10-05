"""评审目录和列表操作约束。"""

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
