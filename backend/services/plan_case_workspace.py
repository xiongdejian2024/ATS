"""计划关联列表及原子批量管理，兼容直接关联和独立树实例。"""
from fastapi import HTTPException
from models import TestCase, TestSuite, Module, User, PlanCaseRelation, Project, TestPlan
from models.plan_workspace import PlanNode, PlanWorkspace
from models.plan_orchestration import PlanRun
from models.case_features import CaseIssue, CaseIssueLink
from services.plan_tree import uses_tree, remember_tree, save_node
from services.plan_orchestration import ACTIVE, build_report
from core.project_access import require_project_access
from core.logger import logger

RESULTS = {"pending":"pending", "pass":"passed", "fail":"failed", "broken":"error", "error":"error", "skip":"skipped"}
NATIVE_RESULTS = {'pending': 'PENDING', 'running': 'RUNNING', 'passed': 'SUCCESS', 'pass': 'SUCCESS',
                  'failed': 'ERROR', 'fail': 'ERROR', 'error': 'ERROR', 'broken': 'ERROR',
                  'fake_error': 'FAKE_ERROR', 'skipped': 'SKIPPED', 'skip': 'SKIPPED', 'cancelled': 'SKIPPED'}


def descendants(rows, root):
    found, pending = {root}, [root]
    while pending:
        parent = pending.pop()
        for row in rows:
            if row.parent_id == parent and row.id not in found:
                found.add(row.id); pending.append(row.id)
    return found


