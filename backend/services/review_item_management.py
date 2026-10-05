"""评审条目的人员调整、取消关联与同单重新提审，共用项目锁和事务。"""

from fastapi import HTTPException
from sqlalchemy import func
from models import TestCase, Project
from models.case_governance import (
    CaseReviewItem,
    CaseReviewDecision,
    CaseReviewComment,
    CaseReviewEvent,
    CaseVersion,
)
from core.permissions import has_global_permission
from core.project_access import project_allows
from services import case_governance as governance
from services.review_workspace import require_mutable
from core.logger import logger
from utils.datetime_utils import beijing_now


def re_review_permissions(db, user, project_id):
    project = db.get(Project, project_id)
    return (
        project_allows(db, user, project, "test_case:update"),
        has_global_permission(db, user.id, "system", "manage"),
    )


def locked_items(db, user, project_id, review_id, identifiers):
    governance.project_access(db, user, project_id, "update")
    review = governance.get_review(db, user, project_id, review_id, lock=True)
    require_mutable(db, review)
    if review.status in {"cancelled", "superseded"}:
        raise HTTPException(409, "评审已关闭，不能修改关联用例")
    items = (
        db.query(CaseReviewItem)
        .filter(
            CaseReviewItem.review_id == review.id, CaseReviewItem.id.in_(identifiers)
        )
        .order_by(CaseReviewItem.id)
        .populate_existing()
        .with_for_update()
        .all()
    )
    if len(items) != len(identifiers):
        raise HTTPException(404, "所选评审用例不存在，请刷新后重试")
    return review, items


def change_reviewers(db, user, project_id, review_id, request):
    review, items = locked_items(db, user, project_id, review_id, request.itemIds)
    eligible = {person["id"] for person in governance.reviewers(db, project_id)}
    if not set(request.reviewerIds) <= eligible:
        raise HTTPException(422, "评审人必须属于当前项目")
    assignments = {}
    for item in items:
        old = item.reviewer_ids or review.reviewer_ids
        values = list(
            dict.fromkeys((old if request.append else []) + request.reviewerIds)
        )
        if len(values) > 50:
            raise HTTPException(422, "每条用例最多指定50位评审人")
        assignments[item.id] = values
    votes = {}
    for decision in (
        db.query(CaseReviewDecision)
        .filter(CaseReviewDecision.item_id.in_(request.itemIds))
        .populate_existing()
        .with_for_update()
        .all()
    ):
        votes.setdefault(decision.item_id, []).append(decision)
    reset_authors = {}
    for event in (
        db.query(CaseReviewEvent)
        .filter(
            CaseReviewEvent.review_id == review.id,
            CaseReviewEvent.item_id.in_(request.itemIds),
            CaseReviewEvent.action.in_(["重新提审", "评审结论"]),
        )
        .order_by(CaseReviewEvent.created_at.desc(), CaseReviewEvent.id.desc())
        .all()
    ):
        if (
            event.action == "评审结论"
            and (event.detail or {}).get("decision") == "suggestion"
        ):
            continue
        reset_authors.setdefault(
            event.item_id,
            (
                event.actor_id
                if event.action == "重新提审"
                and not (event.detail or {}).get("automatic")
                else None
            ),
        )
    for item in items:
        before = list(item.reviewer_ids or review.reviewer_ids)
        item.reviewer_ids = assignments[item.id]
        if review.mode == "multiple":
            effective = [
                vote
                for vote in votes.get(item.id, [])
                if vote.reviewer_id in item.reviewer_ids
            ]
            item.status = (
                "re_review"
                if reset_authors.get(item.id) in item.reviewer_ids
                else (
                    "rejected"
                    if any(vote.decision == "rejected" for vote in effective)
                    else (
                        "approved"
                        if len(effective) == len(item.reviewer_ids)
                        else "pending"
                    )
                )
            )
        governance.review_event(
            db,
            review,
            user.id,
            "修改评审人",
            dict(
                caseId=item.case_id,
                before=before,
                after=item.reviewer_ids,
                append=request.append,
            ),
            item.id,
        )
    db.flush()
    governance.refresh_review_status(db, review)
    review.updated_at = beijing_now()
    db.flush()
    logger.info(
        "评审人已修改 review_id={} actor_id={} append={} item_count={}",
        review.id,
        user.id,
        request.append,
        len(items),
    )
    return governance.review_data(db, review, include_items=False)


