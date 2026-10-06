"""规划脑图的完整结构草稿：锁内校验，名称、顺序、删除及配置原子保存。"""

import hashlib
import json
from uuid import UUID
from typing import Literal
from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field, StrictInt
from core.logger import logger
from core.project_access import require_project_access
from models import TestPlan, TestCase, TestSuite, PlanCaseRelation, User
from models.plan_workspace import PlanNode, PlanWorkspace
from models.plan_execution_config import PlanExecutionConfig
from models.plan_orchestration import PlanRun, PlanSettings
from services.plan_candidate_project import lock_run_sources, require_case_sources
from services.plan_execution_config import ConfigSave, ExecutionConfig
from services.plan_orchestration import ACTIVE, get_policy
from services import plan_tree

Category = Literal["functional", "api", "scenario"]


class CollectionDraft(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    id: str = Field(min_length=1, max_length=36)
    name: str = Field(min_length=1, max_length=255)
    category: Category
    parentId: str | None = Field(None, max_length=36)
    position: StrictInt = Field(ge=0, le=2147483647)
    materializeDefault: Category | None = None


class MinderSave(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    expectedFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    executionMode: Literal["serial", "parallel"] | None = None
    points: list[CollectionDraft] = Field(max_length=10000)
    deleteDefaults: list[Category] = Field(default_factory=list, max_length=3)
    configurations: dict[str, ConfigSave] = Field(
        default_factory=dict, max_length=10000
    )


def current_rows(db, model, **filters):
    return (
        db.query(model).filter_by(**filters).populate_existing().with_for_update().all()
    )


def state(db, plan):
    """指纹包含实际关联与执行模板，旧预览不能覆盖另一页的增删或配置。"""
    nodes = plan_tree.nodes(db, plan.id, current_read=True)
    relations = current_rows(db, PlanCaseRelation, plan_id=plan.id)
    suites = current_rows(db, TestSuite, plan_id=plan.id)
    configs = current_rows(db, PlanExecutionConfig, plan_id=plan.id)
    workspaces = current_rows(db, PlanWorkspace, plan_id=plan.id)
    ids = {r.case_id for r in relations} | {n.case_id for n in nodes if n.case_id}
    ids.update(cid for suite in suites for cid in suite.case_ids or [])
    cases = (
        db.query(TestCase)
        .filter(TestCase.id.in_(ids))
        .populate_existing()
        .with_for_update()
        .all()
    )
    workspace = workspaces[0] if workspaces else None

    def fields(row, names):
        return {name: getattr(row, name) for name in names}

    content = dict(
        plan=fields(
            plan, ["id", "project_id", "name", "environment_id", "environment_config"]
        ),
        workspace=fields(workspace, ["archived", "uses_tree"]) if workspace else None,
        policy=get_policy(db, plan.id, current_read=True),
        nodes=[
            fields(
                n,
                [
                    "id",
                    "parent_id",
                    "name",
                    "node_type",
                    "category",
                    "case_id",
                    "suite_id",
                    "assigned_to",
                    "linked_functional_id",
                    "position",
                    "config",
                ],
            )
            for n in nodes
        ],
        relations=[
            fields(
                r, ["id", "case_id", "collection_id", "execution_order", "assigned_to"]
            )
            for r in relations
        ],
        suites=[
            fields(s, ["id", "case_ids", "environment_id", "execution_command"])
            for s in suites
        ],
        configurations=[fields(c, ["scope", "revision", "config"]) for c in configs],
        cases=[fields(c, ["id", "project_id", "type", "deleted_at"]) for c in cases],
    )
    for name in ("nodes", "relations", "suites", "configurations", "cases"):
        content[name].sort(key=lambda item: item.get("id", item.get("scope", "")))
    fingerprint = hashlib.sha256(
        json.dumps(
            content,
            sort_keys=True,
            ensure_ascii=False,
            default=str,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    return dict(
        nodes=nodes,
        relations=relations,
        suites=suites,
        configs=configs,
        cases=cases,
        workspace=workspace,
        fingerprint=fingerprint,
    )


def locked_plan(db, user, plan_id, *, writing):
    initial = db.get(TestPlan, plan_id)
    if not initial:
        raise HTTPException(404, "测试计划不存在")
    require_project_access(
        db,
        user,
        initial.project_id,
        "test_plan:update" if writing else "test_plan:read",
    )
    target_id = initial.project_id
    try:
        sources = lock_run_sources(db, plan_id)
    except ValueError as exc:
        logger.exception("规划脑图来源锁定失败：计划={}", plan_id)
        raise HTTPException(409, str(exc)) from exc
    plan = (
        db.query(TestPlan)
        .filter_by(id=plan_id)
        .populate_existing()
        .with_for_update()
        .one_or_none()
    )
    if not plan or plan.project_id != target_id:
        raise HTTPException(409, "计划所属项目已变化，请刷新")
    current_user = (
        db.query(User)
        .filter_by(id=user.id)
        .populate_existing()
        .with_for_update()
        .one_or_none()
    )
    if not current_user or not current_user.status:
        raise HTTPException(403, "用户已停用或不存在")
    require_project_access(
        db,
        current_user,
        plan.project_id,
        "test_plan:update" if writing else "test_plan:read",
        current_read=True,
    )
    snapshot = state(db, plan)
    if {c.project_id for c in snapshot["cases"]} - sources:
        raise HTTPException(409, "关联来源已变化，请刷新后重试")
    return plan, current_user, snapshot


def workspace_data(db, plan, snapshot):
    from services.plan_case_workspace import entries
    from services.plan_execution_config import catalog

    rows = snapshot["nodes"]
    return dict(
        fingerprint=snapshot["fingerprint"],
        policy=get_policy(db, plan.id),
        nodes=[plan_tree.node_data(db, n) for n in rows],
        entries={
            category: entries(db, plan, category, current_read=True)[0]
            for category in ("functional", "api", "scenario")
        },
        executionCatalog=catalog(db, plan, get_policy(db, plan.id), rows),
        usesTree=bool(snapshot["workspace"] and snapshot["workspace"].uses_tree)
        or any(n.node_type != "point" for n in rows),
    )


def load(db, user, plan_id):
    plan, _, snapshot = locked_plan(db, user, plan_id, writing=False)
    result = workspace_data(db, plan, snapshot)
    logger.debug(
        "已读取一致的规划脑图：计划={}，节点数={}", plan.id, len(snapshot["nodes"])
    )
    return result


def save(db, user, plan_id, data):
    plan, user, snapshot = locked_plan(db, user, plan_id, writing=True)
    if snapshot["workspace"] and snapshot["workspace"].archived:
        raise HTTPException(409, "归档计划不可修改测试规划")
    if snapshot["fingerprint"] != data.expectedFingerprint:
        raise HTTPException(
            409, "测试规划或关联已被其他页面修改，请保留草稿并刷新后核对"
        )
    if (
        db.query(PlanRun)
        .filter(PlanRun.plan_id == plan.id, PlanRun.status.in_(ACTIVE))
        .populate_existing()
        .with_for_update()
        .first()
    ):
        raise HTTPException(409, "计划正在排队或执行，请结束后再修改测试规划")
    require_project_access(
        db, user, plan.project_id, "test_case:read", current_read=True
    )
    require_case_sources(db, user.id, snapshot["cases"], current_read=True)
    if data.executionMode is not None:
        settings = db.get(PlanSettings, plan.id) or PlanSettings(plan_id=plan.id)
        settings.execution_mode = data.executionMode
        db.add(settings)
        db.flush()
        logger.info(
            "计划根执行方式已进入规划事务：计划={}，方式={}",
            plan.id,
            data.executionMode,
        )
    originals = {n.id: n for n in snapshot["nodes"] if n.node_type == "point"}
    wanted = {p.id: p for p in data.points}
    if len(wanted) != len(data.points) or len(set(data.deleteDefaults)) != len(
        data.deleteDefaults
    ):
        raise HTTPException(422, "测试集或默认测试集标识不能重复")
    materialized = {}
    changed_categories = set(data.deleteDefaults)
    for point in data.points:
        original = originals.get(point.id)
        if not point.name.strip():
            raise HTTPException(422, "测试集名称不能为空")
        if original:
            if (
                point.parentId != original.parent_id
                or point.category != original.category
                or point.materializeDefault
            ):
                raise HTTPException(
                    422, "只能在原分类和父级内排序，不能改变测试集层级或分类"
                )
        else:
            try:
                if str(UUID(point.id)) != point.id:
                    raise ValueError("临时测试集标识不是规范UUID")
            except ValueError as exc:
                logger.exception("临时测试集标识无效：计划={}", plan.id)
                raise HTTPException(422, "新增测试集须使用有效UUID") from exc
            if point.parentId or db.get(PlanNode, point.id):
                raise HTTPException(
                    422, "新增测试集只能位于当前分类根，标识不能已被使用"
                )
        if point.parentId and point.parentId not in wanted:
            raise HTTPException(422, "保留的测试集不能属于已删除的父测试集")
        if not original or (original.name, original.position) != (
            point.name.strip(),
            point.position,
        ):
            changed_categories.add(point.category)
            if any(
                other.id != point.id
                and other.category == point.category
                and other.name.strip() == point.name.strip()
                for other in data.points
            ):
                raise HTTPException(422, "同一分类的测试集名称不能重复")
        if point.materializeDefault:
            if (
                point.materializeDefault != point.category
                or point.category in materialized
                or point.category in data.deleteDefaults
            ):
                raise HTTPException(422, "默认测试集转换不能重复、跨分类或同时删除")
            materialized[point.category] = point
    deleted_points = set(originals) - set(wanted)
    changed_categories.update(
        originals[identifier].category for identifier in deleted_points
    )
    # 子树关联随父集取消；保留的旧层级和混合分类投影不被扁平化。
    removed_nodes = set(deleted_points)
    while True:
        expanded = removed_nodes | {
            n.id for n in snapshot["nodes"] if n.parent_id in removed_nodes
        }
        if expanded == removed_nodes:
            break
        removed_nodes = expanded
    if removed_nodes.intersection(wanted):
        raise HTTPException(422, "不能删除父测试集而保留其子集")
    case_map = {case.id: case for case in snapshot["cases"]}

    def category_of(relation):
        case = case_map.get(relation.case_id)
        return case.type if case and case.type in ("api", "scenario") else "functional"

    uses = bool(snapshot["workspace"] and snapshot["workspace"].uses_tree) or any(
        n.node_type != "point" for n in snapshot["nodes"]
    )
    default_nodes = [
        n for n in snapshot["nodes"] if n.node_type != "point" and n.parent_id is None
    ]
    default_categories = (
        (
            {n.category for n in default_nodes}
            if uses
            else {
                category_of(r) for r in snapshot["relations"] if r.collection_id is None
            }
        )
        - set(data.deleteDefaults)
        - set(materialized)
    )
    for point in data.points:
        original = originals.get(point.id)
        if (
            point.name.strip() == "默认测试集"
            and point.category in default_categories
            and (
                not original
                or (original.name, original.position)
                != (point.name.strip(), point.position)
            )
        ):
            raise HTTPException(
                422, "同一分类已存在默认测试集，请改名或编辑原默认测试集"
            )
    if uses:
        removed_nodes.update(
            n.id for n in default_nodes if n.category in data.deleteDefaults
        )
    removed_relations = [
        r
        for r in snapshot["relations"]
        if r.collection_id in deleted_points
        or (
            not uses
            and r.collection_id is None
            and category_of(r) in data.deleteDefaults
        )
    ]
    removed_relation_ids = {r.id for r in removed_relations}
    removed_cases = {r.case_id for r in removed_relations}
    remaining_cases = {
        r.case_id for r in snapshot["relations"] if r.id not in removed_relation_ids
    }
    suites = {s.id: s for s in snapshot["suites"]}
    for node in snapshot["nodes"]:
        if node.id in removed_nodes or node.node_type == "point":
            continue
        remaining_cases.update(
            [node.case_id]
            if node.case_id
            else (
                suites[node.suite_id].case_ids or [] if node.suite_id in suites else []
            )
        )
    unlinked_cases = removed_cases - remaining_cases
    # 旧直接关联也驱动测试套范围；只移除已无任何实例覆盖的成员，历史快照独立保留。
    affected_suites = [
        s for s in snapshot["suites"] if unlinked_cases.intersection(s.case_ids or [])
    ]
    from services.test_suite_service import TestSuiteService

    for suite in affected_suites:
        try:
            TestSuiteService.require_idle(db, suite.id, current_read=True)
        except ValueError as exc:
            logger.exception(
                "活动测试套拒绝规划删除：计划={}，测试套={}", plan.id, suite.id
            )
            raise HTTPException(409, str(exc)) from exc
    for suite in affected_suites:
        suite.case_ids = [
            cid for cid in suite.case_ids or [] if cid not in unlinked_cases
        ]
    # 默认集只有用户改名或拖动后才实体化，不因打开脑图写入原数据。
    for point in data.points:
        original = originals.get(point.id)
        if original:
            original.name, original.position = point.name.strip(), point.position
        else:
            db.add(
                PlanNode(
                    id=point.id,
                    plan_id=plan.id,
                    name=point.name.strip(),
                    category=point.category,
                    node_type="point",
                    parent_id=None,
                    position=point.position,
                    config={},
                )
            )
    db.flush()
    for category, point in materialized.items():
        if uses:
            for node in default_nodes:
                if node.category == category:
                    node.parent_id = point.id
        else:
            for relation in snapshot["relations"]:
                if relation.collection_id is None and category_of(relation) == category:
                    relation.collection_id = point.id
        old_scope = f"default:{category}"
        old = next((c for c in snapshot["configs"] if c.scope == old_scope), None)
        if old:
            old.scope, old.node_id = f"node:{category}:{point.id}", point.id
    for relation in removed_relations:
        db.delete(relation)
    if uses and removed_nodes:
        plan_tree.remember_tree(db, plan.id)
    if removed_nodes:
        db.query(PlanNode).filter(
            PlanNode.plan_id == plan.id,
            PlanNode.linked_functional_id.in_(removed_nodes),
        ).update({"linked_functional_id": None}, synchronize_session="fetch")
        db.query(PlanExecutionConfig).filter(
            PlanExecutionConfig.plan_id == plan.id,
            PlanExecutionConfig.node_id.in_(removed_nodes),
        ).delete(synchronize_session="fetch")
        # 从叶到根显式清理，SQLite未开启FK时也与MySQL一致。
        pending = {n.id: n for n in snapshot["nodes"] if n.id in removed_nodes}
        while pending:
            leaves = [
                n
                for n in pending.values()
                if not any(child.parent_id == n.id for child in pending.values())
            ]
            if not leaves:
                raise HTTPException(409, "旧测试集层级形成循环，删除已回滚")
            for node in leaves:
                db.delete(node)
                pending.pop(node.id)
            db.flush()
    for category in data.deleteDefaults:
        db.query(PlanExecutionConfig).filter_by(
            plan_id=plan.id, scope=f"default:{category}"
        ).delete(synchronize_session="fetch")
    db.flush()
    from services.plan_execution_config import save as save_config

    for scope, config in data.configurations.items():
        if config.name is not None or config.expectedName is not None:
            raise HTTPException(422, "测试集名称须随完整规划结构提交")
        save_config(db, plan, scope, config)
    # 改动API/场景结构后启用真实分类顺序，避免只改变脑图而执行仍沿旧测试套顺序。
    for category in changed_categories - {"functional"}:
        scope = f"root:{category}"
        if (
            not db.query(PlanExecutionConfig)
            .filter_by(plan_id=plan.id, scope=scope)
            .first()
        ):
            save_config(
                db,
                plan,
                scope,
                ConfigSave(
                    config=ExecutionConfig(
                        extended=False,
                        executionMode=get_policy(db, plan.id)["executionMode"],
                    ),
                    expectedRevision=0,
                ),
            )
    db.flush()
    logger.info(
        "已原子保存测试规划：计划={}，新增集={}，删除节点={}，取消直接关联={}，默认集转换={}，配置数={}",
        plan.id,
        len(set(wanted) - set(originals)),
        len(removed_nodes),
        len(removed_relations),
        len(materialized),
        len(data.configurations),
    )
    return workspace_data(db, plan, state(db, plan))
