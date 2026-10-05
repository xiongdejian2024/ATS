"""原生计划列表只读真实配置及实例报告；隔离库内验证，不创建执行队列。"""
import json
from datetime import datetime
import httpx
import pytest
from fastapi import HTTPException
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from models import TestCase as Case, TestPlan as Plan, PlanCaseRelation, TestExecution, Project, Module, ProjectMember
from models.native_case import NativeCaseConfig, ApiDefinition, ApiTestEnvironment
from models.plan_orchestration import PlanRun, PlanRunItem
from models.plan_case_view import PlanCaseSavedView
from models.task_queue import TaskQueue
from services.plan_tree import save_node
from services.native_case import fingerprint
from services.plan_case_filter import parse_plan_filters
BASE='/orchestration/plans/plan/case-workspace'

@pytest.fixture
def native_workspace(workspace_http):
    db,app,identity=workspace_http
    for cid,category in [('case-0','api'),('case-1','scenario')]:
        case=db.get(Case,cid);case.type=category;case.is_automated=True;case.status='failed'
    db.add(ApiDefinition(id='definition',project_id='project',name='实际接口',protocol='HTTP',path='/诊断',parameters={},updated_by='owner'))
    db.add(ApiTestEnvironment(id='native-env',project_id='project',name='原生用例配置环境',address='隔离配置地址',updated_by='owner'));db.flush()
    db.add(NativeCaseConfig(case_id='case-0',state='PROCESSING',api_definition_id='definition',environment_id='native-env',definition_fingerprint=fingerprint({}),parameters={},updated_by="owner"))
    db.add(NativeCaseConfig(case_id='case-1',state='UNDERWAY',environment_id='native-env',parameters={},updated_by='owner'))
    db.get(Case,'case-1').steps=[dict(action='场景步骤',expected='原预期')]
    db.commit();return db,app,identity


def c(field,operator,value=None):return dict(field=field,operator=operator,value=value)
def filters(category,*conditions,logic='and',**extra):return dict(category=category,filters=json.dumps(dict(conditions=list(conditions),logic=logic)),**extra)
def frozen_run(db,identifier,cases,day=1):
    rows=[dict(caseId=cid,associationId=association,result=result,executionId=f'execution-{identifier}') for cid,association,result in cases]
    db.add(PlanRun(id=identifier,plan_id='plan',executor_id='owner',plan_name='冻结计划',status='completed',created_at=datetime(2026,10,day),config_snapshot={},case_snapshot=[],manual_results={},report=dict(cases=rows,items=[dict(executionId=f'execution-{identifier}',environmentId='node')])));db.commit()

@pytest.mark.asyncio
async def test_native_values_and_plan_result_executor_environment_ignore_main_case_status(native_workspace):
    db,app,_=native_workspace
    relation=db.query(PlanCaseRelation).filter_by(plan_id='plan',case_id='case-0').one();relation.assigned_to='stranger'
    db.query(PlanCaseRelation).filter_by(plan_id='plan',case_id='case-1').one().execution_status='pass'
    db.add(TestExecution(id='global-failure',case_id='case-0',executor_id='stranger',result='failed',executed_at=datetime(2026,10,9)))
    frozen_run(db,'plan-success',[('case-0','case-0','passed')])
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        response=await client.get(BASE,params={'category':'api'});assert response.status_code==200,response.text
        data=response.json()['data'];assert data['total']==1
        row=data['items'][0]
        assert (row['nativeState'],row['protocol'],row['path'])==('PROCESSING','HTTP','/诊断')
        assert row['nativeResult']=='SUCCESS' and row['result']=='passed' and row['runId']=='plan-success'
        assert row['nativeExecutorId']=='owner' and row['nativeExecutorName']=='计划负责人' and row['assignedTo']=='stranger'
        assert row['environmentLabel']=='原生用例配置环境' and row['nativeExecutionEnvironmentName']=='软件节点'
        assert 'lastReportStatus' not in row and 'apiChange' not in row
        scene=(await client.get(BASE,params={'category':'scenario'})).json()['data']['items'][0]
        assert scene['nativeResult']=='PENDING' and scene['nativeExecutorId'] is None
        plan=(await client.get('/test-plans/plan')).json()['data']
        assert plan['totalCases']==2 and plan['executedCases']==1 and plan['caseStatusCounts']['pass']==1
        plans=(await client.get('/test-plans',params={'project_id':'project'})).json()['data']['items']
        assert plans[0]['executedCases']==1 and plans[0]['caseStatusCounts']['pass']==1
        params=filters('api',c('protocol','belongs_to',['HTTP']),c('path','contains','诊断'),c('nativeState','equals','PROCESSING'),c('environmentName','equals','native-env'),c('executorId','equals','CURRENT_USER'),c('result','equals','SUCCESS'))
        assert (await client.get(BASE,params=params)).json()['data']['total']==1
        assert (await client.get(BASE,params={'category':'api','result':'ERROR'})).json()['data']['total']==0
        assert (await client.get(BASE,params={'category':'api','executor':'stranger'})).json()['data']['total']==0
    assert db.query(TaskQueue).count()==0

