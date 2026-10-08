"""Static Mock is explicit, bounded and never reaches the actual target transport."""
import asyncio
from copy import deepcopy
import httpx
import pytest
from pydantic import ValidationError
from framework.native_http.models import FrozenCase, RequestSpec
from framework.native_http.variable_models import wire_case
from framework.native_http.engine import execute
from services import native_variable_delivery as delivery


@pytest.mark.asyncio
async def test_saved_mock_uses_extractions_assertions_and_real_timing_without_target_calls():
    calls=[]
    def target(request): calls.append(request); return httpx.Response(500)
    case=FrozenCase(id='mock',category='api',requests=[dict(name='mock',url='http://fixture.invalid/',reportPhases=True,mockResponse=dict(enable=True,statusCode=201,body='{"value":"selected"}',headers={'Content-Type':'application/json'},delayMs=20),postProcessorConfig=dict(processors=[dict(id='p',extractors=[dict(id='e',variableName='v',expression='$.value')])]),responseAssertions=[dict(id='a',name='variable',assertionType='VARIABLE',variableAssertionItems=[dict(variableName='v',condition='EQUALS',expectedValue='selected')])])])
    result=await execute(case,transport=httpx.MockTransport(target),extended_details=True)
    assert result['status']=='passed' and not calls
    detail=result['native_detail'];assert detail['version']==2
    attempt=detail['steps'][0]['attempts'][0]
    assert attempt['source']=='mock' and attempt['response']['statusCode']==201
    assert attempt['timings']['httpMs']>=15
    assert all(attempt['timings'][key]>=0 for key in ('preparationMs','extractionMs','assertionMs'))
    assert 'dnsMs' not in attempt['timings']
    assert attempt['extractResults'][0]['value']=='selected'


@pytest.mark.asyncio
async def test_legacy_details_have_no_new_fields_and_failed_http_has_measured_phase():
    async def target(request): await asyncio.sleep(0.01);raise httpx.ReadTimeout('synthetic timeout',request=request)
    case=FrozenCase(id='old',category='api',requests=[dict(name='old',url='http://fixture.test/')])
    result=await execute(case,transport=httpx.MockTransport(target))
    attempt=result['native_detail']['steps'][0]['attempts'][0]
    assert result['native_detail']['version']==1 and 'source' not in attempt and 'timings' not in attempt
    assert attempt['response'] is None
    result=await execute(case,transport=httpx.MockTransport(target),extended_details=True)
    attempt=result['native_detail']['steps'][0]['attempts'][0]
    assert attempt['timings']['httpMs']>=5 and attempt['timings']['extractionMs'] is None


def test_disabled_defaults_strip_and_capability_is_distinct():
    case=FrozenCase(id='old',category='api',requests=[dict(name='old',url='http://fixture.test/',mockResponse={'enable':False})])
    wire=wire_case(case)
    assert 'mockResponse' not in wire['requests'][0] and 'reportPhases' not in wire['requests'][0]
    assert delivery.required_capabilities({'native_cases':[wire]})==set()
    case.requests[0].mockResponse.enable=True
    assert delivery.required_capabilities({'native_cases':[wire_case(case)]})=={delivery.PROCESSORS_CAPABILITY}
    case.requests[0].initialVariables=RequestSpec(initialVariables=[dict(name='v')]).initialVariables
    assert delivery.required_capabilities({'native_cases':[wire_case(case)]})=={delivery.PROCESSORS_CAPABILITY,delivery.CAPABILITY}


@pytest.mark.parametrize('mock',[{'enable':1},{'statusCode':True},{'statusCode':199},{'delayMs':3001},{'headers':{'x':'a\r\nb'}},{'body':'中'*131072}])
def test_bounded_mock_rejected(mock):
    with pytest.raises(ValidationError):RequestSpec(mockResponse=mock)


@pytest.mark.asyncio
async def test_mock_obeys_explicit_response_timeout_instead_of_connect_timeout():
    case=FrozenCase(id='mock',category='api',requests=[dict(name='mock',url='http://fixture.invalid',connectTimeoutMs=100,responseTimeoutMs=5,mockResponse={'enable':True,'delayMs':100})])
    result=await execute(case,extended_details=True)
    assert result['status']=='error' and result['native_detail']['steps'][0]['attempts'][0]['response'] is None
