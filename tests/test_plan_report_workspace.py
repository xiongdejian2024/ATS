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


@pytest.mark.asyncio
async def test_rename_delete_revokes_shares_but_retains_frozen_history(reports_http):
    from copy import deepcopy
    from api.v1.plan_group_execution import router as groups
    from models.plan_report_workspace import PlanReportWorkspace, GroupReportWorkspace
    from models.plan_group_execution import PlanGroupRun
    db, app, identity = reports_http
    app.include_router(groups)
    direct = await start_plan_run(db, 'manual', 'owner')
    record_manual_result(db, direct.id, 'case-2', ManualResultInput(result='passed'), 'owner')
    await advance_plan_runs(db)
    frozen = deepcopy(direct.report)
    db.add(PlanGroup(id='group', project_id='project', name='报告管理组'))
    db.flush()
    db.add(PlanSettings(plan_id='manual', group_id='group'))
    db.commit()
    group = await start_group_run(db, 'group', 'owner')
    await advance_group_runs(db)
    child_id = db.query(PlanGroupRunChild).filter_by(run_id=group.id).one().plan_run_id
    record_manual_result(db, child_id, 'case-2', ManualResultInput(result='passed'), 'owner')
    await advance_plan_runs(db)
    await advance_group_runs(db)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        base = '/orchestration/projects/project/reports'
        assert (await client.put(base + f'/PLAN/{direct.id}/name', json={'name':'   '})).status_code == 422
        assert (await client.put(base + f'/PLAN/{direct.id}/name', json={'name':'独立报告改名'})).json()['data']['name'] == '独立报告改名'
        assert (await client.put(base + f'/GROUP/{group.id}/name', json={'name':'聚合报告改名'})).status_code == 200
        rows = (await client.get(base, params={'search':'改名'})).json()['data']['items']
        assert {row['name'] for row in rows} == {'独立报告改名', '聚合报告改名'}
        assert (await client.get(base + f'/PLAN/{direct.id}')).json()['data']['name'] == '独立报告改名'
        assert (await client.get(f'/plan-groups/runs/{group.id}')).json()['data']['reportName'] == '聚合报告改名'
        share = (await client.post(f'/orchestration/runs/{direct.id}/shares', json={'expiresHours':1})).json()['data']['token']
        group_share = (await client.post(f'/plan-groups/runs/{group.id}/share', json={'expiresHours':1})).json()['data']['path']
        assert (await client.get(f'/orchestration/shared/{share}')).status_code == 200
        invalid = [{'kind':'PLAN','id':direct.id}, {'kind':'GROUP','id':'outside'}]
        assert (await client.post(base + '/batch-delete', json={'reports':invalid})).status_code == 404
        assert not db.get(PlanReportWorkspace, direct.id).deleted
        assert (await client.post(base + '/batch-delete', json={'reports':[invalid[0],invalid[0]]})).status_code == 422
        selected = [{'kind':'PLAN','id':direct.id}, {'kind':'GROUP','id':group.id}]
        assert (await client.post(base + '/batch-delete', json={'reports':selected})).json()['data']['deleted'] == 2
        assert (await client.get(base)).json()['data']['total'] == 1  # 子计划报告仍独立保留
        for path in (base + f'/PLAN/{direct.id}', base + f'/GROUP/{group.id}', f'/orchestration/runs/{direct.id}/report',
                     f'/orchestration/runs/{direct.id}/pdf', f'/orchestration/shared/{share}', f'/plan-groups/runs/{group.id}/pdf', group_share):
            assert (await client.get(path)).status_code == 404, path
        assert (await client.post(f'/orchestration/runs/{direct.id}/shares',json={'expiresHours':1})).status_code == 404
        assert (await client.post(f'/plan-groups/runs/{group.id}/share',json={'expiresHours':1})).status_code == 404
        assert (await client.delete(base + f'/PLAN/{direct.id}')).status_code == 200  # 删除可安全重试
        db.expire_all()
        assert db.get(PlanRun, direct.id).report == frozen
        assert db.get(PlanGroupRun, group.id).report['passRate'] == 100
        assert db.get(GroupReportWorkspace, group.id).deleted
        assert (await client.get(f'/orchestration/runs/{direct.id}')).status_code == 200  # 执行记录保持可读


@pytest.mark.asyncio
async def test_readonly_member_capabilities_and_active_delete_guard(reports_http):
    from models import ProjectMember
    db, app, identity = reports_http
    db.add(ProjectMember(project_id='project', user_id='stranger', role='member'))
    db.commit()
    run = await start_plan_run(db, 'manual', 'owner')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        base = '/orchestration/projects/project/reports'
        assert (await client.delete(base + f'/PLAN/{run.id}')).status_code == 409
        identity['id']='stranger'
        payload=(await client.get(base)).json()['data']
        assert not payload['canRename'] and not payload['canDelete'] and payload['total']==1
        assert (await client.put(base + f'/PLAN/{run.id}/name',json={'name':'无权限改名'})).status_code==403
        assert (await client.delete(base + f'/PLAN/{run.id}')).status_code==403
