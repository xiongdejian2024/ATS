"""分类根及测试集的完整执行配置；请求环境与资源池分别保存。"""

from sqlalchemy import Column, String, Integer, JSON, ForeignKey
from database import Base
from models.base import BaseModel


class PlanResourcePool(Base, BaseModel):
    __tablename__ = "plan_resource_pools"
    project_id = Column(
        String(36),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name = Column(String(255), nullable=False)
    environment_ids = Column(JSON, nullable=False, default=list)
    revision = Column(Integer, nullable=False, default=1)


class PlanExecutionConfig(Base):
    __tablename__ = "plan_execution_configs"
    plan_id = Column(
        String(36), ForeignKey("test_plans.id", ondelete="CASCADE"), primary_key=True
    )
    scope = Column(String(80), primary_key=True)
    category = Column(String(16), nullable=False)
    node_id = Column(
        String(36), ForeignKey("plan_nodes.id", ondelete="CASCADE"), nullable=True
    )
    config = Column(JSON, nullable=False, default=dict)
    revision = Column(Integer, nullable=False, default=1)
