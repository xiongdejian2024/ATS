"""快速提取仅评估历史实际响应，不访问目标，不生成执行记录。"""

import base64
import httpx
from fastapi import HTTPException
from core.logger import logger
from core.project_access import require_project_access
from services.case_governance import case_for_project
from models.test_suite import TestSuiteExecution
from framework.native_http.extractions import matches, sample_values
from framework.native_http.result_details import NativeDetail


def latest_response(db, user, project_id, case_id):
    require_project_access(db, user, project_id)
    case = case_for_project(db, project_id, case_id)
    if case.type != "api":
        raise HTTPException(422, "快速提取需选择API用例")
    row = (
        db.query(TestSuiteExecution)
        .filter_by(case_id=case_id)
        .filter(TestSuiteExecution.native_detail.is_not(None))
        .order_by(TestSuiteExecution.executed_at.desc(), TestSuiteExecution.id.desc())
        .first()
    )
    if not row:
        return dict(
            available=False,
            response=None,
            executionId=None,
            message="请先执行请求，取得实际响应后使用快速提取",
        )
    try:
        detail = NativeDetail.model_validate(row.native_detail)
        attempt = next(
            (
                a
                for s in reversed(detail.steps)
                for a in reversed(s.attempts)
                if a.response and a.request
            ),
            None,
        )
        if not attempt:
            return dict(
                available=False,
                response=None,
                executionId=row.id,
                message="最近执行未取得响应",
            )
        complete = not (
            attempt.response.body.truncated
            or attempt.response.headersTruncated
            or attempt.request.headersTruncated
        )
        return dict(
            available=complete,
            response=attempt.model_dump(),
            executionId=row.id,
            message="" if complete else "实际响应已截断，无法用于完整提取测试",
        )
    except Exception:
        logger.exception(
            "读取快速提取实际响应失败：项目={}，用例={}", project_id, case_id
        )
        raise HTTPException(500, "实际响应格式无效，请核对服务日志")


def preview(db, user, project_id, case_id, rule, expected_execution_id):
    source = latest_response(db, user, project_id, case_id)
    if not source["available"]:
        raise HTTPException(409, source["message"])
    if source["executionId"] != expected_execution_id:
        raise HTTPException(409, "响应已更新，请重新打开快速提取后测试")
    data = source["response"]
    response = httpx.Response(
        data["response"]["statusCode"],
        content=base64.b64decode(data["response"]["body"]["base64"]),
        headers=data["response"]["headers"],
        extensions={
            "http_version": data["response"]["httpVersion"].encode("ascii"),
            "reason_phrase": data["response"]["reason"].encode("latin-1"),
        },
        request=httpx.Request(
            data["request"]["method"],
            data["request"]["url"],
            headers=data["request"]["headers"],
        ),
    )
    response.encoding = data["response"]["body"]["charset"]
    try:
        values = sample_values(rule, matches(rule, response))
        if sum(len(v.encode("utf-8")) for v in values) > 1024 * 1024:
            raise ValueError("快速提取结果超过1MiB")
        # 预览保留全部匹配；实际执行由结果匹配规则选择并生成变量。
        return dict(values=values, executionId=source["executionId"])
    except Exception as exception:
        logger.exception(
            "快速提取表达式测试失败：项目={}，用例={}", project_id, case_id
        )
        raise HTTPException(
            422, "表达式评估失败：" + type(exception).__name__
        ) from exception
