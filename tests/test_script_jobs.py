"""Formal script semantics, authorization, immutable runs and migration boundaries."""
import asyncio
import json
import time
import uuid
from types import SimpleNamespace
import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine, inspect, text
from models import Environment, User, TaskQueue, TestSuiteExecution as SuiteExecution, TestExecution as CaseExecution
from models.script_job import ScriptJobRun, ScriptJobLog
from models.agent_log import AgentLogCursor
from schemas.script_job import ScriptJobCreate, ScriptJobConfig, ResolveScriptJob
from services import script_jobs as jobs
from services.agent_log_ingest import persist_log_batch
from services.raw_log_export import export_log_chunk, LogExportRequest
from test_plan_orchestration import plan_lab
from test_agent_capacity_admission import make_agent


@pytest.fixture
def script_lab(plan_lab, monkeypatch):
    from api.v1.websocket import manager
    db, _ = plan_lab
    node = db.get(Environment, "node"); node.created_by = "owner"; node.max_concurrent_tasks = 1
    db.commit()
    sent = []
    socket = object()
    session = SimpleNamespace(environment_id="node", websocket=socket, protocol_version=2,
        capabilities=frozenset({"script_jobs_v1"}), auth_received=True, last_seen=time.monotonic(), session_id="session-A")
    monkeypatch.setattr(manager, "sessions", {"node": session})
    monkeypatch.setattr(manager, "active_connections", {"node": socket})
    async def send(target, message):
        sent.append((target, message)); return True
    monkeypatch.setattr(manager, "send_session", send)
    return db, db.get(User, "owner"), manager, session, sent


def definition(**changes):
    return dict(projectId="project", name="plain", environmentId="node", mode="python",
                script="print('hello')", command="", args=[], workDir="", timeoutSeconds=5, **changes)


def create(lab):
    return jobs.create_job(lab[0], lab[1], ScriptJobCreate(**definition()))


def terminal(run, **changes):
    return dict(script_job_id=run.job_id, execution_id=run.execution_id,
                result="success", exit_code=0, duration_seconds=0.01, **changes)


@pytest.mark.asyncio
async def test_plain_job_is_frozen_idempotent_and_has_no_case_reports(script_lab):
    db, user, _, session, sent = script_lab
    job = create(script_lab)
    run = await jobs.trigger(db, user, job.id, "request")
    assert run.delivery_state == "sent" and sent[0][0] is session
    update = ScriptJobConfig(**{k:v for k,v in definition().items() if k != "projectId"})
    update.script = "print('new')"
    jobs.update_job(db, user, job.id, update)
    replay = await jobs.trigger(db, user, job.id, "request")
    assert replay.execution_id == run.execution_id and len(sent) == 1
    assert run.config_snapshot["script"] == "print('hello')" and run.config_snapshot["revision"] == 1
    assert jobs.complete(db, "node", terminal(run))
    assert jobs.complete(db, "node", terminal(run))
    assert jobs.run_json(db, run)["status"] == "completed"
    assert not db.query(SuiteExecution).count() and not db.query(CaseExecution).count()
    assert db.query(TaskQueue).one().suite_id is None


@pytest.mark.asyncio
async def test_offline_pending_cancel_and_unsupported_node(script_lab):
    db, user, manager, session, sent = script_lab
    job = create(script_lab)
    manager.active_connections.clear()
    run = await jobs.trigger(db, user, job.id, "offline")
    assert jobs.run_json(db, run)["status"] == "pending" and not sent
    await jobs.cancel(db, user, job.id, run.execution_id)
    assert jobs.run_json(db, run)["status"] == "cancelled"
    manager.active_connections["node"] = session.websocket
    session.capabilities = frozenset()
    with pytest.raises(HTTPException) as error:
        await jobs.trigger(db, user, job.id, "old-agent")
    assert error.value.status_code == 409
    assert db.query(TaskQueue).count() == 1


@pytest.mark.asyncio
async def test_pending_snapshot_dispatch_rechecks_owner(script_lab):
    from services.queued_dispatch import dispatch_pending_suites
    db, user, manager, session, sent = script_lab
    job = create(script_lab)
    manager.active_connections.clear()
    run = await jobs.trigger(db, user, job.id, "queued")
    db.get(Environment, "node").created_by = "other"; db.commit()
    manager.active_connections["node"] = session.websocket
    await dispatch_pending_suites(db, "node")
    assert not sent and jobs.run_json(db, run)["status"] == "failed"


