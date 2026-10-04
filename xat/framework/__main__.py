"""XAT 命令行入口，复用 pytest 而不自行实现测试引擎。"""

import argparse
import logging
import os
import sys
from pathlib import Path

import pytest

from .integrations.runtime import IntegrationSettings


def main(argv=None):
    parser = argparse.ArgumentParser(description="XAT 的 SAT / ECU 执行入口")
    parser.add_argument("--mode", choices=["offline", "sat"], default="offline")
    parser.add_argument("--sat-root")
    parser.add_argument("--ecu-root")
    parser.add_argument("--allow-hardware", action="store_true", default=None)
    parser.add_argument("--tests")
    parser.add_argument("--bench-config")
    parser.add_argument("--case-config")
    parser.add_argument("--selection")
    parser.add_argument("--output-dir", default="xat-results")
    options, extra = parser.parse_known_args(argv)
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
    )
    logger = logging.getLogger("xat.integrations")
    try:
        settings = IntegrationSettings.from_environment(
            mode=options.mode,
            sat_root=options.sat_root,
            ecu_root=options.ecu_root,
            allow_hardware=options.allow_hardware,
        )
        settings.prepare()
        directory = Path(options.output_dir).resolve()
        directory.mkdir(parents=True, exist_ok=True)
        os.environ["TEST_LOG_FILE_DIR"] = str(directory / "logs")
        os.environ["ALLURE_RESULTS_DIR"] = str(directory / "allure-results")
        test_path = (
            str(settings.sat_path(options.tests or "test_case"))
            if options.mode == "sat"
            else str(
                Path(options.tests).resolve()
                if options.tests
                else Path(__file__).parent / "integrations" / "offline_cases.py"
            )
        )
        args = [
            "-p",
            "framework.hooks",
            "-p",
            "framework.integrations.plugin",
            "--xat-mode",
            options.mode,
            "--sat-root",
            str(settings.sat_root),
            "--ecu-root",
            str(settings.ecu_root),
            "--xat-results",
            str(directory / "results.json"),
            "--junitxml",
            str(directory / "junit.xml"),
            "-o",
            "addopts=",
            "-p",
            "no:cacheprovider",
        ]
        if settings.allow_hardware:
            args.append("--allow-hardware")
        if options.selection:
            args += ["--xat-selection", str(Path(options.selection).resolve())]
        for flag, value in [
            ("--xat-bench-config", options.bench_config),
            ("--xat-case-config", options.case_config),
        ]:
            if value:
                args += [flag, str(settings.sat_path(value))]
        if options.mode == "offline":
            os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
            args += [
                "--noconftest",
                "-c",
                str(Path(__file__).parent / "integrations" / "pytest.ini"),
            ]
        else:
            args += [
                "-c",
                str(settings.sat_path("pytest.ini")),
                "--alluredir",
                str(directory / "allure-results"),
            ]
            for flag, value in [
                ("--tbcfg", options.bench_config),
                ("--tccfg", options.case_config),
            ]:
                if value:
                    args += [flag, str(settings.sat_path(value))]
        logger.info(
            "开始 XAT 执行：模式=%s，用例=%s，产物=%s",
            options.mode,
            test_path,
            directory,
        )
        return int(pytest.main(args + [test_path] + extra))
    except Exception:
        logger.exception("XAT 执行启动失败")
        return 2


if __name__ == "__main__":
    sys.exit(main())
