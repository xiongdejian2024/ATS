"""
SocketCAN 硬件适配器

基于 python-can 库封装 Linux SocketCAN 接口。
支持 CAN 和 CANFD 模式，以及周期消息发送。
"""

import logging
from typing import Any, Dict, Optional

try:
    import can
except ImportError:
    can = None

from xat_ecu.hal.adapter import BaseHardwareAdapter
from xat_ecu.hal.registry import AdapterRegistry

logger = logging.getLogger(__name__)


@AdapterRegistry.register("socketcan")
class SocketCANAdapter(BaseHardwareAdapter):
    """
    SocketCAN 硬件适配器，支持 Linux SocketCAN (CAN/CANFD)。
    """

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        if can is None:
            raise ImportError(
                "python-can library is required for SocketCANAdapter. "
                "Install with: pip install python-can"
            )
        self.channel: str = self._config.get("channel", "can0")
        self.bitrate: int = self._config.get("bitrate", 500000)
        self.is_fd: bool = self._config.get("is_fd", False)
        self.bus: Optional["can.interface.Bus"] = None
        self.cyclic_tasks: Dict[int, "can.CyclicSendTaskABC"] = {}

    # ============================================================
    # BaseHardwareAdapter 模板方法实现
    # ============================================================

    def _do_connect(self, config: Dict[str, Any]) -> None:
        self.channel = config.get("channel", self.channel)
        self.bitrate = config.get("bitrate", self.bitrate)
        self.is_fd = config.get("fd", self.is_fd)

        self.bus = can.interface.Bus(
            interface="socketcan",
            channel=self.channel,
            bitrate=self.bitrate,
            fd=self.is_fd,
            receive_own_messages=True,
        )
        logger.info(
            f"SocketCAN opened: channel={self.channel}, "
            f"bitrate={self.bitrate}, fd={self.is_fd}"
        )

    def _do_disconnect(self) -> None:
        for task in self.cyclic_tasks.values():
            task.stop()
        self.cyclic_tasks.clear()

        if self.bus:
            self.bus.shutdown()
            self.bus = None

    def _do_send(self, data: bytes, **kwargs: Any) -> None:
        if self.bus is None:
            return
        msg_id = kwargs.get("msg_id", 0)
        can_msg = can.Message(
            arbitration_id=msg_id,
            data=data,
            is_extended_id=kwargs.get("is_extended_id", msg_id > 0x7FF),
            is_fd=self.is_fd,
            bitrate_switch=self.is_fd,
        )
        self.bus.send(can_msg)

    def _do_receive(self, timeout: float) -> Optional[bytes]:
        if self.bus is None:
            return None
        can_msg = self.bus.recv(timeout=timeout)
        if can_msg is None:
            return None
        return bytes(can_msg.data)

    # ============================================================
    # SocketCAN 扩展方法（周期消息）
    # ============================================================

    def add_cyclic_msg(self, msg_id: int, data: bytes,
                       cycle_time: float) -> None:
        """添加周期发送消息"""
        if self.bus is None:
            return
        can_msg = can.Message(
            arbitration_id=msg_id,
            data=data,
            is_extended_id=msg_id > 0x7FF,
            is_fd=self.is_fd,
            bitrate_switch=self.is_fd,
        )
        if msg_id in self.cyclic_tasks:
            self.cyclic_tasks[msg_id].stop()
        self.cyclic_tasks[msg_id] = self.bus.send_periodic(can_msg, cycle_time)

    def remove_cyclic_msg(self, msg_id: int) -> None:
        """移除周期发送消息"""
        if msg_id in self.cyclic_tasks:
            self.cyclic_tasks[msg_id].stop()
            del self.cyclic_tasks[msg_id]

    def modify_cyclic_data(self, msg_id: int, data: bytes) -> None:
        """修改周期发送消息的数据"""
        if msg_id in self.cyclic_tasks:
            msg = can.Message(
                arbitration_id=msg_id,
                data=data,
                is_extended_id=msg_id > 0x7FF,
                is_fd=self.is_fd,
                bitrate_switch=self.is_fd,
            )
            self.cyclic_tasks[msg_id].modify_data(msg)

    def recv_message(self, timeout: float = 1.0) -> Optional[Dict[str, Any]]:
        """
        接收一条完整的 CAN 消息并返回结构化字典（含 msg_id）。
        用于上层 transport 需要 msg_id 信息的场景。
        """
        if self.bus is None:
            return None
        can_msg = self.bus.recv(timeout=timeout)
        if can_msg is None:
            return None
        return {
            "msg_id": can_msg.arbitration_id,
            "data": bytes(can_msg.data),
            "timestamp": can_msg.timestamp,
            "dlc": can_msg.dlc,
            "is_fd": can_msg.is_fd,
            "is_extended_id": can_msg.is_extended_id,
            "channel": self.channel,
        }
