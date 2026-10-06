"""计划详情分类统计和当前关联缺陷，不向执行节点发送消息。"""
from models import TestCase, TestSuite, PlanCaseRelation
from models.plan_workspace import PlanNode
from models.case_features import CaseIssue, CaseIssueLink
from utils.serializer import serialize_model


def category_counts(db, plan_id, legacy_cases):
    nodes = db.query(PlanNode).filter(PlanNode.plan_id == plan_id, PlanNode.node_type != "point").all()
    counts = dict(functional=0, api=0, scenario=0)
    from services.plan_tree import uses_tree
    if uses_tree(db, plan_id):
        for node in nodes:
            counts[node.category] += 1
    else:
        for item in legacy_cases:
            counts[item.get("type") if item.get("type") in ("api", "scenario") else "functional"] += 1
    return counts


def plan_case_ids(db, plan_id):
    nodes = db.query(PlanNode).filter(PlanNode.plan_id == plan_id, PlanNode.node_type != "point").all()
    from services.plan_tree import uses_tree
    if not uses_tree(db, plan_id):
        return {row.case_id for row in db.query(PlanCaseRelation).filter_by(plan_id=plan_id)}
    ids = {node.case_id for node in nodes if node.case_id}
    suite_ids = {node.suite_id for node in nodes if node.suite_id and not node.case_id}
    for suite in db.query(TestSuite).filter(TestSuite.id.in_(suite_ids)):
        ids.update(suite.case_ids or [])
    return ids


def defects(db, plan):
    ids = plan_case_ids(db, plan.id)
    cases = db.query(TestCase).filter(TestCase.id.in_(ids), TestCase.project_id == plan.project_id).all()
    names = {row.id: row.name for row in cases}
    rows = db.query(CaseIssue, CaseIssueLink).join(CaseIssueLink, CaseIssueLink.issue_id == CaseIssue.id).filter(
        CaseIssue.project_id == plan.project_id, CaseIssue.kind == "defect", CaseIssueLink.case_id.in_(names)).all()
    items = {}
    for issue, link in rows:
        item = items.setdefault(issue.id, dict(**serialize_model(issue, camel_case=True), cases=[]))
        item["cases"].append(dict(id=link.case_id, name=names[link.case_id], linkId=link.id))
    # 旧主用例绑定只作为历史记录呈现；新绑定明确携带计划实例身份。
    for item in items.values():
        item['bindingScope'] = 'case'
    from services.plan_case_defect import query
    for link, issue in query(db, plan):
        item = items.setdefault(issue.id, dict(**serialize_model(issue, camel_case=True), cases=[], bindingScope='instance'))
        item['cases'].append(dict(id=link.case_id, name=link.case_snapshot.get('name', ''), linkId=link.id, associationKey=link.association_key))
    return dict(items=list(items.values()), cases=[dict(id=row.id, name=row.name) for row in cases if not row.deleted_at])
