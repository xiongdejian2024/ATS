# ATS confirmed implementation and acceptance matrix

> Active scope corrected on 2026-10-08: the user confirmed that earlier unfinished business features remain in scope. Controller/Agent/scripts/logs have priority, followed by the finite historical rows below. Lower API-testing priority does not cancel previously confirmed work. Groovy is excluded. Blue ATS UI supersedes the old purple-theme entry in the historical reference. Do not infer an unlimited third-party feature roadmap.

## Current source audit (2026-10-08)

Baseline: main `ee7424ad5d61a4d6edc1a713d7edd7460d5641a1`; reviewed PostgreSQL candidate `36757100a45f0ff30bf049defaf5dfbf471c058d`. No `AGENTS.md` or `.agents/skills` exists in this checkout or its workspace parent. Existing source, workflow tests and the two recorded scope documents are the evidence; historical prose alone cannot close a row.

Status vocabulary: **implemented** means code exists, **pending development** identifies actual missing behavior, **pending acceptance** identifies missing runtime/interaction proof, **excluded** means explicitly outside scope, **external blocker** requires unavailable equipment/service/authority. A row may contain both implemented and pending portions.

| IDs | Source-verified implementation | Actual remainder / acceptance |
|---|---|---|
| F76–F78 | `FunctionalCaseMinder.vue`: multi-select one submission, full-folder server scope, enter/return/breadcrumb/minimap, case number/priority/instance defect counts | Pending browser acceptance; do not reimplement these features |
| R01–R03 | `suite_results.py`, `agent_connections.py`, `task_queue_service.py`, Agent outboxes: interrupted XAT results, bounded viewers, current-session fencing, shared atomic slots, permission recheck | Ordinary unknown execution now has audited closure with operator/stop confirmation/reason, immutable queue identity and late-result fencing; Windows process-tree and real platform acceptance open |
| R04 / logs | `agent_log_ingest.py`, spool, `raw_log_export.py`, browser bounded viewer: durable sequence ACK/replay, per-run quota, paged download | Global capacity/policy/safe copy-only gzip archival implemented; no automatic permanent deletion authorized |
| Script jobs | `script_jobs.py`, `ScriptJobs.vue`, `script_runtime.py`: standalone Python/Shell/argv, frozen runs, idempotent trigger retry, unknown manual closure | Browser and Windows acceptance open; no Groovy/DSL, Cron, auto-upgrade, untrusted-code sandbox or multi-controller scope |
| D01 | `plan_case_defects.py`, `PlanDefects.vue`: instance-specific create/bind/unbind, aggregate pagination and basic detail | Aggregate create/bind entry implemented with paged instance selection and draft protections; browser acceptance open |
| D02 | Existing defect state/entity/relations | Defect template/custom fields/files/mentions/distinct permissions and detail remain pending development; do not count case templates as defect templates |
| E01 / storage | Case disk attachments, DB execution images and immutable media references; explicit draft cleanup | Persistent local/database/explicit-S3 adapter implemented; shared file-library directories/picker, case/comment/review-event/execution references and expired-known-evidence inventory/copy archive now implemented. Browser acceptance and untracked external-object reconciliation pending. Permanent deletion requires separate authorization |
| E02 | `PlanFunctionalExecution.vue`: source-case editing and immutable independent histories. `plan_collaboration.py`: active batches already support steps/attachments/comments | Active frozen batch entrance implemented with duplicate-instance matching, paging and report draft protection; structured mentions and exact saved-content notification sources implemented; browser acceptance pending; preserve ambiguity/409 safety |
| C01 | Case template/custom-field CRUD and validation, table settings and inline edits exist | Dynamic custom-field columns now use stable field keys, safe typed values and existing table settings; preferences survive late metadata and temporarily unavailable fields. Template/menu interaction comparison acceptance remains open |
| C02 | Independent detail tabs, relationships/history and attachment upload/download exist | Rich comments, structured mentions and file-library links implemented with private drafts and scoped references; full detail/table interaction acceptance open |
| C03 | `CaseMindMap.vue`: module hierarchy, case/STEP/TEXT nodes and editing | TEXT description/expected rich content, module sibling/child creation, original-ID case/module cut-move, case content copy, deletion confirmation, priority/detail entrance and Ctrl/Cmd+C/X/V, Delete/Enter/Escape now implemented with persistence acknowledgements and draft guards. Real browser/blue-UI interaction acceptance remains open; a whole-module-subtree copying policy was not confirmed |
| C04 | Actual Excel/CSV/XMind imports, validation/cover, two Excel layouts/XMind export and recycle lifecycle | XMind template, three-step import confirmation, grouped field selection, per-node XMind masks, recycle advanced filters/sort/custom columns now implemented; browser acceptance remains open |
| V01 | Review filter/paging, column settings/widths and cross-page association selection exist | Personal advanced views and association drawer advanced filter/display settings missing |
| V02 | `ReviewCaseTable.vue` and review_case_workspace: readonly full filtered mind map (bounded at 10000); voting/re-review/history/rich reasons exist | Reason image upload/file attachments implemented with immutable event references; structured reason mentions implemented; full review map exists; browser/blue-UI comparison acceptance remains pending |
| P01 | Plan/group/module CRUD, basic filtering/copy/archive/execute exist | Personal advanced views and right-hand table group-member expansion missing; tree group members already expand. Other table/drawer interaction acceptance needs concrete comparison |
| P02 | Reports: real filtering/sort/rename/delete/PDF, metrics/category counts/details/summary/share exist | Personal views, configurable columns/cards and separate test-set defect analysis missing. Group and single-plan report summary refresh/navigation draft guards now exist; browser acceptance remains open |
| P03 | `plan_execution_config.py`: separate request environments and project node pools, inherited configuration, version checks/freeze/retry/failure-stop exist | Environment groups/cross-project mapping and independent resource-pool lifecycle missing |
| P04 | Three planning layouts, navigator/zoom/drag/fullscreen, transactional drafts and default-collection projection exist | Fine theme/default-collection interaction comparison and acceptance remain open; retain blue UI |
| A01–A02 | Extraction/variable assertions/request environments exist; standalone scripts belong to the reliable-script row | Persisted initial/environment variables, bounded SQL/global hooks/Mock/advanced reports stay lower priority; full Groovy/Java-expression compatibility excluded |
| Q01 | Existing permission and request-lifecycle protections | Verify every changed workflow’s errors, readonly states, retries, user/project isolation and narrow screens |

