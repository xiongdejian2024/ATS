"""关联抽屉的视图使用主用例条件，拒绝计划实例字段。"""

import json
from fastapi import HTTPException
from pydantic import field_validator
from schemas.case_governance import SavedViewRename
from core.logger import logger


def validate_filters(values):
    if not isinstance(values, dict) or set(values) - {'filterConditions', 'filterLogic'}:
        raise ValueError('关联视图只支持高级筛选条件和组合逻辑')
    if len(json.dumps(values, ensure_ascii=False)) > 20000:
        raise ValueError('关联视图条件过大')
    try:
        from services.case_query import parse_filters
        from services.plan_definition_candidates import FIELDS
        from services.native_candidate_context import NATIVE_FIELDS
        # 这里只验证结构；接口/用例字段范围在带资源模式的路由中再次校验。
        parse_filters(dict(conditions=values.get('filterConditions', []), logic=values.get('filterLogic', 'and')), extra_fields=FIELDS | NATIVE_FIELDS)
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
