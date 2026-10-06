"""功能脑图范围执行：锁内重新选实例、请求幂等、历史冻结，绝不下发节点任务。"""
import hashlib
import json
from fastapi import HTTPException
from models.plan_case_execution import PlanCaseExecution
from models.plan_orchestration import PlanRun
from services.plan_case_execution import execute, can_execute
from services.plan_native_selection import resolve
from services.plan_orchestration import ACTIVE
from core.logger import logger


def request_body(data, user):
    return dict(scope=data.model_dump(mode='json', exclude={'requestId'}), executorId=str(user.id))


def preview(db, plan, user, selection):
    plan, user, rows, summary = resolve(db, plan, user, selection)
    summary['canExecute'] = bool(rows and can_execute(db, user, plan)
        and not db.query(PlanRun.id).filter(PlanRun.plan_id == plan.id, PlanRun.status.in_(ACTIVE)).first())
    return summary


def submit(db, plan, user, data):
    # 与已有选择器共用来源/项目/计划锁和当前权限读；历史重试不再套用已变化的结果筛选。
    plan, user, rows, summary = resolve(db, plan, user, data, writing=True, action='execute')
    body = request_body(data, user)
    digest = hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    previous = db.query(PlanCaseExecution).filter_by(plan_id=plan.id, request_id=str(data.requestId)).all()
    if previous:
        if any(row.payload_hash != digest for row in previous):
            raise HTTPException(409, '同一请求编号不能提交不同的脑图执行范围或内容')
        logger.info('功能脑图执行请求已重放：计划={}，数量={}，请求={}', plan.id, len(previous), data.requestId)
        return dict(updated=len(previous), replayed=True)
    if not rows:
        raise HTTPException(422, '当前脑图范围没有可执行的功能用例关联')
    result = execute(db, user, plan, data, resolved_rows=rows, request_body=body)
    logger.info('功能脑图范围回填完成：计划={}，全范围={}，数量={}，请求={}', plan.id, data.selectAll, result['updated'], data.requestId)
    return result
