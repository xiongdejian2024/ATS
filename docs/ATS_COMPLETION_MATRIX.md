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
| D02 | Versioned independent defect detail, typed templates/custom fields, file evidence, rich mentions, comments/history and distinct permissions implemented | Full local Python/frontend/build and independent reviews passed; exact-head push/PR and merged-main CI passed. Browser acceptance open; no outgoing notification service |
| E01 / storage | Case disk attachments, DB execution images and immutable media references; explicit draft cleanup | Persistent local/database/explicit-S3 adapter implemented; shared file-library directories/picker, case/comment/review-event/execution references and expired-known-evidence inventory/copy archive now implemented. Browser acceptance and untracked external-object reconciliation pending. Permanent deletion requires separate authorization |
| E02 | `PlanFunctionalExecution.vue`: source-case editing and immutable independent histories. `plan_collaboration.py`: active batches already support steps/attachments/comments | Active frozen batch entrance implemented with duplicate-instance matching, paging and report draft protection; structured mentions and exact saved-content notification sources implemented; browser acceptance pending; preserve ambiguity/409 safety |
| C01 | Case template/custom-field CRUD and validation, table settings and inline edits exist | Dynamic custom-field columns now use stable field keys, safe typed values and existing table settings; preferences survive late metadata and temporarily unavailable fields. Template/menu interaction comparison acceptance remains open |
| C02 | Independent detail tabs, relationships/history and attachment upload/download exist | Rich comments, structured mentions and file-library links implemented with private drafts and scoped references; full detail/table interaction acceptance open |
| C03 | `CaseMindMap.vue`: module hierarchy, case/STEP/TEXT nodes and editing | TEXT description/expected rich content, module sibling/child creation, original-ID case/module cut-move, case content copy, deletion confirmation, priority/detail entrance and Ctrl/Cmd+C/X/V, Delete/Enter/Escape now implemented with persistence acknowledgements and draft guards. Real browser/blue-UI interaction acceptance remains open; a whole-module-subtree copying policy was not confirmed |
| C04 | Actual Excel/CSV/XMind imports, validation/cover, two Excel layouts/XMind export and recycle lifecycle | XMind template, three-step import confirmation, grouped field selection, per-node XMind masks, recycle advanced filters/sort/custom columns now implemented; browser acceptance remains open |
| V01 | Review filter/paging, column settings/widths and cross-page association selection exist | Association drawer and review-home advanced AND/OR filters, private personal views and scoped display settings now implemented. Exact-final-head and merged-main CI passed; browser acceptance remains open |
| V02 | `ReviewCaseTable.vue` and review_case_workspace: readonly full filtered mind map (bounded at 10000); voting/re-review/history/rich reasons exist | Reason image upload/file attachments implemented with immutable event references; structured reason mentions implemented; full review map exists; browser/blue-UI comparison acceptance remains pending |
| P01 | Plan/group/module CRUD, basic filtering/copy/archive/execute exist | Personal advanced views and bounded on-demand right-hand group-member expansion merged with exact-final-head CI passed; merged-main CI passed; browser acceptance pending. Tree group members already expand; other table/drawer interaction acceptance needs concrete comparison |
| P02 | Reports: real filtering/sort/rename/delete/PDF, metrics/category counts/details/summary/share exist | Personal advanced views and configurable columns merged with exact-head and main CI passed. Configurable detail cards, frozen configuration and separate test-set/defect analysis merged with exact-head and main CI passed. Group and single-plan report summary refresh/navigation draft guards exist; browser acceptance remains open |
| P03 | Separate request environments and project node pools, inherited configuration/freeze/retry/failure-stop exist; project environment-group CRUD and cross-project mapping now implemented with current permissions, revisions, safe create retry and frozen execution | Environment-group exact-head and merged-main CI passed; browser acceptance pending. Independent Node resource-pool lifecycle merged with repaired exact-head and main CI passed |
| P04 | Three planning layouts, navigator/zoom/drag/fullscreen, transactional drafts and default-collection projection exist | Fine theme/default-collection interaction comparison and acceptance remain open; retain blue UI |
| A01–A02 | Extraction/variable assertions/request environments exist; standalone scripts belong to the reliable-script row | A01 variables merged with full local, exact-head and main CI passed. Bounded SQL/global/script hooks, Mock and measured reports implemented/reviewed; A02 final integrated/database/exact-head checks running; browser acceptance open. Full Groovy/Java-expression compatibility excluded |
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
| R02 | Slow log subscribers cannot stall Agent/result processing; reconnect recovers durable history | Implemented; automated checks and merged-main CI passed; browser pending | Bounded per-client delivery, timeout/overflow isolation, ordered healthy stream, no cross-project log access. Parts 72/75. |
| R03 | Controller/Agent capacity, capability admission and concurrent dispatch | Implemented/reviewed with actual PostgreSQL and merged-main CI passed; Windows/platform acceptance open | Inspect existing queue protections before editing; simultaneous dispatch/cancel/reconnect, exact slot accounting. Part 75. |
| R04 | Large persistent logs, aggregation cost and remaining static-log routes | Implemented with quotas, bounded reads, compression and copy-only archival; browser pending | Complete stored output, bounded UI/API reads, no whole-file rewrite per chunk; retained historical routes. Part 72. |
| D01 | Aggregate defect page create/associate entry and detail workflow | Implemented; full regression and merged-main CI passed; browser pending | Existing per-instance links and independent repeated instances remain correct. Part 75. |
| D02 | Defect template/custom fields, files/mentions and distinct defect permissions | Implemented; full regression, exact-head and merged-main CI passed; browser acceptance open | Existing CaseIssue identities retained; no external notification recipient or new service. [Workflow and migration](DEFECT_WORKSPACE.md). Part 75. |
| E01 | Functional execution file-library association and expired orphan-image cleanup | Implemented for known evidence with inventory/copy-only archival; current regression passed; browser/external-object inventory open | Referenced media never deleted; preview/submit/cancel/retry and crash-refresh leftovers covered. Parts 19–22, 73. |
| E02 | Functional execution mentions, separate master detail and active-run association | Implemented; browser acceptance pending | Immutable history snapshots and active batch ownership remain distinct. Parts 73/75. |
| C01 | Case templates, custom fields and remaining table/menu conditions | Merged with exact-commit CI passed; browser acceptance pending | Current fields, permissions, archived/recycled and cross-project cases; top matrix. |
| C02 | Case detail tabs, rich comments and file-library interactions | Implemented; regression and merged-main CI passed; browser pending | Real writes, attachment access and history; no placeholder controls. Top matrix. |
| C03 | Case mind-map module/text nodes, clipboard actions and shortcuts | Merged with exact-commit CI passed; browser acceptance pending | Case copy creates new identities; case/module cut moves original identities. Synchronous operation fences, draft guards and per-scope clipboard. Unconfirmed create results require refreshing and verifying before retry, rather than claiming create idempotency. |
| C04 | Import/export step UI, templates, field groups and recycle-bin interaction | Implemented/reviewed and merged-main CI passed; browser pending | Actual Excel/XMind round trip, scope/exclusion exactness, recoverable deletion boundaries. Top matrix. |
| V01 | Review advanced personal views and association-window display settings | Merged with exact-commit and main CI passed; browser acceptance pending | Current review permissions/archiving/selection/re-review continue to pass. Parts 38–39 + top matrix. |
| V02 | Review full mind-map and image/mention/attachment reasons | Implemented and automated checks passed; browser/blue-UI comparison pending | Independent effective votes/history, no stale draft sharing, linked-file access controls. Top matrix. |
| P01 | Plan home views, table expansion/operations and create/edit drawer details | Advanced personal views and group expansion merged with exact-head CI passed; browser acceptance pending | Check existing plan/group management, not reimplement working workflows. Top matrix. |
| P02 | Plan report personal views, columns, configuration cards and analysis | Personal views/columns merged with exact-head and main CI passed; detail cards/frozen configuration/test-set defect analysis merged with exact-head and main CI passed; browser acceptance pending | Accurate frozen report data and scoped export/share; top matrix. |
| P03 | Project environment groups, cross-project mapping and resource-pool management | Environment-group exact-head and main CI passed; browser acceptance pending. Independent Node pool lifecycle implemented/reviewed; exact-head and merged-main CI passed | Request targets and Agent execution pools remain separate; no new infrastructure provisioned. Part 56. |
| P04 | Remaining planning-map themes/default-collection projection | Implemented and automated checks passed; browser interaction pending | Existing layouts, draft transactions, APIs and selection preserved. Parts 61–64. |
| A01 | Literal environment/initial variables and existing ${name} expansion | Merged with full local and exact-head CI passed; main CI passed; browser acceptance open | [Limits, frozen scope and compatibility](NATIVE_INITIAL_VARIABLES.md). Full Groovy/Java-expression compatibility excluded. |
| A02 | Scripts/SQL/global hooks/Mock and advanced HTTP reports | Bounded implementation and independent reviews passed; final checks running; browser acceptance open | [Finite execution semantics and limits](NATIVE_PROCESSORS.md). Parts 55/71. |
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


