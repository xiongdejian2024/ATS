"""隔离 SQLite 的用例版本/评审/视图回归；不连接 Agent 或台架。"""

import uuid
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from database import SessionLocal, get_db
from api.deps import get_current_user
from api.v1.case_governance import router
from models import User, Project, ProjectMember, TestCase as Case
from models.case_governance import CaseVersion, CaseSavedView
from schemas.test_case import TestCaseCreate as CaseCreate, TestCaseUpdate as CaseUpdate
from services.test_case_service import TestCaseService


@pytest.fixture
def governance():
    db = SessionLocal()
    users = [
        User(
            id=str(uuid.uuid4()),
            username=f"评审用户{i}",
            email=f"case{i}@example.test",
            password_hash="未使用",
        )
        for i in range(4)
    ]
    db.add_all(users)
    db.flush()
    project = Project(
        id=str(uuid.uuid4()),
        name="软件验收项目",
        owner_id=users[0].id,
        created_by=users[0].id,
    )
    other = Project(id=str(uuid.uuid4()), name="隔离项目", owner_id=users[3].id)
    db.add_all([project, other])
    db.flush()
    db.add_all([ProjectMember(project_id=project.id, user_id=u.id) for u in users[1:3]])
    db.commit()
    cases = [
        TestCaseService.create_test_case(
            db,
            CaseCreate(
                project_id=project.id,
                name=f"用例{i}",
                type="functional",
                steps=[{"step": 1, "action": "打开", "expected": "可见"}],
            ),
            users[0].id,
        )
        for i in range(2)
    ]
    foreign = TestCaseService.create_test_case(
        db,
        CaseCreate(project_id=other.id, name="其他项目用例", type="functional"),
        users[3].id,
    )
    state = {"user": users[0]}
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    from api.v1.test_cases import router as cases_router
    from api.v1.projects import router as projects_router

    app.include_router(cases_router, prefix="/api/v1/test-cases")
    app.include_router(projects_router, prefix="/api/v1/projects")
    app.dependency_overrides[get_current_user] = lambda: state["user"]
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as client:
        yield dict(
            db=db,
            client=client,
            users=users,
            project=project,
            cases=cases,
            foreign=foreign,
            state=state,
            base=f"/api/v1/projects/{project.id}/case-governance",
        )
    db.rollback()
    db.close()


def request_review(g, reviewers=None, policy="all", cases=None):
    response = g["client"].post(
        g["base"] + "/reviews",
        json={
            "name": "版本评审",
            "caseIds": cases or [g["cases"][0].id],
            "reviewerIds": reviewers or [g["users"][1].id, g["users"][2].id],
            "policy": policy,
        },
    )
    assert response.status_code == 200, response.text
    return response.json()["data"]


def test_version_capture_compare_restore_and_stale_rejection(governance):
    g = governance
    client = g["client"]
    case = g["cases"][0]
    url = g["base"] + f"/cases/{case.id}"
    assert client.get(url + "/versions").json()["data"][0]["version"] == 1
    TestCaseService.update_test_case(
        g["db"],
        case.id,
        CaseUpdate(
            name="修改后", steps=[{"step": 1, "action": "新增", "expected": "成功"}]
        ),
        g["users"][0].id,
    )
    versions = client.get(url + "/versions").json()["data"]
    assert [v["version"] for v in versions] == [2, 1]
    changes = client.get(url + "/compare", params={"before": 1, "after": 2}).json()[
        "data"
    ]["changes"]
    assert {c["field"] for c in changes} == {"name", "steps"}
    restored = client.post(
        url + f"/versions/{versions[-1]['id']}/restore",
        json={"expectedVersion": 2, "reason": "撤销错误编辑"},
    )
    assert restored.status_code == 200, restored.text
    assert restored.json()["data"]["version"] == 3
    assert g["db"].get(Case, case.id).name == "用例0"
    stale = client.post(
        url + f"/versions/{versions[0]['id']}/restore",
        json={"expectedVersion": 2, "reason": "旧页面"},
    )
    assert stale.status_code == 409
    assert g["db"].query(CaseVersion).filter_by(case_id=case.id).count() == 3


def test_create_commit_false_is_atomic_and_noop_edit_not_new_version(governance):
    g = governance
    db = g["db"]
    case = TestCaseService.create_test_case(
        db,
        CaseCreate(project_id=g["project"].id, name="未提交", type="functional"),
        g["users"][0].id,
        commit=False,
    )
    identifier = case.id
    assert db.query(CaseVersion).filter_by(case_id=identifier).count() == 1
    db.rollback()
    assert db.get(Case, identifier) is None
    assert db.query(CaseVersion).filter_by(case_id=identifier).count() == 0
    case = g["cases"][0]
    TestCaseService.update_test_case(
        db, case.id, CaseUpdate(name=case.name), g["users"][0].id
    )
    assert db.query(CaseVersion).filter_by(case_id=case.id).count() == 1


