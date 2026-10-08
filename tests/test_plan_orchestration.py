"""计划编排软件验收：仅隔离 SQLite 和消息替身，不连接真实台架。"""
from datetime import timedelta
import pytest
from database import SessionLocal
from models import User, Project, TestCase as Case, TestPlan as Plan, PlanCaseRelation, Environment, TestSuite as Suite
from models.plan_orchestration import PlanRun, PlanRunItem, PlanGroup
from models.task_queue import TaskQueue
from services.plan_orchestration import start_plan_run, advance_plan_runs, cancel_plan_run, save_policy, build_report, record_manual_result, resolve_uncertain_run
from services.suite_results import handle_run_result
from schemas.plan_orchestration import PlanPolicy, ManualResultInput
from utils.datetime_utils import beijing_now


@pytest.fixture
def plan_lab(monkeypatch):
    from api.v1.websocket import manager
    sent = []
    async def send(environment_id, message):
        sent.append((environment_id, message))
        return True
    monkeypatch.setattr(manager, "send_message", send)
    monkeypatch.setattr(manager, "active_connections", {"node": object()})
    with SessionLocal() as db:
        db.add(User(id="owner", username="计划负责人", email="plan@example.test", password_hash="不使用的测试密码"))
        db.flush()
        db.add(Project(id="project", name="隔离项目", owner_id="owner"))
        db.add(Environment(id="node", name="软件节点", max_concurrent_tasks=3, is_online=True))
        db.flush()
        db.add(Plan(id="plan", project_id="project", owner_id="owner", name="回归计划", plan_number="TP-001"))
        db.flush()
        for i in range(3):
            db.add(Case(id=f"case-{i}", project_id="project", name=f"用例 {i}", case_code=f"CODE-{i}", type="functional", steps=[], is_automated=i < 2, created_by="owner"))
        db.flush()
        for i in range(2):
            db.add(PlanCaseRelation(plan_id="plan", case_id=f"case-{i}", execution_order=i))
            db.add(Suite(id=f"suite-{i}", plan_id="plan", name=f"测试套 {i}", environment_id="node", execution_command="xat --mode offline", case_ids=[f"case-{i}"], created_by="owner"))
        db.commit()
        yield db, sent


def finish(db, item, result="passed"):
    assert handle_run_result(db, "node", dict(suite_id=item.suite_id, execution_id=item.execution_id,
                    case_id=item.suite_snapshot["caseIds"][0], result=result, duration="0.1s"))
    task = db.query(TaskQueue).filter_by(execution_id=item.execution_id).one()
    task.status = "completed" if result == "passed" else "failed"
    task.completed_at = beijing_now()
    db.commit()


@pytest.mark.asyncio
async def test_serial_real_queue_and_independent_history(plan_lab):
    db, sent = plan_lab
    run = await start_plan_run(db, "plan", "owner", idempotency_key="计划幂等")
    repeated = await start_plan_run(db, "plan", "owner", idempotency_key="计划幂等")
    assert repeated.id == run.id and db.query(PlanRun).count() == 1
    assert db.query(TaskQueue).count() == 1 and not sent
    await advance_plan_runs(db)
    assert len(sent) == 1 and sent[0][1]["case_codes"] == ["CODE-0"]
    items = db.query(PlanRunItem).filter_by(run_id=run.id).order_by(PlanRunItem.sequence).all()
    assert [i.status for i in items] == ["running", "waiting"]
    finish(db, items[0])
    await advance_plan_runs(db)
    assert len(sent) == 2 and items[1].status == "running"
    finish(db, items[1])
    await advance_plan_runs(db)
    assert run.status == "completed" and run.report["passRate"] == 100
    old_report = run.report.copy()
    new = await start_plan_run(db, "plan", "owner")
    await advance_plan_runs(db)
    new_item = db.query(PlanRunItem).filter_by(run_id=new.id, sequence=0).one()
    finish(db, new_item, "failed")
    await advance_plan_runs(db)
    assert run.report == old_report and run.report["counts"]["failed"] == 0


