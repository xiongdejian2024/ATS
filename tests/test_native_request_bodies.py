"""正文实际字节、项目权限、冻结版本及真实回环Agent传输验收。"""

import asyncio
import base64
import hashlib
import importlib.util
from pathlib import Path
import httpx
import pytest
from pydantic import ValidationError
from framework.native_http.models import FrozenCase, FrozenRequest, RequestSpec
from framework.native_http.engine import execute
from test_native_http_agent_e2e import native_lab, dispatch, finished, scope
from test_http_agent_e2e import lab, until


def meta(identifier, content, name="原文件.bin"):
    return dict(
        fileId=identifier,
        fileName=name,
        contentType="application/octet-stream",
        byteLength=len(content),
        sha256=hashlib.sha256(content).hexdigest(),
    )


@pytest.mark.parametrize(
    "value",
    [
        {
            "bodyType": "multipart",
            "multipartParams": [{"key": "a", "paramType": "json", "value": "{"}],
        },
        {
            "bodyType": "multipart",
            "multipartParams": [{"key": "a", "files": [{"fileId": "file"}]}],
        },
        {
            "bodyType": "multipart",
            "multipartParams": [
                {
                    "key": "a",
                    "paramType": "file",
                    "files": [{"fileId": "f", "fileAlias": "../bad"}],
                }
            ],
        },
        {
            "bodyType": "multipart",
            "multipartParams": [
                {
                    "key": "a",
                    "paramType": "file",
                    "files": [{"fileId": "f"}, {"fileId": "f"}],
                }
            ],
        },
        {"bodyType": "xml", "body": {}},
        {"bodyType": "binary", "body": "非文件"},
        {"binaryBody": {"file": {"fileId": "f"}}},
        {"bodyDrafts": {"unknown": "非法模式"}},
    ],
)
def test_invalid_body_contract(value):
    with pytest.raises(ValidationError):
        RequestSpec.model_validate(value)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body_type,content,custom_type",
    [
        ("binary", b"\x00\xff\x01" * 100000, None),
        ("binary", b"", "custom/type"),
        ("xml", "<请求>中文</请求>".encode(), None),
        ("xml", b"<root/>", "custom/xml"),
    ],
)
async def test_actual_binary_xml_headers_and_capture(body_type, content, custom_type):
    seen = []
    req = dict(
        bodyType=body_type, method="POST", name="正文真实发送", url="http://owned.test/"
    )
    if body_type == "binary":
        req.update(binaryBody={"file": {"fileId": "f"}}, files=[meta("f", content)])
    else:
        req["body"] = content.decode()
    if custom_type:
        req["headers"] = {"content-type": custom_type}

    async def loader(_):
        return content

    def target(request):
        seen.append(request)
        return httpx.Response(200)

    result = await execute(
        FrozenCase(id="c", category="api", requests=[req]),
        transport=httpx.MockTransport(target),
        file_loader=loader,
    )
    assert result["status"] == "passed" and seen[0].content == content
    assert seen[0].headers["content-type"] == (
        custom_type
        or ("application/xml" if body_type == "xml" else "application/octet-stream")
    )
    captured = result["native_detail"]["steps"][0]["attempts"][0]["request"]["body"]
    assert captured["byteLength"] == len(content)
    assert base64.b64decode(captured["base64"]) == content[: 256 * 1024]
    assert captured["truncated"] == (len(content) > 256 * 1024)


@pytest.mark.asyncio
async def test_multipart_real_order_multiple_files_alias_disabled_and_timing():
    contents = {"one": b"\x00\xff", "two": b"second"}
    loaded = []
    seen = []
    rows = [
        {"key": "text", "value": "中文"},
        {"key": "json", "paramType": "json", "value": '{"v":1}'},
        {
            "key": "files",
            "paramType": "file",
            "files": [{"fileId": "one", "fileAlias": "改名.bin"}, {"fileId": "two"}],
        },
        {
            "key": "skip",
            "enable": False,
            "paramType": "file",
            "files": [{"fileId": "missing"}],
        },
    ]

    async def loader(value):
        loaded.append(value.fileId)
        await asyncio.sleep(0.04)
        return contents[value.fileId]

    def target(request):
        seen.append(request)
        return httpx.Response(200)

    result = await execute(
        FrozenCase(
            id="c",
            category="api",
            requests=[
                FrozenRequest(
                    name="多文件",
                    url="http://owned.test/",
                    method="POST",
                    bodyType="multipart",
                    multipartParams=rows,
                    files=[meta(k, v) for k, v in contents.items()],
                )
            ],
        ),
        transport=httpx.MockTransport(target),
        file_loader=loader,
    )
    assert result["status"] == "passed" and loaded == ["one", "two"]
    raw = seen[0].content
    assert (
        raw.index(b'name="text"')
        < raw.index(b'name="json"')
        < raw.index("改名.bin".encode())
        < raw.index("原文件.bin".encode())
    )
    assert (
        raw.count(b'name="files"') == 2
        and b"application/json" in raw
        and b"\x00\xff" in raw
    )
    assert b"missing" not in raw and b'name="skip"' not in raw
    actual = result["native_detail"]["steps"][0]["attempts"][0]
    assert (
        actual["response"]["responseTimeMs"]
        < result["steps"][0]["duration"] * 1000 - 60
    )


