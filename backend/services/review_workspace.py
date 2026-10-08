"""评审首页：独立目录、分页摘要和受权限保护的原子操作。"""

from sqlalchemy import case, cast, Numeric, String, func, or_, and_
from fastapi import HTTPException
from models import Project, User
from models.case_governance import (
    CaseReview,
    CaseReviewItem,
    CaseReviewDecision,
    CaseReviewEvent,
    CaseReviewComment,
    CaseReviewFollow,
)
from models.review_workspace import ReviewModule, ReviewWorkspace
from core.project_access import project_allows
from core.logger import logger
from services import case_governance as governance
import json
from datetime import datetime, time
from utils.datetime_utils import BEIJING_TZ, beijing_now


def lock_project(db, project_id):
    return (
        db.query(Project)
        .filter_by(id=project_id)
        .populate_existing()
        .with_for_update()
        .one()
    )


def module_rows(db, project_id, lock=False):
    query = (
        db.query(ReviewModule)
        .filter_by(project_id=project_id)
        .order_by(ReviewModule.position, ReviewModule.created_at, ReviewModule.id)
    )
    return query.populate_existing().with_for_update().all() if lock else query.all()


def descendants(rows, identifier):
    result = {identifier}
    while True:
        expanded = result | {row.id for row in rows if row.parent_id in result}
        if expanded == result:
            return result
        result = expanded


def module_for_project(db, project_id, identifier, lock=False):
    if identifier is None:
        return None
    query = db.query(ReviewModule).filter_by(project_id=project_id, id=identifier)
    row = query.populate_existing().with_for_update().first() if lock else query.first()
    if not row:
        raise HTTPException(404, "评审模块不存在")
    return row


def module_data(row):
    return dict(id=row.id, name=row.name, parentId=row.parent_id, position=row.position)


def save_module(db, user, project_id, body, identifier=None):
    governance.project_access(db, user, project_id, "update")
    lock_project(db, project_id)
    row = (
        module_for_project(db, project_id, identifier, lock=True)
        if identifier
        else ReviewModule(project_id=project_id)
    )
    module_for_project(db, project_id, body.parentId, lock=True)
    if identifier and body.parentId in descendants(
        module_rows(db, project_id, lock=True), identifier
    ):
        raise HTTPException(422, "模块不能移动到自身或子模块")
    duplicate = db.query(ReviewModule).filter_by(
        project_id=project_id, parent_id=body.parentId, name=body.name
    )
    if identifier:
        duplicate = duplicate.filter(ReviewModule.id != identifier)
    if duplicate.populate_existing().with_for_update().first():
        raise HTTPException(409, "同级评审模块名称重复")
    row.name, row.parent_id, row.position = body.name, body.parentId, body.position
    siblings = [
        m
        for m in module_rows(db, project_id, lock=True)
        if m.parent_id == body.parentId and m.id != row.id
    ]
    siblings.insert(min(body.position, len(siblings)), row)
    for position, sibling in enumerate(siblings):
        sibling.position = position
    db.add(row)
    db.flush()
    logger.info(
        "评审模块已保存 project_id={} module_id={} actor_id={}",
        project_id,
        row.id,
        user.id,
    )
    return module_data(row)


def workspace(db, review, lock=False):
    query = db.query(ReviewWorkspace).filter_by(review_id=review.id)
    # 当前读：归档和投票使用相同锁顺序，不能被 MySQL RR 的旧快照绕过。
    return (
        query.populate_existing().with_for_update().first() if lock else query.first()
    )


def metadata(db, review):
    row = workspace(db, review)
    return dict(
        number=row.number if row else None,
        moduleId=row.module_id if row else None,
        tags=list(row.tags or []) if row else [],
        archived=bool(row and row.archived),
        startTime=period_value(row.start_time if row else None, review.start_date),
        endTime=period_value(row.end_time if row else None, review.end_date),
    )


def period_value(value, legacy_date):
    value = value or (datetime.combine(legacy_date, time.min) if legacy_date else None)
    return value.replace(tzinfo=BEIJING_TZ).isoformat() if value else None


