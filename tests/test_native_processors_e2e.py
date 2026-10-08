"""Actual loopback controller-Agent frozen SQL/Mock/detail/ACK regression."""
import json
from loguru import logger
from framework.native_http.models import FrozenCase
from framework.native_http.variable_models import wire_case
import pytest
from conftest import isolated_database,sat_config
from test_http_agent_e2e import lab
from test_native_http_agent_e2e import native_lab,scope,dispatch,finished

@pytest.mark.asyncio
async def test_real_controller_agent_sql_mock_report_persistence(native_lab):
    from database import SessionLocal
    from models.plan_orchestration import PlanRunItem
    from models.test_suite import TestSuiteExecution
    value=native_lab
    request={**value['request'],'reportPhases':True,'query':{'q':'${sql_value}'},'preProcessors':[dict(type='sql',id='sql',query='SELECT :value AS selected',parameters={'value':'frozen-sql'},bindings=[dict(name='sql_value',column='selected')])],'mockResponse':dict(enable=True,statusCode=201,headers={'x-lab':'owned-loopback','Content-Type':'application/json'},body='{"accepted":true,"rows":[{"value":7}]}')}
    await value['config'](value['api'],{'request':request},revision=1)
    run_id=await scope(value,'api')
    changed={**request,'mockResponse':{**request['mockResponse'],'statusCode':500},'preProcessors':[]}
    await value['config'](value['api'],{'request':changed},revision=2)
    await dispatch(run_id);await finished(run_id)
    assert value['hits']==[]
    with SessionLocal() as db:
        item=db.query(PlanRunItem).filter_by(run_id=run_id).one()
        from services.suite_results import result_id
        rows=[db.get(TestSuiteExecution,result_id(item.execution_id,value['api']['id']))]
        assert len(rows)==1 and rows[0].result=='passed',json.dumps(rows[0].native_detail,ensure_ascii=False)
        detail=rows[0].native_detail
        assert detail['version']==2
        attempt=detail['steps'][0]['attempts'][0]
        assert attempt['source']=='mock'
        assert 'q=frozen-sql' in attempt['request']['url']
        assert attempt['response']['statusCode']==201
        assert attempt['processorResults'][0]['result']=='passed'
        assert attempt['timings']['preProcessorsMs']>=0
    from test_http_agent_e2e import until
    await until(lambda:not list(value['agent'].sat_runner.outbox.glob('*.json')))


import asyncio
import time
async def hook_job(value, tmp_path, phase, timeout=3, sleep=0):
    path=tmp_path/'hook-evidence.txt'
    script='from pathlib import Path\nimport os,time\np=Path('+repr(str(path))+')\nwith p.open("a") as f: f.write('+repr(phase+'\n')+')\n'
    if sleep:
        script+='Path('+repr(str(tmp_path/'child.pid'))+').write_text(str(os.getpid()))\ntime.sleep('+str(sleep)+')\n'
    data=dict(projectId=value['api']['projectId'],name=phase,environmentId=value['environment']['id'],mode='python',script=script,timeoutSeconds=timeout)
    job=await value['post']('/script-jobs',data)
    return job,dict(type='script',id=phase,jobId=job['id'],expectedRevision=job['revision']),data


def read_native_result(value, run_id, case):
    from database import SessionLocal
    from models.plan_orchestration import PlanRunItem
    from models.test_suite import TestSuiteExecution
    from services.suite_results import result_id
    with SessionLocal() as db:
        item=db.query(PlanRunItem).filter_by(run_id=run_id).one()
        row=db.get(TestSuiteExecution,result_id(item.execution_id,case['id']))
        return row.result,row.native_detail,item.execution_id


