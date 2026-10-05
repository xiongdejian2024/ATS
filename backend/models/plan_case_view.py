"""按项目、成员和用例分类隔离计划工作区个人视图。"""

from sqlalchemy import Column, String, JSON, ForeignKey, UniqueConstraint
from database import Base
from models.base import BaseModel


class PlanCaseSavedView(Base, BaseModel):
    __tablename__ = "plan_case_saved_views"
    __table_args__ = (
        UniqueConstraint("project_id", "owner_id", "category", "name", name="uq_plan_case_view"),
    )
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    owner_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    category = Column(String(20), nullable=False)
    name = Column(String(255), nullable=False)
    filters = Column(JSON, nullable=False)
