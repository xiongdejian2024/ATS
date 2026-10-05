"""评审条目的人员调整与取消关联，在同一项目锁和事务中完成。"""

from fastapi import HTTPException
from models.case_governance import CaseReviewItem, CaseReviewDecision, CaseReviewComment
from services import case_governance as governance
from services.review_workspace import require_mutable
from core.logger import logger
from utils.datetime_utils import beijing_now


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
                "rejected"
                if any(vote.decision == "rejected" for vote in effective)
                else (
                    "approved"
                    if len(effective) == len(item.reviewer_ids)
                    else "pending"
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
