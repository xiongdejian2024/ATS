"""Versioned defect workflow on synthetic data; no outgoing notifications/services."""

from copy import deepcopy
import pytest
from sqlalchemy import inspect, text
from models import Permission, ProjectPermission, Notification, ProjectMember
from models.case_features import CaseIssue
from models.defect_workspace import (
    DefectProfile,
    DefectTemplate,
    DefectComment,
    DefectEvent,
)
from test_file_library import library, upload, png
from test_case_features import features
from test_case_governance import governance


@pytest.fixture
def defects(library):
    from api.v1.defect_workspace import router
    from api.v1.mentions import router as members
    from api.v1.notifications import router as inbox

    g = library
    app = g["client"].app
    app.include_router(router, prefix="/api/v1")
    app.include_router(members, prefix="/api/v1")
    app.include_router(inbox, prefix="/api/v1/notifications")
    g["defects"] = f"/api/v1/projects/{g['project'].id}/defects"
    return g


def grant(g, user, actions):
    db = g["db"]
    for action in actions:
        code = "defect:" + action
        permission = db.query(Permission).filter_by(code=code).first()
        if not permission:
            permission = Permission(
                code=code, name=code, resource="defect", action=action
            )
            db.add(permission)
            db.flush()
        db.add(
            ProjectPermission(
                project_id=g["project"].id, user_id=user.id, permission_id=permission.id
            )
        )
    db.commit()


def create(g, **fields):
    response = g["client"].post(
        g["defects"],
        json={"title": "Synthetic defect", "requestId": "create", **fields},
    )
    assert response.status_code == 200, response.text
    return response.json()["data"]


def detail(g, identifier):
    response = g["client"].get(g["defects"] + "/" + identifier)
    assert response.status_code == 200, response.text
    return response.json()["data"]


def body(data, **fields):
    allowed = {
        "title",
        "description",
        "descriptionFormat",
        "status",
        "externalRef",
        "templateId",
        "customFields",
    }
    return {
        **{k: v for k, v in data.items() if k in allowed},
        "expectedRevision": data["revision"],
        "fileIds": [r["id"] for r in data["files"]],
        **fields,
    }


def test_crud_keyed_retry_version_archive_and_legacy_plain_identity(defects):
    g = defects
    c = g["client"]
    base = g["defects"]
    receipt = create(g)
    identifier = receipt["id"]
    original = detail(g, identifier)
    assert original["descriptionFormat"] == "plain" and original["revision"] == 1
    assert c.get(base).json()["data"]["total"] == 1
    assert (
        c.put(base + "/" + identifier, json=body(original, title="Later")).json()[
            "data"
        ]["revision"]
        == 2
    )
    assert create(g) == {**receipt, "replayed": True}
    assert (
        c.put(base + "/" + identifier, json=body(original, title="Stale")).status_code
        == 409
    )
    assert detail(g, identifier)["title"] == "Later"
    assert (
        c.post(base, json={"title": "Different", "requestId": "create"}).status_code
        == 409
    )
    assert (
        c.put(
            base + "/" + identifier + "/archive",
            json={"archived": True, "expectedRevision": 2},
        ).status_code
        == 200
    )
    assert (
        c.get(base).json()["data"]["total"] == 0
        and c.get(base, params={"archived": True}).json()["data"]["total"] == 1
    )
    assert (
        c.put(base + "/" + identifier, json=body(detail(g, identifier))).status_code
        == 409
    )
    assert (
        c.put(
            base + "/" + identifier + "/archive",
            json={"archived": False, "expectedRevision": 3},
        ).status_code
        == 200
    )
    assert g["db"].get(CaseIssue, identifier) is not None
    events = c.get(base + "/" + identifier + "/history").json()["data"]
    assert events["total"] == 4
    assert {e["revision"] for e in events["items"]} == {1, 2, 3, 4}
    assert (
        next(e for e in events["items"] if e["revision"] == 1)["detail"]["snapshot"][
            "title"
        ]
        == "Synthetic defect"
    )


