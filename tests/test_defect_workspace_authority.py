import pytest
from types import SimpleNamespace
from fastapi import HTTPException
from conftest import isolated_database
from test_plan_orchestration import plan_lab
from models import User
from models.defect_workspace import DefectComment, DefectProfile
from schemas.defect_workspace import (
    DefectWrite,
    DefectCommentWrite,
    DefectTemplateWrite,
)
from services import defect_workspace as service, mentions
from database import SessionLocal


def create(db):
    user = db.get(User, "owner")
    result = service.save(
        db, user, "project", DefectWrite(title="缺陷", requestId="create-1")
    )
    db.commit()
    return user, result["id"]


def test_comment_receipt_revision_is_frozen(plan_lab):
    db, _ = plan_lab
    user, identifier = create(db)
    payload = DefectCommentWrite(
        content="原评论", requestId="comment-1", expectedRevision=1
    )
    first = service.add_comment(db, user, "project", identifier, payload)
    db.commit()
    assert first["revision"] == 2
    service.save(
        db,
        user,
        "project",
        DefectWrite(title="后来修改", expectedRevision=2),
        identifier,
    )
    db.commit()
    retry = service.add_comment(
        db,
        user,
        "project",
        identifier,
        payload.model_copy(update={"expectedRevision": 3}),
    )
    db.commit()
    assert retry["revision"] == 2
    assert db.query(DefectComment).count() == 1


@pytest.mark.parametrize("unavailable", ["deleted", "archived"])
def test_notification_rechecks_availability_after_project_lock(
    plan_lab, monkeypatch, unavailable
):
    db, _ = plan_lab
    user, identifier = create(db)
    comment = service.add_comment(
        db,
        user,
        "project",
        identifier,
        DefectCommentWrite(content="原评论", requestId="comment-1", expectedRevision=1),
    )
    db.commit()
    # Exact source has loaded the old ordinary rows before entering authority().
    original = service.authority

    def change_before_lock(*args, **kwargs):
        with SessionLocal() as other:
            if unavailable == "deleted":
                other.get(DefectComment, comment["id"]).deleted = True
            else:
                other.get(DefectProfile, identifier).archived = True
            other.commit()
        return original(*args, **kwargs)

    monkeypatch.setattr(service, "authority", change_before_lock)
    notification = SimpleNamespace(
        type="mention_defect_comment", related_id=comment["id"], user_id="owner"
    )
    with pytest.raises(HTTPException) as caught:
        mentions.source(db, user, notification)
    assert caught.value.status_code == 404


def test_defect_number_overflow_is_422(plan_lab):
    db, _ = plan_lab
    user = db.get(User, "owner")
    template = service.save_template(
        db,
        user,
        "project",
        DefectTemplateWrite(
            name="数值模板", fields=[dict(key="n", name="数字", type="number")]
        ),
    )
    db.commit()
    with pytest.raises(HTTPException) as caught:
        service.save(
            db,
            user,
            "project",
            DefectWrite(
                title="数值", templateId=template["id"], customFields={"n": 10**1000}
            ),
        )
    assert caught.value.status_code == 422


from test_plan_workspace import workspace_http
from models import (
    Permission,
    ProjectPermission,
    ProjectMember,
    TestPlan as Plan,
    PlanCaseRelation,
)
from models.case_features import CaseIssueLink
from services import plan_case_defect
from schemas.plan_case_defect import PlanDefectCreate
from uuid import uuid4
import httpx


def grants(db, *codes):
    for code in codes:
        resource, action = code.split(":")
        permission = Permission(code=code, name=code, resource=resource, action=action)
        db.add(permission)
        db.flush()
        db.add(
            ProjectPermission(
                project_id="project", user_id="stranger", permission_id=permission.id
            )
        )
    db.add(ProjectMember(project_id="project", user_id="stranger", role="tester"))
    db.commit()


