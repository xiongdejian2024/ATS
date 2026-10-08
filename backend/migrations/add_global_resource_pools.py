"""Preview/apply three missing independent-pool tables; preserve existing data."""


def upgrade(engine, *, apply=False):
    from sqlalchemy import inspect
    from database import Base
    from models.global_resource_pool import (
        GlobalResourcePool,
        GlobalResourcePoolProject,
        GlobalResourcePoolMember,
    )

    if engine.dialect.name not in {"sqlite", "mysql", "postgresql"}:
        raise ValueError("Unsupported ATS database dialect")
    inspector = inspect(engine)
    if not all(
        inspector.has_table(name) for name in ["users", "projects", "environments"]
    ):
        raise ValueError("Create/upgrade existing ATS parent tables first")
    missing = []
    for table in [
        GlobalResourcePool.__table__,
        GlobalResourcePoolProject.__table__,
        GlobalResourcePoolMember.__table__,
    ]:
        if not inspector.has_table(table.name):
            missing.append(table)
        elif not set(table.columns.keys()) <= {
            column["name"] for column in inspector.get_columns(table.name)
        }:
            raise ValueError(
                "Incompatible existing resource-pool table; no objects changed"
            )
    if apply:
        Base.metadata.create_all(engine, tables=missing, checkfirst=True)
    return [table.name for table in missing]
