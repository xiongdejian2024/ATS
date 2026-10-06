"""复用独立MySQL基座，验证历史迁移、实际详情JSON回读及精确回收。"""

import asyncio
import importlib.util
import logging
import sys
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "xat"))
logging.basicConfig(
    filename=ROOT / "logs/第67部分MySQL验收.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("HTTP报告数据库验收")


def verify(db):
    from sqlalchemy import text
    from models.test_suite import TestSuiteExecution
    from framework.native_http.engine import execute
    from framework.native_http.models import FrozenCase, FrozenRequest
    import httpx

    identifier = str(uuid4())
    row = TestSuiteExecution(
        id=identifier,
        suite_id="suite",
        case_id="case-0",
        environment_id="offline",
        executor_id="owner",
        result="passed",
        duration="0.01s",
        log_output="历史日志保留",
    )
    db.add(row)
    db.commit()
    try:
        # 历史表DDL前先提交准备事务，避免元数据锁等待。
        with db.bind.begin() as connection:
            connection.execute(
                text("ALTER TABLE test_suite_executions DROP COLUMN native_detail")
            )
        spec = importlib.util.spec_from_file_location(
            "http_detail_upgrade", ROOT / "scripts/upgrade_native_http_detail.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        assert module.upgrade(False, db.bind) == ["native_detail"]
        assert module.upgrade(True, db.bind) == ["native_detail"]
        assert module.upgrade(True, db.bind) == []
        db.expire_all()
        row = db.get(TestSuiteExecution, identifier)
        assert (
            row.native_detail is None
            and row.log_output == "历史日志保留"
            and row.result == "passed"
        )
        result = asyncio.run(
            execute(
                FrozenCase(
                    id="case-0",
                    category="api",
                    requests=[
                        FrozenRequest(
                            name="数据库实际交换",
                            url="http://loopback.test/",
                            assertions=[dict(expected=201)],
                        )
                    ],
                ),
                transport=httpx.MockTransport(
                    lambda _: httpx.Response(
                        201,
                        headers=[("Set-Cookie", "a=1"), ("Set-Cookie", "b=2")],
                        json={"实际": "响应"},
                    )
                ),
            )
        )
        row.native_detail = result["native_detail"]
        db.commit()
        db.expire_all()
        row = db.get(TestSuiteExecution, identifier)
        assert row.native_detail == result["native_detail"]
        actual = row.native_detail["steps"][0]["attempts"][0]
        assert (
            actual["assertions"][0]["actualValue"] == "201"
            and actual["response"]["body"]["byteLength"] > 0
        )
        assert (
            len(
                [
                    h
                    for h in actual["response"]["headers"]
                    if h[0].lower() == "set-cookie"
                ]
            )
            == 2
        )
        log.info(
            "MySQL历史执行日志及结果保留、可空详情迁移幂等、实际响应字节/重复头/断言JSON回读通过；MockTransport无网络发送"
        )
    finally:
        db.rollback()
        row = db.get(TestSuiteExecution, identifier)
        if row:
            db.delete(row)
            db.commit()
        log.info("独立历史样本已按唯一ID回收")


if __name__ == "__main__":
    try:
        spec = importlib.util.spec_from_file_location(
            "native_mysql_base", ROOT / "scripts/verify_plan_native_http_mysql.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.main(verify_request=verify)
    except Exception:
        log.exception("HTTP报告MySQL验收失败")
        raise
