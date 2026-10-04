"""计划测试点树、配置继承及关联实例编译。"""
from copy import copy, deepcopy
from sqlalchemy import func
from fastapi import HTTPException
from models.plan_workspace import PlanNode
from models.test_plan import TestPlan
from models.test_case import TestCase
from models.test_suite import TestSuite
from models.environment import Environment
from models.task_queue import TaskQueue
from models.user import User
from core.project_access import require_project_access
from utils.serializer import serialize_model
from core.logger import logger


def nodes(db, plan_id):
    return db.query(PlanNode).filter_by(plan_id=plan_id).order_by(PlanNode.position, PlanNode.created_at, PlanNode.id).all()


def effective_config(db, node):
    ancestors, seen = [], set()
    current = node
    while current:
        if current.id in seen:
            raise ValueError("测试点层级形成循环")
        seen.add(current.id)
        ancestors.append(current)
        current = db.get(PlanNode, current.parent_id) if current.parent_id else None
    plan = db.get(TestPlan, node.plan_id)
    config = {"environmentId": plan.environment_id} if plan.environment_id else {}
    for ancestor in reversed(ancestors):
        for key, value in (ancestor.config or {}).items():
            if value is not None:
                config[key] = value
                if key == "environmentId":
                    config.pop("resourcePool", None)
                elif key == "resourcePool":
                    config.pop("environmentId", None)
    return config


def node_data(db, node):
    data = serialize_model(node, camel_case=True)
    data["effectiveConfig"] = effective_config(db, node)
    if node.case_id:
        case = db.get(TestCase, node.case_id)
        data["case"] = serialize_model(case, camel_case=True) if case else None
    return data


def save_node(db, plan, data, existing=None):
    row = existing or PlanNode(plan_id=plan.id)
    name = str(data.get("name", row.name or "")).strip()
    if not name or len(name) > 255:
        raise HTTPException(422, "节点名称须为1到255字")
    row.name = name
    row.node_type = data.get("nodeType", row.node_type or "point")
    row.category = data.get("category", row.category or "functional")
    if row.node_type not in ("point", "case", "suite") or row.category not in ("functional", "api", "scenario"):
        raise HTTPException(422, "节点类型或用例分类无效")
    parent_id = data.get("parentId", row.parent_id) or None
    cursor, seen = parent_id, {row.id} if row.id else set()
    while cursor:
        parent = db.get(PlanNode, cursor)
        if not parent or parent.plan_id != plan.id or parent.node_type != "point" or cursor in seen:
            raise HTTPException(400, "父测试点无效或形成循环")
        seen.add(cursor)
        cursor = parent.parent_id
    if row.id and row.node_type != "point" and db.query(PlanNode).filter_by(parent_id=row.id).first():
        raise HTTPException(409, "含子节点的测试点不能转换为用例")
    row.parent_id = parent_id
    row.case_id = data.get("caseId", row.case_id) or None
    row.suite_id = data.get("suiteId", row.suite_id) or None
    if row.node_type == "point":
        row.case_id = row.suite_id = None
    if row.node_type == "case":
        case = db.get(TestCase, row.case_id) if row.case_id else None
        if not case or case.deleted_at or case.project_id != plan.project_id:
            raise HTTPException(400, "用例不存在、已回收或不属于当前项目")
        if row.category != "functional" and not case.is_automated:
            raise HTTPException(400, "API/场景用例需要可执行的自动化用例")
        if case.is_automated and not row.suite_id:
            raise HTTPException(400, "自动化用例需要关联测试套")
    if row.suite_id:
        suite = db.get(TestSuite, row.suite_id)
        if not suite or suite.plan_id != plan.id or (row.case_id and row.case_id not in suite.case_ids):
            raise HTTPException(400, "测试套必须属于本计划并包含关联用例")
    elif row.node_type == "suite":
        raise HTTPException(400, "场景节点需要选择测试套")
    assigned = data.get("assignedTo", row.assigned_to) or None
    if assigned:
        user = db.get(User, assigned)
        if not user or not user.status:
            raise HTTPException(400, "执行人不存在或已停用")
        require_project_access(db, user, plan.project_id, "test_plan:read")
    row.assigned_to = assigned
    linked = data.get("linkedFunctionalId", row.linked_functional_id) or None
    if linked:
        target = db.get(PlanNode, linked)
        if not target or target.plan_id != plan.id or target.node_type != "case" or target.category != "functional" or target.id == row.id:
            raise HTTPException(400, "自动化结果只能关联当前计划内的功能用例节点")
        case = db.get(TestCase, target.case_id)
        if not case or case.is_automated:
            raise HTTPException(400, "关联的功能用例必须是手工用例")
    row.linked_functional_id = linked
    config = deepcopy(data.get("config", row.config or {}))
    if not isinstance(config, dict) or set(config) - {"executionMode", "environmentId", "resourcePool"}:
        raise HTTPException(422, "配置仅支持串并行、环境和资源池")
    if config.get("executionMode") not in (None, "serial", "parallel"):
        raise HTTPException(422, "执行模式无效")
    if config.get("environmentId") and config.get("resourcePool"):
        raise HTTPException(422, "指定环境和资源池不能同时设置")
    pool = config.get("resourcePool") or []
    if not isinstance(pool, list) or len(pool) > 100:
        raise HTTPException(422, "资源池必须为最多100个ATS执行环境")
    for env_id in pool + ([config["environmentId"]] if config.get("environmentId") else []):
        if not db.get(Environment, env_id):
            raise HTTPException(400, "执行环境不存在")
    row.config = config
    if "position" in data:
        row.position = int(data["position"])
    elif existing is None:
        # 同级新增节点默认追加，避免同一秒创建后由随机 UUID 改变串行顺序。
        last = db.query(func.max(PlanNode.position)).filter_by(plan_id=plan.id, parent_id=parent_id).scalar()
        row.position = (last + 1) if last is not None else 0
    db.add(row)
    db.flush()
    logger.info("已保存计划测试点节点：计划={}，节点={}，分类={}", plan.id, row.id, row.category)
    return row


