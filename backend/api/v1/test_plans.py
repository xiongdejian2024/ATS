# -*- coding: utf-8 -*-
"""测试计划相关 API（独立 URL 前缀）- 使用数据库存储"""
from typing import Optional, List
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.common import APIResponse, ResponseStatus
from api.deps import get_current_user
from models import User
from services.test_plan_service import TestPlanService
from utils.serializer import serialize_model, serialize_list
from core.logger import logger
from api.v1.plan_orchestration import require_plan
from core.project_access import require_project_access
from models.plan_orchestration import PlanRun, PlanSettings
from models.test_case import TestCase
from models.test_plan import PlanCaseRelation
from schemas.plan_orchestration import ManualResultInput
from services.plan_orchestration import record_manual_result
from services.plan_workspace import apply_tree_statistics
from services.plan_orchestration import start_plan_run, cancel_plan_run, run_data, run_logs, get_policy, ACTIVE


router = APIRouter()


def validate_plan_cases(db, project_id, case_ids):
    if not isinstance(case_ids, list) or len(case_ids) != len(set(case_ids)):
        raise HTTPException(400, "用例必须为不重复的列表")
    cases = db.query(TestCase).filter(TestCase.id.in_(case_ids), TestCase.deleted_at.is_(None)).all()
    if len(cases) != len(case_ids) or any(c.project_id != project_id for c in cases):
        raise HTTPException(400, "选择的用例不存在或不属于当前项目")


def record_active_manual_result(db, plan_id, case_id, execution_status, user_id):
    if not db.query(PlanCaseRelation).filter_by(plan_id=plan_id, case_id=case_id).first():
        raise HTTPException(404, "用例关联不存在")
    mapping = {"pass": "passed", "fail": "failed", "error": "error", "broken": "error", "skip": "skipped"}
    if execution_status not in {"pending", *mapping}:
        raise HTTPException(400, "无效的用例执行状态")
    run = db.query(PlanRun).filter(PlanRun.plan_id == plan_id, PlanRun.status.in_(ACTIVE)).first()
    if run:
        if execution_status == "pending":
            raise HTTPException(409, "执行批次中不能重置已回填结果")
        try:
            record_manual_result(db, run.id, case_id, ManualResultInput(result=mapping[execution_status]), str(user_id))
        except ValueError as exc:
            logger.exception("回填活动计划批次失败：计划={}，用例={}", plan_id, case_id)
            raise HTTPException(409, str(exc)) from exc


