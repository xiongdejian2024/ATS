#!/usr/bin/env python3
"""只增加可空HTTP详情JSON列，历史执行及日志保留；支持SQLite/MySQL幂等升级。"""

import argparse
import sys
from pathlib import Path
from sqlalchemy import inspect, text
from sqlalchemy.schema import CreateColumn

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
from database import engine
from models.test_suite import TestSuiteExecution
from core.logger import logger


def upgrade(apply=False, connection_engine=None):
    target = connection_engine or engine
    table, name = "test_suite_executions", "native_detail"
    inspector = inspect(target)
    if table not in inspector.get_table_names():
        raise RuntimeError("执行记录表尚未初始化")
    actual = {c["name"]: c for c in inspector.get_columns(table)}
    column = TestSuiteExecution.__table__.c[name]
    if name in actual:
        if (
            not actual[name]["nullable"]
            or actual[name]["type"]._type_affinity is not column.type._type_affinity
        ):
            raise RuntimeError("HTTP详情列结构不兼容")
        logger.info("HTTP详情列已存在，结构兼容，无需升级")
        return []
    logger.info("HTTP详情列增量检查：待增加={}，执行={}", name, apply)
    if apply:
        declaration = str(CreateColumn(column).compile(dialect=target.dialect))
        with target.begin() as connection:
            connection.execute(text(f"ALTER TABLE {table} ADD COLUMN {declaration}"))
        logger.info("HTTP详情可空列已增加；历史结果和日志没有改写")
    return [name]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        upgrade(args.apply)
    except Exception:
        logger.exception("HTTP详情增量升级失败")
        raise
