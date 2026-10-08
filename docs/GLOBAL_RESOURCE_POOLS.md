# Independent Node resource pools

The blue **独立资源池** page manages a shared set of existing ATS Agent nodes,
separately from the existing per-plan resource pools. This finite implementation
supports `Node` pools for API and scenario execution. It provisions no Agent,
Kubernetes service, cloud resource, organization or new execution language.

## Authority and lifecycle

Existing `system:manage` authority controls create, edit, enable/disable and delete.
A user with current plan-read access sees only pools applicable to their selected
project, with management controls disabled; other project scope identities and node
tokens/addresses are absent from those responses. Node candidates require system
management authority. Pool and node lists are server-paged and search escapes SQL
wildcards. Pool details report configured, online, running and currently available
capacity; overlapping pools share each node's actual task slots.

A pool has a name, description, enabled state, API/scenario applicability, either
all-project or explicit project scope, and 1–100 distinct existing enabled nodes.
Edits, enable changes and deletes require the saved revision. Keyed creation retries
acknowledge the original revision 1 receipt, rather than granting an old creation
draft permission to overwrite a later revision. Validation precedes relation writes;
failed writes retain the existing pool. There is no silent selection truncation.

Current project/actor/permission locks precede pool writes. Pool membership writes
lock the pool before its sorted nodes. Existing node deletion locks the node and
reads current pool references, returning 409 without deleting a referenced node,
even on SQLite installations without FK enforcement. Pool deletion checks current
execution configurations joined to surviving plans. It preserves frozen batches,
node records, historical orphan configurations and existing project pools.

## Execution and reporting

Execution configuration stores `testResourcePoolScope=global` and the pool ID.
Legacy configurations without the new scope remain `project`; `DEFAULT` belongs
to the project's normal execution configuration. API and scenario choices are
filtered by exact applicability. Current pool enablement, project/category scope
and enabled member nodes are checked before creating a batch.

Whole-plan, selected-suite and native-range execution all freeze the pool version
and ordered node members before committing a run. Dispatch, retries and historical
reports consume the frozen members. Later edits or disabling the pool affect new
batches, without rewriting existing batch targets. Reports expose only the safe
pool scope/ID/revision and frozen node IDs. Execution authority and configuration
update authority are rechecked after the project locks, including idempotent run
receipt reads; revocation after an API precheck cannot create unauthorized work.

The page guards drafts on navigation, retry and delete confirmations. Actor/project
changes, ABA changes and unmount invalidate late responses and confirmation
callbacks. Submitted save acknowledgements update their own baseline while
preserving any later draft. Candidate state is limited to the current 50-node page
and at most 100 selected nodes; selection enforces the limit immediately. Selected
nodes subsequently disabled remain removable, while new disabled/unknown nodes
cannot be selected.

## Additive migration

Fresh model registration and the PostgreSQL schema export contain **92 tables**.
Existing installations preview `scripts/upgrade_global_resource_pools.py` first;
`--apply` explicitly creates only the three missing pool tables. Parent tables and
existing pool columns are validated before creating objects. No existing table,
row, branch or database has been replaced by this implementation. Deployment and
production database changes were not performed.

The CI MySQL job applies this migration to its prior disposable synthetic legacy
fixture, checks preview/read-only behavior, idempotence, exact queue retention and
the actual member-to-node RESTRICT foreign key. PostgreSQL CI includes the new
HTTP authority, scope, migration and frozen execution regressions. Exact published
commit and merged-main CI results are recorded in the completion matrix when they
finish; SQLite checks alone do not prove MySQL runtime interleaving behavior.

## Acceptance evidence

Local focused backend integration: **141 passed**, covering pools, authority,
three execution entrances, configuration/groups, orchestration/native range,
report policy and PostgreSQL export/initialization. Independent audits reproduced
and verified the authority races, referenced-node deletion and deleted-plan
reference behavior. Frontend candidate/selection, drafts, retries, scope changes
and unmount tests passed in the complete 454-test frontend check; additional
independent ABA and unmount cases are promoted into the published check. Type checking and
production build are separate from browser interaction acceptance.

Real browser, Windows, deployed controller/Agent and physical bench acceptance
remain open. Those checks are not closed by these software regressions.
