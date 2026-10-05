"""评审目录与首页的软件回归：隔离库，不创建 Agent 或台架任务。"""

from test_case_governance import governance, request_review
from models.case_governance import (
    CaseReview,
    CaseReviewItem,
    CaseVersion,
    CaseReviewEvent,
)
from models.review_workspace import ReviewWorkspace, ReviewModule
from models import TestCase as Case


def endpoint(g):
    return g["base"] + "/review-workspace"


def module(g, name, parent=None):
    response = g["client"].post(
        endpoint(g) + "/modules", json={"name": name, "parentId": parent}
    )
    assert response.status_code == 200, response.text
    return response.json()["data"]


def listing(g, **params):
    response = g["client"].get(endpoint(g), params=params)
    assert response.status_code == 200, response.text
    return response.json()["data"]


def test_tree_hierarchy_duplicates_cycles_and_project_isolation(governance):
    g = governance
    parent = module(g, "动力系统")
    child = module(g, "点火", parent["id"])
    assert (
        g["client"]
        .post(endpoint(g) + "/modules", json={"name": "动力系统"})
        .status_code
        == 409
    )
    assert (
        g["client"]
        .put(
            endpoint(g) + "/modules/" + parent["id"],
            json={"name": "动力系统", "parentId": child["id"]},
        )
        .status_code
        == 422
    )
    other_url = (
        f"/api/v1/projects/{g['foreign'].project_id}/case-governance/review-workspace"
    )
    foreign = g["client"].post(other_url + "/modules", json={"name": "异域"})
    # 本项目负责人不能写其他人的项目。
    assert foreign.status_code == 403
    assert (
        next(row for row in listing(g)["modules"] if row["id"] == child["id"])[
            "parentId"
        ]
        == parent["id"]
    )
    g["state"]["user"] = g["users"][1]
    assert listing(g)["permissions"] == {"update": False, "delete": False}
    assert (
        g["client"]
        .post(endpoint(g) + "/modules", json={"name": "只读禁止"})
        .status_code
        == 403
    )
    assert g["db"].query(ReviewModule).count() == 2


def test_list_summary_scope_tags_descendants_and_literal_search(governance):
    g = governance
    parent, child = module(g, "父模块"), None
    child = module(g, "子模块", parent["id"])
    review = request_review(g)
    created = g["client"].post(
        g["base"] + "/reviews",
        json={
            "name": "特殊_%名称",
            "caseIds": [g["cases"][1].id],
            "reviewerIds": [g["users"][2].id],
            "itemReviewers": {g["cases"][1].id: [g["users"][1].id]},
            "moduleId": child["id"],
            "tags": ["烟雾测试"],
        },
    )
    assert created.status_code == 200, created.text
    identifier = created.json()["data"]["id"]
    assert created.json()["data"]["number"] > review["number"]
    assert listing(g, moduleId=parent["id"])["total"] == 1
    assert listing(g, moduleId=parent["id"], includeDescendants=False)["total"] == 0
    assert listing(g, moduleId="default")["total"] == 1
    assert listing(g, search="_%")["total"] == 1
    assert listing(g, search="烟雾测试")["items"][0]["modulePath"] == "父模块/子模块"
    assert listing(g, search=identifier)["total"] == 1
    assert listing(g, size=1)["total"] == 2
    assert len(listing(g, page=2, size=1)["items"]) == 1
    g["state"]["user"] = g["users"][1]
    assert listing(g, scope="reviewByMe")["total"] == 2
    assert listing(g, scope="createByMe")["total"] == 0
    assert all(row["lifecycle"] == "prepared" for row in listing(g)["items"])
    assert g["client"].get(endpoint(g), params={"sort": "非法字段"}).status_code == 422


