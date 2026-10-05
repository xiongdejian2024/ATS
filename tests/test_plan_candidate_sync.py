"""同步功能用例已有自动化关联，核验真实范围、分类目标与原子写入。"""
from datetime import datetime
import httpx
import pytest
from models import TestCase as Case, TestPlan as Plan, TestSuite as Suite, PlanCaseRelation
from models.case_features import CaseAutomationLink
from models.case_governance import CaseVersion
from models.plan_workspace import PlanNode
from models.task_queue import TaskQueue
from services.plan_tree import save_node
from test_plan_candidate_projects import cross
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab

BASE = '/orchestration/plans/plan/case-workspace'


@pytest.fixture
def sync_lab(cross):
    db, app, identity = cross
    for identifier, kind in [('api-0','api'), ('api-1','api'), ('scenario-0','scenario'), ('recycled','api')]:
        db.add(Case(id=identifier, project_id='source', name=identifier, case_code='SYNC-'+identifier,
                    type=kind, is_automated=True, steps=[], created_by='owner', deleted_at=datetime.now() if identifier == 'recycled' else None))
    db.flush()
    for source, target, kind in [('foreign-0','api-0','api'), ('foreign-1','api-0','api'), ('foreign-1','api-1','api'),
                                  ('foreign-0','scenario-0','scenario'), ('foreign-2','api-1','api'), ('foreign-0','recycled','api')]:
        db.add(CaseAutomationLink(case_id=source, target_case_id=target, category=kind, created_by='owner'))
    db.add(CaseAutomationLink(case_id='foreign-0', suite_id='suite-0', category='api', created_by='owner'))
    db.add(CaseAutomationLink(case_id='foreign-0', external_ref='只保留引用', category='scenario', created_by='owner'))
    db.add_all([PlanNode(id='api-parent',plan_id='plan',name='接口测试集',category='api',node_type='point'),
                PlanNode(id='scenario-parent',plan_id='plan',name='场景测试集',category='scenario',node_type='point')])
    db.commit()
    return db, app, identity


def body(**kwargs):
    return dict(projectId='source', caseIds=['foreign-0','foreign-1'], syncCase=True,
                apiCaseCollectionId='api-parent', apiScenarioCollectionId='scenario-parent', **kwargs)


@pytest.mark.asyncio
async def test_sync_limit_applies_to_expanded_targets_before_any_write(sync_lab,monkeypatch):
    db, app, _ = sync_lab
    import services.plan_candidate_selection as selection
    monkeypatch.setattr(selection,'LIMIT',1)
    # 仅选择一个功能用例，却展开两个接口用例，边界必须针对展开结果校验。
    selected = {**body(),'caseIds':['foreign-1']}
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        for endpoint in ['/candidates/selection','/associate']:
            r = await client.post(BASE+endpoint,json=selected)
            assert r.status_code == 422 and '同步最多关联' in r.json()['detail']
    assert db.query(PlanCaseRelation).count() == 2 and db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_sync_preview_real_links_targets_and_legacy_dedup(sync_lab):
    db, app, _ = sync_lab
    before = db.query(Case).count()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        catalog = (await client.get(BASE+'/candidates',params=dict(projectId='source'))).json()['data']
        assert [r['id'] for r in catalog['syncCollections']['api']] == ['default','api-parent']
        assert [r['id'] for r in catalog['syncCollections']['scenario']] == ['default','scenario-parent']
        preview = (await client.post(BASE+'/candidates/selection',json=body())).json()['data']
        assert preview['count'] == 2 and preview['sync']['api']['count'] == 2 and preview['sync']['scenario']['count'] == 1
        assert db.query(PlanCaseRelation).count() == 2
        result = await client.post(BASE+'/associate',json=body())
        assert result.status_code == 200, result.text
        assert result.json()['data'] == dict(added=2,synced=dict(api=2,scenario=1))
        actual = {r.case_id:r.collection_id for r in db.query(PlanCaseRelation)}
        assert actual['api-0'] == actual['api-1'] == 'api-parent' and actual['scenario-0'] == 'scenario-parent'
        assert 'recycled' not in actual and 'foreign-2' not in actual
        assert (await client.post(BASE+'/associate',json=body())).json()['data'] == dict(added=0,synced=dict(api=0,scenario=0))
    assert db.query(Case).count() == before and db.query(TaskQueue).count() == db.query(CaseVersion).count() == 0


