"""原生接口/场景配置、真实报告来源、权限、参数变更与版本回滚。"""
import json
from datetime import datetime
import httpx
import pytest
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from models import TestCase as Case, Project, ProjectMember, TestExecution
from models.test_suite import TestSuiteExecution as SuiteExecution
from models.native_case import NativeCaseConfig, ApiDefinition, ApiTestEnvironment
from models.case_governance import CaseVersion
from models.task_queue import TaskQueue
from api.v1.native_case import router
from api.v1.case_governance import router as governance_router

BASE='/projects/project/native-cases'
CANDIDATES='/orchestration/plans/plan/case-workspace/candidates'


@pytest.fixture
def native(workspace_http):
    db,app,identity=workspace_http
    app.include_router(router);app.include_router(governance_router)
    for cid, category in [('case-0','api'),('case-1','api'),('case-2','scenario')]:
        row=db.get(Case,cid);row.type=category;row.is_automated=True;row.status='failed'
    db.get(Case,'case-2').steps=[dict(action=f'已保存步骤{i}',expected='原结果') for i in range(3)]
    db.add(Project(id='other',name='另外项目',owner_id='owner'));db.flush()
    db.add(ApiDefinition(id='foreign',project_id='other',name='外部定义',protocol='TCP',path='/外部',parameters={},updated_by='owner'))
    db.add(ApiTestEnvironment(id='foreign-env',project_id='other',name='外部环境',address='隔离地址',updated_by='owner'))
    db.commit();return db,app,identity


def filters(category,*conditions,logic='and'):
    return dict(category=category,filters=json.dumps(dict(conditions=list(conditions),logic=logic)))


def c(field,operator,value=None):return dict(field=field,operator=operator,value=value)


async def prepare(client):
    body=dict(name='实际接口定义',protocol='HTTP',path='/诊断',parameters={'enabled':False,'count':0})
    response=await client.post(BASE+'/definitions',json=body);assert response.status_code==200,response.text
    definition=response.json()['data']['definitions'][0]
    response=await client.post(BASE+'/environments',json=dict(name='项目接口环境',address='http://127.0.0.1:1'))
    assert response.status_code==200,response.text
    env=response.json()['data']['environments'][0]
    return definition,env


def config(definition,env,**changes):
    return dict(state='PROCESSING',apiDefinitionId=definition['id'],environmentId=env['id'],parameters=definition['parameters'],expectedDefinitionRevision=definition['revision'],**changes)


