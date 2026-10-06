"""临时MySQL保存提取协议、冻结模板与并发入队；不连接业务目标。"""

import asyncio
import importlib.util
import json
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
sys.path.insert(0, str(ROOT / "xat"))
logging.basicConfig(
    filename=ROOT / "logs/第70部分MySQL验收.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("提取器数据库验收")


def verify(db):
    import httpx
    from models.native_case import NativeCaseConfig, ApiDefinition
    from models import TestCase
    from services.native_http_execution import _request
    from framework.native_http.models import FrozenCase
    from framework.native_http.engine import execute

    case = db.get(TestCase, "case-0")
    definition = ApiDefinition(
        id="extract70-definition",
        project_id=case.project_id,
        name="隔离提取定义",
        protocol="HTTP",
        path="http://owned.test/echo",
        parameters={},
        updated_by="owner",
    )
    config = db.get(NativeCaseConfig, case.id)
    if config is None:
        config = NativeCaseConfig(case_id=case.id, state="DONE", updated_by="owner")
        db.add(config)
    db.add(definition)
    db.flush()
    config.api_definition_id = definition.id
    config.environment_id = None
    extractor = dict(
        id="row",
        variableName="变量",
        variableType="TEMPORARY",
        expression="$.value",
        extractType="JSON_PATH",
        resultMatchingRule="SPECIFIC",
        resultMatchingRuleNum=1,
        description="中文描述",
        enable=True,
    )
    config.parameters = {
        "request": dict(
            method="POST",
            bodyType="json",
            body={"previous": "${变量}"},
            postProcessorConfig={
                "processors": [
                    dict(
                        id="post",
                        name="参数提取",
                        enable=True,
                        processorType="EXTRACT",
                        extractors=[extractor],
                    )
                ]
            },
        )
    }
    db.commit()
    db.expire_all()
    loaded = db.get(NativeCaseConfig, case.id)
    assert (
        loaded.parameters["request"]["postProcessorConfig"]["processors"][0][
            "extractors"
        ][0]
        == extractor
    )
    frozen = _request(db, case, loaded, None)
    loaded.parameters = {"request": {"method": "GET"}}
    db.commit()
    assert (
        frozen.postProcessorConfig.processors[0].extractors[0].description == "中文描述"
    )
    sent = []

    def target(request):
        sent.append(json.loads(request.content))
        return httpx.Response(201, json={"value": 7})

    out = asyncio.run(
        execute(
            FrozenCase(id=case.id, category="scenario", requests=[frozen, frozen]),
            transport=httpx.MockTransport(target),
        )
    )
    assert out["status"] == "passed" and sent == [
        {"previous": "${变量}"},
        {"previous": "7"},
    ]
    assert (
        out["native_detail"]["steps"][1]["attempts"][0]["extractResults"][0]["value"]
        == "7"
    )
    log.info(
        "MySQL保留中文和高级设置；修改当前配置不改变冻结提取；内存Transport两步骤传递成功，未连接业务目标"
    )


if __name__ == "__main__":
    try:
        spec = importlib.util.spec_from_file_location(
            "extract_mysql_base", ROOT / "scripts/verify_plan_native_http_mysql.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.main(verify_request=verify)
    except Exception:
        log.exception("提取器MySQL隔离验收失败")
        raise
