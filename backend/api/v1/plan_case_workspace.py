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
from schemas.plan_case_view import PlanCaseViewCreate, PlanCaseViewUpdate
from schemas.plan_candidate_view import CandidateViewCreate, CandidateViewUpdate
from schemas.plan_candidate_selection import Association, CandidateSelection
from services import plan_case_view as views_service
from services.plan_candidate_project import source_scope, projects
from schemas.plan_native_selection import NativeWorkspaceSelection, NativeWorkspaceBatch, NativeWorkspaceRun
router=APIRouter()
Category=Literal['functional','api','scenario']
ResourceType=Literal['CASE','API']


def candidate_view_scope(category, resource_type):
    if resource_type == 'API':
        if category != 'api':
            from fastapi import HTTPException
            raise HTTPException(422, '接口模式只适用于API分类')
        return 'api-definition'
    return category + '-drawer'


def candidate_view_filters(filters, category, resource_type):
    candidate_view_scope(category, resource_type)
    if resource_type == 'API':
        from services.plan_definition_candidates import parse_definition_filters
        return parse_definition_filters(filters)
    from services.plan_candidate_filter import parse_candidate_filters
    return parse_candidate_filters(filters, category)

class Selection(BaseModel):
    source:Literal['legacy','node']
    id:str=Field(min_length=1,max_length=36)
class Batch(BaseModel):
    category:Category='functional'
    action:Literal['assign','move','unlink']
    selections:list[Selection]=Field(min_length=1,max_length=500)
    assignedTo:str|None=Field(None,max_length=36)
    collectionId:str|None=Field(None,max_length=36)

