"""计划组冻结、真实软件队列、定时幂等与可撤销报告验收。"""
from datetime import datetime, timedelta, timezone
import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from api.deps import get_current_user
from database import get_db
from models import User, TestPlan as Plan, PlanCaseRelation, TestCase as Case
from models.plan_orchestration import PlanGroup, PlanSettings, PlanRunItem
from models.plan_group_execution import PlanGroupPolicy, PlanGroupRun, PlanGroupShare
from models.task_queue import TaskQueue
from services.plan_group_execution import start_group_run, advance_group_runs, cancel_group_run, children, run_data
from services.plan_orchestration import advance_plan_runs, record_manual_result
from schemas.plan_orchestration import ManualResultInput
from test_plan_orchestration import plan_lab, finish


@pytest.fixture
def group_lab(plan_lab):
    db, sent = plan_lab
    db.add(PlanGroup(id="group", project_id="project", name="版本回归组"))
    db.add(Plan(id="manual", project_id="project", owner_id="owner", name="手工计划", plan_number="TP-002"))
    db.flush()
    db.add_all([PlanSettings(plan_id="plan", group_id="group"), PlanSettings(plan_id="manual", group_id="group"),
                PlanCaseRelation(plan_id="manual", case_id="case-2"),
                PlanGroupPolicy(group_id="group", plan_order=["plan", "manual"], stop_on_failure=True)])
    db.commit()
    return db, sent


async def finish_automatic(db, child, result="passed"):
    await advance_plan_runs(db)
    for item in db.query(PlanRunItem).filter_by(run_id=child.id).order_by(PlanRunItem.sequence).all():
        if item.status == "running":
            finish(db, item, result)
            await advance_plan_runs(db)


@pytest.mark.asyncio
async def test_serial_freezes_all_members_and_keeps_independent_report(group_lab):
    db, sent = group_lab
    run = await start_group_run(db, "group", "owner", "serial")
    assert (await start_group_run(db, "group", "owner", "serial")).id == run.id
    first, second = children(db, run)
    assert [first.status, second.status] == ["group_waiting", "group_waiting"]
    assert db.query(TaskQueue).count() == 0 and not sent
    with pytest.raises(ValueError):
        record_manual_result(db, second.id, "case-2", ManualResultInput(result="passed"), "owner")
    original = second.case_snapshot[0]["name"]
    db.get(Case, "case-2").name = "执行后修改的用例"
    db.commit()
    await advance_group_runs(db)
    assert second.status == "group_waiting" and db.query(TaskQueue).count() == 1
    await finish_automatic(db, first)
    await advance_group_runs(db)
    assert first.status == "completed" and second.status == "running"
    assert second.case_snapshot[0]["name"] == original
    record_manual_result(db, second.id, "case-2", ManualResultInput(result="passed"), "owner")
    await advance_plan_runs(db)
    await advance_group_runs(db)
    data = run_data(db, run)
    assert run.status == "completed" and run.active_group_id is None
    assert data["report"]["total"] == 3 and data["report"]["passRate"] == 100
    assert len(sent) == 2 and len(data["children"]) == 2


@pytest.mark.asyncio
async def test_parallel_release_and_failed_serial_stop(group_lab):
    db, sent = group_lab
    run = await start_group_run(db, "group", "owner")
    first, second = children(db, run)
    await advance_group_runs(db)
    await finish_automatic(db, first, "failed")
    await advance_group_runs(db)
    await advance_plan_runs(db)
    await advance_group_runs(db)
    assert first.status == "failed" and second.status == "cancelled"
    assert run.status == "failed" and run.report["counts"]["cancelled"] == 1
    policy = db.get(PlanGroupPolicy, "group")
    policy.execution_mode, policy.stop_on_failure = "parallel", False
    db.commit()
    parallel = await start_group_run(db, "group", "owner")
    await advance_group_runs(db)
    assert all(c.status in ("queued", "running") for c in children(db, parallel))


@pytest.mark.asyncio
async def test_cancel_before_dispatch_and_permissions(group_lab):
    db, sent = group_lab
    run = await start_group_run(db, "group", "owner")
    with pytest.raises(HTTPException) as error:
        await start_group_run(db, "group", "owner")
    assert error.value.status_code == 409
    await cancel_group_run(db, run, db.get(User, "owner"))
    await advance_plan_runs(db)
    await advance_group_runs(db)
    assert run.status == "cancelled" and not sent and db.query(TaskQueue).count() == 0
    run = await start_group_run(db, "group", "owner")
    db.get(User, "owner").status = False
    db.commit()
    await advance_group_runs(db)
    await advance_plan_runs(db)
    await advance_group_runs(db)
    await advance_plan_runs(db)
    await advance_group_runs(db)
    assert run.status == "failed" and not sent


@pytest.mark.asyncio
async def test_schedule_group_idempotence_and_cancel(group_lab):
    from services.task_scheduler import create_schedule, trigger_schedule, scheduler_tick, cancel_run, reconcile_runs
    from schemas.task_center import ScheduleCreate
    db, sent = group_lab
    owner = db.get(User, "owner")
    schedule = create_schedule(db, owner, ScheduleCreate(projectId="project", name="每日版本", targetType="group", targetId="group", cronExpression="0 9 * * 1-5"))
    assert schedule.enabled is False
    run = await trigger_schedule(db, owner, schedule, "相同请求")
    assert (await trigger_schedule(db, owner, schedule, "相同请求")).id == run.id
    assert run.group_run_id and db.query(PlanGroupRun).count() == 1
    await cancel_run(db, owner, run)
    await scheduler_tick(db)
    await reconcile_runs(db)
    assert run.status == "cancelled" and not sent


@pytest.mark.asyncio
async def test_api_pdf_share_expiry_revoke_and_foreign_access(group_lab):
    from api.v1.plan_group_execution import router
    db, sent = group_lab
    run = await start_group_run(db, "group", "owner")
    await cancel_group_run(db, run, db.get(User, "owner"))
    state = {"user": db.get(User, "owner")}
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user] = lambda: state["user"]
    with TestClient(app) as client:
        base = "/api/v1/plan-groups/runs/" + run.id
        assert client.put(base+"/summary", json={"conclusion":"中文验收结论"}).status_code == 200
        assert client.get(base+"/pdf").content.startswith(b"%PDF-")
        share = client.post(base+"/share", json={"expiresHours":1}).json()["data"]
        assert client.get(share["path"]).content.startswith(b"%PDF-")
        assert client.delete(base+"/shares/"+share["id"]).status_code == 200
        assert client.get(share["path"]).status_code == 404
        share = client.post(base+"/share", json={"expiresHours":1}).json()["data"]
        db.get(PlanGroupShare, share["id"]).expires_at = datetime.now(timezone.utc).replace(tzinfo=None)-timedelta(seconds=1)
        db.commit()
        assert client.get(share["path"]).status_code == 404
        db.add(User(id="stranger", username="外部用户", email="other@example.test", password_hash="测试"))
        db.commit()
        state["user"] = db.get(User, "stranger")
        assert client.get(base).status_code == 403
