"""Independent script definitions and immutable executions; never test cases."""
import uuid
from sqlalchemy import Column, String, Text, Integer, Float, JSON, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from database import Base


class ScriptJob(Base):
    __tablename__ = "script_jobs"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    environment_id = Column(String(36), ForeignKey("environments.id"), nullable=False)
    config = Column(JSON, nullable=False)
    revision = Column(Integer, nullable=False, default=1)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class ScriptJobRun(Base):
    __tablename__ = "script_job_runs"
    execution_id = Column(String(36), primary_key=True)
    job_id = Column(String(36), ForeignKey("script_jobs.id"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    environment_id = Column(String(36), ForeignKey("environments.id"), nullable=False)
    executor_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    request_id = Column(String(80), nullable=False, unique=True)
    config_snapshot = Column(JSON, nullable=False)
    delivery_state = Column(String(20), nullable=False, default="queued")
    dispatch_attempted_at = Column(DateTime, nullable=True)
    dispatch_session_id = Column(String(36), nullable=True)
    cancel_requested_at = Column(DateTime, nullable=True)
    result = Column(String(20), nullable=True)
    exit_code = Column(Integer, nullable=True)
    duration_seconds = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)
    log_delivery = Column(JSON, nullable=True)
    closed_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    closed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False)


class ScriptJobLog(Base):
    __tablename__ = "script_job_logs"
    id = Column(String(36), primary_key=True)
    script_job_id = Column(String(36), ForeignKey("script_jobs.id"), nullable=False, index=True)
    execution_id = Column(String(36), ForeignKey("script_job_runs.execution_id"), nullable=False, unique=True)
    message = Column(Text().with_variant(LONGTEXT(), "mysql"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
