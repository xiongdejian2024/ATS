"""First-admin safety on disposable databases only; no real account credentials."""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import os
from threading import Event
from types import SimpleNamespace
import warnings

import pytest
from sqlalchemy import select

from backend.scripts import create_admin as bootstrap
from core.permissions import SYSTEM_PERMISSIONS, has_global_permission
from core.security import verify_password
from database import SessionLocal, engine
from models import Permission, Role, RolePermission, User, UserRole

SYNTHETIC_PASSWORD = "V7!Ridge-Kite#Harbor38"
CREDENTIALS = bootstrap.AdminCredentials("bootstrap_owner", "owner@example.com", SYNTHETIC_PASSWORD)
AUTH_MODELS = (User, Role, Permission, UserRole, RolePermission)


@pytest.fixture(autouse=True)
def clean_admin_environment(monkeypatch):
    for key in ("ADMIN_USERNAME", "ADMIN_EMAIL", "ADMIN_PASSWORD", "ADMIN_FULL_NAME"):
        monkeypatch.delenv(key, raising=False)


def state():
    """Capture every auth-table column, including hashes and existing grants."""
    with SessionLocal() as db:
        return {
            model.__tablename__: sorted(tuple(row) for row in db.execute(select(model.__table__)))
            for model in AUTH_MODELS
        }


def set_cli_credentials(monkeypatch, credentials=CREDENTIALS):
    monkeypatch.setenv("ADMIN_USERNAME", credentials.username)
    monkeypatch.setenv("ADMIN_EMAIL", credentials.email)
    monkeypatch.setenv("ADMIN_PASSWORD", credentials.password)


@pytest.mark.parametrize(
    "change",
    [
        {"username": ""},
        {"email": ""},
        {"username": "bad\nname"},
        {"email": "bad-address"},
        {"password": ""},
        {"password": "admin123"},
        {"password": "Password123456789!"},
        {"password": "abcdefghijklmnopqrstuv"},
        {"password": "Aa1!Aa1!Aa1!Aa1!"},
        {"password": "V7!" + "x" * 70},
        {"password": "V7!" + "海" * 24},
        {"password": "V7!Ridge\nKite#Harbor38"},
        {"password": "bootstrap_owner-82!Fresh"},
        {"password": "V7!owner-Ridge#Harbor38"},
        {"full_name": ""},
    ],
)
def test_invalid_credentials_never_open_database(change, monkeypatch, capsys):
    credentials = replace(CREDENTIALS, **change)
    set_cli_credentials(monkeypatch, credentials)
    monkeypatch.setenv("ADMIN_FULL_NAME", credentials.full_name)
    opened = []
    monkeypatch.setattr(bootstrap, "open_session", lambda: opened.append(True))
    assert bootstrap.main([]) == 1
    assert opened == []
    output = capsys.readouterr()
    assert "bootstrap refused" in output.err
    if credentials.password:
        assert credentials.password not in output.out + output.err
    assert "ADMIN_PASSWORD" not in os.environ


def test_missing_inputs_have_no_defaults(monkeypatch, capsys):
    opened = []
    monkeypatch.setattr(bootstrap, "open_session", lambda: opened.append(True))
    monkeypatch.setattr(
        bootstrap.getpass, "getpass", lambda _: pytest.fail("must validate identity first")
    )
    assert bootstrap.main([]) == 1
    assert opened == []
    assert "username" in capsys.readouterr().err


def test_noninteractive_missing_password_never_reads_stdin(monkeypatch, capsys):
    monkeypatch.setattr(bootstrap.sys, "stdin", SimpleNamespace(isatty=lambda: False))
    monkeypatch.setattr(bootstrap, "open_session", lambda: pytest.fail("must not open database"))
    monkeypatch.setattr(bootstrap.getpass, "getpass", lambda _: pytest.fail("must not read stdin"))
    assert bootstrap.main(["--username", CREDENTIALS.username, "--email", CREDENTIALS.email]) == 1
    assert "one-shot ADMIN_PASSWORD" in capsys.readouterr().err


