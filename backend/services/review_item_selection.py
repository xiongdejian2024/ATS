"""评审批量操作共用筛选范围及排除项；写入时在项目锁内重新解析。"""

from fastapi import HTTPException
from sqlalchemy import or_
from models import TestCase
from models.case_governance import CaseReviewItem
from services import case_governance as governance
from services.review_case_workspace import query_scope, assigned_expression
from services.review_item_management import re_review_permissions
from services.review_workspace import metadata, require_mutable
from core.logger import logger


def selected_query(db, user, review, body, *, current_read=False):
    if body.selectAll:
        condition = body.condition
        query, _, _, _ = query_scope(
            db,
            review,
            folder=condition.folder,
            include_descendants=condition.includeDescendants,
            search=condition.search,
            priority=condition.priority,
            state=condition.state,
            states=condition.states,
            reviewer_id=condition.reviewerId,
            creator_id=condition.creatorId,
            only_mine=condition.onlyMine,
            user=user,
            current_read=current_read,
        )
    else:
        query = db.query(CaseReviewItem).filter(
            CaseReviewItem.review_id == review.id,
            CaseReviewItem.id.in_(body.itemIds),
        )
    return query.filter(CaseReviewItem.id.notin_(body.excludeIds))


def resolve(db, user, project_id, review_id, body, *, writing=False):
    review = governance.get_review(db, user, project_id, review_id, lock=writing)
    if writing:
        require_mutable(db, review)
        if review.status in {"cancelled", "superseded"}:
            raise HTTPException(409, "评审已关闭，不能修改关联用例")
    query = selected_query(db, user, review, body, current_read=writing)
    rows = (
        query.with_entities(CaseReviewItem.id).order_by(CaseReviewItem.id).limit(10001)
    )
    identifiers = [
        row[0] for row in (rows.with_for_update() if writing else rows).all()
    ]
    if len(identifiers) > 10000:
        raise HTTPException(422, "每批最多操作10000条用例，请缩小筛选范围")
    if not body.selectAll and len(identifiers) != len(body.itemIds):
        raise HTTPException(404, "所选评审用例不存在，请刷新后重试")
    if writing and not identifiers:
        raise HTTPException(409, "当前筛选范围已无可操作用例，请刷新后重新选择")
    if writing:
        logger.info(
            "评审批量范围已在项目锁内解析 review_id={} actor_id={} select_all={} selected={} excluded={}",
            review.id,
            user.id,
            body.selectAll,
            len(identifiers),
            len(body.excludeIds),
        )
    return review, identifiers


def preview(db, user, project_id, review_id, body):
    review = governance.get_review(db, user, project_id, review_id)
    query = selected_query(db, user, review, body)
    count = query.count()
    if count > 10000:
        raise HTTPException(422, "每批最多操作10000条用例，请缩小筛选范围")
    if not body.selectAll and count != len(body.itemIds):
        raise HTTPException(404, "所选评审用例不存在，请刷新后重试")
    if not body.selectAll:
        query = query.outerjoin(TestCase, TestCase.id == CaseReviewItem.case_id)
    invalid_case = or_(
        TestCase.id.is_(None),
        TestCase.deleted_at.is_not(None),
        TestCase.project_id != project_id,
    )
    assigned = assigned_expression(review).contains(
        '"' + str(user.id) + '"', autoescape=True
    )
    all_assigned = not query.filter(~assigned).first()
    live = not query.filter(invalid_case).first()
    editable, administrator = re_review_permissions(db, user, project_id)
    mutable = not metadata(db, review)["archived"] and review.status not in {
        "cancelled",
        "superseded",
    }
    excluded = 0
    if body.selectAll and body.excludeIds:
        # 只计入本次范围内真正排除的关联，其他范围的旧排除项不会影响数量。
        original = body.model_copy(update={"excludeIds": []})
        excluded = (
            selected_query(db, user, review, original)
            .filter(CaseReviewItem.id.in_(body.excludeIds))
            .count()
        )
    return dict(
        count=count,
        excludedCount=excluded,
        canVote=bool(count and mutable and live and all_assigned),
        canReReview=bool(
            count and mutable and live and editable and (administrator or all_assigned)
        ),
    )


def selected_cases(db, user, project_id, review_id, body):
    _, identifiers = resolve(db, user, project_id, review_id, body)
    return dict(
        caseIds=[
            row[0]
            for row in db.query(CaseReviewItem.case_id)
            .filter(CaseReviewItem.id.in_(identifiers))
            .order_by(CaseReviewItem.id)
            .all()
        ]
    )


def apply(db, user, project_id, review_id, body, operation):
    governance.project_access(db, user, project_id, "update")
    _, identifiers = resolve(db, user, project_id, review_id, body, writing=True)
    return operation(body.model_copy(update={"itemIds": identifiers}))


def vote(db, user, project_id, review_id, body):
    _, identifiers = resolve(db, user, project_id, review_id, body, writing=True)
    review = governance.vote_reviews(db, user, project_id, review_id, identifiers, body)
    return governance.review_data(db, review, include_items=False)
