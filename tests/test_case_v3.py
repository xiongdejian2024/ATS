"""V3 用例语义回归：最后结论、组合筛选、模块和文件互操作。"""

import io
import json
import zipfile
import pytest
from test_case_governance import governance, request_review
from test_case_features import features
from models.module import Module
from models.case_governance import CaseReviewEvent, CaseReviewFollow
from services.case_interchange import read_xmind, export_xmind
from fastapi import HTTPException


def test_single_review_last_effective_vote_and_suggestion_history(governance):
    g = governance
    review = request_review(g, policy="any")
    assert review["mode"] == "single"
    url = (
        g["base"] + f"/reviews/{review['id']}/items/{review['items'][0]['id']}/decision"
    )
    g["state"]["user"] = g["users"][1]
    assert (
        g["client"]
        .post(url, json={"decision": "approved", "comment": "第一次通过"})
        .json()["data"]["status"]
        == "approved"
    )
    g["state"]["user"] = g["users"][2]
    assert (
        g["client"]
        .post(url, json={"decision": "rejected", "comment": "最后结论不通过"})
        .json()["data"]["status"]
        == "rejected"
    )
    result = (
        g["client"]
        .post(url, json={"decision": "suggestion", "comment": "建议不计票"})
        .json()["data"]
    )
    assert result["status"] == "rejected"
    assert len([v for v in result["history"] if v["action"] == "评审结论"]) == 3
    assert (
        g["client"]
        .post(url, json={"decision": "approved", "comment": "修订通过"})
        .json()["data"]["status"]
        == "approved"
    )


def test_multiple_review_revote_assignments_batch_atomic_and_resubmit(governance):
    g = governance
    c = g["client"]
    body = {
        "name": "逐条评审",
        "mode": "multiple",
        "caseIds": [v.id for v in g["cases"]],
        "reviewerIds": [g["users"][1].id, g["users"][2].id],
        "itemReviewers": {g["cases"][1].id: [g["users"][2].id]},
        "startDate": "2020-01-01",
        "endDate": "2020-01-02",
    }
    review = c.post(g["base"] + "/reviews", json=body).json()["data"]
    g["state"]["user"] = g["users"][1]
    response = c.post(
        g["base"] + f"/reviews/{review['id']}/batch-decision",
        json={
            "itemIds": [i["id"] for i in review["items"]],
            "decision": "approved",
            "comment": "批量权限测试",
        },
    )
    assert response.status_code == 403
    assert all(
        not i["decisions"]
        for i in c.get(g["base"] + f"/reviews/{review['id']}").json()["data"]["items"]
    )
    first = next(i for i in review["items"] if i["caseId"] == g["cases"][0].id)
    url = g["base"] + f"/reviews/{review['id']}/items/{first['id']}/decision"
    assert (
        c.post(
            url, json={"decision": "rejected", "comment": "仍可在周期后投票"}
        ).status_code
        == 200
    )
    assert (
        c.post(url, json={"decision": "approved", "comment": "更正结论"}).json()[
            "data"
        ]["items"][review["items"].index(first)]["status"]
        == "pending"
    )
    g["state"]["user"] = g["users"][2]
    response = c.post(
        g["base"] + f"/reviews/{review['id']}/batch-decision",
        json={
            "itemIds": [i["id"] for i in review["items"]],
            "decision": "approved",
            "comment": "全部通过",
        },
    )
    assert response.json()["data"]["status"] == "approved"
    g["state"]["user"] = g["users"][0]
    assert c.put(g["base"] + f"/reviews/{review['id']}", json=body).status_code == 409
    c.put(f"/api/v1/test-cases/{g['cases'][0].id}", json={"name": "内容已变"})
    new = c.post(g["base"] + f"/reviews/{review['id']}/resubmit", json={}).json()[
        "data"
    ]
    assert new["id"] != review["id"] and new["parentReviewId"] == review["id"]
    assert (
        next(i for i in new["items"] if i["caseId"] == g["cases"][0].id)["snapshot"][
            "name"
        ]
        == "内容已变"
    )
    assert (
        c.get(g["base"] + f"/reviews/{review['id']}").json()["data"]["status"]
        == "superseded"
    )


