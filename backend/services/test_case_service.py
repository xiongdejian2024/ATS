"""测试用例服务层"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models.test_case import TestCase
from models.module import Module
from schemas.test_case import TestCaseCreate, TestCaseUpdate
import uuid
from datetime import datetime
from utils.datetime_utils import beijing_now


class TestCaseService:
    """测试用例服务类"""

    @staticmethod
    def validate_references(db: Session, project_id: str, data: dict):
        from fastapi import HTTPException
        from models.user import User

        if (
            data.get("module_id")
            and not db.query(Module)
            .filter_by(id=str(data["module_id"]), project_id=str(project_id))
            .first()
        ):
            raise HTTPException(422, "用例模块不属于当前项目")
        if data.get("executor_id") and not db.get(User, str(data["executor_id"])):
            raise HTTPException(422, "用例执行人不存在")

    @staticmethod
    def get_test_cases(
        db: Session,
        project_id: str,
        page: int = 1,
        size: int = 20,
        search: Optional[str] = None,
        module_id: Optional[str] = None,
        module_ids: Optional[str] = None,  # 逗号分隔的模块 ID 列表
        status: Optional[str] = None,
        priority: Optional[str] = None,
        type: Optional[str] = None,
        tags: Optional[str] = None,  # 标签筛选（逗号分隔）
        is_automated: Optional[bool] = None,  # 是否自动化
        requirement_ref: Optional[str] = None,  # 需求关联
        precondition: Optional[str] = None,  # 前置条件
        review_status: Optional[str] = None,
        filters: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        mine: bool = False,
        followed: bool = False,
        user_id: Optional[str] = None,
        case_ids: Optional[str] = None,
    ):
        """获取测试用例列表；统一高级条件与导出的过滤语义。"""
        from services.case_query import query_cases

        return query_cases(
            db,
            project_id,
            page=page,
            size=size,
            search=search,
            module_id=module_id,
            module_ids=module_ids,
            status=status,
            priority=priority,
            type=type,
            tags=tags,
            is_automated=is_automated,
            requirement_ref=requirement_ref,
            precondition=precondition,
            review_status=review_status,
            filters=filters,
            sort_by=sort_by,
            sort_order=sort_order,
            mine=mine,
            followed=followed,
            user_id=user_id,
            case_ids=case_ids,
        )

    @staticmethod
    def get_test_case(db: Session, case_id: str) -> Optional[TestCase]:
        """获取单个测试用例"""
        return (
            db.query(TestCase)
            .filter(TestCase.id == case_id, TestCase.deleted_at.is_(None))
            .first()
        )

    @staticmethod
    def create_test_case(
        db: Session,
        case_data: TestCaseCreate,
        current_user_id: str,
        *,
        commit: bool = True,
    ) -> TestCase:
        """创建测试用例"""
        TestCaseService.validate_references(
            db, str(case_data.project_id), case_data.model_dump()
        )
        from services.case_features import prepare_case_template

        data = prepare_case_template(
            db,
            str(case_data.project_id),
            case_data.model_dump(),
            case_data.model_fields_set,
        )
        case_data = TestCaseCreate(**data)
        # 生成case_code（如果未提供）- 纯数字格式
        case_code = case_data.case_code
        if not case_code:
            timestamp = int(beijing_now().timestamp() * 1000) % 1000000
            case_code = f"{timestamp:06d}"

            # 确保case_code唯一
            while db.query(TestCase).filter(TestCase.case_code == case_code).first():
                timestamp = (timestamp + 1) % 1000000
                case_code = f"{timestamp:06d}"

        # 创建测试用例对象（当前暂不强制关联模块，避免与尚未落库的模块产生外键冲突）
        test_case = TestCase(
            id=str(uuid.uuid4()),
            project_id=str(case_data.project_id),
            # TODO: 当模块管理切换为数据库实现后，再恢复对 module_id 的真实写入
            module_id=(
                str(case_data.module_id)
                if getattr(case_data, "module_id", None)
                else None
            ),
            case_code=case_code,
            name=case_data.name,
            type=case_data.type,
            priority=case_data.priority,
            is_automated=case_data.is_automated,
            precondition=case_data.precondition,
            case_edit_type=case_data.case_edit_type,
            text_description=case_data.text_description,
            expected_result=case_data.expected_result,
            description=case_data.description,
            steps=case_data.steps or [],
            requirement_ref=case_data.requirement_ref,
            module_path=case_data.module_path,
            level=case_data.level or case_data.priority,  # level默认使用priority
            executor_id=str(case_data.executor_id) if case_data.executor_id else None,
            tags=case_data.tags or [],
            status="not_executed",
            created_by=current_user_id,
            updated_by=current_user_id,
        )
        test_case.template_id = case_data.template_id
        test_case.custom_fields = case_data.custom_fields or {}

        from services.case_governance import snapshot_case
        from core.logger import logger

        try:
            db.add(test_case)
            db.flush()
            snapshot_case(db, test_case, current_user_id, "创建用例")
            from services.case_features import change

            change(db, test_case, current_user_id, "创建用例")
            if commit:
                db.commit()
            db.refresh(test_case)
        except Exception:
            db.rollback()
            logger.exception("创建用例及版本失败")
            raise

        return test_case

    @staticmethod
    def _lock_case_for_write(db: Session, case_id: str) -> Optional[TestCase]:
        project_id = (
            db.query(TestCase.project_id)
            .filter(TestCase.id == case_id, TestCase.deleted_at.is_(None))
            .scalar()
        )
        if not project_id:
            return None
        from services.review_workspace import lock_project

        lock_project(db, project_id)
        return (
            db.query(TestCase)
            .filter(TestCase.id == case_id, TestCase.deleted_at.is_(None))
            .populate_existing()
            .with_for_update()
            .first()
        )

    @staticmethod
    def update_test_case(
        db: Session, case_id: str, case_data: TestCaseUpdate, current_user_id: str
    ) -> Optional[TestCase]:
        """更新测试用例"""
        test_case = TestCaseService._lock_case_for_write(db, case_id)

        if not test_case:
            return None

        from services.case_governance import snapshot_case
        from core.logger import logger

        try:
            TestCaseService.validate_references(
                db, test_case.project_id, case_data.model_dump(exclude_unset=True)
            )
            snapshot_case(db, test_case, current_user_id, "修改前保存版本")
            update_data = case_data.model_dump(exclude_unset=True)
            from services.case_features import prepare_case_template

            update_data = prepare_case_template(
                db,
                test_case.project_id,
                update_data,
                case_data.model_fields_set,
                existing=test_case,
            )
            for field, value in update_data.items():
                setattr(test_case, field, value)
            test_case.updated_by = current_user_id
            test_case.updated_at = beijing_now()
            snapshot_case(db, test_case, current_user_id, "编辑用例")
            from services.case_features import change

            change(
                db,
                test_case,
                current_user_id,
                "编辑用例",
                {"fields": list(update_data)},
            )
            db.commit()
            db.refresh(test_case)
        except Exception:
            db.rollback()
            logger.exception("修改用例及版本失败 case_id={}", case_id)
            raise

        return test_case

    @staticmethod
    def delete_test_case(
        db: Session, case_id: str, current_user_id: str | None = None, *, commit: bool = True
    ) -> bool:
        """删除测试用例"""
        test_case = TestCaseService._lock_case_for_write(db, case_id)

        if not test_case:
            return False

        from services.case_governance import snapshot_case
        from core.logger import logger

        try:
            snapshot_case(
                db,
                test_case,
                current_user_id or test_case.updated_by or test_case.created_by,
                "删除前保留用例版本",
            )
            actor = current_user_id or test_case.updated_by or test_case.created_by
            test_case.deleted_at = beijing_now()
            test_case.deleted_by = actor
            from services.case_features import change

            change(db, test_case, actor, "移入回收站")
            if commit:
                db.commit()
            else:
                db.flush()
        except Exception:
            db.rollback()
            logger.exception("删除用例失败 case_id={}", case_id)
            raise

        return True

    @staticmethod
    def get_case_tree(db: Session, project_id: str) -> List[dict]:
        """获取测试用例树（包含模块和用例）"""
        # 获取所有模块
        modules = db.query(Module).filter(Module.project_id == project_id).all()

        # 获取所有测试用例
        cases = (
            db.query(TestCase)
            .filter(TestCase.project_id == project_id, TestCase.deleted_at.is_(None))
            .all()
        )

        # 构建树结构
        module_map = {}
        tree_data = []

        # 首先构建模块树
        for module in modules:
            module_node = {
                "key": module.id,
                "title": module.name,
                "type": "module",
                "level": getattr(module, "priority", "P2"),
                "children": [],
            }
            module_map[module.id] = module_node

        # 建立父子关系
        for module in modules:
            node = module_map[module.id]
            if module.parent_id and module.parent_id in module_map:
                module_map[module.parent_id]["children"].append(node)
            else:
                tree_data.append(node)

        # 将用例添加到对应模块
        for case in cases:
            case_node = {
                "key": case.id,
                "title": case.name,
                "type": "case",
                "caseCode": case.case_code,
                "level": case.priority,
                "tags": case.tags or [],
            }

            if case.module_id and case.module_id in module_map:
                module_map[case.module_id]["children"].append(case_node)
            else:
                # 无模块的用例直接添加到根级别
                tree_data.append(case_node)

        return tree_data
