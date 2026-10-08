# Literal initial and environment variables

API requests and scenarios accept up to 100 `initialVariables` declarations.
Request environments persist the same declaration rows in an additive sidecar.
Rows contain `name`, literal string `value`, `enable` and `description`; duplicate
names (including disabled rows) and declarations over 64 KiB are refused. Empty
strings and whitespace are preserved. The existing `${name}` renderer substitutes
one literal pass; there is no Groovy/Java evaluation, shell interpolation or secret
vault behavior.

For each request and retry, the scope is composed in this order: environment,
scenario, request, extracted temporary results. Later layers override earlier ones.
Only extractor writes/deletions enter the shared temporary scope; request-local
values do not leak into following steps. Equal-value extractor writes and derived
alias cleanup remain explicit. Assertions see the same attempt scope after
extraction. Environment declarations are frozen with the request and replay does
not reread a subsequently edited environment.

Environment edits use the existing parent revision. Old clients omitting
`variables` preserve current declarations; explicit `[]` clears them. Current
project permission and an enabled current actor are checked again after the project
lock, for both environment and case writes. The additive migration defaults to
preview and never grants permissions or deletes existing data.

All four suite dispatch entrances require an authenticated current Agent session
advertising `native_http_variables_v1` before claiming a slot. Pool selection also
skips incompatible sessions. Such tasks stay pending without a slot until a capable
Agent is available; the captured session sends the actual message. A replacement
after claim retains the existing conservative uncertain-delivery behavior and never
redirects the message to the replacement socket. Empty declaration fields are
removed from variable-free wire so the committed original strict Agent model still
accepts it. Frozen native messages are limited to 12 MiB before creating/claiming a
task, below the Agent's 16 MiB reception limit.

The blue editor has initial/environment variable tables, persistent incomplete
drafts, actor/project/case fencing, safe save baselines and guarded closes/reloads.
Successful entity writes are acknowledged independently from optional subsequent
metadata reads. Real browser, Windows, hardware and deployment acceptance remains
separate from the automated synthetic loopback regressions.
