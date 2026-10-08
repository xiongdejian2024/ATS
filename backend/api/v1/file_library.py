"""Shared file directory/picker APIs. No permanent deletion route."""
from fastapi import APIRouter, Depends, File, UploadFile, Query, Form
from sqlalchemy.orm import Session
from sqlalchemy import or_
from pydantic import BaseModel, ConfigDict, Field, StrictBool
from database import get_db
from api.deps import get_current_user
from core.project_access import require_project_access
from models.file_library import LibraryFile, LibraryReference
from services import file_library as service
from api.v1.case_governance import result, transact

router = APIRouter(prefix='/projects/{project_id}/file-library', tags=['共享文件库'])

class FolderInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str = Field(min_length=1, max_length=255)
    parentId: str | None = Field(default=None, max_length=36)

class ArchiveInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    archived: StrictBool

class ReferenceInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    fileIds: list[str] = Field(min_length=1, max_length=50)

@router.get('/folders')
def folders(project_id: str, db: Session=Depends(get_db), user=Depends(get_current_user)):
    service.require_library_read(db,user,project_id)
    return result(service.folders(db,project_id))

@router.post('/folders')
def create_folder(project_id: str, body: FolderInput, db: Session=Depends(get_db), user=Depends(get_current_user)):
    return result(transact(db,lambda: service.write_folder(db,user,project_id,body.name,body.parentId)))

@router.put('/folders/{identifier}')
def update_folder(project_id: str, identifier: str, body: FolderInput, db: Session=Depends(get_db), user=Depends(get_current_user)):
    return result(transact(db,lambda: service.write_folder(db,user,project_id,body.name,body.parentId,identifier)))

@router.get('/files')
def files(project_id: str, folderId: str | None=None, search: str=Query('',max_length=255), archived: bool=False, imagesOnly: bool=False, page: int=Query(1,ge=1), db: Session=Depends(get_db), user=Depends(get_current_user)):
    service.require_library_read(db,user,project_id);service.folder(db,project_id,folderId)
    rows=db.query(LibraryFile).filter_by(project_id=project_id,folder_id=folderId or None,archived=archived).filter(or_(LibraryFile.published.is_(True),LibraryFile.uploaded_by==str(user.id)))
    if imagesOnly: rows=rows.filter(LibraryFile.mime_type.in_(list(service.IMAGE_TYPES.values())))
    if search.strip(): rows=rows.filter(LibraryFile.file_name.contains(search.strip(),autoescape=True))
    total=rows.count();items=rows.order_by(LibraryFile.created_at.desc(),LibraryFile.id).offset((page-1)*20).limit(20).all()
    from core.project_access import project_allows
    from models import Project
    return result(dict(items=[service.data(r) for r in items],total=total,page=page,size=20,canManage=project_allows(db,user,db.get(Project,project_id),'test_case:update')))

@router.post('/files')
def upload(project_id: str, file: UploadFile=File(...), folderId: str | None=Form(None), image: bool=Form(False), published: bool=Form(False), db: Session=Depends(get_db), user=Depends(get_current_user)):
    return result(service.upload(db,user,project_id,file,folderId,image,published))

@router.get('/files/{identifier}/{operation}')
def download(project_id: str, identifier: str, operation: str, db: Session=Depends(get_db), user=Depends(get_current_user)):
    from fastapi import HTTPException
    if operation not in {'download','preview'}: raise HTTPException(404,'文件操作不存在')
    service.require_library_read(db,user,project_id)
    row=service.find(db,project_id,identifier)
    if not row.published and row.uploaded_by != str(user.id): raise HTTPException(403,'此文件尚未发布到项目库')
    return service.download(db,row,operation=='preview')

@router.put('/files/{identifier}/archive')
def archive(project_id: str, identifier: str, body: ArchiveInput, db: Session=Depends(get_db), user=Depends(get_current_user)):
    require_project_access(db,user,project_id,'test_case:update')
    def operation():
        row=service.find(db,project_id,identifier,lock=True);row.archived=body.archived;db.flush();return service.data(row)
    return result(transact(db,operation))

@router.get('/cases/{case_id}/references')
def case_references(project_id: str, case_id: str, db: Session=Depends(get_db), user=Depends(get_current_user)):
    from services.case_features import find_case
    find_case(db,user,project_id,case_id)
    return result(service.references(db,project_id,'case',case_id))

@router.post('/cases/{case_id}/references')
def link_case(project_id: str, case_id: str, body: ReferenceInput, db: Session=Depends(get_db), user=Depends(get_current_user)):
    from services.case_features import find_case
    def operation():
        case=find_case(db,user,project_id,case_id,permission='update',lock=True)
        from services.case_features import change
        change(db,case,user.id,'关联文件库',{'fileIds':sorted(set(body.fileIds))})
        service.reference(db,user,project_id,body.fileIds,'case',case_id)
        return service.references(db,project_id,'case',case_id)
    return result(transact(db,operation))


@router.delete('/cases/{case_id}/references/{identifier}')
def unlink_case(project_id: str, case_id: str, identifier: str, db: Session=Depends(get_db), user=Depends(get_current_user)):
    from services.case_features import find_case, change
    def operation():
        case=find_case(db,user,project_id,case_id,permission='update',lock=True)
        service.find(db,project_id,identifier,lock=True)
        row=db.query(LibraryReference).filter_by(file_id=identifier,entity_kind='case',entity_id=case_id).with_for_update().first()
        if row: row.active=False
        change(db,case,user.id,'取消文件库关联',{'fileId':identifier})
    transact(db,operation)
    return result()
