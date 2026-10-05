"""执行描述图片的上传、鉴权、历史引用和草稿清理。"""

import re
import warnings
from html.parser import HTMLParser
from io import BytesIO
from PIL import Image, ImageSequence, UnidentifiedImageError
from fastapi import HTTPException
from models.plan_case_media import PlanCaseMedia, PlanCaseMediaLink
from services.plan_case_execution import can_execute
from config import settings
from core.logger import logger
from utils.file_handler import secure_filename

URL = re.compile(
    r"^/api/v1/plan-orchestration/plans/([^/]+)/execution-media/([a-f0-9-]{36})/preview$"
)
FORMATS = {
    "PNG": "image/png",
    "JPEG": "image/jpeg",
    "GIF": "image/gif",
    "WEBP": "image/webp",
}


def linked(db, identifier):
    return (
        db.query(PlanCaseMediaLink).filter_by(media_id=identifier).first() is not None
    )


def media_data(row):
    return dict(
        id=row.id,
        fileName=row.file_name,
        fileSize=row.file_size,
        mimeType=row.mime_type,
        src=f"/api/v1/plan-orchestration/plans/{row.plan_id}/execution-media/{row.id}/preview",
    )


def upload(db, user, plan, file):
    if not can_execute(db, user, plan):
        raise HTTPException(409, "归档计划不能上传执行描述图片")
    name = secure_filename(file.filename or "图片")
    if not name or "\x00" in name or len(name) > 255:
        raise HTTPException(422, "图片文件名不合法")
    raw = file.file.read(settings.MAX_FILE_SIZE + 1)
    if not raw or len(raw) > settings.MAX_FILE_SIZE:
        raise HTTPException(422, "图片内容为空或超过当前文件大小限制")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(BytesIO(raw)) as image:
                mime = FORMATS.get(image.format)
                if not mime:
                    raise HTTPException(422, "支持PNG、JPEG、GIF和WebP图片")
                image.verify()
            # JPEG 的 verify 不会解码像素，动画也需逐帧验证，避免保存无法显示的截图。
            with Image.open(BytesIO(raw)) as decoded:
                for frame in ImageSequence.Iterator(decoded):
                    frame.load()
    except (
        UnidentifiedImageError,
        OSError,
        SyntaxError,
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
    ) as exc:
        logger.exception("执行描述图片解码失败：计划={}", plan.id)
        raise HTTPException(422, "文件不是完整的有效图片") from exc
    row = PlanCaseMedia(
        plan_id=plan.id,
        uploaded_by=str(user.id),
        file_name=name,
        file_size=len(raw),
        mime_type=mime,
        content=raw,
    )
    db.add(row)
    db.flush()
    logger.info(
        "执行描述图片已上传：计划={}，图片={}，字节={}", plan.id, row.id, len(raw)
    )
    return media_data(row)


def find(db, user, plan, identifier, lock=False):
    query = db.query(PlanCaseMedia).filter_by(id=identifier, plan_id=plan.id)
    row = (query.with_for_update() if lock else query).first()
    if not row:
        raise HTTPException(404, "此计划中不存在该图片")
    if str(row.uploaded_by) != str(user.id) and not linked(db, row.id):
        raise HTTPException(403, "未提交图片仅上传人可访问")
    return row


def remove(db, user, plan, identifier):
    row = find(db, user, plan, identifier, lock=True)
    if not can_execute(db, user, plan):
        raise HTTPException(409, "归档计划不能删除未提交图片")
    if str(row.uploaded_by) != str(user.id):
        raise HTTPException(403, "只能删除本人未提交的图片")
    if linked(db, row.id):
        raise HTTPException(409, "图片已被执行历史引用，不能删除")
    db.delete(row)
    logger.info("未提交执行描述图片已删除：计划={}，图片={}", plan.id, identifier)


class MediaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            self.sources.extend(value for key, value in attrs if key == "src" and value)


def description_media(db, user, plan, description):
    parser = MediaParser()
    parser.feed(description)
    ids = set()
    for source in parser.sources:
        if not source.startswith("/api/v1/plan-orchestration/"):
            continue
        match = URL.fullmatch(source)
        if not match or match[1] != plan.id:
            raise HTTPException(422, "执行描述含有其他计划或无效的图片引用")
        row = find(db, user, plan, match[2], lock=True)
        ids.add(row.id)
    return sorted(ids)
