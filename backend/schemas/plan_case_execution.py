"""计划功能用例手工回填参数，与节点任务分发分离。"""
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class Selection(BaseModel):
    model_config = ConfigDict(extra='forbid')
    source: Literal['legacy', 'node']
    id: str = Field(min_length=1, max_length=36)

class StepResult(BaseModel):
    model_config = ConfigDict(extra='forbid')
    index: int = Field(ge=0, le=999)
    result: Literal['pending', 'passed', 'failed', 'blocked']
    actual: str = Field('', max_length=10000)

class ExecuteInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    requestId: UUID
    selections: list[Selection] = Field(min_length=1, max_length=500)
    result: Literal['pending', 'passed', 'failed', 'blocked']
    description: str = Field('', max_length=20000)
    stepResults: list[StepResult] = Field(default_factory=list, max_length=1000)
