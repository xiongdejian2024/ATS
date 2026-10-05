"""计划分类列表与关联管理接口。"""
from typing import Literal
from uuid import UUID
from fastapi import APIRouter, Depends, Query, UploadFile, File
from fastapi.responses import Response
from urllib.parse import quote
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import get_db
from api.deps import get_current_user
from api.v1.plan_workspace import plan_access, ok
from api.v1.case_governance import transact
from core.project_access import require_project_access
from services import plan_case_workspace as service
from schemas.plan_case_execution import ExecuteInput
router=APIRouter()
Category=Literal['functional','api','scenario']
class Selection(BaseModel):
    source:Literal['legacy','node']
    id:str=Field(min_length=1,max_length=36)
class Batch(BaseModel):
    category:Category='functional'
    action:Literal['assign','move','unlink']
    selections:list[Selection]=Field(min_length=1,max_length=500)
    assignedTo:str|None=Field(None,max_length=36)
    collectionId:str|None=Field(None,max_length=36)
class Association(BaseModel):
    category:Category='functional'
    caseIds:list[str]=Field(min_length=1,max_length=500)
    collectionId:str|None=Field(None,max_length=36)
    suiteId:str|None=Field(None,max_length=36)

@router.get('/plans/{plan_id}/case-workspace/candidates')
def candidates(plan_id:str,category:Category='functional',search:str=Query('',max_length=255),
               folder:str='all',priority:str|None=None,page:int=Query(1,ge=1),size:int=Query(20,ge=1,le=100),
               db:Session=Depends(get_db),user=Depends(get_current_user)):
    plan=plan_access(db,user,plan_id)
    require_project_access(db,user,plan.project_id,'test_case:read')
    return ok(service.candidates(db,plan,category,search,folder,priority,page,size))

@router.get('/plans/{plan_id}/case-workspace')
def listing(plan_id:str,category:Category='functional',tree_type:Literal['COLLECTION','MODULE']='COLLECTION',folder:str|None=None,
            view:Literal['list','mind']='list',include_descendants:bool=True,search:str=Query('',max_length=255),priority:str|None=None,result:str|None=None,
            executor:str|None=None,tag:str|None=None,page:int=Query(1,ge=1),size:int=Query(20,ge=1,le=100),
            sort:Literal['caseCode','name','priority','createdAt','updatedAt','result']='createdAt',direction:Literal['asc','desc']='desc',
            db:Session=Depends(get_db),user=Depends(get_current_user)):
    plan=plan_access(db,user,plan_id)
    require_project_access(db,user,plan.project_id,'test_case:read')
    params=dict(view=view,tree_type=tree_type,folder=folder,include_descendants=include_descendants,search=search,priority=priority,result=result,executor=executor,tag=tag,page=page,size=size,sort=sort,direction=direction)
    from services.plan_case_execution import can_execute
    payload = service.listing(db,plan,category,params)
    payload["canExecute"] = can_execute(db,user,plan)
    return ok(payload)

@router.post('/plans/{plan_id}/case-workspace/batch')
def batch(plan_id:str,data:Batch,db:Session=Depends(get_db),user=Depends(get_current_user)):
    plan=plan_access(db,user,plan_id,'update')
    require_project_access(db,user,plan.project_id,'test_case:read')
    return ok(transact(db,lambda:service.batch(db,plan,user,data)))

@router.post('/plans/{plan_id}/case-workspace/associate')
def associate(plan_id:str,data:Association,db:Session=Depends(get_db),user=Depends(get_current_user)):
    plan=plan_access(db,user,plan_id,'update')
    require_project_access(db,user,plan.project_id,'test_case:read')
    return ok(transact(db,lambda:service.associate(db,plan,user,data)))


@router.post('/plans/{plan_id}/case-workspace/execute')
def execute_cases(plan_id: str, data: 'ExecuteInput', db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_case_execution import execute
    plan = plan_access(db,user,plan_id,'execute')
    require_project_access(db,user,plan.project_id,'test_case:read')
    return ok(transact(db,lambda:execute(db,user,plan,data)))


@router.get('/plans/{plan_id}/case-workspace/execution')
def execution_detail(plan_id: str, source: Literal['legacy','node'], associationId: str = Query(min_length=1,max_length=36), caseId: str = Query(min_length=1,max_length=36),
                     page: int = Query(1,ge=1), size: int = Query(20,ge=1,le=100), db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_case_execution import detail
    plan = plan_access(db,user,plan_id)
    require_project_access(db,user,plan.project_id,'test_case:read')
    return ok(detail(db,user,plan,source,associationId,caseId,page,size))


@router.post('/plans/{plan_id}/execution-media')
def upload_execution_image(plan_id: str, file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_case_media import upload
    plan=plan_access(db,user,plan_id,'execute')
    require_project_access(db,user,plan.project_id,'test_case:read')
    return ok(transact(db,lambda:upload(db,user,plan,file)))


class CleanupImages(BaseModel):
    ids: list[UUID] = Field(min_length=1, max_length=500)


@router.post('/plans/{plan_id}/execution-media/cleanup')
def cleanup_execution_images(plan_id: str, data: CleanupImages, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_case_media import cleanup_owned
    # 只收尾本人的未引用文件；归档或执行权限改变后也可释放自己的草稿。
    plan = plan_access(db,user,plan_id)
    require_project_access(db,user,plan.project_id,'test_case:read')
    return ok(transact(db,lambda:cleanup_owned(db,user,plan,[str(identifier) for identifier in data.ids])))


def execution_image(db,user,plan_id,media_id):
    from services.plan_case_media import find
    plan=plan_access(db,user,plan_id)
    require_project_access(db,user,plan.project_id,'test_case:read')
    return find(db,user,plan,media_id)


@router.get('/plans/{plan_id}/execution-media/{media_id}/preview')
def preview_execution_image(plan_id: str, media_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    row=execution_image(db,user,plan_id,media_id)
    return Response(row.content,media_type=row.mime_type,headers={'X-Content-Type-Options':'nosniff','Cache-Control':'private, no-store'})


@router.get('/plans/{plan_id}/execution-media/{media_id}/download')
def download_execution_image(plan_id: str, media_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    row=execution_image(db,user,plan_id,media_id)
    return Response(row.content,media_type='application/octet-stream',headers={'Content-Disposition':"attachment; filename*=UTF-8''"+quote(row.file_name,safe=''),'X-Content-Type-Options':'nosniff','Cache-Control':'private, no-store'})


@router.delete('/plans/{plan_id}/execution-media/{media_id}')
def delete_execution_image(plan_id: str, media_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_case_media import remove
    plan=plan_access(db,user,plan_id,'execute')
    require_project_access(db,user,plan.project_id,'test_case:read')
    return ok(transact(db,lambda:remove(db,user,plan,media_id)))
