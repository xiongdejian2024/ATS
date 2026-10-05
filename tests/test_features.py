"""Actual single-case dispatch, local upload, private HTML snapshots and inbox."""

from datetime import datetime
import uuid
import httpx
import pytest
from test_http_agent_e2e import lab, until, queue_states


async def other_user(client):
    from database import SessionLocal
    from models import User
    from core.security import get_password_hash

    with SessionLocal() as db:
        db.add(
            User(
                id=str(uuid.uuid4()),
                username="other",
                email="other@example.com",
                password_hash=get_password_hash("own-test"),
            )
        )
        db.commit()
    other = httpx.AsyncClient(base_url=client.base_url)
    response = await other.post(
        "/api/v1/auth/login", json={"username": "other", "password": "own-test"}
    )
    data = response.json()["data"]
    other.headers["Authorization"] = "Bearer " + (
        data.get("accessToken") or data["access_token"]
    )
    return other


@pytest.mark.asyncio
async def test_single_case_real_history_report_and_private_inbox(lab):
    from database import SessionLocal
    from models import TestExecution, TestSuite, Notification

    client = lab["client"]
    case = lab["cases"][1]
    original = lab["suite"]
    response = await client.post(
        f"/api/v1/test-cases/{case['id']}/execute", json={"suiteId": original["id"]}
    )
    assert response.status_code == 200, response.text
    with SessionLocal() as db:
        single = db.query(TestSuite).filter(TestSuite.id != original["id"]).one()
        identifier = single.id
        assert single.case_ids == [case["id"]]
        assert len(db.get(TestSuite, original["id"]).case_ids) == 4
    await until(
        lambda: bool(queue_states(identifier))
        and set(queue_states(identifier).values()) == {"completed"}
    )
    with SessionLocal() as db:
        rows = db.query(TestExecution).all()
        assert (
            len(rows) == 1
            and rows[0].case_id == case["id"]
            and rows[0].result == "passed"
        )
        assert "call: passed" in rows[0].execution_log
        execution_id = rows[0].id
        rows[0].execution_log = '<script>alert("log")</script>'
        db.commit()
    history = await client.get(
        "/api/v1/executions", params={"project_id": case["projectId"]}
    )
    assert history.status_code == 200, history.text
    assert history.json()["data"]["total"] == 1
    log = await client.get("/api/v1/executions/" + execution_id + "/logs")
    assert "<script>" in str(log.json())
    assert (await client.get("/api/v1/executions/missing")).status_code == 404
    # 报告按执行记录的业务日期筛选。UTC runner 的“今天”在北京时间
    # 00:00—07:59 期间仍是前一天；不能用宿主日期代替执行日期。
    execution_day = datetime.fromisoformat(
        history.json()["data"]["items"][0]["executedAt"]
    ).date().isoformat()
    request = dict(
        name="<script>Report</script>",
        projectId=case["projectId"],
        type="detailed",
        format="html",
        startDate=execution_day,
        endDate=execution_day,
    )
    response = await client.post("/api/v1/dashboard/reports", json=request)
    assert response.status_code == 200, response.text
    report = response.json()["data"]
    rid = report["id"]
    assert (
        report["passedCases"] == 1
        and report["executedCases"] == 1
        and report["totalCases"] == 4
    )
    download = await client.get(f"/api/v1/dashboard/reports/{rid}/download")
    assert download.status_code == 200 and "<script>" not in download.text
    assert "&lt;script&gt;" in download.text and "实际结果记录数：1" in download.text
    assert "sandbox" in download.headers["content-security-policy"]
    inbox = (await client.get("/api/v1/notifications")).json()["data"]
    assert inbox["total"] == 2
    other = await other_user(client)
    try:
        assert (await other.get("/api/v1/notifications")).json()["data"]["total"] == 0
        assert (
            await other.put(
                "/api/v1/notifications/" + inbox["items"][0]["id"] + "/read"
            )
        ).status_code == 404
        assert (
            await other.get(f"/api/v1/dashboard/reports/{rid}/download")
        ).status_code == 404
        assert (
            await other.get(
                "/api/v1/executions", params={"project_id": case["projectId"]}
            )
        ).status_code == 403
        assert (await other.get("/api/v1/dashboard/reports")).json()["data"][
            "total"
        ] == 0
    finally:
        await other.aclose()
    assert (
        await client.get(
            f"/api/v1/dashboard/reports/{rid}/download", headers={"Authorization": ""}
        )
    ).status_code == 401
    assert (await client.put("/api/v1/notifications/read-all")).status_code == 200
    assert all(
        row["isRead"]
        for row in (await client.get("/api/v1/notifications")).json()["data"]["items"]
    )
    request.update(name="No execution", startDate="2099-01-01", endDate="2099-01-02")
    empty = await client.post("/api/v1/dashboard/reports", json=request)
    assert (
        empty.status_code == 200
        and empty.json()["data"]["passedCases"] == 0
        and empty.json()["data"]["executedCases"] == 0
    )
    request["format"] = "pdf"
    assert (
        await client.post("/api/v1/dashboard/reports", json=request)
    ).status_code == 422
    print(
        "Features: selected one case actually ran, template retained four; real history and escaped HTML; private downloads and user-scoped inbox; empty report zero passed"
    )


