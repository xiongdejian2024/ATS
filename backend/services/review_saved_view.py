"""评审个人视图复用已有表；保留固定业务命名空间和当前权限锁。"""
from types import SimpleNamespace
from fastapi import HTTPException
from models import User
from core.project_access import require_project_access
from services import plan_case_view
from services.plan_candidate_filter import parse_candidate_filters

CANDIDATES = "review-candidates"
INDEX = "review-index"


def access(db, user, project_id, *, writing=False):
    if writing:
        user = db.query(User).filter_by(id=str(user.id)).populate_existing().with_for_update(read=True).one_or_none()
        if not user or not user.status:
            raise HTTPException(403, "用户不存在或已停用")
    require_project_access(db, user, project_id, "test_case:read", current_read=writing)
    return user, SimpleNamespace(project_id=project_id)


def validate(filters):
    if filters is None:
        raise HTTPException(422, "个人视图条件不能为空")
    parse_candidate_filters(dict(conditions=filters.get("filterConditions", []),
                                logic=filters.get("filterLogic", "and")), "functional")


def listing(db, user, project_id, category=CANDIDATES):
    user, scope = access(db, user, project_id)
    return [plan_case_view.data(row) for row in plan_case_view.scope(db, user, scope, category)
            .order_by(plan_case_view.PlanCaseSavedView.created_at.desc()).all()]


def save(db, user, project_id, body, view_id=None, category=CANDIDATES):
    user, scope = access(db, user, project_id, writing=True)
    if not view_id or "filters" in body.model_fields_set:
        if category == INDEX:
            from schemas.review_workspace import review_index_view_filters
            review_index_view_filters(body.filters)
        else:
            validate(body.filters)
    return plan_case_view.save(db, user, scope, category, body, view_id)


def remove(db, user, project_id, view_id, category=CANDIDATES):
    user, scope = access(db, user, project_id, writing=True)
    plan_case_view.remove(db, user, scope, category, view_id)
