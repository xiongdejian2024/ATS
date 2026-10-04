"""用例扩展输入契约；未知字段拒绝，避免假保存。"""

from typing import Any, Literal
from pydantic import Field, model_validator
from schemas.case_governance import StrictRequest


class CustomField(StrictRequest):
    key: str = Field(pattern=r"^[A-Za-z][A-Za-z0-9_]{0,49}$")
    name: str = Field(min_length=1, max_length=100)
    type: Literal[
        "text", "textarea", "number", "boolean", "date", "select", "multiselect"
    ]
    required: bool = False
    options: list[str] = Field(default_factory=list, max_length=100)
    default: Any = None


class TemplateWrite(StrictRequest):
    name: str = Field(min_length=1, max_length=100)
    fields: list[CustomField] = Field(default_factory=list, max_length=50)
    defaults: dict[str, Any] = Field(default_factory=dict)
    isDefault: bool = False

    @model_validator(mode="after")
    def validate_template(self):
        if len({f.key for f in self.fields}) != len(self.fields):
            raise ValueError("自定义字段键不能重复")
        if set(self.defaults) - {
            "type",
            "priority",
            "precondition",
            "steps",
            "tags",
            "is_automated",
        }:
            raise ValueError("模板默认属性不支持该字段")
        for f in self.fields:
            if f.type in {"select", "multiselect"} and (
                not f.options or len(set(f.options)) != len(f.options)
            ):
                raise ValueError("选择字段必须配置不重复的选项")
        return self


class IssueWrite(StrictRequest):
    kind: Literal["requirement", "defect"]
    title: str = Field(min_length=1, max_length=300)
    description: str = Field(default="", max_length=30000)
    status: Literal["open", "in_progress", "resolved", "closed"] = "open"
    externalRef: str | None = Field(default=None, max_length=500)


class IssueLinkWrite(StrictRequest):
    issueId: str


class RelationWrite(StrictRequest):
    targetCaseId: str
    kind: Literal["precondition", "postcondition", "related"]


class AutomationWrite(StrictRequest):
    category: Literal["api", "scenario", "ui", "script"]
    targetCaseId: str | None = None
    suiteId: str | None = None
    externalRef: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def require_target(self):
        if (
            sum(bool(v) for v in [self.targetCaseId, self.suiteId, self.externalRef])
            != 1
        ):
            raise ValueError("请选择一个自动化用例、执行套件或外部引用")
        return self


class CommentWrite(StrictRequest):
    content: str = Field(min_length=1, max_length=10000)


class ProjectSettingsWrite(StrictRequest):
    autoResubmit: bool
