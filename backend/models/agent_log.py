"""Durable Agent log replay cursor and raw logs for direct (non-suite) tasks."""

from sqlalchemy import Column, String, BigInteger, DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.mysql import LONGTEXT
from database import Base


class AgentLogCursor(Base):
    __tablename__ = "agent_log_cursors"
    id = Column(String(36), primary_key=True)
    environment_id = Column(
        String(36),
        ForeignKey("environments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    stream_id = Column(String(36), nullable=False)
    through_sequence = Column(BigInteger, nullable=False, default=0)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class AgentTaskLog(Base):
    __tablename__ = "agent_task_logs"
    id = Column(String(36), primary_key=True)
    environment_id = Column(
        String(36),
        ForeignKey("environments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    task_id = Column(String(255), nullable=False, index=True)
    message = Column(Text().with_variant(LONGTEXT(), "mysql"), nullable=False)
    timestamp = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
