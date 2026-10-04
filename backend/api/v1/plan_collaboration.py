"""计划执行协作与真实 PDF/限时分享接口。"""
import base64
from datetime import datetime
from typing import Literal
from urllib.parse import quote
from fastapi import APIRouter, Depends, HTTPException, Response, Query
from sqlalchemy.orm import Session
from database import get_db
from api.deps import get_current_user
from models.plan_workspace import PlanRunComment, PlanRunAttachment, PlanReportSummary, PlanReportShare
from services.plan_collaboration import require_association, attach, enriched_report, create_share, shared_run
from utils.serializer import serialize_model
from schemas.common import APIResponse, ResponseStatus

router = APIRouter()


def ok(data=None):
    return APIResponse(status=ResponseStatus.SUCCESS, message="操作成功", data=data)


def access(db, user, run_id, action="read"):
    from api.v1.plan_orchestration import require_run
    return require_run(db, user, run_id, action)


@router.get("/projects/{project_id}/reports")
def report_list(project_id: str, page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100),
                search: str | None = Query(None, max_length=255), plan_name: str | None = Query(None, max_length=255),
                kind: Literal["PLAN", "GROUP"] | None = None, result_status: str | None = Query(None, max_length=30),
                trigger_mode: Literal["manual", "cron"] | None = None, operator: str | None = Query(None, max_length=100),
                start_time: datetime | None = None, end_time: datetime | None = None,
                min_rate: float | None = Query(None, ge=0, le=100), max_rate: float | None = Query(None, ge=0, le=100),
                sort: Literal["created_at", "pass_rate", "result_status", "name"] = "created_at",
                direction: Literal["asc", "desc"] = "desc", db: Session = Depends(get_db), user=Depends(get_current_user)):
    from core.project_access import require_project_access
    from services.plan_report_workspace import list_reports
    require_project_access(db, user, project_id, "test_plan:read")
    # 正式数据库连接使用北京时间；先统一时区，避免混合时区比较抛出异常。
    from utils.datetime_utils import BEIJING_TZ
    start_time = start_time.astimezone(BEIJING_TZ).replace(tzinfo=None) if start_time and start_time.tzinfo else start_time
    end_time = end_time.astimezone(BEIJING_TZ).replace(tzinfo=None) if end_time and end_time.tzinfo else end_time
    if (start_time and end_time and start_time > end_time) or (min_rate is not None and max_rate is not None and min_rate > max_rate):
        raise HTTPException(422, "筛选范围的起点不能晚于终点")
    return ok(list_reports(db, project_id, page=page, size=size, search=search, plan_name=plan_name, kind=kind,
                           result_status=result_status, trigger_mode=trigger_mode, operator=operator,
                           start_time=start_time, end_time=end_time, min_rate=min_rate, max_rate=max_rate,
                           sort=sort, direction=direction))


@router.get("/projects/{project_id}/reports/{kind}/{run_id}")
def report_detail(project_id: str, kind: Literal["PLAN", "GROUP"], run_id: str,
                  db: Session = Depends(get_db), user=Depends(get_current_user)):
    from core.project_access import require_project_access
    from models import TestPlan
    require_project_access(db, user, project_id, "test_plan:read")
    if kind == "PLAN":
        run = access(db, user, run_id)
        if db.get(TestPlan, run.plan_id).project_id != project_id:
            raise HTTPException(404, "此项目中不存在该报告")
        payload = enriched_report(db, run)
        name = run.plan_name
    else:
        from api.v1.plan_group_execution import find_run
        from services.plan_group_execution import run_data
        run = find_run(db, user, run_id)
        if run.project_id != project_id:
            raise HTTPException(404, "此项目中不存在该报告")
        payload, name = run_data(db, run), run.group_name
    return ok(dict(kind=kind, name=name + " 报告", payload=payload))


