"""Current node authority after an RR snapshot; only an explicit disposable CI DB."""
import os
from types import SimpleNamespace
import pytest
from sqlalchemy import create_engine,Column,String
from sqlalchemy.engine import make_url
from sqlalchemy.orm import declarative_base,Session
from fastapi import HTTPException
from framework.native_http.hook_models import FrozenScriptHook


def test_hook_dispatch_does_not_overwrite_locked_node_with_old_rr_snapshot(monkeypatch):
    source=os.environ.get('ATS_MYSQL_TEST_URL')
    if not source:pytest.skip('Dedicated disposable MySQL CI service is not configured')
    url=make_url(source)
    if (os.environ.get('CI')!='true' or os.environ.get('ATS_MYSQL_ISOLATED')!='1' or url.host not in {'127.0.0.1','localhost'} or url.database!='ats_migration_test' or url.get_backend_name()!='mysql' or url.query):
        pytest.fail('Refusing any database other than explicit loopback CI fixture')
    Base=declarative_base()
    class Node(Base):
        __tablename__='ats_native_hook_rr_fixture'
        id=Column(String(36),primary_key=True)
        created_by=Column(String(36),nullable=False)
    from services import native_hooks,script_jobs
    actor=SimpleNamespace(id='owner',status=True)
    monkeypatch.setattr(native_hooks,'Environment',Node)
    monkeypatch.setattr(script_jobs,'Environment',Node)
    monkeypatch.setattr(script_jobs,'has_global_permission',lambda *args,**kw:False)
    monkeypatch.setattr(script_jobs,'find_job',lambda *args,**kw:SimpleNamespace(project_id='project'))
    # User authority is independent of the node snapshot under test.
    class UserQuery:
        def filter_by(self,**kw):return self
        def populate_existing(self):return self
        def with_for_update(self,**kw):return self
        def first(self):return actor
    engine=create_engine(url,isolation_level='REPEATABLE READ',pool_pre_ping=True)
    try:
        Base.metadata.create_all(engine)
        with engine.begin() as connection:connection.execute(Node.__table__.insert().values(id='node',created_by='owner'))
        with Session(engine) as session:
            original_query=session.query
            monkeypatch.setattr(session,'query',lambda model:UserQuery() if model is native_hooks.User else original_query(model))
            assert session.query(Node).first().created_by=='owner' # Establish old RR snapshot.
            with engine.begin() as connection:connection.execute(Node.__table__.update().values(created_by='revoked'))
            fresh=session.query(Node).populate_existing().with_for_update().first()
            assert fresh.created_by=='revoked'
            hook=FrozenScriptHook(id='hook',jobId='job',projectId='project',revision=1,config=dict(name='hook',environmentId='node',mode='python',script='print("fixture")',timeoutSeconds=1))
            with pytest.raises(HTTPException) as rejected:
                native_hooks.authorize_frozen(session,'owner',{'native_cases':[{'requests':[{'preProcessors':[hook.model_dump()]}]}]},node_current=True)
            assert rejected.value.status_code==403 and fresh.created_by=='revoked'
    finally:
        Base.metadata.drop_all(engine) # Only this named synthetic audit table.
        engine.dispose()
