"""Build the same ordered dispatch message for initial and queued executions."""

from models.test_case import TestCase


def build_suite_message(db, suite, execution_id, executor_id, case_snapshots=None):
    if not suite.case_ids:
        raise ValueError("至少需要选择一个测试用例")
    cases = db.query(TestCase).filter(TestCase.id.in_(suite.case_ids), TestCase.deleted_at.is_(None)).all()
    by_id = {case.id: case for case in cases}
    if len(by_id) != len(suite.case_ids):
        raise ValueError("部分所选测试用例已不存在或存在重复选择")
    from models.test_plan import TestPlan

    plan = db.get(TestPlan, suite.plan_id)
    if not plan or any(
        case.project_id != plan.project_id or not case.is_automated for case in cases
    ):
        raise ValueError("所选用例必须为测试计划所属项目的自动化用例")
    snapshots = {c["id"]: c for c in case_snapshots or []}
    git_enabled = suite.git_enabled == "true"
    return {
        "type": "execute_test_suite",
        "suite_id": suite.id,
        "plan_id": suite.plan_id,
        "execution_id": execution_id,
        "git_repo_url": suite.git_repo_url if git_enabled else None,
        "git_branch": suite.git_branch if git_enabled else None,
        "git_token": suite.git_token if git_enabled else None,
        "execution_command": suite.execution_command,
        "case_ids": suite.case_ids,
        "case_codes": [snapshots.get(case_id, {}).get("caseCode", by_id[case_id].case_code) for case_id in suite.case_ids],
        "executor_id": executor_id,
    }


def is_xat_command(command):
    """统一识别 XAT 命令和原 ats-sat 兼容入口。"""
    return command.strip().split(maxsplit=1)[:1] in (["xat"], ["ats-sat"])
