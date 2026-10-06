"""把主原生配置冻结为实际HTTP执行输入；环境是请求目标，资源节点另行选择。"""

from copy import deepcopy
from urllib.parse import urljoin, urlsplit
from uuid import uuid5, NAMESPACE_URL
from fastapi import HTTPException
from models import TestCase, TestSuite, Environment
from models.native_case import NativeCaseConfig, ApiDefinition, ApiTestEnvironment
from services.plan_candidate_project import require_case_sources
from core.logger import logger
from framework.native_http.models import (
    RequestSpec,
    FrozenRequest,
    FrozenCase,
    ScenarioSpec,
)

COMMAND = "ats-native-http"


def read(db, model, identity, *, current_read=True):
    query = (
        db.query(model).filter(model.case_id == identity)
        if model is NativeCaseConfig
        else db.query(model).filter_by(id=identity)
    )
    return (
        query.populate_existing().with_for_update() if current_read else query
    ).one_or_none()


def configured(db, case):
    if case.type not in {"api", "scenario"}:
        return False
    config = read(db, NativeCaseConfig, case.id)
    if not config:
        return False
    parameters = config.parameters or {}
    if case.type == "scenario":
        return "scenario" in parameters
    return "request" in parameters


def freeze(db, case, user, *, environment_id=None):
    try:
        config = read(db, NativeCaseConfig, case.id)
        if not config:
            raise ValueError("原生用例缺少请求配置")
        if case.type == "api":
            requests = [_request(db, case, config, environment_id)]
            stopped = True
        elif case.type == "scenario":
            scenario = ScenarioSpec.model_validate(config.parameters.get("scenario"))
            requests = []
            for step in scenario.steps:
                if not step.enabled:
                    continue
                child = read(db, TestCase, step.apiCaseId)
                if (
                    not child
                    or child.deleted_at
                    or child.type != "api"
                    or child.project_id != case.project_id
                ):
                    raise ValueError("场景步骤须引用同来源项目中未回收的API用例")
                require_case_sources(db, user.id, [child], current_read=True)
                child_config = read(db, NativeCaseConfig, child.id)
                if not child_config:
                    raise ValueError("场景步骤API缺少请求配置")
                requests.append(
                    _request(
                        db, child, child_config, environment_id or config.environment_id
                    )
                )
            if not requests:
                raise ValueError("场景至少需要一个启用的实际请求步骤")
            stopped = scenario.stopOnFailure
        else:
            raise ValueError("原生HTTP执行只支持API用例或场景")
        return FrozenCase(
            id=case.id, category=case.type, requests=requests, stopOnFailure=stopped
        ).model_dump()
    except ValueError as exception:
        logger.exception("原生HTTP冻结校验失败：用例={}", case.id)
        raise HTTPException(
            409, "原生HTTP请求、环境、断言或场景步骤配置无效，请检查配置后重试"
        ) from exception


def _request(db, case, config, override_environment):
    definition = (
        read(db, ApiDefinition, config.api_definition_id)
        if config.api_definition_id
        else None
    )
    if (
        not definition
        or definition.project_id != case.project_id
        or definition.protocol not in {"HTTP", "HTTPS"}
    ):
        raise ValueError("原生HTTP用例须关联同来源项目的HTTP接口定义")
    request = RequestSpec.model_validate(
        deepcopy((config.parameters or {}).get("request"))
    )
    from framework.native_http.parameters import path_parameters

    # 含变量的REST值要到Agent拿到前序响应后再编码，冻结原始占位路径。
    path = (
        definition.path
        if any(r.enable and "${" in r.value for r in (request.restParams or []))
        else path_parameters(definition.path, request.restParams)
    )
    target_id = override_environment or config.environment_id
    target = read(db, ApiTestEnvironment, target_id) if target_id else None
    if target_id and (not target or target.project_id != case.project_id):
        raise ValueError("请求环境不属于接口来源项目或已删除")
    if target:
        if urlsplit(path).scheme or path.startswith("//"):
            raise ValueError("使用请求环境时，接口路径须为相对路径，不能覆盖环境主机")
        url = urljoin(target.address.rstrip("/") + "/", path)
    else:
        url = path
    from services.native_request_files import frozen_files

    return FrozenRequest(
        **request.model_dump(exclude={"bodyDrafts", "jsonBody"}),
        files=frozen_files(db, case.project_id, request),
        name=case.name,
        url=url,
    )


def managed_suite(db, plan, case, node_id, actor_id):
    """真实原生执行模板是队列协议适配记录；没有shell命令或用户仓库。"""
    identity = str(uuid5(NAMESPACE_URL, f"ats-native-http:{plan.id}:{case.id}"))
    suite = read(db, TestSuite, identity)
    if suite:
        if (
            suite.plan_id != plan.id
            or suite.execution_command != COMMAND
            or suite.case_ids != [case.id]
        ):
            raise HTTPException(409, "原生执行模板身份冲突，请检查执行记录")
        if node_id:
            resource = read(db, Environment, node_id)
            if not resource or not resource.status:
                raise HTTPException(409, "执行资源节点不存在或已停用")
            suite.environment_id = node_id
        return suite
    if not node_id:
        raise HTTPException(
            409, "请先为测试计划或测试集配置执行资源节点；请求环境不是执行节点"
        )
    resource = read(db, Environment, node_id)
    if not resource or not resource.status:
        raise HTTPException(409, "执行资源节点不存在或已停用")
    suite = TestSuite(
        id=identity,
        plan_id=plan.id,
        name=case.name,
        environment_id=node_id,
        execution_command=COMMAND,
        case_ids=[case.id],
        git_enabled="false",
        created_by=str(actor_id),
    )
    db.add(suite)
    db.flush()
    return suite
