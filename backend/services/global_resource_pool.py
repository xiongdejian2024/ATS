"""Independent pool authority, exact project scoping and frozen node membership."""

from hashlib import sha256
import json
from fastapi import HTTPException
from sqlalchemy import or_, func
from models import Project, User, Environment, TestPlan, TaskQueue
from models.global_resource_pool import (
    GlobalResourcePool as Pool,
    GlobalResourcePoolProject as PoolProject,
    GlobalResourcePoolMember as Member,
)
from core.permissions import has_global_permission
from core.project_access import require_project_access


def actor(db, user):
    current = (
        db.query(User)
        .filter_by(id=str(user.id))
        .populate_existing()
        .with_for_update(read=True)
        .one_or_none()
    )
    if not current or not current.status:
        raise HTTPException(403, "用户已停用或不存在")
    return current


def manages(db, user, *, current_read=False):
    return bool(
        user.status
        and has_global_permission(
            db, user.id, "system", "manage", current_read=current_read
        )
    )


def lock_admin(db, user):
    # All project locks precede the pool lock, matching configuration/run writes.
    # Admin pool writes are rare; this serializes scope/reference changes safely.
    db.query(Project.id).order_by(
        Project.id
    ).populate_existing().with_for_update().all()
    current = actor(db, user)
    if not manages(db, current, current_read=True):
        raise HTTPException(403, "需要现有系统管理权限")
    return current


def row(db, identity):
    value = (
        db.query(Pool)
        .filter_by(id=identity)
        .populate_existing()
        .with_for_update()
        .one_or_none()
    )
    if not value:
        raise HTTPException(404, "独立资源池不存在")
    return value


def visible_query(db, project_id, category=None, *, enabled=False):
    scope = db.query(PoolProject.pool_id).filter_by(project_id=project_id)
    query = db.query(Pool).filter(or_(Pool.all_projects.is_(True), Pool.id.in_(scope)))
    if enabled:
        query = query.filter(Pool.enabled.is_(True))
    if category == "api":
        query = query.filter(Pool.api_enabled.is_(True))
    elif category == "scenario":
        query = query.filter(Pool.scenario_enabled.is_(True))
    return query


def choices(db, project_id):
    return [
        dict(
            id=p.id,
            name=p.name,
            applications=(["api"] if p.api_enabled else [])
            + (["scenario"] if p.scenario_enabled else []),
        )
        for p in visible_query(db, project_id, enabled=True).order_by(
            Pool.name, Pool.id
        )
    ]


