"""关联预览与写入共用候选范围，写入在项目锁内使用当前读。"""
from fastapi import HTTPException
from models import TestCase, TestPlan, TestSuite, PlanCaseRelation
from models.plan_workspace import PlanNode, PlanWorkspace
from core.project_access import require_project_access, project_allows
from core.logger import logger
from services.review_workspace import lock_project

LIMIT = 10000


def state(db, plan, *, current_read=False):
    def read(query):
        return (query.populate_existing().with_for_update() if current_read else query).all()
    if current_read:
        plan = db.query(TestPlan).filter_by(id=plan.id).populate_existing().with_for_update().one_or_none()
        if not plan:
            raise HTTPException(404, '计划不存在')
    workspaces = read(db.query(PlanWorkspace).filter_by(plan_id=plan.id))
    workspace = workspaces[0] if workspaces else None
    nodes = read(db.query(PlanNode).filter_by(plan_id=plan.id))
    uses_tree = bool(workspace and workspace.uses_tree) or any(n.node_type != 'point' for n in nodes)
    suites = read(db.query(TestSuite).filter_by(plan_id=plan.id))
    relations = read(db.query(PlanCaseRelation).filter_by(plan_id=plan.id))
    return plan, workspace, uses_tree, suites, relations


def resolve(db, plan, user, selection, *, writing=False):
    if writing:
        lock_project(db, plan.project_id)
    plan, workspace, uses_tree, suites, relations = state(db, plan, current_read=writing)
    require_project_access(db, user, plan.project_id, 'test_case:read')
    project = require_project_access(db, user, plan.project_id, 'test_plan:update' if writing else 'test_plan:read')
    if writing and workspace and workspace.archived:
        raise HTTPException(409, '归档计划不可修改关联')
    excluded_count = 0
    if selection.selectAll:
        condition = selection.condition
        if condition.filters is not None or condition.mine:
            from services.plan_candidate_filter import filter_cases
            cases, _, _ = filter_cases(db, plan, selection.category, condition.filters, str(user.id), condition.mine, current_read=writing)
        else:
            from services.case_candidates import candidate_query
            query, _, _, _ = candidate_query(db, plan.project_id, selection.category, condition.search, condition.folder, condition.priority, current_read=writing)
            if not uses_tree:
                query = query.filter(TestCase.id.notin_([r.case_id for r in relations]))
            cases = query.order_by(TestCase.created_at.desc(), TestCase.id).limit(LIMIT + len(selection.excludeIds) + 1).all()
    else:
        query = db.query(TestCase).filter(TestCase.id.in_(selection.caseIds), TestCase.project_id == plan.project_id, TestCase.deleted_at.is_(None)).order_by(TestCase.created_at.desc(), TestCase.id)
        cases = (query.populate_existing().with_for_update() if writing else query).all()
        if len(cases) != len(selection.caseIds):
            raise HTTPException(404, '用例不存在、已回收或不属于当前项目')
        if any((c.type if c.type in ('api', 'scenario') else 'functional') != selection.category for c in cases):
            raise HTTPException(422, '请选择当前分类的用例')
        if selection.category != 'functional' and any(not c.is_automated for c in cases):
            raise HTTPException(422, 'API/场景分类只能关联可执行的自动化用例')
    if not uses_tree:
        linked = {r.case_id for r in relations}
        cases = [c for c in cases if c.id not in linked]
    if selection.selectAll:
        excluded = set(selection.excludeIds)
        excluded_count = sum(c.id in excluded for c in cases)
        cases = [c for c in cases if c.id not in excluded]
    if len(cases) > LIMIT:
        raise HTTPException(422, '每批最多关联10000条用例，请缩小筛选范围')
    if writing and selection.selectAll and not cases:
        raise HTTPException(409, '当前范围已无可关联用例，请刷新后重新选择')
    automated = [c for c in cases if c.is_automated]
    compatible = [s.id for s in suites if all(c.id in (s.case_ids or []) for c in automated)]
    summary = dict(count=len(cases), excludedCount=excluded_count, automatedCount=len(automated),
                   usesTree=uses_tree, compatibleSuiteIds=compatible,
                   canAssociate=project_allows(db, user, project, 'test_plan:update') and not bool(workspace and workspace.archived))
    if writing:
        logger.info('计划关联范围已在锁内解析：计划={}，分类={}，全选={}，数量={}，排除={}', plan.id, selection.category, selection.selectAll, len(cases), excluded_count)
    return cases, summary, suites, relations


def preview(db, plan, user, selection):
    return resolve(db, plan, user, selection)[1]
