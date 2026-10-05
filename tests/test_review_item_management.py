"""修改评审人、取消关联及批量投票的事务与历史回归。"""

from test_case_governance import governance, request_review
from test_review_workspace import endpoint, listing
from models.case_governance import (
    CaseReviewItem,
    CaseReviewDecision,
    CaseReviewEvent,
    CaseVersion,
)


def manage(g, review, action, ids=None, **extra):
    return g["client"].post(
        endpoint(g) + f"/{review['id']}/{action}",
        json={"itemIds": ids or [i["id"] for i in review["items"]], **extra},
    )


def vote(g, review, who, item=None, decision="approved"):
    g["state"]["user"] = g["users"][who]
    response = g["client"].post(
        g["base"]
        + f"/reviews/{review['id']}/items/{(item or review['items'][0])['id']}/decision",
        json={"decision": decision, "comment": "原评审记录"},
    )
    assert response.status_code == 200, response.text
    g["state"]["user"] = g["users"][0]
    return response.json()["data"]


def detail(g, review):
    response = g["client"].get(endpoint(g) + f"/{review['id']}/detail")
    assert response.status_code == 200, response.text
    return response.json()["data"]


def test_multiple_replacement_append_recomputes_from_current_people_preserves_history(
    governance,
):
    g = governance
    review = request_review(g, reviewers=[g["users"][1].id])
    before = g["db"].get(CaseReviewItem, review["items"][0]["id"]).version_id
    vote(g, review, 1)
    changed = manage(g, review, "item-reviewers", reviewerIds=[g["users"][2].id])
    assert changed.status_code == 200, changed.text
    data = changed.json()["data"]
    assert (
        data["items"] == []
        and data["unReviewCount"] == 1
        and data["underReviewedCount"] == 0
    )
    assert data["lifecycle"] == "prepared"
    assert listing(g, lifecycle="prepared")["total"] == 1
    current = g["db"].get(CaseReviewItem, review["items"][0]["id"])
    assert (
        current.reviewer_ids == [g["users"][2].id]
        and current.status == "pending"
        and current.version_id == before
    )
    assert g["db"].query(CaseReviewDecision).count() == 1
    assert g["db"].query(CaseReviewEvent).filter_by(action="评审结论").count() == 1
    # 把原评审人加回来，原有效票仍可参与新的人员组合。
    assert (
        manage(
            g, review, "item-reviewers", reviewerIds=[g["users"][1].id], append=True
        ).status_code
        == 200
    )
    assert detail(g, review)["underReviewedCount"] == 1
    assert vote(g, review, 2)["passCount"] == 1
    # 重复追加去重，不改变关联编号或版本；单条人数不超过50。
    assert (
        manage(
            g, review, "item-reviewers", reviewerIds=[g["users"][1].id], append=True
        ).status_code
        == 200
    )
    assert len(current.reviewer_ids) == 2
    assert (
        manage(g, review, "item-reviewers", reviewerIds=[g["users"][1].id]).json()[
            "data"
        ]["passCount"]
        == 1
    )


def test_rejecting_removed_person_does_not_affect_new_multiple_result_and_single_keeps_result(
    governance,
):
    g = governance
    review = request_review(g)
    vote(g, review, 1, decision="rejected")
    vote(g, review, 2)
    changed = manage(g, review, "item-reviewers", reviewerIds=[g["users"][2].id])
    assert changed.status_code == 200 and changed.json()["data"]["passCount"] == 1
    assert g["db"].query(CaseReviewDecision).count() == 2
    single = request_review(g, reviewers=[g["users"][1].id], policy="any")
    vote(g, single, 1)
    changed = manage(g, single, "item-reviewers", reviewerIds=[g["users"][2].id])
    assert changed.status_code == 200 and changed.json()["data"]["passCount"] == 1
    assert vote(g, single, 2, decision="rejected")["unPassCount"] == 1


def test_unlink_removes_only_relationship_and_reassociation_starts_fresh(governance):
    g = governance
    review = request_review(
        g, cases=[c.id for c in g["cases"]], reviewers=[g["users"][1].id], policy="any"
    )
    vote(g, review, 1)
    old = review["items"][0]
    from models.case_governance import CaseReviewComment

    discussion = CaseReviewComment(
        review_id=review["id"],
        item_id=old["id"],
        author_id=g["users"][0].id,
        content="保留讨论原文",
    )
    g["db"].add(discussion)
    g["db"].commit()
    version_count = g["db"].query(CaseVersion).count()
    response = manage(g, review, "disassociate", ids=[old["id"]])
    assert response.status_code == 200, response.text
    data = response.json()["data"]
    assert data["caseCount"] == 1 and old["caseId"] not in data["associatedCaseIds"]
    assert g["db"].get(CaseReviewItem, old["id"]) is None
    assert discussion.item_id is None and discussion.content == "保留讨论原文"
    assert g["db"].query(CaseReviewDecision).filter_by(item_id=old["id"]).count() == 0
    assert g["db"].query(CaseReviewEvent).filter_by(action="评审结论").count() == 1
    assert g["db"].query(CaseVersion).count() == version_count
    new = g["client"].post(
        endpoint(g) + f"/{review['id']}/associate",
        json={"caseIds": [old["caseId"]], "reviewerIds": [g["users"][1].id]},
    )
    assert new.status_code == 200, new.text
    item = next(i for i in new.json()["data"]["items"] if i["caseId"] == old["caseId"])
    assert (
        item["id"] != old["id"]
        and item["status"] == "pending"
        and item["decisions"] == []
    )
    assert g["db"].query(CaseVersion).count() == version_count


