"""统一列表与导出的筛选语义，未知字段和运算明确拒绝。"""

import json
from fastapi import HTTPException

FIELDS = {
    "id": "case_code",
    "caseCode": "case_code",
    "name": "name",
    "moduleId": "module_id",
    "priority": "priority",
    "level": "priority",
    "type": "type",
    "status": "status",
    "isAutomated": "is_automated",
    "tags": "tags",
    "requirementRef": "requirement_ref",
    "precondition": "precondition",
    "executorId": "executor_id",
    "createdBy": "created_by",
    "templateId": "template_id",
    "createdAt": "created_at",
    "updatedAt": "updated_at",
}
OPERATORS = {
    "equals",
    "not_equals",
    "contains",
    "not_contains",
    "in",
    "not_in",
    "belongs_to",
    "not_belongs_to",
    "is_empty",
    "is_not_empty",
    "gt",
    "gte",
    "lt",
    "lte",
    "starts_with",
    "ends_with",
}


def parse_filters(raw):
    if not raw:
        return [], "and"
    if isinstance(raw, str):
        if len(raw) > 30000:
            raise HTTPException(422, "筛选条件过大")
        try:
            raw = json.loads(raw)
        except ValueError as exc:
            raise HTTPException(422, "筛选条件不是有效JSON") from exc
    if not isinstance(raw, dict) or set(raw) - {"conditions", "logic"}:
        raise HTTPException(422, "筛选结构不合法")
    conditions, logic = raw.get("conditions", []), raw.get("logic", "and")
    if (
        logic not in {"and", "or"}
        or not isinstance(conditions, list)
        or len(conditions) > 100
    ):
        raise HTTPException(422, "筛选逻辑或条件数量不合法")
    for item in conditions:
        if not isinstance(item, dict) or item.get("operator") not in OPERATORS:
            raise HTTPException(422, "不支持的筛选运算符")
        field = item.get("field", "")
        if not isinstance(field, str):
            raise HTTPException(422, "筛选字段必须为字符串")
        if (
            field not in FIELDS
            and field not in {"reviewResult", "review_status"}
            and not field.startswith("customFields.")
        ):
            raise HTTPException(422, "不支持的筛选字段")
        if item["operator"] in {
            "in",
            "not_in",
            "belongs_to",
            "not_belongs_to",
        } and not isinstance(item.get("value"), (list, str)):
            raise HTTPException(422, "筛选集合必须为字符串或数组")
    return conditions, logic


def matches(actual, operator, expected):
    empty = actual is None or actual == "" or actual == []
    if operator == "is_empty":
        return empty
    if operator == "is_not_empty":
        return not empty
    if (
        isinstance(actual, bool)
        and isinstance(expected, str)
        and expected in {"true", "false"}
    ):
        expected = expected == "true"
    if operator == "equals":
        return actual == expected
    if operator == "not_equals":
        return actual != expected
    if operator in {"contains", "not_contains"}:
        if isinstance(actual, list):
            result = all(
                v in actual
                for v in (expected if isinstance(expected, list) else [expected])
            )
        else:
            result = str(expected or "").casefold() in str(actual or "").casefold()
        return result if operator == "contains" else not result
    if operator in {"in", "not_in", "belongs_to", "not_belongs_to"}:
        values = expected if isinstance(expected, list) else [expected]
        result = (
            any(v in values for v in actual)
            if isinstance(actual, list)
            else actual in values
        )
        return not result if operator in {"not_in", "not_belongs_to"} else result
    if operator == "starts_with":
        return str(actual or "").casefold().startswith(str(expected or "").casefold())
    if operator == "ends_with":
        return str(actual or "").casefold().endswith(str(expected or "").casefold())
    if hasattr(actual, "isoformat"):
        actual = actual.isoformat()
    if actual is None or expected is None:
        return False
    try:
        return {
            "gt": lambda: actual > expected,
            "gte": lambda: actual >= expected,
            "lt": lambda: actual < expected,
            "lte": lambda: actual <= expected,
        }[operator]()
    except TypeError as exc:
        raise HTTPException(422, "筛选字段与比较值类型不一致") from exc


