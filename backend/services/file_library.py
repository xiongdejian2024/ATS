"""Shared files remain immutable: archive only hides them from new selections."""
import hashlib
import re
import warnings
from html.parser import HTMLParser
from io import BytesIO
from uuid import uuid4
from fastapi import HTTPException, UploadFile, Response
from fastapi.responses import FileResponse
from PIL import Image, ImageSequence, UnidentifiedImageError
from sqlalchemy import func
from models.file_library import LibraryFolder, LibraryFile, LibraryReference
from services import attachment_storage as storage
from services.review_workspace import lock_project
from core.project_access import require_project_access
from utils.file_handler import secure_filename, validate_file_upload
from config import settings

IMAGE_TYPES = {'PNG': 'image/png', 'JPEG': 'image/jpeg', 'GIF': 'image/gif', 'WEBP': 'image/webp'}
URL = re.compile(r'^/api/v1/projects/([^/]+)/file-library/files/([a-f0-9-]{36})/preview$')


def require_library_read(db,user,project_id):
    from models import Project
    from core.project_access import project_allows
    project=db.get(Project,project_id)
    if project and project_allows(db,user,project,'test_case:read'):
        return require_project_access(db,user,project_id,'test_case:read')
    # A defect-only grant can use the existing project-shared library. It does
    # not grant case CRUD or make published files private defect attachments.
    from services.defect_workspace import authority
    return authority(db,user,project_id,'read')[1]


def folder(db, project_id, identifier):
    if not identifier:
        return None
    row = db.query(LibraryFolder).filter_by(project_id=project_id, id=identifier).first()
    if not row:
        raise HTTPException(404, '此项目中不存在该文件目录')
    return row


def folders(db, project_id):
    # A bounded, explicit tree; do not silently hide overflowing folders.
    rows = db.query(LibraryFolder).filter_by(project_id=project_id).order_by(LibraryFolder.name, LibraryFolder.id).limit(1001).all()
    if len(rows) > 1000:
        raise HTTPException(409, '文件目录超过当前1000项展示限制')
    return [dict(id=r.id, name=r.name, parentId=r.parent_id) for r in rows]


def write_folder(db, user, project_id, name, parent_id, identifier=None):
    require_project_access(db, user, project_id, 'test_case:update')
    lock_project(db, project_id)
    name = name.strip()
    if not name or len(name) > 255 or any(c in name for c in '/\\\x00'):
        raise HTTPException(422, '文件目录名称不合法')
    # MySQL repeatable-read may already have a snapshot from authorization.
    # After the project lock, read current directory rows for every validation.
    current_rows=db.query(LibraryFolder).filter_by(project_id=project_id).order_by(LibraryFolder.id).populate_existing().with_for_update().limit(1001).all()
    by_id={item.id:item for item in current_rows}
    if parent_id and parent_id not in by_id or identifier and identifier not in by_id:
        raise HTTPException(404,'此项目中不存在该文件目录')
    row=by_id[identifier] if identifier else LibraryFolder(project_id=project_id)
    current,visited=by_id.get(parent_id),set()
    while current:
        if current.id==identifier or current.id in visited:
            raise HTTPException(409,'文件目录不能形成循环')
        visited.add(current.id);current=by_id.get(current.parent_id)
    if any(item.id!=identifier and item.parent_id==(parent_id or None) and item.name==name for item in current_rows):
        raise HTTPException(409,'同一目录中已有此名称')
    if not identifier and len(current_rows)>=1000:
        raise HTTPException(409,'文件目录已达到当前1000项限制')
    row.name, row.parent_id = name, parent_id or None
    db.add(row); db.flush(); return dict(id=row.id, name=row.name, parentId=row.parent_id)


