"""在现有 Agent 队列上编排计划，批次与报告永久独立。"""
import uuid
from sqlalchemy.orm import Session
from models.test_plan import TestPlan, PlanCaseRelation
from models.test_case import TestCase
from models.test_suite import TestSuite, TestSuiteExecution, TestSuiteLog
from models.task_queue import TaskQueue
from models.environment import Environment
from models.user import User
from core.project_access import require_project_access
from models.plan_orchestration import PlanGroup, PlanSettings, PlanRun, PlanRunItem
from services.suite_dispatch import build_suite_message
from services.suite_results import result_id
from services.task_queue_service import TaskQueueService
from utils.datetime_utils import beijing_now
from utils.serializer import serialize_model
from core.logger import logger

ACTIVE = ("queued", "running", "cancelling", "needs_confirmation")
TERMINAL = ("completed", "failed", "cancelled", "skipped")


def get_policy(db, plan_id):
    row = db.get(PlanSettings, plan_id)
    return dict(groupId=row.group_id if row else None,
                executionMode=row.execution_mode if row else "serial",
                stopOnFailure=row.stop_on_failure if row else False,
                passThreshold=row.pass_threshold if row else 100,
                suiteOrder=row.suite_order if row else [])


def save_policy(db, plan_id, policy):
    plan = db.get(TestPlan, plan_id)
    if not plan:
        raise ValueError("测试计划不存在")
    if policy.group_id:
        group = db.get(PlanGroup, policy.group_id)
        if not group or group.project_id != plan.project_id:
            raise ValueError("计划组不属于当前项目")
    suites = {s.id for s in db.query(TestSuite).filter_by(plan_id=plan_id).all()}
    if len(policy.suite_order) != len(set(policy.suite_order)) or not set(policy.suite_order) <= suites:
        raise ValueError("测试套顺序必须使用当前计划中不重复的测试套")
    row = db.get(PlanSettings, plan_id) or PlanSettings(plan_id=plan_id)
    for key, value in policy.model_dump().items():
        setattr(row, key, value)
    db.add(row)
    db.commit()
    logger.info("已保存计划策略：计划={}，模式={}", plan_id, policy.execution_mode)
    return get_policy(db, plan_id)


def _enqueue(db, run, item):
    if db.query(TaskQueue).filter_by(execution_id=item.execution_id).first():
        return
    db.flush()
    runnable = db.query(PlanRun.id).filter(PlanRun.status.in_(("queued", "running")))
    claimed = db.query(PlanRunItem).filter(PlanRunItem.id == item.id, PlanRunItem.status == "waiting", PlanRunItem.run_id.in_(runnable)).update(
        {"status": "pending"}, synchronize_session=False)
    if claimed != 1:
        return
    db.add(TaskQueue(id=str(uuid.uuid4()), environment_id=item.environment_id,
                     suite_id=item.suite_id, execution_id=item.execution_id,
                     executor_id=run.executor_id, status="pending", priority=0))
    item.status = "pending"