def apply_conditions(cases, conditions, logic, review_statuses):
    def check(case, condition):
        field = condition["field"]
        if field in {"reviewResult", "review_status"}:
            value = review_statuses.get(case.id, "not_reviewed")
        elif field.startswith("customFields."):
            value = (case.custom_fields or {}).get(field.split(".", 1)[1])
        else:
            value = getattr(case, FIELDS[field])
        expected = condition.get("value")
        if field == "moduleId":
            if isinstance(expected, list):
                expected = [
                    None if v in {"null", "unplanned", "__unassigned__"} else v
                    for v in expected
                ]
            elif isinstance(expected, str) and expected in {
                "null",
                "unplanned",
                "__unassigned__",
            }:
                expected = None
        return matches(value, condition["operator"], expected)

    combine = all if logic == "and" else any
    return [
        case
        for case in cases
        if not conditions or combine(check(case, c) for c in conditions)
    ]


def query_cases(db, project_id, **options):
    from models.test_case import TestCase
    from models.case_features import CaseFollow
    from services.case_governance import current_review_statuses
    from sqlalchemy import or_

    page, size = options.get("page", 1), options.get("size", 20)
    if page < 1 or not 1 <= size <= 100000:
        raise HTTPException(422, "分页参数不合法")
    sort_by = options.get("sort_by", "created_at")
    sort_by = FIELDS.get(sort_by, sort_by)
    if sort_by not in {
        "case_code",
        "name",
        "priority",
        "type",
        "status",
        "created_at",
        "updated_at",
        "module_id",
    } or options.get("sort_order", "desc") not in {"asc", "desc"}:
        raise HTTPException(422, "不支持的排序字段或方向")
    conditions, logic = parse_filters(options.get("filters"))
    query = db.query(TestCase).filter(
        TestCase.project_id == project_id, TestCase.deleted_at.is_(None)
    )
    if options.get("case_ids"):
        ids = list(
            dict.fromkeys(
                v.strip() for v in options["case_ids"].split(",") if v.strip()
            )
        )
        if len(ids) > 10000:
            raise HTTPException(422, "选择用例过多")
        query = query.filter(TestCase.id.in_(ids))
        if query.count() != len(ids):
            raise HTTPException(404, "选择中包含不可访问或已删除用例")
    if options.get("mine"):
        query = query.filter(TestCase.created_by == options.get("user_id"))
    if options.get("followed"):
        query = query.filter(
            TestCase.id.in_(
                db.query(CaseFollow.case_id).filter(
                    CaseFollow.user_id == options.get("user_id")
                )
            )
        )
    if options.get("module_ids"):
        ids = [v.strip() for v in options["module_ids"].split(",") if v.strip()]
        criterion = TestCase.module_id.in_(ids)
        if set(ids) & {"null", "unplanned", "__unassigned__"}:
            criterion = or_(criterion, TestCase.module_id.is_(None))
        query = query.filter(criterion)
    elif options.get("module_id"):
        query = query.filter(
            TestCase.module_id.is_(None)
            if options["module_id"] == "null"
            else TestCase.module_id == options["module_id"]
        )
    for field in ["status", "priority", "type", "is_automated"]:
        value = options.get(field)
        if value is not None and value != "":
            query = query.filter(getattr(TestCase, field) == value)
    for field in ["requirement_ref", "precondition"]:
        if options.get(field):
            query = query.filter(
                getattr(TestCase, field).contains(options[field], autoescape=True)
            )
    # JSON 数组及自定义字段在筛选候选集上统一计算，避免 MySQL/SQLite JSON 运算差异。
    cases = query.order_by(
        (
            getattr(TestCase, sort_by).desc()
            if options.get("sort_order", "desc") == "desc"
            else getattr(TestCase, sort_by).asc()
        ),
        TestCase.id,
    ).all()
    if options.get("search"):
        word = options["search"].casefold()
        cases = [
            case
            for case in cases
            if word in case.name.casefold()
            or word in case.case_code.casefold()
            or any(word in str(tag).casefold() for tag in (case.tags or []))
        ]
    if options.get("tags"):
        tags = [v.strip() for v in options["tags"].split(",") if v.strip()]
        cases = [
            case for case in cases if all(tag in (case.tags or []) for tag in tags)
        ]
    statuses = current_review_statuses(db, cases)
    if options.get("review_status"):
        cases = [
            case for case in cases if statuses.get(case.id) == options["review_status"]
        ]
    cases = apply_conditions(cases, conditions, logic, statuses)
    total = len(cases)
    return {
        "items": cases[(page - 1) * size : page * size],
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size,
        "hasNext": page * size < total,
        "hasPrev": page > 1,
        "reviewStatuses": statuses,
    }
