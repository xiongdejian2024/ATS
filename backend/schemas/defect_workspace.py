"""Versioned bounded defect input contracts; no arbitrary JSON or fake save."""

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, model_validator
from typing import Literal, Any
from schemas.case_features import CustomField


class StrictInput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class DefectWrite(StrictInput):
    title: str = Field(min_length=1, max_length=300)
    description: str = Field("", max_length=30000)
    descriptionFormat: Literal["plain", "rich"] = "plain"
    status: Literal["open", "in_progress", "resolved", "closed"] = "open"
    externalRef: str | None = Field(None, max_length=500)
    templateId: str | None = Field(None, min_length=1, max_length=36)
    customFields: dict[str, Any] = Field(default_factory=dict, max_length=50)
    fileIds: list[str] = Field(default_factory=list, max_length=50)
    expectedRevision: StrictInt = Field(0, ge=0)
    requestId: str | None = Field(None, min_length=1, max_length=36)

    @model_validator(mode="after")
    def valid(self):
        if not self.title.strip():
            raise ValueError("缺陷标题不能为空")
        if len(self.fileIds) != len(set(self.fileIds)):
            raise ValueError("文件不能重复")
        return self


class RevisionInput(StrictInput):
    expectedRevision: StrictInt = Field(ge=0)


class ArchiveInput(RevisionInput):
    archived: StrictBool


class DefectTemplateWrite(StrictInput):
    name: str = Field(min_length=1, max_length=100)
    fields: list[CustomField] = Field(default_factory=list, max_length=50)
    defaults: dict[str, Any] = Field(default_factory=dict)
    isDefault: StrictBool = False
    expectedRevision: StrictInt = Field(0, ge=0)

    @model_validator(mode="after")
    def valid(self):
        if not self.name.strip() or len({f.key for f in self.fields}) != len(self.fields):
            raise ValueError("名称为空或字段键重复")
        if set(self.defaults) - {"status", "description", "externalRef"}:
            raise ValueError("模板默认属性不支持此字段")
        for f in self.fields:
            if f.type in {"select", "multiselect"} and (
                not f.options or len(set(f.options)) != len(f.options)
            ):
                raise ValueError("选择字段需要不重复的候选项")
        DefectWrite(title="validation", **self.defaults)
        return self


class DefectCommentWrite(StrictInput):
    content: str = Field(min_length=1, max_length=10000)
    fileIds: list[str] = Field(default_factory=list, max_length=50)
    expectedRevision: StrictInt = Field(ge=0)
    requestId: str = Field(min_length=1, max_length=36)
