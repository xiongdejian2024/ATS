"""计划关联列表及原子批量管理，兼容直接关联和独立树实例。"""
from fastapi import HTTPException
from models import TestCase, TestSuite, Module, User, PlanCaseRelation, Project
from models.plan_workspace import PlanNode, PlanWorkspace
from models.plan_orchestration import PlanRun
from models.case_features import CaseIssue, CaseIssueLink
from services.plan_tree import uses_tree, remember_tree, save_node
from services.plan_orchestration import ACTIVE, build_report
from core.project_access import require_project_access
from core.logger import logger

RESULTS = {"pending":"pending", "pass":"passed", "fail":"failed", "broken":"error", "error":"error", "skip":"skipped"}


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
    cases = {case.id:case for case in db.query(TestCase).filter(TestCase.id.in_(ids), TestCase.project_id == plan.project_id)}
    modules = db.query(Module).filter_by(project_id=plan.project_id).order_by(Module.sort_order, Module.created_at).all()
    module_names = {row.id:row.name for row in modules}
    user_ids = {uid for case in cases.values() for uid in (case.created_by,case.executor_id) if uid}
    user_ids.update(row.assigned_to for _,row,_,_,_ in associations if row.assigned_to)
    users = {row.id:row.username for row in db.query(User).filter(User.id.in_(user_ids))}
    bugs = {}
    for link, issue in db.query(CaseIssueLink,CaseIssue).join(CaseIssue, CaseIssue.id == CaseIssueLink.issue_id).filter(CaseIssueLink.case_id.in_(ids), CaseIssue.project_id == plan.project_id, CaseIssue.kind == 'defect'):
        bugs.setdefault(link.case_id, set()).add(issue.id)
    run = db.query(PlanRun).filter_by(plan_id=plan.id).order_by(PlanRun.created_at.desc()).first()
    results = (run.report if run.status not in ACTIVE and run.report else build_report(db,run))['cases'] if run else []
    by_association = {(item.get('associationId',item['caseId']),item['caseId']):item for item in results}
    project = db.get(Project, plan.project_id)
    items = []
    for source, association, case_id, collection_id, grouped in associations:
        case = cases.get(case_id)
        if not case: continue
        actual_category = case.type if case.type in ('api','scenario') else 'functional'
        if source == 'legacy' and actual_category != category: continue
        result = by_association.get((association.id if source == 'node' else case_id,case_id))
        executor = association.assigned_to
        items.append(dict(id=f'{source}:{association.id}:{case_id}', source=source, associationId=association.id, caseId=case.id,
            name=case.name, caseCode=case.case_code, priority=case.priority, tags=case.tags or [],
            collectionId=collection_id, collectionName=points[collection_id].name if collection_id in points else '默认测试集',
            projectName=project.name if project else '', moduleId=case.module_id, moduleName=module_names.get(case.module_id,'未分配模块'),
            createdAt=case.created_at, updatedAt=case.updated_at, createdByName=users.get(case.created_by,'未知用户'),
            assignedTo=executor, executorName=users.get(executor,'未分配'), isAutomated=case.is_automated, recycled=bool(case.deleted_at),
            result=result['result'] if result else (RESULTS.get(association.execution_status,'pending') if source == 'legacy' else 'pending'),
            bugCount=len(bugs.get(case.id,set())), runId=run.id if result else None,
            grouped=grouped, precondition=case.precondition, steps=case.steps, caseEditType=case.case_edit_type,
            textDescription=case.text_description, expectedResult=case.expected_result, description=case.description))
    from services.plan_case_execution import overlay
    return overlay(db, plan.id, items, run), list(points.values()), modules, uses


