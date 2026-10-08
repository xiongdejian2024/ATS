"""计划首页有限字段的参数化 SQL 条件；计数和分页共享同一查询。"""
import json
import math
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import and_, or_, cast, String, DateTime, case, func
from models.test_plan import TestPlan, PlanCaseRelation
from models.plan_workspace import PlanWorkspace, PlanGroupWorkspace, PlanFollow
from models.plan_orchestration import PlanSettings
from utils.datetime_utils import BEIJING_TZ

TEXT = {"id", "name", "description", "planNumber"}
SELECT = {"status", "planType", "moduleId", "groupId", "ownerId", "archived", "followed"}
NUMBER = set()
DATE = {"createdAt", "updatedAt", "startDate", "endDate"}
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
    if field in {"startDate", "endDate"}:
        if parsed.tzinfo:
            parsed = parsed.astimezone(BEIJING_TZ)
        return parsed.date()
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
                raise ValueError("不支持的计划字段或运算符")
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
            enums = {"status": {"not_started", "running", "completed", "paused", "overdue"},
                     "planType": {"manual", "automated", "mixed", "functional"},
                     "archived": {"true", "false"}, "followed": {"true", "false"}}
            if field in enums and any(v not in enums[field] for v in values):
                raise ValueError("不支持的计划枚举值")
            if operator not in COLLECTION | {"between", "contains", "not_contains"} and isinstance(value, list):
                raise ValueError("此运算符只接受单值")
            if kind(field) == "number" and operator == "between" and value[0] > value[1]:
                raise ValueError("筛选开始数值大于结束数值")
            active.append(row)
        return active, logic
    except (ValueError, TypeError, OverflowError) as exc:
        raise HTTPException(422, "计划筛选条件不合法") from exc


def json_member(column, value):
    # JSON 的精确字符串 token；兼容历史 ensure_ascii 编码，转义 SQL 通配符。
    return or_(*(cast(column, String).contains(json.dumps(value, ensure_ascii=ascii), autoescape=True) for ascii in (False, True)))



def effective_status(db):
    """与旧逾期规则一致的只读投影，筛选、计数和响应使用同一状态。"""
    from datetime import date
    pending = db.query(PlanCaseRelation.id).filter(
        PlanCaseRelation.plan_id == TestPlan.id,
        PlanCaseRelation.execution_status == "pending").exists()
    return case((and_(TestPlan.end_date < date.today(),
                      TestPlan.status.not_in(["completed", "overdue"]), pending), "overdue"),
                else_=TestPlan.status)


def apply(db, query, rows, logic, user_id):
    # 相关标量子查询避免增添重复 JOIN，分组成员的模块取实际组位置。
    group_id = db.query(PlanSettings.group_id).filter(PlanSettings.plan_id == TestPlan.id).correlate(TestPlan).scalar_subquery()
    group_module = db.query(PlanGroupWorkspace.module_id).filter(PlanGroupWorkspace.group_id == group_id).correlate(TestPlan).scalar_subquery()
    module_id = case((group_id.is_not(None), group_module), else_=PlanWorkspace.module_id)
    followed = db.query(PlanFollow.id).filter(PlanFollow.plan_id == TestPlan.id,
                                             PlanFollow.user_id == str(user_id)).exists()
    columns = dict(id=TestPlan.id, name=TestPlan.name, description=TestPlan.description,
        planNumber=TestPlan.plan_number, status=effective_status(db), planType=TestPlan.plan_type,
        ownerId=TestPlan.owner_id, moduleId=module_id, groupId=group_id,
        archived=func.coalesce(PlanWorkspace.archived, False), followed=followed,
        startDate=TestPlan.start_date, endDate=TestPlan.end_date,
        createdAt=TestPlan.created_at, updatedAt=TestPlan.updated_at)
    predicates=[]
    for row in rows:
        field, op, value = row["field"], row["operator"], row.get("value")
        values = value if isinstance(value, list) else [value]
        if field == "ownerId": values = [str(user_id) if v == "CURRENT_USER" else v for v in values]
        if field in {"moduleId", "groupId"}: values = [None if v in {"default", "__ungrouped__", "__unassigned__"} else v for v in values]
        if field in {"archived", "followed"}: values = [v == "true" for v in values]
        value = values if isinstance(value, list) else values[0]
        if field == "tags":
            col = PlanWorkspace.tags
            empty = or_(col.is_(None), cast(col, String).in_(["[]", "null"]))
            if op in EMPTY: pred = empty if op == "is_empty" else ~empty
            elif op.startswith("count_"):
                length = func.json_length(col) if db.get_bind().dialect.name == "mysql" else func.json_array_length(col)
                length = case((empty, 0), else_=length)
                pred = length > value if op == "count_gt" else length < value
            else:
                positive=or_(*(json_member(col,v) for v in values))
                pred=~func.coalesce(positive,False) if op == "not_contains" else positive
        else:
            col=columns[field]
            empty=or_(col.is_(None),col == "") if field in TEXT else col.is_(None)
            if op in EMPTY: pred=empty if op == "is_empty" else ~empty
            elif op in COLLECTION:
                positive=or_(col.in_([v for v in values if v is not None]), col.is_(None) if None in values else False)
                pred=~func.coalesce(positive,False) if op.startswith("not_") else positive
            elif op in {"contains", "not_contains"}:
                positive=or_(*(func.lower(col).contains(v.lower(),autoescape=True) for v in values))
                pred=~func.coalesce(positive,False) if op == "not_contains" else positive
            else:
                if field in DATE: value=[date_value(v,field) for v in values] if op == "between" else date_value(value,field)
                pred=col.between(*value) if op == "between" else {
                    "equals":lambda:col == value, "not_equals":lambda:~func.coalesce(col == value,False),
                    "gt":lambda:col > value,"gte":lambda:col >= value,"lt":lambda:col < value,"lte":lambda:col <= value}[op]()
        predicates.append(pred)
    return query.filter((and_ if logic == "and" else or_)(*predicates)) if predicates else query
