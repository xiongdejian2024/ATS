"""实例缺陷批量绑定采用功能脑图相同范围；严格拒绝混用参数。"""
from uuid import UUID
from pydantic import Field, field_validator
from schemas.plan_functional_minder import FunctionalMinderSelection


class PlanDefectCreate(FunctionalMinderSelection):
    requestId: UUID
    title: str = Field(min_length=1, max_length=300)
    description: str = Field('', max_length=20000)

    @field_validator('title')
    @classmethod
    def nonempty(cls, value):
        if not value.strip(): raise ValueError('缺陷标题不能为空')
        return value.strip()


class PlanDefectAssociate(FunctionalMinderSelection):
    issueIds: list[str] = Field(min_length=1, max_length=100)

    @field_validator('issueIds')
    @classmethod
    def unique(cls, values):
        if len(values) != len(set(values)) or any(not v or len(v) > 36 for v in values):
            raise ValueError('缺陷ID无效或重复')
        return values
