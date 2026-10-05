"""跨项目保留主用例引用、来源授权、个人视图及执行冻结，绝不发送真实任务。"""
import json
import uuid
import httpx
import pytest
from fastapi import HTTPException
from models import Project, ProjectMember, TestCase as Case, TestPlan as Plan, TestSuite as Suite, Module, PlanCaseRelation
from models.plan_workspace import PlanNode
from models.case_governance import CaseVersion
from models.case_features import CaseIssue, CaseIssueLink
from models.task_queue import TaskQueue
from services.plan_tree import save_node
from services.plan_orchestration import start_plan_run
from services.suite_dispatch import build_suite_message
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from test_native_case_filters import native, prepare, config, c

BASE = '/orchestration/plans/plan/case-workspace'


@pytest.fixture
def cross(workspace_http):
    db, app, identity = workspace_http
    db.add_all([Project(id='source', name='来源项目', owner_id='stranger'), Project(id='hidden', name='未授权项目', owner_id='stranger')]); db.flush()
    db.add(ProjectMember(project_id='source', user_id='owner', role='member'))
    db.add(Module(id='source-module', project_id='source', name='来源模块')); db.flush()
    db.add_all([Case(id=f'foreign-{i}', project_id='source', name=f'来源用例{i}', case_code=f'FOREIGN-{i}', type='functional', steps=[],
        is_automated=False, created_by='owner', module_id='source-module' if i else None, tags=['来源标签']) for i in range(3)])
    db.add(Plan(id='source-plan', project_id='source', name='来源计划', plan_number='SOURCE', owner_id='stranger'))
    db.add(Case(id='hidden-case', project_id='hidden', name='隐藏用例', case_code='HIDDEN', type='functional', steps=[], created_by='stranger'))
    db.add(CaseIssue(id='source-bug', project_id='source', kind='defect', title='来源缺陷', created_by='owner', updated_by='owner')); db.flush()
    db.add(CaseIssueLink(issue_id='source-bug', case_id='foreign-1', created_by='owner')); db.commit()
    return db, app, identity


@pytest.mark.asyncio
async def test_source_choices_scope_original_references_counts_and_manual_history(cross):
    db, app, _ = cross
    before = db.query(Case).count()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        projects = (await client.get(BASE+'/candidates/projects')).json()['data']
        assert {p['id'] for p in projects} == {'project', 'source'}
        source = (await client.get(BASE+'/candidates', params=dict(projectId='source', size=1))).json()['data']
        assert source['total'] == 3 and source['projectId'] == 'source' and source['plans'] == [dict(id='source-plan', name='来源计划')]
        assert [m['id'] for m in source['modules']] == ['source-module'] and {s['id'] for s in source['suites']} == {'suite-0', 'suite-1'}
        assert (await client.get(BASE+'/candidates', params=dict(projectId='source', folder='source-module'))).json()['data']['total'] == 2
        body = dict(projectId='source', moduleMaps={'all':dict(selectAll=True,excludeIds=['foreign-2'])})
        assert (await client.post(BASE+'/candidates/selection', json=body)).json()['data']['count'] == 2
        result = await client.post(BASE+'/associate', json=body)
        assert result.status_code == 200, result.text
        assert result.json()['data']['added'] == 2
        listing = (await client.get(BASE, params=dict(tree_type='MODULE'))).json()['data']
        foreign = next(r for r in listing['items'] if r['caseId'] == 'foreign-1')
        assert foreign['projectId'] == 'source' and foreign['projectName'] == '来源项目' and foreign['moduleName'] == '来源模块' and foreign['bugCount'] == 1
        assert next(m for m in listing['modules'] if m['id'] == 'source')['count'] == 2
        assert next(m for m in listing['modules'] if m['id'] == 'source-module')['parentId'] == 'source'
        assert (await client.get(BASE, params=dict(tree_type='MODULE', folder='source_default'))).json()['data']['total'] == 1
        assert (await client.get(BASE, params=dict(tree_type='MODULE', folder='source'))).json()['data']['total'] == 2
        filters = json.dumps(dict(conditions=[c('projectId','equals','source')]))
        assert (await client.get(BASE, params=dict(filters=filters))).json()['data']['total'] == 2
        own = (await client.get(BASE, params=dict(mine=True))).json()['data']['items']
        assert {'foreign-0', 'foreign-1'} <= {r['caseId'] for r in own}
        result = await client.post(BASE+'/execute', json=dict(requestId=str(uuid.uuid4()), selections=[dict(source='legacy',id=foreign['associationId'])], result='passed'))
        assert result.status_code == 200, result.text
        history = (await client.get(BASE+'/execution', params=dict(source='legacy', associationId=foreign['associationId'], caseId='foreign-1'))).json()['data']
        assert history['history'][0]['caseSnapshot']['projectId'] == 'source'
        assert (await client.post(BASE+'/associate', json=dict(projectId='source',caseIds=['foreign-1']))).json()['data']['added'] == 0
    assert db.query(Case).count() == before and db.get(Case,'foreign-1').project_id == 'source'
    assert db.query(TaskQueue).count() == db.query(CaseVersion).count() == 0