@router.get("", response_model=APIResponse)
async def get_test_plans(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = 1,
    size: int = 20,
    search: Optional[str] = None,
    status: Optional[str] = None,
    type: Optional[str] = None,  # 前端使用的参数名
    plan_type: Optional[str] = None,  # 备用参数名
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    owner_id: Optional[str] = None,
    group_id: Optional[str] = None,
    module_id: Optional[str] = None,
    include_descendants: bool = False,
    archived: Optional[bool] = False,
    followed: bool = False,
    tag: Optional[str] = None,
):
    """获取测试计划列表（按项目过滤）"""
    try:
        # 保存内置 type 函数的引用，避免被覆盖
        import builtins
        type_func = builtins.type
        
        logger.debug(f"获取测试计划列表 - project_id: {project_id}, project_id_type: {type_func(project_id)}, page: {page}, size: {size}")
        
        # 使用 plan_type 或 type 参数（优先使用 plan_type，避免覆盖内置函数）
        # 注意：这里的 type 是函数参数名，不是内置函数
        actual_plan_type = plan_type if plan_type is not None else type
        
        if not project_id:
            logger.warning("错误: project_id 参数为空")
            return APIResponse(
                status=ResponseStatus.SUCCESS,
                message="获取成功",
                data={
                    "items": [],
                    "total": 0,
                    "page": page,
                    "size": size,
                    "pages": 0,
                    "hasNext": False,
                    "hasPrev": False,
                },
            )
        
        require_project_access(db, current_user, project_id, "test_plan:read")
        result = TestPlanService.get_test_plans(
            db=db,
            project_id=project_id,
            page=page,
            size=size,
            search=search,
            status=status,
            plan_type=actual_plan_type,  # 使用实际的值
            owner_id=owner_id,
            group_id=group_id, start_date=start_date, end_date=end_date, module_id=module_id,
            archived=archived, followed_by=current_user.id if followed else None, tag=tag,
            include_descendants=include_descendants,
        )

        logger.debug(f"Service返回结果 - 总数: {result['total']}, 项目数: {len(result['items'])}")

        # 序列化返回数据
        items = serialize_list(result["items"], camel_case=True)
        logger.debug(f"序列化后项目数: {len(items)}")
        
        # 为每个计划添加统计信息
        for item in items:
            plan_id = item.get("id")
            item["executionPolicy"] = get_policy(db, plan_id)
            from services.plan_workspace import metadata
            item.update(metadata(db, plan_id, current_user.id))
            try:
                cases = TestPlanService.get_plan_cases(db, plan_id)
                item["totalCases"] = len(cases)
                # 计算已执行的用例数（非pending状态）
                item["executedCases"] = sum(
                    1 for case in cases 
                    if case.get("executionStatus") and case.get("executionStatus") != "pending"
                )
                # 统计各状态的用例数量
                item["caseStatusCounts"] = {
                    "pending": sum(1 for case in cases if case.get("executionStatus") == "pending" or not case.get("executionStatus")),
                    "pass": sum(1 for case in cases if case.get("executionStatus") == "pass"),
                    "fail": sum(1 for case in cases if case.get("executionStatus") == "fail"),
                    "broken": sum(1 for case in cases if case.get("executionStatus") == "broken"),
                    "error": sum(1 for case in cases if case.get("executionStatus") == "error"),
                    "skip": sum(1 for case in cases if case.get("executionStatus") == "skip")
                }
            except Exception as e:
                logger.exception(f"获取计划 {plan_id} 的用例失败")
                item["totalCases"] = 0
                item["executedCases"] = 0
                item["caseStatusCounts"] = {
                    "pending": 0,
                    "pass": 0,
                    "fail": 0,
                    "broken": 0,
                    "error": 0,
                    "skip": 0
                }

        response_data = {
            "items": items,
            "total": result["total"],
            "page": result["page"],
            "size": result["size"],
            "pages": result["pages"],
            "hasNext": result["hasNext"],
            "hasPrev": result["hasPrev"],
        }
        
        logger.debug(f"返回数据 - items数量: {len(response_data['items'])}, total: {response_data['total']}")

        for item in items:
            apply_tree_statistics(db, item["id"], item)

        return APIResponse(
            status=ResponseStatus.SUCCESS,
            message="获取成功",
            data=response_data,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("获取测试计划列表失败")
        raise HTTPException(500, "获取测试计划列表失败") from e


@router.get("/{plan_id}", response_model=APIResponse)
async def get_test_plan(
    plan_id: str,
    project_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取测试计划详情"""
    require_plan(db, current_user, plan_id, "read")
    plan = TestPlanService.get_test_plan(db, plan_id)
    
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="测试计划不存在")

    if project_id and plan.project_id != project_id:
        raise HTTPException(404, "此项目中不存在该计划")

    plan_data = serialize_model(plan, camel_case=True)
    
    # 添加关联的测试用例（已包含执行状态）
    cases = TestPlanService.get_plan_cases(db, plan_id)
    # cases已经是字典格式，直接使用
    plan_data["testCases"] = cases
    plan_data["totalCases"] = len(cases)
    # 计算已执行的用例数（非pending状态）
    plan_data["executedCases"] = sum(
        1 for case in cases 
        if case.get("executionStatus") and case.get("executionStatus") != "pending"
    )
    # 统计各状态的用例数量
    plan_data["caseStatusCounts"] = {
        "pending": sum(1 for case in cases if case.get("executionStatus") == "pending" or not case.get("executionStatus")),
        "pass": sum(1 for case in cases if case.get("executionStatus") == "pass"),
        "fail": sum(1 for case in cases if case.get("executionStatus") == "fail"),
        "broken": sum(1 for case in cases if case.get("executionStatus") == "broken"),
        "error": sum(1 for case in cases if case.get("executionStatus") == "error"),
        "skip": sum(1 for case in cases if case.get("executionStatus") == "skip")
    }
    apply_tree_statistics(db, plan_id, plan_data)
    from core.project_access import project_allows
    from models import Project
    from services.plan_detail import category_counts
    project = db.get(Project, plan.project_id)
    plan_data["categoryCounts"] = category_counts(db, plan_id, cases)
    plan_data["capabilities"] = {key: project_allows(db, current_user, project, "test_plan:" + action)
                                 for key, action in (("edit", "update"), ("execute", "execute"), ("copy", "create"), ("delete", "delete"))}
    # 确保 plan_data 包含 projectId（用于前端加载模块列表）
    if "projectId" not in plan_data and plan.project_id:
        plan_data["projectId"] = str(plan.project_id)

    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="获取成功",
        data=plan_data,
    )


@router.post("", response_model=APIResponse)
async def create_test_plan(
    plan_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建测试计划"""
    try:
        logger.debug(f"收到创建测试计划请求: {plan_data}")
        
        project_id = plan_data.get("project_id")
        if not project_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="project_id 不能为空")

        require_project_access(db, current_user, project_id, "test_plan:create")

        validate_plan_cases(db, project_id, plan_data.get("testCaseIds", []))
        # 验证必填字段
        if not plan_data.get("name"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="计划名称不能为空")
        
        if not plan_data.get("startDate"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="开始日期不能为空")

        plan = TestPlanService.create_test_plan(
            db=db,
            project_id=project_id,
            plan_data=plan_data,
            current_user_id=str(current_user.id)
        )

        return APIResponse(
            status=ResponseStatus.SUCCESS,
            message="创建成功",
            data=serialize_model(plan, camel_case=True),
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("创建测试计划失败")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"创建失败: {str(e)}")


@router.put("/{plan_id}", response_model=APIResponse)
async def update_test_plan(
    plan_id: str,
    plan_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """更新测试计划"""
    require_plan(db, current_user, plan_id, "update")
    if db.query(PlanRun).filter(PlanRun.plan_id == plan_id, PlanRun.status.in_(ACTIVE)).first():
        raise HTTPException(409, "计划批次仍在执行，请先完成或取消")
    if "testCaseIds" in plan_data:
        plan = require_plan(db, current_user, plan_id, "update")
        validate_plan_cases(db, plan.project_id, plan_data["testCaseIds"])
    try:
        plan = TestPlanService.update_test_plan(
            db=db,
            plan_id=plan_id,
            plan_data=plan_data,
            current_user_id=str(current_user.id)
        )

        if not plan:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="测试计划不存在")

        # 序列化计划数据
        plan_data_response = serialize_model(plan, camel_case=True)
        
        # 添加关联的测试用例（与 get_test_plan 保持一致）
        cases = TestPlanService.get_plan_cases(db, plan_id)
        plan_data_response["testCases"] = cases
        plan_data_response["totalCases"] = len(cases)
        plan_data_response["executedCases"] = sum(
            1 for case in cases 
            if case.get("executionStatus") and case.get("executionStatus") != "pending"
        )
        plan_data_response["caseStatusCounts"] = {
            "pending": sum(1 for case in cases if case.get("executionStatus") == "pending" or not case.get("executionStatus")),
            "pass": sum(1 for case in cases if case.get("executionStatus") == "pass"),
            "fail": sum(1 for case in cases if case.get("executionStatus") == "fail"),
            "broken": sum(1 for case in cases if case.get("executionStatus") == "broken"),
            "error": sum(1 for case in cases if case.get("executionStatus") == "error"),
            "skip": sum(1 for case in cases if case.get("executionStatus") == "skip")
        }
        if "projectId" not in plan_data_response and plan.project_id:
            plan_data_response["projectId"] = str(plan.project_id)

        return APIResponse(
            status=ResponseStatus.SUCCESS,
            message="更新成功",
            data=plan_data_response,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("更新测试计划失败")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"更新失败: {str(e)}")


@router.delete("/{plan_id}", response_model=APIResponse)
async def delete_test_plan(
    plan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除测试计划"""
    require_plan(db, current_user, plan_id, "delete")
    if db.query(PlanRun).filter(PlanRun.plan_id == plan_id, PlanRun.status.in_(ACTIVE)).first():
        raise HTTPException(409, "计划批次仍在执行，请先完成或取消")
    success = TestPlanService.delete_test_plan(db, plan_id)
    
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="测试计划不存在")

    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="删除成功",
    )


@router.get("/{plan_id}/cases", response_model=APIResponse)
async def get_plan_cases(
    plan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取计划关联的用例列表"""
    require_plan(db, current_user, plan_id, "read")
    cases = TestPlanService.get_plan_cases(db, plan_id)

    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="获取成功",
        data=cases,
    )


@router.post("/{plan_id}/cases", response_model=APIResponse)
async def add_cases_to_plan(
    plan_id: str,
    case_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """向计划添加用例"""
    require_plan(db, current_user, plan_id, "update")
    if db.query(PlanRun).filter(PlanRun.plan_id == plan_id, PlanRun.status.in_(ACTIVE)).first():
        raise HTTPException(409, "计划批次仍在执行，请先完成或取消")
    case_ids = case_data.get("caseIds", [])
    
    if not case_ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="caseIds 不能为空")

    plan = require_plan(db, current_user, plan_id, "update")
    validate_plan_cases(db, plan.project_id, case_ids)
    TestPlanService.add_cases_to_plan(db, plan_id, case_ids)

    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="添加成功",
    )


