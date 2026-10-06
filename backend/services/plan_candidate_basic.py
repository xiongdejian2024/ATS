"""关联窗口基础筛选共用SQL范围，列表、模块计数和锁内保存保持一致。"""

from functools import partial
from fastapi import HTTPException
from sqlalchemy import select
from models import TestCase, User, Project, ProjectMember
from models.native_case import ApiDefinition, NativeCaseConfig


def definition_filters(query, condition):
    if condition.protocols is not None:
        query = query.filter(ApiDefinition.protocol.in_(condition.protocols))
    if condition.methods:
        query = query.filter(
            ApiDefinition.parameters["request"]["method"].as_string().in_(condition.methods)
        )
    if condition.createdBy:
        query = query.filter(ApiDefinition.created_by.in_(condition.createdBy))
    return query


def case_query(
    db, project_id, category, search, folder, priority, *, condition, current_read=False
):
    from services.case_candidates import candidate_query
    from services.case_candidates import descendants
    from sqlalchemy import func

    if condition.protocols is None and not condition.createdBy:
        return candidate_query(
            db, project_id, category, search, folder, priority, current_read=current_read
        )
    # 在基础SQL内过滤后再计算模块计数，不能仅过滤当前页面。
    query, modules, _, _ = candidate_query(
        db, project_id, category, search, "all", priority, current_read=current_read
    )
    if condition.protocols is not None:
        definitions = select(ApiDefinition.id).where(
            ApiDefinition.project_id == project_id,
            ApiDefinition.protocol.in_(condition.protocols),
        )
        query = query.filter(
            TestCase.id.in_(
                select(NativeCaseConfig.case_id).where(
                    NativeCaseConfig.api_definition_id.in_(definitions)
                )
            )
        )
    if condition.createdBy:
        query = query.filter(TestCase.created_by.in_(condition.createdBy))
    counts = dict(
        query.with_entities(TestCase.module_id, func.count(TestCase.id))
        .group_by(TestCase.module_id)
        .all()
    )
    known = {m.id for m in modules}
    folders = [
        dict(
            id=m.id,
            name=m.name,
            parentId=m.parent_id,
            count=sum(counts.get(key, 0) for key in descendants(modules, m.id)),
        )
        for m in modules
    ]
    totals = dict(
        all=sum(counts.values()), unassigned=sum(n for key, n in counts.items() if key not in known)
    )
    if folder == "unassigned":
        from sqlalchemy import or_

        query = query.filter(or_(TestCase.module_id.is_(None), TestCase.module_id.notin_(known)))
    elif folder != "all":
        if folder not in known:
            raise HTTPException(404, "关联选择目录不属于当前项目")
        query = query.filter(TestCase.module_id.in_(descendants(modules, folder)))
    return query, modules, folders, totals


def query_factory(condition, resource_type):
    if resource_type == "API":
        from services.plan_definition_candidates import query

        def definitions(*args, **kwargs):
            records, modules, folders, counts = query(*args, **kwargs)
            return definition_filters(records, condition), modules, folders, counts

        return definitions
    return partial(case_query, condition=condition)


def options(db, project_id):
    # 只返回真实定义协议与当前项目人员；不虚构未配置的执行协议。
    protocols = [
        row[0]
        for row in db.query(ApiDefinition.protocol)
        .filter_by(project_id=project_id)
        .distinct()
        .order_by(ApiDefinition.protocol)
    ]
    project = db.get(Project, project_id)
    members = db.query(ProjectMember.user_id).filter_by(project_id=project_id)
    creators = [
        dict(value=row.id, text=row.full_name or row.username)
        for row in db.query(User)
        .filter(User.status.is_(True), (User.id.in_(members) | (User.id == project.owner_id)))
        .order_by(User.username, User.id)
    ]
    return dict(protocols=protocols, creators=creators)


def validate(category, resource_type, condition):
    basic = condition.protocols is not None or bool(condition.methods) or bool(condition.createdBy)
    if basic and category != "api" or condition.methods and resource_type != "API":
        raise HTTPException(422, "基础协议及请求方式筛选不属于当前资源模式")
    if basic and (condition.filters is not None or condition.mine):
        raise HTTPException(422, "高级视图不能混用接口基础筛选")


def case_candidates(
    db, source, category, search, folder, priority, page, size, condition, sort, direction
):
    from utils.serializer import serialize_model

    records, modules, folders, counts = case_query(
        db, source.project_id, category, search, folder, priority, condition=condition
    )
    column = (
        {"id": TestCase.case_code, "name": TestCase.name, "createdAt": TestCase.created_at}[sort]
        if sort
        else TestCase.created_at
    )
    descending = direction == "desc" if sort else True
    records = records.order_by(column.desc() if descending else column.asc(), TestCase.id)
    names = {m.id: m.name for m in modules}
    total = records.count()
    page_rows = records.offset((page - 1) * size).limit(size).all()
    return dict(
        items=[
            dict(
                serialize_model(row, camel_case=True),
                moduleName=names.get(row.module_id, "未分配模块"),
            )
            for row in page_rows
        ],
        total=total,
        page=page,
        size=size,
        modules=folders,
        counts=counts,
    )
