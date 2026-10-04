"""
Core Errors - 统一异常体系

替代原有散布在 common/error_code.py、common/exception_error.py、
framework/exception/ 等处的重复异常定义。
"""

from typing import Optional


class AutomotiveSDKError(Exception):
    """SDK 根异常类"""

    def __init__(self, message: str = "", code: Optional[int] = None):
        self.code = code
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


# ============================================================
# Connection & Hardware Errors
# ============================================================

class ConnectionError(AutomotiveSDKError):
    """连接错误 - 无法连接到设备或 ECU"""
    pass


class HardwareError(AutomotiveSDKError):
    """硬件错误 - 硬件设备操作失败"""
    pass


class HardwareNotFoundError(HardwareError):
    """硬件设备未找到"""
    pass


class HardwareInitError(HardwareError):
    """硬件初始化失败"""
    pass


# ============================================================
# Communication & Protocol Errors
# ============================================================

class TimeoutError(AutomotiveSDKError):
    """超时错误 - 通信或响应超时"""
    pass


class ProtocolError(AutomotiveSDKError):
    """协议错误 - 协议层解析或构建失败"""
    pass


class TransportError(AutomotiveSDKError):
    """传输层错误"""
    pass


class BusError(TransportError):
    """总线通信错误"""
    pass


class DoIPError(ProtocolError):
    """DoIP 协议错误"""
    pass


class DoCANError(ProtocolError):
    """DoCAN 协议错误"""
    pass


# ============================================================
# Diagnostic Errors
# ============================================================

class DiagnosticError(AutomotiveSDKError):
    """诊断操作错误"""
    pass


class NegativeResponseError(DiagnosticError):
    """收到 UDS 否定响应"""

    def __init__(self, service_id: int, nrc: int,
                 message: str = ""):
        self.service_id = service_id
        self.nrc = nrc
        nrc_name = NRC_NAMES.get(nrc, f"Unknown(0x{nrc:02X})")
        msg = message or (
            f"Negative response for service 0x{service_id:02X}: "
            f"NRC 0x{nrc:02X} ({nrc_name})"
        )
        super().__init__(msg, code=nrc)


class SecurityAccessError(DiagnosticError):
    """安全访问错误"""
    pass


class FlashError(DiagnosticError):
    """刷写操作错误"""
    pass


class FlashVerifyError(FlashError):
    """刷写校验失败"""
    pass


# ============================================================
# Configuration Errors
# ============================================================

class ConfigurationError(AutomotiveSDKError):
    """配置错误 - 配置文件缺失或格式错误"""
    pass


class VehicleNotFoundError(ConfigurationError):
    """车型未注册"""
    pass


class VersionNotFoundError(ConfigurationError):
    """版本未找到"""
    pass


class CredentialError(ConfigurationError):
    """凭证获取失败"""
    pass


# ============================================================
# Plugin Errors
# ============================================================

class PluginError(AutomotiveSDKError):
    """插件错误"""
    pass


class PluginNotFoundError(PluginError):
    """插件未找到"""
    pass


# ============================================================
# NRC Code Names (UDS ISO 14229-1)
# ============================================================

NRC_NAMES = {
    0x10: "GeneralReject",
    0x11: "ServiceNotSupported",
    0x12: "SubFunctionNotSupported",
    0x13: "IncorrectMessageLengthOrInvalidFormat",
    0x14: "ResponseTooLong",
    0x21: "BusyRepeatRequest",
    0x22: "ConditionsNotCorrect",
    0x24: "RequestSequenceError",
    0x25: "NoResponseFromSubnetComponent",
    0x26: "FailurePreventsExecutionOfRequestedAction",
    0x31: "RequestOutOfRange",
    0x33: "SecurityAccessDenied",
    0x35: "InvalidKey",
    0x36: "ExceededNumberOfAttempts",
    0x37: "RequiredTimeDelayNotExpired",
    0x70: "UploadDownloadNotAccepted",
    0x71: "TransferDataSuspended",
    0x72: "GeneralProgrammingFailure",
    0x73: "WrongBlockSequenceCounter",
    0x78: "RequestCorrectlyReceived-ResponsePending",
    0x7E: "SubFunctionNotSupportedInActiveSession",
    0x7F: "ServiceNotSupportedInActiveSession",
}
