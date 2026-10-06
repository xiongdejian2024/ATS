"""复用独立MySQL基座，验证真实参数元数据保存、版本和冻结；不发送HTTP。"""

import importlib.util
import logging
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
logging.basicConfig(
    filename=ROOT / "logs/第65部分MySQL验收.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("请求参数数据库验收")


def verify(db):
    from models import User, TestCase
    from models.native_case import ApiDefinition, NativeCaseConfig
    from services.native_case import save_config
    from schemas.native_case import ConfigInput
    from services.native_http_execution import freeze

    definition = db.get(ApiDefinition, "http-definition")
    definition.path = "/items/{id}"
    db.flush()
    config = db.get(NativeCaseConfig, "case-0")
    body = ConfigInput(
        state="DONE",
        apiDefinitionId=definition.id,
        environmentId="http-env",
        expectedRevision=config.revision,
        expectedDefinitionRevision=definition.revision,
        parameters={
            "request": {
                "method": "POST",
                "queryParams": [
                    {
                        "key": "q",
                        "value": "中文",
                        "enable": False,
                        "description": "禁用仍保留",
                    }
                ],
                "headerParams": [{"key": "X-Test", "value": "value"}],
                "restParams": [{"key": "id", "value": "one/two"}],
                "bodyType": "form",
                "body": {},
                "formParams": [{"key": "field", "value": "text"}],
                "authConfig": {
                    "authType": "BASIC",
                    "basicAuth": {
                        "userName": "local-reader",
                        "password": "temporary-only",
                    },
                },
                "connectTimeoutMs": 0,
                "responseTimeoutMs": 5000,
            }
        },
    )
    save_config(db, db.get(User, "owner"), "project", "case-0", body)
    db.flush()
    db.expire_all()
    row = db.get(NativeCaseConfig, "case-0")
    assert row.parameters["request"]["queryParams"][0]["description"] == "禁用仍保留"
    assert not row.parameters["request"]["queryParams"][0]["enable"]
    frozen = freeze(db, db.get(TestCase, "case-0"), db.get(User, "owner"))["requests"][
        0
    ]
    assert frozen["url"] == "http://127.0.0.1:2/items/one%2Ftwo"
    assert (
        frozen["authConfig"]["basicAuth"]["userName"] == "local-reader"
        and frozen["formParams"][0]["value"] == "text"
    )
    assert frozen["connectTimeoutMs"] == 0 and frozen["responseTimeoutMs"] == 5000
    log.info(
        "MySQL参数启停/描述/REST/表单/认证/超时真实保存及版本冻结通过；本段回滚，无HTTP发送"
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
        log.exception("请求参数MySQL验收失败")
        raise
