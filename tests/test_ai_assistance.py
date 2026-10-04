"""AI 的 HTTP 协议替身、隔离权限及草稿入库回归，不连接真实模型。"""
import json
import asyncio
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import uuid
import httpx
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from database import SessionLocal
from api.deps import get_current_user
from api.v1.ai_assistance import router
from models import User, Project, TestCase as Case
from models.ai_assistance import AIModelConfig, AIConversation, AICaseDraft


@pytest.fixture
def ai_lab(monkeypatch):
    with SessionLocal() as db:
        owner = User(id=str(uuid.uuid4()), username="ai-owner", email="ai-owner@example.com", password_hash="unused")
        other = User(id=str(uuid.uuid4()), username="ai-other", email="ai-other@example.com", password_hash="unused")
        db.add_all([owner, other]); db.flush()
        project = Project(id=str(uuid.uuid4()), name="AI隔离项目", owner_id=owner.id, created_by=owner.id)
        db.add(project); db.commit()
        actor = {"id": owner.id}; pid = project.id; owner_id=owner.id; other_id=other.id
    app=FastAPI();app.include_router(router,prefix="/api/v1")
    def current_user():
        with SessionLocal() as db:return db.get(User,actor["id"])
    app.dependency_overrides[get_current_user]=current_user
    answer={"content":"连接成功", "status":200, "timeout":False}
    requests=[]
    def provider(request):
        requests.append(request)
        if answer["timeout"]:raise httpx.ReadTimeout("模型测试超时",request=request)
        return httpx.Response(answer["status"],json={"choices":[{"message":{"content":answer["content"]}}]})
    factory=httpx.AsyncClient
    monkeypatch.setattr("services.ai_assistance.httpx.AsyncClient",lambda **kwargs:factory(transport=httpx.MockTransport(provider),**kwargs))
    dns = {"addresses": ["127.0.0.1"]}
    def resolve(host, port, *args, **kwargs):
        return [(socket.AF_INET6 if ":" in address else socket.AF_INET, socket.SOCK_STREAM,
                 socket.IPPROTO_TCP, "", (address, port, 0, 0) if ":" in address else (address, port))
                for address in dns["addresses"]]
    monkeypatch.setattr("services.ai_assistance.socket.getaddrinfo", resolve)
    with TestClient(app) as client:
        yield {"client":client,"project":pid,"owner":owner_id,"other":other_id,"actor":actor,"answer":answer,"requests":requests,
               "app": app, "async_factory": factory, "dns": dns}


def configure(lab):
    response=lab["client"].put('/api/v1/ai/configuration/personal',json={"base_url":"https://model.example/v1","model":"test-model","api_key":"local-secret-test","enabled":True})
    assert response.status_code==200,response.text
    assert "local-secret-test" not in response.text


def generate(lab):
    case={"name":"边界输入验证","type":"functional","priority":"P1","steps":[{"action":"输入边界值","expected":"准确提示"}]}
    lab["answer"]["content"]=json.dumps({"cases":[case]},ensure_ascii=False)
    return lab["client"].post('/api/v1/ai/generate-cases',json={"project_id":lab["project"],"requirement":"输入超出边界时显示错误提示","count":1})


def test_configuration_encryption_and_personal_scope(ai_lab):
    lab=ai_lab;configure(lab);client=lab['client']
    with SessionLocal() as db:
        row=db.query(AIModelConfig).one()
        assert row.api_key_encrypted and 'local-secret-test' not in row.api_key_encrypted
    assert client.post('/api/v1/ai/configuration/test').status_code==200
    request=lab['requests'][-1]
    assert str(request.url)=='https://127.0.0.1/v1/chat/completions'
    assert request.headers['host']=='model.example'
    assert request.extensions['sni_hostname']=='model.example'
    assert request.headers['authorization']=='Bearer local-secret-test'
    lab['actor']['id']=lab['other']
    assert client.get('/api/v1/ai/configuration').json()['data']['personal'] is None
    assert client.put('/api/v1/ai/configuration/system',json={'base_url':'https://model.example/v1','model':'x'}).status_code==403
    assert client.post('/api/v1/ai/configuration/test').status_code==409


