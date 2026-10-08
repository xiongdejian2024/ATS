"""Safety and schema-drift checks; live PostgreSQL tests run separately in CI."""

from copy import deepcopy
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest
from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.dialects import postgresql

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import init_postgres as initializer

DIALECT = postgresql.dialect()


class Reflection:
    """An independent reflected schema snapshot, with no database connection."""

    def __init__(self, metadata, exists=True, names=None):
        self.exists = exists
        self.tables = {}
        self.views = []
        self.schemas_read = []
        selected = set(metadata.tables) if names is None else set(names)
        for table in metadata.tables.values():
            if table.name not in selected:
                continue
            columns = []
            for column in table.c:
                default = initializer._expected_default(column, DIALECT)
                if column is table.autoincrement_column:
                    default = f"nextval('ats.{table.name}_{column.name}_seq'::regclass)"
                columns.append(dict(name=column.name, type=column.type, nullable=column.nullable, default=default, identity=None))
            self.tables[table.name] = dict(
                columns=columns,
                primary=dict(constrained_columns=[c.name for c in table.primary_key]),
                uniques=[dict(column_names=[c.name for c in constraint.columns])
                         for constraint in table.constraints
                         if isinstance(constraint, initializer.UniqueConstraint)],
                fks=[dict(
                    constrained_columns=list(constraint.column_keys), referred_schema="ats",
                    referred_table=constraint.elements[0].column.table.name,
                    referred_columns=[fk.column.name for fk in constraint.elements],
                    options=dict(ondelete=constraint.ondelete, onupdate=constraint.onupdate),
                ) for constraint in table.constraints
                     if isinstance(constraint, initializer.ForeignKeyConstraint)],
                indexes=[dict(name=index.name, column_names=[c.name for c in index.columns], unique=index.unique)
                         for index in table.indexes],
                checks=[dict(sqltext=str(constraint.sqltext)) for constraint in table.constraints
                        if isinstance(constraint, initializer.CheckConstraint)],
            )

    def has_schema(self, schema):
        self.schemas_read.append(schema)
        return self.exists

    def get_table_names(self, schema):
        self.schemas_read.append(schema)
        return sorted(self.tables)

    def get_view_names(self, schema):
        self.schemas_read.append(schema)
        return self.views

    def get_materialized_view_names(self, schema):
        self.schemas_read.append(schema)
        return []

    def get_foreign_table_names(self, schema):
        self.schemas_read.append(schema)
        return []

    def _read(self, name, schema, key):
        self.schemas_read.append(schema)
        return self.tables[name][key]

    def get_columns(self, name, schema):
        return self._read(name, schema, "columns")

    def get_pk_constraint(self, name, schema):
        return self._read(name, schema, "primary")

    def get_unique_constraints(self, name, schema):
        return self._read(name, schema, "uniques")

    def get_foreign_keys(self, name, schema, **kwargs):
        assert kwargs == {"postgresql_ignore_search_path": True}
        return self._read(name, schema, "fks")

    def get_indexes(self, name, schema):
        return self._read(name, schema, "indexes")

    def get_check_constraints(self, name, schema):
        return self._read(name, schema, "checks")


