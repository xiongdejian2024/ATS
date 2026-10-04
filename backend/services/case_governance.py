"""用例治理：不可变快照、版本锁定评审及项目内批量更新。"""

from copy import deepcopy
from fastapi import HTTPException
from sqlalchemy import select
from models import TestCase, User
from models.project import Project, ProjectMember
from models.module import Module
from models.case_governance import (
    CaseVersion,
    CaseReview,
    CaseReviewItem,
    CaseReviewDecision,
    CaseReviewComment,
)
from core.project_access import require_project_access
from core.logger import logger
from utils.datetime_utils import beijing_now

SNAPSHOT_FIELDS = (
    "case_code",
    "name",
    "type",
    "priority",
    "precondition",
    "steps",
    "requirement_ref",
    "module_path",
    "module_id",
    "level",
    "executor_id",
    "tags",
    "is_automated",
)


def project_access(db, user, project_id, action="read"):
    """评审和查看允许项目成员；写入继续使用既有明确权限。"""
    return require_project_access(db, user, project_id, f"test_case:{action}")


def case_for_project(db, project_id, case_id, lock=False):
    query = db.query(TestCase).filter_by(project_id=project_id, id=case_id)
    case = (query.with_for_update() if lock else query).first()
    if not case:
        raise HTTPException(404, "项目中不存在该用例")
    return case


def latest_version(db, case_id):
    return (
        db.query(CaseVersion)
        .filter_by(case_id=case_id)
        .order_by(CaseVersion.version.desc())
        .first()
    )


def snapshot_case(db, case, actor_id, reason, force=False):
    """由写事务调用；不自行 commit，失败时原用例与快照一起回滚。"""
    snapshot = {field: deepcopy(getattr(case, field)) for field in SNAPSHOT_FIELDS}
    previous = latest_version(db, case.id)
    if previous and previous.snapshot == snapshot and not force:
        return previous
    version = CaseVersion(
        project_id=case.project_id,
        case_id=case.id,
        version=(previous.version + 1 if previous else 1),
        snapshot=snapshot,
        reason=reason,
        created_by=actor_id,
    )
    db.add(version)
    db.flush()
    logger.info(
        "用例版本已保存 case_id={} version={} actor_id={}",
        case.id,
        version.version,
        actor_id,
    )
    return version


def version_data(version):
    return dict(
        id=version.id,
        caseId=version.case_id,
        version=version.version,
        snapshot=version.snapshot,
        reason=version.reason,
        createdBy=version.created_by,
        createdAt=version.created_at.isoformat(),
    )


def restore_version(db, user, project_id, case_id, version_id, request):
    project_access(db, user, project_id, "update")
    case = case_for_project(db, project_id, case_id, lock=True)
    target = (
        db.query(CaseVersion)
        .filter_by(id=version_id, project_id=project_id, case_id=case_id)
        .first()
    )
    if not target:
        raise HTTPException(404, "版本不存在")
    current = snapshot_case(db, case, str(user.id), "回滚前保存当前内容")
    if current.version != request.expectedVersion:
        raise HTTPException(409, "用例已经被修改，请刷新版本后重试")
    module_id = target.snapshot.get("module_id")
    if (
        module_id
        and not db.query(Module).filter_by(id=module_id, project_id=project_id).first()
    ):
        raise HTTPException(409, "历史版本所属模块已不存在，请先恢复模块")
    executor_id = target.snapshot.get("executor_id")
    if executor_id and not db.get(User, executor_id):
        raise HTTPException(409, "历史版本执行人已不存在")
    for field in SNAPSHOT_FIELDS:
        setattr(case, field, deepcopy(target.snapshot.get(field)))
    case.updated_by = str(user.id)
    case.updated_at = beijing_now()
    version = snapshot_case(
        db, case, str(user.id), f"恢复 v{target.version}：{request.reason}", force=True
    )
    return version


def reviewers(db, project_id):
    project = db.get(Project, project_id)
    ids = {
        m.user_id
        for m in db.query(ProjectMember).filter_by(project_id=project_id).all()
    } | {project.owner_id}
    return [
        dict(id=u.id, name=u.full_name or u.username)
        for u in db.query(User).filter(User.id.in_(ids), User.status.is_(True)).all()
    ]


