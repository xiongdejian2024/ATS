"""同一评审内重新提审：历史、版本、权限及重新投票的软件回归。"""

from test_case_governance import governance, request_review
from test_review_item_management import manage, vote, detail
from test_review_workspace import endpoint, listing
from models.case_governance import (
    CaseReview,
    CaseReviewItem,
    CaseVersion,
    CaseReviewDecision,
    CaseReviewEvent,
)
from schemas.test_case import TestCaseUpdate as CaseUpdate
from services.test_case_service import TestCaseService


def owned_review(g, **extra):
    return request_review(g, reviewers=[g["users"][0].id, g["users"][1].id], **extra)


def rows(g, review, **params):
    response = g["client"].get(endpoint(g) + f"/{review['id']}/items", params=params)
    assert response.status_code == 200, response.text
    return response.json()["data"]


def test_same_review_refreshes_version_preserves_history_and_discussion(governance):
    g = governance
    review = owned_review(g)
    item = review["items"][0]
    old_version = g["db"].get(CaseReviewItem, item["id"]).version_id
    vote(g, review, 0)
    vote(g, review, 1)
    assert detail(g, review)["lifecycle"] == "completed"
    assert (
        g["client"]
        .post(
            g["base"] + f"/reviews/{review['id']}/comments",
            json={
                "itemId": item["id"],
                "content": "旧轮讨论保留",
            },
        )
        .status_code
        == 200
    )
    TestCaseService.update_test_case(
        g["db"], item["caseId"], CaseUpdate(name="当前最新内容"), g["users"][0].id
    )
    version_count = g["db"].query(CaseVersion).count()
    response = manage(
        g, review, "re-review", comment="<p><strong>重新审阅当前内容</strong></p>"
    )
    assert response.status_code == 200, response.text
    data = response.json()["data"]
    assert data["id"] == review["id"] and data["number"] == review["number"]
    assert data["reReviewedCount"] == 1 and data["reviewedCount"] == 0
    assert data["lifecycle"] == "underway" and data["progress"] == 0
    assert g["db"].query(CaseReview).count() == 1
    assert g["db"].query(CaseReviewDecision).count() == 0
    assert g["db"].query(CaseVersion).count() == version_count
    record = rows(g, review, state="re_review")["items"][0]
    assert record["id"] == item["id"] and record["version"] == 2
    assert record["snapshot"]["name"] == "当前最新内容" and not record["outdated"]
    assert record["canReReview"] and record["reviewState"] == "re_review"
    assert g["db"].get(CaseVersion, old_version).snapshot["name"] != "当前最新内容"
    reset = next(e for e in data["history"] if e["action"] == "重新提审")
    assert reset["detail"]["beforeVersionId"] == old_version
    assert len(reset["detail"]["invalidatedDecisions"]) == 2
    assert all(e["abandoned"] for e in data["history"] if e["action"] == "评审结论")
    assert data["comments"][0]["content"] == "旧轮讨论保留"
    assert listing(g, lifecycle="underway")["total"] == 1


def test_new_round_never_reuses_old_votes_and_people_changes_keep_reset_state(
    governance,
):
    g = governance
    review = owned_review(g)
    vote(g, review, 0, decision="rejected")
    vote(g, review, 1)
    assert manage(g, review, "re-review").status_code == 200
    # 建议不结束重新提审；移除再添加原人员不能复活上一轮票。
    vote(g, review, 0, decision="suggestion")
    assert (
        manage(g, review, "item-reviewers", reviewerIds=[g["users"][1].id]).json()[
            "data"
        ]["unReviewCount"]
        == 1
    )
    assert (
        manage(
            g, review, "item-reviewers", reviewerIds=[g["users"][0].id], append=True
        ).json()["data"]["reReviewedCount"]
        == 1
    )
    assert g["db"].query(CaseReviewDecision).count() == 0
    data = vote(g, review, 0)
    assert data["underReviewedCount"] == 1 and data["reReviewedCount"] == 0
    assert data["unPassCount"] == 0 and data["passCount"] == 0
    assert vote(g, review, 1)["lifecycle"] == "completed"
    assert manage(g, review, "re-review", comment="再开一轮").status_code == 200
    data = detail(g, review)
    assert (
        data["reReviewedCount"] == 1 and g["db"].query(CaseReviewDecision).count() == 0
    )
    assert (
        sum(e["abandoned"] for e in data["history"] if e["action"] == "评审结论") == 5
    )
    assert g["db"].query(CaseReviewEvent).filter_by(action="重新提审").count() == 2
    assert (
        sum(e["abandoned"] for e in data["history"] if e["action"] == "重新提审") == 1
    )


def test_single_and_batch_use_same_item_ids_and_other_cases_are_untouched(governance):
    g = governance
    review = owned_review(g, cases=[c.id for c in g["cases"]], policy="any")
    for item in review["items"]:
        vote(g, review, 0, item=item)
    identifiers = [i["id"] for i in review["items"]]
    assert manage(g, review, "re-review", ids=identifiers[:1]).status_code == 200
    data = detail(g, review)
    assert data["passCount"] == 1 and data["reReviewedCount"] == 1
    assert g["db"].query(CaseReviewDecision).count() == 1
    assert manage(g, review, "re-review", ids=identifiers).status_code == 200
    assert detail(g, review)["reReviewedCount"] == 2
    assert {i.id for i in g["db"].query(CaseReviewItem).all()} == set(identifiers)
    assert vote(g, review, 0)["passCount"] == 1