async def start_plan_run(db: Session, plan_id: str, user_id: str, suite_ids=None,
                         notes=None, idempotency_key=None, commit=True):
    """先持久化批次与任务，派发由调度循环在事务提交后完成。"""
    if idempotency_key:
        existing = db.query(PlanRun).filter_by(idempotency_key=idempotency_key).first()
        if existing:
            if existing.plan_id != plan_id or existing.executor_id != str(user_id):
                raise ValueError("幂等键已被其他计划执行使用")
            return existing
    plan = db.query(TestPlan).filter_by(id=plan_id).with_for_update().first()
    if not plan:
        raise ValueError("测试计划不存在")
    if db.query(PlanRun).filter(PlanRun.plan_id == plan_id, PlanRun.status.in_(ACTIVE)).first():
        raise ValueError("当前计划已有执行中的批次，请完成或取消后再次执行")
    suites = db.query(TestSuite).filter_by(plan_id=plan_id).order_by(TestSuite.created_at, TestSuite.id).all()
    if suite_ids is not None:
        requested = list(suite_ids)
        known = {s.id for s in suites}
        if len(requested) != len(set(requested)) or not set(requested) <= known:
            raise ValueError("选择的测试套不属于当前计划或存在重复")
        suites = [s for s in suites if s.id in requested]
    policy = get_policy(db, plan_id)
    ordering = {sid: i for i, sid in enumerate(policy["suiteOrder"])}
    suites.sort(key=lambda s: ordering.get(s.id, len(ordering)))
    relations = db.query(PlanCaseRelation).filter_by(plan_id=plan_id).order_by(PlanCaseRelation.execution_order).all()
    case_ids = list(dict.fromkeys([r.case_id for r in relations] + [cid for s in suites for cid in s.case_ids]))
    cases = {c.id: c for c in db.query(TestCase).filter(TestCase.id.in_(case_ids)).all()}
    if not cases:
        raise ValueError("请先为计划关联用例或添加测试套")
    if any(c.project_id != plan.project_id for c in cases.values()):
        raise ValueError("计划包含不属于当前项目的用例")
    covered = {cid for s in suites for cid in s.case_ids}
    if suite_ids is None and any(c.is_automated and c.id not in covered for c in cases.values()):
        raise ValueError("存在未配置测试套的自动化用例，请先配置执行命令和节点")
    if suite_ids is not None:
        case_ids = [cid for cid in case_ids if cid in covered or not cases[cid].is_automated]
    for suite in suites:
        if not db.get(Environment, suite.environment_id):
            raise ValueError("执行环境不存在")
        build_suite_message(db, suite, "校验", str(user_id))
    run = PlanRun(id=str(uuid.uuid4()), plan_id=plan_id, executor_id=str(user_id),
                  idempotency_key=idempotency_key, status="queued" if suites else "running",
                  plan_name=plan.name, config_snapshot=policy, notes=notes,
                  case_snapshot=[dict(id=cid, name=cases[cid].name, caseCode=cases[cid].case_code,
                                      isAutomated=cases[cid].is_automated) for cid in case_ids],
                  manual_results={})
    db.add(run)
    db.flush()
    for i, suite in enumerate(suites):
        item = PlanRunItem(id=str(uuid.uuid4()), run_id=run.id, suite_id=suite.id,
                           execution_id=str(uuid.uuid4()), environment_id=suite.environment_id,
                           sequence=i, status="waiting",
                           suite_snapshot=dict(name=suite.name, caseIds=list(suite.case_ids),
                                               executionCommand=suite.execution_command,
                                               environmentId=suite.environment_id))
        db.add(item)
        if i == 0 or policy["executionMode"] == "parallel":
            _enqueue(db, run, item)
    plan.status = "running"
    if commit:
        db.commit()
    else:
        db.flush()
    logger.info("已创建计划执行批次：计划={}，批次={}，测试套数={}", plan_id, run.id, len(suites))
    return run


def _items(db, run_id):
    return db.query(PlanRunItem).filter_by(run_id=run_id).order_by(PlanRunItem.sequence).all()


def build_report(db, run):
    """只读取本批次 execution_id 对应结果，绝不混入历史或最新用例状态。"""
    rows = []
    items = _items(db, run.id)
    cases = {c["id"]: c for c in run.case_snapshot}
    for item in items:
        for cid in item.suite_snapshot["caseIds"]:
            result = db.get(TestSuiteExecution, result_id(item.execution_id, cid))
            state = result.result if result else (
                "skipped" if item.status == "skipped" else
                "cancelled" if item.status == "cancelled" else
                "error" if item.status in ("completed", "failed") else "pending")
            rows.append(dict(caseId=cid, caseName=cases.get(cid, {}).get("name", cid),
                             suiteName=item.suite_snapshot["name"], executionId=item.execution_id,
                             result=state, notes=result.error_message if result else item.error_message,
                             duration=result.duration if result else None))
    for case in run.case_snapshot:
        if not case["isAutomated"]:
            result = (run.manual_results or {}).get(case["id"], {})
            rows.append(dict(caseId=case["id"], caseName=case["name"], suiteName="手工测试",
                             executionId=None, result=result.get("result", "cancelled" if run.status == "cancelled" else "pending"),
                             notes=result.get("notes"), duration=None))
    counts = {key: sum(r["result"] == key for r in rows)
              for key in ("passed", "failed", "error", "skipped", "cancelled", "pending")}
    total = len(rows)
    rate = round(100 * counts["passed"] / total, 2) if total else 0
    outcome = "cancelled" if run.status in ("cancelled", "cancelling") else (
        "running" if counts["pending"] or any(i.status not in TERMINAL for i in items) else
        "passed" if total and rate >= run.config_snapshot["passThreshold"] else "failed")
    return dict(total=total, counts=counts, passRate=rate, passThreshold=run.config_snapshot["passThreshold"],
                outcome=outcome, cases=rows, items=[dict(id=i.id, suiteId=i.suite_id,
                    suiteName=i.suite_snapshot["name"], executionId=i.execution_id,
                    status=i.status, environmentId=i.environment_id, errorMessage=i.error_message) for i in items])