## External boundaries

- Deployment: Render card requirement declined; ClawCloud not selected; old Sites frontend lacks a backend connection. No new service, credential, paid resource or network/security change is authorized. Development continues independently.
- PostgreSQL candidate preserves the existing MySQL controller. Only the new first-admin bootstrap supports PostgreSQL/SQLite and deliberately refuses MySQL; migrations retain their individual dialect boundaries.
- Real browser, Windows process-tree, physical bench/driver/firmware and deployed-service acceptance must remain open until actually exercised. Software tests and CI are separate evidence.
- No real user data or secrets belong in test fixtures, repository reports, logs or notifications. Archive policies default off and copy evidence; they must not silently clear source logs or unacknowledged Agent spool.

The historical table below preserves original IDs and evidence. The audited table above corrects stale or overly broad statuses; later delivery records must name each changed subitem and its actual tests/commit/CI.

## Scope and evidence

This is a continuation of the existing ATS frontend, Python backend, Agent and XAT
project. It preserves the ATS identity, existing data contracts and offline test
boundary. It does not silently add the mobile app, microservice rewrite, cloud
infrastructure or analytics roadmap from the “后续规划” section of 需求文档.md.

The detailed UI/workflow backlog comes from the existing
[MS-V3逐项验收记录](MS-V3界面逐项复刻验收.md), particularly its current top-level
matrix and parts 72–75, together with [用例计划对齐记录](MS-V3用例计划对齐清单.md).
Earlier “implemented” category summaries are not evidence that every interaction
is complete. Each item must be checked against current code before implementation;
old omissions already resolved by later entries must not be recreated.

