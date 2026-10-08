"""任务队列服务"""
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, update
from models.task_queue import TaskQueue
from models.environment import Environment
from models.test_suite import TestSuite
from utils.datetime_utils import beijing_now
from utils.serializer import serialize_model, serialize_list
from core.logger import logger
import uuid


class TaskQueueService:
    """任务队列服务类"""
    
    @staticmethod
    def get_running_task_count(db: Session, environment_id: str) -> int:
        """获取环境中正在运行的任务数量"""
        count = db.query(TaskQueue).filter(
            and_(
                TaskQueue.environment_id == environment_id,
                TaskQueue.status == "running"
            )
        ).count()
        return count
    
    @staticmethod
    def get_pending_task_count(db: Session, environment_id: str) -> int:
        """获取环境中等待中的任务数量"""
        count = db.query(TaskQueue).filter(
            and_(
                TaskQueue.environment_id == environment_id,
                TaskQueue.status == "pending"
            )
        ).count()
        return count
    
    @staticmethod
    def can_execute_immediately(db: Session, environment_id: str) -> bool:
        """检查是否可以立即执行任务"""
        environment = db.query(Environment).filter(Environment.id == environment_id).first()
        if not environment:
            return False
        
        max_tasks = environment.max_concurrent_tasks or 1
        running_count = TaskQueueService.get_running_task_count(db, environment_id)
        
        return running_count < max_tasks
    
    @staticmethod
    def add_to_queue(
        db: Session,
        environment_id: str,
        suite_id: str,
        execution_id: str,
        executor_id: str,
        priority: int = 0
    ) -> TaskQueue:
        """将任务添加到队列"""
        task = TaskQueue(
            id=str(uuid.uuid4()),
            environment_id=environment_id,
            suite_id=suite_id,
            execution_id=execution_id,
            executor_id=executor_id,
            status="pending",
            priority=priority,
            created_at=beijing_now()
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        logger.info(f"任务已加入队列: environment_id={environment_id}, suite_id={suite_id}, execution_id={execution_id}")
        return task
    
    @staticmethod
    def lock_environment(db: Session, environment_id: str) -> Optional[Environment]:
        """Serialize slot decisions until the caller commits/rolls back.

        MySQL uses a current locking read, not an earlier repeatable-read
        snapshot. SQLite has no row locks, so its offline/test path obtains a
        write reservation with a no-op UPDATE before inspecting capacity.
        """
        if db.get_bind().dialect.name == "sqlite":
            db.execute(update(Environment).where(Environment.id == environment_id).values(
                id=Environment.id, updated_at=Environment.updated_at
            ), execution_options={"synchronize_session": False})
        return db.query(Environment).filter_by(id=environment_id).populate_existing().with_for_update().first()

    @staticmethod
    def start_task(
        db: Session, execution_id: str, *, environment_id: Optional[str] = None,
        commit: bool = True, eligibility=(),
    ) -> Optional[TaskQueue]:
        """Atomically reserve one slot and claim a pending execution.

        Only the returned claim owner may dispatch. With commit=False the
        caller must commit its delivery bookkeeping before network I/O, or
        roll back the entire claim. Extra predicates preserve orchestration
        cancellation/eligibility checks in the same conditional UPDATE.
        """
        environment_id = environment_id or db.query(TaskQueue.environment_id).filter_by(
            execution_id=execution_id
        ).scalar()
        if not environment_id:
            return None
        environment = TaskQueueService.lock_environment(db, environment_id)
        # Locking read is essential under MySQL REPEATABLE READ: an ordinary
        # COUNT could reuse a snapshot from before the environment lock.
        running = db.query(TaskQueue.id).filter_by(
            environment_id=environment_id, status="running"
        ).with_for_update().all()
        task = None
        if environment and environment.status and len(running) < max(1, environment.max_concurrent_tasks or 1):
            changed = db.query(TaskQueue).filter(
                TaskQueue.execution_id == execution_id,
                TaskQueue.environment_id == environment_id,
                TaskQueue.status == "pending", *eligibility,
            ).update({"status": "running", "started_at": beijing_now()}, synchronize_session=False)
            if changed == 1:
                task = db.query(TaskQueue).filter_by(execution_id=execution_id).populate_existing().one()
            elif changed > 1:
                # Corrupt duplicate IDs must never dispatch multiple workloads.
                db.rollback()
                raise ValueError("执行ID对应多个任务，无法安全派发")
        if commit:
            db.commit()
            if task:
                db.refresh(task)
        if task:
            logger.info("任务已领取运行槽：环境={}，执行={}", environment_id, execution_id)
        return task

    @staticmethod
    def complete_task(
        db: Session,
        execution_id: str,
        status: str = "completed"
    ) -> Optional[TaskQueue]:
        """完成任务（从running或pending变为completed/failed/cancelled）"""
        task = db.query(TaskQueue).filter(
            TaskQueue.execution_id == execution_id
        ).first()
        
        if task:
            values = {"status": status}
            if status in ["completed", "failed", "cancelled"]:
                values["completed_at"] = beijing_now()
            changed = db.query(TaskQueue).filter(
                TaskQueue.id == task.id, TaskQueue.status.in_(("running", "pending"))
            ).update(values, synchronize_session=False)
            db.commit()
            db.refresh(task)
            if changed:
                logger.info(f"任务完成: execution_id={execution_id}, status={status}")
                return task
        return None

    @staticmethod
    def get_next_pending_task(db: Session, environment_id: str) -> Optional[TaskQueue]:
        """获取下一个待执行的任务（按优先级和创建时间排序）"""
        # 计划项由编排调度统一领取，避免旧完成回调绕过失败停止与派发确认。
        from models.plan_orchestration import PlanRunItem
        from models.task_schedule import TaskScheduleRun
        task = db.query(TaskQueue).filter(
            ~TaskQueue.execution_id.in_(db.query(PlanRunItem.execution_id)),
            ~TaskQueue.execution_id.in_(db.query(TaskScheduleRun.execution_id).filter(
                TaskScheduleRun.execution_id.isnot(None)
            )),
            and_(
                TaskQueue.environment_id == environment_id,
                TaskQueue.status == "pending"
            )
        ).order_by(
            TaskQueue.priority.desc(),
            TaskQueue.created_at.asc()
        ).first()
        
        return task
    
    @staticmethod
    def get_queue_status(db: Session, environment_id: str) -> Dict[str, Any]:
        """获取队列状态"""
        environment = db.query(Environment).filter(Environment.id == environment_id).first()
        if not environment:
            return {
                "maxConcurrentTasks": 1,
                "runningCount": 0,
                "pendingCount": 0,
                "canExecute": False
            }
        
        max_tasks = environment.max_concurrent_tasks or 1
        running_count = TaskQueueService.get_running_task_count(db, environment_id)
        pending_count = TaskQueueService.get_pending_task_count(db, environment_id)
        
        return {
            "maxConcurrentTasks": max_tasks,
            "runningCount": running_count,
            "pendingCount": pending_count,
            "canExecute": running_count < max_tasks
        }
    
    @staticmethod
    def get_queue_tasks(
        db: Session,
        environment_id: str,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """获取队列中的任务列表"""
        query = db.query(TaskQueue).filter(
            TaskQueue.environment_id == environment_id
        )
        
        if status:
            query = query.filter(TaskQueue.status == status)
        
        total = query.count()
        tasks = query.order_by(
            TaskQueue.priority.desc(),
            TaskQueue.created_at.asc()
        ).offset(skip).limit(limit).all()
        
        return {
            "items": serialize_list(tasks, camel_case=True),
            "total": total,
            "skip": skip,
            "limit": limit
        }
