"""Independent defect workspace APIs; project/actor checks live inside transactions."""

from typing import Literal
from fastapi import APIRouter, Depends, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from api.deps import get_current_user
from api.v1.case_governance import result, transact
from schemas.defect_workspace import (
    DefectWrite,
    DefectTemplateWrite,
    RevisionInput,
    ArchiveInput,
    DefectCommentWrite,
)
from services import defect_workspace as service

router = APIRouter(prefix="/projects/{project_id}/defects", tags=["缺陷工作区"])


@router.get("")
def list_defects(
    project_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: str = Query("", max_length=255),
    status: Literal["open", "in_progress", "resolved", "closed"] | None = None,
    archived: bool = False,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        transact(
            db, lambda: service.listing(db, user, project_id, page, size, search, status, archived)
        )
    )


@router.get("/templates")
def templates(project_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return result(transact(db, lambda: service.templates(db, user, project_id)))


@router.post("/templates")
def create_template(
    project_id: str,
    body: DefectTemplateWrite,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(transact(db, lambda: service.save_template(db, user, project_id, body)))


@router.put("/templates/{identifier}")
def edit_template(
    project_id: str,
    identifier: str,
    body: DefectTemplateWrite,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        transact(db, lambda: service.save_template(db, user, project_id, body, identifier))
    )


@router.delete("/templates/{identifier}")
def delete_template(
    project_id: str,
    identifier: str,
    body: RevisionInput,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        transact(
            db,
            lambda: service.remove_template(
                db, user, project_id, identifier, body.expectedRevision
            ),
        )
    )


@router.post("")
def create_defect(
    project_id: str,
    body: DefectWrite,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(transact(db, lambda: service.save(db, user, project_id, body)))


@router.get("/{identifier}")
def detail(
    project_id: str, identifier: str, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return result(transact(db, lambda: service.detail(db, user, project_id, identifier)))


@router.put("/{identifier}")
def edit_defect(
    project_id: str,
    identifier: str,
    body: DefectWrite,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(transact(db, lambda: service.save(db, user, project_id, body, identifier)))


@router.put("/{identifier}/archive")
def archive(
    project_id: str,
    identifier: str,
    body: ArchiveInput,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        transact(db, lambda: service.set_archived(db, user, project_id, identifier, body))
    )


@router.get("/{identifier}/comments")
def comments(
    project_id: str,
    identifier: str,
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(transact(db, lambda: service.comments(db, user, project_id, identifier, page)))


@router.post("/{identifier}/comments")
def comment(
    project_id: str,
    identifier: str,
    body: DefectCommentWrite,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(transact(db, lambda: service.add_comment(db, user, project_id, identifier, body)))


@router.delete("/{identifier}/comments/{comment_id}")
def remove_comment(
    project_id: str,
    identifier: str,
    comment_id: str,
    body: RevisionInput,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        transact(
            db,
            lambda: service.delete_comment(
                db, user, project_id, identifier, comment_id, body.expectedRevision
            ),
        )
    )


@router.get("/{identifier}/history")
def history(
    project_id: str,
    identifier: str,
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(transact(db, lambda: service.history(db, user, project_id, identifier, page)))
