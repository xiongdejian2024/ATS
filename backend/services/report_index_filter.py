"""报告首页有限字段的参数化 SQL 条件；计数和分页共享同一查询。"""
import json
import math
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import and_, or_, cast, String, DateTime, case, func
from utils.datetime_utils import BEIJING_TZ

TEXT = {"id", "name", "planName", "operator"}
SELECT = {"kind", "resultStatus", "triggerMode", "executorId"}
NUMBER = {"passRate"}
DATE = {"createTime", "completedAt"}
FIELDS = TEXT | SELECT | NUMBER | DATE
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
    return parsed.astimezone(BEIJING_TZ).replace(tzinfo=None) if parsed.tzinfo else parsed


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
                raise ValueError("不支持的报告字段或运算符")
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
            enums = {"kind": {"PLAN", "GROUP"}, "triggerMode": {"manual", "cron"},
                "resultStatus": {"passed", "failed", "completed", "cancelled", "queued", "running", "cancelling", "needs_confirmation", "group_waiting", "skipped"}}
            if field in enums and any(v not in enums[field] for v in values):
                raise ValueError("不支持的报告枚举值")
            if field == "passRate" and any(v < 0 or v > 100 for v in values):
                raise ValueError("通过率必须为0到100")
            if operator not in COLLECTION | {"between", "contains", "not_contains"} and isinstance(value, list):
                raise ValueError("此运算符只接受单值")
            if kind(field) == "number" and operator == "between" and value[0] > value[1]:
                raise ValueError("筛选开始数值大于结束数值")
            active.append(row)
        return active, logic
    except (ValueError, TypeError, OverflowError) as exc:
        raise HTTPException(422, "报告筛选条件不合法") from exc


def json_member(column, value):
    # JSON 的精确字符串 token；兼容历史 ensure_ascii 编码，转义 SQL 通配符。
    return or_(*(cast(column, String).contains(json.dumps(value, ensure_ascii=ascii), autoescape=True) for ascii in (False, True)))




def apply(query, columns, raw, user_id):
    rows, logic = parse(raw)
    mapping = dict(id=columns.id, name=columns.name, planName=columns.plan_name,
        operator=columns.operator, kind=columns.kind, resultStatus=columns.result_status,
        triggerMode=columns.trigger_mode, executorId=columns.executor_id,
        passRate=columns.pass_rate, createTime=columns.created_at, completedAt=columns.completed_at)
    predicates=[]
    for row in rows:
        field, op, value=row["field"],row["operator"],row.get("value")
        values=value if isinstance(value,list) else [value]
        if field == "executorId":
            values=[str(user_id) if v == "CURRENT_USER" else v for v in values]
            value=values if isinstance(value,list) else values[0]
        col=mapping[field]
        empty=or_(col.is_(None),col == "") if field in TEXT else col.is_(None)
        if op in EMPTY: pred=empty if op == "is_empty" else ~empty
        elif op in COLLECTION:
            positive=col.in_(values)
            pred=~func.coalesce(positive,False) if op.startswith("not_") else positive
        elif op in {"contains", "not_contains"}:
            positive=or_(*(func.lower(col).contains(v.lower(),autoescape=True) for v in values))
            pred=~func.coalesce(positive,False) if op == "not_contains" else positive
        else:
            if field in DATE:value=[date_value(v,field) for v in values] if op == "between" else date_value(value,field)
            pred=col.between(*value) if op == "between" else {
                "equals":lambda:col == value,"not_equals":lambda:~func.coalesce(col == value,False),
                "gt":lambda:col > value,"gte":lambda:col >= value,"lt":lambda:col < value,"lte":lambda:col <= value}[op]()
        predicates.append(pred)
    return query.where((and_ if logic == "and" else or_)(*predicates)) if predicates else query
