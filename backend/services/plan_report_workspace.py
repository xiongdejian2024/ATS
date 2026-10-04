"""计划及计划组报告目录，筛选和分页在数据库执行，不修改执行批次。"""
from sqlalchemy import select, union_all, literal, func, case, or_
from models import TestPlan, User
from models.plan_orchestration import PlanRun
from models.plan_group_execution import PlanGroupRun, PlanGroupRunChild
from models.task_schedule import TaskScheduleRun

TERMINAL = ("completed", "failed", "cancelled", "skipped")


def _branch(model, kind, project_id):
    is_plan = kind == "PLAN"
    name = model.plan_name if is_plan else model.group_name
    source_id = model.plan_id if is_plan else model.group_id
    trigger_match = TaskScheduleRun.plan_run_id == model.id if is_plan else TaskScheduleRun.group_run_id == model.id
    if is_plan:
        # 组的定时触发也传递给子计划，不能把子批次误标为手动触发。
        parents = select(PlanGroupRunChild.run_id).where(PlanGroupRunChild.plan_run_id == model.id).correlate(model)
        trigger_match = or_(trigger_match, TaskScheduleRun.group_run_id.in_(parents))
    trigger = select(TaskScheduleRun.trigger_type).where(trigger_match).limit(1).correlate(model).scalar_subquery()
    frozen = model.status.in_(TERMINAL)
    query = select(
        model.id.label("id"), literal(kind).label("kind"), source_id.label("source_id"),
        name.label("plan_name"), (name + literal(" 报告")).label("name"),
        model.status.label("status"),
        case((frozen, func.coalesce(model.report["outcome"].as_string(), model.status)), else_=model.status).label("result_status"),
        case((frozen, model.report["passRate"].as_float()), else_=None).label("pass_rate"),
        func.coalesce(trigger, "manual").label("trigger_mode"),
        model.executor_id.label("executor_id"), func.coalesce(User.full_name, User.username).label("operator"),
        model.created_at.label("created_at"), model.completed_at.label("completed_at"),
    ).outerjoin(User, User.id == model.executor_id)
    if is_plan:
        return query.join(TestPlan, TestPlan.id == model.plan_id).where(TestPlan.project_id == project_id)
    return query.where(model.project_id == project_id)


def list_reports(db, project_id, *, page=1, size=20, search=None, plan_name=None, kind=None,
                 result_status=None, trigger_mode=None, operator=None, start_time=None, end_time=None,
                 min_rate=None, max_rate=None, sort="created_at", direction="desc"):
    rows = union_all(_branch(PlanRun, "PLAN", project_id), _branch(PlanGroupRun, "GROUP", project_id)).subquery()
    query = select(rows)
    for value, column in ((search, rows.c.name), (plan_name, rows.c.plan_name), (operator, rows.c.operator)):
        if value and value.strip():
            query = query.where(column.contains(value.strip(), autoescape=True))
    for value, column in ((kind, rows.c.kind), (result_status, rows.c.result_status), (trigger_mode, rows.c.trigger_mode)):
        if value:
            query = query.where(column == value)
    for value, column, lower in ((start_time, rows.c.created_at, True), (end_time, rows.c.created_at, False),
                                 (min_rate, rows.c.pass_rate, True), (max_rate, rows.c.pass_rate, False)):
        if value is not None:
            query = query.where(column >= value if lower else column <= value)
    total = db.scalar(select(func.count()).select_from(query.subquery()))
    ordering = {"created_at": rows.c.created_at, "pass_rate": rows.c.pass_rate,
                "result_status": rows.c.result_status, "name": rows.c.name}[sort]
    query = query.order_by(ordering.asc() if direction == "asc" else ordering.desc(), rows.c.kind, rows.c.id)
    items = []
    for row in db.execute(query.offset((page - 1) * size).limit(size)).mappings():
        items.append(dict(id=row["id"], kind=row["kind"], sourceId=row["source_id"], name=row["name"],
                          planName=row["plan_name"], status=row["status"], resultStatus=row["result_status"],
                          passRate=row["pass_rate"], triggerMode=row["trigger_mode"],
                          executorId=row["executor_id"], createUserName=row["operator"],
                          createTime=row["created_at"], completedAt=row["completed_at"]))
    return dict(items=items, total=total, page=page, size=size)
