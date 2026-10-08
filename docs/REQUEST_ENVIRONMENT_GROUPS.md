# Request environment groups

The **请求环境组** project page maps each source project to one of that source
project's native HTTP request environments. Execution selects the target by the
case's source project. This target is separate from the Agent node/resource pool
that runs the request. The existing blue ATS layout and project selector remain.

Project `test_plan:read` controls listing; `test_plan:update` controls saving;
`test_plan:delete` controls deletion. Every source directory and mapping requires
current `test_case:read` in that source project. Catalogs expose IDs/names, never
target addresses or environment parameters. Readonly actors can inspect saved
mappings without gaining write authority. A failed source-directory read preserves
the saved mapping instead of silently removing it.

Writes lock projects in a fixed order, recheck the enabled actor and current
permissions, validate every mapping before replacement, and require the expected
revision. A referenced group cannot be deleted. The reference check is a locking
current read, including under MySQL repeatable-read isolation. HTTP responses
freeze the write's own revision before commit expires its ORM instance.

The page sends a stable creation `requestId`. Retrying identical creation after
a lost response returns the same group and its original creation revision;
changed content under that ID is rejected. It never grants a later writer's
revision to the old creation draft. Save errors preserve the draft; pending writes,
dirty-close confirmations and late responses are fenced by actor/project identity.

Plan execution, selected test-suite execution, and category/test-set range
execution all freeze the resolved environment ID, group revision and native
requests in the new batch. Later mapping/environment changes do not retarget
existing batches or dispatches. Missing/inaccessible source mappings reject the
whole new batch before queueing. Selected suites with category configuration use
the real association's collection inheritance and preserve manual work; ambiguous
multi-template cases are rejected. Configured suite selection requires native
HTTP or a case-filterable XAT command. Ordinary scripts retain their independent
Python/Shell/argv script-job workflow.

Report configuration cards show the frozen group ID/revision and resolved
environment ID. They do not look up today's mapping or disclose target addresses.
The existing single-environment field remains backward compatible; environment
and environment-group selections are mutually exclusive.

## Existing database upgrade

The two added tables are `request_environment_groups` and
`request_environment_group_mappings`; fresh schema exports now contain 89 model
tables. An operator uses the existing ATS database configuration to preview:

```bash
python scripts/upgrade_request_environment_groups.py
```

After reviewing that preview, the explicitly chosen operator operation is:

```bash
python scripts/upgrade_request_environment_groups.py --apply
```

This creates only missing group/mapping tables, checks required parent tables,
refuses an incompatible existing group table, and preserves existing objects and
rows. It creates no database, users, credentials or services. No live deployment
database was changed during development.

## Acceptance boundary

Formal API/service regressions cover three execution entrances, cross-project
targets, immutable batches, current source access, revision conflicts, rollback,
keyed creation retry and additive migration. Frontend tests cover readonly state,
draft/error preservation, source-selector responses and actor/project changes.
CI includes actual PostgreSQL and a disposable MySQL RR interleaving in which a
new configuration commits while deletion waits for the project lock.

These tests do not close real browser, Windows, hardware or deployed-service
acceptance. Independent/global resource-pool lifecycle is a separate P03 item.