Published integration baseline: main at `f7fcb510e0227ab7eaa6dfd86fc3a823daac0f03`.
The three original feature/fix branch histories are retained. Merge tree equals
`97a81cb6ef2c4a368df4053462fb8ad58983b172`; 627 Python and 191 frontend tests,
type check and production build passed locally.

## Work and acceptance

| ID | Area and remaining outcome | Current state | Acceptance / evidence |
|---|---|---|---|
| F76 | Functional-plan mind map: multi-selection execution through one submit window | Implemented; automated checks/review passed, browser pending | Full server scope incl. unloaded >100 cases, duplicate-instance isolation, retry idempotence; zero Agent tasks. Part 75. |
| F77 | Enter/return to mind-map folders, breadcrumb navigation and minimap | Implemented; automated checks/review passed, browser pending | Ancestor navigation, cycle-safe path, actual viewport coordinates, drafts protected on leave. Part 75. |
| F78 | Mind-map case number, priority and per-instance defect indicators | Implemented; automated checks/review passed, browser pending | Repeated master case instances retain independent defect counts; no invented data. Part 75. |
| R01 | Timeout/cancel preserve finished results, complete/ACK before slot release | Done | INTERRUPTED_XAT_RESULTS.md; 30 added regression cases in 627-test baseline. |
| R02 | Slow log subscribers cannot stall Agent/result processing; reconnect recovers durable history | Implemented and independently tested; integration pending | Bounded per-client delivery, timeout/overflow isolation, ordered healthy stream, no cross-project log access. Parts 72/75. |
| R03 | Controller/Agent capacity, capability admission and concurrent dispatch | In development and independent review | Inspect existing queue protections before editing; simultaneous dispatch/cancel/reconnect, exact slot accounting. Part 75. |
| R04 | Large persistent logs, aggregation cost and remaining static-log routes | Audit pending | Complete stored output, bounded UI/API reads, no whole-file rewrite per chunk; retained historical routes. Part 72. |
| D01 | Aggregate defect page create/associate entry and detail workflow | Pending | Existing per-instance links and independent repeated instances remain correct. Part 75. |
| D02 | Defect template/custom fields, files/mentions and distinct defect permissions | Pending scope decomposition | Map current CaseIssue capabilities to recorded requirements; no new external notification recipient assumed. Part 75. |
| E01 | Functional execution file-library association and expired orphan-image cleanup | Pending | Referenced media never deleted; preview/submit/cancel/retry and crash-refresh leftovers covered. Parts 19–22, 73. |
| E02 | Functional execution mentions, separate master detail and active-run association | Implemented; browser acceptance pending | Immutable history snapshots and active batch ownership remain distinct. Parts 73/75. |
| C01 | Case templates, custom fields and remaining table/menu conditions | Software implemented; exact-commit CI and browser acceptance pending | Current fields, permissions, archived/recycled and cross-project cases; top matrix. |
| C02 | Case detail tabs, rich comments and file-library interactions | Audit pending | Real writes, attachment access and history; no placeholder controls. Top matrix. |
| C03 | Case mind-map module/text nodes, clipboard actions and shortcuts | Merged with exact-commit CI passed; browser acceptance pending | Case copy creates new identities; case/module cut moves original identities. Synchronous operation fences, draft guards and per-scope clipboard. Unconfirmed create results require refreshing and verifying before retry, rather than claiming create idempotency. |
| C04 | Import/export step UI, templates, field groups and recycle-bin interaction | Audit pending | Actual Excel/XMind round trip, scope/exclusion exactness, recoverable deletion boundaries. Top matrix. |
| V01 | Review advanced personal views and association-window display settings | Pending | Current review permissions/archiving/selection/re-review continue to pass. Parts 38–39 + top matrix. |
| V02 | Review full mind-map and image/mention/attachment reasons | Pending | Independent effective votes/history, no stale draft sharing, linked-file access controls. Top matrix. |
| P01 | Plan home views, table expansion/operations and create/edit drawer details | Audit pending | Check existing plan/group management, not reimplement working workflows. Top matrix. |
| P02 | Plan report personal views, columns, configuration cards and analysis | Pending | Accurate frozen report data and scoped export/share; top matrix. |
| P03 | Project environment groups, cross-project mapping and resource-pool management | Pending scope decomposition | Existing Agent nodes are not equivalent to the full recorded environment model. Part 56. |
| P04 | Remaining planning-map themes/default-collection projection | Audit pending | Existing layouts, draft transactions, APIs and selection preserved. Parts 61–64. |
| A01 | Advanced HTTP environment/initial variables and full expression compatibility | Deferred priority, not declared done | Existing extraction/variable assertion scope stays isolated; part 71 and priority note in part 72. |
| A02 | Scripts/SQL/global hooks/Mock and advanced HTTP reports | Deferred priority; requires bounded design | No arbitrary production execution, credentials or external sharing implied. Parts 55/71. |
| Q01 | Common permissions, empty/error/read-only states and narrow-screen interaction | Continuous verification | Apply to each changed workflow, include repeated/interrupted actions and Back/Forward. |