def test_all_reviewers_and_immutable_snapshot(governance):
    g = governance
    review = request_review(g)
    item = review["items"][0]
    TestCaseService.update_test_case(
        g["db"], g["cases"][0].id, CaseUpdate(name="评审后编辑"), g["users"][0].id
    )
    fetched = g["client"].get(g["base"] + f"/reviews/{review['id']}").json()["data"]
    assert fetched["items"][0]["snapshot"]["name"] == "用例0"
    assert fetched["items"][0]["outdated"] is True
    vote_url = g["base"] + f"/reviews/{review['id']}/items/{item['id']}/decision"
    assert (
        g["client"]
        .post(vote_url, json={"decision": "approved", "comment": "未指定人员"})
        .status_code
        == 403
    )
    g["state"]["user"] = g["users"][1]
    first = g["client"].post(
        vote_url, json={"decision": "approved", "comment": "步骤完整"}
    )
    assert first.status_code == 200, first.text
    assert first.json()["data"]["status"] == "pending"
    assert (
        g["client"]
        .post(vote_url, json={"decision": "approved", "comment": "重复"})
        .status_code
        == 409
    )
    g["state"]["user"] = g["users"][2]
    second = g["client"].post(
        vote_url, json={"decision": "approved", "comment": "预期清楚"}
    )
    assert second.json()["data"]["status"] == "approved"


def test_any_policy_rejection_comments_and_cancel(governance):
    g = governance
    review = request_review(g, policy="any")
    g["state"]["user"] = g["users"][1]
    comment = g["client"].post(
        g["base"] + f"/reviews/{review['id']}/comments",
        json={"content": "建议补充边界条件"},
    )
    assert comment.json()["data"]["comments"][0]["content"] == "建议补充边界条件"
    vote = g["client"].post(
        g["base"]
        + f"/reviews/{review['id']}/items/{review['items'][0]['id']}/decision",
        json={"decision": "rejected", "comment": "缺少错误路径"},
    )
    assert vote.json()["data"]["status"] == "rejected"
    g["state"]["user"] = g["users"][0]
    review = request_review(g, policy="any")
    g["state"]["user"] = g["users"][1]
    vote = g["client"].post(
        g["base"]
        + f"/reviews/{review['id']}/items/{review['items'][0]['id']}/decision",
        json={"decision": "approved", "comment": "符合要求"},
    )
    assert vote.json()["data"]["status"] == "approved"
    g["state"]["user"] = g["users"][0]
    review = request_review(g)
    assert (
        g["client"]
        .post(g["base"] + f"/reviews/{review['id']}/cancel")
        .json()["data"]["status"]
        == "cancelled"
    )


def test_project_isolation_and_member_cannot_modify(governance):
    g = governance
    url = g["base"] + f"/cases/{g['foreign'].id}/versions"
    assert g["client"].get(url).status_code == 404
    body = {
        "name": "非法评审",
        "caseIds": [g["foreign"].id],
        "reviewerIds": [g["users"][0].id],
    }
    assert g["client"].post(g["base"] + "/reviews", json=body).status_code == 404
    body["caseIds"] = [g["cases"][0].id]
    body["reviewerIds"] = [g["users"][3].id]
    assert g["client"].post(g["base"] + "/reviews", json=body).status_code == 422
    g["state"]["user"] = g["users"][3]
    assert g["client"].get(g["base"] + "/reviews").status_code == 403
    g["state"]["user"] = g["users"][1]
    assert (
        g["client"]
        .post(
            g["base"] + "/batch", json={"caseIds": [g["cases"][0].id], "priority": "P0"}
        )
        .status_code
        == 403
    )


def test_private_views_persistence_and_validation(governance):
    g = governance
    client = g["client"]
    response = client.post(
        g["base"] + "/views",
        json={
            "name": "冒烟视图",
            "filters": {"search": "smoke", "moduleKeys": [], "filterConditions": []},
        },
    )
    assert response.status_code == 200, response.text
    identifier = response.json()["data"]["id"]
    g["db"].expire_all()
    assert (
        client.get(g["base"] + "/views").json()["data"][0]["filters"]["search"]
        == "smoke"
    )
    duplicate = client.post(
        g["base"] + "/views", json={"name": "冒烟视图", "filters": {}}
    )
    assert duplicate.status_code == 409
    assert (
        client.post(
            g["base"] + "/views",
            json={"name": "坏视图", "filters": {"script": "任意字段"}},
        ).status_code
        == 422
    )
    g["state"]["user"] = g["users"][1]
    assert client.get(g["base"] + "/views").json()["data"] == []
    assert client.delete(g["base"] + f"/views/{identifier}").status_code == 404
    g["state"]["user"] = g["users"][0]
    assert client.delete(g["base"] + f"/views/{identifier}").status_code == 200


