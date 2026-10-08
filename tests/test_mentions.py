"""Synthetic identities and local databases only; no outgoing messages."""
import pytest
from fastapi import HTTPException
from models import User, ProjectMember, Notification, LibraryFile
from models.case_features import CaseComment
from models.case_governance import CaseReviewEvent, CaseReviewDecision
from services.mentions import prepare
from test_file_library import library, upload
from test_case_features import features
from test_case_governance import governance, request_review
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab


def token(identifier, label='forged label'):
    return f'<span data-mention-id="{identifier}" data-mention-label="{label}">@{label}</span>'


@pytest.fixture
def mention_lab(library):
    from api.v1.mentions import router
    from api.v1.notifications import router as notifications
    g=library
    g['client'].app.include_router(router,prefix='/api/v1')
    g['client'].app.include_router(notifications,prefix='/api/v1/notifications')
    return g


def test_canonical_ids_escaped_labels_duplicates_self_and_plain_text(mention_lab):
    g=mention_lab;db=g['db'];recipient=g['users'][1]
    recipient.full_name='Member < & "safe"';db.commit()
    url=g['features']+f"/cases/{g['cases'][0].id}/comments"
    content='<p>'+token(recipient.id)+token(recipient.id)+token(g['users'][0].id)+'</p>'
    response=g['client'].post(url,json={'content':content})
    assert response.status_code==200,response.text
    stored=response.json()['data']['content'];assert 'forged label' not in stored
    assert 'Member &lt; &amp; &quot;safe&quot;' in stored
    notices=db.query(Notification).all();assert len(notices)==1 and notices[0].user_id==recipient.id
    assert recipient.full_name not in notices[0].content and g['cases'][0].name not in notices[0].content
    assert g['client'].post(url,json={'content':'plain @username & < 5'}).status_code==200
    assert db.query(Notification).count()==1
    old=stored;recipient.full_name='New name';db.commit()
    assert db.get(CaseComment,response.json()['data']['id']).content==old


def test_picker_literal_search_bounds_and_revoked_or_disabled_recipient(mention_lab):
    g=mention_lab;c=g['client'];p=g['project'].id;base=f'/api/v1/projects/{p}/mention-members'
    data=c.get(base).json()['data'];assert data['total']==3 and data['size']==20
    assert c.get(base,params={'search':'%'}).json()['data']['total']==0
    assert c.get(base,params={'page':0}).status_code==422
    assert c.get(base,params={'context':'anything'}).status_code==422
    url=g['features']+f"/cases/{g['cases'][0].id}/comments"
    assert c.post(url,json={'content':token(g['users'][3].id)}).status_code==422
    recipient=g['users'][1];recipient.status=False;g['db'].commit()
    assert c.post(url,json={'content':token(recipient.id)}).status_code==422
    recipient.status=True;g['db'].query(ProjectMember).filter_by(project_id=p,user_id=recipient.id).delete();g['db'].commit()
    assert c.post(url,json={'content':token(recipient.id)}).status_code==422
    assert g['db'].query(CaseComment).count()==0 and g['db'].query(Notification).count()==0
    g['state']['user']=g['users'][3];assert c.get(base).status_code==403


def test_invalid_nodes_and_recipient_limits(mention_lab):
    g=mention_lab;identifier=g['users'][1].id
    for value in [f'<span data-mention-id="{identifier}">unfinished',f'<img data-mention-id="{identifier}">',f'<span data-mention-id="{identifier}" />',f'<span data-mention-id="{identifier}"><b>nested</b></span>',f'<span data-mention-id="{identifier}" data-mention-id="{identifier}">duplicate</span>', ''.join(token(f'member-{i}') for i in range(21))]:
        with pytest.raises(HTTPException) as error:prepare(g['db'],g['users'][0],g['project'].id,value)
        assert error.value.status_code==422


def test_noncanonical_id_rejected_under_case_insensitive_database_comparison():
    from sqlalchemy import create_engine,MetaData,String
    from sqlalchemy.orm import Session
    from database import Base
    from models import Project
    metadata=MetaData()
    for table in Base.metadata.tables.values():table.to_metadata(metadata)
    metadata.tables['users'].c.id.type=String(36,collation='NOCASE')
    engine=create_engine('sqlite://');metadata.create_all(engine)
    with Session(engine) as db:
        actor=User(id='abc-def',username='synthetic',email='casefold@example.test',password_hash='unused');db.add(actor);db.flush()
        db.add(Project(id='casefold-project',name='Synthetic',owner_id=actor.id));db.commit()
        with pytest.raises(HTTPException) as error:prepare(db,actor,'casefold-project',token('ABC-DEF'))
        assert error.value.status_code==422
    engine.dispose()