## Environment-dependent verification and exclusions

- Real vehicle/bench hardware, driver ABI, device locking and firmware flashing
  require their actual hardware and separate execution authority. Offline success
  cannot close these checks. Preserve explicitly unsupported/archived legacy paths
  rather than fabricating success (XAT功能迁移.md).
- Production MySQL/Redis/Celery changes are not part of this cloud pass. Isolated
  database tests may be added when dependencies are available; SQLite does not
  prove MySQL concurrent locking behavior.
- Real model-provider calls, billing or external notifications are not activated.
  Existing synthetic HTTP protocol checks remain the accepted local validation.
- Interactive browser validation remains open: the dot cloud browser currently
  blocks the local test URL with ERR_BLOCKED_BY_CLIENT, while launching an extra
  Chromium process inside the command sandbox fails at socket permissions. No
  access restriction is bypassed and no user-computer route is substituted.
  Unit/API/type/build results are reported separately from browser verification.

This matrix is a live implementation record, not a claim that the whole product
is complete. Close rows only with concrete implementation and applicable tests;
record actual blockers rather than redefining the requested completion goal.

## First functional mind-map increment

Changed behavior has passed 202 frontend unit tests, strict type checking and a production build; five focused backend tests include a 102-instance overlapping-folder union and idempotent replay. Independent review reproduced and fixed a stale preview after awaited cleanup/navigation and added result-only draft protection. The broader backend run passed all628 tests after a test-boundary SQLite pool isolation fix. The two initial reflection failures were reproduced in both independent worktrees and traced to per-connection stale SQLite schema state after DROP/recreate; production behavior and negative schema validators were unchanged. Interactive browser validation remains blocked as described above, so this increment is not a whole-product completion claim.

## Integrated mind-map and log candidate

After combining the independently reviewed mind-map and log-stream changes,
all **655 Python tests** and **218 frontend tests**, strict type checking and the
production build passed together in the dot cloud workspace. The pool-isolation
fix is limited to test teardown. No interactive browser, production database or
hardware acceptance is implied. Node capacity, aggregate defect actions and the
remaining rows continue as separate increments.


## Cloud goal continuation, 2026-10-08

