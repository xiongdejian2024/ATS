from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from api.deps import get_current_user
from api.v1.case_governance import result, transact
from database import get_db
from schemas.request_environment_group import (
    EnvironmentGroupInput,
    EnvironmentGroupRevision,
)
from services import request_environment_group as service

router = APIRouter(
    prefix="/projects/{project_id}/request-environment-groups", tags=["请求环境组"]
)


@router.get("")
def listing(
    project_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None, max_length=255),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(service.catalog(db, user, project_id, page, size, search))


@router.get("/source-environments")
def source_environments(
    project_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return result(service.source_catalog(db, user, project_id))


@router.post("")
def create(
    project_id: str,
    body: EnvironmentGroupInput,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(transact(db, lambda: _save_response(db, user, project_id, body)))


@router.put("/{identity}")
def update(
    project_id: str,
    identity: str,
    body: EnvironmentGroupInput,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        transact(db, lambda: _save_response(db, user, project_id, body, identity))
    )


def _save_response(db, user, project_id, body, identity=None):
    row = service.save(db, user, project_id, body, identity)
    # Freeze this write's revision before commit expires the ORM instance.
    # A retried keyed create acknowledges the original creation, even if a
    # later writer has changed the current row. It must not grant that newer
    # revision to a stale creation draft.
    return dict(
        id=row.id, revision=1 if not identity and body.requestId else row.revision
    )


@router.delete("/{identity}")
def remove(
    project_id: str,
    identity: str,
    body: EnvironmentGroupRevision,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    transact(
        db,
        lambda: service.remove(db, user, project_id, identity, body.expectedRevision),
    )
    return result()