def apply_period(db, review, request):
    row = workspace(db, review, lock=True)
    if row is None:
        old = metadata(db, review)
        row = set_metadata(db, review, old["moduleId"], old["tags"])
    if {"startTime", "endTime"} & request.model_fields_set:
        row.start_time = (
            request.startTime.replace(tzinfo=None) if request.startTime else None
        )
        row.end_time = request.endTime.replace(tzinfo=None) if request.endTime else None
        review.start_date = request.startTime.date() if request.startTime else None
        review.end_date = request.endTime.date() if request.endTime else None
    elif {"startDate", "endDate"} & request.model_fields_set:
        # 日期版客户端往返相同日期时保留精确时间；只有明确改日期才退回日期精度。
        same_dates = (
            row.start_time
            and row.end_time
            and row.start_time.date() == request.startDate
            and row.end_time.date() == request.endDate
        )
        if not same_dates:
            row.start_time = row.end_time = None
        review.start_date, review.end_date = request.startDate, request.endDate
    db.flush()


def update_header(db, user, project_id, identifier, request):
    governance.project_access(db, user, project_id, "update")
    review = governance.get_review(db, user, project_id, identifier, lock=True)
    require_mutable(db, review)
    if review.status in {"cancelled", "superseded"}:
        raise HTTPException(409, "评审已关闭，不能编辑基本信息")
    if request.mode and request.mode != review.mode:
        raise HTTPException(422, "已创建评审的模式不能修改")
    eligible = {r["id"] for r in governance.reviewers(db, project_id)}
    if not set(request.reviewerIds) <= eligible:
        raise HTTPException(422, "默认评审人必须属于当前项目")
    # 旧数据未保存逐条分配时先冻结既有人员，改默认人员只作用于之后关联的用例。
    items = (
        db.query(CaseReviewItem)
        .filter_by(review_id=identifier)
        .populate_existing()
        .with_for_update()
        .all()
    )
    for item in items:
        if not item.reviewer_ids:
            item.reviewer_ids = list(review.reviewer_ids)
    before = dict(
        name=review.name,
        reviewerIds=review.reviewer_ids,
        description=review.description,
        **metadata(db, review),
    )
    review.name, review.description, review.reviewer_ids = (
        request.name,
        request.description,
        request.reviewerIds,
    )
    set_metadata(db, review, request.moduleId, request.tags)
    apply_period(db, review, request)
    review.updated_at = beijing_now()
    governance.review_event(
        db,
        review,
        user.id,
        "编辑基本信息",
        {"before": before, "after": request.model_dump(mode="json")},
    )
    db.flush()
    logger.info(
        "评审基本信息已更新，历史结论保留 project_id={} review_id={} actor_id={}",
        project_id,
        identifier,
        user.id,
    )
    return governance.review_data(db, review)


def associate_cases(db, user, project_id, identifier, request):
    """追加关联只创建新条目，不重建已有分配、快照或评审结论。"""
    governance.project_access(db, user, project_id, "update")
    review = governance.get_review(db, user, project_id, identifier, lock=True)
    require_mutable(db, review)
    if review.status in {"cancelled", "superseded"}:
        raise HTTPException(409, "评审已关闭，不能关联用例")
    items = (
        db.query(CaseReviewItem)
        .filter_by(review_id=identifier)
        .populate_existing()
        .with_for_update()
        .all()
    )
    if {item.case_id for item in items} & set(request.caseIds):
        raise HTTPException(409, "包含已关联用例，请刷新后重新选择")
    if len(items) + len(request.caseIds) > 10000:
        raise HTTPException(422, "一个评审最多关联10000个用例")
    eligible = {row["id"] for row in governance.reviewers(db, project_id)}
    if not set(request.reviewerIds) <= eligible:
        raise HTTPException(422, "评审人必须属于当前项目且有效")
    cases = [
        governance.case_for_project(db, project_id, cid, lock=True)
        for cid in sorted(request.caseIds)
    ]
    if any(case.type in {"api", "scenario"} for case in cases):
        raise HTTPException(422, "评审仅支持功能用例")
    for case in cases:
        version = governance.snapshot_case(db, case, str(user.id), "关联评审时保存版本")
        db.add(
            CaseReviewItem(
                review_id=identifier,
                case_id=case.id,
                version_id=version.id,
                status="pending",
                reviewer_ids=list(request.reviewerIds),
            )
        )
    db.flush()
    governance.refresh_review_status(db, review)
    review.updated_at = beijing_now()
    governance.review_event(
        db,
        review,
        user.id,
        "关联用例",
        {"caseIds": request.caseIds, "reviewerIds": request.reviewerIds},
    )
    db.flush()
    logger.info(
        "评审追加关联完成，已有结论保留 project_id={} review_id={} count={} actor_id={}",
        project_id,
        identifier,
        len(cases),
        user.id,
    )
    return governance.review_data(db, review)


