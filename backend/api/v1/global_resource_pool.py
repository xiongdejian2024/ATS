from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from api.deps import get_current_user
from api.v1.case_governance import result, transact
from schemas.global_resource_pool import PoolInput, PoolRevision, PoolEnable
from services import global_resource_pool as service

router = APIRouter(prefix="/resource-pools", tags=["独立执行资源池"])


@router.get("")
def catalog(
    projectId: str | None = Query(None, max_length=36),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None, max_length=255),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(service.catalog(db, user, projectId, page, size, search))


@router.get("/nodes")
def nodes(
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    search: str | None = Query(None, max_length=255),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(service.node_catalog(db, user, page, size, search))


@router.post("")
def create(body: PoolInput, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return result(transact(db, lambda: service.save(db, user, body)))


@router.put("/{identity}")
def update(
    identity: str, body: PoolInput, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return result(transact(db, lambda: service.save(db, user, body, identity)))


@router.put("/{identity}/enabled")
def enabled(
    identity: str, body: PoolEnable, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return result(transact(db, lambda: service.set_enabled(db, user, identity, body)))


@router.delete("/{identity}")
def remove(
    identity: str, body: PoolRevision, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    transact(db, lambda: service.remove(db, user, identity, body.expectedRevision))
    return result()
