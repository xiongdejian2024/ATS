"""Shared evidence uses synthetic bytes and isolated databases; no external S3."""
from io import BytesIO
import pytest
from PIL import Image
from models import AttachmentBlob, LibraryFile, LibraryReference
from models.case_governance import CaseReviewEvent, CaseReviewDecision
from test_case_features import features
from test_case_governance import governance, request_review
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from api.v1.file_library import router

@pytest.fixture
def library(features,monkeypatch):
    monkeypatch.setenv('ATS_ATTACHMENT_BACKEND','database')
    features['client'].app.include_router(router,prefix='/api/v1')
    features['library']=f"/api/v1/projects/{features['project'].id}/file-library"
    return features

def png():
    output=BytesIO();Image.new('RGB',(2,2),'blue').save(output,format='PNG');return output.getvalue()

def upload(g,name='evidence.txt',raw=b'synthetic evidence',**params):
    response=g['client'].post(g['library']+'/files',files={'file':(name,raw,'application/octet-stream')},data={key:str(value).lower() if isinstance(value,bool) else value for key,value in params.items()})
    assert response.status_code==200,response.text
    return response.json()['data']


def test_directory_cycles_duplicate_names_and_project_access(library):
    g=library;c,base=g['client'],g['library']
    first=c.post(base+'/folders',json={'name':'root'}).json()['data']
    child=c.post(base+'/folders',json={'name':'child','parentId':first['id']}).json()['data']
    assert c.put(base+'/folders/'+first['id'],json={'name':'root','parentId':child['id']}).status_code==409
    assert c.post(base+'/folders',json={'name':'child','parentId':first['id']}).status_code==409
    assert c.post(base+'/folders',json={'name':'../bad'}).status_code==422
    assert c.put(base+'/folders/'+child['id'],json={'name':'moved','parentId':None}).status_code==200
    g['state']['user']=g['users'][1]
    assert c.post(base+'/folders',json={'name':'forbidden'}).status_code==403
    g['state']['user']=g['users'][3]
    assert c.get(base+'/folders').status_code==403


def test_private_draft_published_references_archive_and_immutable_bytes(library):
    g=library;c,base=g['client'],g['library'];file=upload(g)
    assert not file['published'] and file['mimeType']=='application/octet-stream'
    g['state']['user']=g['users'][1]
    assert c.get(base+'/files/'+file['id']+'/download').status_code==403
    assert c.get(base+'/files').json()['data']['total']==0
    g['state']['user']=g['users'][0]
    case=g['cases'][0].id
    url=base+f'/cases/{case}/references'
    assert c.post(url,json={'fileIds':[file['id'],file['id']]}).status_code==200
    assert g['db'].query(LibraryReference).count()==1
    g['state']['user']=g['users'][1]
    result=c.get(base+'/files/'+file['id']+'/download');assert result.content==b'synthetic evidence'
    assert result.headers['x-content-type-options']=='nosniff' and result.headers['cache-control']=='private, no-store'
    assert c.get(base+'/files/'+file['id']+'/preview').status_code==422
    assert c.delete(url+'/'+file['id']).status_code==403
    g['state']['user']=g['users'][0]
    assert c.put(base+'/files/'+file['id']+'/archive',json={'archived':True}).status_code==200
    assert c.get(base+'/files').json()['data']['total']==0
    assert c.get(url).json()['data'][0]['archived']
    assert c.get(base+'/files/'+file['id']+'/download').content==b'synthetic evidence'
    assert c.post(url,json={'fileIds':[file['id']]}).status_code==409
    assert c.delete(url+'/'+file['id']).status_code==200
    assert c.get(url).json()['data']==[]
    assert g['db'].query(LibraryReference).count()==1 and g['db'].query(AttachmentBlob).count()==1
    assert c.put(base+'/files/'+file['id']+'/archive',json={'archived':False}).status_code==200
    assert c.post(url,json={'fileIds':[file['id']]}).status_code==200
    # A corrupted blob cannot be served under its preserved digest.
    row=g['db'].get(LibraryFile,file['id']);g['db'].get(AttachmentBlob,row.file_path).content=b'corrupt';g['db'].commit()
    assert c.get(base+'/files/'+file['id']+'/download').status_code==409


