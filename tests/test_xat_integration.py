"""真实 XAT 子进程验收；不加载台架 Hook、不连接设备。"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def run_xat(tmp_path, *args, native=False):
    env = dict(
        os.environ,
        PYTHONPATH=str(ROOT / "xat"),
        TEST_LOG_FILE_DIR=str(tmp_path / "logs"),
        ALLURE_RESULTS_DIR=str(tmp_path / "allure"),
    )
    for key in ("ATS_CASE_SELECTION", "ATS_RESULT_FILE", "XAT_ALLOW_HARDWARE"):
        env.pop(key, None)
    command = [sys.executable, "-m", "pytest" if native else "framework"]
    if native:
        command += ["-o", "addopts=", "--xat-results", str(tmp_path / "results.json")]
    else:
        command += ["--output-dir", str(tmp_path)]
    result = subprocess.run(
        command + list(args),
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    path = tmp_path / "results.json"
    rows = json.loads(path.read_text()) if path.exists() else []
    return result, rows


def test_xat_original_examples_report_actual_failure(tmp_path):
    """原示例不改，原 conftest 加载新插件并准确报告一个失败。"""
    result, rows = run_xat(
        tmp_path, str(ROOT / "xat/tests/test_example.py"), native=True
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert len(rows) == 3
    assert {row["case_code"]: row["status"] for row in rows} == {
        "853873": "passed",
        "144943": "failed",
        "144163": "passed",
    }
    assert "总测试数: 3" in result.stdout


def test_xat_hardware_gate_is_checked_before_imports(tmp_path):
    result, rows = run_xat(
        tmp_path, "--mode", "sat", "--sat-root", str(tmp_path / "missing-sat")
    )
    assert result.returncode == 2
    assert "真实 SAT 台架执行已关闭" in result.stderr
    assert "Traceback" in result.stderr
    assert not rows


def test_xat_selection_missing_case_fails_and_teardown_is_recorded(tmp_path):
    source = tmp_path / "test_phases.py"
    source.write_text("""import pytest
@pytest.fixture
def broken_cleanup():
    yield
    raise RuntimeError("清理失败")
def test_caseid_good(): assert True
def test_caseid_cleanup(broken_cleanup): assert True
def test_caseid_not_selected(): assert False
""")
    selection = tmp_path / "selection.json"
    selection.write_text(
        json.dumps({code: code + "-id" for code in ["good", "cleanup", "missing"]})
    )
    # 不需要外部源码，直接使用 XAT 插件验证真实 pytest 生命周期。
    result, rows = run_xat(
        tmp_path,
        "-p",
        "framework.hooks",
        "-p",
        "framework.integrations.plugin",
        "--noconftest",
        "--xat-selection",
        str(selection),
        str(source),
        native=True,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert {row["case_code"]: row["status"] for row in rows} == {
        "good": "passed",
        "cleanup": "error",
        "missing": "error",
    }
    assert "清理失败" in next(
        row["error"] for row in rows if row["case_code"] == "cleanup"
    )


def test_xat_missing_selection_does_not_return_success(tmp_path):
    source = tmp_path / "test_missing.py"
    source.write_text("def test_caseid_good(): assert True\n")
    selection = tmp_path / "selection.json"
    selection.write_text(json.dumps({"good": "id", "missing": "missing-id"}))
    result, rows = run_xat(
        tmp_path,
        "-p",
        "framework.hooks",
        "-p",
        "framework.integrations.plugin",
        "--noconftest",
        "--xat-selection",
        str(selection),
        str(source),
        native=True,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert {row["status"] for row in rows} == {"passed", "error"}


def test_xat_invalid_selection_rejected(tmp_path):
    selection = tmp_path / "selection.json"
    selection.write_text('{"case_codes": ["001", "001"], "case_ids": ["id1", "id2"]}')
    result, rows = run_xat(
        tmp_path,
        "-p",
        "framework.integrations.plugin",
        "--noconftest",
        "--xat-selection",
        str(selection),
        native=True,
    )
    assert result.returncode == 4
    assert "编号不可重复" in result.stderr


def test_xat_full_run_preserves_repeated_parameter_names(tmp_path):
    source = tmp_path / "test_parameters.py"
    source.write_text("""import pytest
@pytest.mark.parametrize("value", [1, 2], ids=["good", "bad"])
def test_alpha(value): assert value == 1
@pytest.mark.parametrize("value", [1, 2], ids=["good", "bad"])
def test_beta(value): assert value == 1
""")
    result, rows = run_xat(
        tmp_path,
        "-p",
        "framework.hooks",
        "-p",
        "framework.integrations.plugin",
        "--noconftest",
        str(source),
        native=True,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert len(rows) == 4
    assert len({row["case_code"] for row in rows}) == 4
    assert sorted(row["status"] for row in rows) == [
        "failed",
        "failed",
        "passed",
        "passed",
    ]


@pytest.mark.xat_external
def test_xat_cli_uses_real_sat_ecu_fixtures_and_cleans_each_case(tmp_path, sat_config):
    result, rows = run_xat(
        tmp_path,
        "--mode",
        "offline",
        "--sat-root",
        sat_config.sat_root,
        "--ecu-root",
        sat_config.ecu_root,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert len(rows) == 4 and all(row["status"] == "passed" for row in rows)
    assert "XAT测试框架启动" in result.stdout
    assert "总测试数: 4" in result.stdout
    assert (tmp_path / "junit.xml").exists()
    source = tmp_path / "test_lifecycle.py"
    source.write_text("""import pytest
def test_caseid_first(ecu_simulator, pytestconfig, sat_runtime):
    assert "sat_framework/utils/data_type.py" in sat_runtime.types.__file__.replace("\\\\", "/")
    assert "automotive_sdk.services.simulator" == type(ecu_simulator).__module__
    ecu_simulator.start_simulation(ecus=["ECU"])
    pytestconfig.previous_simulator = ecu_simulator
    with pytest.raises(ValueError, match="台架模式"):
        sat_runtime.module("core.framework_base")
def test_caseid_second(ecu_simulator, pytestconfig):
    assert not pytestconfig.previous_simulator.is_running
    assert pytestconfig.previous_simulator.get_simulated_ecus() == []
    assert ecu_simulator is not pytestconfig.previous_simulator
def test_caseid_sdk(ecu_sdk): pass
""")
    run_dir = tmp_path / "custom"
    run_dir.mkdir()
    result, rows = run_xat(
        run_dir,
        "--mode",
        "offline",
        "--sat-root",
        sat_config.sat_root,
        "--ecu-root",
        sat_config.ecu_root,
        "--tests",
        str(source),
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert {row["case_code"]: row["status"] for row in rows} == {
        "first": "passed",
        "second": "passed",
        "sdk": "error",
    }
