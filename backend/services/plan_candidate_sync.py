"""同步功能用例已有的接口/场景关联，预览与写入共用当前范围。"""
from fastapi import HTTPException
from models import TestCase
from models.case_features import CaseAutomationLink
from models.plan_workspace import PlanNode

CATEGORIES = {'api': 'apiCaseCollectionId', 'scenario': 'apiScenarioCollectionId'}


def collection(db, plan, identifier, category, *, current_read=False):
    # 默认测试集没有单独的测试点记录；未选择与选择默认测试集分别表示跳过和同步。
    if identifier == 'default':
        return None
    query = db.query(PlanNode).filter_by(id=identifier, plan_id=plan.id, node_type='point', category=category)
    row = (query.populate_existing().with_for_update() if current_read else query).one_or_none()
    if not row:
        raise HTTPException(422, '同步测试集必须属于当前计划及对应分类')
    return row.id


def resolve(db, plan, selection, functional, suites, relations, uses_tree, *, current_read=False):
    groups, summary = {}, {}
    source_ids = {case.id for case in functional}
    source_project = selection.projectId or plan.project_id
    for category, field in CATEGORIES.items():
        identifier = getattr(selection, field)
        targets = []
        parent = None
        if identifier:
            parent = collection(db, plan, identifier, category, current_read=current_read)
            query = (db.query(CaseAutomationLink, TestCase)
                     .join(TestCase, TestCase.id == CaseAutomationLink.target_case_id)
                     .filter(CaseAutomationLink.case_id.in_(source_ids), CaseAutomationLink.category == category,
                             TestCase.type == category, TestCase.deleted_at.is_(None), TestCase.is_automated.is_(True))
                     .order_by(CaseAutomationLink.case_id, TestCase.created_at, TestCase.id, CaseAutomationLink.id))
            rows = (query.populate_existing().with_for_update() if current_read else query).all()
            if any(case.project_id != source_project for _, case in rows):
                raise HTTPException(409, '同步关联用例的来源项目已改变，请更新功能用例关联')
            seen = set() if uses_tree else {r.case_id for r in relations}
            pairs = set()
            for link, case in rows:
                pair = (link.case_id, case.id)
                if pair in pairs or not uses_tree and case.id in seen:
                    continue
                pairs.add(pair)
                seen.add(case.id)
                targets.append(case)
            from services.plan_candidate_selection import LIMIT
            if len(targets) > LIMIT:
                raise HTTPException(422, '每类同步最多关联10000条用例，请缩小功能用例范围')
        ids = {case.id for case in targets}
        groups[category] = dict(cases=targets, collectionId=parent)
        summary[category] = dict(count=len(targets), compatibleSuiteIds=[s.id for s in suites if ids <= set(s.case_ids or [])])
    return groups, summary


def validate_suites(groups, data, suites, uses_tree):
    selected = {}
    for category, field in [('api', 'syncApiSuiteId'), ('scenario', 'syncScenarioSuiteId')]:
        identifier = getattr(data, field)
        suite = next((s for s in suites if s.id == identifier), None)
        if identifier and not suite:
            raise HTTPException(422, '同步测试套必须属于当前计划')
        cases = groups.get(category, {}).get('cases', [])
        if uses_tree and cases and (not suite or not {c.id for c in cases} <= set(suite.case_ids or [])):
            raise HTTPException(422, '同步自动化用例须选择包含该分类全部用例的当前计划测试套')
        selected[category] = suite
    return selected
