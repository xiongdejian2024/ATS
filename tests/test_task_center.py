"""任务中心使用隔离数据库与真实回环 Agent 的软件验收。"""

from datetime import datetime, timedelta
import uuid

import pytest
from test_http_agent_e2e import lab, until, queue_states
from test_features import other_user
from models.task_schedule import TaskSchedule, TaskScheduleRun


async def make_schedule(lab, target_type="suite", cron=None):
    response = await lab["client"].post("/api/v1/task-center", json={
        "projectId": lab["plan"]["projectId"], "name": "隔离软件任务",
        "targetType": target_type, "targetId": lab[target_type]["id"],
        "cronExpression": cron, "timezone": "Asia/Shanghai",
    })
    assert response.status_code == 200, response.text
    return response.json()["data"]


async def trigger(lab, schedule, request_id="测试点击"):
    response = await lab["client"].post(f'/api/v1/task-center/{schedule["id"]}/run', json={"requestId": request_id})
    assert response.status_code == 200, response.text
    return response.json()["data"]


def test_cron_uses_timezone_and_validates():
    from services.task_scheduler import next_fire_time

    now = datetime(2026, 10, 5, 0, 0, 30)
    assert next_fire_time("0 9 * * 1-5", "Asia/Shanghai", now) == datetime(2026, 10, 5, 1)
    assert next_fire_time("0 9 * * 1-5", "UTC", now) == datetime(2026, 10, 5, 9)
    for expression, timezone in [("bad", "UTC"), ("70 * * * *", "UTC"), ("* * * * *", "BAD/ZONE")]:
        with pytest.raises(ValueError):
            next_fire_time(expression, timezone, now)


@pytest.mark.asyncio
async def test_immediate_run_is_idempotent_and_uses_real_agent(lab):
    from database import SessionLocal
    from models import TestSuiteExecution
    from services.task_scheduler import scheduler_tick, reconcile_runs

    schedule = await make_schedule(lab)
    assert schedule["enabled"] is False and schedule["nextRunAt"] is None
    first = await trigger(lab, schedule)
    second = await trigger(lab, schedule)
    assert first["id"] == second["id"]
    assert first["status"] == "queued"
    assert len(queue_states(lab["suite"]["id"])) == 1
    with SessionLocal() as db:
        await scheduler_tick(db)
    await until(lambda: queue_states(lab["suite"]["id"]).get(first["executionId"]) in {"completed", "failed"})
    with SessionLocal() as db:
        await reconcile_runs(db)
        # 四条结果确实由 Agent + XAT 子进程产生。
        assert db.query(TestSuiteExecution).count() == 4
        assert db.get(TaskScheduleRun, first["id"]).status in {"completed", "failed"}
    history = await lab["client"].get(f'/api/v1/task-center/{schedule["id"]}/runs')
    assert history.json()["data"]["total"] == 1


@pytest.mark.asyncio
async def test_due_restart_recovery_coalesces_and_stale_claim_cannot_duplicate(lab):
    from database import SessionLocal
    from services.task_scheduler import enqueue_due, utc_now

    schedule = await make_schedule(lab, cron="* * * * *")
    with SessionLocal() as db:
        assert await enqueue_due(db) == 0  # 创建不会暗中启用。
    response = await lab["client"].post(f'/api/v1/task-center/{schedule["id"]}/enabled', json={"enabled": True})
    assert response.status_code == 200
    now = utc_now()
    with SessionLocal() as db:
        row = db.get(TaskSchedule, schedule["id"])
        row.next_run_at = now - timedelta(days=2)
        db.commit()
    # 模拟重启：新会话从持久化记录恢复，只合并一次过期触发。
    with SessionLocal() as first, SessionLocal() as stale:
        stale.get(TaskSchedule, schedule["id"])
        assert await enqueue_due(first, now) == 1
        assert await enqueue_due(stale, now) == 0
    with SessionLocal() as restarted:
        assert await enqueue_due(restarted, now) == 0
        assert restarted.query(TaskScheduleRun).filter_by(schedule_id=schedule["id"]).count() == 1
        assert restarted.get(TaskSchedule, schedule["id"]).next_run_at > now
    response = await lab["client"].post(f'/api/v1/task-center/{schedule["id"]}/enabled', json={"enabled": False})
    assert response.json()["data"]["nextRunAt"] is None