def require_mutable(db, review):
    row = workspace(db, review, lock=True)
    if row and row.archived:
        raise HTTPException(409, "评审已归档，不能修改评审内容")


def set_metadata(db, review, module_id=None, tags=None):
    module_for_project(db, review.project_id, module_id, lock=True)
    row = workspace(db, review, lock=True)
    if row is None:
        row = ReviewWorkspace(review_id=review.id, tags=[])
        db.add(row)
    row.module_id = module_id
    if tags is not None:
        row.tags = tags
    db.flush()
    return row


def summary_query(db, project_id):
    item_counts = (
        db.query(
            CaseReviewItem.review_id.label("review_id"),
            func.count(CaseReviewItem.id).label("total"),
            func.sum(case((CaseReviewItem.status == "approved", 1), else_=0)).label(
                "passed"
            ),
            func.sum(
                case((CaseReviewItem.status.in_(["approved", "rejected"]), 1), else_=0)
            ).label("finished"),
        )
        .group_by(CaseReviewItem.review_id)
        .subquery()
    )
    total = func.coalesce(item_counts.c.total, 0)
    passed = func.coalesce(item_counts.c.passed, 0)
    from services.review_case_workspace import approved_vote

    started = (
        db.query(CaseReviewItem.id)
        .filter(
            CaseReviewItem.review_id == CaseReview.id,
            or_(CaseReviewItem.status != "pending", approved_vote(db, CaseReview)),
        )
        .exists()
        .correlate(CaseReview)
    )
    lifecycle = case(
        (ReviewWorkspace.archived.is_(True), "archived"),
        (CaseReview.status.in_(["cancelled", "superseded"]), CaseReview.status),
        (and_(total > 0, item_counts.c.finished == total), "completed"),
        (started, "underway"),
        else_="prepared",
    ).label("lifecycle")
    ratio = passed * 1.0 / func.nullif(total, 0)
    if db.get_bind().dialect.name == "postgresql":
        # PostgreSQL round(value, places) accepts NUMERIC, not DOUBLE PRECISION.
        ratio = cast(ratio, Numeric)
    rate = (func.round(ratio, 2) * 100).label(
        "pass_rate"
    )
    query = (
        db.query(
            CaseReview,
            ReviewWorkspace,
            total.label("total"),
            passed.label("passed"),
            lifecycle,
            rate,
        )
        .outerjoin(ReviewWorkspace, ReviewWorkspace.review_id == CaseReview.id)
        .outerjoin(item_counts, item_counts.c.review_id == CaseReview.id)
        .filter(CaseReview.project_id == project_id)
    )
    return query, lifecycle, rate


