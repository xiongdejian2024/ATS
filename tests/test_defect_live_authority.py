import pytest, httpx
from conftest import isolated_database
from test_plan_orchestration import plan_lab
from test_plan_workspace import workspace_http
from test_defect_workspace_authority import create, grants
from database import SessionLocal
from models import (
    User,
    ProjectMember,
    Permission,
    ProjectPermission,
    TestCase as Case,
    TestPlan as Plan,
    PlanCaseRelation,
)
from models.case_features import CaseIssueLink
from services import defect_workspace as service, plan_case_workspace


@pytest.mark.asyncio
@pytest.mark.parametrize("route", ["mixed", "linked", "plan", "counts"])
async def test_current_manager_downgrade_hides_live_defects(workspace_http, route):
    from api.v1.case_features import router as features

    db, app, identity = workspace_http
    app.include_router(features, prefix="/features")
    owner, identifier = create(db)
    db.add(CaseIssueLink(issue_id=identifier, case_id="case-0", created_by="owner"))
    db.add(ProjectMember(project_id="project", user_id="stranger", role="manager"))
    db.commit()
    # Strong identity-map reference mirrors a row already loaded in the request.
    member = (
        db.query(ProjectMember)
        .filter_by(project_id="project", user_id="stranger")
        .one()
    )
    assert service.allows(db, db.get(User, "stranger"), "project", "read")
    with SessionLocal() as other:
        other.query(ProjectMember).filter_by(
            project_id="project", user_id="stranger"
        ).update({"role": "tester"})
        other.commit()
    assert member.role == "manager"
    identity["id"] = "stranger"
    paths = {
        "mixed": "/features/projects/project/case-features/issues",
        "linked": "/features/projects/project/case-features/cases/case-0/issues",
        "plan": "/orchestration/plans/plan/defects",
        "counts": "/orchestration/plans/plan/case-workspace",
    }
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(paths[route])
    if route == "plan":
        assert response.status_code == 403, response.text
    elif route == "counts":
        assert response.status_code == 200, response.text
        assert all(
            item["caseBugCount"] == 0 and item["bugCount"] == 0
            for item in response.json()["data"]["items"]
        ), response.text
    else:
        assert response.status_code == 200, response.text
        assert response.json()["data"] == [], response.text


@pytest.mark.asyncio
async def test_batch_case_update_revocation_is_checked_inside_defect_bridge(
    workspace_http, monkeypatch
):
    from services import case_selection
    from schemas.case_selection import CaseSelectionIssue

    db, app, identity = workspace_http
    owner, identifier = create(db)
    grants(db, "test_case:update", "defect:read")
    user = db.get(User, "stranger")
    original = service.require_associable

    def revoked(*args, **kwargs):
        with SessionLocal() as other:
            pid = other.query(Permission.id).filter_by(code="test_case:update").scalar()
            other.query(ProjectPermission).filter_by(
                project_id="project", user_id="stranger", permission_id=pid
            ).delete()
            other.commit()
        return original(*args, **kwargs)

    monkeypatch.setattr(service, "require_associable", revoked)
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as caught:
        case_selection.link_issue(
            db,
            user,
            "project",
            CaseSelectionIssue(caseIds=["case-0"], issueId=identifier),
        )
    assert caught.value.status_code == 403
    db.rollback()


@pytest.mark.asyncio
async def test_manual_execute_revocation_is_checked_before_freezing_live_defect(
    workspace_http, monkeypatch
):
    from services.plan_orchestration import start_plan_run

    db, app, identity = workspace_http
    owner, identifier = create(db)
    case = db.get(Case, "case-2")
    case.steps = [{"action": "手工", "expected": "结果"}]
    db.add(PlanCaseRelation(plan_id="plan", case_id="case-2"))
    db.commit()
    run = await start_plan_run(db, "plan", "owner")
    frozen = next(c for c in run.case_snapshot if c["id"] == "case-2")
    key = frozen.get("associationId", "case-2")
    grants(db, "test_plan:execute", "defect:read")
    identity["id"] = "stranger"
    original = service.authority

    def revoked(*args, **kwargs):
        with SessionLocal() as other:
            pid = (
                other.query(Permission.id).filter_by(code="test_plan:execute").scalar()
            )
            other.query(ProjectPermission).filter_by(
                project_id="project", user_id="stranger", permission_id=pid
            ).delete()
            other.commit()
        return original(*args, **kwargs)

    monkeypatch.setattr(service, "authority", revoked)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.put(
            f"/orchestration/runs/{run.id}/cases/{key}/result",
            json=dict(
                result="failed",
                stepResults=[dict(index=0, result="failed", defectIds=[identifier])],
            ),
        )
        assert response.status_code == 403, response.text


@pytest.mark.asyncio
async def test_legacy_plan_create_retains_current_original_modify_permissions(
    workspace_http, monkeypatch
):
    db, app, identity = workspace_http
    grants(db, "test_plan:update", "test_case:update", "defect:read", "defect:create")
    identity["id"] = "stranger"
    original = service.authority

    def revoked(*args, **kwargs):
        with SessionLocal() as other:
            pids = [
                x[0]
                for x in other.query(Permission.id).filter(
                    Permission.code.in_(["test_plan:update", "test_case:update"])
                )
            ]
            other.query(ProjectPermission).filter(
                ProjectPermission.project_id == "project",
                ProjectPermission.user_id == "stranger",
                ProjectPermission.permission_id.in_(pids),
            ).delete(synchronize_session=False)
            other.commit()
        return original(*args, **kwargs)

    monkeypatch.setattr(service, "authority", revoked)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/orchestration/plans/plan/defects",
            json=dict(caseId="case-0", title="旧入口"),
        )
        assert response.status_code == 403, response.text
