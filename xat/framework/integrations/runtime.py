"""XAT 内部框架与库的运行配置，旧目录不参与源码加载。"""
import importlib
import logging
import os
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel

logger = logging.getLogger("xat.integrations")
_package_parent = Path(__file__).resolve().parents[2]
XAT_ROOT = _package_parent if _package_parent.name == "xat" else Path(os.environ.get("XAT_PROJECT_ROOT", Path.cwd())).resolve()
WORKSPACE = XAT_ROOT.parent


class IntegrationSettings(BaseModel):
    mode: Literal["none", "offline", "sat", "hardware"] = "none"
    # 兼容旧参数名，仅作为用户配置/用例资源根目录，绝不加入 sys.path。
    sat_root: Path = XAT_ROOT
    ecu_root: Path = XAT_ROOT / "packages/ecu"
    allow_hardware: bool = False

    @classmethod
    def from_environment(cls, **overrides):
        values = {
            "sat_root": os.environ.get("XAT_PROJECT_ROOT", XAT_ROOT),
            "allow_hardware": os.environ.get("XAT_ALLOW_HARDWARE", "false"),
        }
        values.update({key: value for key, value in overrides.items() if value is not None})
        return cls(**values)

    def prepare(self):
        if self.mode in {"sat", "hardware"} and not self.allow_hardware:
            raise ValueError("真实 XAT 台架执行已关闭（disabled），需要显式允许硬件")
        self.sat_root = self.sat_root.expanduser().resolve()
        # ecu-root 保留以兼容已保存的命令，不再控制库来源。
        self.ecu_root = XAT_ROOT / "packages/ecu"
        if self.mode != "none":
            importlib.import_module("framework.automotive.utils.data_type")
            importlib.import_module("xat_ecu")
        logger.info("XAT 初始化：模式=%s，资源根目录=%s", self.mode, self.sat_root)

    def sat_path(self, value):
        path = (self.sat_root / value).resolve()
        path.relative_to(self.sat_root)
        if not path.exists():
            raise ValueError(f"XAT 配置或用例路径不存在：{path}")
        return path


class XATRuntime:
    """加载迁入 XAT 的框架类型和配置；设备模块仍按需加载。"""
    def __init__(self, settings, bench_config=None, case_config=None):
        self.settings = settings
        self.types = self.module("utils.data_type")
        self.bench_config = self._read_yaml(bench_config)
        self.case_config = self._read_yaml(case_config)

    def module(self, name):
        if self.settings.mode not in {"sat", "hardware"} and name != "utils.data_type":
            raise ValueError("离线模式加载框架数据类型；设备 Hook 需要台架模式")
        try:
            return importlib.import_module("framework.automotive." + name)
        except Exception:
            logger.exception("加载 XAT 框架模块失败：%s", name)
            raise

    def _read_yaml(self, value):
        if not value:
            return {}
        path = self.settings.sat_path(value)
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("XAT YAML 配置必须是对象")
            logger.info("已读取 XAT 配置：%s", path)
            from xat_ecu.resources import resolve_environment
            return resolve_environment(data)
        except Exception:
            logger.exception("读取 XAT 配置失败：%s", path)
            raise


SATRuntime = XATRuntime  # 已有用例 fixture 的兼容名称。
