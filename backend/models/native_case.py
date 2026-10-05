"""项目原生接口定义、环境与用例配置，执行结果仍由实际记录提供。"""
from sqlalchemy import Column, String, JSON, Integer, ForeignKey, DateTime, func
from database import Base
from models.base import BaseModel


class ApiDefinition(Base, BaseModel):
    __tablename__ = 'native_api_definitions'
    project_id = Column(String(36), ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    protocol = Column(String(50), nullable=False)
    path = Column(String(500), nullable=False)
    parameters = Column(JSON, nullable=False, default=dict)
    revision = Column(Integer, nullable=False, default=1)
    updated_by = Column(String(36), ForeignKey('users.id'), nullable=False)


class ApiTestEnvironment(Base, BaseModel):
    __tablename__ = 'native_api_environments'
    project_id = Column(String(36), ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=False)
    revision = Column(Integer, nullable=False, default=1)
    updated_by = Column(String(36), ForeignKey('users.id'), nullable=False)


class NativeCaseConfig(Base):
    __tablename__ = 'native_case_configs'
    case_id = Column(String(36), ForeignKey('test_cases.id', ondelete='CASCADE'), primary_key=True)
    state = Column(String(30), nullable=False)
    environment_id = Column(String(36), ForeignKey('native_api_environments.id'), nullable=True)
    api_definition_id = Column(String(36), ForeignKey('native_api_definitions.id'), nullable=True)
    definition_fingerprint = Column(String(64), nullable=True)
    parameters = Column(JSON, nullable=False, default=dict)
    revision = Column(Integer, nullable=False, default=1)
    updated_by = Column(String(36), ForeignKey('users.id'), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