def test_typed_templates_defaults_revisions_retention_and_atomic_invalid_values(
    defects,
):
    g = defects
    c = g["client"]
    base = g["defects"]
    template = {
        "name": "Typed",
        "isDefault": True,
        "fields": [
            {
                "key": "severity",
                "name": "Severity",
                "type": "select",
                "options": ["high", "low"],
                "required": True,
            },
            {"key": "count", "name": "Count", "type": "number", "default": 0},
            {"key": "flag", "name": "Flag", "type": "boolean", "default": False},
        ],
        "defaults": {"status": "in_progress", "description": "Template default"},
        "expectedRevision": 0,
    }
    saved = c.post(base + "/templates", json=template)
    assert saved.status_code == 200, saved.text
    t = saved.json()["data"]
    receipt = create(g, customFields={"severity": "high"})
    record = detail(g, receipt["id"])
    assert (
        record["templateId"] == t["id"]
        and record["status"] == "in_progress"
        and record["description"] == "Template default"
    )
    assert record["customFields"] == {"severity": "high", "count": 0, "flag": False}
    assert (
        c.put(
            base + "/" + record["id"],
            json=body(record, customFields={"severity": "high", "count": True}),
        ).status_code
        == 422
    )
    assert detail(g, record["id"])["revision"] == 1
    incompatible = {
        **template,
        "expectedRevision": 1,
        "fields": [
            {
                "key": "severity",
                "name": "Severity",
                "type": "select",
                "options": ["low"],
                "required": True,
            }
        ],
    }
    assert c.put(base + "/templates/" + t["id"], json=incompatible).status_code == 409
    assert (
        c.request(
            "DELETE", base + "/templates/" + t["id"], json={"expectedRevision": 1}
        ).status_code
        == 409
    )
    assert c.get(base + "/templates").json()["data"]["items"][0]["revision"] == 1
    legacy = c.put(
        g["features"] + "/issues/" + record["id"],
        json={
            "kind": "defect",
            "title": "Blind old dialog",
            "description": "Lost fields",
        },
    )
    assert (
        legacy.status_code == 409
        and detail(g, record["id"])["customFields"]["severity"] == "high"
    )


def test_independent_permissions_no_case_update_bypass_and_defect_only_files(defects):
    g = defects
    c = g["client"]
    base = g["defects"]
    identifier = create(g)["id"]
    member = g["users"][1]
    g["state"]["user"] = member
    assert (
        c.get(g["features"] + "/issues", params={"kind": "defect"}).status_code == 403
    )
    assert c.get(g["features"] + "/issues").json()["data"] == []
    assert c.get(base).status_code == 403
    grant(g, member, ["read"])
    assert c.get(base).status_code == 200
    assert not c.get(base).json()["data"]["canUpdate"]
    assert (
        c.put(
            base + "/" + identifier,
            json=body(detail(g, identifier), title="Not allowed"),
        ).status_code
        == 403
    )
    # A defect-only explicit project grant does not grant generic case access.
    outsider = g["users"][3]
    grant(g, outsider, ["read", "create", "update"])
    g["state"]["user"] = outsider
    assert (
        c.get(g["features"] + "/issues", params={"kind": "requirement"}).status_code
        == 403
    )
    item = upload(g)
    created = create(g, requestId="only-defect", fileIds=[item["id"]])
    d = detail(g, created["id"])
    assert d["files"][0]["id"] == item["id"]
    response = c.get(g["library"] + "/files/" + item["id"] + "/download")
    assert response.status_code == 200 and response.content == b"synthetic evidence"
    assert c.get(base + "/templates").status_code == 200
    assert (
        c.get(
            f"/api/v1/projects/{g['project'].id}/mention-members",
            params={"context": "defect"},
        ).status_code
        == 200
    )


