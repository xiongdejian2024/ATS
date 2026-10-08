"""Build the same ordered dispatch message for initial and queued executions."""

from models.test_case import TestCase


def build_suite_message(db, suite, execution_id, executor_id, case_snapshots=None, *, current_read=False, node_current=False):
    if not suite.case_ids:
        raise ValueError("至少需要选择一个测试用例")
    query = db.query(TestCase).filter(TestCase.id.in_(suite.case_ids), TestCase.deleted_at.is_(None))
    cases = (query.populate_existing().with_for_update() if current_read else query).all()
    by_id = {case.id: case for case in cases}
    if len(by_id) != len(suite.case_ids):
        raise ValueError("部分所选测试用例已不存在或存在重复选择")
    from models.test_plan import TestPlan

    plan = db.get(TestPlan, suite.plan_id)
    if not plan or any(
        not case.is_automated and suite.execution_command != "ats-native-http" for case in cases
    ):
        raise ValueError("所选用例必须为可执行的自动化用例")
    from services.plan_candidate_project import require_case_sources
    require_case_sources(db, executor_id, [c for c in cases if c.project_id != plan.project_id], current_read=True)
    snapshots = {c["id"]: c for c in case_snapshots or []}
    native_cases = None
    if suite.execution_command == 'ats-native-http':
        from framework.native_http.models import FrozenCase
        from framework.native_http.variable_models import wire_case
        native_cases = [wire_case(FrozenCase.model_validate(c)) for c in getattr(suite, 'native_cases', None) or []]
        if [c['id'] for c in native_cases] != suite.case_ids:
            raise ValueError('冻结原生HTTP请求与派发范围不一致')
    git_enabled = suite.git_enabled == "true"
    message = {
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
        **({"native_cases": native_cases} if native_cases is not None else {}),
    }
    if native_cases is not None:
        from services.native_hooks import authorize_frozen, required_node
        hook_node=required_node(message)
        if hook_node and hook_node != suite.environment_id:
            raise ValueError('冻结脚本钩子与派发节点不一致')
        authorize_frozen(db, executor_id, message, node_current=node_current)
        from services.native_variable_delivery import validate_budget
        validate_budget(message)
    return message


def is_xat_command(command):
    """统一识别 XAT 命令和原 ats-sat 兼容入口。"""
    return command.strip().split(maxsplit=1)[:1] in (["xat"], ["ats-sat"])


def load_dispatch_suite(db, suite_id, executor_id):
    """Current-read permission/configuration check inside a slot transaction."""
    from core.project_access import require_project_access
    from models import User, TestSuite, TestPlan

    executor = db.query(User).filter_by(id=executor_id).populate_existing().with_for_update(read=True).first()
    if not executor or not executor.status:
        raise ValueError("测试套执行人不存在或已被禁用")
    suite = db.query(TestSuite).filter_by(id=suite_id).populate_existing().with_for_update().first()
    plan = (db.query(TestPlan).filter_by(id=suite.plan_id).populate_existing().with_for_update().first()
            if suite else None)
    if not suite or not plan:
        raise ValueError("测试套或所属计划不存在")
    require_project_access(db, executor, plan.project_id, "test_plan:execute", current_read=True)
    return suite