@pytest.mark.parametrize("failure", ["mismatch", "echo", "eof", "cancel"])
def test_interactive_failure_never_opens_database(failure, monkeypatch, capsys):
    monkeypatch.setattr(bootstrap.sys, "stdin", SimpleNamespace(isatty=lambda: True))
    monkeypatch.setattr(bootstrap, "open_session", lambda: pytest.fail("must not open database"))
    answers = iter([SYNTHETIC_PASSWORD, "a-different-confirmation"])

    def prompt(_):
        if failure == "echo":
            warnings.warn("echo unavailable", bootstrap.getpass.GetPassWarning)
            pytest.fail("getpass must not fall back to visible entry")
        if failure == "eof":
            raise EOFError
        if failure == "cancel":
            raise KeyboardInterrupt
        return next(answers)

    monkeypatch.setattr(bootstrap.getpass, "getpass", prompt)
    assert bootstrap.main(["--username", CREDENTIALS.username, "--email", CREDENTIALS.email]) == 1
    output = capsys.readouterr()
    assert SYNTHETIC_PASSWORD not in output.out + output.err
    assert "Traceback" not in output.err


def test_accidental_password_argument_is_not_echoed(capsys):
    with pytest.raises(SystemExit) as result:
        bootstrap.main(["--password", SYNTHETIC_PASSWORD])
    assert result.value.code == 2
    assert SYNTHETIC_PASSWORD not in capsys.readouterr().err
    assert SYNTHETIC_PASSWORD not in repr(CREDENTIALS)


@pytest.mark.parametrize("password_source", ["environment", "terminal"])
def test_successful_bootstrap_supports_original_auth_and_permissions(
    password_source, monkeypatch, capsys
):
    prompts = []
    if password_source == "environment":
        set_cli_credentials(monkeypatch)
        args = []
    else:
        monkeypatch.setattr(bootstrap.sys, "stdin", SimpleNamespace(isatty=lambda: True))
        monkeypatch.setattr(
            bootstrap.getpass,
            "getpass",
            lambda prompt: prompts.append(prompt) or SYNTHETIC_PASSWORD,
        )
        args = ["--username", CREDENTIALS.username, "--email", CREDENTIALS.email]
    assert bootstrap.main(args) == 0
    assert "ADMIN_PASSWORD" not in os.environ
    if password_source == "terminal":
        assert len(prompts) == 2
    output = capsys.readouterr()
    with SessionLocal() as db:
        user = db.query(User).one()
        assert user.username == CREDENTIALS.username
        assert user.email == CREDENTIALS.email
        assert user.status is True
        assert user.password_hash != SYNTHETIC_PASSWORD
        assert verify_password(SYNTHETIC_PASSWORD, user.password_hash)
        assert not verify_password("admin123", user.password_hash)
        assert user.password_hash not in output.out + output.err
        assert db.query(UserRole).count() == 1
        assert db.query(Permission).count() == len(SYSTEM_PERMISSIONS)
        assert db.query(RolePermission).count() == len(SYSTEM_PERMISSIONS)
        for code in SYSTEM_PERMISSIONS:
            resource, action = code.split(":", 1)
            assert has_global_permission(db, user.id, resource, action)
    assert SYNTHETIC_PASSWORD not in output.out + output.err
    # Exercise the existing login service, including active-account checks.
    import asyncio
    from services.auth_service import authenticate_user

    with SessionLocal() as db:
        user = asyncio.run(authenticate_user(db, CREDENTIALS.username, SYNTHETIC_PASSWORD))
        assert user.username == CREDENTIALS.username


