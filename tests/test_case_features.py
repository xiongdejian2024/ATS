"""用例扩展的隔离数据库与临时附件验收，不运行台架。"""

import pytest
from test_case_governance import governance
from api.v1.case_features import router
from models.test_case import TestCase as Case, CaseAttachment
from models.case_features import CaseChange
from config import settings


@pytest.fixture
def features(governance, tmp_path, monkeypatch):
    g = governance
    g["client"].app.include_router(router, prefix="/api/v1")
    g["features"] = f"/api/v1/projects/{g['project'].id}/case-features"
    monkeypatch.setenv("CASE_ATTACHMENT_DIR", str(tmp_path))
    g["storage"] = tmp_path
    return g


def test_attachment_bytes_permissions_limits_and_deletion(features, monkeypatch):
    g = features
    c, base = g["client"], g["features"]
    url = base + f"/cases/{g['cases'][0].id}/attachments"
    response = c.post(
        url, files={"file": ("../验收.pdf", b"%PDF-evidence", "application/pdf")}
    )
    assert response.status_code == 200, response.text
    attachment = response.json()["data"]
    assert "/" not in attachment["fileName"]
    download = base + f"/attachments/{attachment['id']}/download"
    assert c.get(download).content == b"%PDF-evidence"
    assert "attachment;" in c.get(download).headers["content-disposition"]
    assert "nosniff" == c.get(download).headers["x-content-type-options"]
    assert (
        c.post(url, files={"file": ("x.html", b"<script/>", "text/html")}).status_code
        == 400
    )
    monkeypatch.setattr(settings, "MAX_FILE_SIZE", 4)
    assert (
        c.post(url, files={"file": ("x.pdf", b"12345", "application/pdf")}).status_code
        == 400
    )
    g["state"]["user"] = g["users"][3]
    assert c.get(download).status_code == 403
    g["state"]["user"] = g["users"][1]
    assert c.get(download).status_code == 200
    assert c.delete(download.removesuffix("/download")).status_code == 403
    g["state"]["user"] = g["users"][0]
    assert c.delete(download.removesuffix("/download")).status_code == 200
    assert c.get(download).status_code == 404
    assert not [p for p in g["storage"].rglob("*") if p.is_file()]
    assert g["db"].query(CaseChange).filter_by(action="删除附件").count() == 1


def test_recycle_restore_purge_preserves_versions_and_blocks_cross_project(features):
    g = features
    c, base, case = g["client"], g["features"], g["cases"][0]
    assert c.delete(f"/api/v1/test-cases/{case.id}").status_code == 200
    assert g["db"].get(Case, case.id).deleted_at is not None
    assert (
        c.get(
            f"/api/v1/test-cases/{case.id}", params={"project_id": g["project"].id}
        ).status_code
        == 404
    )
    assert (
        c.get("/api/v1/test-cases", params={"project_id": g["project"].id}).json()[
            "data"
        ]["total"]
        == 1
    )
    assert c.get(base + "/recycle-bin").json()["data"]["total"] == 1
    assert c.post(base + f"/cases/{g['foreign'].id}/restore").status_code == 404
    assert c.post(base + f"/cases/{case.id}/restore").status_code == 200
    assert g["db"].get(Case, case.id).deleted_at is None
    assert c.delete(base + f"/cases/{case.id}/purge").status_code == 404
    assert c.delete(f"/api/v1/test-cases/{case.id}").status_code == 200
    assert c.delete(base + f"/cases/{case.id}/purge").status_code == 200
    assert g["db"].get(Case, case.id) is None
    from models.case_governance import CaseVersion

    assert g["db"].query(CaseVersion).filter_by(case_id=case.id).count() == 1


def test_attachment_hidden_when_case_deleted_and_restored(features):
    g = features
    c, base, case = g["client"], g["features"], g["cases"][0]
    attachment = c.post(
        base + f"/cases/{case.id}/attachments",
        files={"file": ("证据.pdf", b"ok", "application/pdf")},
    ).json()["data"]
    url = base + f"/attachments/{attachment['id']}/download"
    c.delete(f"/api/v1/test-cases/{case.id}")
    assert c.get(url).status_code == 404
    c.post(base + f"/cases/{case.id}/restore")
    assert c.get(url).content == b"ok"


def test_purge_refuses_destroying_execution_history(features):
    from models.test_execution import TestExecution

    g = features
    case = g["cases"][0]
    g["db"].add(
        TestExecution(case_id=case.id, executor_id=g["users"][0].id, result="passed")
    )
    g["db"].commit()
    g["client"].delete(f"/api/v1/test-cases/{case.id}")
    assert (
        g["client"].delete(g["features"] + f"/cases/{case.id}/purge").status_code == 409
    )
    assert g["db"].query(TestExecution).filter_by(case_id=case.id).count() == 1