def _cancel_waiting_item(db, item, target_status="cancelled", reason=None):
    """只取消尚未被领取的项，不能覆盖另一进程刚领取的运行槽。"""
    task = db.query(TaskQueue).filter_by(execution_id=item.execution_id).populate_existing().first()
    if task:
        changed = db.query(TaskQueue).filter_by(id=task.id, status="pending").update(
            {"status": "cancelled", "completed_at": beijing_now()}, synchronize_session=False)
        if changed:
            item.status = target_status
            item.error_message = reason
            db.flush()
            return True
        # 条件更新失败后读取最新已提交状态；MySQL 使用当前读，SQLite 由 CAS 保证不覆盖。
        task = db.query(TaskQueue).filter_by(id=task.id).with_for_update().populate_existing().one()
        if item.status != "skipped":
            item.status = task.status
        return False
    changed = db.query(PlanRunItem).filter_by(id=item.id, status="waiting").update(
        {"status": target_status, "error_message": reason}, synchronize_session=False)
    if changed:
        db.refresh(item)
        return True
    db.refresh(item)
    return False


async def cancel_plan_run(db, run_id, user_id=None):
    run = db.get(PlanRun, run_id)
    if not run:
        raise ValueError("执行批次不存在")
    # 先提交取消意图，其他派发器必须在领取时同时检查该状态。
    changed = db.query(PlanRun).filter(PlanRun.id == run_id, PlanRun.status.in_(ACTIVE)).update(
        {"status": "cancelling"}, synchronize_session=False)
    db.commit()
    db.refresh(run)
    if not changed:
        return run
    from api.v1.websocket import manager
    for item in _items(db, run.id):
        _cancel_waiting_item(db, item)
        db.commit()
        task = db.query(TaskQueue).filter_by(execution_id=item.execution_id).populate_existing().first()
        if task and task.status == "running":
            # Agent 完成确认之前保留运行槽，断线时由后续 tick 重试取消。
            await manager.send_message(item.environment_id, dict(type="cancel_test_suite",
                                       suite_id=item.suite_id, execution_id=item.execution_id))
    logger.info("已请求取消计划执行：批次={}，用户={}", run_id, user_id)
    return run


