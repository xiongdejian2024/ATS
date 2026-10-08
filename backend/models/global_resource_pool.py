"""Independent Node resource pools; existing project pools remain unchanged."""

from sqlalchemy import Column, String, Text, Integer, Boolean, ForeignKey
from database import Base
from models.base import BaseModel


class GlobalResourcePool(Base, BaseModel):
    __tablename__ = "global_resource_pools"
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False, default="")
    enabled = Column(Boolean, nullable=False, default=True)
    api_enabled = Column(Boolean, nullable=False, default=True)
    scenario_enabled = Column(Boolean, nullable=False, default=True)
    all_projects = Column(Boolean, nullable=False, default=False)
    revision = Column(Integer, nullable=False, default=1)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    creation_key = Column(String(180), unique=True, nullable=True)
    creation_fingerprint = Column(String(64), nullable=True)


class GlobalResourcePoolProject(Base):
    __tablename__ = "global_resource_pool_projects"
    pool_id = Column(
        String(36), ForeignKey("global_resource_pools.id", ondelete="CASCADE"), primary_key=True
    )
    project_id = Column(
        String(36), ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True, index=True
    )


class GlobalResourcePoolMember(Base):
    __tablename__ = "global_resource_pool_members"
    pool_id = Column(
        String(36), ForeignKey("global_resource_pools.id", ondelete="CASCADE"), primary_key=True
    )
    environment_id = Column(
        String(36), ForeignKey("environments.id", ondelete="RESTRICT"), primary_key=True, index=True
    )
    position = Column(Integer, nullable=False)