def test_review_copy_edit_follow_keeps_old_history(governance):
    g = governance
    c = g["client"]
    review = request_review(g)
    copied = c.post(g["base"] + f"/reviews/{review['id']}/copy", json={}).json()["data"]
    assert copied["id"] != review["id"]
    edited = c.put(
        g["base"] + f"/reviews/{copied['id']}",
        json={
            "name": "编辑评审",
            "caseIds": [g["cases"][0].id],
            "reviewerIds": [g["users"][1].id],
            "mode": "single",
        },
    )
    assert edited.status_code == 200, edited.text
    assert edited.json()["data"]["mode"] == "single"
    url = g["base"] + f"/reviews/{review['id']}/follow"
    assert c.post(url).status_code == 200 and c.post(url).status_code == 200
    assert c.get(url).json()["data"]["count"] == 1
    assert c.delete(url).status_code == 200


def test_advanced_filter_or_not_multi_tag_sort_and_export(features):
    g = features
    c = g["client"]
    first, second = g["cases"]
    c.put(
        f"/api/v1/test-cases/{first.id}",
        json={"priority": "P0", "tags": ["冒烟", "回归"]},
    )
    c.put(f"/api/v1/test-cases/{second.id}", json={"priority": "P1", "tags": ["回归"]})
    query = {
        "project_id": g["project"].id,
        "filters": json.dumps(
            {
                "logic": "or",
                "conditions": [
                    {"field": "priority", "operator": "in", "value": ["P0", "P1"]},
                    {"field": "name", "operator": "equals", "value": "不匹配"},
                ],
            }
        ),
        "sort_by": "priority",
        "sort_order": "asc",
    }
    data = c.get("/api/v1/test-cases", params=query).json()["data"]
    assert [r["id"] for r in data["items"]] == [first.id, second.id]
    query["filters"] = json.dumps(
        {
            "logic": "and",
            "conditions": [
                {"field": "priority", "operator": "not_in", "value": ["P0"]}
            ],
        }
    )
    assert (
        c.get("/api/v1/test-cases", params=query).json()["data"]["items"][0]["id"]
        == second.id
    )
    assert (
        c.get(
            "/api/v1/test-cases",
            params={"project_id": g["project"].id, "tags": "冒烟,回归"},
        ).json()["data"]["total"]
        == 1
    )
    query["filters"] = json.dumps(
        {"conditions": [{"field": "unsupported", "operator": "equals", "value": 1}]}
    )
    assert c.get("/api/v1/test-cases", params=query).status_code == 422
    export = c.get(
        f"/api/v1/projects/{g['project'].id}/cases/export",
        params={"case_ids": first.id},
    )
    assert export.status_code == 200, export.text
    import openpyxl

    rows = list(openpyxl.load_workbook(io.BytesIO(export.content)).active.values)
    assert len(rows) == 2 and first.name in rows[1]
    assert (
        c.get(
            f"/api/v1/projects/{g['project'].id}/cases/export",
            params={"case_ids": g["foreign"].id},
        ).status_code
        == 404
    )


def test_module_move_root_cycle_and_project_isolation(features):
    g = features
    db = g["db"]
    c = g["client"]
    parent = Module(project_id=g["project"].id, name="父", level=1)
    db.add(parent)
    db.flush()
    child = Module(project_id=g["project"].id, name="子", parent_id=parent.id, level=2)
    other = Module(project_id=g["foreign"].project_id, name="外部", level=1)
    db.add_all([child, other])
    db.commit()
    base = f"/api/v1/projects/{g['project'].id}/modules"
    assert c.put(base + f"/{parent.id}", json={"parentId": child.id}).status_code == 422
    assert c.put(base + f"/{child.id}", json={"parentId": other.id}).status_code == 422
    assert c.put(base + f"/{other.id}", json={"parentId": None}).status_code == 404
    assert (
        c.put(
            base + f"/{child.id}", json={"parentId": None, "sortOrder": 3}
        ).status_code
        == 200
    )
    db.refresh(child)
    assert child.parent_id is None and child.level == 1 and child.sort_order == 3