def test_read_only_unassigned_and_mixed_selection_reject_without_writes(governance):
    g = governance
    review = owned_review(g, cases=[c.id for c in g["cases"]])
    vote(g, review, 0)
    second = review["items"][1]
    assert (
        manage(
            g,
            review,
            "item-reviewers",
            ids=[second["id"]],
            reviewerIds=[g["users"][1].id],
        ).status_code
        == 200
    )
    assert not next(
        row for row in rows(g, review)["items"] if row["id"] == second["id"]
    )["canReReview"]
    assert manage(g, review, "re-review").status_code == 403
    assert g["db"].query(CaseReviewDecision).count() == 1
    g["state"]["user"] = g["users"][1]
    assert not rows(g, review)["items"][0]["canReReview"]
    assert manage(g, review, "re-review").status_code == 403
    g["state"]["user"] = g["users"][0]
    foreign = owned_review(g, cases=[g["cases"][0].id])
    assert (
        manage(
            g,
            review,
            "re-review",
            ids=[review["items"][0]["id"], foreign["items"][0]["id"]],
        ).status_code
        == 404
    )
    assert manage(g, review, "re-review", comment="文" * 10001).status_code == 422
    assert manage(g, review, "re-review", ids=[" "]).status_code == 422
    assert g["db"].query(CaseReviewEvent).filter_by(action="重新提审").count() == 0
    assert g["db"].query(CaseReviewDecision).count() == 1


def test_archive_closed_and_recycled_cases_cannot_be_rereviewed(governance):
    g = governance
    review = owned_review(g, policy="any")
    vote(g, review, 0)
    assert g["client"].post(endpoint(g) + f"/{review['id']}/archive").status_code == 200
    assert manage(g, review, "re-review").status_code == 409
    assert not rows(g, review)["items"][0]["canReReview"]
    current = owned_review(g, cases=[g["cases"][1].id])
    from utils.datetime_utils import beijing_now

    g["cases"][1].deleted_at = beijing_now()
    g["db"].commit()
    assert manage(g, current, "re-review").status_code == 404
    assert g["db"].query(CaseReviewEvent).filter_by(action="重新提审").count() == 0
    g["cases"][1].deleted_at = None
    g["db"].get(CaseReview, current["id"]).status = "cancelled"
    g["db"].commit()
    assert manage(g, current, "re-review").status_code == 409


def test_system_manager_with_project_update_can_reset_unassigned_case(governance):
    g = governance
    review = request_review(g)
    vote(g, review, 1)
    from models import Role, Permission, UserRole, RolePermission

    role = Role(name="同单提审系统管理", display_name="系统管理")
    permission = Permission(
        code="system:manage", name="系统管理", resource="system", action="manage"
    )
    g["db"].add_all([role, permission])
    g["db"].flush()
    g["db"].add_all(
        [
            UserRole(user_id=g["users"][0].id, role_id=role.id),
            RolePermission(role_id=role.id, permission_id=permission.id),
        ]
    )
    g["db"].commit()
    assert rows(g, review)["items"][0]["canReReview"]
    response = manage(g, review, "re-review")
    assert response.status_code == 200, response.text
    assert response.json()["data"]["reReviewedCount"] == 1


def test_250_items_reset_in_one_batch_without_loading_each_version(governance):
    from uuid import uuid4
    from sqlalchemy import event
    from models import TestCase as Case

    g = governance
    cases = [
        Case(
            id=str(uuid4()),
            project_id=g["project"].id,
            name=f"重新提审批量{i}",
            case_code=f"ROUND-{i:03}",
            type="functional",
            steps=[],
            created_by=g["users"][0].id,
        )
        for i in range(250)
    ]
    g["db"].add_all(cases)
    g["db"].commit()
    review = request_review(
        g, cases=[c.id for c in cases], reviewers=[g["users"][0].id], policy="any"
    )
    ids = [i["id"] for i in review["items"]]
    assert (
        g["client"]
        .post(
            g["base"] + f"/reviews/{review['id']}/batch-decision",
            json={"itemIds": ids, "decision": "approved"},
        )
        .status_code
        == 200
    )
    versions = g["db"].query(CaseVersion).count()
    statements = []

    def record(_connection, _cursor, statement, _params, _context, _many):
        if statement.lstrip().lower().startswith("select"):
            statements.append(statement)

    event.listen(g["db"].bind, "before_cursor_execute", record)
    try:
        response = manage(g, review, "re-review", ids=ids)
    finally:
        event.remove(g["db"].bind, "before_cursor_execute", record)
    assert response.status_code == 200, response.text
    data = response.json()["data"]
    assert data["reReviewedCount"] == 250 and data["reviewedCount"] == 0
    assert len(statements) < 50
    assert sum(e["abandoned"] for e in data["history"]) == 250
    assert g["db"].query(CaseReviewDecision).count() == 0
    assert g["db"].query(CaseVersion).count() == versions
