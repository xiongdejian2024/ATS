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
| E01 / storage | Case disk attachments, DB execution images and immutable media references; explicit draft cleanup | Persistent local/database/explicit-S3 adapter implemented; shared file-library directory/picker missing; expired orphan inventory/safe archive pending. Permanent deletion requires separate authorization |
| E02 | `PlanFunctionalExecution.vue`: source-case editing and immutable independent histories. `plan_collaboration.py`: active batches already support steps/attachments/comments | Active frozen batch entrance implemented with duplicate-instance matching, paging and report draft protection; structured mentions missing; preserve ambiguity/409 safety |
| C01 | Case template/custom-field CRUD and validation, table settings and inline edits exist | Complete template interaction/custom-field columns/menu conditions pending development or comparison acceptance |
| C02 | Independent detail tabs, relationships/history and attachment upload/download exist | Rich comments and file-library links missing; full detail/table interaction acceptance open |
| C03 | `CaseMindMap.vue`: case copy/paste, module rename, name/precondition/steps editing | Text nodes, full module creation/cut/shortcuts missing; separate from F76–F78 |
| C04 | Actual Excel/CSV/XMind imports, validation/cover, two Excel layouts/XMind export and recycle lifecycle | XMind template, stepped import, field grouping/XMind field choice and full recycle filters missing |
| V01 | Review filter/paging, column settings/widths and cross-page association selection exist | Personal advanced views and association drawer advanced filter/display settings missing |
| V02 | `ReviewCaseTable.vue`: readonly current-page mind map; voting/re-review/history/rich reasons exist | Full review map and reason image upload/attachments/structured mentions missing (`ReviewResultForm` has no uploadImage) |
| P01 | Plan/group/module CRUD, basic filtering/copy/archive/execute exist | Personal views, expanded group rows and complete table/drawer conditions missing |
| P02 | Reports: real filtering/sort/rename/delete/PDF, metrics/category counts/details/summary/share exist | Personal views, configurable columns/cards and complete frozen-data analysis missing |
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
| E02 | Functional execution mentions, separate master detail and active-run association | Pending | Immutable history snapshots and active batch ownership remain distinct. Parts 73/75. |
| C01 | Case templates, custom fields and remaining table/menu conditions | Audit pending | Current fields, permissions, archived/recycled and cross-project cases; top matrix. |
| C02 | Case detail tabs, rich comments and file-library interactions | Audit pending | Real writes, attachment access and history; no placeholder controls. Top matrix. |
| C03 | Case mind-map module/text nodes, clipboard actions and shortcuts | Audit pending | Verify existing case editor before adding; no lost drafts or unintended duplicate records. Top matrix. |
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
