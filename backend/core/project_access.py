"""测试管理扩展共用的项目权限入口。"""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Project, ProjectMember, User
from core.permissions import has_global_permission, has_project_permission


def require_project_access(db: Session, user: User, project_id: str,
                           permission: str = "test_case:read") -> Project:
    project = db.get(Project, str(project_id))
    if not project:
        raise HTTPException(404, "项目不存在")
    resource, action = permission.split(":", 1)
    if (str(user.id) in {project.owner_id, project.created_by}
            or has_global_permission(db, user.id, resource, action)
            or has_project_permission(db, user.id, project.id, resource, action)):
        return project
    member = db.query(ProjectMember).filter_by(project_id=project.id, user_id=user.id).first()
    if member and (action == "read" or member.role in {"admin", "owner", "manager", "maintainer"}):
        return project
    raise HTTPException(403, "没有此项目的操作权限")
