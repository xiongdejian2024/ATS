"""评审关联：服务端分页、目录计数、筛选全选及复制草稿保存。"""

from test_case_governance import governance
from test_review_workspace import endpoint
from models import Module, TestCase as Case
from models.case_governance import CaseReview


def test_review_candidates_paging_scope_counts_and_full_filtered_selection(governance):
    g = governance
    parent = Module(project_id=g["project"].id, name="父目录")
    g["db"].add(parent)
    g["db"].flush()
    child = Module(project_id=g["project"].id, name="子目录", parent_id=parent.id)
    g["db"].add(child)
    g["db"].flush()
    for i in range(25):
        g["db"].add(
            Case(
                project_id=g["project"].id,
                name=f"分页关联{i:02}",
                case_code=f"分页{i:02}",
                type="functional",
                steps=[],
                module_id=child.id,
                priority="P1",
                created_by=g["users"][0].id,
            )
        )
    g["db"].add(
        Case(
            project_id=g["project"].id,
            name="不得关联API",
            case_code="API",
            type="api",
            created_by=g["users"][0].id,
            steps=[],
            module_id=child.id,
        )
    )
    g["db"].commit()
    url = endpoint(g) + "/candidates"
    result = (
        g["client"].get(url, params={"folder": parent.id, "size": 20}).json()["data"]
    )
    assert result["total"] == 25 and len(result["items"]) == 20
    assert next(m for m in result["modules"] if m["id"] == parent.id)["count"] == 25
    assert result["counts"] == {"all": 27, "unassigned": 2}
    other_page = (
        g["client"]
        .get(url, params={"folder": parent.id, "size": 20, "page": 2})
        .json()["data"]
    )
    assert len(other_page["items"]) == 5
    assert not set(r["id"] for r in result["items"]) & set(
        r["id"] for r in other_page["items"]
    )
    selected = (
        g["client"]
        .post(
            endpoint(g) + "/candidate-selection",
            json={
                "folder": parent.id,
                "priority": "P1",
                "search": "分页",
                "excludeIds": [result["items"][0]["id"]],
            },
        )
        .json()["data"]
    )
    assert selected["total"] == 24 and len(set(selected["caseIds"])) == 24
    assert result["items"][0]["id"] not in selected["caseIds"]
    assert g["client"].get(url, params={"folder": "wrong"}).status_code == 404
    assert g["client"].get(url, params={"size": 101}).status_code == 422
    assert g["client"].get(url, params={"search": "_%"}).json()["data"]["total"] == 0
    g["state"]["user"] = g["users"][1]
    assert g["client"].get(url).status_code == 200
    assert (
        g["client"].post(endpoint(g) + "/candidate-selection", json={}).status_code
        == 403
    )
    foreign = f"/api/v1/projects/{g['foreign'].project_id}/case-governance/review-workspace/candidates"
    assert g["client"].get(foreign).status_code == 403
    assert g["db"].query(CaseReview).count() == 0


def test_copy_draft_header_overrides_create_only_when_saved(governance):
    g = governance
    original = (
        g["client"]
        .post(
            g["base"] + "/reviews",
            json={
                "name": "草稿源",
                "reviewerIds": [g["users"][1].id],
                "caseIds": [g["cases"][0].id],
                "mode": "single",
            },
        )
        .json()["data"]
    )
    # 只读源详情不会新建副本。
    assert g["client"].get(g["base"] + f"/reviews/{original['id']}").status_code == 200
    assert g["db"].query(CaseReview).count() == 1
    copy = g["client"].post(
        g["base"] + f"/reviews/{original['id']}/copy",
        json={
            "name": "确认保存的副本",
            "reviewerIds": [g["users"][2].id],
            "description": "草稿编辑",
            "tags": ["复制标签"],
            "moduleId": None,
            "startTime": "2026-10-05T09:45:00+08:00",
            "endTime": "2026-10-06T10:30:00+08:00",
        },
    )
    assert copy.status_code == 200, copy.text
    data = copy.json()["data"]
    assert data["name"] == "确认保存的副本" and data["tags"] == ["复制标签"]
    assert data["startTime"] == "2026-10-05T09:45:00+08:00"
    assert data["items"][0]["caseId"] == original["items"][0]["caseId"]
    assert data["items"][0]["reviewerIds"] == original["items"][0]["reviewerIds"]
    assert not data["items"][0]["decisions"]


def test_copy_invalid_composite_request_rejects_without_partial_rows(governance):
    g = governance
    original = (
        g["client"]
        .post(
            g["base"] + "/reviews",
            json={"name": "参数校验源", "reviewerIds": [g["users"][1].id]},
        )
        .json()["data"]
    )
    url = g["base"] + f"/reviews/{original['id']}/copy"
    for invalid in [
        {"tags": ["重复", "重复"]},
        {"startTime": "2026-10-05T09:00:00+08:00"},
        {"caseIds": None},
        {"reviewerIds": []},
        {"tags": ["过长" * 51]},
    ]:
        response = g["client"].post(url, json=invalid)
        assert response.status_code == 422, response.text
        assert g["db"].query(CaseReview).count() == 1
