"""计划首页高级视图、真实计数和按组分页的软件回归。"""
import json
from datetime import date, timedelta
import pytest
import httpx
from fastapi import HTTPException
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from models import TestPlan as Plan, Project, User
from models.plan_case_view import PlanCaseSavedView
from models.plan_workspace import PlanWorkspace, PlanGroupWorkspace, PlanModule, PlanFollow
from models.plan_orchestration import PlanGroup, PlanSettings
from services.test_plan_service import TestPlanService
from services.plan_index_filter import parse


def condition(field, value=None, operator="equals"):
    return dict(field=field,value=value,operator=operator)


def filters(*rows, logic="and"):
    return json.dumps(dict(conditions=list(rows),logic=logic))


@pytest.mark.asyncio
async def test_private_plan_views_owner_namespace_quota_and_validation(workspace_http):
    db,app,identity=workspace_http
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url="http://test") as client:
        path='/orchestration/projects/project/index-views'
        body=dict(name="负责的计划",filters=dict(filterConditions=[condition("ownerId","CURRENT_USER")],filterLogic="and"))
        response=await client.post(path,json=body)
        assert response.status_code==200,response.text
        row=response.json()['data']; assert db.get(PlanCaseSavedView,row['id']).category=='plan-index'
        renamed=await client.put(path+'/'+row['id'],json=dict(name="个人计划"))
        assert renamed.json()['data']['filters']==body['filters']
        assert (await client.post(path,json=dict(body,name="个人计划"))).status_code==409
        for i in range(9):assert (await client.post(path,json=dict(body,name=f"视图{i}"))).status_code==200
        assert (await client.post(path,json=dict(body,name="超额"))).status_code==409
        db.add(PlanCaseSavedView(project_id='project',owner_id='owner',category='review-index',name='评审',filters={}))
        db.commit()
        assert len((await client.get(path)).json()['data'])==10
        for invalid in (None,dict(scope="all"),dict(filterConditions=[condition("createdBy","owner")])):
            assert (await client.put(path+'/'+row['id'],json=dict(name='非法',filters=invalid))).status_code==422
        identity['id']='stranger'
        assert (await client.get(path)).status_code==403
        assert (await client.delete(path+'/'+row['id'])).status_code==403
        identity['id']='owner';db.get(User,'owner').status=False;db.commit()
        assert (await client.put(path+'/'+row['id'],json=dict(name="停用"))).status_code==403
        db.get(User,'owner').status=True;db.commit()
        assert (await client.delete(path+'/'+row['id'])).status_code==200


@pytest.mark.asyncio
async def test_sql_counts_paging_groups_or_scope_and_effective_status_are_readonly(workspace_http):
    db,app,identity=workspace_http
    first=db.get(Plan,'plan');first.name='Literal_%';first.end_date=date.today()-timedelta(days=1)
    db.add(Project(id='other',name='其他项目',owner_id='stranger'))
    db.add(Plan(id='other-plan',project_id='other',owner_id='stranger',name='Literal_%',plan_number='TP-OTHER'))
    db.add(Plan(id='second',project_id='project',owner_id='owner',name='Second',plan_number='TP-002',status='completed'))
    db.add(PlanModule(id='mod',project_id='project',name='组模块'))
    db.add(PlanGroup(id='group',project_id='project',name='组'))
    db.flush()
    db.add(PlanSettings(plan_id='plan',group_id='group'))
    db.add(PlanSettings(plan_id='second',group_id='group'))
    db.add(PlanGroupWorkspace(group_id='group',module_id='mod'))
    db.add(PlanWorkspace(plan_id='plan',tags=['回归_%','诊断']))
    db.add(PlanWorkspace(plan_id='second',tags=[],archived=True))
    db.add(PlanFollow(plan_id='plan',user_id='owner'));db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url="http://test") as client:
        async def listing(raw,**params):
            response=await client.get('/test-plans',params=dict(project_id='project',filters=raw,**params))
            assert response.status_code==200,response.text
            return response.json()['data']
        data=await listing(filters(condition('name','_%','contains')))
        assert data['total']==1 and data['items'][0]['id']=='plan'
        assert data['items'][0]['status']=='overdue' and db.get(Plan,'plan').status=='not_started'
        assert (await listing(filters(condition('status','overdue'))))['total']==1
        assert (await listing(filters(),status='overdue'))['total']==1
        assert (await listing(filters(),status='not_started'))['total']==0
        assert (await listing(filters(condition('ownerId','CURRENT_USER'),condition('followed','true'),condition('moduleId','mod'),condition('groupId','group'),condition('tags',1,'count_gt'))))['total']==1
        for navigation in (dict(group_id='group'),dict(module_id='mod',include_descendants=True),dict(group_id='group',module_id='mod',include_descendants=True)):
            assert (await listing(filters(condition('moduleId','mod')),**navigation))['total']==1
        raw=filters(condition('name','_%','contains'),condition('archived','true'),logic='or')
        pages=[await listing(raw,page=i,size=1,group_id='group') for i in (1,2)]
        assert all(p['total']==2 for p in pages)
        assert {item['id'] for p in pages for item in p['items']}=={'plan','second'}
        assert (await listing(raw,group_id='__ungrouped__'))['total']==0
        assert db.get(Plan,'plan').status=='not_started'
        for params in (dict(page=0),dict(size=0),dict(size=101),dict(filters='x'*20001)):
            assert (await client.get('/test-plans',params=dict(project_id='project',**params))).status_code==422


@pytest.mark.parametrize('rows',[
    [condition('createdBy','owner')],[condition('archived',True)],
    [condition('status','arbitrary')],[condition('tags',9223372036854775808,'count_gt')],
    [condition('tags',True,'count_lt')],[condition('ownerId',{},'equals')],
    [condition('endDate','not-date','gte')],[condition('name','x','gt')],
    [condition('startDate',['2026-10-09','2026-10-08'],'between')],
])
def test_plan_filter_rejects_unknown_unbounded_or_untyped_values(rows):
    with pytest.raises(HTTPException) as error:parse(dict(conditions=rows))
    assert error.value.status_code==422


@pytest.mark.asyncio
async def test_plan_only_permission_loads_members_and_private_views_without_case_permission(workspace_http):
    from models import Permission, ProjectPermission
    db,app,identity=workspace_http
    permission=Permission(code="test_plan:read",name="查看计划",resource="test_plan",action="read")
    db.add(permission);db.flush()
    db.add(ProjectPermission(project_id="project",user_id="stranger",permission_id=permission.id));db.commit()
    identity["id"]="stranger"
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url="http://test") as client:
        response=await client.get('/orchestration/projects/project/members')
        assert response.status_code==200,response.text
        assert {row['id'] for row in response.json()['data']}=={'owner'}
        body=dict(name="只读个人视图",filters=dict(filterConditions=[condition("ownerId","CURRENT_USER")],filterLogic="and"))
        assert (await client.post('/orchestration/projects/project/index-views',json=body)).status_code==200
        db.query(ProjectPermission).filter_by(user_id='stranger').delete();db.commit()
        assert (await client.get('/orchestration/projects/project/members')).status_code==403
        assert (await client.post('/orchestration/projects/project/index-views',json=dict(body,name="撤权"))).status_code==403
