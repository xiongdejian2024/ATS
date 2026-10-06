"""文件权限、不可变字节及冻结身份读取；没有任意路径或外部URL。"""

import hashlib
from fastapi import HTTPException
from sqlalchemy.orm import defer
from models.native_request_file import NativeRequestFile
from models.plan_orchestration import PlanRunItem
from models.task_queue import TaskQueue
from models.environment import Environment
from core.project_access import require_project_access, project_allows
from core.logger import logger
from config import settings
from utils.file_handler import secure_filename
from utils.datetime_utils import beijing_now


def metadata(row):
    return dict(
        fileId=row.id,
        fileName=row.file_name,
        contentType=row.content_type,
        byteLength=row.byte_length,
        sha256=row.sha256,
    )


def references(request):
    if request.bodyType == "binary":
        return [request.binaryBody.file] if request.binaryBody.file else []
    return (
        [
            f
            for p in request.multipartParams
            if p.enable and p.paramType == "file"
            for f in p.files
        ]
        if request.bodyType == "multipart"
        else []
    )


def rows_for_request(db, project_id, request):
    rows = []
    for identifier in dict.fromkeys(f.fileId for f in references(request)):
        row = (
            db.query(NativeRequestFile)
            .options(defer(NativeRequestFile.content))
            .filter_by(id=identifier, project_id=project_id)
            .populate_existing()
            .with_for_update()
            .one_or_none()
        )
        if not row or row.deleted_at:
            raise ValueError("请求文件不属于来源项目、已移除或不存在")
        rows.append(row)
    return rows


def frozen_files(db, project_id, request):
    if request.bodyType == "binary" and request.binaryBody.file is None:
        raise ValueError("二进制请求必须选择一个实际文件")
    return [metadata(row) for row in rows_for_request(db, project_id, request)]


def upload(db, user, project_id, file):
    project = require_project_access(db, user, project_id, "test_case:read")
    if not any(
        project_allows(db, user, project, "test_case:" + action)
        for action in ("create", "update")
    ):
        raise HTTPException(403, "没有此项目的文件上传权限")
    name = secure_filename(file.filename or "请求文件").strip()
    content_type = file.content_type or "application/octet-stream"
    if (
        not name
        or len(name) > 255
        or any(c in name + content_type for c in "\x00\r\n")
        or len(content_type) > 255
    ):
        raise HTTPException(422, "文件名称或类型无效")
    content = file.file.read(settings.MAX_FILE_SIZE + 1)
    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(413, "文件超过上传大小限制")
    row = NativeRequestFile(
        project_id=project_id,
        file_name=name,
        content_type=content_type,
        byte_length=len(content),
        sha256=hashlib.sha256(content).hexdigest(),
        content=content,
        created_by=user.id,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    logger.info(
        "请求文件已保存：项目={}，文件={}，字节={}", project_id, row.id, len(content)
    )
    return metadata(row)


def get_user_file(db, user, project_id, identifier, action="read"):
    require_project_access(db, user, project_id, "test_case:" + action)
    row = (
        db.query(NativeRequestFile)
        .options(defer(NativeRequestFile.content))
        .filter_by(id=identifier, project_id=project_id)
        .first()
    )
    if not row or row.deleted_at:
        raise HTTPException(404, "请求文件不存在或已移除")
    return row


def remove(db, user, project_id, identifier):
    row = get_user_file(db, user, project_id, identifier, "update")
    row.deleted_at = beijing_now()
    db.commit()
    logger.info(
        "请求文件已移除：项目={}，文件={}；冻结执行字节保留", project_id, identifier
    )


def get_agent_file(db, execution_id, identifier, token):
    env = db.query(Environment).filter_by(token=token).first() if token else None
    if not env or not env.status:
        raise HTTPException(401, "执行节点认证无效")
    task = (
        db.query(TaskQueue)
        .filter_by(execution_id=execution_id, environment_id=env.id)
        .first()
    )
    item = db.query(PlanRunItem).filter_by(execution_id=execution_id).first()
    if not task or not item or task.status not in {"pending", "running"}:
        raise HTTPException(404, "执行身份无效或已结束")
    expected = next(
        (
            f
            for c in item.suite_snapshot.get("nativeCases") or []
            for req in c["requests"]
            for f in req.get("files", [])
            if f["fileId"] == identifier
        ),
        None,
    )
    if expected is None:
        raise HTTPException(404, "文件不属于本次冻结执行")
    row = db.get(NativeRequestFile, identifier) if expected else None
    if (
        not row
        or row.byte_length != expected["byteLength"]
        or row.sha256 != expected["sha256"]
    ):
        raise HTTPException(409, "冻结文件内容不可用或校验值不一致")
    # 已移除的编辑文件只允许有冻结引用的本执行读取，普通用户下载不可见。
    return row
