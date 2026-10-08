"""原生配置事务、项目归属和版本冲突；不提交网络或台架任务。"""
from copy import deepcopy
from sqlalchemy.orm.attributes import flag_modified
import hashlib
import json
from fastapi import HTTPException
from models.native_case import ApiDefinition, ApiTestEnvironment, NativeCaseConfig
from models.native_environment_variables import NativeEnvironmentVariables
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
    definitions = rows(ApiDefinition, ['name', 'protocol', 'path', 'parameters', 'module_id', 'state', 'tags', 'created_by'])
    from models import TestCase
    environments = rows(ApiTestEnvironment, ['name', 'address'])
    declarations = {r.environment_id: r.variables for r in db.query(NativeEnvironmentVariables).filter(NativeEnvironmentVariables.environment_id.in_([r['id'] for r in environments])).all()}
    for item in environments:
        item['variables'] = deepcopy(declarations.get(item['id'], []))
    return dict(definitions=definitions, environments=environments,
                apiCases=[dict(id=c.id, name=c.name) for c in db.query(TestCase).filter_by(project_id=project_id, type='api').filter(TestCase.deleted_at.is_(None)).order_by(TestCase.created_at, TestCase.id)],
                protocols=sorted({r['protocol'] for r in definitions}),
                canCreate=project_allows(db, user, project, 'test_case:create'),
                canEdit=project_allows(db, user, project, 'test_case:update'))


def save_entity(db, user, project_id, model, body, identity=None):
    require_project_access(db, user, project_id, 'test_case:update' if identity else 'test_case:create')
    lock_project(db, project_id)
    from models import User
    user = db.query(User).filter_by(id=user.id).populate_existing().with_for_update(read=True).first()
    if not user or not user.status:
        raise HTTPException(403, '当前用户不存在或已被禁用')
    require_project_access(db, user, project_id, 'test_case:update' if identity else 'test_case:create', current_read=True)
    row = entity(db, model, project_id, identity, lock=True) if identity else model(project_id=project_id, revision=0)
    if row.revision != body.expectedRevision:
        raise HTTPException(409, '配置已经被修改，请刷新后重试；当前草稿可保留')
    if model is ApiDefinition and 'request' in body.parameters:
        validate_parameters(db, project_id, 'api', body.parameters, body.protocol)
    if model is ApiDefinition and body.module_id:
        from models import Module
        entity(db, Module, project_id, body.module_id, lock=True)
    # 旧客户端没有提交元数据时保留原值；不能用默认空值覆盖新客户端已保存的模块。
    values = body.model_dump(exclude={'expectedRevision', 'variables'})
    if model is ApiDefinition:
        for field in {'module_id', 'state', 'tags'} - body.model_fields_set:
            values.pop(field, None)
        if not identity:
            row.created_by = str(user.id)
    for field, value in values.items():
        setattr(row, field, deepcopy(value))
    if model is ApiDefinition:
        flag_modified(row, "parameters")
    row.updated_by = str(user.id)
    row.revision += 1
    db.add(row); db.flush()
    if model is ApiTestEnvironment and (not identity or 'variables' in body.model_fields_set):
        declarations = db.query(NativeEnvironmentVariables).filter_by(environment_id=row.id).populate_existing().with_for_update().first()
        if declarations is None:
            declarations = NativeEnvironmentVariables(environment_id=row.id)
        declarations.variables = [v.model_dump() for v in body.variables]
        db.add(declarations)
        db.flush()
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
    lock_project(db, project_id)
    from models import User
    user = db.query(User).filter_by(id=user.id).populate_existing().with_for_update(read=True).first()
    if not user or not user.status:
        raise HTTPException(403, '当前用户不存在或已被禁用')
    require_project_access(db, user, project_id, 'test_case:update', current_read=True)
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
    native = validate_parameters(db, project_id, case.type, body.parameters, definition.protocol if definition else None)
    from services.case_governance import snapshot_case
    snapshot_case(db, case, str(user.id), '原生配置修改前保存版本')
    if not row: row = NativeCaseConfig(case_id=case.id, revision=0)
    if native:
        case.is_automated = True
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


def validate_parameters(db, project_id, category, parameters, protocol=None):
    """声明式请求配置保存前校验；配置实际执行后即为自动化用例。"""
    from models import TestCase
    try:
        if category == 'api' and 'request' in parameters:
            from framework.native_http.models import RequestSpec
            if protocol not in {'HTTP', 'HTTPS'}: raise ValueError('请求配置仅用于HTTP/HTTPS接口')
            request = RequestSpec.model_validate(parameters['request'])
            from services.native_request_files import rows_for_request
            rows_for_request(db, project_id, request)
            return True
        if category == 'scenario' and 'scenario' in parameters:
            from framework.native_http.models import ScenarioSpec
            scenario = ScenarioSpec.model_validate(parameters['scenario'])
            ids = {step.apiCaseId for step in scenario.steps}
            children = db.query(TestCase).filter(TestCase.id.in_(ids), TestCase.project_id == project_id, TestCase.type == 'api', TestCase.deleted_at.is_(None)).populate_existing().with_for_update().all()
            if len(children) != len(ids) or not any(step.enabled for step in scenario.steps):
                raise ValueError('场景需启用至少一个同项目API用例步骤')
            return True
        return False
    except ValueError as exception:
        logger.exception('保存原生执行配置校验失败：项目={}，分类={}', project_id, category)
        raise HTTPException(422, '请求体、断言或场景步骤配置无效，请检查后重试') from exception


def content_changed(case, snapshot, *, current_read=False):
    if case.type not in STATES:
        return False
    from sqlalchemy.orm import object_session
    return fingerprint(config_snapshot(object_session(case), case, current_read=current_read)) != fingerprint(snapshot.get('native_config'))
