# Native processors and explicit Mock reports

The bounded A02 scope is saved/frozen SQL and ordinary-script pre/post processors,
once-per-case global processors, a local static Mock response, and measured HTTP
phase reports. It uses the existing controller, Agent slot, script runtime and durable
log/result protocol. It does not add an external service or request real credentials.

## Execution and permissions

- API and scenario configuration may declare up to ten global pre/post processors
  per phase. Each frozen case runs its global pre phase once before requests and its
  global post phase once after normal request processing. A scenario uses its own
  globals; API steps use their request pre/post declarations.
- Request pre/post processors run in order for each attempt. Pre failure sends no
  HTTP request; post failure never retries an already completed HTTP side effect.
  Later processors are recorded as skipped. Request post processing requires an
  obtained response; network/preparation failures do not run that phase. Global pre
  failure skips requests and global post. Cancellation starts no new post work.
- Global SQL scope contains the first frozen request environment plus scenario
  initial values, or the API request initial values for an API case. Request scope
  keeps environment → scenario → request → temporary-binding precedence. Only
  explicit SQL/extraction bindings carry between scopes; SQL bindings commit as a
  group after all requested output columns exist. Each retry rebuilds request scope.
- A script hook saves only a same-project ScriptJob reference and optional expected
  revision. The controller checks enabled actor, current project execute permission
  and node ownership/system manage, then freezes the existing bounded Python,
  Shell or command-plus-argv configuration. Editing the job does not change an
  existing frozen run. Argument strings retain ordinary script-job semantics.
- All hooks in one frozen case must bind the same actual Agent node. Explicitly
  selected mismatching nodes fail before queue creation; a pool may select the hook
  node only when that node is a member. All four real dispatch paths verify current
  node/project authority and captured authenticated capabilities before claiming.
  A scheduled suite whose node changed while queued is rejected.
- Hooks run inside the parent executor slot and parent execution log ID; they do not
  create a child queue or ScriptJobRun. Per-hook files remain unique across cases.
  The complete hook deadline includes startup/output/completion log backpressure.
  Cancellation and timeout complete process-group cleanup before returning a result.
  Node/project/job locking orders avoid the freezer/updater lock cycle. Ordinary
  script mutations and idempotent receipts refresh and SHARE-lock their enabled
  actor; old receipts retain frozen-node authority after job retargeting, including
  fresh authority after a concurrent conflict rollback.

## Synthetic read-only SQL

A SQL processor uses a new in-memory SQLite database seeded only from its declared
synthetic fixtures. It cannot connect to the controller database or take a file path,
server address, credential, extension or external database connection. SQL text is
never variable-substituted; parameter values use bound parameters. A deny-by-default
authorizer rejects writes, transaction controls, ATTACH, PRAGMA and non-whitelisted
functions. Cancellation interrupts the worker and awaits its exit.

Limits: ten tables, twenty columns per table, one thousand declared rows per table,
8192 SQL characters, one hundred parameters/bindings, 256 KiB declaration, 50–2000 ms
time budget, one million VM operations, at most one thousand returned rows, and
64 KiB returned data. Rows are checked while streaming before a result can amplify
into a large allocation. SQL output values are rendered as literal bounded text.

## Static Mock and reports

An enabled Mock response supplies status 200–599, up to 100 bounded headers, UTF-8
body (131072 characters within an aggregate 256 KiB budget) and delay 0–3000 ms. It
returns inside the Agent, opens no Mock server and makes no call to the target URL.
It still builds the actual request and exercises extraction, assertions and processors;
its delay respects the explicit response timeout. Disabled Mock remains a real HTTP
request. The saved/frozen response is used even if configuration subsequently changes.

New extensions require native_http_processors_v1; hooks additionally require
script_jobs_v1, and variable declarations retain native_http_variables_v1. Unsupported, protocol-1
or unauthenticated sessions stay pending without consuming capacity. Old messages
strip empty declarations and old executions retain strict detail version 1. The final
native dispatch message remains limited to 12 MiB (Agent receives at most 16 MiB).
The Agent rejects an extension that its controller did not negotiate.

Version 2 records source=http/mock, measured preparation, HTTP/Mock exchange,
extraction, assertion and pre/post processor durations, ordered processor outcomes
and bounded variable bindings. Absent stages remain absent; the blue report displays
“未记录” instead of a fabricated zero. DNS/TCP/TLS timings are not inferred. Responses
and total detail retain the existing 256 KiB body capture and 8 MiB detail budgets;
processor results are at most twenty per request/global scope with one hundred
bindings each, 4096-character values and explicit omission/truncation counts.
The browser uses text interpolation for bodies, names and bound values.

## Acceptance status

Formal tests cover authorizer limits, streaming memory amplification, immutable
bindings, Mock timeout, current-session admission at four entrances, global once
semantics, plain Python/Shell/argv, backpressure deadlines, pre/post side effects,
physical process teardown, current node revocation, controller–Agent HTTP and Mock
reports with durable results/ACK, and cross-case hook files. Frontend component tests
cover invalid draft preservation, guarded save/leave, readonly state, actor/project ABA,
unmount, paged script/version selection, old reports and true zero timings.

Final full-suite, actual disposable PostgreSQL/MySQL and exact published-head CI
results are recorded in ATS_COMPLETION_MATRIX.md when they finish. Real browser,
Windows process-tree, hardware and public deployment acceptance remain open. This
bounded SQL scope does not imply a production database connector; full Groovy/Java
expressions, nested runners and the old 23-group API expansion remain excluded.
