# PostgreSQL / Supabase controller

The original FastAPI controller, ATS users/JWT/RBAC, HTTP routes, Agent WebSocket,
queue and Vue application remain intact. PostgreSQL is storage; Supabase Auth and
Realtime do not replace these protocols. Never expose the ATS schema through the
Supabase Data API or grant it to `anon`/`authenticated`. ATS permissions are enforced
by the controller, whose database role must be scoped to its dedicated schema.

## Deployment contract

Use Python 3.11+, install `requirements-integration.txt`, and provide the variables
in `deploy/postgres.env.example` through the host's protected secret configuration.
The file contains placeholders only. Passwords in URLs must be percent-encoded.
Use the exact endpoint from the selected project's Connect panel; prefer a direct
connection or session pooler for this persistent service. Transaction-mode poolers
are unsupported because the controller relies on connection session settings.
IPv4-only hosts normally
need the session pooler. TLS certificate validation must stay enabled. Psycopg
prepared statements are disabled for pooler compatibility.
Mount the trusted root certificate obtained from the provider's official Connect
instructions at the `sslrootcert` path in the example, or configure a documented
system trust-store path supported by the deployed libpq. Do not replace
`verify-full` with disabled certificate verification to work around missing CA files.

Connections explicitly set `Asia/Shanghai` over SQL, matching the existing MySQL +08:00
session contract. Several original ATS columns are timestamp-without-time-zone
and their readers interpret naive values as Beijing time; using a UTC session
would incorrectly mark fresh heartbeats stale. Timezone-aware columns retain
their instant and return an explicit offset. This port does not reinterpret old
stored timestamps or copy data from an existing MySQL database.
The session setup runs in autocommit so a later application rollback cannot undo
it; it also sets the dedicated search path even if a pooler filters startup options.

Run from `backend/` with the same environment used to initialize the schema:

```
uvicorn main:app --host 127.0.0.1 --port 17400 --workers 1
```

Exactly one controller process is required: Agent session ownership and live
subscribers are currently process-local. Do not use multiple workers or replicas.
An authenticated private gateway must forward `/api/v1/*` and upgrade `/ws/*` to
the controller. Forward original paths, query parameters and Authorization; do not
log tokens. Browser private-site identity is an additional boundary and does not
replace ATS login. Agents connect to an explicitly authorized controller endpoint.
No production scripts are run during installation.

The host needs persistent process supervision, reliable outbound PostgreSQL TLS,
private HTTP/WebSocket ingress, and writable persistent storage for application
logs/uploads. Start with 2 CPU and 2 GiB RAM, then size from measured workload.
Database log retention and quotas remain the original ATS operator settings;
backups, restoration and disk monitoring must be provisioned separately.

`/health` reports process liveness only. `/ready` returns 200 only when database
access succeeds and all expected model tables/columns exist; otherwise it returns
503 without connection details. This does not validate external Agent connectivity.

## First administrator

After schema initialization, use the explicit, operator-run
[first-admin bootstrap](ADMIN_BOOTSTRAP.md) with the same protected database
configuration and dedicated `DATABASE_SCHEMA`. From the repository root:

```bash
python backend/scripts/create_admin.py --username your-login --email you@example.com
```

Replace both identity values; the terminal prompts for and confirms a strong
password without echoing it. There is no default login or password. This command
runs only while the user table is empty and commits permissions, the system admin
role and the new user together. PostgreSQL serializes concurrent attempts with a
transaction-scoped table lock. It never runs automatically on startup or deploy.
Real credential entry and any production bootstrap are separate operator actions;
repository tests use synthetic accounts in disposable databases only.

## Verification boundaries

Regression tests use a disposable loopback database named `ats_pg_regression` via
`ATS_POSTGRES_TEST_URL`; they drop/recreate tables. Never point them at a user
database. The guard rejects other host/database names. Real PostgreSQL CI uses
synthetic users, scripts and nodes. MySQL and default isolated SQLite remain
supported and have separate checks.

In the dot execution environment, an HTTP server reachable inside one execution
invocation is not evidence that Sites or a later invocation can reach it. A
supported private ingress and a separately verified persistent host are still
required. No real Supabase credentials are included or configured by these files.

## Render Free

`render.yaml` builds `deploy/Dockerfile.controller` and starts
`scripts/start_render.py` on Render's `PORT` with exactly one worker. The image
includes the controller and XAT framework contracts only, not ECU packages,
hardware tooling, case assets, frontend or Agent spool. The entrypoint requires
independent, explicitly configured JWT and origin service secrets; it generates
none and never runs migrations automatically. Initialize/inspect the dedicated
schema separately before deployment, using `scripts/init_postgres.py` (read-only)
and its explicit `--apply` action only after approval.

Sites must add `X-ATS-Origin-Authorization: Bearer <ATS_ORIGIN_SERVICE_KEY>` on the
server, removing any browser-supplied value. Every HTTP and WebSocket route,
including `/health`, `/ready` and `/ws/agent`, requires it. ATS JWT and Agent
authentication still apply after this gate. No origin bypass is granted to Agents;
their private gateway access needs a separately configured supported path before
claiming remote Agent connectivity. Secrets never belong in Vue code or query
strings. Uvicorn access/INFO handshake logging is disabled to avoid recording
existing ATS token-bearing WebSocket query strings.

Render uses its default TCP health check. An authorized gateway can call `/ready`
for database readiness; a TCP check alone does not establish database availability.
Free instances have 512 MB RAM, can sleep/restart, and have ephemeral local disk.
Controller task state, results and raw execution logs live in PostgreSQL. Agent
spools remain on Agent machines. Controller diagnostic files and the existing
local attachment/upload paths are **not durable** on Render Free. The attachment
feature needs an approved external object-storage adapter before uploads are used
as durable evidence. Database persistence does not preserve those local files.
Do not present the free tier as continuously available or production-reliable.

Official platform references: [Render Free](https://render.com/docs/free),
[health checks](https://render.com/docs/health-checks),
[Blueprint specification](https://render.com/docs/blueprint-spec).
