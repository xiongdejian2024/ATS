# -*- coding: utf-8 -*-
"""数据模型模块"""
from database import Base
from .user import User
from .project import Project, ProjectMember
from .module import Module
from .test_case import TestCase, CaseAttachment
from .filter_field import FilterField
from .test_plan import TestPlan, PlanCaseRelation
from .test_execution import TestExecution, ExecutionAttachment
from .test_suite import TestSuite, TestSuiteExecution, TestSuiteLog
from .test_report import TestReport
from .task_queue import TaskQueue
from .environment import Environment
from .notification import Notification
from .ai_assistance import AIModelConfig, AIConversation, AICaseDraft
from .case_governance import CaseVersion, CaseReview, CaseReviewItem, CaseReviewDecision, CaseReviewComment, CaseSavedView
from .case_features import CaseChange
from .plan_orchestration import PlanGroup, PlanSettings, PlanRun, PlanRunItem
from .task_schedule import TaskSchedule, TaskScheduleRun
from .role import Role, Permission, UserRole, RolePermission, ProjectPermission

__all__ = [
    "Base",
    "User",
    "Project",
    "ProjectMember",
    "Module",
    "TestCase",
    "CaseAttachment",
    "FilterField",
    "TestPlan",
    "PlanCaseRelation",
    "TestExecution",
    "ExecutionAttachment",
    "TestReport",
    "TestSuite",
    "TestSuiteExecution",
    "TestSuiteLog",
    "Environment",
    "TaskQueue",
    "Notification",
    "Role",
    "Permission",
    "UserRole",
    "RolePermission",
    "ProjectPermission",
]
