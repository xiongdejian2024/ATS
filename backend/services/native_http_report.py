"""按冻结执行身份读取原生HTTP实际详情，不从最新配置推测历史结果。"""

import json
import sys
from pathlib import Path
from fastapi import HTTPException
from core.logger import logger
from models.plan_orchestration import PlanRunItem
from models.test_suite import TestSuiteExecution
from services.suite_results import result_id


def contract():
    xat = str(Path(__file__).resolve().parents[2] / "xat")
    if xat not in sys.path:
        sys.path.insert(0, xat)
    from framework.native_http.result_details import NativeDetail, DETAIL_LIMIT

    return NativeDetail, DETAIL_LIMIT


def validate_detail(raw, suite, task, case_id, db):
    from services.native_http_execution import COMMAND

    model, limit = contract()
    try:
        if (
            suite.execution_command != COMMAND
            or len(json.dumps(raw, ensure_ascii=False).encode("utf-8")) > limit
        ):
            raise ValueError("实际详情不属于原生HTTP或超过范围")
        detail = model.model_validate(raw)
        item = (
            db.query(PlanRunItem)
            .filter_by(execution_id=task.execution_id)
            .one_or_none()
        )
        frozen = next(
            (
                c
                for c in (
                    (item.suite_snapshot.get("nativeCases") or []) if item else []
                )
                if c["id"] == case_id
            ),
            None,
        )
        if frozen and detail.totalSteps != len(frozen["requests"]):
            raise ValueError("实际详情步骤数与冻结请求范围不一致")
        return detail.model_dump()
    except Exception:
        logger.exception(
            "原生HTTP详情校验失败：执行={}，用例={}", task.execution_id, case_id
        )
        raise


def read_detail(db, run, execution_id, case_id):
    item = (
        db.query(PlanRunItem)
        .filter_by(run_id=run.id, execution_id=execution_id)
        .one_or_none()
    )
    if not item or case_id not in item.suite_snapshot.get("caseIds", []):
        raise HTTPException(404, "本批次不存在此执行用例")
    frozen = next(
        (
            c
            for c in (item.suite_snapshot.get("nativeCases") or [])
            if c["id"] == case_id
        ),
        None,
    )
    row = db.get(TestSuiteExecution, result_id(execution_id, case_id))
    base = dict(
        executionId=execution_id,
        caseId=case_id,
        category=item.suite_snapshot.get("category", "api"),
        result=row.result if row else item.status,
        duration=row.duration if row else None,
    )
    if row and row.native_detail:
        model, _ = contract()
        try:
            return dict(
                base,
                available=True,
                detail=model.model_validate(row.native_detail).model_dump(),
            )
        except Exception:
            logger.exception(
                "历史原生HTTP详情格式无效：执行={}，用例={}", execution_id, case_id
            )
            raise HTTPException(500, "实际HTTP详情格式无效，请核对服务日志")
    return dict(
        base,
        available=False,
        detail=None,
        message="此执行尚未回传HTTP详情" if not row else "此历史执行未保存HTTP交换详情",
        native=bool(frozen),
    )