C01 final commit `962a3c028368548d99b53b2dc887530ab5aee8ba` passed push/PR CI `37819500664` / `37819512093`; PR #8 merged as `716788711de79be009fc5e296450f3a371aecd72`. C03 main CI `37818399016` succeeded. The subsequent main run `37824403887` succeeded.

## Review association advanced views (2026-10-08)

Association candidates support current-project functional-case AND/OR conditions, custom fields and the current creator. Paged reads and all-result selection share the existing case-condition engine and exclude recycled/non-functional cases; advanced conditions supersede hidden basic filters. Association remains an explicit selection/confirmation and preserves existing review snapshots. Private personal views reuse the existing table in a fixed business namespace, with owner/project isolation, at most ten views and current enabled-actor/project authority for writes. No database table or external service is added.

The association table supports scoped persisted columns, widths and page size. Filter/name/settings drafts survive failed writes, canceled closing and storage errors. Pending operations block duplicate selection/submission. Project/actor/open generations and component-unmount fences reject old reads, writes and confirmation callbacks; an old deletion confirmation cannot issue a request after its component is removed. Optional shared filter guards preserve conditions on cancellation and acknowledge only successful view saves.

Focused backend: **11 passed** (candidate views and existing review workspaces); focused frontend: **8 passed** (actual component state with controlled responses). PostgreSQL CI explicitly includes the new candidate-view regressions and remains required before dialect acceptance. Review-home advanced personal views are still development work. These checks do not claim real browser/blue-UI interaction acceptance.