@pytest.fixture
def metadata():
    value = MetaData()
    Table("users", value, Column("id", String(36), primary_key=True),
          Column("name", String(100), nullable=False, unique=True))
    Table("jobs", value, Column("id", Integer, primary_key=True),
          Column("owner_id", String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
          Column("kind", String(16), nullable=False, server_default="suite"),
          initializer.CheckConstraint("kind = 'suite' OR kind = 'script'"))
    return value


def test_complete_metadata_plans_all_82_tables_and_only_selected_schema():
    from database import Base
    import models  # noqa: F401

    reflection = Reflection(Base.metadata, exists=False, names=[])
    plan = initializer.plan_schema(reflection, Base.metadata, "ats", DIALECT)
    assert plan["expectedTableCount"] == len(plan["createTables"]) == 87
    assert plan["createSchema"] and plan["existingTables"] == []
    assert set(reflection.schemas_read) == {"ats"}


def test_compatible_tables_are_preserved_and_only_missing_tables_planned(metadata):
    reflection = Reflection(metadata, names=["users"])
    before = deepcopy(reflection.tables)
    plan = initializer.plan_schema(reflection, metadata, "ats", DIALECT)
    assert plan["createTables"] == ["jobs"] and not plan["createSchema"]
    assert list(reflection.tables) == list(before)
    assert set(reflection.schemas_read) == {"ats"}


@pytest.mark.parametrize("schema", ["public", "auth", "storage", "pg_catalog", "pg_temp", "information_schema",
                                    "supabase_migrations", "realtime", "BadCase", "ats,public", 'ats";drop schema x',
                                    "", "x" * 64])
def test_invalid_or_managed_schema_is_rejected_before_connecting(schema):
    with pytest.raises(ValueError):
        initializer.initialize(schema=schema)


@pytest.mark.parametrize("part", ["column_name", "column_type", "nullable", "default", "pk", "fk",
                                  "fk_schema", "unique", "unique_nulls", "index", "partial_index", "unique_index", "check"])
def test_existing_schema_drift_blocks_creation(metadata, part):
    reflection = Reflection(metadata)
    users, jobs = reflection.tables["users"], reflection.tables["jobs"]
    if part == "column_name":
        users["columns"].append(dict(name="legacy", type=String(), nullable=True))
    elif part == "column_type":
        users["columns"][1]["type"] = String(20)
    elif part == "nullable":
        users["columns"][1]["nullable"] = True
    elif part == "default":
        jobs["columns"][2]["default"] = "'script'::character varying"
    elif part == "pk":
        users["primary"]["constrained_columns"] = ["name"]
    elif part == "fk":
        jobs["fks"][0]["options"]["ondelete"] = "SET NULL"
    elif part == "fk_schema":
        jobs["fks"][0]["referred_schema"] = "public"
    elif part == "unique":
        users["uniques"] = []
    elif part == "unique_nulls":
        users["uniques"][0]["dialect_options"] = {"postgresql_nulls_not_distinct": True}
    elif part == "index":
        jobs["indexes"] = []
    elif part == "partial_index":
        jobs["indexes"][0]["dialect_options"] = {"postgresql_where": "kind = 'suite'"}
    elif part == "unique_index":
        jobs["indexes"].append(dict(name="extra_unique", column_names=["kind"], unique=True))
    elif part == "check":
        jobs["checks"][0]["sqltext"] = "kind = 'suite'"
    with pytest.raises(initializer.IncompatibleSchema):
        initializer.plan_schema(reflection, metadata, "ats", DIALECT)


def test_postgres_reflected_defaults_and_check_casts_are_compatible(metadata):
    reflection = Reflection(metadata)
    jobs = reflection.tables["jobs"]
    jobs["columns"][2]["default"] = "'suite'::character varying"
    jobs["checks"][0]["sqltext"] = "(((kind)::text = 'suite'::text) OR ((kind)::text = 'script'::text))"
    assert initializer.plan_schema(reflection, metadata, "ats", DIALECT)["createTables"] == []
    assert initializer._check_expression("a = 'x' AND (b IS NULL OR c IS NULL)") != initializer._check_expression("(a = 'x' AND b IS NULL) OR c IS NULL")


@pytest.mark.parametrize("nulls_not_distinct", [True, False, None])
def test_nullable_unique_index_preserves_null_distinctness(nulls_not_distinct):
    metadata = MetaData()
    Table("environments", metadata, Column("id", String(36), primary_key=True),
          Column("token", String(255), nullable=True, unique=True, index=True))
    reflection = Reflection(metadata)
    index = reflection.tables["environments"]["indexes"][0]
    if nulls_not_distinct is not None:
        index["dialect_options"] = {"postgresql_nulls_not_distinct": nulls_not_distinct}
    if nulls_not_distinct:
        with pytest.raises(initializer.IncompatibleSchema, match="required indexes differ"):
            initializer.plan_schema(reflection, metadata, "ats", DIALECT)
    else:
        assert initializer.plan_schema(reflection, metadata, "ats", DIALECT)["createTables"] == []


@pytest.mark.parametrize("kind", ["table", "view"])
def test_non_ats_relations_are_refused(metadata, kind):
    reflection = Reflection(metadata)
    if kind == "table":
        reflection.tables["unrelated"] = {}
    else:
        reflection.views = ["unrelated"]
    with pytest.raises(initializer.IncompatibleSchema, match="Unexpected"):
        initializer.plan_schema(reflection, metadata, "ats", DIALECT)


class Connection:
    dialect = DIALECT

    def __init__(self):
        self.statements = []
        self.committed = False
        self.rolled_back = False
        self.unvalidated = []

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        pass

    def begin(self):
        connection = self

        class Transaction:
            def __enter__(self):
                return self

            def __exit__(self, kind, *_args):
                connection.rolled_back = kind is not None
                connection.committed = kind is None

        return Transaction()

    def execute(self, statement, params=None):
        self.statements.append((str(statement), params))
        return SimpleNamespace(scalars=lambda: SimpleNamespace(all=lambda: self.unvalidated))

    exec_driver_sql = execute

    def execution_options(self, **kwargs):
        assert kwargs == {"schema_translate_map": {None: "ats"}}
        return self


def fake_engine(connection):
    return SimpleNamespace(dialect=connection.dialect, connect=lambda: connection)


def test_plan_is_read_only_and_never_creates_objects(metadata, monkeypatch):
    connection = Connection()
    reflection = Reflection(metadata, exists=False, names=[])
    monkeypatch.setattr(initializer, "inspect", lambda _connection: reflection)
    monkeypatch.setattr(metadata, "create_all", lambda *_args, **_kwargs: pytest.fail("Preview wrote schema"))
    plan = initializer.initialize(connection_engine=fake_engine(connection), metadata=metadata)
    assert not plan["applied"] and plan["createTables"] == ["jobs", "users"]
    statements = [sql for sql, _params in connection.statements]
    assert statements[0] == "SET TRANSACTION READ ONLY"
    assert not any(sql.startswith(("CREATE", "ALTER", "DROP", "INSERT", "UPDATE", "DELETE", "LOCK")) for sql in statements)


def test_apply_creates_missing_tables_in_one_transaction_after_validation(metadata, monkeypatch):
    connection = Connection()
    before = Reflection(metadata, exists=False, names=[])
    after = Reflection(metadata)
    inspections = iter([before, after])
    monkeypatch.setattr(initializer, "inspect", lambda _connection: next(inspections))
    writes = []

    def create(bind, *, tables, checkfirst):
        assert bind is connection and not checkfirst
        assert not connection.committed
        writes.extend(table.name for table in tables)

    monkeypatch.setattr(metadata, "create_all", create)
    plan = initializer.initialize(True, connection_engine=fake_engine(connection), metadata=metadata)
    assert plan["applied"] and sorted(writes) == ["jobs", "users"]
    assert connection.committed and not connection.rolled_back
    sql = [statement for statement, _params in connection.statements]
    assert "CREATE SCHEMA ats" in sql
    assert any("pg_advisory_xact_lock" in statement for statement in sql)


@pytest.mark.parametrize("failure", ["incompatible", "unvalidated", "post_create"])
def test_apply_fails_closed_and_rolls_back(metadata, monkeypatch, failure):
    connection = Connection()
    before = Reflection(metadata)
    if failure == "incompatible":
        before.tables["users"]["columns"][0]["nullable"] = True
    elif failure == "unvalidated":
        connection.unvalidated = ["not_valid_fk"]
    else:
        before = Reflection(metadata, exists=False, names=[])
    monkeypatch.setattr(initializer, "inspect", lambda _connection: before)
    writes = []
    monkeypatch.setattr(metadata, "create_all", lambda *_args, **_kwargs: writes.append("create"))
    with pytest.raises(initializer.IncompatibleSchema):
        initializer.initialize(True, connection_engine=fake_engine(connection), metadata=metadata)
    assert connection.rolled_back and not connection.committed
    assert writes == (["create"] if failure == "post_create" else [])


def test_other_database_engine_rejected_before_connection(metadata):
    engine = SimpleNamespace(dialect=SimpleNamespace(name="sqlite"), connect=lambda: pytest.fail("connected"))
    with pytest.raises(ValueError, match="Only PostgreSQL"):
        initializer.initialize(connection_engine=engine, metadata=metadata)


@pytest.mark.parametrize("error_type", [RuntimeError, ValueError])
def test_cli_suppresses_driver_exception_details(monkeypatch, capsys, error_type):
    def fail(*_args, **_kwargs):
        raise error_type("postgresql://secret-password@example.test/database")

    monkeypatch.setattr(initializer, "initialize", fail)
    monkeypatch.setenv("DATABASE_SCHEMA", "ats")
    assert initializer.main([]) == 1
    captured = capsys.readouterr()
    assert "secret-password" not in captured.err and "example.test" not in captured.err


def test_cli_selects_dedicated_schema_before_backend_import(monkeypatch, capsys):
    import os

    monkeypatch.delenv("DATABASE_SCHEMA", raising=False)

    def initialize(apply, *, schema):
        assert not apply and schema == "ats" and os.environ["DATABASE_SCHEMA"] == "ats"
        return {"schema": schema, "applied": False}

    monkeypatch.setattr(initializer, "initialize", initialize)
    assert initializer.main([]) == 0
    assert '"schema": "ats"' in capsys.readouterr().out
