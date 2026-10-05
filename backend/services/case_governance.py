"""用例治理：不可变快照、版本锁定评审及项目内批量更新。"""

from copy import deepcopy
from uuid import uuid4
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
    CaseReviewEvent,
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
    "case_edit_type",
    "text_description",
    "expected_result",
    "description",
    "steps",
    "requirement_ref",
    "module_path",
    "module_id",
    "level",
    "executor_id",
    "tags",
    "is_automated",
    "template_id",
    "custom_fields",
)


def project_access(db, user, project_id, action="read"):
    """评审和查看允许项目成员；写入继续使用既有明确权限。"""
    return require_project_access(db, user, project_id, f"test_case:{action}")


def case_for_project(db, project_id, case_id, lock=False):
    if lock:
        from services.review_workspace import lock_project

        lock_project(db, project_id)
    query = (
        db.query(TestCase)
        .filter_by(project_id=project_id, id=case_id)
        .filter(TestCase.deleted_at.is_(None))
    )
    case = (query.populate_existing().with_for_update() if lock else query).first()
    if not case:
        raise HTTPException(404, "项目中不存在该用例")
    return case


def latest_version(db, case_id):
    return (
        db.query(CaseVersion)
        .filter_by(case_id=case_id)
        .order_by(CaseVersion.version.desc())
        .populate_existing()
        .with_for_update()
        .first()
    )


def snapshot_case(db, case, actor_id, reason, force=False):
    """由写事务调用；不自行 commit，失败时原用例与快照一起回滚。"""
    from services.review_workspace import lock_project

    lock_project(db, case.project_id)
    # 普通读取后取得锁时刷新主用例，保留调用方尚未提交的实际编辑。
    if not db.is_modified(case, include_collections=False):
        case = (
            db.query(TestCase)
            .filter_by(id=case.id)
            .populate_existing()
            .with_for_update()
            .one()
        )
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
    from services.case_features import change

    change(
        db,
        case,
        actor_id,
        "保存版本",
        {
            "version": version.version,
            "reason": reason,
            "fields": [
                field
                for field in SNAPSHOT_FIELDS
                if not previous or previous.snapshot.get(field) != snapshot.get(field)
            ],
        },
    )
    logger.info(
        "用例版本已保存 case_id={} version={} actor_id={}",
        case.id,
        version.version,
        actor_id,
    )
    if previous:
        from services.review_auto_resubmit import handle_case_change

        handle_case_change(db, case, actor_id, version, previous.snapshot, snapshot)
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
        value = target.snapshot.get(field)
        if field == "case_edit_type":
            value = value or "STEP"  # 兼容新增文本字段前的不可变历史快照。
        setattr(case, field, deepcopy(value))
    from services.case_features import prepare_case_template

    prepared = prepare_case_template(
        db,
        project_id,
        {"template_id": case.template_id, "custom_fields": case.custom_fields or {}},
        {"template_id", "custom_fields"},
        existing=case,
    )
    case.custom_fields = prepared["custom_fields"]
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
    from services import review_workspace as workspace_service

    workspace_service.lock_project(db, project_id)
    workspace_service.module_for_project(db, project_id, request.moduleId, lock=True)
    eligible = {r["id"] for r in reviewers(db, project_id)}
    requested = set(request.reviewerIds) | {
        v for values in request.itemReviewers.values() for v in values
    }
    if not requested <= eligible:
        raise HTTPException(422, "评审人必须为本项目的有效成员或负责人")
    cases = [
        case_for_project(db, project_id, cid, lock=True)
        for cid in sorted(request.caseIds)
    ]
    review = CaseReview(
        project_id=project_id,
        name=request.name,
        policy=(
            "any"
            if (
                request.mode == "single"
                or (not request.mode and request.policy == "any")
            )
            else "all"
        ),
        mode=request.mode or ("single" if request.policy == "any" else "multiple"),
        description=request.description,
        start_date=request.startDate,
        end_date=request.endDate,
        created_at=beijing_now(),
        reviewer_ids=request.reviewerIds,
        created_by=str(user.id),
        status="pending",
    )
    db.add(review)
    db.flush()
    workspace_service.set_metadata(db, review, request.moduleId, request.tags)
    workspace_service.apply_period(db, review, request)
    for case in cases:
        version = snapshot_case(db, case, str(user.id), "提交评审时保存版本")
        db.add(
            CaseReviewItem(
                review_id=review.id,
                case_id=case.id,
                version_id=version.id,
                status="pending",
                reviewer_ids=request.itemReviewers.get(case.id, request.reviewerIds),
            )
        )
    db.flush()
    review_event(db, review, user.id, "创建评审", {"caseIds": request.caseIds})
    logger.info(
        "用例评审已创建 review_id={} case_count={} policy={}",
        review.id,
        len(cases),
        request.policy,
    )
    return review