Final frontend suite: **352 passed across 74 files**, strict type checks and production build passed (32.17 seconds). Independent backend review additionally exercised unknown system fields and disabled/revoked actors retained by old sessions: all rejected without writes. Exact-head CI remains required before this association increment is merged.

PR #9 first commit `dd5c788c2f8bed0ff0e1cb4ebafed4cf78a0cb6a` is published. A follow-up preserves the mandatory current-creator scope when saving/reopening personal OR views; review-only types and strict boolean validation keep plan-view contracts compatible. Follow-up backend **12 passed**, focused frontend **9 passed**, full frontend **353 passed** and independent strict types passed. Earlier-head CI cannot qualify the follow-up source.


PR #9 follow-up source `eaf8e0824511668fc8c8170903214dcad259501a` is published; its push CI `37826795398` succeeded and PR CI `37826802101` also succeeded. The follow-up production build passed (36.21 seconds), with 353 frontend and 12 focused backend tests. Main `716788711de79be009fc5e296450f3a371aecd72` CI `37824403887` succeeded.

## Review-home advanced personal views (2026-10-08)

The review list supports finite typed AND/OR conditions for real review fields, including aggregate counts/pass rate, status, exact tags, creator/default or per-item reviewers, modules and dates. Count and paging use the same parameterized SQL query. Ordinary lists retain the default exclusion of archived reviews; explicit advanced lifecycle conditions can select archives. Current-creator/reviewer system scopes remain an independent mandatory constraint and are preserved by personal views. The fixed `review-index` namespace isolates home views from association and plan views; owner/project authority and per-namespace quota retain existing locks and transactions. Reads never mutate review snapshots/events.