def test_batch_atomic_invalid_case_and_record_versions(governance):
    g = governance
    db = g["db"]
    client = g["client"]
    response = client.post(
        g["base"] + "/batch",
        json={"caseIds": [g["cases"][0].id, g["foreign"].id], "priority": "P0"},
    )
    assert response.status_code == 404
    assert db.get(Case, g["cases"][0].id).priority == "P2"
    assert db.query(CaseVersion).filter_by(case_id=g["cases"][0].id).count() == 1
    response = client.post(
        g["base"] + "/batch",
        json={
            "caseIds": [c.id for c in g["cases"]],
            "priority": "P0",
            "isAutomated": True,
            "tags": ["冒烟"],
        },
    )
    assert response.json()["data"]["updated"] == 2
    for case in g["cases"]:
        assert db.get(Case, case.id).priority == "P0"
        assert db.get(Case, case.id).is_automated is True
        assert db.query(CaseVersion).filter_by(case_id=case.id).count() == 2


def test_snapshot_failure_rolls_back_original_case(governance, monkeypatch):
    from services import case_governance

    g = governance
    case = g["cases"][0]
    original = case_governance.snapshot_case

    def fail_changed(db, row, actor, reason, force=False):
        if row.name == "应回滚":
            raise RuntimeError("模拟快照写入失败")
        return original(db, row, actor, reason, force)

    monkeypatch.setattr(case_governance, "snapshot_case", fail_changed)
    with pytest.raises(RuntimeError):
        TestCaseService.update_test_case(
            g["db"], case.id, CaseUpdate(name="应回滚"), g["users"][0].id
        )
    assert g["db"].get(Case, case.id).name == "用例0"
    assert g["db"].query(CaseVersion).filter_by(case_id=case.id).count() == 1


def test_real_review_status_filter_and_existing_case_permissions(governance):
    g = governance
    review = request_review(g, reviewers=[g["users"][0].id])
    url = "/api/v1/test-cases"
    params = {"project_id": g["project"].id, "review_status": "pending"}
    listed = g["client"].get(url, params=params).json()["data"]
    assert listed["total"] == 1 and listed["items"][0]["reviewResult"] == "pending"
    voted = g["client"].post(
        g["base"]
        + f"/reviews/{review['id']}/items/{review['items'][0]['id']}/decision",
        json={"decision": "approved", "comment": "审阅通过"},
    )
    assert voted.status_code == 200
    params["review_status"] = "passed"
    assert g["client"].get(url, params=params).json()["data"]["total"] == 1
    g["client"].put(url + f"/{g['cases'][0].id}", json={"name": "再次修改"})
    assert g["client"].get(url, params=params).json()["data"]["total"] == 0
    params["review_status"] = "resubmit"
    assert g["client"].get(url, params=params).json()["data"]["total"] == 1
    g["state"]["user"] = g["users"][3]
    assert g["client"].get(url, params=params).status_code == 403
    assert (
        g["client"].put(url + f"/{g['cases'][0].id}", json={"name": "越权"}).status_code
        == 403
    )
    assert g["client"].delete(url + f"/{g['cases'][0].id}").status_code == 403


