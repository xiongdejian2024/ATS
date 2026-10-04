"""
Core Types - SDK 数据类型定义

使用 dataclass 和 Enum 定义所有跨模块共享的数据结构，
替代原有散布在各处的 dict 和 namedtuple。
"""

from dataclasses import dataclass, field
from enum import Enum, IntEnum, auto
from typing import Any, Dict, List, Optional, Union


# ============================================================
# Enumerations
# ============================================================

class BusType(Enum):
    """总线类型"""
    CAN = "can"
    CANFD = "canfd"
    LIN = "lin"
    FLEXRAY = "flexray"
    ETHERNET = "ethernet"
    SOMEIP = "someip"


class DiagMode(Enum):
    """诊断通信模式"""
    DOIP = "doip"          # Diagnostics over IP (ISO 13400)
    DOCAN = "docan"        # Diagnostics over CAN (ISO 15765)
    DOLIN = "dolin"        # Diagnostics over LIN


class DiagSession(IntEnum):
    """UDS 诊断会话类型 (ISO 14229 Service 0x10)"""
    DEFAULT = 0x01
    PROGRAMMING = 0x02
    EXTENDED = 0x03


class MessageDirection(Enum):
    """消息方向"""
    TX = "tx"
    RX = "rx"
    BOTH = "both"


class NrcCode(IntEnum):
    """UDS 否定响应码 (Negative Response Codes)"""
    GENERAL_REJECT = 0x10
    SERVICE_NOT_SUPPORTED = 0x11
    SUB_FUNCTION_NOT_SUPPORTED = 0x12
    INCORRECT_MSG_LENGTH_OR_FORMAT = 0x13
    RESPONSE_TOO_LONG = 0x14
    BUSY_REPEAT_REQUEST = 0x21
    CONDITIONS_NOT_CORRECT = 0x22
    REQUEST_SEQUENCE_ERROR = 0x24
    REQUEST_OUT_OF_RANGE = 0x31
    SECURITY_ACCESS_DENIED = 0x33
    INVALID_KEY = 0x35
    EXCEEDED_NUMBER_OF_ATTEMPTS = 0x36
    REQUIRED_TIME_DELAY_NOT_EXPIRED = 0x37
    UPLOAD_DOWNLOAD_NOT_ACCEPTED = 0x70
    TRANSFER_DATA_SUSPENDED = 0x71
    GENERAL_PROGRAMMING_FAILURE = 0x72
    WRONG_BLOCK_SEQUENCE_COUNTER = 0x73
    RESPONSE_PENDING = 0x78
    SERVICE_NOT_SUPPORTED_IN_ACTIVE_SESSION = 0x7F


class SecurityLevel(IntEnum):
    """UDS 安全访问等级"""
    LEVEL_1 = 0x01
    LEVEL_2 = 0x03
    LEVEL_3 = 0x05
    LEVEL_4 = 0x07
    LEVEL_5 = 0x09
    LEVEL_6 = 0x0B
    LEVEL_7 = 0x0D
    LEVEL_8 = 0x11


class CarMode(IntEnum):
    """整车模式"""
    NORMAL = 0
    TRANSPORT = 1
    FACTORY = 2
    CRASH = 3
    DYNO = 5


class UsageMode(IntEnum):
    """使用模式"""
    ABANDONED = 0
    INACTIVE = 1
    CONVENIENCE = 2
    ACTIVE = 11
    DRIVING = 13


class ResetType(IntEnum):
    """ECU 复位类型 (UDS Service 0x11)"""
    HARD_RESET = 0x01
    KEY_OFF_ON_RESET = 0x02
    SOFT_RESET = 0x03


# ============================================================
# Data Classes - Bus Layer
# ============================================================

@dataclass
class BusMessage:
    """
    通用总线消息

    对 CAN/LIN/FlexRay 消息的统一封装。
    """
    msg_id: int
    data: bytes
    bus_type: BusType = BusType.CAN
    channel: str = ""
    timestamp: float = 0.0
    is_fd: bool = False
    is_extended_id: bool = False
    direction: MessageDirection = MessageDirection.TX

    # FlexRay 专属字段
    slot_id: Optional[int] = None
    base_cycle: Optional[int] = None
    repetition: Optional[int] = None

    # 元数据
    msg_name: Optional[str] = None
    tx_node: Optional[str] = None
    rx_nodes: Optional[List[str]] = None