Home views reuse the guarded filter editor and current member catalog. Advanced application clears hidden basic conditions; extra module navigation remains an explicit narrowing constraint. Canceled radio/detail/route transitions preserve filter drafts. Scope snapshots include a monotonically increasing generation, preventing project/actor/open round trips from acknowledging old writes, releasing current locks or closing fresh drafts. Page, association drawer and reusable view editor all enforce this boundary, including checks after awaited closing decisions and native unload draft guards.

Independent review reproduced and then closed three boundaries: old-write ACK after project/actor return, SQLite legacy period midnight precision and oversized integer driver errors. Legacy date predicates now use the same six-digit fraction as exact SQLite timestamps; numeric conditions outside the shared safe range return 422 before reading or saving. Focused permanent backend **28 passed**; independent backend tests including the original failing cases **34 passed**. Focused frontend **18 passed**, and independent original page reproductions **4 passed**. Final frontend **362 passed across 75 files**; strict types and production build passed (32.26 seconds). Exact-head PostgreSQL/MySQL/Agent/XAT CI remains required before merge. These controlled state/software checks do not close real browser, Windows or hardware acceptance.

The review-home increment and range-generation correction are added to the open PR #9 before merge. Earlier-head green checks do not qualify this broader final source; the PR title/body must describe both reviewed workflows.


PR #9 final source `ce0108284d398eddaa02982aea3d617fc47249cd` passed push/PR CI `37829146137` / `37829151261`, including **1121 backend tests passed, 12 skipped**, real PostgreSQL 17, MySQL migrations, frontend and controller container checks. Merged as main `aa34f6be361005ae7688e32fbf09d1d1dea5ccf7`; main CI `37831207790` remains pending at this record.

## Plan-home advanced views and group expansion (2026-10-08)

Plan lists now support finite typed AND/OR conditions for actual plan fields, exact tags, responsible user (including CURRENT_USER), effective group-module location, group, follow/archive state and dates. Project and navigation group/module scopes remain mandatory outer constraints. Count and paging share the same SQL query. Advanced overdue filtering and its response use the existing rule as a read-only projection; no GET writes occur on that advanced path, while old basic-list behavior remains compatible. Global sample-plan debug reads/logs were removed. Paging is bounded at 100 per API request.

Private personal views reuse the existing saved-view table under the fixed plan-index namespace with owner/project isolation, ten-view quota, enabled-actor and current project permission locks. They save only explicit visible conditions. A plan-authorized member directory avoids requiring case permissions to build the filter catalog. No creator field is fabricated from the responsible user, and no new database table or external resource is introduced.

The right-hand group table expands members on demand in twenty-row pages using the same current conditions plus the immutable selected group ID. At most ten expanded groups retain data; refresh/group metadata/scope/query changes invalidate cached and pending responses. Group/module navigation, view changes, route leave and same-component route updates honor filter/name/group drafts. Pending group inputs/closing are disabled; successful ACKs preserve any newer draft. Project/actor generations and operation ownership keep old ACKs, confirmations and finally blocks from modifying fresh data or unlocking newer writes.

Permanent focused backend **36 passed**, including existing plan and review compatibility; backend independent **27 passed** plus the new plan-only permission test. Frontend actual-parent/shared-editor/group tests **19 passed** and independent original reproductions **4 passed**. Independent reviews passed. Final full frontend, strict types/build, PostgreSQL CI and exact-head checks remain required. Real browser/blue-UI, Windows and hardware acceptance remains open.

Final P01 frontend validation: **381 passed across 78 files**, strict Vue/TypeScript checking and production build passed (30.19 seconds). `git diff --check` passed. Exact published head CI is still pending.


P01 source `bd2e650b20f1fe92a233a555851ff6cd79aaded5` passed push/PR CI `37832494585` / `37832533270`, including **1133 backend tests passed, 12 skipped**, PostgreSQL 17, MySQL migration, frontend and controller checks. PR #10 merged as `c00e46e5616739bf5a3447476652852b454182d8`; main run `37834536661` is pending at this record. V01 main run `37831207790` succeeded.

