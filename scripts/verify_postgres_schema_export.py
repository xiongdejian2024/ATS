"""Verify the DDL only in a fresh loopback ats_pg_export_regression database.

Does not create roles, remove objects, or accept production connection settings.
Use a separate disposable PostgreSQL instance; this command creates synthetic rows.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import DBAPIError

from export_postgres_schema import DEFAULT_OUTPUT, load_metadata, render_schema
from init_postgres import initialize


def outside_snapshot(connection):
    # Unrelated catalog definitions and ACLs must be byte-for-byte unchanged.
    # PostgreSQL necessarily creates pg_toast storage/indexes owned by ats
    # tables; those are ATS implementation objects, not unrelated relations.
    # Relation sizes/statistics can change as PostgreSQL maintains catalogs.
    namespaces = connection.exec_driver_sql("""
        SELECT oid, nspname, nspowner, nspacl::text FROM pg_catalog.pg_namespace
        WHERE nspname <> 'ats' ORDER BY oid
    """).all()
    relations = connection.exec_driver_sql("""
        SELECT c.oid, n.nspname, c.relname, c.relkind, c.relowner, c.relacl::text
        FROM pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace
        WHERE n.nspname <> 'ats' AND c.oid NOT IN (
            SELECT t.reltoastrelid FROM pg_catalog.pg_class t
            JOIN pg_catalog.pg_namespace ns ON ns.oid=t.relnamespace
            WHERE ns.nspname='ats'
            UNION ALL
            SELECT i.indexrelid FROM pg_catalog.pg_index i
            JOIN pg_catalog.pg_class t ON t.reltoastrelid=i.indrelid
            JOIN pg_catalog.pg_namespace ns ON ns.oid=t.relnamespace
            WHERE ns.nspname='ats'
        ) ORDER BY c.oid
    """).all()
    return namespaces, relations


def expect_failure(connection, statement, sqlstate):
    try:
        connection.exec_driver_sql(statement)
    except DBAPIError as exc:
        assert exc.orig.sqlstate == sqlstate, (type(exc.orig).__name__, exc.orig.sqlstate)
    else:
        raise AssertionError(f"Expected PostgreSQL error {sqlstate}")


def verify(url):
    parsed = make_url(url)
    if (parsed.drivername != "postgresql+psycopg"
            or parsed.host != "127.0.0.1" or parsed.port != 15433
            or parsed.database != "ats_pg_export_regression"
            or parsed.username != "agent" or parsed.password or parsed.query
            or any(name.startswith("PG") for name in os.environ)):
        raise ValueError("Only the separate loopback agent@127.0.0.1:15433/ats_pg_export_regression instance is allowed.")
    metadata = load_metadata()
    ddl = DEFAULT_OUTPUT.read_text(encoding="utf-8")
    assert ddl == render_schema(metadata), "Regenerate and review the checked-in DDL first"
    engine = create_engine(parsed, connect_args={"connect_timeout": 5})
    try:
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            assert connection.exec_driver_sql("SHOW server_version_num").scalar_one() == "170011"
            assert not inspect(connection).has_schema("ats"), "Refusing a previously initialized test database"
            baseline = outside_snapshot(connection)
            # An error after all generated DDL proves atomic rollback in autocommit.
            failure_ddl = ddl.replace("\nEND\n$ats_fresh_schema$;", "\nRAISE EXCEPTION 'synthetic rollback probe';\nEND\n$ats_fresh_schema$;")
            assert failure_ddl != ddl
            expect_failure(connection, failure_ddl, "P0001")
            assert not inspect(connection).has_schema("ats")
            assert outside_snapshot(connection) == baseline

        # Prove the block does not commit its caller's surrounding transaction.
        with engine.connect() as connection:
            transaction = connection.begin()
            connection.exec_driver_sql(ddl)
            assert len(inspect(connection).get_table_names(schema="ats")) == 87
            transaction.rollback()
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            assert not inspect(connection).has_schema("ats")
            connection.exec_driver_sql(ddl)
            assert outside_snapshot(connection) == baseline

        plan = initialize(False, schema="ats", connection_engine=engine, metadata=metadata)
        assert plan["expectedTableCount"] == 87 and len(plan["existingTables"]) == 87
        assert not plan["createSchema"] and plan["createTables"] == []
        index_count = comment_count = 0
        with engine.connect() as connection:
            inspector = inspect(connection)
            for table in metadata.tables.values():
                actual_indexes = {
                    item["name"] for item in inspector.get_indexes(table.name, schema="ats")
                    if not item.get("duplicates_constraint")
                }
                assert actual_indexes == {index.name for index in table.indexes}, table.name
                index_count += len(actual_indexes)
                assert inspector.get_table_comment(table.name, schema="ats")["text"] == table.comment
                comment_count += table.comment is not None
                columns = {item["name"]: item for item in inspector.get_columns(table.name, schema="ats")}
                for column in table.columns:
                    assert columns[column.name].get("comment") == column.comment
                    comment_count += column.comment is not None
            assert connection.exec_driver_sql("SELECT pg_catalog.pg_get_serial_sequence('ats.review_workspaces', 'number')").scalar_one() == "ats.review_workspaces_number_seq"
            assert connection.exec_driver_sql("""
                SELECT count(*) FROM pg_catalog.pg_class c
                JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace
                JOIN pg_catalog.pg_depend d ON d.objid=c.oid AND d.deptype='a'
                WHERE n.nspname='ats' AND c.relkind='S'
            """).scalar_one() == 1

        with engine.begin() as connection:
            scoped = connection.execution_options(schema_translate_map={None: "ats"})

            def insert(table, **values):
                return scoped.execute(metadata.tables[table].insert().values(**values))

            insert("users", id="sentinel", username="synthetic", email="synthetic@test.invalid", password_hash="synthetic-only")
            insert("projects", id="project", name="Synthetic", owner_id="sentinel")
            insert("environments", id="environment", name="Synthetic")
            insert("test_plans", id="plan", project_id="project", plan_number="SYNTHETIC", name="Synthetic", owner_id="sentinel")
            insert("test_suites", id="suite", plan_id="plan", name="Synthetic", environment_id="environment", execution_command="synthetic", case_ids=[], created_by="sentinel")
            now = datetime.now(timezone.utc)
            insert("script_jobs", id="job", project_id="project", name="Synthetic", environment_id="environment", config={}, created_by="sentinel", updated_by="sentinel", created_at=now, updated_at=now)
            for number in range(2):
                insert("case_reviews", id=f"review-{number}", project_id="project", name="Synthetic", reviewer_ids=[], created_by="sentinel")
                result = insert("review_workspaces", review_id=f"review-{number}")
                assert result.inserted_primary_key == (number + 1,)
            insert("agent_log_cursors", id="cursor", environment_id="environment", stream_id="synthetic", through_sequence=2**40)
            insert("agent_task_logs", id="log", environment_id="environment", task_id="task", message="raw\nsynthetic log")
            # Omit kind to exercise its actual database server default.
            connection.exec_driver_sql("""
                INSERT INTO ats.task_queue
                (id,environment_id,suite_id,execution_id,executor_id,status,priority)
                VALUES ('suite-queue','environment','suite','suite-exec','sentinel','pending',0)
            """)
            insert("task_queue", id="script-queue", environment_id="environment", kind="script", script_job_id="job", execution_id="script-exec", executor_id="sentinel")

        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            assert connection.exec_driver_sql("SELECT kind FROM ats.task_queue WHERE id='suite-queue'").scalar_one() == "suite"
            for update in (
                "kind='script'", "suite_id=NULL", "script_job_id='job'", "kind='unknown'"
            ):
                expect_failure(connection, f"UPDATE ats.task_queue SET {update} WHERE id='suite-queue'", "23514")
            expect_failure(connection, "UPDATE ats.task_queue SET script_job_id='missing' WHERE id='script-queue'", "23503")
            expect_failure(connection, "UPDATE ats.agent_log_cursors SET environment_id='missing' WHERE id='cursor'", "23503")
            assert connection.exec_driver_sql("SELECT through_sequence FROM ats.agent_log_cursors WHERE id='cursor'").scalar_one() == 2**40
            assert connection.exec_driver_sql("SELECT updated_at IS NOT NULL FROM ats.agent_log_cursors WHERE id='cursor'").scalar_one()
            expect_failure(connection, ddl, "42P06")
            assert connection.exec_driver_sql("SELECT id FROM ats.users").scalar_one() == "sentinel"
            assert connection.exec_driver_sql("SELECT count(*) FROM ats.task_queue").scalar_one() == 2
            assert len(inspect(connection).get_table_names(schema="ats")) == 87
            assert outside_snapshot(connection) == baseline

        final_plan = initialize(False, schema="ats", connection_engine=engine, metadata=metadata)
        assert final_plan["createTables"] == []
        return {
            "postgresVersion": "17.11", "schema": "ats", "tables": 87,
            "modelIndexes": index_count, "modelComments": comment_count,
            "ownedSerialSequences": 1,
            "ddlSha256": hashlib.sha256(ddl.encode("utf-8")).hexdigest(),
            "checks": ["full initializer reflection", "exact index names", "all comments",
                       "autocommit failure rollback", "caller transaction rollback",
                       "generated serial values", "suite and script queue constraints",
                       "BIGINT cursor and server defaults", "foreign key enforcement",
                       "existing schema refusal preserves sentinel", "other schemas and relations unchanged"],
        }
    finally:
        engine.dispose()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database-url", required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.database_url), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
