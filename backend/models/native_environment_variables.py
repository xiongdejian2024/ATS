"""Additive environment declarations; the parent revision controls edits."""

from sqlalchemy import Column, String, JSON, ForeignKey
from database import Base


class NativeEnvironmentVariables(Base):
    __tablename__ = "native_environment_variables"
    environment_id = Column(
        String(36),
        ForeignKey("native_api_environments.id", ondelete="CASCADE"),
        primary_key=True,
    )
    variables = Column(JSON, nullable=False, default=list)
