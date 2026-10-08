"""Bounded parent-slot hooks, immutable references and once-per-case phases."""
import asyncio
from copy import deepcopy
from types import SimpleNamespace
import time
import httpx
import pytest
from loguru import logger
from pydantic import ValidationError
from framework.native_http.models import FrozenCase, RequestSpec, ScenarioSpec
from framework.native_http.hook_models import FrozenScriptHook
from framework.native_http.engine import execute
from agent.native_hook_runtime import execute as run_hook
from test_plan_orchestration import plan_lab
from test_plan_native_workspace import native_workspace
from test_plan_workspace import workspace_http


def hook(identifier='hook', script='print("fixture")', **changes):
    config=dict(name='hook',environmentId='node',mode='python',script=script,timeoutSeconds=1)
    config.update(changes)
    return FrozenScriptHook(id=identifier,jobId='job',projectId='project',revision=1,config=config)


def request(**changes):
    value=dict(name='request',url='http://fixture.invalid',mockResponse={'enable':True})
    value.update(changes)
    return value


@pytest.mark.asyncio
async def test_global_hooks_run_once_and_request_hooks_run_each_attempt():
    seen=[];responses=[500,200,200]
    async def callback(value):seen.append(value.id);return {}
    def transport(value):return httpx.Response(responses.pop(0))
    case=FrozenCase(id='case',category='scenario',retryTimes=1,requests=[request(mockResponse=None,preProcessors=[hook('pre')],postProcessors=[hook('post')]),request(mockResponse=None)],globalPreProcessors=[hook('global-pre')],globalPostProcessors=[hook('global-post')])
    result=await execute(case,transport=httpx.MockTransport(transport),hook_executor=callback,extended_details=True)
    assert result['status']=='passed'
    assert seen==['global-pre','pre','post','pre','post','global-post']
    assert [r['phase'] for r in result['native_detail']['globalProcessorResults']]==['global_pre','global_post']


@pytest.mark.asyncio
async def test_global_failure_skips_requests_and_remaining_global_hooks():
    seen=[]
    async def callback(value):seen.append(value.id);raise ValueError('synthetic failure')
    case=FrozenCase(id='case',category='api',requests=[request()],globalPreProcessors=[hook('bad'),hook('never')],globalPostProcessors=[hook('post')])
    result=await execute(case,hook_executor=callback,extended_details=True)
    assert result['status']=='error' and seen==['bad']
    assert result['native_detail']['steps'][0]['attempts']==[]
    assert [r['result'] for r in result['native_detail']['globalProcessorResults']]==['error','skipped','skipped']


@pytest.mark.asyncio
@pytest.mark.parametrize('phase',['preProcessors','postProcessors'])
async def test_hook_failure_never_retries_parent_side_effect(phase):
    hits=[];hooks=[]
    def transport(value):hits.append(value);return httpx.Response(200)
    async def callback(value):hooks.append(value.id);raise ValueError('synthetic')
    case=FrozenCase(id='case',category='api',retryTimes=3,requests=[request(mockResponse=None,**{phase:[hook()]})])
    result=await execute(case,transport=httpx.MockTransport(transport),hook_executor=callback,extended_details=True)
    assert result['status']=='error' and len(hits)==(0 if phase=='preProcessors' else 1)
    assert hooks==['hook'] and len(result['native_detail']['steps'][0]['attempts'])==1


@pytest.mark.asyncio
async def test_cancellation_runs_no_post_hooks():
    seen=[];entered=asyncio.Event()
    async def callback(value):
        seen.append(value.id);entered.set();await asyncio.Event().wait()
    case=FrozenCase(id='case',category='api',requests=[request(preProcessors=[hook('pre')],postProcessors=[hook('post')])],globalPostProcessors=[hook('global-post')])
    task=asyncio.create_task(execute(case,hook_executor=callback,extended_details=True));await entered.wait();task.cancel()
    with pytest.raises(asyncio.CancelledError):await task
    assert seen==['pre']


@pytest.mark.asyncio
@pytest.mark.parametrize('blocked',['start','finish'])
async def test_deadline_includes_log_backpressure(tmp_path,blocked):
    logs=[]
    async def log(message,text,**kw):
        logs.append(text)
        if ('开始' if blocked=='start' else '完成') in text:await asyncio.Event().wait()
    runner=SimpleNamespace(agent=SimpleNamespace(work_dir=tmp_path,environment_id='node',logger=logger,config=SimpleNamespace()),log=log)
    start=time.monotonic()
    with pytest.raises(asyncio.TimeoutError):await run_hook(runner,{'execution_id':'execution'},hook(),tmp_path/'hook')
    assert time.monotonic()-start<1.5
    assert any(text.strip()=='fixture' for text in logs)==(blocked=='finish')