## Report-home personal views and configurable columns (2026-10-08)

Report lists use finite typed AND/OR conditions for actual union fields: report/plan names, kind, state, trigger, executor, pass rate and creation/completion dates. Current project and basic/navigation constraints remain mandatory outer predicates, with common count/paging SQL. Saved views use a fixed `report-index` namespace with private ownership, ten-view quota and current enabled-user/project read locks. No report history, frozen result or task is changed by these reads. SQLite legacy group creation times are projected from UTC to the existing Beijing-naive report contract without changing stored history; microseconds and exact date bounds are retained. Portable CASE null ordering preserves existing SQLite/MySQL behavior on PostgreSQL.

The original blue list supports scoped column visibility/order/widths and page size, including existing size 100. Storage errors retain setting drafts while ordinary same-size paging/sorting remains usable. Advanced views clear hidden basic filters. Inline renames acknowledge canonical server names without discarding newer drafts. Project/actor generations fence delayed reads, saves, deletion confirmations and PDF blobs; post-guard checks also close the microtask gap between an awaited leave decision and its caller. The same reproduced guard-tail issue is corrected in plan-home group/module navigation and deletion. Old P01 green CI does not qualify this follow-up.

Permanent backend report checks: **14 passed**. Combined own focused checks **21 passed**; independent backend checks **24 passed** including actual group writes/time windows, permission revocation, literal matching, union count/paging and absence of task/history writes. Frontend focused checks **41 passed**, full suite **401 passed across 80 files**. Independent frontend review passed original report reproductions **15/15**, plan confirmation-tail reproductions **16/16**, shared/page tests **40/40** and delayed download compatibility **2/2**. A strict build caught test-only return annotations; these were corrected and the affected three files passed **29 tests**. Final strict Vue/TypeScript checking and production build passed (29.47 seconds); exact-head CI remains required before merge. Real browser, Windows and hardware acceptance remain open. This increment does not close the still-missing report detail configuration cards, frozen execution configuration or separate test-set defect analysis.


P01 main CI `37834536661` succeeded. P02 report-home source `ea218caeb964f09500673e08f51e3d27ec66ffe6` passed push/PR CI `37835726919` / `37835770878`, including **1143 backend tests passed, 12 skipped** (707.10 seconds), PostgreSQL 17, MySQL migration, frontend and controller checks. PR #11 merged as `87bcd16a603370755f02c3893812620505de4af5`; main run `37838178814` is pending at this record.

## Report detail cards and frozen analysis (2026-10-08)

Plan and group reports provide configurable overview, execution-result analysis, test-set analysis, step-defect locations and frozen execution configuration cards. Personal card order/visibility is scoped by actor/project/report kind; overview stays visible. Failed persistence retains the draft, cancellation remains usable and stale project/actor/ABA/unmount confirmations cannot discard fresh settings. Existing case results, collaboration, summary, PDF/share and child-report entrances remain available. Analysis counts actual batch rows and does not substitute current-case results or current-defect state.

All new ordinary, native-range and configured-tree runs freeze actual test-set identity/name/path (including default test sets); legacy direct associations freeze their recorded collection before execution. Multi-case suites preserve a per-case set mapping. Older snapshots lacking the information explicitly show an unrecorded test set. Group analysis separates child-run identities, even when master case or set IDs repeat. Each defect occurrence retains its saved instance, execution, step, title and state; unique defects and location counts remain distinct. Frozen configuration projects explicit policy, retry, inheritance, request-environment/resource IDs and initial node membership; command/git/native request/authentication fields are absent from the new card projection. GET does not read current cases/sets/defects or enqueue tasks. Report enrichment now copies the frozen report object before adding derived fields.

