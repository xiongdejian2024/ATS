"""评审关联用例的数据库分页与模块范围，不修改评审票或版本。"""

import json
from sqlalchemy import case, cast, String, func, or_, and_, literal
from fastapi import HTTPException
from models import TestCase, Module, User
from models.case_governance import (
    CaseReview,
    CaseReviewItem,
    CaseVersion,
    CaseReviewDecision,
)
from services import case_governance as governance
from services.case_candidates import descendants
from services.review_workspace import metadata
from services.review_progress import count_metrics


def approved_vote(db, review):
    return (
        db.query(CaseReviewDecision.id)
        .filter(
            CaseReviewDecision.item_id == CaseReviewItem.id,
            CaseReviewDecision.decision == "approved",
            func.instr(
                assigned_expression(review),
                literal('"') + CaseReviewDecision.reviewer_id + literal('"'),
            )
            > 0,
        )
        .exists()
        .correlate(CaseReviewItem, CaseReview)
    )


def state_expression(db, review):
    return case(
        (CaseReviewItem.status != "pending", CaseReviewItem.status),
        (approved_vote(db, review), "under_review"),
        else_="un_review",
    )


def summary_metrics(db, review, archived, started):
    counts = dict(
        db.query(CaseReviewItem.status, func.count())
        .filter_by(review_id=review.id)
        .group_by(CaseReviewItem.status)
        .all()
    )
    partial = (
        db.query(CaseReviewItem.id)
        .filter(
            CaseReviewItem.review_id == review.id,
            CaseReviewItem.status == "pending",
            approved_vote(db, review),
        )
        .count()
    )
    return count_metrics(
        sum(counts.values()),
        counts.get("approved", 0),
        counts.get("rejected", 0),
        counts.get("re_review", 0),
        partial,
        archived=archived,
        status=review.status,
        started=started,
    )


def assigned_expression(review):
    value = cast(CaseReviewItem.reviewer_ids, String)
    fallback = (
        cast(review.reviewer_ids, String)
        if review is CaseReview
        else json.dumps(review.reviewer_ids)
    )
    return func.coalesce(
        case((value.in_(["[]", "null"]), fallback), else_=value), fallback
    )


def filtered_query(
    db,
    review,
    *,
    search="",
    priority=None,
    state=None,
    states=None,
    reviewer_id=None,
    creator_id=None,
    only_mine=False,
    user=None,
):
    query = (
        db.query(CaseReviewItem)
        .join(TestCase, TestCase.id == CaseReviewItem.case_id)
        .join(CaseVersion, CaseVersion.id == CaseReviewItem.version_id)
        .filter(
            CaseReviewItem.review_id == review.id,
            TestCase.project_id == review.project_id,
            CaseVersion.project_id == review.project_id,
            TestCase.deleted_at.is_(None),
            TestCase.type.notin_(["api", "scenario"]),
        )
    )
    keyword = search.strip().casefold()
    if keyword:
        query = query.filter(
            or_(
                func.lower(TestCase.name).contains(keyword, autoescape=True),
                func.lower(TestCase.case_code).contains(keyword, autoescape=True),
                func.lower(cast(TestCase.tags, String)).contains(
                    keyword, autoescape=True
                ),
                func.lower(cast(TestCase.tags, String)).contains(
                    json.dumps(keyword, ensure_ascii=True)[1:-1], autoescape=True
                ),
            )
        )
    if priority:
        query = query.filter(TestCase.priority == priority)
    if state:
        query = query.filter(state_expression(db, review) == state)
    if states:
        query = query.filter(state_expression(db, review).in_(states))
    if reviewer_id:
        query = query.filter(
            assigned_expression(review).contains(
                '"' + reviewer_id + '"', autoescape=True
            )
        )
    if only_mine:
        query = query.filter(
            assigned_expression(review).contains(
                '"' + str(user.id) + '"', autoescape=True
            )
        )
    if creator_id:
        query = query.filter(TestCase.created_by == creator_id)
    return query


def query_scope(db, review, folder="all", include_descendants=True, **filters):
    query = filtered_query(db, review, **filters)
    modules = (
        db.query(Module)
        .filter_by(project_id=review.project_id)
        .order_by(Module.sort_order, Module.created_at, Module.id)
        .all()
    )
    ids = {m.id for m in modules}
    direct = dict(
        query.with_entities(TestCase.module_id, func.count(CaseReviewItem.id))
        .group_by(TestCase.module_id)
        .all()
    )
    folders = [
        dict(
            id=m.id,
            name=m.name,
            parentId=m.parent_id,
            count=sum(direct.get(i, 0) for i in descendants(modules, m.id)),
        )
        for m in modules
    ]
    counts = dict(
        all=sum(direct.values()),
        unassigned=sum(count for key, count in direct.items() if key not in ids),
    )
    if folder == "unassigned":
        query = query.filter(
            or_(TestCase.module_id.is_(None), TestCase.module_id.notin_(ids))
        )
    elif folder != "all":
        if folder not in ids:
            raise HTTPException(404, "用例模块不存在于当前项目")
        query = query.filter(
            TestCase.module_id.in_(
                descendants(modules, folder) if include_descendants else {folder}
            )
        )
    return query, modules, folders, counts