@pytest.mark.parametrize("matching", ["username", "email", "neither"])
@pytest.mark.parametrize("is_admin", [False, True])
def test_existing_users_are_never_reset_enabled_promoted_or_supplemented(
    matching, is_admin, monkeypatch, capsys
):
    with SessionLocal.begin() as db:
        existing = User(
            username="existing_owner",
            email="existing@example.com",
            password_hash="unchanged-synthetic-hash",
            status=False,
        )
        db.add(existing)
        db.flush()
        role = Role(name="admin" if is_admin else "viewer", display_name="Existing", is_system=True)
        db.add(role)
        db.flush()
        db.add(UserRole(user_id=existing.id, role_id=role.id))
    before = state()
    credentials = CREDENTIALS
    if matching == "username":
        credentials = replace(credentials, username="existing_owner")
    elif matching == "email":
        credentials = replace(credentials, email="existing@example.com")
    set_cli_credentials(monkeypatch, credentials)
    assert bootstrap.main([]) == 1
    assert "users already exist" in capsys.readouterr().err
    assert state() == before
    # A direct helper caller cannot silently promote an existing identity either.
    with SessionLocal() as db, pytest.raises(bootstrap.BootstrapError, match="users already exist"):
        bootstrap.create_admin_user(
            db, credentials.username, credentials.email, credentials.password
        )
    assert state() == before


def test_repeat_bootstrap_preserves_created_account(monkeypatch, capsys):
    set_cli_credentials(monkeypatch)
    assert bootstrap.main([]) == 0
    before = state()
    set_cli_credentials(monkeypatch, replace(CREDENTIALS, password="Z9!Meadow-Finch$Stream57"))
    assert bootstrap.main([]) == 1
    assert state() == before
    assert "users already exist" in capsys.readouterr().err


def test_role_and_permission_initialization_is_idempotent_and_transactional():
    with SessionLocal.begin() as db:
        bootstrap.init_roles(db, bootstrap.init_permissions(db))
        bootstrap.init_roles(db, bootstrap.init_permissions(db))
    before = state()
    with SessionLocal.begin() as db:
        bootstrap.init_roles(db, bootstrap.init_permissions(db))
    assert state() == before
    assert len(before["roles"]) == 1
    assert len(before["permissions"]) == len(SYSTEM_PERMISSIONS)
    assert len(before["role_permissions"]) == len(SYSTEM_PERMISSIONS)


def test_unknown_admin_role_is_not_adopted(monkeypatch, capsys):
    with SessionLocal.begin() as db:
        db.add(Role(name="admin", display_name="Custom", is_system=False))
    before = state()
    set_cli_credentials(monkeypatch)
    assert bootstrap.main([]) == 1
    assert "non-system role" in capsys.readouterr().err
    assert state() == before  # Newly flushed permissions must also roll back.


def test_failed_user_insert_rolls_back_permissions_roles_and_account(monkeypatch, capsys):
    original = bootstrap.create_admin_user
    unsafe_error = (
        "postgresql://synthetic:db-secret@example.test/ats hash=$2b$12$synthetic "
        + SYNTHETIC_PASSWORD
    )

    def fail_after_insert(*args):
        original(*args)
        raise RuntimeError(unsafe_error)

    monkeypatch.setattr(bootstrap, "create_admin_user", fail_after_insert)
    set_cli_credentials(monkeypatch)
    assert bootstrap.main([]) == 1
    output = capsys.readouterr()
    assert "bootstrap failed" in output.err
    for secret in (SYNTHETIC_PASSWORD, "db-secret", "$2b$12$synthetic", "Traceback"):
        assert secret not in output.out + output.err
    assert all(not rows for rows in state().values())


@pytest.mark.parametrize("error_type", [RuntimeError, ValueError])
def test_configuration_errors_are_sanitized(error_type, monkeypatch, capsys):
    def unavailable():
        raise error_type("db-secret " + SYNTHETIC_PASSWORD)

    set_cli_credentials(monkeypatch)
    monkeypatch.setattr(bootstrap, "open_session", unavailable)
    assert bootstrap.main([]) == 1
    output = capsys.readouterr()
    assert "db-secret" not in output.err
    assert SYNTHETIC_PASSWORD not in output.err
    assert "Traceback" not in output.err