def test_default_template_custom_types_version_and_isolation(features):
    g = features
    c, base = g["client"], g["features"]
    body = {
        "name": "车载用例",
        "isDefault": True,
        "defaults": {"priority": "P1"},
        "fields": [
            {
                "key": "ecu",
                "name": "控制器",
                "type": "select",
                "options": ["ECU1", "ECU2"],
                "required": True,
            }
        ],
    }
    template = c.post(base + "/templates", json=body)
    assert template.status_code == 200, template.text
    template_id = template.json()["data"]["id"]
    payload = {
        "project_id": g["project"].id,
        "name": "默认模板用例",
        "type": "functional",
    }
    assert c.post("/api/v1/test-cases", json=payload).status_code == 422
    payload["custom_fields"] = {"ecu": "ECU1"}
    created = c.post("/api/v1/test-cases", json=payload)
    assert created.status_code == 200, created.text
    case = created.json()["data"]
    assert case["templateId"] == template_id and case["priority"] == "P1"
    assert (
        c.put(
            f"/api/v1/test-cases/{case['id']}",
            json={"custom_fields": {"ecu": "UNKNOWN"}},
        ).status_code
        == 422
    )
    assert (
        c.put(
            f"/api/v1/test-cases/{case['id']}", json={"custom_fields": {"ecu": "ECU2"}}
        ).status_code
        == 200
    )
    versions = c.get(g["base"] + f"/cases/{case['id']}/versions").json()["data"]
    assert versions[0]["snapshot"]["custom_fields"] == {"ecu": "ECU2"}
    assert c.delete(base + f"/templates/{template_id}").status_code == 409
    payload.update(project_id=g["foreign"].project_id, template_id=template_id)
    g["state"]["user"] = g["users"][3]
    assert c.post("/api/v1/test-cases", json=payload).status_code == 422


def test_requirement_defect_associations_and_dependency_cycles(features):
    g = features
    c, base = g["client"], g["features"]
    first, second = g["cases"]
    issue = c.post(
        base + "/issues", json={"kind": "defect", "title": "接口错误"}
    ).json()["data"]
    link = c.post(base + f"/cases/{first.id}/issues", json={"issueId": issue["id"]})
    assert link.status_code == 200, link.text
    assert (
        c.get(base + f"/cases/{first.id}/issues").json()["data"][0]["title"]
        == "接口错误"
    )
    assert c.delete(base + f"/issues/{issue['id']}").status_code == 409
    assert (
        c.post(
            base + f"/cases/{g['foreign'].id}/issues", json={"issueId": issue["id"]}
        ).status_code
        == 404
    )
    relation = c.post(
        base + f"/cases/{first.id}/relations",
        json={"targetCaseId": second.id, "kind": "postcondition"},
    )
    assert relation.status_code == 200, relation.text
    assert (
        c.get(base + f"/cases/{second.id}/relations").json()["data"][0]["kind"]
        == "precondition"
    )
    assert (
        c.post(
            base + f"/cases/{second.id}/relations",
            json={"targetCaseId": first.id, "kind": "postcondition"},
        ).status_code
        == 422
    )
    assert (
        c.post(
            base + f"/cases/{first.id}/relations",
            json={"targetCaseId": first.id, "kind": "related"},
        ).status_code
        == 422
    )


def test_member_follow_comment_and_automation_target_validation(features):
    g = features
    c, base, case = g["client"], g["features"], g["cases"][0]
    assert (
        c.post(
            base + f"/cases/{case.id}/automation",
            json={"category": "script", "targetCaseId": g["cases"][1].id},
        ).status_code
        == 422
    )
    c.put(f"/api/v1/test-cases/{g['cases'][1].id}", json={"is_automated": True})
    linked = c.post(
        base + f"/cases/{case.id}/automation",
        json={"category": "script", "targetCaseId": g["cases"][1].id},
    )
    assert linked.status_code == 200, linked.text
    assert (
        c.get(base + "/automation-targets").json()["data"]["cases"][0]["id"]
        == g["cases"][1].id
    )
    g["state"]["user"] = g["users"][1]
    assert c.post(base + f"/cases/{case.id}/follow").status_code == 200
    assert c.post(base + f"/cases/{case.id}/follow").status_code == 200
    assert c.get(base + f"/cases/{case.id}/follow").json()["data"] == {
        "followed": True,
        "count": 1,
    }
    comment = c.post(
        base + f"/cases/{case.id}/comments", json={"content": "补充边界"}
    ).json()["data"]
    g["state"]["user"] = g["users"][2]
    assert (
        c.delete(base + f"/cases/{case.id}/comments/{comment['id']}").status_code == 403
    )
    g["state"]["user"] = g["users"][1]
    assert (
        c.delete(base + f"/cases/{case.id}/comments/{comment['id']}").status_code == 200
    )
    assert c.get(base + f"/cases/{case.id}/comments").json()["data"] == []
