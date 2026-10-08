"""冻结配置/测试集/步骤缺陷分析的真实批次回归。"""
from copy import deepcopy
import json
import pytest
from sqlalchemy import event
from test_plan_orchestration import plan_lab
from test_plan_tree import node
from test_plan_group_execution import group_lab
from models import TestCase as Case, User
from models.plan_workspace import PlanNode
from models.plan_orchestration import PlanRunItem, PlanSettings
from models.case_features import CaseIssue
from schemas.plan_orchestration import ManualResultInput
from services.plan_orchestration import start_plan_run, record_manual_result, advance_plan_runs, build_report
from services.plan_collaboration import enriched_report
from services.plan_group_execution import start_group_run, run_data
from services.plan_report_details import analyse


@pytest.mark.asyncio
async def test_frozen_test_sets_duplicates_step_defects_and_no_read_writes(plan_lab):
    db, sent = plan_lab
    root = node(db, nodeType='point', caseId=None, name='父集')
    point = node(db, nodeType='point', caseId=None, parentId=root.id, name='执行时集')
    first = node(db, parentId=point.id, name='实例甲')
    second = node(db, name='默认实例')
    db.get(Case, 'case-2').steps = [{'action': '步骤一'}, {'action': '步骤二'}]
    defect = CaseIssue(id='defect-frozen', project_id='project', title='当时缺陷', status='open', kind='defect', created_by='owner', updated_by='owner')
    db.add(defect); db.commit()
    run = await start_plan_run(db, 'plan', 'owner')
    step = dict(index=0, result='failed', actual='', notes='', defectIds=[defect.id], attachments=[])
    record_manual_result(db, run.id, first.id, ManualResultInput(result='failed', stepResults=[step, dict(step, index=1)]), 'owner')
    record_manual_result(db, run.id, second.id, ManualResultInput(result='failed', stepResults=[step]), 'owner')
    await advance_plan_runs(db)
    assert run.status == 'failed'
    frozen = deepcopy(run.report)
    point.name = '今日集'; defect.title = '今日缺陷'; defect.status = 'closed'
    db.get(Case, 'case-2').name = '今日用例'; db.commit()
    writes = []
    def observe(conn, cursor, statement, parameters, context, many):
        if statement.lstrip().split()[0].upper() in {'INSERT','UPDATE','DELETE'}: writes.append(statement)
    event.listen(db.get_bind(), 'before_cursor_execute', observe)
    try: payload = enriched_report(db, run)
    finally: event.remove(db.get_bind(), 'before_cursor_execute', observe)
    report = payload['reportDetails']
    custom = next(s for s in report['testSets'] if s['testSet']['id'] == point.id)
    assert custom['testSet']['name'] == '执行时集'
    assert [p['name'] for p in custom['testSet']['path']] == ['父集', '执行时集']
    assert custom['total'] == 1 and custom['counts']['failed'] == 1 and custom['defectCount'] == 1
    assert next(s for s in report['testSets'] if s['testSet']['id'] == 'DEFAULT')['total'] == 1
    assert report['defects'][0]['title'] == '当时缺陷' and report['defects'][0]['occurrenceCount'] == 3
    assert {o['associationId'] for o in report['defects'][0]['occurrences']} == {first.id, second.id}
    assert all(o['status'] == 'open' for o in report['defects'][0]['occurrences'])
    assert run.report == frozen and not writes and not sent


