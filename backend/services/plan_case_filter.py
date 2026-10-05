"""复用主用例条件运算，计划结果与执行人始终按关联实例判断。"""

from models import TestCase
from services.case_query import parse_filters, matches, matches_case
from services.case_filter_context import CaseFilterContext
from services.case_governance import current_review_statuses
from fastapi import HTTPException

PLAN_FIELDS = {"collectionId", "projectId", "result", "bugCount"}


def parse_plan_filters(raw):
    conditions, logic = parse_filters(raw, extra_fields=PLAN_FIELDS)
    for condition in conditions:
        if condition['field'] == 'bugCount':
            if condition['operator'] not in {'equals', 'not_equals', 'gt', 'gte', 'lt', 'lte', 'is_empty', 'is_not_empty'}:
                raise HTTPException(422, '缺陷数只支持整数比较')
            if condition['operator'] not in {'is_empty', 'is_not_empty'} and (
                type(condition.get('value')) is not int or condition['value'] < 0
            ):
                raise HTTPException(422, '缺陷数必须为非负整数')
    return conditions, logic


def filter_entries(db, plan, items, raw, user_id):
    conditions, logic = parse_plan_filters(raw)
    context = CaseFilterContext(
        db, plan.project_id, conditions, user_id, include_recycled=True
    )
    if not context.conditions:
        return items
    ids = {item["caseId"] for item in items}
    cases = {
        case.id: case
        for case in db.query(TestCase).filter(
            TestCase.id.in_(ids), TestCase.project_id == plan.project_id
        )
    }
    statuses = current_review_statuses(db, list(cases.values())) if any(
        c["field"] in {"reviewResult", "review_status"} for c in conditions
    ) else {}

    def check(item, condition):
        field = condition["field"]
        if field in PLAN_FIELDS or field == "executorId":
            value = (plan.project_id if field == "projectId" else
                     item.get("assignedTo" if field == "executorId" else field))
            expected = condition.get("value")
            if field == "collectionId":
                expected = [None if v == "__default__" else v for v in expected] if isinstance(expected, list) else (None if expected == "__default__" else expected)
            return matches(value, condition["operator"], expected)
        return matches_case(cases[item["caseId"]], condition, statuses, context)

    combine = all if logic == "and" else any
    return [item for item in items if combine(check(item, c) for c in context.conditions)]
