"""测试计划工作区扩展；新增表保留旧计划数据。"""
from sqlalchemy import Column, String, Text, Boolean, Integer, JSON, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.dialects.mysql import LONGTEXT
from database import Base
from models.base import BaseModel


class PlanModule(Base, BaseModel):
    __tablename__ = "plan_modules"
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_id = Column(String(36), ForeignKey("plan_modules.id", ondelete="RESTRICT"), nullable=True)
    name = Column(String(120), nullable=False)
    position = Column(Integer, nullable=False, default=0)


class PlanWorkspace(Base):
    __tablename__ = "plan_workspaces"
    plan_id = Column(String(36), ForeignKey("test_plans.id", ondelete="CASCADE"), primary_key=True)
    module_id = Column(String(36), ForeignKey("plan_modules.id", ondelete="SET NULL"), nullable=True)
    tags = Column(JSON, nullable=False, default=list)
    archived = Column(Boolean, nullable=False, default=False)
    uses_tree = Column(Boolean, nullable=False, default=False)


class PlanFollow(Base, BaseModel):
    __tablename__ = "plan_follows"
    __table_args__ = (UniqueConstraint("plan_id", "user_id", name="uq_plan_follow_user"),)
    plan_id = Column(String(36), ForeignKey("test_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


class PlanNode(Base, BaseModel):
    """测试点/关联实例；同一用例可通过不同节点重复关联。"""
    __tablename__ = "plan_nodes"
    plan_id = Column(String(36), ForeignKey("test_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_id = Column(String(36), ForeignKey("plan_nodes.id", ondelete="CASCADE"), nullable=True)
    name = Column(String(255), nullable=False)
    node_type = Column(String(16), nullable=False, default="point")
    category = Column(String(16), nullable=False, default="functional")
    case_id = Column(String(36), ForeignKey("test_cases.id", ondelete="RESTRICT"), nullable=True)
    suite_id = Column(String(36), ForeignKey("test_suites.id", ondelete="RESTRICT"), nullable=True)
    assigned_to = Column(String(36), ForeignKey("users.id"), nullable=True)
    linked_functional_id = Column(String(36), ForeignKey("plan_nodes.id", ondelete="SET NULL"), nullable=True)
    position = Column(Integer, nullable=False, default=0)
    config = Column(JSON, nullable=False, default=dict)


class PlanRunComment(Base, BaseModel):
    __tablename__ = "plan_run_comments"
    run_id = Column(String(36), ForeignKey("plan_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    association_id = Column(String(80), nullable=False)
    author_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)


class PlanRunAttachment(Base, BaseModel):
    __tablename__ = "plan_run_attachments"
    run_id = Column(String(36), ForeignKey("plan_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    association_id = Column(String(80), nullable=False)
    author_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    mime_type = Column(String(120), nullable=False)
    content_base64 = Column(Text().with_variant(LONGTEXT(), 'mysql'), nullable=False)


class PlanReportSummary(Base):
    __tablename__ = "plan_report_summaries"
    run_id = Column(String(36), ForeignKey("plan_runs.id", ondelete="CASCADE"), primary_key=True)
    summary = Column(JSON, nullable=False, default=dict)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=False)


class PlanReportShare(Base, BaseModel):
    __tablename__ = "plan_report_shares"
    run_id = Column(String(36), ForeignKey("plan_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = Column(String(64), nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, nullable=False, default=False)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)


class PlanGroupWorkspace(Base):
    __tablename__ = "plan_group_workspaces"
    group_id = Column(String(36), ForeignKey("plan_groups.id", ondelete="CASCADE"), primary_key=True)
    module_id = Column(String(36), ForeignKey("plan_modules.id", ondelete="SET NULL"), nullable=True)
    tags = Column(JSON, nullable=False, default=list)
    archived = Column(Boolean, nullable=False, default=False)