def entries(db, plan, category):
    nodes = db.query(PlanNode).filter_by(plan_id=plan.id).order_by(PlanNode.position, PlanNode.created_at).all()
    points = {node.id:node for node in nodes if node.node_type == "point"}
    uses = uses_tree(db, plan.id)
    associations = []
    if uses:
        suite_ids = {node.suite_id for node in nodes if node.suite_id}
        suites = {row.id:row for row in db.query(TestSuite).filter(TestSuite.id.in_(suite_ids), TestSuite.plan_id == plan.id)}
        for node in nodes:
            if node.node_type == "point" or node.category != category: continue
            suite = suites.get(node.suite_id)
            for case_id in [node.case_id] if node.case_id else (suite.case_ids if suite else []):
                associations.append(("node", node, case_id, node.parent_id, node.node_type == "suite"))
    else:
        for relation in db.query(PlanCaseRelation).filter_by(plan_id=plan.id).order_by(PlanCaseRelation.execution_order):
            associations.append(("legacy", relation, relation.case_id, relation.collection_id, False))
    ids = {item[2] for item in associations}
    cases = {case.id:case for case in db.query(TestCase).filter(TestCase.id.in_(ids))}
    source_ids = {case.project_id for case in cases.values()} or {plan.project_id}
    projects = {p.id:p for p in db.query(Project).filter(Project.id.in_(source_ids))}
    modules = db.query(Module).filter(Module.project_id.in_(source_ids)).order_by(Module.sort_order, Module.created_at).all()
    module_names = {row.id:row.name for row in modules}
    user_ids = {uid for case in cases.values() for uid in (case.created_by,case.executor_id) if uid}
    user_ids.update(row.assigned_to for _,row,_,_,_ in associations if row.assigned_to)
    users = {row.id:row.username for row in db.query(User).filter(User.id.in_(user_ids))}
    bugs = {}
    for link, issue in db.query(CaseIssueLink,CaseIssue).join(CaseIssue, CaseIssue.id == CaseIssueLink.issue_id).filter(CaseIssueLink.case_id.in_(ids), CaseIssue.project_id.in_(source_ids), CaseIssue.kind == 'defect'):
        bugs.setdefault(link.case_id, set()).add(issue.id)
    run = db.query(PlanRun).filter_by(plan_id=plan.id).order_by(PlanRun.created_at.desc()).first()
    results = (run.report if run.status not in ACTIVE and run.report else build_report(db,run))['cases'] if run else []
    by_association = {(item.get('associationId',item['caseId']),item['caseId']):item for item in results}
    association_runs = {key: run for key in by_association}
    native = {}
    if category != 'functional':
        from services.native_candidate_context import NativeCandidateContext
        native = {identifier: NativeCandidateContext(db, identifier, include_reports=False) for identifier in source_ids}
        # 保留每个实例最近一次真实计划结果，后续只执行部分测试套不能抹掉其他实例的历史。
        by_association, association_runs, report_environments = {}, {}, {}
        for historical in db.query(PlanRun).filter_by(plan_id=plan.id).order_by(PlanRun.created_at.desc(), PlanRun.id.desc()):
            report = historical.report if historical.status not in ACTIVE and historical.report else build_report(db, historical)
            report_environments[historical.id] = {item['executionId']: item.get('environmentId') for item in report.get('items', []) if item.get('executionId')}
            execution_states = {item['executionId']: item.get('status') for item in report.get('items', []) if item.get('executionId')}
            for item in report.get('cases', []):
                key = (item.get('associationId') or item['caseId'], item['caseId'])
                if key not in by_association and item.get('result') is not None:
                    by_association[key] = dict(item, result='running') if item['result'] == 'pending' and execution_states.get(item.get('executionId')) in {'running', 'cancelling'} else item
                    association_runs[key] = historical
        execution_users = {row.executor_id for row in association_runs.values() if row.executor_id}
        users.update({row.id: row.username for row in db.query(User).filter(User.id.in_(execution_users))})
        from models.environment import Environment
        environment_ids = {identifier for mapping in report_environments.values() for identifier in mapping.values() if identifier}
        environments = {row.id: row.name for row in db.query(Environment).filter(Environment.id.in_(environment_ids))}
        for key, item in by_association.items():
            actual_run = association_runs[key]
            environment_id = report_environments[actual_run.id].get(item.get('executionId'))
            item = dict(item, executionEnvironmentName=environments.get(environment_id))
            by_association[key] = item
    project = db.get(Project, plan.project_id)
    items = []
    for source, association, case_id, collection_id, grouped in associations:
        case = cases.get(case_id)
        if not case: continue
        actual_category = case.type if case.type in ('api','scenario') else 'functional'
        if source == 'legacy' and actual_category != category: continue
        result_key = (association.id if source == 'node' else case_id,case_id)
        result = by_association.get(result_key)
        result_run = association_runs.get(result_key)
        executor = association.assigned_to
        items.append(dict(id=f'{source}:{association.id}:{case_id}', source=source, associationId=association.id, caseId=case.id,
            name=case.name, caseCode=case.case_code, priority=case.priority, tags=case.tags or [],
            collectionId=collection_id, collectionName=points[collection_id].name if collection_id in points else '默认测试集',
            projectId=case.project_id, projectName=projects[case.project_id].name if case.project_id in projects else '', moduleId=case.module_id, moduleName=module_names.get(case.module_id,'未分配模块'),
            createdAt=case.created_at, updatedAt=case.updated_at, createdByName=users.get(case.created_by,'未知用户'),
            assignedTo=executor, executorName=users.get(executor,'未分配'), isAutomated=case.is_automated, recycled=bool(case.deleted_at),
            result=result['result'] if result else (RESULTS.get(association.execution_status,'pending') if source == 'legacy' and category == 'functional' else 'pending'),
            bugCount=len(bugs.get(case.id,set())), runId=result_run.id if result and result_run else None,
            grouped=grouped, precondition=case.precondition, steps=case.steps, caseEditType=case.case_edit_type,
            textDescription=case.text_description, expectedResult=case.expected_result, description=case.description))
    from services.plan_case_execution import overlay
    items = overlay(db, plan.id, items, run) if category == 'functional' else items
    if category != 'functional':
        for item in items:
            values = native[item['projectId']].values(cases[item['caseId']])
            item.update({key: value for key, value in values.items() if key not in {'lastReportStatus', 'apiChange'}})
            item['nativeResult'] = NATIVE_RESULTS.get(item['result'], item['result'])
            result_key = (item['associationId'] if item['source'] == 'node' else item['caseId'], item['caseId'])
            actual_run = association_runs.get(result_key)
            item['nativeExecutorId'] = actual_run.executor_id if actual_run else None
            item['nativeExecutorName'] = users.get(item['nativeExecutorId'], '-')
            item['nativeExecutionEnvironmentName'] = by_association.get(result_key, {}).get('executionEnvironmentName')
        visible_points = {point.id for point in points.values() if point.category == category}
        for identifier in list(visible_points):
            parent = points[identifier].parent_id
            while parent in points and parent not in visible_points:
                visible_points.add(parent); parent = points[parent].parent_id
        points = {key: point for key, point in points.items() if key in visible_points}
    return items, list(points.values()), modules, uses


