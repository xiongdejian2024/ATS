"""Independent script jobs, run history and the shared bounded log protocol."""
import asyncio
import json
from fastapi import APIRouter, Depends, Query, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from api.deps import get_current_user
from core.project_access import require_project_access
from core.security import verify_token
from database import get_db, SessionLocal
from models import User, Environment
from models.script_job import ScriptJob, ScriptJobRun, ScriptJobLog
from schemas.script_job import ScriptJobCreate, ScriptJobConfig, ResolveScriptJob
from schemas.task_center import RunTrigger
from schemas.common import APIResponse, ResponseStatus
from services import script_jobs as service
from services.bounded_logs import log_window
from services.raw_log_export import LogExportRequest, export_log_chunk

router = APIRouter()


def output(data, message="操作成功"):
    return APIResponse(status=ResponseStatus.SUCCESS, message=message, data=data)


@router.get("/nodes")
def nodes(projectId: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    from api.v1.websocket import manager
    require_project_access(db, user, projectId, "test_plan:read")
    result = []
    for node in db.query(Environment).filter_by(status=True).order_by(Environment.name).all():
        try:
            service.require_node(db, user, node.id)
        except HTTPException:
            continue
        session = manager.sessions.get(node.id)
        result.append(dict(id=node.id, name=node.name, isOnline=bool(session and manager.is_live(session) and getattr(session, "auth_received", False)),
                           supportsScriptJobs=service.capable(session, manager), owned=True, osType=node.os_type))
    return output({"items": result})


@router.get("")
def jobs(projectId: str, page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100),
         db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_project_access(db, user, projectId, "test_plan:read")
    query = db.query(ScriptJob).filter_by(project_id=projectId)
    return output(dict(items=[service.job_json(j) for j in query.order_by(ScriptJob.created_at.desc(), ScriptJob.id).offset((page-1)*size).limit(size)],
                       total=query.count(), page=page, size=size))


@router.post("")
def create(data: ScriptJobCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return output(service.job_json(service.create_job(db, user, data)))


@router.get("/{job_id}")
def detail(job_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return output(service.job_json(service.find_job(db, user, job_id)))


@router.put("/{job_id}")
def update(job_id: str, data: ScriptJobConfig, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return output(service.job_json(service.update_job(db, user, job_id, data)))


@router.post("/{job_id}/runs")
async def trigger(job_id: str, data: RunTrigger, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return output(service.run_json(db, await service.trigger(db, user, job_id, data.request_id)), "执行已加入正式队列")


@router.get("/{job_id}/runs")
def history(job_id: str, page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100),
            db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    service.find_job(db, user, job_id)
    query = db.query(ScriptJobRun).filter_by(job_id=job_id)
    return output(dict(items=[service.run_json(db, r) for r in query.order_by(ScriptJobRun.created_at.desc(), ScriptJobRun.execution_id).offset((page-1)*size).limit(size)],
                       total=query.count(), page=page, size=size))


@router.get("/{job_id}/runs/{execution_id}")
def run_detail(job_id: str, execution_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return output(service.run_json(db, service.find_run(db, user, job_id, execution_id)))


@router.post("/{job_id}/runs/{execution_id}/cancel")
async def cancel(job_id: str, execution_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return output(service.run_json(db, await service.cancel(db, user, job_id, execution_id)))


@router.post("/{job_id}/runs/{execution_id}/resolve")
async def resolve(job_id: str, execution_id: str, data: ResolveScriptJob, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    run = service.resolve(db, user, job_id, execution_id, data)
    from services.queued_dispatch import dispatch_pending_suites
    await dispatch_pending_suites(db, run.environment_id)
    return output(service.run_json(db, run))


def log_query(db, user, job_id, execution_id):
    service.find_run(db, user, job_id, execution_id)
    return db.query(ScriptJobLog).filter_by(script_job_id=job_id, execution_id=execution_id)


@router.get("/{job_id}/runs/{execution_id}/logs")
def logs(job_id: str, execution_id: str, skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=20),
         tail_chars: int = Query(32768, alias="tailChars", ge=1, le=32768),
         db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return output(log_window(log_query(db, user, job_id, execution_id), skip, limit,
                             tail_chars=tail_chars, latest=True, model=ScriptJobLog))


@router.post("/{job_id}/runs/{execution_id}/logs/export")
def export(job_id: str, execution_id: str, data: LogExportRequest,
           db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return output(export_log_chunk(log_query(db, user, job_id, execution_id),
        f"script-job:{job_id}:run:{execution_id}", user.id, data,
        model=ScriptJobLog, subject="script_job_id", label="job"))


async def script_log_websocket(websocket: WebSocket):
    from api.v1.websocket import frontend_manager
    await websocket.accept()
    key = None
    with SessionLocal() as db:
        try:
            token = websocket.query_params.get("token")
            job_id = websocket.query_params.get("job_id")
            execution_id = websocket.query_params.get("execution_id")
            try:
                user = db.get(User, verify_token(token, "access")) if token else None
                if not user or not user.status or not job_id or not execution_id:
                    raise HTTPException(403, "无效身份")
                service.find_run(db, user, job_id, execution_id)
            except Exception:
                await websocket.close(code=1008, reason="Script run not found or access denied")
                return
            user_id = str(user.id)
            key = "script:" + execution_id
            await frontend_manager.connect(websocket, key)
            frontend_manager.enqueue_message(websocket, key, dict(type="connected", job_id=job_id, execution_id=execution_id))
            db.rollback()
            while frontend_manager.is_connected(websocket, key):
                try:
                    # Re-read authority on each heartbeat turn. A prior identity
                    # map or HTTP login must not keep a revoked subscription alive.
                    db.rollback()
                    db.expire_all()
                    current = db.query(User).filter_by(id=user_id).populate_existing().first()
                    if not current or not current.status:
                        raise HTTPException(403, "用户已停用")
                    service.find_run(db, current, job_id, execution_id)
                    db.rollback()
                except HTTPException:
                    await websocket.close(code=1008, reason="Script log access revoked")
                    break
                try:
                    data = await asyncio.wait_for(websocket.receive_text(), 30)
                    if len(data) > 4096:
                        await websocket.close(code=1009); break
                    payload = json.loads(data)
                    if isinstance(payload, dict) and payload.get("type") == "ping":
                        if not frontend_manager.enqueue_message(websocket, key, {"type": "pong"}):
                            break
                except asyncio.TimeoutError:
                    if not frontend_manager.enqueue_message(websocket, key, {"type": "ping"}):
                        break
                except (ValueError, WebSocketDisconnect):
                    break
        finally:
            if key:
                cleanup = frontend_manager.disconnect(websocket, key)
                if cleanup:
                    await cleanup