def test_files_mentions_and_history_are_one_transaction_source_access_is_current(mention_lab):
    g=mention_lab;c=g['client'];file=upload(g);url=g['features']+f"/cases/{g['cases'][0].id}/comments"
    assert c.post(url,json={'content':token(g['users'][1].id),'fileIds':[file['id'],'missing']}).status_code==404
    assert not g['db'].get(LibraryFile,file['id']).published
    assert g['db'].query(Notification).count()==0 and g['db'].query(CaseComment).count()==0
    row=c.post(url,json={'content':token(g['users'][1].id)}).json()['data']
    notice=g['db'].query(Notification).one();endpoint=f'/api/v1/notifications/{notice.id}/source'
    assert c.get(endpoint).status_code==404
    g['state']['user']=g['users'][1];result=c.get(endpoint)
    assert result.status_code==200 and result.json()['data']['route']['query']['caseId']==g['cases'][0].id
    assert result.json()['data']['content']==row['content'] and result.json()['data']['sourceId']==row['id']
    g['db'].query(ProjectMember).filter_by(project_id=g['project'].id,user_id=g['users'][1].id).delete();g['db'].commit()
    assert c.get(endpoint).status_code==403
    # Inbox retains only a generic message after access is revoked.
    assert c.get('/api/v1/notifications').json()['data']['items'][0]['content']==notice.content
    g['state']['user']=g['users'][0];c.delete(url+'/'+row['id'])
    g['state']['user']=g['users'][1];assert c.get(endpoint).status_code==404


def test_review_batch_persists_each_event_but_notifies_once(mention_lab):
    g=mention_lab;c=g['client'];review=request_review(g,reviewers=[g['users'][0].id],cases=[row.id for row in g['cases']])
    # Same endpoint/schema as existing batch decisions.
    url=g['base']+f"/reviews/{review['id']}/batch-decision"
    response=c.post(url,json={'itemIds':[row['id'] for row in review['items']],'decision':'suggestion','comment':token(g['users'][1].id)})
    assert response.status_code==200,response.text
    events=g['db'].query(CaseReviewEvent).filter_by(action='评审结论').all()
    assert len(events)==2 and all('forged label' not in row.detail['comment'] for row in events)
    assert g['db'].query(Notification).count()==1 and g['db'].query(CaseReviewDecision).count()==0
    notice=g['db'].query(Notification).one();g['state']['user']=g['users'][1]
    result=c.get(f'/api/v1/notifications/{notice.id}/source');assert result.status_code==200
    assert result.json()['data']['route']['query']['reviewId']==review['id']


@pytest.mark.asyncio
async def test_execution_replay_retains_labels_and_does_not_renotify_disabled_recipient(workspace_http):
    import httpx
    from uuid import uuid4
    from api.v1.mentions import router
    from api.v1.notifications import router as notifications
    from models.plan_case_execution import PlanCaseExecution
    from test_plan_case_execution import body, BASE
    db,app,identity=workspace_http;app.include_router(router,prefix='/api/v1');app.include_router(notifications,prefix='/notifications')
    recipient=User(id=str(uuid4()),username='synthetic-member',email='mention@example.test',password_hash='unused');db.add(recipient);db.flush()
    db.add(ProjectMember(project_id='project',user_id=recipient.id));db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        row=(await client.get(BASE)).json()['data']['items'][0]
        payload=body([row],description=token(recipient.id));response=await client.post(BASE+'/execute',json=payload)
        assert response.status_code==200,response.text
        record=db.query(PlanCaseExecution).one();stored=record.description;notice=db.query(Notification).one()
        identity['id']=recipient.id;source=await client.get(f'/notifications/{notice.id}/source');assert source.status_code==200
        from models import Permission,ProjectPermission
        permission=db.query(Permission).filter_by(code='test_plan:read').first()
        if not permission:
            permission=Permission(code='test_plan:read',name='Synthetic plan read',resource='test_plan',action='read');db.add(permission);db.flush()
        db.add(ProjectPermission(project_id='project',user_id=recipient.id,permission_id=permission.id))
        db.query(ProjectMember).filter_by(project_id='project',user_id=recipient.id).delete();db.commit()
        assert (await client.get(f'/notifications/{notice.id}/source')).status_code==403
        recipient.status=False;db.commit();identity['id']='owner'
        replay=await client.post(BASE+'/execute',json=payload);assert replay.status_code==200 and replay.json()['data']['replayed']
        assert db.query(Notification).count()==1 and db.query(PlanCaseExecution).one().description==stored
        payload['requestId']=str(uuid4());assert (await client.post(BASE+'/execute',json=payload)).status_code==422


