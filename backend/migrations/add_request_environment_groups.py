"""Non-destructive two-table upgrade for an existing ATS database.

Pass the existing SQLAlchemy engine explicitly; this module does not load .env,
connect on import, alter existing rows/columns, or remove any table.
"""


def upgrade(engine, *, apply=False):
    from sqlalchemy import inspect
    from database import Base
    from models.request_environment_group import (
        RequestEnvironmentGroup,
        RequestEnvironmentMapping,
    )

    if engine.dialect.name not in {"sqlite", "postgresql", "mysql"}:
        raise ValueError("Unsupported ATS database dialect")
    inspector = inspect(engine)
    if not all(
        inspector.has_table(name)
        for name in ("users", "projects", "native_api_environments")
    ):
        raise ValueError("Create/upgrade the existing ATS parent schema first")
    tables = [RequestEnvironmentGroup.__table__, RequestEnvironmentMapping.__table__]
    missing = []
    for table in tables:
        if not inspector.has_table(table.name):
            missing.append(table)
        elif not set(table.columns.keys()) <= {
            column["name"] for column in inspector.get_columns(table.name)
        }:
            raise ValueError(
                "Existing environment-group table is incompatible; no objects changed"
            )
    if apply:
        Base.metadata.create_all(bind=engine, tables=missing, checkfirst=True)
    return [table.name for table in missing]
