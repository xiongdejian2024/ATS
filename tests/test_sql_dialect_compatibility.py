"""Query dialect coverage without contacting a configured external database.

Compilation checks supplement SQLite behavior tests; they do not substitute for
the PostgreSQL integration suite against an ephemeral server.
"""

from types import SimpleNamespace

import pytest
from sqlalchemy import create_mock_engine, literal, select
from sqlalchemy.dialects import mysql, postgresql, sqlite
from sqlalchemy.orm import Query, Session

from database import SessionLocal
from models.agent_log import AgentTaskLog
from models.case_governance import CaseReview, CaseReviewItem
from models.script_job import ScriptJobLog
from models.test_suite import TestSuiteLog as SuiteLog
from services.bounded_logs import log_window
from services.review_case_workspace import approved_vote
from services.review_workspace import summary_query
from services.sql_dialect import text_position, text_tail


@pytest.fixture(params=["sqlite", "mysql", "postgresql"])
def dialect_session(request):
    dialect = {
        "sqlite": sqlite.dialect(),
        "mysql": mysql.dialect(),
        "postgresql": postgresql.dialect(),
    }[request.param]
    # Mock engines compile SQL only and cannot connect to a real database.
    engine = create_mock_engine(f"{request.param}://", lambda *_args: None)
    with Session(bind=engine) as db:
        yield db, dialect


@pytest.mark.parametrize("model", [SuiteLog, AgentTaskLog, ScriptJobLog])
def test_tail_projection_uses_engine_specific_character_semantics(dialect_session, model, monkeypatch):
    db, dialect = dialect_session
    statements = []

    def capture(query):
        statements.append(query.statement)
        return []

    monkeypatch.setattr(Query, "all", capture)
    monkeypatch.setattr(Query, "scalar", lambda _query: 0)
    result = log_window(db.query(model), 0, 1000, 7, True, model=model)
    assert result == {"items": [], "total": 0, "skip": 0, "limit": 20}
    assert len(statements) == 1
    statement = statements[0]
    compiled = statement.compile(dialect=dialect)
    sql = str(compiled).lower()
    body_function = "right(" if dialect.name == "postgresql" else "substr("
    assert f"{model.__tablename__}.message" not in sql.split(body_function)[0]
    assert f"{model.__tablename__}.timestamp desc" in sql
    assert f"{model.__tablename__}.id desc" in sql
    if dialect.name == "postgresql":
        assert f"right({model.__tablename__}.message," in sql
        assert "substr(" not in sql
        assert 7 in compiled.params.values()
        assert -7 not in compiled.params.values()
    else:
        assert f"substr({model.__tablename__}.message," in sql
        assert -7 in compiled.params.values()


@pytest.mark.parametrize("value", ["", "短", "完整前段\n中文😀末尾", "e\u0301界🙂"])
@pytest.mark.parametrize("characters", [1, 3, 32768])
def test_sqlite_tail_remains_unicode_character_based(value, characters):
    with SessionLocal() as db:
        assert db.scalar(select(text_tail(db, literal(value), characters))) == value[-characters:]


@pytest.mark.parametrize(
    ("haystack", "needle", "position"),
    [
        ('["reviewer-10"]', '"reviewer-1"', 0),
        ('["reviewer-1", "reviewer-10"]', '"reviewer-1"', 2),
        ('["id_%", "中文😀"]', '"id_%"', 2),
        ('["id_%", "中文😀"]', '"中文😀"', 10),
    ],
)
def test_position_preserves_literal_exact_id_membership(haystack, needle, position):
    with SessionLocal() as db:
        assert db.scalar(select(text_position(db, literal(haystack), literal(needle)))) == position


@pytest.mark.parametrize("current_read", [False, True])
@pytest.mark.parametrize("review", [CaseReview, SimpleNamespace(reviewer_ids=["reviewer-1"])])
def test_review_approved_vote_compiles_correlated_membership(dialect_session, current_read, review):
    db, dialect = dialect_session
    statement = select(CaseReviewItem.id).where(approved_vote(db, review, current_read))
    sql = str(statement.compile(dialect=dialect)).lower()
    assert ("strpos(" if dialect.name == "postgresql" else "instr(") in sql
    assert "case_review_decisions.item_id = case_review_items.id" in sql
    assert "case_review_decisions.reviewer_id" in sql
    assert "case_review_decisions.decision =" in sql
    if dialect.name != "sqlite":
        assert ("for update" in sql) is current_read


def test_review_summary_rounds_numeric_on_postgresql(dialect_session):
    db, dialect = dialect_session
    query, _lifecycle, _rate = summary_query(db, "synthetic-project")
    sql = str(query.statement.compile(dialect=dialect)).lower()
    assert "round(" in sql and "nullif(" in sql
    if dialect.name == "postgresql":
        assert "round(cast(" in sql
        assert " as numeric)" in sql
        assert "instr(" not in sql
    else:
        assert "round(cast(" not in sql