@pytest.mark.asyncio
async def test_failure_stop_and_policy_snapshot(plan_lab):
    db, sent = plan_lab
    save_policy(db, "plan", PlanPolicy(stopOnFailure=True))
    run = await start_plan_run(db, "plan", "owner")
    save_policy(db, "plan", PlanPolicy(executionMode="parallel", stopOnFailure=False, passThreshold=0))
    await advance_plan_runs(db)
    first = db.query(PlanRunItem).filter_by(run_id=run.id, sequence=0).one()
    finish(db, first, "failed")
    await advance_plan_runs(db)
    assert len(sent) == 1 and run.status == "failed"
    assert run.report["counts"]["skipped"] == 1 and run.report["counts"]["failed"] == 1
    assert run.config_snapshot["passThreshold"] == 100


@pytest.mark.asyncio
async def test_parallel_obeys_node_capacity_and_threshold(plan_lab):
    db, sent = plan_lab
    db.get(Environment, "node").max_concurrent_tasks = 1
    db.commit()
    save_policy(db, "plan", PlanPolicy(executionMode="parallel", passThreshold=50))
    run = await start_plan_run(db, "plan", "owner")
    await advance_plan_runs(db)
    assert len(sent) == 1
    first, second = db.query(PlanRunItem).filter_by(run_id=run.id).order_by(PlanRunItem.sequence).all()
    finish(db, first, "failed")
    await advance_plan_runs(db)
    assert len(sent) == 2
    finish(db, second)
    await advance_plan_runs(db)
    assert run.status == "completed" and run.report["passRate"] == 50


@pytest.mark.asyncio
async def test_cancel_keeps_slot_until_agent_ack(plan_lab):
    db, sent = plan_lab
    run = await start_plan_run(db, "plan", "owner")
    await advance_plan_runs(db)
    await cancel_plan_run(db, run.id, "owner")
    assert run.status == "cancelling"
    task = db.query(TaskQueue).one()
    assert task.status == "running" and sent[-1][1]["type"] == "cancel_test_suite"
    task.status = "cancelled"
    db.commit()
    await advance_plan_runs(db)
    assert run.status == "cancelled" and run.report["outcome"] == "cancelled"
    assert run.report["counts"]["cancelled"] == 2


@pytest.mark.asyncio
async def test_manual_batch_does_not_inherit_old_result(plan_lab):
    db, sent = plan_lab
    db.query(Suite).delete()
    db.query(PlanCaseRelation).delete()
    db.add(PlanCaseRelation(plan_id="plan", case_id="case-2", execution_status="pass"))
    db.commit()
    run = await start_plan_run(db, "plan", "owner")
    assert build_report(db, run)["counts"]["pending"] == 1
    record_manual_result(db, run.id, "case-2", ManualResultInput(result="failed", notes="实际结果不符"), "owner")
    await advance_plan_runs(db)
    assert run.status == "failed" and run.report["cases"][0]["notes"] == "实际结果不符"
    assert not sent and db.query(TaskQueue).count() == 0
    with pytest.raises(ValueError):
        record_manual_result(db, run.id, "case-2", ManualResultInput(result="passed"), "owner")


@pytest.mark.asyncio
async def test_dispatch_uncertainty_never_replays(plan_lab):
    db, sent = plan_lab
    run = await start_plan_run(db, "plan", "owner")
    await advance_plan_runs(db)
    item = db.query(PlanRunItem).filter_by(run_id=run.id, sequence=0).one()
    item.delivery_state = "dispatching"
    item.dispatch_attempted_at = beijing_now() - timedelta(seconds=40)
    db.commit()
    await advance_plan_runs(db)
    assert run.status == "needs_confirmation" and len(sent) == 1
    assert db.query(TaskQueue).one().status == "running"
    resolve_uncertain_run(db, run.id, "owner")
    assert run.status == "failed" and db.query(TaskQueue).one().status == "failed"


@pytest.mark.asyncio
async def test_suite_snapshot_is_locked_while_waiting(plan_lab):
    from services.test_suite_service import TestSuiteService
    db, sent = plan_lab
    await start_plan_run(db, "plan", "owner")
    with pytest.raises(ValueError, match="排队或执行"):
        TestSuiteService.require_idle(db, "suite-1")
    with pytest.raises(ValueError, match="已有执行中的批次"):
        await start_plan_run(db, "plan", "owner")


def test_group_and_policy_reject_cross_project(plan_lab):
    db, sent = plan_lab
    db.add(Project(id="other", name="其他项目", owner_id="owner"))
    db.flush()
    db.add(PlanGroup(id="foreign-group", project_id="other", name="外部组"))
    db.commit()
    with pytest.raises(ValueError, match="不属于当前项目"):
        save_policy(db, "plan", PlanPolicy(groupId="foreign-group"))
    with pytest.raises(ValueError, match="不重复的测试套"):
        save_policy(db, "plan", PlanPolicy(suiteOrder=["suite-0", "suite-0"]))


