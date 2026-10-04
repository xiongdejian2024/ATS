"""AI 辅助接口：配置、会话、草稿与人工确认。"""
from typing import Literal
from sqlalchemy import update
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from loguru import logger
from database import get_db
from api.deps import get_current_user
from core.permissions import has_global_permission
from core.project_access import require_project_access
from models.ai_assistance import AIModelConfig, AIConversation, AICaseDraft
from schemas.ai_assistance import ModelConfiguration, ChatRequest, GenerateRequest, DraftUpdate, DraftDecision
from schemas.test_case import TestCaseCreate
from services import ai_assistance as service
from services.test_case_service import TestCaseService

router = APIRouter(prefix="/ai", tags=["AI 辅助"])


def ok(data):
    return {"status": "success", "data": data}


def system_permission(db, user):
    if not has_global_permission(db, user.id, "system", "manage"):
        raise HTTPException(403, "只有系统管理员可修改系统模型设置")


@router.get("/configuration")
def configuration(db: Session = Depends(get_db), user=Depends(get_current_user)):
    personal = db.query(AIModelConfig).filter_by(owner_key=user.id).first()
    system = db.query(AIModelConfig).filter_by(owner_key="system").first()
    return ok({"personal": service.config_view(personal), "system": service.config_view(system),
               "can_manage_system": has_global_permission(db, user.id, "system", "manage")})


@router.put("/configuration/{scope}")
def set_configuration(scope: Literal["personal", "system"], body: ModelConfiguration,
                      db: Session = Depends(get_db), user=Depends(get_current_user)):
    if scope == "system":
        system_permission(db, user)
    key = "system" if scope == "system" else user.id
    row = db.query(AIModelConfig).filter_by(owner_key=key).first()
    if not row:
        row = AIModelConfig(owner_key=key)
        db.add(row)
    for field in ("base_url", "model", "timeout_seconds", "enabled"):
        setattr(row, field, getattr(body, field))
    if body.api_key:
        row.api_key_encrypted = service.encrypt_key(body.api_key)
    elif body.clear_api_key:
        row.api_key_encrypted = None
    db.commit()
    logger.info("模型配置已保存：范围={}，用户={}", scope, user.id)
    return ok(service.config_view(row))


@router.delete("/configuration/personal")
def remove_personal_configuration(db: Session = Depends(get_db), user=Depends(get_current_user)):
    row = db.query(AIModelConfig).filter_by(owner_key=user.id).first()
    if row:
        db.delete(row)
        db.commit()
    return ok({"restored_system_default": True})


@router.post("/configuration/test")
async def test_configuration(db: Session = Depends(get_db), user=Depends(get_current_user)):
    config = service.get_config(db, user)
    await service.complete(config, [{"role": "user", "content": "请只回复：连接成功"}])
    return ok({"connected": True, "model": config.model})