@router.delete("/{plan_id}/cases", response_model=APIResponse)
async def remove_cases_from_plan(
    plan_id: str,
    case_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """从计划移除用例"""
    require_plan(db, current_user, plan_id, "update")
    if db.query(PlanRun).filter(PlanRun.plan_id == plan_id, PlanRun.status.in_(ACTIVE)).first():
        raise HTTPException(409, "计划批次仍在执行，请先完成或取消")
    case_ids = case_data.get("caseIds", [])
    
    if not case_ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="caseIds 不能为空")

    TestPlanService.remove_cases_from_plan(db, plan_id, case_ids)

    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="移除成功",
    )


@router.post("/{plan_id}/pause", response_model=APIResponse)
async def pause_plan(
    plan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """兼容暂停入口：活动批次实际发送取消，保留全部历史结果。"""
    plan = require_plan(db, current_user, plan_id, "execute")
    runs = db.query(PlanRun).filter(PlanRun.plan_id == plan_id, PlanRun.status.in_(ACTIVE)).all()
    if runs:
        for run in runs:
            await cancel_plan_run(db, run.id, str(current_user.id))
    else:
        plan.status = "paused"
        db.commit()
    return APIResponse(status=ResponseStatus.SUCCESS, message="已请求停止执行")


@router.post("/{plan_id}/resume", response_model=APIResponse)
async def resume_plan(
    plan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """再次执行创建新批次，取消的历史批次保持不变。"""
    require_plan(db, current_user, plan_id, "execute")
    try:
        run = await start_plan_run(db, plan_id, str(current_user.id), notes="重新执行计划")
    except ValueError as exc:
        logger.exception("重新执行计划失败：计划={}", plan_id)
        db.rollback()
        raise HTTPException(409, str(exc)) from exc
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        logger.exception("启动计划执行发生异常：计划={}", plan_id)
        db.rollback()
        raise
    return APIResponse(status=ResponseStatus.SUCCESS, message="新的执行批次已创建", data=run_data(db, run))


@router.post("/{plan_id}/complete", response_model=APIResponse)
async def complete_plan(
    plan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """完成计划"""
    require_plan(db, current_user, plan_id, "update")
    if db.query(PlanRun).filter(PlanRun.plan_id == plan_id, PlanRun.status.in_(ACTIVE)).first():
        raise HTTPException(409, "计划批次仍在执行，请先完成或取消")
    plan = TestPlanService.update_plan_status(db, plan_id, "completed")
    
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="测试计划不存在")

    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="完成成功",
    )


@router.post("/{plan_id}/execute", response_model=APIResponse)
async def execute_plan(
    plan_id: str,
    execution_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建真实执行批次，后台调度通过原 Agent 队列执行。"""
    require_plan(db, current_user, plan_id, "execute")
    try:
        run = await start_plan_run(db, plan_id, str(current_user.id),
            suite_ids=execution_data.get("suiteIds"), notes=execution_data.get("notes"),
            idempotency_key=execution_data.get("idempotencyKey"))
    except ValueError as exc:
        logger.exception("启动计划执行失败：计划={}", plan_id)
        db.rollback()
        raise HTTPException(409, str(exc)) from exc
    return APIResponse(status=ResponseStatus.SUCCESS, message="执行批次已创建", data=run_data(db, run))



@router.post("/{plan_id}/stop", response_model=APIResponse)
async def stop_plan_execution(
    plan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """取消当前批次；不提前释放仍在执行的 Agent 槽位。"""
    require_plan(db, current_user, plan_id, "execute")
    runs = db.query(PlanRun).filter(PlanRun.plan_id == plan_id, PlanRun.status.in_(ACTIVE)).all()
    for run in runs:
        await cancel_plan_run(db, run.id, str(current_user.id))
    return APIResponse(status=ResponseStatus.SUCCESS, message="已请求停止", data={"runIds": [r.id for r in runs]})


@router.get("/{plan_id}/executions", response_model=APIResponse)
async def get_plan_executions(
    plan_id: str,
    page: int = 1,
    size: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """返回真实执行批次与汇总，不使用最新状态拼装历史。"""
    require_plan(db, current_user, plan_id)
    page, size = max(1, page), min(100, max(1, size))
    query = db.query(PlanRun).filter_by(plan_id=plan_id)
    total = query.count()
    items = query.order_by(PlanRun.created_at.desc()).offset((page - 1) * size).limit(size).all()
    return APIResponse(status=ResponseStatus.SUCCESS, message="获取成功", data={
        "items": [run_data(db, run) for run in items], "total": total, "page": page, "size": size})


@router.get("/{plan_id}/executions/{run_id}/logs", response_model=APIResponse)
async def get_plan_run_logs(plan_id: str, run_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    require_plan(db, current_user, plan_id)
    run = db.get(PlanRun, run_id)
    if not run or run.plan_id != plan_id:
        raise HTTPException(404, "执行批次不存在")
    return APIResponse(status=ResponseStatus.SUCCESS, message="获取成功", data={"executionLog": run_logs(db, run)})


@router.post("/{plan_id}/clone", response_model=APIResponse)
async def clone_plan(
    plan_id: str,
    clone_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """克隆计划"""
    project_id = clone_data.get("project_id")
    if not project_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="project_id 不能为空")

    source_plan = require_plan(db, current_user, plan_id)
    require_project_access(db, current_user, project_id, "test_plan:create")
    if source_plan.project_id != project_id:
        raise HTTPException(400, "复制计划仅支持同项目，跨项目请重新选择用例")
    new_plan = TestPlanService.clone_plan(
        db=db,
        plan_id=plan_id,
        project_id=project_id,
        current_user_id=str(current_user.id)
    )

    if not new_plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="源测试计划不存在")

    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="克隆成功",
        data=serialize_model(new_plan, camel_case=True),
    )


@router.put("/{plan_id}/cases/{case_id}/status", response_model=APIResponse)
async def update_case_execution_status(
    plan_id: str,
    case_id: str,
    status_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """更新用例执行状态"""
    require_plan(db, current_user, plan_id, "execute")
    execution_status = status_data.get("status")
    if not execution_status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="status 不能为空")

    record_active_manual_result(db, plan_id, case_id, execution_status, current_user.id)
    success = TestPlanService.update_case_execution_status(
        db=db,
        plan_id=plan_id,
        case_id=case_id,
        status=execution_status
    )

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用例关联不存在")

    # 返回更新后的计划信息（包含最新的执行进度）
    plan = TestPlanService.get_test_plan(db, plan_id)
    plan_data = serialize_model(plan, camel_case=True) if plan else None
    
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="更新成功",
        data=plan_data
    )


@router.put("/{plan_id}/cases/status", response_model=APIResponse)
async def batch_update_case_execution_status(
    plan_id: str,
    updates_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """批量更新用例执行状态"""
    require_plan(db, current_user, plan_id, "execute")
    updates = updates_data.get("updates", [])
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="updates 不能为空")

    for update in updates:
        if not update.get("caseId"):
            raise HTTPException(400, "用例编号不能为空")
        record_active_manual_result(db, plan_id, update["caseId"], update.get("status"), current_user.id)
    TestPlanService.batch_update_case_execution_status(
        db=db,
        plan_id=plan_id,
        updates=updates
    )
    
    # 返回更新后的计划信息（包含最新的执行进度）
    plan = TestPlanService.get_test_plan(db, plan_id)
    plan_data = serialize_model(plan, camel_case=True) if plan else None

    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="批量更新成功",
        data=plan_data
    )
