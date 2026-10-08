"""Versioned, project-scoped defect details and immutable collaboration evidence."""

from copy import deepcopy
from hashlib import sha256
from html import escape
import json
from fastapi import HTTPException
from sqlalchemy import or_
from models import Project, User, TestPlan
from models.case_features import CaseIssue as Issue, CaseIssueLink
from models.defect_workspace import (
    DefectTemplate as Template,
    DefectProfile as Profile,
    DefectComment as Comment,
    DefectEvent as Event,
)
from models.file_library import LibraryReference, LibraryFile
from core.project_access import require_project_access, project_allows
from services import file_library as files, mentions
from services.case_features import validate_custom_values


def authority(db, user, project_id, action="read"):
    project = (
        db.query(Project)
        .filter_by(id=project_id)
        .populate_existing()
        .with_for_update()
        .one_or_none()
    )
    if not project:
        raise HTTPException(404, "项目不存在")
    current = (
        db.query(User)
        .filter_by(id=str(user.id))
        .populate_existing()
        .with_for_update(read=True)
        .one_or_none()
    )
    if not current or not current.status:
        raise HTTPException(403, "用户已停用或不存在")
    require_project_access(
        db, current, project_id, "defect:" + action, current_read=True
    )
    return current, project


def allows(db, user, project_id, action="read", *, current_read=False):
    if current_read:
        project = (
            db.query(Project)
            .filter_by(id=project_id)
            .populate_existing()
            .with_for_update(read=True)
            .one_or_none()
        )
        user = (
            db.query(User)
            .filter_by(id=str(user.id))
            .populate_existing()
            .with_for_update(read=True)
            .one_or_none()
            if user
            else None
        )
    else:
        project = db.get(Project, project_id)
    return bool(
        project
        and user
        and project_allows(
            db, user, project, "defect:" + action, current_read=current_read
        )
    )


def capabilities(db, user, project_id):
    return {
        "can"
        + action.capitalize(): allows(db, user, project_id, action, current_read=True)
        for action in ["create", "read", "update", "delete"]
    }


def issue(db, project_id, identifier):
    row = (
        db.query(Issue)
        .filter_by(id=identifier, project_id=project_id, kind="defect")
        .populate_existing()
        .with_for_update()
        .one_or_none()
    )
    if not row:
        raise HTTPException(404, "此项目中不存在该缺陷")
    return row


def profile(db, row):
    return (
        db.query(Profile)
        .filter_by(issue_id=row.id)
        .populate_existing()
        .with_for_update()
        .one_or_none()
    )


def template_data(row):
    return dict(
        id=row.id,
        name=row.name,
        fields=row.fields,
        defaults=row.defaults,
        isDefault=row.is_default,
        revision=row.revision,
    )


def templates(db, user, project_id):
    authority(db, user, project_id)
    rows = (
        db.query(Template)
        .filter_by(project_id=project_id)
        .order_by(Template.name, Template.id)
        .limit(101)
        .all()
    )
    if len(rows) > 100:
        raise HTTPException(409, "模板超过100项，请缩小项目配置")
    return dict(
        items=[template_data(row) for row in rows], **capabilities(db, user, project_id)
    )


