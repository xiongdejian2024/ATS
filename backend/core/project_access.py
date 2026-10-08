"""测试管理扩展共用的项目权限入口。"""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Project, ProjectMember, User
from core.permissions import has_global_permission, has_project_permission


def require_project_access(db: Session, user: User, project_id: str,
                           permission: str = "test_case:read", *, current_read=False) -> Project:
    project = (db.query(Project).filter_by(id=str(project_id)).populate_existing().with_for_update().one_or_none()
               if current_read else db.get(Project, str(project_id)))
    if not project:
        raise HTTPException(404, "项目不存在")
    if project_allows(db, user, project, permission, current_read=current_read):
        return project
    raise HTTPException(403, "没有此项目的操作权限")


def project_allows(db: Session, user: User, project: Project, permission: str, *, current_read=False) -> bool:
    """复用同一规则展示可操作按钮，最终写入仍须服务端授权。"""
    if not user.status:
        return False
    resource, action = permission.split(":", 1)
    if (str(user.id) in {project.owner_id, project.created_by}
            or has_global_permission(db, user.id, resource, action, current_read=current_read)
            or has_project_permission(db, user.id, project.id, resource, action, current_read=current_read)):
        return True
    query = db.query(ProjectMember).filter_by(project_id=project.id, user_id=user.id)
    member = (query.populate_existing().with_for_update() if current_read else query).first()
    if resource == "defect" and has_global_permission(db, user.id, "system", "manage", current_read=current_read):
        return True
    if member and ((action == "read" and resource != "defect") or member.role in {"admin", "owner", "manager", "maintainer"}):
        return True
    return False