@pytest.mark.asyncio
async def test_project_access_and_cross_project_target_are_rejected(lab):
    schedule = await make_schedule(lab)
    stranger = await other_user(lab["client"])
    try:
        for path in [f'/api/v1/task-center?projectId={schedule["projectId"]}', f'/api/v1/task-center/{schedule["id"]}/runs']:
            assert (await stranger.get(path)).status_code == 403
        assert (await stranger.post(f'/api/v1/task-center/{schedule["id"]}/run', json={"requestId": "越权"})).status_code == 403
        assert (await stranger.post(f'/api/v1/task-center/{schedule["id"]}/enabled', json={"enabled": True})).status_code == 403
    finally:
        await stranger.aclose()
    project = await lab["post"]("/projects", {"name": "另一个隔离项目"})
    response = await lab["client"].post("/api/v1/task-center", json={
        "projectId": project["id"], "name": "错误目标", "targetType": "suite", "targetId": lab["suite"]["id"],
    })
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_queued_cancel_never_dispatches(lab):
    from database import SessionLocal
    from services.task_scheduler import scheduler_tick

    schedule = await make_schedule(lab)
    run = await trigger(lab, schedule)
    response = await lab["client"].post(f'/api/v1/task-center/{schedule["id"]}/runs/{run["id"]}/cancel')
    assert response.status_code == 200, response.text
    assert response.json()["data"]["status"] == "cancelled"
    with SessionLocal() as db:
        await scheduler_tick(db)
    assert queue_states(lab["suite"]["id"])[run["executionId"]] == "cancelled"
    assert not lab["agent"].sat_runner.has_suite(lab["suite"]["id"])


@pytest.mark.asyncio
async def test_running_cancel_waits_for_actual_agent_completion(lab):
    from database import SessionLocal
    from services.task_scheduler import scheduler_tick, reconcile_runs

    schedule = await make_schedule(lab)
    run = await trigger(lab, schedule)
    with SessionLocal() as db:
        await scheduler_tick(db)
    await until(lambda: lab["agent"].sat_runner.has_suite(lab["suite"]["id"]))
    response = await lab["client"].post(f'/api/v1/task-center/{schedule["id"]}/runs/{run["id"]}/cancel')
    assert response.status_code == 200, response.text
    assert response.json()["data"]["status"] in {"cancelling", "cancelled"}
    await until(lambda: queue_states(lab["suite"]["id"])[run["executionId"]] == "cancelled")
    with SessionLocal() as db:
        await reconcile_runs(db)
        assert db.get(TaskScheduleRun, run["id"]).status == "cancelled"


@pytest.mark.asyncio
async def test_dispatch_crash_is_visible_and_only_user_can_resolve(lab):
    from database import SessionLocal
    from models.task_queue import TaskQueue
    from services.task_scheduler import reconcile_runs, utc_now

    schedule = await make_schedule(lab)
    run = await trigger(lab, schedule)
    with SessionLocal() as db:
        row = db.get(TaskScheduleRun, run["id"])
        row.delivery_state, row.status = "dispatching", "running"
        row.dispatch_attempted_at = utc_now() - timedelta(seconds=40)
        db.query(TaskQueue).filter_by(execution_id=row.execution_id).update({"status": "running"})
        db.commit()
    with SessionLocal() as restarted:
        await reconcile_runs(restarted)
        row = restarted.get(TaskScheduleRun, run["id"])
        assert row.status == "needs_confirmation"
        assert "不会自动重派" in row.error_message
    response = await lab["client"].post(f'/api/v1/task-center/{schedule["id"]}/runs/{run["id"]}/resolve')
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "failed"
    assert queue_states(lab["suite"]["id"])[run["executionId"]] == "failed"


@pytest.mark.asyncio
async def test_plan_task_creates_real_plan_run_and_no_second_suite_dispatch(lab):
    from database import SessionLocal
    from models.plan_orchestration import PlanRun, PlanRunItem
    from services.task_scheduler import scheduler_tick, reconcile_runs

    schedule = await make_schedule(lab, "plan")
    run = await trigger(lab, schedule)
    assert run["planRunId"] and run["executionId"] is None
    with SessionLocal() as db:
        assert db.get(PlanRun, run["planRunId"])
        assert db.query(PlanRunItem).filter_by(run_id=run["planRunId"]).count() == 1
        await scheduler_tick(db)
    await until(lambda: bool(queue_states(lab["suite"]["id"])) and all(s in {"completed", "failed"} for s in queue_states(lab["suite"]["id"]).values()))
    with SessionLocal() as db:
        await scheduler_tick(db)
        assert db.get(TaskScheduleRun, run["id"]).status in {"completed", "failed"}
    assert len(queue_states(lab["suite"]["id"])) == 1