def get_review(db, user, project_id, review_id, lock=False):
    project_access(db, user, project_id)
    if lock:
        from services.review_workspace import lock_project

        lock_project(db, project_id)
    query = db.query(CaseReview).filter_by(project_id=project_id, id=review_id)
    review = (query.populate_existing().with_for_update() if lock else query).first()
    if not review:
        raise HTTPException(404, "评审不存在")
    return review


def serialize_review_item(item, version, case, decisions, reviewer_ids):
    return dict(
        id=item.id,
        caseId=item.case_id,
        status=item.status,
        reviewerIds=item.reviewer_ids or reviewer_ids,
        version=version.version,
        snapshot=version.snapshot,
        outdated=(
            case is None
            or case.deleted_at is not None
            or any(
                getattr(case, field) != version.snapshot.get(field)
                for field in SNAPSHOT_FIELDS
            )
        ),
        decisions=[
            dict(
                reviewerId=d.reviewer_id,
                decision=d.decision,
                comment=d.comment,
                updatedAt=d.updated_at.isoformat(),
            )
            for d in decisions
        ],
    )


def review_data(db, review, *, include_items=True):
    from services.review_workspace import metadata
    from services.review_progress import metrics

    items = []
    if include_items:
        rows = (
            db.query(CaseReviewItem, CaseVersion, TestCase)
            .join(CaseVersion, CaseVersion.id == CaseReviewItem.version_id)
            .outerjoin(TestCase, TestCase.id == CaseReviewItem.case_id)
            .filter(CaseReviewItem.review_id == review.id)
            .order_by(CaseReviewItem.created_at, CaseReviewItem.id)
            .all()
        )
        votes = {}
        for decision in (
            db.query(CaseReviewDecision)
            .join(CaseReviewItem, CaseReviewItem.id == CaseReviewDecision.item_id)
            .filter(CaseReviewItem.review_id == review.id)
            .all()
        ):
            votes.setdefault(decision.item_id, []).append(decision)
        items = [
            serialize_review_item(
                item, version, current, votes.get(item.id, []), review.reviewer_ids
            )
            for item, version, current in rows
        ]
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
    events = [
        dict(
            id=e.id,
            itemId=e.item_id,
            actorId=e.actor_id,
            action=e.action,
            detail=e.detail,
            createdAt=e.created_at.isoformat(),
        )
        for e in db.query(CaseReviewEvent)
        .filter_by(review_id=review.id)
        .order_by(CaseReviewEvent.created_at, CaseReviewEvent.id)
        .all()
    ]
    abandoned = {
        identifier
        for event in events
        if event["action"] == "重新提审"
        for identifier in (event["detail"] or {}).get("invalidatedEventIds", [])
    }
    for event in events:
        event["abandoned"] = event["id"] in abandoned
    info = metadata(db, review)
    started = any(e["action"] == "评审结论" for e in events)
    if include_items:
        progress = metrics(
            items, archived=info["archived"], status=review.status, started=started
        )
        associated = [item["caseId"] for item in items]
    else:
        from services.review_case_workspace import summary_metrics

        progress = summary_metrics(db, review, info["archived"], started)
        associated = [
            row[0]
            for row in db.query(CaseReviewItem.case_id)
            .filter_by(review_id=review.id)
            .all()
        ]
    return dict(
        **info,
        **progress,
        associatedCaseIds=associated,
        id=review.id,
        name=review.name,
        policy=review.policy,
        mode=review.mode,
        description=review.description,
        parentReviewId=review.parent_review_id,
        startDate=review.start_date.isoformat() if review.start_date else None,
        endDate=review.end_date.isoformat() if review.end_date else None,
        reviewerIds=review.reviewer_ids,
        status=review.status,
        createdBy=review.created_by,
        createdAt=review.created_at.isoformat(),
        items=items,
        comments=comments,
        history=events,
    )


