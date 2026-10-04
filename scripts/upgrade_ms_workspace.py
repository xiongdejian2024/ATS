#!/usr/bin/env python3
"""预览或执行用例、计划工作区增量升级；只新增表、列和索引，禁止重建已有表。"""
import argparse
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from sqlalchemy import JSON, Text, inspect, text, UniqueConstraint
from sqlalchemy.schema import CreateColumn, CreateIndex, CreateTable, AddConstraint
from core.logger import logger


# 明确允许扩展的原业务表，其他已有表出现模型漂移时立即停止。
EXTENSIBLE_TABLES = {
    "test_cases", "case_reviews", "case_review_items", "case_saved_views",
    "test_plans", "plan_settings", "plan_runs", "plan_run_items", "plan_case_relations",
    "task_schedules", "task_schedule_runs", "plan_groups",
}


def _constraint_name(prefix, table, columns):
    import hashlib
    raw=prefix+'_'+table+'_'+'_'.join(columns)
    return raw if len(raw)<=60 else raw[:45]+'_'+hashlib.sha256(raw.encode()).hexdigest()[:12]


def _column_sql(column, dialect):
    """Python 默认值不会进入 DDL；为已有行补充等价、可复查的 SQL 默认值。"""
    rendered = str(CreateColumn(column).compile(dialect=dialect))
    if column.nullable or column.server_default is not None:
        return rendered
    default = column.default
    if default is None:
        raise RuntimeError(f"{column.table.name}.{column.name} 非空新列没有默认值，已停止升级")
    value = default.arg
    if default.is_callable:
        # SQLAlchemy 对 list/dict 进行了 context 包装，只允许已知纯构造器。
        unwrapped = getattr(value, "__wrapped__", value)
        if unwrapped not in (list, dict):
            raise RuntimeError(f"{column.table.name}.{column.name} 默认值需要显式数据迁移")
        value = unwrapped()
    if isinstance(column.type, JSON):
        literal = "'" + json.dumps(value, ensure_ascii=False).replace("'", "''") + "'"
        if dialect.name == "mysql":
            literal = f"({literal})"
    elif isinstance(value, bool):
        literal = "1" if value else "0"
    elif isinstance(value, (int, float)):
        literal = str(value)
    elif isinstance(value, str):
        literal = "'" + value.replace("'", "''") + "'"
        # MySQL 8 要求 TEXT/BLOB 默认值使用表达式，即使默认值为空字符串。
        if dialect.name == "mysql" and isinstance(column.type, Text):
            literal=f"({literal})"
    else:
        raise RuntimeError(f"{column.table.name}.{column.name} 默认值不受支持")
    return rendered + " DEFAULT " + literal


