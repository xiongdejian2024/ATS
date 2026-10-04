"""功能用例执行描述图片；图片引用与执行历史一起保留。"""

from sqlalchemy import Column, String, Integer, LargeBinary, ForeignKey
from sqlalchemy.dialects.mysql import LONGBLOB
from database import Base
from models.base import BaseModel


class PlanCaseMedia(Base, BaseModel):
    __tablename__ = "plan_case_media"
    plan_id = Column(
        String(36),
        ForeignKey("test_plans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    uploaded_by = Column(
        String(36),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(50), nullable=False)
    content = Column(LargeBinary().with_variant(LONGBLOB(), "mysql"), nullable=False)


class PlanCaseMediaLink(Base):
    __tablename__ = "plan_case_media_links"
    execution_id = Column(
        String(36),
        ForeignKey("plan_case_executions.id", ondelete="CASCADE"),
        primary_key=True,
    )
    media_id = Column(
        String(36),
        ForeignKey("plan_case_media.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
