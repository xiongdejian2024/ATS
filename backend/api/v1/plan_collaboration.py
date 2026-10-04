"""计划执行协作与真实 PDF/限时分享接口。"""
import base64
from urllib.parse import quote
from fastapi import APIRouter, Depends, HTTPException, Response
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
