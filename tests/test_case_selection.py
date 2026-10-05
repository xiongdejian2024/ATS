"""主用例跨页范围：共同集合、事务回滚、权限及真实导出回归。"""
import io
import json
import zipfile
import pytest
import openpyxl
from fastapi import HTTPException
from test_case_governance import governance
from models import TestCase as Case, Module
from models.case_features import CaseIssue, CaseIssueLink, CaseFollow
from models.case_governance import CaseVersion, CaseReview, CaseReviewItem
from models.task_queue import TaskQueue
from services.test_case_service import TestCaseService


@pytest.fixture
def selection(governance):
    g = governance
    rows = [Case(id=f"range-{i}", project_id=g["project"].id,
        name=f"范围用例{i:02}", case_code=f"RANGE-{i:02}", type="functional",
        priority="P1", steps=[{"step": 1, "action": "打开", "expected": "可见"}],
        created_by=g["users"][0].id) for i in range(23)]
    g["db"].add_all(rows)
    g["db"].commit()
    g["scope"] = dict(selectAll=True, condition={"search": "范围用例"}, excludeIds=["range-0", "range-21"])
    g["expected"] = {r.id for r in rows} - {"range-0", "range-21"}
    return g


def post(g, route, **extra):
    response = g["client"].post(g["base"]+route, json={**g["scope"], **extra})
    assert response.status_code == 200, response.text
    return response.json()["data"]


def test_preview_membership_and_review_draft_have_no_writes(selection):
    g = selection
    before = g["db"].query(CaseVersion).count()
    result = post(g, "/selection/preview")
    assert result["count"] == 21 and result["excludedCount"] == 2
    assert all(result["permissions"].values())
    members = post(g, "/selection/membership", candidateIds=["range-0", "range-1", "range-21", g["foreign"].id])
    assert members["caseIds"] == ["range-1"]
    result = g["client"].post(g["base"]+"/review-workspace/candidate-selection", json={"selectionScope": g["scope"], "search": "范围用例"})
    assert result.status_code == 200, result.text
    assert set(result.json()["data"]["caseIds"]) == {"range-0", "range-21"}
    assert g["db"].query(CaseVersion).count() == before
    assert g["db"].query(CaseReview).count() == g["db"].query(TaskQueue).count() == 0


def test_update_move_copy_issue_delete_share_same_exclusions(selection):
    g = selection
    db = g["db"]
    assert post(g, "/batch", priority="P0")["updated"] == 21
    assert {r.id for r in db.query(Case).filter_by(priority="P0")} == g["expected"]
    module = Module(project_id=g["project"].id, name="范围迁移")
    issue = CaseIssue(project_id=g["project"].id, kind="requirement", title="范围需求", created_by=g["users"][0].id, updated_by=g["users"][0].id)
    db.add_all([module, issue]); db.commit()
    assert post(g, "/batch", moduleId=module.id)["updated"] == 21
    assert {r.id for r in db.query(Case).filter_by(module_id=module.id)} == g["expected"]
    linked = post(g, "/selection/issues", issueId=issue.id)
    assert linked == {"linked": 21, "created": 21}
    assert post(g, "/selection/issues", issueId=issue.id)["created"] == 0
    assert {r.case_id for r in db.query(CaseIssueLink)} == g["expected"]
    copies = post(g, "/batch-copy", moduleId=None)["caseIds"]
    assert len(set(copies)) == 21
    assert {db.get(Case, i).name.removesuffix("（副本）") for i in copies} == {db.get(Case, i).name for i in g["expected"]}
    # 复制后的名称也命中搜索，精确排除新副本以核对原始集合。
    g["scope"]["excludeIds"] += copies
    assert post(g, "/selection/delete")["deleted"] == 21
    assert {r.id for r in db.query(Case).filter(Case.deleted_at.isnot(None))} == g["expected"]
    assert all(db.get(Case, i).deleted_at is None for i in ["range-0", "range-21", *copies])
    assert db.query(TaskQueue).count() == 0


def test_range_review_union_assignments_and_snapshot(selection):
    g = selection
    response = g["client"].post(g["base"]+"/reviews", json={
        "name":"跨页范围评审", "selection":g["scope"], "caseIds":["range-0"],
        "reviewerIds":[g["users"][0].id], "itemReviewers":{"range-0":[g["users"][1].id]}})
    assert response.status_code == 200, response.text
    review = response.json()["data"]
    assert {i["caseId"] for i in review["items"]} == g["expected"] | {"range-0"}
    assert next(i for i in review["items"] if i["caseId"] == "range-0")["reviewerIds"] == [g["users"][1].id]
    assert all(i["snapshot"]["name"].startswith("范围用例") for i in review["items"])
    invalid = g["client"].put(g["base"]+"/reviews/"+review["id"], json={"name":"无效替换", "reviewerIds":[g["users"][0].id], "selection":g["scope"]})
    assert invalid.status_code == 422
    assert g["db"].query(CaseReviewItem).count() == 22


