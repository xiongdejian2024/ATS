"""关联抽屉的视图使用主用例条件，拒绝计划实例字段。"""

import json
from fastapi import HTTPException
from pydantic import field_validator
from schemas.case_governance import SavedViewRename
from services.plan_candidate_filter import parse_candidate_filters
from core.logger import logger


def validate_filters(values):
    if not isinstance(values, dict) or set(values) - {'filterConditions', 'filterLogic'}:
        raise ValueError('关联视图只支持高级筛选条件和组合逻辑')
    if len(json.dumps(values, ensure_ascii=False)) > 20000:
        raise ValueError('关联视图条件过大')
    try:
        parse_candidate_filters(dict(conditions=values.get('filterConditions', []), logic=values.get('filterLogic', 'and')))
    except HTTPException as exc:
        logger.exception("计划关联视图条件校验失败")
        raise ValueError(exc.detail) from exc
    return values


class CandidateViewCreate(SavedViewRename):
    filters: dict

    @field_validator('filters')
    @classmethod
    def valid_filters(cls, value):
        return validate_filters(value)


class CandidateViewUpdate(SavedViewRename):
    filters: dict | None = None

    @field_validator('filters')
    @classmethod
    def valid_filters(cls, value):
        return validate_filters(value)
