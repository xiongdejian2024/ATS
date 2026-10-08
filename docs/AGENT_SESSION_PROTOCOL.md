# Controller–Agent transport ownership and recovery

## Design source and scope

The architecture borrows the separation of responsibilities in Jenkins:

- [Using agents](https://www.jenkins.io/doc/book/using/using-agents/): the controller assigns work to agents; executors bound concurrent work. ATS keeps scheduling, permissions and durable run state on the controller, and user scripts/process teardown on the Agent.
- [Controller isolation](https://www.jenkins.io/doc/book/security/controller-isolation/): build scripts should not execute with controller filesystem privileges. ATS uses a narrow allowlist of typed Agent messages rather than allowing Agents to execute arbitrary controller code. Deploy Agents with separate OS identity/machine and no access to controller secrets. The transport itself is not a script sandbox.
- [Remoting architecture](https://www.jenkins.io/doc/developer/architecture/remoting/): controller/Agent communication is an explicit layer. ATS implements its own JSON/WebSocket protocol; it does not add Java, Groovy, Jenkins Remoting or general-purpose RPC.

## Reproduced race and ownership fix

Previously: register socket A, register replacement B, then A closes or its send fails. Cleanup by environment ID alone deleted B and wrote the node offline. A buffered heartbeat/result could also mutate current state; receive timeouts only sent ping indefinitely.

Each accepted socket now has a random session ID (generation), its socket identity, a monotonic liveness deadline and a serialized sender. A replacement invalidates the old generation before bounded asynchronous close. Every incoming handler is admitted under the environment's local async lock; registration takes that same lock. An already admitted handler finishes before replacement, and a late waiting frame is discarded before persistence, queue release or ACK. Outbound ACKs explicitly target the admitted session, not whichever socket happens to be current by then. Cleanup, send failure and token invalidation use compare-and-remove. Token authentication is rechecked after waiting for admission; token invalidation removes ownership before potentially slow notification I/O.

This prevents stale-session false ACKs. It does not revoke a frame already transmitted before replacement, stop previously authorized scripts, or prove that a network write reached the other process.

## Protocol and rollout

- New Agents request `protocol_version=2` in the WebSocket URL.
- The controller authenticates the existing environment token and sends ordered `welcome` then `auth_success`, carrying identical `session_id`, `protocol_version=2`, working directory, reconnect delay and liveness timeout.
- The Agent becomes ready only after validating both handshake frames. All subsequent frames carry that session ID/version; a mismatch, invalid JSON/object/type or unsupported protocol closes the connection without result ACK.
- The session envelope is added to a copy at send time. Durable event IDs/execution IDs and on-disk result payloads are unchanged and rebind to the newly authenticated connection during replay.
- No version parameter (or explicit 1) selects compatibility mode for old Agents. They retain server-side socket-identity fencing but are not required to echo the new fields. Upgrade the controller first: a v2 Agent intentionally refuses an old controller lacking this handshake.
- Frames are capped at 16 MiB (matching the existing 10 MiB workspace upload after base64 expansion); this is a transport ceiling, not an intended log batch size.
- HTTP heartbeat is no longer an unauthenticated alternative to transport ownership. It requires `Authorization: Bearer <environment token>` and `X-Agent-Session-ID: <current session>` and cannot establish an offline connection.

The v2 handshake here negotiates transport version/session/liveness only. Durable log batching separately advertises its own capability when its handler is installed. There is no implemented runner-capability routing, label-expression scheduler, or negotiated executor capacity. Controller Environment capacity and Agent YAML capacity remain independent conservative gates; see [node admission](NODE_CAPACITY_ADMISSION.md).

## Liveness, restart and reconnect

A valid inbound frame proves Agent liveness. After 30 seconds without one, the controller sends an application ping; the existing Agent replies with pong. After 90 seconds without a valid inbound frame, the controller retires the session even when sending ping still succeeds. Unknown/malformed/stale frames cannot keep it alive. Heartbeat/pong/other valid frames refresh liveness; hardware inventory changes only when corresponding heartbeat fields are provided. DB status writes are throttled to five seconds for ordinary traffic, with explicit heartbeats immediate. While a local session exists, status reads use its monotonic deadline rather than prematurely expiring the throttled DB timestamp. Idle receive waits release SQL read transactions instead of reserving a pool connection per idle Agent.

The Agent also expires an unresponsive controller, uses bounded opening/handshake/send/close timeouts, and retries initial controller unavailability as well as later network flaps. Retry delay has jitter and exponential backoff capped at 60 seconds; a short-lived successful handshake does not reset the backoff. It resets after at least 30 seconds of healthy authenticated activity. Only the matching socket's failure clears client state, so a delayed old send/receiver cannot retire its replacement.

On controller startup, persisted online flags are reset; shutdown retires current sessions. Agents reconnect and get new generations. Result replay runs alongside receive/ACK processing, avoiding an authentication callback deadlock with a large outbox. Process cancellation maps and durable admission markers survive a transport reconnect as before. Restarting the Agent can replay already recorded results from its unchanged workspace; it does not automatically recover or rerun an uncertain/orphaned process.

## Deployment limits and delivery semantics

**Exactly one controller process/worker owns WebSockets, API dispatch and these in-memory session locks.** Do not deploy multiple Uvicorn workers/controllers, rolling-overlap replicas, or a separate process that expects this connection registry to route dispatch. Startup online-flag reset also assumes this topology. UUID generations are not database leases, cross-process compare-and-swap ownership or distributed fencing. No migration is needed for this explicitly single-controller increment. Multi-controller support requires durable ownership leases plus routed dispatch and independently qualified DB concurrency.

Operate one Agent process/workspace per environment token. Two live Agents sharing a token replace each other and may keep reconnecting; this change does not coordinate their operating-system processes or deduplicate work across unrelated workspaces. Transport ownership and execution ownership are different.

Completed execution IDs are removed from in-memory admission/runner sets only when their persistent admission marker remains present. Those markers still reject delayed dispatch and replay after restart and must be retained. Embedders without a workspace, or runs with missing/unreadable markers, keep their in-memory duplicate guard.

Result delivery is durable retry plus idempotent result handling, not exactly-once execution. A committed result whose ACK is lost is replayed and ACKed again. The existing handler may also ACK a valid late event already superseded by a durable terminal run state; this preserves the existing result contract. A failed dispatch write remains uncertain and retains its running reservation; it is not automatically re-executed. Only terminal Agent events release running slots after teardown. Accepted-ID markers remain persistent and must not be deleted as routine cleanup. Agent crashes can leave work needing investigation.

The database's online field is a status cache, not an execution lease. If the database itself is unavailable, offline persistence may fail and be corrected by expiry/startup; local transport ownership still retires immediately. Timeout guarantees assume a functioning event loop, not an OS/process freeze. These tests do not qualify production MySQL, multi-controller deployment, physical hardware, proxy idle policies or browser rendering.

## Verification

- `tests/test_agent_session_fencing.py`: overlapping v2/legacy sockets, stale close/heartbeat/results/logs, old-send failure, serialized admitted handler, protocol/frame errors, no stale ACK, live pong versus silent Agent timeout, token revocation while registration waits, HTTP bypass rejection, DB startup/expiry/pool release, v2 handshake readiness, client stale-ACK/old-send protection, retry backoff and initial outage.
- `tests/test_agent_session_restart_e2e.py`: actual loopback HTTP/WebSocket, completed offline script results, Agent object restart with the same disk outbox, a new authenticated generation, replay ACK and no duplicate result rows.
- Existing transport, native HTTP/XAT, admission, cancellation and interrupted-result regressions remain required together with the root `tests` aggregate.

Run from repository root:

```sh
env -u ALL_PROXY -u all_proxy /workspace/shared/ATS-venv/bin/python -m pytest tests -q
```

No production settings, credentials, deployment or hardware were changed by this increment.

Validation on the isolated cloud worktree: root Python aggregate **721 passed**; independent final session/restart focused review **35 passed**. Scoped Black, fatal/undefined-name Flake8 checks, Mypy on the protocol/connection/client modules, compilation and `git diff --check` passed. The aggregate used disposable SQLite databases and loopback HTTP/WebSockets with proxy variables cleared. No production MySQL or hardware result is implied.
