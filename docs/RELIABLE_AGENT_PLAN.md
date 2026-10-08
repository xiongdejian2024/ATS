# Reliable controller–Agent script execution and bounded logs

Priority update: 2026-10-08, following the user's explicit priority: reliable cloud–Agent communication, user-authored scripts, live logs, and bounded/compressed browser presentation. The user subsequently confirmed that earlier unfinished business features remain in scope. Their finite, source-audited list is in [ATS completion matrix](ATS_COMPLETION_MATRIX.md). Groovy/DSL is excluded; advanced API-testing remains lower priority. Existing implementations and branches are preserved. Reliability priority does not cancel confirmed review, report, defect, file-library or plan work.

## Architecture references

Jenkins describes a controller that schedules/monitors work and agents that execute it through bounded executors: [Using agents](https://www.jenkins.io/doc/book/using/using-agents/). Its [controller isolation guidance](https://www.jenkins.io/doc/book/security/controller-isolation/) separates build execution from controller authority. [Remoting](https://www.jenkins.io/doc/developer/architecture/remoting/) documents Jenkins' communication layer; ATS does not adopt that Java implementation or Groovy.

The following are ATS design and acceptance choices informed by those principles, not guarantees inherited from Jenkins.

## Five acceptance groups

| Group | Required outcome | Current evidence / remaining work |
|---|---|---|
| A. Connection ownership | Authenticated registration, current-session fencing, heartbeat expiry, bounded reconnect backoff; stale sockets cannot change replacement state or ACK data | Implemented and independently reviewed: stale-session fencing, initial outage retry, liveness expiry and same-disk replay. Single-controller ownership only; no unsupported multi-worker guarantee. |
| B. Authoritative task lifecycle | Server queue/claim, bounded shared capacity, stable execution ID, durable acceptance/result ACK, cancellation/timeout process-group cleanup, persisted terminal outcome | Capacity and terminal-slot repair published with blue theme in main 0c233b2; exact-commit CI passed. Persistent admission markers preserve restart deduplication; ambiguous acceptance remains explicit. Never claim general exactly-once execution. |
| C. Script execution contract | User scripts run on Agent using validated argument/context boundaries, bounded timeout/output/resources; controller never runs uploaded task code | Formal script-suite runtime now has finite deadlines, nonblocking Unicode output, process cleanup and durable checkpoint results. The independent /script-jobs entry now uses explicit formal queue kinds, frozen runs, exit-code outcomes, capability-gated dispatch and durable completion/log delivery. It requires no test cases or proprietary result file; the old direct-task debug channel remains separate. Trusted scripts are not an OS sandbox. |
| D. Durable log transport | Bounded Agent memory/disk spool, sequenced batches, persistence-before-ACK, replay/dedup and explicit gap/quota policy; retained raw diagnostics | Durable bounded Agent spool/replay, commit-before-ACK, permanent-error diagnostics and quota/cancel failure tests implemented. Three-minute soak persisted 12,200 lines and drained the spool. Global server retention remains a separate policy/implementation decision; no automatic deletion is enabled. |
| E. Browser log presentation | Bounded records/bytes/DOM, virtualized window, pause/follow, repeated-line folding without deleting raw evidence, paged history/download | 20-record/2000-line/512 KiB UTF-8 virtualized tail, Unicode-safe clipping, repeat folding and node-history request cleanup implemented/reviewed. Bounded authenticated raw export and plan-history preview are implemented and independently reviewed; integrated validation: 817 Python tests, 237 frontend tests, type check and build passed. Browser interaction QA currently blocked by cloud browser restrictions; unit/build evidence is separate. |

Published communication/raw-export baseline: main `d8df05adefb0dc77a01a32702d5ea35ea7a77bd5`; exact-commit GitHub software checks passed (run 37730569445). The integrated independent script-job increment passed 847 Python tests (one optional MySQL test skipped locally), 282 frontend tests, type checking and production build. CI includes a separate disposable MySQL 8 migration qualification job; consult the exact commit’s Actions result before deployment.

## Acceptance discipline

Each group closes only with final integrated tests, independent review, explicit failure-injection evidence and exact published commit CI. Exercise network loss/reconnect, duplicate dispatch/replay, late old-session messages, cancellation during startup/finalization, child processes surviving the shell, slow viewers, high-volume output, quota exhaustion and restart recovery. Record limits and remaining platform boundaries (live MySQL, Windows process trees, hardware and browser interaction), rather than treating static checks as runtime proof.

No production deployment, credential creation, security/network setting changes, or physical test-bench operations are part of this work.

## Script-job operator path

Open **脚本作业**, choose a project and owned/authorized Agent node, then select Shell, Python or an executable with exact argv. Save and run; offline nodes retain pending work, and only a current authenticated session advertising `script_jobs_v1` may claim it. Run history carries the frozen configuration, exit code, cancellation/timeout outcome and bounded live/raw logs. Unknown executions require explicit operator verification before closing; they are never automatically rerun.

Existing MySQL installations must preview and apply `scripts/upgrade_script_jobs.py` before the updated controller. The migration preserves existing queue rows and adds explicit suite/script target constraints. Existing SQLite NOT NULL queue schemas are refused before DDL because this migration does not rebuild user tables. Fresh SQLite remains supported for isolated validation. No production database was migrated in this work.
