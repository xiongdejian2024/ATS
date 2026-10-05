"""独立评审创建/基本信息编辑：保留有效票、旧分配与快照。"""

from test_case_governance import governance, request_review
from models.case_governance import (
    CaseReviewItem,
    CaseReviewDecision,
    CaseVersion,
    CaseReviewEvent,
)
from models import TestCase as Case
from test_review_workspace import endpoint, listing, module


def header_body(g, **overrides):
    return dict(
        name="基本信息更新",
        reviewerIds=[g["users"][2].id],
        mode="single",
        description="新的说明",
        moduleId=None,
        tags=["编辑验证"],
        startTime="2026-10-05T09:30:01.123456+08:00",
        endTime="2026-10-05T10:00:00+08:00",
        **overrides,
    )


def test_create_empty_default_review_and_255_name_period_timezone(governance):
    g = governance
    name = "评" * 255
    response = g["client"].post(
        g["base"] + "/reviews",
        json={
            "name": name,
            "caseIds": [],
            "reviewerIds": [g["users"][1].id],
            "mode": "single",
            "startTime": "2026-10-05T01:30:01.123456Z",
            "endTime": "2026-10-05T10:00:00+08:00",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()["data"]
    assert (
        data["items"] == [] and data["startTime"] == "2026-10-05T09:30:01.123456+08:00"
    )
    assert data["startDate"] == "2026-10-05"
    assert listing(g)["items"][0]["lifecycle"] == "prepared"
    assert listing(g)["items"][0]["startTime"] == data["startTime"]
    assert g["client"].post(endpoint(g) + f"/{data['id']}/archive").status_code == 409
    assert (
        g["client"]
        .post(
            g["base"] + "/reviews",
            json={"name": "评" * 256, "reviewerIds": [g["users"][1].id]},
        )
        .status_code
        == 422
    )
    for period in [
        dict(startTime="2026-10-05T10:00:00"),
        dict(startTime="2026-10-05T10:00:00", endTime="2026-10-05T09:00:00"),
    ]:
        invalid = g["client"].post(
            g["base"] + "/reviews",
            json={"name": "时间校验", "reviewerIds": [g["users"][1].id], **period},
        )
        assert invalid.status_code == 422


def test_header_edit_keeps_decisions_versions_assignments_and_case_content(governance):
    g = governance
    review = (
        g["client"]
        .post(
            g["base"] + "/reviews",
            json={
                "name": "有效票保留",
                "caseIds": [c.id for c in g["cases"]],
                "reviewerIds": [g["users"][1].id],
                "mode": "single",
            },
        )
        .json()["data"]
    )
    identifier = review["id"]
    item_ids = [i["id"] for i in review["items"]]
    g["state"]["user"] = g["users"][1]
    assert (
        g["client"]
        .post(
            g["base"] + f"/reviews/{identifier}/items/{item_ids[0]}/decision",
            json={"decision": "approved", "comment": "已确认"},
        )
        .status_code
        == 200
    )
    g["state"]["user"] = g["users"][0]
    versions = g["db"].query(CaseVersion).count()
    target = module(g, "编辑目标")
    body = header_body(g)
    body["moduleId"] = target["id"]
    response = g["client"].put(endpoint(g) + f"/{identifier}/header", json=body)
    assert response.status_code == 200, response.text
    data = response.json()["data"]
    assert {i["id"] for i in data["items"]} == set(item_ids)
    assert data["reviewerIds"] == [g["users"][2].id]
    assert all(i["reviewerIds"] == [g["users"][1].id] for i in data["items"])
    assert data["items"][0]["decisions"][0]["comment"] == "已确认"
    assert g["db"].query(CaseVersion).count() == versions
    assert g["db"].query(CaseReviewDecision).count() == 1
    assert listing(g)["items"][0]["passRate"] == 50
    assert g["db"].get(Case, g["cases"][0].id).name == "用例0"
    copied = g["client"].post(g["base"] + f"/reviews/{identifier}/copy").json()["data"]
    assert (
        copied["startTime"] == data["startTime"] and copied["moduleId"] == target["id"]
    )
    assert all(not i["decisions"] for i in copied["items"])


def test_header_edit_freezes_legacy_assignment_rejects_mode_change_and_is_atomic(
    governance,
):
    g = governance
    review = request_review(g, reviewers=[g["users"][1].id])
    item = g["db"].get(CaseReviewItem, review["items"][0]["id"])
    item.reviewer_ids = None
    g["db"].commit()
    body = header_body(g)
    body["mode"] = "multiple"
    response = g["client"].put(endpoint(g) + f"/{review['id']}/header", json=body)
    assert response.status_code == 200, response.text
    assert response.json()["data"]["items"][0]["reviewerIds"] == [g["users"][1].id]
    body["mode"] = "single"
    assert (
        g["client"].put(endpoint(g) + f"/{review['id']}/header", json=body).status_code
        == 422
    )
    body["mode"] = "multiple"
    body["reviewerIds"] = [g["users"][3].id]
    body["name"] = "不能写入"
    assert (
        g["client"].put(endpoint(g) + f"/{review['id']}/header", json=body).status_code
        == 422
    )
    detail = g["client"].get(g["base"] + f"/reviews/{review['id']}").json()["data"]
    assert detail["name"] == "基本信息更新" and detail["reviewerIds"] == [
        g["users"][2].id
    ]
    g["state"]["user"] = g["users"][1]
    assert (
        g["client"]
        .put(endpoint(g) + f"/{review['id']}/header", json=header_body(g))
        .status_code
        == 403
    )


def test_empty_copy_and_legacy_period_clear_header_history_is_readonly(governance):
    g = governance
    response = g["client"].post(
        g["base"] + "/reviews",
        json={
            "name": "空评审",
            "reviewerIds": [g["users"][1].id],
            "mode": "single",
            "startDate": "2026-10-05",
            "endDate": "2026-10-06",
        },
    )
    assert response.status_code == 200
    review = response.json()["data"]
    assert review["startTime"] == "2026-10-05T00:00:00+08:00"
    copied = g["client"].post(g["base"] + f"/reviews/{review['id']}/copy")
    assert copied.status_code == 200 and copied.json()["data"]["items"] == []
    body = header_body(g)
    body["startTime"] = body["endTime"] = None
    updated = (
        g["client"]
        .put(endpoint(g) + f"/{review['id']}/header", json=body)
        .json()["data"]
    )
    assert updated["startTime"] is None and updated["startDate"] is None
    assert any(e["action"] == "编辑基本信息" for e in updated["history"])
    assert (
        g["db"]
        .query(CaseReviewEvent)
        .filter_by(review_id=review["id"], action="评审结论")
        .count()
        == 0
    )


def test_legacy_date_editor_keeps_precise_period_when_days_are_unchanged(governance):
    g = governance
    created = (
        g["client"]
        .post(
            g["base"] + "/reviews",
            json={
                "name": "旧日期编辑兼容",
                "caseIds": [g["cases"][0].id],
                "reviewerIds": [g["users"][1].id],
                "mode": "single",
                "startTime": "2026-10-05T09:30:01+08:00",
                "endTime": "2026-10-06T10:00:00+08:00",
            },
        )
        .json()["data"]
    )
    response = g["client"].put(
        g["base"] + f"/reviews/{created['id']}",
        json={
            "name": "日期客户端编辑",
            "caseIds": [g["cases"][0].id],
            "reviewerIds": [g["users"][1].id],
            "mode": "single",
            "startDate": "2026-10-05",
            "endDate": "2026-10-06",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["data"]["startTime"] == created["startTime"]
    assert response.json()["data"]["endTime"] == created["endTime"]


def test_header_edit_rejects_archived_closed_and_foreign_project(governance):
    g = governance
    review = request_review(g)
    item_id = review["items"][0]["id"]
    for user in g["users"][1:3]:
        g["state"]["user"] = user
        assert (
            g["client"]
            .post(
                g["base"] + f"/reviews/{review['id']}/items/{item_id}/decision",
                json={"decision": "approved", "comment": "归档前确认"},
            )
            .status_code
            == 200
        )
    g["state"]["user"] = g["users"][0]
    assert g["client"].post(endpoint(g) + f"/{review['id']}/archive").status_code == 200
    body = header_body(g)
    body["mode"] = "multiple"
    assert (
        g["client"].put(endpoint(g) + f"/{review['id']}/header", json=body).status_code
        == 409
    )
    foreign = f"/api/v1/projects/{g['foreign'].project_id}/case-governance/review-workspace/{review['id']}/header"
    assert g["client"].put(foreign, json=body).status_code == 403
    g["state"]["user"] = g["users"][3]
    assert g["client"].put(foreign, json=body).status_code == 404
    g["state"]["user"] = g["users"][0]
    detail = g["client"].get(g["base"] + f"/reviews/{review['id']}").json()["data"]
    assert detail["name"] == review["name"]
    assert len(detail["items"][0]["decisions"]) == 2
    closed = request_review(g)
    assert (
        g["client"].post(g["base"] + f"/reviews/{closed['id']}/cancel").status_code
        == 200
    )
    assert (
        g["client"].put(endpoint(g) + f"/{closed['id']}/header", json=body).status_code
        == 409
    )


def test_resubmit_legacy_changed_dates_override_precise_source_period(governance):
    g = governance
    original = (
        g["client"]
        .post(
            g["base"] + "/reviews",
            json={
                "name": "精确周期重提审",
                "reviewerIds": [g["users"][1].id],
                "mode": "single",
                "startTime": "2026-10-05T09:30:01+08:00",
                "endTime": "2026-10-06T10:00:00+08:00",
            },
        )
        .json()["data"]
    )
    response = g["client"].post(
        g["base"] + f"/reviews/{original['id']}/resubmit",
        json={
            "startDate": "2026-10-07",
            "endDate": "2026-10-08",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["data"]["startTime"] == "2026-10-07T00:00:00+08:00"
    assert response.json()["data"]["endTime"] == "2026-10-08T00:00:00+08:00"