def test_files_rich_mentions_exact_history_retry_and_revocation(defects):
    from test_mentions import token

    g = defects
    c = g["client"]
    base = g["defects"]
    recipient = g["users"][1]
    grant(g, recipient, ["read"])
    image = upload(g, "proof.png", png(), image=True)
    attachment = upload(g)
    content = "<p>" + token(recipient.id) + '</p><img src="' + image["src"] + '">'
    created = create(
        g, description=content, descriptionFormat="rich", fileIds=[attachment["id"]]
    )
    identifier = created["id"]
    d = detail(g, identifier)
    assert "forged label" not in d["description"] and {f["id"] for f in d["files"]} == {
        image["id"],
        attachment["id"],
    }
    event = g["db"].query(DefectEvent).one()
    notice = g["db"].query(Notification).one()
    assert notice.type == "mention_defect_event"
    assert (
        "Synthetic" not in notice.content and recipient.username not in notice.content
    )
    assert (
        create(
            g, description=content, descriptionFormat="rich", fileIds=[attachment["id"]]
        )["replayed"]
        and g["db"].query(Notification).count() == 1
    )
    comment = c.post(
        base + "/" + identifier + "/comments",
        json={
            "content": "<p>" + token(recipient.id) + "</p>",
            "fileIds": [attachment["id"]],
            "expectedRevision": 1,
            "requestId": "comment",
        },
    )
    assert comment.status_code == 200, comment.text
    receipt = comment.json()["data"]
    retry = c.post(
        base + "/" + identifier + "/comments",
        json={
            "content": "<p>" + token(recipient.id) + "</p>",
            "fileIds": [attachment["id"]],
            "expectedRevision": 999,
            "requestId": "comment",
        },
    ).json()["data"]
    assert retry["revision"] == receipt["revision"] == 2 and retry["replayed"]
    assert (
        g["db"].query(DefectComment).count() == 1
        and g["db"].query(Notification).count() == 2
    )
    g["state"]["user"] = recipient
    source = c.get("/api/v1/notifications/" + notice.id + "/source")
    assert source.status_code == 200, source.text
    assert source.json()["data"]["content"] == d["description"]
    g["db"].query(ProjectPermission).filter_by(
        project_id=g["project"].id, user_id=recipient.id
    ).delete()
    g["db"].commit()
    assert c.get("/api/v1/notifications/" + notice.id + "/source").status_code == 403
    g["state"]["user"] = g["users"][0]
    assert (
        c.request(
            "DELETE",
            base + "/" + identifier + "/comments/" + receipt["id"],
            json={"expectedRevision": 2},
        ).status_code
        == 200
    )
    assert c.get(base + "/" + identifier + "/comments").json()["data"]["total"] == 0
    assert g["db"].query(DefectComment).one().deleted
    assert c.get(base + "/" + identifier + "/history").json()["data"]["total"] == 3


def test_failed_file_and_recipient_checks_roll_back_all_defect_changes(defects):
    from test_mentions import token

    g = defects
    c = g["client"]
    base = g["defects"]
    file = upload(g)
    response = c.post(
        base,
        json={
            "title": "Atomic",
            "requestId": "failed",
            "fileIds": [file["id"], "missing"],
        },
    )
    assert response.status_code == 404, response.text
    assert (
        g["db"].query(CaseIssue).count()
        == g["db"].query(DefectEvent).count()
        == g["db"].query(DefectProfile).count()
        == 0
    )
    from models import LibraryFile

    assert not g["db"].get(LibraryFile, file["id"]).published
    assert (
        c.post(
            base,
            json={
                "title": "Atomic",
                "descriptionFormat": "rich",
                "description": token(g["users"][1].id),
                "requestId": "recipient",
            },
        ).status_code
        == 422
    )
    assert (
        g["db"].query(Notification).count() == 0
        and g["db"].query(CaseIssue).count() == 0
    )


def test_retained_archived_evidence_can_survive_other_field_edit(defects):
    g = defects
    file = upload(g)
    identifier = create(g, fileIds=[file["id"]])["id"]
    d = detail(g, identifier)
    assert (
        g["client"]
        .put(
            g["library"] + "/files/" + file["id"] + "/archive", json={"archived": True}
        )
        .status_code
        == 200
    )
    assert (
        g["client"]
        .put(g["defects"] + "/" + identifier, json=body(d, status="closed"))
        .status_code
        == 200
    )
    assert detail(g, identifier)["files"][0]["archived"]
    assert (
        g["client"]
        .post(g["defects"], json={"title": "New", "fileIds": [file["id"]]})
        .status_code
        == 409
    )
    history = (
        g["client"].get(g["defects"] + "/" + identifier + "/history").json()["data"]
    )
    assert all(e["files"][0]["id"] == file["id"] for e in history["items"])


@pytest.mark.parametrize(
    "invalid",
    [
        {"title": " "},
        {"expectedRevision": True},
        {"descriptionFormat": "html"},
        {"customFields": {"unknown": "value"}},
        {"status": "invented"},
        {"fileIds": ["duplicate", "duplicate"]},
        {"extra": True},
    ],
)
def test_strict_inputs_do_not_write(defects, invalid):
    response = defects["client"].post(
        defects["defects"], json={"title": "Strict", **invalid}
    )
    assert response.status_code == 422, response.text
    assert defects["db"].query(CaseIssue).count() == 0