def item_data(
    db,
    user,
    review,
    item,
    version,
    current,
    decisions,
    module_names,
    people,
    archived,
    re_review_permissions=(False, False),
    personal_state="un_review",
):
    data = governance.serialize_review_item(
        item, version, current, decisions, review.reviewer_ids
    )
    reviewing = item.status == "pending" and any(
        d.decision == "approved" and d.reviewer_id in data["reviewerIds"]
        for d in decisions
    )
    state = (
        ("under_review" if reviewing else "un_review")
        if item.status == "pending"
        else item.status
    )
    data.update(
        reviewState=state,
        myStatus=personal_state,
        name=current.name if current else version.snapshot.get("name", "已删除用例"),
        caseCode=(
            current.case_code if current else version.snapshot.get("case_code", "")
        ),
        priority=(
            current.priority if current else version.snapshot.get("priority", "P2")
        ),
        moduleId=current.module_id if current else None,
        moduleName=module_names.get(
            current.module_id if current else None, "未分配模块"
        ),
        createdBy=current.created_by if current else None,
        creator=people.get(current.created_by if current else None, ""),
        recycled=current is None or current.deleted_at is not None,
        canVote=current is not None
        and current.deleted_at is None
        and not archived
        and review.status not in {"cancelled", "superseded"}
        and str(user.id) in data["reviewerIds"],
        canReReview=not archived
        and review.status not in {"cancelled", "superseded"}
        and current is not None
        and current.deleted_at is None
        and re_review_permissions[0]
        and (re_review_permissions[1] or str(user.id) in data["reviewerIds"]),
    )
    return data


def listing(
    db,
    user,
    project_id,
    review_id,
    *,
    page=1,
    size=20,
    sort="createdAt",
    order="desc",
    view="list",
    folder="all",
    include_descendants=True,
    **filters,
):
    review = governance.get_review(db, user, project_id, review_id)
    query, modules, folders, counts = query_scope(
        db, review, folder, include_descendants, user=user, **filters
    )
    total = query.count()
    column = {
        "caseCode": TestCase.case_code,
        "name": TestCase.name,
        "createdAt": CaseReviewItem.created_at,
    }.get(sort)
    if column is None:
        raise HTTPException(422, "不支持的评审用例排序字段")
    query = query.order_by(
        column.desc() if order == "desc" else column.asc(), CaseReviewItem.id
    )
    if view == "list":
        query = query.offset((page - 1) * size).limit(size)
    else:
        query = query.limit(10000)
    rows = query.with_entities(CaseReviewItem, CaseVersion, TestCase).all()
    decisions = {}
    for vote in (
        db.query(CaseReviewDecision)
        .filter(CaseReviewDecision.item_id.in_([i.id for i, _, _ in rows]))
        .all()
    ):
        decisions.setdefault(vote.item_id, []).append(vote)
    people = {
        u.id: u.full_name or u.username
        for u in db.query(User)
        .filter(User.id.in_({c.created_by for _, _, c in rows}))
        .all()
    }
    module_names = {m.id: m.name for m in modules}
    archived = metadata(db, review)["archived"]
    from services.review_item_management import re_review_permissions

    permissions = re_review_permissions(db, user, project_id)
    from services.review_reading import personal_states

    personal = personal_states(db, user, review.id, [i.id for i, _, _ in rows])
    items = [
        item_data(
            db,
            user,
            review,
            item,
            version,
            current,
            decisions.get(item.id, []),
            module_names,
            people,
            archived,
            permissions,
            personal.get(item.id, "un_review"),
        )
        for item, version, current in rows
    ]
    return dict(
        items=items, total=total, page=page, size=size, modules=folders, counts=counts
    )


def get_item(db, user, project_id, review_id, item_id):
    from services.review_item_management import re_review_permissions

    review = governance.get_review(db, user, project_id, review_id)
    item = db.query(CaseReviewItem).filter_by(review_id=review.id, id=item_id).first()
    if not item:
        raise HTTPException(404, "评审用例不存在")
    version, current = db.get(CaseVersion, item.version_id), db.get(
        TestCase, item.case_id
    )
    if version.project_id != project_id or (
        current and current.project_id != project_id
    ):
        raise HTTPException(404, "评审用例不属于当前项目")
    votes = db.query(CaseReviewDecision).filter_by(item_id=item.id).all()
    modules = {
        m.id: m.name for m in db.query(Module).filter_by(project_id=project_id).all()
    }
    author = (
        db.get(User, current.created_by) if current and current.created_by else None
    )
    people = {author.id: author.full_name or author.username} if author else {}
    from services.review_reading import personal_states

    return item_data(
        db,
        user,
        review,
        item,
        version,
        current,
        votes,
        modules,
        people,
        metadata(db, review)["archived"],
        re_review_permissions(db, user, project_id),
        personal_states(db, user, review.id, [item.id]).get(item.id, "un_review"),
    )
