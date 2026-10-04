"""报告可编辑名称和删除标记；独立存放，不改变冻结的执行结果。"""
from sqlalchemy import Column, String, Boolean, ForeignKey
from database import Base


class PlanReportWorkspace(Base):
    __tablename__ = "plan_report_workspaces"
    run_id = Column(String(36), ForeignKey("plan_runs.id", ondelete="CASCADE"), primary_key=True)
    name = Column(String(255), nullable=True)
    deleted = Column(Boolean, nullable=False, default=False)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=False)


class GroupReportWorkspace(Base):
    __tablename__ = "group_report_workspaces"
    run_id = Column(String(36), ForeignKey("plan_group_runs.id", ondelete="CASCADE"), primary_key=True)
    name = Column(String(255), nullable=True)
    deleted = Column(Boolean, nullable=False, default=False)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=False)
