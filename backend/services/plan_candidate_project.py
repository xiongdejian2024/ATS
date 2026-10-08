"""目标计划与来源项目分别授权，双项目按固定顺序锁定。"""
from types import SimpleNamespace
from fastapi import HTTPException
from models import Project, User
from core.project_access import require_project_access, project_allows
from core.logger import logger


def source_scope(db, user, plan, project_id=None, *, writing=False):
    target_id = plan.project_id
    source_id = project_id or target_id
    if writing:
        for identifier in sorted({target_id, source_id}):
            project = db.query(Project).filter_by(id=identifier).populate_existing().with_for_update().one_or_none()
            if not project:
                raise HTTPException(404, '项目不存在')
        current_user = db.query(User).filter_by(id=user.id).populate_existing().with_for_update(read=True).one_or_none()
        if not current_user or not current_user.status:
            raise HTTPException(403, '用户不存在或已停用')
        user = current_user
    require_project_access(db, user, target_id, 'test_plan:update' if writing else 'test_plan:read', current_read=writing)
    require_project_access(db, user, target_id, 'test_case:read', current_read=writing)
    project = require_project_access(db, user, source_id, 'test_case:read', current_read=writing)
    logger.debug('计划关联来源已核验：计划={}，目标项目={}，来源项目={}，写入={}', plan.id, target_id, source_id, writing)
    return SimpleNamespace(project_id=source_id, id=plan.id), project


def projects(db, user, plan):
    source_scope(db, user, plan)
    return [dict(id=p.id, name=p.name) for p in db.query(Project).order_by(Project.name, Project.id)
            if project_allows(db, user, p, 'test_case:read')]


def require_case_sources(db, user_id, cases, *, current_read=False):
    """配置和执行使用实际来源权限，读取既有计划关联仍由计划权限控制。"""
    if not cases:
        return
    if current_read:
        for identifier in sorted({case.project_id for case in cases}):
            db.query(Project).filter_by(id=identifier).populate_existing().with_for_update().one_or_none()
    user = (db.query(User).filter_by(id=str(user_id)).populate_existing().with_for_update(read=True).one_or_none()
            if current_read else db.get(User, str(user_id)))
    if not user or not user.status:
        raise HTTPException(403, '用户不存在或已停用')
    for identifier in sorted({case.project_id for case in cases}):
        require_project_access(db, user, identifier, 'test_case:read', current_read=current_read)


def lock_run_sources(db, plan_id, *, extra_project_ids=()):
    """执行与关联都先锁项目再锁计划，避免跨项目双向操作反序等待。"""
    from models import TestPlan, TestCase, TestSuite, PlanCaseRelation
    from models.plan_workspace import PlanNode
    plan = db.get(TestPlan, plan_id)
    if not plan:
        raise ValueError('测试计划不存在')
    identifiers = {r.case_id for r in db.query(PlanCaseRelation).filter_by(plan_id=plan_id)}
    identifiers.update(n.case_id for n in db.query(PlanNode).filter_by(plan_id=plan_id) if n.case_id)
    identifiers.update(cid for suite in db.query(TestSuite).filter_by(plan_id=plan_id) for cid in suite.case_ids or [])
    sources = {c.project_id for c in db.query(TestCase).filter(TestCase.id.in_(identifiers))} | {plan.project_id} | set(extra_project_ids)
    for identifier in sorted(sources):
        if not db.query(Project).filter_by(id=identifier).populate_existing().with_for_update().one_or_none():
            raise ValueError('计划来源项目已不存在')
    return sources
