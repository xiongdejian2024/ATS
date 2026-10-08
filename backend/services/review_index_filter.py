"""评审首页有限字段的参数化 SQL 条件；计数和分页共享同一查询。"""
import json
import math
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import and_, or_, cast, String, DateTime, case, func
from models.case_governance import CaseReview, CaseReviewItem
from models.review_workspace import ReviewWorkspace
from utils.datetime_utils import BEIJING_TZ

TEXT = {"id", "name", "description"}
SELECT = {"lifecycle", "mode", "moduleId", "createdBy", "reviewerId"}
NUMBER = {"number", "caseCount", "passRate"}
DATE = {"createdAt", "startTime", "endTime"}
FIELDS = TEXT | SELECT | NUMBER | DATE | {"tags"}
EMPTY = {"is_empty", "is_not_empty"}
COLLECTION = {"belongs_to", "not_belongs_to", "in", "not_in"}
OPERATORS = {
    "text": EMPTY | {"contains", "not_contains", "equals", "not_equals"},
    "select": EMPTY | COLLECTION | {"equals", "not_equals"},
    "number": EMPTY | {"equals", "not_equals", "gt", "gte", "lt", "lte", "between"},
    "date": EMPTY | {"between", "gt", "gte", "lt", "lte"},
    "tags": EMPTY | {"contains", "not_contains", "count_gt", "count_lt"},
}


def kind(field):
    return "text" if field in TEXT else "select" if field in SELECT else "number" if field in NUMBER else "date" if field in DATE else "tags"


def date_value(value, field):
    if not isinstance(value, str) or len(value) > 50:
        raise ValueError("日期必须为ISO文本")
    parsed = datetime.fromisoformat(value)
    # 精确评审周期按既有 API 约定存储北京时间；创建时间由数据库生成。
    if field != "createdAt":
        return parsed.astimezone(BEIJING_TZ).replace(tzinfo=None) if parsed.tzinfo else parsed
    from datetime import timezone
    return parsed.astimezone(timezone.utc) if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def parse(raw):
    if raw is None:
        return [], "and"
    try:
        if isinstance(raw, str):
            if len(raw) > 20000:
                raise ValueError("筛选条件过大")
            raw = json.loads(raw)
        if not isinstance(raw, dict) or set(raw) - {"conditions", "logic"}:
            raise ValueError("筛选结构不合法")
        rows, logic = raw.get("conditions", []), raw.get("logic", "and")
        if logic not in {"and", "or"} or not isinstance(rows, list) or len(rows) > 100:
            raise ValueError("筛选逻辑或数量不合法")
        active = []
        for row in rows:
            if not isinstance(row, dict) or set(row) - {"field", "operator", "value"}:
                raise ValueError("条件结构不合法")
            field, operator = row.get("field"), row.get("operator")
            if field not in FIELDS or operator not in OPERATORS[kind(field)]:
                raise ValueError("不支持的评审字段或运算符")
            value = row.get("value")
            if operator in EMPTY:
                active.append(row); continue
            if value is None or value == "" or value == []:
                continue
            values = value if isinstance(value, list) else [value]
            if len(values) > 100 or (operator == "between" and len(values) != 2):
                raise ValueError("筛选集合或区间不合法")
            if kind(field) == "number" or operator.startswith("count_"):
                if any(type(v) not in {int, float} or not math.isfinite(v) or abs(v) > 9007199254740991 for v in values):
                    raise ValueError("数量必须为有限数值")
                if operator.startswith("count_") and (type(value) is not int or value < 0):
                    raise ValueError("数量必须为非负整数")
            elif kind(field) == "date":
                converted = [date_value(v, field) for v in values]
                if operator == "between" and converted[0] > converted[1]:
                    raise ValueError("筛选开始时间晚于结束时间")
            elif any(not isinstance(v, str) or len(v) > 255 for v in values):
                raise ValueError("筛选值必须为有界文本")
            if field == "lifecycle" and any(v not in {"prepared", "underway", "completed", "archived", "cancelled", "superseded"} for v in values):
                raise ValueError("不支持的评审状态")
            if field == "mode" and any(v not in {"single", "multiple"} for v in values):
                raise ValueError("不支持的评审模式")
            if operator not in COLLECTION | {"between", "contains", "not_contains"} and isinstance(value, list):
                raise ValueError("此运算符只接受单值")
            if kind(field) == "number" and operator == "between" and value[0] > value[1]:
                raise ValueError("筛选开始数值大于结束数值")
            active.append(row)
        return active, logic
    except (ValueError, TypeError, OverflowError) as exc:
        raise HTTPException(422, "评审筛选条件不合法") from exc


