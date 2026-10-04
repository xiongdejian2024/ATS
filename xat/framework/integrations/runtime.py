"""配置源码路径，按需加载现有 SAT 和 ECU 实现。"""

import importlib
import logging
import os
import sys
from pathlib import Path

import yaml
from pydantic import BaseModel
from typing import Literal

logger = logging.getLogger("xat.integrations")
_package_parent = Path(__file__).resolve().parents[2]
_current_directory = Path.cwd()
WORKSPACE = (
    _package_parent.parent
    if _package_parent.name == "xat"
    else (
        _current_directory.parent
        if _current_directory.name == "xat"
        else _current_directory
    )
)


class IntegrationSettings(BaseModel):
    mode: Literal["none", "offline", "sat"] = "none"
    sat_root: Path = WORKSPACE.parent / "sat"
    ecu_root: Path = WORKSPACE.parent / "ecu-simulator"
    allow_hardware: bool = False

    @classmethod
    def from_environment(cls, **overrides):
        values = {
            "sat_root": os.environ.get(
                "XAT_SAT_ROOT",
                os.environ.get("ATS_SAT_ROOT", cls.model_fields["sat_root"].default),
            ),
            "ecu_root": os.environ.get(
                "XAT_ECU_ROOT",
                os.environ.get("ATS_ECU_ROOT", cls.model_fields["ecu_root"].default),
            ),
            "allow_hardware": os.environ.get("XAT_ALLOW_HARDWARE", "false"),
        }
        values.update(
            {key: value for key, value in overrides.items() if value is not None}
        )
        return cls(**values)

    def prepare(self):
        if self.mode == "none":
            return
        if self.mode == "sat" and not self.allow_hardware:
            raise ValueError("真实 SAT 台架执行已关闭（disabled），需要显式允许硬件")
        self.sat_root = self.sat_root.expanduser().resolve()
        self.ecu_root = self.ecu_root.expanduser().resolve()
        required = [
            self.sat_root / "sat_framework",
            self.ecu_root / "src" / "automotive_sdk",
        ]
        if self.mode == "sat":
            required.append(self.ecu_root / "ecu_simulator")
        for directory in required:
            if not directory.is_dir():
                raise ValueError(f"集成源码目录不存在：{directory}")
        paths = [self.sat_root, self.ecu_root / "src", self.ecu_root]
        for path in reversed(paths):
            if str(path) not in sys.path:
                sys.path.insert(0, str(path))
        logger.info(
            "XAT 集成初始化：模式=%s，SAT=%s，ECU=%s",
            self.mode,
            self.sat_root,
            self.ecu_root,
        )

    def sat_path(self, value):
        path = (self.sat_root / value).resolve()
        path.relative_to(self.sat_root)
        if not path.exists():
            raise ValueError(f"SAT 配置或用例路径不存在：{path}")
        return path


class SATRuntime:
    """供 XAT 用例访问原 SAT 数据类型和配置，台架模块按需导入。"""

    def __init__(self, settings, bench_config=None, case_config=None):
        self.settings = settings
        self.types = self.module("utils.data_type")
        self.bench_config = self._read_yaml(bench_config)
        self.case_config = self._read_yaml(case_config)

    def module(self, name):
        if self.settings.mode != "sat" and name != "utils.data_type":
            raise ValueError("离线模式仅加载 SAT 数据类型；其他 SAT 模块需要台架模式")
        try:
            return importlib.import_module("sat_framework." + name)
        except Exception:
            logger.exception("加载 SAT 模块失败：%s", name)
            raise

    def _read_yaml(self, value):
        if not value:
            return {}
        path = self.settings.sat_path(value)
        try:
            with path.open(encoding="utf-8") as source:
                data = yaml.safe_load(source)
            if not isinstance(data, dict):
                raise ValueError("SAT YAML 配置必须是对象")
            logger.info("已读取 SAT 配置：%s", path)
            return data
        except Exception:
            logger.exception("读取 SAT 配置失败：%s", path)
            raise