def review_event(db, review, actor_id, action, detail, item_id=None):
    db.add(
        CaseReviewEvent(
            review_id=review.id,
            item_id=item_id,
            actor_id=str(actor_id),
            action=action,
            detail=detail,
            created_at=beijing_now(),
        )
    )


def refresh_review_status(db, review):
    states = [
        i.status
        for i in db.query(CaseReviewItem)
        .filter_by(review_id=review.id)
        .populate_existing()
        .with_for_update()
        .all()
    ]
    review.status = (
        "rejected"
        if "rejected" in states
        else (
            "approved" if states and all(s == "approved" for s in states) else "pending"
        )
    )


def apply_review_vote(db, review, item, user, request, votes):
    """共享单条与批量投票规则；调用方已锁定评审并验证全部权限。"""
    review_event(db, review, user.id, "评审结论", request.model_dump(), item.id)
    if request.decision == "suggestion":
        return
    decision = next((d for d in votes if d.reviewer_id == str(user.id)), None)
    if decision is None:
        decision = CaseReviewDecision(
            id=str(uuid4()), item_id=item.id, reviewer_id=str(user.id)
        )
        db.add(decision)
        votes.append(decision)
    decision.decision, decision.comment, decision.updated_at = (
        request.decision,
        request.comment,
        beijing_now(),
    )
    assigned = item.reviewer_ids or review.reviewer_ids
    effective = sorted(
        (d for d in votes if d.reviewer_id in assigned),
        key=lambda d: (d.updated_at.replace(tzinfo=None), d.id),
        reverse=True,
    )
    if review.mode == "single":
        item.status = effective[0].decision
    elif any(d.decision == "rejected" for d in effective):
        item.status = "rejected"
    else:
        item.status = "approved" if len(effective) == len(assigned) else "pending"


def vote_reviews(db, user, project_id, review_id, item_ids, request):
    review = get_review(db, user, project_id, review_id, lock=True)
    from services.review_workspace import require_mutable

    require_mutable(db, review)
    if review.status in {"cancelled", "superseded"}:
        raise HTTPException(409, "该评审已取消或已重新提审")
    items = (
        db.query(CaseReviewItem)
        .filter(CaseReviewItem.review_id == review.id, CaseReviewItem.id.in_(item_ids))
        .order_by(CaseReviewItem.id)
        .populate_existing()
        .with_for_update()
        .all()
    )
    if len(items) != len(set(item_ids)):
        raise HTTPException(404, "评审用例不存在")
    if any(
        str(user.id) not in (item.reviewer_ids or review.reviewer_ids) for item in items
    ):
        raise HTTPException(403, "只有该用例的指定评审人可以提交结论")
    mapping = {}
    for vote in (
        db.query(CaseReviewDecision)
        .filter(CaseReviewDecision.item_id.in_(item_ids))
        .populate_existing()
        .with_for_update()
        .all()
    ):
        mapping.setdefault(vote.item_id, []).append(vote)
    for item in items:
        apply_review_vote(
            db, review, item, user, request, mapping.setdefault(item.id, [])
        )
    db.flush()
    if request.decision != "suggestion":
        refresh_review_status(db, review)
    review.updated_at = beijing_now()
    db.flush()
    logger.info(
        "评审结论已记录 review_id={} actor_id={} decision={} item_count={}",
        review.id,
        user.id,
        request.decision,
        len(items),
    )
    return review


def vote_review(db, user, project_id, review_id, item_id, request):
    return vote_reviews(db, user, project_id, review_id, [item_id], request)


