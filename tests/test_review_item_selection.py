"""真实数据库范围全选、排除项及四种批量操作原子性。"""

from sqlalchemy import event
from test_case_governance import governance, request_review
from test_review_workspace import endpoint
from test_review_case_workspace import prepare, rows
from test_review_item_management import vote, detail
from models.case_governance import (
    CaseReviewItem,
    CaseReviewDecision,
    CaseReviewEvent,
    CaseVersion,
)
from services.review_item_selection import resolve
from schemas.review_workspace import ReviewItemSelection
from utils.datetime_utils import beijing_now


def call(g, review, action, **body):
    return g["client"].post(endpoint(g) + f"/{review['id']}/{action}", json=body)


def all_selection(**condition):
    return dict(selectAll=True, condition=condition)


def test_all_pages_exclusion_and_preview_do_not_materialize_or_write_versions(
    governance,
):
    g = governance
    review, cases, parent, child, foreign = prepare(g)
    before = g["db"].query(CaseVersion).count()
    first = rows(g, review, size=10, sort="caseCode", order="asc")
    excluded = first["items"][0]["id"]
    g["state"]["user"] = g["users"][1]
    response = call(
        g, review, "item-selection", **all_selection(), excludeIds=[excluded]
    )
    assert response.status_code == 200, response.text
    data = response.json()["data"]
    assert data == dict(count=22, excludedCount=1, canVote=True, canReReview=False)
    assert "itemIds" not in data and g["db"].query(CaseVersion).count() == before
    voted = call(
        g,
        review,
        "batch-decision",
        **all_selection(),
        excludeIds=[excluded],
        decision="approved",
    )
    assert voted.status_code == 200, voted.text
    decisions = g["db"].query(CaseReviewDecision).all()
    assert len(decisions) == 22 and excluded not in {d.item_id for d in decisions}
    assert g["db"].query(CaseVersion).count() == before
    assert voted.json()["data"]["items"] == []


def test_scope_filters_match_list_and_cannot_escape_project_or_review(governance):
    g = governance
    review, cases, parent, child, foreign = prepare(g)
    g["state"]["user"] = g["users"][1]
    for condition in [
        dict(folder=parent.id),
        dict(folder=parent.id, includeDescendants=False),
        dict(folder="unassigned"),
        dict(search="_%"),
        dict(search="中文标签"),
        dict(priority="P3"),
        dict(reviewerId=g["users"][1].id),
        dict(creatorId=g["users"][0].id),
        dict(onlyMine=True),
        dict(state="un_review"),
    ]:
        expected = rows(g, review, **condition)["total"]
        response = call(g, review, "item-selection", **all_selection(**condition))
        assert (
            response.status_code == 200 and response.json()["data"]["count"] == expected
        ), response.text
    own_item = next(i for i in review["items"] if i["caseId"] == cases[0].id)
    g["state"]["user"] = g["users"][0]
    other = request_review(g, cases=[cases[1].id], reviewers=[g["users"][1].id])
    g["state"]["user"] = g["users"][1]
    # 不属于本范围的排除项只会被忽略，不能扩大范围或修改另一评审。
    response = call(
        g,
        review,
        "batch-decision",
        **all_selection(folder=parent.id, includeDescendants=False),
        excludeIds=[other["items"][0]["id"]],
        decision="approved",
    )
    assert (
        response.status_code == 200 and g["db"].query(CaseReviewDecision).count() == 1
    )
    assert g["db"].query(CaseReviewDecision).first().item_id == own_item["id"]
    assert (
        call(
            g, review, "item-selection", **all_selection(folder=foreign.id)
        ).status_code
        == 404
    )
    g["state"]["user"] = g["users"][3]
    assert call(g, review, "item-selection", **all_selection()).status_code == 403


