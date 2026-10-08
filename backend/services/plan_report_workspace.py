"""计划及计划组报告目录，筛选和分页在数据库执行，不修改执行批次。"""
from sqlalchemy import select, union_all, literal, func, case, or_, cast, String, DateTime, type_coerce
from models import TestPlan, User
from models.plan_orchestration import PlanRun
from models.plan_group_execution import PlanGroupRun, PlanGroupRunChild
from models.task_schedule import TaskScheduleRun
from models.plan_report_workspace import PlanReportWorkspace, GroupReportWorkspace
from fastapi import HTTPException
from core.logger import logger

TERMINAL = ("completed", "failed", "cancelled", "skipped")


def _branch(model, kind, project_id, dialect_name=None):
    is_plan = kind == "PLAN"
    name = model.plan_name if is_plan else model.group_name
    source_id = model.plan_id if is_plan else model.group_id
    workspace = PlanReportWorkspace if is_plan else GroupReportWorkspace
    trigger_match = TaskScheduleRun.plan_run_id == model.id if is_plan else TaskScheduleRun.group_run_id == model.id
    if is_plan:
        # 组的定时触发也传递给子计划，不能把子批次误标为手动触发。
        parents = select(PlanGroupRunChild.run_id).where(PlanGroupRunChild.plan_run_id == model.id).correlate(model)
        trigger_match = or_(trigger_match, TaskScheduleRun.group_run_id.in_(parents))
    trigger = select(TaskScheduleRun.trigger_type).where(trigger_match).limit(1).correlate(model).scalar_subquery()
    frozen = model.status.in_(TERMINAL)
    created_at=model.created_at
    if not is_plan and dialect_name == "sqlite":
        # SQLite CURRENT_TIMESTAMP stores UTC for group rows. PlanRun is explicitly
        # created with beijing_now(); normalize only this legacy group default.
        raw=cast(model.created_at,String)
        fraction=func.coalesce(func.nullif(func.substr(raw,20),""),".000000")
        created_at=type_coerce(func.strftime("%Y-%m-%d %H:%M:%S",model.created_at,"+8 hours") + fraction,DateTime())
    query = select(
        model.id.label("id"), literal(kind).label("kind"), source_id.label("source_id"),
        name.label("plan_name"), func.coalesce(workspace.name, name + literal(" 报告")).label("name"),
        model.status.label("status"),
        case((frozen, func.coalesce(model.report["outcome"].as_string(), model.status)), else_=model.status).label("result_status"),
        case((frozen, model.report["passRate"].as_float()), else_=None).label("pass_rate"),
        func.coalesce(trigger, "manual").label("trigger_mode"),
        model.executor_id.label("executor_id"), func.coalesce(User.full_name, User.username).label("operator"),
        created_at.label("created_at"), model.completed_at.label("completed_at"),
    ).outerjoin(User, User.id == model.executor_id).outerjoin(workspace, workspace.run_id == model.id).where(or_(workspace.deleted.is_(None), workspace.deleted.is_(False)))
    if is_plan:
        return query.join(TestPlan, TestPlan.id == model.plan_id).where(TestPlan.project_id == project_id)
    return query.where(model.project_id == project_id)