def create_review(db, user, project_id, request):
    project_access(db, user, project_id, "update")
    eligible = {r["id"] for r in reviewers(db, project_id)}
    if not set(request.reviewerIds) <= eligible:
        raise HTTPException(422, "评审人必须为本项目的有效成员或负责人")
    cases = [
        case_for_project(db, project_id, cid, lock=True)
        for cid in sorted(request.caseIds)
    ]
    review = CaseReview(
        project_id=project_id,
        name=request.name,
        policy=request.policy,
        reviewer_ids=request.reviewerIds,
        created_by=str(user.id),
        status="pending",
    )
    db.add(review)
    db.flush()
    for case in cases:
        version = snapshot_case(db, case, str(user.id), "提交评审时保存版本")
        db.add(
            CaseReviewItem(
                review_id=review.id,
                case_id=case.id,
                version_id=version.id,
                status="pending",
            )
        )
    db.flush()
    logger.info(
        "用例评审已创建 review_id={} case_count={} policy={}",
        review.id,
        len(cases),
        request.policy,
    )
    return review


def get_review(db, user, project_id, review_id, lock=False):
    project_access(db, user, project_id)
    query = db.query(CaseReview).filter_by(project_id=project_id, id=review_id)
    review = (query.with_for_update() if lock else query).first()
    if not review:
        raise HTTPException(404, "评审不存在")
    return review


def review_data(db, review):
    items = []
    for item in (
        db.query(CaseReviewItem)
        .filter_by(review_id=review.id)
        .order_by(CaseReviewItem.created_at, CaseReviewItem.id)
        .all()
    ):
        version = db.get(CaseVersion, item.version_id)
        case = db.get(TestCase, item.case_id)
        outdated = case is None or any(
            getattr(case, field) != version.snapshot.get(field)
            for field in SNAPSHOT_FIELDS
        )
        decisions = [
            dict(
                reviewerId=d.reviewer_id,
                decision=d.decision,
                comment=d.comment,
                updatedAt=d.updated_at.isoformat(),
            )
            for d in db.query(CaseReviewDecision).filter_by(item_id=item.id).all()
        ]
        items.append(
            dict(
                id=item.id,
                caseId=item.case_id,
                status=item.status,
                version=version.version,
                snapshot=version.snapshot,
                outdated=outdated,
                decisions=decisions,
            )
        )
    comments = [
        dict(
            id=c.id,
            itemId=c.item_id,
            authorId=c.author_id,
            content=c.content,
            createdAt=c.created_at.isoformat(),
        )
        for c in db.query(CaseReviewComment)
        .filter_by(review_id=review.id)
        .order_by(CaseReviewComment.created_at, CaseReviewComment.id)
        .all()
    ]
    return dict(
        id=review.id,
        name=review.name,
        policy=review.policy,
        reviewerIds=review.reviewer_ids,
        status=review.status,
        createdBy=review.created_by,
        createdAt=review.created_at.isoformat(),
        items=items,
        comments=comments,
    )


def vote_review(db, user, project_id, review_id, item_id, request):
    review = get_review(db, user, project_id, review_id, lock=True)
    if str(user.id) not in review.reviewer_ids:
        raise HTTPException(403, "只有指定评审人可以提交结论")
    if review.status != "pending":
        raise HTTPException(409, "评审已结束，请创建新的评审单")
    item = db.query(CaseReviewItem).filter_by(review_id=review.id, id=item_id).first()
    if not item:
        raise HTTPException(404, "评审用例不存在")
    if item.status != "pending":
        raise HTTPException(409, "该用例已完成评审")
    if (
        db.query(CaseReviewDecision)
        .filter_by(item_id=item.id, reviewer_id=str(user.id))
        .first()
    ):
        raise HTTPException(409, "已经提交过评审结论")
    db.add(
        CaseReviewDecision(
            item_id=item.id,
            reviewer_id=str(user.id),
            decision=request.decision,
            comment=request.comment,
        )
    )
    db.flush()
    decisions = db.query(CaseReviewDecision).filter_by(item_id=item.id).all()
    if any(d.decision == "rejected" for d in decisions):
        item.status = "rejected"
    elif review.policy == "any" or len(decisions) == len(review.reviewer_ids):
        item.status = "approved"
    db.flush()
    statuses = [
        i.status for i in db.query(CaseReviewItem).filter_by(review_id=review.id).all()
    ]
    review.status = (
        "rejected"
        if "rejected" in statuses
        else ("approved" if all(s == "approved" for s in statuses) else "pending")
    )
    logger.info(
        "评审结论已记录 review_id={} item_id={} reviewer_id={} decision={}",
        review.id,
        item.id,
        user.id,
        request.decision,
    )
    db.flush()
    return review


