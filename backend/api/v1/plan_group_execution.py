"""计划组执行、聚合报告及可撤销分享。"""
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import secrets

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from pydantic import BaseModel, Field
from typing import Literal
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from api.deps import get_current_user
from api.v1.case_governance import result, transact
from core.project_access import require_project_access
from core.logger import logger
from database import get_db
from models.plan_group_execution import PlanGroupPolicy, PlanGroupRun, PlanGroupShare
from models.plan_orchestration import PlanSettings
from models import TestPlan
from services import plan_group_execution as service
from services.plan_report_export import render_plan_report

router = APIRouter(prefix="/plan-groups", tags=["计划组执行"])


class Policy(BaseModel):
    executionMode: Literal["serial", "parallel"] = "serial"
    stopOnFailure: bool = False
    passThreshold: float = Field(100, ge=0, le=100)
    planOrder: list[str] = Field(default_factory=list, max_length=1000)


class Trigger(BaseModel):
    requestId: str = Field(min_length=1, max_length=80)


class ShareInput(BaseModel):
    expiresHours: int = Field(24, ge=1, le=720)


class Summary(BaseModel):
    conclusion: str = Field("", max_length=10000)
    risk: str = Field("", max_length=10000)
    notes: str = Field("", max_length=10000)


def find_run(db, user, run_id, action="read"):
    run = db.get(PlanGroupRun, run_id)
    if not run:
        raise HTTPException(404, "计划组批次不存在")
    require_project_access(db, user, run.project_id, "test_plan:" + action)
    return run


def policy_data(db, group_id):
    policy = service.get_policy(db, group_id)
    order = {pid: i for i, pid in enumerate(policy["planOrder"])}
    members = db.query(TestPlan).join(PlanSettings, PlanSettings.plan_id == TestPlan.id).filter(
        PlanSettings.group_id == group_id).order_by(TestPlan.created_at, TestPlan.id).all()
    members.sort(key=lambda plan: order.get(plan.id, len(order)))
    return dict(**policy, members=[dict(id=plan.id, name=plan.name) for plan in members])


@router.get("/{group_id}/settings")
def settings(group_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    service.find_group(db, user, group_id)
    return result(policy_data(db, group_id))


@router.put("/{group_id}/settings")
def save_settings(group_id: str, data: Policy, db: Session = Depends(get_db), user=Depends(get_current_user)):
    service.find_group(db, user, group_id, "update")
    member_ids = {s.plan_id for s in db.query(PlanSettings).filter_by(group_id=group_id).all()}
    if len(set(data.planOrder)) != len(data.planOrder) or not set(data.planOrder) <= member_ids:
        raise HTTPException(400, "排序包含重复或不属于计划组的计划")
    def operation():
        row = db.get(PlanGroupPolicy, group_id) or PlanGroupPolicy(group_id=group_id)
        row.execution_mode, row.stop_on_failure = data.executionMode, data.stopOnFailure
        row.pass_threshold, row.plan_order = data.passThreshold, data.planOrder
        db.add(row)
    transact(db, operation)
    return result(policy_data(db, group_id))


@router.post("/{group_id}/runs")
async def execute(group_id: str, data: Trigger, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        run = await service.start_group_run(db, group_id, user.id, f"group:{group_id}:{user.id}:{data.requestId}")
        return result(service.run_data(db, run))
    except ValueError as exc:
        db.rollback()
        logger.exception("计划组执行参数无效：计划组={}", group_id)
        raise HTTPException(400, str(exc)) from exc
    except IntegrityError as exc:
        db.rollback()
        logger.exception("计划组批次并发冲突：计划组={}", group_id)
        raise HTTPException(409, "计划组已有活动批次，请刷新后重试") from exc
    except Exception:
        db.rollback()
        logger.exception("创建计划组执行失败：计划组={}", group_id)
        raise


@router.get("/{group_id}/runs")
def history(group_id: str, page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), db: Session = Depends(get_db), user=Depends(get_current_user)):
    service.find_group(db, user, group_id)
    query = db.query(PlanGroupRun).filter_by(group_id=group_id)
    return result(dict(items=[service.run_data(db, r) for r in query.order_by(PlanGroupRun.created_at.desc()).offset((page-1)*size).limit(size).all()], total=query.count()))


@router.get("/runs/{run_id}")
def detail(run_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_report_workspace import ensure_visible
    run = find_run(db, user, run_id)
    ensure_visible(db, "GROUP", run_id)
    return result(service.run_data(db, run))


@router.post("/runs/{run_id}/cancel")
async def cancel(run_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    run = find_run(db, user, run_id, "execute")
    await service.cancel_group_run(db, run, user)
    return result(service.run_data(db, run))


@router.put("/runs/{run_id}/summary")
def summary(run_id: str, data: Summary, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_report_workspace import ensure_visible
    run = find_run(db, user, run_id, "update")
    ensure_visible(db, "GROUP", run_id)
    def operation():
        run.summary = data.model_dump()
    transact(db, operation)
    return result(service.run_data(db, run))


@router.get("/runs/{run_id}/pdf")
def export_pdf(run_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_report_workspace import ensure_visible
    run = find_run(db, user, run_id)
    ensure_visible(db, "GROUP", run_id)
    return Response(render_plan_report(service.run_data(db, run)), media_type="application/pdf",
                    headers={"Content-Disposition": f'attachment; filename="ATS-group-{run_id}.pdf"'})


@router.post("/runs/{run_id}/share")
def share(run_id: str, data: ShareInput, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_report_workspace import ensure_visible
    run = find_run(db, user, run_id)
    ensure_visible(db, "GROUP", run_id)
    token = secrets.token_urlsafe(32)
    row = PlanGroupShare(run_id=run.id, token_hash=sha256(token.encode()).hexdigest(), created_by=str(user.id),
                         expires_at=datetime.now(timezone.utc).replace(tzinfo=None)+timedelta(hours=data.expiresHours))
    transact(db, lambda: db.add(row))
    return result(dict(id=row.id, path=f"/api/v1/plan-groups/shared/{token}/pdf", expiresAt=row.expires_at.isoformat()+"Z"))


@router.delete("/runs/{run_id}/shares/{share_id}")
def revoke(run_id: str, share_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    find_run(db, user, run_id)
    row = db.get(PlanGroupShare, share_id)
    if not row or row.run_id != run_id or row.created_by != str(user.id):
        raise HTTPException(404, "分享不存在或不是当前用户创建")
    def operation():
        row.revoked = True
    transact(db, operation)
    return result()


@router.get("/shared/{token}/pdf")
def public_pdf(token: str, db: Session = Depends(get_db)):
    row = db.query(PlanGroupShare).filter_by(token_hash=sha256(token.encode()).hexdigest(), revoked=False).first()
    if not row or row.expires_at <= datetime.now(timezone.utc).replace(tzinfo=None):
        raise HTTPException(404, "分享不存在、已撤销或已过期")
    run = db.get(PlanGroupRun, row.run_id)
    from services.plan_report_workspace import ensure_visible
    ensure_visible(db, "GROUP", row.run_id)
    return Response(render_plan_report(service.run_data(db, run)), media_type="application/pdf",
                    headers={"Cache-Control": "no-store", "Content-Disposition": 'inline; filename="ATS-group-report.pdf"'})