@pytest.mark.asyncio
async def test_duplicate_instances_and_later_partial_report_keep_individual_latest_results(native_workspace):
    db,app,_=native_workspace;plan=db.get(Plan,'plan')
    point=save_node(db,plan,dict(name='API测试集',nodeType='point',category='api'))
    nodes=[save_node(db,plan,dict(name=f'实例{i}',nodeType='case',category='api',caseId='case-0',suiteId='suite-0',parentId=point.id if i==0 else None)) for i in range(2)];db.commit()
    frozen_run(db,'old-both',[('case-0',nodes[0].id,'passed'),('case-0',nodes[1].id,'fake_error')])
    frozen_run(db,'new-partial',[('case-0',nodes[1].id,'failed')],2)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        data=(await client.get(BASE,params={'category':'api'})).json()['data'];assert data['total']==2
        rows={row['associationId']:row for row in data['items']}
        assert rows[nodes[0].id]['nativeResult']=='SUCCESS' and rows[nodes[0].id]['runId']=='old-both'
        assert rows[nodes[1].id]['nativeResult']=='ERROR' and rows[nodes[1].id]['runId']=='new-partial'
        plan=(await client.get('/test-plans/plan')).json()['data']
        assert plan['totalCases']==2 and plan['executedCases']==2 and plan['caseStatusCounts']['pass']==1 and plan['caseStatusCounts']['fail']==1
        data=(await client.get(BASE,params=filters('api',c('result','equals','SUCCESS')))).json()['data'];assert data['total']==1 and data['counts']['all']==1 and data['counts']['default']==0
        assert next(row for row in data['collections'] if row['id']==point.id)['count']==1
        # 更新批次当前确实包含此实例时，以当前未执行状态覆盖旧结果。
        frozen_run(db,'new-pending',[('case-0',nodes[1].id,'pending')],3)
        data=(await client.get(BASE,params={'category':'api','result':'PENDING'})).json()['data'];assert data['total']==1 and data['items'][0]['associationId']==nodes[1].id
    assert db.query(TaskQueue).count()==0

@pytest.mark.asyncio
async def test_protocol_empty_multi_priority_source_metadata_and_scenario_steps(native_workspace):
    db,app,_=native_workspace
    db.add(Project(id='source',name='跨项目来源',owner_id='owner'));db.flush()
    db.add(Module(id='source-module',project_id='source',name='来源模块'));db.flush()
    db.add(Case(id='foreign-case',project_id='source',module_id='source-module',case_code='FOREIGN',name='跨项目API',type='api',is_automated=True,priority='P3',steps=[],created_by='owner'))
    db.add(ApiDefinition(id='source-definition',project_id='source',name='来源定义',protocol='TCP',path='/来源',parameters={},updated_by='owner'))
    db.add(ApiTestEnvironment(id='source-env',project_id='source',name='来源配置环境',address='隔离地址',updated_by='owner'));db.flush()
    db.add(NativeCaseConfig(case_id='foreign-case',state='DONE',api_definition_id='source-definition',environment_id='source-env',parameters={},updated_by='owner'))
    db.add(PlanCaseRelation(plan_id='plan',case_id='foreign-case',execution_order=2));db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        data=(await client.get(BASE,params={'category':'api','protocols':'HTTP,TCP'})).json()['data'];assert data['total']==2 and data['nativeOptions']['protocols']==['HTTP','TCP']
        assert {e['id'] for e in data['nativeOptions']['environments']}=={'native-env','source-env'}
        assert next(m for m in data['modules'] if m['id']=='source-module')['projectId']=='source'
        assert (await client.get(BASE,params={'category':'api','protocols':''})).json()['data']['total']==0
        assert (await client.get(BASE,params={'category':'api','protocols':'TCP','priority':'P2,P3'})).json()['data']['items'][0]['projectId']=='source'
        data=(await client.get(BASE,params=filters('scenario',c('stepTotal','equals',1),c('nativeState','equals','UNDERWAY')))).json()['data'];assert data['total']==1 and data['items'][0]['stepTotal']==1
        assert (await client.get(BASE,params={'category':'scenario','protocols':'HTTP'})).status_code==422