@pytest.mark.asyncio
async def test_switch_off_blank_category_default_and_current_module_exclusion(sync_lab):
    db, app, _ = sync_lab
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        for bad in [{**body(),'category':'api'}, {**body(),'syncCase':False}, {**body(),'syncCase':'true'}, {**body(),'apiCaseCollectionId':'scenario-parent'}]:
            r = await client.post(BASE+'/associate',json=bad)
            assert r.status_code == 422, r.text
        assert db.query(PlanCaseRelation).count() == 2
        selected = dict(projectId='source',moduleMaps={'all':dict(selectAll=True,excludeIds=['foreign-1','foreign-2'])},syncCase=True,apiCaseCollectionId='default')
        preview = (await client.post(BASE+'/candidates/selection',json=selected)).json()['data']
        assert preview['count'] == 1 and preview['sync']['api']['count'] == 1 and preview['sync']['scenario']['count'] == 0
        # 预览之后新增一条真实关系；写入须重新查询，不能照搬预览计数。
        db.add(CaseAutomationLink(case_id='foreign-0',target_case_id='api-1',category='api',created_by='owner'));db.commit()
        r = await client.post(BASE+'/associate',json=selected)
        assert r.json()['data'] == dict(added=1,synced=dict(api=2,scenario=0))
        assert all(r.collection_id is None for r in db.query(PlanCaseRelation).filter(PlanCaseRelation.case_id.in_(['api-0','api-1'])))
        r = await client.post(BASE+'/associate',json=dict(projectId='source',caseIds=['foreign-1'],syncCase=True))
        assert r.json()['data'] == dict(added=1,synced=dict(api=0,scenario=0))


@pytest.mark.asyncio
async def test_tree_sync_repeated_instances_require_complete_target_suites(sync_lab):
    db, app, _ = sync_lab
    db.query(PlanCaseRelation).delete()
    save_node(db,db.get(Plan,'plan'),dict(name='原手工用例',nodeType='case',caseId='case-2'))
    db.get(Suite,'suite-0').case_ids = ['api-0','api-1']
    db.get(Suite,'suite-1').case_ids = ['scenario-0'];db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        preview = (await client.post(BASE+'/candidates/selection',json=body())).json()['data']
        assert preview['sync']['api'] == dict(count=3,compatibleSuiteIds=['suite-0'])
        assert preview['sync']['scenario'] == dict(count=1,compatibleSuiteIds=['suite-1'])
        assert (await client.post(BASE+'/associate',json=body())).status_code == 422
        assert (await client.post(BASE+'/associate',json=body(syncApiSuiteId='suite-1',syncScenarioSuiteId='suite-1'))).status_code == 422
        assert db.query(PlanNode).filter_by(node_type='case').count() == 1
        for _ in range(2):
            r = await client.post(BASE+'/associate',json=body(syncApiSuiteId='suite-0',syncScenarioSuiteId='suite-1'))
            assert r.status_code == 200, r.text
            assert r.json()['data'] == dict(added=2,synced=dict(api=3,scenario=1))
        assert db.query(PlanNode).filter_by(case_id='api-0',suite_id='suite-0',parent_id='api-parent').count() == 4
        assert db.query(PlanNode).filter_by(case_id='scenario-0',suite_id='suite-1',parent_id='scenario-parent').count() == 2
    assert db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_sync_target_project_change_and_late_failure_roll_back_all(sync_lab,monkeypatch):
    db, app, _ = sync_lab
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
        db.get(Case,'api-0').project_id = 'hidden';db.commit()
        assert (await client.post(BASE+'/associate',json=body())).status_code == 409
        assert db.query(PlanCaseRelation).count() == 2
        db.get(Case,'api-0').project_id = 'source';db.query(PlanCaseRelation).delete()
        save_node(db,db.get(Plan,'plan'),dict(name='手工',nodeType='case',caseId='case-2'))
        db.get(Suite,'suite-0').case_ids=['api-0','api-1','scenario-0'];db.commit()
        import services.plan_case_workspace as service
        original = service.save_node
        def fail_sync(*args,**kwargs):
            if args[2]['category'] == 'scenario': raise RuntimeError('模拟最后一类同步写入失败')
            return original(*args,**kwargs)
        monkeypatch.setattr(service,'save_node',fail_sync)
        with pytest.raises(RuntimeError,match='模拟最后一类'):
            await client.post(BASE+'/associate',json=body(syncApiSuiteId='suite-0',syncScenarioSuiteId='suite-0'))
        assert db.query(PlanNode).filter_by(node_type='case').count() == 1
        assert db.query(TaskQueue).count() == db.query(CaseVersion).count() == 0