def json_member(column, value):
    # JSON 的精确字符串 token；兼容历史 ensure_ascii 编码，转义 SQL 通配符。
    return or_(*(cast(column, String).contains(json.dumps(value, ensure_ascii=ascii), autoescape=True) for ascii in (False, True)))


def apply(db, query, state, rate, raw, user_id):
    rows, logic = parse(raw)
    total = query.column_descriptions[2]["expr"]
    def legacy_period(column):
        return func.strftime("%Y-%m-%d %H:%M:%S.000000", column) if db.get_bind().dialect.name == "sqlite" else cast(column, DateTime)
    start = func.coalesce(ReviewWorkspace.start_time, legacy_period(CaseReview.start_date))
    end = func.coalesce(ReviewWorkspace.end_time, legacy_period(CaseReview.end_date))
    columns = dict(id=CaseReview.id, name=CaseReview.name, description=CaseReview.description,
                   number=ReviewWorkspace.number, lifecycle=state, mode=CaseReview.mode,
                   moduleId=ReviewWorkspace.module_id, createdBy=CaseReview.created_by,
                   createdAt=CaseReview.created_at, startTime=start, endTime=end,
                   passRate=func.coalesce(rate, 0), caseCount=total)
    predicates = []
    for row in rows:
        field, operator, value = row["field"], row["operator"], row.get("value")
        values = value if isinstance(value, list) else [value]
        if field in {"createdBy", "reviewerId"}:
            values = [user_id if v == "CURRENT_USER" else v for v in values]
            value = values if isinstance(value, list) else values[0]
        if field == "moduleId":
            values = [None if v in {"default", "__unassigned__"} else v for v in values]
            value = values if isinstance(value, list) else values[0]
        if field == "reviewerId":
            positive = or_(*(or_(json_member(CaseReview.reviewer_ids, v), db.query(CaseReviewItem.id).filter(
                CaseReviewItem.review_id == CaseReview.id, json_member(CaseReviewItem.reviewer_ids, v)).exists()) for v in values))
            if operator in EMPTY:
                positive = or_(cast(CaseReview.reviewer_ids, String).not_in(["[]", "null"]), db.query(CaseReviewItem.id).filter(
                    CaseReviewItem.review_id == CaseReview.id, cast(CaseReviewItem.reviewer_ids, String).not_in(["[]", "null"])).exists())
                predicates.append(~positive if operator == "is_empty" else positive)
            else:
                predicates.append(~positive if operator in {"not_equals", "not_in", "not_belongs_to"} else positive)
            continue
        if field == "tags":
            column = ReviewWorkspace.tags
            empty = or_(column.is_(None), cast(column, String).in_(["[]", "null"]))
            if operator in EMPTY:
                predicate = empty if operator == "is_empty" else ~empty
            elif operator.startswith("count_"):
                length = func.json_length(column) if db.get_bind().dialect.name == "mysql" else func.json_array_length(column)
                length = case((empty, 0), else_=length)
                predicate = length > value if operator == "count_gt" else length < value
            else:
                positive = or_(*(json_member(column, v) for v in values))
                predicate = ~func.coalesce(positive, False) if operator == "not_contains" else positive
            predicates.append(predicate); continue
        column = columns[field]
        empty = or_(column.is_(None), column == "") if field in TEXT else column.is_(None)
        if operator in EMPTY:
            predicate = empty if operator == "is_empty" else ~empty
        elif operator in COLLECTION:
            positive = or_(column.in_([v for v in values if v is not None]), column.is_(None) if None in values else False)
            predicate = ~func.coalesce(positive, False) if operator.startswith("not_") else positive
        elif operator in {"contains", "not_contains"}:
            positive = or_(*(func.lower(column).contains(v.lower(), autoescape=True) for v in values))
            predicate = ~func.coalesce(positive, False) if operator == "not_contains" else positive
        else:
            if field in DATE:
                value = [date_value(v, field) for v in values] if operator == "between" else date_value(value, field)
            predicate = column.between(*value) if operator == "between" else {
                "equals": lambda: column == value, "not_equals": lambda: ~func.coalesce(column == value, False),
                "gt": lambda: column > value, "gte": lambda: column >= value,
                "lt": lambda: column < value, "lte": lambda: column <= value,
            }[operator]()
        predicates.append(predicate)
    return query.filter((and_ if logic == "and" else or_)(*predicates)) if predicates else query
