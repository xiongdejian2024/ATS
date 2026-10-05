"""核心用例内容变更触发系统同单重新提审，不创建后续评审单。"""

from models import User
from models.case_features import CaseProjectSettings
from models.case_governance import CaseReview, CaseReviewItem
from models.review_workspace import ReviewWorkspace
from services.review_item_management import reset_items
from core.logger import logger

TRIGGER_FIELDS = ("name", "steps", "text_description", "expected_result")


def handle_case_change(db, case, actor_id, version, before, after):
    """由保存版本的写事务调用；调用方持有项目和用例锁。"""
    changed = [
        field for field in TRIGGER_FIELDS if before.get(field) != after.get(field)
    ]
    if not changed:
        return 0
    settings = (
        db.query(CaseProjectSettings)
        .filter_by(project_id=case.project_id)
        .populate_existing()
        .with_for_update()
        .first()
    )
    if not settings or not settings.auto_resubmit:
        return 0
    reviews = (
        db.query(CaseReview)
        .join(CaseReviewItem, CaseReviewItem.review_id == CaseReview.id)
        .filter(
            CaseReview.project_id == case.project_id,
            CaseReviewItem.case_id == case.id,
            CaseReview.status.notin_(["cancelled", "superseded"]),
        )
        .order_by(CaseReview.id)
        .populate_existing()
        .with_for_update()
        .all()
    )
    if not reviews:
        return 0
    workspaces = {
        row.review_id: row
        for row in db.query(ReviewWorkspace)
        .filter(ReviewWorkspace.review_id.in_([review.id for review in reviews]))
        .order_by(ReviewWorkspace.review_id)
        .populate_existing()
        .with_for_update()
        .all()
    }
    eligible = {
        review.id: review
        for review in reviews
        if not (workspaces.get(review.id) and workspaces[review.id].archived)
    }
    if not eligible:
        return 0
    items = (
        db.query(CaseReviewItem)
        .filter(
            CaseReviewItem.review_id.in_(eligible), CaseReviewItem.case_id == case.id
        )
        .order_by(CaseReviewItem.id)
        .populate_existing()
        .with_for_update()
        .all()
    )
    actor = db.get(User, str(actor_id))
    for item in items:
        reset_items(
            db,
            actor,
            eligible[item.review_id],
            [item],
            {case.id: version},
            automatic=True,
            changed_fields=changed,
        )
    logger.info(
        "用例变更自动同单提审完成 project_id={} case_id={} version={} review_count={} fields={}",
        case.project_id,
        case.id,
        version.version,
        len(items),
        changed,
    )
    return len(items)
