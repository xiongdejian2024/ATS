"""Explicit persistent attachment backends with legacy local-path compatibility.

Database blobs need no external service. S3 is optional and never falls back to
sample MinIO credentials. Existing local files are not migrated or removed.
"""
import os
import tempfile
from pathlib import Path
from urllib.parse import quote

from fastapi import HTTPException, Response
from fastapi.responses import FileResponse
from models.attachment_blob import AttachmentBlob
from sqlalchemy import func
from config import settings


def local_root():
    return Path(os.environ.get("CASE_ATTACHMENT_DIR", Path(__file__).resolve().parents[1] / "uploads" / "cases")).resolve()


def local_path(key):
    root = local_root()
    path = (root / key).resolve()
    if not key or Path(key).is_absolute() or not path.is_relative_to(root):
        raise HTTPException(409, "附件路径不合法")
    return path


def backend_name():
    value = os.environ.get("ATS_ATTACHMENT_BACKEND", "local")
    if value not in {"local", "database", "s3"}:
        raise ValueError("ATS_ATTACHMENT_BACKEND must be local, database or s3")
    return value


def s3_client():
    # Credentials must be deliberately supplied; do not create services/buckets.
    import boto3
    from botocore.config import Config
    bucket = os.environ.get("ATS_ATTACHMENT_S3_BUCKET")
    access = os.environ.get("ATS_ATTACHMENT_S3_ACCESS_KEY")
    secret = os.environ.get("ATS_ATTACHMENT_S3_SECRET_KEY")
    endpoint = os.environ.get("ATS_ATTACHMENT_S3_ENDPOINT")
    if not bucket or not access or not secret:
        raise ValueError("S3 attachment configuration is incomplete")
    if endpoint and not endpoint.startswith("https://"):
        raise ValueError("S3 attachment endpoint must use HTTPS")
    return boto3.client("s3", endpoint_url=endpoint, aws_access_key_id=access,
                        aws_secret_access_key=secret,
                        region_name=os.environ.get("ATS_ATTACHMENT_S3_REGION", "us-east-1"),
                        config=Config(connect_timeout=5, read_timeout=15, retries={"max_attempts": 2})), bucket


def write(db, relative, file):
    # Uploads are already limited by validate_file_upload; enforce again here.
    raw = file.file.read(settings.MAX_FILE_SIZE + 1)
    if len(raw) > settings.MAX_FILE_SIZE:
        raise HTTPException(413, "附件超过文件大小限制")
    backend = backend_name()
    if backend == "database":
        key = "db:" + relative
        db.add(AttachmentBlob(key=key, content=raw))
        return key, len(raw)
    if backend == "s3":
        client, bucket = s3_client()
        key = "cases/" + relative.replace("\\", "/")
        client.put_object(Bucket=bucket, Key=key, Body=raw, ContentType="application/octet-stream")
        return "s3:" + key, len(raw)
    path = local_path(relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=".upload-")
    try:
        with os.fdopen(descriptor, "wb") as output:
            output.write(raw); output.flush(); os.fsync(output.fileno())
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise
    return relative, len(raw)


def download(db, row):
    headers = {"X-Content-Type-Options": "nosniff", "Cache-Control": "private, no-store",
               "Content-Disposition": "attachment; filename*=UTF-8''" + quote(row.file_name, safe="")}
    if row.file_path.startswith("db:"):
        # Limit bytes in SQL, before the driver materializes historical blobs.
        found = db.query(func.substr(AttachmentBlob.content, 1, settings.MAX_FILE_SIZE + 1)).filter(AttachmentBlob.key == row.file_path).first()
        if found is None:
            raise HTTPException(404, "附件文件不存在")
        raw = bytes(found[0])
        if len(raw) > settings.MAX_FILE_SIZE:
            raise HTTPException(413, "附件超过当前下载限制")
        return Response(raw, media_type="application/octet-stream", headers=headers)
    if row.file_path.startswith("s3:"):
        client, bucket = s3_client()
        try:
            obj = client.get_object(Bucket=bucket, Key=row.file_path[3:])
        except client.exceptions.NoSuchKey as exc:
            raise HTTPException(404, "附件文件不存在") from exc
        source = obj["Body"]
        try:
            if obj["ContentLength"] > settings.MAX_FILE_SIZE:
                raise HTTPException(413, "附件超过当前下载限制")
            raw = source.read(settings.MAX_FILE_SIZE + 1)
            if len(raw) > settings.MAX_FILE_SIZE or len(raw) != obj["ContentLength"]:
                raise HTTPException(409, "附件内容不完整或超过下载限制")
        finally:
            source.close()
        return Response(raw, media_type="application/octet-stream", headers=headers)
    path = local_path(row.file_path)
    if not path.is_file():
        raise HTTPException(404, "附件文件不存在")
    return FileResponse(path, filename=row.file_name, media_type="application/octet-stream", headers=headers)


def delete_blob(db, key):
    if key.startswith("db:"):
        db.query(AttachmentBlob).filter_by(key=key).delete(synchronize_session=False)


def remove_external(key):
    if isinstance(key, Path):
        key.unlink(missing_ok=True)
    elif key.startswith("s3:"):
        client, bucket = s3_client()
        client.delete_object(Bucket=bucket, Key=key[3:])
    elif not key.startswith("db:"):
        local_path(key).unlink(missing_ok=True)