@pytest.mark.asyncio
async def test_changed_file_digest_never_sends_request():
    seen = []

    async def loader(_):
        return b"wrong"

    req = FrozenRequest(
        name="冻结校验",
        url="http://owned.test/",
        bodyType="binary",
        binaryBody={"file": {"fileId": "f"}},
        files=[meta("f", b"right")],
    )
    result = await execute(
        FrozenCase(id="c", category="api", requests=[req]),
        transport=httpx.MockTransport(lambda r: seen.append(r)),
        file_loader=loader,
    )
    assert result["status"] == "error" and seen == []


@pytest.mark.asyncio
@pytest.mark.parametrize("body_type", ["binary", "multipart"])
async def test_real_agent_file_permissions_hidden_freeze_and_exact_bytes(
    native_lab, body_type, monkeypatch
):
    from database import SessionLocal
    from config import settings
    from models.native_case import ApiDefinition
    from models.plan_orchestration import PlanRunItem, PlanRun
    from models.task_queue import TaskQueue
    from models import User, ProjectMember
    from core.security import create_access_token

    v = native_lab
    client = v["client"]
    project = v["api"]["projectId"]
    base = f"/api/v1/projects/{project}/native-cases/request-files"
    content = b"\x00\xff" + "真实文件字节".encode() * 6000
    first = await client.post(
        base, files={"file": ("binary.bin", content, "application/octet-stream")}
    )
    assert first.status_code == 200, first.text
    file = first.json()["data"]
    second = (
        await client.post(
            base, files={"file": ("empty.bin", b"", "application/octet-stream")}
        )
    ).json()["data"]
    assert file["sha256"] == hashlib.sha256(content).hexdigest() and file[
        "byteLength"
    ] == len(content)
    assert (
        await client.get(base + "/" + file["fileId"] + "/download")
    ).content == content
    assert (await client.get(base, params={"search": "binary"})).json()["data"][
        "total"
    ] == 1
    original_limit = settings.MAX_FILE_SIZE
    assert (
        await client.post(base, files={"file": ("file." + "x" * 300, b"x")})
    ).status_code == 422
    monkeypatch.setattr(settings, "MAX_FILE_SIZE", 2)
    assert (
        await client.post(base, files={"file": ("too.bin", b"123")})
    ).status_code == 413
    monkeypatch.setattr(settings, "MAX_FILE_SIZE", original_limit)
    with SessionLocal() as db:
        reader = User(
            id="file-reader",
            username="文件只读",
            email="file-reader@example.test",
            password_hash="隔离",
        )
        db.add(reader)
        db.flush()
        db.add(ProjectMember(project_id=project, user_id=reader.id, role="viewer"))
        definition = db.query(ApiDefinition).filter_by(project_id=project).one()
        definition.path = "/upload"
        db.commit()
        definition_id, definition_revision = definition.id, definition.revision
    reader_headers = {
        "Authorization": "Bearer " + create_access_token({"sub": "file-reader"})
    }
    assert (await client.get(base, headers=reader_headers)).status_code == 200
    assert (
        await client.post(
            base, headers=reader_headers, files={"file": ("bad.bin", b"x")}
        )
    ).status_code == 403
    assert (
        await client.delete(base + "/" + file["fileId"], headers=reader_headers)
    ).status_code == 403
    request = dict(
        method="POST",
        bodyType=body_type,
        assertions=[{"expected": 201}],
        bodyDrafts={"text": "仅编辑器缓存"},
    )
    if body_type == "binary":
        request["binaryBody"] = {
            "file": {"fileId": file["fileId"]},
            "description": "原描述",
        }
    else:
        request["multipartParams"] = [
            {"key": "text", "value": "中文"},
            {
                "key": "files",
                "paramType": "file",
                "files": [
                    {"fileId": file["fileId"], "fileAlias": "别名.bin"},
                    {"fileId": second["fileId"]},
                ],
            },
        ]
    await v["config"](v["api"], {"request": request}, revision=1)
    run_id = await scope(v, "api")
    with SessionLocal() as db:
        item = db.query(PlanRunItem).filter_by(run_id=run_id).one()
        execution = item.execution_id
        frozen = item.suite_snapshot["nativeCases"][0]["requests"][0]
        assert "bodyDrafts" not in frozen or frozen["bodyDrafts"] == {}
        assert frozen["files"][0]["sha256"] == file[
            "sha256"
        ] and '"content":' not in json_dump(frozen)
    endpoint = f"/api/v1/native-http/executions/{execution}/files/{file['fileId']}"
    token_headers = {"X-Agent-Token": v["environment"]["token"]}
    assert (await client.get(endpoint)).status_code == 401
    assert (
        await client.get(endpoint, headers={"X-Agent-Token": "wrong"})
    ).status_code == 401
    assert (
        await client.get(endpoint.replace(execution, "wrong"), headers=token_headers)
    ).status_code == 404
    assert (
        await client.get(
            endpoint.replace(file["fileId"], "missing"), headers=token_headers
        )
    ).status_code == 404
    assert (await client.delete(base + "/" + file["fileId"])).status_code == 200
    assert (
        await client.get(base + "/" + file["fileId"] + "/download")
    ).status_code == 404
    assert (await client.get(endpoint, headers=token_headers)).content == content
    invalid = await client.put(
        f"/api/v1/projects/{project}/native-cases/cases/{v['api']['id']}",
        json={
            "state": "DONE",
            "apiDefinitionId": definition_id,
            "environmentId": v["request_environment"]["id"],
            "parameters": {"request": request},
            "expectedRevision": 2,
            "expectedDefinitionRevision": definition_revision,
        },
    )
    assert invalid.status_code == 422
    await dispatch(run_id)
    await finished(run_id)
    assert len(v["upload_hits"]) == 1
    hit = v["upload_hits"][0]
    if body_type == "binary":
        assert (
            hit["content"] == content
            and hit["content_type"] == "application/octet-stream"
        )
    else:
        assert hit["parts"] == [
            ("text", None, "中文", None),
            ("files", "别名.bin", content, "application/octet-stream"),
            ("files", "empty.bin", b"", "application/octet-stream"),
        ]
    assert (await client.get(endpoint, headers=token_headers)).status_code == 404
    with SessionLocal() as db:
        report = db.get(PlanRun, run_id).report
        assert report["total"] == report["counts"]["passed"] == 1
    await until(lambda: not list(v["agent"].sat_runner.outbox.glob("*.json")))
    print(
        "请求文件真实验收通过：权限、冻结后移除、精确字节、Agent下载及中心报告",
        body_type,
    )