def save_template(db, user, project_id, data, identifier=None):
    user, _ = authority(db, user, project_id, "update")
    rows = (
        db.query(Template)
        .filter_by(project_id=project_id)
        .order_by(Template.id)
        .populate_existing()
        .with_for_update()
        .all()
    )
    row = (
        next((r for r in rows if r.id == identifier), None)
        if identifier
        else Template(project_id=project_id, revision=0)
    )
    if not row:
        raise HTTPException(404, "缺陷模板不存在")
    if row.revision != data.expectedRevision:
        raise HTTPException(409, "模板已修改，请刷新后核对；草稿保留")
    if not identifier and len(rows) >= 100:
        raise HTTPException(409, "每项目最多100个缺陷模板")
    name = data.name.strip()
    if any(r.id != identifier and r.name == name for r in rows):
        raise HTTPException(409, "此项目已有同名缺陷模板")
    fields = [f.model_dump() for f in data.fields]
    validate_custom_values(
        [{**f, "required": False} for f in fields],
        {f["key"]: f["default"] for f in fields if f["default"] is not None},
    )
    if (
        identifier
        and db.query(Profile.issue_id)
        .join(Issue, Issue.id == Profile.issue_id)
        .filter(Profile.template_id == identifier, Issue.project_id == project_id)
        .with_for_update()
        .first()
    ):
        for used in (
            db.query(Profile)
            .filter_by(template_id=identifier)
            .populate_existing()
            .with_for_update()
        ):
            try:
                validate_custom_values(fields, used.custom_fields)
            except (HTTPException, ValueError):
                raise HTTPException(
                    409, "此字段变更与现有缺陷值不兼容，请保留字段或新建模板"
                ) from None
    if data.isDefault:
        for other in rows:
            if other.id != identifier and other.is_default:
                other.is_default = False
                other.revision += 1
    row.name, row.fields, row.defaults, row.is_default = (
        name,
        fields,
        deepcopy(data.defaults),
        data.isDefault,
    )
    row.revision += 1
    row.updated_by = str(user.id)
    db.add(row)
    db.flush()
    return template_data(row)


def remove_template(db, user, project_id, identifier, revision):
    authority(db, user, project_id, "update")
    row = (
        db.query(Template)
        .filter_by(id=identifier, project_id=project_id)
        .populate_existing()
        .with_for_update()
        .one_or_none()
    )
    if not row:
        raise HTTPException(404, "缺陷模板不存在")
    if row.revision != revision:
        raise HTTPException(409, "模板已修改，请刷新后核对")
    if (
        db.query(Profile.issue_id)
        .join(Issue, Issue.id == Profile.issue_id)
        .filter(Profile.template_id == identifier, Issue.project_id == project_id)
        .with_for_update()
        .first()
    ):
        raise HTTPException(409, "模板仍被缺陷使用，不能删除")
    db.delete(row)
    db.flush()


def data(db, row, meta=None):
    meta = meta if meta is not None else profile(db, row)
    return dict(
        id=row.id,
        projectId=row.project_id,
        kind="defect",
        title=row.title,
        description=row.description,
        status=row.status,
        externalRef=row.external_ref,
        createdBy=row.created_by,
        updatedBy=row.updated_by,
        createdAt=row.created_at,
        updatedAt=row.updated_at,
        revision=meta.revision if meta else 0,
        templateId=meta.template_id if meta else None,
        customFields=meta.custom_fields if meta else {},
        descriptionFormat=meta.description_format if meta else "plain",
        archived=bool(meta and meta.archived),
    )


