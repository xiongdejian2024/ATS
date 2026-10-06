"""计划模块、关注和批量管理接口。"""
from fastapi import APIRouter, Depends, HTTPException
from services.plan_execution_config import ConfigSave, PoolSave
from services.plan_minder_edit import MinderSave, MinderCandidatePreview
from sqlalchemy.orm import Session
from database import get_db
from api.deps import get_current_user
from core.project_access import require_project_access
from models.plan_workspace import PlanModule, PlanWorkspace, PlanFollow
from models.test_plan import TestPlan
from services.plan_workspace import metadata, update_metadata
from utils.serializer import serialize_model
from schemas.common import APIResponse, ResponseStatus
from pydantic import BaseModel, Field

router = APIRouter()


def ok(data=None):
    return APIResponse(status=ResponseStatus.SUCCESS, message="操作成功", data=data)


def plan_access(db, user, plan_id, action="read"):
    plan = db.get(TestPlan, plan_id)
    if not plan:
        raise HTTPException(404, "计划不存在")
    require_project_access(db, user, plan.project_id, f"test_plan:{action}")
    return plan


def editable_node_plan(db, user, plan_id):
    plan = plan_access(db, user, plan_id, "update")
    workspace = db.get(PlanWorkspace, plan_id)
    if workspace and workspace.archived:
        raise HTTPException(409, "归档计划不可修改测试集或关联配置")
    return plan


class PlanDefectWrite(BaseModel):
    caseId: str = Field(min_length=1, max_length=36)
    title: str = Field(min_length=1, max_length=300)
    description: str = Field("", max_length=20000)