def revise_review(db, user, project_id, review_id, request):
    project_access(db, user, project_id, "update")
    review = get_review(db, user, project_id, review_id, lock=True)
    from services.review_workspace import require_mutable, metadata, set_metadata

    require_mutable(db, review)
    old_metadata = metadata(db, review)
    set_metadata(
        db,
        review,
        (
            request.moduleId
            if "moduleId" in request.model_fields_set
            else old_metadata["moduleId"]
        ),
        request.tags if "tags" in request.model_fields_set else old_metadata["tags"],
    )
    if review.status in {"cancelled", "superseded"}:
        raise HTTPException(409, "该评审已关闭，请复制或重新提审")
    item_ids = [
        i.id
        for i in db.query(CaseReviewItem)
        .filter_by(review_id=review.id)
        .populate_existing()
        .with_for_update()
        .all()
    ]
    if (
        db.query(CaseReviewDecision)
        .filter(CaseReviewDecision.item_id.in_(item_ids))
        .first()
    ):
        raise HTTPException(409, "已有有效结论，请重新提审以保留历史")
    eligible = {r["id"] for r in reviewers(db, project_id)}
    requested = set(request.reviewerIds) | {
        v for values in request.itemReviewers.values() for v in values
    }
    if not requested <= eligible:
        raise HTTPException(422, "评审人必须属于当前项目")
    cases = [
        case_for_project(db, project_id, cid, lock=True) for cid in request.caseIds
    ]
    db.query(CaseReviewComment).filter(CaseReviewComment.item_id.in_(item_ids)).update(
        {"item_id": None}, synchronize_session=False
    )
    db.query(CaseReviewItem).filter_by(review_id=review.id).delete(
        synchronize_session=False
    )
    review.name, review.description, review.reviewer_ids = (
        request.name,
        request.description,
        request.reviewerIds,
    )
    review.mode = request.mode or ("single" if request.policy == "any" else "multiple")
    review.policy = "any" if review.mode == "single" else "all"
    from services.review_workspace import apply_period

    apply_period(db, review, request)
    for case in cases:
        version = snapshot_case(db, case, str(user.id), "编辑评审时保存版本")
        db.add(
            CaseReviewItem(
                review_id=review.id,
                case_id=case.id,
                version_id=version.id,
                status="pending",
                reviewer_ids=request.itemReviewers.get(case.id, request.reviewerIds),
            )
        )
    review_event(db, review, user.id, "编辑评审", {"caseIds": request.caseIds})
    db.flush()
    return review


def clone_review(db, user, project_id, review_id, body, resubmit=False):
    from schemas.case_governance import ReviewCreate

    source = get_review(db, user, project_id, review_id, lock=True)
    from services.review_workspace import require_mutable, metadata

    if resubmit:
        require_mutable(db, source)
    project_access(db, user, project_id, "update")
    items = db.query(CaseReviewItem).filter_by(review_id=review_id).all()
    data = dict(
        **{
            key: value
            for key, value in metadata(db, source).items()
            if key in {"moduleId", "tags", "startTime", "endTime"}
        },
        name=source.name[: (255 - len("（重新提审）" if resubmit else "（副本）"))]
        + ("（重新提审）" if resubmit else "（副本）"),
        caseIds=[i.case_id for i in items],
        reviewerIds=source.reviewer_ids,
        mode=source.mode,
        description=source.description,
        itemReviewers={i.case_id: i.reviewer_ids or source.reviewer_ids for i in items},
        startDate=source.start_date,
        endDate=source.end_date,
    )
    overrides = body.model_dump(exclude_unset=True)
    if any(
        overrides.get(key, "非空") is None
        for key in (
            "caseIds",
            "name",
            "reviewerIds",
            "mode",
            "description",
            "itemReviewers",
            "tags",
        )
    ):
        raise HTTPException(422, "复制或重新提审的基本信息和用例字段不能为null")
    data.update(overrides)
    if {"startDate", "endDate"} & overrides.keys():
        # 旧日期请求只有明确改变周期时才覆盖源记录的精确时间。
        if data["startDate"] != source.start_date or data["endDate"] != source.end_date:
            data.pop("startTime", None)
            data.pop("endTime", None)
    data["itemReviewers"] = {
        key: value
        for key, value in data["itemReviewers"].items()
        if key in data["caseIds"]
    }
    from pydantic import ValidationError

    try:
        request = ReviewCreate(**data)
    except ValidationError as error:
        logger.exception("复制或重新提审参数校验失败 review_id={}", source.id)
        raise HTTPException(422, "复制或重新提审参数无效：" + str(error)) from error
    row = create_review(db, user, project_id, request)
    row.parent_review_id = source.id
    if resubmit:
        source.status = "superseded"
        review_event(db, source, user.id, "重新提审", {"newReviewId": row.id})
    review_event(
        db,
        row,
        user.id,
        "复制评审" if not resubmit else "重新提审",
        {"sourceReviewId": source.id},
    )
    db.flush()
    return row


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
        .filter(
            CaseReviewItem.case_id.in_(mapping),
            CaseReview.status.notin_(["cancelled", "superseded"]),
        )
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
            "re_review": "resubmit",
        }[item.status]
        matched.add(item.case_id)
    return statuses
