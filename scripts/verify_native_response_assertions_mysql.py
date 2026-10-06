"""复用独立MySQL基座，验证响应断言真实保存及冻结；不发送HTTP。"""

import importlib.util
import logging
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
logging.basicConfig(
    filename=ROOT / "logs/第66部分MySQL验收.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("响应断言数据库验收")


def verify(db):
    from models import User, TestCase
    from models.native_case import NativeCaseConfig
    from services.native_case import save_config
    from schemas.native_case import ConfigInput
    from services.native_http_execution import freeze

    groups = [
        {
            "id": "time",
            "name": "响应时间",
            "assertionType": "RESPONSE_TIME",
            "expectedValue": 5000,
        },
        {
            "id": "code",
            "name": "状态码",
            "assertionType": "RESPONSE_CODE",
            "expectedValue": "201",
            "condition": "EQUALS",
        },
        {
            "id": "body",
            "name": "响应体",
            "assertionType": "RESPONSE_BODY",
            "assertionBodyType": "JSON_PATH",
            "jsonPathAssertion": {
                "assertions": [
                    {
                        "expression": "$.value",
                        "condition": "EQUALS",
                        "expectedValue": "7",
                        "enable": False,
                    }
                ]
            },
            "xpathAssertion": {
                "responseFormat": "HTML",
                "assertions": [{"expression": "//p", "enable": True}],
            },
            "regexAssertion": {
                "assertions": [{"expression": "accepted", "enable": True}]
            },
        },
        {
            "id": "header",
            "name": "响应头",
            "assertionType": "RESPONSE_HEADER",
            "enable": False,
            "assertions": [
                {
                    "header": "X-Lab",
                    "condition": "CONTAINS",
                    "expectedValue": "owned",
                    "enable": True,
                }
            ],
        },
    ]
    row = db.get(NativeCaseConfig, "case-0")
    original_revision = row.revision
    save_config(
        db,
        db.get(User, "owner"),
        "project",
        "case-0",
        ConfigInput(
            state="DONE",
            apiDefinitionId="http-definition",
            environmentId="http-env",
            expectedRevision=original_revision,
            expectedDefinitionRevision=1,
            parameters={
                "request": {
                    "responseAssertions": groups,
                    "assertions": [
                        {"source": "status", "operator": "equals", "expected": 201}
                    ],
                }
            },
        ),
    )
    db.flush()
    db.expire_all()
    row = db.get(NativeCaseConfig, "case-0")
    assert row.revision == original_revision + 1
    frozen = freeze(db, db.get(TestCase, "case-0"), db.get(User, "owner"))["requests"][
        0
    ]
    saved = row.parameters["request"]["responseAssertions"]
    assert saved == groups
    assert [g["id"] for g in frozen["responseAssertions"]] == [g["id"] for g in groups]
    assert frozen["responseAssertions"][2]["xpathAssertion"]["responseFormat"] == "HTML"
    assert not frozen["responseAssertions"][2]["jsonPathAssertion"]["assertions"][0][
        "enable"
    ]
    assert not frozen["responseAssertions"][3]["enable"]
    assert frozen["assertions"][0]["expected"] == 201
    log.info(
        "四类断言顺序/禁用分组及行/三类正文缓存/旧断言真实保存和版本冻结通过；本段回滚，无HTTP发送"
    )


if __name__ == "__main__":
    try:
        spec = importlib.util.spec_from_file_location(
            "native_mysql_base", ROOT / "scripts/verify_plan_native_http_mysql.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.main(verify_request=verify)
    except Exception:
        log.exception("响应断言MySQL验收失败")
        raise
