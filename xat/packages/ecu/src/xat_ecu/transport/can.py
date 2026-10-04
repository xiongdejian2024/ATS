"""
CAN/CANFD Transport Layer

实现 ITransport 接口，对 IHardwareAdapter 进行包装，
提供 CAN 总线级别的消息收发、过滤器和周期消息管理。
"""

import logging
import time
from typing import Any, Callable, Dict, List, Optional

from xat_ecu.core.interfaces import IHardwareAdapter, ITransport
from xat_ecu.core.types import BusMessage, BusType

logger = logging.getLogger(__name__)


class CANTransport(ITransport):
    """
    CAN/CANFD 传输层

    封装 IHardwareAdapter，提供 BusMessage 级别的收发抽象。
    """

    def __init__(self, adapter: IHardwareAdapter, **kwargs: Any):
        self._adapter = adapter
        self._config: Dict[str, Any] = kwargs
        self._filters: List[Dict[str, int]] = []
        self._rx_callback: Optional[Callable[[BusMessage], None]] = None
        self._opened: bool = False

    # ============================================================
    # ITransport 接口实现
    # ============================================================

    def open(self, config: Dict[str, Any]) -> None:
        """打开 CAN 传输通道"""
        self._config.update(config)
        if not self._adapter.is_connected:
            self._adapter.connect(config)
        self._opened = True
        logger.info(f"CANTransport opened with config: {config}")

    def close(self) -> None:
        """关闭 CAN 传输通道"""
        try:
            if self._adapter.is_connected:
                self._adapter.disconnect()
        finally:
            self._opened = False
        logger.info("CAN 传输已关闭")

    def send_message(self, message: BusMessage) -> None:
        """发送 CAN 总线消息"""
        if not self._opened:
            raise RuntimeError("CANTransport is not open.")
        self._adapter.send(
            message.data if isinstance(message.data, bytes)
            else bytes(message.data),
            msg_id=message.msg_id,
            is_extended_id=message.is_extended_id,
            is_fd=message.is_fd,
        )

    def receive_message(self, timeout: float = 1.0) -> Optional[BusMessage]:
        """接收 CAN 总线消息"""
        if not self._opened:
            raise RuntimeError("CANTransport is not open.")

        # 如果适配器有 recv_message 扩展方法（返回字典含 msg_id），使用它
        if hasattr(self._adapter, "recv_message"):
            result = self._adapter.recv_message(timeout)
            if result is None:
                return None
            msg = BusMessage(
                msg_id=result.get("msg_id", 0),
                data=result.get("data", b""),
                bus_type=BusType.CANFD if result.get("is_fd") else BusType.CAN,
                channel=result.get("channel", ""),
                timestamp=result.get("timestamp", time.time()),
                is_fd=result.get("is_fd", False),
                is_extended_id=result.get("is_extended_id", False),
            )
        else:
            raw = self._adapter.receive(timeout)
            if raw is None:
                return None
            msg = BusMessage(
                msg_id=0,
                data=raw,
                bus_type=BusType.CAN,
                timestamp=time.time(),
            )

        if self._rx_callback:
            self._rx_callback(msg)

        return msg

    @property
    def bus_type(self) -> BusType:
        """当前传输层的总线类型"""
        return BusType.CANFD if self._config.get("is_fd") else BusType.CAN

    @property
    def is_open(self) -> bool:
        """通道是否已打开"""
        return self._opened

    def add_filter(self, msg_id: int, mask: int = 0xFFFFFFFF) -> None:
        """添加 CAN ID 过滤器"""
        self._filters.append({"can_id": msg_id, "can_mask": mask})
        logger.debug(f"Filter added: ID=0x{msg_id:X}, Mask=0x{mask:X}")

    def clear_filters(self) -> None:
        """清除所有过滤器"""
        self._filters.clear()

    def set_callback(self, callback: Callable[[BusMessage], None]) -> None:
        """设置消息接收回调"""
        self._rx_callback = callback

    # ============================================================
    # CAN 扩展方法（周期消息）
    # ============================================================

    def add_cyclic_message(self, msg_id: int, data: bytes,
                           cycle_time: float) -> None:
        """添加周期发送消息"""
        if hasattr(self._adapter, "add_cyclic_msg"):
            self._adapter.add_cyclic_msg(msg_id, data, cycle_time)

    def remove_cyclic_message(self, msg_id: int) -> None:
        """移除周期发送消息"""
        if hasattr(self._adapter, "remove_cyclic_msg"):
            self._adapter.remove_cyclic_msg(msg_id)