def test_draft_edit_revision_and_idempotent_accept(ai_lab):
    lab=ai_lab;configure(lab);client=lab['client']
    r=generate(lab);assert r.status_code==200,r.text
    draft=r.json()['data'][0]
    with SessionLocal() as db:assert db.query(Case).count()==0
    content=draft['content'];content['name']='经人工审阅的用例'
    url='/api/v1/ai/drafts/'+draft['id']
    r=client.put(url,json={'revision':1,'content':content});assert r.status_code==200,r.text
    assert client.put(url,json={'revision':1,'content':content}).status_code==409
    for _ in range(2):
        r=client.post(url+'/accept',json={'revision':2});assert r.status_code==200,r.text
    with SessionLocal() as db:
        row=db.query(Case).one();assert row.name==content['name'] and not row.is_automated
        assert row.steps[0]['expected']=='准确提示'
        assert db.query(AICaseDraft).one().imported_case_id==row.id


def test_invalid_model_output_and_timeout_do_not_create_cases(ai_lab):
    lab=ai_lab;configure(lab);client=lab['client']
    request={'project_id':lab['project'],'requirement':'验证错误响应不产生草稿','count':1}
    lab['answer']['content']='这不是JSON'
    assert client.post('/api/v1/ai/generate-cases',json=request).status_code==502
    lab['answer']['timeout']=True
    assert client.post('/api/v1/ai/generate-cases',json=request).status_code==504
    with SessionLocal() as db:
        assert db.query(AICaseDraft).count()==0 and db.query(Case).count()==0


def test_chat_and_draft_cross_user_project_isolation(ai_lab):
    lab=ai_lab;configure(lab);client=lab['client']
    r=client.post('/api/v1/ai/chat',json={'project_id':lab['project'],'message':'如何覆盖边界条件？'})
    assert r.status_code==200,r.text
    cid=r.json()['data']['id'];draft=generate(lab).json()['data'][0]
    lab['actor']['id']=lab['other']
    assert client.get('/api/v1/ai/conversations/'+cid).status_code==404
    assert client.get('/api/v1/ai/drafts',params={'project_id':lab['project']}).status_code==403
    assert client.post('/api/v1/ai/drafts/'+draft['id']+'/accept',json={'revision':1}).status_code==404
    assert client.post('/api/v1/ai/chat',json={'project_id':lab['project'],'message':'越权输入'}).status_code==403


def test_without_model_and_dismissed_draft_are_explicit(ai_lab):
    lab=ai_lab;client=lab['client']
    assert client.post('/api/v1/ai/chat',json={'project_id':lab['project'],'message':'测试'}).status_code==409
    configure(lab);draft=generate(lab).json()['data'][0]
    url='/api/v1/ai/drafts/'+draft['id']
    assert client.post(url+'/dismiss',json={'revision':1}).status_code==200
    assert client.post(url+'/accept',json={'revision':2}).status_code==409
    assert client.put('/api/v1/ai/configuration/personal',json={'base_url':'http://169.254.169.254/v1','model':'x'}).status_code==422
    with SessionLocal() as db:assert db.query(Case).count()==0


@pytest.mark.asyncio
async def test_concurrent_chat_rejects_stale_write_without_losing_saved_turn(ai_lab, monkeypatch):
    lab = ai_lab
    configure(lab)
    initial = lab['client'].post('/api/v1/ai/chat', json={'project_id': lab['project'], 'message': '开始需求分析'})
    cid = initial.json()['data']['id']
    ready = asyncio.Event()
    entered = 0

    async def complete_together(config, messages):
        nonlocal entered
        entered += 1
        if entered == 2:
            ready.set()
        await asyncio.wait_for(ready.wait(), timeout=5)
        return '分析：' + messages[-1]['content']

    monkeypatch.setattr('services.ai_assistance.complete', complete_together)
    async with lab['async_factory'](transport=httpx.ASGITransport(app=lab['app']), base_url='http://isolated') as client:
        responses = await asyncio.gather(*[
            client.post('/api/v1/ai/chat', json={'project_id': lab['project'], 'conversation_id': cid, 'message': text})
            for text in ['窗口甲补充', '窗口乙补充']
        ])
    assert sorted(r.status_code for r in responses) == [200, 409]
    accepted = next(r.json()['data'] for r in responses if r.status_code == 200)
    with SessionLocal() as db:
        row = db.get(AIConversation, cid)
        assert row.revision == 2 and len(row.messages) == 4
        assert row.messages == accepted['messages']
        assert row.messages[0]['content'] == '开始需求分析'


def synchronize_draft_reads(monkeypatch):
    """在SQLite上强制两请求都先读到旧版本，验证CAS而不是仅验证串行点击。"""
    from api.v1 import ai_assistance
    original = ai_assistance.editable_draft
    barrier = threading.Barrier(2)

    def read_then_wait(*args, **kwargs):
        row = original(*args, **kwargs)
        barrier.wait(timeout=5)
        return row

    monkeypatch.setattr(ai_assistance, 'editable_draft', read_then_wait)