def list_reviews(
    db,
    user,
    project_id,
    *,
    page=1,
    size=20,
    scope="all",
    module_id=None,
    include_descendants=True,
    search="",
    lifecycle=None,
    mode=None,
    reviewer_id=None,
    creator_id=None,
    sort="createdAt",
    order="desc",
    filters=None,
):
    project = governance.project_access(db, user, project_id)
    modules = module_rows(db, project_id)
    query, state, rate = summary_query(db, project_id)
    from services.review_index_filter import parse, apply
    advanced, _ = parse(filters)
    query = apply(db, query, state, rate, filters, str(user.id))
    if lifecycle:
        query = query.filter(state == lifecycle)
    elif not any(row["field"] == "lifecycle" for row in advanced):
        query = query.filter(
            or_(
                ReviewWorkspace.archived.is_(False), ReviewWorkspace.review_id.is_(None)
            )
        )
    if module_id == "default":
        query = query.filter(ReviewWorkspace.module_id.is_(None))
    elif module_id:
        module_for_project(db, project_id, module_id)
        ids = descendants(modules, module_id) if include_descendants else {module_id}
        query = query.filter(ReviewWorkspace.module_id.in_(ids))
    # 指定人员同时包括默认评审人及逐条分配；不把“我评审的”误实现成只看未完成。
    assigned = reviewer_id or (str(user.id) if scope == "reviewByMe" else None)
    if assigned:
        item_assigned = (
            db.query(CaseReviewItem.id)
            .filter(
                CaseReviewItem.review_id == CaseReview.id,
                cast(CaseReviewItem.reviewer_ids, String).contains(
                    '"' + assigned + '"', autoescape=True
                ),
            )
            .exists()
        )
        query = query.filter(
            or_(
                cast(CaseReview.reviewer_ids, String).contains(
                    '"' + assigned + '"', autoescape=True
                ),
                item_assigned,
            )
        )
    if scope == "createByMe":
        query = query.filter(CaseReview.created_by == str(user.id))
    if creator_id:
        query = query.filter(CaseReview.created_by == creator_id)
    if mode:
        query = query.filter(CaseReview.mode == mode)
    if search:
        query = query.filter(
            or_(
                CaseReview.id.contains(search, autoescape=True),
                cast(ReviewWorkspace.number, String).contains(search, autoescape=True),
                CaseReview.name.contains(search, autoescape=True),
                cast(ReviewWorkspace.tags, String).contains(search, autoescape=True),
                cast(ReviewWorkspace.tags, String).contains(
                    json.dumps(search, ensure_ascii=True)[1:-1], autoescape=True
                ),
            )
        )
    count = query.count()
    sort_column = {
        "number": ReviewWorkspace.number,
        "name": CaseReview.name,
        "createdAt": CaseReview.created_at,
        "passRate": rate,
    }[sort]
    rows = (
        query.order_by(
            sort_column.asc() if order == "asc" else sort_column.desc(),
            CaseReview.id.asc(),
        )
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    review_ids = [row[0].id for row in rows]
    item_reviewers = {}
    for review_id, ids in (
        db.query(CaseReviewItem.review_id, CaseReviewItem.reviewer_ids)
        .filter(CaseReviewItem.review_id.in_(review_ids))
        .all()
    ):
        item_reviewers.setdefault(review_id, set()).update(ids or [])
    user_ids = (
        {row[0].created_by for row in rows}
        | {identifier for row in rows for identifier in row[0].reviewer_ids}
        | {i for ids in item_reviewers.values() for i in ids}
    )
    names = {
        u.id: u.full_name or u.username
        for u in db.query(User).filter(User.id.in_(user_ids)).all()
    }
    module_map = {row.id: row for row in modules}

    def module_path(identifier):
        path, seen = [], set()
        while identifier and identifier in module_map and identifier not in seen:
            seen.add(identifier)
            current = module_map[identifier]
            path.insert(0, current.name)
            identifier = current.parent_id
        return "/".join(path) or "默认模块"

    items = []
    for review, info, total, passed, status, percent in rows:
        ids = list(
            dict.fromkeys(
                review.reviewer_ids + sorted(item_reviewers.get(review.id, set()))
            )
        )
        module = module_map.get(info.module_id) if info else None
        items.append(
            dict(
                id=review.id,
                number=info.number if info else None,
                name=review.name,
                caseCount=total,
                passedCount=passed,
                # NUMERIC aggregates arrive as Decimal on PostgreSQL; keep the
                # public JSON field numeric rather than Pydantic's Decimal string.
                passRate=float(round(percent or 0, 2)),
                lifecycle=status,
                mode=review.mode,
                reviewerIds=ids,
                reviewers=[names.get(i, i) for i in ids],
                createdBy=review.created_by,
                creator=names.get(review.created_by, review.created_by),
                moduleId=info.module_id if info else None,
                moduleName=module.name if module else "默认模块",
                modulePath=module_path(info.module_id if info else None),
                tags=info.tags if info else [],
                description=review.description,
                startDate=review.start_date,
                endDate=review.end_date,
                startTime=period_value(
                    info.start_time if info else None, review.start_date
                ),
                endTime=period_value(info.end_time if info else None, review.end_date),
                createdAt=review.created_at,
                archived=bool(info and info.archived),
            )
        )
    counts = dict(
        db.query(ReviewWorkspace.module_id, func.count(CaseReview.id))
        .select_from(CaseReview)
        .outerjoin(ReviewWorkspace, ReviewWorkspace.review_id == CaseReview.id)
        .filter(
            CaseReview.project_id == project_id,
            or_(
                ReviewWorkspace.archived.is_(False), ReviewWorkspace.review_id.is_(None)
            ),
        )
        .group_by(ReviewWorkspace.module_id)
        .all()
    )
    return dict(
        items=items,
        total=count,
        page=page,
        size=size,
        modules=[dict(**module_data(m), count=counts.get(m.id, 0)) for m in modules],
        defaultCount=counts.get(None, 0),
        allCount=sum(counts.values()),
        permissions={
            action: project_allows(db, user, project, "test_case:" + action)
            for action in ("update", "delete")
        },
    )


def move_reviews(db, user, project_id, body):
    governance.project_access(db, user, project_id, "update")
    lock_project(db, project_id)
    module_for_project(db, project_id, body.moduleId, lock=True)
    reviews = [
        governance.get_review(db, user, project_id, identifier, lock=True)
        for identifier in sorted(body.reviewIds)
    ]
    for review in reviews:
        require_mutable(db, review)
    for review in reviews:
        old = metadata(db, review)
        set_metadata(db, review, body.moduleId, old["tags"])
        governance.review_event(
            db,
            review,
            user.id,
            "移动评审",
            {"fromModuleId": old["moduleId"], "moduleId": body.moduleId},
        )
    db.flush()
    logger.info(
        "评审已批量移动 project_id={} count={} module_id={} actor_id={}",
        project_id,
        len(reviews),
        body.moduleId,
        user.id,
    )
    return dict(moved=len(reviews))


def remove_reviews(db, reviews):
    # 显式删除关联记录，SQLite/MySQL 均保持一致；不删除用例与版本快照。
    ids = [r.id for r in reviews]
    item_ids = (
        db.query(CaseReviewItem.id).filter(CaseReviewItem.review_id.in_(ids)).subquery()
    )
    db.query(CaseReviewDecision).filter(
        CaseReviewDecision.item_id.in_(db.query(item_ids.c.id))
    ).delete(synchronize_session=False)
    for model in (
        CaseReviewComment,
        CaseReviewFollow,
        CaseReviewEvent,
        CaseReviewItem,
        ReviewWorkspace,
    ):
        db.query(model).filter(model.review_id.in_(ids)).delete(
            synchronize_session=False
        )
    db.query(CaseReview).filter(CaseReview.id.in_(ids)).delete(
        synchronize_session=False
    )
    db.flush()


def delete_review(db, user, project_id, identifier, body):
    governance.project_access(db, user, project_id, "delete")
    review = governance.get_review(db, user, project_id, identifier, lock=True)
    if body.name != review.name:
        raise HTTPException(409, "评审名称不匹配，请刷新后确认")
    remove_reviews(db, [review])
    logger.info(
        "评审已删除 project_id={} review_id={} actor_id={}",
        project_id,
        identifier,
        user.id,
    )
    return dict(deleted=1)


def delete_module(db, user, project_id, identifier, body):
    governance.project_access(db, user, project_id, "delete")
    lock_project(db, project_id)
    row = module_for_project(db, project_id, identifier, lock=True)
    if body.name != row.name:
        raise HTTPException(409, "模块名称不匹配，请刷新后确认")
    rows = module_rows(db, project_id, lock=True)
    ids = descendants(rows, identifier)
    reviews = (
        db.query(CaseReview)
        .join(ReviewWorkspace, ReviewWorkspace.review_id == CaseReview.id)
        .filter(CaseReview.project_id == project_id, ReviewWorkspace.module_id.in_(ids))
        .populate_existing()
        .with_for_update()
        .all()
    )
    remove_reviews(db, reviews)
    # 从叶子向上删除，避免依赖自关联级联行为。
    remaining = {r.id: r for r in rows if r.id in ids}
    while remaining:
        parents = {r.parent_id for r in remaining.values()}
        leaves = [i for i in remaining if i not in parents]
        if not leaves:
            raise HTTPException(409, "评审模块存在循环，请修复目录后重试")
        for i in leaves:
            db.delete(remaining.pop(i))
        db.flush()
    logger.info(
        "评审模块及资源已删除 project_id={} module_id={} modules={} reviews={} actor_id={}",
        project_id,
        identifier,
        len(ids),
        len(reviews),
        user.id,
    )
    return dict(deletedModules=len(ids), deletedReviews=len(reviews))


def archive_review(db, user, project_id, identifier):
    governance.project_access(db, user, project_id, "delete")
    review = governance.get_review(db, user, project_id, identifier, lock=True)
    require_mutable(db, review)
    items = (
        db.query(CaseReviewItem)
        .filter_by(review_id=identifier)
        .populate_existing()
        .with_for_update()
        .all()
    )
    if (
        review.status in {"cancelled", "superseded"}
        or not items
        or any(i.status not in {"approved", "rejected"} for i in items)
    ):
        raise HTTPException(409, "只有全部用例评审完成后才能归档")
    old = metadata(db, review)
    info = set_metadata(db, review, old["moduleId"], old["tags"])
    info.archived = True
    governance.review_event(db, review, user.id, "归档评审", {})
    db.flush()
    logger.info(
        "评审已归档 project_id={} review_id={} actor_id={}",
        project_id,
        identifier,
        user.id,
    )
    return dict(archived=True)
