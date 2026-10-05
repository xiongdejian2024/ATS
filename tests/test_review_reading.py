"""独立审阅只读详情、个人历史结果及权限范围回归。"""

from test_case_governance import governance, request_review
from test_review_item_management import vote, manage, detail
from test_review_workspace import endpoint
from models import TestCase as Case
from models.case_governance import CaseVersion, CaseReviewDecision, CaseReviewItem
from models.case_features import (
    CaseProjectSettings,
    CaseTemplate,
    CaseIssue,
    CaseIssueLink,
)
from models.test_case import CaseAttachment
from services.test_case_service import TestCaseService
from schemas.test_case import TestCaseUpdate as CaseUpdate


def reading(g, review, item=None):
    return g["client"].get(
        endpoint(g)
        + f"/{review['id']}/items/{(item or review['items'][0])['id']}/reading"
    )


def test_reading_snapshot_basic_requirements_files_and_history_are_readonly(governance):
    g = governance
    db = g["db"]
    case = g["cases"][0]
    template = CaseTemplate(
        project_id=g["project"].id,
        name="审阅自定义模板",
        fields=[{"key": "purpose", "name": "测试目的", "type": "text"}],
        defaults={},
        created_by=g["users"][0].id,
    )
    db.add(template)
    db.flush()
    TestCaseService.update_test_case(
        db,
        case.id,
        CaseUpdate(
            template_id=template.id,
            custom_fields={"purpose": "读取真实值"},
            case_edit_type="TEXT",
            text_description="<p>文本描述</p>",
            expected_result="<p>整体预期</p>",
            description="<p>备注</p>",
        ),
        g["users"][0].id,
    )
    review = request_review(g)
    vote(g, review, 1)
    issue = CaseIssue(
        project_id=g["project"].id,
        kind="requirement",
        title="软件需求",
        status="open",
        created_by=g["users"][0].id,
        updated_by=g["users"][0].id,
    )
    db.add(issue)
    db.flush()
    db.add(
        CaseIssueLink(case_id=case.id, issue_id=issue.id, created_by=g["users"][0].id)
    )
    db.add(
        CaseAttachment(
            case_id=case.id,
            file_name="审阅附件.txt",
            file_path="/private/never-expose",
            file_size=12,
            file_type="text/plain",
        )
    )
    db.commit()
    count = db.query(CaseVersion).count()
    response = reading(g, review)
    assert response.status_code == 200, response.text
    data = response.json()["data"]
    assert (
        data["review"]["items"] == []
        and data["item"]["snapshot"]["case_edit_type"] == "TEXT"
    )
    assert data["item"]["snapshot"]["custom_fields"]["purpose"] == "读取真实值"
    assert data["customFields"][0]["name"] == "测试目的"
    assert data["createdAt"] and data["item"]["creator"]
    assert [r["title"] for r in data["requirements"]] == ["软件需求"]
    assert data["attachments"][0]["fileName"] == "审阅附件.txt"
    assert "never-expose" not in response.text and "filePath" not in response.text
    assert (
        len(data["history"]) == 1
        and data["history"][0]["detail"]["decision"] == "approved"
    )
    assert (
        db.query(CaseVersion).count() == count
        and db.query(CaseReviewDecision).count() == 1
    )


def test_my_result_uses_latest_nonabandoned_history_and_does_not_filter_assignment(
    governance,
):
    g = governance
    review = request_review(g, cases=[c.id for c in g["cases"]])
    vote(g, review, 1)
    g["state"]["user"] = g["users"][1]
    data = reading(g, review).json()["data"]
    assert (
        data["item"]["myStatus"] == "approved"
        and data["item"]["reviewState"] == "under_review"
    )
    vote(g, review, 1, decision="suggestion")
    g["state"]["user"] = g["users"][1]
    assert reading(g, review).json()["data"]["item"]["myStatus"] == "under_review"
    # 本人历史是建议，有效通过票仍保留，不将历史结果冒充整体状态。
    assert g["db"].query(CaseReviewDecision).count() == 1
    g["state"]["user"] = g["users"][0]
    assert manage(g, review, "re-review").status_code == 403
    # 用指定的项目所有者发起新评审，验证手动与系统重提审发起人差异。
    owned = request_review(g, reviewers=[g["users"][0].id, g["users"][1].id])
    vote(g, owned, 0)
    assert manage(g, owned, "re-review").status_code == 200
    assert reading(g, owned).json()["data"]["item"]["myStatus"] == "re_review"
    g["db"].add(CaseProjectSettings(project_id=g["project"].id, auto_resubmit=True))
    g["db"].commit()
    TestCaseService.update_test_case(
        g["db"], g["cases"][0].id, CaseUpdate(name="系统自动提审"), g["users"][0].id
    )
    assert reading(g, owned).json()["data"]["item"]["myStatus"] == "un_review"
    history = reading(g, owned).json()["data"]["history"]
    assert len(history) == 3 and sum(e["abandoned"] for e in history) == 2


def test_multiple_result_range_and_reading_permissions_preserve_all_data(governance):
    g = governance
    review = request_review(
        g, cases=[c.id for c in g["cases"]], reviewers=[g["users"][0].id], policy="any"
    )
    vote(g, review, 0)
    response = g["client"].get(
        endpoint(g) + f"/{review['id']}/items", params={"states": "approved,un_review"}
    )
    assert response.status_code == 200 and response.json()["data"]["total"] == 2
    assert (
        g["client"]
        .get(endpoint(g) + f"/{review['id']}/items", params={"states": "bad"})
        .status_code
        == 422
    )
    g["state"]["user"] = g["users"][1]
    data = reading(g, review).json()["data"]
    assert not data["item"]["canVote"] and data["item"]["myStatus"] == "un_review"
    g["state"]["user"] = g["users"][0]
    foreign = request_review(g, cases=[g["cases"][1].id])
    assert reading(g, review, item=foreign["items"][0]).status_code == 404
    g["state"]["user"] = g["users"][3]
    assert reading(g, review).status_code == 403
    assert g["db"].query(CaseReviewDecision).count() == 1


def test_recycled_and_archived_reading_keeps_snapshot_without_vote_entry(governance):
    g = governance
    review = request_review(g, reviewers=[g["users"][0].id], policy="any")
    vote(g, review, 0)
    assert g["client"].post(endpoint(g) + f"/{review['id']}/archive").status_code == 200
    data = reading(g, review).json()["data"]
    assert data["review"]["archived"] and not data["item"]["canVote"]
    from utils.datetime_utils import beijing_now

    g["cases"][0].deleted_at = beijing_now()
    g["db"].commit()
    data = reading(g, review).json()["data"]
    assert data["item"]["recycled"] and not data["item"]["canVote"]
    assert data["item"]["snapshot"]["name"] and len(data["history"]) == 1


def test_recycled_live_review_cannot_vote_and_history_stays_unchanged(governance):
    g = governance
    review = request_review(g, reviewers=[g["users"][0].id], policy="any")
    from utils.datetime_utils import beijing_now

    g["cases"][0].deleted_at = beijing_now()
    g["db"].commit()
    data = reading(g, review).json()["data"]
    assert data["item"]["recycled"] and not data["item"]["canVote"]
    response = g["client"].post(
        g["base"]
        + f"/reviews/{review['id']}/items/{review['items'][0]['id']}/decision",
        json={"decision": "approved"},
    )
    assert response.status_code == 404
    assert reading(g, review).json()["data"]["history"] == []
    assert g["db"].query(CaseReviewDecision).count() == 0
