"""用例扩展服务：附件存储、回收站和可追溯变更。"""

import os
import uuid
from pathlib import Path
from fastapi import HTTPException
from core.logger import logger
from core.project_access import require_project_access
from models.test_case import TestCase, CaseAttachment
from models.case_features import CaseChange
from utils.file_handler import validate_file_upload, secure_filename, save_upload_file
from utils.datetime_utils import beijing_now
from copy import deepcopy
from datetime import date
from models.case_features import (
    CaseTemplate,
    CaseIssue,
    CaseIssueLink,
    CaseRelation,
    CaseAutomationLink,
    CaseFollow,
    CaseComment,
)
from utils.serializer import serialize_model


def validate_custom_values(fields, values):
    if not isinstance(values, dict):
        raise HTTPException(422, "自定义字段值必须是对象")
    allowed = {field["key"] for field in fields}
    if set(values) - allowed:
        raise HTTPException(422, "存在模板未定义的自定义字段")
    output = deepcopy(values)
    for field in fields:
        key, kind = field["key"], field["type"]
        value = output.get(key, field.get("default"))
        if value is None or value == "" or value == []:
            if field.get("required"):
                raise HTTPException(422, f"自定义字段 {field['name']} 为必填项")
            output[key] = value
            continue
        valid = True
        if kind in {"text", "textarea"}:
            valid = isinstance(value, str) and len(value) <= 10000
        elif kind == "number":
            import math

            valid = type(value) in {int, float} and math.isfinite(value)
        elif kind == "boolean":
            valid = type(value) is bool
        elif kind == "date":
            try:
                valid = (
                    isinstance(value, str)
                    and date.fromisoformat(value).isoformat() == value
                )
            except (TypeError, ValueError):
                valid = False
        elif kind == "select":
            valid = value in field.get("options", [])
        elif kind == "multiselect":
            valid = (
                isinstance(value, list)
                and all(
                    isinstance(v, str) and v in field.get("options", []) for v in value
                )
                and len(value) == len(set(value))
            )
        if not valid:
            raise HTTPException(422, f"自定义字段 {field['name']} 的值或类型不合法")
        output[key] = value
    return output


def prepare_case_template(db, project_id, data, fields_set, existing=None):
    template_id = (
        data.get("template_id")
        if "template_id" in fields_set
        else (existing.template_id if existing else None)
    )
    template = None
    if template_id:
        template = (
            db.query(CaseTemplate)
            .filter_by(id=template_id, project_id=project_id)
            .first()
        )
        if not template:
            raise HTTPException(422, "用例模板不属于当前项目")
    elif existing is None and "template_id" not in fields_set:
        template = (
            db.query(CaseTemplate)
            .filter_by(project_id=project_id, is_default=True)
            .first()
        )
    if existing is None and template:
        for key, value in template.defaults.items():
            if key not in fields_set:
                data[key] = deepcopy(value)
    values = (
        data.get("custom_fields")
        if "custom_fields" in fields_set
        else (existing.custom_fields if existing else {})
    )
    data["custom_fields"] = validate_custom_values(
        template.fields if template else [], values or {}
    )
    data["template_id"] = template.id if template else None
    return data


def write_template(db, user, project_id, body, identifier=None):
    require_project_access(db, user, project_id, "test_case:update")
    # 锁定项目保证同一事务只能产生一个默认模板。
    from models.project import Project

    db.query(Project).filter_by(id=project_id).with_for_update().first()
    row = (
        db.query(CaseTemplate).filter_by(id=identifier, project_id=project_id).first()
        if identifier
        else CaseTemplate(project_id=project_id, created_by=str(user.id))
    )
    if not row:
        raise HTTPException(404, "模板不存在")
    if body.isDefault:
        db.query(CaseTemplate).filter_by(project_id=project_id).update(
            {"is_default": False}
        )
    row.name, row.fields, row.defaults, row.is_default = (
        body.name,
        [f.model_dump() for f in body.fields],
        body.defaults,
        body.isDefault,
    )
    # 校验有默认值的字段；必填字段允许由创建用例时填写。
    validate_custom_values(
        [{**f, "required": False} for f in row.fields],
        {f["key"]: f["default"] for f in row.fields if f.get("default") is not None},
    )
    from schemas.test_case import TestCaseCreate

    try:
        TestCaseCreate(
            project_id=project_id,
            name="模板校验",
            **{"type": "functional", **row.defaults},
        )
    except ValueError as exc:
        raise HTTPException(422, "模板默认属性不合法") from exc
    if row.defaults.get("priority", "P2") not in {"P0", "P1", "P2", "P3"}:
        raise HTTPException(422, "模板默认优先级不合法")
    db.add(row)
    db.flush()
    logger.info("用例模板已保存 project_id={} template_id={}", project_id, row.id)
    return row