@pytest.mark.asyncio
async def test_source_permission_explicit_project_and_saved_views_isolation(cross):
    db, app, identity = cross
    body = dict(projectId='source', selectAll=True, condition=dict(filters=dict(conditions=[c('createdBy','equals','CURRENT_USER')]), mine=True))
    view = dict(name='同名视图', filters=dict(filterConditions=[c('tags','belongs_to',['来源标签'])], filterLogic='and'))
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        for path in ['/candidates', '/candidates/views']:
            assert (await client.get(BASE+path, params=dict(projectId='hidden'))).status_code == 403
        assert (await client.post(BASE+'/associate', json=dict(projectId='hidden',caseIds=['hidden-case']))).status_code == 403
        assert (await client.post(BASE+'/associate', json=dict(caseIds=['foreign-1']))).status_code == 404
        assert (await client.post(BASE+'/associate', json=dict(projectId='source',caseIds=['foreign-1','case-2']))).status_code == 404
        assert (await client.post(BASE+'/candidates/selection', json=body)).json()['data']['count'] == 3
        a = await client.post(BASE+'/candidates/views', params=dict(projectId='source'), json=view)
        b = await client.post(BASE+'/candidates/views', json=view)
        assert a.status_code == b.status_code == 200
        view_id = a.json()['data']['id']
        assert (await client.delete(BASE+f'/candidates/views/{view_id}')).status_code == 404
        assert len((await client.get(BASE+'/candidates/views', params=dict(projectId='source'))).json()['data']) == 1
        db.query(ProjectMember).filter_by(project_id='source',user_id='owner').delete(); db.commit()
        assert (await client.post(BASE+'/candidates/selection', json=body)).status_code == 403
        assert (await client.post(BASE+'/associate', json=body)).status_code == 403
        assert {p['id'] for p in (await client.get(BASE+'/candidates/projects')).json()['data']} == {'project'}
    assert db.query(PlanCaseRelation).count() == 2 and db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_foreign_tree_preserves_instance_move_and_manual_freeze(cross):
    db, app, _ = cross
    plan = db.get(Plan,'plan')
    db.query(PlanCaseRelation).delete(); db.query(Suite).delete()
    save_node(db, plan, dict(name='原手工',nodeType='case',caseId='case-2')); db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        body = dict(projectId='source', caseIds=['foreign-1'])
        for _ in range(2):
            r = await client.post(BASE+'/associate',json=body)
            assert r.status_code == 200, r.text
        rows = db.query(PlanNode).filter_by(case_id='foreign-1').all()
        assert len(rows) == 2
        point = save_node(db,plan,dict(name='测试集',nodeType='point'))
        save_node(db,plan,dict(parentId=point.id),rows[0]);db.commit()
        # 直接节点入口不能绕过来源授权插入外部新用例。
        with pytest.raises(HTTPException):
            save_node(db,plan,dict(name='绕过',nodeType='case',caseId='foreign-2'))
        db.rollback()
    run = await start_plan_run(db,'plan','owner')
    assert len(run.case_snapshot) == 3
    foreign = [s for s in run.case_snapshot if s['id'] == 'foreign-1']
    assert len(foreign) == 2 and all(s['projectId'] == db.get(CaseVersion,s['versionId']).project_id == 'source' for s in foreign)
    assert db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
@pytest.mark.parametrize('category', ['api','scenario'])
async def test_native_foreign_scope_target_suites_and_dispatch_revalidation(native, category):
    db, app, _ = native
    db.add(Project(id='target',name='目标计划项目',owner_id='owner'));db.flush()
    db.get(Plan,'plan').project_id = 'target'; db.query(PlanCaseRelation).delete(); db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        definition, env = await prepare(client)
        if category == 'api':
            target = 'case-0'
            assert (await client.put('/projects/project/native-cases/cases/'+target,json=config(definition,env))).status_code == 200
            conditions = [c('protocol','equals','HTTP'),c('apiChange','equals',False)]
        else:
            target = 'case-2'
            assert (await client.put('/projects/project/native-cases/cases/'+target,json=dict(state='UNDERWAY', environmentId=env['id']))).status_code == 200
            conditions = [c('stepTotal','equals',3)]
        body = dict(projectId='project', category=category, selectAll=True, condition=dict(filters=dict(conditions=conditions)))
        r = await client.post(BASE+'/candidates/selection', json=body)
        assert r.status_code == 200, r.text
        assert r.json()['data']['count'] == 1
        assert (await client.post(BASE+'/associate', json=body)).json()['data']['added'] == 1
        suite = db.get(Suite,'suite-0'); suite.case_ids = [target]; db.commit()
        message = build_suite_message(db,suite,'只构建消息不发送','owner')
        assert message['case_ids'] == [target] and message['plan_id'] == 'plan'
        db.get(Project,'project').owner_id = 'stranger'; db.get(Project,'project').created_by = 'stranger'; db.commit()
        with pytest.raises(HTTPException) as exc:
            build_suite_message(db,suite,'只构建消息不发送','owner')
        assert exc.value.status_code == 403
    assert db.query(TaskQueue).count() == 0

@pytest.mark.asyncio
async def test_selected_local_suite_does_not_execute_or_freeze_unselected_foreign_automation(cross):
    db, _, _ = cross
    local = db.get(Case,'case-0')
    foreign = db.get(Case,'foreign-1'); foreign.is_automated = True
    db.add(PlanCaseRelation(plan_id='plan',case_id=foreign.id))
    db.query(ProjectMember).filter_by(project_id='source',user_id='owner').delete();db.commit()
    run = await start_plan_run(db,'plan','owner',suite_ids=['suite-0'],commit=False)
    assert foreign.id not in {c['id'] for c in run.case_snapshot}
    assert db.query(CaseVersion).filter_by(case_id=foreign.id).count() == 0
    assert {c['id'] for c in run.case_snapshot} == {'case-0'}
    db.rollback()