@pytest.mark.asyncio
async def test_http_groups_history_logs_and_project_isolation(plan_lab):
    from fastapi import FastAPI
    import httpx
    from api.v1.test_plans import router as old_router
    from api.v1.plan_orchestration import router as new_router
    from api.deps import get_current_user
    from database import get_db
    from models.test_suite import TestSuiteLog
    db, sent = plan_lab
    db.add(User(id="outsider", username="无权限用户", email="outsider@example.test", password_hash="测试替身"))
    db.commit()
    app = FastAPI()
    app.include_router(old_router, prefix="/test-plans")
    app.include_router(new_router, prefix="/plan-orchestration")
    app.dependency_overrides[get_db] = lambda: db
    identity = {"id": "owner"}
    app.dependency_overrides[get_current_user] = lambda: db.get(User, identity["id"])
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        group_response = await client.post("/plan-orchestration/projects/project/groups", json={"name": "发布回归"})
        assert group_response.status_code == 200, group_response.text
        group_id = group_response.json()["data"]["id"]
        assert (await client.put("/plan-orchestration/plans/plan/settings", json={"groupId": group_id})).status_code == 200
        grouped = await client.get("/test-plans", params={"project_id": "project", "group_id": group_id})
        assert grouped.status_code == 200 and grouped.json()["data"]["total"] == 1
        response = await client.post("/test-plans/plan/execute", json={"notes": "接口触发"})
        assert response.status_code == 200, response.text
        run_id = response.json()["data"]["id"]
        assert (await client.post("/test-plans/plan/execute", json={})).status_code == 409
        history = await client.get("/test-plans/plan/executions")
        assert history.json()["data"]["total"] == 1
        item = db.query(PlanRunItem).filter_by(run_id=run_id, sequence=0).one()
        db.add(TestSuiteLog(suite_id=item.suite_id, execution_id=item.execution_id, message="该批次的真实日志"))
        db.add(TestSuiteLog(suite_id=item.suite_id, execution_id="other-execution", message="不属于该批次"))
        db.commit()
        log_response = await client.get(f"/test-plans/plan/executions/{run_id}/logs")
        assert "该批次的真实日志" in log_response.text and "不属于该批次" not in log_response.text
        assert (await client.delete(f"/plan-orchestration/groups/{group_id}")).status_code == 200
        assert db.get(Plan, "plan") is not None
        identity["id"] = "outsider"
        for path in [f"/plan-orchestration/runs/{run_id}", f"/plan-orchestration/runs/{run_id}/logs", f"/test-plans/plan/executions/{run_id}/logs", "/test-plans/plan/executions", "/test-plans?project_id=project", "/plan-orchestration/projects/project/groups"]:
            denied = await client.get(path)
            assert denied.status_code == 403, (path, denied.text)
        assert (await client.post("/test-plans/plan/stop")).status_code == 403
        assert (await client.put("/plan-orchestration/plans/plan/settings", json={})).status_code == 403


@pytest.mark.asyncio
async def test_offline_disabled_and_legacy_dispatch_cannot_bypass_policy(plan_lab, monkeypatch):
    from api.v1.websocket import manager
    from services.task_queue_service import TaskQueueService
    db, sent = plan_lab
    run = await start_plan_run(db, "plan", "owner")
    db.get(Environment, "node").status = False
    db.commit()
    await advance_plan_runs(db)
    assert not sent and run.status == "queued"
    db.get(Environment, "node").status = True
    db.commit()
    monkeypatch.setattr(manager, "active_connections", {})
    await advance_plan_runs(db)
    assert not sent
    assert TaskQueueService.get_next_pending_task(db, "node") is None
    monkeypatch.setattr(manager, "active_connections", {"node": object()})
    await advance_plan_runs(db)
    assert len(sent) == 1


@pytest.mark.asyncio
async def test_missing_case_results_fail_instead_of_false_success(plan_lab):
    db, sent = plan_lab
    run = await start_plan_run(db, "plan", "owner", suite_ids=["suite-0"])
    await advance_plan_runs(db)
    task = db.query(TaskQueue).one()
    task.status = "completed"
    db.commit()
    await advance_plan_runs(db)
    assert run.status == "failed" and run.report["counts"]["error"] == 1
    assert run.report["passRate"] == 0


