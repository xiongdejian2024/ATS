"""计划组执行策略、冻结的成员批次及报告分享。"""
from sqlalchemy import Column, String, JSON, Boolean, Float, DateTime, ForeignKey, Integer
from database import Base
from models.base import BaseModel


class PlanGroupPolicy(Base):
    __tablename__ = "plan_group_policies"
    group_id = Column(String(36), ForeignKey("plan_groups.id", ondelete="CASCADE"), primary_key=True)
    execution_mode = Column(String(20), nullable=False, default="serial")
    stop_on_failure = Column(Boolean, nullable=False, default=False)
    pass_threshold = Column(Float, nullable=False, default=100)
    plan_order = Column(JSON, nullable=False, default=list)


class PlanGroupRun(Base, BaseModel):
    __tablename__ = "plan_group_runs"
    # 组删除后保留历史批次及报告中的原组标识。
    group_id = Column(String(36), nullable=False, index=True)
    active_group_id = Column(String(36), nullable=True, unique=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False, index=True)
    group_name = Column(String(100), nullable=False)
    executor_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    idempotency_key = Column(String(200), nullable=True, unique=True)
    status = Column(String(30), nullable=False, default="queued", index=True)
    config_snapshot = Column(JSON, nullable=False)
    report = Column(JSON, nullable=True)
    summary = Column(JSON, nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)


class PlanGroupRunChild(Base):
    __tablename__ = "plan_group_run_children"
    run_id = Column(String(36), ForeignKey("plan_group_runs.id", ondelete="CASCADE"), primary_key=True)
    plan_run_id = Column(String(36), ForeignKey("plan_runs.id"), primary_key=True)
    sequence = Column(Integer, nullable=False)


class PlanGroupShare(Base, BaseModel):
    __tablename__ = "plan_group_shares"
    run_id = Column(String(36), ForeignKey("plan_group_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = Column(String(64), nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, nullable=False, default=False)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
