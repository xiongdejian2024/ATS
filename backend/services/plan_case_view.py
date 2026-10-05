"""计划个人视图CRUD；使用所有者锁约束并发上限。"""

from fastapi import HTTPException
from models import User
from models.plan_case_view import PlanCaseSavedView
from core.logger import logger


def scope(db, user, plan, category):
    return db.query(PlanCaseSavedView).filter_by(
        project_id=plan.project_id, owner_id=str(user.id), category=category
    )


def data(row):
    return dict(id=row.id, name=row.name, filters=row.filters)


def save(db, user, plan, category, body, view_id=None):
    db.query(User).filter_by(id=str(user.id)).with_for_update().first()
    query = scope(db, user, plan, category)
    row = query.filter_by(id=view_id).with_for_update().first() if view_id else None
    if view_id and not row:
        raise HTTPException(404, "个人视图不存在")
    if not view_id:
        if query.count() >= 10:
            raise HTTPException(409, "每个项目的此分类最多创建10个个人视图")
        row = PlanCaseSavedView(project_id=plan.project_id, owner_id=str(user.id),
                                category=category, name=body.name, filters=body.filters)
        db.add(row)
    else:
        row.name = body.name
        if "filters" in body.model_fields_set:
            row.filters = body.filters
    db.flush()
    logger.info("计划个人视图已保存 project_id={} category={} owner_id={} view_id={}",
                plan.project_id, category, user.id, row.id)
    return data(row)


def remove(db, user, plan, category, view_id):
    row = scope(db, user, plan, category).filter_by(id=view_id).with_for_update().first()
    if not row:
        raise HTTPException(404, "个人视图不存在")
    db.delete(row)
    logger.info("计划个人视图已删除 project_id={} owner_id={} view_id={}",
                plan.project_id, user.id, view_id)
