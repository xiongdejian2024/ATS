"""分类根控制测试集顺序，测试集控制用例顺序；停止条件限定到对应分支。"""

from copy import deepcopy
from types import SimpleNamespace
from fastapi import HTTPException
from models import TestCase, TestSuite, Environment
from services.native_http_execution import configured, freeze, managed_suite
from services.plan_tree import effective_config


def compile_configured_tree(db, plan, policy, all_nodes, configurations, user):
    node_map = {node.id: node for node in all_nodes}
    entries = []

    def leaf(node, category, scope, dependencies, stop_dependencies):
        case = db.get(TestCase, node.case_id) if node.case_id else None
        if node.case_id and (not case or case.deleted_at):
            raise HTTPException(409, "测试集包含已回收或不存在的用例")
        suite = db.get(TestSuite, node.suite_id) if node.suite_id else None
        old = effective_config(db, node, node_map=node_map, plan=plan)
        runtime = deepcopy(old)
        native_case = None
        active = configurations.active(category)
        ms_config = configurations.effective(scope) if active else None
        if case and configured(db, case) and user:
            native_case = freeze(
                db,
                case,
                user,
                environment_id=(
                    ms_config["requestEnvironmentId"]
                    if ms_config and ms_config["requestEnvironmentId"] != "NONE"
                    else None
                ),
            )
        if active:
            if not native_case and (
                ms_config["retryOnFailure"]
                or ms_config["requestEnvironmentId"] != "NONE"
            ):
                raise HTTPException(
                    409,
                    "请求环境和步骤重试需要已配置原生HTTP请求的API或场景；请先在用例详情完成配置",
                )
            fallback = (
                old.get("environmentId")
                or (suite.environment_id if suite else None)
                or plan.environment_id
            )
            ms_config, resource_id, members = configurations.runtime(scope, fallback)
            runtime = dict(
                executionMode=ms_config["executionMode"],
                environmentId=resource_id,
                resourcePool=members,
                msExecution=ms_config,
            )
            if native_case:
                native_case.update(
                    retryTimes=(
                        ms_config["retryTimes"] if ms_config["retryOnFailure"] else 0
                    ),
                    retryInterval=ms_config["retryInterval"],
                )
        else:
            members = old.get("resourcePool") or []
            available = (
                db.query(Environment)
                .filter(Environment.id.in_(members), Environment.status.is_(True))
                .all()
                if members
                else []
            )
            if members and not available:
                raise HTTPException(409, "旧资源池没有启用的节点")
            available.sort(key=lambda env: (not env.is_online, members.index(env.id)))
            resource_id = (
                old.get("environmentId")
                or (available[0].id if available else None)
                or (suite.environment_id if suite else None)
                or plan.environment_id
            )
        if native_case:
            suite = managed_suite(db, plan, case, resource_id, user.id)
        if suite:
            suite = SimpleNamespace(
                **{
                    column.name: deepcopy(getattr(suite, column.name))
                    for column in TestSuite.__table__.columns
                }
            )
            if node.case_id:
                suite.case_ids = [node.case_id]
            suite.environment_id = resource_id
        entries.append(
            dict(
                node=node,
                suite=suite,
                config=runtime,
                prerequisites=list(dict.fromkeys(dependencies)),
                stopPrerequisites=list(dict.fromkeys(stop_dependencies)),
                nativeCase=native_case,
            )
        )
        return [node.id]

    for category in ("functional", "api", "scenario"):
        selected = [
            node
            for node in all_nodes
            if node.node_type != "point" and node.category == category
        ]
        selected_ids = {node.id for node in selected}
        visible = set()
        for node in selected:
            parent, seen = node.parent_id, set()
            while parent:
                if parent in seen or parent not in node_map:
                    raise HTTPException(409, "测试集层级无效或形成循环")
                seen.add(parent)
                visible.add(parent)
                parent = node_map[parent].parent_id
        children = {}
        for node in all_nodes:
            if node.id in selected_ids or node.id in visible:
                children.setdefault(node.parent_id, []).append(node)
        active = configurations.active(category)
        root_scope = f"root:{category}"
        root_config = (
            configurations.effective(root_scope)
            if active
            else dict(executionMode=policy["executionMode"], stopOnFailure=False)
        )

        def collection(parent_id, scope, deps, stop_deps):
            config = (
                configurations.effective(scope)
                if active
                else (
                    effective_config(
                        db, node_map[parent_id], node_map=node_map, plan=plan
                    )
                    if parent_id
                    else {}
                )
            )
            mode = config.get("executionMode", root_config["executionMode"])
            stop = active and mode == "serial" and config["stopOnFailure"]
            previous, leaves = list(deps), []
            for node in children.get(parent_id, []):
                before = previous if mode == "serial" else list(deps)
                guards = list(stop_deps) + (previous if stop else [])
                if node.node_type == "point":
                    branch = collection(
                        node.id, f"node:{category}:{node.id}", before, guards
                    )
                else:
                    branch = leaf(node, category, scope, before, guards)
                leaves.extend(branch)
                if mode == "serial" and branch:
                    previous = branch
            return leaves

        # 无归属用例组成默认测试集，根节点串行时按测试集整体等待。
        default = [node for node in children.get(None, []) if node.node_type != "point"]
        groups = [(None, f"default:{category}", default)] if default else []
        groups += [
            (node.id, f"node:{category}:{node.id}", children.get(node.id, []))
            for node in children.get(None, [])
            if node.node_type == "point"
        ]
        previous = []
        for parent, scope, unused in groups:
            deps = previous if root_config["executionMode"] == "serial" else []
            stop_deps = (
                deps
                if root_config["executionMode"] == "serial"
                and root_config["stopOnFailure"]
                else []
            )
            if parent is None:
                original = children.get(None, [])
                children[None] = default
                branch = collection(None, scope, deps, stop_deps)
                children[None] = original
            else:
                branch = collection(parent, scope, deps, stop_deps)
            if branch and root_config["executionMode"] == "serial":
                previous = branch
    driven = {
        entry["node"].linked_functional_id
        for entry in entries
        if entry["node"].linked_functional_id
    }
    for entry in entries:
        entry["prerequisites"] = [
            dep for dep in entry["prerequisites"] if dep not in driven
        ]
        entry["stopPrerequisites"] = [
            dep for dep in entry["stopPrerequisites"] if dep not in driven
        ]
    return entries