- Published `8bf7570`: PostgreSQL UUID/VARCHAR user-service compatibility, restored finite historical scope, log capacity and copy-only archival. Its GitHub software-check run `37791007193` succeeded.
- Published `aabd9e6`: ordinary unknown-suite delivery audit/closure, shared-lock late-message fencing and durable attachments. Baseline plus changes: 1059 Python tests passed and 6 optional environment tests skipped locally. CI PostgreSQL found an invalid synthetic foreign-key fixture (`different-owner` had no User); the subsequent increment creates that synthetic principal instead of weakening the constraint. This CI failure is not counted as acceptance.
- Next business increment: aggregate defect create/bind by exact plan instance; independent execution links to a selected active frozen batch; result/comment/summary drafts persist through independent successful actions. Pending writes block switching, stale collaboration/share responses are ignored, and native refresh has a beforeunload handler.
- Frontend 292 tests passed, including custom-renderer report tests with deferred promises. They prove field baselines/response isolation, not actual browser Router/DOM/inert/refresh behavior. Related backend API tests verify exact frozen duplicates, legacy fallback, paging, execute-only permissions, archive and outsiders. Blue UI is preserved.
- Remaining code backlog remains the explicit D02, shared-library/orphan inventory/mentions, C01–C04, V01–V02, P01–P04 and bounded lower-priority A01–A02 subitems in the audited table. This record does not close the whole-product goal.


PR #1 merged to main as `23eb4baa0949cadbf9b17c279bef39d6ff1092f5`; exact-head main CI `37797500891` succeeded. Candidate, push and PR regression suites are green. No deployment acceptance is implied.

## Shared evidence increment (working branch)

Shared project folders, paged/cross-page file selection, explicit project publication, private image drafts, case file links, rich discussions, review reasons/files and independent execution descriptions are implemented. Bytes, digests and original reference identities stay stable; removing a case link only deactivates its current display. Archived files remain accessible to existing project-authorized history readers. Image previews require verified raster content and bounded decoding; credentials only go to exact local preview routes.

`evidence_capacity.py` inventories expired known evidence without references (including old plan-image rows); inactive historical references still prevent orphan classification. Explicit enabled copying writes bounded atomic gzip JSONL archives and never deletes source records/files. Unknown external objects are not listed or reconciled: an uncertain external commit may still need operator inventory; no external access is requested.

Independent frontend/backend reviews passed after mixed-reference lock ordering, MySQL current-read directory validation and draft-navigation corrections. Frontend 298 tests and production build passed; library/archive incremental tests include cross-project/private-draft rejection, rollback, immutable vote events, archived idempotent execution replay, corrupted digest rejection, quota and disk failure. Disposable PostgreSQL concurrency is a separate CI-only test. Real browser remains pending, as do full review-map browser acceptance and the other explicitly retained business rows. Structured mentions are recorded below.

Full isolated backend suite completed: **1070 passed, 6 skipped** (511.81 seconds). Later bounded-download/archive and additional library regressions passed separately (**15 passed, 1 disposable-PostgreSQL skip**); frontend **298 passed**, current production build succeeded. Exact final GitHub CI remains required before this library increment is merged.


## Structured mentions delivery (2026-10-08)

Project member picker uses 20-row pages and literal search; rich-text mentions keep stable user IDs, with at most 20 recipients. Submission rechecks current enabled identities and project membership, canonicalizes/escapes labels and rejects malformed or noncanonical IDs. Case discussion, immutable review events (including suggestions/batch votes), independent execution descriptions and frozen-run comments use the same validation. Batch operations send at most one notification per recipient. Execution request digests remain based on submitted input; accepted retries preserve history and do not notify again after a recipient changes.

Notifications contain a generic hint and entity ID, without comment excerpts or project names. The saved-content page rechecks current source permissions, including both plan/case read for independent execution and deleted-report visibility. Denied/cancelled navigation keeps notifications unread. Member selection blocks report writes and draft closing. PostgreSQL CI covers reciprocal mentions across projects and concurrent personal-view quota/mention transactions; identity reads use shared locks and quota writes use project locks/current reads.

Existing frozen-run comments remain plaintext, including literal angle brackets. New rich comments explicitly set `contentFormat=rich`. Existing deployments must preview then apply `python scripts/upgrade_run_comment_format.py --apply` before running the new controller; the additive column defaults to `plain`, preserves content, and is idempotent on SQLite/MySQL/PostgreSQL. Fresh PostgreSQL DDL is regenerated with the same 87 tables. This feature uses the existing notification table, adds no external message service, and sends no Slack/email messages during acceptance. Defect mentions remain D02 work, and full review-map browser acceptance remains V02. Real browser acceptance remains open.


