#!/usr/bin/env python3
"""Preview/apply a data-preserving MySQL script-job migration; never rebuild tables."""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from sqlalchemy import inspect, text, UniqueConstraint
from sqlalchemy.schema import CreateTable, CreateIndex

TABLES = ("script_jobs", "script_job_runs", "script_job_logs")


def migration_plan(engine):
    from database import Base
    import models
    inspector = inspect(engine)
    existing = set(inspector.get_table_names())
    if not {"users", "projects", "environments", "test_suites", "task_queue"} <= existing:
        raise RuntimeError("不是已初始化的ATS数据库")
    columns = {c["name"]: c for c in inspector.get_columns("task_queue")}
    if engine.dialect.name == "sqlite" and not columns["suite_id"]["nullable"]:
        # Preflight before ANY DDL. SQLite cannot relax this constraint without
        # rebuilding user data; the migration does not silently take that route.
        raise RuntimeError("旧SQLite的task_queue.suite_id为NOT NULL；本迁移禁止重建已有表。请先制定独立数据迁移方案；数据库未修改")
    if engine.dialect.name not in {"mysql", "sqlite"}:
        raise RuntimeError("仅支持MySQL升级或新建SQLite结构")
    steps = []
    for name in TABLES:
        table = Base.metadata.tables[name]
        if name not in existing:
            steps.append((f"创建{name}", str(CreateTable(table).compile(dialect=engine.dialect))))
            steps.extend((f"创建索引{index.name}", str(CreateIndex(index).compile(dialect=engine.dialect))) for index in table.indexes)
        else:
            actual = {c["name"]: c for c in inspector.get_columns(name)}
            for col in table.columns:
                found = actual.get(col.name)
                if found is None or found["type"]._type_affinity is not col.type._type_affinity or bool(found["nullable"]) != bool(col.nullable):
                    raise RuntimeError(f"已有{name}.{col.name}结构不兼容，禁止覆盖或重建")
                expected_length, actual_length = getattr(col.type, "length", None), getattr(found["type"], "length", None)
                if expected_length and actual_length and actual_length < expected_length:
                    raise RuntimeError(f"已有{name}.{col.name}字段长度不足")
            primary = tuple(inspector.get_pk_constraint(name).get("constrained_columns") or [])
            if primary != tuple(c.name for c in table.primary_key.columns):
                raise RuntimeError(f"已有{name}主键不兼容")
            actual_indices = inspector.get_indexes(name)
            actual_unique = {tuple(c["column_names"]) for c in inspector.get_unique_constraints(name)}
            actual_unique |= {tuple(i["column_names"]) for i in actual_indices if i.get("unique")}
            expected_unique = {tuple(c.name for c in constraint.columns) for constraint in table.constraints if isinstance(constraint, UniqueConstraint)}
            if not expected_unique <= actual_unique:
                raise RuntimeError(f"已有{name}缺少关键唯一约束，禁止静默继续")
            actual_foreign = {(tuple(f["constrained_columns"]), f["referred_table"], tuple(f["referred_columns"])) for f in inspector.get_foreign_keys(name)}
            expected_foreign = {(tuple(c.name for c in fk.columns), next(iter(fk.elements)).column.table.name,
                                 tuple(e.column.name for e in fk.elements)) for fk in table.foreign_key_constraints}
            if not expected_foreign <= actual_foreign:
                raise RuntimeError(f"已有{name}缺少关键外键，禁止静默继续")
            existing_indices = {i["name"] for i in actual_indices}
            steps.extend((f"补充索引{index.name}", str(CreateIndex(index).compile(dialect=engine.dialect)))
                         for index in table.indexes if index.name not in existing_indices)
    if "kind" not in columns:
        steps.append(("增加queue类型并为历史行默认suite", "ALTER TABLE task_queue ADD COLUMN kind VARCHAR(16) NOT NULL DEFAULT 'suite'"))
    if "script_job_id" not in columns:
        sql = "ALTER TABLE task_queue ADD COLUMN script_job_id VARCHAR(36) NULL"
        if engine.dialect.name == "sqlite":
            sql += " REFERENCES script_jobs(id)"
        steps.append(("增加独立脚本目标", sql))
    if not columns["suite_id"]["nullable"]:
        steps.append(("保留旧测试套外键并允许脚本目标", "ALTER TABLE task_queue MODIFY COLUMN suite_id VARCHAR(36) NULL"))
    foreign = {(tuple(f["constrained_columns"]), f["referred_table"]) for f in inspector.get_foreign_keys("task_queue")}
    if (("script_job_id",), "script_jobs") not in foreign and engine.dialect.name == "mysql":
        steps.append(("增加脚本作业外键", "ALTER TABLE task_queue ADD CONSTRAINT fk_task_queue_script_job FOREIGN KEY (script_job_id) REFERENCES script_jobs(id)"))
    indices = {i["name"] for i in inspector.get_indexes("task_queue")}
    if "ix_task_queue_script_job_id" not in indices:
        steps.append(("增加脚本目标索引", "CREATE INDEX ix_task_queue_script_job_id ON task_queue(script_job_id)"))
    checks = {c["name"] for c in inspector.get_check_constraints("task_queue")}
    if "ck_task_queue_target" not in checks:
        if engine.dialect.name == "sqlite":
            raise RuntimeError("已有SQLite缺少目标一致性约束；禁止重建，数据库未修改")
        steps.append(("约束每个queue恰有一个目标", "ALTER TABLE task_queue ADD CONSTRAINT ck_task_queue_target CHECK ((kind = 'suite' AND suite_id IS NOT NULL AND script_job_id IS NULL) OR (kind = 'script' AND suite_id IS NULL AND script_job_id IS NOT NULL))"))
    return steps


def upgrade(engine, apply=False):
    steps = migration_plan(engine)
    if not apply:
        return steps
    with engine.connect() as connection:
        before = connection.execute(text("SELECT COUNT(*) FROM task_queue")).scalar_one()
    for _, sql in steps:
        with engine.begin() as connection:
            connection.execute(text(sql))
    if migration_plan(engine):
        raise RuntimeError("迁移未完成，保留已完成的增量步骤，可检查后重试")
    with engine.connect() as connection:
        after = connection.execute(text("SELECT COUNT(*) FROM task_queue")).scalar_one()
        invalid = connection.execute(text("SELECT COUNT(*) FROM task_queue WHERE NOT ((kind = 'suite' AND suite_id IS NOT NULL AND script_job_id IS NULL) OR (kind = 'script' AND suite_id IS NULL AND script_job_id IS NOT NULL))")).scalar_one()
    if before != after or invalid:
        raise RuntimeError("迁移后的任务行数或目标约束校验失败，请检查；不会自动删除数据")
    return steps


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="执行预览的增量DDL；默认只读")
    args = parser.parse_args()
    from database import engine
    for description, sql in upgrade(engine, args.apply):
        print(description + "\n" + sql)
