"""主列表、导出和批量操作共用范围；写入取得项目锁后重新查询。"""

from fastapi import HTTPException
from models import TestCase, Project
from core.project_access import require_project_access, project_allows
from core.logger import logger
from services.case_query import query_cases
from services.review_workspace import lock_project

LIMIT = 10000
SELECTION_FIELDS = {"selectAll", "caseIds", "excludeIds", "includeIds", "condition"}


def resolve(db, user, project_id, body, *, writing=False, action="read"):
    require_project_access(db, user, project_id, f"test_case:{action}")
    if writing:
        lock_project(db, project_id)
    if body.selectAll:
        result = query_cases(
            db, project_id, **body.condition.model_dump(exclude_none=True),
            user_id=str(user.id), page=1, size=LIMIT + len(body.excludeIds) + 1,
            current_read=writing,
        )
        excluded = set(body.excludeIds)
        cases = [case for case in result["items"] if case.id not in excluded]
        count = result["total"] - sum(case.id in excluded for case in result["items"])
        # 超过读取边界时，未读到的排除项只能减少数量，不能证明范围在上限内。
        if result["total"] > LIMIT + len(body.excludeIds):
            raise HTTPException(422, "每批最多操作10000条用例，请缩小筛选范围")
        excluded_count = result["total"] - count
    else:
        cases = []
        excluded_count = 0
    explicit = body.includeIds if body.selectAll else body.caseIds
    if explicit:
        query = db.query(TestCase).filter(
            TestCase.project_id == project_id, TestCase.deleted_at.is_(None),
            TestCase.id.in_(explicit),
        )
        if writing:
            query = query.populate_existing().with_for_update()
        extra = query.order_by(TestCase.id).all()
        if len(extra) != len(explicit):
            raise HTTPException(404, "选择中包含其他项目或已回收的用例，请重新选择")
        cases = list({case.id: case for case in cases + extra}.values())
    if len(cases) > LIMIT:
        raise HTTPException(422, "每批最多操作10000条用例，请缩小筛选范围")
    if writing and not cases:
        raise HTTPException(409, "当前范围已无可操作用例，请刷新后重新选择")
    if writing:
        logger.info(
            "主用例批量范围已解析 project_id={} actor_id={} select_all={} count={} excluded={}",
            project_id, user.id, body.selectAll, len(cases), excluded_count,
        )
    return cases, excluded_count


def preview(db, user, project_id, body):
    cases, excluded = resolve(db, user, project_id, body)
    project = db.get(Project, project_id)
    return dict(
        count=len(cases), excludedCount=excluded,
        permissions={action: project_allows(db, user, project, f"test_case:{action}")
                     for action in ["update", "create", "delete", "export"]},
    )


def delete(db, user, project_id, body):
    from services.test_case_service import TestCaseService
    cases, _ = resolve(db, user, project_id, body, writing=True, action="delete")
    for case in cases:
        TestCaseService.delete_test_case(db, case.id, str(user.id), commit=False)
    logger.info("主用例批量移入回收站已暂存 project_id={} count={}", project_id, len(cases))
    return dict(deleted=len(cases))


def link_issue(db, user, project_id, body):
    from models.case_features import CaseIssueLink
    from services.case_features import issue_for_project, change
    cases, _ = resolve(db, user, project_id, body, writing=True, action="update")
    issue_for_project(db, project_id, body.issueId)
    existing = {row[0] for row in db.query(CaseIssueLink.case_id).filter(
        CaseIssueLink.issue_id == body.issueId,
        CaseIssueLink.case_id.in_([case.id for case in cases]),
    ).with_for_update().all()}
    for case in cases:
        if case.id not in existing:
            db.add(CaseIssueLink(case_id=case.id, issue_id=body.issueId, created_by=str(user.id)))
            change(db, case, user.id, "关联需求缺陷", {"issueId": body.issueId})
    db.flush()
    logger.info("主用例批量关联已暂存 project_id={} count={} newly_linked={}", project_id, len(cases), len(cases)-len(existing))
    return dict(linked=len(cases), created=len(cases)-len(existing))
