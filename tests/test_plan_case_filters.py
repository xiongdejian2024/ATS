"""计划高级筛选与个人视图验收，所有数据和执行记录均在隔离库。"""

import json
from uuid import uuid4
from datetime import datetime
import httpx
import pytest
from test_plan_workspace import workspace_http
from test_plan_orchestration import plan_lab
from models import TestCase as Case, TestPlan as Plan, Project, ProjectMember, CaseAttachment
from models.case_features import CaseIssue, CaseIssueLink, CaseTemplate
from models.case_governance import CaseVersion, CaseSavedView
from models.plan_case_view import PlanCaseSavedView
from models.task_queue import TaskQueue
from services.plan_tree import save_node
from services.plan_case_filter import parse_plan_filters
from fastapi import HTTPException

BASE = '/orchestration/plans/plan/case-workspace'


def test_bug_count_rejects_negative_fraction_boolean_text_and_array_operators():
    for value in [-1, 1.5, True, '1']:
        with pytest.raises(HTTPException) as exc:
            parse_plan_filters(dict(conditions=[condition('bugCount', 'equals', value)]))
        assert exc.value.status_code == 422
    with pytest.raises(HTTPException) as exc:
        parse_plan_filters(dict(conditions=[condition('bugCount', 'count_gt', 1)]))
    assert exc.value.status_code == 422


def condition(field, operator, value=None):
    return dict(field=field, operator=operator, value=value)


def params(*rows, logic='and', **extra):
    return dict(filters=json.dumps(dict(conditions=list(rows), logic=logic)), **extra)


@pytest.mark.asyncio
async def test_instance_result_executor_counts_and_refinement_do_not_collapse_duplicates(workspace_http):
    db, app, identity = workspace_http
    plan = db.get(Plan, 'plan')
    db.get(Case, 'case-0').is_automated = False
    point = save_node(db, plan, dict(name='范围', nodeType='point'))
    nodes = [save_node(db, plan, dict(name=f'实例{i}', nodeType='case', category='functional', caseId='case-0',
                                     parentId=point.id if i == 0 else None, assignedTo='owner' if i == 0 else None)) for i in range(2)]
    # 主用例状态和默认执行人与计划关联故意不同。
    db.get(Case, 'case-0').status = 'failed'
    db.get(Case, 'case-0').executor_id = 'stranger'
    db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        result = await client.post(BASE + '/execute', json=dict(requestId=str(uuid4()), selections=[dict(source='node', id=nodes[0].id)], result='passed'))
        assert result.status_code == 200, result.text
        all_rows = (await client.get(BASE)).json()['data']
        assert all_rows['total'] == 2 and len({r['id'] for r in all_rows['items']}) == 2
        data = (await client.get(BASE, params=params(condition('result', 'belongs_to', ['passed']),
                condition('executorId', 'belongs_to', ['CURRENT_USER']), search='旧搜索不应截断', folder='旧目录'))).json()['data']
        assert data['total'] == 1 and data['items'][0]['associationId'] == nodes[0].id
        assert data['counts']['all'] == 1 and data['counts']['default'] == 0
        assert next(r['count'] for r in data['collections'] if r['id'] == point.id) == 1
        data = (await client.get(BASE, params=params(condition('executorId', 'is_empty'), condition('result', 'equals', 'pending')))).json()['data']
        assert data['total'] == 1 and data['items'][0]['associationId'] == nodes[1].id
        data = (await client.get(BASE, params=params(condition('collectionId', 'belongs_to', ['__default__'])))).json()['data']
        assert data['items'][0]['associationId'] == nodes[1].id
        assert (await client.get(BASE, params=params(condition('result', 'equals', 'passed'), refine=True, result='pending'))).json()['data']['total'] == 0
        assert (await client.get(BASE, params=params(condition('name', 'contains', '用例'), refine=True, search='不存在'))).json()['data']['total'] == 0
        data = (await client.get(BASE, params=params(condition('name', 'contains', '不存在'), condition('result', 'equals', 'pending'), condition('id', 'contains', ''), logic='or', view='mind', size=1))).json()['data']
        assert data['total'] == 1 and len(data['items']) == 1
        identity['id'] = 'stranger'
        assert (await client.get(BASE, params=params(condition('executorId', 'belongs_to', ['CURRENT_USER'])))).status_code == 403
    assert db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_project_related_values_dates_custom_fields_and_recycled_rows_are_readonly(workspace_http):
    db, app, identity = workspace_http
    case = db.get(Case, 'case-0')
    case.requirement_ref = '旧需求'
    case.tags = ['回归', '诊断']
    case.created_at = datetime(2026, 10, 5, 0)
    case.updated_by = 'owner'
    case.template_id = 'typed'
    case.custom_fields = {'deadline': '2026-10-05', 'enabled': False, 'score': 0}
    case.deleted_at = datetime(2026, 10, 5, 9)
    db.add(CaseTemplate(id='typed', project_id='project', name='日期模板', created_by='owner',
                        fields=[dict(key='deadline', type='date'), dict(key='enabled', type='boolean'), dict(key='score', type='number')]))
    db.add(CaseAttachment(case_id=case.id, file_name='诊断说明.pdf', file_path='隔离假路径'))
    for identifier, kind, title in [('requirement', 'requirement', '诊断需求'), ('defect', 'defect', '真实缺陷')]:
        db.add(CaseIssue(id=identifier, project_id='project', kind=kind, title=title, created_by='owner', updated_by='owner'))
        db.flush(); db.add(CaseIssueLink(issue_id=identifier, case_id=case.id, created_by='owner'))
    from models.plan_case_defect import PlanCaseDefect
    from models import PlanCaseRelation
    association = db.query(PlanCaseRelation).filter_by(plan_id='plan', case_id=case.id).one()
    db.add(PlanCaseDefect(plan_id='plan', association_key=f'legacy:{association.id}:{case.id}', case_id=case.id, issue_id='defect', case_snapshot={'name':case.name}, created_by='owner', updated_by='owner'))
    db.get(Case, 'case-1').created_by = 'stranger'
    db.commit()
    versions = db.query(CaseVersion).count()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        rows = [condition('projectId', 'belongs_to', ['project']), condition('attachment', 'contains', '说明'),
                condition('requirementRef', 'contains', '诊断'), condition('bugCount', 'equals', 1),
                condition('tags', 'count_gt', 1), condition('updatedBy', 'belongs_to', ['CURRENT_USER']),
                condition('createdAt', 'between', ['2026-10-05T00:00:00Z', '2026-10-05T01:00:00Z']),
                condition('customFields.deadline', 'between', ['2026-10-05', '2026-10-05']),
                condition('customFields.enabled', 'equals', False), condition('customFields.score', 'equals', 0),
                condition('reviewResult', 'belongs_to', ['not_reviewed'])]
        for row in rows:
            individual = (await client.get(BASE, params=params(row))).json()['data']
            assert any(r['caseId'] == 'case-0' for r in individual['items']), row
        response = await client.get(BASE, params=params(*rows))
        assert response.status_code == 200, response.text
        assert [r['caseId'] for r in response.json()['data']['items']] == ['case-0']
        assert (await client.get(BASE, params=params(condition('requirementRef', 'not_contains', '诊断')))).json()['data']['total'] == 1
        assert (await client.get(BASE, params=params(condition('attachment', 'is_empty')))).json()['data']['total'] == 1
        assert (await client.get(BASE, params=params(mine=True))).json()['data']['total'] == 1
        assert (await client.get(BASE, params=params(condition('name', 'contains', '用例 1'), mine=True))).json()['data']['total'] == 0
        for raw in ['{', '{"logic":"错"}', json.dumps(dict(conditions=[condition('outside', 'equals', 'x')])),
                    json.dumps(dict(conditions=[condition('createdAt', 'between', ['错误', '日期'])]))]:
            assert (await client.get(BASE, params={'filters': raw})).status_code == 422
    assert case.custom_fields == {'deadline': '2026-10-05', 'enabled': False, 'score': 0}
    assert db.query(CaseVersion).count() == versions and db.query(TaskQueue).count() == 0


