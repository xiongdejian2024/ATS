"""详情与列表状态一致：多人部分票、建议、完成、归档及官方比例舍入。"""

from test_case_governance import governance, request_review
from test_review_workspace import listing, endpoint
from schemas.test_case import TestCaseCreate as CaseCreate
from services.test_case_service import TestCaseService
from services.review_progress import metrics


def test_progress_halfway_rounding_matches_official_two_decimal_display():
    # 1/32为3.125%，官方toFixed(2)显示3.13%，不能沿用Python银行家舍入3.12%。
    rows = [{"status": "approved"}] + [{"status": "pending"}] * 31
    data = metrics(rows, started=True)
    assert data["progress"] == 3.13 and data["passRate"] == 3
    # JS的23/160*100为14.374999999999998，toFixed(2)显示14.37%。
    rows = [{"status": "approved"}] * 23 + [{"status": "pending"}] * 137
    assert metrics(rows, started=True)["progress"] == 14.37


def get_detail(g, identifier):
    response = g["client"].get(g["base"] + f"/reviews/{identifier}")
    assert response.status_code == 200, response.text
    return response.json()["data"]


def vote(g, review, item, person, decision="approved"):
    g["state"]["user"] = person
    response = g["client"].post(
        g["base"] + f"/reviews/{review['id']}/items/{item['id']}/decision",
        json={"decision": decision, "comment": "核对进度"},
    )
    assert response.status_code == 200, response.text
    return response.json()["data"]


def assert_counts(data, expected):
    assert [
        data[key]
        for key in [
            "passCount",
            "unPassCount",
            "reReviewedCount",
            "underReviewedCount",
            "unReviewCount",
        ]
    ] == expected
    assert sum(expected) == data["caseCount"]


def test_partial_multi_votes_suggestion_completion_and_archive_match_list(governance):
    g = governance
    review = request_review(g, cases=[c.id for c in g["cases"]])
    assert review["lifecycle"] == "prepared" and review["progress"] == 0
    assert_counts(review, [0, 0, 0, 0, 2])
    first, second = review["items"]
    partial = vote(g, review, first, g["users"][1])
    assert partial["lifecycle"] == "underway" and partial["status"] == "pending"
    assert partial["progress"] == partial["passRate"] == 0
    assert_counts(partial, [0, 0, 0, 1, 1])
    suggestion = vote(g, review, first, g["users"][2], "suggestion")
    assert_counts(suggestion, [0, 0, 0, 1, 1])
    passed = vote(g, review, first, g["users"][2])
    assert passed["progress"] == passed["passRate"] == 50
    assert_counts(passed, [1, 0, 0, 0, 1])
    completed = vote(g, review, second, g["users"][1], "rejected")
    assert completed["lifecycle"] == "completed" and completed["status"] == "rejected"
    assert completed["progress"] == 100 and completed["passRate"] == 50
    assert_counts(completed, [1, 1, 0, 0, 0])
    summary = listing(g)["items"][0]
    assert (
        summary["lifecycle"] == completed["lifecycle"]
        and summary["passRate"] == completed["passRate"]
    )
    g["state"]["user"] = g["users"][0]
    assert g["client"].post(endpoint(g) + f"/{review['id']}/archive").status_code == 200
    archived = get_detail(g, review["id"])
    assert archived["lifecycle"] == "archived" and archived["progress"] == 100
    assert_counts(archived, [1, 1, 0, 0, 0])
    assert (
        listing(g, lifecycle="archived")["items"][0]["passRate"] == archived["passRate"]
    )


def test_empty_cancelled_and_superseded_detail_states(governance):
    g = governance
    response = g["client"].post(
        g["base"] + "/reviews",
        json={"name": "空评审", "reviewerIds": [g["users"][0].id]},
    )
    empty = response.json()["data"]
    assert empty["caseCount"] == empty["progress"] == empty["passRate"] == 0
    assert empty["lifecycle"] == "prepared"
    assert (
        g["client"].post(g["base"] + f"/reviews/{empty['id']}/cancel").status_code
        == 200
    )
    assert get_detail(g, empty["id"])["lifecycle"] == "cancelled"
    original = request_review(g)
    response = g["client"].post(
        g["base"] + f"/reviews/{original['id']}/resubmit", json={}
    )
    assert response.status_code == 200, response.text
    assert response.json()["data"]["lifecycle"] == "prepared"
    assert get_detail(g, original["id"])["lifecycle"] == "superseded"


def test_pass_rate_uses_official_ratio_rounding_in_detail_and_database_list(governance):
    g = governance
    cases = list(g["cases"])
    for i in range(6):
        cases.append(
            TestCaseService.create_test_case(
                g["db"],
                CaseCreate(
                    project_id=g["project"].id, name=f"舍入用例{i}", type="functional"
                ),
                g["users"][0].id,
            )
        )
    for total, expected_rate in [(3, 33), (8, 13)]:
        review = request_review(
            g,
            cases=[c.id for c in cases[:total]],
            reviewers=[g["users"][0].id],
            policy="any",
        )
        detail = vote(g, review, review["items"][0], g["users"][0])
        assert detail["passRate"] == expected_rate
        assert detail["progress"] == round(100 / total, 2)
        summary = next(r for r in listing(g)["items"] if r["id"] == review["id"])
        assert (
            summary["passRate"] == expected_rate
            and summary["lifecycle"] == detail["lifecycle"]
        )