def test_current_scope_is_requeried_after_preview_and_permission_failure_is_atomic(
    governance,
):
    g = governance
    review = request_review(
        g, cases=[c.id for c in g["cases"]], reviewers=[g["users"][0].id]
    )
    first, second = review["items"]
    scope = all_selection(state="un_review")
    assert call(g, review, "item-selection", **scope).json()["data"]["count"] == 2
    vote(g, review, 0, item=first)
    # 预览之后结果变化，提交只处理此刻仍在筛选范围内的一条。
    response = call(
        g,
        review,
        "batch-decision",
        **scope,
        decision="rejected",
        comment="当前范围的软件理由",
    )
    assert response.status_code == 200, response.text
    decisions = {d.item_id: d.decision for d in g["db"].query(CaseReviewDecision).all()}
    assert decisions == {first["id"]: "approved", second["id"]: "rejected"}
    assert (
        call(g, review, "batch-decision", **scope, decision="approved").status_code
        == 409
    )
    g["db"].get(CaseReviewItem, second["id"]).reviewer_ids = [g["users"][1].id]
    g["db"].commit()
    assert not call(g, review, "item-selection", **all_selection()).json()["data"][
        "canVote"
    ]
    events = g["db"].query(CaseReviewEvent).count()
    assert (
        call(
            g, review, "batch-decision", **all_selection(), decision="approved"
        ).status_code
        == 403
    )
    assert g["db"].query(CaseReviewEvent).count() == events
    assert {
        d.item_id: d.decision for d in g["db"].query(CaseReviewDecision).all()
    } == decisions


def test_people_re_review_and_unlink_share_scope_exclusions_and_keep_main_cases(
    governance,
):
    g = governance
    review = request_review(
        g, cases=[c.id for c in g["cases"]], reviewers=[g["users"][0].id]
    )
    first, second = review["items"]
    selection = {**all_selection(), "excludeIds": [second["id"]]}
    before = g["db"].query(CaseVersion).count()
    vote(g, review, 0, item=first)
    response = call(g, review, "re-review", **selection, comment="<p>同单软件重提</p>")
    assert (
        response.status_code == 200
        and g["db"].get(CaseReviewItem, first["id"]).status == "re_review"
    )
    assert g["db"].get(CaseReviewItem, second["id"]).status == "pending"
    assert not g["db"].query(CaseReviewDecision).count()
    assert (
        call(
            g,
            review,
            "item-reviewers",
            **selection,
            reviewerIds=[g["users"][1].id],
            append=True,
        ).status_code
        == 200
    )
    assert len(g["db"].get(CaseReviewItem, first["id"]).reviewer_ids) == 2
    assert g["db"].get(CaseReviewItem, second["id"]).reviewer_ids == [g["users"][0].id]
    response = call(g, review, "disassociate", **selection)
    assert response.status_code == 200 and response.json()["data"]["caseCount"] == 1
    assert g["db"].get(CaseReviewItem, first["id"]) is None
    assert g["db"].get(CaseReviewItem, second["id"]) is not None
    assert (
        all(c.deleted_at is None for c in g["cases"])
        and g["db"].query(CaseVersion).count() == before
    )


def test_schema_ambiguous_empty_or_foreign_selection_is_rejected_without_writes(
    governance,
):
    g = governance
    review = request_review(g)
    item = review["items"][0]["id"]
    for body in [
        {},
        dict(selectAll=True, itemIds=[item]),
        dict(itemIds=[item], excludeIds=[item]),
        dict(itemIds=[item], condition={"search": "x"}),
        dict(selectAll=True, condition={"page": 1}),
        dict(selectAll=True, condition={"projectId": g["foreign"].project_id}),
        dict(selectAll=True, condition={"state": "fake"}),
        dict(selectAll=True, excludeIds=[""]),
        dict(selectAll=True, excludeIds=[item, item]),
    ]:
        assert call(g, review, "item-selection", **body).status_code == 422
    assert call(g, review, "item-selection", itemIds=["missing"]).status_code == 404
    assert (
        call(
            g,
            review,
            "batch-decision",
            **all_selection(),
            decision="suggestion",
            comment="<p></p>",
        ).status_code
        == 422
    )
    assert g["db"].query(CaseReviewDecision).count() == 0


