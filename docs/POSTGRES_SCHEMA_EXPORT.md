# Fresh PostgreSQL schema export

`deploy/postgres_schema.sql` creates the original ATS controller's 89 model tables
in the fixed `ats` schema. It is a fresh initialization artifact, not an upgrade or
data migration. It refuses **any existing `ats` schema**, including an empty or
already compatible one, before creating a table. It does not create database roles,
passwords, extensions, or application users; insert data; issue grants; or drop or
replace existing objects.

The artifact preserves model column order, PostgreSQL types, nullability, primary
keys, unique/check/foreign-key constraints and delete actions, 215 model indexes
with their original names, 52 model comments, and all server defaults. The
`review_workspaces.number` SERIAL primary key creates the owned
`ats.review_workspaces_number_seq` sequence. Python-side defaults, UUID generation,
and ORM `onupdate` behavior remain in the controller, exactly as with
`scripts/init_postgres.py`; they are not converted into new database behavior.

## Atomic application

The entire file is **one PostgreSQL `DO` statement** containing static,
schema-qualified DDL. It has no transaction `BEGIN` or `COMMIT` commands. The
`BEGIN`/`END` inside the dollar-quoted body delimit a PL/pgSQL block, not a new
transaction. A failure anywhere rolls back the whole statement, including when
submitted in autocommit. If the caller already has a transaction, the statement
participates in that transaction and cannot commit it.

For an approved Supabase admin `apply_migration`, submit the complete file unchanged
as the query. Do not split it at semicolons or strip the `DO` block. It requires the
standard PostgreSQL `plpgsql` language and permission to create the dedicated
schema. No Supabase operation is performed by the generator or the tests.

For an operator's existing PostgreSQL connection, either ordinary `psql -f` or
`psql --single-transaction -f` works. Use `-v ON_ERROR_STOP=1` so an existing schema
or another error is reported as failure. Keep connection credentials outside the
file and command history. Read-only post-application inspection uses:

```bash
python scripts/init_postgres.py --schema ats
```

Roles, credentials, access grants, and Supabase API exposure are separate deployment
steps requiring their own authorization. PostgreSQL applies the executing owner's
existing default privileges to new objects; absence of `GRANT` statements is not an
audit of those pre-existing privileges. Keep ATS behind its controller and do not
expose this schema through the Supabase Data API. The export changes only `ats`
objects and their PostgreSQL-owned TOAST storage; it sets transaction-local
`search_path=pg_catalog` and `lock_timeout=10s` while executing.

## Deterministic offline generation

Run in a fresh Python process with SQLAlchemy installed (verified with 2.1.4):

```bash
python scripts/export_postgres_schema.py
python scripts/export_postgres_schema.py --check
sha256sum deploy/postgres_schema.sql
```

The generator imports the original models with an isolated declarative `Base`.
It does not import application settings, load `.env`, construct a database engine,
or open a network connection. `DATABASE_URL` and `DATABASE_SCHEMA` are ignored.
There is no schema-selection option. Model-count changes or already-qualified
source metadata require review. Tables, constraints, and indexes are ordered
deterministically, including across different Python hash seeds. `--check` verifies
the checked-in UTF-8 bytes without overwriting them. Use it after a model or
SQLAlchemy upgrade and review any regenerated DDL.

## Regression verification

Offline checks:

```bash
python -m pytest tests/test_postgres_ddl_export.py --noconftest -q -o addopts=''
```

For real PostgreSQL validation, start a fresh, disposable PostgreSQL 17.11 instance
bound only to `127.0.0.1:15433`, with no Unix socket, in a new data directory. Use the
local `agent` user and create the empty database `ats_pg_export_regression`. Then,
in the same execution invocation as the server startup, run:

```bash
python scripts/verify_postgres_schema_export.py \
  --database-url postgresql+psycopg://agent@127.0.0.1:15433/ats_pg_export_regression
```

The verifier refuses another host, port, username, database, query parameters,
passwords, any `PG*` environment overrides, a different PostgreSQL version, or an
existing `ats` schema. It creates synthetic rows and leaves the disposable database
intact. It does not run the main test suite's destructive database fixtures.

It checks complete initializer reflection; exact index names and comments; owned
serial values; suite/script queue checks and foreign keys; BIGINT cursors and
server defaults; rollback after a forced final error in autocommit; rollback of a
surrounding transaction; and a second application that refuses the existing schema
and preserves sentinel rows. It compares unrelated schema/relation definitions and
ACLs before and after. PostgreSQL's automatically created TOAST objects belonging
to ATS tables are included in ATS's storage, not treated as unrelated changes.