@pytest.mark.parametrize("layout", ["case", "step"])
def test_actual_excel_and_xmind_contents(selection, layout):
    g = selection
    response = g["client"].post(g["base"]+"/selection/export", json={**g["scope"], "format":"xlsx", "layout":layout, "fields":"ID,用例名称", "sortBy":"name", "sortOrder":"asc"})
    assert response.status_code == 200, response.text
    rows = list(openpyxl.load_workbook(io.BytesIO(response.content)).active.values)
    assert rows[0] == ("ID", "用例名称")
    assert [row[1] for row in rows[1:]] == sorted(g["db"].get(Case, i).name for i in g["expected"])
    response = g["client"].post(g["base"]+"/selection/export", json={**g["scope"], "format":"xmind"})
    assert response.status_code == 200
    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        content = json.loads(archive.read("content.json"))
    branches = content[0]["rootTopic"]["children"]["attached"]
    assert {b["title"] for b in branches} == {g["db"].get(Case,i).name for i in g["expected"]}


def test_permission_identity_and_invalid_scope(selection):
    g = selection
    g["state"]["user"] = g["users"][1]
    preview = post(g, "/selection/preview")
    assert preview["count"] == 21 and not preview["permissions"]["update"]
    for path, extra in [("/batch", {"priority":"P0"}), ("/batch-copy",{"moduleId":None}), ("/selection/delete",{}), ("/selection/issues",{"issueId":"wrong"})]:
        assert g["client"].post(g["base"]+path,json={**g["scope"], **extra}).status_code == 403
    g["state"]["user"] = g["users"][0]
    invalids = [{}, {"caseIds":[g["foreign"].id]}, {"caseIds":["range-0"],"selectAll":True}, {"caseIds":["range-0"],"condition":{"mine":True}}, {"selectAll":True,"condition":{"user_id":g["users"][1].id}}, {"caseIds":["range-0","range-0"]}]
    for body in invalids:
        assert g["client"].post(g["base"]+"/selection/delete",json=body).status_code in {404,422}
    assert g["client"].post(g["base"]+"/batch",json={"selectAll":True,"condition":{"search":"不存在"},"priority":"P0"}).status_code == 409
    assert not any(r.deleted_at for r in g["db"].query(Case))
    assert post(g, "/selection/preview", condition={"filters":{"conditions":[{"field":"createdBy","operator":"equals","value":"CURRENT_USER"}],"logic":"and"}})["count"] == 23
    g["state"]["user"] = g["users"][1]
    assert post(g, "/selection/preview", condition={"mine":True})["count"] == 0


def test_failure_rolls_back_all_cases_versions_and_deletions(selection, monkeypatch):
    g = selection
    from services import case_governance
    original = case_governance.snapshot_case
    calls = 0
    def fail_snapshot(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 4: raise HTTPException(409, "注入第二条快照失败")
        return original(*args, **kwargs)
    before = g["db"].query(CaseVersion).count()
    monkeypatch.setattr(case_governance, "snapshot_case", fail_snapshot)
    assert g["client"].post(g["base"]+"/batch",json={**g["scope"],"priority":"P0"}).status_code == 409
    assert g["db"].query(CaseVersion).count() == before
    assert not g["db"].query(Case).filter_by(priority="P0").count()
    original_delete = TestCaseService.delete_test_case
    calls = 0
    def fail_delete(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 2: raise HTTPException(409, "注入第二条删除失败")
        return original_delete(*args, **kwargs)
    monkeypatch.setattr(TestCaseService, "delete_test_case", fail_delete)
    assert g["client"].post(g["base"]+"/selection/delete",json=g["scope"]).status_code == 409
    assert not g["db"].query(Case).filter(Case.deleted_at.isnot(None)).count()


def test_ten_thousand_limit_after_exclusion(governance):
    g = governance
    db = g["db"]
    db.add_all([Case(id=f"limit-{i}",project_id=g["project"].id,name="边界",case_code=f"LIMIT-{i}",type="functional",steps=[],created_by=g["users"][0].id) for i in range(10001)])
    db.commit()
    body = {"selectAll":True,"condition":{"search":"边界"}}
    assert g["client"].post(g["base"]+"/selection/preview",json=body).status_code == 422
    assert g["client"].post(g["base"]+"/selection/preview",json={**body,"excludeIds":["limit-0"]}).json()["data"]["count"] == 10000
    assert g["client"].post(g["base"]+"/selection/preview",json={**body,"excludeIds":[g["foreign"].id]}).status_code == 422


def test_empty_dynamic_scope_can_save_explicit_review_additions(selection):
    g = selection
    response = g["client"].post(g["base"]+"/reviews", json={
        "name":"空范围追加评审", "selection":{"selectAll":True,"condition":{"search":"不存在"}},
        "caseIds":["range-0"],"reviewerIds":[g["users"][0].id]})
    assert response.status_code == 200, response.text
    assert [i["caseId"] for i in response.json()["data"]["items"]] == ["range-0"]