def listing(db, plan, category, params):
    items, points, modules, uses = entries(db,plan,category)
    search = (params.get('search') or '').strip().casefold()
    results = set((params.get('result') or '').split(','))
    priorities = set((params.get('priority') or '').split(','))
    selected_protocols = set(params['protocols'].split(',')) if params.get('protocols') is not None else None
    filtered = [item for item in items if (not search or search in (item['name']+' '+item['caseCode']).casefold())
        and (not params.get('priority') or item['priority'] in priorities)
        and (not params.get('result') or item.get('nativeResult', item['result']) in results)
        and (not params.get('executor') or item.get('nativeExecutorId', item['assignedTo']) == params['executor'])
        and (selected_protocols is None or item.get('protocol') in selected_protocols)
        and (not params.get('tag') or params['tag'] in item['tags'])]
    if params.get('filters') is not None:
        from services.plan_case_filter import filter_entries
        filtered = filter_entries(db, plan, items, params['filters'], params.get('user_id'), category)
        if params.get('refine'):
            filtered = [item for item in filtered if
                (not search or search in (item['name']+' '+item['caseCode']).casefold())
                and (not params.get('result') or item.get('nativeResult', item['result']) in results)]
    if params.get('mine'):
        own_ids = {row.id for row in db.query(TestCase.id).filter(TestCase.id.in_([item['caseId'] for item in items]), TestCase.created_by == params.get('user_id'))}
        filtered = [item for item in filtered if item['caseId'] in own_ids]
    def tree_rows(rows, field):
        payload = []
        for row in rows:
            ids=descendants(rows,row.id)
            payload.append(dict(id=row.id,name=row.name,parentId=row.parent_id,count=sum(item[field] in ids for item in filtered),
                                **({'category': row.category} if field == 'collectionId' else {})))
        return payload
    collections=tree_rows(points,'collectionId'); module_tree=tree_rows(modules,'moduleId')
    source_ids = {item['projectId'] for item in items}
    grouped_modules = bool(source_ids - {plan.project_id})
    project_rows = {p.id:p for p in db.query(Project).filter(Project.id.in_(source_ids))}
    if grouped_modules:
        module_projects = {row.id:row.project_id for row in modules}
        for row in module_tree:
            row['projectId'] = module_projects[row['id']]
            row['parentId'] = row['parentId'] or row['projectId']
        for identifier in sorted(source_ids):
            module_tree.append(dict(id=identifier, name=project_rows[identifier].name, parentId=None,
                projectId=identifier, nodeType='PROJECT', count=sum(item['projectId'] == identifier for item in filtered)))
            module_tree.append(dict(id=identifier + '_default', name='未分配模块', parentId=identifier,
                projectId=identifier, nodeType='DEFAULT', count=sum(item['projectId'] == identifier and (not item['moduleId'] or item['moduleId'] not in {m.id for m in modules}) for item in filtered)))
    counts=dict(all=len(filtered),default=sum(not item['collectionId'] for item in filtered),unassigned=sum(not item['moduleId'] or item['moduleId'] not in {row.id for row in modules} for item in filtered))
    folder=params.get('folder')
    if params.get('filters') is None and folder and folder != 'all':
        field, rows = ('collectionId',points) if params['tree_type']=='COLLECTION' else ('moduleId',modules)
        if folder == 'default': filtered=[item for item in filtered if not item['collectionId']]
        elif folder == 'unassigned': filtered=[item for item in filtered if not item['moduleId'] or item['moduleId'] not in {row.id for row in modules}]
        elif params['tree_type'] == 'MODULE' and grouped_modules and folder in source_ids:
            filtered=[item for item in filtered if item['projectId'] == folder]
        elif params['tree_type'] == 'MODULE' and grouped_modules and folder.endswith('_default') and folder[:-8] in source_ids:
            filtered=[item for item in filtered if item['projectId'] == folder[:-8] and (not item['moduleId'] or item['moduleId'] not in {row.id for row in modules})]
        else:
            if folder not in {row.id for row in rows}: raise HTTPException(404,'当前计划或项目中不存在此目录')
            scope=descendants(rows,folder) if params['include_descendants'] else {folder}
            filtered=[item for item in filtered if item[field] in scope]
    filtered.sort(key=lambda item:(str(item.get(params['sort']) or ''),item['id']),reverse=params['direction']=='desc')
    page,size=params['page'],params['size'];total=len(filtered)
    payload = dict(items=filtered if params.get("view")=="mind" else filtered[(page-1)*size:page*size],total=total,page=page,size=size,collections=collections,modules=module_tree,counts=counts,usesTree=uses,projects=[dict(id=p.id, name=p.name) for p in project_rows.values()])
    if category != 'functional':
        payload['nativeOptions'] = dict(protocols=sorted({item['protocol'] for item in items if item.get('protocol')}),
            environments=list({item['environmentName']: dict(id=item['environmentName'], name=item['environmentLabel']) for item in items if item.get('environmentName')}.values()))
    return payload