Report refresh, child navigation and all single-plan write/read acknowledgements now enforce project/actor/run generations and post-guard scope checks. A delayed FileReader cannot submit after an actor change. Successful comments/results acknowledge only the submitted fields, preserving newer drafts. GET ACK preserves summary input entered during refresh; a successful summary save invalidates older reads so they cannot revert the confirmed baseline. This corrects reproduced boundaries without claiming real browser acceptance.

Permanent backend **52 passed** across report details, tree, configured execution, native range and group compatibility; last parent-type validation **5 passed**. Independent backend **56 passed** including the original missing ordinary default-set and frozen-object regressions. Final frontend focused **36 passed**, full frontend **423 passed across 82 files**. Independent frontend original reproductions **11/11** and repository focused **36/36** passed. Strict Vue/TypeScript and final production build passed (26.82 seconds). Exact-head CI remains required before merge. Browser/blue-UI, Windows and physical hardware acceptance remain open. No new external resource or database table is required.


## P03 delivery: request environment groups and cross-project targets

Project environment-group CRUD, per-source mappings, readonly controls, paged
listing and private drafts are implemented. Writes recheck current source/owner
permissions and enabled actors, require revisions, preserve errors, and freeze
response versions before commit. Stable creation request IDs prevent duplicate
create retries and never grant later revisions to stale creation drafts.

Plan, selected-suite and native-range execution resolve groups by actual case
source, fail atomically for missing mappings, and freeze requests/group revisions.
Selected suites reuse collection inheritance while preserving manual work and
excluding unselected suites. Unsupported generic commands or ambiguous templates
are rejected before dispatch; ordinary scripts retain their independent entry.
Reports display only the frozen group/target IDs and group revision.

Independent review exposed and verified fixes for MySQL RR reference reads,
post-commit response revisions, selected-suite configuration bypass, Vue source
selector proxy state, and late deletion notifications. Permanent API regressions:
**15 passed**; configuration/native-range/orchestration combination **62 passed**.
Schema/report compatibility combination **67 passed, 1 optional MySQL skip**.
Frontend **437 passed in 83 files**, focused environment/tag/tree **24 passed**;
strict production build passed (27.52 seconds). These are local software checks,
not real-browser/Windows/hardware/deployed acceptance.

CI now includes actual PG environment-group regressions and disposable MySQL
repeatable-read interleaving/migration tests. Exact-head CI remains pending at this
record. The additive two-table upgrade defaults to preview; no existing deployment
database was changed. Fresh PostgreSQL export contains 89 model tables.

P02 report-home main CI `37838178814` succeeded. Report detail first CI
`37839053368` / `37839095988` exposed two pre-existing native-case test fixture FK
ordering errors after adding those tests to PG coverage. Fix source
`c4bda08fff4e2448efc86951d07592299f0e73a7` persists parent cases before native
configs; exact runs `37841011888` / `37841018696` are pending here. Local two-case
regressions passed. No failed candidate was merged.

Independent/global resource-pool lifecycle remains the next P03 development item;
this environment-group delivery does not close that separate scope.


## 2026-10-08 report details, environment groups and independent pools

- PR12 final `c4bda08fff4e2448efc86951d07592299f0e73a7`: exact runs
  37841011888/37841018696 passed; merged main `b4f32bfb917b8d36cfd0292a83ef12585f0d1b21`,
  run 37843038651 passed. The initial failure was synthetic PostgreSQL FK fixture
  insertion order; explicit parent flush repaired it before merge.
- PR13 final `d8ca351da562cb8d6ca6098a96d475578c272894`: exact runs
  37843674211/37843684209 passed, including actual MySQL8 group migration and
  production-remove RR interleaving. Merged main
  `d0dec0fc725db5e052bd801d4b5d176b578fca5a`, run 37845362743 passed.
  A stale real initializer's literal table count was replaced with complete
  registered-model count before merge.
- Independent/global pool implementation: [behavior and migration](GLOBAL_RESOURCE_POOLS.md).
  Local backend integration 141 passed, new authority tests promoted from
  independent audit; whole-plan, selected-suite and native-range targets frozen.
  Existing project pools retain compatibility. Final exact-head CI is pending
  publication; real browser acceptance remains open.
