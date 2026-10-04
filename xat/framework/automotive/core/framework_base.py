"""XAT 原生 pytest 生命周期；设备执行 Hook 按需加载。"""
import logging
import os

import pytest
from framework.automotive.core.options import pytest_addoption as _add_options
from framework.automotive.fixture.fixture_base import FixtureBase
from framework.automotive.utils.data_type import EcuInfo

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    _add_options(parser)


def pytest_configure(config):
    mode = config.getoption('xat_mode', default='offline')
    allow = config.getoption('allow_hardware', default=False)
    if mode in {'sat', 'hardware'}:
        if not allow:
            raise pytest.UsageError('XAT 台架执行需要显式允许硬件')
        # 原设备/分布式 Hook 已迁入，只有明确设备模式才加载。
        from .hardware_engine import FrameworkBase
        engine = FrameworkBase()
        # 本入口已经注册选项，因此实例只接管配置及后续生命周期。
        config.pluginmanager.register(HardwareHookAdapter(engine), 'xat-automotive-hardware')
        engine.pytest_configure(config)
    try:
        from xat_ecu import reporting
    except ImportError:
        logger.info('未安装 ECU 库，pytest 生命周期不启用库报告接收器')
        return
    try:
        import allure
    except ImportError:
        logger.info('没有安装 Allure，库报告使用标准日志')
        config._xat_previous_reporter = reporting.set_reporter()
    else:
        config._xat_previous_reporter = reporting.set_reporter(allure)


def pytest_unconfigure(config):
    if hasattr(config, '_xat_previous_reporter'):
        from xat_ecu import reporting
        reporting.set_reporter(config._xat_previous_reporter)


class HardwareHookAdapter:
    """转发原框架设备和分布式 Hook；框架选项与库加载保持分离。"""
    def __init__(self, engine):
        self.engine = engine

    def __getattr__(self, name):
        if not name.startswith('pytest_') or name in {'pytest_addoption', 'pytest_configure'}:
            raise AttributeError(name)
        # 原函数的 fb 位于独立模块；替换为本次 pytest 会话实例。
        from . import hardware_engine
        hardware_engine.fb = self.engine
        return getattr(hardware_engine, name)

    def __dir__(self):
        from . import hardware_engine
        return list(set(super().__dir__()) | {name for name in dir(hardware_engine) if name.startswith('pytest_') and name not in {'pytest_addoption', 'pytest_configure'}})


@pytest.fixture(scope='session')
def ecu(request):
    """软件用例元数据；实际设备由用例按需申请独立 ECU 库 fixture。"""
    hardware = request.config.pluginmanager.get_plugin('xat-automotive-hardware')
    return hardware.engine.ecu(request) if hardware else EcuInfo()


@pytest.fixture(scope='module', autouse=True)
def case_module_hook(request, ecu):
    FixtureBase.case_module_hook(request, ecu)


@pytest.fixture(scope='class', autouse=True)
def case_class_hook(request, ecu):
    FixtureBase.case_class_hook(request, ecu)


@pytest.fixture(scope='function', autouse=True)
def case_function_hook(request, ecu):
    FixtureBase.case_function_hook(request, ecu)