def test_management_scope_validation_permissions_and_archive_are_atomic(governance):
    g = governance
    review = request_review(g)
    other = request_review(g, cases=[g["cases"][1].id])
    item = review["items"][0]
    for action, extra in [
        ("item-reviewers", {"reviewerIds": [g["users"][2].id]}),
        ("disassociate", {}),
    ]:
        response = manage(
            g, review, action, ids=[item["id"], other["items"][0]["id"]], **extra
        )
        assert response.status_code == 404, response.text
        assert (
            g["db"].get(CaseReviewItem, item["id"]).reviewer_ids
            == review["reviewerIds"]
        )
        g["state"]["user"] = g["users"][1]
        assert manage(g, review, action, **extra).status_code == 403
        g["state"]["user"] = g["users"][0]
    assert (
        manage(g, review, "item-reviewers", reviewerIds=[g["users"][3].id]).status_code
        == 422
    )
    assert manage(g, review, "item-reviewers", reviewerIds=[]).status_code == 422
    assert (
        manage(g, review, "disassociate", ids=[item["id"], item["id"]]).status_code
        == 422
    )
    vote(g, review, 1)
    vote(g, review, 2)
    assert g["client"].post(endpoint(g) + f"/{review['id']}/archive").status_code == 200
    assert (
        manage(g, review, "item-reviewers", reviewerIds=[g["users"][1].id]).status_code
        == 409
    )
    assert manage(g, review, "disassociate").status_code == 409
    assert g["db"].query(CaseReviewEvent).filter_by(action="修改评审人").count() == 0
    assert g["db"].query(CaseReviewEvent).filter_by(action="取消关联").count() == 0


def test_bulk_more_than_200_is_atomic_and_does_not_query_each_snapshot(governance):
    from uuid import uuid4
    from sqlalchemy import event
    from models import TestCase as Case

    g = governance
    cases = [
        Case(
            id=str(uuid4()),
            project_id=g["project"].id,
            name=f"批量软件用例{i}",
            case_code=f"BATCH-{i:03}",
            type="functional",
            steps=[],
            created_by=g["users"][0].id,
        )
        for i in range(250)
    ]
    g["db"].add_all(cases)
    g["db"].commit()
    review = request_review(
        g, cases=[c.id for c in cases], reviewers=[g["users"][1].id], policy="any"
    )
    g["state"]["user"] = g["users"][1]
    statements = []

    def record(_conn, _cursor, sql, _params, _ctx, _many):
        if sql.lstrip().lower().startswith("select"):
            statements.append(sql)

    event.listen(g["db"].bind, "before_cursor_execute", record)
    try:
        response = g["client"].post(
            g["base"] + f"/reviews/{review['id']}/batch-decision",
            json={
                "itemIds": [i["id"] for i in review["items"]],
                "decision": "approved",
            },
        )
    finally:
        event.remove(g["db"].bind, "before_cursor_execute", record)
    assert response.status_code == 200, response.text
    data = response.json()["data"]
    assert data["passCount"] == 250 and len(data["items"]) == 250
    assert len(statements) < 50
    assert (
        g["db"].query(CaseReviewDecision).count() == 250
        and g["db"].query(CaseReviewEvent).filter_by(action="评审结论").count() == 250
    )
    # 混入不存在的条目，整批没有新的票或历史。
    response = g["client"].post(
        g["base"] + f"/reviews/{review['id']}/batch-decision",
        json={
            "itemIds": [review["items"][0]["id"], str(uuid4())],
            "decision": "rejected",
            "comment": "不应写入",
        },
    )
    assert response.status_code == 404
    assert (
        g["db"].query(CaseReviewDecision).filter_by(decision="approved").count() == 250
    )
    assert g["db"].query(CaseReviewEvent).filter_by(action="评审结论").count() == 250


def test_all_unlink_and_suggestion_alone_remain_prepared(governance):
    g = governance
    review = request_review(g, reviewers=[g["users"][1].id], policy="any")
    vote(g, review, 1, decision="suggestion")
    assert (
        detail(g, review)["lifecycle"] == "prepared"
        and listing(g, lifecycle="prepared")["total"] == 1
    )
    vote(g, review, 1)
    assert detail(g, review)["lifecycle"] == "completed"
    removed = manage(g, review, "disassociate")
    assert removed.status_code == 200, removed.text
    data = removed.json()["data"]
    assert (
        data["caseCount"] == 0
        and data["status"] == "pending"
        and data["lifecycle"] == "prepared"
    )
    assert listing(g, lifecycle="prepared")["total"] == 1
    for body in [{"itemIds": []}, {"itemIds": [" "]}]:
        assert (
            g["client"]
            .post(endpoint(g) + f"/{review['id']}/disassociate", json=body)
            .status_code
            == 422
        )
