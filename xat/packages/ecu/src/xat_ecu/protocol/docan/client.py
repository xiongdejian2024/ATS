"""
DoCAN Diagnostic Client (ISO 15765-2)

实现 ISO-TP 传输协议：单帧 (SF)、首帧 (FF)、连续帧 (CF)、流控帧 (FC)。
同时实现 ITransport 接口以便上层直接调用。
"""

import logging
import time
from typing import Any, Callable, Dict, List, Optional

from xat_ecu.core.interfaces import IHardwareAdapter, ITransport
from xat_ecu.core.types import BusMessage, BusType
from xat_ecu.core.errors import ProtocolError, TimeoutError

logger = logging.getLogger(__name__)

# ISO-TP 帧类型常量
SF = 0x00  # Single Frame
FF = 0x10  # First Frame
CF = 0x20  # Consecutive Frame
FC = 0x30  # Flow Control


class DocanClient(ITransport):
    """
    DoCAN (ISO 15765-2) 诊断客户端

    提供基于 CAN 的 ISO-TP 分帧传输能力。
    """

    def __init__(self, hw_adapter: IHardwareAdapter):
        self._hw_adapter = hw_adapter
        self._opened: bool = False
        self._tx_id: int = 0
        self._rx_id: int = 0
        self._is_fd: bool = False
        self._max_payload: int = 7  # CAN classic: 7 bytes SF payload
        self._block_size: int = 0
        self._st_min: float = 0.01  # 10ms default separation time

    # ============================================================
    # ITransport 接口实现
    # ============================================================

    def open(self, config: Dict[str, Any]) -> None:
        """打开 DoCAN 通道"""
        self._tx_id = config.get("tx_id", 0)
        self._rx_id = config.get("rx_id", 0)
        self._is_fd = config.get("is_fd", False)
        self._max_payload = 62 if self._is_fd else 7

        if not self._hw_adapter.is_connected:
            self._hw_adapter.connect(config)

        self._opened = True
        logger.info(
            f"DoCAN opened: TX=0x{self._tx_id:X}, RX=0x{self._rx_id:X}, "
            f"FD={self._is_fd}"
        )

    def close(self) -> None:
        """关闭 DoCAN 通道"""
        self._opened = False
        logger.info("DoCAN closed.")

    def send_message(self, message: BusMessage) -> None:
        """通过 ISO-TP 发送诊断消息"""
        if not self._opened:
            raise ProtocolError("DoCAN channel is not open.")
        data = message.data if isinstance(message.data, bytes) \
            else bytes(message.data)
        self._send_isotp(data)

    def receive_message(self, timeout: float = 1.0) -> Optional[BusMessage]:
        """通过 ISO-TP 接收诊断消息"""
        if not self._opened:
            raise ProtocolError("DoCAN channel is not open.")

        data = self._receive_isotp(timeout)
        if data is None:
            return None

        return BusMessage(
            msg_id=self._rx_id,
            data=data,
            bus_type=BusType.CAN,
            timestamp=time.time(),
        )

    @property
    def bus_type(self) -> BusType:
        return BusType.CAN

    @property
    def is_open(self) -> bool:
        return self._opened

    # ============================================================
    # ISO-TP 传输实现
    # ============================================================

    def _send_isotp(self, data: bytes) -> None:
        """ISO-TP 分帧发送"""
        length = len(data)

        if length <= self._max_payload:
            # Single Frame
            frame = bytes([SF | length]) + data
            self._send_raw(frame)
        else:
            # First Frame
            ff_byte0 = FF | ((length >> 8) & 0x0F)
            ff_byte1 = length & 0xFF
            ff_payload = data[:self._max_payload - 1]
            frame = bytes([ff_byte0, ff_byte1]) + ff_payload
            self._send_raw(frame)

            # Wait for Flow Control
            fc = self._wait_flow_control()
            if fc is None:
                raise TimeoutError("No Flow Control received")

            # Consecutive Frames
            offset = self._max_payload - 1
            seq_num = 1
            while offset < length:
                cf_byte = CF | (seq_num & 0x0F)
                cf_payload = data[offset:offset + self._max_payload]
                frame = bytes([cf_byte]) + cf_payload
                self._send_raw(frame)
                offset += self._max_payload
                seq_num = (seq_num + 1) & 0x0F
                time.sleep(self._st_min)

    def _receive_isotp(self, timeout: float) -> Optional[bytes]:
        """ISO-TP 分帧接收"""
        raw = self._receive_raw(timeout)
        if raw is None:
            return None

        frame_type = raw[0] & 0xF0

        if frame_type == SF:
            # Single Frame
            length = raw[0] & 0x0F
            return raw[1:1 + length]

        elif frame_type == FF:
            # First Frame
            length = ((raw[0] & 0x0F) << 8) | raw[1]
            result = bytearray(raw[2:])

            # Send Flow Control
            self._send_flow_control()

            # Receive Consecutive Frames
            while len(result) < length:
                cf = self._receive_raw(timeout)
                if cf is None:
                    raise TimeoutError("Consecutive frame timeout")
                if (cf[0] & 0xF0) != CF:
                    raise ProtocolError(
                        f"Expected CF, got 0x{cf[0]:02X}"
                    )
                result.extend(cf[1:])

            return bytes(result[:length])

        else:
            logger.warning(f"Unexpected frame type: 0x{frame_type:02X}")
            return raw

    def _send_raw(self, frame: bytes) -> None:
        """发送原始 CAN 帧"""
        # 填充至 8 字节 (或 64 字节 for CANFD)
        pad_len = 64 if self._is_fd else 8
        padded = frame.ljust(pad_len, b"\xCC")
        self._hw_adapter.send(padded, msg_id=self._tx_id)

    def _receive_raw(self, timeout: float) -> Optional[bytes]:
        """接收原始 CAN 帧"""
        return self._hw_adapter.receive(timeout)

    def _wait_flow_control(self, timeout: float = 2.0) -> Optional[bytes]:
        """等待流控帧"""
        raw = self._receive_raw(timeout)
        if raw and (raw[0] & 0xF0) == FC:
            self._block_size = raw[1]
            self._st_min = raw[2] / 1000.0 if raw[2] < 0x80 else 0.001
            return raw
        return None

    def _send_flow_control(self) -> None:
        """发送流控帧"""
        fc_frame = bytes([FC, 0x00, 0x0A])  # BS=0, STmin=10ms
        self._send_raw(fc_frame)