def test_incremental_import_keeps_omitted_cases_and_fields_and_versions(governance):
    from io import BytesIO
    import pandas as pd

    g = governance
    client = g["client"]
    db = g["db"]
    url = f"/api/v1/projects/{g['project'].id}/cases/import"

    def upload(rows, **params):
        stream = BytesIO()
        pd.DataFrame(rows).to_excel(stream, index=False)
        return client.post(
            url,
            params=params,
            files={
                "file": (
                    "cases.xlsx",
                    stream.getvalue(),
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            },
        )

    preview = upload([{"用例名称": "新增导入"}], validate_only=True)
    assert preview.json()["data"]["preview"]["to_delete"] == 0
    assert db.query(Case).filter_by(project_id=g["project"].id).count() == 2
    response = upload([{"用例名称": "新增导入"}])
    assert response.status_code == 200, response.text
    assert response.json()["data"]["deleted"] == 0
    assert db.query(Case).filter_by(project_id=g["project"].id).count() == 3
    added = db.query(Case).filter_by(name="新增导入").one()
    assert db.query(CaseVersion).filter_by(case_id=added.id).count() == 1
    original = g["cases"][0]
    response = upload([{"ID": original.case_code, "用例名称": "只改名称"}])
    assert response.json()["data"]["updated"] == 1
    assert db.get(Case, original.id).steps == [
        {"step": 1, "action": "打开", "expected": "可见"}
    ]
    assert db.query(CaseVersion).filter_by(case_id=original.id).count() == 2
    response = upload(
        [{"ID": original.case_code, "用例名称": "不覆盖"}], overwrite=False
    )
    assert response.json()["data"]["updated"] == 0
    assert db.get(Case, original.id).name == "只改名称"
    invalid = upload([{"ID": g["foreign"].case_code, "用例名称": "跨项目"}])
    assert invalid.json()["status"] == "error"
    assert db.query(Case).filter_by(project_id=g["project"].id).count() == 3
    g["state"]["user"] = g["users"][3]
    assert upload([{"用例名称": "越权导入"}]).status_code == 403


def test_batch_move_copy_and_preserved_review_after_case_delete(governance):
    from models.module import Module

    g = governance
    db, client = g["db"], g["client"]
    module = Module(id=str(uuid.uuid4()), project_id=g["project"].id, name="迁入模块")
    other = Module(
        id=str(uuid.uuid4()), project_id=g["foreign"].project_id, name="其他项目模块"
    )
    db.add_all([module, other])
    db.commit()
    case = g["cases"][0]
    response = client.post(
        g["base"] + "/batch", json={"caseIds": [case.id], "moduleId": other.id}
    )
    assert response.status_code == 422
    assert db.get(Case, case.id).module_id is None
    response = client.post(
        g["base"] + "/batch", json={"caseIds": [case.id], "moduleId": module.id}
    )
    assert response.status_code == 200, response.text
    assert db.get(Case, case.id).module_id == module.id
    assert db.query(CaseVersion).filter_by(case_id=case.id).count() == 2
    copied = client.post(
        g["base"] + "/batch-copy", json={"caseIds": [case.id], "moduleId": None}
    )
    assert copied.status_code == 200, copied.text
    copy = db.get(Case, copied.json()["data"]["caseIds"][0])
    assert (
        copy.module_id is None and copy.name == "用例0（副本）" and copy.id != case.id
    )
    assert db.query(CaseVersion).filter_by(case_id=copy.id).count() == 1
    review = request_review(g, reviewers=[g["users"][0].id])
    assert client.delete(f"/api/v1/test-cases/{case.id}").status_code == 200
    assert db.get(Case, case.id).deleted_at is not None
    assert TestCaseService.get_test_case(db, case.id) is None
    assert db.query(CaseVersion).filter_by(case_id=case.id).count() == 2
    preserved = client.get(g["base"] + f"/reviews/{review['id']}").json()["data"]
    assert preserved["items"][0]["snapshot"]["name"] == "用例0"
    assert preserved["items"][0]["outdated"] is True


def test_project_case_compatibility_routes_persist_and_reject_foreign_access(
    governance,
):
    g = governance
    client = g["client"]
    db = g["db"]
    prefix = f"/api/v1/projects/{g['project'].id}/cases"
    response = client.post(
        prefix,
        json={
            "project_id": g["project"].id,
            "name": "兼容入口新增",
            "type": "functional",
        },
    )
    assert response.status_code == 200, response.text
    case_id = response.json()["data"]["id"]
    assert db.get(Case, case_id).name == "兼容入口新增"
    assert db.query(CaseVersion).filter_by(case_id=case_id).count() == 1
    assert client.get(prefix).json()["data"]["total"] == 3
    response = client.put(prefix + f"/{case_id}", json={"name": "兼容入口修改"})
    assert response.status_code == 200, response.text
    assert client.get(prefix + f"/{case_id}").json()["data"]["name"] == "兼容入口修改"
    assert db.query(CaseVersion).filter_by(case_id=case_id).count() == 2
    assert client.get(prefix + f"/{g['foreign'].id}").status_code == 404
    g["state"]["user"] = g["users"][3]
    assert client.get(prefix).status_code == 403
    assert client.get(prefix + "/export").status_code == 403
    g["state"]["user"] = g["users"][0]
    assert client.delete(prefix + f"/{case_id}").status_code == 200
    assert db.get(Case, case_id).deleted_at is not None
    assert TestCaseService.get_test_case(db, case_id) is None
