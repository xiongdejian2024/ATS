"""
Core Interfaces - 所有模块的抽象接口定义

通过 ABC 抽象基类实现依赖倒置原则 (DIP)，上层模块仅依赖接口而非具体实现。
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from xat_ecu.core.types import (
    BusMessage,
    BusType,
    DiagRequest,
    DiagResponse,
    EcuInfo,
    SignalValue,
)


class IHardwareAdapter(ABC):
    """
    硬件设备适配器接口

    所有硬件驱动（Tosun、Toomoss、PCAN、SocketCAN 等）都必须实现此接口。
    通过 HardwareFactory 统一创建和管理。

    生命周期: connect() → send()/receive() → disconnect()
    """

    @abstractmethod
    def connect(self, config: Dict[str, Any]) -> None:
        """
        连接硬件设备

        Args:
            config: 设备配置字典，包含通道、波特率等参数
                Example: {"channel": "can0", "bitrate": 500000, "fd": True}

        Raises:
            HardwareError: 设备连接失败
        """
        ...

    @abstractmethod
    def disconnect(self) -> None:
        """断开硬件连接并释放资源"""
        ...

    @abstractmethod
    def send(self, data: bytes, **kwargs: Any) -> None:
        """
        发送数据到硬件

        Args:
            data: 要发送的原始字节数据
            **kwargs: 额外参数 (msg_id, is_fd 等)

        Raises:
            HardwareError: 发送失败
        """
        ...

    @abstractmethod
    def receive(self, timeout: float = 1.0) -> Optional[bytes]:
        """
        从硬件接收数据

        Args:
            timeout: 接收超时时间（秒）

        Returns:
            接收到的原始字节数据，超时返回 None
        """
        ...

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """当前是否已连接"""
        ...

    def start_record_log(self, path: str) -> None:
        """开始记录通信日志（可选实现）"""
        pass

    def stop_record_log(self) -> Optional[str]:
        """停止记录通信日志，返回日志文件路径（可选实现）"""
        return None


class ITransport(ABC):
    """
    传输层接口

    对不同总线类型（CAN, LIN, FlexRay, Ethernet）提供统一的消息收发抽象。
    """

    @abstractmethod
    def open(self, config: Dict[str, Any]) -> None:
        """
        打开传输通道

        Args:
            config: 通道配置
        """
        ...

    @abstractmethod
    def close(self) -> None:
        """关闭传输通道"""
        ...

    @abstractmethod
    def send_message(self, message: BusMessage) -> None:
        """
        发送总线消息

        Args:
            message: 封装好的总线消息
        """
        ...

    @abstractmethod
    def receive_message(self, timeout: float = 1.0) -> Optional[BusMessage]:
        """
        接收总线消息

        Args:
            timeout: 接收超时时间

        Returns:
            BusMessage 或 None（超时）
        """
        ...

    @property
    @abstractmethod
    def bus_type(self) -> BusType:
        """当前传输层的总线类型"""
        ...

    @property
    @abstractmethod
    def is_open(self) -> bool:
        """通道是否已打开"""
        ...

    def add_filter(self, msg_id: int, mask: int = 0xFFFFFFFF) -> None:
        """添加消息过滤器（可选实现）"""
        pass

    def clear_filters(self) -> None:
        """清除所有消息过滤器（可选实现）"""
        pass

    def set_callback(self, callback: Callable[[BusMessage], None]) -> None:
        """设置消息接收回调（可选实现）"""
        pass


class IDiagnosticClient(ABC):
    """
    诊断客户端接口

    提供 UDS (ISO 14229) 诊断仪侧的操作抽象，
    支持通过 DoIP 或 DoCAN 发送诊断请求。
    """

    @abstractmethod
    def connect(self, ecu: str, **kwargs: Any) -> None:
        """
        连接到目标 ECU

        Args:
            ecu: ECU 名称 (如 "BGM", "TCAM")
            **kwargs: 额外连接参数 (server_ip, doip_id 等)
        """
        ...

    @abstractmethod
    def disconnect(self) -> None:
        """断开诊断连接"""
        ...

    @abstractmethod
    def send_request(self, request: DiagRequest) -> DiagResponse:
        """
        发送诊断请求并等待响应

        Args:
            request: 诊断请求数据

        Returns:
            诊断响应数据
        """
        ...

    @abstractmethod
    def read_did(self, did: int, **kwargs: Any) -> DiagResponse:
        """
        读取数据标识符 (UDS Service 0x22)

        Args:
            did: Data Identifier (如 0xF190 表示 VIN)

        Returns:
            DiagResponse 包含 DID 数据
        """
        ...

    @abstractmethod
    def write_did(self, did: int, data: bytes, **kwargs: Any) -> DiagResponse:
        """
        写入数据标识符 (UDS Service 0x2E)

        Args:
            did: Data Identifier
            data: 要写入的数据

        Returns:
            DiagResponse
        """
        ...

    @abstractmethod
    def session_control(self, session: int) -> DiagResponse:
        """
        诊断会话控制 (UDS Service 0x10)

        Args:
            session: 会话类型 (1=Default, 2=Programming, 3=Extended)
        """
        ...

    @abstractmethod
    def security_access(self, level: int, **kwargs: Any) -> DiagResponse:
        """
        安全访问 (UDS Service 0x27)

        Args:
            level: 安全等级 (1, 3, 5, ...)

        Returns:
            DiagResponse 包含安全访问结果
        """
        ...

    @abstractmethod
    def ecu_reset(self, reset_type: int = 0x01) -> DiagResponse:
        """
        ECU 复位 (UDS Service 0x11)

        Args:
            reset_type: 复位类型 (1=Hard, 2=Key Off/On, 3=Soft)
        """
        ...


class IDiagnosticServer(ABC):
    """
    诊断服务端接口

    模拟 ECU 侧的 UDS 诊断服务响应。
    """

    @abstractmethod
    def start(self, ecu: str, **kwargs: Any) -> None:
        """启动诊断服务模拟"""
        ...

    @abstractmethod
    def stop(self) -> None:
        """停止诊断服务模拟"""
        ...

    @abstractmethod
    def set_response(self, service_id: int, sub_function: int,
                     response_data: bytes) -> None:
        """
        设置特定服务的模拟响应数据

        Args:
            service_id: UDS 服务 ID
            sub_function: 子功能 ID
            response_data: 响应数据
        """
        ...

    @abstractmethod
    def set_nrc(self, service_id: int, nrc_code: int) -> None:
        """
        设置否定响应码

        Args:
            service_id: UDS 服务 ID
            nrc_code: 否定响应码 (NRC)
        """
        ...


class IVehicleProfile(ABC):
    """
    车型配置接口

    封装特定车型+版本的 ECU 拓扑、总线配置、信号数据库等信息。
    不同车型通过实现此接口来注册到 VehicleRegistry。
    """

    @property
    @abstractmethod
    def vehicle_type(self) -> str:
        """车型标识 (如 'mars1', 'venus', 'jupiter')"""
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """版本标识 (如 'v_3_0_0')"""
        ...

    @abstractmethod
    def get_ecu_list(self) -> List[str]:
        """获取该车型的所有 ECU 名称列表"""
        ...

    @abstractmethod
    def get_ecu_info(self, ecu_name: str) -> EcuInfo:
        """获取指定 ECU 的详细信息"""
        ...

    @abstractmethod
    def get_bus_config(self, bus_name: str) -> Dict[str, Any]:
        """获取指定总线通道的配置信息"""
        ...

    @abstractmethod
    def get_network_topology(self) -> Dict[str, Any]:
        """获取整车网络拓扑"""
        ...

    @abstractmethod
    def get_signal_database(self) -> "ISignalDatabase":
        """获取信号数据库"""
        ...

    @abstractmethod
    def get_diagnostic_config(self, ecu_name: str) -> Dict[str, Any]:
        """获取指定 ECU 的诊断配置 (CAN ID, DoIP ID 等)"""
        ...


class ISignalDatabase(ABC):
    """
    信号数据库接口

    提供对 CAN/LIN/FlexRay 信号矩阵的查询和操作能力。
    数据来源可以是 DBC/LDF/ARXML/JSON 等格式。
    """

    @abstractmethod
    def get_message(self, msg_name: str) -> Dict[str, Any]:
        """获取消息定义"""
        ...

    @abstractmethod
    def get_message_by_id(self, msg_id: int, bus_type: BusType) -> Dict[str, Any]:
        """通过消息 ID 获取消息定义"""
        ...

    @abstractmethod
    def get_signal(self, signal_name: str) -> SignalValue:
        """获取信号定义及当前值"""
        ...

    @abstractmethod
    def get_signals_in_message(self, msg_name: str) -> List[str]:
        """获取消息中的所有信号名称"""
        ...

    @abstractmethod
    def get_init_pdu_data(self, msg_name: str) -> List[int]:
        """获取消息的初始 PDU 数据"""
        ...

    @abstractmethod
    def get_bus_messages(self, bus_name: str) -> List[str]:
        """获取指定总线上的所有消息名称"""
        ...

    @abstractmethod
    def get_cyclic_messages(self, bus_name: str) -> List[Dict[str, Any]]:
        """获取指定总线上的所有周期消息及其配置"""
        ...


class ICredentialProvider(ABC):
    """
    凭证提供者接口

    将凭证管理从硬编码中解耦，支持多种凭证来源
    （环境变量、Vault、配置文件等）。
    """

    @abstractmethod
    def get_credential(self, name: str) -> Dict[str, str]:
        """
        获取指定名称的凭证

        Args:
            name: 凭证名称 (如 "bgm_ssh", "tcam_ssh", "jira")

        Returns:
            {"username": "...", "password": "...", "host": "...", "port": "..."}
        """
        ...

    @abstractmethod
    def has_credential(self, name: str) -> bool:
        """检查指定凭证是否存在"""
        ...
