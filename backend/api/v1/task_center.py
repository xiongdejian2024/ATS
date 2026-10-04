"""任务中心接口：项目隔离、显式启用与独立执行历史。"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from api.deps import get_current_user
from core.project_access import require_project_access
from database import get_db
from models import TestPlan, TestSuite, User
from models.task_schedule import TaskSchedule, TaskScheduleRun
from schemas.common import APIResponse, ResponseStatus
from schemas.task_center import ScheduleCreate, ScheduleUpdate, ScheduleEnabled, RunTrigger
from services import task_scheduler as scheduler

router = APIRouter()


def output(data, message="操作成功"):
    return APIResponse(status=ResponseStatus.SUCCESS, message=message, data=data)


def timestamp(value):
    return value.isoformat(timespec="seconds") + "Z" if value else None


def schedule_json(row):
    return {
        "id": row.id, "projectId": row.project_id, "name": row.name,
        "targetType": row.target_type, "targetId": row.target_id,
        "cronExpression": row.cron_expression, "timezone": row.timezone,
        "enabled": row.enabled, "nextRunAt": timestamp(row.next_run_at),
        "lastRunAt": timestamp(row.last_run_at), "createdAt": timestamp(row.created_at),
    }


def run_json(row):
    return {
        "id": row.id, "scheduleId": row.schedule_id, "triggerType": row.trigger_type,
        "scheduledFor": timestamp(row.scheduled_for), "status": row.status,
        "executionId": row.execution_id, "planRunId": row.plan_run_id,
        "groupRunId": row.group_run_id,
        "errorMessage": row.error_message, "createdAt": timestamp(row.created_at),
        "deliveryState": row.delivery_state,
        "completedAt": timestamp(row.completed_at),
    }


def find_schedule(db, user, schedule_id, action="read"):
    row = db.get(TaskSchedule, schedule_id)
    if row is None:
        raise HTTPException(404, "任务不存在")
    require_project_access(db, user, row.project_id, "test_plan:" + action)
    return row


@router.get("/targets")
def targets(projectId: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_project_access(db, user, projectId, "test_plan:read")
    from models.plan_orchestration import PlanGroup
    groups = db.query(PlanGroup).filter_by(project_id=projectId).order_by(PlanGroup.name).all()
    plans = db.query(TestPlan).filter_by(project_id=projectId).order_by(TestPlan.name).all()
    suites = db.query(TestSuite).join(TestPlan, TestPlan.id == TestSuite.plan_id).filter(
        TestPlan.project_id == projectId,
    ).order_by(TestSuite.name).all()
    return output({
        "plans": [{"id": p.id, "name": p.name} for p in plans],
        "suites": [{"id": s.id, "name": s.name, "planId": s.plan_id} for s in suites],
        "groups": [{"id": g.id, "name": g.name} for g in groups],
    })


@router.get("")
def list_schedules(projectId: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_project_access(db, user, projectId, "test_plan:read")
    rows = db.query(TaskSchedule).filter_by(project_id=projectId).order_by(TaskSchedule.created_at.desc()).all()
    return output({"items": [schedule_json(row) for row in rows], "total": len(rows)})


@router.post("")
def create(data: ScheduleCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        row = scheduler.create_schedule(db, user, data)
        return output(schedule_json(row), "任务已保存，定时执行默认关闭")
    except ValueError as exc:
        scheduler.logger.exception("任务定义校验失败：项目={}", data.project_id)
        raise HTTPException(400, str(exc)) from exc


@router.put("/{schedule_id}")
def update_schedule(schedule_id: str, data: ScheduleUpdate, db: Session = Depends(get_db),
                    user: User = Depends(get_current_user)):
    row = find_schedule(db, user, schedule_id, "execute")
    expression = (data.cron_expression or "").strip() or None
    if not data.name.strip():
        raise HTTPException(400, "任务名称不能为空")
    try:
        # 复用校验器，手动任务也校验时区。
        next_at = scheduler.next_fire_time(expression or "0 0 * * *", data.timezone)
    except ValueError as exc:
        scheduler.logger.exception("任务配置校验失败：任务={}", schedule_id)
        raise HTTPException(400, str(exc)) from exc
    row.name, row.cron_expression, row.timezone = data.name.strip(), expression, data.timezone
    if not expression:
        row.enabled = False
    row.next_run_at = next_at if row.enabled else None
    row.updated_at = scheduler.utc_now()
    db.commit()
    scheduler.logger.info("任务配置已更新：任务={}", row.id)
    return output(schedule_json(row))


@router.post("/{schedule_id}/enabled")
def enabled(schedule_id: str, data: ScheduleEnabled, db: Session = Depends(get_db),
            user: User = Depends(get_current_user)):
    row = find_schedule(db, user, schedule_id, "execute")
    try:
        scheduler.set_enabled(db, user, row, data.enabled)
        return output(schedule_json(row))
    except ValueError as exc:
        scheduler.logger.exception("定时开关配置校验失败：任务={}", schedule_id)
        raise HTTPException(400, str(exc)) from exc


@router.post("/{schedule_id}/run")
async def trigger(schedule_id: str, data: RunTrigger, db: Session = Depends(get_db),
                  user: User = Depends(get_current_user)):
    row = find_schedule(db, user, schedule_id, "execute")
    try:
        run = await scheduler.trigger_schedule(db, user, row, data.request_id)
        # 即时按钮写入真实队列，周期循环负责发送；测试环境可显式调用tick。
        return output(run_json(run), "已创建执行记录并加入队列")
    except ValueError as exc:
        db.rollback()
        scheduler.logger.exception("手动任务触发校验失败：任务={}", schedule_id)
        raise HTTPException(400, str(exc)) from exc


@router.get("/{schedule_id}/runs")
def history(schedule_id: str, page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100),
            db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    find_schedule(db, user, schedule_id)
    query = db.query(TaskScheduleRun).filter_by(schedule_id=schedule_id)
    total = query.count()
    rows = query.order_by(TaskScheduleRun.created_at.desc()).offset((page - 1) * size).limit(size).all()
    return output({"items": [run_json(row) for row in rows], "total": total, "page": page, "size": size})


@router.post("/{schedule_id}/runs/{run_id}/cancel")
async def cancel(schedule_id: str, run_id: str, db: Session = Depends(get_db),
                 user: User = Depends(get_current_user)):
    find_schedule(db, user, schedule_id, "execute")
    run = db.get(TaskScheduleRun, run_id)
    if run is None or run.schedule_id != schedule_id:
        raise HTTPException(404, "执行记录不存在")
    return output(run_json(await scheduler.cancel_run(db, user, run)))


@router.post("/{schedule_id}/runs/{run_id}/resolve")
def resolve(schedule_id: str, run_id: str, db: Session = Depends(get_db),
            user: User = Depends(get_current_user)):
    find_schedule(db, user, schedule_id, "execute")
    run = db.get(TaskScheduleRun, run_id)
    if run is None or run.schedule_id != schedule_id:
        raise HTTPException(404, "执行记录不存在")
    return output(run_json(scheduler.resolve_uncertain_run(db, user, run)))