@pytest.mark.asyncio
async def test_parallel_due_claims_create_one_trigger(lab):
    import asyncio
    from concurrent.futures import ThreadPoolExecutor
    from database import SessionLocal
    from services.task_scheduler import enqueue_due, utc_now

    schedule = await make_schedule(lab, cron="* * * * *")
    now = utc_now()
    with SessionLocal() as db:
        row = db.get(TaskSchedule, schedule["id"])
        row.enabled, row.next_run_at = True, now - timedelta(minutes=1)
        db.commit()

    def compete():
        with SessionLocal() as db:
            return asyncio.run(enqueue_due(db, now))

    with ThreadPoolExecutor(max_workers=2) as workers:
        results = list(workers.map(lambda _: compete(), range(2)))
    assert sum(results) == 1
    assert len(queue_states(lab["suite"]["id"])) == 1


@pytest.mark.asyncio
async def test_disabled_executor_records_failure_without_running(lab):
    from database import SessionLocal
    from models import User
    from services.task_scheduler import enqueue_due, utc_now

    schedule = await make_schedule(lab, cron="* * * * *")
    now = utc_now()
    with SessionLocal() as db:
        row = db.get(TaskSchedule, schedule["id"])
        row.enabled, row.next_run_at = True, now - timedelta(minutes=1)
        db.get(User, row.created_by).status = False
        db.commit()
    with SessionLocal() as db:
        assert await enqueue_due(db, now) == 0
        record = db.query(TaskScheduleRun).filter_by(schedule_id=schedule["id"]).one()
        assert record.status == "failed" and record.error_message
        assert db.get(TaskSchedule, schedule["id"]).next_run_at > now
    assert queue_states(lab["suite"]["id"]) == {}


@pytest.mark.asyncio
async def test_offline_node_preserves_queue_then_resumes(lab):
    from database import SessionLocal
    from services.task_scheduler import scheduler_tick

    schedule = await make_schedule(lab)
    run = await trigger(lab, schedule)
    # 暂时移除隔离测试节点连接，实际套接字保持可用于恢复；没有替换执行结果。
    environment_id = lab["environment"]["id"]
    websocket = lab["manager"].active_connections.pop(environment_id)
    try:
        with SessionLocal() as db:
            await scheduler_tick(db)
        assert queue_states(lab["suite"]["id"])[run["executionId"]] == "pending"
    finally:
        lab["manager"].active_connections[environment_id] = websocket
    with SessionLocal() as db:
        await scheduler_tick(db)
    await until(lambda: queue_states(lab["suite"]["id"])[run["executionId"]] in {"completed", "failed"})
    assert len(queue_states(lab["suite"]["id"])) == 1


@pytest.mark.parametrize("failure_mode", ["false", "exception"])
@pytest.mark.asyncio
async def test_task_send_uncertainty_keeps_slot_and_never_replays(lab, monkeypatch, failure_mode):
    """Agent 已实际收到消息后注入本地失败，保持未知状态直到真实 ACK。"""
    from database import SessionLocal
    from models import TestSuiteExecution
    from models.task_queue import TaskQueue
    from services.task_scheduler import scheduler_tick
    original_send = lab["manager"].send_message
    attempts = []
    async def deliver_then_fail(environment_id, message):
        delivered = await original_send(environment_id, message)
        if message.get("type") != "execute_test_suite":
            return delivered
        attempts.append(message["execution_id"])
        assert delivered
        if failure_mode == "exception":
            raise ConnectionError("测试注入：节点已收到，本地连接随后异常")
        return False
    monkeypatch.setattr(lab["manager"], "send_message", deliver_then_fail)
    schedule = await make_schedule(lab)
    run = await trigger(lab, schedule)
    with SessionLocal() as db:
        await scheduler_tick(db)
        row = db.get(TaskScheduleRun, run["id"])
        assert row.status == "needs_confirmation" and row.delivery_state == "uncertain"
        assert db.query(TaskQueue).one().status == "running"
        await scheduler_tick(db)
        await scheduler_tick(db)
        assert len(attempts) == 1
    await until(lambda: queue_states(lab["suite"]["id"])[run["executionId"]] == "completed")
    with SessionLocal() as db:
        await scheduler_tick(db)
        assert db.get(TaskScheduleRun, run["id"]).status == "completed"
        assert db.query(TestSuiteExecution).count() == 4
        assert db.query(TaskQueue).count() == 1
    assert len(attempts) == 1
