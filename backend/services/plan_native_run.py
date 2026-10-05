"""原生分类列表按关联实例冻结批次；复用ATS队列，不发送网络消息。"""
from copy import deepcopy
from hashlib import sha256
import json
from types import SimpleNamespace
from uuid import uuid4
from fastapi import HTTPException
from models import TestCase, TestSuite, PlanCaseRelation, Environment
from models.plan_workspace import PlanNode
from models.plan_orchestration import PlanRun, PlanRunItem, PlanSettings
from services.plan_native_selection import resolve
from services.plan_tree import nodes, compile_tree
from services.plan_orchestration import ACTIVE, get_policy, _enqueue
from services.test_suite_service import TestSuiteService
from services.suite_dispatch import build_suite_message, is_xat_command
from services.plan_candidate_project import require_case_sources
from services.case_governance import snapshot_case
from core.logger import logger
from utils.datetime_utils import beijing_now


def start(db, plan, user, data):
    plan, user, selected, summary = resolve(db, plan, user, data, writing=True, action='execute')
    fingerprint = sha256(json.dumps(data.model_dump(exclude={'requestId'}), sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
    key = 'native-range:' + data.requestId
    existing = db.query(PlanRun).filter_by(idempotency_key=key).populate_existing().with_for_update().one_or_none()
    if existing:
        if existing.plan_id != plan.id or existing.executor_id != str(user.id) or existing.config_snapshot.get('requestFingerprint') != fingerprint:
            raise HTTPException(409, '执行请求ID已被其他范围或用户使用')
        logger.info('返回已创建的原生范围批次，未重复入队：计划={}，批次={}', plan.id, existing.id)
        return existing
    if not selected:
        raise HTTPException(409, '当前选择范围已为空，请刷新后重新选择')
    if db.query(PlanRun.id).filter(PlanRun.plan_id == plan.id, PlanRun.status.in_(ACTIVE)).with_for_update().first():
        raise HTTPException(409, '当前计划已有执行中的批次，请完成或取消后再次执行')
    # 保持当前查询对象的引用；不能让 db.get 回到预览前的MySQL普通快照。
    all_nodes = nodes(db, plan.id, current_read=True)
    relations = db.query(PlanCaseRelation).filter_by(plan_id=plan.id).populate_existing().with_for_update().all()
    suites = db.query(TestSuite).filter_by(plan_id=plan.id).populate_existing().with_for_update().all()
    cases = db.query(TestCase).filter(TestCase.id.in_({row['caseId'] for row in selected}), TestCase.deleted_at.is_(None)).populate_existing().with_for_update().all()
    settings = db.query(PlanSettings).filter_by(plan_id=plan.id).populate_existing().with_for_update().one_or_none()
    policy = get_policy(db, plan.id, current_read=True)
    case_map, suite_map = {c.id: c for c in cases}, {s.id: s for s in suites}
    if len(case_map) != len({row['caseId'] for row in selected}):
        raise HTTPException(409, '所选用例已回收或不存在')
    node_ids = {row['associationId'] for row in selected if row['source'] == 'node'}
    legacy_ids = {row['associationId'] for row in selected if row['source'] == 'legacy'}
    scoped = [n for n in all_nodes if n.node_type == 'point' or n.id in node_ids]
    for relation in sorted(relations, key=lambda r: (r.execution_order, r.id)):
        if relation.id not in legacy_ids:
            continue
        from services.native_http_execution import configured, COMMAND
        native = configured(db, case_map[relation.case_id])
        compatible = [s for s in suites if relation.case_id in (s.case_ids or []) and s.execution_command != COMMAND]
        if not native and len(compatible) != 1:
            raise HTTPException(409, '所选用例须关联唯一可执行测试套；存在多个模板时，请在测试规划指定实例的测试套')
        scoped.append(SimpleNamespace(id=relation.id, parent_id=relation.collection_id, node_type='case', category=data.category,
            case_id=relation.case_id, suite_id=compatible[0].id if len(compatible) == 1 else None, name=case_map[relation.case_id].name,
            assigned_to=relation.assigned_to, linked_functional_id=None, config={}))
    environment_ids = {suite.environment_id for suite in suites}
    if plan.environment_id: environment_ids.add(plan.environment_id)
    for node in scoped:
        config = node.config or {}
        environment_ids.update(config.get('resourcePool') or [])
        if config.get('environmentId'): environment_ids.add(config['environmentId'])
    environments = db.query(Environment).filter(Environment.id.in_(environment_ids)).order_by(Environment.id).populate_existing().with_for_update().all()
    # 只编译所选叶子及其祖先，未选中的手工用例和兄弟实例不成为前置。
    entries = compile_tree(db, plan, policy, current_read=True, scope_nodes=scoped, user=user)
    suites = db.query(TestSuite).filter_by(plan_id=plan.id).populate_existing().with_for_update().all()
    suite_map = {suite.id: suite for suite in suites}
    extra_ids = {e['suite'].environment_id for e in entries if e['suite']}
    environments = db.query(Environment).filter(Environment.id.in_(environment_ids | extra_ids)).order_by(Environment.id).populate_existing().with_for_update().all()
    if {e['node'].id for e in entries} != {row['associationId'] for row in selected}:
        raise HTTPException(409, '所选实例的测试集层级已改变，请刷新后重新执行')
    for entry in entries:
        node, suite = entry['node'], entry['suite']
        case = case_map.get(node.case_id)
        if not case or not (case.is_automated or entry.get('nativeCase')) or not suite or suite.id not in suite_map or node.case_id not in (suite_map[suite.id].case_ids or []):
            raise HTTPException(409, '所选用例已回收或未配置有效的自动化测试套')
        if not entry.get("nativeCase") and not is_xat_command(suite.execution_command):
            raise HTTPException(409, '范围执行需要支持用例过滤的XAT测试套，请在测试规划更新执行命令')
        environment = next((env for env in environments if env.id == suite.environment_id), None)
        if not environment or not environment.status:
            raise HTTPException(409, '所选实例的执行环境不存在或已停用')
        TestSuiteService.require_idle(db, suite.id, current_read=True)
        suite.native_cases = [entry['nativeCase']] if entry.get('nativeCase') else None
        build_suite_message(db, suite, '范围校验', str(user.id), current_read=True)
    require_case_sources(db, user.id, [c for c in cases if c.project_id != plan.project_id], current_read=True)
    frozen = {}
    for case in cases:
        version = snapshot_case(db, case, str(user.id), '原生计划范围执行冻结用例版本')
        frozen[case.id] = dict(id=case.id, name=case.name, caseCode=case.case_code, isAutomated=True, projectId=case.project_id,
                              versionId=version.id, version=version.version, snapshot=deepcopy(version.snapshot))
    snapshots = [dict(deepcopy(frozen[e['node'].case_id]), associationId=e['node'].id, category=data.category,
        nodeName=e['node'].name, assignedTo=e['node'].assigned_to, prerequisites=e['prerequisites'], linkedFunctionalId=None) for e in entries]
    run = PlanRun(id=str(uuid4()), plan_id=plan.id, executor_id=str(user.id), plan_name=plan.name, created_at=beijing_now(),
        idempotency_key=key, status='queued', case_snapshot=snapshots, manual_results={}, config_snapshot=dict(policy,
            nodeGraph=True, nativeRange=True, category=data.category, selectedCount=len(selected), excludedCount=summary['excludedCount'], requestFingerprint=fingerprint))
    db.add(run); db.flush()
    for index, entry in enumerate(entries):
        node, suite = entry['node'], entry['suite']
        item = PlanRunItem(id=str(uuid4()), run_id=run.id, suite_id=suite.id, execution_id=str(uuid4()), environment_id=suite.environment_id,
            sequence=index, status='waiting', suite_snapshot=dict(name=suite.name, caseIds=[node.case_id], executionCommand=suite.execution_command,
                environmentId=suite.environment_id, nodeId=node.id, category=data.category, linkedFunctionalId=None,
                prerequisites=entry['prerequisites'], resourcePool=entry['config'].get('resourcePool', []),
                gitEnabled=suite.git_enabled, gitRepoUrl=suite.git_repo_url, gitBranch=suite.git_branch,
                nativeCases=[entry['nativeCase']] if entry.get('nativeCase') else None))
        db.add(item)
        if not entry['prerequisites']:
            _enqueue(db, run, item)
    plan.status = 'running'; db.flush()
    logger.info('已冻结原生计划范围批次并入队：计划={}，批次={}，分类={}，实例数={}，排除={}', plan.id, run.id, data.category, len(entries), summary['excludedCount'])
    return run
