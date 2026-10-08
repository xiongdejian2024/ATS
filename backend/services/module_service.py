# -*- coding: utf-8 -*-
"""模块服务层"""

from typing import Optional, List
from sqlalchemy.orm import Session
from models.module import Module
from schemas.module import ModuleCreate, ModuleUpdate
import uuid
from datetime import datetime
from utils.datetime_utils import beijing_now


class ModuleService:
    """模块服务类"""

    @staticmethod
    def get_modules(db: Session, project_id: str) -> List[Module]:
        """获取项目的所有模块"""
        return (
            db.query(Module)
            .filter(Module.project_id == project_id)
            .order_by(Module.sort_order, Module.created_at)
            .all()
        )

    @staticmethod
    def get_modules_with_case_count(db: Session, project_id: str) -> List[dict]:
        """获取项目的所有模块及其用例数量"""
        from models.test_case import TestCase
        from sqlalchemy import func

        modules = (
            db.query(Module)
            .filter(Module.project_id == project_id)
            .order_by(Module.sort_order, Module.created_at)
            .all()
        )

        # 获取每个模块的用例数量
        case_counts = (
            db.query(TestCase.module_id, func.count(TestCase.id).label("count"))
            .filter(TestCase.project_id == project_id, TestCase.deleted_at.is_(None))
            .group_by(TestCase.module_id)
            .all()
        )

        # 构建模块 ID 到用例数量的映射
        count_map = {row.module_id: row.count for row in case_counts}

        # 获取总用例数
        total_count = (
            db.query(func.count(TestCase.id))
            .filter(TestCase.project_id == project_id, TestCase.deleted_at.is_(None))
            .scalar()
            or 0
        )

        result = []
        for module in modules:
            result.append(
                {
                    "id": module.id,
                    "projectId": module.project_id,
                    "name": module.name,
                    "parentId": module.parent_id,
                    "level": module.level,
                    "sortOrder": module.sort_order,
                    "description": module.description,
                    "createdAt": (
                        module.created_at.isoformat() if module.created_at else None
                    ),
                    "updatedAt": (
                        module.updated_at.isoformat() if module.updated_at else None
                    ),
                    "caseCount": count_map.get(module.id, 0),  # 该模块直接包含的用例数
                }
            )

        return result, total_count

    @staticmethod
    def get_module(db: Session, module_id: str) -> Optional[Module]:
        """获取单个模块"""
        return db.query(Module).filter(Module.id == module_id).first()

    @staticmethod
    def create_module(
        db: Session, project_id: str, module_data: ModuleCreate, current_user_id: str
    ) -> Module:
        """创建模块"""
        # 计算层级
        level = 1
        if module_data.parent_id:
            parent = db.query(Module).filter_by(id=module_data.parent_id,project_id=project_id).populate_existing().with_for_update().first()
            if not parent:
                from fastapi import HTTPException
                raise HTTPException(422,"父模块不属于当前项目")
            level = parent.level + 1

        module = Module(
            id=str(uuid.uuid4()),
            project_id=project_id,
            name=module_data.name,
            parent_id=module_data.parent_id,
            level=level,
            sort_order=module_data.sort_order,
            description=module_data.description,
        )

        db.add(module)
        db.commit()
        db.refresh(module)

        return module

    @staticmethod
    def update_module(
        db: Session, module_id: str, module_data: ModuleUpdate, current_user_id: str
    ) -> Optional[Module]:
        """更新模块"""
        module = db.query(Module).filter(Module.id == module_id).populate_existing().with_for_update().first()

        if not module:
            return None

        # 更新字段
        if module_data.name is not None:
            module.name = module_data.name

        if "parent_id" in module_data.model_fields_set:
            parent_id = module_data.parent_id
            if parent_id:
                parent = (
                    db.query(Module)
                    .filter(
                        Module.id == parent_id, Module.project_id == module.project_id
                    )
                    .populate_existing().with_for_update().first()
                )
                if not parent:
                    from fastapi import HTTPException

                    raise HTTPException(422, "父模块不属于当前项目")
                seen = {module.id}
                cursor = parent
                while cursor:
                    if cursor.id in seen:
                        from fastapi import HTTPException

                        raise HTTPException(422, "模块不能移动到自身或子模块内")
                    seen.add(cursor.id)
                    cursor = (
                        db.query(Module).filter_by(id=cursor.parent_id,project_id=module.project_id).populate_existing().with_for_update().first()
                        if cursor.parent_id
                        else None
                    )
            module.parent_id = module_data.parent_id if module_data.parent_id else None
            # 重新计算层级
            if module.parent_id:
                parent = db.query(Module).filter(Module.id == module.parent_id).first()
                if parent:
                    module.level = parent.level + 1
            else:
                module.level = 1

        if module_data.sort_order is not None:
            module.sort_order = module_data.sort_order

        if module_data.description is not None:
            module.description = module_data.description

        module.updated_at = beijing_now()

        # 修改父级后，同步整棵子树的层级；兄弟顺序由前端明确传递 sortOrder。
        changed_ids=ModuleService.sync_subtree_levels(db,[module])
        ModuleService.sync_case_module_paths(db,module.project_id,changed_ids)
        db.commit()
        db.refresh(module)
        return module

    @staticmethod
    def sync_subtree_levels(db: Session, roots: List[Module]):
        queue = list(roots)
        visited = set()
        while queue:
            parent = queue.pop(0)
            if parent.id in visited:
                from fastapi import HTTPException

                raise HTTPException(409, "现有模块层级存在循环，请先修复")
            visited.add(parent.id)
            for child in (
                db.query(Module)
                .filter_by(parent_id=parent.id, project_id=parent.project_id)
                .populate_existing().with_for_update().all()
            ):
                child.level = parent.level + 1
                queue.append(child)
        return visited

    @staticmethod
    def sync_case_module_paths(db: Session, project_id: str, module_ids):
        """父级移动/重命名后同步本项目的显示路径，不改用例身份或历史。"""
        if not module_ids:
            return
        # SessionLocal 禁用 autoflush；当前读前先写入本事务内的新名称/父级/层级。
        db.flush()
        from models.test_case import TestCase
        paths=ModuleService.module_paths(db,project_id,module_ids)
        cases=db.query(TestCase).filter(TestCase.project_id==project_id,TestCase.module_id.in_(module_ids)).populate_existing().with_for_update().all()
        for case in cases:
            case.module_path=paths[case.module_id]

    @staticmethod
    def module_paths(db: Session, project_id: str, module_ids):
        """在调用者持有项目写锁时读取完整路径，兼容 MySQL 当前读。"""
        from fastapi import HTTPException
        modules={m.id:m for m in db.query(Module).filter_by(project_id=project_id).populate_existing().with_for_update().all()}
        paths={}
        for module_id in module_ids:
            names=[];seen=set();cursor=modules.get(module_id)
            if not cursor:
                raise HTTPException(422,"目标模块不属于本项目")
            while cursor:
                if cursor.id in seen or len(seen)>=1000:
                    raise HTTPException(409,"现有模块层级存在循环或过深，请先修复")
                seen.add(cursor.id);names.append(cursor.name)
                if cursor.parent_id and cursor.parent_id not in modules:
                    raise HTTPException(409,"现有父模块不属于当前项目，请先核对关联")
                cursor=modules.get(cursor.parent_id)
            path='/'.join(reversed(names))
            if len(path)>500:
                raise HTTPException(422,"模块路径超过500字符，请缩短名称或层级")
            paths[module_id]=path
        return paths

    @staticmethod
    def delete_module(db: Session, module_id: str) -> bool:
        """删除模块"""
        module = db.query(Module).filter(Module.id == module_id).populate_existing().with_for_update().first()

        if not module:
            return False

        # 旧创建入口曾允许跨项目父级。拒绝删除这类旧关联，避免 ORM 回填外项目行。
        from models.test_case import TestCase
        foreign_children=db.query(Module.id).filter(Module.parent_id==module.id,Module.project_id!=module.project_id).first()
        foreign_cases=db.query(TestCase.id).filter(TestCase.module_id==module.id,TestCase.project_id!=module.project_id).first()
        if foreign_children or foreign_cases:
            from fastapi import HTTPException
            raise HTTPException(409,"模块存在跨项目旧关联，请先核对并修复关联")

        # 提升子模块时同步整棵子树层级，保留所有模块内容。
        children=db.query(Module).filter_by(parent_id=module.id,project_id=module.project_id).populate_existing().with_for_update().all()
        parent=(db.query(Module).filter_by(id=module.parent_id,project_id=module.project_id).populate_existing().with_for_update().first() if module.parent_id else None)
        for child in children:
            # 同时更新 ORM 关系，避免删除旧父节点时 UOW 再把已提升子节点置为根。
            child.parent=parent
            child.level=parent.level+1 if parent else 1
        changed_ids=ModuleService.sync_subtree_levels(db,children)
        ModuleService.sync_case_module_paths(db,module.project_id,changed_ids)

        # 将关联的测试用例的 module_id 设置为 None
        db.query(TestCase).filter(TestCase.module_id == module_id,TestCase.project_id==module.project_id).update(
            {"module_id": None,"module_path":None}
        )

        db.delete(module)
        db.commit()

        return True

    @staticmethod
    def get_module_tree(db: Session, project_id: str) -> List[dict]:
        """获取模块树结构"""
        modules = ModuleService.get_modules(db, project_id)

        # 构建模块映射
        module_map = {}
        for module in modules:
            module_map[module.id] = {
                "key": module.id,
                "title": module.name,
                "type": "module",
                "level": f"P{min(module.level, 3)}",
                "children": [],
            }

        # 构建树结构
        tree = []
        for module in modules:
            node = module_map[module.id]
            if module.parent_id and module.parent_id in module_map:
                module_map[module.parent_id]["children"].append(node)
            else:
                tree.append(node)

        return tree