def test_verified_image_only_preview_and_bounded_file_listing(library):
    g=library;c,base=g['client'],g['library']
    invalid=c.post(base+'/files',files={'file':('fake.png',b'<script>bad</script>','image/png')},data={'image':'true'})
    assert invalid.status_code==422 and g['db'].query(LibraryFile).count()==0
    file=upload(g,'screenshot.png',png(),image=True)
    result=c.get(base+'/files/'+file['id']+'/preview')
    assert result.status_code==200 and result.headers['content-type']=='image/png'
    assert result.headers['content-disposition']=='inline' and "sandbox" in result.headers['content-security-policy']
    for index in range(21):upload(g,f'file-{index}.txt',published=True)
    data=c.get(base+'/files').json()['data'];assert data['total']==22 and len(data['items'])==20
    assert len(c.get(base+'/files',params={'page':2}).json()['data']['items'])==2
    images=c.get(base+'/files',params={'imagesOnly':'true'}).json()['data'];assert images['total']==1 and images['items'][0]['id']==file['id']
    assert c.get(base+'/files',params={'page':0}).status_code==422


def test_comment_references_rollback_cross_project_and_history_retention(library):
    g=library;c=g['client'];first=upload(g);foreign_id='00000000-0000-0000-0000-000000000000'
    url=g['features']+f"/cases/{g['cases'][0].id}/comments"
    assert c.post(url,json={'content':'with file','fileIds':[first['id'],foreign_id]}).status_code==404
    assert not g['db'].get(LibraryFile,first['id']).published
    assert g['db'].query(LibraryReference).count()==0
    comment=c.post(url,json={'content':'<p>rich evidence</p>','fileIds':[first['id']]}).json()['data']
    data=c.get(url).json()['data'];assert data[0]['files'][0]['id']==first['id'] and data[0]['canDelete']
    assert c.delete(url+'/'+comment['id']).status_code==200
    assert g['db'].query(LibraryReference).count()==1 and g['db'].query(AttachmentBlob).count()==1


def test_review_event_references_remain_independent_of_mutable_vote(library):
    g=library;c=g['client'];image=upload(g,'vote.png',png(),image=True);file=upload(g)
    review=request_review(g,reviewers=[g['users'][0].id]);item=review['items'][0]['id'];url=g['base']+f"/reviews/{review['id']}/items/{item}/decision"
    first=c.post(url,json={'decision':'suggestion','comment':f'<p>reason</p><img src="{image["src"]}">','fileIds':[file['id']]})
    assert first.status_code==200,first.text
    event=g['db'].query(CaseReviewEvent).filter_by(action='评审结论').one()
    refs=g['db'].query(LibraryReference).filter_by(entity_kind='review_event',entity_id=event.id).all();assert len(refs)==2
    assert g['db'].query(CaseReviewDecision).count()==0
    assert c.post(url,json={'decision':'approved','comment':'new conclusion'}).status_code==200
    assert len(g['db'].query(LibraryReference).filter_by(entity_id=event.id).all())==2
    assert c.put(g['library']+'/files/'+image['id']+'/archive',json={'archived':True}).status_code==200
    assert c.get(g['library']+'/files/'+image['id']+'/preview').content==png()
    assert c.post(url,json={'decision':'suggestion','comment':f'<img src="{image["src"]}">'}).status_code==409
    assert g['db'].query(CaseReviewDecision).one().decision=='approved'


