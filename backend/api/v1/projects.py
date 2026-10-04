# -*- coding: utf-8 -*-
"""项目相关API"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional, Dict, Any
from database import get_db
from models import Project
from schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse
from schemas.test_case import TestCaseCreate, TestCaseUpdate, TestCaseResponse
from schemas.module import ModuleCreate, ModuleUpdate
from schemas.common import APIResponse, ResponseStatus
from api.deps import get_current_user
from models import User
from utils.serializer import serialize_model, serialize_list
from services.module_service import ModuleService
from core.logger import logger
import uuid
import json
from pathlib import Path

router = APIRouter()


@router.get("", response_model=APIResponse)
async def get_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = 1,
    size: int = 20,
    search: Optional[str] = None,
    status: Optional[str] = None,
):
    """获取项目列表（使用数据库持久化，支持分页）"""
    # 查询所有项目，按创建时间倒序
    query = db.query(Project).order_by(Project.created_at.desc())
    
    # 搜索条件
    if search:
        query = query.filter(
            or_(
                Project.name.contains(search),
                Project.description.contains(search)
            )
        )
    
    # 状态过滤
    if status:
        query = query.filter(Project.status == status)
    
    # 总数
    total = query.count()
    
    # 分页
    offset = (page - 1) * size
    items = query.offset(offset).limit(size).all()

    # 获取所有相关的用户ID
    user_ids = set()
    for item in items:
        if item.created_by:
            user_ids.add(item.created_by)
        if item.owner_id:
            user_ids.add(item.owner_id)
    
    # 批量查询用户信息
    users = db.query(User).filter(User.id.in_(user_ids)).all() if user_ids else []
    user_map = {str(u.id): u.username or u.email or str(u.id) for u in users}
    
    # 构建项目列表，包含用户名
    project_list = []
    for item in items:
        project_data = serialize_model(item, camel_case=True)
        # 添加用户名字段
        project_data['createdByName'] = user_map.get(item.created_by, 'Unknown')
        project_data['updatedByName'] = user_map.get(item.owner_id, user_map.get(item.created_by, 'Unknown'))
        project_list.append(project_data)
    
    # 计算总页数
    pages = (total + size - 1) // size if total > 0 else 0
    
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="获取成功",
        data={
            "items": project_list,
            "total": total,
            "page": page,
            "size": size,
            "pages": pages,
            "hasNext": page < pages,
            "hasPrev": page > 1,
        },
    )


@router.get("/{project_id}", response_model=APIResponse)
async def get_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目详情（数据库）"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="项目不存在")

    # 使用序列化器统一转换为camelCase
    data = serialize_model(project, camel_case=True)
    
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="获取成功",
        data=data,
    )


@router.post("", response_model=APIResponse)
async def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建项目（写入数据库）"""
    owner_id = str(project_data.owner_id) if project_data.owner_id else str(current_user.id)

    project = Project(
        name=project_data.name,
        description=project_data.description,
        owner_id=owner_id,
        status="active",
        created_by=str(current_user.id),
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    data = {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "ownerId": project.owner_id,
        "status": project.status,
        "createdAt": project.created_at.isoformat() if project.created_at else "",
        "updatedAt": project.updated_at.isoformat() if project.updated_at else "",
        "createdBy": project.created_by or project.owner_id,
    }

    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="创建成功",
        data=data,
    )


@router.put("/{project_id}", response_model=APIResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新项目（数据库）"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="项目不存在")

    if project_data.name is not None:
        project.name = project_data.name
    if project_data.description is not None:
        project.description = project_data.description
    if project_data.status is not None:
        project.status = project_data.status

    db.commit()
    db.refresh(project)

    data = {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "ownerId": project.owner_id,
        "status": project.status,
        "createdAt": project.created_at.isoformat() if project.created_at else "",
        "updatedAt": project.updated_at.isoformat() if project.updated_at else "",
        "createdBy": project.created_by or project.owner_id,
    }

    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="更新成功",
        data=data,
    )


@router.delete("/{project_id}", response_model=APIResponse)
async def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除项目（数据库，级联删除测试用例等）"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="项目不存在")

    db.delete(project)
    db.commit()

    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="删除成功",
    )


