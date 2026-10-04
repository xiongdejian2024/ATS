"""计划编排请求约束。"""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class PlanPolicy(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    group_id: str | None = Field(None, alias="groupId")
    execution_mode: Literal["serial", "parallel"] = Field("serial", alias="executionMode")
    stop_on_failure: bool = Field(False, alias="stopOnFailure")
    pass_threshold: float = Field(100, ge=0, le=100, alias="passThreshold")
    suite_order: list[str] = Field(default_factory=list, alias="suiteOrder")


class GroupInput(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(None, max_length=2000)


class ManualResultInput(BaseModel):
    result: Literal["passed", "failed", "error", "skipped"]
    notes: str = Field("", max_length=10000)
