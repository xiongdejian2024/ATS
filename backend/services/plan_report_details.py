"""只由批次快照构建配置、测试集与逐实例缺陷分析；不读取当前用例/缺陷。"""
from copy import deepcopy
from math import isfinite


def freeze_test_sets(entries, all_nodes):
    node_map = {node.id: node for node in all_nodes}
    for entry in entries:
        parent = entry['node'].parent_id
        ancestors, seen = [], set()
        while parent:
            if parent in seen or parent not in node_map:
                raise ValueError('测试集层级无效或形成循环')
            seen.add(parent)
            node = node_map[parent]
            if node.node_type != 'point':
                raise ValueError('测试集父节点必须为测试点')
            ancestors.append(dict(id=node.id, name=node.name))
            parent = node.parent_id
        entry['testSet'] = dict(id=ancestors[0]['id'] if ancestors else 'DEFAULT',
                                name=ancestors[0]['name'] if ancestors else '默认测试集',
                                path=list(reversed(ancestors)))
    return entries


def _policy(snapshot):
    source = snapshot if isinstance(snapshot, dict) else {}
    result = {}
    if source.get('executionMode') in ('serial', 'parallel'):
        result['executionMode'] = source['executionMode']
    for key in ('stopOnFailure', 'extended', 'retryOnFailure'):
        if isinstance(source.get(key), bool):
            result[key] = source[key]
    for key in ('passThreshold', 'retryTimes', 'retryInterval', 'requestEnvironmentGroupRevision', 'testResourcePoolRevision'):
        value = source.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool) and isfinite(value):
            result[key] = value
    for key in ('testResourcePoolId', 'testResourcePoolScope', 'requestEnvironmentId', 'requestEnvironmentGroupId', 'resolvedRequestEnvironmentId'):
        if isinstance(source.get(key), str):
            result[key] = source[key]
    return result


def _test_set(row):
    value = row.get('testSet')
    return deepcopy(value) if isinstance(value, dict) and value.get('id') else dict(id=None, name='未记录测试集', path=[])


def analyse(rows, default_run_id='', default_plan_name=''):
    """同一主用例、缺陷在不同批次/实例/步骤出现时保留独立位置。"""
    groups, defects = {}, {}
    seen_occurrences = set()
    for row in rows:
        run_id = row.get('planRunId') or default_run_id
        plan_name = row.get('planName') or default_plan_name
        category = row.get('category') or 'functional'
        test_set = _test_set(row)
        key = (run_id, category, test_set['id'])
        group = groups.setdefault(key, dict(key=f'{run_id}:{category}:{test_set["id"] or "UNRECORDED"}',
            planRunId=run_id, planName=plan_name, category=category, testSet=test_set,
            total=0, counts={}, defectIds=set()))
        group['total'] += 1
        state = row.get('result') or 'pending'
        group['counts'][state] = group['counts'].get(state, 0) + 1
        for step in row.get('stepResults') or []:
            for defect in step.get('defects') or []:
                defect_id = defect.get('id')
                if not defect_id:
                    continue
                group['defectIds'].add(defect_id)
                identity = (run_id, row.get('executionId'), row.get('associationId') or row.get('caseId'),
                            row.get('caseId'), step.get('index'), defect_id)
                if identity in seen_occurrences:
                    continue
                seen_occurrences.add(identity)
                # 首次保存值用于列表，逐位置记录保留各步骤冻结的名称/状态。
                item = defects.setdefault(defect_id, dict(id=defect_id, title=defect.get('title') or defect_id,
                    status=defect.get('status'), occurrences=[]))
                item['occurrences'].append(dict(key=':'.join(str(v or '') for v in identity),
                    planRunId=run_id, planName=plan_name, caseId=row.get('caseId'), caseName=row.get('caseName'),
                    associationId=row.get('associationId') or row.get('caseId'), executionId=row.get('executionId'),
                    category=category, testSet=test_set, stepIndex=step.get('index'),
                    title=defect.get('title') or defect_id, status=defect.get('status')))
    for group in groups.values():
        group['defectCount'] = len(group.pop('defectIds'))
        group['passRate'] = round(100 * group['counts'].get('passed', 0) / group['total'], 2)
    for item in defects.values():
        item['occurrenceCount'] = len(item['occurrences'])
    return dict(testSets=list(groups.values()), defects=list(defects.values()))


def details(db, runs, report, *, group_policy=None, group_name=None):
    from models.plan_orchestration import PlanRunItem
    policies = []
    if group_policy is not None:
        policies.append(dict(key='GROUP', planName=group_name, **_policy(group_policy)))
    run_map = {run.id: run for run in runs}
    for run in runs:
        policies.append(dict(key=run.id, planRunId=run.id, planName=run.plan_name, **_policy(run.config_snapshot)))
    items = []
    if run_map:
        for item in db.query(PlanRunItem).filter(PlanRunItem.run_id.in_(run_map)).order_by(
                PlanRunItem.run_id, PlanRunItem.sequence, PlanRunItem.id).all():
            snapshot = item.suite_snapshot or {}
            saved_sets = list({value['id']: value for value in (snapshot.get('caseTestSets') or {}).values() if isinstance(value, dict) and value.get('id')}.values())
            test_set = snapshot.get('testSet') or (saved_sets[0] if len(saved_sets) == 1 else dict(id=None, name='多个测试集', path=[]) if saved_sets else None)
            items.append(dict(id=item.id, planRunId=item.run_id, planName=run_map[item.run_id].plan_name,
                suiteName=snapshot.get('name'), category=snapshot.get('category'), testSet=deepcopy(test_set) if test_set else _test_set(snapshot),
                testSets=deepcopy(saved_sets),
                executionId=item.execution_id, environmentId=snapshot.get('environmentId'),
                resourcePool=deepcopy(snapshot.get('resourcePool') or []),
                executionConfig=_policy(snapshot.get('executionConfig'))))
    single = runs[0] if len(runs) == 1 and group_policy is None else None
    result = analyse(report.get('cases') or [], single.id if single else '', single.plan_name if single else '')
    result['configuration'] = dict(policies=policies, items=items)
    return result
