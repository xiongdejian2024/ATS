"""计划步骤证据、报告总结和有时效的只读分享。"""
import base64
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from models.test_plan import TestPlan
from models.plan_workspace import PlanRunAttachment, PlanReportSummary, PlanReportShare
from core.logger import logger


def require_association(run, association_id):
    snapshot = next((c for c in run.case_snapshot if c.get("associationId", c["id"]) == association_id), None)
    if not snapshot:
        raise HTTPException(404, "本批次不存在此用例关联")
    return snapshot


def validate_steps(db, run, case, steps):
    from models.case_features import CaseIssue
    size = len(case.get("snapshot", {}).get("steps") or [])
    seen = set()
    clean = []
    project_id = db.get(TestPlan, run.plan_id).project_id
    for step in steps:
        index = step.get("index")
        if not isinstance(index, int) or isinstance(index, bool) or index < 0 or index >= size or index in seen:
            raise ValueError("步骤序号无效或重复")
        seen.add(index)
        if step.get("result") not in ("passed", "failed", "error", "skipped", "pending"):
            raise ValueError("步骤结果无效")
        defect_ids = step.get("defectIds", [])
        attachment_ids = step.get("attachments", [])
        if not isinstance(defect_ids, list) or not isinstance(attachment_ids, list):
            raise ValueError("缺陷和附件必须使用列表")
        frozen_defects = []
        for defect_id in defect_ids:
            defect = db.get(CaseIssue, defect_id)
            if not defect or defect.project_id != project_id or defect.kind != "defect":
                raise ValueError("缺陷不属于当前项目")
            frozen_defects.append(dict(id=defect.id, title=defect.title, description=defect.description, status=defect.status))
        for attachment_id in attachment_ids:
            attachment = db.get(PlanRunAttachment, attachment_id)
            if not attachment or attachment.run_id != run.id or attachment.association_id != case.get("associationId", case["id"]):
                raise ValueError("附件不属于当前批次用例")
        actual, notes = str(step.get("actual", "")), str(step.get("notes", ""))
        if len(actual) > 10000 or len(notes) > 10000:
            raise ValueError("步骤实际结果或备注过长")
        clean.append(dict(index=index, result=step["result"], actual=actual, notes=notes,
                          defectIds=list(dict.fromkeys(defect_ids)), defects=frozen_defects, attachments=list(dict.fromkeys(attachment_ids))))
    return sorted(clean, key=lambda step: step["index"])


def attach(db, run, association_id, user_id, data):
    require_association(run, association_id)
    name = str(data.get("name", "")).strip()
    encoded = data.get("contentBase64", "")
    if not name or len(name) > 255 or not isinstance(encoded, str) or len(encoded) > 7_000_000:
        raise HTTPException(422, "附件须有名称且不超过5MB")
    try:
        raw = base64.b64decode(encoded, validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        logger.exception("计划附件编码校验失败：批次={}", run.id)
        raise HTTPException(422, "附件内容编码无效") from exc
    if not raw or len(raw) > 5 * 1024 * 1024:
        raise HTTPException(422, "附件须为1字节到5MB")
    row = PlanRunAttachment(run_id=run.id, association_id=association_id, author_id=user_id,
                            name=name, mime_type=str(data.get("mimeType", "application/octet-stream"))[:120], content_base64=encoded)
    db.add(row)
    db.commit()
    logger.info("已保存计划执行证据：批次={}，附件={}", run.id, row.id)
    return row


def enriched_report(db, run):
    from services.plan_orchestration import run_data
    payload = run_data(db, run)
    summary = db.get(PlanReportSummary, run.id)
    payload["summary"] = summary.summary if summary else {}
    categories = {}
    for row in payload["report"]["cases"]:
        category = row.get("category", "functional")
        segment = categories.setdefault(category, {"total": 0, "counts": {}})
        segment["total"] += 1
        segment["counts"][row["result"]] = segment["counts"].get(row["result"], 0) + 1
    payload["report"]["categories"] = categories
    payload["report"]["bugs"] = list({defect["id"]: defect for row in payload["report"]["cases"] for step in row.get("stepResults", []) for defect in step.get("defects", [])}.values())
    return payload


def create_share(db, run, user_id, hours):
    if not isinstance(hours, int) or isinstance(hours, bool) or not 1 <= hours <= 24 * 90:
        raise HTTPException(422, "分享有效期须为1小时到90天")
    token = secrets.token_urlsafe(32)
    row = PlanReportShare(run_id=run.id, token_hash=hashlib.sha256(token.encode()).hexdigest(),
                          expires_at=datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=hours), created_by=user_id)
    db.add(row)
    db.commit()
    logger.info("已创建计划报告限时分享：批次={}，分享={}", run.id, row.id)
    return row, token


def shared_run(db, token):
    from models.plan_orchestration import PlanRun
    row = db.query(PlanReportShare).filter_by(token_hash=hashlib.sha256(token.encode()).hexdigest()).first()
    if not row or row.revoked or row.expires_at <= datetime.now(timezone.utc).replace(tzinfo=None):
        raise HTTPException(404, "报告分享不存在、已过期或被撤销")
    run = db.get(PlanRun, row.run_id)
    if not run:
        raise HTTPException(404, "报告不存在")
    return run
