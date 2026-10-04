"""兼容旧 Agent 命令；结果实现统一归属 XAT。"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "xat"))
from framework.integrations.results import ATSResults


def pytest_configure(config):
    config.addinivalue_line("markers", "ats_case(code): XAT/ATS 用例编号")
    selection_path = os.environ.get("ATS_CASE_SELECTION")
    if selection_path:
        from framework.integrations.plugin import load_selection

        config.pluginmanager.register(
            ATSResults(
                load_selection(selection_path), Path(os.environ["ATS_RESULT_FILE"])
            )
        )