- Remaining independent development: D02 defect templates/custom fields/detail
  attachments/mentions/distinct permission; bounded A01/A02 variable, SQL/hook/Mock
  and report items. Do not stop merely because a delivery slice merged.


## D02 independent defect workspace, 2026-10-08

Existing CaseIssue IDs, case/plan associations and frozen report history remain
compatible. Four additive sidecars provide typed template fields/defaults, explicit
plain/rich description format, optimistic revisions, soft archive/restore, keyed
create/comment receipts and immutable history/file references. Structured defect
mentions use the existing in-app notification system and recheck current source
authority. Ordinary case access no longer substitutes for independent defect
read/write permission; owners/managers and explicit existing grants retain their
recorded authority. No actual grants or user data were changed.

The original blue interface now includes a project-scoped Defects entry, bounded
list/comment/history pagination, template management and full detail from plan
links. Submitted snapshots establish saved baselines while later drafts survive
ACKs; actor/project/identity/unmount changes fence old reads, writes and confirms.
Plain legacy descriptions remain literal until explicit conversion.

Local SQLite/schema/compatibility combination: **78 passed**. Actual loopback
PostgreSQL workflow/authority/mentions/legacy combination: **51 passed**. Additive
migration preview/apply/idempotence/legacy refusal: **2 passed**, optional actual
MySQL skipped locally and included in the dedicated CI service. Formal front
interaction **16 passed**, independent reviewer **9 passed**. Final full backend **1223 passed / 15 optional skips**, frontend **472 passed**,
type check and production build succeeded. Exact head `ffa2fd3f33ce07e364f7273b1796ec08861e0a7e`
push/PR CI **37850725934/37850778240 succeeded**; merged to main as
`5a9f5b2cfae7ada297b3e62658e692f296f2e1e0`. Merged-main CI **37852569067 succeeded**.
Real browser, Windows, hardware and production deployment remain open.

Independent pool candidate's PostgreSQL job initially timed out: its test kept
a catalog authority transaction open before deleting that grant on a second
connection. The test now ends the simulated read request first, leaving production
locking intact. Actual PostgreSQL pool regressions **27 passed in 24.14 seconds**;
repair source `0b0a45272a9f40f2b6ba4b544ad2c18954215da0` runs
37849235383/37849240554 succeeded; merged main `52bbfa1ea4d5aad4ef79d506aa4e51d15adedee8`
run **37850939141 succeeded**. A timeout is not counted as acceptance.

Remaining independent development is the finite bounded A01/A02 initial/environment
variable, SQL/hook/Mock and report work. Do not stop because a slice merged.

## A01 literal variables increment, 2026-10-08

Environment sidecar declarations and request/scenario initial values now have bounded
blue editors and frozen native execution. Scope is rebuilt per attempt; only extracted
results carry across requests. Old environment clients preserve omitted fields, current
actor/permission is checked after locks, and all four claim paths plus pool selection
require the actual current Agent capability. Variable-free messages are accepted by
the committed original strict schema; final wire is bounded to 12 MiB.

Local compatibility combination **196 passed**; actual disposable PostgreSQL **40
passed**, followed by current-authority/four-entrance/real-Agent combination **10 passed**.
Formal frontend workflow regression includes incomplete drafts, failed auxiliary reads,
actor/case ABA, unmount, later ACK edits and confirmation resumption fences. Final full
Python/frontend/build and exact published-head CI remain required before merging this
increment. Actual MySQL migration runs only on the dedicated synthetic CI service.
Browser, Windows, hardware and deployment acceptance remain open. The remaining A02
SQL/hooks/Mock/report definitions need the finite bounded implementation audit.

## A01 merge and bounded A02 implementation, 2026-10-08

A01 final full Python **1247 passed / 16 skipped**; frontend **490 tests / 87 files**,
type check and production build passed. Independent backend **32**, frontend **15**
passed; actual disposable PostgreSQL **40 + 10** passed. PR #16 final head
`e2f135c2620510f700685c3a6054bdfc57649700` push and PR software/XAT runs
37853389903, 37853389950, 37853429384 and 37853429467 all succeeded. It merged
to main `02511f4a6f34318a0f2f2f8972780015a4989a92`; main XAT run 37856636729
and software run 37856636819 both succeeded. D02 merged-main run
37852569067 succeeded.

