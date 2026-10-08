# ATS remaining implementation and acceptance matrix

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