def list_reports(db, project_id, *, page=1, size=20, search=None, plan_name=None, kind=None,
                 result_status=None, trigger_mode=None, operator=None, start_time=None, end_time=None,
                 min_rate=None, max_rate=None, sort="created_at", direction="desc", filters=None, user_id=None):
    dialect=db.get_bind().dialect.name
    rows = union_all(_branch(PlanRun, "PLAN", project_id, dialect), _branch(PlanGroupRun, "GROUP", project_id, dialect)).subquery()
    query = select(rows)
    if filters is not None:
        from services.report_index_filter import apply
        query = apply(query, rows.c, filters, user_id)
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
    # Preserve SQLite/MySQL ordering on PostgreSQL as well: NULL first in ASC,
    # NULL last in DESC, using a portable CASE rather than NULLS LAST syntax.
    null_rank=case((ordering.is_(None),0),else_=1)
    query = query.order_by(null_rank.asc() if direction == "asc" else null_rank.desc(),
                           ordering.asc() if direction == "asc" else ordering.desc(), rows.c.kind, rows.c.id)
    items = []
    for row in db.execute(query.offset((page - 1) * size).limit(size)).mappings():
        items.append(dict(id=row["id"], kind=row["kind"], sourceId=row["source_id"], name=row["name"],
                          planName=row["plan_name"], status=row["status"], resultStatus=row["result_status"],
                          passRate=row["pass_rate"], triggerMode=row["trigger_mode"],
                          executorId=row["executor_id"], createUserName=row["operator"],
                          createTime=row["created_at"], completedAt=row["completed_at"]))
    return dict(items=items, total=total, page=page, size=size)


def report_workspace(kind):
    return PlanReportWorkspace if kind == "PLAN" else GroupReportWorkspace


def ensure_visible(db, kind, run_id):
    row = db.get(report_workspace(kind), run_id)
    if row and row.deleted:
        raise HTTPException(404, "报告已删除")
    return row


def report_name(db, kind, run_id, original):
    # 底层执行历史仍可读取；只有报告入口检查删除标记。
    row = db.get(report_workspace(kind), run_id)
    return row.name if row and row.name else original + " 报告"


def require_report(db, user, project_id, kind, run_id, action="read", include_deleted=False):
    from core.project_access import require_project_access
    require_project_access(db, user, project_id, "test_plan:" + action)
    run = db.get(PlanRun if kind == "PLAN" else PlanGroupRun, run_id)
    actual_project = db.get(TestPlan, run.plan_id).project_id if run and kind == "PLAN" else run.project_id if run else None
    if actual_project != project_id:
        raise HTTPException(404, "此项目中不存在该报告")
    if not include_deleted:
        ensure_visible(db, kind, run_id)
    return run


def rename_report(db, user, project_id, kind, run_id, name):
    require_report(db, user, project_id, kind, run_id, "update")
    clean = name.strip()
    if not clean or len(clean) > 255:
        raise HTTPException(422, "报告名称须为1到255字")
    model = report_workspace(kind)
    row = db.get(model, run_id) or model(run_id=run_id, updated_by=str(user.id))
    row.name, row.updated_by = clean, str(user.id)
    db.add(row)
    try:
        db.commit()
    except Exception:
        db.rollback()
        logger.exception("报告重命名失败：类型={}，批次={}", kind, run_id)
        raise
    logger.info("报告已重命名：项目={}，类型={}，批次={}", project_id, kind, run_id)
    return clean


def delete_reports(db, user, project_id, reports):
    from models.plan_workspace import PlanReportShare
    from models.plan_group_execution import PlanGroupShare
    keys = [(item.kind, item.id) for item in reports]
    if len(set(keys)) != len(keys):
        raise HTTPException(422, "报告列表不能重复")
    # 先授权全部实体，再写入；混入其他项目时整个批量操作均不生效。
    for kind, run_id in keys:
        run = require_report(db, user, project_id, kind, run_id, "delete", include_deleted=True)
        if run.status not in TERMINAL:
            raise HTTPException(409, "请等待执行结束后删除报告")
    try:
        for kind, run_id in keys:
            model = report_workspace(kind)
            row = db.get(model, run_id) or model(run_id=run_id, updated_by=str(user.id))
            row.deleted, row.updated_by = True, str(user.id)
            db.add(row)
            share_model = PlanReportShare if kind == "PLAN" else PlanGroupShare
            db.query(share_model).filter_by(run_id=run_id).update({"revoked": True})
        db.commit()
    except Exception:
        db.rollback()
        logger.exception("删除报告失败：项目={}，报告数={}", project_id, len(keys))
        raise
    logger.info("报告已删除并撤销分享：项目={}，报告数={}，执行快照保留", project_id, len(keys))
    return len(keys)
