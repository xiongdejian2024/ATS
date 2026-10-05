"""测试用例相关 API（独立 URL 前缀）"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.common import APIResponse, ResponseStatus
from schemas.test_case import TestCaseCreate, TestCaseUpdate
from api.deps import get_current_user
from models import User
from services.test_case_service import TestCaseService
from utils.serializer import serialize_model, serialize_list
from core.logger import logger
from services.suite_dispatch import is_xat_command
from core.project_access import require_project_access


router = APIRouter()


@router.get("", response_model=APIResponse)
async def get_test_cases(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = 1,
    size: int = 20,
    search: Optional[str] = None,
    module_id: Optional[str] = None,
    module_ids: Optional[str] = None,  # 逗号分隔的模块 ID 列表（包含子模块）
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
    case_ids: Optional[str] = None,
):
    """获取测试用例列表（按项目过滤，使用数据库持久化）"""
    try:
        require_project_access(db, current_user, project_id, "test_case:read")
        result = TestCaseService.get_test_cases(
            db=db,
            project_id=project_id,
            page=page,
            size=size,
            search=search,
            module_id=module_id,
            module_ids=module_ids,  # 传递多个模块 ID
            status=status,
            priority=priority,
            type=type,
            tags=tags,
            is_automated=is_automated,
            requirement_ref=requirement_ref,
            precondition=precondition,
            review_status=review_status,
            filters=filters, sort_by=sort_by, sort_order=sort_order,
            mine=mine, followed=followed, user_id=str(current_user.id), case_ids=case_ids,
        )

        # 序列化items为camelCase
        serialized_items = serialize_list(result["items"], camel_case=True)
        for item in serialized_items:
            item["reviewResult"] = result["reviewStatuses"].get(str(item["id"]), "not_reviewed")
        
        return APIResponse(
            status=ResponseStatus.SUCCESS,
            message="获取成功",
            data={
                "items": serialized_items,
                "total": result["total"],
                "page": result["page"],
                "size": result["size"],
                "pages": result["pages"],
                "hasNext": result["hasNext"],
                "hasPrev": result["hasPrev"],
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"获取测试用例列表失败: project_id={project_id}")
        raise HTTPException(status_code=500, detail=f"获取测试用例列表失败: {str(e)}")


# 注意：/tree 和 /filter-fields 必须在 /{case_id} 之前定义，否则会被错误匹配
@router.get("/tree", response_model=APIResponse)
async def get_case_tree(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取用例树（包含模块和用例）"""
    try:
        require_project_access(db, current_user, project_id, "test_case:read")
        tree_data = TestCaseService.get_case_tree(db=db, project_id=project_id)

        return APIResponse(
            status=ResponseStatus.SUCCESS,
            message="获取成功",
            data=tree_data,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"获取用例树失败: project_id={project_id}")
        raise HTTPException(status_code=500, detail=f"获取用例树失败: {str(e)}")


