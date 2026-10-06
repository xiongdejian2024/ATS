"""复用独立临时MySQL验收基座，验证接口协议与列筛选SQL范围；不触发执行。"""

import importlib.util
import logging
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
logging.basicConfig(
    filename=ROOT / "logs/第64部分MySQL验收.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("关联接口基础筛选验收")


def verify_basic(db, user):
    from models import TestPlan
    from models.native_case import ApiDefinition
    from schemas.plan_candidate_selection import CandidateCondition, CandidateSelection
    from services.plan_case_workspace import candidates
    from services.plan_candidate_selection import preview

    history = db.get(ApiDefinition, "history")
    history.parameters = {"request": {"method": "POST"}}
    history.created_by = "owner"
    db.get(ApiDefinition, "excluded").protocol = "TCP"
    db.commit()
    condition = CandidateCondition(
        protocols=["HTTP"], methods=["POST"], createdBy=["owner"]
    )
    listing = candidates(
        db,
        db.get(TestPlan, "plan"),
        "api",
        "",
        "all",
        None,
        1,
        20,
        resource_type="API",
        condition=condition,
        sort="name",
        direction="asc",
        user_id="owner",
    )
    assert listing["total"] == listing["counts"]["all"] == 1
    assert (
        listing["items"][0]["id"] == "history" and listing["items"][0]["caseTotal"] == 2
    )
    filtered_selection = CandidateSelection(
        category="api",
        resourceType="API",
        moduleMaps={"all": {"selectAll": True}},
        condition=condition,
    )
    summary = preview(db, db.get(TestPlan, "plan"), user, filtered_selection)
    assert summary["count"] == 2 and summary["selectedDefinitionCount"] == 1
    assert summary["moduleCounts"]["module"] == {"total": 1, "selected": 1}
    db.commit()
    empty_listing = candidates(
        db,
        db.get(TestPlan, "plan"),
        "api",
        "",
        "all",
        None,
        1,
        20,
        resource_type="CASE",
        condition=CandidateCondition(protocols=[]),
    )
    assert empty_listing["total"] == empty_listing["counts"]["all"] == 0
    log.info(
        "MySQL嵌套JSON请求方式、协议与创建人联合SQL分页和目录计数通过；模块全选只展开当前真实子用例，空协议返回0"
    )


if __name__ == "__main__":
    try:
        spec = importlib.util.spec_from_file_location(
            "definition_mysql_base", ROOT / "scripts/verify_plan_definition_mysql.py"
        )
        baseline = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(baseline)
        baseline.main(verify_basic=verify_basic)
    except Exception:
        log.exception("关联接口基础筛选MySQL验收失败")
        raise
