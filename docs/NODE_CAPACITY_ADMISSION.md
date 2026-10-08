# Node-capacity admission and release

## Reproduced defects

Before this change, the focused regressions reproduced both of these at limit 1:

- Two requests observed an available backend slot, then `start_task` marked both
  queue rows running. The direct API and completion/reconnect/cancel callbacks
  did not participate in the Environment row lock used by plans and schedules.
  Several callbacks also sent after a failed/duplicate claim.
- XAT and native HTTP each started their own task immediately. Neither consulted
  `Agent.config.max_concurrent_tasks`; legacy startup only checked a process map
  populated later, leaving an additional same-turn duplicate-start window.

Review also identified premature release after a legacy final case result,
legacy cancellation releasing on socket-send success, stale pending cancellation
turning an already-started run terminal, and surviving shell descendants.

## Backend contract

`TaskQueueService.start_task` is the admission authority for direct suites,
ordinary queued suites, reconnect, completion, plan orchestration and scheduled
runs. Only its successful claim owner sends an execution message.

1. Lock the Environment row, then current-read running queue IDs.
2. Check enabled state and configured capacity.
3. Conditionally update one pending execution to running, preserving the caller's
   plan/schedule eligibility predicates.
4. Commit slot ownership and dispatch bookkeeping before any network await.

MySQL uses `SELECT ... FOR UPDATE`, including for the capacity read, so a
REPEATABLE READ snapshot established before the Environment lock cannot provide
an obsolete running count. SQLite has no equivalent row locks: its offline path
uses a no-op Environment UPDATE to acquire a write reservation. Concurrent SQLite
regressions verify that separate sessions using that path cannot overclaim; they
are not evidence that production MySQL locking or deployment topology works.

Queued, scheduled, plan and direct dispatch recheck execution identity, current
permission/configuration and enabled executor state. Queued ordinary dispatch
excludes plan/schedule-owned executions so it cannot bypass their policies.

Running slots are released by terminal Agent events, after child/request cleanup.
A case result alone never releases a slot. Pending cancellation takes the same
Environment lock and current-reads the queue row before deciding whether local
cancellation is safe or a running Agent must receive the request.

A failed/exceptional socket write retains its running reservation and is not
blindly retried. For ordinary suites, a scoped cancel can recover a message that
provably never started, as described below. Existing plan/schedule manual
uncertainty-resolution flows remain unchanged.

## Agent contract

A single shared admission gate covers XAT, native HTTP, legacy suites and generic
`task` commands. Its configured cap is `task.max_concurrent` in the Agent YAML.
The backend's Environment cap and Agent cap are independently enforced; if the
Agent cap is lower, backend-reserved work waits locally without starting a
process/request. Waiting for capacity does not block the WebSocket receive loop.

- Admission is reserved before background coroutine startup.
- Execution IDs deduplicate across runner kinds, active/queued/completed work,
  reconnects, and subsequent starts using the same workspace.
- Legacy runs additionally serialize by suite because their files are shared.
  A waiting same-suite legacy run does not consume a node slot.
- Queued cancellation reports cancelled without waiting for an occupied slot.
  Cancellation targets the actual execution across every runner kind.
- Slots stay owned through teardown and durable terminal-event preparation.
  POSIX cleanup handles children ignoring SIGTERM and children whose shell
  leader already exited, including generic task and XAT subprocess groups.
- Reconnect retains the generic task executor's live cancellation map.

The Agent stores small admission markers in its existing work directory. Accepted
markers prevent replay after restart. An unknown scoped cancellation can create a
persistent cancelled-before-start tombstone and acknowledge it only when there
is no accepted marker, execution directory or ambiguous legacy workspace.
Tombstones block delayed execution even after the completion ACK and restart.

Do not remove admission markers or change workspaces to retry uncertain work.
Existing execution artifacts, unreadable data, or old legacy workspaces may
represent orphaned processes; those remain uncertain rather than falsely
acknowledging termination. This increment does not implement automatic orphan
recovery or a new ordinary-suite manual-resolution UI. Operators must investigate
those cases; no workload is automatically re-executed.

## Verification

New regressions:

- `tests/test_node_capacity_admission.py`: overlapping sessions/duplicate claims,
  direct + plan + scheduler + reconnect competition, stale cancellation,
  terminal CAS, last-result retention, revoked executor, failed-send retention.
- `tests/test_agent_capacity_admission.py`: mixed runner limits, duplicate IDs,
  same-suite legacy serialization, queued/scoped cancellation, reconnect and
  exception release, tombstones across restart, ambiguous old workspace refusal,
  real legacy process teardown and SIGTERM-resistant/background descendants.
- `tests/test_node_capacity_e2e.py`: actual loopback HTTP/WebSocket, native HTTP
  blocked at the target while XAT waits locally, cancellation followed by real
  offline XAT results, and never-delivered ordinary dispatch recovery.

Run from the repository root using `requirements-integration.txt`:

```sh
env -u ALL_PROXY -u all_proxy python -m pytest tests -q -o addopts=''
```

Unsetting these two variables is only for local-loopback tests where the cloud
proxy's optional SOCKS driver is absent. No production configuration is changed.
No frontend API or schema migration is needed. No real bench/hardware, production
MySQL, Redis, Celery deployment, or Windows process-tree validation is claimed.

### Verified cloud run (2026-10-08)

- Python 3.12.14: all **658 tests passed** (22 deprecation/ORM warnings), including
  both new real loopback native HTTP/XAT and uncertain-dispatch recovery tests.
- Four focused capacity/cancellation files independently reviewed and run:
  **44 tests passed**, with no remaining blocking review finding.
- The two separate-session/mixed-source races passed five additional repeated
  runs (**10 checks**).
- Modified Python files passed compile checks and focused fatal-error lint;
  `git diff --check` passed. These are not claims of full repository style lint.
- Included the existing SQLite-pool fixture isolation and Python 3.11
  immediate-cancellation test-boundary fixes before final validation. The existing
  reconnect test now explicitly holds reconnection until durable outbox evidence
  is observed, removing a transient-file polling race without mocking delivery.
- An initial aggregate exposed an accidentally removed execution-history import;
  it was restored and the entire final aggregate rerun successfully.

Frontend code was not changed by this increment. Production MySQL locking needs
its own deployment-level validation; no live database or hardware was contacted.
