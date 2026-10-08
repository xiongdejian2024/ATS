"""Plan or initialize ATS tables in a dedicated PostgreSQL schema.

The default is a read-only inspection. --apply only creates the selected schema
and missing tables after every existing table passes the compatibility checks.
Existing tables, rows, permissions, and Supabase-managed schemas are not changed.
"""

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

from sqlalchemy import CheckConstraint, ForeignKeyConstraint, UniqueConstraint, inspect, text
from sqlalchemy.schema import CreateSchema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

RESERVED_SCHEMAS = {
    "public", "auth", "storage", "information_schema", "extensions", "realtime",
    "supabase_functions", "supabase_migrations", "vault", "graphql", "graphql_public",
    "net", "cron",
}


class IncompatibleSchema(RuntimeError):
    """Initialization cannot safely add tables to the existing schema."""


class InitializerConfigurationError(ValueError):
    """A safe-to-display validation error produced by this tool itself."""


def validate_schema_name(schema):
    if (
        not isinstance(schema, str)
        or re.fullmatch(r"[a-z][a-z0-9_]{0,62}", schema) is None
        or schema in RESERVED_SCHEMAS
        or schema.startswith("pg_")
    ):
        raise InitializerConfigurationError("Use a dedicated lowercase ATS schema, such as ats; managed schemas are forbidden.")
    return schema


def _type_name(column_type, dialect):
    value = column_type.compile(dialect=dialect).upper()
    # PostgreSQL's unqualified FLOAT is reflected as DOUBLE PRECISION.
    return "DOUBLE PRECISION" if value == "FLOAT" else value


def _default_text(value):
    if value is None:
        return None
    return re.sub(r"::(?:character varying|text)\b", "", str(value)).strip()


def _expected_default(column, dialect):
    if column.server_default is None:
        return None
    value = column.server_default.arg
    if isinstance(value, str):
        return column.type.literal_processor(dialect)(value)
    return str(value.compile(dialect=dialect))


def _check_expression(value):
    """Normalize reflected parentheses/casts without dropping Boolean grouping.

    ATS currently has a simple AND/OR check on task_queue. Unknown forms remain
    conservative text comparisons instead of guessing that they are equivalent.
    """
    value = _default_text(value)
    value = re.sub(r'"([a-z][a-z0-9_]*)"', r"\1", value)

    def outer(expression):
        while expression.startswith("(") and expression.endswith(")"):
            depth, quoted = 0, False
            for index, char in enumerate(expression):
                if char == "'":
                    quoted = not quoted
                if not quoted:
                    depth += (char == "(") - (char == ")")
                    if depth == 0:
                        break
            if index != len(expression) - 1:
                break
            expression = expression[1:-1].strip()
        return expression

    def split(expression, operator):
        parts, start, depth, quoted = [], 0, 0, False
        marker = f" {operator} "
        for index, char in enumerate(expression):
            if char == "'":
                quoted = not quoted
            if not quoted:
                depth += (char == "(") - (char == ")")
                if depth == 0 and expression[index:index + len(marker)].upper() == marker:
                    parts.append(expression[start:index].strip())
                    start = index + len(marker)
        return parts + [expression[start:].strip()] if parts else None

    def normalize(expression):
        expression = outer(expression.strip())
        for operator in ("OR", "AND"):
            parts = split(expression, operator)
            if parts:
                return (operator, tuple(normalize(part) for part in parts))
        expression = re.sub(r"\(([a-z][a-z0-9_]*)\)", r"\1", expression)
        return re.sub(r"\s+", " ", expression).strip()

    return normalize(value)


def _fk_signature(constraint, schema):
    options = constraint.get("options", {})
    return (
        tuple(constraint["constrained_columns"]),
        constraint.get("referred_schema") or schema,
        constraint["referred_table"],
        tuple(constraint["referred_columns"]),
        options.get("ondelete") or "NO ACTION",
        options.get("onupdate") or "NO ACTION",
        bool(options.get("deferrable")),
        options.get("initially") or "IMMEDIATE",
    )


def _plain_index(index):
    options = index.get("dialect_options", {})
    return (
        tuple(index["column_names"]),
        bool(index.get("unique")),
        options.get("postgresql_where") is None
        and options.get("postgresql_using", "btree") == "btree"
        and not options.get("postgresql_nulls_not_distinct", False)
        and not index.get("column_sorting")
        and all(name is not None for name in index["column_names"]),
    )