def batch_update(db, user, project_id, request):
    project_access(db, user, project_id, "update")
    cases = [
        case_for_project(db, project_id, cid, lock=True)
        for cid in sorted(set(request.caseIds))
    ]
    changes = request.model_dump(exclude_unset=True, exclude={"caseIds"})
    changes = {
        key: value
        for key, value in changes.items()
        if value is not None or key == "moduleId"
    }
    if not changes:
        raise HTTPException(422, "至少选择一个需要更新的字段")
    module = None
    if changes.get("moduleId"):
        module = (
            db.query(Module)
            .filter_by(project_id=project_id, id=changes["moduleId"])
            .first()
        )
        if not module:
            raise HTTPException(422, "目标模块不属于本项目")
    for case in cases:
        snapshot_case(db, case, str(user.id), "批量修改前保存版本")
        for field, value in changes.items():
            setattr(
                case,
                {"isAutomated": "is_automated", "moduleId": "module_id"}.get(
                    field, field
                ),
                value,
            )
            if field == "priority":
                case.level = value
            if field == "moduleId":
                case.module_path = module.name if module else None
        case.updated_by = str(user.id)
        case.updated_at = beijing_now()
        snapshot_case(db, case, str(user.id), "批量修改用例")
    logger.info("批量用例修改已暂存 project_id={} count={}", project_id, len(cases))
    return len(cases)


def batch_copy(db, user, project_id, request):
    from services.test_case_service import TestCaseService
    from schemas.test_case import TestCaseCreate

    project_access(db, user, project_id, "create")
    cases = [
        case_for_project(db, project_id, cid, lock=True)
        for cid in sorted(set(request.caseIds))
    ]
    module = None
    if request.moduleId:
        module = (
            db.query(Module)
            .filter_by(project_id=project_id, id=request.moduleId)
            .first()
        )
        if not module:
            raise HTTPException(422, "目标模块不属于本项目")
    copies = []
    for case in cases:
        data = {field: deepcopy(getattr(case, field)) for field in SNAPSHOT_FIELDS}
        data.update(
            project_id=project_id,
            case_code=None,
            name=case.name[:494] + "（副本）",
            module_id=request.moduleId,
            module_path=module.name if module else None,
        )
        copied = TestCaseService.create_test_case(
            db, TestCaseCreate(**data), str(user.id), commit=False
        )
        copies.append(copied.id)
    logger.info("批量用例复制已暂存 project_id={} count={}", project_id, len(copies))
    return copies


def current_review_statuses(db, cases):
    """按当前内容匹配评审快照；旧版本通过不得展示为当前版本通过。"""
    mapping = {case.id: case for case in cases}
    statuses = {case.id: "not_reviewed" for case in cases}
    if not mapping:
        return statuses
    rows = (
        db.query(CaseReviewItem, CaseVersion, CaseReview)
        .join(CaseVersion, CaseVersion.id == CaseReviewItem.version_id)
        .join(CaseReview, CaseReview.id == CaseReviewItem.review_id)
        .filter(CaseReviewItem.case_id.in_(mapping), CaseReview.status != "cancelled")
        .order_by(CaseReview.created_at.desc(), CaseReview.id.desc())
        .all()
    )
    matched = set()
    for item, version, review in rows:
        if item.case_id in matched:
            continue
        case = mapping[item.case_id]
        if any(
            getattr(case, field) != version.snapshot.get(field)
            for field in SNAPSHOT_FIELDS
        ):
            if statuses[item.case_id] == "not_reviewed":
                statuses[item.case_id] = "resubmit"
            continue
        statuses[item.case_id] = {
            "approved": "passed",
            "rejected": "rejected",
            "pending": "pending",
        }[item.status]
        matched.add(item.case_id)
    return statuses
