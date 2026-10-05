"""计划和评审共享数据库候选查询；范围计数和分页使用同一筛选条件。"""

from fastapi import HTTPException
from models import TestCase, Module


def descendants(rows, root):
    found, pending = {root}, [root]
    while pending:
        parent = pending.pop()
        for row in rows:
            if row.parent_id == parent and row.id not in found:
                found.add(row.id)
                pending.append(row.id)
    return found


def candidate_query(db, project_id, category, search, folder, priority):
    from sqlalchemy import func, or_

    query = db.query(TestCase).filter(
        TestCase.project_id == project_id, TestCase.deleted_at.is_(None)
    )
    query = (
        query.filter(TestCase.type.notin_(["api", "scenario"]))
        if category == "functional"
        else query.filter(TestCase.type == category)
    )
    if category != "functional":
        query = query.filter(TestCase.is_automated.is_(True))
    keyword = search.strip().casefold()
    if keyword:
        query = query.filter(
            or_(
                func.lower(TestCase.name).contains(keyword, autoescape=True),
                func.lower(TestCase.case_code).contains(keyword, autoescape=True),
            )
        )
    if priority:
        query = query.filter(TestCase.priority == priority)
    modules = (
        db.query(Module)
        .filter_by(project_id=project_id)
        .order_by(Module.sort_order, Module.created_at)
        .all()
    )
    module_counts = dict(
        query.with_entities(TestCase.module_id, func.count(TestCase.id))
        .group_by(TestCase.module_id)
        .all()
    )
    folders = [
        dict(
            id=row.id,
            name=row.name,
            parentId=row.parent_id,
            count=sum(module_counts.get(key, 0) for key in descendants(modules, row.id)),
        )
        for row in modules
    ]
    counts = dict(
        all=sum(module_counts.values()),
        unassigned=sum(
            count for key, count in module_counts.items() if key not in {row.id for row in modules}
        ),
    )
    if folder == "unassigned":
        query = query.filter(
            or_(
                TestCase.module_id.is_(None), TestCase.module_id.notin_([row.id for row in modules])
            )
        )
    elif folder != "all":
        if folder not in {row.id for row in modules}:
            raise HTTPException(404, "关联选择目录不属于当前项目")
        query = query.filter(TestCase.module_id.in_(descendants(modules, folder)))
    return query, modules, folders, counts


def candidates(db, project_id, category, search, folder, priority, page, size):
    from utils.serializer import serialize_model

    query, modules, folders, counts = candidate_query(
        db, project_id, category, search, folder, priority
    )
    total = query.count()
    records = (
        query.order_by(TestCase.created_at.desc(), TestCase.id)
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    module_names = {row.id: row.name for row in modules}
    items = [
        dict(
            serialize_model(row, camel_case=True),
            moduleName=module_names.get(row.module_id, "未分配模块"),
        )
        for row in records
    ]
    return dict(items=items, total=total, page=page, size=size, modules=folders, counts=counts)
