"""任务中心：持久化调度定义与每次独立触发记录。"""

import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text, Index
from database import Base


class TaskSchedule(Base):
    __tablename__ = "task_schedules"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    target_type = Column(String(16), nullable=False)
    target_id = Column(String(36), nullable=False)
    cron_expression = Column(String(100), nullable=True)
    timezone = Column(String(64), nullable=False, default="Asia/Shanghai")
    enabled = Column(Boolean, nullable=False, default=False)
    next_run_at = Column(DateTime, nullable=True, index=True)
    last_run_at = Column(DateTime, nullable=True)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class TaskScheduleRun(Base):
    __tablename__ = "task_schedule_runs"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    schedule_id = Column(String(36), ForeignKey("task_schedules.id"), nullable=False, index=True)
    trigger_key = Column(String(200), nullable=False, unique=True)
    trigger_type = Column(String(16), nullable=False)
    scheduled_for = Column(DateTime, nullable=False)
    executor_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    execution_id = Column(String(36), nullable=True, unique=True)
    plan_run_id = Column(String(36), nullable=True, unique=True)
    group_run_id = Column(String(36), nullable=True, unique=True, index=True)
    status = Column(String(20), nullable=False, default="queued", index=True)
    error_message = Column(Text, nullable=True)
    delivery_state = Column(String(20), nullable=False, default="queued")
    dispatch_attempted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)


Index("ix_task_schedules_due", TaskSchedule.enabled, TaskSchedule.next_run_at)
