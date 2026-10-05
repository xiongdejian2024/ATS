"""评审首页及关联用例工作区接口，复用既有版本和评审票。"""

from typing import Literal
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from api.deps import get_current_user
from database import get_db
from api.v1.case_governance import result, transact
from schemas.review_workspace import (
    ModuleSave,
    ConfirmDelete,
    ReviewMove,
    ReviewCandidateSelection,
    ReviewAssociate,
    ReviewItemSelection,
    ReviewItemReviewers,
    ReviewItemReReview,
    ReviewItemVote,
)
from services import review_workspace as service
from schemas.case_governance import ReviewHeader

router = APIRouter(prefix="/review-workspace", tags=["评审首页"])


@router.get("/{review_id}/detail")
def detail(
    project_id: str,
    review_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    from services.case_governance import get_review, review_data

    return result(
        review_data(
            db, get_review(db, user, project_id, review_id), include_items=False
        )
    )


@router.get("/{review_id}/items")
def linked_items(
    project_id: str,
    review_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: str = Query("", max_length=255),
    folder: str = "all",
    includeDescendants: bool = True,
    priority: Literal["P0", "P1", "P2", "P3"] | None = None,
    state: (
        Literal["approved", "rejected", "under_review", "un_review", "re_review"] | None
    ) = None,
    states: str | None = Query(None, max_length=100),
    reviewerId: str | None = None,
    creatorId: str | None = None,
    onlyMine: bool = False,
    sort: Literal["caseCode", "name", "createdAt"] = "createdAt",
    order: Literal["asc", "desc"] = "desc",
    view: Literal["list", "mind"] = "list",
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    from services.review_case_workspace import listing

    selected_states = [value.strip() for value in states.split(",")] if states else []
    if set(selected_states) - {
        "approved",
        "rejected",
        "under_review",
        "un_review",
        "re_review",
    }:
        raise HTTPException(422, "不支持的评审结果范围")
    return result(
        listing(
            db,
            user,
            project_id,
            review_id,
            page=page,
            size=size,
            search=search,
            folder=folder,
            include_descendants=includeDescendants,
            priority=priority,
            state=state,
            states=selected_states,
            reviewer_id=reviewerId,
            creator_id=creatorId,
            only_mine=onlyMine,
            sort=sort,
            order=order,
            view=view,
        )
    )


@router.get("/{review_id}/items/{item_id}")
def linked_item(
    project_id: str,
    review_id: str,
    item_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    from services.review_case_workspace import get_item

    return result(get_item(db, user, project_id, review_id, item_id))


@router.get("/{review_id}/items/{item_id}/reading")
def read_case(
    project_id: str,
    review_id: str,
    item_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    from services.review_reading import reading

    return result(reading(db, user, project_id, review_id, item_id))


@router.post("/{review_id}/item-reviewers")
def change_item_reviewers(
    project_id: str,
    review_id: str,
    body: ReviewItemReviewers,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    from services.review_item_management import change_reviewers
    from services.review_item_selection import apply

    return result(
        transact(
            db,
            lambda: apply(
                db,
                user,
                project_id,
                review_id,
                body,
                lambda selected: change_reviewers(
                    db, user, project_id, review_id, selected
                ),
            ),
        )
    )


@router.post("/{review_id}/disassociate")
def disassociate_items(
    project_id: str,
    review_id: str,
    body: ReviewItemSelection,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    from services.review_item_management import disassociate
    from services.review_item_selection import apply

    return result(
        transact(
            db,
            lambda: apply(
                db,
                user,
                project_id,
                review_id,
                body,
                lambda selected: disassociate(
                    db, user, project_id, review_id, selected
                ),
            ),
        )
    )


@router.post("/{review_id}/re-review")
def re_review_items(
    project_id: str,
    review_id: str,
    body: ReviewItemReReview,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    from services.review_item_management import re_review
    from services.review_item_selection import apply

    return result(
        transact(
            db,
            lambda: apply(
                db,
                user,
                project_id,
                review_id,
                body,
                lambda selected: re_review(db, user, project_id, review_id, selected),
            ),
        )
    )


@router.post("/{review_id}/item-selection")
def item_selection(
    project_id: str,
    review_id: str,
    body: ReviewItemSelection,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    from services.review_item_selection import preview

    return result(preview(db, user, project_id, review_id, body))


@router.post("/{review_id}/selection-case-ids")
def selection_case_ids(
    project_id: str,
    review_id: str,
    body: ReviewItemSelection,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    from services.review_item_selection import selected_cases

    return result(selected_cases(db, user, project_id, review_id, body))


@router.post("/{review_id}/batch-decision")
def selected_vote(
    project_id: str,
    review_id: str,
    body: ReviewItemVote,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    from services.review_item_selection import vote

    return result(transact(db, lambda: vote(db, user, project_id, review_id, body)))


@router.put("/{review_id}/header")
def update_header(
    project_id: str,
    review_id: str,
    body: ReviewHeader,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        transact(
            db, lambda: service.update_header(db, user, project_id, review_id, body)
        )
    )


@router.post("/{review_id}/associate")
def associate_cases(
    project_id: str,
    review_id: str,
    body: ReviewAssociate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        transact(
            db, lambda: service.associate_cases(db, user, project_id, review_id, body)
        )
    )


@router.get("/candidates")
def candidates(
    project_id: str,
    search: str = Query("", max_length=255),
    folder: str = "all",
    priority: Literal["P0", "P1", "P2", "P3"] | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    from services.case_governance import project_access
    from services.case_candidates import candidates as shared_candidates

    project_access(db, user, project_id)
    return result(
        shared_candidates(
            db, project_id, "functional", search, folder, priority, page, size
        )
    )


@router.post("/candidate-selection")
def select_candidates(
    project_id: str,
    body: ReviewCandidateSelection,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    from fastapi import HTTPException
    from services.case_governance import project_access
    from services.case_candidates import candidate_query
    from models import TestCase
    from core.logger import logger

    project_access(db, user, project_id, "update")
    query, _, _, _ = candidate_query(
        db, project_id, "functional", body.search, body.folder, body.priority
    )
    excluded = set(body.excludeIds)
    if body.selectionScope:
        from services.case_selection import resolve

        scoped, _ = resolve(db, user, project_id, body.selectionScope)
        excluded.update(case.id for case in scoped)
    query = query.filter(TestCase.id.notin_(excluded))
    total = query.count()
    if total + len(excluded) > 10000:
        raise HTTPException(422, "一个评审最多关联10000个用例，请缩小筛选范围")
    identifiers = [
        row[0]
        for row in query.with_entities(TestCase.id)
        .order_by(TestCase.created_at.desc(), TestCase.id)
        .all()
    ]
    logger.info(
        "评审草稿全选筛选结果 project_id={} count={} actor_id={}",
        project_id,
        len(identifiers),
        user.id,
    )
    return result(dict(caseIds=identifiers, total=len(identifiers)))


@router.get("")
def reviews(
    project_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    scope: Literal["all", "reviewByMe", "createByMe"] = "all",
    moduleId: str | None = None,
    includeDescendants: bool = True,
    search: str = Query("", max_length=200),
    lifecycle: (
        Literal[
            "prepared", "underway", "completed", "archived", "cancelled", "superseded"
        ]
        | None
    ) = None,
    mode: Literal["single", "multiple"] | None = None,
    reviewerId: str | None = None,
    creatorId: str | None = None,
    sort: Literal["number", "name", "createdAt", "passRate"] = "createdAt",
    order: Literal["asc", "desc"] = "desc",
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        service.list_reviews(
            db,
            user,
            project_id,
            page=page,
            size=size,
            scope=scope,
            module_id=moduleId,
            include_descendants=includeDescendants,
            search=search,
            lifecycle=lifecycle,
            mode=mode,
            reviewer_id=reviewerId,
            creator_id=creatorId,
            sort=sort,
            order=order,
        )
    )


@router.post("/modules")
def create_module(
    project_id: str,
    body: ModuleSave,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(transact(db, lambda: service.save_module(db, user, project_id, body)))


@router.put("/modules/{module_id}")
def update_module(
    project_id: str,
    module_id: str,
    body: ModuleSave,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        transact(db, lambda: service.save_module(db, user, project_id, body, module_id))
    )


@router.post("/modules/{module_id}/delete")
def delete_module(
    project_id: str,
    module_id: str,
    body: ConfirmDelete,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        transact(
            db, lambda: service.delete_module(db, user, project_id, module_id, body)
        )
    )


@router.post("/move")
def move(
    project_id: str,
    body: ReviewMove,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        transact(db, lambda: service.move_reviews(db, user, project_id, body))
    )


@router.post("/{review_id}/delete")
def delete(
    project_id: str,
    review_id: str,
    body: ConfirmDelete,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        transact(
            db, lambda: service.delete_review(db, user, project_id, review_id, body)
        )
    )


@router.post("/{review_id}/archive")
def archive(
    project_id: str,
    review_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        transact(db, lambda: service.archive_review(db, user, project_id, review_id))
    )