def issue_for_project(db, project_id, identifier):
    row = db.query(CaseIssue).filter_by(id=identifier, project_id=project_id).first()
    if not row:
        raise HTTPException(404, "需求或缺陷不存在")
    return row


def write_issue(db, user, project_id, body, identifier=None):
    require_project_access(db, user, project_id, "test_case:update")
    row = (
        issue_for_project(db, project_id, identifier)
        if identifier
        else CaseIssue(project_id=project_id, created_by=str(user.id))
    )
    if identifier and row.kind != body.kind:
        raise HTTPException(422, "已创建实体不能切换需求或缺陷类型")
    for key, value in body.model_dump().items():
        setattr(row, "external_ref" if key == "externalRef" else key, value)
    row.updated_by = str(user.id)
    db.add(row)
    db.flush()
    logger.info("需求缺陷实体已保存 project_id={} issue_id={}", project_id, row.id)
    return row


def add_relation(db, user, project_id, case_id, body):
    case = find_case(db, user, project_id, case_id, "update", lock=True)
    find_case(db, user, project_id, body.targetCaseId)
    if case_id == body.targetCaseId:
        raise HTTPException(422, "用例不能关联自身")
    source, target = (
        (body.targetCaseId, case_id)
        if body.kind == "precondition"
        else (case_id, body.targetCaseId)
    )
    kind = "related" if body.kind == "related" else "dependency"
    if kind == "related":
        source, target = sorted([source, target])
    else:
        from models.project import Project

        db.query(Project).filter_by(id=project_id).with_for_update().first()
        rows = (
            db.query(CaseRelation)
            .filter_by(project_id=project_id, kind="dependency")
            .all()
        )
        graph = {}
        for row in rows:
            graph.setdefault(row.source_case_id, []).append(row.target_case_id)
        todo, seen = [target], set()
        while todo:
            node = todo.pop()
            if node == source:
                raise HTTPException(422, "前后置关系不能形成循环")
            if node not in seen:
                seen.add(node)
                todo.extend(graph.get(node, []))
    row = CaseRelation(
        project_id=project_id,
        source_case_id=source,
        target_case_id=target,
        kind=kind,
        created_by=str(user.id),
    )
    db.add(row)
    db.flush()
    change(
        db,
        case,
        user.id,
        "关联用例",
        {"targetCaseId": body.targetCaseId, "kind": body.kind},
    )
    return row


def relation_data(db, row, case_id):
    target_id = (
        row.target_case_id if row.source_case_id == case_id else row.source_case_id
    )
    target = db.get(TestCase, target_id)
    return dict(
        id=row.id,
        targetCaseId=target_id,
        name=target.name if target else "已删除用例",
        caseCode=target.case_code if target else None,
        deleted=bool(not target or target.deleted_at),
        kind=(
            "related"
            if row.kind == "related"
            else ("postcondition" if row.source_case_id == case_id else "precondition")
        ),
    )


def add_automation(db, user, project_id, case_id, body):
    case = find_case(db, user, project_id, case_id, "update", lock=True)
    if body.targetCaseId:
        target = find_case(db, user, project_id, body.targetCaseId)
        if not target.is_automated or target.id == case_id:
            raise HTTPException(422, "目标必须为其他自动化用例")
    if body.suiteId:
        from models.test_suite import TestSuite
        from models.test_plan import TestPlan

        if (
            not db.query(TestSuite)
            .join(TestPlan, TestPlan.id == TestSuite.plan_id)
            .filter(TestSuite.id == body.suiteId, TestPlan.project_id == project_id)
            .first()
        ):
            raise HTTPException(422, "执行套件不属于当前项目")
    row = CaseAutomationLink(
        case_id=case_id,
        category=body.category,
        target_case_id=body.targetCaseId,
        suite_id=body.suiteId,
        external_ref=body.externalRef,
        created_by=str(user.id),
    )
    db.add(row)
    db.flush()
    change(db, case, user.id, "关联自动化", body.model_dump())
    return row


def change(db, case, actor_id, action, detail=None):
    db.add(
        CaseChange(
            project_id=case.project_id,
            case_id=case.id,
            actor_id=str(actor_id),
            action=action,
            detail=detail or {},
        )
    )
    logger.info("用例变更已记录 case_id={} action={}", case.id, action)


