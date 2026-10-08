"""固定 report-index 命名空间；当前用户/项目锁保护私人视图。"""
from types import SimpleNamespace
from fastapi import HTTPException
from models import User
from core.project_access import require_project_access
from services import plan_case_view

CATEGORY = "report-index"


def access(db,user,project_id,writing=False):
    if writing:
        user=db.query(User).filter_by(id=str(user.id)).populate_existing().with_for_update(read=True).one_or_none()
        if not user or not user.status: raise HTTPException(403,"用户不存在或已停用")
    require_project_access(db,user,project_id,"test_plan:read",current_read=writing)
    return user,SimpleNamespace(project_id=project_id)


def listing(db,user,project_id):
    user,scope=access(db,user,project_id)
    return [plan_case_view.data(row) for row in plan_case_view.scope(db,user,scope,CATEGORY).order_by(plan_case_view.PlanCaseSavedView.created_at.desc())]


def save(db,user,project_id,body,view_id=None):
    user,scope=access(db,user,project_id,True)
    return plan_case_view.save(db,user,scope,CATEGORY,body,view_id,permission="test_plan:read")


def remove(db,user,project_id,view_id):
    user,scope=access(db,user,project_id,True)
    plan_case_view.remove(db,user,scope,CATEGORY,view_id)