from test_http_agent_e2e import lab, until, queue_states


@pytest.mark.asyncio
async def test_plan_http_agent_xat_real_report(lab):
    """真实 HTTP → 计划批次 → WebSocket → Agent → XAT → 独立报告。"""
    client = lab["client"]
    plan_id = lab["plan"]["id"]
    response = await client.post(f"/api/v1/test-plans/{plan_id}/execute", json={"notes": "纯软件端到端"})
    assert response.status_code == 200, response.text
    run_id = response.json()["data"]["id"]
    with SessionLocal() as db:
        await advance_plan_runs(db)
    await until(lambda: bool(queue_states(lab["suite"]["id"])) and set(queue_states(lab["suite"]["id"]).values()) == {"completed"})
    with SessionLocal() as db:
        await advance_plan_runs(db)
    report_response = await client.get(f"/api/v1/plan-orchestration/runs/{run_id}")
    assert report_response.status_code == 200, report_response.text
    run = report_response.json()["data"]
    assert run["status"] == "completed" and run["report"]["counts"]["passed"] == 4
    assert {r["caseId"] for r in run["report"]["cases"]} == {c["id"] for c in lab["cases"]}
    logs = await client.get(f"/api/v1/plan-orchestration/runs/{run_id}/logs")
    assert "XAT测试框架启动" in logs.text
    history = await client.get(f"/api/v1/test-plans/{plan_id}/executions")
    assert history.json()["data"]["total"] == 1
    print("计划端到端验收通过：真实 Agent 完成 4 条软件用例，报告与日志按执行批次准确关联")


@pytest.mark.parametrize("change", ["disabled", "revoked"])
@pytest.mark.asyncio
async def test_plan_dispatch_rechecks_executor_permission(plan_lab, change):
    db, sent = plan_lab
    run = await start_plan_run(db, "plan", "owner")
    if change == "disabled":
        db.get(User, "owner").status = False
    else:
        db.add(User(id="new-owner", username="新负责人", email="new-owner@example.test", password_hash="测试替身"))
        db.flush()
        db.get(Project, "project").owner_id = "new-owner"
    db.commit()
    await advance_plan_runs(db)
    assert not sent
    assert db.query(TaskQueue).filter_by(status="running").count() == 0
    item = db.query(PlanRunItem).filter_by(run_id=run.id, sequence=0).one()
    assert item.status == "failed" and "权限" in item.error_message


@pytest.mark.asyncio
async def test_cancel_pending_cas_does_not_overwrite_concurrent_dispatch(plan_lab, monkeypatch):
    from sqlalchemy.orm import Query
    db, sent = plan_lab
    run = await start_plan_run(db, "plan", "owner")
    original = Query.update
    raced = {"done": False}
    def race_claim(query, values, *args, **kwargs):
        if (not raced["done"] and query.column_descriptions[0]["entity"] is TaskQueue
                and values.get("status") == "cancelled"):
            raced["done"] = True
            with SessionLocal() as other:
                original(other.query(TaskQueue).filter_by(status="pending"), {"status": "running"})
                other.commit()
        return original(query, values, *args, **kwargs)
    monkeypatch.setattr(Query, "update", race_claim)
    await cancel_plan_run(db, run.id, "owner")
    assert raced["done"] and db.query(TaskQueue).one().status == "running"
    assert run.status == "cancelling" and sent[-1][1]["type"] == "cancel_test_suite"


@pytest.mark.asyncio
async def test_concurrent_manual_results_merge_without_lost_update(plan_lab):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier, local
    from sqlalchemy import event
    from database import engine
    db, sent = plan_lab
    db.query(Suite).delete()
    db.query(PlanCaseRelation).delete()
    db.add(Case(id="case-3", project_id="project", name="第二条手工用例", case_code="CODE-3", type="functional", steps=[], is_automated=False, created_by="owner"))
    db.flush()
    for cid in ["case-2", "case-3"]:
        db.add(PlanCaseRelation(plan_id="plan", case_id=cid))
    db.commit()
    run_id = (await start_plan_run(db, "plan", "owner")).id
    barrier, per_thread = Barrier(2), local()
    def after_read(conn, cursor, statement, parameters, context, executemany):
        # Both requests first observe the same revision. Current authority
        # locking may serialize them before UPDATE; do not put a barrier
        # inside that serialized region.
        if statement.startswith("SELECT ") and "FROM plan_runs" in statement and not getattr(per_thread, "waited", False):
            per_thread.waited = True
            barrier.wait(timeout=5)
    event.listen(engine, "after_cursor_execute", after_read)
    def record(cid):
        with SessionLocal() as session:
            record_manual_result(session, run_id, cid, ManualResultInput(result="passed", notes=cid), "owner")
    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(record, cid) for cid in ["case-2", "case-3"]]
            for future in futures:
                future.result(timeout=15)
    finally:
        event.remove(engine, "after_cursor_execute", after_read)
    db.expire_all()
    result = db.get(PlanRun, run_id)
    assert set(result.manual_results) == {"case-2", "case-3"}
    assert result.manual_revision == 2