def test_archived_closed_and_recycled_items_are_not_writable_by_selection(governance):
    g = governance
    review = request_review(
        g, cases=[c.id for c in g["cases"]], reviewers=[g["users"][0].id]
    )
    g["cases"][0].deleted_at = beijing_now()
    g["db"].commit()
    assert (
        call(g, review, "item-selection", **all_selection()).json()["data"]["count"]
        == 1
    )
    assert (
        call(
            g, review, "batch-decision", **all_selection(), decision="approved"
        ).status_code
        == 200
    )
    assert g["db"].query(CaseReviewDecision).count() == 1
    # 已回收的关联保留历史，不计入当前可选范围；明确取消它后整单才能归档。
    recycled = next(i for i in review["items"] if i["caseId"] == g["cases"][0].id)
    assert call(g, review, "disassociate", itemIds=[recycled["id"]]).status_code == 200
    assert g["client"].post(endpoint(g) + f"/{review['id']}/archive").status_code == 200
    data = call(g, review, "item-selection", **all_selection()).json()["data"]
    assert data["count"] == 1 and not data["canVote"] and not data["canReReview"]
    for action, extra in [
        ("batch-decision", dict(decision="approved")),
        ("re-review", {}),
        ("item-reviewers", dict(reviewerIds=[g["users"][0].id])),
        ("disassociate", {}),
    ]:
        assert call(g, review, action, **all_selection(), **extra).status_code == 409
    g["state"]["user"] = g["users"][1]
    assert (
        call(
            g,
            review,
            "item-reviewers",
            **all_selection(),
            reviewerIds=[g["users"][1].id],
        ).status_code
        == 403
    )
    g["state"]["user"] = g["users"][0]
    closed = request_review(g, cases=[g["cases"][1].id], reviewers=[g["users"][0].id])
    assert (
        g["client"].post(g["base"] + f"/reviews/{closed['id']}/cancel").status_code
        == 200
    )
    assert not call(g, closed, "item-selection", **all_selection()).json()["data"][
        "canVote"
    ]
    assert (
        call(
            g, closed, "batch-decision", **all_selection(), decision="approved"
        ).status_code
        == 409
    )


def test_selection_uses_ids_query_and_does_not_load_all_snapshots(governance):
    g = governance
    review, _, _, _, _ = prepare(g)
    before = g["db"].query(CaseVersion).count()
    statements = []

    def record(connection, cursor, statement, parameters, context, executemany):
        statements.append(statement)

    event.listen(g["db"].bind, "before_cursor_execute", record)
    try:
        _, ids = resolve(
            g["db"],
            g["users"][0],
            g["project"].id,
            review["id"],
            ReviewItemSelection(selectAll=True),
            writing=True,
        )
    finally:
        event.remove(g["db"].bind, "before_cursor_execute", record)
    assert (
        len(ids) == 23
        and len([s for s in statements if s.lower().lstrip().startswith("select")]) < 15
    )
    assert not any("case_versions.snapshot" in s.lower() for s in statements)
    assert g["db"].query(CaseVersion).count() == before


def test_real_10001_selection_limit_and_exclusion_reduce_to_10000(governance):
    import uuid
    from models import TestCase as Case

    g = governance
    review = request_review(g, reviewers=[g["users"][0].id])
    cases, versions, items = [], [], []
    for _ in range(10000):
        case_id, version_id, item_id = (str(uuid.uuid4()) for _ in range(3))
        cases.append(
            dict(
                id=case_id,
                project_id=g["project"].id,
                case_code="范围-" + case_id,
                name="选择上限软件样本",
                type="functional",
                priority="P2",
                steps=[],
                created_by=g["users"][0].id,
            )
        )
        versions.append(
            dict(
                id=version_id,
                project_id=g["project"].id,
                case_id=case_id,
                version=1,
                snapshot={},
                reason="软件选择上限回归",
                created_by=g["users"][0].id,
            )
        )
        items.append(
            dict(
                id=item_id,
                review_id=review["id"],
                case_id=case_id,
                version_id=version_id,
                status="pending",
                reviewer_ids=[g["users"][0].id],
            )
        )
    for model, values in [
        (Case, cases),
        (CaseVersion, versions),
        (CaseReviewItem, items),
    ]:
        g["db"].bulk_insert_mappings(model, values)
    g["db"].commit()
    assert call(g, review, "item-selection", **all_selection()).status_code == 422
    assert (
        call(
            g, review, "batch-decision", **all_selection(), decision="approved"
        ).status_code
        == 422
    )
    assert g["db"].query(CaseReviewDecision).count() == 0
    response = call(
        g, review, "item-selection", **all_selection(), excludeIds=[items[0]["id"]]
    )
    assert response.status_code == 200 and response.json()["data"]["count"] == 10000
    assert response.json()["data"]["excludedCount"] == 1