@router.post('/plans/{plan_id}/case-workspace/candidates/selection')
def candidate_selection(plan_id: str, data: CandidateSelection, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_candidate_selection import preview
    plan = plan_access(db, user, plan_id)
    require_project_access(db, user, plan.project_id, 'test_case:read')
    return ok(preview(db, plan, user, data))

@router.get('/plans/{plan_id}/case-workspace/candidates/projects')
def candidate_projects(plan_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return ok(projects(db, user, plan_access(db, user, plan_id)))


@router.get('/plans/{plan_id}/case-workspace/candidates')
def candidates(plan_id:str,category:Category='functional',resourceType:ResourceType='CASE',search:str=Query('',max_length=255),
               folder:str='all',priority:str|None=None,protocols:str|None=Query(None,max_length=5000),methods:str|None=Query(None,max_length=5000),createdBy:str|None=Query(None,max_length=5000),sort:Literal['id','name','createdAt']|None=None,direction:Literal['asc','desc']='asc',page:int=Query(1,ge=1),size:int=Query(20,ge=1,le=100),
               filters:str|None=Query(None,max_length=30000),mine:bool=False,projectId:str|None=Query(None,min_length=1,max_length=36),db:Session=Depends(get_db),user=Depends(get_current_user)):
    plan=plan_access(db,user,plan_id)
    require_project_access(db,user,plan.project_id,'test_case:read')
    candidate_view_scope(category, resourceType)
    source, _ = source_scope(db, user, plan, projectId)
    import json
    from schemas.plan_candidate_selection import CandidateCondition
    from fastapi import HTTPException
    from pydantic import ValidationError
    try:
        condition = CandidateCondition(protocols=None if protocols is None else protocols.split(',') if protocols else [], methods=methods.split(',') if methods else [], createdBy=createdBy.split(',') if createdBy else [], filters=None if filters is None else json.loads(filters), mine=mine)
    except (ValidationError, ValueError) as exception:
        from core.logger import logger
        logger.exception('关联窗口基础筛选参数无效')
        raise HTTPException(422, '关联窗口筛选参数无效') from exception
    return ok(service.candidates(db,plan,category,search,folder,priority,page,size,filters=filters,mine=mine,user_id=str(user.id), source=source, resource_type=resourceType, condition=condition, sort=sort, direction=direction))

@router.get('/plans/{plan_id}/case-workspace')
def listing(plan_id:str,category:Category='functional',tree_type:Literal['COLLECTION','MODULE']='COLLECTION',folder:str|None=None,
            view:Literal['list','mind']='list',include_descendants:bool=True,search:str=Query('',max_length=255),priority:str|None=None,result:str|None=None,
            executor:str|None=None,tag:str|None=None,protocols:str|None=Query(None,max_length=1000),page:int=Query(1,ge=1),size:int=Query(20,ge=1,le=100),
            sort:Literal['caseCode','name','priority','createdAt','updatedAt','result']='createdAt',direction:Literal['asc','desc']='desc',
            filters:str|None=Query(None,max_length=30000),refine:bool=False,mine:bool=False,db:Session=Depends(get_db),user=Depends(get_current_user)):
    plan=plan_access(db,user,plan_id)
    require_project_access(db,user,plan.project_id,'test_case:read')
    if protocols is not None and category != 'api':
        from fastapi import HTTPException
        raise HTTPException(422, '协议筛选只适用于API用例')
    params=dict(view=view,tree_type=tree_type,folder=folder,include_descendants=include_descendants,search=search,priority=priority,result=result,executor=executor,tag=tag,protocols=protocols,page=page,size=size,sort=sort,direction=direction,filters=filters,user_id=str(user.id),refine=refine,mine=mine)
    from services.plan_case_execution import can_execute
    payload = service.listing(db,plan,category,params)
    payload["canExecute"] = can_execute(db,user,plan)
    return ok(payload)


def view_access(db, user, plan_id):
    plan = plan_access(db, user, plan_id)
    require_project_access(db, user, plan.project_id, 'test_case:read')
    return plan


@router.get('/plans/{plan_id}/case-workspace/candidates/views')
def candidate_views(plan_id: str, category: Category = 'functional', resourceType: ResourceType = 'CASE', projectId: str | None = Query(None, min_length=1, max_length=36), db: Session = Depends(get_db), user=Depends(get_current_user)):
    plan = view_access(db, user, plan_id)
    plan, _ = source_scope(db, user, plan, projectId)
    rows = views_service.scope(db, user, plan, candidate_view_scope(category, resourceType)).order_by(views_service.PlanCaseSavedView.created_at.desc()).all()
    return ok([views_service.data(row) for row in rows])


@router.post('/plans/{plan_id}/case-workspace/candidates/views')
def create_candidate_view(plan_id: str, body: CandidateViewCreate, category: Category = 'functional', resourceType: ResourceType = 'CASE', projectId: str | None = Query(None, min_length=1, max_length=36), db: Session = Depends(get_db), user=Depends(get_current_user)):
    plan = view_access(db, user, plan_id)
    plan, _ = source_scope(db, user, plan, projectId)
    candidate_view_filters(dict(conditions=body.filters.get('filterConditions', []), logic=body.filters.get('filterLogic', 'and')), category, resourceType)
    return ok(transact(db, lambda: views_service.save(db, user, plan, candidate_view_scope(category, resourceType), body)))


@router.put('/plans/{plan_id}/case-workspace/candidates/views/{view_id}')
def update_candidate_view(plan_id: str, view_id: str, body: CandidateViewUpdate, category: Category = 'functional', resourceType: ResourceType = 'CASE', projectId: str | None = Query(None, min_length=1, max_length=36), db: Session = Depends(get_db), user=Depends(get_current_user)):
    plan = view_access(db, user, plan_id)
    plan, _ = source_scope(db, user, plan, projectId)
    if body.filters is not None:
        candidate_view_filters(dict(conditions=body.filters.get('filterConditions', []), logic=body.filters.get('filterLogic', 'and')), category, resourceType)
    return ok(transact(db, lambda: views_service.save(db, user, plan, candidate_view_scope(category, resourceType), body, view_id)))


@router.delete('/plans/{plan_id}/case-workspace/candidates/views/{view_id}')
def delete_candidate_view(plan_id: str, view_id: str, category: Category = 'functional', resourceType: ResourceType = 'CASE', projectId: str | None = Query(None, min_length=1, max_length=36), db: Session = Depends(get_db), user=Depends(get_current_user)):
    plan = view_access(db, user, plan_id)
    plan, _ = source_scope(db, user, plan, projectId)
    transact(db, lambda: views_service.remove(db, user, plan, candidate_view_scope(category, resourceType), view_id))
    return ok()


@router.get('/plans/{plan_id}/case-workspace/views')
def views(plan_id: str, category: Category = 'functional', db: Session = Depends(get_db), user=Depends(get_current_user)):
    plan = view_access(db, user, plan_id)
    rows = views_service.scope(db, user, plan, category).order_by(views_service.PlanCaseSavedView.created_at.desc()).all()
    return ok([views_service.data(row) for row in rows])


@router.post('/plans/{plan_id}/case-workspace/views')
def create_view(plan_id: str, body: PlanCaseViewCreate, category: Category = 'functional', db: Session = Depends(get_db), user=Depends(get_current_user)):
    plan = view_access(db, user, plan_id)
    from services.plan_case_filter import parse_plan_filters
    parse_plan_filters(dict(conditions=body.filters.get('filterConditions', []), logic=body.filters.get('filterLogic', 'and')), category)
    return ok(transact(db, lambda: views_service.save(db, user, plan, category, body)))


@router.put('/plans/{plan_id}/case-workspace/views/{view_id}')
def update_view(plan_id: str, view_id: str, body: PlanCaseViewUpdate, category: Category = 'functional', db: Session = Depends(get_db), user=Depends(get_current_user)):
    plan = view_access(db, user, plan_id)
    from services.plan_case_filter import parse_plan_filters
    if body.filters is not None:
        parse_plan_filters(dict(conditions=body.filters.get('filterConditions', []), logic=body.filters.get('filterLogic', 'and')), category)
    return ok(transact(db, lambda: views_service.save(db, user, plan, category, body, view_id)))


@router.delete('/plans/{plan_id}/case-workspace/views/{view_id}')
def delete_view(plan_id: str, view_id: str, category: Category = 'functional', db: Session = Depends(get_db), user=Depends(get_current_user)):
    plan = view_access(db, user, plan_id)
    transact(db, lambda: views_service.remove(db, user, plan, category, view_id))
    return ok()

@router.post('/plans/{plan_id}/case-workspace/batch')
def batch(plan_id:str,data:Batch,db:Session=Depends(get_db),user=Depends(get_current_user)):
    plan=plan_access(db,user,plan_id,'update')
    require_project_access(db,user,plan.project_id,'test_case:read')
    return ok(transact(db,lambda:service.batch(db,plan,user,data)))


@router.post('/plans/{plan_id}/case-workspace/selection')
def native_selection(plan_id: str, data: NativeWorkspaceSelection, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_native_selection import preview
    return ok(preview(db, plan_access(db,user,plan_id), user, data))


@router.post('/plans/{plan_id}/case-workspace/batch-range')
def native_batch_range(plan_id: str, data: NativeWorkspaceBatch, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_native_selection import apply
    plan = plan_access(db,user,plan_id,'update')
    return ok(transact(db,lambda:apply(db,plan,user,data)))

@router.post('/plans/{plan_id}/case-workspace/run-range')
def native_run_range(plan_id: str, data: NativeWorkspaceRun, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_native_run import start
    from services.plan_orchestration import run_data
    from core.logger import logger
    from fastapi import HTTPException
    plan = plan_access(db, user, plan_id, 'execute')
    try:
        run = start(db, plan, user, data)
        db.commit()
        return ok(run_data(db, run))
    except ValueError as exception:
        db.rollback()
        logger.exception('原生计划范围执行校验失败：计划={}', plan_id)
        raise HTTPException(409, str(exception)) from exception
    except Exception:
        db.rollback()
        logger.exception('原生计划范围执行失败，整批已回滚：计划={}', plan_id)
        raise


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
