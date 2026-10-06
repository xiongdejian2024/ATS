"""计划实例缺陷：项目权限与关联锁内核对，复用现有缺陷业务模型。"""
import hashlib
import json
from fastapi import HTTPException
from models import Project
from models.case_features import CaseIssue
from models.plan_case_defect import PlanCaseDefect
from models.plan_case_execution import PlanCaseExecution
from models.plan_workspace import PlanWorkspace
from services.plan_native_selection import resolve
from services.plan_case_workspace import entries
from core.project_access import project_allows
from core.logger import logger
from utils.serializer import serialize_model


def capabilities(db, plan, user, *, available=True):
    settings = db.get(PlanWorkspace, plan.id)
    project = db.get(Project, plan.project_id)
    associate = bool(available and not (settings and settings.archived)
        and project_allows(db, user, project, 'test_plan:execute'))
    return dict(canAssociate=associate, canCreate=associate and project_allows(db, user, project, 'test_case:update'))


def preview(db, plan, user, selection):
    plan, user, rows, summary = resolve(db, plan, user, selection)
    return dict(**summary, **capabilities(db, plan, user, available=bool(rows)))


def query(db, plan):
    return db.query(PlanCaseDefect, CaseIssue).join(CaseIssue, CaseIssue.id == PlanCaseDefect.issue_id).filter(
        PlanCaseDefect.plan_id == plan.id, PlanCaseDefect.active.is_(True),
        CaseIssue.project_id == plan.project_id, CaseIssue.kind == 'defect')


def listing(db, plan, user, key, page, size, search):
    current = next((row for row in entries(db, plan, 'functional')[0] if row['id'] == key and not row['grouped']), None)
    if not current and not db.query(PlanCaseDefect.id).filter_by(plan_id=plan.id, association_key=key).first() and not db.query(PlanCaseExecution.id).filter_by(plan_id=plan.id, association_key=key).first():
        raise HTTPException(404, '当前计划没有此功能用例关联或历史')
    rows = query(db, plan).filter(PlanCaseDefect.association_key == key)
    if search.strip(): rows = rows.filter(CaseIssue.title.contains(search.strip(), autoescape=True))
    total = rows.count()
    result = []
    for link, issue in rows.order_by(PlanCaseDefect.created_at.desc(), PlanCaseDefect.id.desc()).offset((page-1)*size).limit(size):
        result.append(dict(**serialize_model(issue, camel_case=True), linkId=link.id, associationKey=key, caseName=link.case_snapshot.get('name', ''), linkedAt=link.created_at))
    return dict(items=result, total=total, page=page, size=size, detached=not bool(current),
        **capabilities(db, plan, user, available=bool(current and not current['recycled'])))


def candidates(db, plan, page, size, search):
    rows = db.query(CaseIssue).filter_by(project_id=plan.project_id, kind='defect')
    if search.strip(): rows = rows.filter(CaseIssue.title.contains(search.strip(), autoescape=True))
    total = rows.count()
    return dict(items=[serialize_model(row, camel_case=True) for row in rows.order_by(CaseIssue.created_at.desc(), CaseIssue.id.desc()).offset((page-1)*size).limit(size)], total=total, page=page, size=size)


def bind(db, plan, user, selected, issues, *, request=None, digest=None):
    if len(selected) * len(issues) > 10000:
        raise HTTPException(422, '每批最多绑定10000条实例缺陷关系，请缩小范围；不会截断选择')
    links = { (row.association_key, row.issue_id): row for row in db.query(PlanCaseDefect).filter(
        PlanCaseDefect.plan_id == plan.id, PlanCaseDefect.association_key.in_([r['id'] for r in selected]),
        PlanCaseDefect.issue_id.in_([issue.id for issue in issues])).populate_existing().with_for_update() }
    count = 0
    for item in selected:
        for issue in issues:
            key = (item['id'], issue.id)
            row = links.get(key)
            if row and row.active: continue
            if not row:
                row = PlanCaseDefect(plan_id=plan.id, association_key=item['id'], issue_id=issue.id,
                    case_id=item['caseId'], case_snapshot=dict(id=item['caseId'], name=item['name'], caseCode=item['caseCode'], projectId=item['projectId']),
                    created_by=str(user.id), create_request_id=request, create_payload_hash=digest)
                db.add(row)
            row.active = True
            row.updated_by = str(user.id)
            count += 1
    db.flush()
    logger.info('计划实例缺陷绑定完成：计划={}，实例={}，缺陷={}，新关联={}', plan.id, len(selected), len(issues), count)
    return count


def associate(db, plan, user, data):
    plan, user, rows, _ = resolve(db, plan, user, data, writing=True, action='execute')
    if not rows: raise HTTPException(409, '当前选择范围已为空，请刷新后重新选择')
    issues = db.query(CaseIssue).filter(CaseIssue.id.in_(data.issueIds), CaseIssue.project_id == plan.project_id, CaseIssue.kind == 'defect').populate_existing().with_for_update().all()
    if len(issues) != len(data.issueIds): raise HTTPException(404, '缺陷不存在或不属于计划项目')
    return dict(updated=bind(db, plan, user, rows, issues))


def create(db, plan, user, data):
    plan, user, rows, _ = resolve(db, plan, user, data, writing=True, action='execute')
    from core.project_access import require_project_access
    require_project_access(db, user, plan.project_id, 'test_case:update', current_read=True)
    body = dict(payload=data.model_dump(mode='json', exclude={'requestId'}), userId=str(user.id))
    digest = hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    previous = db.query(PlanCaseDefect).filter_by(plan_id=plan.id, create_request_id=str(data.requestId)).populate_existing().with_for_update().all()
    if previous:
        if any(link.create_payload_hash != digest for link in previous): raise HTTPException(409, '同一请求编号不能新建不同范围或内容的缺陷')
        return dict(issueId=previous[0].issue_id, updated=len(previous), replayed=True)
    if not rows: raise HTTPException(409, '当前选择范围已为空，请刷新后重新选择')
    from services.case_features import write_issue
    from schemas.case_features import IssueWrite
    issue = write_issue(db, user, plan.project_id, IssueWrite(kind='defect', title=data.title, description=data.description))
    count = bind(db, plan, user, rows, [issue], request=str(data.requestId), digest=digest)
    logger.info('已新建计划实例缺陷：计划={}，缺陷={}，请求={}', plan.id, issue.id, data.requestId)
    return dict(issueId=issue.id, updated=count, replayed=False)


def disassociate(db, plan, user, link_id):
    link = db.query(PlanCaseDefect).filter_by(plan_id=plan.id, id=link_id).first()
    if not link: raise HTTPException(404, '此计划没有该缺陷关联')
    from schemas.plan_functional_minder import FunctionalMinderSelection
    resolve(db, plan, user, FunctionalMinderSelection(selectIds=[link.association_key]), writing=True, action='execute')
    link = db.query(PlanCaseDefect).filter_by(plan_id=plan.id, id=link_id).populate_existing().with_for_update().one()
    link.active = False
    link.updated_by = str(user.id)
    logger.info('已取消计划实例缺陷关联：计划={}，关联={}', plan.id, link.id)
    return dict(updated=1)