def json_dump(value):
    import json

    return json.dumps(value)


def test_file_table_incremental_upgrade_preserves_legacy_and_is_idempotent():
    from sqlalchemy import create_engine, inspect, text

    target = create_engine("sqlite:///:memory:")
    with target.begin() as connection:
        connection.execute(
            text("CREATE TABLE legacy_business (id INTEGER PRIMARY KEY, value TEXT)")
        )
        connection.execute(text("INSERT INTO legacy_business VALUES (1, '历史原值')"))
    path = (
        Path(__file__).resolve().parents[1] / "scripts/upgrade_native_request_files.py"
    )
    spec = importlib.util.spec_from_file_location("file_upgrade_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.upgrade(False, target) == ["native_request_files"]
    assert inspect(target).get_table_names() == ["legacy_business"]
    assert module.upgrade(True, target) == ["native_request_files"]
    assert module.upgrade(True, target) == []
    with target.connect() as connection:
        assert (
            connection.execute(
                text("SELECT value FROM legacy_business WHERE id=1")
            ).scalar()
            == "历史原值"
        )
    from sqlalchemy.schema import CreateTable
    from models.native_request_file import NativeRequestFile

    table = NativeRequestFile.__table__
    table.drop(target)
    ddl = str(CreateTable(table).compile(dialect=target.dialect)).replace(
        "file_name VARCHAR(255)", "file_name VARCHAR(1)"
    )
    with target.begin() as connection:
        connection.execute(text(ddl))
    with pytest.raises(RuntimeError, match="结构不兼容"):
        module.upgrade(True, target)
    target.dispose()


def test_mysql_inherited_collation_is_compatible_but_length_and_blob_stay_strict():
    from sqlalchemy import String, LargeBinary
    from sqlalchemy.dialects.mysql import VARCHAR, BLOB, LONGBLOB, dialect

    path = (
        Path(__file__).resolve().parents[1] / "scripts/upgrade_native_request_files.py"
    )
    spec = importlib.util.spec_from_file_location("file_type_upgrade_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    mysql = dialect()
    assert module.same_column_type(
        VARCHAR(255, collation="utf8mb4_unicode_ci"), String(255), mysql
    )
    assert not module.same_column_type(
        VARCHAR(1, collation="utf8mb4_unicode_ci"), String(255), mysql
    )
    expected = LargeBinary().with_variant(LONGBLOB(), "mysql")
    assert module.same_column_type(LONGBLOB(), expected, mysql)
    assert not module.same_column_type(BLOB(), expected, mysql)
