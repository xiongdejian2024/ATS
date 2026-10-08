"""计划首页个人视图只保存可见条件，不虚构创建人或隐含范围。"""
import json
from fastapi import HTTPException
from pydantic import field_validator
from schemas.case_governance import SavedViewRename
from services.plan_index_filter import parse


def validate(value):
    if not isinstance(value,dict) or set(value)-{"filterConditions","filterLogic"}:
        raise ValueError("计划视图结构不合法")
    if len(json.dumps(value,ensure_ascii=False))>20000:
        raise ValueError("计划视图条件过大")
    try:
        parse(dict(conditions=value.get("filterConditions",[]),logic=value.get("filterLogic","and")))
    except HTTPException as exc:
        raise ValueError("计划视图条件不合法") from exc
    return value


class PlanIndexViewCreate(SavedViewRename):
    filters: dict
    @field_validator("filters")
    @classmethod
    def filters_valid(cls,value): return validate(value)


class PlanIndexViewUpdate(SavedViewRename):
    filters: dict | None = None
    @field_validator("filters")
    @classmethod
    def filters_valid(cls,value): return validate(value)
