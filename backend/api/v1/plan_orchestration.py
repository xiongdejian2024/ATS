"""计划组、执行策略与批次报告接口。"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from api.deps import get_current_user
from core.project_access import require_project_access
from core.logger import logger
from models.test_plan import TestPlan
from models.plan_orchestration import PlanGroup, PlanSettings, PlanRun
from schemas.common import APIResponse, ResponseStatus
from schemas.plan_orchestration import GroupInput, PlanPolicy, ManualResultInput
from services.plan_orchestration import get_policy, save_policy, run_data, run_logs, record_manual_result, cancel_plan_run, resolve_uncertain_run
from utils.serializer import serialize_model
from services.plan_workspace import group_metadata, update_group_metadata, clone_group

router = APIRouter()


def ok(data=None, message="操作成功"):
    return APIResponse(status=ResponseStatus.SUCCESS, message=message, data=data)


def require_plan(db, user, plan_id, action="read"):
    plan = db.get(TestPlan, plan_id)
    if not plan:
        raise HTTPException(404, "测试计划不存在")
    require_project_access(db, user, plan.project_id, f"test_plan:{action}")
    return plan


def require_run(db, user, run_id, action="read"):
    run = db.get(PlanRun, run_id)
    if not run:
        raise HTTPException(404, "执行批次不存在")
    require_plan(db, user, run.plan_id, action)
    return run


@router.get("/projects/{project_id}/groups", response_model=APIResponse)
def groups(project_id: str, archived: bool = False, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_project_access(db, user, project_id, "test_plan:read")
    items = db.query(PlanGroup).filter_by(project_id=project_id).order_by(PlanGroup.created_at).all()
    return ok([dict(**serialize_model(g, camel_case=True), **group_metadata(db, g.id), planCount=db.query(PlanSettings).filter_by(group_id=g.id).count()) for g in items if group_metadata(db, g.id)["archived"] == archived])


@router.post("/projects/{project_id}/groups", response_model=APIResponse)
def create_group(project_id: str, data: GroupInput, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_project_access(db, user, project_id, "test_plan:create")
    if not data.name.strip():
        raise HTTPException(422, "计划组名称不能为空")
    if db.query(PlanGroup).filter_by(project_id=project_id, name=data.name.strip()).first():
        raise HTTPException(409, "计划组名称已存在")
    group = PlanGroup(project_id=project_id, name=data.name.strip(), description=data.description)
    db.add(group)
    db.flush()
    update_group_metadata(db, group, data.model_dump(by_alias=True))
    db.commit()
    logger.info("已创建计划组：项目={}，计划组={}", project_id, group.id)
    return ok(serialize_model(group, camel_case=True))


@router.put("/groups/{group_id}", response_model=APIResponse)
def update_group(group_id: str, data: GroupInput, db: Session = Depends(get_db), user=Depends(get_current_user)):
    group = db.get(PlanGroup, group_id)
    if not group:
        raise HTTPException(404, "计划组不存在")
    require_project_access(db, user, group.project_id, "test_plan:update")
    if not data.name.strip():
        raise HTTPException(422, "计划组名称不能为空")
    if db.query(PlanGroup).filter(PlanGroup.project_id == group.project_id, PlanGroup.name == data.name.strip(), PlanGroup.id != group_id).first():
        raise HTTPException(409, "计划组名称已存在")
    group.name, group.description = data.name.strip(), data.description
    update_group_metadata(db, group, data.model_dump(by_alias=True))
    db.commit()
    logger.info("已更新计划组：计划组={}", group_id)
    return ok(serialize_model(group, camel_case=True))


@router.delete("/groups/{group_id}", response_model=APIResponse)
def delete_group(group_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    group = db.get(PlanGroup, group_id)
    if not group:
        raise HTTPException(404, "计划组不存在")
    require_project_access(db, user, group.project_id, "test_plan:delete")
    from models.plan_group_execution import PlanGroupRun, PlanGroupPolicy
    from models.plan_workspace import PlanGroupWorkspace
    if db.query(PlanGroupRun).filter_by(active_group_id=group_id).first():
        raise HTTPException(409, "请先完成或取消正在执行的计划组")
    db.query(PlanGroupPolicy).filter_by(group_id=group_id).delete()
    db.query(PlanGroupWorkspace).filter_by(group_id=group_id).delete()
    db.query(PlanSettings).filter_by(group_id=group_id).update({"group_id": None})
    db.delete(group)
    db.commit()
    logger.info("已删除计划组，组内计划保留：计划组={}", group_id)
    return ok()


@router.get("/plans/{plan_id}/settings", response_model=APIResponse)
def settings(plan_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_plan(db, user, plan_id)
    return ok(get_policy(db, plan_id))


@router.put("/plans/{plan_id}/settings", response_model=APIResponse)
def update_settings(plan_id: str, data: PlanPolicy, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_plan(db, user, plan_id, "update")
    try:
        return ok(save_policy(db, plan_id, data))
    except ValueError as exc:
        logger.exception("保存计划执行策略失败：计划={}", plan_id)
        db.rollback()
        raise HTTPException(400, str(exc)) from exc


@router.get("/runs/{run_id}", response_model=APIResponse)
def report(run_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return ok(run_data(db, require_run(db, user, run_id)))


@router.get("/runs/{run_id}/logs", response_model=APIResponse)
def logs(run_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return ok({"executionLog": run_logs(db, require_run(db, user, run_id))})


@router.post("/runs/{run_id}/cancel", response_model=APIResponse)
async def cancel(run_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_run(db, user, run_id, "execute")
    return ok(run_data(db, await cancel_plan_run(db, run_id, str(user.id))), "已请求取消，运行中任务等待 Agent 确认")


@router.put("/runs/{run_id}/cases/{case_id}/result", response_model=APIResponse)
def manual_result(run_id: str, case_id: str, data: ManualResultInput, db: Session = Depends(get_db), user=Depends(get_current_user)):
    run = require_run(db, user, run_id)
    snapshot = next((case for case in run.case_snapshot if case.get("associationId", case["id"]) == case_id), None)
    if not snapshot or snapshot.get("assignedTo") != str(user.id):
        require_plan(db, user, run.plan_id, "execute")
    try:
        return ok(run_data(db, record_manual_result(db, run_id, case_id, data, str(user.id))))
    except ValueError as exc:
        logger.exception("回填计划手工结果失败：批次={}", run_id)
        raise HTTPException(400, str(exc)) from exc


@router.post("/runs/{run_id}/resolve", response_model=APIResponse)
def resolve(run_id: str, confirmation: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_run(db, user, run_id, "execute")
    if confirmation.get("agentStopped") is not True:
        raise HTTPException(400, "请先确认节点未执行或执行已停止")
    try:
        return ok(run_data(db, resolve_uncertain_run(db, run_id, str(user.id))))
    except ValueError as exc:
        logger.exception("人工核对计划状态失败：批次={}", run_id)
        raise HTTPException(409, str(exc)) from exc


from api.v1.plan_workspace import router as workspace_router
router.include_router(workspace_router)
from api.v1.plan_collaboration import router as collaboration_router
router.include_router(collaboration_router)


@router.post("/groups/{group_id}/clone", response_model=APIResponse)
def copy_group(group_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    group = db.get(PlanGroup, group_id)
    if not group:
        raise HTTPException(404, "计划组不存在")
    require_project_access(db, user, group.project_id, "test_plan:create")
    return ok(serialize_model(clone_group(db, group, str(user.id)), camel_case=True))