def collection(db, plan, identifier, category=None):
    row=db.get(PlanNode,identifier) if identifier else None
    if identifier and (not row or row.plan_id != plan.id or row.node_type != 'point'):
        raise HTTPException(422,'测试集必须是当前计划的测试点')
    if row and category and row.category != category:
        raise HTTPException(422,'测试集必须属于当前用例分类')
    return row


def selected_rows(db,plan,selections,category):
    visible={ (item['source'],item['associationId']) for item in entries(db,plan,category)[0] if not item['grouped'] }
    keys=[(item.source,item.id) for item in selections]
    if len(set(keys)) != len(keys): raise HTTPException(422,'不能重复选择同一关联')
    if not set(keys) <= visible: raise HTTPException(404,'关联不存在、不属于此分类或需要在测试规划中管理')
    return [(source,db.get(PlanNode if source=='node' else PlanCaseRelation,identifier)) for source,identifier in keys]


def batch(db,plan,user,data):
    workspace=db.get(PlanWorkspace,plan.id)
    if workspace and workspace.archived: raise HTTPException(409,'归档计划不可修改关联')
    rows=selected_rows(db,plan,data.selections,data.category)
    if data.action=='assign' and data.assignedTo:
        assignee=db.get(User,data.assignedTo)
        if not assignee or not assignee.status: raise HTTPException(422,'执行人不存在或已停用')
        require_project_access(db,assignee,plan.project_id,'test_plan:read')
    if data.action=='move': collection(db,plan,data.collectionId,data.category)
    if data.action=='unlink':
        legacy_ids={row.id for source,row in rows if source=='legacy'}
        remaining={row.case_id for row in db.query(PlanCaseRelation).filter(PlanCaseRelation.plan_id==plan.id,~PlanCaseRelation.id.in_(legacy_ids))}
        removed={row.case_id for source,row in rows if source=='legacy'}-remaining
        affected=[suite for suite in db.query(TestSuite).filter_by(plan_id=plan.id) if removed.intersection(suite.case_ids or [])]
        from services.test_suite_service import TestSuiteService
        for suite in affected:
            try: TestSuiteService.require_idle(db,suite.id)
            except ValueError as exc:
                logger.exception('测试套执行中，拒绝取消对应计划关联：测试套={}',suite.id)
                raise HTTPException(409,str(exc)) from exc
        for suite in affected:
            suite.case_ids=[case_id for case_id in suite.case_ids if case_id not in removed]
    for source,row in rows:
        if data.action=='assign': row.assigned_to=data.assignedTo or None
        elif data.action=='move':
            if source=='node': save_node(db,plan,{'parentId':data.collectionId or None},row)
            else: row.collection_id=data.collectionId or None
        else:
            if source=='node':
                remember_tree(db,plan.id)
                db.query(PlanNode).filter_by(linked_functional_id=row.id).update({'linked_functional_id':None})
            db.delete(row)
    logger.info('已更新计划分类关联：计划={}，分类={}，操作={}，数量={}',plan.id,data.category,data.action,len(rows))
    return dict(updated=len(rows))