def make_archive(name, content):
    data = io.BytesIO()
    with zipfile.ZipFile(data, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(name, content)
    return data.getvalue()


def test_xmind_standard_json_xml_and_roundtrip(features):
    g = features
    case = g["cases"][0]
    rows = read_xmind(export_xmind([case]))
    assert rows[0]["用例名称"] == case.name
    assert json.loads(rows[0]["测试步骤"]) == case.steps
    xml = '<xmap-content xmlns="urn:xmind:xmap:xmlns:content:2.0"><sheet><topic><title>模块</title><children><topics type="attached"><topic><title>普通叶子用例</title></topic></topics></children></topic></sheet></xmap-content>'
    assert read_xmind(make_archive("content.xml", xml))[0]["用例名称"] == "普通叶子用例"
    base = f"/api/v1/projects/{g['project'].id}/cases"
    exported = g["client"].get(
        base + "/export", params={"format": "xmind", "case_ids": case.id}
    )
    assert exported.status_code == 200, exported.text
    imported = g["client"].post(
        base + "/import",
        files={"file": ("往返.xmind", exported.content, "application/octet-stream")},
    )
    assert (
        imported.status_code == 200 and imported.json()["status"] == "success"
    ), imported.text


def test_xmind_rejects_entities_and_expansion_bomb():
    xml = '<!DOCTYPE x [<!ENTITY attack SYSTEM "file:///etc/passwd">]><xmap-content><sheet><topic><title>&attack;</title></topic></sheet></xmap-content>'
    with pytest.raises(HTTPException) as error:
        read_xmind(make_archive("content.xml", xml))
    assert error.value.status_code == 422
    with pytest.raises(HTTPException) as error:
        read_xmind(make_archive("content.json", " " * (21 * 1024 * 1024)))
    assert error.value.status_code == 413


def test_auto_resubmit_setting_snapshot_hook_and_member_permissions(features):
    g = features
    c = g["client"]
    assert c.get(g["features"] + "/settings").json()["data"] == {"autoResubmit": False}
    g["state"]["user"] = g["users"][1]
    assert (
        c.put(g["features"] + "/settings", json={"autoResubmit": True}).status_code
        == 403
    )
    g["state"]["user"] = g["users"][0]
    assert (
        c.put(g["features"] + "/settings", json={"autoResubmit": True}).status_code
        == 200
    )
    review = request_review(g)
    response = c.put(
        f"/api/v1/test-cases/{g['cases'][0].id}", json={"name": "自动触发新轮次"}
    )
    assert response.status_code == 200, response.text
    rows = c.get(g["base"] + "/reviews").json()["data"]
    assert len(rows) == 2
    newer = next(row for row in rows if row["id"] != review["id"])
    assert (
        newer["parentReviewId"] == review["id"]
        and newer["items"][0]["snapshot"]["name"] == "自动触发新轮次"
    )
    assert (
        next(row for row in rows if row["id"] == review["id"])["status"] == "superseded"
    )


def test_step_export_fields_and_xmind_module_preview_is_read_only(features):
    g = features
    c = g["client"]
    base = f"/api/v1/projects/{g['project'].id}/cases"
    exported = c.get(
        base + "/export",
        params={
            "case_ids": g["cases"][0].id,
            "layout": "step",
            "fields": "caseCode,name,step,action,expected",
        },
    )
    import openpyxl

    rows = list(openpyxl.load_workbook(io.BytesIO(exported.content)).active.values)
    assert rows[0] == ("ID", "用例名称", "步骤序号", "操作", "预期结果")
    assert rows[1][2:] == (1, "打开", "可见")
    data = [
        {
            "rootTopic": {
                "title": "项目",
                "children": {
                    "attached": [
                        {
                            "title": "模块A",
                            "children": {
                                "attached": [
                                    {
                                        "title": "模块B",
                                        "children": {"attached": [{"title": "新用例"}]},
                                    }
                                ]
                            },
                        }
                    ]
                },
            }
        }
    ]
    file = make_archive("content.json", json.dumps(data, ensure_ascii=False))
    preview = c.post(
        base + "/import?validate_only=true", files={"file": ("模块.xmind", file)}
    )
    assert preview.json()["status"] == "success", preview.text
    assert g["db"].query(Module).count() == 0
    imported = c.post(base + "/import", files={"file": ("模块.xmind", file)})
    assert imported.json()["status"] == "success", imported.text
    assert g["db"].query(Module).count() == 2
    assert c.get(
        "/api/v1/test-cases", params={"project_id": g["project"].id, "search": "新用例"}
    ).json()["data"]["items"][0]["moduleId"]


def test_import_keeps_explicit_fields_over_template_defaults(features):
    g = features
    c = g["client"]
    template = c.post(
        g["features"] + "/templates",
        json={
            "name": "默认导入",
            "isDefault": True,
            "defaults": {
                "priority": "P1",
                "steps": [{"step": 1, "action": "默认步骤", "expected": "默认"}],
            },
            "fields": [],
        },
    )
    assert template.status_code == 200
    csv = "用例名称,用例等级,测试步骤\n显式值,P0,1. 显式步骤\n"
    response = c.post(
        f"/api/v1/projects/{g['project'].id}/cases/import",
        files={"file": ("导入.csv", csv.encode())},
    )
    assert response.json()["status"] == "success", response.text
    row = c.get(
        "/api/v1/test-cases", params={"project_id": g["project"].id, "search": "显式值"}
    ).json()["data"]["items"][0]
    assert row["priority"] == "P0" and row["steps"][0]["action"] == "显式步骤"


@pytest.mark.parametrize('layout',['case','step'])
def test_excel_actual_roundtrip_retains_steps_template_custom_and_requirement(features,layout):
    g=features;c=g['client'];case=g['cases'][0]
    template=c.post(g['features']+'/templates',json={'name':'往返模板','fields':[{'key':'platform','name':'平台','type':'text'}]}).json()['data']
    payload={'precondition':'车辆启动','steps':[{'step':1,'action':'第一行\n第二行','expected':'应答1\n应答2'},{'step':2,'action':'下一步','expected':'完成'}],'requirement_ref':'REQ-中文-001','tags':['冒烟','控制器'],'template_id':template['id'],'custom_fields':{'platform':'车型A'}}
    assert c.put(f'/api/v1/test-cases/{case.id}',json=payload).status_code==200
    base=f"/api/v1/projects/{g['project'].id}/cases"
    exported=c.get(base+'/export',params={'case_ids':case.id,'layout':layout})
    assert exported.status_code==200
    c.put(f'/api/v1/test-cases/{case.id}',json={'steps':[],'precondition':'改变','requirement_ref':'改变','custom_fields':{'platform':'B'}})
    imported=c.post(base+'/import',files={'file':('往返.xlsx',exported.content)})
    assert imported.json()['status']=='success',imported.text
    current=c.get(f'/api/v1/test-cases/{case.id}',params={'project_id':g['project'].id}).json()['data']
    assert current['steps']==payload['steps']
    assert current['precondition']==payload['precondition'] and current['requirementRef']==payload['requirement_ref']
    assert current['customFields']==payload['custom_fields'] and current['templateId']==template['id']
