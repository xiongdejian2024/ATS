"""选择 XAT/ATS 用例，在全部阶段结束后原子写入结果。"""

import json
import os
from collections import Counter
from pathlib import Path

import pytest
import logging

logger = logging.getLogger("xat.integrations")


class ATSResults:
    def __init__(self, selection, result_path):
        self.selection = selection
        self.result_path = result_path
        self.rows = {}
        self.reports = {}
        self.mapping = {}
        self.selection_errors = False
        self.result_path.parent.mkdir(parents=True, exist_ok=True)
        self.flush()

    @pytest.hookimpl(trylast=True)
    def pytest_collection_modifyitems(self, config, items):
        selected, deselected, assigned = [], [], set()
        candidates_by_node = {}
        for item in items:
            marker = item.get_closest_marker("ats_case")
            if marker:
                candidates = [str(code) for code in marker.args]
            elif self.selection is not None and item.nodeid in self.selection:
                candidates = [item.nodeid]
            elif "[" in item.name:
                # SAT's case_info_helper treats the parametrized ID as the case ID.
                candidates = [item.name.split("[", 1)[1].rsplit("]", 1)[0]]
            elif "_caseid_" in item.name:
                suffix = item.name.rsplit("_caseid_", 1)[1]
                # Preserve named offline codes; SAT also maps a method to several numeric IDs.
                candidates = (
                    [suffix]
                    if not suffix.replace("_", "").isdigit()
                    or (self.selection is not None and suffix in self.selection)
                    else suffix.split("_")
                )
            else:
                candidates = [item.nodeid]
            candidates_by_node[item.nodeid] = candidates
        counts = Counter(
            code for codes in candidates_by_node.values() for code in codes
        )
        for item in items:
            candidates = candidates_by_node[item.nodeid]
            # 全量执行时普通参数化 ID 可能重复，用完整 node ID 保存独立结果。
            if self.selection is None and any(counts[code] > 1 for code in candidates):
                candidates = [item.nodeid]
            codes = (
                candidates
                if self.selection is None
                else [code for code in candidates if code in self.selection]
            )
            if codes:
                if assigned.intersection(codes):
                    self.selection_errors = True
                    raise pytest.UsageError(
                        "所选用例编号对应多个测试，请使用唯一的完整 node ID"
                    )
                assigned.update(codes)
                self.mapping[item.nodeid] = codes
                selected.append(item)
            else:
                deselected.append(item)
        items[:] = selected
        config.hook.pytest_deselected(items=deselected)

    def pytest_runtest_logreport(self, report):
        codes = self.mapping.get(report.nodeid)
        if codes is None:
            return
        phases = self.reports.setdefault(report.nodeid, {})
        phases[report.when] = report
        if report.when != "teardown":
            return
        failed = [p for p in phases.values() if p.failed]
        skipped = [p for p in phases.values() if p.skipped]
        status = (
            "error"
            if any(p.when != "call" for p in failed)
            else ("failed" if failed else "skipped" if skipped else "passed")
        )
        for code in codes:
            self.rows[code] = {
                "test_name": report.nodeid,
                "case_code": code,
                "case_id": self.selection[code] if self.selection is not None else None,
                "status": status,
                "duration": sum(p.duration for p in phases.values()),
                "error": "\n".join(str(p.longrepr) for p in failed + skipped) or None,
                "log": "\n".join(
                    [
                        f"{p.when}: {p.outcome} ({p.duration:.3f}s)"
                        for p in phases.values()
                    ]
                    + list(
                        dict.fromkeys(
                            text for p in phases.values() for _, text in p.sections
                        )
                    )
                ),
            }
        logger.info("XAT 用例结束：%s，状态=%s", report.nodeid, status)
        self.flush()

    def pytest_sessionfinish(self, session, exitstatus):
        for code, case_id in (self.selection or {}).items():
            if code not in self.rows:
                self.rows[code] = {
                    "test_name": code,
                    "case_code": code,
                    "case_id": case_id,
                    "status": "error",
                    "duration": 0,
                    "error": f"所选用例未完成（pytest 退出码 {int(exitstatus)}）",
                }
        if self.selection_errors or any(
            row["status"] == "error" for row in self.rows.values()
        ):
            if session.exitstatus == 0:
                session.exitstatus = pytest.ExitCode.TESTS_FAILED
        self.flush()

    def flush(self):
        try:
            temporary = self.result_path.with_suffix(".tmp")
            temporary.write_text(
                json.dumps(list(self.rows.values()), ensure_ascii=False),
                encoding="utf-8",
            )
            os.replace(temporary, self.result_path)
        except Exception:
            logger.exception("写入 XAT 结果失败：%s", self.result_path)
            raise
