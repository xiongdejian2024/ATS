"""
Bus Service - 总线管理服务

替代原有的 bus_app.py，提供总线级别的消息收发、
周期消息管理和通信记录。
不再直接导入 BosApi/YouZiClient 等第三方（通过 PluginRegistry 注入）。
"""

import logging
import threading
import time
from typing import Any, Callable, Dict, List, Optional

from xat_ecu.core.interfaces import IHardwareAdapter, IVehicleProfile
from xat_ecu.core.types import BusMessage, BusType, CyclicMessage
from xat_ecu.core.errors import ConnectionError
from xat_ecu.transport.can import CANTransport

logger = logging.getLogger(__name__)


class BusService:
    """
    总线管理服务

    管理多路总线通道的消息收发、周期消息和通信记录。
    """

    def __init__(self, vehicle_profile: IVehicleProfile,
                 hardware_factory: Callable[..., IHardwareAdapter]):
        self._vehicle_profile = vehicle_profile
        self._hardware_factory = hardware_factory

        # 每条总线一个 transport 实例
        self._transports: Dict[str, CANTransport] = {}
        # 周期消息追踪
        self._cyclic_tasks: Dict[str, Dict[int, CyclicMessage]] = {}
        self._cyclic_thread: Optional[threading.Thread] = None
        self._cyclic_running: bool = False
        # 录制
        self._recording: bool = False
        self._record_path: Optional[str] = None
        self._record_buffer: List[Dict[str, Any]] = []

    # ============================================================
    # 总线通道管理
    # ============================================================

    def _get_or_create_transport(self, bus_name: str) -> CANTransport:
        """获取或创建指定总线的传输层"""
        if bus_name in self._transports:
            transport = self._transports[bus_name]
            if transport.is_open:
                return transport

        # 从车型配置获取总线参数
        bus_config: Dict[str, Any] = {}
        if self._vehicle_profile is not None:
            try:
                bus_config = self._vehicle_profile.get_bus_config(bus_name)
            except Exception:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/services/bus.py")
                pass

        # 创建硬件适配器
        adapter = self._hardware_factory(**bus_config)
        transport = CANTransport(adapter)
        transport.open(bus_config)
        self._transports[bus_name] = transport
        logger.info(f"Bus transport created for: {bus_name}")
        return transport

    # ============================================================
    # 消息收发
    # ============================================================

    def send_single(self, bus_name: str, msg_id: int, data: bytes,
                    **kwargs: Any) -> None:
        """
        发送单帧消息

        Args:
            bus_name: 总线名称 (如 "bodycan", "chassis")
            msg_id: 消息 ID
            data: 消息数据
        """
        transport = self._get_or_create_transport(bus_name)
        msg = BusMessage(
            msg_id=msg_id,
            data=data,
            bus_type=BusType.CAN,
            channel=bus_name,
            timestamp=time.time(),
            is_fd=kwargs.get("is_fd", False),
            is_extended_id=kwargs.get("is_extended_id", msg_id > 0x7FF),
            msg_name=kwargs.get("msg_name"),
        )
        transport.send_message(msg)
        logger.debug(f"Sent on {bus_name}: ID=0x{msg_id:X}, data={data.hex()}")

        if self._recording:
            self._record_buffer.append({
                "timestamp": time.time(),
                "bus": bus_name,
                "direction": "TX",
                "msg_id": msg_id,
                "data": data.hex(),
            })

    def receive(self, bus_name: str,
                timeout: float = 1.0) -> Optional[BusMessage]:
        """
        从指定总线接收一条消息

        Args:
            bus_name: 总线名称
            timeout: 接收超时（秒）

        Returns:
            BusMessage 或 None（超时）
        """
        transport = self._get_or_create_transport(bus_name)
        msg = transport.receive_message(timeout)

        if msg and self._recording:
            data_hex = msg.data.hex() if isinstance(msg.data, bytes) \
                else bytes(msg.data).hex()
            self._record_buffer.append({
                "timestamp": time.time(),
                "bus": bus_name,
                "direction": "RX",
                "msg_id": msg.msg_id,
                "data": data_hex,
            })

        return msg

    # ============================================================
    # 周期消息
    # ============================================================

    def start_cyclic_messages(self, bus_name: str = None) -> None:
        """
        启动周期消息发送

        Args:
            bus_name: 如果指定，只启动该总线的周期消息；否则启动全部
        """
        if self._vehicle_profile is None:
            logger.warning("No vehicle profile, cannot load cyclic messages")
            return

        if bus_name:
            self._start_cyclic_for_bus(bus_name)
        else:
            # 启动所有总线的周期消息
            try:
                sig_db = self._vehicle_profile.get_signal_database()
                # 尝试获取所有总线名称
                for bus in (self._vehicle_profile.get_network_topology()
                            .get("buses", {}).keys()):
                    self._start_cyclic_for_bus(bus)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/services/bus.py")
                logger.error(f"Failed to start cyclic messages: {e}")

        self._cyclic_running = True
        logger.info(f"Cyclic messages started for: {bus_name or 'all buses'}")

    def _start_cyclic_for_bus(self, bus_name: str) -> None:
        """为指定总线启动周期消息"""
        transport = self._get_or_create_transport(bus_name)

        try:
            sig_db = self._vehicle_profile.get_signal_database()
            cyclic_msgs = sig_db.get_cyclic_messages(bus_name)

            for msg_cfg in cyclic_msgs:
                msg_name = msg_cfg.get("name", "")
                msg_id = msg_cfg.get("msg_id", 0)
                cycle_time = msg_cfg.get("cycle_time", 0.01)
                init_data = msg_cfg.get("init_data", [0] * 8)

                if hasattr(transport._adapter, "add_cyclic_msg"):
                    transport._adapter.add_cyclic_msg(
                        msg_id, bytes(init_data), cycle_time
                    )

                if bus_name not in self._cyclic_tasks:
                    self._cyclic_tasks[bus_name] = {}
                self._cyclic_tasks[bus_name][msg_id] = CyclicMessage(
                    message=BusMessage(
                        msg_id=msg_id,
                        data=bytes(init_data),
                        bus_type=BusType.CAN,
                        channel=bus_name,
                        msg_name=msg_name,
                    ),
                    cycle_time=cycle_time,
                    is_active=True,
                )
                logger.debug(
                    f"Cyclic: {msg_name} (0x{msg_id:X}) @ {cycle_time}s"
                )
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/services/bus.py")
            logger.warning(f"Cannot load cyclic for {bus_name}: {e}")

    def stop_cyclic_messages(self, bus_name: str = None) -> None:
        """停止周期消息发送"""
        buses = [bus_name] if bus_name else list(self._cyclic_tasks.keys())
        for bus in buses:
            transport = self._transports.get(bus)
            if transport and hasattr(transport._adapter, "remove_cyclic_msg"):
                for msg_id in list(self._cyclic_tasks.get(bus, {}).keys()):
                    transport._adapter.remove_cyclic_msg(msg_id)
            self._cyclic_tasks.pop(bus, None)

        self._cyclic_running = False
        logger.info(f"Cyclic messages stopped for: {bus_name or 'all'}")

    def pause_cyclic_messages(self) -> None:
        """暂停所有周期消息"""
        self.stop_cyclic_messages()

    def resume_cyclic_messages(self) -> None:
        """恢复所有周期消息"""
        self.start_cyclic_messages()

    # ============================================================
    # 过滤器
    # ============================================================

    def add_filter(self, bus_name: str, msg_id: int,
                   mask: int = 0xFFFFFFFF) -> None:
        """添加消息过滤器"""
        transport = self._get_or_create_transport(bus_name)
        transport.add_filter(msg_id, mask)
        logger.debug(f"Filter added on {bus_name}: 0x{msg_id:X}")

    # ============================================================
    # 通信记录
    # ============================================================

    def start_recording(self, path: str) -> None:
        """开始记录总线通信"""
        self._recording = True
        self._record_path = path
        self._record_buffer = []
        logger.info(f"Bus recording started: {path}")

    def stop_recording(self) -> str:
        """停止记录并保存"""
        self._recording = False
        path = self._record_path or "/tmp/bus_record.log"

        try:
            with open(path, "w") as f:
                for entry in self._record_buffer:
                    f.write(
                        f"{entry['timestamp']:.6f} "
                        f"{entry['bus']} "
                        f"{entry['direction']} "
                        f"0x{entry['msg_id']:X} "
                        f"{entry['data']}\n"
                    )
            logger.info(f"Bus recording saved: {path} "
                       f"({len(self._record_buffer)} messages)")
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/services/bus.py")
            logger.error(f"Failed to save recording: {e}")

        self._record_buffer = []
        return path

    # ============================================================
    # 状态查询
    # ============================================================

    def get_bus_status(self) -> Dict[str, Any]:
        """获取所有总线通道状态"""
        status: Dict[str, Any] = {}
        for bus_name, transport in self._transports.items():
            status[bus_name] = {
                "is_open": transport.is_open,
                "bus_type": transport.bus_type.value,
                "cyclic_count": len(
                    self._cyclic_tasks.get(bus_name, {})
                ),
            }
        return status

    # ============================================================
    # 资源清理
    # ============================================================

    def close(self) -> None:
        """关闭所有总线通道并释放资源"""
        self.stop_cyclic_messages()
        if self._recording:
            self.stop_recording()
        for transport in self._transports.values():
            if transport.is_open:
                transport.close()
        self._transports.clear()
        logger.info("All bus transports closed.")