@pytest.mark.asyncio
async def test_single_case_rejects_incompatible_template(lab):
    client = lab["client"]
    base = "/api/v1/test-cases/" + lab["cases"][0]["id"] + "/execute"
    assert (await client.post(base, json={"suiteId": "missing"})).status_code == 404
    sid = lab["suite"]["id"]
    await client.put(
        "/api/v1/test-plans/suites/" + sid, json={"case_ids": [lab["cases"][1]["id"]]}
    )
    assert (await client.post(base, json={"suiteId": sid})).status_code == 422
    await client.put(
        "/api/v1/test-plans/suites/" + sid,
        json={"case_ids": [lab["cases"][0]["id"]], "execution_command": "pytest"},
    )
    assert (await client.post(base, json={"suiteId": sid})).status_code == 422
    from database import SessionLocal
    from models import TestSuite

    with SessionLocal() as db:
        assert db.query(TestSuite).count() == 1


@pytest.mark.asyncio
async def test_local_upload_boundaries_and_no_overwrite(lab, tmp_path):
    client = lab["client"]
    root = lab["agent"].work_dir
    endpoint = "/api/v1/environments/" + lab["environment"]["id"] + "/workspace/upload"

    async def upload(name="sample.bin", path="uploads", content=b"original\x00bytes"):
        return await client.post(
            endpoint,
            data={"path": path},
            files={"file": (name, content, "application/octet-stream")},
        )

    response = await upload()
    assert response.status_code == 200, response.text
    actual = root / "uploads" / "sample.bin"
    assert actual.read_bytes() == b"original\x00bytes"
    response = await upload(content=b"replacement")
    assert response.status_code >= 400 and actual.read_bytes() == b"original\x00bytes"
    for name in ["../escape", "x/y", "x\\y", ".."]:
        response = await upload(name=name)
        assert response.status_code == 400, response.text
    for path in ["../outside", "/absolute", "x/../../outside", "x\\y"]:
        assert (await upload(path=path)).status_code == 400
    outside = tmp_path / "outside"
    outside.mkdir()
    (root / "linked").symlink_to(outside, target_is_directory=True)
    response = await upload(path="linked")
    assert response.status_code >= 400 and not list(outside.iterdir())
    assert (
        await upload(name="at-limit.bin", content=b"x" * (10 * 1024 * 1024))
    ).status_code == 200
    assert (root / "uploads" / "at-limit.bin").stat().st_size == 10 * 1024 * 1024
    assert (await upload(content=b"x" * (10 * 1024 * 1024 + 1))).status_code == 413
    assert actual.read_bytes() == b"original\x00bytes"
    other = await other_user(client)
    try:
        response = await other.post(
            endpoint, files={"file": ("other.txt", b"outside-user")}
        )
        assert response.status_code == 403 and not (root / "other.txt").exists()
    finally:
        await other.aclose()
    print(
        "Upload: binary bytes persisted; overwrite, traversal, hostile names, symlink escape, >10MB all rejected; originals preserved"
    )


