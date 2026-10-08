"""Preview/add a single sidecar; leave existing environment rows and grants intact."""

from sqlalchemy import inspect


def upgrade(engine, *, apply=False):
    from database import Base
    from models.native_environment_variables import NativeEnvironmentVariables

    inspector = inspect(engine)
    if engine.dialect.name not in {"sqlite", "mysql", "postgresql"}:
        raise ValueError("Unsupported ATS database dialect")
    if not inspector.has_table("native_api_environments"):
        raise ValueError("Create/upgrade ATS environment parent first")
    table = NativeEnvironmentVariables.__table__
    if inspector.has_table(table.name):
        if not set(table.columns.keys()) <= {
            c["name"] for c in inspector.get_columns(table.name)
        }:
            raise ValueError("Incompatible variable sidecar; no objects changed")
        return []
    if apply:
        Base.metadata.create_all(engine, tables=[table], checkfirst=True)
    return [table.name]
