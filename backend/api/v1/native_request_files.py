"""项目请求文件管理及有执行身份的Agent读取接口。"""

from urllib.parse import quote
from fastapi import APIRouter, Depends, File, UploadFile, Header, Response, Query
from sqlalchemy.orm import Session, defer
from database import get_db
from api.deps import get_current_user
from api.v1.case_governance import result, transact
from core.project_access import require_project_access
from models.native_request_file import NativeRequestFile
from services import native_request_files as service
from config import settings

router = APIRouter(
    prefix="/projects/{project_id}/native-cases/request-files", tags=["HTTP请求文件"]
)
agent_router = APIRouter(prefix="/native-http", tags=["原生执行文件传输"])


def response(row):
    return Response(
        row.content,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": "attachment; filename*=UTF-8''"
            + quote(row.file_name),
            "Cache-Control": "no-store",
            "X-Content-Type-Options": "nosniff",
        },
    )


@router.get("")
def listing(
    project_id: str,
    search: str = Query("", max_length=255),
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_project_access(db, user, project_id, "test_case:read")
    query = (
        db.query(NativeRequestFile)
        .options(defer(NativeRequestFile.content))
        .filter_by(project_id=project_id, deleted_at=None)
    )
    if search:
        query = query.filter(
            NativeRequestFile.file_name.contains(search, autoescape=True)
        )
    return result(
        dict(
            items=[
                service.metadata(row)
                for row in query.order_by(
                    NativeRequestFile.created_at.desc(), NativeRequestFile.id
                )
                .offset((page - 1) * size)
                .limit(size)
            ],
            total=query.count(),
            maxFileSize=settings.MAX_FILE_SIZE,
        )
    )


@router.post("")
def upload(
    project_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(transact(db, lambda: service.upload(db, user, project_id, file)))


@router.get("/{file_id}")
def metadata(
    project_id: str,
    file_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(
        service.metadata(service.get_user_file(db, user, project_id, file_id))
    )


@router.get("/{file_id}/download")
def download(
    project_id: str,
    file_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return response(service.get_user_file(db, user, project_id, file_id))


@router.delete("/{file_id}")
def remove(
    project_id: str,
    file_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return result(transact(db, lambda: service.remove(db, user, project_id, file_id)))


@agent_router.get("/executions/{execution_id}/files/{file_id}")
def agent_download(
    execution_id: str,
    file_id: str,
    x_agent_token: str | None = Header(None),
    db: Session = Depends(get_db),
):
    return response(service.get_agent_file(db, execution_id, file_id, x_agent_token))
