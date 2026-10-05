"""原生列表范围预览与批量操作共用实际实例，在锁内重新解析范围。"""
from fastapi import HTTPException
from models import TestCase, User
from models.plan_workspace import PlanNode
from core.project_access import require_project_access, project_allows
from core.logger import logger
from services import plan_case_workspace as workspace
from services.plan_candidate_selection import state, LIMIT
from services.plan_candidate_project import lock_run_sources


def resolve(db, plan, user, selection, *, writing=False):
    target_id = plan.project_id
    if writing:
        try:
            locked_sources = lock_run_sources(db, plan.id)
        except ValueError as exc:
            logger.exception('原生计划范围来源锁定失败：计划={}', plan.id)
            raise HTTPException(409, str(exc)) from exc
        plan, settings, _, suites, relations = state(db, plan, current_read=True)
        if plan.project_id != target_id:
            raise HTTPException(409, '计划所属项目已改变，请刷新后重新选择')
        user = db.query(User).filter_by(id=user.id).populate_existing().with_for_update().one_or_none()
        if not user or not user.status:
            raise HTTPException(403, '用户不存在或已停用')
        ids = {r.case_id for r in relations}
        ids.update(cid for suite in suites for cid in suite.case_ids or [])
        ids.update(n.case_id for n in db.query(PlanNode).filter_by(plan_id=plan.id).populate_existing().with_for_update() if n.case_id)
        cases = db.query(TestCase).filter(TestCase.id.in_(ids)).populate_existing().with_for_update().all()
        if any(case.project_id not in locked_sources for case in cases):
            raise HTTPException(409, '关联来源项目已改变，请刷新后重新选择')
        if settings and settings.archived:
            raise HTTPException(409, '归档计划不可修改关联')
    require_project_access(db, user, plan.project_id, 'test_case:read', current_read=writing)
    project = require_project_access(db, user, plan.project_id, 'test_plan:update' if writing else 'test_plan:read', current_read=writing)
    condition = selection.condition.model_dump() if selection.selectAll else {}
    data = workspace.listing(db, plan, selection.category, dict(condition, view='mind', sort='caseCode', direction='asc', page=1, size=20, user_id=str(user.id)), current_read=writing)
    eligible = {row['id']: row for row in data['items'] if not row['grouped']}
    if selection.selectAll:
        excluded = set(selection.excludeIds)
        selected = [row for key, row in eligible.items() if key not in excluded]
        excluded_count = len(excluded & eligible.keys())
    else:
        if any(key not in eligible for key in selection.selectIds):
            raise HTTPException(404, '选择的关联实例不存在、不属于当前计划分类或不可单独操作')
        selected = [eligible[key] for key in selection.selectIds]
        excluded_count = 0
    if len(selected) > LIMIT:
        raise HTTPException(422, f'每批最多处理{LIMIT}个关联实例，请缩小范围；不会截断选择')
    summary = dict(count=len(selected), eligibleCount=len(eligible), excludedCount=excluded_count,
                   canModify=bool(selected and project_allows(db, user, project, 'test_plan:update')))
    logger.debug('已核对原生计划实例范围：计划={}，分类={}，全选={}，实际选择={}，实际排除={}，写入={}', plan.id, selection.category, selection.selectAll, len(selected), excluded_count, writing)
    return plan, user, selected, summary


def preview(db, plan, user, selection):
    plan, user, _, summary = resolve(db, plan, user, selection)
    from models.plan_workspace import PlanWorkspace
    settings = db.get(PlanWorkspace, plan.id)
    if settings and settings.archived:
        summary['canModify'] = False
    return summary


def apply(db, plan, user, data):
    plan, user, selected, _ = resolve(db, plan, user, data, writing=True)
    if not selected:
        raise HTTPException(409, '当前选择范围已为空，请刷新后重新选择')
    # 已锁定当前关联，按实例处理，重复主用例不能合并为一个选择。
    # 不使用 db.get 的普通快照查询：范围中可能出现预览后才提交的新实例。
    # 保持当前对象的强引用，后续树移动校验也能读取当前父节点与测试套。
    _, settings, _, suites, relations = state(db, plan, current_read=True)
    nodes = db.query(PlanNode).filter_by(plan_id=plan.id).populate_existing().with_for_update().all()
    cases = db.query(TestCase).filter(TestCase.id.in_([row['caseId'] for row in selected])).populate_existing().with_for_update().all()
    associations = {('legacy', row.id): row for row in relations}
    associations.update({('node', row.id): row for row in nodes})
    rows = [(row['source'], associations[(row['source'], row['associationId'])]) for row in selected]
    return workspace.batch(db, plan, user, data, resolved_rows=rows, current_read=True)