@pytest.mark.asyncio
async def test_existing_project_module_plan_and_dashboard(lab):
    """验证既有项目搜索、模块树、计划状态和仪表盘的实际契约。"""
    client, post = lab["client"], lab["post"]
    project_id = lab["cases"][0]["projectId"]
    response = await client.get("/api/v1/projects", params={"search": "SAT software"})
    assert response.status_code == 200, response.text
    assert response.json()["data"]["total"] == 1
    assert (await client.get("/api/v1/projects", params={"search": "不存在"})).json()[
        "data"
    ]["total"] == 0
    module = await post(
        f"/projects/{project_id}/modules", {"name": "诊断", "sortOrder": 1}
    )
    child = await post(
        f"/projects/{project_id}/modules",
        {"name": "读取DID", "parentId": module["id"], "sortOrder": 2},
    )
    case = lab["cases"][0]
    response = await client.put(
        f'/api/v1/test-cases/{case["id"]}', json={"module_id": child["id"]}
    )
    assert response.status_code == 200, response.text
    modules = (await client.get(f"/api/v1/projects/{project_id}/modules")).json()[
        "data"
    ]["modules"]
    assert any(row["id"] == child["id"] and row["caseCount"] == 1 for row in modules)
    tree = await client.get(
        "/api/v1/test-cases/tree", params={"project_id": project_id}
    )
    assert tree.status_code == 200 and "读取DID" in tree.text
    plan_id = lab["plan"]["id"]
    base = f"/api/v1/test-plans/{plan_id}"
    assert (await client.post(base + "/pause")).status_code == 200
    assert (await client.get(base)).json()["data"]["status"] == "paused"
    assert (await client.post(base + "/resume")).status_code == 200
    assert (
        await client.put(base + f'/cases/{case["id"]}/status', json={})
    ).status_code == 400
    assert (
        await client.put(base + "/cases/missing/status", json={"status": "pass"})
    ).status_code == 404
    # 恢复会创建真实批次；自动化用例必须由 Agent 回传，不能人工伪造通过。
    assert (
        await client.put(base + f'/cases/{case["id"]}/status', json={"status": "pass"})
    ).status_code == 409
    clone = await post(f"/test-plans/{plan_id}/clone", {"project_id": project_id})
    clone_detail = (await client.get("/api/v1/test-plans/" + clone["id"])).json()[
        "data"
    ]
    assert len(clone_detail["testCases"]) == 4
    suite_id = lab["suite"]["id"]
    from services.plan_orchestration import advance_plan_runs
    from database import SessionLocal
    # 软件 fixture 关闭 FastAPI lifespan，显式推进刚才恢复创建的计划批次。
    with SessionLocal() as db:
        await advance_plan_runs(db)
    await until(
        lambda: bool(queue_states(suite_id))
        and set(queue_states(suite_id).values()) == {"completed"}
    )
    with SessionLocal() as db:
        await advance_plan_runs(db)
    history = (await client.get(base + "/executions")).json()["data"]
    assert history["total"] == 1 and history["items"][0]["report"]["counts"]["passed"] == 4
    overview = (
        await client.get("/api/v1/dashboard/overview", params={"projectId": project_id})
    ).json()["data"]
    assert overview["totalProjects"] == 1 and overview["successRate"] == 100
    trend = (
        await client.get("/api/v1/dashboard/trends", params={"projectId": project_id})
    ).json()["data"]
    assert len(trend["dates"]) == 7 and sum(trend["passed"]) == 4
    stats = (await client.get("/api/v1/dashboard/project-stats")).json()["data"]
    assert stats["items"][0]["executionCount"] == 4


@pytest.mark.asyncio
async def test_suite_validation_and_active_template_protection(lab):
    """允许已授权跨项目来源，拒绝空模板和执行期间改模板，保持原结果关联。"""
    client, post = lab["client"], lab["post"]
    other = await post("/projects", {"name": "其他项目"})
    foreign = await post(
        "/test-cases",
        {
            "project_id": other["id"],
            "case_code": "foreign",
            "name": "外部用例",
            "type": "functional",
            "is_automated": True,
        },
    )
    suite_id, plan_id = lab["suite"]["id"], lab["plan"]["id"]
    base = f"/api/v1/test-plans/suites/{suite_id}"
    response = await client.post(
        f"/api/v1/test-plans/{plan_id}/suites",
        json={
            "plan_id": plan_id,
            "name": "无效模板",
            "environment_id": lab["environment"]["id"],
            "execution_command": "ats-sat --mode offline",
            "case_ids": [foreign["id"]],
        },
    )
    assert response.status_code == 200, response.text
    created = response.json()["data"]
    assert created["caseIds"] == [foreign["id"]] and created["planId"] == plan_id
    assert (await client.delete(f"/api/v1/test-plans/suites/{created['id']}" )).status_code == 200
    assert (await client.put(base, json={"case_ids": []})).status_code == 400
    from database import SessionLocal
    from models.task_queue import TaskQueue

    with SessionLocal() as db:
        task = TaskQueue(
            environment_id=lab["environment"]["id"],
            suite_id=suite_id,
            execution_id=str(uuid.uuid4()),
            executor_id=lab["cases"][0]["createdBy"],
            status="pending",
        )
        db.add(task)
        db.commit()
        task_id = task.id
    assert (
        await client.put(base, json={"case_ids": [foreign["id"]]})
    ).status_code == 400
    assert (await client.delete(base)).status_code == 409
    assert len((await client.get(base)).json()["data"]["caseIds"]) == 4
    with SessionLocal() as db:
        db.get(TaskQueue, task_id).status = "cancelled"
        db.commit()
    assert (await client.put(base, json={"name": "结束后可编辑"})).status_code == 200
    # 所选用例在创建模板后被改为手工用例，执行前必须拒绝，不能产生运行中队列项。
    await client.put(
        "/api/v1/test-cases/" + lab["cases"][0]["id"], json={"is_automated": False}
    )
    assert (await client.post(base + "/execute")).status_code == 400
    assert set(queue_states(suite_id).values()) == {"cancelled"}


