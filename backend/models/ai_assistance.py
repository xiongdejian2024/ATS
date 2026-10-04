"""AI 配置、会话和待审阅草稿；不改变已有用例表。"""
from sqlalchemy import Column, String, Text, Boolean, Integer, JSON, ForeignKey
from database import Base
from .base import BaseModel


class AIModelConfig(Base, BaseModel):
    __tablename__ = "ai_model_configs"
    owner_key = Column(String(50), unique=True, nullable=False)
    base_url = Column(String(500), nullable=False)
    model = Column(String(200), nullable=False)
    api_key_encrypted = Column(Text)
    timeout_seconds = Column(Integer, nullable=False, default=60)
    enabled = Column(Boolean, nullable=False, default=True)


class AIConversation(Base, BaseModel):
    __tablename__ = "ai_conversations"
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    messages = Column(JSON, nullable=False, default=list)
    revision = Column(Integer, nullable=False, default=1)


class AICaseDraft(Base, BaseModel):
    __tablename__ = "ai_case_drafts"
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False, index=True)
    batch_id = Column(String(36), nullable=False, index=True)
    content = Column(JSON, nullable=False)
    source_prompt = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="draft")
    revision = Column(Integer, nullable=False, default=1)
    imported_case_id = Column(String(36))
