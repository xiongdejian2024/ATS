"""
Core module - 核心抽象层

提供 SDK 所有模块依赖的基础抽象接口、类型定义、异常体系、
事件总线和插件注册机制。
"""

from xat_ecu.core.interfaces import (
    IHardwareAdapter,
    ITransport,
    IDiagnosticClient,
    IDiagnosticServer,
    IVehicleProfile,
    ICredentialProvider,
    ISignalDatabase,
)
from xat_ecu.core.types import (
    BusType,
    DiagMode,
    MessageDirection,
    BusMessage,
    DiagRequest,
    DiagResponse,
    SignalValue,
    EcuInfo,
    VehicleConfig,
)
from xat_ecu.core.errors import (
    AutomotiveSDKError,
    ConnectionError,
    TimeoutError,
    ProtocolError,
    ConfigurationError,
    HardwareError,
    SecurityAccessError,
)
from xat_ecu.core.events import EventBus, Event
from xat_ecu.core.plugin import PluginRegistry

__all__ = [
    # Interfaces
    "IHardwareAdapter",
    "ITransport",
    "IDiagnosticClient",
    "IDiagnosticServer",
    "IVehicleProfile",
    "ICredentialProvider",
    "ISignalDatabase",
    # Types
    "BusType",
    "DiagMode",
    "MessageDirection",
    "BusMessage",
    "DiagRequest",
    "DiagResponse",
    "SignalValue",
    "EcuInfo",
    "VehicleConfig",
    # Errors
    "AutomotiveSDKError",
    "ConnectionError",
    "TimeoutError",
    "ProtocolError",
    "ConfigurationError",
    "HardwareError",
    "SecurityAccessError",
    # Events & Plugins
    "EventBus",
    "Event",
    "PluginRegistry",
]
