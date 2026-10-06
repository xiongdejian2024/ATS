"""计划关联抽屉读取主用例，所属计划按当前有效树或旧关联查询。"""

from collections import defaultdict
from models import TestCase, TestPlan, TestSuite, PlanCaseRelation
from models.plan_workspace import PlanNode, PlanWorkspace
from services.case_query import parse_filters, matches_case, matches_related, matches
from services.native_candidate_context import NativeCandidateContext, NATIVE_FIELDS
from fastapi import HTTPException
from services.case_filter_context import CaseFilterContext
from services.case_governance import current_review_statuses


def parse_candidate_filters(raw, category=None):
    conditions, logic = parse_filters(raw, extra_fields={'planIds'} | NATIVE_FIELDS)
    unsupported = NATIVE_FIELDS if category == 'functional' else ({'stepTotal'} if category == 'api' else ({'protocol', 'path', 'apiChange'} if category == 'scenario' else set()))
    if any(c['field'] in unsupported for c in conditions):
        raise HTTPException(422, '筛选字段不属于当前用例分类')
    for condition in conditions:
        field, operator, value = condition['field'], condition['operator'], condition.get('value')
        if field == 'apiChange' and (operator != 'equals' or type(value) is not bool):
            raise HTTPException(422, '接口参数变更只支持等于布尔值')
        if field == 'stepTotal':
            if operator not in {'equals', 'not_equals', 'gt', 'gte', 'lt', 'lte', 'between', 'is_empty', 'is_not_empty'}:
                raise HTTPException(422, '步骤数不支持此运算')
            values = value if operator == 'between' else [value]
            if operator not in {'is_empty', 'is_not_empty'} and any(type(v) is not int or v < 0 for v in values):
                raise HTTPException(422, '步骤数必须为非负整数')
    return conditions, logic


def plan_membership(db, project_id, *, current_read=False):
    def read(query):
        return (query.populate_existing().with_for_update() if current_read else query).all()
    plans = read(db.query(TestPlan).filter_by(project_id=project_id))
    ids = {plan.id for plan in plans}
    nodes = read(db.query(PlanNode).filter(PlanNode.plan_id.in_(ids)))
    tree_plans = {node.plan_id for node in nodes if node.node_type != 'point'}
    tree_plans.update(row.plan_id for row in read(db.query(PlanWorkspace).filter(
        PlanWorkspace.plan_id.in_(ids), PlanWorkspace.uses_tree.is_(True))))
    suites = {row.id: row for row in read(db.query(TestSuite).filter(TestSuite.plan_id.in_(ids)))}
    membership = defaultdict(set)
    for node in nodes:
        if node.node_type == 'point':
            continue
        suite = suites.get(node.suite_id)
        for case_id in [node.case_id] if node.case_id else (suite.case_ids if suite and suite.plan_id == node.plan_id else []):
            membership[case_id].add(node.plan_id)
    for row in read(db.query(PlanCaseRelation).filter(PlanCaseRelation.plan_id.in_(ids))):
        if row.plan_id not in tree_plans:
            membership[row.case_id].add(row.plan_id)
    return membership, [dict(id=p.id, name=p.name) for p in plans]


def filter_cases(db, plan, category, raw, user_id, mine, *, current_read=False):
    conditions, logic = parse_candidate_filters(raw, category)
    context = CaseFilterContext(db, plan.project_id, conditions, user_id, current_read=current_read)
    query = db.query(TestCase).filter(TestCase.project_id == plan.project_id, TestCase.deleted_at.is_(None))
    query = query.filter(TestCase.type.notin_(['api', 'scenario'])) if category == 'functional' else query.filter(TestCase.type == category, TestCase.is_automated.is_(True))
    if mine:
        query = query.filter(TestCase.created_by == user_id)
    query = query.order_by(TestCase.created_at.desc(), TestCase.id)
    cases = (query.populate_existing().with_for_update() if current_read else query).all()
    statuses = current_review_statuses(db, cases, current_read=current_read)
    membership = plan_membership(db, plan.project_id, current_read=current_read)[0] if any(c['field'] == 'planIds' for c in conditions) else {}
    native = NativeCandidateContext(db, plan.project_id, current_read=current_read) if category != 'functional' else None
    def check(case, condition):
        if condition['field'] in NATIVE_FIELDS:
            return matches(native.values(case).get(condition['field']), condition['operator'], condition.get('value'))
        if condition['field'] == 'planIds':
            return matches_related(list(membership.get(case.id, [])), condition['operator'], condition.get('value'))
        return matches_case(case, condition, statuses, context)
    combine = all if logic == 'and' else any
    return [case for case in cases if not context.conditions or combine(check(case, c) for c in context.conditions)], statuses, native


def advanced_candidates(db, plan, category, filters, mine, user_id, page, size, sort=None, direction="asc"):
    from models import Module
    from services.case_candidates import descendants
    from utils.serializer import serialize_model

    cases, statuses, native = filter_cases(db, plan, category, filters, user_id, mine)
    if sort:
        field = {"id": "case_code", "name": "name", "createdAt": "created_at"}[sort]
        cases.sort(key=lambda case: (getattr(case, field) or "", case.id), reverse=direction == "desc")
    modules = db.query(Module).filter_by(project_id=plan.project_id).order_by(Module.sort_order, Module.created_at).all()
    counts = defaultdict(int)
    for case in cases:
        counts[case.module_id] += 1
    folders = [dict(id=m.id, name=m.name, parentId=m.parent_id,
                    count=sum(counts[key] for key in descendants(modules, m.id))) for m in modules]
    names = {m.id: m.name for m in modules}
    items = [dict(serialize_model(case, camel_case=True), moduleName=names.get(case.module_id, '未分配模块'),
                  reviewResult=statuses.get(case.id, 'not_reviewed'), **(native.values(case) if native else {})) for case in cases[(page-1)*size:page*size]]
    return dict(items=items, total=len(cases), page=page, size=size, modules=folders,
                counts=dict(all=len(cases), unassigned=sum(count for module, count in counts.items() if module not in names)))
