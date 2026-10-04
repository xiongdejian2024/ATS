#!/usr/bin/env python3
"""检查或创建测试管理扩展表，不删除或重建已有业务表。"""
import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
os.chdir(ROOT / "backend")
from sqlalchemy import inspect, UniqueConstraint, Boolean
from sqlalchemy.dialects.mysql import TINYINT
from database import engine, Base
import models
from core.logger import logger

TABLES = (
    "case_versions", "case_reviews", "case_review_items", "case_review_decisions",
    "case_review_comments", "case_saved_views", "plan_groups", "plan_settings",
    "plan_runs", "plan_run_items", "task_schedules", "task_schedule_runs",
    "ai_model_configs", "ai_conversations", "ai_case_drafts",
)


def check_existing_structure(inspector, existing):
    """阻止部分升级或不兼容表被 checkfirst 静默当作已升级。"""
    problems = []
    for name in TABLES:
        if name not in existing:
            continue
        expected = Base.metadata.tables[name]
        actual_columns = {c["name"]: c for c in inspector.get_columns(name)}
        for column in expected.columns:
            actual = actual_columns.get(column.name)
            if actual is None:
                problems.append(f"{name}.{column.name} 缺少列")
                continue
            mysql_boolean = (isinstance(column.type, Boolean)
                             and isinstance(actual["type"], TINYINT)
                             and actual["type"].display_width == 1)
            if not mysql_boolean and actual["type"]._type_affinity is not column.type._type_affinity:
                problems.append(f"{name}.{column.name} 类型不兼容")
            if bool(actual["nullable"]) != bool(column.nullable):
                problems.append(f"{name}.{column.name} 可空约束不一致")
            expected_length, actual_length = getattr(column.type, "length", None), getattr(actual["type"], "length", None)
            if expected_length and actual_length and actual_length < expected_length:
                problems.append(f"{name}.{column.name} 字段长度不足")
        primary = tuple(inspector.get_pk_constraint(name).get("constrained_columns") or [])
        if primary != tuple(c.name for c in expected.primary_key.columns):
            problems.append(f"{name} 主键不一致")
        actual_unique = {tuple(c["column_names"]) for c in inspector.get_unique_constraints(name)}
        actual_unique |= {tuple(i["column_names"]) for i in inspector.get_indexes(name) if i.get("unique")}
        expected_unique = {tuple(c.name for c in constraint.columns)
                           for constraint in expected.constraints if isinstance(constraint, UniqueConstraint)}
        expected_unique |= {tuple(c.name for c in index.columns) for index in expected.indexes if index.unique}
        for columns in expected_unique - actual_unique:
            problems.append(f"{name} 缺少唯一约束 ({', '.join(columns)})")
        actual_foreign = {(tuple(f["constrained_columns"]), f["referred_table"], tuple(f["referred_columns"]))
                          for f in inspector.get_foreign_keys(name)}
        for constraint in expected.foreign_key_constraints:
            signature = (tuple(e.parent.name for e in constraint.elements),
                         next(iter(constraint.elements)).column.table.name,
                         tuple(e.column.name for e in constraint.elements))
            if signature not in actual_foreign:
                problems.append(f"{name} 缺少外键 ({', '.join(signature[0])})")
    if problems:
        raise RuntimeError("已有扩展表结构不兼容，已停止升级；请通过审查后的迁移处理，不会自动重建或删除：" + "；".join(problems))


def upgrade(apply=False):
    inspector = inspect(engine)
    existing = set(inspector.get_table_names())
    missing = [name for name in TABLES if name not in existing]
    logger.info("测试管理扩展表检查：已存在={}，待创建={}", len(TABLES) - len(missing), missing)
    required = {"users", "projects", "test_cases", "test_plans", "test_suites", "environments", "task_queue"}
    if not required <= existing:
        raise RuntimeError("当前数据库不是已初始化的 ATS，请检查连接配置")
    check_existing_structure(inspector, existing)
    if apply:
        Base.metadata.create_all(engine, tables=[Base.metadata.tables[name] for name in missing], checkfirst=True)
        after = inspect(engine)
        check_existing_structure(after, set(after.get_table_names()))
        logger.info("测试管理扩展表已就绪，结构与关键约束检查通过，已有业务表未修改")
    return missing


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="执行新增表创建；运行前应备份数据库")
    args = parser.parse_args()
    try:
        upgrade(args.apply)
    except Exception:
        logger.exception("测试管理扩展表升级失败，已有业务表未主动删除或重建")
        raise
