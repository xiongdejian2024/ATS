"""任务中心输入校验。"""

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class ScheduleCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    project_id: str = Field(alias="projectId")
    name: str = Field(min_length=1, max_length=255)
    target_type: Literal["suite", "plan", "group"] = Field(alias="targetType")
    target_id: str = Field(alias="targetId")
    cron_expression: str | None = Field(default=None, alias="cronExpression", max_length=100)
    timezone: str = Field(default="Asia/Shanghai", max_length=64)


class ScheduleUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    name: str = Field(min_length=1, max_length=255)
    cron_expression: str | None = Field(default=None, alias="cronExpression", max_length=100)
    timezone: str = Field(default="Asia/Shanghai", max_length=64)


class ScheduleEnabled(BaseModel):
    enabled: bool


class RunTrigger(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    request_id: str = Field(alias="requestId", min_length=1, max_length=80)
