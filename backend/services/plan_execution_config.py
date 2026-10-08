"""MS分类/测试集配置、动态继承、版本校验与执行时冻结。"""

from copy import deepcopy
from typing import Literal
from fastapi import HTTPException
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictInt,
    model_validator,
)
from models import Environment
from models.plan_workspace import PlanNode
from models.plan_workspace import PlanWorkspace
from models.plan_execution_config import PlanExecutionConfig, PlanResourcePool
from models.request_environment_group import RequestEnvironmentGroup
from models.native_case import ApiTestEnvironment
from services.review_workspace import lock_project
from core.logger import logger


class ExecutionConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    extended: StrictBool = True
    executionMode: Literal["serial", "parallel"] = "serial"
    testResourcePoolId: str = Field("DEFAULT", min_length=1, max_length=36)
    requestEnvironmentId: str = Field("NONE", min_length=1, max_length=36)
    requestEnvironmentGroupId: str = Field("NONE", min_length=1, max_length=36)
    stopOnFailure: StrictBool = False
    retryOnFailure: StrictBool = False
    retryTimes: StrictInt = Field(1, ge=1, le=10)
    retryInterval: StrictInt = Field(0, ge=0, le=2147483647)

    @model_validator(mode="after")
    def exclusive_environment(self):
        if (
            self.requestEnvironmentId != "NONE"
            and self.requestEnvironmentGroupId != "NONE"
        ):
            raise ValueError("请求环境和环境组只能选择一种")
        return self