@pytest.mark.asyncio
async def test_native_filters_use_real_definition_environment_reports_and_scene_steps(native):
    db,app,_=native
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        definition,env=await prepare(client)
        response=await client.put(BASE+'/cases/case-0',json=config(definition,env));assert response.status_code==200,response.text
        assert (await client.put(BASE+'/cases/case-2',json=dict(state='UNDERWAY',environmentId=env['id']))).status_code==200
        db.add(TestExecution(id='duplicate',case_id='case-0',executor_id='owner',result='failed',executed_at=datetime(2026,10,5)))
        db.add(SuiteExecution(id='duplicate',suite_id='suite-0',case_id='case-0',environment_id='node',executor_id='owner',result='passed',executed_at=datetime(2026,10,6)))
        db.add(SuiteExecution(id='latest',suite_id='suite-0',case_id='case-0',environment_id='node',executor_id='owner',result='passed',executed_at=datetime(2026,10,7)))
        db.commit()
        query=filters('api',c('protocol','belongs_to',['HTTP']),c('path','contains','诊断'),c('nativeState','belongs_to',['PROCESSING']),c('lastReportStatus','belongs_to',['SUCCESS']),c('apiChange','equals',False),c('environmentName','belongs_to',[env['id']]))
        data=(await client.get(CANDIDATES,params=query)).json()['data']
        assert data['total']==1 and data['items'][0]['id']=='case-0'
        assert data['items'][0]['status']=='failed' and data['items'][0]['lastReportStatus']=='SUCCESS'
        assert data['items'][0]['environmentLabel']=='项目接口环境'
        assert data['counts']['all']==1
        conditions=json.loads(query['filters'])['conditions']
        response=await client.post(CANDIDATES+'/views',params={'category':'api'},json=dict(name='真实原生组合',filters=dict(filterConditions=conditions,filterLogic='and')))
        assert response.status_code==200,response.text
        saved=(await client.get(CANDIDATES+'/views',params={'category':'api'})).json()['data'][0]
        assert saved['filters']['filterConditions']==conditions
        assert next(c['value'] for c in saved['filters']['filterConditions'] if c['field']=='apiChange') is False

        basic=(await client.get(CANDIDATES,params={'category':'api'})).json()['data']
        unconfigured=next(r for r in basic['items'] if r['id']=='case-1')
        assert unconfigured['nativeState'] is None and unconfigured['apiChange'] is None
        assert (await client.get(CANDIDATES,params=filters('api',c('nativeState','is_empty')))).json()['data']['total']==1
        scene=(await client.get(CANDIDATES,params=filters('scenario',c('nativeState','belongs_to',['UNDERWAY']),c('stepTotal','equals',3),c('environmentName','belongs_to',[env['id']])))).json()['data']
        assert scene['total']==1 and scene['items'][0]['stepTotal']==3
        db.add(TestExecution(id='newest',case_id='case-0',executor_id='owner',result='failed',executed_at=datetime(2026,10,8)));db.commit()
        assert (await client.get(CANDIDATES,params=query)).json()['data']['total']==0
        assert (await client.get(CANDIDATES,params=filters('api',c('lastReportStatus','belongs_to',['ERROR'])))).json()['data']['total']==1
        for category,field in [('functional','protocol'),('scenario','apiChange'),('api','stepTotal')]:
            assert (await client.get(CANDIDATES,params=filters(category,c(field,'equals',1)))).status_code==422
            views=CANDIDATES+'/views'
            assert (await client.post(views,params={'category':category},json=dict(name='错分类',filters={'filterConditions':[c(field,'equals',1)]}))).status_code==422
    assert db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_definition_parameter_changes_false_zero_sync_and_concurrent_revision(native):
    db,app,_=native
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        definition,env=await prepare(client);payload=config(definition,env)
        first=(await client.put(BASE+'/cases/case-0',json=payload)).json()['data'];assert not first['apiChange'] and first['revision']==1
        definition_body={k:definition[k] for k in ['name','protocol','path','parameters']}
        # 名称和路径变化不伪装成参数变更；JSON键顺序变化也不产生变更。
        response=await client.put(BASE+'/definitions/'+definition['id'],json={**definition_body,'path':'/新版路径','parameters':{'count':0,'enabled':False},'expectedRevision':1});assert response.status_code==200,response.text
        assert not (await client.get(BASE+'/cases/case-0')).json()['data']['apiChange']
        assert (await client.put(BASE+'/definitions/'+definition['id'],json={**definition_body,'expectedRevision':1})).status_code==409
        definition_body['parameters']={'enabled':0,'count':False}
        response=await client.put(BASE+'/definitions/'+definition['id'],json={**definition_body,'expectedRevision':2});assert response.status_code==200,response.text
        assert (await client.get(BASE+'/cases/case-0')).json()['data']['apiChange']
        version_count=db.query(CaseVersion).count()
        assert (await client.put(BASE+'/cases/case-0',json={**payload,'expectedRevision':1})).status_code==409
        assert db.query(CaseVersion).count()==version_count
        payload.update(expectedRevision=1,expectedDefinitionRevision=3,syncDefinition=True,parameters={'enabled':0,'count':False})
        synced=(await client.put(BASE+'/cases/case-0',json=payload)).json()['data']
        assert not synced['apiChange'] and synced['parameters']==payload['parameters'] and synced['revision']==2
        assert (await client.put(BASE+'/cases/case-0',json=payload)).status_code==409
        assert db.get(Case,'case-0').status=='failed'
    assert db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_native_configuration_permissions_foreign_references_and_snapshot_restore(native):
    db,app,identity=native
    db.add(ProjectMember(project_id='project',user_id='stranger',role='member'));db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        definition,env=await prepare(client);payload=config(definition,env)
        assert (await client.put(BASE+'/cases/case-0',json=payload)).status_code==200
        original=db.query(CaseVersion).filter_by(case_id='case-0').order_by(CaseVersion.version.desc()).first()
        old=original.snapshot['native_config'];assert old['parameters']==payload['parameters']
        for body in [{**payload,'apiDefinitionId':'foreign'},{**payload,'environmentId':'foreign-env'},{**payload,'environmentId':''},{**payload,'apiDefinitionId':''},{**payload,'state':'UNDERWAY'},{**payload,'apiChange':False}]:
            assert (await client.put(BASE+'/cases/case-0',json={**body,'expectedRevision':1})).status_code in {404,422}
        assert db.get(NativeCaseConfig,'case-0').revision==1
        assert (await client.put(BASE+'/cases/case-0',json={**payload,'state':'DONE','expectedRevision':1})).status_code==200
        latest=db.query(CaseVersion).filter_by(case_id='case-0').order_by(CaseVersion.version.desc()).first()
        restore=f'/projects/project/case-governance/cases/case-0/versions/{original.id}/restore'
        response=await client.post(restore,json=dict(expectedVersion=latest.version,reason='恢复实际原生配置'));assert response.status_code==200,response.text
        assert db.get(NativeCaseConfig,'case-0').state=='PROCESSING' and db.get(NativeCaseConfig,'case-0').revision==3
        identity['id']='stranger'
        assert (await client.get(BASE+'/catalog')).status_code==200
        assert (await client.get(BASE+'/cases/case-0')).json()['data']['canEdit'] is False
        assert (await client.put(BASE+'/cases/case-0',json={**payload,'expectedRevision':3})).status_code==403
        assert (await client.post(BASE+'/definitions',json=dict(name='越权',protocol='HTTP',path='/x'))).status_code==403
        assert (await client.get('/projects/other/native-cases/catalog')).status_code==403
    assert db.query(TaskQueue).count()==0