@dataclass
class CyclicMessage:
    """周期消息配置"""
    message: BusMessage
    cycle_time: float          # 发送周期（秒）
    is_active: bool = True     # 是否正在发送
    tx_change: bool = True     # 是否允许动态修改


@dataclass
class SignalValue:
    """信号值"""
    name: str
    value: Union[int, float, str] = 0
    raw_value: int = 0
    bit_position: int = 0
    bit_length: int = 0
    factor: float = 1.0
    offset: float = 0.0
    min_value: float = 0.0
    max_value: float = 0.0
    unit: str = ""
    byte_order: str = "little_endian"  # or "big_endian"
    message_name: str = ""


# ============================================================
# Data Classes - Diagnostic Layer
# ============================================================

@dataclass
class DiagRequest:
    """UDS 诊断请求"""
    service_id: int
    sub_function: Optional[int] = None
    data: bytes = b""
    suppress_positive_response: bool = False

    def to_bytes(self) -> bytes:
        """序列化为原始字节"""
        result = bytes([self.service_id])
        if self.sub_function is not None:
            sf = self.sub_function
            if self.suppress_positive_response:
                sf |= 0x80
            result += bytes([sf])
        result += self.data
        return result


@dataclass
class DiagResponse:
    """UDS 诊断响应"""
    service_id: int
    sub_function: Optional[int] = None
    data: bytes = b""
    is_positive: bool = True
    nrc: Optional[int] = None          # 否定响应码
    raw_data: bytes = b""              # 完整原始响应数据
    timestamp: float = 0.0

    @property
    def is_negative(self) -> bool:
        return not self.is_positive

    @property
    def response_code(self) -> int:
        """正响应返回 SID+0x40，否定响应返回 NRC"""
        if self.is_positive:
            return self.service_id + 0x40
        return self.nrc or 0


# ============================================================
# Data Classes - ECU & Vehicle Configuration
# ============================================================

@dataclass
class EcuInfo:
    """ECU 信息"""
    name: str                              # ECU 名称 (如 "BGM", "TCAM")
    can_req_id: Optional[int] = None       # CAN 诊断请求 ID
    can_res_id: Optional[int] = None       # CAN 诊断响应 ID
    doip_id: Optional[int] = None          # DoIP 逻辑地址
    eth_ip: Optional[str] = None           # 以太网 IP 地址
    bus_type: str = ""                     # 所在总线 (如 "bodycan", "chassis")
    diag_mode: DiagMode = DiagMode.DOIP    # 诊断通信模式
    security_level: Optional[int] = None   # 安全访问等级


@dataclass
class BusChannelConfig:
    """总线通道配置"""
    name: str                              # 通道名称 (如 "bodycan", "adas")
    bus_type: BusType = BusType.CAN
    channel: str = ""                      # 物理通道 (如 "can0", "eth0")
    bitrate: int = 500000
    fd_bitrate: int = 2000000
    is_fd: bool = False


@dataclass
class VehicleConfig:
    """整车配置"""
    vehicle_type: str                      # 车型 (如 "mars1")
    version: str                           # 版本 (如 "v_3_0_0")
    gateway_ip: str = "169.254.1.1"        # 网关 IP
    gateway_ecu: str = "BGM"               # 网关 ECU 名称
    ecu_list: List[str] = field(default_factory=list)
    bus_channels: Dict[str, BusChannelConfig] = field(default_factory=dict)
    ecu_info: Dict[str, EcuInfo] = field(default_factory=dict)


@dataclass
class FlashConfig:
    """刷写配置"""
    firmware_path: str = ""
    key_info: Optional[str] = None
    compression_method: int = 0x00
    target_ecu: str = ""
    target_step: int = 14
    init_step: int = 0
    skip_steps: List[int] = field(default_factory=lambda: [0])