@pytest.mark.asyncio
async def test_unsupported_pending_script_does_not_block_suite(script_lab):
    from services.queued_dispatch import dispatch_pending_suites
    from services.task_queue_service import TaskQueueService
    db, user, manager, session, sent = script_lab
    job = create(script_lab)
    manager.active_connections.clear()
    run = await jobs.trigger(db, user, job.id, "queue-script")
    TaskQueueService.add_to_queue(db, "node", "suite-0", "suite-exec", "owner")
    manager.active_connections["node"] = session.websocket
    session.capabilities = frozenset()
    await dispatch_pending_suites(db, "node")
    assert db.query(TaskQueue).filter_by(execution_id="suite-exec").one().status == "running"
    assert jobs.run_json(db, run)["status"] == "pending"


@pytest.mark.asyncio
async def test_unknown_requires_strict_manual_confirmation(script_lab, monkeypatch):
    db, user, manager, _, _ = script_lab
    job = create(script_lab)
    async def uncertain(*args): return False
    monkeypatch.setattr(manager, "send_session", uncertain)
    run = await jobs.trigger(db, user, job.id, "unknown")
    assert run.delivery_state == "unknown"
    with pytest.raises(HTTPException):
        jobs.resolve(db, user, job.id, run.execution_id, ResolveScriptJob(confirmedStopped=False))
    assert jobs.run_json(db, run)["status"] == "running"
    jobs.resolve(db, user, job.id, run.execution_id, ResolveScriptJob(confirmedStopped=True, reason="local process stopped"))
    assert run.result == "unknown" and run.exit_code is None
    assert jobs.complete(db, "node", terminal(run))
    assert run.result == "unknown" and jobs.run_json(db, run)["status"] == "failed"
    jobs.resolve(db, user, job.id, run.execution_id, ResolveScriptJob(confirmedStopped=True))
    second = await jobs.trigger(db, user, job.id, "new-id")
    assert second.execution_id != run.execution_id


@pytest.mark.asyncio
async def test_cancel_failed_send_cannot_overwrite_concurrent_terminal(script_lab, monkeypatch):
    db, user, manager, _, _ = script_lab
    run = await jobs.trigger(db, user, create(script_lab).id, "cancel-race")
    async def racing(*args):
        assert jobs.complete(db, "node", terminal(run))
        return False
    monkeypatch.setattr(manager, "send_session", racing)
    await jobs.cancel(db, user, run.job_id, run.execution_id)
    assert run.result == "success" and run.delivery_state == "terminal"


@pytest.mark.asyncio
async def test_script_logs_share_cursor_replay_atomicity_and_export(script_lab):
    db, user, _, _, _ = script_lab
    run = await jobs.trigger(db, user, create(script_lab).id, "logs")
    stream = str(uuid.uuid4())
    payload = dict(type="script_job_log", script_job_id=run.job_id, execution_id=run.execution_id,
                   message="原始 😀\r\n  ", raw=True)
    message = dict(stream_id=stream, records=[dict(sequence=1, payload=payload)])
    assert persist_log_batch(db, "foreign-node", message)[0]["type"] == "log_batch_nack"
    assert not db.query(AgentLogCursor).count()
    response, delta = persist_log_batch(db, "node", message)
    assert response["through_sequence"] == 1 and delta[0][0] == "script:" + run.execution_id
    persist_log_batch(db, "node", message)
    assert db.query(ScriptJobLog).one().message == payload["message"]
    invalid = dict(payload, execution_id="foreign")
    rejected = dict(stream_id=stream, records=[dict(sequence=2, payload=payload), dict(sequence=3, payload=invalid)])
    assert persist_log_batch(db, "node", rejected)[0]["type"] == "log_batch_nack"
    assert db.query(AgentLogCursor).one().through_sequence == 1
    assert db.query(ScriptJobLog).one().message == payload["message"]
    chunk = export_log_chunk(db.query(ScriptJobLog), "script:" + run.execution_id, user.id, LogExportRequest(),
                             model=ScriptJobLog, subject="script_job_id", label="job")
    assert chunk["complete"] and payload["message"] in chunk["content"] and "[job=" in chunk["content"]


@pytest.mark.parametrize("bad", [True, 0, float("inf"), float("nan"), -1])
def test_invalid_deadline_rejected(bad):
    data = definition(); data["timeoutSeconds"] = bad
    with pytest.raises(ValueError): ScriptJobCreate(**data)


