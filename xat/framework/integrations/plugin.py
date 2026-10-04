"""XAT 原生 pytest 插件：配置、fixture、选择与结果采集。"""

import json
import logging
import os
from pathlib import Path

import pytest

from .results import ATSResults
from .runtime import IntegrationSettings, SATRuntime

logger = logging.getLogger("xat.integrations")


def pytest_addoption(parser):
    group = parser.getgroup("xat-integration", "XAT 的 SAT / ECU 集成")
    group.addoption("--xat-mode", choices=["none", "offline", "sat", "hardware"], default="none")
    group.addoption("--sat-root")
    group.addoption("--ecu-root")
    group.addoption("--allow-hardware", action="store_true", default=None)
    group.addoption("--xat-bench-config")
    group.addoption("--xat-case-config")
    group.addoption("--xat-selection")
    group.addoption("--xat-results", default=None)


def _settings(config):
    return IntegrationSettings.from_environment(
        mode=config.getoption("xat_mode"),
        sat_root=config.getoption("sat_root"),
        ecu_root=config.getoption("ecu_root"),
        allow_hardware=config.getoption("allow_hardware"),
    )


def pytest_load_initial_conftests(early_config, parser, args):
    # 在 SAT conftest 导入设备模块前先校验开关及设置路径。
    try:
        _settings(early_config).prepare()
    except Exception as exc:
        logger.exception("XAT 集成启动失败")
        raise pytest.UsageError(str(exc)) from exc


def load_selection(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if isinstance(data, dict) and "case_codes" in data:
            codes, ids = data["case_codes"], data["case_ids"]
            if (
                not isinstance(codes, list)
                or not isinstance(ids, list)
                or len(codes) != len(ids)
                or len(set(codes)) != len(codes)
            ):
                raise ValueError("用例编号和 ID 必须一一对应，编号不可重复")
            data = dict(zip(codes, ids))
        if (
            not isinstance(data, dict)
            or not data
            or not all(
                isinstance(code, str) and code and isinstance(case_id, str) and case_id
                for code, case_id in data.items()
            )
        ):
            raise ValueError("选择文件必须包含非空的用例编号到 ID 映射")
        return data
    except Exception:
        logger.exception("读取 XAT 用例选择失败：%s", path)
        raise


def pytest_configure(config):
    try:
        settings = _settings(config)
        settings.prepare()
        config._xat_integration = settings
        selection_path = config.getoption("xat_selection") or os.environ.get(
            "ATS_CASE_SELECTION"
        )
        if not selection_path and Path("test_cases.json").is_file():
            selection_path = "test_cases.json"
        selection = load_selection(selection_path) if selection_path else None
        result_path = (
            config.getoption("xat_results")
            or os.environ.get("ATS_RESULT_FILE")
            or "test_results.json"
        )
        config.addinivalue_line("markers", "ats_case(code): XAT/ATS 用例编号")
        config.addinivalue_line("markers", "sat: 使用 SAT 框架")
        config.addinivalue_line("markers", "ecu: 使用 ECU Simulator")
        config.pluginmanager.register(
            ATSResults(selection, Path(result_path)), "xat-results"
        )
        # 新采集器统一处理全部阶段，避免旧采集器重复写入和提前报告成功。
        from framework.hooks import get_hook_registry

        registry = get_hook_registry()
        registry.unregister("TestCaseFilter")
        registry.unregister("TestReportLog")
        logger.info("XAT 结果输出：%s", result_path)
    except Exception as exc:
        logger.exception("配置 XAT 集成失败")
        raise pytest.UsageError(str(exc)) from exc


@pytest.fixture(scope="session")
def sat_runtime(pytestconfig):
    settings = pytestconfig._xat_integration
    if settings.mode == "none":
        raise ValueError("SAT fixture 需要 --xat-mode offline 或 sat")
    return SATRuntime(
        settings,
        pytestconfig.getoption("xat_bench_config"),
        pytestconfig.getoption("xat_case_config"),
    )


@pytest.fixture(scope="session")
def sat_types(sat_runtime):
    return sat_runtime.types


@pytest.fixture
def ecu_profile():
    """用例可覆盖为现有 SDK 的 IVehicleProfile 实例。"""
    return None


@pytest.fixture
def ecu_simulator(pytestconfig, ecu_profile):
    if pytestconfig._xat_integration.mode == "none":
        raise ValueError("ECU fixture 需要 --xat-mode offline 或 sat")
    try:
        from xat_ecu.services.simulator import SimulatorService

        simulator = SimulatorService(ecu_profile)
        logger.info("创建 ECU 模拟服务")
        yield simulator
    except Exception:
        logger.exception("ECU 模拟用例或资源清理失败")
        raise
    finally:
        if "simulator" in locals():
            try:
                simulator.stop_simulation()
                logger.info("ECU 模拟服务已清理")
            except Exception:
                logger.exception("ECU 模拟服务清理失败")
                raise


@pytest.fixture
def ecu_sdk_options():
    """台架用例须覆盖车型、版本、硬件和配置路径。"""
    return {}


@pytest.fixture
def ecu_sdk(pytestconfig, ecu_sdk_options):
    settings = pytestconfig._xat_integration
    if settings.mode not in {"sat", "hardware"} or not settings.allow_hardware:
        raise ValueError("完整 ECU SDK fixture 需要显式允许的台架模式")
    try:
        from xat_ecu import VehicleSDK

        with VehicleSDK(**ecu_sdk_options) as sdk:
            logger.info("创建 ECU SDK：%s", sdk)
            yield sdk
    except Exception:
        logger.exception("ECU SDK 初始化、用例或资源清理失败")
        raise
