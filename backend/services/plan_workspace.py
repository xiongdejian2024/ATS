"""计划模块与管理元数据，所有改动在调用事务内完成。"""
from copy import deepcopy
from fastapi import HTTPException
from models.plan_workspace import PlanModule, PlanWorkspace, PlanFollow
from models.plan_orchestration import PlanRun, PlanSettings
from models.test_plan import TestPlan
from services.plan_orchestration import ACTIVE
from core.logger import logger


def metadata(db, plan_id, user_id):
    row = db.get(PlanWorkspace, plan_id)
    return dict(moduleId=row.module_id if row else None, tags=row.tags if row else [],
                archived=bool(row and row.archived),
                followed=db.query(PlanFollow).filter_by(plan_id=plan_id, user_id=user_id).first() is not None)


def update_metadata(db, plan, data):
    row = db.get(PlanWorkspace, plan.id) or PlanWorkspace(plan_id=plan.id)
    if "moduleId" in data:
        module = db.get(PlanModule, data["moduleId"]) if data["moduleId"] else None
        if data["moduleId"] and (not module or module.project_id != plan.project_id):
            raise HTTPException(400, "计划模块不属于当前项目")
        row.module_id = data["moduleId"] or None
    if "tags" in data:
        tags = data["tags"]
        if not isinstance(tags, list) or len(tags) > 50 or any(not isinstance(t, str) or len(t.strip()) > 80 for t in tags):
            raise HTTPException(422, "标签最多50个，每个最多80字")
        row.tags = list(dict.fromkeys(t.strip() for t in tags if t.strip()))
    if "archived" in data:
        if data["archived"] and db.query(PlanRun).filter(PlanRun.plan_id == plan.id, PlanRun.status.in_(ACTIVE)).first():
            raise HTTPException(409, "执行中计划不可归档，请先完成或取消")
        row.archived = bool(data["archived"])
    if "groupId" in data:
        from models.plan_orchestration import PlanGroup
        group = db.get(PlanGroup, data["groupId"]) if data["groupId"] else None
        if data["groupId"] and (not group or group.project_id != plan.project_id):
            raise HTTPException(400, "计划组不属于当前项目")
        settings = db.get(PlanSettings, plan.id) or PlanSettings(plan_id=plan.id)
        settings.group_id = data["groupId"] or None
        db.add(settings)
    db.add(row)
    logger.info("已更新计划管理属性：计划={}", plan.id)


def clone_extensions(db, source, target, user_id):
    """复制配置、关联和测试套，执行结果保持独立。"""
    from models.test_suite import TestSuite
    source_meta = db.get(PlanWorkspace, source.id)
    if source_meta:
        db.add(PlanWorkspace(plan_id=target.id, module_id=source_meta.module_id, tags=deepcopy(source_meta.tags), archived=False, uses_tree=source_meta.uses_tree))
    mapping = {}
    for suite in db.query(TestSuite).filter_by(plan_id=source.id).all():
        clone = TestSuite(plan_id=target.id, name=suite.name, description=suite.description,
                          git_enabled=suite.git_enabled, git_repo_url=suite.git_repo_url,
                          git_branch=suite.git_branch, git_token=suite.git_token,
                          environment_id=suite.environment_id, execution_command=suite.execution_command,
                          case_ids=deepcopy(suite.case_ids), created_by=user_id, updated_by=user_id, status="pending")
        db.add(clone)
        db.flush()
        mapping[suite.id] = clone.id
    policy = db.get(PlanSettings, source.id)
    if policy:
        db.add(PlanSettings(plan_id=target.id, group_id=policy.group_id, execution_mode=policy.execution_mode,
                            stop_on_failure=policy.stop_on_failure, pass_threshold=policy.pass_threshold,
                            suite_order=[mapping[s] for s in policy.suite_order or [] if s in mapping]))
    from models.plan_workspace import PlanNode
    originals = db.query(PlanNode).filter_by(plan_id=source.id).all()
    node_map = {}
    for node in originals:
        cloned = PlanNode(plan_id=target.id, name=node.name, node_type=node.node_type, category=node.category,
                          case_id=node.case_id, suite_id=mapping.get(node.suite_id), assigned_to=node.assigned_to,
                          position=node.position, config=deepcopy(node.config))
        db.add(cloned)
        db.flush()
        node_map[node.id] = cloned
    for node in originals:
        node_map[node.id].parent_id = node_map[node.parent_id].id if node.parent_id in node_map else None
        node_map[node.id].linked_functional_id = node_map[node.linked_functional_id].id if node.linked_functional_id in node_map else None
    from models.plan_execution_config import PlanExecutionConfig
    for config in db.query(PlanExecutionConfig).filter_by(plan_id=source.id):
        scope = config.scope
        node_id = node_map[config.node_id].id if config.node_id in node_map else None
        if config.node_id:
            if not node_id:
                continue
            scope = f"node:{config.category}:{node_id}"
        if source.project_id != target.project_id:
            raise HTTPException(409, "包含项目资源池或请求环境配置的计划须在同项目内复制")
        db.add(PlanExecutionConfig(plan_id=target.id, scope=scope, category=config.category, node_id=node_id, config=deepcopy(config.config), revision=1))
    from models.test_plan import PlanCaseRelation
    originals_by_case = {row.case_id: row for row in db.query(PlanCaseRelation).filter_by(plan_id=source.id)}
    for relation in db.query(PlanCaseRelation).filter_by(plan_id=target.id):
        original = originals_by_case.get(relation.case_id)
        if original and original.collection_id in node_map:
            relation.collection_id = node_map[original.collection_id].id
    return mapping


