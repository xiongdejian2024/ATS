"""按具体模块组合范围；父子展开由客户端提交，数据库去重、计数和验证。"""
from fastapi import HTTPException
from sqlalchemy import and_, or_, func
from models import TestCase
from services.case_candidates import candidate_query


def resolve_modules(db, plan, selection, relations, uses_tree, *, current_read=False):
    from services.plan_candidate_selection import LIMIT
    condition = selection.condition
    query, modules, _, _ = candidate_query(db, plan.project_id, selection.category,
        condition.search, 'all', condition.priority, current_read=current_read)
    known = {row.id for row in modules}
    maps = selection.moduleMaps
    if set(maps) - known - {'all', 'unassigned'}:
        raise HTTPException(404, '关联选择模块已删除或不属于当前项目')
    if not uses_tree:
        query = query.filter(TestCase.id.notin_([row.case_id for row in relations]))

    def module_filter(key):
        if key == 'unassigned':
            return or_(TestCase.module_id.is_(None), TestCase.module_id.notin_(known))
        return TestCase.module_id == key

    # 逐条ID在当前读中核对模块归属；移动、回收、分类变化时整批拒绝。
    explicit = {cid: key for key, value in maps.items() for cid in value.selectIds}
    if explicit:
        rows_query = db.query(TestCase).filter(TestCase.id.in_(explicit), TestCase.project_id == plan.project_id,
            TestCase.deleted_at.is_(None))
        rows = (rows_query.populate_existing().with_for_update() if current_read else rows_query).all()
        if len(rows) != len(explicit):
            raise HTTPException(404, '模块选择用例不存在、已回收或不属于当前项目')
        for row in rows:
            actual = row.module_id if row.module_id in known else 'unassigned'
            category = row.type if row.type in ('api', 'scenario') else 'functional'
            if actual != explicit[row.id] or category != selection.category or category != 'functional' and not row.is_automated:
                raise HTTPException(409, '已选用例的模块或分类已改变，请刷新后重新选择')

    clauses, exclusion_clauses = [], []
    base = maps.get('all')
    if base:
        remaining = TestCase.module_id.in_(known - set(maps)) if 'unassigned' in maps else or_(TestCase.module_id.is_(None), TestCase.module_id.notin_(set(maps) - {'all'}))
        clauses.append(and_(remaining, TestCase.id.notin_(base.excludeIds)))
        exclusion_clauses.append(and_(remaining, TestCase.id.in_(base.excludeIds)))
    for key, entry in maps.items():
        if key == 'all':
            continue
        scope = module_filter(key)
        clauses.append(and_(scope, TestCase.id.notin_(entry.excludeIds) if entry.selectAll else TestCase.id.in_(entry.selectIds)))
        if entry.selectAll:
            exclusion_clauses.append(and_(scope, TestCase.id.in_(entry.excludeIds)))
    selected_query = query.filter(or_(*clauses))
    cases = selected_query.order_by(TestCase.created_at.desc(), TestCase.id).limit(LIMIT + 1).all()
    if len(cases) > LIMIT:
        raise HTTPException(422, '每批最多关联10000条用例，请缩小模块范围')
    excluded_query = query.filter(or_(*exclusion_clauses)) if exclusion_clauses else None
    excluded_count = (len(excluded_query.all()) if current_read else excluded_query.count()) if excluded_query is not None else 0
    if current_read:
        return cases, excluded_count, {}
    # 返回精确模块计数，前端按完整树汇总；父子模块从不重复计算。
    def totals(source):
        result = dict(source.with_entities(TestCase.module_id, func.count(TestCase.id)).group_by(TestCase.module_id).all())
        return {**{key: result.get(key, 0) for key in known},
            'unassigned': sum(value for key, value in result.items() if key not in known)}
    total, selected = totals(query), totals(selected_query)
    return cases, excluded_count, {'moduleCounts': {key: {'total': total[key], 'selected': selected[key]} for key in total},
        'eligibleCount': sum(total.values())}