class ConfigSave(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    config: ExecutionConfig
    expectedRevision: StrictInt = Field(ge=0)
    name: str | None = Field(None, min_length=1, max_length=255)
    expectedName: str | None = None


class PoolSave(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    name: str = Field(min_length=1, max_length=255)
    environmentIds: list[str] = Field(min_length=1, max_length=100)
    expectedRevision: StrictInt = Field(0, ge=0)


def scope_node(db, plan, scope):
    parts = scope.split(":")
    if len(parts) not in (2, 3) or parts[1] not in {"api", "scenario"}:
        raise HTTPException(422, "执行配置只支持API或场景分类根和测试集")
    if len(parts) == 2 and parts[0] in {"root", "default"}:
        return parts[1], None
    if len(parts) == 3 and parts[0] == "node":
        node = (
            db.query(PlanNode)
            .filter_by(id=parts[2], plan_id=plan.id)
            .populate_existing()
            .with_for_update()
            .one_or_none()
        )
        if node and node.node_type == "point":
            return parts[1], node
    raise HTTPException(404, "执行配置测试集不存在")


class ConfigurationTree:
    def __init__(self, db, plan, policy, nodes, *, current_read=False):
        self.db, self.plan, self.policy = db, plan, policy
        self.nodes = {node.id: node for node in nodes}
        query = db.query(PlanExecutionConfig).filter_by(plan_id=plan.id)
        rows = (
            query.populate_existing().with_for_update() if current_read else query
        ).all()
        self.rows = {row.scope: row for row in rows}

    def active(self, category):
        return any(row.category == category for row in self.rows.values())

    def effective(self, scope, seen=None):
        seen = set() if seen is None else seen
        if scope in seen:
            raise HTTPException(409, "执行配置的测试集层级形成循环")
        seen.add(scope)
        kind, category, *identity = scope.split(":")
        row = self.rows.get(scope)
        config = (
            ExecutionConfig.model_validate(row.config).model_dump()
            if row
            else ExecutionConfig().model_dump()
        )
        if kind == "root":
            if not row:
                config["executionMode"] = self.policy["executionMode"]
            config["extended"] = False
            return config
        if config["extended"]:
            node = self.nodes.get(identity[0]) if identity else None
            parent = (
                f"node:{category}:{node.parent_id}"
                if node and node.parent_id
                else f"root:{category}"
            )
            inherited = self.effective(parent, seen)
            return dict(inherited, extended=True)
        return config

    def data(self, scope):
        row = self.rows.get(scope)
        return dict(
            scope=scope,
            revision=row.revision if row else 0,
            config=(
                deepcopy(row.config)
                if row
                else ExecutionConfig(
                    extended=not scope.startswith("root:")
                ).model_dump()
            ),
            effectiveConfig=self.effective(scope),
        )

    def runtime(self, scope, fallback_environment):
        config = self.effective(scope)
        pool_id = config["testResourcePoolId"]
        if pool_id == "DEFAULT":
            members = [fallback_environment] if fallback_environment else []
        else:
            pool = (
                self.db.query(PlanResourcePool)
                .filter_by(id=pool_id, project_id=self.plan.project_id)
                .populate_existing()
                .with_for_update()
                .one_or_none()
            )
            if not pool:
                raise HTTPException(409, "执行资源池已删除或不属于计划项目")
            members = list(pool.environment_ids)
        enabled = (
            self.db.query(Environment)
            .filter(Environment.id.in_(members), Environment.status.is_(True))
            .populate_existing()
            .with_for_update()
            .all()
        )
        if not enabled:
            raise HTTPException(
                409, "执行资源池没有启用的节点，请配置资源池或计划默认执行节点"
            )
        enabled.sort(key=lambda env: (not env.is_online, members.index(env.id)))
        return config, enabled[0].id, [env.id for env in enabled]


def catalog(db, plan, policy, nodes):
    tree = ConfigurationTree(db, plan, policy, nodes)
    scopes = [
        f"{kind}:{category}"
        for category in ("api", "scenario")
        for kind in ("root", "default")
    ]
    scopes += [
        f"node:{category}:{node.id}"
        for node in nodes
        if node.node_type == "point"
        for category in ("api", "scenario")
    ]
    return dict(
        configurations={scope: tree.data(scope) for scope in scopes},
        pools=[
            dict(
                id=p.id,
                name=p.name,
                environmentIds=p.environment_ids,
                revision=p.revision,
            )
            for p in db.query(PlanResourcePool)
            .filter_by(project_id=plan.project_id)
            .order_by(PlanResourcePool.name, PlanResourcePool.id)
        ],
        requestEnvironmentGroups=[
            dict(id=g.id, name=g.name)
            for g in db.query(RequestEnvironmentGroup)
            .filter_by(project_id=plan.project_id)
            .order_by(RequestEnvironmentGroup.name, RequestEnvironmentGroup.id)
        ],
        requestEnvironments=[
            dict(id=e.id, name=e.name)
            for e in db.query(ApiTestEnvironment)
            .filter_by(project_id=plan.project_id)
            .order_by(ApiTestEnvironment.name, ApiTestEnvironment.id)
        ],
        resources=[
            dict(id=e.id, name=e.name, enabled=bool(e.status))
            for e in db.query(Environment).order_by(Environment.name, Environment.id)
        ],
    )


def save(db, plan, scope, data):
    lock_project(db, plan.project_id)
    ensure_editable(db, plan)
    category, node = scope_node(db, plan, scope)
    config = data.config.model_dump()
    if scope.startswith("root:") and config["extended"]:
        raise HTTPException(422, "分类根节点不能继承上级配置")
    if not config["extended"]:
        pool_id, target_id = (
            config["testResourcePoolId"],
            config["requestEnvironmentId"],
        )
        if (
            pool_id != "DEFAULT"
            and not db.query(PlanResourcePool)
            .filter_by(id=pool_id, project_id=plan.project_id)
            .populate_existing()
            .with_for_update()
            .one_or_none()
        ):
            raise HTTPException(422, "资源池不属于当前项目")
        group_id = config["requestEnvironmentGroupId"]
        if group_id != "NONE":
            from models.request_environment_group import RequestEnvironmentGroup

            if (
                not db.query(RequestEnvironmentGroup)
                .filter_by(id=group_id, project_id=plan.project_id)
                .populate_existing()
                .with_for_update()
                .one_or_none()
            ):
                raise HTTPException(422, "请求环境组不属于当前计划项目")
        if (
            target_id != "NONE"
            and not db.query(ApiTestEnvironment)
            .filter_by(id=target_id, project_id=plan.project_id)
            .populate_existing()
            .with_for_update()
            .one_or_none()
        ):
            raise HTTPException(422, "接口请求环境不属于当前项目")
    row = (
        db.query(PlanExecutionConfig)
        .filter_by(plan_id=plan.id, scope=scope)
        .populate_existing()
        .with_for_update()
        .one_or_none()
    )
    if (row.revision if row else 0) != data.expectedRevision:
        raise HTTPException(409, "执行配置已被其他页面修改，请刷新后重试")
    if data.name is not None:
        if not node or not data.name.strip():
            raise HTTPException(422, "请填写有效测试集名称")
        if data.expectedName != node.name:
            raise HTTPException(409, "测试集名称已变化，请刷新后重试")
        node.name = data.name.strip()
    if row:
        changed = (
            db.query(PlanExecutionConfig)
            .filter_by(plan_id=plan.id, scope=scope, revision=data.expectedRevision)
            .update(
                dict(config=config, revision=data.expectedRevision + 1),
                synchronize_session=False,
            )
        )
        if changed != 1:
            raise HTTPException(409, "执行配置已变化，请刷新后重试")
        db.refresh(row)
    else:
        row = PlanExecutionConfig(
            plan_id=plan.id,
            scope=scope,
            category=category,
            node_id=node.id if node else None,
            revision=1,
            config=config,
        )
        db.add(row)
    db.flush()
    logger.info(
        "已保存分类或测试集执行配置：计划={}，范围={}，版本={}，继承={}",
        plan.id,
        scope,
        row.revision,
        config["extended"],
    )
    return row


def save_pool(db, plan, data, pool_id=None):
    lock_project(db, plan.project_id)
    ensure_editable(db, plan)
    members = data.environmentIds
    if (
        not data.name.strip()
        or len(set(members)) != len(members)
        or any(not 1 <= len(member) <= 36 for member in members)
    ):
        raise HTTPException(422, "资源池名称和不重复的节点标识不能为空")
    resources = (
        db.query(Environment)
        .filter(Environment.id.in_(members), Environment.status.is_(True))
        .populate_existing()
        .with_for_update()
        .all()
    )
    if len(resources) != len(members):
        raise HTTPException(422, "资源池成员须为已启用的执行节点")
    row = (
        db.query(PlanResourcePool)
        .filter_by(id=pool_id, project_id=plan.project_id)
        .populate_existing()
        .with_for_update()
        .one_or_none()
        if pool_id
        else None
    )
    if pool_id and not row:
        raise HTTPException(404, "资源池不存在")
    if (row.revision if row else 0) != data.expectedRevision:
        raise HTTPException(409, "资源池已被修改，请刷新后重试")
    if row:
        changed = (
            db.query(PlanResourcePool)
            .filter_by(id=row.id, revision=data.expectedRevision)
            .update(
                dict(
                    name=data.name.strip(),
                    environment_ids=members,
                    revision=data.expectedRevision + 1,
                ),
                synchronize_session=False,
            )
        )
        if changed != 1:
            raise HTTPException(409, "资源池已变化，请刷新后重试")
        db.refresh(row)
    else:
        row = PlanResourcePool(
            project_id=plan.project_id,
            revision=1,
            name=data.name.strip(),
            environment_ids=members,
        )
        db.add(row)
    db.flush()
    logger.info(
        "已保存执行资源池：项目={}，资源池={}，节点数={}，版本={}",
        plan.project_id,
        row.id,
        len(members),
        row.revision,
    )
    return row


def ensure_editable(db, plan):
    workspace = (
        db.query(PlanWorkspace)
        .filter_by(plan_id=plan.id)
        .populate_existing()
        .with_for_update()
        .one_or_none()
    )
    if workspace and workspace.archived:
        raise HTTPException(409, "归档计划不能修改执行配置或资源池")
