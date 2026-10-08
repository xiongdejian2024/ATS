"""Offline export regression checks. Real PG validation has a separate guard."""

import os
from pathlib import Path
import subprocess
import sys

import pytest
from sqlalchemy import MetaData, Table, Column, Integer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import export_postgres_schema as exporter


def test_checked_in_export_is_deterministic_and_independent_of_database_settings(tmp_path):
    expected = (ROOT / "deploy/postgres_schema.sql").read_bytes()
    for seed in ("1", "867", "random"):
        destination = tmp_path / f"schema-{seed}.sql"
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/export_postgres_schema.py"), "--output", str(destination)],
            env={**os.environ, "PYTHONHASHSEED": seed,
                 "DATABASE_URL": "not-a-database-url", "DATABASE_SCHEMA": "public",
                 "ENVIRONMENT": "production"},
            capture_output=True, text=True, check=True,
        )
        assert "92 model tables" in result.stdout
        assert destination.read_bytes() == expected


def test_export_never_imports_settings_or_opens_a_socket(tmp_path):
    destination = tmp_path / "offline.sql"
    result = subprocess.run(
        [sys.executable, "-c", "\n".join([
            "import sys",
            f"sys.path.insert(0, {str(ROOT / 'scripts')!r})",
            "def audit(event, args):",
            "    if event == 'socket.__new__': raise AssertionError('opened a network socket')",
            "sys.addaudithook(audit)",
            "import export_postgres_schema as exporter",
            f"exporter.main(['--output', {str(destination)!r}])",
            "assert 'config' not in sys.modules",
            "assert not hasattr(sys.modules['database'], 'engine')",
        ])], capture_output=True, text=True, check=True,
    )
    assert "92 model tables" in result.stdout


def test_model_count_and_source_schema_changes_require_review():
    with pytest.raises(ValueError, match="model count changed"):
        exporter.render_schema(MetaData())
    metadata = MetaData()
    for number in range(92):
        Table(f"example_{number}", metadata, Column("id", Integer, primary_key=True), schema="public")
    with pytest.raises(ValueError, match="another schema"):
        exporter.render_schema(metadata)


def test_check_mode_detects_stale_artifact_without_overwriting(tmp_path):
    destination = tmp_path / "stale.sql"
    destination.write_text("sentinel", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/export_postgres_schema.py"), "--check", "--output", str(destination)],
        capture_output=True, text=True,
    )
    assert result.returncode == 1
    assert destination.read_text(encoding="utf-8") == "sentinel"
