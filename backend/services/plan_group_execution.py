"""计划组按固定成员批次执行；复用计划编排，不绕过节点容量或交付确认。"""
from copy import deepcopy
from uuid import uuid4

from fastapi import HTTPException

from core.logger import logger
from core.project_access import require_project_access
from models import User, TestPlan
from models.plan_orchestration import PlanGroup, PlanSettings, PlanRun, PlanRunItem
from models.plan_group_execution import PlanGroupPolicy, PlanGroupRun, PlanGroupRunChild
from utils.datetime_utils import beijing_now

TERMINAL = {"completed", "failed", "cancelled", "skipped"}


def find_group(db, user, group_id, action="read"):
    group = db.get(PlanGroup, group_id)
    if not group:
        raise HTTPException(404, "计划组不存在")
    require_project_access(db, user, group.project_id, "test_plan:" + action)
    return group


def get_policy(db, group_id):
    policy = db.get(PlanGroupPolicy, group_id)
    return dict(executionMode=policy.execution_mode if policy else "serial",
                stopOnFailure=policy.stop_on_failure if policy else False,
                passThreshold=policy.pass_threshold if policy else 100,
                planOrder=policy.plan_order if policy else [])


def children(db, run):
    return [db.get(PlanRun, row.plan_run_id) for row in db.query(PlanGroupRunChild)
            .filter_by(run_id=run.id).order_by(PlanGroupRunChild.sequence).all()]


def child_data(db, child):
    from services.plan_orchestration import build_report
    return dict(id=child.id, planId=child.plan_id, planName=child.plan_name, status=child.status,
                startedAt=child.started_at.isoformat() if child.started_at else None,
                completedAt=child.completed_at.isoformat() if child.completed_at else None,
                report=child.report if child.status in TERMINAL and child.report else build_report(db, child))


def aggregate(db, run):
    details = [child_data(db, child) for child in children(db, run)]
    rows = [dict(case, planName=child["planName"], planRunId=child["id"])
            for child in details for case in child["report"]["cases"]]
    counts = {state: sum(row["result"] == state for row in rows)
              for state in ("passed", "failed", "error", "blocked", "skipped", "cancelled", "pending")}
    bugs = list({defect["id"]: defect for row in rows for step in row.get("stepResults", [])
                 for defect in step.get("defects", [])}.values())
    rate = round(100 * counts["passed"] / len(rows), 2) if rows else 0
    settled = bool(details) and all(child["status"] in TERMINAL for child in details)
    outcome = "cancelled" if run.status in ("cancelled", "cancelling") else (
        "running" if not settled else "passed" if rows and rate >= run.config_snapshot["passThreshold"] else "failed")
    return dict(total=len(rows), counts=counts, passRate=rate, passThreshold=run.config_snapshot["passThreshold"],
                outcome=outcome, cases=rows, plans=details, bugs=bugs)


def run_data(db, run):
    from services.plan_report_workspace import report_name
    report = run.report if run.status in TERMINAL and run.report else aggregate(db, run)
    return dict(id=run.id, groupId=run.group_id, groupName=run.group_name, projectId=run.project_id,
                status=run.status, startedAt=run.created_at.isoformat() if run.created_at else None,
                completedAt=run.completed_at.isoformat() if run.completed_at else None,
                configSnapshot=run.config_snapshot, summary=run.summary or {}, report=report,
                children=report.get("plans", []), reportName=report_name(db, "GROUP", run.id, run.group_name))


