from pydantic import BaseModel, ConfigDict, Field, StrictInt, model_validator


class MappingInput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    projectId: str = Field(min_length=1, max_length=36)
    environmentId: str = Field(min_length=1, max_length=36)


class EnvironmentGroupInput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    name: str = Field(min_length=1, max_length=255)
    description: str = Field("", max_length=10000)
    expectedRevision: StrictInt = Field(ge=0)
    requestId: str | None = Field(None, min_length=1, max_length=36)
    mappings: list[MappingInput] = Field(min_length=1, max_length=100)

    @model_validator(mode="after")
    def unique_projects(self):
        if not self.name.strip() or len({m.projectId for m in self.mappings}) != len(
            self.mappings
        ):
            raise ValueError("名称不能为空，每个来源项目只能映射一个请求环境")
        return self


class EnvironmentGroupRevision(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    expectedRevision: StrictInt = Field(ge=1)