@pytest.mark.asyncio
async def test_aggregate_does_not_expose_defects_to_plain_member(workspace_http):
    db, app, identity = workspace_http
    user, identifier = create(db)
    db.add(CaseIssueLink(case_id="case-0", issue_id=identifier, created_by="owner"))
    db.add(ProjectMember(project_id="project", user_id="stranger", role="tester"))
    db.commit()
    identity["id"] = "stranger"
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(
            "/orchestration/plans/plan/case-workspace/defects/aggregate"
        )
        assert response.status_code == 403, response.text


def test_create_and_associate_requires_read_as_well_as_create(workspace_http):
    db, app, identity = workspace_http
    grants(db, "test_plan:execute", "defect:create")
    relation = (
        db.query(PlanCaseRelation).filter_by(plan_id="plan", case_id="case-0").one()
    )
    selection = PlanDefectCreate(
        selectIds=[f"legacy:{relation.id}:case-0"], requestId=uuid4(), title="新缺陷"
    )
    with pytest.raises(HTTPException) as caught:
        plan_case_defect.create(
            db, db.get(Plan, "plan"), db.get(User, "stranger"), selection
        )
    assert caught.value.status_code == 403
    db.rollback()


def test_disassociate_requires_read(workspace_http):
    from schemas.plan_case_defect import PlanDefectAssociate
    from models.plan_case_defect import PlanCaseDefect

    db, app, identity = workspace_http
    owner, identifier = create(db)
    relation = (
        db.query(PlanCaseRelation).filter_by(plan_id="plan", case_id="case-0").one()
    )
    selection = PlanDefectAssociate(
        selectIds=[f"legacy:{relation.id}:case-0"], issueIds=[identifier]
    )
    plan_case_defect.associate(db, db.get(Plan, "plan"), owner, selection)
    db.commit()
    link = db.query(PlanCaseDefect).one()
    grants(db, "test_plan:execute")
    with pytest.raises(HTTPException) as caught:
        plan_case_defect.disassociate(
            db, db.get(Plan, "plan"), db.get(User, "stranger"), link.id
        )
    assert caught.value.status_code == 403
    db.rollback()


def test_comment_delete_capability_matches_delete_grant(workspace_http):
    db, app, identity = workspace_http
    owner, identifier = create(db)
    added = service.add_comment(
        db,
        owner,
        "project",
        identifier,
        DefectCommentWrite(content="评论", requestId="comment", expectedRevision=1),
    )
    db.commit()
    grants(db, "defect:read", "defect:delete")
    user = db.get(User, "stranger")
    listed = service.comments(db, user, "project", identifier)
    assert listed["items"][0]["canDelete"] is True
    result = service.delete_comment(db, user, "project", identifier, added["id"], 2)
    assert result["revision"] == 3
    db.commit()


def test_frozen_evidence_is_retained_and_new_archived_attachment_rolls_back(plan_lab):
    from models.file_library import LibraryFile, LibraryReference
    from models.defect_workspace import DefectEvent

    db, _ = plan_lab
    user = db.get(User, "owner")
    fids = [str(uuid4()), str(uuid4())]
    for fid in fids:
        db.add(
            LibraryFile(
                id=fid,
                project_id="project",
                uploaded_by="owner",
                file_name=fid + ".txt",
                file_path="db:synthetic-" + fid,
                file_size=1,
                sha256="a" * 64,
                mime_type="application/octet-stream",
                published=False,
            )
        )
    db.commit()
    receipt = service.save(
        db,
        user,
        "project",
        DefectWrite(title="证据", fileIds=[fids[0]], requestId="evidence"),
    )
    db.commit()
    identifier = receipt["id"]
    service.save(
        db,
        user,
        "project",
        DefectWrite(title="证据更新", fileIds=[fids[1]], expectedRevision=1),
        identifier,
    )
    db.commit()
    for fid in fids:
        db.get(LibraryFile, fid).archived = True
    db.commit()
    service.save(
        db,
        user,
        "project",
        DefectWrite(title="保留已归档证据", fileIds=[fids[1]], expectedRevision=2),
        identifier,
    )
    db.commit()
    history = service.history(db, user, "project", identifier)["items"]
    initial = next(item for item in history if item["revision"] == 1)
    assert initial["detail"]["snapshot"]["title"] == "证据"
    assert [f["id"] for f in initial["files"]] == [fids[0]]
    count = db.query(DefectEvent).count()
    with pytest.raises(HTTPException) as caught:
        service.save(
            db,
            user,
            "project",
            DefectWrite(title="非法添加归档附件", fileIds=fids, expectedRevision=3),
            identifier,
        )
    assert caught.value.status_code == 409
    db.rollback()
    assert service.detail(db, user, "project", identifier)["title"] == "保留已归档证据"
    assert db.query(DefectEvent).count() == count
    assert (
        service.save(
            db,
            user,
            "project",
            DefectWrite(title="证据", fileIds=[fids[0]], requestId="evidence"),
        )["revision"]
        == 1
    )


