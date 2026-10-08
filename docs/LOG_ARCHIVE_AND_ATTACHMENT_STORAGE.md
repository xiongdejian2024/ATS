# Durable evidence capacity and storage

This increment adds software support; it does not configure a service, migrate
production data, delete raw evidence or qualify real deployment/browser/Windows.

## Global logs

`python scripts/log_capacity.py` reports record counts and UTF-8 text bytes for
suite, standalone-script and direct-task logs, including records older than the
configured retention window. SQL computes counts and bytes without loading raw
bodies. This measures text, not database indexes/WAL/backups/physical disk usage.

Settings:

| Variable | Default | Meaning |
|---|---|---|
| `ATS_LOG_ARCHIVE_ENABLED` | `false` | Archival explicitly enabled; no scheduler is installed |
| `ATS_LOG_RETENTION_DAYS` | `30` | Age threshold for archive candidates; never a deletion deadline |
| `ATS_LOG_WARNING_BYTES` | `10737418240` | Global text-capacity warning threshold |
| `ATS_LOG_ARCHIVE_MAX_BYTES` | `1073741824` | Maximum raw bytes per archive record |
| `ATS_LOG_ARCHIVE_DIR` | unset | Operator-selected persistent archive directory |

After deliberately configuring an existing persistent destination, use
`python scripts/log_capacity.py --archive-expired --limit 100` to **copy** aged
records. Each gzip JSON-lines artifact contains identity metadata, at most 65536
Unicode characters per chunk, and a final SHA-256/byte count. The copied prefix
ends at capture; subsequent appends remain in the database. A temporary file is
flushed/fsynced and replaced atomically; failed copies retain previous artifacts.

No DELETE, cursor advancement, Agent spool clearing, automatic pruning or claims
of freed database capacity are included. Permanent deletion requires separate
user authorization and a verified backup/deletion design. Protect archive files
with the same access and backup policy as the source logs.

## Case attachments

Existing local attachments keep their paths. `ATS_ATTACHMENT_BACKEND=local`
(default) writes beneath `CASE_ATTACHMENT_DIR` using an atomic temporary file.
An ephemeral container directory is still ephemeral; configure an existing
persistent directory if using this backend.

`ATS_ATTACHMENT_BACKEND=database` stores new bytes in `attachment_blobs` and
includes them in ordinary database backups, with the existing file-size limit.
It needs no external storage account. Existing local files are not automatically
copied/deleted. Row paths identify their backend, so downloads still work after
changing the backend used for new uploads. All reads first authorize project and
case access, download as attachment/octet-stream, and set `nosniff`/private cache.

`ATS_ATTACHMENT_BACKEND=s3` is an optional adapter for an **already authorized**
bucket. It requires `ATS_ATTACHMENT_S3_BUCKET`, `ATS_ATTACHMENT_S3_ACCESS_KEY`,
`ATS_ATTACHMENT_S3_SECRET_KEY`; optionally set `ATS_ATTACHMENT_S3_ENDPOINT`
(HTTPS only) and `ATS_ATTACHMENT_S3_REGION`. It never creates a bucket or uses
sample MinIO credentials. This implementation is tested with a synthetic client;
actual service configuration and runtime acceptance remain external work.

Preview/apply `python scripts/upgrade_attachment_storage.py [--apply]` before
using the new controller with an existing database. It creates only the new
table; original metadata/files remain untouched. PostgreSQL fresh DDL now covers
84 models (including suite delivery audits). Use schema-specific initialization
instructions for the dedicated PostgreSQL schema; never apply fresh DDL to an
existing installation as an upgrade.

An uncertain database commit or a read failure after commit retains external
bytes. Such orphan candidates need later reconciliation; the controller cannot
infer that a failed HTTP response means an attachment was never committed.

## Ordinary suite unknown execution

Preview/apply `python scripts/upgrade_suite_delivery.py [--apply]` for the new
`suite_deliveries` audit table. Slot claims capture the dispatch session and
frozen node. Failed delivery, absent/expired session or a replaced session makes
the running execution explicit as unknown. The controller never re-dispatches
it automatically. A current-session running task cannot be manually closed via
this unknown-only path.

Open the execution's **日志** page. The operator must have project execution
authority and own/manage the **frozen** Agent node, explicitly confirm that the
execution never started or all related processes stopped, and enter a reason.
Closing records the operator/time/reason and unknown result, marks the queue
failed and releases its slot; it never kills a process or reports success.
Completed results/logs remain. Later completion/result replays are acknowledged
without replacing this audited outcome. Existing plan/scheduled batches retain
their own confirmation entrance and cannot be bypassed here.

Changing runs or users clears confirmation; stale requests and background polls
cannot replace a new selection or a successful closure. Repeated closure is
idempotent, and server validation rejects numeric/truthy pseudo-confirmations.
