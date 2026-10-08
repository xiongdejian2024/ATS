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
    "updatedBy": "updated_by",
    "templateId": "template_id",
    "createdAt": "created_at",
    "updatedAt": "updated_at",
    "deletedAt": "deleted_at",
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
    "between",
    "count_gt",
    "count_lt",
}


def parse_filters(raw, *, extra_fields=()):
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
            and field not in extra_fields
            and field not in {"reviewResult", "review_status", "attachment"}
            and not field.startswith("customFields.")
        ):
            raise HTTPException(422, "不支持的筛选字段")
        if (
            item["operator"]
            in {
                "in",
                "not_in",
                "belongs_to",
                "not_belongs_to",
            }
            and item.get("value") is not None
            and not isinstance(item.get("value"), (list, str))
        ):
            raise HTTPException(422, "筛选集合必须为字符串或数组")
        if item["operator"] == "between" and item.get("value") not in (None, [], ""):
            value = item["value"]
            if (
                not isinstance(value, list)
                or len(value) != 2
                or any(v is None or v == "" for v in value)
            ):
                raise HTTPException(422, "介于条件必须包含两个完整边界")
            from services.filter_values import comparable, temporal

            try:
                if field in {"createdAt", "updatedAt", "deletedAt"}:
                    lower, upper = temporal(value[0]), temporal(value[1])
                else:
                    lower, upper = comparable(value[0], value[1], date_text=True)
                if lower > upper:
                    raise HTTPException(422, "筛选起始边界不能晚于结束边界")
            except (ValueError, TypeError, OverflowError, OSError) as exc:
                raise HTTPException(422, "筛选区间边界不是有效值或类型不一致") from exc
        if item["operator"] in {"count_gt", "count_lt"}:
            value = item.get("value")
            if value is not None and (type(value) is not int or value < 0):
                raise HTTPException(422, "数量条件必须为非负整数")
    # 官方默认条件可以没有值；它们不参与 AND/OR，不将空包含当作全匹配。
    return [
        c
        for c in conditions
        if c["operator"] in {"is_empty", "is_not_empty"}
        or c.get("value") not in (None, "", [])
    ], logic


