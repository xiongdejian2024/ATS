"""用例版本、评审和个人筛选视图；仅新增表，保留既有用例数据。"""

from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    JSON,
    ForeignKey,
    UniqueConstraint,
    Date,
)
from database import Base
from models.base import BaseModel


class CaseVersion(Base, BaseModel):
    __tablename__ = "case_versions"
    __table_args__ = (UniqueConstraint("case_id", "version", name="uq_case_version"),)
    project_id = Column(
        String(36),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # 不级联删除历史，删除用例后仍可供评审和审计引用。
    case_id = Column(String(36), nullable=False, index=True)
    version = Column(Integer, nullable=False)
    snapshot = Column(JSON, nullable=False)
    reason = Column(String(500), nullable=False)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)


class CaseReview(Base, BaseModel):
    __tablename__ = "case_reviews"
    project_id = Column(
        String(36),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name = Column(String(200), nullable=False)
    policy = Column(String(20), nullable=False, default="all")
    reviewer_ids = Column(JSON, nullable=False)
    status = Column(String(30), nullable=False, default="pending")
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    description = Column(Text, nullable=False, default="")
    mode = Column(String(20), nullable=False, default="multiple")
    parent_review_id = Column(String(36), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)


class CaseReviewItem(Base, BaseModel):
    __tablename__ = "case_review_items"
    __table_args__ = (UniqueConstraint("review_id", "case_id", name="uq_review_case"),)
    review_id = Column(
        String(36),
        ForeignKey("case_reviews.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    case_id = Column(String(36), nullable=False, index=True)
    version_id = Column(
        String(36), ForeignKey("case_versions.id", ondelete="CASCADE"), nullable=False
    )
    status = Column(String(30), nullable=False, default="pending")
    reviewer_ids = Column(JSON, nullable=True)


class CaseReviewDecision(Base, BaseModel):
    __tablename__ = "case_review_decisions"
    __table_args__ = (
        UniqueConstraint("item_id", "reviewer_id", name="uq_review_vote"),
    )
    item_id = Column(
        String(36),
        ForeignKey("case_review_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    reviewer_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    decision = Column(String(20), nullable=False)
    comment = Column(Text, nullable=False)


class CaseReviewComment(Base, BaseModel):
    __tablename__ = "case_review_comments"
    review_id = Column(
        String(36),
        ForeignKey("case_reviews.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    item_id = Column(
        String(36),
        ForeignKey("case_review_items.id", ondelete="CASCADE"),
        nullable=True,
    )
    author_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)


class CaseSavedView(Base, BaseModel):
    __tablename__ = "case_saved_views"
    __table_args__ = (
        UniqueConstraint("project_id", "owner_id", "name", name="uq_case_saved_view"),
    )
    project_id = Column(
        String(36),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    owner_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    filters = Column(JSON, nullable=False)


class CaseReviewEvent(Base, BaseModel):
    __tablename__ = "case_review_events"
    review_id = Column(
        String(36),
        ForeignKey("case_reviews.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    item_id = Column(String(36), nullable=True)
    actor_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    action = Column(String(40), nullable=False)
    detail = Column(JSON, nullable=False)


class CaseReviewFollow(Base, BaseModel):
    __tablename__ = "case_review_follows"
    __table_args__ = (
        UniqueConstraint("review_id", "user_id", name="uq_review_follow"),
    )
    review_id = Column(
        String(36),
        ForeignKey("case_reviews.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
