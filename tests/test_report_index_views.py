"""报告个人高级视图只查询真实冻结批次，不触发Agent或改写历史。"""
import json
from copy import deepcopy
import pytest
import httpx
from fastapi import HTTPException
from test_plan_report_workspace import reports_http
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from models import User, TestPlan as Plan
from models.plan_case_view import PlanCaseSavedView
from models.plan_orchestration import PlanRun
from services.plan_orchestration import start_plan_run, record_manual_result, advance_plan_runs
from schemas.plan_orchestration import ManualResultInput
from services.report_index_filter import parse


def condition(field,value=None,operator='equals'):
    return dict(field=field,value=value,operator=operator)


@pytest.mark.asyncio
async def test_private_report_views_crud_quota_validation_and_fixed_namespace(reports_http):
    db,app,identity=reports_http
    base='/orchestration/projects/project/reports/views'
    filters=dict(filterConditions=[condition('executorId','CURRENT_USER')],filterLogic='or')
    body=dict(name='我的报告',filters=filters)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        response=await client.post(base,json=body);assert response.status_code==200,response.text
        row=response.json()['data'];assert db.get(PlanCaseSavedView,row['id']).category=='report-index'
        assert (await client.put(base+'/'+row['id'],json=dict(name='个人报告'))).json()['data']['filters']==filters
        assert (await client.post(base,json=dict(body,name='个人报告'))).status_code==409
        for i in range(9):assert (await client.post(base,json=dict(body,name=f'报告{i}'))).status_code==200
        assert (await client.post(base,json=dict(body,name='超额'))).status_code==409
        assert (await client.get('/orchestration/projects/project/index-views')).json()['data']==[]
        for invalid in (None,dict(mine=True),dict(filterConditions=[condition('priority','P0')]),dict(filterConditions=[condition('passRate',True)])):
            assert (await client.put(base+'/'+row['id'],json=dict(name='非法',filters=invalid))).status_code==422
        identity['id']='stranger';assert (await client.delete(base+'/'+row['id'])).status_code==403
        identity['id']='owner';db.get(User,'owner').status=False;db.commit()
        assert (await client.put(base+'/'+row['id'],json=dict(name='停用'))).status_code==403
        db.get(User,'owner').status=True;db.commit();assert (await client.delete(base+'/'+row['id'])).status_code==200


@pytest.mark.asyncio
async def test_report_advanced_count_paging_and_mandatory_kind_do_not_change_frozen_history(reports_http):
    db,app,identity=reports_http
    first=await start_plan_run(db,'manual','owner')
    record_manual_result(db,first.id,'case-2',ManualResultInput(result='passed'),'owner');await advance_plan_runs(db)
    first.plan_name='Literal_%';db.commit();frozen=deepcopy(first.report)
    second=await start_plan_run(db,'manual','owner')
    from datetime import datetime
    first.created_at=datetime(2026,10,8,8,30);second.created_at=datetime(2026,10,8,9)
    db.commit()
    base='/orchestration/projects/project/reports'
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        async def listing(rows,logic='and',**params):
            response=await client.get(base,params=dict(filters=json.dumps(dict(conditions=rows,logic=logic)),**params));assert response.status_code==200,response.text
            return response.json()['data']
        assert (await listing([condition('name','_%','contains')]))['total']==1
        assert (await listing([condition('executorId','CURRENT_USER'),condition('passRate',100)]))['total']==1
        assert (await listing([condition('passRate',None,'is_empty')]))['items'][0]['id']==second.id
        assert (await listing([condition('createTime',['2026-10-08T00:00:00Z','2026-10-08T01:00:00Z'],'between')]))['total']==2
        assert (await listing([],sort='pass_rate',direction='desc'))['items'][0]['id']==first.id
        assert (await listing([],sort='pass_rate',direction='asc'))['items'][0]['id']==second.id
        rows=[condition('passRate',100),condition('resultStatus','running')]
        pages=[await listing(rows,'or',size=1,page=p) for p in (1,2)]
        assert all(page['total']==2 for page in pages)
        assert {r['id'] for page in pages for r in page['items']}=={first.id,second.id}
        assert (await listing(rows,'or',kind='GROUP'))['total']==0
        assert (await client.get(base.replace('/project/','/other/'),params=dict(filters=json.dumps(dict(conditions=rows,logic='or'))))).json()['data']['total']==0
        db.expire_all();assert db.get(PlanRun,first.id).report==frozen


@pytest.mark.parametrize('rows',[
    [condition('ownerId','owner')],[condition('passRate',True)],[condition('passRate',101)],
    [condition('kind','UNKNOWN')],[condition('triggerMode','webhook')],[condition('createTime','bad','gte')],
    [condition('completedAt',['2026-10-09','2026-10-08'],'between')],
])
def test_invalid_report_filters_return_validation_errors(rows):
    with pytest.raises(HTTPException) as error:parse(dict(conditions=rows))
    assert error.value.status_code==422


@pytest.mark.asyncio
async def test_real_group_creation_uses_current_period_and_exact_sqlite_fractional_bounds(reports_http):
    from datetime import timedelta,timezone
    from models.plan_orchestration import PlanGroup,PlanSettings
    from services.plan_group_execution import start_group_run,advance_group_runs
    from models.plan_group_execution import PlanGroupRunChild
    from utils.datetime_utils import beijing_now,BEIJING_TZ
    db,app,identity=reports_http
    db.add(PlanGroup(id='group-time',project_id='project',name='真实组时间'))
    db.flush();db.add(PlanSettings(plan_id='manual',group_id='group-time'));db.commit()
    before=beijing_now()-timedelta(minutes=1)
    group=await start_group_run(db,'group-time','owner');await advance_group_runs(db)
    child=db.query(PlanGroupRunChild).filter_by(run_id=group.id).one().plan_run_id
    after=beijing_now()+timedelta(minutes=1)
    base='/orchestration/projects/project/reports'
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        raw=dict(conditions=[condition('createTime',[before.isoformat(),after.isoformat()],'between')])
        response=await client.get(base,params=dict(filters=json.dumps(raw)))
        assert response.status_code==200,response.text
        assert {row['id'] for row in response.json()['data']['items']}=={group.id,child}
        ordinary=await client.get(base,params=dict(start_time=before.isoformat(),end_time=after.isoformat()))
        assert {row['id'] for row in ordinary.json()['data']['items']}=={group.id,child}
        # Verify the response's precise boundary using real dialect storage semantics.
        if db.get_bind().dialect.name=='sqlite':
            from datetime import datetime
            group.created_at=datetime(2026,10,8,19,0,0,123456);db.commit()
        data=(await client.get(base,params=dict(kind='GROUP'))).json()['data']['items'][0]
        instant=data['createTime']
        for operator,expected in [('gte',1),('lte',1),('gt',0),('lt',0)]:
            response=await client.get(base,params=dict(kind='GROUP',filters=json.dumps(dict(conditions=[condition('createTime',instant,operator)]))))
            assert response.status_code==200,response.text
            assert response.json()['data']['total']==expected,(operator,response.text)
