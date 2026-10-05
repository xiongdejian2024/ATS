"""评审理由：通过可省略，其他结论拒绝空富文本，批量失败回滚。"""

from test_case_governance import governance, request_review
from models.case_governance import CaseReviewDecision, CaseReviewEvent, CaseReviewItem


def vote(g, review, decision, reason=None):
    body = {"decision": decision}
    if reason is not None:
        body["comment"] = reason
    return g["client"].post(
        g["base"]
        + f"/reviews/{review['id']}/items/{review['items'][0]['id']}/decision",
        json=body,
    )


def test_pass_without_reason_records_vote_and_history(governance):
    g = governance
    review = request_review(g, reviewers=[g["users"][0].id], policy="any")
    response = vote(g, review, "approved")
    assert response.status_code == 200, response.text
    row = response.json()["data"]["items"][0]
    assert row["status"] == "approved" and row["decisions"][0]["comment"] == ""
    history = response.json()["data"]["history"]
    assert history[-1]["detail"]["comment"] == ""


def test_required_reason_rejects_empty_markup_without_changing_valid_vote(governance):
    g = governance
    review = request_review(g, reviewers=[g["users"][0].id], policy="any")
    assert vote(g, review, "approved", "旧有效票").status_code == 200
    count = g["db"].query(CaseReviewEvent).count()
    for decision in ["rejected", "suggestion"]:
        for reason in [
            None,
            " ",
            "<p><br></p>",
            "<p>&nbsp;\u200b\ufeff</p>",
            "<script>不可见</script>",
            '<img src="">',
        ]:
            response = vote(g, review, decision, reason)
            assert response.status_code == 422, response.text
    assert g["db"].query(CaseReviewEvent).count() == count
    row = g["db"].query(CaseReviewDecision).one()
    assert row.comment == "旧有效票" and row.decision == "approved"


def test_rich_reason_roundtrip_and_suggestion_keeps_effective_vote(governance):
    g = governance
    review = request_review(g, reviewers=[g["users"][0].id], policy="any")
    reason = "<p><strong>诊断信息缺失</strong></p><ul><li>补充步骤</li></ul>"
    response = vote(g, review, "rejected", reason)
    assert response.status_code == 200, response.text
    assert response.json()["data"]["items"][0]["decisions"][0]["comment"] == reason
    suggestion = "<p><em>建议增加边界检查</em></p>"
    response = vote(g, review, "suggestion", suggestion)
    assert response.status_code == 200
    row = response.json()["data"]["items"][0]
    assert row["status"] == "rejected" and row["decisions"][0]["comment"] == reason
    history = response.json()["data"]["history"]
    assert any(e["detail"].get("comment") == suggestion for e in history)
    assert vote(g, review, "approved", "x" * 10001).status_code == 422
    assert vote(g, review, "rejected", "数值 1 < 2").status_code == 200


def test_batch_empty_pass_and_invalid_batch_leave_no_partial_votes(governance):
    g = governance
    review = request_review(
        g, cases=[c.id for c in g["cases"]], reviewers=[g["users"][0].id], policy="any"
    )
    url = g["base"] + f"/reviews/{review['id']}/batch-decision"
    ids = [i["id"] for i in review["items"]]
    assert (
        g["client"]
        .post(
            url, json={"itemIds": ids, "decision": "rejected", "comment": "<p><br></p>"}
        )
        .status_code
        == 422
    )
    assert g["db"].query(CaseReviewDecision).count() == 0
    assert (
        g["client"]
        .post(url, json={"itemIds": [ids[0], "不存在的条目"], "decision": "approved"})
        .status_code
        == 404
    )
    assert g["db"].query(CaseReviewDecision).count() == 0
    assert all(i.status == "pending" for i in g["db"].query(CaseReviewItem).all())
    response = g["client"].post(url, json={"itemIds": ids, "decision": "approved"})
    assert response.status_code == 200, response.text
    assert all(
        i["status"] == "approved" and i["decisions"][0]["comment"] == ""
        for i in response.json()["data"]["items"]
    )
