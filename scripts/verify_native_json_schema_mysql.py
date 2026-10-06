"""独立临时MySQL保存Schema与JSON，冻结后编辑仍保持正文，无网络任务。"""

import importlib.util, json, logging, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
sys.path.insert(0, str(ROOT / "xat"))
logging.basicConfig(
    filename=ROOT / "logs/第69部分MySQL验收.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("Schema数据库验收")


def verify(db):
    from models.native_case import NativeCaseConfig, ApiDefinition
    from models import TestCase
    from services.native_http_execution import _request
    from services.native_json_schema import convert_schema
    from framework.native_http.schema_models import JsonSchemaItem

    case = db.get(TestCase, "case-0")
    definition = ApiDefinition(
        id="schema69-definition",
        project_id=case.project_id,
        name="隔离Schema定义",
        protocol="HTTP",
        path="http://owned.test/echo",
        parameters={},
        updated_by="owner",
    )
    tree = {
        "type": "object",
        "properties": {
            "data": {
                "type": "array",
                "items": [
                    {"type": "integer", "defaultValue": 7},
                    {"type": "string", "example": "原正文"},
                ],
            }
        },
        "required": ["data"],
    }
    body = json.loads(
        convert_schema(JsonSchemaItem.model_validate(tree), preview=False)
    )
    config = db.get(NativeCaseConfig, case.id)
    if config is None:
        config = NativeCaseConfig(case_id=case.id, state="DONE", updated_by="owner")
        db.add(config)
    db.add(definition)
    db.flush()
    config.api_definition_id = definition.id
    config.environment_id = None
    config.parameters = {
        "request": {
            "bodyType": "json",
            "body": body,
            "jsonBody": {"enableJsonSchema": True, "jsonSchema": tree},
        }
    }
    db.commit()
    db.expire_all()
    loaded = db.get(NativeCaseConfig, case.id)
    assert loaded.parameters["request"]["jsonBody"]["jsonSchema"] == tree
    frozen = _request(db, case, loaded, None)
    assert frozen.body == body and frozen.jsonBody is None
    loaded.parameters = {"request": {"bodyType": "json", "body": {"changed": True}}}
    db.commit()
    assert frozen.body == body
    log.info(
        "MySQL JSON保持中文、元组、必填与模式；冻结剔除Schema并保留原Json正文；未发送网络任务"
    )


if __name__ == "__main__":
    try:
        spec = importlib.util.spec_from_file_location(
            "schema_mysql_base", ROOT / "scripts/verify_plan_native_http_mysql.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.main(verify_request=verify)
    except Exception:
        log.exception("Schema MySQL隔离验收失败")
        raise