@pytest.mark.asyncio
async def test_native_parameter_types_versions_copy_and_type_conversion(native):
    from schemas.test_case import TestCaseCreate as CaseCreate, TestCaseUpdate as CaseUpdate
    from services.test_case_service import TestCaseService
    from schemas.case_governance import CaseBatchCopy
    from services.case_governance import batch_copy
    db, app, _ = native
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        definition, env = await prepare(client)
        payload = config(definition, env)
        assert (await client.put(BASE+'/cases/case-0',json=payload)).status_code==200
        previous = db.query(CaseVersion).filter_by(case_id='case-0').order_by(CaseVersion.version.desc()).first()
        changed = {**payload, 'expectedRevision':1, 'parameters':{'enabled':0, 'count':False}}
        assert (await client.put(BASE+'/cases/case-0',json=changed)).status_code==200
        current = db.query(CaseVersion).filter_by(case_id='case-0').order_by(CaseVersion.version.desc()).first()
        assert current.version == previous.version+1
        assert type(db.get(NativeCaseConfig,'case-0').parameters['enabled']) is int
        single = TestCaseService.create_test_case(db, CaseCreate(project_id='project',name='独立复制',type='api',copy_source_id='case-0',is_automated=True), 'owner')
        assert db.get(NativeCaseConfig,single.id).api_definition_id == definition['id']
        assert type(db.get(NativeCaseConfig,single.id).parameters['count']) is bool
        owner = db.get(__import__('models').User, 'owner')
        copies = batch_copy(db, owner, 'project', CaseBatchCopy(caseIds=['case-0'], moduleId=None)); db.commit()
        assert db.get(NativeCaseConfig,copies[0]).state=='PROCESSING'
        TestCaseService.update_test_case(db,'case-0',CaseUpdate(type='functional'),'owner')
        assert db.get(NativeCaseConfig,'case-0') is None
        latest = db.query(CaseVersion).filter_by(case_id='case-0').order_by(CaseVersion.version.desc()).first()
        response = await client.post(f'/projects/project/case-governance/cases/case-0/versions/{current.id}/restore',json=dict(expectedVersion=latest.version,reason='恢复原生类型与配置'))
        assert response.status_code==200,response.text
        assert db.get(Case,'case-0').type=='api'
        assert type(db.get(NativeCaseConfig,'case-0').parameters['enabled']) is int
        for condition in [c('stepTotal','equals',-.5),c('stepTotal','equals',True),c('stepTotal','contains',3),c('stepTotal','between',[1,2.5])]:
            assert (await client.get(CANDIDATES,params=filters('scenario',condition))).status_code==422
        for condition in [c('apiChange','equals',0),c('apiChange','not_equals',False)]:
            assert (await client.get(CANDIDATES,params=filters('api',condition))).status_code==422
    assert db.query(TaskQueue).count()==0