def find_case(
    db, user, project_id, case_id, permission="read", deleted=False, lock=False
):
    require_project_access(db, user, project_id, f"test_case:{permission}")
    query = db.query(TestCase).filter_by(project_id=project_id, id=case_id)
    query = query.filter(
        TestCase.deleted_at.is_not(None) if deleted else TestCase.deleted_at.is_(None)
    )
    case = (query.with_for_update() if lock else query).first()
    if not case:
        raise HTTPException(
            404, "回收站中不存在该用例" if deleted else "项目中不存在该用例"
        )
    return case


def storage_root():
    return Path(
        os.environ.get(
            "CASE_ATTACHMENT_DIR",
            Path(__file__).resolve().parents[1] / "uploads" / "cases",
        )
    ).resolve()


def attachment_path(row):
    root = storage_root()
    path = (root / row.file_path).resolve()
    if not path.is_relative_to(root):
        raise HTTPException(409, "附件路径不合法")
    return path


def attachment_data(row):
    return dict(
        id=row.id,
        caseId=row.case_id,
        fileName=row.file_name,
        fileSize=row.file_size,
        fileType=row.file_type,
        uploadedBy=row.uploaded_by,
        uploadTime=row.upload_time.isoformat() if row.upload_time else None,
    )


def upload_attachment(db, user, project_id, case_id, file):
    case = find_case(db, user, project_id, case_id, "update", lock=True)
    validate_file_upload(file)
    name = secure_filename(file.filename or "附件")
    if not name or "\x00" in name:
        raise HTTPException(422, "附件文件名不合法")
    identifier = str(uuid.uuid4())
    relative = str(
        Path(project_id) / case.id / (identifier + Path(name).suffix.lower())
    )
    row = CaseAttachment(
        id=identifier,
        case_id=case.id,
        file_name=name,
        file_path=relative,
        file_type=file.content_type,
        uploaded_by=str(user.id),
    )
    path = attachment_path(row)
    try:
        save_upload_file(file, str(path))
        row.file_size = path.stat().st_size
        db.add(row)
        change(
            db,
            case,
            user.id,
            "上传附件",
            {"attachmentId": identifier, "fileName": name},
        )
        db.commit()
        db.refresh(row)
        return row
    except Exception:
        db.rollback()
        logger.exception("上传用例附件失败 case_id={}", case.id)
        if path.exists():
            path.unlink()
        raise


def find_attachment(db, user, project_id, attachment_id, permission="read"):
    row = db.query(CaseAttachment).filter_by(id=attachment_id).first()
    if not row:
        raise HTTPException(404, "附件不存在")
    case = find_case(
        db, user, project_id, row.case_id, permission, lock=permission != "read"
    )
    return row, case


def remove_files(paths):
    for path in paths:
        try:
            path.unlink(missing_ok=True)
        except Exception:
            logger.exception("清理用例附件文件失败 path={}", path)
            raise


def restore_case(db, user, project_id, case_id):
    case = find_case(db, user, project_id, case_id, "update", deleted=True, lock=True)
    from models.module import Module

    if (
        case.module_id
        and not db.query(Module)
        .filter_by(id=case.module_id, project_id=project_id)
        .first()
    ):
        case.module_id = None
        case.module_path = None
    case.deleted_at = None
    case.deleted_by = None
    case.updated_by = str(user.id)
    case.updated_at = beijing_now()
    change(db, case, user.id, "恢复用例")
    return case


def purge_case(db, user, project_id, case_id):
    case = find_case(db, user, project_id, case_id, "delete", deleted=True, lock=True)
    from models.test_execution import TestExecution
    from models.plan_workspace import PlanNode

    if db.query(PlanNode).filter_by(case_id=case_id).first():
        raise HTTPException(409,"用例仍被计划测试点引用，不能彻底删除")

    if db.query(TestExecution).filter_by(case_id=case_id).first():
        raise HTTPException(409, "用例存在执行历史，不能彻底删除；可保留在回收站")
    paths = [attachment_path(row) for row in case.attachments]
    for model in [CaseIssueLink, CaseAutomationLink, CaseFollow, CaseComment]:
        db.query(model).filter_by(case_id=case_id).delete(synchronize_session=False)
    from sqlalchemy import or_

    db.query(CaseRelation).filter(
        or_(
            CaseRelation.source_case_id == case_id,
            CaseRelation.target_case_id == case_id,
        )
    ).delete(synchronize_session=False)
    db.query(CaseAutomationLink).filter_by(target_case_id=case_id).delete(
        synchronize_session=False
    )
    change(
        db,
        case,
        user.id,
        "彻底删除用例",
        {"name": case.name, "caseCode": case.case_code},
    )
    db.delete(case)
    return paths
