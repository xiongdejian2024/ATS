"""ATS 用例版本、评审和个人视图接口。"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from api.deps import get_current_user
from database import get_db
from models.case_governance import (
    CaseVersion,
    CaseReview,
    CaseReviewItem,
    CaseReviewComment,
    CaseSavedView,
    CaseReviewFollow,
)
from schemas.case_governance import (
    RestoreVersion,
    ReviewCreate,
    ReviewVote,
    ReviewCommentCreate,
    SavedViewCreate,
    CaseBatchUpdate,
    CaseBatchCopy,
    ReviewBatchVote,
    ReviewResubmit,
)
from schemas.common import APIResponse
from services import case_governance as service
from core.logger import logger

router = APIRouter(
    prefix="/projects/{project_id}/case-governance", tags=["用例版本与评审"]
)


def result(data=None, message="操作成功"):
    return APIResponse(status="success", message=message, data=data)


def transact(db, operation):
    try:
        data = operation()
        db.commit()
        return data
    except HTTPException:
        db.rollback()
        raise
    except IntegrityError:
        db.rollback()
        logger.exception("用例治理写入冲突，事务已回滚")
        raise HTTPException(409, "数据已被修改或名称重复，请刷新后重试")
    except Exception:
        db.rollback()
        logger.exception("用例治理写入失败，事务已回滚")
        raise


@router.get("/cases/{case_id}/versions")
def versions(
    project_id: str,
    case_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service.project_access(db, user, project_id)
    service.case_for_project(db, project_id, case_id)
    rows = (
        db.query(CaseVersion)
        .filter_by(project_id=project_id, case_id=case_id)
        .order_by(CaseVersion.version.desc())
        .all()
    )
    return result([service.version_data(row) for row in rows])


@router.get("/cases/{case_id}/compare")
def compare(
    project_id: str,
    case_id: str,
    before: int = Query(ge=1),
    after: int = Query(ge=1),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service.project_access(db, user, project_id)
    service.case_for_project(db, project_id, case_id)
    rows = (
        db.query(CaseVersion)
        .filter(
            CaseVersion.project_id == project_id,
            CaseVersion.case_id == case_id,
            CaseVersion.version.in_([before, after]),
        )
        .all()
    )
    mapping = {row.version: row for row in rows}
    if before not in mapping or after not in mapping:
        raise HTTPException(404, "比较的版本不存在")
    left, right = mapping[before].snapshot, mapping[after].snapshot
    return result(
        dict(
            before=before,
            after=after,
            changes=[
                dict(field=field, before=left.get(field), after=right.get(field))
                for field in service.SNAPSHOT_FIELDS
                if left.get(field) != right.get(field)
            ],
        )
    )


@router.post("/cases/{case_id}/versions/{version_id}/restore")
def restore(
    project_id: str,
    case_id: str,
    version_id: str,
    body: RestoreVersion,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        transact(
            db,
            lambda: service.version_data(
                service.restore_version(db, user, project_id, case_id, version_id, body)
            ),
        ),
        "历史内容已恢复并保存为新版本",
    )


@router.get("/reviewers")
def reviewers(
    project_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    service.project_access(db, user, project_id)
    return result(service.reviewers(db, project_id))


@router.post("/reviews")
def create_review(
    project_id: str,
    body: ReviewCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        transact(
            db,
            lambda: service.review_data(
                db, service.create_review(db, user, project_id, body)
            ),
        )
    )


@router.get("/reviews")
def reviews(
    project_id: str,
    status: str | None = None,
    caseId: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service.project_access(db, user, project_id)
    query = db.query(CaseReview).filter_by(project_id=project_id)
    if status:
        query = query.filter(CaseReview.status == status)
    if search:
        query = query.filter(CaseReview.name.contains(search, autoescape=True))
    if caseId:
        service.case_for_project(db, project_id, caseId)
        query = query.join(
            CaseReviewItem, CaseReviewItem.review_id == CaseReview.id
        ).filter(CaseReviewItem.case_id == caseId)
    return result(
        [
            service.review_data(db, review)
            for review in query.order_by(CaseReview.created_at.desc()).all()
        ]
    )


@router.put("/reviews/{review_id}")
def edit_review(
    project_id: str,
    review_id: str,
    body: ReviewCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        transact(
            db,
            lambda: service.review_data(
                db, service.revise_review(db, user, project_id, review_id, body)
            ),
        )
    )


@router.post("/reviews/{review_id}/copy")
def copy_review(
    project_id: str,
    review_id: str,
    body: ReviewResubmit = ReviewResubmit(),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        transact(
            db,
            lambda: service.review_data(
                db, service.clone_review(db, user, project_id, review_id, body)
            ),
        )
    )


@router.post("/reviews/{review_id}/resubmit")
def resubmit_review(
    project_id: str,
    review_id: str,
    body: ReviewResubmit = ReviewResubmit(),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        transact(
            db,
            lambda: service.review_data(
                db, service.clone_review(db, user, project_id, review_id, body, True)
            ),
        )
    )


@router.post("/reviews/{review_id}/batch-decision")
def batch_vote(
    project_id: str,
    review_id: str,
    body: ReviewBatchVote,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    def operation():
        review = None
        vote = ReviewVote(decision=body.decision, comment=body.comment)
        for identifier in dict.fromkeys(body.itemIds):
            review = service.vote_review(
                db, user, project_id, review_id, identifier, vote
            )
        return service.review_data(db, review)

    return result(transact(db, operation))


@router.get("/reviews/{review_id}/follow")
def review_follow_state(
    project_id: str,
    review_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service.get_review(db, user, project_id, review_id)
    return result(
        {
            "followed": bool(
                db.query(CaseReviewFollow)
                .filter_by(review_id=review_id, user_id=str(user.id))
                .first()
            ),
            "count": db.query(CaseReviewFollow).filter_by(review_id=review_id).count(),
        }
    )


@router.post("/reviews/{review_id}/follow")
def follow_review(
    project_id: str,
    review_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service.get_review(db, user, project_id, review_id)

    def operation():
        if (
            not db.query(CaseReviewFollow)
            .filter_by(review_id=review_id, user_id=str(user.id))
            .first()
        ):
            db.add(CaseReviewFollow(review_id=review_id, user_id=str(user.id)))

    transact(db, operation)
    return result({"followed": True})


@router.delete("/reviews/{review_id}/follow")
def unfollow_review(
    project_id: str,
    review_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service.get_review(db, user, project_id, review_id)
    transact(
        db,
        lambda: db.query(CaseReviewFollow)
        .filter_by(review_id=review_id, user_id=str(user.id))
        .delete(),
    )
    return result({"followed": False})


@router.get("/reviews/{review_id}")
def review_detail(
    project_id: str,
    review_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        service.review_data(db, service.get_review(db, user, project_id, review_id))
    )


@router.post("/reviews/{review_id}/items/{item_id}/decision")
def vote(
    project_id: str,
    review_id: str,
    item_id: str,
    body: ReviewVote,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        transact(
            db,
            lambda: service.review_data(
                db, service.vote_review(db, user, project_id, review_id, item_id, body)
            ),
        )
    )


@router.post("/reviews/{review_id}/comments")
def comment(
    project_id: str,
    review_id: str,
    body: ReviewCommentCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    review = service.get_review(db, user, project_id, review_id)
    if (
        body.itemId
        and not db.query(CaseReviewItem)
        .filter_by(id=body.itemId, review_id=review.id)
        .first()
    ):
        raise HTTPException(404, "评审用例不存在")

    def operation():
        db.add(
            CaseReviewComment(
                review_id=review.id,
                item_id=body.itemId,
                author_id=str(user.id),
                content=body.content,
            )
        )
        db.flush()
        logger.info("评审意见已记录 review_id={} author_id={}", review.id, user.id)
        return service.review_data(db, review)

    return result(transact(db, operation))


@router.post("/reviews/{review_id}/cancel")
def cancel(
    project_id: str,
    review_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    review = service.get_review(db, user, project_id, review_id, lock=True)
    service.project_access(db, user, project_id, "update")
    if review.status != "pending":
        raise HTTPException(409, "评审已结束")

    def operation():
        review.status = "cancelled"
        db.flush()
        logger.info("评审已取消 review_id={} actor_id={}", review.id, user.id)
        return service.review_data(db, review)

    return result(transact(db, operation))


@router.post("/batch")
def batch(
    project_id: str,
    body: CaseBatchUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        dict(
            updated=transact(
                db, lambda: service.batch_update(db, user, project_id, body)
            )
        )
    )


@router.post("/batch-copy")
def batch_copy(
    project_id: str,
    body: CaseBatchCopy,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        dict(
            caseIds=transact(db, lambda: service.batch_copy(db, user, project_id, body))
        )
    )


def view_data(row):
    return dict(id=row.id, name=row.name, filters=row.filters)


@router.get("/views")
def views(
    project_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    service.project_access(db, user, project_id)
    rows = (
        db.query(CaseSavedView)
        .filter_by(project_id=project_id, owner_id=str(user.id))
        .order_by(CaseSavedView.created_at.desc())
        .all()
    )
    return result([view_data(row) for row in rows])


@router.post("/views")
def save_view(
    project_id: str,
    body: SavedViewCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service.project_access(db, user, project_id)

    def operation():
        row = CaseSavedView(
            project_id=project_id,
            owner_id=str(user.id),
            name=body.name,
            filters=body.filters,
        )
        db.add(row)
        db.flush()
        logger.info("个人筛选视图已保存 project_id={} owner_id={}", project_id, user.id)
        return view_data(row)

    return result(transact(db, operation))


@router.delete("/views/{view_id}")
def delete_view(
    project_id: str,
    view_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    service.project_access(db, user, project_id)
    row = (
        db.query(CaseSavedView)
        .filter_by(id=view_id, project_id=project_id, owner_id=str(user.id))
        .first()
    )
    if not row:
        raise HTTPException(404, "个人视图不存在")
    transact(db, lambda: db.delete(row))
    return result()
