"""已有评审追加关联：事务原子性、结论保留、归档及项目权限。"""

from test_case_governance import governance, request_review
from test_review_workspace import endpoint, listing
from models.case_governance import (
    CaseReviewItem,
    CaseReviewDecision,
    CaseReviewEvent,
    CaseVersion,
)


def associate(g, identifier, ids=None, people=None):
    return g["client"].post(
        endpoint(g) + f"/{identifier}/associate",
        json={
            "caseIds": ids or [g["cases"][1].id],
            "reviewerIds": people or [g["users"][2].id],
        },
    )


def test_append_to_approved_review_keeps_existing_ids_assignments_and_vote(governance):
    g = governance
    review = (
        g["client"]
        .post(
            g["base"] + "/reviews",
            json={
                "name": "已有票追加",
                "mode": "single",
                "caseIds": [g["cases"][0].id],
                "reviewerIds": [g["users"][1].id],
            },
        )
        .json()["data"]
    )
    item = review["items"][0]
    g["state"]["user"] = g["users"][1]
    assert (
        g["client"]
        .post(
            g["base"] + f"/reviews/{review['id']}/items/{item['id']}/decision",
            json={"decision": "approved", "comment": "原有效票"},
        )
        .status_code
        == 200
    )
    g["state"]["user"] = g["users"][0]
    before_version = g["db"].get(CaseReviewItem, item["id"]).version_id
    response = associate(g, review["id"])
    assert response.status_code == 200, response.text
    data = response.json()["data"]
    old = next(i for i in data["items"] if i["id"] == item["id"])
    new = next(i for i in data["items"] if i["caseId"] == g["cases"][1].id)
    assert old["status"] == "approved" and old["decisions"][0]["comment"] == "原有效票"
    assert old["reviewerIds"] == [g["users"][1].id] and new["reviewerIds"] == [
        g["users"][2].id
    ]
    assert g["db"].get(CaseReviewItem, item["id"]).version_id == before_version
    assert (
        new["status"] == "pending"
        and not new["decisions"]
        and data["status"] == "pending"
    )
    assert data["reviewerIds"] == [g["users"][1].id]
    summary = listing(g)["items"][0]
    assert (
        summary["lifecycle"] == "underway"
        and summary["passRate"] == 50
        and summary["caseCount"] == 2
    )
    assert g["db"].query(CaseReviewDecision).count() == 1
    assert len([e for e in data["history"] if e["action"] == "关联用例"]) == 1
    g["state"]["user"] = g["users"][2]
    assert (
        g["client"]
        .post(
            g["base"] + f"/reviews/{review['id']}/items/{new['id']}/decision",
            json={"decision": "approved", "comment": "新用例结论"},
        )
        .status_code
        == 200
    )
    assert listing(g)["items"][0]["lifecycle"] == "completed"


def test_empty_review_associate_uses_selected_people_and_keeps_defaults(governance):
    g = governance
    review = (
        g["client"]
        .post(
            g["base"] + "/reviews",
            json={
                "name": "先保存空评审",
                "mode": "single",
                "reviewerIds": [g["users"][1].id],
            },
        )
        .json()["data"]
    )
    response = associate(g, review["id"], ids=[g["cases"][0].id])
    assert response.status_code == 200, response.text
    data = response.json()["data"]
    assert data["items"][0]["reviewerIds"] == [g["users"][2].id]
    assert data["reviewerIds"] == [g["users"][1].id]
    assert listing(g)["items"][0]["lifecycle"] == "prepared"
    assert (
        g["db"]
        .query(CaseReviewEvent)
        .filter_by(review_id=review["id"], action="评审结论")
        .count()
        == 0
    )


def test_association_duplicate_foreign_recycled_and_wrong_category_are_atomic(
    governance,
):
    g = governance
    review = request_review(g)
    count = g["db"].query(CaseVersion).count()
    for ids, expected in [
        ([g["cases"][0].id, g["cases"][1].id], 409),
        ([g["cases"][1].id, g["foreign"].id], 404),
    ]:
        response = associate(g, review["id"], ids=ids)
        assert response.status_code == expected, response.text
        assert (
            g["db"].query(CaseReviewItem).filter_by(review_id=review["id"]).count() == 1
        )
        assert g["db"].query(CaseVersion).count() == count
    assert associate(g, review["id"], people=[g["users"][3].id]).status_code == 422
    g["cases"][1].type = "api"
    g["db"].commit()
    assert associate(g, review["id"]).status_code == 422
    g["cases"][1].type = "functional"
    from utils.datetime_utils import beijing_now

    g["cases"][1].deleted_at = beijing_now()
    g["db"].commit()
    assert associate(g, review["id"]).status_code == 404
    assert (
        g["db"]
        .query(CaseReviewEvent)
        .filter_by(review_id=review["id"], action="关联用例")
        .count()
        == 0
    )
    for body in [
        {"caseIds": [], "reviewerIds": [g["users"][1].id]},
        {"caseIds": [g["cases"][1].id] * 2, "reviewerIds": [g["users"][1].id]},
        {"caseIds": [g["cases"][1].id], "reviewerIds": []},
    ]:
        assert (
            g["client"]
            .post(endpoint(g) + f"/{review['id']}/associate", json=body)
            .status_code
            == 422
        )


def test_association_permissions_closed_and_archived_protection(governance):
    g = governance
    review = request_review(g, reviewers=[g["users"][1].id], policy="any")
    g["state"]["user"] = g["users"][1]
    assert associate(g, review["id"]).status_code == 403
    assert (
        g["client"]
        .post(
            g["base"]
            + f"/reviews/{review['id']}/items/{review['items'][0]['id']}/decision",
            json={"decision": "approved", "comment": "归档前确认"},
        )
        .status_code
        == 200
    )
    g["state"]["user"] = g["users"][0]
    assert g["client"].post(endpoint(g) + f"/{review['id']}/archive").status_code == 200
    assert associate(g, review["id"]).status_code == 409
    cancelled = request_review(g)
    assert (
        g["client"].post(g["base"] + f"/reviews/{cancelled['id']}/cancel").status_code
        == 200
    )
    assert associate(g, cancelled["id"]).status_code == 409
    foreign = f"/api/v1/projects/{g['foreign'].project_id}/case-governance/review-workspace/{review['id']}/associate"
    assert (
        g["client"]
        .post(
            foreign,
            json={"caseIds": [g["foreign"].id], "reviewerIds": [g["users"][3].id]},
        )
        .status_code
        == 403
    )
