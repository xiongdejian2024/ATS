"""计划分类列表与关联管理接口。"""
from typing import Literal
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import get_db
from api.deps import get_current_user
from api.v1.plan_workspace import plan_access, ok
from api.v1.case_governance import transact
from core.project_access import require_project_access
from services import plan_case_workspace as service
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
    caseIds:list[str]=Field(min_length=1,max_length=500)
    collectionId:str|None=Field(None,max_length=36)
    suiteId:str|None=Field(None,max_length=36)

@router.get('/plans/{plan_id}/case-workspace')
def listing(plan_id:str,category:Category='functional',tree_type:Literal['COLLECTION','MODULE']='COLLECTION',folder:str|None=None,
            view:Literal['list','mind']='list',include_descendants:bool=True,search:str=Query('',max_length=255),priority:str|None=None,result:str|None=None,
            executor:str|None=None,tag:str|None=None,page:int=Query(1,ge=1),size:int=Query(20,ge=1,le=100),
            sort:Literal['caseCode','name','priority','createdAt','updatedAt','result']='createdAt',direction:Literal['asc','desc']='desc',
            db:Session=Depends(get_db),user=Depends(get_current_user)):
    plan=plan_access(db,user,plan_id)
    require_project_access(db,user,plan.project_id,'test_case:read')
    params=dict(view=view,tree_type=tree_type,folder=folder,include_descendants=include_descendants,search=search,priority=priority,result=result,executor=executor,tag=tag,page=page,size=size,sort=sort,direction=direction)
    return ok(service.listing(db,plan,category,params))

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