def listing(
    db, user, project_id, page=1, size=20, search="", status=None, archived=False
):
    user, _ = authority(db, user, project_id)
    query = (
        db.query(Issue, Profile)
        .outerjoin(Profile, Profile.issue_id == Issue.id)
        .filter(Issue.project_id == project_id, Issue.kind == "defect")
    )
    query = (
        query.filter(Profile.archived.is_(True))
        if archived
        else query.filter(or_(Profile.issue_id.is_(None), Profile.archived.is_(False)))
    )
    if search:
        query = query.filter(Issue.title.contains(search, autoescape=True))
    if status:
        query = query.filter(Issue.status == status)
    total = query.count()
    rows = (
        query.order_by(Issue.created_at.desc(), Issue.id)
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    return dict(
        items=[data(db, row, meta) for row, meta in rows],
        total=total,
        page=page,
        size=size,
        **capabilities(db, user, project_id),
    )


def detail(db, user, project_id, identifier):
    user, _ = authority(db, user, project_id)
    row = issue(db, project_id, identifier)
    meta = profile(db, row)
    return dict(
        **data(db, row, meta),
        files=files.references(db, project_id, "defect", identifier),
        **capabilities(db, user, project_id),
    )


def digest(payload):
    return sha256(
        json.dumps(
            payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")
        ).encode()
    ).hexdigest()


def image_ids(db, project_id, content, existing):
    parser = files.SourceParser()
    parser.feed(content)
    ids = set()
    for src in parser.sources:
        if "/file-library/" not in src:
            continue
        match = files.URL.fullmatch(src)
        if not match or match[1] != project_id:
            raise HTTPException(422, "富文本含有其他项目或无效文件库图片")
        row = files.find(db, project_id, match[2], lock=True)
        if row.mime_type not in files.IMAGE_TYPES.values():
            raise HTTPException(422, "此文件不是可预览图片")
        if row.archived and row.id not in existing:
            raise HTTPException(409, "新图片已归档，请重新选择")
        ids.add(row.id)
    return ids


def evidence(db, user, project_id, ids, kind, identifier, *, existing=()):
    # Only new selections need publication/archive checks; immutable retained
    # evidence can be carried forward even after its library entry is archived.
    files.reference(db, user, project_id, set(ids) - set(existing), kind, identifier)
    for fid in sorted(set(ids) & set(existing)):
        row = (
            db.query(LibraryReference)
            .filter_by(file_id=fid, entity_kind=kind, entity_id=identifier)
            .with_for_update()
            .first()
        )
        if row:
            row.active = True
        else:
            db.add(
                LibraryReference(
                    file_id=fid,
                    entity_kind=kind,
                    entity_id=identifier,
                    created_by=str(user.id),
                )
            )
    db.flush()


def event(db, user, row, meta, action, *, file_ids=(), comment=None):
    snapshot = data(db, row, meta)
    snapshot.pop("createdAt")
    snapshot.pop("updatedAt")
    item = Event(
        issue_id=row.id,
        actor_id=str(user.id),
        action=action,
        revision=meta.revision,
        detail=dict(
            snapshot=snapshot,
            fileIds=sorted(set(file_ids)),
            **(dict(commentId=comment.id, content=comment.content) if comment else {}),
        ),
    )
    db.add(item)
    db.flush()
    evidence(
        db, user, row.project_id, file_ids, "defect_event", item.id, existing=file_ids
    )
    return item


def save(db, user, project_id, input, identifier=None):
    user, _ = authority(db, user, project_id, "update" if identifier else "create")
    fingerprint = digest(input.model_dump(exclude={"requestId", "expectedRevision"}))
    key = (
        f"{project_id}:{user.id}:{input.requestId}"
        if not identifier and input.requestId
        else None
    )
    if key:
        old = (
            db.query(Profile)
            .filter_by(creation_key=key)
            .populate_existing()
            .with_for_update()
            .one_or_none()
        )
        if old:
            if old.creation_fingerprint != fingerprint:
                raise HTTPException(409, "同一请求编号不能创建不同缺陷")
            return dict(id=old.issue_id, revision=1, replayed=True)
    row = (
        issue(db, project_id, identifier)
        if identifier
        else Issue(project_id=project_id, kind="defect", created_by=str(user.id))
    )
    meta = profile(db, row) if identifier else None
    revision = meta.revision if meta else 0
    if revision != input.expectedRevision:
        raise HTTPException(409, "缺陷已修改，请刷新后核对；草稿保留")
    if meta and meta.archived:
        raise HTTPException(409, "缺陷已归档，请先恢复")
    values = input.model_dump()
    template = None
    if input.templateId:
        template = (
            db.query(Template)
            .filter_by(id=input.templateId, project_id=project_id)
            .populate_existing()
            .with_for_update()
            .one_or_none()
        )
        if not template:
            raise HTTPException(404, "此项目中不存在该缺陷模板")
    elif not identifier and "templateId" not in input.model_fields_set:
        template = (
            db.query(Template)
            .filter_by(project_id=project_id, is_default=True)
            .populate_existing()
            .with_for_update()
            .first()
        )
    if template and not identifier:
        for name, value in template.defaults.items():
            if name not in input.model_fields_set:
                values[name] = deepcopy(value)
    fields = validate_custom_values(
        template.fields if template else [], input.customFields
    )
    content = values["description"]
    recipients = []
    if input.descriptionFormat == "rich":
        content, recipients = mentions.prepare(
            db, user, project_id, content, context="defect", max_length=30000
        )
    current_refs = (
        db.query(LibraryReference)
        .filter_by(entity_kind="defect", entity_id=identifier or "", active=True)
        .populate_existing()
        .with_for_update()
        .all()
    )
    existing = {r.file_id for r in current_refs}
    selected = set(input.fileIds)
    if input.descriptionFormat == "rich":
        selected |= image_ids(db, project_id, content, existing)
    if len(selected) > 50:
        raise HTTPException(422, "描述图片和附件合计最多50个文件")
    row.title, row.description, row.status, row.external_ref = (
        values["title"].strip(),
        content,
        values["status"],
        values["externalRef"],
    )
    row.updated_by = str(user.id)
    db.add(row)
    db.flush()
    if not meta:
        meta = Profile(issue_id=row.id, revision=0)
        db.add(meta)
    meta.template_id = template.id if template else None
    meta.custom_fields = fields
    meta.description_format = input.descriptionFormat
    meta.revision = revision + 1
    meta.archived = False
    if key:
        meta.creation_key = key
        meta.creation_fingerprint = fingerprint
    evidence(db, user, project_id, selected, "defect", row.id, existing=existing)
    for ref in current_refs:
        if ref.file_id not in selected:
            ref.active = False
    db.flush()
    item = event(
        db, user, row, meta, "updated" if identifier else "created", file_ids=selected
    )
    mentions.notify(db, user, recipients, "defect_event", item.id)
    return dict(id=row.id, revision=meta.revision, replayed=False)


def set_archived(db, user, project_id, identifier, input):
    user, _ = authority(db, user, project_id, "delete")
    row = issue(db, project_id, identifier)
    meta = profile(db, row)
    if (meta.revision if meta else 0) != input.expectedRevision:
        raise HTTPException(409, "缺陷已修改，请刷新后核对")
    if not meta:
        meta = Profile(issue_id=identifier, revision=0)
        db.add(meta)
    meta.archived = input.archived
    meta.revision += 1
    db.flush()
    event(
        db,
        user,
        row,
        meta,
        "archived" if input.archived else "restored",
        file_ids=[
            r["id"] for r in files.references(db, project_id, "defect", identifier)
        ],
    )
    return dict(id=row.id, revision=meta.revision)


def comments(db, user, project_id, identifier, page=1):
    authority(db, user, project_id)
    issue(db, project_id, identifier)
    query = db.query(Comment).filter_by(issue_id=identifier, deleted=False)
    total = query.count()
    rows = (
        query.order_by(Comment.created_at, Comment.id)
        .offset((page - 1) * 20)
        .limit(20)
        .all()
    )
    return dict(
        items=[
            dict(
                id=c.id,
                authorId=c.author_id,
                content=c.content,
                createdAt=c.created_at,
                files=files.references(db, project_id, "defect_comment", c.id),
                canDelete=(
                    c.author_id == str(user.id)
                    and allows(db, user, project_id, "update", current_read=True)
                )
                or allows(db, user, project_id, "delete", current_read=True),
            )
            for c in rows
        ],
        total=total,
        page=page,
        size=20,
    )


def add_comment(db, user, project_id, identifier, input):
    user, _ = authority(db, user, project_id, "update")
    row = issue(db, project_id, identifier)
    meta = profile(db, row)
    key = f"{identifier}:{user.id}:{input.requestId}"
    fingerprint = digest(input.model_dump(exclude={"requestId", "expectedRevision"}))
    old = (
        db.query(Comment)
        .filter_by(creation_key=key)
        .populate_existing()
        .with_for_update()
        .one_or_none()
    )
    if old:
        if old.creation_fingerprint != fingerprint:
            raise HTTPException(409, "同一请求编号不能提交不同评论")
        return dict(id=old.id, revision=old.receipt_revision, replayed=True)
    if (meta.revision if meta else 0) != input.expectedRevision:
        raise HTTPException(409, "缺陷已修改，请刷新后核对；评论草稿保留")
    if meta and meta.archived:
        raise HTTPException(409, "归档缺陷不能新增评论")
    content, recipients = mentions.prepare(
        db, user, project_id, input.content, context="defect"
    )
    if not content.strip():
        raise HTTPException(422, "评论不能为空")
    selected = set(input.fileIds) | set(files.image_ids(db, project_id, content))
    if len(selected) > 50:
        raise HTTPException(422, "评论图片和附件合计最多50个文件")
    if not meta:
        meta = Profile(issue_id=identifier, revision=0)
        db.add(meta)
    meta.revision += 1
    comment = Comment(
        issue_id=identifier,
        author_id=str(user.id),
        content=content,
        creation_key=key,
        creation_fingerprint=fingerprint,
        receipt_revision=meta.revision,
    )
    db.add(comment)
    db.flush()
    files.reference(db, user, project_id, selected, "defect_comment", comment.id)
    event(db, user, row, meta, "commented", file_ids=selected, comment=comment)
    mentions.notify(db, user, recipients, "defect_comment", comment.id)
    return dict(id=comment.id, revision=meta.revision, replayed=False)


def delete_comment(db, user, project_id, identifier, comment_id, revision):
    user, _ = authority(db, user, project_id, "read")
    row = issue(db, project_id, identifier)
    meta = profile(db, row)
    if (meta.revision if meta else 0) != revision:
        raise HTTPException(409, "缺陷已修改，请刷新后核对")
    comment = (
        db.query(Comment)
        .filter_by(issue_id=identifier, id=comment_id, deleted=False)
        .populate_existing()
        .with_for_update()
        .one_or_none()
    )
    if not comment:
        raise HTTPException(404, "评论不存在或已删除")
    if not (
        allows(db, user, project_id, "delete", current_read=True)
        or (
            comment.author_id == str(user.id)
            and allows(db, user, project_id, "update", current_read=True)
        )
    ):
        raise HTTPException(403, "只能删除本人评论或使用缺陷删除权限")
    if meta and meta.archived:
        raise HTTPException(409, "归档缺陷不能修改评论")
    comment.deleted = True
    meta.revision += 1
    db.flush()
    event(
        db,
        user,
        row,
        meta,
        "comment_removed",
        file_ids=[
            r["id"]
            for r in files.references(db, project_id, "defect_comment", comment.id)
        ],
        comment=comment,
    )
    return dict(id=identifier, revision=meta.revision)


def history(db, user, project_id, identifier, page=1):
    authority(db, user, project_id)
    issue(db, project_id, identifier)
    query = db.query(Event).filter_by(issue_id=identifier)
    total = query.count()
    rows = (
        query.order_by(Event.revision.desc(), Event.created_at.desc(), Event.id)
        .offset((page - 1) * 20)
        .limit(20)
        .all()
    )
    return dict(
        items=[
            dict(
                id=r.id,
                actorId=r.actor_id,
                action=r.action,
                revision=r.revision,
                detail=r.detail,
                createdAt=r.created_at,
                files=files.references(db, project_id, "defect_event", r.id),
            )
            for r in rows
        ],
        total=total,
        page=page,
        size=20,
    )


def legacy_save(db, user, project_id, body, identifier=None):
    """Keep old basic clients and identities; independent authority still applies.

    Rich/template profiles require their revision before a legacy update so old
    four-field dialogs cannot erase detail edits they never loaded.
    """
    user, _ = authority(db, user, project_id, "update" if identifier else "create")
    row = issue(db, project_id, identifier) if identifier else None
    meta = profile(db, row) if row else None
    from schemas.defect_workspace import DefectWrite

    expected = getattr(body, "expectedRevision", None)
    if (
        identifier
        and meta
        and (
            meta.template_id
            or meta.description_format == "rich"
            or meta.custom_fields
            or files.references(db, project_id, "defect", identifier)
        )
        and expected is None
    ):
        raise HTTPException(409, "该缺陷已有完整详情，请打开缺陷工作区核对版本后修改")
    input = DefectWrite(
        title=body.title,
        description=body.description,
        status=body.status,
        externalRef=body.externalRef,
        templateId=meta.template_id if meta else None,
        customFields=meta.custom_fields if meta else {},
        fileIds=(
            [r["id"] for r in files.references(db, project_id, "defect", identifier)]
            if identifier
            else []
        ),
        expectedRevision=(
            expected if expected is not None else meta.revision if meta else 0
        ),
    )
    receipt = save(db, user, project_id, input, identifier)
    return db.get(Issue, receipt["id"])


def require_associable(db, user, project_id, identifier):
    authority(db, user, project_id, "read")
    row = issue(db, project_id, identifier)
    meta = profile(db, row)
    if meta and meta.archived:
        raise HTTPException(409, "归档缺陷不能新增关联")
    return row
