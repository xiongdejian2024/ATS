"""Add replay cursors/direct-task raw logs; existing suite history stays intact."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from database import engine
import models
from models.agent_log import AgentLogCursor, AgentTaskLog


def upgrade():
    AgentLogCursor.__table__.create(engine, checkfirst=True)
    AgentTaskLog.__table__.create(engine, checkfirst=True)


if __name__ == "__main__":
    upgrade()