@pytest.mark.asyncio
async def test_script_agent_exact_args_tombstone_and_restart_unknown(sat_config):
    agent, events = make_agent(sat_config)
    agent.ws_client.server_capabilities = {"script_jobs_v1"}
    agent.ws_client.session_id = "same-session"
    source = "import sys; print(repr(sys.argv[1:]))"
    msg = dict(script_job_id="job", execution_id="exec", dispatch_session_id="same-session", config={**definition(), "script":source,"args":["a b", "", "$literal"]})
    assert agent.script_job_runner.start(msg)
    await asyncio.gather(*agent.script_job_runner.runs.values())
    assert any("['a b', '', '$literal']" in e.get("message", "") for e in events)
    assert any(e.get("result") == "success" for e in events)
    assert not agent.script_job_runner.start(msg)
    agent.ws_client.session_id = "same-session"
    await agent.script_job_runner.cancel("job", "cancel-before", "same-session")
    assert not agent.script_job_runner.start(dict(msg, execution_id="cancel-before"))
    agent.execution_admission.register("lost")
    agent.execution_admission.release("lost")
    await agent.script_job_runner.cancel("job", "lost")
    assert events[-1]["type"] == "script_job_state" and events[-1]["state"] == "unknown"


@pytest.mark.asyncio
async def test_cancel_immediately_after_agent_admission_never_starts(sat_config):
    agent, events = make_agent(sat_config)
    agent.ws_client.server_capabilities = {"script_jobs_v1"}
    agent.ws_client.session_id = "same-session"
    message = dict(script_job_id="job", execution_id="fast-cancel", dispatch_session_id="same-session", config=definition())
    agent.script_job_runner.start(message)
    await agent.script_job_runner.cancel("job", "fast-cancel")
    assert not any(e.get("type") == "script_job_log" for e in events)
    assert events[-1]["result"] == "cancelled"


def test_existing_sqlite_migration_aborts_before_any_ddl(tmp_path):
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location("upgrade_script_jobs", Path(__file__).resolve().parents[1] / "scripts/upgrade_script_jobs.py")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    upgrade = module.upgrade
    engine = create_engine("sqlite:///" + str(tmp_path / "legacy.sqlite"))
    with engine.begin() as connection:
        for name in ("users", "projects", "environments", "test_suites"):
            connection.execute(text(f"CREATE TABLE {name} (id VARCHAR(36) PRIMARY KEY)"))
        connection.execute(text("CREATE TABLE task_queue (id VARCHAR(36), suite_id VARCHAR(36) NOT NULL)"))
        connection.execute(text("INSERT INTO task_queue VALUES ('keep', 'suite')"))
    before = inspect(engine).get_table_names()
    with pytest.raises(RuntimeError, match="禁止重建"):
        upgrade(engine, apply=True)
    assert inspect(engine).get_table_names() == before
    with engine.connect() as connection:
        assert connection.execute(text("SELECT * FROM task_queue")).all() == [("keep", "suite")]


@pytest.mark.asyncio
async def test_new_empty_agent_cannot_cancel_previous_session_execution(sat_config):
    agent, events = make_agent(sat_config)
    agent.ws_client.session_id = "replacement-session"
    agent.ws_client.server_capabilities = {"script_jobs_v1"}
    await agent.script_job_runner.cancel("job", "missing-from-new-disk", "old-session")
    assert events[-1]["type"] == "script_job_state" and events[-1]["state"] == "unknown"
    assert not agent.execution_admission._marker("missing-from-new-disk").exists()
    assert not any(event.get("type") == "script_job_completed" for event in events)
    assert not agent.script_job_runner.start(dict(script_job_id="job", execution_id="stale-dispatch",
        dispatch_session_id="old-session", config=definition()))


@pytest.mark.asyncio
async def test_queue_freezes_old_node_and_rechecks_current_project_permission(script_lab):
    from services.queued_dispatch import dispatch_pending_suites
    from models import Project
    db, user, manager, session, sent = script_lab
    job = create(script_lab)
    manager.active_connections.clear()
    run = await jobs.trigger(db, user, job.id, "frozen-queue")
    db.add(Environment(id="new-node", name="new", created_by="owner")); db.commit()
    changed = {k:v for k,v in definition().items() if k != "projectId"}
    changed.update(environmentId="new-node", script="print('edited')")
    jobs.update_job(db, user, job.id, ScriptJobConfig(**changed))
    manager.active_connections["node"] = session.websocket
    await dispatch_pending_suites(db, "node")
    assert sent[0][1]["config"]["environmentId"] == "node"
    assert sent[0][1]["config"]["script"] == "print('hello')"
    assert run.environment_id == "node"
    assert jobs.complete(db, "node", terminal(run))
    job.environment_id = "node"; job.config = definition(); db.commit()
    manager.active_connections.clear()
    revoked = await jobs.trigger(db, user, job.id, "revoked-project")
    db.get(Project, "project").owner_id = "other"; db.commit()
    manager.active_connections["node"] = session.websocket
    await dispatch_pending_suites(db, "node")
    assert jobs.run_json(db, revoked)["status"] == "failed" and len(sent) == 1


