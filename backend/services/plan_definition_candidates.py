"""关联接口候选及真实子用例展开，定义ID与用例ID始终区分。"""

from collections import Counter
from fastapi import HTTPException
from models import TestCase, Module, User
from models.native_case import ApiDefinition, NativeCaseConfig
from services.case_candidates import descendants
from services.case_query import parse_filters, matches, matches_related
from services.case_filter_context import CaseFilterContext

FIELDS = {
    "id",
    "name",
    "moduleId",
    "protocol",
    "method",
    "path",
    "nativeState",
    "tags",
    "caseTotal",
    "planIds",
    "createdBy",
    "createdAt",
    "updatedBy",
    "updatedAt",
}


def parse_definition_filters(raw):
    conditions, logic = parse_filters(raw, extra_fields=FIELDS)
    if any(c["field"] not in FIELDS for c in conditions):
        raise HTTPException(422, "筛选字段不属于接口模式")
    for condition in conditions:
        if condition["field"] == "caseTotal":
            operator, value = condition["operator"], condition.get("value")
            if operator not in {
                "equals",
                "not_equals",
                "gt",
                "gte",
                "lt",
                "lte",
                "between",
                "is_empty",
                "is_not_empty",
            }:
                raise HTTPException(422, "接口用例数不支持此运算")
            values = value if operator == "between" else [value]
            if operator not in {"is_empty", "is_not_empty"} and any(
                type(v) is not int or v < 0 for v in values
            ):
                raise HTTPException(422, "接口用例数须为非负整数")
    return conditions, logic


def read(query, current_read):
    return (query.populate_existing().with_for_update() if current_read else query).all()


def children(db, project_id, ids, *, current_read=False):
    # 只展开本项目未回收、可执行的API主用例，不创建副本，也不修改原生配置。
    return read(
        db.query(TestCase, NativeCaseConfig.api_definition_id)
        .join(NativeCaseConfig, NativeCaseConfig.case_id == TestCase.id)
        .filter(
            TestCase.project_id == project_id,
            TestCase.type == "api",
            TestCase.is_automated.is_(True),
            TestCase.deleted_at.is_(None),
            NativeCaseConfig.api_definition_id.in_(ids),
        )
        .order_by(TestCase.created_at.desc(), TestCase.id),
        current_read,
    )


def query(db, project_id, category, search, folder, priority, *, current_read=False):
    from sqlalchemy import func, or_

    if category != "api" or priority:
        raise HTTPException(422, "接口模式不支持用例分类或等级筛选")
    records = db.query(ApiDefinition).filter_by(project_id=project_id)
    keyword = search.strip().casefold()
    if keyword:
        records = records.filter(
            or_(
                func.lower(ApiDefinition.name).contains(keyword, autoescape=True),
                func.lower(ApiDefinition.id).contains(keyword, autoescape=True),
            )
        )
    modules = read(
        db.query(Module)
        .filter_by(project_id=project_id)
        .order_by(Module.sort_order, Module.created_at),
        current_read,
    )
    if folder == "unassigned":
        records = records.filter(
            or_(
                ApiDefinition.module_id.is_(None),
                ApiDefinition.module_id.notin_([m.id for m in modules]),
            )
        )
    elif folder != "all":
        if folder not in {m.id for m in modules}:
            raise HTTPException(404, "接口模块不属于当前来源项目")
        records = records.filter(ApiDefinition.module_id.in_(descendants(modules, folder)))
    if current_read:
        records = records.populate_existing().with_for_update()
    return records, modules, [], {}


def values(definition, case_total, names=None):
    request = (definition.parameters or {}).get("request")
    method = request.get("method") if isinstance(request, dict) else None
    names = names or {}
    return dict(
        id=definition.id,
        name=definition.name,
        moduleId=definition.module_id,
        protocol=definition.protocol,
        path=definition.path,
        method=method,
        nativeState=definition.state,
        tags=definition.tags or [],
        caseTotal=case_total,
        createdBy=definition.created_by,
        updatedBy=definition.updated_by,
        createdByName=names.get(definition.created_by),
        updatedByName=names.get(definition.updated_by),
        createdAt=definition.created_at,
        updatedAt=definition.updated_at,
    )


def filtered(db, project_id, raw, mine, user_id, *, current_read=False):
    conditions, logic = parse_definition_filters(raw)
    context = CaseFilterContext(db, project_id, conditions, user_id, current_read=current_read)
    definitions = read(
        db.query(ApiDefinition)
        .filter_by(project_id=project_id)
        .order_by(ApiDefinition.created_at.desc(), ApiDefinition.id),
        current_read,
    )
    child_rows = children(db, project_id, [d.id for d in definitions], current_read=current_read)
    totals = Counter(identifier for _, identifier in child_rows)
    membership = {}
    if any(c["field"] == "planIds" for c in conditions):
        from services.plan_candidate_filter import plan_membership

        by_case, _ = plan_membership(db, project_id, current_read=current_read)
        for case, identifier in child_rows:
            membership.setdefault(identifier, set()).update(by_case.get(case.id, set()))
    combine = all if logic == "and" else any

    def check(definition, condition):
        field, expected = condition["field"], condition.get("value")
        if field == "planIds":
            return matches_related(
                list(membership.get(definition.id, [])), condition["operator"], expected
            )
        if field == "moduleId":

            def module(value):
                return (
                    None
                    if isinstance(value, str) and value in {"null", "unplanned", "__unassigned__"}
                    else value
                )

            expected = (
                [module(v) for v in expected] if isinstance(expected, list) else module(expected)
            )
        return matches(
            values(definition, totals[definition.id]).get(field),
            condition["operator"],
            expected,
        )

    return [
        d
        for d in definitions
        if (not mine or d.created_by == user_id)
        and (not context.conditions or combine(check(d, c) for c in context.conditions))
    ]