def group_metadata(db, group_id):
    from models.plan_workspace import PlanGroupWorkspace
    row = db.get(PlanGroupWorkspace, group_id)
    return dict(moduleId=row.module_id if row else None, tags=row.tags if row else [], archived=bool(row and row.archived))


def update_group_metadata(db, group, data):
    from models.plan_workspace import PlanGroupWorkspace
    from models.plan_group_execution import PlanGroupRun
    row = db.get(PlanGroupWorkspace, group.id) or PlanGroupWorkspace(group_id=group.id)
    module_id = data.get("moduleId")
    if module_id:
        module = db.get(PlanModule, module_id)
        if not module or module.project_id != group.project_id:
            raise HTTPException(400, "计划组模块不属于当前项目")
    if data.get("archived") and db.query(PlanGroupRun).filter_by(active_group_id=group.id).first():
        raise HTTPException(409, "执行中的计划组不能归档")
    row.module_id, row.tags, row.archived = module_id, data.get("tags", []), bool(data.get("archived", False))
    db.add(row)


def clone_group(db, group, user_id):
    from models.plan_orchestration import PlanGroup
    from models.plan_group_execution import PlanGroupPolicy
    from services.test_plan_service import TestPlanService
    import uuid
    target = PlanGroup(project_id=group.project_id, name=f"{group.name[:80]}（副本 {uuid.uuid4().hex[:6]}）", description=group.description)
    db.add(target)
    db.flush()
    data = group_metadata(db, group.id)
    data["archived"] = False
    update_group_metadata(db, target, data)
    plan_map = {}
    for setting in db.query(PlanSettings).filter_by(group_id=group.id).all():
        copied = TestPlanService.clone_plan(db, setting.plan_id, group.project_id, user_id, commit=False)
        db.flush()
        db.get(PlanSettings, copied.id).group_id = target.id
        plan_map[setting.plan_id] = copied.id
    policy = db.get(PlanGroupPolicy, group.id)
    if policy:
        db.add(PlanGroupPolicy(group_id=target.id, execution_mode=policy.execution_mode,
                               stop_on_failure=policy.stop_on_failure, pass_threshold=policy.pass_threshold,
                               plan_order=[plan_map[pid] for pid in policy.plan_order if pid in plan_map]))
    db.commit()
    logger.info("已完整复制计划组与成员计划：源组={}，副本={}，计划数={}", group.id, target.id, len(plan_map))
    return target


def apply_tree_statistics(db, plan_id, payload):
    """列表按当前树的关联实例统计，并只引用同实例的最近批次结果。"""
    from models.plan_workspace import PlanNode
    from models.test_suite import TestSuite
    rows = db.query(PlanNode).filter(PlanNode.plan_id == plan_id, PlanNode.node_type != "point").all()
    from services.plan_tree import uses_tree
    from services.plan_case_execution import apply_statistics
    if not uses_tree(db, plan_id):
        apply_statistics(db, plan_id, payload)
        return
    run = db.query(PlanRun).filter_by(plan_id=plan_id).order_by(PlanRun.created_at.desc()).first()
    from services.plan_orchestration import build_report
    results = (run.report if run.status not in ACTIVE and run.report else build_report(db, run))["cases"] if run else []
    by_instance = {(row.get("associationId"), row["caseId"]): row["result"] for row in results}
    states = []
    for row in rows:
        suite = db.get(TestSuite, row.suite_id) if row.suite_id else None
        ids = [row.case_id] if row.case_id else suite.case_ids if suite else []
        states.extend(by_instance.get((row.id, cid), "pending") for cid in ids)
    mapping = {"pending": "pending", "passed": "pass", "failed": "fail", "error": "error", "skipped": "skip", "cancelled": "skip"}
    payload["totalCases"] = len(states)
    payload["executedCases"] = sum(state != "pending" for state in states)
    payload["caseStatusCounts"] = {key: sum(mapping.get(state, "pending") == key for state in states) for key in ("pending", "pass", "fail", "broken", "error", "skip")}
    payload["usesTestPointTree"] = True
    apply_statistics(db, plan_id, payload)