def test_partial_reject_is_underway_archive_is_real_and_immutable(governance):
    g = governance
    review = request_review(
        g, reviewers=[g["users"][1].id], cases=[c.id for c in g["cases"]]
    )
    g["state"]["user"] = g["users"][1]
    first, second = review["items"]
    vote_url = g["base"] + f"/reviews/{review['id']}/items/"
    assert (
        g["client"]
        .post(
            vote_url + first["id"] + "/decision",
            json={"decision": "rejected", "comment": "预期不符"},
        )
        .status_code
        == 200
    )
    row = listing(g)["items"][0]
    assert row["lifecycle"] == "underway" and row["passRate"] == 0
    g["state"]["user"] = g["users"][0]
    assert g["client"].post(endpoint(g) + f"/{review['id']}/archive").status_code == 409
    g["state"]["user"] = g["users"][1]
    assert (
        g["client"]
        .post(
            vote_url + second["id"] + "/decision",
            json={"decision": "approved", "comment": "通过"},
        )
        .status_code
        == 200
    )
    assert listing(g)["items"][0]["lifecycle"] == "completed"
    assert listing(g)["items"][0]["passRate"] == 50
    g["state"]["user"] = g["users"][0]
    assert g["client"].post(endpoint(g) + f"/{review['id']}/archive").status_code == 200
    assert listing(g)["total"] == 0
    assert listing(g, lifecycle="archived")["items"][0]["passRate"] == 50
    assert (
        g["client"]
        .get(g["base"] + f"/reviews/{review['id']}")
        .json()["data"]["archived"]
        is True
    )
    assert (
        g["client"].post(g["base"] + f"/reviews/{review['id']}/resubmit").status_code
        == 409
    )
    assert (
        g["client"]
        .post(
            g["base"] + f"/reviews/{review['id']}/comments",
            json={"content": "不允许归档后写"},
        )
        .status_code
        == 409
    )
    assert (
        g["client"]
        .post(endpoint(g) + "/move", json={"reviewIds": [review["id"]]})
        .status_code
        == 409
    )
    g["state"]["user"] = g["users"][1]
    assert (
        g["client"]
        .post(
            vote_url + first["id"] + "/decision",
            json={"decision": "approved", "comment": "不能改历史"},
        )
        .status_code
        == 409
    )
    g["state"]["user"] = g["users"][0]
    copied = g["client"].post(g["base"] + f"/reviews/{review['id']}/copy")
    assert copied.status_code == 200 and copied.json()["data"]["archived"] is False


def test_batch_move_atomic_and_delete_preserves_cases_and_versions(governance):
    g = governance
    parent = module(g, "父模块")
    child = module(g, "子模块", parent["id"])
    review = request_review(g)
    client = g["client"]
    assert (
        client.post(
            endpoint(g) + "/move",
            json={"reviewIds": [review["id"], "不存在"], "moduleId": child["id"]},
        ).status_code
        == 404
    )
    assert (
        g["db"].query(ReviewWorkspace).filter_by(review_id=review["id"]).one().module_id
        is None
    )
    assert (
        client.post(
            endpoint(g) + "/move",
            json={"reviewIds": [review["id"]], "moduleId": child["id"]},
        ).status_code
        == 200
    )
    assert (
        client.post(
            endpoint(g) + "/modules/" + parent["id"] + "/delete",
            json={"name": "错误确认"},
        ).status_code
        == 409
    )
    versions = g["db"].query(CaseVersion).count()
    response = client.post(
        endpoint(g) + "/modules/" + parent["id"] + "/delete",
        json={"name": parent["name"]},
    )
    assert response.status_code == 200, response.text
    assert response.json()["data"] == {"deletedModules": 2, "deletedReviews": 1}
    assert g["db"].query(CaseReview).count() == 0
    assert g["db"].query(CaseReviewItem).count() == 0
    assert g["db"].query(CaseReviewEvent).count() == 0
    assert g["db"].query(ReviewWorkspace).count() == 0
    assert g["db"].query(Case).count() == 3
    assert g["db"].query(CaseVersion).count() == versions
    review = request_review(g)
    assert (
        client.post(
            endpoint(g) + f"/{review['id']}/delete", json={"name": "旧名称"}
        ).status_code
        == 409
    )
    assert (
        client.post(
            endpoint(g) + f"/{review['id']}/delete", json={"name": review["name"]}
        ).status_code
        == 200
    )


def test_legacy_read_is_nonmutating_and_metadata_copy_update_preservation(governance):
    g = governance
    parent = module(g, "评审目录")
    review = request_review(g)
    db = g["db"]
    info = db.query(ReviewWorkspace).filter_by(review_id=review["id"]).one()
    info.tags, info.module_id = ["历史标签"], parent["id"]
    db.commit()
    updated = g["client"].put(
        g["base"] + f"/reviews/{review['id']}",
        json={
            "name": "兼容编辑",
            "caseIds": [g["cases"][0].id],
            "reviewerIds": [g["users"][1].id],
        },
    )
    assert updated.status_code == 200 and updated.json()["data"]["tags"] == ["历史标签"]
    assert updated.json()["data"]["moduleId"] == parent["id"]
    copied = (
        g["client"].post(g["base"] + f"/reviews/{review['id']}/copy").json()["data"]
    )
    assert copied["tags"] == ["历史标签"] and copied["number"] != review["number"]
    db.query(ReviewWorkspace).delete(synchronize_session=False)
    db.commit()
    assert listing(g)["total"] == 2
    assert all(
        row["number"] is None and row["moduleName"] == "默认模块"
        for row in listing(g)["items"]
    )
    assert g["client"].get(g["base"] + f"/reviews/{review['id']}").status_code == 200
    assert db.query(ReviewWorkspace).count() == 0