def candidates(
    db,
    source,
    search,
    folder,
    priority,
    page,
    size,
    filters,
    mine,
    user_id,
    condition=None,
    sort=None,
    direction="asc",
):
    from services.plan_candidate_basic import query_factory
    from schemas.plan_candidate_selection import CandidateCondition

    condition = condition or CandidateCondition()
    basic_query = query_factory(condition, "API")
    column = {
        "id": ApiDefinition.id,
        "name": ApiDefinition.name,
        "createdAt": ApiDefinition.created_at,
    }.get(sort, ApiDefinition.created_at)
    descending = direction == "desc" if sort else True
    if filters is not None or mine:
        definitions = filtered(db, source.project_id, filters, mine, user_id)
        modules = read(
            db.query(Module)
            .filter_by(project_id=source.project_id)
            .order_by(Module.sort_order, Module.created_at),
            False,
        )
        counts = Counter(d.module_id for d in definitions)
        total = len(definitions)
        definitions.sort(
            key=lambda d: (
                getattr(
                    d,
                    {"id": "id", "name": "name", "createdAt": "created_at"}.get(sort, "created_at"),
                ),
                d.id,
            ),
            reverse=descending,
        )
        page_rows = definitions[(page - 1) * size : page * size]
    else:
        records, modules, _, _ = basic_query(db, source.project_id, "api", search, "all", priority)
        from sqlalchemy import func

        counts = Counter(
            dict(
                records.with_entities(ApiDefinition.module_id, func.count(ApiDefinition.id))
                .group_by(ApiDefinition.module_id)
                .all()
            )
        )
        if folder != "all":
            records, _, _, _ = basic_query(db, source.project_id, "api", search, folder, priority)
        total = records.count()
        page_rows = (
            records.order_by(column.desc() if descending else column.asc(), ApiDefinition.id)
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )
    totals = Counter(
        identifier for _, identifier in children(db, source.project_id, [d.id for d in page_rows])
    )
    names = dict(
        db.query(User.id, User.username)
        .filter(
            User.id.in_({uid for d in page_rows for uid in (d.created_by, d.updated_by) if uid})
        )
        .all()
    )
    module_names = {m.id: m.name for m in modules}
    return dict(
        items=[
            dict(
                values(d, totals[d.id], names),
                moduleName=module_names.get(d.module_id, "未分配模块"),
            )
            for d in page_rows
        ],
        total=total,
        page=page,
        size=size,
        modules=[
            dict(
                id=m.id,
                name=m.name,
                parentId=m.parent_id,
                count=sum(counts[key] for key in descendants(modules, m.id)),
            )
            for m in modules
        ],
        counts=dict(
            all=sum(counts.values()),
            unassigned=sum(count for key, count in counts.items() if key not in module_names),
        ),
    )


def resolve_definitions(
    db, source, selection, relations, uses_tree, user_id, *, current_read=False
):
    from services.plan_candidate_selection import LIMIT

    condition, excluded, summary = selection.condition, 0, {}
    from services.plan_candidate_basic import query_factory, definition_filters

    basic_query = query_factory(condition, "API")
    if selection.moduleMaps is not None:
        from services.plan_candidate_modules import resolve_modules

        definitions, excluded, summary = resolve_modules(
            db,
            source,
            selection,
            relations,
            uses_tree,
            current_read=current_read,
            resource_model=ApiDefinition,
        )
    elif selection.selectAll:
        if condition.filters is not None or condition.mine:
            definitions = filtered(
                db,
                source.project_id,
                condition.filters,
                condition.mine,
                user_id,
                current_read=current_read,
            )
        else:
            records, _, _, _ = basic_query(
                db,
                source.project_id,
                "api",
                condition.search,
                condition.folder,
                condition.priority,
                current_read=current_read,
            )
            definitions = (
                records.order_by(ApiDefinition.created_at.desc(), ApiDefinition.id)
                .limit(LIMIT + len(selection.excludeIds) + 1)
                .all()
            )
        excluded_ids = set(selection.excludeIds)
        excluded = sum(d.id in excluded_ids for d in definitions)
        definitions = [d for d in definitions if d.id not in excluded_ids]
    else:
        definitions = read(
            definition_filters(db.query(ApiDefinition), condition)
            .filter(
                ApiDefinition.id.in_(selection.definitionIds),
                ApiDefinition.project_id == source.project_id,
            )
            .order_by(ApiDefinition.created_at.desc(), ApiDefinition.id),
            current_read,
        )
        if len(definitions) != len(selection.definitionIds):
            raise HTTPException(404, "接口不存在或不属于当前来源项目")
    if len(definitions) > LIMIT:
        raise HTTPException(422, "每批最多选择10000个接口，请缩小范围")
    cases = [
        case
        for case, _ in children(
            db,
            source.project_id,
            [d.id for d in definitions],
            current_read=current_read,
        )
    ]
    summary["selectedDefinitionCount"] = len(definitions)
    if current_read:
        from core.logger import logger

        logger.info(
            "接口关联已按当前定义展开：来源项目={}，接口={}，子用例={}，排除接口={}",
            source.project_id,
            len(definitions),
            len(cases),
            excluded,
        )
    return cases, excluded, summary
