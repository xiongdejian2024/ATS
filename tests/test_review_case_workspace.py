"""关联用例真实分页、当前元数据、模块范围和独立快照读取。"""

import uuid
from sqlalchemy import event
from test_case_governance import governance, request_review
from test_review_workspace import endpoint
from models import Module
from models.case_governance import CaseVersion
from schemas.test_case import TestCaseCreate as CaseCreate
from services.test_case_service import TestCaseService
from utils.datetime_utils import beijing_now


def rows(g, review, **params):
    response = g["client"].get(endpoint(g) + f"/{review['id']}/items", params=params)
    assert response.status_code == 200, response.text
    return response.json()["data"]


def prepare(g):
    parent = Module(id=str(uuid.uuid4()), project_id=g["project"].id, name="父模块")
    child = Module(
        id=str(uuid.uuid4()),
        project_id=g["project"].id,
        name="子模块",
        parent_id=parent.id,
    )
    foreign = Module(
        id=str(uuid.uuid4()), project_id=g["foreign"].project_id, name="其他项目模块"
    )
    g["db"].add_all([parent, child, foreign])
    g["db"].commit()
    cases = list(g["cases"])
    for i in range(21):
        cases.append(
            TestCaseService.create_test_case(
                g["db"],
                CaseCreate(
                    project_id=g["project"].id,
                    name=f"列表用例{i:02d}",
                    type="functional",
                    priority="P3",
                ),
                g["users"][0].id,
            )
        )
    cases[0].name, cases[0].case_code, cases[0].module_id = (
        "_% 精确搜索",
        "列表-001",
        parent.id,
    )
    cases[1].name, cases[1].module_id, cases[1].tags = (
        "子模块用例",
        child.id,
        ["中文标签"],
    )
    g["db"].commit()
    review = request_review(
        g, cases=[c.id for c in cases], reviewers=[g["users"][1].id]
    )
    return review, cases, parent, child, foreign


def test_database_pages_modules_literal_search_tags_and_live_metadata(governance):
    g = governance
    review, cases, parent, child, foreign = prepare(g)
    first = rows(g, review, size=20, sort="name", order="asc")
    second = rows(g, review, page=2, size=20, sort="name", order="asc")
    assert (
        first["total"] == 23 and len(first["items"]) == 20 and len(second["items"]) == 3
    )
    assert not ({i["id"] for i in first["items"]} & {i["id"] for i in second["items"]})
    mind = rows(g, review, view="mind", size=10)
    assert mind["total"] == 23 and len(mind["items"]) == 23
    counts = {m["id"]: m["count"] for m in first["modules"]}
    assert counts[parent.id] == 2 and counts[child.id] == 1
    assert first["counts"] == {"all": 23, "unassigned": 21}
    assert rows(g, review, folder=parent.id)["total"] == 2
    assert rows(g, review, folder=parent.id, includeDescendants=False)["total"] == 1
    assert rows(g, review, folder="unassigned")["total"] == 21
    assert rows(g, review, search="_%")["total"] == 1
    assert rows(g, review, search="中文标签")["items"][0]["caseId"] == cases[1].id
    assert rows(g, review, search="列表-001")["total"] == 1
    assert rows(g, review, priority="P3")["total"] == 21
    original = next(i for i in review["items"] if i["caseId"] == cases[0].id)
    cases[0].name = "当前新名称"
    cases[0].module_id = child.id
    g["db"].commit()
    current = rows(g, review, search="当前新名称")["items"][0]
    assert current["name"] == "当前新名称" and current["moduleId"] == child.id
    assert (
        current["snapshot"]["name"] == original["snapshot"]["name"]
        and current["outdated"]
    )
    assert (
        g["client"]
        .get(endpoint(g) + f"/{review['id']}/items", params={"folder": foreign.id})
        .status_code
        == 404
    )
    assert (
        g["client"]
        .get(endpoint(g) + f"/{review['id']}/items", params={"sort": "非法"})
        .status_code
        == 422
    )
    assert (
        g["client"]
        .get(endpoint(g) + f"/{review['id']}/items", params={"size": 101})
        .status_code
        == 422
    )


def test_detail_is_compact_and_individual_snapshot_survives_recycle(governance):
    g = governance
    review, cases, _, _, _ = prepare(g)
    statements = []

    def record(connection, cursor, statement, parameters, context, executemany):
        statements.append(statement)

    event.listen(g["db"].bind, "before_cursor_execute", record)
    try:
        response = g["client"].get(endpoint(g) + f"/{review['id']}/detail")
    finally:
        event.remove(g["db"].bind, "before_cursor_execute", record)
    assert response.status_code == 200, response.text
    detail = response.json()["data"]
    assert (
        detail["items"] == []
        and len(detail["associatedCaseIds"]) == 23
        and detail["caseCount"] == 23
    )
    assert not any("case_versions" in sql.lower() for sql in statements)
    item = next(i for i in review["items"] if i["caseId"] == cases[0].id)
    versions = g["db"].query(CaseVersion).count()
    cases[0].deleted_at = beijing_now()
    g["db"].commit()
    assert rows(g, review)["total"] == 22
    response = g["client"].get(endpoint(g) + f"/{review['id']}/items/{item['id']}")
    assert response.status_code == 200, response.text
    assert response.json()["data"]["snapshot"] == item["snapshot"]
    assert response.json()["data"]["recycled"] and response.json()["data"]["outdated"]
    assert g["db"].query(CaseVersion).count() == versions
    assert (
        g["client"].get(endpoint(g) + f"/{review['id']}/items/未知条目").status_code
        == 404
    )


def test_reviewer_and_state_filters_compact_metrics_and_project_permission(governance):
    g = governance
    review = request_review(g, cases=[c.id for c in g["cases"]])
    item = review["items"][0]
    g["state"]["user"] = g["users"][1]
    response = g["client"].post(
        g["base"] + f"/reviews/{review['id']}/items/{item['id']}/decision",
        json={"decision": "approved"},
    )
    assert response.status_code == 200, response.text
    assert rows(g, review, state="under_review")["total"] == 1
    assert rows(g, review, state="un_review")["total"] == 1
    assert rows(g, review, onlyMine=True)["total"] == 2
    assert rows(g, review, reviewerId=g["users"][2].id)["total"] == 2
    assert rows(g, review, reviewerId=g["users"][0].id)["total"] == 0
    assert rows(g, review, creatorId=g["users"][0].id)["total"] == 2
    data = g["client"].get(endpoint(g) + f"/{review['id']}/detail").json()["data"]
    for key in [
        "lifecycle",
        "passRate",
        "progress",
        "underReviewedCount",
        "unReviewCount",
    ]:
        assert data[key] == response.json()["data"][key]
    assert rows(g, review)["items"][0]["canVote"]
    g["state"]["user"] = g["users"][0]
    assert not rows(g, review)["items"][0]["canVote"]
    g["state"]["user"] = g["users"][3]
    for suffix in ["detail", "items", "items/" + item["id"]]:
        assert (
            g["client"].get(endpoint(g) + f"/{review['id']}/" + suffix).status_code
            == 403
        )