def matches(actual, operator, expected):
    empty = actual is None or actual == "" or actual == []
    if operator == "is_empty":
        return empty
    if operator == "is_not_empty":
        return not empty
    if operator in {"count_gt", "count_lt"}:
        if actual is not None and not isinstance(actual, list):
            raise HTTPException(422, "数量比较只适用于数组字段")
        size = len(actual or [])
        return size > expected if operator == "count_gt" else size < expected
    if operator == "between":
        from services.filter_values import comparable

        lower_actual, lower = comparable(actual, expected[0], date_text=True)
        upper_actual, upper = comparable(actual, expected[1], date_text=True)
        if actual is None:
            return False
        try:
            if lower > upper:
                raise HTTPException(422, "筛选起始边界不能晚于结束边界")
            return lower_actual >= lower and upper_actual <= upper
        except TypeError as exc:
            raise HTTPException(422, "筛选字段与区间边界类型不一致") from exc
    if (
        isinstance(actual, bool)
        and isinstance(expected, str)
        and expected in {"true", "false"}
    ):
        expected = expected == "true"
    if operator in {"equals", "not_equals", "gt", "gte", "lt", "lte"}:
        from services.filter_values import comparable

        actual, expected = comparable(actual, expected)
    if operator == "equals":
        return actual == expected
    if operator == "not_equals":
        return actual != expected
    if operator in {"contains", "not_contains"}:
        if isinstance(actual, list):
            result = any(
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


def matches_related(values, operator, expected):
    if operator in {"is_empty", "is_not_empty"}:
        return not values if operator == "is_empty" else bool(values)
    positive = {
        "not_contains": "contains",
        "not_equals": "equals",
        "not_in": "in",
        "not_belongs_to": "belongs_to",
    }.get(operator, operator)
    found = any(matches(value, positive, expected) for value in values)
    return not found if positive != operator else found


def matches_case(case, condition, review_statuses, context):
    field = condition["field"]
    expected = condition.get("value")
    if field == "attachment":
        return matches_related(
            context.attachments.get(case.id, []), condition["operator"], expected
        )
    if field == "requirementRef":
        values = context.requirements.get(case.id, []) + (
            [case.requirement_ref] if case.requirement_ref else []
        )
        return matches_related(values, condition["operator"], expected)
    if field in {"reviewResult", "review_status"}:
        value = review_statuses.get(case.id, "not_reviewed")
    elif field.startswith("customFields."):
        value, expected = context.custom_value(case, condition)
    else:
        value = getattr(case, FIELDS[field])
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


def apply_conditions(cases, conditions, logic, review_statuses, context):
    combine = all if logic == "and" else any
    return [
        case
        for case in cases
        if not conditions or combine(matches_case(case, c, review_statuses, context) for c in conditions)
    ]


def query_cases(db, project_id, **options):
    from models.test_case import TestCase
    from models.case_features import CaseFollow
    from services.case_governance import current_review_statuses
    from sqlalchemy import or_

    page, size = options.get("page", 1), options.get("size", 20)
    recycled = bool(options.get("recycled", False))
    if page < 1 or not 1 <= size <= 100000:
        raise HTTPException(422, "分页参数不合法")
    sort_by = options.get("sort_by", "created_at")
    sort_by = FIELDS.get(sort_by, sort_by)
    sortable = {
        "case_code",
        "name",
        "priority",
        "type",
        "status",
        "created_at",
        "updated_at",
        "module_id",
    }
    if recycled:
        sortable.add("deleted_at")
    if sort_by not in sortable or options.get("sort_order", "desc") not in {"asc", "desc"}:
        raise HTTPException(422, "不支持的排序字段或方向")
    conditions, logic = parse_filters(options.get("filters"))
    from services.case_filter_context import CaseFilterContext

    current_read = bool(options.get("current_read"))
    context = CaseFilterContext(db, project_id, conditions, options.get("user_id"), current_read=current_read, include_recycled=recycled)
    conditions = context.conditions
    query = db.query(TestCase).filter(
        TestCase.project_id == project_id,
        TestCase.deleted_at.is_not(None) if recycled else TestCase.deleted_at.is_(None),
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
        follows = db.query(CaseFollow.case_id).filter(
            CaseFollow.user_id == options.get("user_id")
        )
        if current_read:
            # 外层锁定读不会使嵌套查询自动成为当前读，单独读取关注关系。
            follows = [row[0] for row in follows.with_for_update().all()]
        query = query.filter(TestCase.id.in_(follows))
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
    if current_read:
        query = query.populate_existing().with_for_update()
    ordered = query.order_by(
        (
            getattr(TestCase, sort_by).desc()
            if options.get("sort_order", "desc") == "desc"
            else getattr(TestCase, sort_by).asc()
        ),
        TestCase.id,
    )
    # 回收站默认列表保留数据库计数和分页，不因复用高级筛选而加载整个历史库。
    if recycled and not conditions and not any(options.get(key) for key in ('search', 'tags', 'review_status')):
        total = query.count()
        cases = ordered.offset((page - 1) * size).limit(size).all()
        return {
            'items': cases, 'total': total, 'page': page, 'size': size,
            'pages': (total + size - 1) // size, 'hasNext': page * size < total,
            'hasPrev': page > 1,
            'reviewStatuses': {},
        }
    cases = ordered.all()
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
    statuses = current_review_statuses(db, cases, current_read=current_read)
    if options.get("review_status"):
        cases = [
            case for case in cases if statuses.get(case.id) == options["review_status"]
        ]
    cases = apply_conditions(cases, conditions, logic, statuses, context)
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
