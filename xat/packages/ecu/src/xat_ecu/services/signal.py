"""
Signal Service - 信号操作服务

替代原有的 i_signal_i_pdu.py (3499行)，提供信号级别的读写操作。
通过 ISignalDatabase 和 BusService 实现信号到总线消息的编解码。
"""

import logging
from typing import Any, Dict, List, Optional, Union

from xat_ecu.core.interfaces import ISignalDatabase, IVehicleProfile
from xat_ecu.core.types import BusMessage, BusType, SignalValue
from xat_ecu.services.bus import BusService

logger = logging.getLogger(__name__)


class SignalService:
    """
    信号操作服务

    提供高级信号级别的读/写 API，内部通过 ISignalDatabase
    查询信号定义，并通过 BusService 操作底层总线消息 PDU。
    """

    def __init__(self, vehicle_profile: IVehicleProfile,
                 bus_service: BusService):
        self._vehicle_profile = vehicle_profile
        self._bus_service = bus_service
        self._signal_db: Optional[ISignalDatabase] = None
        # 缓存: msg_name -> 当前 PDU data (可变字节数组)
        self._pdu_cache: Dict[str, bytearray] = {}

    def _ensure_signal_db(self) -> ISignalDatabase:
        """延迟加载信号数据库"""
        if self._signal_db is None and self._vehicle_profile is not None:
            self._signal_db = self._vehicle_profile.get_signal_database()
        if self._signal_db is None:
            raise RuntimeError("Signal database not loaded")
        return self._signal_db

    # ============================================================
    # 信号级 API
    # ============================================================

    def set_signal(self, signal_name: str,
                   value: Union[int, float]) -> None:
        """
        设置信号值（自动查找所属消息并更新 PDU）

        Args:
            signal_name: 信号名称
            value: 信号物理值
        """
        db = self._ensure_signal_db()
        sig_def = db.get_signal(signal_name)

        # 定位所属消息
        msg_name = sig_def.message_name
        if not msg_name:
            raise ValueError(
                f"Signal '{signal_name}' has no associated message"
            )

        self.set_signal_in_message(msg_name, signal_name, value)

    def get_signal(self, signal_name: str) -> SignalValue:
        """
        获取信号当前值

        Args:
            signal_name: 信号名称

        Returns:
            SignalValue 包含当前物理值和原始值
        """
        db = self._ensure_signal_db()
        sig_def = db.get_signal(signal_name)

        msg_name = sig_def.message_name
        if msg_name and msg_name in self._pdu_cache:
            pdu = self._pdu_cache[msg_name]
            raw_value = self._decode_signal(
                pdu, sig_def.bit_position, sig_def.bit_length,
                sig_def.byte_order
            )
            physical = raw_value * sig_def.factor + sig_def.offset

            return SignalValue(
                name=signal_name,
                value=physical,
                raw_value=raw_value,
                bit_position=sig_def.bit_position,
                bit_length=sig_def.bit_length,
                factor=sig_def.factor,
                offset=sig_def.offset,
                min_value=sig_def.min_value,
                max_value=sig_def.max_value,
                unit=sig_def.unit,
                byte_order=sig_def.byte_order,
                message_name=msg_name,
            )

        # 返回信号定义的默认值
        return SignalValue(
            name=signal_name,
            value=sig_def.value,
            raw_value=sig_def.raw_value,
            bit_position=sig_def.bit_position,
            bit_length=sig_def.bit_length,
            factor=sig_def.factor,
            offset=sig_def.offset,
            unit=sig_def.unit,
            byte_order=sig_def.byte_order,
            message_name=sig_def.message_name,
        )

    def set_signal_in_message(self, msg_name: str, signal_name: str,
                               value: Any) -> None:
        """
        在指定消息中设置信号值

        Args:
            msg_name: 消息名称 (如 "BGM_Status")
            signal_name: 信号名称 (如 "DoorOpen")
            value: 物理值
        """
        db = self._ensure_signal_db()
        sig_def = db.get_signal(signal_name)

        # 获取或初始化 PDU 缓存
        if msg_name not in self._pdu_cache:
            try:
                init_data = db.get_init_pdu_data(msg_name)
                self._pdu_cache[msg_name] = bytearray(init_data)
            except Exception:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/services/signal.py")
                msg_def = db.get_message(msg_name)
                dlc = msg_def.get("dlc", 8) if msg_def else 8
                self._pdu_cache[msg_name] = bytearray(dlc)

        pdu = self._pdu_cache[msg_name]

        # 物理值 → 原始值
        raw_value = int((float(value) - sig_def.offset) / sig_def.factor) \
            if sig_def.factor != 0 else int(value)

        # 编码信号到 PDU
        self._encode_signal(
            pdu, raw_value,
            sig_def.bit_position, sig_def.bit_length,
            sig_def.byte_order
        )

        logger.debug(
            f"Signal {signal_name} in {msg_name} set to {value} "
            f"(raw=0x{raw_value:X})"
        )

    def get_all_signals_in_message(
        self, msg_name: str
    ) -> Dict[str, SignalValue]:
        """获取消息中所有信号的当前值"""
        db = self._ensure_signal_db()
        signal_names = db.get_signals_in_message(msg_name)

        result: Dict[str, SignalValue] = {}
        for sig_name in signal_names:
            try:
                result[sig_name] = self.get_signal(sig_name)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/services/signal.py")
                logger.warning(f"Cannot read signal {sig_name}: {e}")

        return result

    def load_signal_database(self, bus_name: str) -> None:
        """为指定总线加载信号数据库"""
        db = self._ensure_signal_db()
        messages = db.get_bus_messages(bus_name)

        for msg_name in messages:
            try:
                init_data = db.get_init_pdu_data(msg_name)
                self._pdu_cache[msg_name] = bytearray(init_data)
            except Exception:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/services/signal.py")
                pass

        logger.info(
            f"Loaded {len(messages)} messages for bus '{bus_name}'"
        )

    def update_pdu_and_send(self, msg_name: str, bus_name: str) -> None:
        """将缓存的 PDU 数据发送到总线"""
        if msg_name not in self._pdu_cache:
            return

        db = self._ensure_signal_db()
        msg_def = db.get_message(msg_name)
        if not msg_def:
            return

        msg_id = msg_def.get("msg_id", 0)
        pdu = bytes(self._pdu_cache[msg_name])
        self._bus_service.send_single(bus_name, msg_id, pdu)

    # ============================================================
    # 信号编解码
    # ============================================================

    @staticmethod
    def _encode_signal(pdu: bytearray, value: int,
                       bit_position: int, bit_length: int,
                       byte_order: str = "little_endian") -> None:
        """将信号值编码到 PDU 数据中"""
        mask = (1 << bit_length) - 1
        value &= mask

        if byte_order == "little_endian":
            # Intel byte order
            byte_pos = bit_position // 8
            bit_offset = bit_position % 8

            for i in range(bit_length):
                bit_val = (value >> i) & 1
                target_byte = byte_pos + (bit_offset + i) // 8
                target_bit = (bit_offset + i) % 8
                if target_byte < len(pdu):
                    if bit_val:
                        pdu[target_byte] |= (1 << target_bit)
                    else:
                        pdu[target_byte] &= ~(1 << target_bit)
        else:
            # Motorola byte order (big endian)
            start_byte = bit_position // 8
            start_bit = bit_position % 8

            for i in range(bit_length):
                bit_val = (value >> (bit_length - 1 - i)) & 1
                curr_byte = start_byte + (start_bit + i) // 8
                curr_bit = 7 - ((start_bit + i) % 8)
                if curr_byte < len(pdu):
                    if bit_val:
                        pdu[curr_byte] |= (1 << curr_bit)
                    else:
                        pdu[curr_byte] &= ~(1 << curr_bit)

    @staticmethod
    def _decode_signal(pdu: bytes, bit_position: int, bit_length: int,
                       byte_order: str = "little_endian") -> int:
        """从 PDU 数据中解码信号值"""
        value = 0

        if byte_order == "little_endian":
            byte_pos = bit_position // 8
            bit_offset = bit_position % 8

            for i in range(bit_length):
                target_byte = byte_pos + (bit_offset + i) // 8
                target_bit = (bit_offset + i) % 8
                if target_byte < len(pdu):
                    if pdu[target_byte] & (1 << target_bit):
                        value |= (1 << i)
        else:
            start_byte = bit_position // 8
            start_bit = bit_position % 8

            for i in range(bit_length):
                curr_byte = start_byte + (start_bit + i) // 8
                curr_bit = 7 - ((start_bit + i) % 8)
                if curr_byte < len(pdu):
                    if pdu[curr_byte] & (1 << curr_bit):
                        value |= (1 << (bit_length - 1 - i))

        return value
