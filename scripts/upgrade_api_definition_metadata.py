#!/usr/bin/env python3
"""增量添加接口目录、状态、标签和创建人；历史未知值保留为空。"""

import argparse
import sys
from pathlib import Path
from sqlalchemy import inspect, text
from sqlalchemy.schema import CreateColumn, CreateIndex

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
from database import engine
from models.native_case import ApiDefinition
from core.logger import logger

COLUMNS = ("module_id", "state", "tags", "created_by")


def upgrade(apply=False, connection_engine=None):
    target = connection_engine or engine
    inspector = inspect(target)
    if "native_api_definitions" not in inspector.get_table_names():
        raise RuntimeError("接口定义表尚未初始化，请核对数据库")
    actual = {
        column["name"]: column
        for column in inspector.get_columns("native_api_definitions")
    }
    for name in COLUMNS:
        if name in actual:
            expected = ApiDefinition.__table__.c[name]
            if (
                actual[name]["type"]._type_affinity is not expected.type._type_affinity
                or not actual[name]["nullable"]
                or getattr(expected.type, "length", None)
                and getattr(actual[name]["type"], "length", None)
                and actual[name]["type"].length < expected.type.length
            ):
                raise RuntimeError(f"接口元数据列结构不兼容：{name}")
    missing = [name for name in COLUMNS if name not in actual]
    logger.info("接口元数据增量检查：待新增={}，执行={}", missing, apply)
    if apply:
        with target.begin() as connection:
            for name in missing:
                column = ApiDefinition.__table__.c[name]
                declaration = str(CreateColumn(column).compile(dialect=target.dialect))
                if target.dialect.name == "sqlite" and column.foreign_keys:
                    foreign = next(iter(column.foreign_keys))
                    declaration += f" REFERENCES {foreign.column.table.name} ({foreign.column.name})"
                    if foreign.ondelete:
                        declaration += " ON DELETE " + foreign.ondelete
                connection.execute(
                    text("ALTER TABLE native_api_definitions ADD COLUMN " + declaration)
                )
                logger.info("接口元数据列已添加：{}，已有定义未重建", name)
            if target.dialect.name == "mysql":
                foreign_columns = {
                    tuple(f["constrained_columns"])
                    for f in inspect(connection).get_foreign_keys(
                        "native_api_definitions"
                    )
                }
                for name in ("module_id", "created_by"):
                    if (name,) not in foreign_columns:
                        foreign = next(
                            iter(ApiDefinition.__table__.c[name].foreign_keys)
                        )
                        delete = (
                            " ON DELETE " + foreign.ondelete if foreign.ondelete else ""
                        )
                        connection.execute(
                            text(
                                f"ALTER TABLE native_api_definitions ADD CONSTRAINT fk_native_definition_{name} FOREIGN KEY ({name}) REFERENCES {foreign.column.table.name} ({foreign.column.name}){delete}"
                            )
                        )
            indexes = {
                index["name"]
                for index in inspect(connection).get_indexes("native_api_definitions")
            }
            for index in ApiDefinition.__table__.indexes:
                if (
                    tuple(column.name for column in index.columns) == ("module_id",)
                    and index.name not in indexes
                ):
                    connection.execute(CreateIndex(index))
        logger.info("接口元数据迁移完成：历史创建人、状态、标签和模块均未推断填充")
    return missing


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    arguments = parser.parse_args()
    try:
        upgrade(arguments.apply)
    except Exception:
        logger.exception("接口元数据增量迁移失败，请检查完整堆栈后重试")
        raise