@pytest.mark.asyncio
async def test_frozen_run_comment_formats_and_deleted_report_source(workspace_http):
    import httpx
    from uuid import uuid4
    from services.plan_orchestration import start_plan_run
    from api.v1.notifications import router
    from models.plan_report_workspace import PlanReportWorkspace
    db,app,identity=workspace_http;app.include_router(router,prefix='/notifications')
    recipient=User(id=str(uuid4()),username='comment-recipient',email='run-mention@example.test',password_hash='unused');db.add(recipient);db.flush();db.add(ProjectMember(project_id='project',user_id=recipient.id));db.commit()
    run=await start_plan_run(db,'plan','owner');key=run.case_snapshot[0].get('associationId',run.case_snapshot[0]['id']);base=f'/orchestration/runs/{run.id}/cases/{key}'
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        legacy='<b>literal</b> <empty> & '+token(recipient.id)
        old=await client.post(base+'/comments',json={'content':legacy});assert old.status_code==200
        assert old.json()['data']['contentFormat']=='plain' and old.json()['data']['content']==legacy
        assert db.query(Notification).count()==0
        posted=await client.post(base+'/comments',json={'content':token(recipient.id),'contentFormat':'rich'});assert posted.status_code==200,posted.text
        assert posted.json()['data']['contentFormat']=='rich' and 'forged label' not in posted.json()['data']['content']
        rows=(await client.get(base+'/collaboration')).json()['data']['comments'];assert rows[0]['content']==legacy and rows[0]['contentFormat']=='plain'
        assert (await client.post(base+'/comments',json={'content':{'invalid':'type'}})).status_code==422
        assert (await client.post(base+'/comments',json={'content':'x','contentFormat':'invalid'})).status_code==422
        notice=db.query(Notification).one();identity['id']=recipient.id;source=await client.get(f'/notifications/{notice.id}/source');assert source.status_code==200
        assert source.json()['data']['route']['query']['associationId']==key
        assert source.json()['data']['content']==posted.json()['data']['content']
        db.add(PlanReportWorkspace(run_id=run.id,deleted=True,updated_by='owner'));db.commit()
        assert (await client.get(f'/notifications/{notice.id}/source')).status_code==404


def test_comment_format_upgrade_preserves_literal_text_and_is_repeatable():
    from sqlalchemy import create_engine,text,inspect
    from pathlib import Path
    import importlib.util
    spec=importlib.util.spec_from_file_location('ats_run_comment_upgrade',Path(__file__).resolve().parents[1]/'scripts/upgrade_run_comment_format.py')
    migration=importlib.util.module_from_spec(spec);spec.loader.exec_module(migration);upgrade=migration.upgrade
    engine=create_engine('sqlite://')
    with engine.begin() as connection:
        connection.execute(text('CREATE TABLE plan_run_comments (id VARCHAR(36) PRIMARY KEY, content TEXT NOT NULL)'))
        connection.execute(text('INSERT INTO plan_run_comments VALUES (:id,:content)'),{'id':'legacy','content':'<b>literal</b> <empty>'})
    assert upgrade(engine)=='add required'
    assert not any(c['name']=='content_format' for c in inspect(engine).get_columns('plan_run_comments'))
    assert upgrade(engine,apply=True)=='added' and upgrade(engine,apply=True)=='exists'
    with engine.connect() as connection:
        assert tuple(connection.execute(text('SELECT content,content_format FROM plan_run_comments')).one())==('<b>literal</b> <empty>','plain')
    engine.dispose()


