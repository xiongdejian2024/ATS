# Agent script runtime contract

This increment covers trusted user scripts. Commands still execute with the Agent's normal operating-system permissions; this is not a sandbox.

- Legacy suite commands remain shell strings. Generic tasks retain both shell-string and argv-list execution, explicit working directories, and environment overrides.
- The configured Agent default timeout applies to legacy suite preparation and execution. Generic tasks use that default unless their message supplies a timeout. XAT uses its command timeout or the same configured default.
- Timeouts must be finite positive numbers in seconds. Zero, negative values, booleans, null, strings, NaN and infinity fail before process startup with an error terminal result.
- A single deadline covers legacy Git preparation, subprocess startup, chunked output reads, and process exit. Existing Git operation caps remain additional ceilings. Waiting for a shared node slot does not consume execution time.
- Pipe reads use asynchronous 4096-byte chunks, so silent scripts and output without a newline do not block heartbeats, cancellation, or deadlines. UTF-8 decoding preserves characters split across chunks.
- Cancellation and timeout stop the owned POSIX process group (or direct child on non-POSIX platforms) before releasing the admission slot or publishing terminal completion. Durable result delivery and cleanup are outside the execution deadline, so the deadline never intentionally interrupts finalization.
- Configuration/work-directory/environment setup errors in generic tasks return an error result instead of escaping the task coroutine without a response.

## Verification

`tests/test_script_runtime_contract.py` exercises invalid deadlines, shell/argv compatibility, working directory/environment overrides, UTF-8 chunk boundaries, silent/no-newline legacy deadlines, event-loop responsiveness, cancellation with a finished case, and preparation cancellation/deadlines. Existing capacity, interrupted-result and SAT lifecycle tests remain applicable.

No real remote Git service or hardware is required by these tests. Git preparation subprocess cancellation is tested with an isolated local Python process. Output retention/spooling is handled separately and is not changed by this increment.

## Completed results and diagnostic bounds

Legacy case rows now use the same durable per-execution outbox as XAT. A completed row is remembered by case ID after durable storage, even if its socket send fails. On every exit, the writer is stopped before the final checkpoint is recovered. Timeout errors are synthesized only for missing cases; cancellation does not fabricate results for unfinished cases. Replayed case events precede completion and retain stable IDs.

Legacy and XAT checkpoint reads reject files over 16 MiB before JSON decoding. Legacy rows must identify a selected case. Git preparation drains stdout and stderr concurrently but retains only a 64 KiB tail per stream, with an explicit omitted-byte marker. Script stdout chunks use raw=True and preserve whitespace; the companion log-spool integration applies raw concatenation in backend history.

Terminal legacy diagnostics are carried by the durable completion event and never wait for live-log quota. Initial SAT logging, spawn and output reads share its execution deadline. Generic task cancellation interrupts a blocked log callback and drains abandoned pipes while stopping the process.

Native HTTP retains its existing request/retry deadlines in this increment; it does not gain a whole-suite deadline here. Initial native logging is separately capped by the configured Agent default timeout, so it cannot occupy a slot indefinitely on backpressure. Output summary/spool bounds are being integrated separately; this change does not claim complete resource isolation or a script sandbox.

Process termination waits for the owned leader’s OS exit independently of pipe EOF, including a live leader that ignores SIGTERM. Abandoned pipe draining after process-group cleanup is capped at one second; then the pipe transport is closed. A trusted script can deliberately detach into a different session, so this is not a guarantee to terminate arbitrarily detached descendants. Tests explicitly clean up their own detached-process probes.