@pytest.mark.asyncio
async def test_workspace_read_mkdir_delete_and_traversal(lab):
    """通过真实 Agent 验证目录、文件读取/下载/删除及边界。"""
    client = lab["client"]
    base = "/api/v1/environments/" + lab["environment"]["id"] + "/workspace"
    response = await client.post(base + "/mkdir", params={"path": "回归目录"})
    assert response.status_code == 200, response.text
    uploaded = await client.post(
        base + "/upload",
        data={"path": "回归目录"},
        files={"file": ("说明.txt", "软件回归".encode())},
    )
    assert uploaded.status_code == 200, uploaded.text
    listing = await client.get(base + "/list", params={"path": "回归目录"})
    assert listing.status_code == 200 and "说明.txt" in listing.text
    read = await client.get(base + "/read", params={"path": "回归目录/说明.txt"})
    assert read.status_code == 200 and "软件回归" in read.text
    escape = await client.get(base + "/read", params={"path": "../../outside"})
    assert escape.status_code >= 400
    response = await client.post(base + "/delete", params={"path": "回归目录/说明.txt"})
    assert response.status_code == 200, response.text
    assert (
        await client.get(base + "/read", params={"path": "回归目录/说明.txt"})
    ).status_code >= 400


@pytest.mark.asyncio
async def test_report_date_range_includes_business_day_boundaries(lab):
    """报告包含北京时间首末秒，排除相邻日期，与宿主 TZ 无关。"""
    from database import SessionLocal
    from models import TestExecution
    from utils.datetime_utils import BEIJING_TZ

    markers = ("前一天末秒", "当天首秒", "当天末秒", "后一天首秒")
    dates = (
        datetime(2026, 10, 4, 23, 59, 59, tzinfo=BEIJING_TZ),
        datetime(2026, 10, 5, 0, 0, 0, tzinfo=BEIJING_TZ),
        datetime(2026, 10, 5, 23, 59, 59, tzinfo=BEIJING_TZ),
        datetime(2026, 10, 6, 0, 0, 0, tzinfo=BEIJING_TZ),
    )
    with SessionLocal() as db:
        for case, executed_at, marker in zip(lab["cases"], dates, markers):
            db.add(
                TestExecution(
                    id=str(uuid.uuid4()),
                    plan_id=lab["plan"]["id"],
                    case_id=case["id"],
                    executor_id=case["createdBy"],
                    environment_id=lab["environment"]["id"],
                    result="passed",
                    executed_at=executed_at,
                    execution_log=marker,
                )
            )
        db.commit()

    for start, end, expected_markers in (
        ("2026-10-05", "2026-10-05", {"当天首秒", "当天末秒"}),
        ("2026-10-04", "2026-10-04", {"前一天末秒"}),
        ("2026-10-06", "2026-10-06", {"后一天首秒"}),
        ("2026-10-04", "2026-10-06", set(markers)),
    ):
        response = await lab["client"].post(
            "/api/v1/dashboard/reports",
            json=dict(
                name=f"日期边界验收 {start} 至 {end}",
                projectId=lab["cases"][0]["projectId"],
                startDate=start,
                endDate=end,
            ),
        )
        assert response.status_code == 200, response.text
        report = response.json()["data"]
        assert report["passedCases"] == len(expected_markers)
        assert report["executedCases"] == len(expected_markers)
        assert report["totalCases"] == 4
        download = await lab["client"].get(
            f"/api/v1/dashboard/reports/{report['id']}/download"
        )
        assert download.status_code == 200, download.text
        for marker in markers:
            assert (marker in download.text) == (marker in expected_markers)