def listing(db, plan, category, params):
    items, points, modules, uses = entries(db,plan,category)
    search = (params.get('search') or '').strip().casefold()
    results = set((params.get('result') or '').split(','))
    filtered = [item for item in items if (not search or search in (item['name']+' '+item['caseCode']).casefold())
        and (not params.get('priority') or item['priority'] == params['priority'])
        and (not params.get('result') or item['result'] in results)
        and (not params.get('executor') or item['assignedTo'] == params['executor'])
        and (not params.get('tag') or params['tag'] in item['tags'])]
    def tree_rows(rows, field):
        payload = []
        for row in rows:
            ids=descendants(rows,row.id)
            payload.append(dict(id=row.id,name=row.name,parentId=row.parent_id,count=sum(item[field] in ids for item in filtered)))
        return payload
    collections=tree_rows(points,'collectionId'); module_tree=tree_rows(modules,'moduleId')
    counts=dict(all=len(filtered),default=sum(not item['collectionId'] for item in filtered),unassigned=sum(not item['moduleId'] or item['moduleId'] not in {row.id for row in modules} for item in filtered))
    folder=params.get('folder')
    if folder and folder != 'all':
        field, rows = ('collectionId',points) if params['tree_type']=='COLLECTION' else ('moduleId',modules)
        if folder == 'default': filtered=[item for item in filtered if not item['collectionId']]
        elif folder == 'unassigned': filtered=[item for item in filtered if not item['moduleId'] or item['moduleId'] not in {row.id for row in modules}]
        else:
            if folder not in {row.id for row in rows}: raise HTTPException(404,'当前计划或项目中不存在此目录')
            scope=descendants(rows,folder) if params['include_descendants'] else {folder}
            filtered=[item for item in filtered if item[field] in scope]
    filtered.sort(key=lambda item:(str(item.get(params['sort']) or ''),item['id']),reverse=params['direction']=='desc')
    page,size=params['page'],params['size'];total=len(filtered)
    return dict(items=filtered if params.get("view")=="mind" else filtered[(page-1)*size:page*size],total=total,page=page,size=size,collections=collections,modules=module_tree,counts=counts,usesTree=uses)


def collection(db, plan, identifier):
    row=db.get(PlanNode,identifier) if identifier else None
    if identifier and (not row or row.plan_id != plan.id or row.node_type != 'point'):
        raise HTTPException(422,'测试集必须是当前计划的测试点')
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
    if data.action=='move': collection(db,plan,data.collectionId)
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
    workspace=db.get(PlanWorkspace,plan.id)
    if workspace and workspace.archived: raise HTTPException(409,'归档计划不可修改关联')
    collection(db,plan,data.collectionId)
    if len(set(data.caseIds)) != len(data.caseIds): raise HTTPException(422,'关联用例不能重复')
    cases=db.query(TestCase).filter(TestCase.id.in_(data.caseIds),TestCase.project_id==plan.project_id,TestCase.deleted_at.is_(None)).all()
    if len(cases)!=len(data.caseIds): raise HTTPException(404,'用例不存在、已回收或不属于当前项目')
    uses=uses_tree(db,plan.id)
    if any((case.type if case.type in ('api','scenario') else 'functional') != data.category for case in cases):
        raise HTTPException(422,'请选择当前分类的用例')
    if data.category != 'functional' and any(not case.is_automated for case in cases):
        raise HTTPException(422,'API/场景分类只能关联可执行的自动化用例')
    suite=db.get(TestSuite,data.suiteId) if data.suiteId else None
    if data.suiteId and (not suite or suite.plan_id != plan.id):
        raise HTTPException(422,'测试套必须属于当前计划')
    if uses and any(case.is_automated and (not suite or suite.plan_id!=plan.id or case.id not in suite.case_ids) for case in cases):
        raise HTTPException(422,'自动化用例需要选择包含所有关联用例的当前计划测试套')
    existing={row.case_id for row in db.query(PlanCaseRelation).filter_by(plan_id=plan.id)}
    order=db.query(PlanCaseRelation).filter_by(plan_id=plan.id).count()
    added=0
    for case in cases:
        if uses: save_node(db,plan,dict(name=case.name,nodeType='case',category=data.category,caseId=case.id,parentId=data.collectionId,suiteId=suite.id if case.is_automated and suite else None))
        elif case.id not in existing:
            db.add(PlanCaseRelation(plan_id=plan.id,case_id=case.id,collection_id=data.collectionId,execution_order=order+added))
        else: continue
        added+=1
    logger.info('已关联计划分类用例：计划={}，分类={}，数量={}',plan.id,data.category,added)
    return dict(added=added)


def candidates(db, plan, category, search, folder, priority, page, size):
    """数据库分页取可关联用例，目录计数不受当前页或目录范围影响。"""
    from services.case_candidates import candidates as shared_candidates
    result = shared_candidates(db, plan.project_id, category, search, folder, priority, page, size)
    associated, points, _, uses = entries(db, plan, category)
    linked = {item['caseId'] for item in associated}
    items = [dict(item, alreadyLinked=item['id'] in linked) for item in result['items']]
    suites = [dict(id=row.id, name=row.name, caseIds=row.case_ids or []) for row in db.query(TestSuite).filter_by(plan_id=plan.id)]
    return dict(**{key:value for key,value in result.items() if key != "items"}, items=items, usesTree=uses,
                collections=[dict(id=row.id, name=row.name, parentId=row.parent_id, count=0) for row in points], suites=suites)
