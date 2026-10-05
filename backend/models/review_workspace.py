"""评审独立目录与展示元数据；旧评审读取不触发迁移写入。"""

from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    JSON,
    Boolean,
    UniqueConstraint,
    DateTime,
)
from sqlalchemy.dialects.mysql import DATETIME
from database import Base
from models.base import BaseModel


class ReviewModule(Base, BaseModel):
    __tablename__ = "review_modules"
    project_id = Column(
        String(36),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    parent_id = Column(
        String(36), ForeignKey("review_modules.id", ondelete="CASCADE"), nullable=True
    )
    name = Column(String(100), nullable=False)
    position = Column(Integer, nullable=False, default=0)
    __table_args__ = (
        UniqueConstraint(
            "project_id", "parent_id", "name", name="uq_review_module_name"
        ),
    )


class ReviewWorkspace(Base):
    __tablename__ = "review_workspaces"
    # 数据库生成的稳定编号；历史评审在显式修改时获取编号，GET 保持只读。
    number = Column(Integer, primary_key=True, autoincrement=True)
    review_id = Column(
        String(36),
        ForeignKey("case_reviews.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    module_id = Column(
        String(36),
        ForeignKey("review_modules.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    tags = Column(JSON, nullable=False, default=list)
    archived = Column(Boolean, nullable=False, default=False)
    start_time = Column(
        DateTime().with_variant(DATETIME(fsp=6), "mysql"), nullable=True
    )
    end_time = Column(DateTime().with_variant(DATETIME(fsp=6), "mysql"), nullable=True)
