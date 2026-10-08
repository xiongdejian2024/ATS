# Reliable controller–Agent script execution and bounded logs

Scope reset: 2026-10-08, following the user's explicit priority: reliable cloud–Agent communication, user-authored scripts, live logs, and bounded/compressed browser presentation. Groovy/DSL and further advanced API-testing, review, report, and defect feature expansion are deferred. Existing implementations and branches are preserved.

## Architecture references

Jenkins describes a controller that schedules/monitors work and agents that execute it through bounded executors: [Using agents](https://www.jenkins.io/doc/book/using/using-agents/). Its [controller isolation guidance](https://www.jenkins.io/doc/book/security/controller-isolation/) separates build execution from controller authority. [Remoting](https://www.jenkins.io/doc/developer/architecture/remoting/) documents Jenkins' communication layer; ATS does not adopt that Java implementation or Groovy.

The following are ATS design and acceptance choices informed by those principles, not guarantees inherited from Jenkins.

## Five acceptance groups

| Group | Required outcome | Current evidence / remaining work |
|---|---|---|
| A. Connection ownership | Authenticated registration, current-session fencing, heartbeat expiry, bounded reconnect backoff; stale sockets cannot change replacement state or ACK data | Implemented and independently reviewed: stale-session fencing, initial outage retry, liveness expiry and same-disk replay. Single-controller ownership only; no unsupported multi-worker guarantee. |
| B. Authoritative task lifecycle | Server queue/claim, bounded shared capacity, stable execution ID, durable acceptance/result ACK, cancellation/timeout process-group cleanup, persisted terminal outcome | Capacity and terminal-slot repair published with blue theme in main 0c233b2; exact-commit CI passed. Persistent admission markers preserve restart deduplication; ambiguous acceptance remains explicit. Never claim general exactly-once execution. |
| C. Script execution contract | User scripts run on Agent using validated argument/context boundaries, bounded timeout/output/resources; controller never runs uploaded task code | Formal script-suite runtime now has finite deadlines, nonblocking Unicode output, process cleanup and durable checkpoint results. A clear standalone script-job UX/API remains required; generic direct-task debug frames are not an equivalent durable job protocol. Trusted scripts are not an OS sandbox. |
| D. Durable log transport | Bounded Agent memory/disk spool, sequenced batches, persistence-before-ACK, replay/dedup and explicit gap/quota policy; retained raw diagnostics | Durable bounded Agent spool/replay, commit-before-ACK, permanent-error diagnostics and quota/cancel failure tests implemented. Three-minute soak persisted 12,200 lines and drained the spool. Global server retention remains a separate policy/implementation decision; no automatic deletion is enabled. |
| E. Browser log presentation | Bounded records/bytes/DOM, virtualized window, pause/follow, repeated-line folding without deleting raw evidence, paged history/download | 20-record/2000-line/512 KiB UTF-8 virtualized tail, Unicode-safe clipping, repeat folding and node-history request cleanup implemented/reviewed. Bounded raw export and the remaining plan-history modal are in a separate active increment. Browser interaction QA currently blocked by cloud browser restrictions; unit/build evidence is separate. |

Publication baseline: main `0c233b24d42f16d13b104f06468376ea3f3e54bd`; exact-commit GitHub software checks passed. Current communication integration: `e86ceea8eb2192f13158a074a5a79c301659cbb1`, pending final aggregate/publication.

## Acceptance discipline

Each group closes only with final integrated tests, independent review, explicit failure-injection evidence and exact published commit CI. Exercise network loss/reconnect, duplicate dispatch/replay, late old-session messages, cancellation during startup/finalization, child processes surviving the shell, slow viewers, high-volume output, quota exhaustion and restart recovery. Record limits and remaining platform boundaries (live MySQL, Windows process trees, hardware and browser interaction), rather than treating static checks as runtime proof.

No production deployment, credential creation, security/network setting changes, or physical test-bench operations are part of this work.