@pytest.mark.asyncio
async def test_real_scene_global_once_request_hooks_and_frozen_script_versions(native_lab,tmp_path):
    value=native_lab
    jobs={}
    for phase in ('global-pre','request-pre','request-post','global-post'):
        jobs[phase]=await hook_job(value,tmp_path,phase)
    request={**value['request'],'preProcessors':[jobs['request-pre'][1]],'postProcessors':[jobs['request-post'][1]],'reportPhases':True}
    await value['config'](value['api'],{'request':request},revision=1)
    scenario={'globalPreProcessors':[jobs['global-pre'][1]],'globalPostProcessors':[jobs['global-post'][1]],'steps':[{'apiCaseId':value['api']['id']},{'apiCaseId':value['api']['id']}],'stopOnFailure':True}
    await value['config'](value['scene'],{'scenario':scenario},revision=1)
    run_id=await scope(value,'scenario')
    # Existing frozen run must retain all four old sources, revisions and order.
    for phase,(job,_,data) in jobs.items():
        response=await value['client'].put('/api/v1/script-jobs/'+job['id'],json={k:v for k,v in {**data,'script':'raise RuntimeError("must not run updated source")'}.items() if k!='projectId'})
        assert response.status_code==200,response.text
    await dispatch(run_id);await finished(run_id)
    assert (tmp_path/'hook-evidence.txt').read_text().splitlines()==['global-pre','request-pre','request-post','request-pre','request-post','global-post']
    assert len(value['hits'])==2
    result,detail,eid=read_native_result(value,run_id,value['scene'])
    assert result=='passed',detail
    assert [p['result'] for p in detail['globalProcessorResults']]==['passed','passed']
    assert all([p['result'] for p in step['attempts'][0]['processorResults']]==['passed','passed'] for step in detail['steps'])
    from models.script_job import ScriptJobRun
    from database import SessionLocal
    with SessionLocal() as db:assert db.query(ScriptJobRun).count()==0,'hooks must not enqueue independent script runs'
    # Actual directory structure is checked separately through files to avoid assuming layout.
    scripts=list(value['agent'].work_dir.rglob('hook.py'))
    assert len(scripts)==6,len(scripts)


@pytest.mark.asyncio
async def test_real_hook_timeout_skips_http_and_global_post_and_releases_slot(native_lab,tmp_path):
    value=native_lab
    _,pre,_=await hook_job(value,tmp_path,'timeout-pre',timeout=1,sleep=30)
    _,post,_=await hook_job(value,tmp_path,'never-post')
    request={**value['request'],'globalPreProcessors':[pre],'globalPostProcessors':[post],'reportPhases':True}
    await value['config'](value['api'],{'request':request},revision=1)
    run_id=await scope(value,'api');started=time.monotonic()
    await dispatch(run_id);await finished(run_id)
    assert time.monotonic()-started<5
    assert value['hits']==[]
    assert (tmp_path/'hook-evidence.txt').read_text().splitlines()==['timeout-pre']
    result,detail,eid=read_native_result(value,run_id,value['api'])
    assert result=='error',detail
    assert [p['result'] for p in detail['globalProcessorResults']]==['error','skipped']
    await assert_child_dead(tmp_path)
    from database import SessionLocal
    from models.task_queue import TaskQueue
    with SessionLocal() as db:assert db.query(TaskQueue).filter_by(environment_id=value['environment']['id'],status='running').count()==0


async def assert_child_dead(tmp_path):
    import os
    pid=int((tmp_path/'child.pid').read_text())
    from test_http_agent_e2e import until
    def dead():
        try:os.kill(pid,0)
        except ProcessLookupError:return True
        return False
    await until(dead,timeout=3)


@pytest.mark.asyncio
async def test_real_hook_cancel_kills_child_skips_http_and_post(native_lab,tmp_path):
    value=native_lab
    _,pre,_=await hook_job(value,tmp_path,'cancel-pre',timeout=20,sleep=30)
    _,post,_=await hook_job(value,tmp_path,'never-post')
    request={**value['request'],'preProcessors':[pre],'globalPostProcessors':[post],'reportPhases':True}
    await value['config'](value['api'],{'request':request},revision=1)
    run_id=await scope(value,'api');await dispatch(run_id)
    from test_http_agent_e2e import until
    await until(lambda:(tmp_path/'child.pid').exists())
    response=await value['client'].post('/api/v1/plan-orchestration/runs/'+run_id+'/cancel')
    assert response.status_code==200,response.text
    await finished(run_id)
    assert value['hits']==[]
    assert (tmp_path/'hook-evidence.txt').read_text().splitlines()==['cancel-pre']
    await assert_child_dead(tmp_path)
    from database import SessionLocal
    from models.plan_orchestration import PlanRun
    from models.task_queue import TaskQueue
    with SessionLocal() as db:
        assert db.get(PlanRun,run_id).status=='cancelled'
        assert db.query(TaskQueue).filter_by(environment_id=value['environment']['id'],status='running').count()==0