def migration_plan(engine):
    from database import Base
    import models  # 注册全部业务模型
    inspector = inspect(engine)
    existing = set(inspector.get_table_names())
    required = {"users", "projects", "test_cases", "test_plans", "test_suites", "environments", "task_queue"}
    if not required <= existing:
        raise RuntimeError("当前数据库不是已初始化的 ATS，已停止增量升级")
    steps = []
    quote = engine.dialect.identifier_preparer.quote
    for table in Base.metadata.sorted_tables:
        if table.name not in existing:
            steps.append((f"新增表 {table.name}", str(CreateTable(table).compile(dialect=engine.dialect))))
            for index in sorted(table.indexes, key=lambda x: x.name):
                steps.append((f"新增索引 {index.name}", str(CreateIndex(index).compile(dialect=engine.dialect))))
            continue
        actual = {c["name"]: c for c in inspector.get_columns(table.name)}
        missing_columns=set(table.columns.keys())-set(actual)
        for column in table.columns:
            if column.name in actual:
                continue
            if table.name not in EXTENSIBLE_TABLES:
                raise RuntimeError(f"已有表 {table.name} 存在未授权的结构漂移：缺少 {column.name}")
            column_sql=_column_sql(column,engine.dialect)
            if engine.dialect.name=='sqlite':
                # SQLite 只允许在新增列时声明外键；绝不重建已有业务表。
                for foreign in column.foreign_keys:
                    column_sql+=f" REFERENCES {quote(foreign.column.table.name)} ({quote(foreign.column.name)})"
                    if foreign.ondelete: column_sql+=' ON DELETE '+foreign.ondelete
            ddl = f"ALTER TABLE {quote(table.name)} ADD COLUMN {column_sql}"
            steps.append((f"新增列 {table.name}.{column.name}", ddl))
        if table.name=='case_reviews':
            needs_backfill='mode' in missing_columns
            if not needs_backfill:
                with engine.connect() as connection:
                    needs_backfill=bool(connection.execute(text("SELECT COUNT(*) FROM case_reviews WHERE mode IS NULL OR (policy = 'any' AND mode <> 'single') OR (policy <> 'any' AND mode <> 'multiple')")).scalar())
            if needs_backfill:
                # 即使上次进程在 ADD COLUMN 后中断，重试也会继续数据回填。
                steps.append(("将历史评审规则迁为对应评审模式", "UPDATE case_reviews SET mode = CASE WHEN policy = 'any' THEN 'single' ELSE 'multiple' END WHERE mode IS NULL OR (policy = 'any' AND mode <> 'single') OR (policy <> 'any' AND mode <> 'multiple')"))
        # CreateColumn 不包含外键；逐一检查签名补约束，不能只补索引。
        actual_fks={(tuple(fk['constrained_columns']),fk['referred_table'],tuple(fk['referred_columns'])) for fk in inspector.get_foreign_keys(table.name)}
        for constraint in table.foreign_key_constraints:
            columns=tuple(column.name for column in constraint.columns)
            targets=tuple(element.column.name for element in constraint.elements)
            referred=next(iter(constraint.elements)).column.table.name
            if (columns,referred,targets) in actual_fks: continue
            # 本次升级只补新增业务列的约束，不擅自修复原库既有结构差异。
            new_foreign_columns = {"test_cases": {"deleted_by"}}.get(table.name, set())
            if not set(columns).intersection(missing_columns | new_foreign_columns):
                continue
            if table.name not in EXTENSIBLE_TABLES:
                raise RuntimeError(f"已有表 {table.name} 缺少外键约束，需单独审查")
            if engine.dialect.name=='sqlite':
                if set(columns)<=missing_columns: continue
                raise RuntimeError(f"SQLite 已有列 {table.name}.{','.join(columns)} 缺少外键；禁止重建，请人工审查")
            if not constraint.name:
                constraint.name=_constraint_name('fk',table.name,columns)
            steps.append((f"新增外键 {constraint.name}",str(AddConstraint(constraint).compile(dialect=engine.dialect))))
        unique_columns={tuple(c['column_names']) for c in inspector.get_unique_constraints(table.name)}
        unique_columns.update(tuple(i['column_names']) for i in inspector.get_indexes(table.name) if i.get('unique'))
        for constraint in table.constraints:
            if not isinstance(constraint,UniqueConstraint): continue
            columns=tuple(c.name for c in constraint.columns)
            if columns in unique_columns: continue
            name=constraint.name or _constraint_name('uq',table.name,columns)
            ddl=f"CREATE UNIQUE INDEX {quote(name)} ON {quote(table.name)} ({', '.join(quote(c) for c in columns)})"
            steps.append((f"新增唯一约束 {name}",ddl))
        existing_indexes = {index["name"] for index in inspector.get_indexes(table.name)}
        for index in sorted(table.indexes, key=lambda x: x.name):
            if index.name not in existing_indexes:
                steps.append((f"新增索引 {index.name}", str(CreateIndex(index).compile(dialect=engine.dialect))))
    return steps


def upgrade(engine, apply=False):
    steps = migration_plan(engine)
    for description, _ in steps:
        logger.info("数据库升级计划：{}", description)
    if not apply:
        logger.info("仅预览：共 {} 项，未写入数据库", len(steps))
        return steps
    # MySQL DDL 会隐式提交；每个步骤均可重入，失败后不得自动删除或回退用户数据。
    for description, ddl in steps:
        try:
            with engine.begin() as connection:
                connection.execute(text(ddl))
            logger.info("数据库升级已完成：{}", description)
        except Exception:
            logger.exception("数据库升级失败：{}；已完成步骤保留，可修正后重试", description)
            raise
    remaining = migration_plan(engine)
    if remaining:
        raise RuntimeError("升级后仍有未完成结构变更")
    logger.info("用例与计划工作区升级完成，重复检查通过，原业务行未删除")
    return steps


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="执行增量升级；执行前备份数据库")
    arguments = parser.parse_args()
    os.chdir(ROOT / "backend")
    from database import engine
    upgrade(engine, arguments.apply)
