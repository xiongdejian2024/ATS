"""Dispatch uncertainty and audited operator closure, keyed by execution."""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from database import Base


class SuiteDelivery(Base):
    __tablename__ = "suite_deliveries"
    execution_id = Column(String(36), primary_key=True)
    suite_id = Column(String(36), ForeignKey("test_suites.id", ondelete="CASCADE"), nullable=False, index=True)
    environment_id = Column(String(36), ForeignKey("environments.id"), nullable=False)
    session_id = Column(String(36), nullable=True)
    state = Column(String(20), nullable=False, default="dispatching")
    closed_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)
    reason = Column(Text, nullable=True)
