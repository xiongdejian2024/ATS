"""测试计划分组、策略与不可覆盖的执行批次。"""
import uuid
from sqlalchemy import Column, String, Text, Boolean, Integer, Float, JSON, ForeignKey, DateTime, func
from database import Base
from models.base import BaseModel


class PlanGroup(Base, BaseModel):
    __tablename__ = "plan_groups"
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)


class PlanSettings(Base):
    __tablename__ = "plan_settings"
    plan_id = Column(String(36), ForeignKey("test_plans.id", ondelete="CASCADE"), primary_key=True)
    group_id = Column(String(36), ForeignKey("plan_groups.id", ondelete="SET NULL"), nullable=True)
    execution_mode = Column(String(20), nullable=False, default="serial")
    stop_on_failure = Column(Boolean, nullable=False, default=False)
    pass_threshold = Column(Float, nullable=False, default=100)
    suite_order = Column(JSON, nullable=False, default=list)


class PlanRun(Base, BaseModel):
    __tablename__ = "plan_runs"
    plan_id = Column(String(36), ForeignKey("test_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    executor_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    idempotency_key = Column(String(180), nullable=True, unique=True)
    status = Column(String(20), nullable=False, default="queued", index=True)
    plan_name = Column(String(255), nullable=False)
    config_snapshot = Column(JSON, nullable=False)
    case_snapshot = Column(JSON, nullable=False)
    manual_results = Column(JSON, nullable=False, default=dict)
    manual_revision = Column(Integer, nullable=False, default=0)
    notes = Column(Text)
    report = Column(JSON, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)


class PlanRunItem(Base, BaseModel):
    __tablename__ = "plan_run_items"
    run_id = Column(String(36), ForeignKey("plan_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    suite_id = Column(String(36), ForeignKey("test_suites.id", ondelete="CASCADE"), nullable=False, index=True)
    execution_id = Column(String(36), nullable=False, unique=True)
    environment_id = Column(String(36), ForeignKey("environments.id"), nullable=False)
    sequence = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, default="waiting", index=True)
    suite_snapshot = Column(JSON, nullable=False)
    error_message = Column(Text)
    delivery_state = Column(String(30), nullable=False, default="queued")
    dispatch_attempted_at = Column(DateTime(timezone=True), nullable=True)
