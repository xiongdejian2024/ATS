"""核心内容自动同单提审：开关、历史、权限、多评审及事务原子性。"""

import pytest
from test_case_governance import governance, request_review
from test_review_item_management import vote, detail, manage
from test_review_workspace import endpoint
from models.case_features import CaseProjectSettings
from models.case_governance import (
    CaseReview,
    CaseReviewItem,
    CaseVersion,
    CaseReviewDecision,
    CaseReviewEvent,
)
from models import TestCase as Case
from schemas.test_case import TestCaseUpdate as CaseUpdate
from services.test_case_service import TestCaseService


def enable(g, enabled=True):
    db = g["db"]
    row = db.query(CaseProjectSettings).filter_by(project_id=g["project"].id).first()
    if not row:
        row = CaseProjectSettings(project_id=g["project"].id)
        db.add(row)
    row.auto_resubmit = enabled
    db.commit()


def edit(g, **fields):
    response = g["client"].put(f"/api/v1/test-cases/{g['cases'][0].id}", json=fields)
    assert response.status_code == 200, response.text
    return response


@pytest.mark.parametrize(
    "field,value",
    [
        ("name", "核心名称修改"),
        ("steps", [{"step": 1, "action": "新操作", "expected": "新期望"}]),
        ("text_description", "新文本描述"),
        ("expected_result", "新整体预期"),
    ],
)
def test_four_core_fields_reset_same_review_with_system_history(
    governance, field, value
):
    g = governance
    review = request_review(g, cases=[c.id for c in g["cases"]])
    review["items"].sort(key=lambda item: item["caseId"] != g["cases"][0].id)
    vote(g, review, 1)
    vote(g, review, 2)
    second = review["items"][1]
    vote(g, review, 1, item=second)
    enable(g)
    edit(g, **{field: value})
    data = detail(g, review)
    assert data["id"] == review["id"] and data["number"] == review["number"]
    assert data["reReviewedCount"] == 1 and data["underReviewedCount"] == 1
    assert g["db"].query(CaseReview).count() == 1
    assert g["db"].query(CaseReviewDecision).count() == 1
    item = g["db"].get(CaseReviewItem, review["items"][0]["id"])
    assert g["db"].get(CaseVersion, item.version_id).snapshot[field] == value
    reset = next(e for e in data["history"] if e["action"] == "重新提审")
    assert reset["actorId"] == g["users"][0].id
    assert reset["detail"]["automatic"] and reset["detail"]["changedFields"] == [field]
    assert len(reset["detail"]["invalidatedDecisions"]) == 2
    assert (
        sum(e["abandoned"] for e in data["history"] if e["action"] == "评审结论") == 2
    )
    listed = g["client"].get(
        "/api/v1/test-cases",
        params={"project_id": g["project"].id, "review_status": "resubmit"},
    )
    assert listed.status_code == 200, listed.text
    assert listed.json()["data"]["total"] == 1
    assert listed.json()["data"]["items"][0]["id"] == g["cases"][0].id
    # 编辑者未指定为评审人，自动动作仍有效；新票不复用旧轮的通过。
    assert vote(g, review, 1)["underReviewedCount"] == 2
    assert vote(g, review, 2)["passCount"] == 1


def test_disabled_noop_and_metadata_changes_do_not_reset(governance):
    g = governance
    review = request_review(g)
    vote(g, review, 1)
    pinned = g["db"].get(CaseReviewItem, review["items"][0]["id"]).version_id
    edit(g, name="开关关闭时改名")
    enable(g)
    count = g["db"].query(CaseVersion).count()
    edit(g, name="开关关闭时改名")
    assert g["db"].query(CaseVersion).count() == count
    edit(
        g,
        priority="P1",
        precondition="新前置条件",
        tags=["新标签"],
        executor_id=g["users"][2].id,
    )
    assert g["db"].get(CaseReviewItem, review["items"][0]["id"]).version_id == pinned
    assert g["db"].query(CaseReviewDecision).count() == 1
    assert g["db"].query(CaseReviewEvent).filter_by(action="重新提审").count() == 0
    # 评审停在v1，主用例已v3：核心修改应覆盖旧关联，而非仅查上一版。
    edit(g, expected_result="重新审阅核心预期")
    assert detail(g, review)["reReviewedCount"] == 1
    assert g["db"].query(CaseReviewDecision).count() == 0


def test_all_eligible_reviews_reset_archived_closed_keep_original(governance):
    g = governance
    reviews = [request_review(g) for _ in range(4)]
    for review in reviews:
        vote(g, review, 1)
        vote(g, review, 2)
    archived, closed = reviews[2:]
    assert (
        g["client"].post(endpoint(g) + f"/{archived['id']}/archive").status_code == 200
    )
    g["db"].get(CaseReview, closed["id"]).status = "cancelled"
    g["db"].commit()
    pinned = {
        r["id"]: g["db"].get(CaseReviewItem, r["items"][0]["id"]).version_id
        for r in reviews
    }
    enable(g)
    edit(g, name="多个关联同时重新提审")
    assert g["db"].query(CaseReview).count() == 4
    for r in reviews:
        item = g["db"].get(CaseReviewItem, r["items"][0]["id"])
        reset = r in reviews[:2]
        assert (item.status == "re_review") == reset
        assert (item.version_id != pinned[r["id"]]) == reset
    assert g["db"].query(CaseReviewDecision).count() == 4
    assert g["db"].query(CaseReviewEvent).filter_by(action="重新提审").count() == 2