@router.get("/runs/{run_id}/cases/{association_id}/collaboration")
def collaboration(run_id: str, association_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    run = access(db, user, run_id)
    require_association(run, association_id)
    comments = db.query(PlanRunComment).filter_by(run_id=run_id, association_id=association_id).order_by(PlanRunComment.created_at).all()
    attachments = db.query(PlanRunAttachment).filter_by(run_id=run_id, association_id=association_id).all()
    return ok({"comments": [serialize_model(row, camel_case=True) for row in comments],
               "attachments": [{"id": row.id, "name": row.name, "mimeType": row.mime_type, "authorId": row.author_id} for row in attachments]})


@router.post("/runs/{run_id}/cases/{association_id}/comments")
def comment(run_id: str, association_id: str, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    run = access(db, user, run_id)
    require_association(run, association_id)
    content = str(data.get("content", "")).strip()
    if not content or len(content) > 10000:
        raise HTTPException(422, "评论须为1到10000字")
    row = PlanRunComment(run_id=run.id, association_id=association_id, author_id=user.id, content=content)
    db.add(row)
    db.commit()
    return ok(serialize_model(row, camel_case=True))


@router.post("/runs/{run_id}/cases/{association_id}/attachments")
def attachment(run_id: str, association_id: str, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    row = attach(db, access(db, user, run_id), association_id, user.id, data)
    return ok({"id": row.id, "name": row.name})


@router.get("/attachments/{attachment_id}")
def download(attachment_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    row = db.get(PlanRunAttachment, attachment_id)
    if not row:
        raise HTTPException(404, "附件不存在")
    access(db, user, row.run_id)
    return Response(base64.b64decode(row.content_base64), media_type="application/octet-stream", headers={"Content-Disposition": "attachment; filename*=UTF-8''" + quote(row.name), "X-Content-Type-Options": "nosniff"})


@router.get("/runs/{run_id}/report")
def report(run_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return ok(enriched_report(db, access(db, user, run_id)))


@router.put("/runs/{run_id}/summary")
def save_summary(run_id: str, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    access(db, user, run_id, "update")
    if set(data) - {"conclusion", "risk", "notes"} or any(not isinstance(value, str) or len(value) > 20000 for value in data.values()):
        raise HTTPException(422, "总结仅支持结论、风险和备注，每项最多20000字")
    row = db.get(PlanReportSummary, run_id) or PlanReportSummary(run_id=run_id)
    row.summary, row.updated_by = data, user.id
    db.add(row)
    db.commit()
    return ok(data)


def pdf(db, run):
    from services.plan_report_export import render_plan_report
    return Response(render_plan_report(enriched_report(db, run)), media_type="application/pdf", headers={"Cache-Control": "no-store", "Content-Disposition": f'attachment; filename="plan-report-{run.id}.pdf"'})


@router.get("/runs/{run_id}/pdf")
def export_pdf(run_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return pdf(db, access(db, user, run_id))


@router.post("/runs/{run_id}/shares")
def share(run_id: str, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    row, token = create_share(db, access(db, user, run_id, "update"), user.id, data.get("expiresHours", 24))
    return ok({"id": row.id, "token": token, "expiresAt": row.expires_at.isoformat() + "Z", "path": f"/api/v1/plan-orchestration/shared/{token}/pdf"})


@router.delete("/shares/{share_id}")
def revoke(share_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    row = db.get(PlanReportShare, share_id)
    if not row:
        raise HTTPException(404, "分享不存在")
    access(db, user, row.run_id, "update")
    row.revoked = True
    db.commit()
    return ok()


@router.get("/shared/{token}")
def read_shared(token: str, db: Session = Depends(get_db)):
    # 分享只暴露报告及总结，不包含模型配置、内部快照或凭证。
    payload = enriched_report(db, shared_run(db, token))
    return ok({key: payload[key] for key in ("id", "planName", "status", "report", "summary")})


@router.get("/shared/{token}/pdf")
def shared_pdf(token: str, db: Session = Depends(get_db)):
    return pdf(db, shared_run(db, token))


@router.get("/runs/{run_id}/shares")
def shares(run_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    access(db, user, run_id, "update")
    return ok([{"id": row.id, "expiresAt": row.expires_at.isoformat() + "Z", "revoked": row.revoked}
               for row in db.query(PlanReportShare).filter_by(run_id=run_id).order_by(PlanReportShare.created_at.desc())])