## Use-case interchange and recycle completion (2026-10-08)

XMind templates download through the existing permissioned endpoint. Export groups apply the actual supported field mask to visible nodes, hidden ATS metadata and priority markers. Every imported XMind node retains its own provided-column set: mixed masks in one ZIP do not clear an omitted field, create a `nan` module, or overwrite unselected content. Excel/CSV layouts keep their existing compatibility. Import proceeds through file selection, read-only validation and an explicit final write; errors preserve the file, in-flight writes block closing, and project/user changes invalidate old responses.

Recycle advanced conditions reuse project-scoped case semantics, including AND/OR, dates, current-user members, attachments, requirements and template custom fields. Only deleted cases enter the result. Default unfiltered lists retain SQL count/LIMIT/OFFSET without review-history scans. Sorting and user/project-scoped display columns are available; same-tick scope changes retain the target scope's saved columns. Restore/purge operations capture their project and generation, block repeats and retain failed batch selections. Historical purge prohibitions remain unchanged; acceptance uses synthetic fixtures only.

Focused backend regression: **36 passed**. Full frontend suite: **315 passed**. Confirmation/export/recycle component tests exercise controlled async responses, not a real browser. Independent review found mixed-node field loss and same-tick column preference contamination; both have dedicated regressions and were corrected before publication. Independent re-review passed, strict type check and production build passed (32.24 seconds). Full local backend suite completed: **1092 passed, 11 skipped** (509.32 seconds); Exact-head push/PR CI **37808272271 / 37808319233 succeeded**, and PR #4 merged to main as `c72dd519c769e56ea6e85f9d4ba7acbd1cc66e7a`; the new main checks are still pending.

PR #3 merged to main as `4e64492b338ab26fed6fbafe51e2575439f3a407` after exact-head push/PR CI `37805960041` / `37805967356` succeeded. Its six-line process-test race correction preserves the live-child failure assertion and independently passed **22 tests**. Main CI `37807689113` succeeded.


## Plan-group summary protection (2026-10-08)

Group reports now protect summary drafts before refresh, child-report navigation, route changes and native unload. Save acknowledges only the immutable submitted summary snapshot. Sharing, revoking and downloading do not acknowledge unrelated summary drafts. Incoming server summaries update the known persisted baseline while retaining edited values; discarding after a successful save restores that accepted baseline. Pending operations block duplicate actions and navigation, capture run/project/user identity, and ignore stale responses. The independent report parent checks its child closing contract before clearing the component on refresh; forced identity changes clear old content without requiring an old identity's draft approval.

Tests use component state and an explicit parent-child closing contract, plus deferred synthetic responses. They do not claim browser DOM or real RouterView interaction acceptance. Independent review passed; full frontend suite **323 passed**, plus final clipboard scope regression (**9 focused tests passed**). Strict type checks and final production build passed (33.19 seconds); exact-commit checks remain required before merge. P02 personal views, configurable columns/cards and separate test-set defect analysis remain outstanding.


## Case mind-map module prerequisites (2026-10-08)

Source audit found unauthorised module create/delete endpoints and a create path accepting a foreign-project parent. Module write authority now reads the enabled actor with a shared lock, then current project permissions and the project lock; hierarchy rows use current reads. Parent/source project checks fence creation, movement and deletion. Existing cycle checks remain, and deleting a module promotes its child hierarchy at the correct levels while preserving use cases. The ORM parent relationship is updated together with IDs, preventing deletion from resetting promoted children to roots.