@pytest.mark.asyncio
async def test_workspace_views_native_category_validation_and_drawer_isolation(native_workspace):
    db,app,identity=native_workspace
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        body=dict(name='计划API状态',filters=dict(filterConditions=[c('nativeState','equals','PROCESSING'),c('result','equals','PENDING')],filterLogic='and'))
        response=await client.post(BASE+'/views',params={'category':'api'},json=body);assert response.status_code==200,response.text
        saved=response.json()['data'];assert (await client.get(BASE+'/views',params={'category':'api'})).json()['data'][0]['id']==saved['id']
        assert (await client.get(BASE+'/views',params={'category':'scenario'})).json()['data']==[]
        assert (await client.get(BASE+'/candidates/views',params={'category':'api'})).json()['data']==[]
        assert (await client.post(BASE+'/views',params={'category':'functional'},json=body)).status_code==422
        assert (await client.put(BASE+'/views/'+saved['id'],params={'category':'scenario'},json=body)).status_code==404
        assert db.query(PlanCaseSavedView).count()==1
        identity['id']='stranger';assert (await client.get(BASE,params={'category':'api'})).status_code==403
        assert (await client.get(BASE+'/views',params={'category':'api'})).status_code==403
        db.add(ProjectMember(project_id='project',user_id='stranger',role='tester'));db.commit()
        assert (await client.get(BASE+'/views',params={'category':'api'})).json()['data']==[]
        assert (await client.post(BASE+'/batch',json=dict(category='api',action='unlink',selections=[dict(source='legacy',id='missing')]))).status_code==403

@pytest.mark.asyncio
async def test_move_category_guard_and_unlink_do_not_mutate_main_cases_or_create_tasks(native_workspace):
    db,app,_=native_workspace;plan=db.get(Plan,'plan')
    api=save_node(db,plan,dict(name='API测试集',nodeType='point',category='api'))
    other=save_node(db,plan,dict(name='场景测试集',nodeType='point',category='scenario'));db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        data=(await client.get(BASE,params={'category':'api'})).json()['data'];row=data['items'][0];selection=dict(source=row['source'],id=row['associationId'])
        assert {r['id'] for r in data['collections']}=={api.id}
        assert (await client.post(BASE+'/batch',json=dict(category='api',action='move',selections=[selection],collectionId=other.id))).status_code==422
        assert (await client.post(BASE+'/batch',json=dict(category='api',action='move',selections=[selection],collectionId=api.id))).status_code==200
        assert (await client.get(BASE,params={'category':'api','folder':api.id})).json()['data']['items'][0]['collectionName']=='API测试集'
        assert (await client.post(BASE+'/batch',json=dict(category='api',action='unlink',selections=[selection,dict(source='legacy',id='missing')]))).status_code==404
        assert (await client.get(BASE,params={'category':'api'})).json()['data']['total']==1
        assert (await client.post(BASE+'/batch',json=dict(category='api',action='unlink',selections=[selection]))).status_code==200
        assert db.get(Case,row['caseId']) and db.get(Case,row['caseId']).deleted_at is None
    assert db.query(TaskQueue).count()==0


def test_native_workspace_filters_reject_primary_history_fields_and_invalid_category_numbers():
    for field in ['apiChange','lastReportStatus']:
        with pytest.raises(HTTPException):parse_plan_filters(dict(conditions=[c(field,'equals',False)]),'api')
    with pytest.raises(HTTPException):parse_plan_filters(dict(conditions=[c('protocol','equals','HTTP')]),'scenario')
    for value in [True,-1,1.5,'2']:
        with pytest.raises(HTTPException):parse_plan_filters(dict(conditions=[c('stepTotal','equals',value)]),'scenario')


@pytest.mark.asyncio
async def test_native_running_and_cancelled_follow_real_execution_item_without_sending_tasks(native_workspace):
    db,app,_=native_workspace
    run=PlanRun(id='active-native',plan_id='plan',executor_id='owner',plan_name='隔离活动样本',status='running',config_snapshot={'passThreshold':100},case_snapshot=[{'id':'case-0','name':'API用例','isAutomated':True,'projectId':'project','category':'api'}],manual_results={})
    db.add(run);db.flush()
    item=PlanRunItem(id='active-item',run_id=run.id,suite_id='suite-0',execution_id='isolated-running-id',environment_id='node',sequence=0,status='running',suite_snapshot={'name':'隔离模板','caseIds':['case-0'],'category':'api'})
    db.add(item);db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        row=(await client.get(BASE,params={'category':'api','result':'RUNNING'})).json()['data']['items'][0]
        assert row['result']=='running' and row['nativeResult']=='RUNNING' and row['nativeExecutorId']=='owner'
        plan=(await client.get('/test-plans/plan')).json()['data']
        assert plan['executedCases']==0 and plan['caseStatusCounts']['running']==1
        item.status='cancelled';run.status='cancelled';db.commit()
        row=(await client.get(BASE,params={'category':'api','result':'SKIPPED'})).json()['data']['items'][0]
        assert row['result']=='cancelled' and row['nativeResult']=='SKIPPED'
        plan=(await client.get('/test-plans/plan')).json()['data']
        assert plan['executedCases']==1 and plan['caseStatusCounts']['skip']==1
    assert db.query(TaskQueue).count()==0
