"""用例扩展实体；审计记录保留用例删除前的身份。"""

from sqlalchemy import Column, String, Text, JSON, ForeignKey, Boolean, UniqueConstraint
from database import Base
from models.base import BaseModel


class CaseChange(Base, BaseModel):
    __tablename__ = "case_changes"
    project_id = Column(
        String(36),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    case_id = Column(String(36), nullable=False, index=True)
    actor_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    action = Column(String(60), nullable=False)
    detail = Column(JSON, nullable=False)


class CaseTemplate(Base, BaseModel):
    __tablename__ = "case_templates"
    __table_args__ = (
        UniqueConstraint("project_id", "name", name="uq_case_template_name"),
    )
    project_id = Column(
        String(36),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name = Column(String(100), nullable=False)
    fields = Column(JSON, nullable=False, default=list)
    defaults = Column(JSON, nullable=False, default=dict)
    is_default = Column(Boolean, nullable=False, default=False)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)


class CaseIssue(Base, BaseModel):
    __tablename__ = "case_issues"
    project_id = Column(
        String(36),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    kind = Column(String(20), nullable=False, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=False, default="")
    status = Column(String(30), nullable=False, default="open")
    external_ref = Column(String(500), nullable=True)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=False)


class CaseIssueLink(Base, BaseModel):
    __tablename__ = "case_issue_links"
    __table_args__ = (
        UniqueConstraint("case_id", "issue_id", name="uq_case_issue_link"),
    )
    case_id = Column(
        String(36),
        ForeignKey("test_cases.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    issue_id = Column(
        String(36),
        ForeignKey("case_issues.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)


class CaseRelation(Base, BaseModel):
    __tablename__ = "case_relations"
    __table_args__ = (
        UniqueConstraint(
            "source_case_id", "target_case_id", "kind", name="uq_case_relation"
        ),
    )
    project_id = Column(
        String(36),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_case_id = Column(
        String(36),
        ForeignKey("test_cases.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_case_id = Column(
        String(36),
        ForeignKey("test_cases.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    kind = Column(String(20), nullable=False)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)


class CaseAutomationLink(Base, BaseModel):
    __tablename__ = "case_automation_links"
    case_id = Column(
        String(36),
        ForeignKey("test_cases.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category = Column(String(20), nullable=False)
    target_case_id = Column(
        String(36), ForeignKey("test_cases.id", ondelete="CASCADE"), nullable=True
    )
    suite_id = Column(
        String(36), ForeignKey("test_suites.id", ondelete="CASCADE"), nullable=True
    )
    external_ref = Column(String(500), nullable=True)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)


class CaseFollow(Base, BaseModel):
    __tablename__ = "case_follows"
    __table_args__ = (UniqueConstraint("case_id", "user_id", name="uq_case_follow"),)
    case_id = Column(
        String(36),
        ForeignKey("test_cases.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class CaseComment(Base, BaseModel):
    __tablename__ = "case_comments"
    case_id = Column(
        String(36),
        ForeignKey("test_cases.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    author_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
