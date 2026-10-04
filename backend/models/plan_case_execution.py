"""计划功能用例的独立手工执行历史；关联取消后保留快照。"""
from sqlalchemy import Column, String, Text, JSON, ForeignKey, UniqueConstraint, DateTime, func
from sqlalchemy.dialects.mysql import DATETIME
from database import Base
from models.base import BaseModel


class PlanCaseExecution(Base, BaseModel):
    __tablename__ = 'plan_case_executions'
    __table_args__ = (UniqueConstraint('plan_id', 'association_key', 'request_id', name='uq_plan_case_execution_request'),)
    created_at = Column(DateTime(timezone=True).with_variant(DATETIME(fsp=6), 'mysql'), server_default=func.now(), nullable=False)
    plan_id = Column(String(36), ForeignKey('test_plans.id', ondelete='CASCADE'), nullable=False, index=True)
    association_key = Column(String(120), nullable=False, index=True)
    case_id = Column(String(36), ForeignKey('test_cases.id', ondelete='SET NULL'), nullable=True)
    request_id = Column(String(36), nullable=False, index=True)
    payload_hash = Column(String(64), nullable=False)
    executor_id = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    executor_name = Column(String(100), nullable=False)
    result = Column(String(20), nullable=False)
    description = Column(Text, nullable=False, default='')
    step_results = Column(JSON, nullable=False, default=list)
    case_snapshot = Column(JSON, nullable=False)