def catalog(db, user, project_id=None, page=1, size=20, search=None):
    if project_id:
        db.query(Project.id).filter_by(id=project_id).with_for_update().one_or_none()
    current = actor(db, user)
    admin = manages(db, current, current_read=True)
    if not admin:
        if not project_id:
            raise HTTPException(403, "请先选择有计划读取权限的项目")
        require_project_access(
            db, current, project_id, "test_plan:read", current_read=True
        )
    query = db.query(Pool) if admin else visible_query(db, project_id)
    if search:
        query = query.filter(Pool.name.contains(search, autoescape=True))
    total = query.count()
    pools = (
        query.order_by(Pool.created_at, Pool.id)
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    identities = [p.id for p in pools]
    members = (
        db.query(Member)
        .filter(Member.pool_id.in_(identities))
        .order_by(Member.pool_id, Member.position)
        .all()
        if identities
        else []
    )
    scoped = (
        db.query(PoolProject).filter(PoolProject.pool_id.in_(identities)).all()
        if admin and identities
        else []
    )
    environments = (
        db.query(
            Environment.id,
            Environment.name,
            Environment.status,
            Environment.is_online,
            Environment.max_concurrent_tasks,
        )
        .filter(Environment.id.in_({m.environment_id for m in members}))
        .all()
        if members
        else []
    )
    nodes = {n.id: n for n in environments}
    running = (
        dict(
            db.query(TaskQueue.environment_id, func.count(TaskQueue.id))
            .filter(TaskQueue.environment_id.in_(nodes), TaskQueue.status == "running")
            .group_by(TaskQueue.environment_id)
            .all()
        )
        if nodes
        else {}
    )
    items = []
    for pool in pools:
        node_ids = [m.environment_id for m in members if m.pool_id == pool.id]
        selected = [nodes[identity] for identity in node_ids if identity in nodes]
        configured = sum(
            max(1, n.max_concurrent_tasks or 1) for n in selected if n.status
        )
        online = sum(
            max(1, n.max_concurrent_tasks or 1)
            for n in selected
            if n.status and n.is_online
        )
        occupied = sum(running.get(n.id, 0) for n in selected)
        available = (
            sum(
                max(0, max(1, n.max_concurrent_tasks or 1) - running.get(n.id, 0))
                for n in selected
                if n.status and n.is_online
            )
            if pool.enabled
            else 0
        )
        items.append(
            dict(
                id=pool.id,
                name=pool.name,
                description=pool.description,
                type="Node",
                enabled=pool.enabled,
                applications=(["api"] if pool.api_enabled else [])
                + (["scenario"] if pool.scenario_enabled else []),
                allProjects=pool.all_projects,
                projectIds=(
                    [s.project_id for s in scoped if s.pool_id == pool.id]
                    if admin
                    else []
                ),
                environmentIds=node_ids,
                nodes=[
                    dict(
                        id=n.id,
                        name=n.name,
                        enabled=bool(n.status),
                        online=bool(n.is_online),
                        capacity=max(1, n.max_concurrent_tasks or 1),
                    )
                    for n in selected
                ],
                revision=pool.revision,
                capacity=dict(
                    configured=configured,
                    online=online,
                    running=occupied,
                    available=available,
                ),
            )
        )
    return dict(
        items=items, total=total, page=page, size=size, canEdit=admin, canDelete=admin
    )


def node_catalog(db, user, page=1, size=50, search=None):
    current = actor(db, user)
    if not manages(db, current, current_read=True):
        raise HTTPException(403, "需要现有系统管理权限")
    query = db.query(Environment)
    if search:
        query = query.filter(Environment.name.contains(search, autoescape=True))
    return dict(
        total=query.count(),
        page=page,
        size=size,
        items=[
            dict(
                id=n.id,
                name=n.name,
                enabled=bool(n.status),
                online=bool(n.is_online),
                capacity=max(1, n.max_concurrent_tasks or 1),
            )
            for n in query.order_by(Environment.name, Environment.id)
            .offset((page - 1) * size)
            .limit(size)
        ],
    )


def save(db, user, data, identity=None):
    current = lock_admin(db, user)
    value = row(db, identity) if identity else Pool(revision=0)
    if value.revision != data.expectedRevision:
        raise HTTPException(409, "资源池已被修改，请刷新后核对；草稿保留")
    projects = (
        db.query(Project.id)
        .filter(Project.id.in_(data.projectIds))
        .with_for_update()
        .all()
    )
    if len(projects) != len(data.projectIds):
        raise HTTPException(422, "适用项目已删除或不存在")
    body = data.model_dump(exclude={"requestId", "expectedRevision"})
    body["name"] = data.name.strip()
    body["projectIds"] = sorted(body["projectIds"])
    body["applications"] = sorted(body["applications"])
    fingerprint = sha256(
        json.dumps(
            body, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode()
    ).hexdigest()
    key = f"{current.id}:{data.requestId}" if not identity and data.requestId else None
    existing = (
        db.query(Pool)
        .filter_by(creation_key=key)
        .populate_existing()
        .with_for_update()
        .one_or_none()
        if key
        else None
    )
    nodes = (
        db.query(Environment)
        .filter(Environment.id.in_(data.environmentIds), Environment.status.is_(True))
        .order_by(Environment.id)
        .populate_existing()
        .with_for_update()
        .all()
    )
    if len(nodes) != len(data.environmentIds):
        raise HTTPException(422, "资源池成员须为已启用的现有Agent节点")
    if existing:
        if existing.creation_fingerprint != fingerprint:
            raise HTTPException(409, "创建请求ID已用于不同内容")
        return dict(id=existing.id, revision=1)
    value.name, value.description, value.updated_by = (
        data.name.strip(),
        data.description,
        str(current.id),
    )
    value.enabled, value.all_projects = data.enabled, data.allProjects
    value.api_enabled, value.scenario_enabled = (
        "api" in data.applications,
        "scenario" in data.applications,
    )
    value.revision += 1
    if key:
        value.creation_key, value.creation_fingerprint = key, fingerprint
    db.add(value)
    db.flush()
    db.query(PoolProject).filter_by(pool_id=value.id).delete(synchronize_session=False)
    db.query(Member).filter_by(pool_id=value.id).delete(synchronize_session=False)
    for project in data.projectIds:
        db.add(PoolProject(pool_id=value.id, project_id=project))
    for position, node in enumerate(data.environmentIds):
        db.add(Member(pool_id=value.id, environment_id=node, position=position))
    db.flush()
    return dict(id=value.id, revision=value.revision)


def set_enabled(db, user, identity, data):
    lock_admin(db, user)
    value = row(db, identity)
    if value.revision != data.expectedRevision:
        raise HTTPException(409, "资源池已被修改，请刷新后核对")
    value.enabled = data.enabled
    value.revision += 1
    db.flush()
    return dict(id=value.id, revision=value.revision)


def remove(db, user, identity, expected_revision):
    lock_admin(db, user)
    value = row(db, identity)
    if value.revision != expected_revision:
        raise HTTPException(409, "资源池已被修改，请刷新后核对")
    from models.plan_execution_config import PlanExecutionConfig

    if (
        db.query(PlanExecutionConfig.plan_id)
        .join(TestPlan, TestPlan.id == PlanExecutionConfig.plan_id)
        .filter(
            PlanExecutionConfig.config["testResourcePoolScope"].as_string() == "global",
            PlanExecutionConfig.config["testResourcePoolId"].as_string() == identity,
        )
        .populate_existing()
        .with_for_update()
        .first()
    ):
        raise HTTPException(409, "资源池仍被计划执行配置引用，请先改用其他资源池")
    db.query(PoolProject).filter_by(pool_id=identity).delete(synchronize_session=False)
    db.query(Member).filter_by(pool_id=identity).delete(synchronize_session=False)
    db.delete(value)
    db.flush()


def resolve(db, project_id, category, identity):
    value = row(db, identity)
    scope = (
        db.query(PoolProject)
        .filter_by(pool_id=identity, project_id=project_id)
        .populate_existing()
        .with_for_update()
        .one_or_none()
    )
    if (
        not value.enabled
        or not (value.all_projects or scope)
        or not (
            value.api_enabled
            if category == "api"
            else value.scenario_enabled if category == "scenario" else False
        )
    ):
        raise HTTPException(409, "独立资源池已停用或不适用于当前项目/分类")
    members = (
        db.query(Member)
        .filter_by(pool_id=identity)
        .order_by(Member.position)
        .populate_existing()
        .with_for_update()
        .all()
    )
    return value, [m.environment_id for m in members]
