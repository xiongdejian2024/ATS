"""用例附件及回收站接口。"""

from fastapi import APIRouter, Depends, File, UploadFile, Query, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db
from api.deps import get_current_user
from api.v1.case_governance import result, transact
from core.project_access import require_project_access
from models.test_case import TestCase, CaseAttachment
from models.case_features import CaseChange
from services import case_features as service
from utils.serializer import serialize_model, serialize_list
from models.case_features import (
    CaseTemplate,
    CaseIssue,
    CaseIssueLink,
    CaseRelation,
    CaseAutomationLink,
    CaseFollow,
    CaseComment,
)
from schemas.case_features import (
    TemplateWrite,
    IssueWrite,
    IssueLinkWrite,
    RelationWrite,
    AutomationWrite,
    CommentWrite,
)
from sqlalchemy import or_

router = APIRouter(prefix="/projects/{project_id}/case-features", tags=["用例扩展"])


from models.case_features import CaseProjectSettings
from schemas.case_features import ProjectSettingsWrite


@router.get("/settings")
def project_settings(
    project_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    require_project_access(db, user, project_id, "test_case:read")
    row = db.query(CaseProjectSettings).filter_by(project_id=project_id).first()
    return result({"autoResubmit": bool(row and row.auto_resubmit)})


@router.put("/settings")
def write_project_settings(
    project_id: str,
    body: ProjectSettingsWrite,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_project_access(db, user, project_id, "test_case:update")

    def operation():
        row = db.query(CaseProjectSettings).filter_by(project_id=project_id).first()
        if not row:
            row = CaseProjectSettings(project_id=project_id)
        row.auto_resubmit = body.autoResubmit
        db.add(row)

    transact(db, operation)
    return result(body.model_dump())


@router.get("/cases/{case_id}/usage")
def usage(
    project_id: str,
    case_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service.find_case(db, user, project_id, case_id)
    from models.test_plan import TestPlan, PlanCaseRelation
    from models.test_suite import TestSuite
    from models.plan_workspace import PlanNode
    from models.case_governance import CaseReview, CaseReviewItem

    plans = {
        row.id: row
        for row in db.query(TestPlan)
        .join(PlanCaseRelation, PlanCaseRelation.plan_id == TestPlan.id)
        .filter(TestPlan.project_id == project_id, PlanCaseRelation.case_id == case_id)
        .all()
    }
    for plan in db.query(TestPlan).join(PlanNode,PlanNode.plan_id==TestPlan.id).filter(TestPlan.project_id==project_id,PlanNode.case_id==case_id).all():
        plans[plan.id]=plan
    for suite, plan in (
        db.query(TestSuite, TestPlan)
        .join(TestPlan, TestPlan.id == TestSuite.plan_id)
        .filter(TestPlan.project_id == project_id)
        .all()
    ):
        if case_id in (suite.case_ids or []):
            plans[plan.id] = plan
    reviews = (
        db.query(CaseReview)
        .join(CaseReviewItem, CaseReviewItem.review_id == CaseReview.id)
        .filter(CaseReview.project_id == project_id, CaseReviewItem.case_id == case_id)
        .all()
    )
    return result(
        {
            "plans": [
                {"id": p.id, "name": p.name, "status": p.status} for p in plans.values()
            ],
            "reviews": [
                {"id": r.id, "name": r.name, "status": r.status} for r in reviews
            ],
        }
    )


@router.get("/templates")
def templates(
    project_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    require_project_access(db, user, project_id, "test_case:read")
    return result(
        serialize_list(
            db.query(CaseTemplate)
            .filter_by(project_id=project_id)
            .order_by(CaseTemplate.is_default.desc(), CaseTemplate.created_at)
            .all(),
            camel_case=True,
        )
    )


@router.post("/templates")
def create_template(
    project_id: str,
    body: TemplateWrite,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        serialize_model(
            transact(db, lambda: service.write_template(db, user, project_id, body)),
            camel_case=True,
        )
    )


@router.put("/templates/{identifier}")
def update_template(
    project_id: str,
    identifier: str,
    body: TemplateWrite,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        serialize_model(
            transact(
                db,
                lambda: service.write_template(db, user, project_id, body, identifier),
            ),
            camel_case=True,
        )
    )


@router.delete("/templates/{identifier}")
def delete_template(
    project_id: str,
    identifier: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_project_access(db, user, project_id, "test_case:update")
    row = db.query(CaseTemplate).filter_by(id=identifier, project_id=project_id).first()
    if not row:
        raise HTTPException(404, "模板不存在")
    if db.query(TestCase).filter_by(template_id=identifier).first():
        raise HTTPException(409, "模板仍被用例使用，不能删除")
    transact(db, lambda: db.delete(row))
    return result()


@router.get("/issues")
def issues(
    project_id: str,
    kind: str | None = None,
    search: str = "",
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_project_access(db, user, project_id, "test_case:read")
    query = db.query(CaseIssue).filter_by(project_id=project_id)
    if kind:
        query = query.filter_by(kind=kind)
    if search:
        query = query.filter(CaseIssue.title.contains(search))
    return result(
        serialize_list(
            query.order_by(CaseIssue.created_at.desc()).all(), camel_case=True
        )
    )


@router.post("/issues")
def create_issue(
    project_id: str,
    body: IssueWrite,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        serialize_model(
            transact(db, lambda: service.write_issue(db, user, project_id, body)),
            camel_case=True,
        )
    )


@router.put("/issues/{identifier}")
def update_issue(
    project_id: str,
    identifier: str,
    body: IssueWrite,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        serialize_model(
            transact(
                db, lambda: service.write_issue(db, user, project_id, body, identifier)
            ),
            camel_case=True,
        )
    )


@router.delete("/issues/{identifier}")
def delete_issue(
    project_id: str,
    identifier: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_project_access(db, user, project_id, "test_case:delete")
    row = service.issue_for_project(db, project_id, identifier)
    if db.query(CaseIssueLink).filter_by(issue_id=identifier).first():
        raise HTTPException(409, "需求或缺陷仍有关联用例，不能删除")
    from models.plan_orchestration import PlanRun
    from models.test_plan import TestPlan
    for run in db.query(PlanRun).join(TestPlan,TestPlan.id==PlanRun.plan_id).filter(TestPlan.project_id==project_id).all():
        for entry in (run.manual_results or {}).values():
            if any(identifier in step.get("defectIds",[]) for step in entry.get("stepResults",[])):
                raise HTTPException(409,"缺陷已被执行记录引用，请保留历史证据")
    transact(db, lambda: db.delete(row))
    return result()


@router.get("/cases/{case_id}/issues")
def case_issues(
    project_id: str,
    case_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service.find_case(db, user, project_id, case_id)
    rows = (
        db.query(CaseIssueLink, CaseIssue)
        .join(CaseIssue, CaseIssue.id == CaseIssueLink.issue_id)
        .filter(CaseIssueLink.case_id == case_id, CaseIssue.project_id == project_id)
        .all()
    )
    return result(
        [
            {**serialize_model(issue, camel_case=True), "linkId": link.id}
            for link, issue in rows
        ]
    )


@router.post("/cases/{case_id}/issues")
def link_issue(
    project_id: str,
    case_id: str,
    body: IssueLinkWrite,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    case = service.find_case(db, user, project_id, case_id, "update")
    service.issue_for_project(db, project_id, body.issueId)

    def operation():
        row = CaseIssueLink(
            case_id=case_id, issue_id=body.issueId, created_by=str(user.id)
        )
        db.add(row)
        db.flush()
        service.change(db, case, user.id, "关联需求缺陷", body.model_dump())
        return row

    return result(serialize_model(transact(db, operation), camel_case=True))


@router.delete("/cases/{case_id}/issues/{link_id}")
def unlink_issue(
    project_id: str,
    case_id: str,
    link_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    case = service.find_case(db, user, project_id, case_id, "update")
    row = db.query(CaseIssueLink).filter_by(id=link_id, case_id=case_id).first()
    if not row:
        raise HTTPException(404, "关联不存在")

    def operation():
        service.change(db, case, user.id, "取消需求缺陷关联", {"issueId": row.issue_id})
        db.delete(row)

    transact(db, operation)
    return result()


@router.get("/cases/{case_id}/relations")
def relations(
    project_id: str,
    case_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service.find_case(db, user, project_id, case_id)
    rows = (
        db.query(CaseRelation)
        .filter(
            CaseRelation.project_id == project_id,
            or_(
                CaseRelation.source_case_id == case_id,
                CaseRelation.target_case_id == case_id,
            ),
        )
        .all()
    )
    return result([service.relation_data(db, row, case_id) for row in rows])


@router.post("/cases/{case_id}/relations")
def create_relation(
    project_id: str,
    case_id: str,
    body: RelationWrite,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    row = transact(
        db, lambda: service.add_relation(db, user, project_id, case_id, body)
    )
    return result(service.relation_data(db, row, case_id))


@router.delete("/cases/{case_id}/relations/{identifier}")
def delete_relation(
    project_id: str,
    case_id: str,
    identifier: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    case = service.find_case(db, user, project_id, case_id, "update")
    row = (
        db.query(CaseRelation)
        .filter(
            CaseRelation.id == identifier,
            CaseRelation.project_id == project_id,
            or_(
                CaseRelation.source_case_id == case_id,
                CaseRelation.target_case_id == case_id,
            ),
        )
        .first()
    )
    if not row:
        raise HTTPException(404, "用例关系不存在")

    def operation():
        service.change(db, case, user.id, "删除用例关联", {"relationId": identifier})
        db.delete(row)

    transact(db, operation)
    return result()


@router.get("/automation-targets")
def automation_targets(
    project_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    require_project_access(db, user, project_id, "test_case:read")
    from models.test_suite import TestSuite
    from models.test_plan import TestPlan

    cases = (
        db.query(TestCase)
        .filter_by(project_id=project_id, is_automated=True)
        .filter(TestCase.deleted_at.is_(None))
        .all()
    )
    suites = (
        db.query(TestSuite)
        .join(TestPlan, TestPlan.id == TestSuite.plan_id)
        .filter(TestPlan.project_id == project_id)
        .all()
    )
    return result(
        {
            "cases": [{"id": r.id, "name": r.name, "type": r.type} for r in cases],
            "suites": [{"id": r.id, "name": r.name} for r in suites],
        }
    )


@router.get("/cases/{case_id}/automation")
def automation(
    project_id: str,
    case_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service.find_case(db, user, project_id, case_id)
    return result(
        serialize_list(
            db.query(CaseAutomationLink).filter_by(case_id=case_id).all(),
            camel_case=True,
        )
    )


@router.post("/cases/{case_id}/automation")
def create_automation(
    project_id: str,
    case_id: str,
    body: AutomationWrite,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        serialize_model(
            transact(
                db, lambda: service.add_automation(db, user, project_id, case_id, body)
            ),
            camel_case=True,
        )
    )


@router.delete("/cases/{case_id}/automation/{identifier}")
def delete_automation(
    project_id: str,
    case_id: str,
    identifier: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    case = service.find_case(db, user, project_id, case_id, "update")
    row = db.query(CaseAutomationLink).filter_by(id=identifier, case_id=case_id).first()
    if not row:
        raise HTTPException(404, "自动化关联不存在")

    def operation():
        service.change(db, case, user.id, "删除自动化关联", {"linkId": identifier})
        db.delete(row)

    transact(db, operation)
    return result()


@router.get("/cases/{case_id}/follow")
def follow_state(
    project_id: str,
    case_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service.find_case(db, user, project_id, case_id)
    return result(
        {
            "followed": bool(
                db.query(CaseFollow)
                .filter_by(case_id=case_id, user_id=str(user.id))
                .first()
            ),
            "count": db.query(CaseFollow).filter_by(case_id=case_id).count(),
        }
    )


@router.post("/cases/{case_id}/follow")
def follow(
    project_id: str,
    case_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    case = service.find_case(db, user, project_id, case_id)

    def operation():
        if (
            not db.query(CaseFollow)
            .filter_by(case_id=case_id, user_id=str(user.id))
            .first()
        ):
            db.add(CaseFollow(case_id=case_id, user_id=str(user.id)))
            service.change(db, case, user.id, "关注用例")

    transact(db, operation)
    return result({"followed": True})


@router.delete("/cases/{case_id}/follow")
def unfollow(
    project_id: str,
    case_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service.find_case(db, user, project_id, case_id)
    transact(
        db,
        lambda: db.query(CaseFollow)
        .filter_by(case_id=case_id, user_id=str(user.id))
        .delete(),
    )
    return result({"followed": False})


@router.get("/cases/{case_id}/comments")
def comments(
    project_id: str,
    case_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service.find_case(db, user, project_id, case_id)
    return result(
        serialize_list(
            db.query(CaseComment)
            .filter_by(case_id=case_id)
            .order_by(CaseComment.created_at)
            .all(),
            camel_case=True,
        )
    )


@router.post("/cases/{case_id}/comments")
def add_comment(
    project_id: str,
    case_id: str,
    body: CommentWrite,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    case = service.find_case(db, user, project_id, case_id)

    def operation():
        row = CaseComment(case_id=case_id, author_id=str(user.id), content=body.content)
        db.add(row)
        db.flush()
        service.change(db, case, user.id, "发表评论", {"commentId": row.id})
        return row

    return result(serialize_model(transact(db, operation), camel_case=True))


@router.delete("/cases/{case_id}/comments/{identifier}")
def delete_comment(
    project_id: str,
    case_id: str,
    identifier: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    case = service.find_case(db, user, project_id, case_id)
    row = db.query(CaseComment).filter_by(id=identifier, case_id=case_id).first()
    if not row:
        raise HTTPException(404, "评论不存在")
    if row.author_id != str(user.id):
        require_project_access(db, user, project_id, "test_case:update")

    def operation():
        service.change(
            db,
            case,
            user.id,
            "删除评论",
            {"commentId": identifier, "content": row.content},
        )
        db.delete(row)

    transact(db, operation)
    return result()


@router.get("/cases/{case_id}/attachments")
def attachments(
    project_id: str,
    case_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service.find_case(db, user, project_id, case_id)
    return result(
        [
            service.attachment_data(row)
            for row in db.query(CaseAttachment)
            .filter_by(case_id=case_id)
            .order_by(CaseAttachment.upload_time.desc())
            .all()
        ]
    )


@router.post("/cases/{case_id}/attachments")
def upload(
    project_id: str,
    case_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        service.attachment_data(
            service.upload_attachment(db, user, project_id, case_id, file)
        )
    )


@router.get("/attachments/{attachment_id}/download")
def download(
    project_id: str,
    attachment_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    row, _ = service.find_attachment(db, user, project_id, attachment_id)
    path = service.attachment_path(row)
    if not path.is_file():
        raise HTTPException(404, "附件文件不存在")
    return FileResponse(
        path,
        filename=row.file_name,
        media_type="application/octet-stream",
        headers={"X-Content-Type-Options": "nosniff"},
    )


@router.delete("/attachments/{attachment_id}")
def delete_attachment(
    project_id: str,
    attachment_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    row, case = service.find_attachment(db, user, project_id, attachment_id, "update")
    path = service.attachment_path(row)

    def operation():
        service.change(
            db,
            case,
            user.id,
            "删除附件",
            {"attachmentId": row.id, "fileName": row.file_name},
        )
        db.delete(row)

    transact(db, operation)
    service.remove_files([path])
    return result()


@router.get("/recycle-bin")
def recycle_bin(
    project_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=200),
    search: str = "",
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_project_access(db, user, project_id, "test_case:read")
    query = db.query(TestCase).filter(
        TestCase.project_id == project_id, TestCase.deleted_at.is_not(None)
    )
    if search:
        query = query.filter(TestCase.name.contains(search))
    return result(
        {
            "items": serialize_list(
                query.order_by(TestCase.deleted_at.desc())
                .offset((page - 1) * size)
                .limit(size)
                .all(),
                camel_case=True,
            ),
            "total": query.count(),
            "page": page,
            "size": size,
        }
    )


@router.post("/cases/{case_id}/restore")
def restore(
    project_id: str,
    case_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    case = transact(db, lambda: service.restore_case(db, user, project_id, case_id))
    return result(serialize_model(case, camel_case=True))


@router.delete("/cases/{case_id}/purge")
def purge(
    project_id: str,
    case_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    paths = transact(db, lambda: service.purge_case(db, user, project_id, case_id))
    service.remove_files(paths)
    return result()


@router.get("/cases/{case_id}/changes")
def changes(
    project_id: str,
    case_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_project_access(db, user, project_id, "test_case:read")
    rows = (
        db.query(CaseChange)
        .filter_by(project_id=project_id, case_id=case_id)
        .order_by(CaseChange.created_at.desc())
        .limit(500)
        .all()
    )
    return result(serialize_list(rows, camel_case=True))