@pytest.mark.asyncio
@pytest.mark.parametrize('mode',['python','shell','command'])
async def test_plain_scripts_and_argv_use_parent_durable_log(tmp_path,mode):
    import sys
    if mode=='shell' and sys.platform=='win32':pytest.skip('Linux shell fixture')
    source={'python':'import sys; print(repr(sys.argv[1:]))','shell':"printf '%s\\n' \"$@\"",'command':''}[mode]
    values=dict(mode=mode,args=['with space',''],timeoutSeconds=3)
    if mode=='command':values.update(command=sys.executable,args=['-c','import sys; print(repr(sys.argv[1:]))','with space',''])
    logs=[]
    async def log(message,text,**kw):logs.append((message['execution_id'],text))
    runner=SimpleNamespace(agent=SimpleNamespace(work_dir=tmp_path,environment_id='node',logger=logger,config=SimpleNamespace()),log=log)
    await run_hook(runner,{'execution_id':'parent'},hook(script=source,**values),tmp_path/'hook')
    assert logs and all(identifier=='parent' for identifier,_ in logs)
    assert any('with space' in text for _,text in logs)
    if mode!='shell':assert any("''" in text for _,text in logs)


def test_saved_refs_cannot_supply_executable_configs_and_global_ids_are_unique():
    with pytest.raises(ValidationError):RequestSpec(preProcessors=[hook().model_dump()])
    for model,fields in [(ScenarioSpec,{'steps':[{'apiCaseId':'api'}]}),(FrozenCase,{'id':'case','category':'api','requests':[request()]})]:
        with pytest.raises(ValidationError):model(**fields,globalPreProcessors=[hook(),hook()])


def test_reference_freezes_revision_and_dispatch_rechecks_current_owner(native_workspace):
    from models import User,Environment,TestCase
    from models.native_case import NativeCaseConfig
    from schemas.script_job import ScriptJobCreate,ScriptJobConfig
    from services import script_jobs,native_hooks
    from services.native_http_execution import freeze
    from services.suite_dispatch import build_suite_message
    from test_native_http_execution import configure
    from fastapi import HTTPException
    db,_,_=native_workspace;configure(db)
    user=db.get(User,'owner');db.get(Environment,'node').created_by='owner';db.commit()
    data=dict(projectId='project',name='hook',environmentId='node',mode='python',script='print("frozen")',timeoutSeconds=2)
    job=script_jobs.create_job(db,user,ScriptJobCreate(**data))
    row=db.get(NativeCaseConfig,'case-0');row.parameters={'request':{'preProcessors':[dict(type='script',id='hook',jobId=job.id,expectedRevision=1)]}};db.commit()
    frozen=freeze(db,db.get(TestCase,'case-0'),user);message={'native_cases':[frozen]};db.commit()
    update={k:v for k,v in data.items() if k!='projectId'};update['script']='print("changed")'
    script_jobs.update_job(db,user,job.id,ScriptJobConfig(**update))
    assert frozen['requests'][0]['preProcessors'][0]['config']['script']=='print("frozen")'
    native_hooks.authorize_frozen(db,user.id,message,node_current=True);db.commit()
    db.add(User(id='revoked',username='revoked',email='revoked@example.test',password_hash='unused'));db.flush()
    db.get(Environment,'node').created_by='revoked';db.commit()
    with pytest.raises(HTTPException) as error:native_hooks.authorize_frozen(db,user.id,message,node_current=True)
    assert error.value.status_code==403


@pytest.mark.asyncio
async def test_api_global_sql_sees_its_initial_variables_and_binds_request():
    sql=dict(type='sql',id='global-sql',query='SELECT :v AS value',parameters={'v':'${api_value}'},bindings=[dict(name='bound',column='value')])
    case=FrozenCase(id='api',category='api',globalPreProcessors=[sql],requests=[request(initialVariables=[dict(name='api_value',value='frozen-api')],query={'q':'${bound}'})])
    result=await execute(case,extended_details=True)
    assert result['status']=='passed'
    assert 'q=frozen-api' in result['native_detail']['steps'][0]['attempts'][0]['request']['url']
    assert result['native_detail']['globalProcessorResults'][0]['bindings'][0]['value']=='frozen-api'