@pytest.mark.asyncio
async def test_configuration_allowlist_uses_frozen_values_not_current_policy(plan_lab):
    db, sent = plan_lab
    point = node(db, nodeType='point', caseId=None, config={'resourcePool':['node']})
    leaf = node(db, parentId=point.id, category='api', caseId='case-0', suiteId='suite-0')
    run = await start_plan_run(db, 'plan', 'owner', defer=True)
    item = db.query(PlanRunItem).filter_by(run_id=run.id).one()
    frozen = dict(item.suite_snapshot, executionCommand='synthetic-secret-command', gitRepoUrl='https://synthetic.invalid/private',
        nativeCases=[{'headers': {'Authorization':'synthetic-secret'}}],
        executionConfig={'executionMode':'parallel','retryOnFailure':True,'retryTimes':2,'requestEnvironmentId':'request-env',
                         'password':'synthetic-secret'}, resourcePool=['node'])
    item.suite_snapshot = frozen
    db.add(PlanSettings(plan_id='plan', execution_mode='parallel'))
    point.name = '当前名称'; point.config = {'environmentId':'node'}; db.commit()
    result = enriched_report(db, run)['reportDetails']['configuration']
    assert result['policies'][0]['executionMode'] == 'serial'
    row = result['items'][0]
    assert row['testSet']['id'] == point.id and row['environmentId'] == 'node' and row['resourcePool'] == ['node']
    assert row['executionConfig']['executionMode'] == 'parallel' and row['executionConfig']['retryTimes'] == 2
    text = json.dumps(result)
    assert 'synthetic-secret' not in text and 'executionCommand' not in text and 'gitRepoUrl' not in text and 'password' not in text
    assert not sent


@pytest.mark.asyncio
async def test_group_analysis_isolates_child_identity_and_legacy_unknown(group_lab):
    db, sent = group_lab
    run = await start_group_run(db, 'group', 'owner')
    payload = run_data(db, run)
    sets = payload['reportDetails']['testSets']
    assert sum(s['total'] for s in sets) == payload['report']['total'] == 3
    assert len({s['planRunId'] for s in sets}) == 2
    assert all(s['testSet']['id'] == 'DEFAULT' for s in sets)
    policies = payload['reportDetails']['configuration']['policies']
    assert policies[0]['key'] == 'GROUP' and len(policies) == 3
    assert len(payload['reportDetails']['configuration']['items']) == 2
    assert not sent


def test_shared_defect_distinguishes_frozen_status_and_deduplicates_exact_step():
    def case(run, association, title, status):
        step = dict(index=0, defects=[dict(id='same', title=title, status=status)] * 2)
        return dict(planRunId=run, associationId=association, caseId='master', category='functional', result='failed',
                    testSet=dict(id='same-set', name='冻结集', path=[]), stepResults=[step])
    result = analyse([case('one','copy','旧标题','open'),case('two','copy','另一标题','closed')])
    assert len(result['testSets']) == 2 and all(s['defectCount'] == 1 for s in result['testSets'])
    defect = result['defects'][0]
    assert defect['occurrenceCount'] == 2
    assert {o['status'] for o in defect['occurrences']} == {'open','closed'}
    assert {o['title'] for o in defect['occurrences']} == {'旧标题','另一标题'}


@pytest.mark.asyncio
async def test_plain_new_run_records_direct_collection_and_unknown_old_snapshot(plan_lab):
    from models import PlanCaseRelation
    db, sent = plan_lab
    point = node(db, nodeType='point', caseId=None, name='旧关联的真实集')
    db.query(PlanCaseRelation).filter_by(case_id='case-0').one().collection_id = point.id
    db.commit()
    run = await start_plan_run(db, 'plan', 'owner', defer=True)
    rows = enriched_report(db, run)['reportDetails']['testSets']
    assert {r['testSet']['id'] for r in rows} == {point.id, 'DEFAULT'}
    assert next(r for r in rows if r['testSet']['id'] == point.id)['testSet']['name'] == '旧关联的真实集'
    item = db.query(PlanRunItem).filter_by(run_id=run.id, sequence=0).one()
    item.suite_snapshot = {k:v for k,v in item.suite_snapshot.items() if k not in {'testSet','caseTestSets'}}
    db.commit()
    rows = enriched_report(db, run)['reportDetails']['testSets']
    assert next(r for r in rows if r['testSet']['id'] is None)['testSet']['name'] == '未记录测试集'
    assert not sent