Old cross-project module or use-case references cause a `409` refusal with rollback; neither the source nor the external records is silently altered. Independent review reproduced both historical ORM side effects and verified the refusal. Local focused regressions: **18 passed, 1 disposable-PostgreSQL skip**. A real PostgreSQL reciprocal move test is added to the existing CI job and must pass there before concurrent acceptance. TEXT nodes and mind-map clipboard/module interaction remain C03 development, and no real user data or browser/hardware acceptance is touched by these synthetic tests.

The prerequisite commit `bcdad39d87757d0df41b466e8f5e6c6b97fb9875` passed both exact-head runs (`37812614480`, `37812734751`), including disposable PostgreSQL concurrency, and merged as `ceb66684c5015c0e7eb890db3d02b4de66f9e473`. Earlier group report and interchange main runs also completed successfully; each subsequent source change still needs its own checks.

## Case mind-map interaction completion (2026-10-08)

TEXT cases display/edit their actual rich description and expected-result fields and do not expose legacy hidden STEP content. Case copying preserves editable content and removes database/execution identities; cutting moves the original case or module. Module creation supports siblings/children, names, stable parent selection and backend project authority. Delete confirms recycling a case or preserving cases while promoting children when removing a module. Priority editing and detail navigation keep the original blue UI. Standard copy/cut/paste, Delete, Enter and Escape leave input and contenteditable keyboard behavior intact. No unconfirmed whole-module-subtree cloning behavior is added.

Node/modal/route/native-leave guards preserve drafts on cancellation and failed saves. A synchronous pending fence blocks duplicate requests and navigation; project/user generations reject late writes, reads and confirmations and clear old clipboards. Successful saves acknowledge submitted snapshots and canonical records. A failed list refresh cannot replace a successful PUT record with stale props; a confirmed later GET can replace it, including equal MySQL timestamps. Reactive case acknowledgements keep consecutive STEP edits/additions consistent without permanent stale caching. Pending-created records have no new idempotency guarantee: users are prompted to refresh and verify an uncertain result before retry.

Module renaming, moving and promotion refresh affected local case paths in the same transaction, flush pending ORM changes before current reads, preserve identity/history/review snapshots and retain existing outdated/resubmit semantics. Paths over the existing 500-character column bound return `422` with rollback. Case move/copy/create/update use complete nested target paths, and create derives the path from current module rows rather than trusting client path labels. Project locks precede module/FK writes; MySQL module ancestry uses locking current reads. No foreign-project records are rewritten. Focused backend tests: **23 passed, 1 local PostgreSQL skip**; frontend focused mapping/component/real-parent-state tests: **17 passed**. Full frontend: **337 passed**, production build passed (33.73 seconds). Independent review verified persistence failure/order boundaries and source scope; full backend and exact-final-head CI remain required. These state/controlled-response tests do not claim real browser, Windows or hardware acceptance.


C03 final source `ee982cb5a1935797032eb3e2b471e2ba914fb14e` passed push/PR CI `37816317328` / `37816368891`, including **1102 backend tests passed, 12 skipped**, PostgreSQL/MySQL concurrency, frontend and controller container checks. PR #7 merged as `53b36b3e9fd1de0a932f29a5cd15e6392c557177`; main run `37818399016` is pending at this record.

## Dynamic custom-field columns (2026-10-08)

Case lists now derive custom columns from the current project field catalog. Stable field keys separate labels from stored values; boolean false, zero, dates, multiple values and plain text render correctly. Columns remain optional and do not advertise unsupported server sorting. Existing display settings retain order, widths and visibility when metadata arrives late or a field is temporarily unavailable. Opening and closing the settings drawer preserves edited hidden-field preferences; a different actor/project reloads only its own settings. Malformed stored JSON can recover on the next save, while storage failures preserve the draft and report an error.

Final full frontend suite: **344 passed across 71 files**; production build and strict type checks passed (30.12 seconds). Focused helper/component/actual-parent state regressions: **9 passed**. Independent review also exercised shared-table compatibility and controlled late metadata/scope/error responses without finding a remaining blocker. These are component-state tests, not real browser acceptance; exact-final-head CI remains required before merge.