def test_current_permission_revocation_blocks_keyed_retry(workspace_http):
    db, app, identity = workspace_http
    grants(db, "defect:create")
    user = db.get(User, "stranger")
    payload = DefectWrite(title="授权时创建", requestId="retry")
    first = service.save(db, user, "project", payload)
    db.commit()
    # Prime an ordinary permissions snapshot, then revoke in another session.
    assert service.allows(db, user, "project", "create")
    with SessionLocal() as other:
        pid = other.query(Permission.id).filter_by(code="defect:create").scalar()
        other.query(ProjectPermission).filter_by(
            project_id="project", user_id="stranger", permission_id=pid
        ).delete()
        other.commit()
    with pytest.raises(HTTPException) as caught:
        service.save(db, user, "project", payload)
    assert caught.value.status_code == 403
    db.rollback()


def test_disassociate_locks_all_source_projects_before_defect_target_authority(
    workspace_http, monkeypatch
):
    from models import Project, TestCase as Case
    from models.plan_workspace import PlanNode
    from models.plan_case_defect import PlanCaseDefect
    from services.plan_tree import save_node
    from sqlalchemy import event

    db, app, identity = workspace_http
    db.add(Project(id="a-source", name="来源", owner_id="owner"))
    db.flush()
    db.add(
        Case(
            id="foreign",
            project_id="a-source",
            name="来源用例",
            case_code="SRC",
            type="functional",
            steps=[],
            created_by="owner",
        )
    )
    db.flush()
    node = save_node(
        db,
        db.get(Plan, "plan"),
        dict(name="来源实例", nodeType="case", caseId="foreign"),
        source_project_id="a-source",
    )
    db.commit()
    owner, identifier = create(db)
    from schemas.plan_case_defect import PlanDefectAssociate

    plan_case_defect.associate(
        db,
        db.get(Plan, "plan"),
        owner,
        PlanDefectAssociate(
            selectIds=[f"node:{node.id}:foreign"], issueIds=[identifier]
        ),
    )
    db.commit()
    link = db.query(PlanCaseDefect).one()
    locks = []

    def locked(execute_state):
        statement = execute_state.statement
        if getattr(statement, "_for_update_arg", None) is not None and any(
            col.get("entity") is Project
            for col in getattr(statement, "column_descriptions", [])
        ):
            compiled = statement.compile()
            locks.append(compiled.params.get("id_1"))

    event.listen(db, "do_orm_execute", locked)
    try:
        plan_case_defect.disassociate(db, db.get(Plan, "plan"), owner, link.id)
    finally:
        event.remove(db, "do_orm_execute", locked)
    # A real cross-source write uses the same production resolver. Target-first
    # authority violates its sorted project locking order even on SQLite.
    assert locks[:2] == ["a-source", "project"], locks