A02 is the final independent development row of this finite confirmed scope.
[Its bounded definition](NATIVE_PROCESSORS.md) now has implemented frontend,
controller, Agent and XAT paths. Independent frontend **14** and backend/real-process
**19** tests passed; original Mock timeout, SQL allocation, log-backpressure deadline
and stale-node current-read defects were reproduced and repaired. Final formal full
checks, physical PostgreSQL/MySQL and published-head CI remain required before merge.
No real browser, Windows, hardware or deployment check is marked complete.

## Finite goal checklist at A02 publication

The current tables above distinguish implemented code from missing acceptance.
Historical increment paragraphs retain their publication-time pending states.
Confirmed independent code rows R01–R04, scripts, F76–F78, D01–D02, E01–E02,
C01–C04, V01–V02 and P01–P04 are implemented and remain covered by full regressions.
A01 merged-main software/XAT checks passed. A02 code and independent reviews are
complete; its final published-head and merged-main gates are tracked in PR #17.

A02 commits: backend `5353ff64dc884f8eb448481c294244e51ab11f65`, frontend
`d4539ca5b46dd6936b70c990fb29b9cf9a15ca21`. Initial full Python **1297 passed /
16 skipped** before final supplemental fixtures; final-source focused group **61
passed**, frontend **507 / 89 files**, final type check and build passed. Actual
disposable PostgreSQL **61** plus forced concurrent project/node lock interleaving
**1** passed; actual disposable MySQL RR stale-node authority regression **1** passed.
Both database cases are included in dedicated CI jobs. Final-source full Python
rerun and exact-head push/PR software/XAT runs 37857958965 / 37857958873 /
37857964702 / 37857964722 remain in progress at this publication record.

Remaining acceptance is external, not deferred independent implementation:

- Real browser/blue-UI route, DOM, keyboard, viewport and refresh interaction. A clean
  headless Chromium retry at 2026-10-08 23:13 UTC still aborted with the SUID sandbox
  helper configuration error. Component/type/build tests do not close this item.
- Real Windows process-tree/driver and physical XAT vehicle/bench tests, with actual
  hardware and separately authorized execution. Linux subprocess checks do not close it.
- Free public deployment and existing Sites frontend/backend integration. Render card
  binding was refused; ClawCloud is not selected. No new service, credential, permission
  or paid resource is requested. Development and local integration did not wait for it.
- Unknown external storage-object inventory needs an operator-provided inventory.
  Known retained evidence is inventoried/archived; referenced data is never deleted.

Groovy/full Java dialect, old 23-group API expansion, multi-controller operation,
auto-upgrade, new external notification/model-provider services and unconfirmed
whole-module subtree copying remain outside this finite scope. Existing source
branches and real data are preserved. Do not report the above external checks as done.

Final compatibility repair: extension admission additionally requires protocol 2;
all four direct protocol-1 entrance regressions passed (**18 independent**).
Script receipts check their original frozen node after a job retarget, not the
new target's ownership. After any conflict rollback they recheck node/project/job
authority; mutations and receipts refresh/SHARE-lock the enabled actor. Independent
cached-user reproduction and compatibility combination **41 passed**; formal SQLite
**42 passed**, actual PostgreSQL **42 passed / 1 legacy-dialect skip**. Earlier
expanded script PostgreSQL fixture failures were repaired by adding real referenced
User/Environment fixtures, without relaxing foreign keys. Legacy MySQL/SQLite
upgrade is not a PostgreSQL migration; exported PostgreSQL DDL/initializer tests
provide its separate schema coverage. The script checks are now in the PG CI job.

The second complete local Python run **1304 passed / 18 skipped** after final
processor/real-process fixtures; a final full run including this actor/receipt/
protocol repair is running. Frontend **507 passed / 89 files** and final type/build
checks remain green. Actual PostgreSQL protocol admission **17 passed**.