def associate(db,plan,user,data):
    from services.plan_candidate_selection import resolve
    cases, summary, suites, relations = resolve(db, plan, user, data, writing=True)
    collection(db,plan,data.collectionId,data.category)
    uses=summary['usesTree']
    suite=next((s for s in suites if s.id == data.suiteId), None)
    if data.suiteId and (not suite or suite.plan_id != plan.id):
        raise HTTPException(422,'测试套必须属于当前计划')
    if uses and any(case.is_automated and (not suite or suite.plan_id!=plan.id or case.id not in (suite.case_ids or [])) for case in cases):
        raise HTTPException(422,'自动化用例需要选择包含所有关联用例的当前计划测试套')
    sync_groups, sync_suites = {}, {}
    if data.syncCase:
        from services.plan_candidate_sync import resolve as resolve_sync, validate_suites
        sync_groups, _ = resolve_sync(db, plan, data, cases, suites, relations, uses, current_read=True)
        sync_suites = validate_suites(sync_groups, data, suites, uses)
    existing={row.case_id for row in relations}
    order=max((r.execution_order or 0 for r in relations), default=-1)+1
    added=0
    for case in cases:
        if uses: save_node(db,plan,dict(name=case.name,nodeType='case',category=data.category,caseId=case.id,parentId=data.collectionId,suiteId=suite.id if case.is_automated and suite else None), source_project_id=case.project_id)
        elif case.id not in existing:
            db.add(PlanCaseRelation(plan_id=plan.id,case_id=case.id,collection_id=data.collectionId,execution_order=order+added))
        else: continue
        added+=1
    logger.info('已关联计划分类用例：计划={}，分类={}，数量={}',plan.id,data.category,added)
    result = dict(added=added)
    if data.syncCase:
        result['synced'] = {}
        for category, group in sync_groups.items():
            count = 0
            for case in group['cases']:
                if uses:
                    save_node(db, plan, dict(name=case.name, nodeType='case', category=category, caseId=case.id,
                                            parentId=group['collectionId'], suiteId=sync_suites[category].id), source_project_id=case.project_id)
                else:
                    db.add(PlanCaseRelation(plan_id=plan.id, case_id=case.id, collection_id=group['collectionId'], execution_order=order+added+sum(result['synced'].values())+count))
                count += 1
            result['synced'][category] = count
        logger.info('已同步功能用例关联：计划={}，功能={}，接口={}，场景={}', plan.id, added, result['synced']['api'], result['synced']['scenario'])
    return result


def candidates(db, plan, category, search, folder, priority, page, size, *, filters=None, mine=False, user_id=None, source=None):
    """数据库分页取可关联用例，目录计数不受当前页或目录范围影响。"""
    from services.case_candidates import candidates as shared_candidates
    source = source or plan
    if filters is not None or mine:
        from services.plan_candidate_filter import advanced_candidates
        result = advanced_candidates(db, source, category, filters, mine, user_id, page, size)
    else:
        result = shared_candidates(db, source.project_id, category, search, folder, priority, page, size)
    associated, points, _, uses = entries(db, plan, category)
    linked = {item['caseId'] for item in associated}
    items = [dict(item, alreadyLinked=item['id'] in linked) for item in result['items']]
    suites = [dict(id=row.id, name=row.name, caseIds=row.case_ids or []) for row in db.query(TestSuite).filter_by(plan_id=plan.id)]
    if category != 'functional' and filters is None and not mine:
        from services.native_candidate_context import NativeCandidateContext
        native = NativeCandidateContext(db, source.project_id)
        cases = {row.id: row for row in db.query(TestCase).filter(TestCase.id.in_([item['id'] for item in items]))}
        items = [dict(item, **native.values(cases[item['id']])) for item in items]
    project = db.get(Project, source.project_id)
    plans = [dict(id=p.id, name=p.name) for p in db.query(TestPlan).filter_by(project_id=source.project_id)]
    return dict(**{key:value for key,value in result.items() if key != "items"}, items=items, usesTree=uses,
                projectId=source.project_id, projectName=project.name, plans=plans,
                collections=[dict(id=row.id, name=row.name, parentId=row.parent_id, count=0) for row in points], suites=suites,
                syncCollections={kind: [dict(id='default', name='默认测试集', count=0)] + [dict(id=row.id, name=row.name, parentId=row.parent_id, count=0) for row in points if row.category == kind] for kind in ('api', 'scenario')})