def test_concurrent_accept_creates_one_case_and_returns_same_case(ai_lab, monkeypatch):
    lab = ai_lab
    configure(lab)
    draft = generate(lab).json()['data'][0]
    synchronize_draft_reads(monkeypatch)
    url = '/api/v1/ai/drafts/' + draft['id'] + '/accept'
    with ThreadPoolExecutor(max_workers=2) as workers:
        responses = list(workers.map(lambda _: lab['client'].post(url, json={'revision': 1}), range(2)))
    assert [r.status_code for r in responses] == [200, 200]
    assert responses[0].json()['data']['imported_case_id'] == responses[1].json()['data']['imported_case_id']
    with SessionLocal() as db:
        case = db.query(Case).one()
        assert case.case_code == 'AI-' + draft['id']
        assert db.get(AICaseDraft, draft['id']).revision == 2


def test_concurrent_draft_edits_have_one_winner(ai_lab, monkeypatch):
    lab = ai_lab
    configure(lab)
    draft = generate(lab).json()['data'][0]
    synchronize_draft_reads(monkeypatch)
    url = '/api/v1/ai/drafts/' + draft['id']

    def save(name):
        return lab['client'].put(url, json={'revision': 1, 'content': {**draft['content'], 'name': name}})

    with ThreadPoolExecutor(max_workers=2) as workers:
        responses = list(workers.map(save, ['审阅版本甲', '审阅版本乙']))
    assert sorted(r.status_code for r in responses) == [200, 409]
    winner = next(r.json()['data'] for r in responses if r.status_code == 200)
    with SessionLocal() as db:
        row = db.get(AICaseDraft, draft['id'])
        assert row.revision == 2 and row.content == winner['content']


def test_concurrent_dismiss_and_accept_cannot_both_process_draft(ai_lab, monkeypatch):
    lab = ai_lab
    configure(lab)
    draft = generate(lab).json()['data'][0]
    synchronize_draft_reads(monkeypatch)
    prefix = '/api/v1/ai/drafts/' + draft['id']
    with ThreadPoolExecutor(max_workers=2) as workers:
        responses = list(workers.map(lambda action: lab['client'].post(prefix + '/' + action, json={'revision': 1}), ['dismiss', 'accept']))
    assert sorted(r.status_code for r in responses) == [200, 409]
    with SessionLocal() as db:
        row = db.get(AICaseDraft, draft['id'])
        assert row.revision == 2
        assert db.query(Case).count() == (1 if row.status == 'imported' else 0)


def test_draft_accept_failure_rolls_back_claim_and_case(ai_lab, monkeypatch):
    lab = ai_lab
    configure(lab)
    draft = generate(lab).json()['data'][0]
    from services.test_case_service import TestCaseService
    original = TestCaseService.create_test_case

    def fail_after_insert(*args, **kwargs):
        original(*args, **kwargs)
        from fastapi import HTTPException
        raise HTTPException(503, '测试注入：事务提交前中断')

    monkeypatch.setattr(TestCaseService, 'create_test_case', fail_after_insert)
    response = lab['client'].post('/api/v1/ai/drafts/' + draft['id'] + '/accept', json={'revision': 1})
    assert response.status_code == 503
    with SessionLocal() as db:
        row = db.get(AICaseDraft, draft['id'])
        assert row.status == 'draft' and row.revision == 1 and row.imported_case_id is None
        assert db.query(Case).count() == 0


@pytest.mark.parametrize('address', ['169.254.169.254', '224.0.0.1', '0.0.0.0', 'fe80::1', '::', '::ffff:169.254.169.254'])
def test_dns_alias_to_forbidden_address_never_sends_model_request(ai_lab, address):
    lab = ai_lab
    configure(lab)
    lab['dns']['addresses'] = ['192.168.1.4', address]
    response = lab['client'].post('/api/v1/ai/configuration/test')
    assert response.status_code == 400
    assert lab['requests'] == []


@pytest.mark.parametrize('address', ['127.0.0.1', '::1', '192.168.1.8', '10.1.2.3'])
def test_local_model_addresses_are_retained_and_pinned(ai_lab, address):
    lab = ai_lab
    configure(lab)
    lab['dns']['addresses'] = [address]
    assert lab['client'].post('/api/v1/ai/configuration/test').status_code == 200
    request = lab['requests'][0]
    assert request.url.host == address
    assert request.headers['host'] == 'model.example'
    assert request.extensions['sni_hostname'] == 'model.example'
