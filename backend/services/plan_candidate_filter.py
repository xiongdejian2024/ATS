"""计划关联抽屉读取主用例，所属计划按当前有效树或旧关联查询。"""

from collections import defaultdict
from models import TestCase, TestPlan, TestSuite, PlanCaseRelation
from models.plan_workspace import PlanNode, PlanWorkspace
from services.case_query import parse_filters, matches_case, matches_related
from services.case_filter_context import CaseFilterContext
from services.case_governance import current_review_statuses


def parse_candidate_filters(raw):
    return parse_filters(raw, extra_fields={'planIds'})


def plan_membership(db, project_id):
    plans = db.query(TestPlan).filter_by(project_id=project_id).all()
    ids = {plan.id for plan in plans}
    nodes = db.query(PlanNode).filter(PlanNode.plan_id.in_(ids)).all()
    tree_plans = {node.plan_id for node in nodes if node.node_type != 'point'}
    tree_plans.update(row.plan_id for row in db.query(PlanWorkspace).filter(
        PlanWorkspace.plan_id.in_(ids), PlanWorkspace.uses_tree.is_(True)))
    suites = {row.id: row for row in db.query(TestSuite).filter(TestSuite.plan_id.in_(ids))}
    membership = defaultdict(set)
    for node in nodes:
        if node.node_type == 'point':
            continue
        suite = suites.get(node.suite_id)
        for case_id in [node.case_id] if node.case_id else (suite.case_ids if suite and suite.plan_id == node.plan_id else []):
            membership[case_id].add(node.plan_id)
    for row in db.query(PlanCaseRelation).filter(PlanCaseRelation.plan_id.in_(ids)):
        if row.plan_id not in tree_plans:
            membership[row.case_id].add(row.plan_id)
    return membership, [dict(id=p.id, name=p.name) for p in plans]


def filter_cases(db, plan, category, raw, user_id, mine):
    conditions, logic = parse_candidate_filters(raw)
    context = CaseFilterContext(db, plan.project_id, conditions, user_id)
    query = db.query(TestCase).filter(TestCase.project_id == plan.project_id, TestCase.deleted_at.is_(None))
    query = query.filter(TestCase.type.notin_(['api', 'scenario'])) if category == 'functional' else query.filter(TestCase.type == category, TestCase.is_automated.is_(True))
    if mine:
        query = query.filter(TestCase.created_by == user_id)
    cases = query.order_by(TestCase.created_at.desc(), TestCase.id).all()
    statuses = current_review_statuses(db, cases)
    membership = plan_membership(db, plan.project_id)[0] if any(c['field'] == 'planIds' for c in conditions) else {}
    def check(case, condition):
        if condition['field'] == 'planIds':
            return matches_related(list(membership.get(case.id, [])), condition['operator'], condition.get('value'))
        return matches_case(case, condition, statuses, context)
    combine = all if logic == 'and' else any
    return [case for case in cases if not context.conditions or combine(check(case, c) for c in context.conditions)], statuses


def advanced_candidates(db, plan, category, filters, mine, user_id, page, size):
    from models import Module
    from services.case_candidates import descendants
    from utils.serializer import serialize_model

    cases, statuses = filter_cases(db, plan, category, filters, user_id, mine)
    modules = db.query(Module).filter_by(project_id=plan.project_id).order_by(Module.sort_order, Module.created_at).all()
    counts = defaultdict(int)
    for case in cases:
        counts[case.module_id] += 1
    folders = [dict(id=m.id, name=m.name, parentId=m.parent_id,
                    count=sum(counts[key] for key in descendants(modules, m.id))) for m in modules]
    names = {m.id: m.name for m in modules}
    items = [dict(serialize_model(case, camel_case=True), moduleName=names.get(case.module_id, '未分配模块'),
                  reviewResult=statuses.get(case.id, 'not_reviewed')) for case in cases[(page-1)*size:page*size]]
    return dict(items=items, total=len(cases), page=page, size=size, modules=folders,
                counts=dict(all=len(cases), unassigned=sum(count for module, count in counts.items() if module not in names)))
