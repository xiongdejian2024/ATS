"""当前计划手工结果及不可覆盖的历史，绝不创建执行节点任务。"""
import hashlib
import json
from fastapi import HTTPException
from models import TestCase, PlanCaseRelation, Project
from models.plan_workspace import PlanWorkspace
from models.plan_orchestration import PlanRun
from models.plan_case_execution import PlanCaseExecution
from core.project_access import project_allows
from core.logger import logger
from services.plan_orchestration import ACTIVE
from utils.serializer import serialize_model
from utils.datetime_utils import beijing_now


def latest(db, plan_id):
    records = db.query(PlanCaseExecution).filter_by(plan_id=plan_id).order_by(PlanCaseExecution.created_at.desc(), PlanCaseExecution.id.desc()).all()
    result = {}
    for record in records:
        result.setdefault(record.association_key, record)
    return result


def overlay(db, plan_id, items, run):
    """后创建的整计划批次重置当前范围，旧冻结报告保持原样。"""
    current = latest(db, plan_id)
    for item in items:
        record = current.get(item['id'])
        if record and (not run or record.created_at.replace(tzinfo=None) >= run.created_at.replace(tzinfo=None)):
            item.update(result=record.result, executionId=record.id, executedBy=record.executor_name, executedAt=record.created_at, runId=None)
    return items


def can_execute(db, user, plan):
    workspace = db.get(PlanWorkspace, plan.id)
    return not (workspace and workspace.archived) and project_allows(db, user, db.get(Project, plan.project_id), 'test_plan:execute')


def current_selection(db, plan, selections):
    from services.plan_case_workspace import entries
    rows = entries(db, plan, 'functional')[0]
    by_key = {(row['source'], row['associationId']): row for row in rows if not row['grouped']}
    keys = [(row.source, row.id) for row in selections]
    if len(set(keys)) != len(keys):
        raise HTTPException(422, '不能重复选择同一计划关联')
    if any(key not in by_key for key in keys):
        raise HTTPException(404, '功能用例关联不存在或不属于此计划')
    selected = [by_key[key] for key in keys]
    if any(row['recycled'] for row in selected):
        raise HTTPException(409, '已回收用例不可提交执行结果')
    return selected


def execute(db, user, plan, data):
    if not can_execute(db, user, plan):
        raise HTTPException(409, '归档计划不可提交执行结果')
    rows = current_selection(db, plan, data.selections)
    if db.query(PlanRun).filter(PlanRun.plan_id == plan.id, PlanRun.status.in_(ACTIVE)).first():
        raise HTTPException(409, '计划有活动执行批次，请在该批次回填或结束批次后提交')
    steps = [row.model_dump() for row in data.stepResults]
    if steps and len(rows) != 1:
        raise HTTPException(422, '逐步骤结果只支持单个用例')
    if steps:
        indices = [row['index'] for row in steps]
        case = db.get(TestCase, rows[0]['caseId'])
        expected = len(case.steps or []) if case.case_edit_type != 'TEXT' else 0
        if len(set(indices)) != len(indices) or any(index >= expected for index in indices):
            raise HTTPException(422, '步骤编号无效或重复')
        if data.result == 'passed' and (len(steps) != expected or any(row['result'] != 'passed' for row in steps)):
            raise HTTPException(422, '整体通过时已提交的步骤须全部通过')
    request = str(data.requestId)
    body = dict(selections=sorted(row['id'] for row in rows), result=data.result, description=data.description, steps=steps)
    digest = hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    previous = db.query(PlanCaseExecution).filter_by(plan_id=plan.id, request_id=request).all()
    if previous:
        if {row.association_key for row in previous} != set(body['selections']) or any(row.payload_hash != digest for row in previous):
            raise HTTPException(409, '同一请求编号不能提交不同的执行内容')
        return dict(updated=len(previous), replayed=True)
    from services.plan_case_media import description_media
    from models.plan_case_media import PlanCaseMediaLink
    media_ids=description_media(db,user,plan,data.description)
    timestamp = beijing_now()
    for row in rows:
        case = db.get(TestCase, row['caseId'])
        record=PlanCaseExecution(plan_id=plan.id, association_key=row['id'], case_id=case.id, request_id=request,
            payload_hash=digest, executor_id=str(user.id), executor_name=user.username, result=data.result,
            description=data.description, step_results=steps, case_snapshot=serialize_model(case, camel_case=True), created_at=timestamp)
        db.add(record);db.flush()
        for media_id in media_ids:db.add(PlanCaseMediaLink(execution_id=record.id,media_id=media_id))
        if row['source'] == 'legacy':
            relation = db.get(PlanCaseRelation, row['associationId'])
            relation.execution_status = {'passed':'pass', 'failed':'fail'}.get(data.result, data.result)
            relation.execution_updated_at = beijing_now()
    db.flush()
    logger.info('已记录计划功能用例手工结果：计划={}，结果={}，数量={}，请求={}', plan.id, data.result, len(rows), request)
    return dict(updated=len(rows), replayed=False)


def detail(db, user, plan, source, association_id, case_id, page, size):
    from services.plan_case_workspace import entries
    key = f'{source}:{association_id}:{case_id}'
    current = next((row for row in entries(db, plan, 'functional')[0] if row['id'] == key), None)
    query = db.query(PlanCaseExecution).filter_by(plan_id=plan.id, association_key=key)
    count = query.count()
    history = query.order_by(PlanCaseExecution.created_at.desc(), PlanCaseExecution.id.desc()).offset((page-1)*size).limit(size).all()
    if not current and not count:
        raise HTTPException(404, '当前计划没有此用例关联或执行历史')
    return dict(entry=current, detached=current is None, canExecute=bool(current and not current['grouped'] and not current['recycled'] and can_execute(db,user,plan)),
        history=[serialize_model(row, camel_case=True) for row in history], total=count, page=page, size=size)


def apply_statistics(db, plan_id, payload):
    """汇总各分类当前实例结果，与分类列表保持一致，冻结报告不被改写。"""
    from models import TestPlan
    from services.plan_case_workspace import entries
    plan = db.get(TestPlan, plan_id)
    states = [row['result'] for category in ('functional','api','scenario') for row in entries(db,plan,category)[0]]
    mapping = {'passed':'pass','failed':'fail','blocked':'blocked','error':'error','skipped':'skip','cancelled':'skip','pending':'pending','fake_error':'fakeError','running':'running'}
    payload['totalCases'] = len(states)
    payload['executedCases'] = sum(state not in ('pending','running') for state in states)
    payload['caseStatusCounts'] = {key:sum(mapping.get(state,'pending') == key for state in states) for key in ('pending','pass','fail','blocked','broken','error','skip','fakeError','running')}
