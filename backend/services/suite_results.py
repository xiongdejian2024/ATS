"""Per-execution, idempotent SAT results without a schema migration."""

import uuid
from models.task_queue import TaskQueue
from models.test_suite import TestSuite, TestSuiteExecution
from models.test_plan import PlanCaseRelation
from utils.datetime_utils import beijing_now


def result_id(execution_id, case_id):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"ats:{execution_id}:{case_id}"))


def dispatch_case_ids(db, task, suite):
    """计划执行严格使用该执行ID冻结的范围，不能接受未选模板成员的结果。"""
    from models.plan_orchestration import PlanRunItem
    item = db.query(PlanRunItem).filter_by(execution_id=task.execution_id).one_or_none()
    return item.suite_snapshot.get('caseIds', []) if item else suite.case_ids


def handle_run_result(db, environment_id, message):
    suite = db.query(TestSuite).filter(TestSuite.id == message.get("suite_id")).first()
    task = (
        db.query(TaskQueue)
        .filter(TaskQueue.execution_id == message.get("execution_id"))
        .first()
    )
    if (
        not suite
        or not task
        or task.kind != "suite"
        or task.suite_id != suite.id
        or task.environment_id != environment_id
    ):
        return False
    if message.get("case_id") not in dispatch_case_ids(db, task, suite) or message.get("result") not in [
        "passed",
        "failed",
        "error",
        "skipped",
    ]:
        return False
    identifier = result_id(task.execution_id, message["case_id"])
    if db.get(TestSuiteExecution, identifier) or task.status in [
        "completed",
        "failed",
        "cancelled",
    ]:
        return True  # Already persisted, or cancelled before this delayed message.
    native_detail = None
    if message.get("native_detail") is not None:
        from services.native_http_report import validate_detail
        native_detail = validate_detail(message["native_detail"], suite, task, message["case_id"], db)
    row = TestSuiteExecution(
        id=identifier,
        suite_id=suite.id,
        case_id=message["case_id"],
        environment_id=environment_id,
        executor_id=task.executor_id,
        result=message["result"],
        duration=message.get("duration"),
        log_output=message.get("log_output"),
        native_detail=native_detail,
        error_message=message.get("error_message"),
        executed_at=beijing_now(),
    )
    db.add(row)
    from models import TestExecution

    try:
        seconds = float((row.duration or "0").rstrip("s"))
    except ValueError:
        seconds = None
    db.add(
        TestExecution(
            id=identifier,
            plan_id=suite.plan_id,
            case_id=row.case_id,
            environment_id=environment_id,
            executor_id=task.executor_id,
            result=row.result,
            duration=seconds,
            execution_log=row.log_output,
            error_message=row.error_message,
            executed_at=row.executed_at,
        )
    )
    from models import TestCase

    case = db.get(TestCase, row.case_id)
    case.status = row.result
    relation = (
        db.query(PlanCaseRelation)
        .filter(
            PlanCaseRelation.plan_id == suite.plan_id,
            PlanCaseRelation.case_id == row.case_id,
        )
        .first()
    )
    if relation:
        relation.execution_status = {
            "passed": "pass",
            "failed": "fail",
            "error": "error",
            "skipped": "skip",
        }[row.result]
        relation.execution_updated_at = beijing_now()
    db.commit()
    # Only the completion event releases the queue; a last result alone cannot do so.
    return True
