"""Preview/add defect sidecars and permission definitions; no grants or data drops."""

from sqlalchemy import inspect, select


def upgrade(engine, *, apply=False):
    from database import Base
    from models.defect_workspace import (
        DefectTemplate,
        DefectProfile,
        DefectComment,
        DefectEvent,
    )
    from models import Permission
    from core.permissions import SYSTEM_PERMISSIONS

    inspector = inspect(engine)
    if engine.dialect.name not in {"sqlite", "mysql", "postgresql"}:
        raise ValueError("Unsupported ATS database dialect")
    if not all(
        inspector.has_table(t)
        for t in ["users", "projects", "case_issues", "permissions"]
    ):
        raise ValueError("Create/upgrade existing ATS parent tables first")
    tables = [
        DefectTemplate.__table__,
        DefectProfile.__table__,
        DefectComment.__table__,
        DefectEvent.__table__,
    ]
    missing = []
    for table in tables:
        if not inspector.has_table(table.name):
            missing.append(table)
        elif not set(table.columns.keys()) <= {
            c["name"] for c in inspector.get_columns(table.name)
        }:
            raise ValueError("Incompatible defect table; no objects changed")
    definitions = {
        code: name
        for code, name in SYSTEM_PERMISSIONS.items()
        if code.startswith("defect:")
    }
    with engine.connect() as conn:
        present = set(
            conn.execute(
                select(Permission.code).where(Permission.code.in_(definitions))
            ).scalars()
        )
    codes = sorted(set(definitions) - present)
    if apply:
        Base.metadata.create_all(engine, tables=missing, checkfirst=True)
        with engine.begin() as conn:
            for code in codes:
                resource, action = code.split(":", 1)
                conn.execute(
                    Permission.__table__.insert().values(
                        code=code,
                        name=definitions[code],
                        resource=resource,
                        action=action,
                        description="Independent defect authority",
                    )
                )
    return [t.name for t in missing] + ["permission:" + code for code in codes]