def table_issues(inspector, table, schema, dialect):
    """Inspect structure only; never read or rewrite an application's rows."""
    issues = []
    columns = {column["name"]: column for column in inspector.get_columns(table.name, schema=schema)}
    if set(columns) != set(table.c.keys()):
        issues.append("column names differ")
    for column in table.c:
        actual = columns.get(column.name)
        if actual is None:
            continue
        if (_type_name(actual["type"], dialect) != _type_name(column.type, dialect)
                or actual["nullable"] != column.nullable):
            issues.append(f"column {column.name} type/nullability differs")
        default = _default_text(actual.get("default"))
        if column is table.autoincrement_column:
            sequence = f"{table.name}_{column.name}_seq"
            allowed = {
                f"nextval('{sequence}'::regclass)",
                f"nextval('{schema}.{sequence}'::regclass)",
                f"nextval('\"{schema}\".{sequence}'::regclass)",
                f"nextval('\"{schema}\".\"{sequence}\"'::regclass)",
            }
            if not actual.get("identity") and default not in allowed:
                issues.append(f"column {column.name} lacks its generated sequence")
            if (actual.get("identity") or {}).get("always"):
                issues.append(f"column {column.name} rejects explicit generated IDs")
        elif default != _default_text(_expected_default(column, dialect)):
            issues.append(f"column {column.name} server default differs")
        elif actual.get("identity"):
            issues.append(f"column {column.name} is unexpectedly generated")
        if actual.get("computed"):
            issues.append(f"column {column.name} is unexpectedly computed")
    primary = inspector.get_pk_constraint(table.name, schema=schema)["constrained_columns"]
    if primary != [column.name for column in table.primary_key.columns]:
        issues.append("primary key differs")
    expected_unique = {
        tuple(column.name for column in constraint.columns)
        for constraint in table.constraints if isinstance(constraint, UniqueConstraint)
    }
    unique_constraints = inspector.get_unique_constraints(table.name, schema=schema)
    actual_unique = {
        tuple(constraint["column_names"])
        for constraint in unique_constraints
    }
    if expected_unique != actual_unique:
        issues.append("unique constraints differ")
    if any(constraint.get("dialect_options", {}).get("postgresql_nulls_not_distinct")
           for constraint in unique_constraints):
        issues.append("unique constraint NULL semantics differ")
    expected_fks = set()
    for constraint in table.constraints:
        if isinstance(constraint, ForeignKeyConstraint):
            expected_fks.add((
                tuple(constraint.column_keys), schema,
                constraint.elements[0].column.table.name,
                tuple(fk.column.name for fk in constraint.elements),
                constraint.ondelete or "NO ACTION", constraint.onupdate or "NO ACTION",
                bool(constraint.deferrable), constraint.initially or "IMMEDIATE",
            ))
    actual_fks = {
        _fk_signature(constraint, schema)
        for constraint in inspector.get_foreign_keys(
            table.name, schema=schema, postgresql_ignore_search_path=True
        )
    }
    if expected_fks != actual_fks:
        issues.append("foreign keys differ")
    indexes = inspector.get_indexes(table.name, schema=schema)
    actual_indexes = {_plain_index(index) for index in indexes}
    expected_indexes = {
        (tuple(column.name for column in index.columns), bool(index.unique), True)
        for index in table.indexes
    }
    if not expected_indexes.issubset(actual_indexes):
        issues.append("required indexes differ or are missing")
    if any(index.get("unique") and not index.get("duplicates_constraint")
           and _plain_index(index) not in expected_indexes for index in indexes):
        issues.append("unexpected unique index")
    expected_checks = {
        _check_expression(str(constraint.sqltext))
        for constraint in table.constraints if isinstance(constraint, CheckConstraint)
    }
    actual_checks = {
        _check_expression(constraint["sqltext"])
        for constraint in inspector.get_check_constraints(table.name, schema=schema)
    }
    if expected_checks != actual_checks:
        issues.append("check constraints differ")
    return [f"{table.name}: {issue}" for issue in issues]


