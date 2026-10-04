"""升级只使用隔离测试库，验证增量建表及不兼容结构阻断。"""
import os
import re
import importlib.util
from pathlib import Path
import pytest
from sqlalchemy import inspect, text
from database import Base, engine, SessionLocal
from models import User


@pytest.fixture
def upgrader():
    original = os.getcwd()
    try:
        path = Path(__file__).resolve().parents[1] / "scripts/upgrade_test_management.py"
        spec = importlib.util.spec_from_file_location("ats_upgrade_under_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        os.chdir(original)
    return module


def test_upgrade_adds_only_extensions_and_preserves_existing_data(upgrader):
    with SessionLocal() as db:
        db.add(User(id="sentinel", username="原有用户", email="sentinel@example.test", password_hash="原有数据标记"))
        db.commit()
    tables = [Base.metadata.tables[name] for name in upgrader.TABLES]
    Base.metadata.drop_all(engine, tables=tables)
    old_tables = set(inspect(engine).get_table_names())
    missing = upgrader.upgrade(apply=False)
    assert set(missing) == set(upgrader.TABLES)
    assert set(inspect(engine).get_table_names()) == old_tables
    upgrader.upgrade(apply=True)
    assert set(inspect(engine).get_table_names()) - old_tables == set(upgrader.TABLES)
    with SessionLocal() as db:
        assert db.get(User, "sentinel").password_hash == "原有数据标记"
    assert upgrader.upgrade(apply=True) == []


def test_upgrade_blocks_missing_column_before_creating_other_tables(upgrader):
    Base.metadata.tables["plan_groups"].drop(engine)
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE plan_run_items DROP COLUMN delivery_state"))
    with pytest.raises(RuntimeError, match="plan_run_items.delivery_state 缺少列"):
        upgrader.upgrade(apply=True)
    assert "plan_groups" not in inspect(engine).get_table_names()
    assert "delivery_state" not in {c["name"] for c in inspect(engine).get_columns("plan_run_items")}


def test_upgrade_blocks_missing_idempotency_unique_constraint(upgrader):
    with engine.begin() as conn:
        sql = conn.execute(text("SELECT sql FROM sqlite_master WHERE type='table' AND name='plan_runs'")).scalar_one()
        assert "UNIQUE (idempotency_key)" in sql
        # 仅重建隔离测试库中的空表，模拟既有升级不完整的数据库。
        conn.execute(text("DROP TABLE plan_runs"))
        without_unique = re.sub(r",\s*UNIQUE \(idempotency_key\)", "", sql)
        assert without_unique != sql
        conn.execute(text(without_unique))
    with pytest.raises(RuntimeError, match="plan_runs 缺少唯一约束"):
        upgrader.upgrade(apply=True)
