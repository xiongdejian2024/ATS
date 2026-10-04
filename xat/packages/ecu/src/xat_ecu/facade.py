"""
VehicleSDK Facade - SDK 统一入口

替代原有的 ecuinterface.py，提供所有功能的统一访问入口。
所有子服务通过 Lazy 初始化，按需创建。
"""

import logging
from typing import Any, Optional

from xat_ecu.config.manager import ConfigManager
from xat_ecu.core.interfaces import IHardwareAdapter, IVehicleProfile
from xat_ecu.hal.factory import HardwareFactory
from xat_ecu.services.bus import BusService
from xat_ecu.services.diagnostic import DiagnosticService
from xat_ecu.services.flash import FlashService
from xat_ecu.services.signal import SignalService
from xat_ecu.services.simulator import SimulatorService

logger = logging.getLogger(__name__)


class VehicleSDK:
    """
    Automotive SDK 统一入口

    通过 Lazy 初始化和依赖注入，整合所有子服务：
    - diagnostic: UDS 诊断服务
    - flash: ECU 刷写服务
    - bus: 总线消息收发服务
    - signal: 信号级操作服务
    - simulator: ECU 模拟服务

    Usage:
        with VehicleSDK("mars1", "v_3_0_0", hardware="socketcan") as sdk:
            sdk.diagnostic.connect("BGM")
            resp = sdk.diagnostic.read_did(0xF190)
    """

    def __init__(self, vehicle_type: str, version: str,
                 config_path: str = None, hardware: str = "socketcan",
                 **kwargs: Any):
        self.vehicle_type = vehicle_type
        self.version = version
        self.hardware = hardware

        # 配置管理
        config_dir = kwargs.pop("config_dir", None)
        self._transport_factory = kwargs.pop("transport_factory", None)
        self._hardware_factory = kwargs.pop("hardware_factory", None)
        profile = kwargs.pop("profile", None)
        self._config_manager = ConfigManager(config_dir)
        if config_path:
            self._config_manager.load_testbed_config(config_path)

        # 车型配置
        self._registry = self._config_manager.vehicle_registry
        self._profile: Optional[IVehicleProfile] = profile
        if self._profile is None:
            try:
                self._profile = self._registry.load(vehicle_type, version)
            except Exception:
                logger.exception("加载 XAT 车型配置失败：%s/%s", vehicle_type, version)
                raise

        # 硬件工厂函数
        self._hardware_name = hardware
        self._extra_config = kwargs

        # Lazy-init 子服务
        self._diagnostic: Optional[DiagnosticService] = None
        self._flash: Optional[FlashService] = None
        self._bus: Optional[BusService] = None
        self._signal: Optional[SignalService] = None
        self._simulator: Optional[SimulatorService] = None

    # ============================================================
    # 工厂方法
    # ============================================================

    def _create_hardware(self, **config: Any) -> IHardwareAdapter:
        """通过 HardwareFactory 创建硬件适配器"""
        merged = {**self._extra_config, **config}
        if self._hardware_factory:
            return self._hardware_factory(self._hardware_name, **merged)
        return HardwareFactory.create(self._hardware_name, **merged)

    def _create_transport(self, transport_type: str = "can",
                          **config: Any) -> Any:
        """创建传输层实例"""
        if self._transport_factory:
            return self._transport_factory(transport_type=transport_type, **config)
        if transport_type == "can":
            from xat_ecu.transport.can import CANTransport
            return CANTransport(self._create_hardware(**config))
        elif transport_type == "doip":
            from xat_ecu.protocol.doip.client import DoipClient
            return DoipClient()
        elif transport_type == "docan":
            from xat_ecu.protocol.docan.client import DocanClient
            return DocanClient(self._create_hardware(**config))
        else:
            raise ValueError(f"未知传输类型：{transport_type}")

    # ============================================================
    # 子服务属性 (Lazy Init)
    # ============================================================

    @property
    def diagnostic(self) -> DiagnosticService:
        """诊断服务"""
        if self._diagnostic is None:
            self._diagnostic = DiagnosticService(
                self._profile,
                self._create_transport,
            )
        return self._diagnostic

    @property
    def flash(self) -> FlashService:
        """刷写服务"""
        if self._flash is None:
            self._flash = FlashService(self.diagnostic)
        return self._flash

    @property
    def bus(self) -> BusService:
        """总线管理服务"""
        if self._bus is None:
            self._bus = BusService(self._profile, self._create_hardware)
        return self._bus

    @property
    def signal(self) -> SignalService:
        """信号操作服务"""
        if self._signal is None:
            self._signal = SignalService(self._profile, self.bus)
        return self._signal

    @property
    def simulator(self) -> SimulatorService:
        """ECU 模拟服务"""
        if self._simulator is None:
            self._simulator = SimulatorService(self._profile)
        return self._simulator

    @property
    def config(self) -> ConfigManager:
        """配置管理器"""
        return self._config_manager

    @property
    def profile(self) -> Optional[IVehicleProfile]:
        """当前车型配置"""
        return self._profile

    # ============================================================
    # 生命周期管理
    # ============================================================

    def close(self) -> None:
        """清理所有资源"""
        logger.info("清理 XAT ECU SDK 资源")
        errors = []
        for resource, method in [(self._diagnostic, "disconnect"), (self._bus, "close"), (self._simulator, "stop_simulation")]:
            if resource:
                try:
                    getattr(resource, method)()
                except Exception as exc:
                    logger.exception("清理 XAT ECU 资源失败：%s", method)
                    errors.append(exc)
        if errors:
            raise errors[0]
        logger.info("XAT ECU SDK 资源已清理")

    def __enter__(self) -> "VehicleSDK":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def __repr__(self) -> str:
        return (
            f"VehicleSDK(vehicle_type='{self.vehicle_type}', "
            f"version='{self.version}', hardware='{self.hardware}')"
        )