@pytest.mark.asyncio
async def test_real_hook_node_authority_revocation_before_dispatch_rejects(native_lab,tmp_path,monkeypatch):
    from database import SessionLocal
    from models import Environment,User
    from models.plan_orchestration import PlanRunItem
    from models.task_queue import TaskQueue
    from services import script_jobs
    value=native_lab
    _,pre,_=await hook_job(value,tmp_path,'must-not-run')
    await value['config'](value['api'],{'request':{**value['request'],'preProcessors':[pre]}},revision=1)
    run_id=await scope(value,'api')
    with SessionLocal() as db:
        db.add(User(id='revoked-node-owner',username='revoked-node-owner',email='owner@example.test',password_hash='unused'))
        db.flush()
        db.get(Environment,value['environment']['id']).created_by='revoked-node-owner'
        db.commit()
    reads=[];original=script_jobs.require_node
    def spy(db,user,node,*,current_read=False):
        reads.append((node,current_read));return original(db,user,node,current_read=current_read)
    monkeypatch.setattr(script_jobs,'require_node',spy)
    await dispatch(run_id);await finished(run_id)
    assert value['hits']==[] and not (tmp_path/'hook-evidence.txt').exists()
    assert reads and all(current for _,current in reads),reads
    with SessionLocal() as db:
        item=db.query(PlanRunItem).filter_by(run_id=run_id).one()
        assert item.status=='failed'
        assert db.query(TaskQueue).filter_by(execution_id=item.execution_id).one().status=='failed'


@pytest.mark.asyncio
async def test_real_multi_case_hook_directories_do_not_overwrite(native_lab,tmp_path):
    value=native_lab
    _,pre,_=await hook_job(value,tmp_path,'request-pre')
    _,post,_=await hook_job(value,tmp_path,'request-post')
    await value['config'](value['api'],{'request':{**value['request'],'preProcessors':[pre],'postProcessors':[post]}},revision=1)
    response=await value['client'].post('/api/v1/test-plans/'+value['native_plan']['id']+'/execute',json={})
    assert response.status_code==200,response.text
    run_id=response.json()['data']['id']
    from database import SessionLocal
    from models.plan_orchestration import PlanRun
    for _ in range(300):
        await dispatch(run_id)
        with SessionLocal() as db:
            if db.get(PlanRun,run_id).status in ('completed','failed','cancelled'):break
        await asyncio.sleep(0.02)
    assert len(value['hits'])==3
    assert (tmp_path/'hook-evidence.txt').read_text().splitlines()==['request-pre','request-post']*3
    scripts=list(value['agent'].work_dir.rglob('hook.py'))
    assert len(scripts)==6,len(scripts)
    from database import SessionLocal
    from models.plan_orchestration import PlanRunItem
    with SessionLocal() as db:
        eids=[i.execution_id for i in db.query(PlanRunItem).filter_by(run_id=run_id)]
    # Category split creates two native execution IDs, all hook files must remain distinct.
    assert len(eids)==2,eids

@pytest.mark.asyncio
async def test_actual_runner_hook_sequence_is_unique_across_frozen_cases(sat_config,monkeypatch,tmp_path):
    from types import SimpleNamespace
    from agent.agent import Agent
    from agent.native_http_runner import NativeHTTPRunner
    from framework.native_http.hook_models import FrozenScriptHook
    agent=Agent(sat_config);agent.environment_id='node'
    agent.work_dir=sat_config.work_dir;agent.logger=logger
    agent.ws_client=SimpleNamespace(server_capabilities=['native_http_processors_v1'],server_url='ws://127.0.0.1/ws/agent')
    runner=NativeHTTPRunner(agent)
    messages=[]
    async def deliver(message):messages.append(message)
    async def log(*args,**kwargs):pass
    monkeypatch.setattr(runner,'deliver',deliver);monkeypatch.setattr(runner,'log',log)
    hook=FrozenScriptHook(id='same-id',jobId='job',projectId='project',revision=1,config=dict(name='hook',environmentId='node',mode='python',script='print("fixture")',timeoutSeconds=2))
    cases=[FrozenCase(id=cid,category='api',requests=[dict(name=cid,url='http://fixture.invalid',mockResponse={'enable':True},preProcessors=[hook])]) for cid in ['first','second']]
    await runner.execute(dict(suite_id='suite',execution_id='execution',case_ids=[c.id for c in cases],native_cases=[wire_case(c) for c in cases]))
    results=[m for m in messages if m['type']=='test_suite_result']
    assert [r['result'] for r in results]==['passed','passed'],messages
    files=list((agent.work_dir/'suites'/'suite'/'executions'/'execution'/'hooks').glob('*/hook.py'))
    assert sorted(p.parent.name for p in files)==['1','2']
    assert messages[-1]['status']=='completed'
