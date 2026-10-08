"""A frozen hook must not wait for a node held by a script updater's project wait."""
from concurrent.futures import ThreadPoolExecutor
from threading import Event
import pytest
from sqlalchemy import text
from database import engine,SessionLocal
from models import Environment,User,Project
from framework.native_http.hook_models import ScriptHook
from schemas.script_job import ScriptJobCreate,ScriptJobConfig
from services import script_jobs,native_hooks
from test_plan_orchestration import plan_lab
pytestmark=pytest.mark.skipif(engine.dialect.name!='postgresql',reason='Real PostgreSQL concurrent-lock regression')


def test_freeze_project_and_script_update_node_do_not_form_a_lock_cycle(plan_lab):
    db,_=plan_lab
    db.get(Environment,'node').created_by='owner';db.commit()
    data=dict(projectId='project',name='hook',environmentId='node',mode='python',script='print("frozen")',timeoutSeconds=2)
    job=script_jobs.create_job(db,db.get(User,'owner'),ScriptJobCreate(**data));job_id=job.id;db.commit()
    project_locked=Event();node_locked=Event()
    def freeze():
        with SessionLocal() as session:
            session.execute(text("SET LOCAL lock_timeout = '3s'"))
            session.query(Project).filter_by(id='project').populate_existing().with_for_update().one()
            project_locked.set();assert node_locked.wait(3)
            rows=native_hooks.freeze_processors(session,session.get(User,'owner'),'project',[ScriptHook(id='hook',jobId=job_id)])
            session.commit();return rows
    def update():
        assert project_locked.wait(3)
        with SessionLocal() as session:
            session.execute(text("SET LOCAL lock_timeout = '3s'"))
            actor=session.get(User,'owner')
            script_jobs.require_node(session,actor,'node',current_read=True);node_locked.set()
            config={k:v for k,v in data.items() if k!='projectId'};config['script']='print("updated")'
            result=script_jobs.update_job(session,actor,job_id,ScriptJobConfig(**config))
            return result.revision
    with ThreadPoolExecutor(max_workers=2) as executor:
        frozen=executor.submit(freeze);updated=executor.submit(update)
        assert frozen.result(8)[0]['config']['script']=='print("frozen")'
        assert updated.result(8)==2
