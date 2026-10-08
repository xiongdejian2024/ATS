"""评审关联高级视图只读取项目主用例，不触发执行或改写历史。"""
import json
from test_case_governance import governance
from test_review_workspace import endpoint
from models import TestCase as Case, ProjectMember
from models.plan_case_view import PlanCaseSavedView
from models.case_governance import CaseVersion


def condition(field, value, operator="equals"):
    return dict(field=field, operator=operator, value=value)


def test_advanced_pages_and_select_all_use_identical_current_scope(governance):
    g = governance
    db, client = g["db"], g["client"]
    versions_before = db.query(CaseVersion).count()
    first, second = g["cases"]
    first.tags = ["回归"]
    second.tags = ["诊断"]
    first.custom_fields = {"enabled": False, "zero": 0}
    db.add(Case(id="not-functional", project_id=first.project_id, name="排除接口",
                case_code="API", type="api", steps=[], created_by=g["users"][0].id))
    db.commit()
    raw = dict(conditions=[condition("tags", "回归", "contains"), condition("tags", "诊断", "contains")], logic="or")
    url = endpoint(g)
    pages = [client.get(url+"/candidates", params=dict(filters=json.dumps(raw), size=1, page=p, search="过时搜索", folder="非法旧目录", priority="P3")).json()["data"] for p in (1, 2)]
    assert pages[0]["total"] == pages[1]["total"] == 2
    ids = {row["id"] for page in pages for row in page["items"]}
    assert ids == {first.id, second.id}
    picked = client.post(url+"/candidate-selection", json=dict(filters=raw, excludeIds=[first.id], search="旧搜索", folder="非法旧目录"))
    assert picked.status_code == 200, picked.text
    assert picked.json()["data"]["caseIds"] == [second.id]
    typed = dict(conditions=[condition("customFields.enabled", False), condition("customFields.zero", 0)])
    assert client.get(url+"/candidates", params={"filters":json.dumps(typed)}).json()["data"]["total"] == 1
    second.deleted_at = __import__('datetime').datetime.now(); db.commit()
    assert client.post(url+"/candidate-selection", json=dict(filters=raw)).json()["data"]["caseIds"] == [first.id]
    for invalid in ("{", "[]", json.dumps(dict(conditions=[condition("result", "passed")]))):
        assert client.get(url+"/candidates", params={"filters":invalid}).status_code == 422
    assert db.query(CaseVersion).count() == versions_before


def test_candidate_views_crud_owner_project_namespace_and_quota(governance):
    g = governance
    db, client, url = g["db"], g["client"], endpoint(g)+"/candidate-views"
    filters = dict(filterConditions=[condition("tags", "回归", "contains")], filterLogic="and")
    create = lambda name: client.post(url, json=dict(name=name, filters=filters))
    response = create("我的回归")
    assert response.status_code == 200, response.text
    row = response.json()["data"]
    assert db.get(PlanCaseSavedView, row["id"]).category == "review-candidates"
    assert create("我的回归").status_code == 409
    assert client.put(url+"/"+row["id"], json={"name":"重命名"}).json()["data"]["filters"] == filters
    assert client.put(url+"/"+row["id"], json={"name":"重命名", "filters":None}).status_code == 422
    for i in range(9): assert create(f"视图{i}").status_code == 200
    assert create("超上限").status_code == 409
    actor = g["users"][1]
    g["state"]["user"] = actor
    assert client.get(url).json()["data"] == []
    assert client.put(url+"/"+row["id"], json={"name":"越权"}).status_code == 404
    assert client.delete(url+"/"+row["id"]).status_code == 404
    assert create("同名个人视图").status_code == 200
    actor.status = False; db.commit()
    assert create("停用拒绝").status_code == 403
    actor.status = True; db.commit()
    g["state"]["user"] = g["users"][0]
    foreign = url.replace(g["cases"][0].project_id, g["foreign"].project_id)
    assert client.get(foreign).status_code == 403
    db.add(PlanCaseSavedView(project_id=g["cases"][0].project_id, owner_id=g["users"][0].id,
                            category="functional", name="隔离", filters=filters)); db.commit()
    unrelated = db.query(PlanCaseSavedView).filter_by(category="functional").one()
    assert client.delete(url+"/"+unrelated.id).status_code == 404
    assert client.delete(url+"/"+row["id"]).status_code == 200
    assert create("恢复额度").status_code == 200
    assert client.post(url,json=dict(name="接口字段", filters=dict(filterConditions=[condition("apiChange",True)]))).status_code == 422


def test_saved_mine_scope_round_trip_and_identical_selection(governance):
    g = governance
    client, db, base = g["client"], g["db"], endpoint(g)
    first, second = g["cases"]
    first.created_by = g["users"][0].id
    second.created_by = g["users"][1].id
    first.tags = ["回归"]; second.tags = ["回归"]
    db.commit()
    filters = dict(filterConditions=[condition("tags", "回归", "contains")],filterLogic="or",mine=True)
    response = client.post(base+"/candidate-views",json=dict(name="我的回归",filters=filters))
    assert response.status_code == 200, response.text
    saved = client.get(base+"/candidate-views").json()["data"][0]["filters"]
    assert saved == filters
    raw = dict(conditions=saved["filterConditions"],logic=saved["filterLogic"])
    rows = client.get(base+"/candidates",params=dict(filters=json.dumps(raw),mine=saved["mine"])).json()["data"]
    selected = client.post(base+"/candidate-selection",json=dict(filters=raw,mine=saved["mine"])).json()["data"]
    assert [row["id"] for row in rows["items"]] == selected["caseIds"] == [first.id]
    invalid = client.post(base+"/candidate-views",json=dict(name="非法范围",filters={**filters,"mine":"true"}))
    assert invalid.status_code == 422