async def advance_plan_runs(db):
    """由后台调度循环推进，页面关闭和后端重启不丢失编排状态。"""
    from api.v1.websocket import manager
    runs = db.query(PlanRun).filter(PlanRun.status.in_(ACTIVE)).order_by(PlanRun.created_at).all()
    for run in runs:
        try:
            items = _items(db, run.id)
            for item in items:
                task = db.query(TaskQueue).filter_by(execution_id=item.execution_id).first()
                if task and item.status != "skipped" and (item.status != "needs_confirmation" or task.status in TERMINAL):
                    item.status = task.status
                if (item.delivery_state == "dispatching" and item.dispatch_attempted_at
                    and task and task.status == "running" and item.status != "needs_confirmation"
                    and (beijing_now().replace(tzinfo=None) - item.dispatch_attempted_at.replace(tzinfo=None)).total_seconds() > 30):
                    item.status = "needs_confirmation"
                    run.status = "needs_confirmation"
                    item.error_message = "派发后未确认交付，执行状态未知；请核对 Agent 后人工确认，系统不会自动重发"
                    logger.warning("计划任务派发状态待核对：批次={}，执行={}", run.id, item.execution_id)
            if any(i.status == "needs_confirmation" for i in items):
                run.status = "needs_confirmation"
                run.report = build_report(db, run)
                db.commit()
                continue
            if run.status == "cancelling":
                await cancel_plan_run(db, run.id)
            else:
                failed = any(i.status == "failed" for i in items)
                if failed and run.config_snapshot["stopOnFailure"]:
                    for item in items:
                        if item.status in ("waiting", "pending"):
                            _cancel_waiting_item(db, item, "skipped", "前序测试套失败，已停止后续执行")
                elif run.config_snapshot["executionMode"] == "serial":
                    active = any(i.status in ("pending", "running") for i in items)
                    waiting = next((i for i in items if i.status == "waiting"), None)
                    if waiting and not active:
                        _enqueue(db, run, waiting)
                db.commit()
                for item in items:
                    if item.status != "pending":
                        continue
                    environment = db.query(Environment).filter_by(id=item.environment_id).with_for_update().first()
                    if not environment or not environment.status or item.environment_id not in manager.active_connections:
                        db.commit()
                        continue
                    if not TaskQueueService.can_execute_immediately(db, item.environment_id):
                        db.commit()
                        continue
                    try:
                        executor = db.query(User).filter_by(id=run.executor_id).populate_existing().first()
                        plan = db.get(TestPlan, run.plan_id)
                        if not executor or not executor.status:
                            raise ValueError("计划执行人不存在或已被禁用")
                        require_project_access(db, executor, plan.project_id, "test_plan:execute")
                        suite = db.get(TestSuite, item.suite_id)
                        message = build_suite_message(db, suite, item.execution_id, run.executor_id)
                    except Exception:
                        logger.exception("计划派发前校验失败：批次={}，执行={}", run.id, item.execution_id)
                        _cancel_waiting_item(db, item, "failed", "派发前校验失败，请检查执行人权限与测试套配置")
                        # 已拒绝的任务是失败而不是用户取消，报告保存明确原因。
                        db.query(TaskQueue).filter_by(execution_id=item.execution_id, status="cancelled").update({"status": "failed"})
                        db.commit()
                        continue
                    runnable_items = db.query(PlanRunItem.execution_id).join(PlanRun, PlanRun.id == PlanRunItem.run_id).filter(
                        PlanRun.status.in_(("queued", "running")))
                    claimed = db.query(TaskQueue).filter(TaskQueue.execution_id == item.execution_id,
                        TaskQueue.status == "pending", TaskQueue.execution_id.in_(runnable_items)).update(
                        {"status": "running", "started_at": beijing_now()}, synchronize_session=False)
                    if claimed != 1:
                        db.rollback()
                        continue
                    task = db.query(TaskQueue).filter_by(execution_id=item.execution_id).populate_existing().one()
                    item.status = "running"
                    item.delivery_state = "dispatching"
                    item.dispatch_attempted_at = beijing_now()
                    suite.status = "running"
                    db.query(PlanRun).filter_by(id=run.id, status="queued").update({"status": "running"}, synchronize_session=False)
                    db.commit()
                    db.refresh(run)
                    if not await manager.send_message(item.environment_id, message):
                        task.status = item.status = "pending"
                        task.started_at = None
                        item.delivery_state = "queued"
                    else:
                        item.delivery_state = "delivered"
                    db.commit()
            db.refresh(run)
            report = build_report(db, run)
            if all(i.status in TERMINAL for i in items) and (report["counts"]["pending"] == 0 or run.status == "cancelling"):
                final_status = "cancelled" if run.status == "cancelling" else (
                    "completed" if report["outcome"] == "passed" else "failed")
                claimed = db.query(PlanRun).filter_by(id=run.id, status=run.status,
                    manual_revision=run.manual_revision).update(
                        {"status": final_status, "completed_at": beijing_now()}, synchronize_session=False)
                if not claimed:
                    # 手工结果或取消意图发生变化时，下一轮重新计算，不能冻结旧报告。
                    db.rollback()
                    continue
                db.refresh(run)
                plan = db.get(TestPlan, run.plan_id)
                plan.status = "paused" if run.status == "cancelled" else "completed"
                report = build_report(db, run)
                logger.info("计划执行批次已结束：批次={}，状态={}，通过率={}", run.id, run.status, report["passRate"])
            run.report = report
            db.commit()
        except Exception:
            db.rollback()
            logger.exception("推进计划执行批次失败：批次={}", run.id)


