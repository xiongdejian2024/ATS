from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictBool, model_validator


class PoolInput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    name: str = Field(min_length=1, max_length=255)
    description: str = Field("", max_length=10000)
    type: Literal["Node"] = "Node"
    enabled: StrictBool = True
    applications: list[Literal["api", "scenario"]] = Field(min_length=1, max_length=2)
    allProjects: StrictBool = False
    projectIds: list[str] = Field(default_factory=list, max_length=100)
    environmentIds: list[str] = Field(min_length=1, max_length=100)
    expectedRevision: StrictInt = Field(ge=0)
    requestId: str | None = Field(None, min_length=1, max_length=36)

    @model_validator(mode="after")
    def validate_scope(self):
        if not self.name.strip():
            raise ValueError("名称不能为空")
        for values in [self.projectIds, self.environmentIds, self.applications]:
            if len(values) != len(set(values)) or any(
                not 1 <= len(value) <= 36 for value in values
            ):
                raise ValueError("标识须非空且不重复")
        if self.allProjects and self.projectIds or not self.allProjects and not self.projectIds:
            raise ValueError("请选择全部项目或明确的适用项目")
        return self


class PoolRevision(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    expectedRevision: StrictInt = Field(ge=1)


class PoolEnable(PoolRevision):
    enabled: StrictBool