def image_type(raw):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            with Image.open(BytesIO(raw)) as image:
                mime = IMAGE_TYPES.get(image.format)
                if not mime: raise HTTPException(422, '图片格式不支持')
                image.verify()
            with Image.open(BytesIO(raw)) as image:
                # Also limit animated files; bounded bytes alone do not bound decode work.
                if image.width * image.height > 16_000_000 or image.width * image.height * getattr(image, 'n_frames', 1) > 32_000_000:
                    raise HTTPException(422, '图片解码像素超过限制')
                if getattr(image, 'n_frames', 1) > 200:
                    raise HTTPException(422, '图片动画超过200帧限制')
                for frame in ImageSequence.Iterator(image): frame.load()
        return mime
    except (UnidentifiedImageError, OSError, SyntaxError, Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
        raise HTTPException(422, '文件不是完整有效的图片') from exc


def data(row):
    return dict(id=row.id, folderId=row.folder_id, fileName=row.file_name, fileSize=row.file_size,
                mimeType=row.mime_type, sha256=row.sha256, uploadedBy=row.uploaded_by,
                createdAt=row.created_at, archived=row.archived, published=row.published,
                src=f'/api/v1/projects/{row.project_id}/file-library/files/{row.id}/preview' if row.mime_type in IMAGE_TYPES.values() else None)


def find(db, project_id, identifier, lock=False):
    query = db.query(LibraryFile).filter_by(project_id=project_id, id=identifier)
    row = (query.populate_existing().with_for_update() if lock else query).first()
    if not row: raise HTTPException(404, '此项目中不存在该文件')
    return row


def upload(db, user, project_id, file, folder_id=None, image=False, published=False):
    require_library_read(db, user, project_id)
    folder(db, project_id, folder_id)
    name = secure_filename(file.filename or '')
    if not name.strip() or '\x00' in name or len(name) > 255: raise HTTPException(422, '文件名不合法')
    if not image: validate_file_upload(file)
    raw = file.file.read(settings.MAX_FILE_SIZE + 1)
    if not raw or len(raw) > settings.MAX_FILE_SIZE: raise HTTPException(413, '文件为空或超过大小限制')
    # A filename or client Content-Type cannot authorize an inline preview.
    mime = image_type(raw) if image or re.search(r'\.(png|jpe?g|gif|webp)$', name, re.I) else 'application/octet-stream'
    identifier = str(uuid4())
    wrapped = UploadFile(filename=name, file=BytesIO(raw))
    key, size = storage.write(db, f'library/{project_id}/{identifier}', wrapped)
    row = LibraryFile(id=identifier, project_id=project_id, folder_id=folder_id or None, uploaded_by=str(user.id), file_name=name, file_path=key, file_size=size, sha256=hashlib.sha256(raw).hexdigest(), mime_type=mime, published=published)
    commit_started = False
    try:
        db.add(row); db.flush(); commit_started = True; db.commit(); db.refresh(row)
    except BaseException:
        db.rollback()
        if not commit_started and not key.startswith('db:'): storage.remove_external(key)
        raise
    return data(row)


def reference(db, user, project_id, ids, kind, identifier):
    unique = sorted(set(ids))
    if len(unique) > 50: raise HTTPException(422, '一次最多关联50个文件')
    # Acquire in a stable order. Archive also locks these rows.
    for file_id in unique:
        row = find(db, project_id, file_id, lock=True)
        if not row.published and row.uploaded_by != str(user.id): raise HTTPException(403, '此文件尚未发布到项目库')
        if row.archived: raise HTTPException(409, '文件已归档，请重新选择')
        row.published = True
        previous=db.query(LibraryReference).filter_by(file_id=file_id, entity_kind=kind, entity_id=identifier).with_for_update().first()
        if previous:
            previous.active=True
        else:
            db.add(LibraryReference(file_id=file_id, entity_kind=kind, entity_id=identifier, created_by=str(user.id)))
    db.flush()


class SourceParser(HTMLParser):
    def __init__(self): super().__init__(); self.sources = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'img': self.sources.extend(v for k,v in attrs if k == 'src' and v)


def image_ids(db, project_id, content):
    parser = SourceParser(); parser.feed(content or '')
    ids = set()
    for source in parser.sources:
        if '/file-library/' not in source: continue
        match = URL.fullmatch(source)
        if not match or match[1] != project_id: raise HTTPException(422, '富文本含有其他项目或无效的文件库图片')
        row = find(db, project_id, match[2])
        if row.mime_type not in IMAGE_TYPES.values(): raise HTTPException(422, '此文件不是可预览图片')
        if row.archived: raise HTTPException(409, '图片已归档，请重新选择')
        ids.add(row.id)
    return sorted(ids)


def references(db, project_id, kind, identifier):
    rows = db.query(LibraryFile).join(LibraryReference, LibraryReference.file_id == LibraryFile.id).filter(LibraryFile.project_id == project_id, LibraryReference.entity_kind == kind, LibraryReference.entity_id == identifier, LibraryReference.active.is_(True)).order_by(LibraryFile.id).all()
    return [data(row) for row in rows]


def download(db, row, preview=False):
    response = storage.download(db, row)
    if isinstance(response, FileResponse):
        with open(response.path, 'rb') as source: raw = source.read(settings.MAX_FILE_SIZE + 1)
    else: raw = response.body
    if len(raw) != row.file_size or len(raw) > settings.MAX_FILE_SIZE or hashlib.sha256(raw).hexdigest() != row.sha256:
        raise HTTPException(409, '文件内容与保存摘要不符')
    response = Response(raw, media_type='application/octet-stream', headers=dict(response.headers))
    if preview:
        if row.mime_type not in IMAGE_TYPES.values(): raise HTTPException(422, '仅已验证图片支持预览')
        response.media_type = row.mime_type
        response.headers['content-type'] = row.mime_type
        response.headers['content-disposition'] = 'inline'
        response.headers['Content-Security-Policy'] = "default-src 'none'; sandbox"
    return response
