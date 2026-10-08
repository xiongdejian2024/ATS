"""Fault-injected controller transport and transaction boundaries for script jobs."""
import uuid
import pytest
from sqlalchemy.orm import Session
from test_agent_session_fencing import controller, Socket
from test_http_agent_e2e import until
from database import SessionLocal
from models import User, Project, Environment, TaskQueue
from models.script_job import ScriptJob, ScriptJobRun
from schemas.script_job import ScriptJobCreate
from services import script_jobs as jobs
from utils.datetime_utils import beijing_now


def seed(session):
    with SessionLocal() as db:
        db.add(User(id='review-owner', username='review-owner', email='review@example.test', password_hash='unused'))
        db.flush()
        db.add(Project(id='review-project', name='review-project', owner_id='review-owner'))
        db.get(Environment, 'node').created_by = 'review-owner'
        db.commit()
        user=db.get(User, 'review-owner')
        job=jobs.create_job(db, user, ScriptJobCreate(projectId='review-project', name='review', environmentId='node', mode='python', script='pass', timeoutSeconds=1))
        now=beijing_now()
        run=ScriptJobRun(execution_id='review-execution', job_id=job.id, project_id=job.project_id, environment_id='node', executor_id=user.id, request_id='review-request', config_snapshot=job.config, dispatch_session_id=session.session_id, delivery_state='sent', created_at=now)
        db.add(run)
        db.add(TaskQueue(id='review-task', kind='script', script_job_id=job.id, environment_id='node', execution_id=run.execution_id, executor_id=user.id, status='running', started_at=now))
        db.commit()
        return job.id

async def auth(socket, session):
    socket.frame({'type':'auth', 'capabilities':['script_jobs_v1', 'log_batch_v1']}, session)
    await until(lambda: session.auth_received)


def completion(job_id):
    return dict(type='script_job_completed', script_job_id=job_id, execution_id='review-execution', result='success', exit_code=0, duration_seconds=.1, event_id=str(uuid.uuid5(uuid.NAMESPACE_URL,'review-execution:completed')))


def state():
    with SessionLocal() as db:
        run=db.get(ScriptJobRun, 'review-execution')
        task=db.query(TaskQueue).filter_by(execution_id='review-execution').one()
        return run.result, run.delivery_state, task.status, db.query(ScriptJobRun).count()

@pytest.mark.asyncio
async def test_commit_failure_has_no_ack_and_replays_once(controller, monkeypatch):
    _, _, connect=controller
    old, session, old_task=await connect()
    await auth(old, session)
    job_id=seed(session)
    original=jobs.complete
    def fail_commit(db, environment_id, message):
        commit=db.commit
        def failure(): raise RuntimeError('injected commit failure')
        db.commit=failure
        try: return original(db, environment_id, message)
        finally: db.commit=commit
    monkeypatch.setattr(jobs, 'complete', fail_commit)
    old.frame(completion(job_id), session)
    await old_task
    assert not any(p['type']=='sat_event_ack' for p in old.sent)
    assert state()[0] is None and state()[2]=='running'
    monkeypatch.setattr(jobs, 'complete', original)
    current, current_session, _=await connect()
    await auth(current, current_session)
    event=completion(job_id)
    for count in (1,2):
        current.frame(event, current_session)
        await until(lambda: len([p for p in current.sent if p['type']=='sat_event_ack'])==count)
    assert state()==('success','terminal','completed',1)
    assert current.sent[-1]['session_id']==current_session.session_id

@pytest.mark.asyncio
async def test_replaced_script_result_cannot_write_or_ack(controller):
    _, _, connect=controller
    old, old_session, old_task=await connect()
    await auth(old, old_session)
    job_id=seed(old_session)
    current, session, _=await connect()
    await auth(current, session)
    old.frame(completion(job_id), old_session)
    await old_task
    assert not any(p['type']=='sat_event_ack' for p in old.sent)
    assert state()[0] is None and state()[2]=='running'

@pytest.mark.asyncio
async def test_capability_check_never_dispatches_to_replacement(controller, monkeypatch):
    _, manager, connect=controller
    old, session, _=await connect()
    await auth(old, session)
    job_id=seed(session)
    # Release the seeded reservation before exercising a new pending run.
    with SessionLocal() as db:
        task=db.query(TaskQueue).filter_by(execution_id='review-execution').one()
        task.status='completed'; db.commit()
    original=manager.send_session
    replacement=Socket()
    async def replace_before_write(target, message):
        if message.get('type')=='execute_script_job':
            await manager.connect(replacement, 'node', 'node-token', 2)
            assert target is session
        return await original(target, message)
    monkeypatch.setattr(manager, 'send_session', replace_before_write)
    with SessionLocal() as db:
        run=await jobs.trigger(db, db.get(User,'review-owner'), job_id, 'replacement-race')
        assert run.delivery_state=='unknown'
        assert db.query(TaskQueue).filter_by(execution_id=run.execution_id).one().status=='running'
    assert not any(p.get('type')=='execute_script_job' for p in replacement.sent)