@pytest.mark.asyncio
async def test_running_manual_close_rejected_and_cross_node_result_rejected(script_lab):
    db, user, _, _, _ = script_lab
    run = await jobs.trigger(db, user, create(script_lab).id, "protected")
    with pytest.raises(HTTPException) as raised:
        jobs.resolve(db, user, run.job_id, run.execution_id, ResolveScriptJob(confirmedStopped=True))
    assert raised.value.status_code == 409
    assert not jobs.complete(db, "other-node", terminal(run))
    assert not jobs.complete(db, "node", {**terminal(run), "exit_code":7})
    assert jobs.run_json(db, run)["status"] == "running"


@pytest.mark.asyncio
async def test_backend_restart_marks_reserved_script_unknown_without_release(script_lab):
    db, user, manager, _, _ = script_lab
    run = await jobs.trigger(db, user, create(script_lab).id, "restart")
    manager.reset_online_status(); db.refresh(run)
    assert run.delivery_state == "unknown" and jobs.run_json(db, run)["status"] == "running"


def test_fresh_schema_migration_is_noop_and_missing_indexes_are_repaired():
    import importlib.util
    from pathlib import Path
    from database import engine
    spec = importlib.util.spec_from_file_location("upgrade_script_jobs", Path(__file__).resolve().parents[1] / "scripts/upgrade_script_jobs.py")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    assert module.upgrade(engine) == []
    with engine.begin() as connection:
        connection.execute(text("DROP INDEX ix_script_jobs_project_id"))
    assert any("ix_script_jobs_project_id" in sql for _, sql in module.upgrade(engine))
    module.upgrade(engine, apply=True)
    assert module.upgrade(engine) == []


@pytest.mark.asyncio
async def test_mixed_suite_script_batch_has_one_cursor_and_atomic_rollback(script_lab):
    from services.task_queue_service import TaskQueueService
    from models.test_suite import TestSuiteLog
    db, user, _, _, _ = script_lab
    run = await jobs.trigger(db, user, create(script_lab).id, "mixed")
    TaskQueueService.add_to_queue(db, "node", "suite-0", "suite-log-exec", "owner")
    suite = dict(type="test_suite_log", suite_id="suite-0", execution_id="suite-log-exec", message="suite raw", raw=True)
    script = dict(type="script_job_log", script_job_id=run.job_id, execution_id=run.execution_id, message="script raw", raw=True)
    batch = dict(stream_id=str(uuid.uuid4()), records=[dict(sequence=1,payload=suite),dict(sequence=2,payload=script)])
    assert persist_log_batch(db, "node", batch)[0]["through_sequence"] == 2
    assert db.query(AgentLogCursor).count() == 1
    assert db.query(TestSuiteLog).one().message == "suite raw"
    assert db.query(ScriptJobLog).one().message == "script raw"
    bad = dict(stream_id=batch["stream_id"], records=[dict(sequence=3,payload=script),dict(sequence=4,payload={**suite,"suite_id":"wrong"})])
    assert persist_log_batch(db,"node",bad)[0]["type"] == "log_batch_nack"
    assert db.query(AgentLogCursor).one().through_sequence == 2
    assert db.query(ScriptJobLog).one().message == "script raw"


@pytest.mark.asyncio
async def test_unfinished_auth_does_not_claim_script_capacity(script_lab):
    from services.queued_dispatch import dispatch_pending_suites
    from api.v1.script_jobs import nodes
    db, user, _, session, sent = script_lab
    session.auth_received = False
    assert not jobs.capable(session, script_lab[2])
    assert nodes("project", db, user).data["items"][0]["isOnline"] is False
    run = await jobs.trigger(db, user, create(script_lab).id, "auth-pending")
    assert jobs.run_json(db, run)["status"] == "pending" and not sent
    session.auth_received = True
    await dispatch_pending_suites(db, "node")
    assert jobs.run_json(db, run)["status"] == "running" and len(sent) == 1