@router.get("/plans/{plan_id}/defects")
def plan_defects(plan_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_detail import defects
    from core.project_access import project_allows
    plan = plan_access(db, user, plan_id)
    project = require_project_access(db, user, plan.project_id, "test_case:read")
    payload = defects(db, plan)
    workspace = db.get(PlanWorkspace, plan_id)
    payload["canEdit"] = not (workspace and workspace.archived) and project_allows(db, user, project, "test_plan:update") and project_allows(db, user, project, "test_case:update")
    return ok(payload)


@router.post("/plans/{plan_id}/defects")
def create_plan_defect(plan_id: str, data: PlanDefectWrite, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_detail import plan_case_ids
    from services import case_features as service
    from models.case_features import CaseIssueLink
    from schemas.case_features import IssueWrite
    from api.v1.case_governance import transact
    from core.logger import logger
    plan = plan_access(db, user, plan_id, "update")
    workspace = db.get(PlanWorkspace, plan_id)
    if workspace and workspace.archived:
        raise HTTPException(409, "归档计划不可新建缺陷")
    if data.caseId not in plan_case_ids(db, plan.id):
        raise HTTPException(422, "只能关联此计划中的用例")
    if not data.title.strip():
        raise HTTPException(422, "缺陷标题不能为空")
    current = service.find_case(db, user, plan.project_id, data.caseId, "update")
    def operation():
        issue = service.write_issue(db, user, plan.project_id, IssueWrite(kind="defect", title=data.title.strip(), description=data.description, status="open"))
        db.add(CaseIssueLink(case_id=data.caseId, issue_id=issue.id, created_by=str(user.id)))
        service.change(db, current, user.id, "关联计划缺陷", {"planId": plan.id, "issueId": issue.id})
        return issue
    issue = transact(db, operation)
    logger.info("已在计划详情新建并关联缺陷：计划={}，缺陷={}", plan_id, issue.id)
    return ok(serialize_model(issue, camel_case=True))


@router.get("/projects/{project_id}/modules")
def modules(project_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_project_access(db, user, project_id, "test_plan:read")
    return ok([serialize_model(row, camel_case=True) for row in db.query(PlanModule).filter_by(project_id=project_id).order_by(PlanModule.position, PlanModule.created_at)])


def set_module(db, module, data):
    name = str(data.get("name", module.name or "")).strip()
    if not name or len(name) > 120:
        raise HTTPException(422, "模块名称须为1到120字")
    parent_id = data.get("parentId", module.parent_id)
    seen = {module.id} if module.id else set()
    while parent_id:
        parent = db.get(PlanModule, parent_id)
        if not parent or parent.project_id != module.project_id or parent_id in seen:
            raise HTTPException(400, "模块父级不属于本项目或形成循环")
        seen.add(parent_id)
        parent_id = parent.parent_id
    module.name = name
    module.parent_id = data.get("parentId", module.parent_id) or None
    module.position = int(data.get("position", module.position or 0))


@router.post("/projects/{project_id}/modules")
def create_module(project_id: str, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_project_access(db, user, project_id, "test_plan:create")
    row = PlanModule(project_id=project_id)
    set_module(db, row, data)
    db.add(row)
    db.commit()
    return ok(serialize_model(row, camel_case=True))


@router.put("/modules/{module_id}")
def update_module(module_id: str, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    row = db.get(PlanModule, module_id)
    if not row:
        raise HTTPException(404, "模块不存在")
    require_project_access(db, user, row.project_id, "test_plan:update")
    set_module(db, row, data)
    db.commit()
    return ok(serialize_model(row, camel_case=True))


@router.delete("/modules/{module_id}")
def delete_module(module_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    row = db.get(PlanModule, module_id)
    if not row:
        raise HTTPException(404, "模块不存在")
    require_project_access(db, user, row.project_id, "test_plan:delete")
    if db.query(PlanModule).filter_by(parent_id=module_id).first():
        raise HTTPException(409, "请先移走或删除子模块")
    from models.plan_workspace import PlanGroupWorkspace
    db.query(PlanGroupWorkspace).filter_by(module_id=module_id).update({"module_id": None})
    db.query(PlanWorkspace).filter_by(module_id=module_id).update({"module_id": None})
    db.delete(row)
    db.commit()
    return ok()


@router.get("/plans/{plan_id}/workspace")
def get_metadata(plan_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    plan_access(db, user, plan_id)
    return ok(metadata(db, plan_id, user.id))


@router.put("/plans/{plan_id}/workspace")
def save_metadata(plan_id: str, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    plan = plan_access(db, user, plan_id, "update")
    update_metadata(db, plan, data)
    db.commit()
    return ok(metadata(db, plan_id, user.id))


@router.put("/plans/{plan_id}/follow")
def follow(plan_id: str, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    plan_access(db, user, plan_id)
    row = db.query(PlanFollow).filter_by(plan_id=plan_id, user_id=user.id).first()
    if data.get("followed") and not row:
        db.add(PlanFollow(plan_id=plan_id, user_id=user.id))
    elif not data.get("followed") and row:
        db.delete(row)
    db.commit()
    return ok(metadata(db, plan_id, user.id))


@router.post("/projects/{project_id}/plans/batch")
def batch(project_id: str, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_project_access(db, user, project_id, "test_plan:update")
    ids = data.get("planIds", [])
    if not isinstance(ids, list) or not ids or len(ids) > 200:
        raise HTTPException(422, "请选择1到200个计划")
    plans = db.query(TestPlan).filter(TestPlan.id.in_(ids), TestPlan.project_id == project_id).all()
    if len(plans) != len(set(ids)):
        raise HTTPException(400, "计划不存在或不属于当前项目")
    for plan in plans:
        update_metadata(db, plan, data.get("changes", {}))
    db.commit()
    return ok({"updated": len(plans)})


@router.get("/plans/{plan_id}/nodes")
def list_nodes(plan_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_tree import nodes, node_data
    plan_access(db, user, plan_id)
    return ok([node_data(db, row) for row in nodes(db, plan_id)])


@router.get("/plans/{plan_id}/minder-workspace")
def read_minder_workspace(plan_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_minder_edit import load
    from api.v1.case_governance import transact
    return ok(transact(db, lambda: load(db, user, plan_id)))


@router.put("/plans/{plan_id}/minder-workspace")
def save_minder_workspace(plan_id: str, data: MinderSave, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_minder_edit import save
    from api.v1.case_governance import transact
    return ok(transact(db, lambda: save(db, user, plan_id, data)))


@router.post("/plans/{plan_id}/minder-workspace/candidates/selection")
def preview_minder_candidates(
    plan_id: str,
    data: MinderCandidatePreview,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    from services.plan_minder_edit import preview_candidates
    from api.v1.case_governance import transact

    return ok(transact(db, lambda: preview_candidates(db, user, plan_id, data)))


@router.get("/plans/{plan_id}/execution-configurations")
def execution_configurations(plan_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_execution_config import catalog
    from services.plan_orchestration import get_policy
    from services.plan_tree import nodes
    plan = plan_access(db, user, plan_id)
    return ok(catalog(db, plan, get_policy(db, plan.id), nodes(db, plan.id)))


@router.put("/plans/{plan_id}/execution-configurations/{scope}")
def save_execution_configuration(plan_id: str, scope: str, data: ConfigSave, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_execution_config import save
    from api.v1.case_governance import transact
    plan = editable_node_plan(db, user, plan_id)
    transact(db, lambda: save(db, plan, scope, data))
    return execution_configurations(plan_id, db, user)


@router.post("/plans/{plan_id}/resource-pools")
def create_execution_pool(plan_id: str, data: PoolSave, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_execution_config import save_pool
    from api.v1.case_governance import transact
    plan = editable_node_plan(db, user, plan_id)
    transact(db, lambda: save_pool(db, plan, data))
    return execution_configurations(plan_id, db, user)


@router.put("/plans/{plan_id}/resource-pools/{pool_id}")
def update_execution_pool(plan_id: str, pool_id: str, data: PoolSave, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_execution_config import save_pool
    from api.v1.case_governance import transact
    plan = editable_node_plan(db, user, plan_id)
    transact(db, lambda: save_pool(db, plan, data, pool_id))
    return execution_configurations(plan_id, db, user)


@router.post("/plans/{plan_id}/nodes")
def create_node(plan_id: str, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from services.plan_tree import save_node, node_data
    from api.v1.case_governance import transact
    plan = editable_node_plan(db, user, plan_id)
    row = transact(db, lambda: save_node(db, plan, data))
    return ok(node_data(db, row))


@router.put("/nodes/{node_id}")
def update_node(node_id: str, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from models.plan_workspace import PlanNode
    from services.plan_tree import save_node, node_data
    row = db.get(PlanNode, node_id)
    if not row:
        raise HTTPException(404, "测试点节点不存在")
    from api.v1.case_governance import transact
    plan = editable_node_plan(db, user, row.plan_id)
    transact(db, lambda: save_node(db, plan, data, row))
    return ok(node_data(db, row))


@router.delete("/nodes/{node_id}")
def delete_node(node_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from models.plan_workspace import PlanNode
    row = db.get(PlanNode, node_id)
    if not row:
        raise HTTPException(404, "测试点节点不存在")
    editable_node_plan(db, user, row.plan_id)
    from services.plan_tree import uses_tree, remember_tree
    from api.v1.case_governance import transact
    from core.logger import logger
    # 显式清子树让 SQLite（FK可未启用）与 MySQL 一致；批次保存独立快照。
    visited = set()
    def remove(node):
        if node.id in visited:
            raise HTTPException(409, "旧测试集层级形成循环，已停止删除")
        visited.add(node.id)
        for child in db.query(PlanNode).filter_by(parent_id=node.id, plan_id=row.plan_id).all():
            remove(child)
        db.query(PlanNode).filter_by(linked_functional_id=node.id).update({"linked_functional_id": None})
        from models.test_plan import PlanCaseRelation
        db.query(PlanCaseRelation).filter_by(collection_id=node.id).update({"collection_id": None})
        from models.plan_execution_config import PlanExecutionConfig
        db.query(PlanExecutionConfig).filter_by(plan_id=row.plan_id, node_id=node.id).delete(synchronize_session=False)
        db.delete(node)
        db.flush()
    def operation():
        if uses_tree(db, row.plan_id):
            remember_tree(db, row.plan_id)
        remove(row)
    transact(db, operation)
    logger.info("已删除计划测试集或关联节点：计划={}，节点数={}", row.plan_id, len(visited))
    return ok()


@router.post("/plans/{plan_id}/nodes/assign")
def assign_nodes(plan_id: str, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from models.plan_workspace import PlanNode
    from services.plan_tree import save_node
    plan = editable_node_plan(db, user, plan_id)
    ids = data.get("nodeIds", [])
    if not isinstance(ids, list) or not 1 <= len(ids) <= 500 or any(not isinstance(value, str) for value in ids) or len(set(ids)) != len(ids):
        raise HTTPException(422, "请选择1到500个用例节点")
    rows = db.query(PlanNode).filter(PlanNode.plan_id == plan_id, PlanNode.id.in_(ids), PlanNode.node_type != "point").all()
    if len(rows) != len(set(ids)):
        raise HTTPException(400, "关联节点不存在或不属于当前计划")
    from api.v1.case_governance import transact
    def operation():
        for row in rows:
            save_node(db, plan, {"assignedTo": data.get("assignedTo")}, row)
    transact(db, operation)
    return ok({"updated": len(rows)})


@router.get("/plans/{plan_id}/executors")
def executors(plan_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from models.user import User
    plan = plan_access(db, user, plan_id)
    candidates = []
    for candidate in db.query(User).filter(User.status.is_(True)):
        try:
            require_project_access(db, candidate, plan.project_id, "test_plan:read")
        except HTTPException as exc:
            if exc.status_code == 403:
                continue
            raise
        candidates.append({"id": candidate.id, "name": candidate.username})
    return ok(candidates)