def plan_schema(inspector, metadata, schema, dialect):
    validate_schema_name(schema)
    if dialect.name != "postgresql":
        raise InitializerConfigurationError("Only PostgreSQL is supported by this initializer.")
    if any(table.schema is not None for table in metadata.tables.values()):
        raise InitializerConfigurationError("ATS metadata must not target another schema.")
    exists = inspector.has_schema(schema)
    existing = set(inspector.get_table_names(schema=schema)) if exists else set()
    expected = set(metadata.tables)
    issues = [f"Unexpected table: {name}" for name in sorted(existing - expected)]
    if exists:
        other_relations = (
            inspector.get_view_names(schema=schema)
            + inspector.get_materialized_view_names(schema=schema)
            + inspector.get_foreign_table_names(schema=schema)
        )
        issues.extend(f"Unexpected view/foreign table: {name}" for name in sorted(other_relations))
    for name in sorted(existing & expected):
        issues.extend(table_issues(inspector, metadata.tables[name], schema, dialect))
    if issues:
        raise IncompatibleSchema("Existing schema is incompatible; no changes were applied:\n" + "\n".join(issues))
    return {
        "schema": schema,
        "createSchema": not exists,
        "expectedTableCount": len(expected),
        "existingTables": sorted(existing),
        "createTables": sorted(expected - existing),
    }


def initialize(apply=False, *, schema="ats", connection_engine=None, metadata=None):
    validate_schema_name(schema)
    if connection_engine is None or metadata is None:
        from database import Base, engine
        import models  # noqa: F401: registers the complete ATS metadata
        connection_engine = connection_engine if connection_engine is not None else engine
        metadata = metadata if metadata is not None else Base.metadata
    if connection_engine.dialect.name != "postgresql":
        raise InitializerConfigurationError("Only PostgreSQL is supported by this initializer.")
    with connection_engine.connect() as connection, connection.begin():
        if not apply:
            connection.exec_driver_sql("SET TRANSACTION READ ONLY")
        connection.execute(text("SELECT pg_catalog.set_config('search_path', :path, true)"), {"path": f'"{schema}"'})
        connection.execute(text("SELECT pg_catalog.set_config('lock_timeout', '10s', true)"))
        if apply:
            key = int.from_bytes(hashlib.sha256(f"ats:init:{schema}".encode()).digest()[:8], "big", signed=True)
            connection.execute(text("SELECT pg_catalog.pg_advisory_xact_lock(:key)"), {"key": key})
        inspector = inspect(connection)
        if apply and inspector.has_schema(schema):
            quote = connection.dialect.identifier_preparer.quote
            for name in sorted(set(inspector.get_table_names(schema=schema)) & set(metadata.tables)):
                connection.exec_driver_sql(f"LOCK TABLE {quote(schema)}.{quote(name)} IN ACCESS SHARE MODE")
        plan = plan_schema(inspector, metadata, schema, connection.dialect)
        unvalidated = connection.execute(text("""
            SELECT c.conname FROM pg_catalog.pg_constraint AS c
            JOIN pg_catalog.pg_class AS t ON t.oid = c.conrelid
            JOIN pg_catalog.pg_namespace AS n ON n.oid = t.relnamespace
            WHERE n.nspname = :schema AND (NOT c.convalidated OR c.condeferrable)
        """), {"schema": schema}).scalars().all()
        if unvalidated:
            raise IncompatibleSchema("Existing schema has unvalidated/deferred constraints; no changes were applied.")
        if apply:
            if plan["createSchema"]:
                connection.execute(CreateSchema(schema))
            metadata.create_all(
                connection.execution_options(schema_translate_map={None: schema}),
                tables=[metadata.tables[name] for name in plan["createTables"]],
                checkfirst=False,
            )
            verified = plan_schema(inspect(connection), metadata, schema, connection.dialect)
            if verified["createSchema"] or verified["createTables"]:
                raise IncompatibleSchema("Post-create validation failed; initialization was rolled back.")
        return {**plan, "applied": bool(apply)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", default=os.environ.get("DATABASE_SCHEMA") or "ats",
                        help="Dedicated ATS schema (default: DATABASE_SCHEMA or ats).")
    parser.add_argument("--apply", action="store_true", help="Create schema/missing tables after validation.")
    args = parser.parse_args(argv)
    try:
        # CLI selection must be known before database.py validates PG startup.
        # This changes only this command's environment, not the caller's shell.
        os.environ["DATABASE_SCHEMA"] = validate_schema_name(args.schema)
        result = initialize(args.apply, schema=args.schema)
    except (InitializerConfigurationError, IncompatibleSchema) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except Exception as exc:
        # Driver errors can contain credentials, addresses, or SQL parameters.
        print(f"Initialization failed ({type(exc).__name__}); transaction rolled back. Check PostgreSQL access and schema compatibility.", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