@pytest.mark.parametrize('prior_actor_lock',[False,True])
def test_postgres_reciprocal_mentions_do_not_deadlock_authors_or_prior_identity_reads(mention_lab,prior_actor_lock):
    from database import engine,SessionLocal
    if engine.dialect.name!='postgresql':pytest.skip('requires disposable PostgreSQL CI')
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    from sqlalchemy import text
    from uuid import uuid4
    from models import Project
    g=mention_lab;db=g['db'];a,b=g['users'][0].id,g['users'][3].id;pa,pb=g['project'].id,g['foreign'].project_id
    db.add_all([ProjectMember(project_id=pa,user_id=b),ProjectMember(project_id=pb,user_id=a)]);db.commit()
    barrier=Barrier(2)
    def submit(project_id,actor_id,target_id,case_id):
        with SessionLocal() as session:
            session.execute(text("SET LOCAL lock_timeout = '3s'"))
            actor_query=session.query(User).filter_by(id=actor_id)
            actor=(actor_query.with_for_update(read=True) if prior_actor_lock else actor_query).one()
            content,recipients=prepare(session,actor,project_id,token(target_id))
            barrier.wait(timeout=5)
            row=CaseComment(id=str(uuid4()),case_id=case_id,author_id=actor_id,content=content);session.add(row);session.commit();return row.id
    with ThreadPoolExecutor(max_workers=2) as pool:
        first=pool.submit(submit,pa,a,b,g['cases'][0].id);second=pool.submit(submit,pb,b,a,g['foreign'].id)
        ids=[first.result(timeout=10),second.result(timeout=10)]
    assert db.query(CaseComment).filter(CaseComment.id.in_(ids)).count()==2


@pytest.mark.parametrize('kind',['case','plan'])
def test_postgres_view_quota_and_mention_share_project_lock_order(mention_lab,kind):
    from database import engine,SessionLocal
    if engine.dialect.name!='postgresql':pytest.skip('requires disposable PostgreSQL CI')
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    from types import SimpleNamespace
    from sqlalchemy import text
    from models.case_governance import CaseSavedView
    from models.plan_case_view import PlanCaseSavedView
    from api.v1.case_governance import save_view
    from schemas.case_governance import SavedViewCreate
    from schemas.plan_case_view import PlanCaseViewCreate
    from services.plan_case_view import save as save_plan_view
    g=mention_lab;db=g['db'];project_id,owner_id,recipient_id,case_id=g['project'].id,g['users'][0].id,g['users'][1].id,g['cases'][0].id
    model=CaseSavedView if kind=='case' else PlanCaseSavedView
    for i in range(9):
        args=dict(project_id=project_id,owner_id=recipient_id,name=f'old-{i}',filters={})
        if kind=='plan':args['category']='functional'
        db.add(model(**args))
    db.commit();barrier=Barrier(3)
    def create_view(index):
        with SessionLocal() as session:
            session.execute(text("SET LOCAL lock_timeout = '3s'"));user=session.get(User,recipient_id);barrier.wait(timeout=5)
            try:
                if kind=='case':save_view(project_id,SavedViewCreate(name=f'new-{index}',filters={}),session,user)
                else:save_plan_view(session,user,SimpleNamespace(project_id=project_id),'functional',PlanCaseViewCreate(name=f'new-{index}',filters={}));session.commit()
                return 200
            except HTTPException as error:
                session.rollback();return error.status_code
    def create_comment():
        with SessionLocal() as session:
            session.execute(text("SET LOCAL lock_timeout = '3s'"));user=session.get(User,owner_id);barrier.wait(timeout=5)
            content,_=prepare(session,user,project_id,token(recipient_id))
            row=CaseComment(case_id=case_id,author_id=owner_id,content=content);session.add(row);session.commit();return row.id
    with ThreadPoolExecutor(max_workers=3) as pool:
        first=pool.submit(create_view,1);second=pool.submit(create_view,2);comment=pool.submit(create_comment)
        assert sorted([first.result(timeout=10),second.result(timeout=10)])==[200,409]
        comment_id=comment.result(timeout=10)
    assert db.query(model).filter_by(project_id=project_id,owner_id=recipient_id).count()==10
    assert db.get(CaseComment,comment_id)
