"""Create the first ATS administrator with explicit credentials and one transaction.

This is an operator-run bootstrap, never a password-reset or account-promotion tool.
Database imports are deferred until input validation succeeds.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import getpass
import os
from pathlib import Path
import re
import sys
from typing import TYPE_CHECKING
import warnings

from email_validator import EmailNotValidError, validate_email

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from models import Permission, Role, User

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


class BootstrapError(ValueError):
    """Only fixed, safe-to-display messages belong in this exception."""


@dataclass(frozen=True)
class AdminCredentials:
    username: str
    email: str
    password: str = field(repr=False)
    full_name: str = "系统管理员"


def validate_identity(username: str, email: str, full_name: str) -> str:
    if not isinstance(username, str) or not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9_.-]{2,49}", username
    ):
        raise BootstrapError(
            "Specify a username of 3–50 letters, digits, dots, underscores or hyphens."
        )
    try:
        if not isinstance(email, str) or len(email) > 100:
            raise EmailNotValidError("Invalid email")
        normalized_email = validate_email(email, check_deliverability=False).normalized
        if len(normalized_email) > 100 or email != email.strip():
            raise EmailNotValidError("Invalid email")
    except EmailNotValidError:
        raise BootstrapError("Specify a valid email address of at most 100 characters.") from None
    if (
        not isinstance(full_name, str)
        or not full_name.strip()
        or len(full_name) > 100
        or not full_name.isprintable()
    ):
        raise BootstrapError("Full name must be printable text of 1–100 characters.")
    return normalized_email


def validate_credentials(credentials: AdminCredentials) -> AdminCredentials:
    email = validate_identity(credentials.username, credentials.email, credentials.full_name)
    password = credentials.password
    if not isinstance(password, str) or len(password) < 16 or len(password.encode("utf-8")) > 72:
        raise BootstrapError(
            "Password must have at least 16 characters and at most 72 UTF-8 bytes."
        )
    classes = sum(
        (
            any(c.islower() for c in password),
            any(c.isupper() for c in password),
            any(c.isdigit() for c in password),
            any(not c.isalnum() for c in password),
        )
    )
    forbidden = ("password", "qwerty", "admin123", "letmein", "changeme", "12345678")
    identity_parts = (credentials.username.casefold(), email.split("@", 1)[0].casefold())
    if (
        not password.isprintable()
        or password != password.strip()
        or classes < 3
        or len(set(password)) < 8
        or any(part in password.casefold() for part in forbidden)
        or any(len(part) >= 3 and part in password.casefold() for part in identity_parts)
    ):
        raise BootstrapError(
            "Use a unique password with at least three character types; avoid common passwords and account names."
        )
    return AdminCredentials(credentials.username, email, password, credentials.full_name)


def read_credentials(args: argparse.Namespace) -> AdminCredentials:
    # Remove the one-shot secret from this process's environment before imports.
    # This cannot remove a value exported by the parent shell or host configuration.
    password = os.environ.pop("ADMIN_PASSWORD", None)
    username = args.username if args.username is not None else os.environ.get("ADMIN_USERNAME", "")
    email = args.email if args.email is not None else os.environ.get("ADMIN_EMAIL", "")
    full_name = (
        args.full_name
        if args.full_name is not None
        else os.environ.get("ADMIN_FULL_NAME", "系统管理员")
    )
    email = validate_identity(username, email, full_name)
    if password is None:
        if not sys.stdin.isatty():
            raise BootstrapError(
                "No password supplied. Use an interactive terminal or one-shot ADMIN_PASSWORD secret injection."
            )
        try:
            with warnings.catch_warnings():
                # getpass normally falls back to echoing stdin without a terminal.
                # Fail closed instead, before that fallback can read a password.
                warnings.simplefilter("error", getpass.GetPassWarning)
                password = getpass.getpass("New administrator password: ")
                confirmation = getpass.getpass("Confirm password: ")
        except (getpass.GetPassWarning, EOFError):
            raise BootstrapError(
                "Hidden password entry is unavailable; use one-shot ADMIN_PASSWORD secret injection."
            ) from None
        if password != confirmation:
            raise BootstrapError("Passwords do not match.")
    return validate_credentials(AdminCredentials(username, email, password, full_name))


def init_permissions(db: Session) -> dict[str, Permission]:
    """Idempotently add missing permissions; the caller owns the transaction."""
    from core.permissions import SYSTEM_PERMISSIONS
    from models import Permission

    permissions = {}
    for code, name in SYSTEM_PERMISSIONS.items():
        permission = db.query(Permission).filter(Permission.code == code).first()
        if permission is None:
            resource, action = code.split(":", 1)
            permission = Permission(
                code=code, name=name, resource=resource, action=action, description=f"{name}权限"
            )
            db.add(permission)
        permissions[code] = permission
    db.flush()
    return permissions


def system_roles() -> dict:
    """The original role definitions, loaded after credential validation."""
    from core.permissions import SYSTEM_PERMISSIONS

    return {
        "admin": {
            "name": "系统管理员",
            "description": "拥有所有系统权限的管理员角色",
            "permissions": list(SYSTEM_PERMISSIONS.keys()),
        }
    }


def init_roles(db: Session, permissions: dict[str, Permission]) -> dict[str, Role]:
    """Initialize every defined system role; the caller owns the transaction."""
    from models import Role, RolePermission

    roles = {}
    for role_name, definition in system_roles().items():
        role = db.query(Role).filter(Role.name == role_name).first()
        if role is None:
            role = Role(
                name=role_name,
                display_name=definition["name"],
                is_system=True,
                description=definition.get("description", ""),
            )
            db.add(role)
            db.flush()
        elif not role.is_system:
            raise BootstrapError(
                "An existing non-system role conflicts with bootstrap; review it manually."
            )
        for code in definition["permissions"]:
            if code not in permissions:
                raise BootstrapError(
                    "A system role references a missing permission; review role configuration."
                )
            permission = permissions[code]
            grant = (
                db.query(RolePermission)
                .filter(
                    RolePermission.role_id == role.id, RolePermission.permission_id == permission.id
                )
                .first()
            )
            if grant is None:
                db.add(RolePermission(role_id=role.id, permission_id=permission.id))
        roles[role_name] = role
    db.flush()
    return roles


def require_empty_users(db: Session) -> None:
    from models import User

    if db.query(User.id).first() is not None:
        raise BootstrapError(
            "Bootstrap refused: users already exist. Use the authenticated account-management or recovery workflow."
        )


def create_admin_user(
    db: Session, username: str, email: str, password: str, full_name: str = "系统管理员"
) -> User:
    """Insert only a new first user; no defaults, promotion, reset or commit.

    Use bootstrap_admin for the locked, atomic operator workflow. This helper
    expects its caller to hold the bootstrap lock and own the transaction.
    """
    credentials = validate_credentials(AdminCredentials(username, email, password, full_name))
    from core.security import get_password_hash
    from models import Role, User, UserRole

    require_empty_users(db)
    role = db.query(Role).filter(Role.name == "admin", Role.is_system.is_(True)).first()
    if role is None:
        raise BootstrapError("System administrator role is missing; initialize roles first.")
    user = User(
        username=credentials.username,
        email=credentials.email,
        password_hash=get_password_hash(credentials.password),
        full_name=credentials.full_name,
        status=True,
    )
    db.add(user)
    db.flush()
    db.add(UserRole(user_id=user.id, role_id=role.id))
    db.flush()
    return user


def bootstrap_admin(db: Session, credentials: AdminCredentials) -> None:
    """Serialize the empty-user check and commit all bootstrap writes together."""
    credentials = validate_credentials(credentials)
    from sqlalchemy import text

    if db.in_transaction():
        raise BootstrapError("Bootstrap requires a fresh database session.")
    dialect = db.get_bind().dialect.name
    if dialect not in {"postgresql", "sqlite"}:
        raise BootstrapError(
            "Safe first-admin bootstrap supports PostgreSQL and SQLite only; this database was not changed."
        )
    with db.begin():
        if dialect == "postgresql":
            # Empty SELECT FOR UPDATE cannot lock future rows. This lock also
            # blocks ordinary concurrent user inserts until commit or rollback.
            db.execute(text("SET LOCAL lock_timeout = '10s'"))
            db.execute(text("LOCK TABLE users IN SHARE ROW EXCLUSIVE MODE"))
        else:
            db.execute(text("BEGIN IMMEDIATE"))
        require_empty_users(db)
        permissions = init_permissions(db)
        init_roles(db, permissions)
        create_admin_user(
            db, credentials.username, credentials.email, credentials.password, credentials.full_name
        )


def open_session() -> Session:
    from database import SessionLocal

    return SessionLocal()


class SafeArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        # argparse's default error includes unknown arguments, potentially a
        # mistakenly supplied password. Never echo rejected arguments.
        self.exit(
            2, "Invalid arguments. Use --help; never pass passwords as command-line arguments.\n"
        )


def main(argv: list[str] | None = None) -> int:
    parser = SafeArgumentParser(
        description="Create the first administrator in an initialized, empty ATS user database."
    )
    parser.add_argument("--username", help="Explicit login name (or ADMIN_USERNAME)")
    parser.add_argument("--email", help="Explicit email address (or ADMIN_EMAIL)")
    parser.add_argument("--full-name", help="Display name (or ADMIN_FULL_NAME)")
    args = parser.parse_args(argv)
    try:
        credentials = read_credentials(args)
        with open_session() as db:
            bootstrap_admin(db, credentials)
    except BootstrapError as error:
        print(f"Administrator bootstrap refused: {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Administrator bootstrap cancelled.", file=sys.stderr)
        return 1
    except Exception:
        # Driver/configuration/SQL errors may contain connection strings, SQL
        # parameters or hashes. Do not print their text or a traceback.
        print(
            "Administrator bootstrap failed. Check database configuration, schema and account state before retrying; error details are withheld to protect secrets.",
            file=sys.stderr,
        )
        return 1
    print("First administrator created successfully. Use the credentials you supplied to sign in.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
