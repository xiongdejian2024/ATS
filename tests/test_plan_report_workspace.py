"""独立报告目录：真实手工批次、SQL分页筛选与项目隔离。"""
from datetime import datetime
import httpx
import pytest
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from models import Project, TestPlan as Plan, PlanCaseRelation
from models.plan_orchestration import PlanRun, PlanGroup, PlanSettings
from models.plan_group_execution import PlanGroupRunChild
from models.task_schedule import TaskSchedule, TaskScheduleRun
from services.plan_orchestration import start_plan_run, record_manual_result, advance_plan_runs
from services.plan_group_execution import start_group_run, advance_group_runs
from schemas.plan_orchestration import ManualResultInput


@pytest.fixture
def reports_http(workspace_http):
    db, app, identity = workspace_http
    db.add(Project(id="other", name="另一隔离项目", owner_id="owner"))
    db.add(Plan(id="manual", project_id="project", owner_id="owner", name="手工回归", plan_number="TP-002"))
    db.flush()
    db.add(PlanCaseRelation(plan_id="manual", case_id="case-2"))
    db.commit()
    return db, app, identity


@pytest.mark.asyncio
async def test_directory_lists_frozen_plan_and_group_with_real_trigger(reports_http):
    db, app, identity = reports_http
    direct = await start_plan_run(db, "manual", "owner")
    record_manual_result(db, direct.id, "case-2", ManualResultInput(result="passed"), "owner")
    await advance_plan_runs(db)
    assert direct.report["passRate"] == 100
    db.add(PlanGroup(id="group", project_id="project", name="集成回归"))
    db.flush()
    db.add(PlanSettings(plan_id="manual", group_id="group"))
    db.commit()
    group = await start_group_run(db, "group", "owner")
    await advance_group_runs(db)
    child_id = db.query(PlanGroupRunChild).filter_by(run_id=group.id).one().plan_run_id
    record_manual_result(db, child_id, "case-2", ManualResultInput(result="failed"), "owner")
    await advance_plan_runs(db)
    await advance_group_runs(db)
    now = datetime(2026, 10, 5, 10)
    direct.created_at, group.created_at = datetime(2026, 10, 3, 10), now
    db.get(PlanRun, child_id).created_at = datetime(2026, 10, 4, 10)
    db.add(TaskSchedule(id="scheduled", project_id="project", name="定时组", target_type="group", target_id="group", created_by="owner", created_at=now, updated_at=now))
    db.flush()
    db.add(TaskScheduleRun(schedule_id="scheduled", trigger_key="cron-test", trigger_type="cron", scheduled_for=now,
                           executor_id="owner", group_run_id=group.id, created_at=now))
    db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        base = "/orchestration/projects/project/reports"
        listing = (await client.get(base)).json()["data"]
        assert listing["total"] == 3
        assert [(row["kind"], row["triggerMode"]) for row in listing["items"]] == [("GROUP", "cron"), ("PLAN", "cron"), ("PLAN", "manual")]
        assert listing["items"][0]["resultStatus"] == "failed"
        assert listing["items"][2]["passRate"] == 100
        assert (await client.get(base, params={"page": 2, "size": 1})).json()["data"]["items"][0]["id"] == child_id
        assert (await client.get(base, params={"kind": "GROUP", "trigger_mode": "cron"})).json()["data"]["total"] == 1
        assert (await client.get(base, params={"min_rate": 100, "result_status": "passed", "operator": "负责人"})).json()["data"]["total"] == 1
        assert (await client.get(base, params={"search": "%"})).json()["data"]["total"] == 0  # 搜索不是SQL通配符
        assert (await client.get(base, params={"plan_name": "手工", "start_time": "2026-10-04T00:00:00+08:00", "end_time": "2026-10-04T23:59:59"})).json()["data"]["total"] == 1
        assert (await client.get(base, params={"sort": "pass_rate", "direction": "desc"})).json()["data"]["items"][0]["id"] == direct.id
        assert (await client.get(base + f"/PLAN/{direct.id}")).json()["data"]["payload"]["report"]["passRate"] == 100
        assert (await client.get(base + f"/GROUP/{group.id}")).json()["data"]["payload"]["children"][0]["id"] == child_id
        assert (await client.get(f"/orchestration/projects/other/reports/PLAN/{direct.id}")).status_code == 404
        assert (await client.get(f"/orchestration/projects/other/reports/GROUP/{group.id}")).status_code == 404
        assert (await client.get('/orchestration/projects/other/reports')).json()["data"]["total"] == 0
        identity["id"] = "stranger"
        for path in (base, base + f"/PLAN/{direct.id}", base + f"/GROUP/{group.id}"):
            assert (await client.get(path)).status_code == 403


@pytest.mark.asyncio
async def test_active_report_and_filter_validation_do_not_dispatch(reports_http):
    db, app, identity = reports_http
    run = await start_plan_run(db, "manual", "owner")
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        base = "/orchestration/projects/project/reports"
        row = (await client.get(base)).json()["data"]["items"][0]
        assert row["passRate"] is None and row["resultStatus"] == run.status
        for params in ({"min_rate": 90, "max_rate": 20}, {"size": 101}, {"sort": "report"},
                       {"start_time": "2026-10-05T00:00:00+08:00", "end_time": "2026-10-01T00:00:00"}):
            assert (await client.get(base, params=params)).status_code == 422
    from models.task_queue import TaskQueue
    assert db.query(TaskQueue).count() == 0