@router.get("/conversations")
def conversations(project_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_project_access(db, user, project_id)
    rows = db.query(AIConversation).filter_by(user_id=user.id, project_id=project_id).order_by(AIConversation.updated_at.desc()).limit(100).all()
    return ok([{"id": row.id, "title": row.title, "updated_at": row.updated_at.isoformat()} for row in rows])


@router.get("/conversations/{identifier}")
def conversation(identifier: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    row = service.owned_conversation(db, user, identifier)
    require_project_access(db, user, row.project_id)
    return ok({"id": row.id, "title": row.title, "messages": row.messages})


@router.delete("/conversations/{identifier}")
def delete_conversation(identifier: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    row = service.owned_conversation(db, user, identifier)
    require_project_access(db, user, row.project_id)
    db.delete(row)
    db.commit()
    return ok({"deleted": True})


@router.post("/chat")
async def chat(body: ChatRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_project_access(db, user, body.project_id)
    config = service.get_config(db, user)
    row = service.owned_conversation(db, user, body.conversation_id) if body.conversation_id else None
    if row and row.project_id != body.project_id:
        raise HTTPException(400, "会话不属于当前项目")
    history = list(row.messages) if row else []
    revision = row.revision if row else None
    if len(history) >= 200:
        raise HTTPException(409, "此会话已达到长度上限，请新建会话")
    turn = {"role": "user", "content": body.message}
    content = await service.complete(config, [{"role": "system", "content": "你是 ATS 测试助手，用中文帮助分析需求、设计测试、解释失败。只依据用户提供的信息，不声称执行了测试或访问了设备。"}, *history[-12:], turn])
    if not row:
        row = AIConversation(user_id=user.id, project_id=body.project_id, title=body.message[:100])
        row.messages = [*history, turn, {"role": "assistant", "content": content}]
        db.add(row)
    else:
        changed = db.execute(update(AIConversation).where(
            AIConversation.id == row.id, AIConversation.user_id == user.id,
            AIConversation.revision == revision,
        ).values(messages=[*history, turn, {"role": "assistant", "content": content}],
                 revision=revision + 1).execution_options(synchronize_session=False))
        if changed.rowcount != 1:
            db.rollback()
            raise HTTPException(409, "会话已在其他窗口更新，请刷新后重新发送；本次内容没有覆盖已保存消息")
    db.commit()
    db.refresh(row)
    return ok({"id": row.id, "title": row.title, "messages": row.messages})


@router.post("/generate-cases")
async def generate(body: GenerateRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_project_access(db, user, body.project_id, "test_case:create")
    return ok(await service.generate_drafts(db, user, body))


@router.get("/drafts")
def drafts(project_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_project_access(db, user, project_id)
    rows = db.query(AICaseDraft).filter_by(project_id=project_id, user_id=user.id).order_by(AICaseDraft.created_at.desc()).limit(200).all()
    return ok([service.draft_view(row) for row in rows])


def editable_draft(db, user, identifier, revision, allow_imported=False):
    row = db.query(AICaseDraft).filter_by(id=identifier, user_id=user.id).with_for_update().first()
    if not row:
        raise HTTPException(404, "草稿不存在")
    require_project_access(db, user, row.project_id, "test_case:create")
    if allow_imported and row.status == "imported":
        return row
    if row.status != "draft" or row.revision != revision:
        raise HTTPException(409, "草稿已被修改或处理，请刷新后重试")
    return row


def claim_draft(db, user, row, revision, *, allow_imported=False):
    """同事务CAS领取草稿，SQLite和MySQL都不会产生并发覆盖。"""
    changed = db.execute(update(AICaseDraft).where(
        AICaseDraft.id == row.id, AICaseDraft.user_id == user.id,
        AICaseDraft.status == "draft", AICaseDraft.revision == revision,
    ).values(revision=revision + 1).execution_options(synchronize_session=False))
    if changed.rowcount != 1:
        db.rollback()
        current = db.query(AICaseDraft).filter_by(id=row.id, user_id=user.id).first()
        if allow_imported and current and current.status == "imported":
            return current, False
        raise HTTPException(409, "草稿已被修改或处理，请刷新后重试")
    db.refresh(row)
    return row, True


@router.put("/drafts/{identifier}")
def update_draft(identifier: str, body: DraftUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    row = editable_draft(db, user, identifier, body.revision)
    row, _ = claim_draft(db, user, row, body.revision)
    row.content = body.content.model_dump()
    db.commit()
    return ok(service.draft_view(row))


@router.post("/drafts/{identifier}/dismiss")
def dismiss_draft(identifier: str, body: DraftDecision, db: Session = Depends(get_db), user=Depends(get_current_user)):
    row = editable_draft(db, user, identifier, body.revision)
    row, _ = claim_draft(db, user, row, body.revision)
    row.status = "dismissed"
    db.commit()
    return ok(service.draft_view(row))


@router.post("/drafts/{identifier}/accept")
def accept_draft(identifier: str, body: DraftDecision, db: Session = Depends(get_db), user=Depends(get_current_user)):
    row = editable_draft(db, user, identifier, body.revision, allow_imported=True)
    if row.status == "imported":
        return ok(service.draft_view(row))
    row, claimed = claim_draft(db, user, row, body.revision, allow_imported=True)
    if not claimed:
        return ok(service.draft_view(row))
    content = dict(row.content)
    content["steps"] = [{"step": index + 1, **step} for index, step in enumerate(content["steps"])]
    try:
        case = TestCaseService.create_test_case(db, TestCaseCreate(project_id=row.project_id,
              case_code="AI-" + row.id, is_automated=False, **content), user.id, commit=False)
        row.status, row.imported_case_id = "imported", case.id
        db.commit()
        logger.info("AI 草稿经用户确认入库：草稿={}，用例={}，用户={}", row.id, case.id, user.id)
        return ok(service.draft_view(row))
    except Exception:
        db.rollback()
        logger.exception("AI 草稿入库失败，已回滚事务")
        raise
