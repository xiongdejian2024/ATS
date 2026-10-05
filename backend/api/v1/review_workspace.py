"""MeterSphere 风格的评审首页接口；调用原有版本评审服务。"""

from typing import Literal
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from api.deps import get_current_user
from database import get_db
from api.v1.case_governance import result, transact
from schemas.review_workspace import ModuleSave, ConfirmDelete, ReviewMove
from services import review_workspace as service
from schemas.case_governance import ReviewHeader

router = APIRouter(prefix="/review-workspace", tags=["评审首页"])


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
