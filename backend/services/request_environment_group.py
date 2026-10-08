"""当前权限、固定项目锁顺序及批次冻结前的跨项目环境解析。"""

from fastapi import HTTPException
from hashlib import sha256
import json
from models import Project, TestPlan, User
from models.native_case import ApiTestEnvironment
from models.request_environment_group import (
    RequestEnvironmentGroup,
    RequestEnvironmentMapping,
)
from core.project_access import require_project_access, project_allows


def _actor(db, user):
    actor = (
        db.query(User)
        .filter_by(id=str(user.id))
        .populate_existing()
        .with_for_update(read=True)
        .one_or_none()
    )
    if not actor or not actor.status:
        raise HTTPException(403, "用户已停用或不存在")
    return actor


def _row(db, project_id, identity, *, lock=False):
    query = (
        db.query(RequestEnvironmentGroup)
        .filter_by(id=identity, project_id=project_id)
        .populate_existing()
    )
    value = (query.with_for_update() if lock else query).one_or_none()
    if not value:
        raise HTTPException(404, "请求环境组不存在或不属于当前项目")
    return value


def catalog(db, user, project_id, page=1, size=20, search=None):
    project = require_project_access(db, user, project_id, "test_plan:read")
    query = db.query(RequestEnvironmentGroup).filter_by(project_id=project_id)
    if search:
        query = query.filter(
            RequestEnvironmentGroup.name.contains(search, autoescape=True)
        )
    total = query.count()
    groups = (
        query.order_by(RequestEnvironmentGroup.created_at, RequestEnvironmentGroup.id)
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    # 分组不包含目标地址或其他来源环境内容；每个来源目录独立授权。
    mappings = (
        db.query(RequestEnvironmentMapping)
        .filter(RequestEnvironmentMapping.group_id.in_([g.id for g in groups]))
        .all()
        if groups
        else []
    )
    by_group = {}
    for mapping in mappings:
        by_group.setdefault(mapping.group_id, []).append(
            dict(
                projectId=mapping.source_project_id,
                environmentId=mapping.environment_id,
            )
        )
    return dict(
        total=total,
        page=page,
        size=size,
        items=[
            dict(
                id=g.id,
                name=g.name,
                description=g.description,
                revision=g.revision,
                mappings=by_group.get(g.id, []),
            )
            for g in groups
        ],
        canEdit=project_allows(db, user, project, "test_plan:update"),
        canDelete=project_allows(db, user, project, "test_plan:delete"),
    )


def source_catalog(db, user, project_id):
    require_project_access(db, user, project_id, "test_case:read")
    return [
        dict(id=e.id, name=e.name)
        for e in db.query(ApiTestEnvironment)
        .filter_by(project_id=project_id)
        .order_by(ApiTestEnvironment.name, ApiTestEnvironment.id)
    ]


def save(db, user, project_id, data, identity=None):
    require_project_access(db, user, project_id, "test_plan:update")
    previous = (
        db.query(RequestEnvironmentMapping.source_project_id)
        .filter_by(group_id=identity)
        .all()
        if identity
        else []
    )
    project_ids = {
        project_id,
        *(m.projectId for m in data.mappings),
        *(p[0] for p in previous),
    }
    for pid in sorted(project_ids):
        if (
            not db.query(Project)
            .filter_by(id=pid)
            .populate_existing()
            .with_for_update()
            .one_or_none()
        ):
            raise HTTPException(404, "来源项目不存在")
    actor = _actor(db, user)
    require_project_access(db, actor, project_id, "test_plan:update", current_read=True)
    creation_key = (
        f"{project_id}:{actor.id}:{data.requestId}"
        if not identity and data.requestId
        else None
    )
    fingerprint_body = data.model_dump(exclude={"requestId", "expectedRevision"})
    fingerprint_body["name"] = data.name.strip()
    fingerprint_body["mappings"] = sorted(
        fingerprint_body["mappings"], key=lambda m: m["projectId"]
    )
    fingerprint = sha256(
        json.dumps(
            fingerprint_body, sort_keys=True, ensure_ascii=False, separators=(",", ":")
        ).encode()
    ).hexdigest()
    existing = (
        db.query(RequestEnvironmentGroup)
        .filter_by(creation_key=creation_key)
        .populate_existing()
        .with_for_update()
        .one_or_none()
        if creation_key
        else None
    )
    if existing and existing.creation_fingerprint != fingerprint:
        raise HTTPException(409, "创建请求ID已用于不同内容，请核对已保存环境组")
    row = (
        _row(db, project_id, identity, lock=True)
        if identity
        else RequestEnvironmentGroup(project_id=project_id, revision=0)
    )
    if row.revision != data.expectedRevision:
        raise HTTPException(409, "环境组已被修改，请刷新后重试；草稿保留")
    environments = {}
    for mapping in sorted(data.mappings, key=lambda m: m.projectId):
        require_project_access(
            db, actor, mapping.projectId, "test_case:read", current_read=True
        )
        environment = (
            db.query(ApiTestEnvironment)
            .filter_by(id=mapping.environmentId, project_id=mapping.projectId)
            .populate_existing()
            .with_for_update()
            .one_or_none()
        )
        if not environment:
            raise HTTPException(422, "映射请求环境不属于对应来源项目")
        environments[mapping.projectId] = environment.id
    if existing:
        return existing
    if creation_key:
        row.creation_key, row.creation_fingerprint = creation_key, fingerprint
    row.name, row.description, row.updated_by = (
        data.name.strip(),
        data.description,
        str(actor.id),
    )
    row.revision += 1
    db.add(row)
    db.flush()
    db.query(RequestEnvironmentMapping).filter_by(group_id=row.id).delete(
        synchronize_session=False
    )
    for source_id, environment_id in environments.items():
        db.add(
            RequestEnvironmentMapping(
                group_id=row.id,
                source_project_id=source_id,
                environment_id=environment_id,
            )
        )
    db.flush()
    return row


def remove(db, user, project_id, identity, expected_revision):
    require_project_access(db, user, project_id, "test_plan:delete")
    db.query(Project).filter_by(
        id=project_id
    ).populate_existing().with_for_update().one_or_none()
    require_project_access(
        db, _actor(db, user), project_id, "test_plan:delete", current_read=True
    )
    row = _row(db, project_id, identity, lock=True)
    if row.revision != expected_revision:
        raise HTTPException(409, "环境组已被修改，请刷新后重试")
    from models.plan_execution_config import PlanExecutionConfig

    if (
        db.query(PlanExecutionConfig.plan_id)
        .join(TestPlan, TestPlan.id == PlanExecutionConfig.plan_id)
        .filter(
            TestPlan.project_id == project_id,
            PlanExecutionConfig.config["requestEnvironmentGroupId"].as_string()
            == identity,
        )
        .populate_existing()
        .with_for_update()
        .first()
    ):
        raise HTTPException(409, "环境组仍被执行配置引用，请先改用其他环境")
    db.query(RequestEnvironmentMapping).filter_by(group_id=identity).delete(
        synchronize_session=False
    )
    db.delete(row)
    db.flush()


def resolve(db, user, owner_project_id, source_project_id, group_id):
    """只在创建批次时读取当前映射；后续调度继续使用原生请求冻结内容。"""
    actor = _actor(db, user)
    require_project_access(
        db, actor, owner_project_id, "test_plan:execute", current_read=True
    )
    require_project_access(
        db, actor, source_project_id, "test_case:read", current_read=True
    )
    group = _row(db, owner_project_id, group_id, lock=True)
    mapping = (
        db.query(RequestEnvironmentMapping)
        .filter_by(group_id=group_id, source_project_id=source_project_id)
        .populate_existing()
        .with_for_update()
        .one_or_none()
    )
    if not mapping:
        raise HTTPException(409, "请求环境组未配置该用例来源项目的环境映射")
    environment = (
        db.query(ApiTestEnvironment)
        .filter_by(id=mapping.environment_id, project_id=source_project_id)
        .populate_existing()
        .with_for_update()
        .one_or_none()
    )
    if not environment:
        raise HTTPException(409, "请求环境组映射已失效，请更新配置")
    return dict(
        environmentId=environment.id, groupId=group.id, groupRevision=group.revision
    )