def re_review(db, user, project_id, review_id, request):
    """同单重新提审：旧票作废，历史和旧版本保留；整批权限先校验。"""
    review, items = locked_items(db, user, project_id, review_id, request.itemIds)
    _, administrator = re_review_permissions(db, user, project_id)
    if not administrator and any(
        str(user.id) not in (item.reviewer_ids or review.reviewer_ids) for item in items
    ):
        raise HTTPException(403, "只有指定评审人或系统管理员可以重新提审")
    case_ids = [item.case_id for item in items]
    if db.query(TestCase).filter(
        TestCase.id.in_(case_ids),
        TestCase.project_id == project_id,
        TestCase.deleted_at.is_(None),
    ).count() != len(items):
        raise HTTPException(404, "所选用例已回收或不属于当前项目")
    latest = (
        db.query(CaseVersion.case_id, func.max(CaseVersion.version).label("number"))
        .filter(CaseVersion.project_id == project_id, CaseVersion.case_id.in_(case_ids))
        .group_by(CaseVersion.case_id)
        .subquery()
    )
    versions = {
        v.case_id: v
        for v in db.query(CaseVersion)
        .join(
            latest,
            (CaseVersion.case_id == latest.c.case_id)
            & (CaseVersion.version == latest.c.number),
        )
        .all()
    }
    if len(versions) != len(items):
        raise HTTPException(409, "所选用例版本不存在，请刷新后重试")
    reset_items(db, user, review, items, versions, comment=request.comment)
    return governance.review_data(db, review, include_items=False)


def reset_items(
    db,
    user,
    review,
    items,
    versions,
    *,
    comment="",
    automatic=False,
    changed_fields=None,
):
    """仅供已校验权限并持有项目、评审和条目锁的调用方，共用新轮次规则。"""
    identifiers = [item.id for item in items]
    votes = {}
    for vote in (
        db.query(CaseReviewDecision)
        .filter(CaseReviewDecision.item_id.in_(identifiers))
        .populate_existing()
        .with_for_update()
        .all()
    ):
        votes.setdefault(vote.item_id, []).append(vote)
    old_events = {}
    for event in (
        db.query(CaseReviewEvent)
        .filter(
            CaseReviewEvent.review_id == review.id,
            CaseReviewEvent.item_id.in_(identifiers),
            CaseReviewEvent.action.in_(["评审结论", "重新提审"]),
        )
        .all()
    ):
        old_events.setdefault(event.item_id, []).append(event.id)
    for item in items:
        governance.review_event(
            db,
            review,
            user.id,
            "重新提审",
            dict(
                caseId=item.case_id,
                comment=comment,
                automatic=automatic,
                changedFields=changed_fields or [],
                beforeStatus=item.status,
                beforeVersionId=item.version_id,
                versionId=versions[item.case_id].id,
                invalidatedEventIds=old_events.get(item.id, []),
                invalidatedDecisions=[
                    dict(
                        id=v.id,
                        reviewerId=v.reviewer_id,
                        decision=v.decision,
                        comment=v.comment,
                        updatedAt=v.updated_at.isoformat(),
                    )
                    for v in votes.get(item.id, [])
                ],
            ),
            item.id,
        )
        item.version_id = versions[item.case_id].id
        item.status = "re_review"
    db.query(CaseReviewDecision).filter(
        CaseReviewDecision.item_id.in_(identifiers)
    ).delete(synchronize_session=False)
    db.flush()
    governance.refresh_review_status(db, review)
    review.updated_at = beijing_now()
    db.flush()
    logger.info(
        "评审同单重新提审完成 review_id={} actor_id={} item_count={} automatic={}",
        review.id,
        user.id,
        len(items),
        automatic,
    )


def disassociate(db, user, project_id, review_id, request):
    review, items = locked_items(db, user, project_id, review_id, request.itemIds)
    identifiers = [item.id for item in items]
    case_ids = [item.case_id for item in items]
    db.query(CaseReviewDecision).filter(
        CaseReviewDecision.item_id.in_(identifiers)
    ).delete(synchronize_session=False)
    # 保留讨论正文和作者，将已取消关联的条目讨论留在整单历史中。
    db.query(CaseReviewComment).filter(
        CaseReviewComment.item_id.in_(identifiers)
    ).update({CaseReviewComment.item_id: None}, synchronize_session=False)
    db.query(CaseReviewItem).filter(CaseReviewItem.id.in_(identifiers)).delete(
        synchronize_session=False
    )
    governance.review_event(
        db, review, user.id, "取消关联", dict(itemIds=identifiers, caseIds=case_ids)
    )
    db.flush()
    governance.refresh_review_status(db, review)
    review.updated_at = beijing_now()
    db.flush()
    logger.info(
        "评审用例关联已取消 review_id={} actor_id={} item_count={}",
        review.id,
        user.id,
        len(items),
    )
    return governance.review_data(db, review, include_items=False)
