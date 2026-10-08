"""分类根控制测试集顺序，测试集控制用例顺序；停止条件限定到对应分支。"""

from copy import deepcopy
from types import SimpleNamespace
from uuid import NAMESPACE_URL, uuid5
from fastapi import HTTPException
from models import TestCase, TestSuite, Environment
from services.native_http_execution import configured, freeze, managed_suite
from services.plan_tree import effective_config


def compile_selected_suites(db, plan, policy, suites, user):
    """Apply the same inherited configuration to the legacy suite selection.

    Temporary leaves use real association/collection IDs. Ordinary commands
    cannot be safely split by case, so configured selection rejects those
    instead of running a command repeatedly or ignoring its target settings.
    Unconfigured suite selection retains its existing behavior.
    """
    from models import PlanCaseRelation
    from services.plan_tree import nodes, compile_tree
    from services.plan_execution_config import ConfigurationTree
    from services.suite_dispatch import is_xat_command

    all_nodes = nodes(db, plan.id, current_read=True)
    configuration = ConfigurationTree(db, plan, policy, all_nodes, current_read=True)
    selected_ids = {cid for suite in suites for cid in suite.case_ids}
    cases = {
        case.id: case
        for case in db.query(TestCase)
        .filter(TestCase.id.in_(selected_ids), TestCase.deleted_at.is_(None))
        .populate_existing()
        .with_for_update()
        .all()
    }
    category = lambda case: case.type if case.type in {"api", "scenario"} else "api"
    if not any(configuration.active(category(case)) for case in cases.values()):
        return None
    if len(cases) != len(selected_ids):
        raise HTTPException(409, "所选测试套含已回收或不存在的用例")
    relations = (
        db.query(PlanCaseRelation)
        .filter_by(plan_id=plan.id)
        .populate_existing()
        .with_for_update()
        .all()
    )
    relation_map = {row.case_id: row for row in relations}
    scoped = [node for node in all_nodes if node.node_type == "point"]
    seen = set()
    for suite in suites:
        if not suite.case_ids:
            raise HTTPException(409, "分类执行配置需要测试套关联明确的用例范围")
        for cid in suite.case_ids:
            case = cases[cid]
            native = configured(db, case)
            if cid in seen:
                if native:
                    continue
                raise HTTPException(
                    409, "所选用例关联多个测试套，请在测试规划选择明确实例后执行"
                )
            if not native and not is_xat_command(suite.execution_command):
                raise HTTPException(
                    409,
                    "分类配置的测试套选择需要原生HTTP或支持用例过滤的XAT命令，请使用独立脚本入口执行普通脚本",
                )
            seen.add(cid)
            relation = relation_map.get(cid)
            scoped.append(
                SimpleNamespace(
                    id=(
                        relation.id
                        if relation
                        else str(
                            uuid5(
                                NAMESPACE_URL,
                                f"ats:selected:{plan.id}:{suite.id}:{cid}",
                            )
                        )
                    ),
                    parent_id=relation.collection_id if relation else None,
                    node_type="case",
                    category=category(case),
                    case_id=cid,
                    suite_id=suite.id,
                    name=case.name,
                    assigned_to=relation.assigned_to if relation else None,
                    linked_functional_id=None,
                    config={},
                )
            )
    # Legacy suite selection also carries the plan's manual work into the run.
    for relation in relations:
        if relation.case_id in seen:
            continue
        case = (
            db.query(TestCase)
            .filter_by(id=relation.case_id)
            .populate_existing()
            .with_for_update()
            .one_or_none()
        )
        if case and not case.deleted_at and not case.is_automated:
            scoped.append(
                SimpleNamespace(
                    id=relation.id,
                    parent_id=relation.collection_id,
                    node_type="case",
                    category="functional",
                    case_id=case.id,
                    suite_id=None,
                    name=case.name,
                    assigned_to=relation.assigned_to,
                    linked_functional_id=None,
                    config={},
                )
            )
    return compile_tree(
        db, plan, policy, current_read=True, scope_nodes=scoped, user=user
    )


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
        mapped_environment = None
        if (
            case
            and configured(db, case)
            and user
            and ms_config
            and ms_config.get("requestEnvironmentGroupId", "NONE") != "NONE"
        ):
            from services.request_environment_group import resolve

            mapped_environment = resolve(
                db,
                user,
                plan.project_id,
                case.project_id,
                ms_config["requestEnvironmentGroupId"],
            )
        if case and configured(db, case) and user:
            environment_id = (
                mapped_environment["environmentId"]
                if mapped_environment
                else (
                    ms_config["requestEnvironmentId"]
                    if ms_config and ms_config["requestEnvironmentId"] != "NONE"
                    else None
                )
            )
            native_case = freeze(
                db,
                case,
                user,
                environment_id=environment_id,
            )
        if active:
            if not native_case and (
                ms_config["retryOnFailure"]
                or ms_config["requestEnvironmentId"] != "NONE"
                or ms_config.get("requestEnvironmentGroupId", "NONE") != "NONE"
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
            if mapped_environment:
                ms_config = dict(
                    ms_config,
                    resolvedRequestEnvironmentId=mapped_environment["environmentId"],
                    requestEnvironmentGroupRevision=mapped_environment["groupRevision"],
                )
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