def record_manual_result(db, run_id, case_id, data, user_id):
    # 版本号条件更新在 MySQL 与 SQLite 都生效，不依赖 SQLite 忽略的 FOR UPDATE。
    for attempt in range(5):
        run = db.query(PlanRun).filter_by(id=run_id).populate_existing().first()
        if not run or run.status not in ("queued", "running"):
            raise ValueError("只有进行中的批次可以回填手工结果")
        case = next((c for c in run.case_snapshot if c["id"] == case_id), None)
        if not case or case["isAutomated"]:
            raise ValueError("只能回填本批次关联的手工用例")
        updated = dict(run.manual_results or {})
        updated[case_id] = dict(result=data.result, notes=data.notes, executorId=user_id,
                               updatedAt=beijing_now().isoformat())
        changed = db.query(PlanRun).filter(PlanRun.id == run_id,
            PlanRun.status.in_(("queued", "running")), PlanRun.manual_revision == run.manual_revision).update(
                {"manual_results": updated, "manual_revision": run.manual_revision + 1}, synchronize_session=False)
        if not changed:
            db.rollback()
            logger.info("手工结果并发更新冲突，重新读取后合并：批次={}，重试={}", run_id, attempt + 1)
            continue
        relation = db.query(PlanCaseRelation).filter_by(plan_id=run.plan_id, case_id=case_id).first()
        if relation:
            relation.execution_status = {"passed": "pass", "failed": "fail", "error": "error", "skipped": "skip"}[data.result]
            relation.execution_updated_at = beijing_now()
        db.commit()
        db.refresh(run)
        logger.info("已回填计划手工结果：批次={}，用例={}，结果={}", run_id, case_id, data.result)
        return run
    raise ValueError("其他人员正在更新结果，请刷新后重试")


def run_data(db, run, include_report=True):
    data = serialize_model(run, camel_case=True)
    if include_report:
        data["report"] = run.report if run.status not in ACTIVE and run.report else build_report(db, run)
    else:
        data.pop("caseSnapshot", None)
        data.pop("manualResults", None)
        data.pop("report", None)
    return data


def run_logs(db, run):
    ids = [item.execution_id for item in _items(db, run.id)]
    logs = db.query(TestSuiteLog).filter(TestSuiteLog.execution_id.in_(ids)).order_by(TestSuiteLog.timestamp, TestSuiteLog.sequence_number).all()
    return "\n".join(f"[{row.timestamp}] {row.message}" for row in logs)


def resolve_uncertain_run(db, run_id, user_id):
    """仅在用户明确确认节点未执行或已停止后关闭状态不确定的批次。"""
    run = db.get(PlanRun, run_id)
    if not run or run.status != "needs_confirmation":
        raise ValueError("该批次不处于待核对状态")
    for item in _items(db, run.id):
        task = db.query(TaskQueue).filter_by(execution_id=item.execution_id).first()
        if item.status == "running":
            raise ValueError("仍有正常运行的测试套，请先等待结束或取消")
        if item.status not in TERMINAL:
            item.status = "failed" if item.status == "needs_confirmation" else "cancelled"
            item.error_message = "用户已确认节点未执行或已停止，人工终止该批次"
            if task:
                task.status = item.status
                task.completed_at = beijing_now()
    run.status = "failed"
    run.completed_at = beijing_now()
    run.report = build_report(db, run)
    db.get(TestPlan, run.plan_id).status = "paused"
    db.commit()
    logger.warning("用户确认后已终止状态不确定的计划批次：批次={}，用户={}", run_id, user_id)
    return run
