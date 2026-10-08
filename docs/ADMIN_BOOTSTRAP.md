# Create the first administrator safely

This is a one-time, operator-run bootstrap for an initialized ATS database with
**no users**. It uses the original ATS password/JWT/RBAC system. It does not use
Supabase Auth, migrate a schema, reset an existing password, enable a disabled
account, or promote an existing user. Do not run it as a startup or deployment hook.

## Prerequisites

- Install the backend dependencies and initialize the intended ATS schema first.
- Supply the same protected `DATABASE_URL` and, for PostgreSQL, dedicated
  `DATABASE_SCHEMA` used by the controller. Check the target before executing.
  Database credentials must remain in the approved secret configuration.
- Run once from an operator terminal before normal service use. Do not run it
  against a different application's database or a schema with existing users.
- This guarded command supports PostgreSQL and SQLite. SQLite is useful for
  isolated tests. Other dialects, including MySQL, fail closed without querying or
  modifying their database; the old unsafe MySQL bootstrap defaults are removed.

## Preferred: hidden interactive password entry

From the repository root, with the application's Python environment active:

```bash
python backend/scripts/create_admin.py --username your-login --email you@example.com
```

Replace `your-login` and `you@example.com` with the intended administrator's
identity. Alternatively, from `backend/` with uv:

```bash
uv run python scripts/create_admin.py --username your-login --email you@example.com
```

The script prompts for the password twice with `getpass`; neither entry is
printed. Cancellation, an unavailable terminal, an echo-fallback warning, a
mismatch, missing identity or invalid credentials causes an error before opening
a database session. If no terminal is available, use a protected one-shot
`ADMIN_PASSWORD` environment injection; a piped password is not accepted.

Input requirements:

- Username: explicitly supplied, 3–50 ASCII letters, digits, dots, underscores or
  hyphens, beginning with a letter or digit.
- Email: explicitly supplied, valid, at most 100 characters.
- Password: unique, at least 16 characters and at most 72 UTF-8 bytes (the bcrypt
  limit); at least three of lowercase, uppercase, digit and non-alphanumeric;
  at least eight distinct characters; no control characters or outer whitespace.
  Common password fragments and account names are rejected. Prefer a fresh random
  password from a password manager; these checks do not estimate full entropy.
- Optional `--full-name`: 1–100 printable characters; defaults to `系统管理员`.

Username, email and display name can also be supplied as `ADMIN_USERNAME`,
`ADMIN_EMAIL` and `ADMIN_FULL_NAME`; explicit CLI options take precedence. There
are no default username, email or password values. Empty password injection is
rejected instead of falling back to another source. Do not supply passwords as
command-line arguments; even rejected arguments are not echoed in errors.

## One-shot environment input

An approved secret manager may inject `ADMIN_PASSWORD` into only the bootstrap
process. Do not save it in Render service variables, `.env`, a repository file,
CI logs, shell history, or a permanent shell export. Disable shell tracing and
secret logging in the launcher. The script removes the variable from its own
process environment before loading application settings; it cannot remove a
secret exported by a parent shell or stored in a hosting service.

For a one-shot Bash example without typing the secret into the command itself:

```bash
(
  set +x
  IFS= read -r -s -p 'New administrator password: ' ATS_BOOTSTRAP_SECRET || exit 1
  printf '\n'
  ADMIN_PASSWORD="$ATS_BOOTSTRAP_SECRET" python backend/scripts/create_admin.py \
    --username your-login --email you@example.com
)
```

The temporary shell variable expires with the subshell. Environment injection does
not ask for a second entry; prepare and store the intended password securely
before launch. Neither the success output nor errors include the password, hash,
SQL parameters or database connection string. Avoid running the command under
third-party debug tooling that captures process inputs or local variables.

## Transactions, retries and existing accounts

PostgreSQL obtains `LOCK TABLE users IN SHARE ROW EXCLUSIVE MODE` before checking
for users. The transaction holds that lock through commit or rollback, preventing
two simultaneous first-admin attempts from both succeeding. A transaction-local
10-second lock timeout bounds a wait on an active writer. SQLite uses
`BEGIN IMMEDIATE`. An empty-table `SELECT FOR UPDATE` is not used as a substitute.

If any user exists, including a disabled or differently named user, the command
exits nonzero before changing users, roles, permissions or grants. Re-running a
successful bootstrap therefore refuses; it does not replace the earlier password.
Use the authenticated account-management or approved recovery workflow for an
existing installation.

For an empty user table, permission and role initialization reuses existing
system rows and associations without duplication. An existing non-system role
named `admin` causes refusal. All newly needed permissions, role associations,
the new user and their admin grant commit in one transaction. A failure rolls
back pending writes. An unconfirmed database/connection error should be followed
by checking account state before retrying; a lost commit acknowledgement does not
prove the server rolled back.

The Python helpers remain importable for isolated tests and controlled callers,
but do not commit. Their caller owns the transaction; use `bootstrap_admin` for
the locked first-admin workflow. `create_admin_user` requires explicit validated
credentials and also refuses nonempty user tables. Do not use the initialization
helpers to change permissions in an existing installation without separate review.

## Focused regression checks

From the repository root:

```bash
python -m pytest tests/test_admin_bootstrap.py -q -o addopts=''
```

The default fixture creates disposable SQLite state. It checks input rejection
before database access, hidden input, output redaction, no changes to existing
accounts, permission idempotence, full rollback, original authentication, and
concurrent first-admin attempts. The same tests can run in the repository's
isolated PostgreSQL regression harness. Never set its destructive test URL to a
real user database.