def test_automatic_system_history_and_reviewer_change_do_not_revive_votes(governance):
    g = governance
    review = request_review(g, reviewers=[g["users"][0].id, g["users"][1].id])
    vote(g, review, 0)
    enable(g)
    edit(g, name="编辑者也是评审人")
    assert detail(g, review)["reReviewedCount"] == 1
    # 自动发起人语义为系统，即使实际编辑者还在新名单，多人调整也改为未评审。
    response = manage(
        g, review, "item-reviewers", reviewerIds=[g["users"][0].id, g["users"][2].id]
    )
    assert response.status_code == 200, response.text
    assert response.json()["data"]["unReviewCount"] == 1
    assert g["db"].query(CaseReviewDecision).count() == 0
    edit(g, name="自动再开一轮")
    events = detail(g, review)["history"]
    assert sum(e["abandoned"] for e in events if e["action"] == "重新提审") == 1


def test_readonly_edit_and_failure_on_second_review_are_atomic(governance, monkeypatch):
    g = governance
    reviews = [request_review(g) for _ in range(2)]
    for r in reviews:
        vote(g, r, 1)
    enable(g)
    old_name = g["cases"][0].name
    version_count = g["db"].query(CaseVersion).count()
    g["state"]["user"] = g["users"][1]
    assert (
        g["client"]
        .put(f"/api/v1/test-cases/{g['cases'][0].id}", json={"name": "只读编辑"})
        .status_code
        == 403
    )
    g["state"]["user"] = g["users"][0]
    from services import review_auto_resubmit

    original = review_auto_resubmit.reset_items
    calls = []

    def fail_second(*args, **kwargs):
        calls.append(1)
        if len(calls) == 2:
            raise RuntimeError("模拟第二评审写入故障")
        return original(*args, **kwargs)

    monkeypatch.setattr(review_auto_resubmit, "reset_items", fail_second)
    with pytest.raises(RuntimeError, match="第二评审写入故障"):
        TestCaseService.update_test_case(
            g["db"], g["cases"][0].id, CaseUpdate(name="必须全部回滚"), g["users"][0].id
        )
    g["db"].expire_all()
    assert len(calls) == 2
    assert g["db"].get(Case, g["cases"][0].id).name == old_name
    assert g["db"].query(CaseVersion).count() == version_count
    assert g["db"].query(CaseReviewDecision).count() == 2
    assert g["db"].query(CaseReviewEvent).filter_by(action="重新提审").count() == 0


def test_version_restore_uses_same_automatic_hook(governance):
    g = governance
    review = request_review(g)
    edit(g, name="恢复前内容")
    versions = (
        g["client"]
        .get(g["base"] + f"/cases/{g['cases'][0].id}/versions")
        .json()["data"]
    )
    enable(g)
    response = g["client"].post(
        g["base"] + f"/cases/{g['cases'][0].id}/versions/{versions[-1]['id']}/restore",
        json={"expectedVersion": 2, "reason": "恢复核心内容"},
    )
    assert response.status_code == 200, response.text
    assert detail(g, review)["reReviewedCount"] == 1
    assert (
        g["db"].get(CaseReviewItem, review["items"][0]["id"]).version_id
        == response.json()["data"]["id"]
    )


def test_native_parameter_type_change_resets_same_review(governance):
    from api.v1.native_case import router
    g = governance
    g['client'].app.include_router(router, prefix='/api/v1')
    case=g['cases'][0]
    TestCaseService.update_test_case(g['db'],case.id,CaseUpdate(type='api',is_automated=True),g['users'][0].id)
    base=f"/api/v1/projects/{g['project'].id}/native-cases"
    response=g['client'].post(base+'/definitions',json=dict(name='真实参数定义',protocol='HTTP',path='/软件验证',parameters={'enabled':False}))
    assert response.status_code==200,response.text
    definition=response.json()['data']['definitions'][0]
    payload=dict(state='PROCESSING',apiDefinitionId=definition['id'],expectedDefinitionRevision=1,parameters={'enabled':False})
    assert g['client'].put(base+'/cases/'+case.id,json=payload).status_code==200
    review=request_review(g);vote(g,review,1);vote(g,review,2);enable(g)
    response=g['client'].put(base+'/cases/'+case.id,json={**payload,'expectedRevision':1,'parameters':{'enabled':0}})
    assert response.status_code==200,response.text
    data=detail(g,review)
    assert data['reReviewedCount']==1
    event=next(e for e in data['history'] if e['action']=='重新提审')
    assert event['detail']['changedFields']==['native_config'] and event['detail']['automatic']
    assert g['db'].query(CaseReview).count()==1
