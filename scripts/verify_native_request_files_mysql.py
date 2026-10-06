"""独立MySQL迁移、LONGBLOB字节回读与冻结校验，复用项目已有隔离基座。"""

import asyncio
import hashlib
import importlib.util
import logging
from pathlib import Path
import sys
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "xat"))
logging.basicConfig(
    filename=ROOT / "logs/第68部分MySQL验收.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("请求文件数据库验收")


def verify(db):
    from sqlalchemy import inspect, text
    from models.native_request_file import NativeRequestFile
    from framework.native_http.models import RequestSpec, FrozenRequest, FrozenCase
    from framework.native_http.engine import execute
    from services.native_request_files import frozen_files
    import httpx

    db.commit()
    table = NativeRequestFile.__table__
    table.drop(db.bind)
    spec = importlib.util.spec_from_file_location(
        "files_upgrade", ROOT / "scripts/upgrade_native_request_files.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.upgrade(False, db.bind) == ["native_request_files"]
    assert module.upgrade(True, db.bind) == ["native_request_files"]
    assert module.upgrade(True, db.bind) == []
    assert (
        str(
            next(
                c["type"]
                for c in inspect(db.bind).get_columns(table.name)
                if c["name"] == "content"
            )
        ).lower()
        == "longblob"
    )
    content = b"\x00\xff" + "超过普通BLOB的真实内容".encode() * 8000
    identifier = str(uuid4())
    try:
        row = NativeRequestFile(
            id=identifier,
            project_id="project",
            file_name="原文件.bin",
            content_type="application/octet-stream",
            byte_length=len(content),
            sha256=hashlib.sha256(content).hexdigest(),
            content=content,
            created_by="owner",
        )
        db.add(row)
        db.commit()
        db.expire_all()
        row = db.get(NativeRequestFile, identifier)
        assert len(content) > 65535 and row.content == content
        request = RequestSpec(
            method="POST",
            bodyType="binary",
            binaryBody={"file": {"fileId": identifier}},
        )
        frozen = frozen_files(db, "project", request)
        req = FrozenRequest(
            **request.model_dump(exclude={"bodyDrafts"}),
            files=frozen,
            name="数据库文件",
            url="http://owned.test/"
        )

        async def loader(_):
            return row.content

        hits = []

        def target(value):
            hits.append(value.content)
            return httpx.Response(200)

        result = asyncio.run(
            execute(
                FrozenCase(id="case-0", category="api", requests=[req]),
                file_loader=loader,
                transport=httpx.MockTransport(target),
            )
        )
        assert result["status"] == "passed" and hits == [content]
        log.info(
            "新表迁移幂等，LONGBLOB超过64KiB字节及SHA256回读一致，冻结文件实际发送保持；仅MockTransport"
        )
    finally:
        db.rollback()
        db.query(NativeRequestFile).filter_by(id=identifier).delete()
        db.commit()
        log.info("独立请求文件样本按唯一ID回收")


if __name__ == "__main__":
    try:
        spec = importlib.util.spec_from_file_location(
            "native_mysql_base", ROOT / "scripts/verify_plan_native_http_mysql.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.main(verify_request=verify)
    except Exception:
        log.exception("请求文件MySQL验收失败")
        raise
