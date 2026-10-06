"""增量创建请求文件表；不重建或修改已有业务表，SQLite/MySQL幂等。"""

import argparse
import sys
from pathlib import Path
from sqlalchemy import inspect

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
from database import engine
import models
from models.native_request_file import NativeRequestFile
from core.logger import logger


def upgrade(apply=False, connection_engine=None):
    target = connection_engine or engine
    table = NativeRequestFile.__table__
    inspector = inspect(target)
    if table.name in inspector.get_table_names():
        columns = {c["name"]: c for c in inspector.get_columns(table.name)}
        if (
            set(columns) != set(table.c.keys())
            or any(
                columns[c.name]["nullable"] != c.nullable
                or columns[c.name]["type"].compile(dialect=target.dialect).lower()
                != c.type.compile(dialect=target.dialect).lower()
                for c in table.c
            )
            or inspector.get_pk_constraint(table.name)["constrained_columns"]
            != [c.name for c in table.primary_key.columns]
        ):
            raise RuntimeError("已有请求文件表结构不兼容")
        logger.info("请求文件表结构兼容，无需升级")
        return []
    logger.info("请求文件表待创建：执行={}", apply)
    if apply:
        table.create(target, checkfirst=True)
        logger.info("不可变请求文件表已创建，原业务表保持")
    return [table.name]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    try:
        upgrade(parser.parse_args().apply)
    except Exception:
        logger.exception("请求文件表升级失败")
        raise