def test_cross_project_and_other_authors_private_draft_never_partially_publish(library):
    g=library;c=g['client'];first=upload(g)
    g['state']['user']=g['users'][1];private=upload(g)
    g['state']['user']=g['users'][3]
    other=f"/api/v1/projects/{g['foreign'].project_id}/file-library"
    response=c.post(other+'/files',files={'file':('foreign.txt',b'foreign evidence','text/plain')},data={'published':'true'})
    assert response.status_code==200,response.text
    foreign=response.json()['data']
    g['state']['user']=g['users'][0]
    target=g['library']+f"/cases/{g['cases'][0].id}/references"
    assert c.post(target,json={'fileIds':[first['id'],foreign['id']]}).status_code==404
    assert not g['db'].get(LibraryFile,first['id']).published
    assert c.post(target,json={'fileIds':[first['id'],private['id']]}).status_code==403
    assert not g['db'].get(LibraryFile,first['id']).published and not g['db'].get(LibraryFile,private['id']).published
    assert g['db'].query(LibraryReference).count()==0
    assert c.post(g['features']+f"/cases/{g['cases'][0].id}/comments",json={'content':f'<img src="{foreign["src"] or other+"/files/"+foreign["id"]+"/preview"}">'}).status_code==422


def test_postgres_mixed_image_reference_locks_use_one_order(library):
    from database import engine,SessionLocal
    if engine.dialect.name!='postgresql':pytest.skip('requires disposable PostgreSQL CI')
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    from uuid import uuid4
    from sqlalchemy import text
    from models import User
    from models.case_features import CaseComment
    from services.file_library import image_ids,reference
    g=library;files=[upload(g,'one.png',png(),image=True,published=True),upload(g,'two.png',png(),image=True,published=True)]
    project_id,user_id,case_id=g['project'].id,g['users'][0].id,g['cases'][0].id
    barrier=Barrier(2)
    def submit(reverse):
        with SessionLocal() as db:
            db.execute(text("SET LOCAL lock_timeout = '3s'"))
            user=db.get(User,user_id)
            ids=image_ids(db,project_id,''.join(f'<img src="{f["src"]}">' for f in (files[::-1] if reverse else files)))
            comment=CaseComment(id=str(uuid4()),case_id=case_id,author_id=user_id,content='synthetic concurrent evidence');db.add(comment);db.flush()
            barrier.wait(timeout=5)
            reference(db,user,project_id,ids,'comment',comment.id);db.commit()
            return comment.id
    with ThreadPoolExecutor(max_workers=2) as pool:
        first=pool.submit(submit,False);second=pool.submit(submit,True)
        identifiers=[first.result(timeout=10),second.result(timeout=10)]
    assert g['db'].query(LibraryReference).filter(LibraryReference.entity_id.in_(identifiers)).count()==4


@pytest.mark.asyncio
async def test_independent_execution_library_history_replay_after_archive(workspace_http,monkeypatch):
    import httpx
    from test_plan_case_execution import body,BASE
    from models.plan_case_execution import PlanCaseExecution
    monkeypatch.setenv('ATS_ATTACHMENT_BACKEND','database')
    db,app,_=workspace_http;app.include_router(router,prefix='/api/v1')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        response=await client.post('/api/v1/projects/project/file-library/files',files={'file':('image.png',png(),'image/png')},data={'image':'true'})
        assert response.status_code==200,response.text
        file=response.json()['data'];row=(await client.get(BASE)).json()['data']['items'][0]
        payload=body([row],description=f'<p>frozen</p><img src="{file["src"]}">')
        assert (await client.post(BASE+'/execute',json=payload)).status_code==200
        record=db.query(PlanCaseExecution).one()
        assert db.query(LibraryReference).filter_by(entity_kind='case_execution',entity_id=record.id).count()==1
        await client.put('/api/v1/projects/project/file-library/files/'+file['id']+'/archive',json={'archived':True})
        assert (await client.post(BASE+'/execute',json=payload)).json()['data']['replayed']
        assert (await client.get(file['src'])).content==png()
        assert db.query(PlanCaseExecution).count()==1