async def start_group_run(db, group_id, user_id, idempotency_key=None, commit=True):
    from services.plan_orchestration import start_plan_run
    user = db.get(User, str(user_id))
    group = find_group(db, user, group_id, "execute")
    from models.plan_workspace import PlanGroupWorkspace
    workspace = db.get(PlanGroupWorkspace, group_id)
    if workspace and workspace.archived:
        raise HTTPException(400, "归档计划组不能执行，请先取消归档")
    if idempotency_key:
        old = db.query(PlanGroupRun).filter_by(idempotency_key=idempotency_key).first()
        if old:
            if old.group_id != group_id or old.executor_id != str(user_id):
                raise HTTPException(409, "请求编号已用于其他计划组或执行人")
            return old
    if db.query(PlanGroupRun).filter_by(active_group_id=group_id).first():
        raise HTTPException(409, "计划组已有活动批次")
    members = db.query(TestPlan).join(PlanSettings, PlanSettings.plan_id == TestPlan.id).filter(
        PlanSettings.group_id == group_id, TestPlan.project_id == group.project_id).order_by(TestPlan.created_at, TestPlan.id).all()
    if not members:
        raise HTTPException(400, "请先将测试计划加入计划组")
    policy = get_policy(db, group_id)
    ordering = {pid: index for index, pid in enumerate(policy["planOrder"])}
    members.sort(key=lambda plan: ordering.get(plan.id, len(ordering)))
    run = PlanGroupRun(id=str(uuid4()), group_id=group.id, active_group_id=group.id,
                       project_id=group.project_id, group_name=group.name, executor_id=str(user_id),
                       idempotency_key=idempotency_key, status="queued", config_snapshot=deepcopy(policy))
    db.add(run)
    db.flush()  # 活动组唯一约束先占位，任何子计划错误由调用事务整体回滚。
    for index, plan in enumerate(members):
        child = await start_plan_run(db, plan.id, str(user_id), idempotency_key=f"group:{run.id}:{plan.id}", commit=False, defer=True)
        db.add(PlanGroupRunChild(run_id=run.id, plan_run_id=child.id, sequence=index))
    db.flush()
    if commit:
        db.commit()
    logger.info("计划组批次已创建并冻结全部成员：计划组={}，批次={}，成员={}", group_id, run.id, len(members))
    return run


async def cancel_group_run(db, run, user):
    from services.plan_orchestration import cancel_plan_run
    require_project_access(db, user, run.project_id, "test_plan:execute")
    if run.status in TERMINAL:
        return run
    run.status = "cancelling"
    db.commit()  # 先持久化组取消意图，后续即使中断也不会释放等待的成员。
    for child in children(db, run):
        if child.status not in TERMINAL:
            await cancel_plan_run(db, child.id, user_id=str(user.id))
    await advance_group_runs(db)
    return run


async def advance_group_runs(db):
    from services.plan_orchestration import release_plan_run, cancel_plan_run, build_report
    identifiers = [row.id for row in db.query(PlanGroupRun).filter(PlanGroupRun.status.notin_(TERMINAL)).all()]
    for identifier in identifiers:
        run = db.query(PlanGroupRun).filter_by(id=identifier).with_for_update().populate_existing().one()
        records = children(db, run)
        if run.status == "cancelling":
            for child in records:
                if child.status not in TERMINAL:
                    await cancel_plan_run(db, child.id)
        else:
            failed = any(child.status == "failed" for child in records)
            waiting = [child for child in records if child.status == "group_waiting"]
            if failed and run.config_snapshot["stopOnFailure"]:
                for child in waiting:
                    await cancel_plan_run(db, child.id)
            else:
                active = any(child.status not in TERMINAL | {"group_waiting"} for child in records)
                release = waiting if run.config_snapshot["executionMode"] == "parallel" else waiting[:1] if not active else []
                for child in release:
                    owner = db.get(User, run.executor_id)
                    if not owner or not owner.status:
                        await cancel_plan_run(db, child.id)
                        child.status = "failed"
                        child.notes = "执行人已被停用，计划组停止派发"
                        child.report = build_report(db, child)
                        continue
                    try:
                        require_project_access(db, owner, run.project_id, "test_plan:execute")
                    except HTTPException:
                        logger.exception("计划组执行人权限已失效：批次={}", run.id)
                        await cancel_plan_run(db, child.id)
                        child.status = "failed"
                        child.notes = "执行权限已失效，计划组停止派发"
                        child.report = build_report(db, child)
                        continue
                    release_plan_run(db, child)
                    logger.info("计划组已释放成员执行：批次={}，计划批次={}", run.id, child.id)
        db.flush()
        records = children(db, run)
        if all(child.status in TERMINAL for child in records):
            run.report = aggregate(db, run)
            run.status = "cancelled" if run.status == "cancelling" else "completed" if run.report["outcome"] == "passed" else "failed"
            run.active_group_id = None
            run.completed_at = beijing_now()
        elif run.status != "cancelling":
            run.status = "needs_confirmation" if any(child.status == "needs_confirmation" for child in records) else "running"
        db.commit()
