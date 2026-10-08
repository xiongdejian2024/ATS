# Independent defect workspace

The original blue ATS navigation includes **缺陷**. Select a project, filter the
20-row page by title/status/archive, and open a versioned detail. Plan instance and
aggregate details link to the same workspace using the retained issue/project IDs.

Owners, recorded project managers and existing system managers may manage defects.
Other users require independent `defect:read/create/update/delete` grants. Ordinary
case read/update and ordinary project membership do not substitute for defect
authority. The controller rechecks current actor/project authority within the
write transaction, including keyed retries and old case/plan association routes.
The migration registers permission definitions without granting them to anyone.

Templates provide up to 50 typed fields and defaults. The existing seven field
types are supported: text, textarea, number, boolean, date, select and multiselect.
Changing a used template refuses incompatible saved values; create a different
template instead. A used template cannot be removed. Selecting a new default
updates prior default revisions; the interface refreshes the actual catalog.

Descriptions explicitly distinguish plain and rich content. Existing literal HTML
remains plain until the user chooses rich conversion, which escapes the original
text. Rich descriptions/comments support structured mentions of currently
authorized project members. Notifications stay within the existing ATS inbox,
carry generic hints and recheck current source availability when opened.

Files use the existing project shared library. Published files remain visible to
authorized library readers; defect evidence is not a private attachment store.
Current edits and immutable history retain exact references and original bytes.
Archiving an issue/comment/file does not erase saved evidence. Existing archived
evidence may remain associated; new archived attachments are refused.

Every write uses an optimistic revision. Creation and comment submission use
bounded request keys; identical retries return their original receipt revision,
even after later edits. A failed or conflicting write preserves the draft. A
successful ACK records the submitted baseline and preserves text entered later.
Changing actor/project/identity or leaving the component fences old responses
and confirmations. List, comments and history are paged; file caches are limited
to the selected current description/comment files. Archive/restore is explicit;
no hard deletion of issue identity, associations or immutable events is added.

## Existing installations

Before updating the controller, preview the additive migration:

```bash
python scripts/upgrade_defect_workspace.py
```

After reviewing the preview against the operator's existing database, apply it:

```bash
python scripts/upgrade_defect_workspace.py --apply
```

SQLite, MySQL and PostgreSQL are supported. Four sidecars and four missing defect
permission definitions are added; prior CaseIssue IDs/content and queue rows are
retained. Existing incompatible sidecars are refused before mutation. The command
does not create users, grant permissions, rewrite reports, provision services or
delete data. No production database was migrated during this development.
Fresh PostgreSQL initialization uses the regenerated 96-model schema export.

Software checks and independent review are recorded in
[the completion matrix](ATS_COMPLETION_MATRIX.md). Controlled component tests do
not substitute for real browser, Windows, hardware or deployment acceptance.