@router.get("/filter-fields", response_model=APIResponse)
async def get_filter_fields(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取测试用例筛选字段配置"""
    try:
        require_project_access(db, current_user, project_id, "test_case:read")
        from services.filter_field_service import FilterFieldService
        from utils.serializer import serialize_list

        filter_fields = FilterFieldService.get_project_fields(project_id, db)

        # 序列化为camelCase
        serialized_fields = serialize_list(filter_fields, camel_case=True)
        
        return APIResponse(
            status=ResponseStatus.SUCCESS,
            message="获取成功",
            data=serialized_fields,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"获取筛选字段配置失败: project_id={project_id}")
        raise HTTPException(status_code=500, detail=f"获取筛选字段配置失败: {str(e)}")


@router.get("/{case_id}", response_model=APIResponse)
async def get_test_case(
    case_id: str,
    project_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取测试用例详情"""
    try:
        test_case = TestCaseService.get_test_case(db=db, case_id=case_id)

        if not test_case:
            raise HTTPException(status_code=404, detail="测试用例不存在")

        if project_id and project_id != test_case.project_id:
            raise HTTPException(status_code=404, detail="项目中不存在该用例")
        require_project_access(db, current_user, test_case.project_id, "test_case:read")

        # 序列化为camelCase
        serialized_case = serialize_model(test_case, camel_case=True)
        
        return APIResponse(
            status=ResponseStatus.SUCCESS,
            message="获取成功",
            data=serialized_case,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"获取测试用例详情失败: case_id={case_id}")
        raise HTTPException(status_code=500, detail=f"获取测试用例失败: {str(e)}")


@router.post("", response_model=APIResponse)
async def create_test_case(
    case_data: TestCaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建测试用例（使用数据库持久化）"""
    try:
        require_project_access(db, current_user, str(case_data.project_id), "test_case:create")
        # 确保steps不为None
        if case_data.steps is None:
            case_data.steps = []

        test_case = TestCaseService.create_test_case(
            db=db,
            case_data=case_data,
            current_user_id=str(current_user.id),
        )

        # 序列化为camelCase
        serialized_case = serialize_model(test_case, camel_case=True)
        
        return APIResponse(
            status=ResponseStatus.SUCCESS,
            message="创建成功",
            data=serialized_case,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("创建测试用例失败")
        raise HTTPException(status_code=400, detail=f"创建失败: {str(e)}")


@router.put("/{case_id}", response_model=APIResponse)
async def update_test_case(
    case_id: str,
    case_data: TestCaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """更新测试用例"""
    try:
        existing = TestCaseService.get_test_case(db, case_id)
        if not existing:
            raise HTTPException(404, "测试用例不存在")
        require_project_access(db, current_user, existing.project_id, "test_case:update")
        test_case = TestCaseService.update_test_case(
            db=db,
            case_id=case_id,
            case_data=case_data,
            current_user_id=str(current_user.id)
        )

        if not test_case:
            raise HTTPException(status_code=404, detail="测试用例不存在")

        # 序列化为camelCase
        serialized_case = serialize_model(test_case, camel_case=True)
        
        return APIResponse(
            status=ResponseStatus.SUCCESS,
            message="更新成功",
            data=serialized_case,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"更新测试用例失败: case_id={case_id}")
        raise HTTPException(status_code=500, detail=f"更新测试用例失败: {str(e)}")


@router.delete("/{case_id}", response_model=APIResponse)
async def delete_test_case(
    case_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除测试用例"""
    try:
        existing = TestCaseService.get_test_case(db, case_id)
        if not existing:
            raise HTTPException(404, "测试用例不存在")
        require_project_access(db, current_user, existing.project_id, "test_case:delete")
        success = TestCaseService.delete_test_case(db=db, case_id=case_id, current_user_id=str(current_user.id))

        if not success:
            raise HTTPException(status_code=404, detail="测试用例不存在")

        return APIResponse(
            status=ResponseStatus.SUCCESS,
            message="删除成功",
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"删除测试用例失败: case_id={case_id}")
        raise HTTPException(status_code=500, detail=f"删除测试用例失败: {str(e)}")



@router.post('/{case_id}/execute')
async def execute_case(case_id: str, body: dict, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    from models import TestCase
    from models.test_suite import TestSuite
    from models.test_plan import TestPlan
    from services.access import require_project
    from services.environment_service import EnvironmentService
    from services.test_suite_service import TestSuiteService
    from api.v1.test_suites import execute_test_suite
    case=db.get(TestCase,case_id)
    template=db.get(TestSuite,body.get('suiteId',''))
    if not case or case.deleted_at or not template: raise HTTPException(404,'用例或执行模板不存在')
    require_project(db,current_user,case.project_id,'test_plan','execute')
    plan=db.get(TestPlan,template.plan_id)
    if plan.project_id!=case.project_id or case_id not in template.case_ids:
        raise HTTPException(422,'所选模板必须属于同项目并包含该用例')
    if not case.is_automated: raise HTTPException(422,'仅自动化用例可由Agent执行')
    if not is_xat_command(template.execution_command):
        raise HTTPException(422,'单用例选择支持 xat/ats-sat 模板，其他命令不能保证只运行所选用例')
    environment=EnvironmentService.get_environment(db,template.environment_id)
    if not environment or not environment.get('isOnline'): raise HTTPException(503,'模板执行环境未在线')
    values={field:getattr(template,field) for field in ['git_enabled','git_repo_url','git_branch','git_token','environment_id','execution_command']}
    values.update(name='单用例：'+case.name[:200],case_ids=[case_id],description='基于既有模板 '+template.id)
    suite=TestSuiteService.create_test_suite(db,template.plan_id,values,str(current_user.id))
    return await execute_test_suite(suite.id,db,current_user)
