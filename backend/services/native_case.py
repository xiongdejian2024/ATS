"""原生配置事务、项目归属和版本冲突；不提交网络或台架任务。"""
from copy import deepcopy
from sqlalchemy.orm.attributes import flag_modified
import hashlib
import json
from fastapi import HTTPException
from models.native_case import ApiDefinition, ApiTestEnvironment, NativeCaseConfig
from services.case_governance import case_for_project
from services.review_workspace import lock_project
from core.project_access import require_project_access, project_allows
from core.logger import logger

STATES = {'api': {'PROCESSING', 'DEPRECATED', 'DONE'}, 'scenario': {'UNDERWAY', 'DEPRECATED', 'COMPLETED'}}


def fingerprint(parameters):
    return hashlib.sha256(json.dumps(parameters, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def entity(db, model, project_id, identity, *, lock=False):
    query = db.query(model).filter_by(id=identity, project_id=project_id).populate_existing()
    row = (query.with_for_update() if lock else query).first()
    if not row:
        raise HTTPException(404, '引用对象不属于当前项目或已不存在')
    return row


def catalog(db, user, project_id):
    project = require_project_access(db, user, project_id)
    def rows(model, fields):
        return [dict(id=r.id, revision=r.revision, **{f: getattr(r, f) for f in fields})
                for r in db.query(model).filter_by(project_id=project_id).order_by(model.created_at, model.id)]
    definitions = rows(ApiDefinition, ['name', 'protocol', 'path', 'parameters'])
    return dict(definitions=definitions, environments=rows(ApiTestEnvironment, ['name', 'address']),
                protocols=sorted({r['protocol'] for r in definitions}),
                canCreate=project_allows(db, user, project, 'test_case:create'),
                canEdit=project_allows(db, user, project, 'test_case:update'))


def save_entity(db, user, project_id, model, body, identity=None):
    require_project_access(db, user, project_id, 'test_case:update' if identity else 'test_case:create')
    lock_project(db, project_id)
    row = entity(db, model, project_id, identity, lock=True) if identity else model(project_id=project_id, revision=0)
    if row.revision != body.expectedRevision:
        raise HTTPException(409, '配置已经被修改，请刷新后重试；当前草稿可保留')
    for field, value in body.model_dump(exclude={'expectedRevision'}).items():
        setattr(row, field, deepcopy(value))
    if model is ApiDefinition:
        flag_modified(row, "parameters")
    row.updated_by = str(user.id)
    row.revision += 1
    db.add(row); db.flush()
    logger.info('原生配置已保存 project_id={} model={} id={} revision={}', project_id, model.__tablename__, row.id, row.revision)
    return catalog(db, user, project_id)


def config_snapshot(db, case, *, current_read=False):
    query = db.query(NativeCaseConfig).filter_by(case_id=case.id)
    row = query.populate_existing().with_for_update().first() if current_read else db.get(NativeCaseConfig, case.id)
    if not row:
        return None
    return {f: deepcopy(getattr(row, f)) for f in ('state', 'environment_id', 'api_definition_id', 'definition_fingerprint', 'parameters')}


def restore_config(db, case, value, actor_id):
    row = db.query(NativeCaseConfig).filter_by(case_id=case.id).populate_existing().with_for_update().first()
    if not value:
        if row: db.delete(row)
        db.flush(); return
    if case.type not in STATES or value['state'] not in STATES[case.type]:
        raise HTTPException(409, '历史原生配置与用例类型不一致')
    for field, model in [('environment_id', ApiTestEnvironment), ('api_definition_id', ApiDefinition)]:
        if value.get(field): entity(db, model, case.project_id, value[field])
    if not row:
        row = NativeCaseConfig(case_id=case.id, revision=0)
    for field, v in value.items(): setattr(row, field, deepcopy(v))
    flag_modified(row, "parameters")
    row.revision += 1; row.updated_by = actor_id; db.add(row); db.flush()


def config_data(db, user, project_id, case_id):
    project = require_project_access(db, user, project_id)
    case = case_for_project(db, project_id, case_id)
    if case.type not in STATES: raise HTTPException(422, '此用例不是API用例或场景')
    row = db.get(NativeCaseConfig, case.id)
    definition = entity(db, ApiDefinition, project_id, row.api_definition_id) if row and row.api_definition_id else None
    from services.native_candidate_context import NativeCandidateContext
    native = NativeCandidateContext(db, project_id).values(case)
    return dict(lastReportStatus=native['lastReportStatus'], stepTotal=native['stepTotal'], state=row.state if row else None, environmentId=row.environment_id if row else None,
                apiDefinitionId=row.api_definition_id if row else None, parameters=row.parameters if row else {},
                revision=row.revision if row else 0,
                apiChange=(row.definition_fingerprint != fingerprint(definition.parameters)) if definition else None,
                canEdit=project_allows(db, user, project, 'test_case:update'))


def save_config(db, user, project_id, case_id, body):
    require_project_access(db, user, project_id, 'test_case:update')
    case = case_for_project(db, project_id, case_id, lock=True)
    if case.type not in STATES or body.state not in STATES[case.type]:
        raise HTTPException(422, '原生用例状态与分类不一致')
    row = db.query(NativeCaseConfig).filter_by(case_id=case.id).populate_existing().with_for_update().first()
    if (row.revision if row else 0) != body.expectedRevision:
        raise HTTPException(409, '用例配置已经被修改，请刷新后重试；当前草稿可保留')
    if body.environmentId: entity(db, ApiTestEnvironment, project_id, body.environmentId, lock=True)
    definition = None
    if case.type == 'api':
        if not body.apiDefinitionId: raise HTTPException(422, '请选择关联接口定义')
        definition = entity(db, ApiDefinition, project_id, body.apiDefinitionId, lock=True)
        if definition.revision != body.expectedDefinitionRevision:
            raise HTTPException(409, '接口定义已经被修改，请重新加载后再保存用例配置')
    elif body.apiDefinitionId or body.syncDefinition:
        raise HTTPException(422, '场景不能保存接口用例专属配置')
    from services.case_governance import snapshot_case
    snapshot_case(db, case, str(user.id), '原生配置修改前保存版本')
    if not row: row = NativeCaseConfig(case_id=case.id, revision=0)
    changed_definition = row.api_definition_id != body.apiDefinitionId
    row.state = body.state; row.environment_id = body.environmentId
    row.api_definition_id = body.apiDefinitionId
    row.parameters = deepcopy(body.parameters)
    flag_modified(row, "parameters")
    if definition and (changed_definition or body.syncDefinition):
        row.definition_fingerprint = fingerprint(definition.parameters)
    row.revision += 1; row.updated_by = str(user.id); db.add(row); db.flush()
    case.updated_by = str(user.id)
    from utils.datetime_utils import beijing_now
    case.updated_at = beijing_now()
    snapshot_case(db, case, str(user.id), '修改原生用例配置')
    logger.info('原生用例配置已保存 project_id={} case_id={} revision={}', project_id, case_id, row.revision)
    return config_data(db, user, project_id, case_id)


def content_changed(case, snapshot, *, current_read=False):
    if case.type not in STATES:
        return False
    from sqlalchemy.orm import object_session
    return fingerprint(config_snapshot(object_session(case), case, current_read=current_read)) != fingerprint(snapshot.get('native_config'))
