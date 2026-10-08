"""项目请求环境组；每个来源项目映射到该项目自己的请求环境。"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey
from database import Base
from models.base import BaseModel


class RequestEnvironmentGroup(Base, BaseModel):
    __tablename__ = "request_environment_groups"
    project_id = Column(
        String(36),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False, default="")
    revision = Column(Integer, nullable=False, default=1)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    creation_key = Column(String(180), nullable=True, unique=True)
    creation_fingerprint = Column(String(64), nullable=True)


class RequestEnvironmentMapping(Base):
    __tablename__ = "request_environment_group_mappings"
    group_id = Column(
        String(36),
        ForeignKey("request_environment_groups.id", ondelete="CASCADE"),
        primary_key=True,
    )
    source_project_id = Column(
        String(36), ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True
    )
    environment_id = Column(
        String(36),
        ForeignKey("native_api_environments.id", ondelete="RESTRICT"),
        nullable=False,
    )