def compile_tree(db, plan, policy):
    """将树编译为关联实例及显式前置节点，保留分支串并行语义。"""
    all_nodes = nodes(db, plan.id)
    if not any(n.node_type != "point" for n in all_nodes):
        return None
    children = {}
    for node in all_nodes:
        children.setdefault(node.parent_id, []).append(node)
    entries = []
    def walk(parent_id, prerequisites, mode):
        previous = list(prerequisites)
        leaves = []
        for node in children.get(parent_id, []):
            config = effective_config(db, node)
            deps = previous if mode == "serial" else list(prerequisites)
            if node.node_type == "point":
                branch = walk(node.id, deps, config.get("executionMode", mode))
            else:
                suite = copy(db.get(TestSuite, node.suite_id)) if node.suite_id else None
                case = db.get(TestCase, node.case_id) if node.case_id else None
                if node.case_id and (not case or case.deleted_at):
                    raise ValueError("计划测试点包含已回收的用例")
                if suite:
                    # 复制 ORM 对象仅作发送视图，不加入 Session；使用独立属性避免修改原套。
                    from types import SimpleNamespace
                    suite = SimpleNamespace(**{column.name: deepcopy(getattr(suite, column.name)) for column in TestSuite.__table__.columns})
                    if node.case_id:
                        suite.case_ids = [node.case_id]
                    pool = config.get("resourcePool") or []
                    if config.get("environmentId"):
                        suite.environment_id = config["environmentId"]
                    elif pool:
                        available = db.query(Environment).filter(Environment.id.in_(pool), Environment.status.is_(True)).all()
                        if not available:
                            raise ValueError("资源池没有启用的执行环境")
                        available.sort(key=lambda env: (not env.is_online, db.query(TaskQueue).filter(TaskQueue.environment_id == env.id, TaskQueue.status.in_(("pending", "running"))).count(), pool.index(env.id)))
                        suite.environment_id = available[0].id
                entries.append(dict(node=node, suite=suite, config=config, prerequisites=list(dict.fromkeys(deps))))
                branch = [node.id]
            leaves.extend(branch)
            if mode == "serial":
                previous = branch or previous
        return leaves
    walk(None, [], policy["executionMode"])
    # 功能用例由自动化结果驱动时不能作为该自动化的前置，否则形成隐含死锁。
    driven = {e["node"].linked_functional_id for e in entries if e["node"].linked_functional_id}
    for entry in entries:
        entry["prerequisites"] = [dep for dep in entry["prerequisites"] if dep not in driven]
    return entries
