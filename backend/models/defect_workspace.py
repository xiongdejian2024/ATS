"""Additive defect workspace; existing CaseIssue identities and evidence survive."""

from database import Base
from models.base import BaseModel
from sqlalchemy import Column, String, Text, JSON, Boolean, Integer, ForeignKey, UniqueConstraint


class DefectTemplate(Base, BaseModel):
    __tablename__ = "defect_templates"
    __table_args__ = (UniqueConstraint("project_id", "name", name="uq_defect_template_name"),)
    project_id = Column(
        String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name = Column(String(100), nullable=False)
    fields = Column(JSON, nullable=False, default=list)
    defaults = Column(JSON, nullable=False, default=dict)
    is_default = Column(Boolean, nullable=False, default=False)
    revision = Column(Integer, nullable=False, default=1)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=False)


class DefectProfile(Base):
    __tablename__ = "defect_profiles"
    issue_id = Column(
        String(36), ForeignKey("case_issues.id", ondelete="CASCADE"), primary_key=True
    )
    template_id = Column(
        String(36),
        ForeignKey("defect_templates.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    custom_fields = Column(JSON, nullable=False, default=dict)
    revision = Column(Integer, nullable=False, default=1)
    description_format = Column(String(10), nullable=False, default="plain")
    archived = Column(Boolean, nullable=False, default=False)
    creation_key = Column(String(180), unique=True, nullable=True)
    creation_fingerprint = Column(String(64), nullable=True)


class DefectComment(Base, BaseModel):
    __tablename__ = "defect_comments"
    issue_id = Column(
        String(36), ForeignKey("case_issues.id", ondelete="CASCADE"), nullable=False, index=True
    )
    author_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)
    creation_key = Column(String(180), unique=True, nullable=True)
    creation_fingerprint = Column(String(64), nullable=True)
    receipt_revision = Column(Integer, nullable=False)


class DefectEvent(Base, BaseModel):
    __tablename__ = "defect_events"
    issue_id = Column(
        String(36), ForeignKey("case_issues.id", ondelete="CASCADE"), nullable=False, index=True
    )
    actor_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    action = Column(String(30), nullable=False)
    revision = Column(Integer, nullable=False)
    detail = Column(JSON, nullable=False)