@pytest.mark.asyncio
async def test_views_crud_limit_owner_project_category_and_main_case_isolation(workspace_http):
    db, app, identity = workspace_http
    db.add(Project(id='other', name='另项目', owner_id='owner')); db.flush()
    db.add(Plan(id='other-plan', project_id='other', name='另计划', owner_id='owner', plan_number='OTHER'))
    db.add(Plan(id='same-project-plan', project_id='project', name='同项目计划', owner_id='owner', plan_number='SAME'))
    db.add(ProjectMember(project_id='project', user_id='stranger', role='member')); db.commit()
    url = BASE + '/views'
    filters = dict(filterConditions=[condition('result', 'equals', 'pending')], filterLogic='and')
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        first = (await client.post(url, json=dict(name='原视图', filters=filters))).json()['data']
        assert (await client.get('/orchestration/plans/same-project-plan/case-workspace/views')).json()['data'][0]['id'] == first['id']
        assert (await client.get('/orchestration/plans/other-plan/case-workspace/views')).json()['data'] == []
        assert (await client.get(url, params={'category': 'api'})).json()['data'] == []
        update = await client.put(url + '/' + first['id'], json=dict(name='重命名'))
        assert update.json()['data']['filters'] == filters
        assert (await client.put(url + '/' + first['id'], json=dict(name='重命名', filters={}))).json()['data']['filters'] == {}
        for bad in [None, {'mine': True}, {'filterLogic': '错'}, {'filterConditions': [condition('bad', 'equals', 1)]}]:
            assert (await client.put(url + '/' + first['id'], json=dict(name='错误', filters=bad))).status_code == 422
        assert (await client.post(url, json=dict(name='重命名', filters={}))).status_code == 409
        identity['id'] = 'stranger'
        assert (await client.get(url)).json()['data'] == []
        assert (await client.put(url + '/' + first['id'], json=dict(name='越权'))).status_code == 404
        assert (await client.delete(url + '/' + first['id'])).status_code == 404
        assert (await client.post(url, json=dict(name='只读成员个人视图', filters={}))).status_code == 200
        identity['id'] = 'owner'
        for i in range(9):
            assert (await client.post(url, json=dict(name=f'视图{i}', filters=filters))).status_code == 200
        assert (await client.post(url, json=dict(name='超额', filters={}))).status_code == 409
        assert (await client.post(url, params={'category': 'api'}, json=dict(name='分类独立', filters={}))).status_code == 200
        assert (await client.delete(url + '/' + first['id'])).status_code == 200
        assert (await client.post(url, json=dict(name='删除后补充', filters={}))).status_code == 200
    assert db.query(CaseSavedView).count() == 0 and db.query(PlanCaseSavedView).count() == 12
    assert db.query(CaseVersion).count() == 0 and db.query(TaskQueue).count() == 0
