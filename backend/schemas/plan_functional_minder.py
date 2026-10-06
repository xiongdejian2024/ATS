"""功能脑图当前范围与执行参数；复用已有严格实例选择规则。"""
from uuid import UUID
from typing import Literal
from pydantic import Field, field_validator, model_validator
from schemas.plan_native_selection import NativeWorkspaceSelection, NativeWorkspaceCondition


class FunctionalMinderCondition(NativeWorkspaceCondition):
    folderIds: list[str] = Field(default_factory=list, max_length=500)
    entryIds: list[str] = Field(default_factory=list, max_length=10000)

    @field_validator('entryIds')
    @classmethod
    def instances(cls, values):
        return NativeWorkspaceSelection.identities(values)

    @field_validator('folderIds')
    @classmethod
    def folders(cls, values):
        if len(values) != len(set(values)) or any(not value or len(value) > 80 for value in values):
            raise ValueError('目录ID无效或重复')
        return values

    @model_validator(mode='after')
    def union_scope(self):
        if (self.folderIds or self.entryIds) and self.folder != 'all':
            raise ValueError('多节点范围不能混用单目录范围')
        return self


class FunctionalMinderSelection(NativeWorkspaceSelection):
    category: Literal['functional'] = 'functional'
    condition: FunctionalMinderCondition = Field(default_factory=FunctionalMinderCondition)


class FunctionalMinderExecute(FunctionalMinderSelection):
    requestId: UUID
    result: Literal['pending', 'passed', 'failed', 'blocked']
    description: str = Field('', max_length=20000)

    @property
    def stepResults(self):
        # 脑图整体/目录回填不伪造逐步骤结果；步骤弹窗走原单用例执行入口。
        return []


class FunctionalMinderBatch(FunctionalMinderSelection):
    action: Literal['assign', 'unlink']
    assignedTo: str | None = Field(None, min_length=1, max_length=36)

    @model_validator(mode='after')
    def assign_only(self):
        if self.action != 'assign' and 'assignedTo' in self.model_fields_set:
            raise ValueError('执行人字段只适用于更改执行人')
        return self
