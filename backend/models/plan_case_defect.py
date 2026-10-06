"""计划关联实例的缺陷绑定；取消用例关联后保留身份快照。"""
from sqlalchemy import Column, String, JSON, Boolean, ForeignKey, UniqueConstraint
from database import Base
from models.base import BaseModel


class PlanCaseDefect(Base, BaseModel):
    __tablename__ = 'plan_case_defects'
    __table_args__ = (UniqueConstraint('plan_id', 'association_key', 'issue_id', name='uq_plan_case_defect_binding'),)
    plan_id = Column(String(36), ForeignKey('test_plans.id', ondelete='CASCADE'), nullable=False, index=True)
    association_key = Column(String(120), nullable=False, index=True)
    issue_id = Column(String(36), ForeignKey('case_issues.id', ondelete='CASCADE'), nullable=False, index=True)
    case_id = Column(String(36), ForeignKey('test_cases.id', ondelete='SET NULL'), nullable=True)
    case_snapshot = Column(JSON, nullable=False)
    create_request_id = Column(String(36), nullable=True, index=True)
    create_payload_hash = Column(String(64), nullable=True)
    active = Column(Boolean, nullable=False, default=True)
    created_by = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    updated_by = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
