"""Synthetic SQL, read-only authorization, budgets and parent request semantics."""
import asyncio
import httpx
import pytest
from pydantic import ValidationError
from framework.native_http.sql_models import SqlProcessor
from framework.native_http.sql_runtime import execute as sql
from framework.native_http.engine import execute
from framework.native_http.models import FrozenCase


def processor(**changes):
    values=dict(id='sql',query='SELECT value FROM fixture WHERE key = :key',parameters={'key':'${key}'},tables=[dict(name='fixture',columns=[dict(name='key'),dict(name='value')],rows=[dict(key='selected',value='bound-value')])],bindings=[dict(name='token',column='value')])
    values.update(changes)
    return SqlProcessor.model_validate(values)


@pytest.mark.asyncio
async def test_sql_binding_is_literal_and_cannot_inject_or_carry_fixture_between_runs():
    variables={'key':'selected'};temporary={}
    result=await sql(processor(),variables,temporary)
    assert result['rowCount']==1 and variables['token']==temporary['token']=='bound-value'
    with pytest.raises(ValueError):await sql(processor(),{'key':"' OR 1=1 --"},{})
    with pytest.raises(Exception):await sql(processor(tables=[]),{'key':'selected'},{})


@pytest.mark.asyncio
@pytest.mark.parametrize('query',['DELETE FROM fixture','UPDATE fixture SET value="changed"','DROP TABLE fixture','ATTACH DATABASE "file:forbidden" AS other','PRAGMA database_list','SELECT load_extension("forbidden")','SELECT randomblob(1000000000)','SELECT printf("%1000000000s","x")','SELECT 1; SELECT 2'])
async def test_sql_rejects_mutation_files_extensions_and_unbounded_functions(query):
    with pytest.raises(Exception):await sql(processor(query=query,bindings=[]),{'key':'selected'},{})


@pytest.mark.asyncio
async def test_recursion_and_result_budgets_are_bounded():
    with pytest.raises(Exception):await sql(processor(query='WITH RECURSIVE n(x) AS (VALUES(1) UNION ALL SELECT x+1 FROM n) SELECT sum(x) FROM n',bindings=[],timeoutMs=50),{}, {})
    with pytest.raises(ValueError,match='行数'):await sql(processor(query='SELECT a.key FROM fixture a CROSS JOIN fixture b UNION ALL SELECT key FROM fixture',bindings=[],maxRows=1),{}, {})
    p=processor(query='SELECT value FROM fixture',tables=[dict(name='fixture',columns=[dict(name='value')],rows=[dict(value='x'*40000),dict(value='y'*40000)])],bindings=[])
    with pytest.raises(ValueError,match='64KiB'):await sql(p,{}, {})


@pytest.mark.asyncio
async def test_cancel_interrupts_worker_and_propagates():
    p=processor(query='WITH RECURSIVE n(x) AS (VALUES(1) UNION ALL SELECT x+1 FROM n) SELECT sum(x) FROM n',bindings=[])
    task=asyncio.create_task(sql(p,{},{}));await asyncio.sleep(0)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):await asyncio.wait_for(task,2)


@pytest.mark.asyncio
async def test_sql_preparation_binds_http_and_post_failure_does_not_retry_completed_http():
    hits=[]
    def target(request):hits.append(dict(request.url.params));return httpx.Response(200)
    pre=processor().model_dump()
    bad=processor(id='post',query='DELETE FROM fixture',bindings=[]).model_dump()
    case=FrozenCase(id='sql',category='api',retryTimes=2,requests=[dict(name='sql',url='http://fixture.test/',initialVariables=[dict(name='key',value='selected')],query={'token':'${token}'},preProcessors=[pre],postProcessors=[bad])])
    result=await execute(case,transport=httpx.MockTransport(target),extended_details=True)
    assert hits==[{'token':'bound-value'}] and result['status']=='error'
    attempt=result['native_detail']['steps'][0]['attempts'][0]
    assert [p['result'] for p in attempt['processorResults']]==['passed','error']
    assert attempt['processorResults'][0]['rowCount']==1
    assert len(result['native_detail']['steps'][0]['attempts'])==1


@pytest.mark.asyncio
async def test_failed_preprocessor_sends_no_http():
    hits=[]
    def target(request):hits.append(request);return httpx.Response(200)
    case=FrozenCase(id='sql',category='api',requests=[dict(name='sql',url='http://fixture.test/',preProcessors=[processor(query='DELETE FROM fixture').model_dump()])])
    result=await execute(case,transport=httpx.MockTransport(target),extended_details=True)
    assert not hits and result['status']=='error'


@pytest.mark.asyncio
async def test_amplified_rows_are_streamed_before_64k_capture_limit():
    import tracemalloc
    p=processor(query='WITH RECURSIVE n(x) AS (VALUES(1) UNION ALL SELECT x+1 FROM n WHERE x<1000) SELECT :large AS value FROM n',parameters={'large':'x'*63000},tables=[],bindings=[],maxRows=1000)
    tracemalloc.start()
    try:
        with pytest.raises(ValueError,match='64KiB'):await sql(p,{}, {})
        _,peak=tracemalloc.get_traced_memory()
        assert peak<8*1024*1024
    finally:tracemalloc.stop()