@pytest.mark.asyncio
async def test_empty_new_tables_do_not_dispatch_legacy_pending_task(plan_lab):
    """升级后新增表为空，新的调度循环不能意外消费旧台架队列。"""
    from services.task_scheduler import scheduler_tick
    db, sent = plan_lab
    db.get(Suite, "suite-0").execution_command = "xat --mode hardware"
    db.add(TaskQueue(id="legacy-task", suite_id="suite-0", environment_id="node",
                     execution_id="legacy-execution", executor_id="owner", status="pending"))
    db.commit()
    await scheduler_tick(db)
    assert sent == []
    assert db.get(TaskQueue, "legacy-task").status == "pending"


@pytest.mark.parametrize("failure_mode", ["false", "exception"])
@pytest.mark.asyncio
async def test_plan_send_uncertainty_keeps_slot_and_never_replays(lab, monkeypatch, failure_mode):
    """消息真实交付后注入本地发送失败，证明不能依据 False 重发。"""
    from models.test_suite import TestSuiteExecution
    manager = lab["manager"]
    original_send = manager.send_message
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
    monkeypatch.setattr(manager, "send_message", deliver_then_fail)
    response = await lab["client"].post(f'/api/v1/test-plans/{lab["plan"]["id"]}/execute', json={})
    assert response.status_code == 200, response.text
    run_id = response.json()["data"]["id"]
    with SessionLocal() as db:
        await advance_plan_runs(db)
        run = db.get(PlanRun, run_id)
        item = db.query(PlanRunItem).filter_by(run_id=run_id).one()
        assert run.status == item.status == "needs_confirmation"
        assert item.delivery_state == "uncertain"
        assert db.query(TaskQueue).one().status == "running"
        await advance_plan_runs(db)
        await advance_plan_runs(db)
        assert len(attempts) == 1
    await until(lambda: set(queue_states(lab["suite"]["id"]).values()) == {"completed"})
    with SessionLocal() as db:
        await advance_plan_runs(db)
        assert db.get(PlanRun, run_id).status == "completed"
        assert db.query(TestSuiteExecution).count() == 4
        assert db.query(TaskQueue).count() == 1
    assert len(attempts) == 1


@pytest.mark.asyncio
async def test_text_manual_result_uses_frozen_description_not_hidden_steps(plan_lab):
    """文本用例不要求回填保留的步骤草稿，并冻结文本内容。"""
    db, sent = plan_lab
    case = db.get(Case, 'case-2')
    case.case_edit_type = 'TEXT'
    case.text_description = '<p>冻结文本说明</p>'
    case.expected_result = '<p>文本预期</p>'
    case.description = '冻结备注'
    case.steps = [{'step':1,'action':'隐藏的步骤草稿','expected':'草稿预期'}]
    db.add(PlanCaseRelation(plan_id='plan',case_id=case.id,execution_order=2))
    db.commit()
    run = await start_plan_run(db,'plan','owner')
    frozen = next(item for item in run.case_snapshot if item['id'] == case.id)
    assert frozen['snapshot']['text_description'] == '<p>冻结文本说明</p>'
    case.text_description = '后续编辑'
    db.commit()
    record_manual_result(db,run.id,case.id,ManualResultInput(result='passed',notes='文本验收通过'),'owner')
    assert run.manual_results[case.id]['result'] == 'passed'
    assert run.manual_results[case.id]['stepResults'] == []
    assert next(item for item in build_report(db,run)['cases'] if item['caseId'] == case.id)['snapshot']['text_description'] == '<p>冻结文本说明</p>'
