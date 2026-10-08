"""任务队列模型"""
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Boolean, func, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base
import uuid


class TaskQueue(Base):
    """任务队列表"""
    __tablename__ = "task_queue"
    __table_args__ = (CheckConstraint("(kind = 'suite' AND suite_id IS NOT NULL AND script_job_id IS NULL) OR (kind = 'script' AND suite_id IS NULL AND script_job_id IS NOT NULL)", name="ck_task_queue_target"),)
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    environment_id = Column(String(36), ForeignKey("environments.id", ondelete="CASCADE"), nullable=False, index=True, comment="环境ID")
    kind = Column(String(16), nullable=False, default="suite", server_default="suite")
    suite_id = Column(String(36), ForeignKey("test_suites.id", ondelete="CASCADE"), nullable=True, index=True, comment="测试套ID")
    script_job_id = Column(String(36), ForeignKey("script_jobs.id"), nullable=True, index=True)
    execution_id = Column(String(36), nullable=False, index=True, comment="执行ID")
    executor_id = Column(String(36), ForeignKey("users.id"), nullable=False, comment="执行人ID")
    status = Column(String(50), default="pending", nullable=False, index=True, comment="状态: pending, running, completed, failed, cancelled")
    priority = Column(Integer, default=0, nullable=False, comment="优先级，数字越大优先级越高")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True, comment="创建时间")
    started_at = Column(DateTime(timezone=True), nullable=True, comment="开始执行时间")
    completed_at = Column(DateTime(timezone=True), nullable=True, comment="完成时间")
    
    # 关系
    environment = relationship("Environment")
    suite = relationship("TestSuite")
    executor = relationship("User")
    
    def __repr__(self):
        return f"<TaskQueue(id={self.id}, environment_id={self.environment_id}, suite_id={self.suite_id}, status={self.status})>"

