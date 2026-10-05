"""独立用例审阅的只读详情与个人历史状态，不创建版本或执行任务。"""

from models import TestCase
from models.test_case import CaseAttachment
from models.case_features import CaseIssue, CaseIssueLink, CaseTemplate
from models.case_governance import CaseReviewEvent
from services import case_governance as governance
from services.review_case_workspace import get_item
from utils.serializer import serialize_model


def personal_states(db, user, review_id, identifiers):
    events = (
        db.query(CaseReviewEvent)
        .filter(
            CaseReviewEvent.review_id == review_id,
            CaseReviewEvent.item_id.in_(identifiers),
            CaseReviewEvent.action.in_(["评审结论", "重新提审"]),
        )
        .order_by(CaseReviewEvent.created_at.desc(), CaseReviewEvent.id.desc())
        .all()
    )
    abandoned = {
        identifier
        for e in events
        if e.action == "重新提审"
        for identifier in (e.detail or {}).get("invalidatedEventIds", [])
    }
    states = {}
    for event in events:
        details = event.detail or {}
        if (
            event.id in abandoned
            or event.actor_id != str(user.id)
            or details.get("automatic")
        ):
            continue
        if event.item_id in states:
            continue
        states[event.item_id] = (
            "re_review"
            if event.action == "重新提审"
            else {
                "approved": "approved",
                "rejected": "rejected",
                "suggestion": "under_review",
            }.get(details.get("decision"), "un_review")
        )
    return states


def reading(db, user, project_id, review_id, item_id):
    item = get_item(db, user, project_id, review_id, item_id)
    review = governance.get_review(db, user, project_id, review_id)
    data = governance.review_data(db, review, include_items=False)
    history = [
        e
        for e in data["history"]
        if e["itemId"] == item_id and e["action"] in {"评审结论", "重新提审"}
    ]
    data.pop("history")
    data.pop("comments")
    case = db.get(TestCase, item["caseId"])
    template_id = item["snapshot"].get("template_id")
    template = (
        db.query(CaseTemplate).filter_by(id=template_id, project_id=project_id).first()
        if template_id
        else None
    )
    requirements = (
        db.query(CaseIssue)
        .join(CaseIssueLink, CaseIssueLink.issue_id == CaseIssue.id)
        .filter(
            CaseIssueLink.case_id == item["caseId"],
            CaseIssue.project_id == project_id,
            CaseIssue.kind == "requirement",
        )
        .order_by(CaseIssue.created_at, CaseIssue.id)
        .all()
    )
    attachments = (
        db.query(CaseAttachment)
        .filter_by(case_id=item["caseId"])
        .order_by(CaseAttachment.upload_time, CaseAttachment.id)
        .all()
    )
    return dict(
        review=data,
        item=item,
        history=history,
        createdAt=case.created_at.isoformat() if case else None,
        customFields=template.fields if template else [],
        requirements=[serialize_model(r) for r in requirements],
        attachments=[
            dict(
                id=a.id,
                caseId=a.case_id,
                fileName=a.file_name,
                fileSize=a.file_size,
                fileType=a.file_type,
                uploadedBy=a.uploaded_by,
                uploadTime=a.upload_time.isoformat(),
            )
            for a in attachments
        ],
    )
