from io import BytesIO
from types import SimpleNamespace

import pytest
from fastapi import UploadFile, HTTPException
from database import SessionLocal
from models.attachment_blob import AttachmentBlob
from services import attachment_storage as store
from test_case_features import features
from test_case_governance import governance


def upload(raw=b"persisted\x00binary"):
    return UploadFile(filename="证据.txt", file=BytesIO(raw))


def row(key): return SimpleNamespace(file_path=key, file_name="证据.txt")


def test_database_attachment_survives_session_restart_and_backend_switch(monkeypatch):
    monkeypatch.setenv("ATS_ATTACHMENT_BACKEND", "database")
    with SessionLocal() as db:
        key, size = store.write(db, "project/case/evidence.txt", upload())
        db.commit()
    monkeypatch.setenv("ATS_ATTACHMENT_BACKEND", "local")
    with SessionLocal() as db:
        response = store.download(db, row(key))
        assert response.body == b"persisted\x00binary" and size == len(response.body)
        assert response.headers["x-content-type-options"] == "nosniff"
        assert "private" in response.headers["cache-control"]
        store.delete_blob(db, key); db.rollback()
        assert db.get(AttachmentBlob, key) is not None
        store.delete_blob(db, key); db.commit()
        with pytest.raises(HTTPException): store.download(db, row(key))


def test_local_atomic_upload_legacy_read_and_path_escape(monkeypatch, tmp_path):
    monkeypatch.setenv("CASE_ATTACHMENT_DIR", str(tmp_path))
    monkeypatch.setenv("ATS_ATTACHMENT_BACKEND", "local")
    with SessionLocal() as db:
        key, size = store.write(db, "p/c/e.txt", upload())
        assert store.local_path(key).read_bytes() == b"persisted\x00binary"
        assert store.download(db, row(key)).path == store.local_path(key)
    with pytest.raises(HTTPException): store.local_path("../escape")
    with pytest.raises(HTTPException): store.local_path(str(tmp_path / "p"))
    assert not list(tmp_path.rglob(".upload-*"))


def test_s3_adapter_explicit_configuration_and_bounded_read(monkeypatch):
    monkeypatch.setenv("ATS_ATTACHMENT_BACKEND", "s3")
    for name in ("ATS_ATTACHMENT_S3_BUCKET", "ATS_ATTACHMENT_S3_ACCESS_KEY", "ATS_ATTACHMENT_S3_SECRET_KEY"):
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(ValueError, match="incomplete"): store.s3_client()
    objects = {}
    class FakeClient:
        def put_object(self, **kwargs): objects[kwargs["Key"]] = kwargs["Body"]
        def get_object(self, **kwargs):
            data = objects[kwargs["Key"]]
            return dict(Body=BytesIO(data), ContentLength=len(data))
        def delete_object(self, **kwargs): objects.pop(kwargs["Key"])
    monkeypatch.setattr(store, "s3_client", lambda: (FakeClient(), "synthetic-bucket"))
    with SessionLocal() as db:
        key, _ = store.write(db, "project/case/e.txt", upload())
        assert store.download(db, row(key)).body == b"persisted\x00binary"
    store.remove_external(key)
    assert objects == {}


def test_database_upload_rollback_and_size_limit(monkeypatch):
    monkeypatch.setenv("ATS_ATTACHMENT_BACKEND", "database")
    with SessionLocal() as db:
        key, _ = store.write(db, "temporary", upload())
        db.rollback()
        assert db.get(AttachmentBlob, key) is None
        monkeypatch.setattr(store.settings, "MAX_FILE_SIZE", 1)
        with pytest.raises(HTTPException) as error: store.write(db, "large", upload())
        assert error.value.status_code == 413


def test_service_refresh_failure_preserves_committed_metadata_and_local_file(features, monkeypatch):
    from models import CaseAttachment
    from services import case_features
    context = features
    db = context["db"]
    monkeypatch.setenv("ATS_ATTACHMENT_BACKEND", "local")
    monkeypatch.setattr(db, "refresh", lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("temporary read failure")))
    with pytest.raises(OSError):
        case_features.upload_attachment(db, context["state"]["user"], context["project"].id, context["cases"][0].id, upload())
    with SessionLocal() as check:
        attachment = check.query(CaseAttachment).one()
        assert store.local_path(attachment.file_path).read_bytes() == b"persisted\x00binary"
