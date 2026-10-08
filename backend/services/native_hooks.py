"""Frozen script references retain current project/node authority without child queues."""
from copy import deepcopy
from fastapi import HTTPException
from models import User
from models import Environment, ScriptJob
from services import script_jobs
from framework.native_http.hook_models import FrozenScriptHook


def freeze_processors(db, user, project_id, processors):
    rows=[]
    for processor in processors:
        if processor.type == 'sql':
            rows.append(processor.model_dump()); continue
        actor=db.query(User).filter_by(id=user.id).populate_existing().with_for_update(read=True).first()
        if not actor or not actor.status: raise HTTPException(403,'当前脚本执行人已被禁用')
        reference=db.query(ScriptJob).filter_by(id=processor.jobId,project_id=project_id).populate_existing().first()
        if not reference: raise HTTPException(403,'钩子必须引用同来源项目的脚本作业')
        job=script_jobs.find_job(db,actor,processor.jobId,'execute',current_read=True)
        if job.project_id != project_id: raise HTTPException(403,'钩子必须引用同来源项目的脚本作业')
        if processor.expectedRevision is not None and processor.expectedRevision != job.revision:
            raise HTTPException(409,'脚本钩子版本已变化，请刷新引用后重试')
        # Freeze already owns its project lock. It must not take a node lock
        # after that project; dispatch owns the node and rechecks current rights.
        db.query(Environment).filter_by(id=job.environment_id).populate_existing().first()
        script_jobs.require_node(db,actor,job.environment_id,current_read=False)
        rows.append(FrozenScriptHook(**processor.model_dump(),projectId=job.project_id,revision=job.revision,config=deepcopy(job.config)).model_dump())
    return rows


def hooks(message):
    for case in message.get('native_cases',[]) or []:
        for p in case.get('globalPreProcessors',[]) + case.get('globalPostProcessors',[]):
            if p.get('type') == 'script': yield p
        for request in case.get('requests',[]):
            for p in request.get('preProcessors',[]) + request.get('postProcessors',[]):
                if p.get('type') == 'script': yield p


def required_node(message):
    nodes={p['config']['environmentId'] for p in hooks(message)}
    if len(nodes)>1: raise ValueError('同一原生执行的脚本钩子必须绑定同一个节点')
    return next(iter(nodes),None)


def bind_node(native_case, selected, pool=None):
    node=required_node({'native_cases':[native_case]})
    if not node: return selected
    if pool:
        if node not in pool: raise HTTPException(409,'脚本钩子节点不在当前资源池内')
        return node
    if selected != node: raise HTTPException(409,'脚本钩子节点与当前执行节点不一致')
    return selected


def authorize_frozen(db, user_id, message, *, node_current=False):
    rows=list(hooks(message))
    if not rows: return
    actor=db.query(User).filter_by(id=user_id).populate_existing().with_for_update(read=True).first()
    if not actor or not actor.status: raise HTTPException(403,'当前脚本执行人已被禁用')
    for source in rows:
        hook=FrozenScriptHook.model_validate(source)
        job=script_jobs.find_job(db,actor,hook.jobId,'execute',current_read=True)
        if job.project_id != hook.projectId: raise HTTPException(403,'冻结脚本来源项目不一致')
        if not node_current:
            db.query(Environment).filter_by(id=hook.config.environmentId).populate_existing().first()
        # Actual dispatch already owns this same node lock. A locking current
        # read must retain its fresh owner under MySQL REPEATABLE READ; never
        # overwrite it with an ordinary snapshot read before claiming a slot.
        script_jobs.require_node(db,actor,hook.config.environmentId,current_read=node_current)
    required_node(message)
