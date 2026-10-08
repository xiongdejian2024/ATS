# XAT interrupted-result recovery

Follow-on update: [node-capacity admission](NODE_CAPACITY_ADMISSION.md) now extends
terminal-event slot release to native HTTP and legacy scripts as well. The original
legacy immediate-cancellation behavior described below is historical.

## Problem

XAT already atomically checkpoints each fully completed test after teardown in
`results.json`. The Agent previously read that file only after a normal process
exit. Timeout therefore overwrote completed tests with synthetic errors, and
cancellation discarded all completed rows.

The suite-wide cancel API used by the frontend also immediately marked XAT tasks
cancelled. The result receiver intentionally rejects new rows for terminal tasks,
so merely fixing the Agent could not recover results through that UI flow.

## Changes

- Terminate the XAT subprocess before reading its final atomic checkpoint on all
  exit paths, including cancellation and timeout.
- Validate checkpoint shape, selected case IDs, uniqueness, terminal statuses and
  finite non-negative durations before serializing result events.
- Deliver completed cases before the terminal execution event through the
  existing durable outbox and ACK mechanism.
- On timeout, unfinished cases still receive timeout errors. On cancellation,
  unfinished cases remain without fabricated results.
- Keep running XAT queue slots until the Agent's terminal event for both scoped
  and suite-wide cancellation. An undeliverable cancellation returns HTTP 503.
- Preserve the existing immediate-cancellation behavior for legacy non-XAT jobs.
- Consume cancellation requested before the execution coroutine starts, and
  protect final result/terminal delivery from late or repeated cancellation.
  Cancelling a caller waiting on cancellation cannot cancel finalization itself.
- Apply the same lifecycle contract to the native HTTP runner, the only SATRunner
  subclass, retaining cancellation of active requests and retry waits.

No schema migration or frontend API change is required. This does not introduce
live streaming of per-case results during an uninterrupted run.

## Regression checks

`tests/test_sat_interrupted_results.py` launches a real pytest process with one
passing case followed by a sleeping case. It verifies timeout/cancel recovery,
terminal-event ordering, cleanup, checkpoint validation and corrupt-file handling.

`tests/test_sat_cancellation_lifecycle.py` exercises immediate startup cancellation,
late cancellation during result delivery, repeated cancellation while terminating
the process, cancellation of the waiting caller, and the native HTTP subclass's
startup/finalization boundaries. A late request after process
execution has already ended preserves its natural outcome while finalization
finishes; it must not suppress the terminal event.

`tests/test_sat_interrupted_e2e.py` covers timeout, per-execution cancellation and
suite-wide cancellation using real HTTP, WebSocket, Agent, pytest subprocess and
SQLite persistence. Only synthetic offline tests run; no hardware is accessed.

`tests/test_suite_cancel_preserves_results.py` covers backend queue-slot retention,
result persistence, replay idempotence, successor dispatch, command aliases,
multiple running executions and cancellation-delivery failures.

Run from the repository root after installing `requirements-integration.txt`:

```sh
python -m pytest tests -q -o addopts=''
cd frontend
npm ci
npm run type-check
npm run test:unit
npm run build
```

For the dot cloud environment, remove only `ALL_PROXY`/`all_proxy` from the test
process environment if HTTPX attempts to initialize an unavailable SOCKS driver;
keep `NO_PROXY` including `127.0.0.1,localhost` for the local test server. No remote
service proxy or security setting needs changing.

Real bench hardware, production MySQL/Redis/Celery and interactive browser QA are
outside this regression pass. Passing these tests does not certify those systems.

## Verified cloud run (2026-10-08)

Baseline: `codex/sat-ecu-integration` at
`0ab1d4895499284821cef6a913a3a38749f12679`.

- Python 3.12.14: all **627 tests passed** (19 existing deprecation/ORM warnings).
- Node 24.19.0: **191 frontend unit tests passed**; type check and production build passed.
- Modified Python files: compile checks and focused fatal-error lint passed.
- `git diff --check`: passed.
- The two Agent interruption regressions failed before the fix. Four initial
  backend cancellation regressions failed before the backend fix. Three additional
  cancellation-lifecycle regressions failed before the lifecycle fix.

The initial local HTTP checks were blocked by HTTPX initializing a SOCKS proxy
without the optional driver. The final successful run used the local-loopback
proxy adjustment described above; no application dependency change was needed.
