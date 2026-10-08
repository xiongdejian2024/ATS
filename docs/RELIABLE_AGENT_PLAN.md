# Reliable controller–Agent script execution and bounded logs

Scope reset: 2026-10-08, following the user's explicit priority: reliable cloud–Agent communication, user-authored scripts, live logs, and bounded/compressed browser presentation. Groovy/DSL and further advanced API-testing, review, report, and defect feature expansion are deferred. Existing implementations and branches are preserved.

## Architecture references

Jenkins describes a controller that schedules/monitors work and agents that execute it through bounded executors: [Using agents](https://www.jenkins.io/doc/book/using/using-agents/). Its [controller isolation guidance](https://www.jenkins.io/doc/book/security/controller-isolation/) separates build execution from controller authority. [Remoting](https://www.jenkins.io/doc/developer/architecture/remoting/) documents Jenkins' communication layer; ATS does not adopt that Java implementation or Groovy.

The following are ATS design and acceptance choices informed by those principles, not guarantees inherited from Jenkins.

## Five acceptance groups

| Group | Required outcome | Current evidence / remaining work |
|---|---|---|
| A. Connection ownership | Authenticated registration, current-session fencing, heartbeat expiry, bounded reconnect backoff; stale sockets cannot change replacement state or ACK data | Session overlap/late-close defect reproduced; implementation and failure injection underway. Single-controller ownership must be explicit; no unsupported multi-worker guarantee. |
| B. Authoritative task lifecycle | Server queue/claim, bounded shared capacity, stable execution ID, durable acceptance/result ACK, cancellation/timeout process-group cleanup, persisted terminal outcome | Capacity and terminal-slot repair implemented and independently reviewed; publishing with blue theme. Restart/ambiguous acceptance and capability compatibility remain acceptance checks. Never claim general exactly-once execution. |
| C. Script execution contract | User scripts run on Agent using validated argument/context boundaries, bounded timeout/output/resources; controller never runs uploaded task code | Existing Python/XAT and legacy shell execution retained. Audit paths, argument shapes, environment and invalid limits; trusted scripts are not an OS sandbox. |
| D. Durable log transport | Bounded Agent memory/disk spool, sequenced batches, persistence-before-ACK, replay/dedup and explicit gap/quota policy; retained raw diagnostics | Slow browser isolation/history recovery already published. Durable Agent spool/replay implementation underway; retention and disk-full behavior need measured failure tests. |
| E. Browser log presentation | Bounded records/bytes/DOM, virtualized window, pause/follow, repeated-line folding without deleting raw evidence, paged history/download | Existing 20-record/2000-line/512K-character virtualized tail and reconnect recovery tested. Byte-bound/folding/high-volume soak audit underway. Browser interaction QA currently blocked by cloud browser restrictions; unit/build evidence is separate. |

Publication baseline: main `959653277f6d3d30633f18efba9dff46b6e4eaec`; exact-commit GitHub software checks passed. Local focused integration starts at `83a19ad569720bc8e2a910845ade3196b77d570a` (capacity repair).

## Acceptance discipline

Each group closes only with final integrated tests, independent review, explicit failure-injection evidence and exact published commit CI. Exercise network loss/reconnect, duplicate dispatch/replay, late old-session messages, cancellation during startup/finalization, child processes surviving the shell, slow viewers, high-volume output, quota exhaustion and restart recovery. Record limits and remaining platform boundaries (live MySQL, Windows process trees, hardware and browser interaction), rather than treating static checks as runtime proof.

No production deployment, credential creation, security/network setting changes, or physical test-bench operations are part of this work.
