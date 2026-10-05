"""个人视图只保存明确支持的高级条件，拒绝未知参数。"""

import json
from pydantic import field_validator
from fastapi import HTTPException
from schemas.case_governance import SavedViewRename
from services.plan_case_filter import parse_plan_filters


def validate_filters(values):
    if not isinstance(values, dict) or set(values) - {"filterConditions", "filterLogic"}:
        raise ValueError("计划视图只支持高级筛选条件和组合逻辑")
    if len(json.dumps(values, ensure_ascii=False)) > 20000:
        raise ValueError("个人视图筛选条件过大")
    try:
        parse_plan_filters({"conditions": values.get("filterConditions", []),
                       "logic": values.get("filterLogic", "and")})
    except HTTPException as exc:
        raise ValueError(exc.detail) from exc
    return values


class PlanCaseViewCreate(SavedViewRename):
    filters: dict

    @field_validator("filters")
    @classmethod
    def valid_filters(cls, values):
        return validate_filters(values)


class PlanCaseViewUpdate(SavedViewRename):
    filters: dict | None = None

    @field_validator("filters")
    @classmethod
    def valid_filters(cls, values):
        return validate_filters(values)
