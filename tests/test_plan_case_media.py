"""执行描述图片：真实解码、权限、历史引用与事务边界。"""

from io import BytesIO
import httpx
import pytest
from PIL import Image
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from test_plan_case_execution import body, BASE
from models import TestPlan as Plan, Project, ProjectMember
from models.plan_case_media import PlanCaseMedia, PlanCaseMediaLink
from models.plan_case_execution import PlanCaseExecution
from models.plan_workspace import PlanWorkspace
from models.task_queue import TaskQueue

MEDIA = "/orchestration/plans/plan/execution-media"


def png():
    stream = BytesIO()
    Image.new("RGB", (32, 24), "green").save(stream, format="PNG")
    return stream.getvalue()


async def upload(client):
    response = await client.post(
        MEDIA, files={"file": ("软件验收.png", png(), "text/html")}
    )
    assert response.status_code == 200, response.text
    return response.json()["data"]


@pytest.mark.asyncio
async def test_media_permissions_history_batch_idempotence_and_unlink(workspace_http):
    db, app, identity = workspace_http
    db.add(ProjectMember(project_id="project", user_id="stranger", role="member"))
    db.commit()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        media = await upload(client)
        assert media["mimeType"] == "image/png" and media["fileSize"] == len(png())
        path = MEDIA + "/" + media["id"]
        preview = await client.get(path + "/preview")
        assert (
            preview.content == png() and preview.headers["content-type"] == "image/png"
        )
        assert preview.headers["cache-control"] == "private, no-store"
        assert preview.headers["x-content-type-options"] == "nosniff"
        download = await client.get(path + "/download")
        assert (
            download.content == png()
            and "attachment;" in download.headers["content-disposition"]
        )
        identity["id"] = "stranger"
        assert (await client.get(path + "/preview")).status_code == 403
        assert (
            await client.post(MEDIA, files={"file": ("x.png", png())})
        ).status_code == 403
        assert (await client.delete(path)).status_code == 403
        identity["id"] = "owner"
        rows = (await client.get(BASE)).json()["data"]["items"]
        payload = body(
            rows,
            description=f'<p>执行截图</p><img src="{media["src"]}" alt="截图"><img src="{media["src"]}">',
        )
        assert (await client.post(BASE + "/execute", json=payload)).status_code == 200
        assert db.query(PlanCaseMediaLink).count() == len(rows)
        assert (await client.post(BASE + "/execute", json=payload)).json()["data"][
            "replayed"
        ]
        assert db.query(PlanCaseMediaLink).count() == len(rows)
        assert (await client.delete(path)).status_code == 409
        row = rows[0]
        assert (
            await client.post(
                BASE + "/batch",
                json=dict(
                    action="unlink",
                    selections=[dict(source=row["source"], id=row["associationId"])],
                ),
            )
        ).status_code == 200
        identity["id"] = "stranger"
        assert (await client.get(path + "/preview")).content == png()
        detail = (
            await client.get(
                BASE + "/execution",
                params=dict(
                    source=row["source"],
                    associationId=row["associationId"],
                    caseId=row["caseId"],
                ),
            )
        ).json()["data"]
        assert (
            detail["detached"] and media["src"] in detail["history"][0]["description"]
        )
        assert db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_invalid_files_private_draft_delete_and_archive(
    workspace_http, monkeypatch
):
    db, app, identity = workspace_http
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        for raw in (b"", "<html>伪装图片</html>".encode(), png()[:16]):
            assert (
                await client.post(MEDIA, files={"file": ("bad.png", raw, "image/png")})
            ).status_code == 422
        from services.plan_case_media import settings

        with monkeypatch.context() as patch:
            patch.setattr(settings, "MAX_FILE_SIZE", 10)
            assert (
                await client.post(MEDIA, files={"file": ("large.png", png())})
            ).status_code == 422
        assert db.query(PlanCaseMedia).count() == 0
        media = await upload(client)
        path = MEDIA + "/" + media["id"]
        db.add(PlanWorkspace(plan_id="plan", archived=True))
        db.commit()
        assert (
            await client.post(MEDIA, files={"file": ("x.png", png())})
        ).status_code == 409
        assert (await client.delete(path)).status_code == 409
        assert (await client.get(path + "/preview")).status_code == 200
        db.get(PlanWorkspace, "plan").archived = False
        db.commit()
        assert (await client.delete(path)).status_code == 200
        assert (await client.get(path + "/preview")).status_code == 404
        assert db.query(PlanCaseExecution).count() == 0


@pytest.mark.asyncio
async def test_foreign_media_rejected_and_failed_commit_rolls_back_links(
    workspace_http, monkeypatch
):
    db, app, identity = workspace_http
    db.add(Project(id="other", name="另一项目", owner_id="owner"))
    db.flush()
    db.add(
        Plan(
            id="other-plan",
            project_id="other",
            plan_number="OTHER",
            name="另一计划",
            owner_id="owner",
        )
    )
    db.commit()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        media = await upload(client)
        assert (
            await client.get(
                MEDIA.replace("/plan/", "/other-plan/") + "/" + media["id"] + "/preview"
            )
        ).status_code == 404
        rows = (await client.get(BASE)).json()["data"]["items"]
        for source in (
            media["src"].replace("/plan/", "/other-plan/"),
            media["src"] + "?forged=1",
        ):
            assert (
                await client.post(
                    BASE + "/execute",
                    json=body(rows, description=f'<img src="{source}">'),
                )
            ).status_code == 422
        payload = body(rows, description=f'<img src="{media["src"]}">')

        def failure():
            raise RuntimeError("软件回归模拟图片引用提交失败")

        with monkeypatch.context() as patch:
            patch.setattr(db, "commit", failure)
            with pytest.raises(RuntimeError, match="图片引用提交失败"):
                await client.post(BASE + "/execute", json=payload)
        assert db.query(PlanCaseExecution).count() == 0
        assert db.query(PlanCaseMediaLink).count() == 0
        assert db.query(PlanCaseMedia).count() == 1
        assert db.query(TaskQueue).count() == 0
        # 草稿未被失败提交占用，上传人仍可删除。
        assert (await client.delete(MEDIA + "/" + media["id"])).status_code == 200