def test_unsupported_dialect_fails_before_any_database_statement(monkeypatch):
    with SessionLocal() as db:
        monkeypatch.setattr(
            db, "get_bind", lambda: SimpleNamespace(dialect=SimpleNamespace(name="mysql"))
        )
        monkeypatch.setattr(
            db, "execute", lambda *a, **k: pytest.fail("must not query unsupported database")
        )
        with pytest.raises(bootstrap.BootstrapError, match="PostgreSQL and SQLite only"):
            bootstrap.bootstrap_admin(db, CREDENTIALS)
    assert all(not rows for rows in state().values())


def test_concurrent_first_admin_bootstraps_create_only_one_user(monkeypatch):
    if engine.dialect.name not in {"postgresql", "sqlite"}:
        pytest.skip("CLI fails closed for unsupported database dialects")
    # A pre-initialized admin role must not let different usernames evade the lock.
    with SessionLocal.begin() as db:
        bootstrap.init_roles(db, bootstrap.init_permissions(db))
    first_entered = Event()
    release_first = Event()
    second_attempted = Event()
    second_passed_empty_check = Event()
    original = bootstrap.init_permissions

    def held_initializer(db):
        if not first_entered.is_set():
            first_entered.set()
            assert release_first.wait(10)
        else:
            second_passed_empty_check.set()
        return original(db)

    monkeypatch.setattr(bootstrap, "init_permissions", held_initializer)

    def attempt(credentials, second=False):
        if second:
            second_attempted.set()
        with SessionLocal() as db:
            try:
                bootstrap.bootstrap_admin(db, credentials)
                return "created"
            except bootstrap.BootstrapError as error:
                assert "users already exist" in str(error)
                return "refused"

    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(attempt, CREDENTIALS)
        try:
            assert first_entered.wait(10)
            second = pool.submit(
                attempt,
                replace(CREDENTIALS, username="second_owner", email="second@example.com"),
                True,
            )
            assert second_attempted.wait(10)
            assert not second_passed_empty_check.wait(0.2)
        finally:
            release_first.set()
        assert first.result(timeout=10) == "created"
        assert second.result(timeout=10) == "refused"
    with SessionLocal() as db:
        assert db.query(User).count() == 1
        assert db.query(UserRole).count() == 1
        assert db.query(RolePermission).count() == len(SYSTEM_PERMISSIONS)


def test_all_defined_roles_keep_their_permission_sets(monkeypatch):
    definitions = bootstrap.system_roles()
    definitions["reviewer"] = {
        "name": "Synthetic reviewer",
        "permissions": ["test_case:read", "test_plan:read"],
    }
    monkeypatch.setattr(bootstrap, "system_roles", lambda: definitions)
    with SessionLocal.begin() as db:
        permissions = bootstrap.init_permissions(db)
        for _ in range(2):
            roles = bootstrap.init_roles(db, permissions)
        assert set(roles) == set(definitions)
    before = state()
    with SessionLocal.begin() as db:
        bootstrap.init_roles(db, bootstrap.init_permissions(db))
        for name, definition in definitions.items():
            codes = (
                db.query(Permission.code)
                .join(RolePermission)
                .join(Role)
                .filter(Role.name == name)
                .all()
            )
            assert {code for (code,) in codes} == set(definition["permissions"])
    assert state() == before


def test_exact_72_utf8_bytes_are_accepted_without_truncation():
    password = "Ab7!xY" + "海林" * 11
    assert len(password.encode("utf-8")) == 72
    credentials = replace(CREDENTIALS, password=password)
    with SessionLocal() as db:
        bootstrap.bootstrap_admin(db, credentials)
    with SessionLocal() as db:
        assert verify_password(password, db.query(User).one().password_hash)
    with pytest.raises(bootstrap.BootstrapError, match="72 UTF-8 bytes"):
        bootstrap.validate_credentials(replace(credentials, password=password + "a"))