@router.get("/{project_id}/modules", response_model=APIResponse)
async def get_project_modules(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目模块列表（数据库持久化，包含用例数量）"""
    from core.project_access import require_project_access
    require_project_access(db,current_user,project_id,"test_case:read")
    module_list, total_case_count = ModuleService.get_modules_with_case_count(db, project_id)
    
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="获取成功",
        data={
            "modules": module_list,
            "totalCaseCount": total_case_count
        }
    )


@router.post("/{project_id}/modules", response_model=APIResponse)
async def create_module(
    project_id: str,
    module_data: ModuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建模块（数据库持久化）"""
    try:
        module = ModuleService.create_module(
            db=db,
            project_id=project_id,
            module_data=module_data,
            current_user_id=str(current_user.id)
        )
        
        return APIResponse(
            status=ResponseStatus.SUCCESS,
            message="创建成功",
            data=serialize_model(module, camel_case=True)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("创建模块失败")
        raise HTTPException(status_code=400, detail=f"创建失败: {str(e)}")


@router.put("/{project_id}/modules/{module_id}", response_model=APIResponse)
async def update_module(
    project_id: str,
    module_id: str,
    module_data: ModuleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新模块（数据库持久化）"""
    from core.project_access import require_project_access
    from models.module import Module
    require_project_access(db,current_user,project_id,"test_case:update")
    if not db.query(Module).filter_by(id=module_id,project_id=project_id).first():
        raise HTTPException(404,"项目中不存在该模块")
    try:
        module = ModuleService.update_module(
            db=db, module_id=module_id, module_data=module_data,
            current_user_id=str(current_user.id)
        )
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        logger.exception("更新模块失败 module_id={}",module_id)
        raise
    
    if not module:
        raise HTTPException(status_code=404, detail="模块不存在")
    
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="更新成功",
        data=serialize_model(module, camel_case=True)
    )


@router.delete("/{project_id}/modules/{module_id}", response_model=APIResponse)
async def delete_module(
    project_id: str,
    module_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除模块（数据库持久化）"""
    success = ModuleService.delete_module(db=db, module_id=module_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="模块不存在")
    
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="删除成功"
    )


@router.get("/{project_id}/case-tree", response_model=APIResponse)
async def get_case_tree(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """兼容入口：返回当前项目的真实模块与用例。"""
    from api.v1.test_cases import get_case_tree as canonical
    return await canonical(project_id=project_id, db=db, current_user=current_user)


# 测试用例相关路由
@router.get("/{project_id}/cases", response_model=APIResponse)
async def get_test_cases(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = 1,
    size: int = 20,
    search: str = None,
    module_id: str = None,
    status: str = None,
    priority: str = None,
    type: str = None
):
    """兼容入口：返回真实用例与当前版本评审结果。"""
    from api.v1.test_cases import get_test_cases as canonical
    return await canonical(project_id=project_id, db=db, current_user=current_user,
                           page=page, size=size, search=search, module_id=module_id,
                           status=status, priority=priority, type=type)


@router.get("/{project_id}/cases/export")
async def export_test_cases(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    module_id: str = None,
    module_ids: str = None,  # 逗号分隔的模块 ID 列表（包含子模块）
    status: str = None,
    priority: str = None,
    type: str = None,
    search: str = None,
    case_ids: str = None,
    filters: str = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    mine: bool = False,
    followed: bool = False,
    tags: str = None,
    review_status: str = None,
    is_automated: bool = None,
    format: str = "xlsx",
    layout: str = "case",
    fields: str = None,
):
    """导出测试用例到Excel"""
    from core.project_access import require_project_access
    require_project_access(db, current_user, project_id, "test_case:export")
    from fastapi.responses import StreamingResponse
    from io import BytesIO
    from utils.excel_handler import export_to_excel
    from services.test_case_service import TestCaseService
    from uuid import UUID
    from models.module import Module
    
    try:
        # 使用服务层获取测试用例
        # 获取所有符合条件的用例（不分页）
        result = TestCaseService.get_test_cases(
            db=db,
            project_id=project_id,
            page=1,
            size=99999,  # 获取所有用例
            search=search,
            module_id=module_id,
            module_ids=module_ids,
            status=status,
            priority=priority,
            type=type,
            case_ids=case_ids, filters=filters,sort_by=sort_by,sort_order=sort_order,
            mine=mine,followed=followed,tags=tags,review_status=review_status,
            is_automated=is_automated,user_id=str(current_user.id),
        )
        
        cases = result["items"]
        if format not in {"xlsx","xmind"}:
            raise HTTPException(422,"不支持的导出格式")
        if format == "xmind":
            from services.case_interchange import export_xmind
            rows=db.query(Module).filter_by(project_id=project_id).all()
            by_id={m.id:m for m in rows}
            paths={}
            for module in rows:
                cursor,parts,seen=module,[],set()
                while cursor and cursor.id not in seen:
                    seen.add(cursor.id);parts.append(cursor.name);cursor=by_id.get(cursor.parent_id)
                paths[module.id]="/".join(reversed(parts))
            return StreamingResponse(BytesIO(export_xmind(cases,paths)),media_type="application/octet-stream",headers={"Content-Disposition":"attachment; filename=cases.xmind"})
        if layout not in {"case","step"}:
            raise HTTPException(422,"不支持的导出布局")
        
        # 获取模块信息用于显示模块路径
        modules = db.query(Module).filter(Module.project_id == project_id).all()
        # 构建模块映射：id -> Module对象
        module_dict = {str(m.id): m for m in modules}
        
        # 构建模块路径的函数
        def get_module_path(module_id: str) -> str:
            """递归构建模块的完整路径，格式：父模块/子模块"""
            if not module_id or module_id not in module_dict:
                return ""
            
            module = module_dict[module_id]
            path_parts = [module.name]
            
            # 递归向上查找父模块
            current_module = module
            while current_module.parent_id:
                parent_id = str(current_module.parent_id)
                if parent_id in module_dict:
                    parent_module = module_dict[parent_id]
                    path_parts.insert(0, parent_module.name)
                    current_module = parent_module
                else:
                    break
            
            return "/".join(path_parts)
        
        # 获取用户信息用于显示创建人和更新人
        from models import User
        user_ids = set()
        for case in cases:
            if case.created_by:
                user_ids.add(case.created_by)
            if case.updated_by:
                user_ids.add(case.updated_by)
        users = db.query(User).filter(User.id.in_(user_ids)).all() if user_ids else []
        user_map = {str(u.id): u.username or u.email or str(u.id) for u in users}
        
        # 准备导出数据，按照前端显示的字段顺序
        export_data = []
        for case in cases:
            # 格式化测试步骤
            steps_text = ""
            if case.steps:
                steps_list = []
                for i, step in enumerate(case.steps):
                    if isinstance(step, dict):
                        step_num = step.get('step', i + 1)
                        action = step.get('action', '')
                        expected = step.get('expected', '')
                        if expected:
                            steps_list.append(f"{step_num}. {action}\n   期望: {expected}")
                        else:
                            steps_list.append(f"{step_num}. {action}")
                    else:
                        steps_list.append(f"{i + 1}. {str(step)}")
                steps_text = "\n".join(steps_list)
            
            # 格式化标签
            tags_text = ""
            if case.tags:
                if isinstance(case.tags, list):
                    tags_text = ",".join(str(tag) for tag in case.tags)
                else:
                    tags_text = str(case.tags)
            
            # 获取模块路径（完整路径，如：模块a/模块b）
            module_path = ""
            if case.module_id:
                module_path = get_module_path(str(case.module_id))
            
            # 获取创建人和更新人
            created_by_name = user_map.get(case.created_by, "") if case.created_by else ""
            updated_by_name = user_map.get(case.updated_by, "") if case.updated_by else ""
            
            # 格式化日期时间
            created_at_str = ""
            if case.created_at:
                created_at_str = case.created_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(case.created_at, 'strftime') else str(case.created_at)
            
            updated_at_str = ""
            if case.updated_at:
                updated_at_str = case.updated_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(case.updated_at, 'strftime') else str(case.updated_at)
            
            # 按照前端显示的字段顺序组织数据
            export_data.append({
                "ID": case.case_code or str(case.id)[:8] if hasattr(case, 'id') else "",
                "用例名称": case.name or "",
                "用例等级": case.priority or "",
                "评审结果": result['reviewStatuses'].get(case.id,'not_reviewed'),
                "执行结果": case.status or "",
                "所属模块": module_path,
                "标签": tags_text,
                "是否自动化": "是" if getattr(case, 'is_automated', False) else "否",
                "创建人": created_by_name,
                "创建时间": created_at_str,
                "更新人": updated_by_name,
                "更新时间": updated_at_str,
                "用例类型": case.type or "",
                "前置条件": case.precondition or "",
                "测试步骤": steps_text,
                "需求关联": case.requirement_ref or "",
                "模板ID": case.template_id or "",
                "自定义字段": json.dumps(case.custom_fields or {},ensure_ascii=False),
            })
        
        if layout=='step':
            step_rows=[]
            for case,row in zip(cases,export_data):
                for index,step in enumerate(case.steps or [{}],1):
                    step_rows.append({**row,'步骤序号':step.get('step',index),'操作':step.get('action',''),'预期结果':step.get('expected','')})
            export_data=step_rows
        if fields:
            mapping={'caseCode':'ID','name':'用例名称','priority':'用例等级','reviewResult':'评审结果','status':'执行结果','modulePath':'所属模块','tags':'标签','isAutomated':'是否自动化','createdBy':'创建人','createdAt':'创建时间','updatedBy':'更新人','updatedAt':'更新时间','type':'用例类型','precondition':'前置条件','steps':'测试步骤','requirementRef':'需求关联','templateId':'模板ID','customFields':'自定义字段','step':'步骤序号','action':'操作','expected':'预期结果'}
            selected=list(dict.fromkeys(mapping.get(value.strip(),value.strip()) for value in fields.split(',') if value.strip()))
            allowed=set(mapping.values())-({'步骤序号','操作','预期结果'} if layout=='case' else set())
            if not selected or not set(selected)<=allowed: raise HTTPException(422,'导出字段不合法')
            export_data=[{key:row.get(key,'') for key in selected} for row in export_data]
        # 创建内存中的Excel文件
        from tempfile import NamedTemporaryFile
        import os
        
        # 创建临时文件
        with NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            # 导出到临时文件
            export_to_excel(export_data, tmp_path, "测试用例")
            
            # 读取文件内容到内存
            with open(tmp_path, 'rb') as f:
                file_content = f.read()
            
            # 删除临时文件
            os.unlink(tmp_path)
            
            # 创建文件流
            file_stream = BytesIO(file_content)
            
            # 生成文件名
            from datetime import datetime
            import urllib.parse
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"测试用例导出_{timestamp}.xlsx"
            
            # 使用 RFC 5987 编码文件名（支持中文）
            encoded_filename = urllib.parse.quote(filename, safe='')
            content_disposition = f"attachment; filename*=UTF-8''{encoded_filename}"
            
            # 返回文件流
            return StreamingResponse(
                file_stream,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={
                    "Content-Disposition": content_disposition
                }
            )
        except Exception as e:
            # 确保临时文件被删除
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            logger.exception("导出测试用例文件处理失败")
            raise e
            
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("导出测试用例失败")
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@router.get("/{project_id}/cases/template")
async def download_case_template(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """下载测试用例导入模板"""
    from core.project_access import require_project_access
    require_project_access(db, current_user, project_id, "test_case:read")
    from fastapi.responses import StreamingResponse
    from io import BytesIO
    from utils.excel_handler import export_to_excel
    from tempfile import NamedTemporaryFile
    import os
    import urllib.parse
    
    try:
        # 创建空的模板数据，只包含表头
        # 字段顺序与导出保持一致
        template_data = [{
            "ID": "",  # 用例编号，留空表示新增，填写表示更新
            "用例名称": "",
            "用例等级": "",
            "评审结果": "",
            "执行结果": "",
            "所属模块": "",  # 模块路径，如：模块a/模块b
            "标签": "",
            "是否自动化": "",
            "创建人": "",
            "创建时间": "",
            "更新人": "",
            "更新时间": "",
            "用例类型": "",
            "前置条件": "",
            "测试步骤": "",  # 格式：1. 步骤1\n   期望: 期望1\n2. 步骤2\n   期望: 期望2
            "期望结果": "",
        }]
        
        # 创建临时文件
        with NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            # 导出到临时文件
            export_to_excel(template_data, tmp_path, "测试用例")
            
            # 读取文件内容到内存
            with open(tmp_path, 'rb') as f:
                file_content = f.read()
            
            # 删除临时文件
            os.unlink(tmp_path)
            
            # 创建文件流
            file_stream = BytesIO(file_content)
            
            # 生成文件名
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"测试用例导入模板_{timestamp}.xlsx"
            
            # 使用 RFC 5987 编码文件名（支持中文）
            encoded_filename = urllib.parse.quote(filename, safe='')
            content_disposition = f"attachment; filename*=UTF-8''{encoded_filename}"
            
            # 返回文件流
            return StreamingResponse(
                file_stream,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={
                    "Content-Disposition": content_disposition
                }
            )
        except Exception as e:
            # 确保临时文件被删除
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            logger.exception("下载模板文件处理失败")
            raise e
            
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("下载模板失败")
        raise HTTPException(status_code=500, detail=f"下载模板失败: {str(e)}")


@router.post("/{project_id}/cases/import", response_model=APIResponse)
async def import_test_cases(
    project_id: str,
    file: UploadFile = File(...),
    validate_only: bool = False,  # 是否只校验不导入
    overwrite: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """导入测试用例（支持只校验模式）"""
    from core.project_access import require_project_access
    from services.case_governance import snapshot_case
    require_project_access(db, current_user, project_id, "test_case:import")
    from tempfile import NamedTemporaryFile
    import os
    import pandas as pd
    from utils.excel_handler import read_excel_file
    from models.test_case import TestCase
    from models.module import Module
    from services.test_case_service import TestCaseService
    from schemas.test_case import TestCaseCreate, TestCaseUpdate
    import json
    import re
    
    # 保存上传的文件
    suffix = Path(file.filename or '').suffix.lower()
    if suffix not in {'.csv','.xlsx','.xls','.xmind'}:
        raise HTTPException(422,'只支持Excel、CSV或XMind文件')
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_path = tmp_file.name
        content = await file.read()
        if len(content)>10*1024*1024:
            raise HTTPException(413,'导入文件超过10MiB')
        tmp_file.write(content)
    
    try:
        # 读取Excel文件
        # 编号按字符串读取，避免数字编号丢失前导零。
        if suffix == '.xmind':
            from services.case_interchange import read_xmind
            df=pd.DataFrame(read_xmind(content))
        else:
            df = pd.read_csv(tmp_path, dtype={"ID": str}) if suffix == '.csv' else pd.read_excel(tmp_path, dtype={"ID": str})
        
        # 验证必需的列
        required_columns = ["用例名称"]  # 至少需要用例名称
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"缺少必需的列: {', '.join(missing_columns)}"
            )
        
        # 获取项目下的所有模块，用于模块路径解析
        modules = db.query(Module).filter(Module.project_id == project_id).all()
        module_dict = {str(m.id): m for m in modules}
        pending_modules=[]
        if suffix=='.xmind':
            for value in df.get('所属模块',[]):
                parent_id=None
                for level,name in enumerate(str(value).split('/'),1):
                    if not name: continue
                    existing=next((m for m in modules if m.name==name and m.parent_id==parent_id),None)
                    if not existing:
                        existing=Module(id=str(uuid.uuid4()),project_id=project_id,name=name,parent_id=parent_id,level=level,sort_order=0)
                        modules.append(existing);pending_modules.append(existing)
                    parent_id=existing.id
        
        # 构建模块路径映射：路径 -> 模块ID
        def get_module_id_by_path(module_path: str) -> Optional[str]:
            """根据模块路径查找模块ID"""
            if not module_path or pd.isna(module_path):
                return None
            
            path_parts = str(module_path).split('/')
            if not path_parts:
                return None
            
            # 从根模块开始查找
            current_modules = [m for m in modules if m.parent_id is None]
            
            for part in path_parts:
                part = part.strip()
                found = None
                for m in current_modules:
                    if m.name == part:
                        found = m
                        break
                if not found:
                    return None
                current_modules = [m for m in modules if str(m.parent_id) == str(found.id)]
            
            return str(found.id) if found else None
        
        # 获取项目下的所有用例，用于ID校验
        existing_query = db.query(TestCase).filter(TestCase.project_id == project_id)
        existing_cases = (existing_query if validate_only else existing_query.with_for_update()).all()
        case_code_map = {case.case_code: case for case in existing_cases if case.case_code}
        case_id_map = {str(case.id): case for case in existing_cases}
        
        # 按模块分组现有用例
        cases_by_module = {}
        for case in existing_cases:
            module_id = str(case.module_id) if case.module_id else 'null'
            if module_id not in cases_by_module:
                cases_by_module[module_id] = []
            cases_by_module[module_id].append(case)
        
        # 解析测试步骤的函数
        def parse_steps(steps_text: str) -> List[Dict]:
            """解析测试步骤文本为结构化数据"""
            if not steps_text or pd.isna(steps_text):
                return []
            if str(steps_text).lstrip().startswith('['):
                try:
                    parsed=json.loads(steps_text)
                    if not isinstance(parsed,list) or any(not isinstance(s,dict) or not isinstance(s.get('action',''),str) or not isinstance(s.get('expected',''),str) for s in parsed):
                        raise ValueError('步骤格式不合法')
                    return parsed
                except ValueError as exc:
                    raise HTTPException(422,'步骤JSON格式不合法') from exc
            
            steps = []
            lines = str(steps_text).split('\n')
            current_step = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # 匹配步骤格式：1. 步骤内容 或 1. 步骤内容\n   期望: 期望内容
                step_match = re.match(r'^(\d+)\.\s*(.+)$', line)
                if step_match:
                    if current_step:
                        steps.append(current_step)
                    step_num = int(step_match.group(1))
                    action = step_match.group(2).strip()
                    current_step = {
                        'step': step_num,
                        'action': action,
                        'expected': ''
                    }
                elif current_step and line.startswith('期望:'):
                    current_step['expected'] = line.replace('期望:', '').strip()
            
            if current_step:
                steps.append(current_step)
            
            return steps if steps else []
        
        # 校验和解析每一行数据
        validation_errors = []
        import_data = []  # 存储解析后的数据
        
        for index, row in df.iterrows():
            row_num = index + 2  # Excel行号（第1行是表头）
            row_errors = []
            
            # 获取ID（用例编号）
            case_id = None
            if 'ID' in df.columns and not pd.isna(row.get('ID')):
                case_id = str(row['ID']).strip()
                if case_id:
                    # 检查ID是否存在
                    if case_id not in case_code_map:
                        row_errors.append(f"ID '{case_id}' 在数据库中不存在")
                    elif case_code_map[case_id].deleted_at:
                        row_errors.append(f"ID '{case_id}' 已在回收站，请先恢复后再导入")
            
            # 校验用例名称（必填）
            name = None
            if '用例名称' in df.columns and not pd.isna(row.get('用例名称')):
                name = str(row['用例名称']).strip()
                if not name:
                    row_errors.append("用例名称不能为空")
            else:
                row_errors.append("用例名称不能为空")
            
            # 解析其他字段
            priority = 'P2'
            if '用例等级' in df.columns and not pd.isna(row.get('用例等级')):
                priority_val = str(row['用例等级']).strip()
                if priority_val in ['P0', 'P1', 'P2', 'P3']:
                    priority = priority_val
                else:
                    row_errors.append(f"用例等级 '{priority_val}' 无效，应为 P0/P1/P2/P3")
            
            case_type = 'functional'
            if '用例类型' in df.columns and not pd.isna(row.get('用例类型')):
                type_val = str(row['用例类型']).strip()
                valid_types = ['functional', 'interface', 'ui', 'performance', 'security']
                if type_val in valid_types:
                    case_type = type_val
                else:
                    row_errors.append(f"用例类型 '{type_val}' 无效")
            
            status = 'not_executed'
            if '执行结果' in df.columns and not pd.isna(row.get('执行结果')):
                status_val = str(row['执行结果']).strip()
                valid_statuses = ['not_executed', 'passed', 'failed', 'blocked', 'skipped']
                if status_val in valid_statuses:
                    status = status_val
                else:
                    row_errors.append(f"执行结果 '{status_val}' 无效")
            
            # 解析模块路径
            module_id = None
            if '所属模块' in df.columns and not pd.isna(row.get('所属模块')):
                module_path = str(row['所属模块']).strip()
                if module_path:
                    module_id = get_module_id_by_path(module_path)
                    if not module_id:
                        row_errors.append(f"模块路径 '{module_path}' 不存在")
            
            # 解析标签
            tags = []
            if '标签' in df.columns and not pd.isna(row.get('标签')):
                tags_text = str(row['标签']).strip()
                if tags_text:
                    tags = [tag.strip() for tag in tags_text.split(',') if tag.strip()]
            
            # 解析测试步骤
            steps = []
            if '测试步骤' in df.columns and not pd.isna(row.get('测试步骤')):
                steps_text = str(row['测试步骤'])
                steps = parse_steps(steps_text)
            
            # 其他字段
            precondition = None
            if '前置条件' in df.columns and not pd.isna(row.get('前置条件')):
                precondition = str(row['前置条件']).strip() or None
            
            is_automated = False
            if '是否自动化' in df.columns and not pd.isna(row.get('是否自动化')):
                automated_val = str(row['是否自动化']).strip()
                is_automated = automated_val in ['是', 'true', 'True', '1', 'yes']
            extra_values={}
            for key,column in [('requirement_ref','需求关联'),('template_id','模板ID')]:
                if column in df.columns:
                    extra_values[key]=None if pd.isna(row.get(column)) else str(row[column]).strip() or None
            if '自定义字段' in df.columns:
                try:
                    extra_values['custom_fields']={} if pd.isna(row.get('自定义字段')) else json.loads(str(row['自定义字段']))
                except ValueError:
                    row_errors.append('自定义字段必须为JSON对象')
            try:
                from services.case_features import prepare_case_template
                existing_for_template=case_code_map.get(case_id) if case_id else None
                data_for_template={'type':case_type,'priority':priority,'precondition':precondition,'steps':steps,'tags':tags,'is_automated':is_automated,**extra_values}
                columns_for_template={'type':'用例类型','priority':'用例等级','precondition':'前置条件','steps':'测试步骤','tags':'标签','is_automated':'是否自动化'}
                explicit_fields=set(extra_values)|{field for field,column in columns_for_template.items() if column in df.columns}
                prepared=prepare_case_template(db,project_id,data_for_template,explicit_fields,existing=existing_for_template)
                extra_values.update({key:prepared[key] for key in ['template_id','custom_fields']})
                if existing_for_template is None:
                    extra_values.update({field:prepared[field] for field,column in columns_for_template.items() if column not in df.columns})
            except HTTPException as exc:
                row_errors.append(str(exc.detail))
            
            # 收集该行的所有错误
            if row_errors:
                validation_errors.append({
                    'row': row_num,
                    'id': case_id or '(新增)',
                    'name': name or '(未填写)',
                    'errors': row_errors
                })
            else:
                # 确定操作类型
                operation = 'create'
                existing_case = None
                values = {
                    'name': name, 'type': case_type, 'priority': priority,
                    'status': status, 'module_id': module_id, 'precondition': precondition,
                    'steps': steps, 'tags': tags, 'is_automated': is_automated,
                    **extra_values,
                }
                
                if case_id:
                    if case_id in case_code_map:
                        existing_case = case_code_map[case_id]
                        # 局部列导入只更新文件中存在的字段，不清空未提供的步骤等内容。
                        for field, column in {
                            'type':'用例类型', 'priority':'用例等级', 'status':'执行结果',
                            'module_id':'所属模块', 'precondition':'前置条件',
                            'steps':'测试步骤', 'tags':'标签', 'is_automated':'是否自动化',
                        }.items():
                            if column not in df.columns:
                                values[field] = getattr(existing_case, field)
                        # 检查内容是否有变化
                        has_changes = overwrite and any(getattr(existing_case, field) != value for field, value in values.items())
                        if has_changes:
                            operation = 'update'
                        else:
                            operation = 'no_change'
                    else:
                        # ID存在但数据库中不存在，已在上面报错
                        continue
                else:
                    operation = 'create'
                
                import_data.append({
                    'row': row_num,
                    'operation': operation,
                    'case_id': case_id,
                    'existing_case': existing_case,
                    'data': values
                })
        
        # 增量合并：上传文件里未出现的用例保持不变，删除必须单独显式操作。
        
        # 如果有校验错误，返回错误信息
        if validation_errors:
            error_messages = []
            for error in validation_errors:
                error_msg = f"第{error['row']}行 (ID: {error['id']}, 用例名称: {error['name']}): " + "; ".join(error['errors'])
                error_messages.append(error_msg)
            
            return APIResponse(
                status=ResponseStatus.ERROR,
                message="导入校验失败",
                data={
                    'total': len(df),
                    'validated': len(import_data),
                    'errors': len(validation_errors),
                    'error_details': error_messages,
                    'validation_errors': validation_errors
                }
            )
        
        # 如果只是校验模式，返回校验结果
        if validate_only:
            return APIResponse(
                status=ResponseStatus.SUCCESS,
                message="校验通过",
                data={
                    'total': len(df),
                    'validated': len(import_data),
                    'errors': 0,
                    'error_details': [],
                    'validation_errors': [],
                    'preview': {
                        'to_create': len([item for item in import_data if item['operation'] == 'create']),
                        'to_update': len([item for item in import_data if item['operation'] == 'update']),
                        'to_delete': 0,
                        'no_change': len([item for item in import_data if item['operation'] == 'no_change'])
                    }
                }
            )
        
        # 所有校验通过，执行导入操作
        created_count = 0
        updated_count = 0
        deleted_count = 0
        
        try:
            db.add_all(pending_modules)
            db.flush()
            # 执行新增和更新
            for item in import_data:
                if item['operation'] == 'create':
                    # 生成case_code
                    import time
                    timestamp = int(time.time() * 1000) % 1000000
                    case_code = f"{timestamp:06d}"
                    while db.query(TestCase).filter(TestCase.case_code == case_code).first():
                        timestamp = (timestamp + 1) % 1000000
                        case_code = f"{timestamp:06d}"
                    
                    new_case = TestCase(
                        id=str(uuid.uuid4()),
                        project_id=project_id,
                        module_id=item['data']['module_id'],
                        case_code=case_code,
                        name=item['data']['name'],
                        type=item['data']['type'],
                        priority=item['data']['priority'],
                        precondition=item['data']['precondition'],
                        steps=item['data']['steps'] or [],
                        tags=item['data']['tags'],
                        status=item['data']['status'],
                        is_automated=item['data']['is_automated'],
                        created_by=str(current_user.id),
                        updated_by=str(current_user.id)
                    )
                    for field,value in item['data'].items():
                        setattr(new_case,field,value)
                    db.add(new_case)
                    db.flush()
                    snapshot_case(db, new_case, str(current_user.id), "导入新增用例")
                    created_count += 1
                    
                elif item['operation'] == 'update':
                    existing_case = item['existing_case']
                    snapshot_case(db, existing_case, str(current_user.id), "导入更新前保存版本")
                    existing_case.name = item['data']['name']
                    existing_case.type = item['data']['type']
                    existing_case.priority = item['data']['priority']
                    existing_case.status = item['data']['status']
                    existing_case.module_id = item['data']['module_id']
                    existing_case.precondition = item['data']['precondition']
                    existing_case.steps = item['data']['steps'] or []
                    existing_case.tags = item['data']['tags']
                    existing_case.is_automated = item['data']['is_automated']
                    existing_case.updated_by = str(current_user.id)
                    for field,value in item['data'].items():
                        setattr(existing_case,field,value)
                    from utils.datetime_utils import beijing_now
                    existing_case.updated_at=beijing_now()
                    snapshot_case(db, existing_case, str(current_user.id), "导入更新用例")
                    updated_count += 1
            
            db.commit()
            logger.info("用例增量导入完成 project_id={} created={} updated={} deleted=0", project_id, created_count, updated_count)
            
            return APIResponse(
                status=ResponseStatus.SUCCESS,
                message="导入成功",
                data={
                    'total': len(df),
                    'created': created_count,
                    'updated': updated_count,
                    'deleted': deleted_count,
                    'no_change': len([item for item in import_data if item['operation'] == 'no_change'])
                }
            )
            
        except HTTPException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            logger.exception("导入用例失败")
            raise HTTPException(status_code=500, detail=f"导入失败: {str(e)}")
    
    finally:
        # 清理临时文件
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@router.get("/{project_id}/cases/{case_id}", response_model=APIResponse)
async def get_test_case(
    project_id: str,
    case_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """兼容入口：按项目读取真实用例。"""
    from api.v1.test_cases import get_test_case as canonical
    return await canonical(case_id=case_id, project_id=project_id, db=db, current_user=current_user)


@router.post("/{project_id}/cases", response_model=APIResponse)
async def create_test_case(
    project_id: str,
    case_data: TestCaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """兼容入口：同一服务事务创建用例及初始版本。"""
    from api.v1.test_cases import create_test_case as canonical
    if str(case_data.project_id) != project_id:
        raise HTTPException(422, "请求中的项目与路径不一致")
    return await canonical(case_data=case_data, db=db, current_user=current_user)


@router.put("/{project_id}/cases/{case_id}", response_model=APIResponse)
async def update_test_case(
    project_id: str,
    case_id: str,
    case_data: TestCaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """兼容入口：验证项目后保存用例与版本。"""
    from services.case_governance import case_for_project
    from api.v1.test_cases import update_test_case as canonical
    case_for_project(db, project_id, case_id)
    return await canonical(case_id=case_id, case_data=case_data, db=db, current_user=current_user)


@router.delete("/{project_id}/cases/{case_id}", response_model=APIResponse)
async def delete_test_case(
    project_id: str,
    case_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """兼容入口：显式删除用例并保留版本。"""
    from services.case_governance import case_for_project
    from api.v1.test_cases import delete_test_case as canonical
    case_for_project(db, project_id, case_id)
    return await canonical(case_id=case_id, db=db, current_user=current_user)
