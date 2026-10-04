"""
Diagnostic Service - 诊断服务

替代原有的 Sd_Tester 和 Diagnostic_Odx_Client_Sim_App，
提供统一的 UDS 诊断操作接口。
通过 DiagMode 自动选择 DoIP 或 DoCAN 底层传输。
"""

import logging
import time
from typing import Any, Callable, Dict, Optional

from xat_ecu.core.interfaces import ITransport, IVehicleProfile
from xat_ecu.core.types import (
    BusMessage,
    BusType,
    DiagMode,
    DiagRequest,
    DiagResponse,
    DiagSession,
    ResetType,
)
from xat_ecu.core.errors import (
    DiagnosticError,
    NegativeResponseError,
    TimeoutError,
)
from xat_ecu.protocol.uds.builder import UdsBuilder
from xat_ecu.protocol.uds.parser import UdsParser

logger = logging.getLogger(__name__)

# UDS Service IDs
SID_DIAG_SESSION_CTRL = 0x10
SID_ECU_RESET = 0x11
SID_CLEAR_DTC = 0x14
SID_READ_DTC = 0x19
SID_READ_DID = 0x22
SID_SECURITY_ACCESS = 0x27
SID_WRITE_DID = 0x2E
SID_IO_CONTROL = 0x2F
SID_ROUTINE_CTRL = 0x31
SID_REQUEST_DOWNLOAD = 0x34
SID_TRANSFER_DATA = 0x36
SID_TRANSFER_EXIT = 0x37
SID_TESTER_PRESENT = 0x3E
SID_COMM_CONTROL = 0x28
SID_DTC_SETTING = 0x85

# UDS 否定响应 SID
NRC_SID = 0x7F


class DiagnosticService:
    """
    诊断服务 — 替代 Sd_Tester / Diagnostic_Odx_Client_Sim_App

    通过注入 IVehicleProfile 和传输工厂实现解耦：
    - 根据 DiagMode 自动创建 DoIP 或 DoCAN 客户端
    - 所有 UDS 服务方法都通过统一的 _send_uds() 调度
    """

    def __init__(self, vehicle_profile: IVehicleProfile,
                 transport_factory: Callable[..., ITransport]):
        self._vehicle_profile = vehicle_profile
        self._transport_factory = transport_factory
        self._transport: Optional[ITransport] = None
        self._current_ecu: Optional[str] = None
        self._current_mode: Optional[DiagMode] = None
        self._default_timeout: float = 5.0

    # ============================================================
    # 连接管理
    # ============================================================

    def connect(self, ecu: str, mode: DiagMode = DiagMode.DOIP,
                **kwargs: Any) -> None:
        """
        连接到目标 ECU

        Args:
            ecu: ECU 名称 (如 "BGM", "TCAM")
            mode: 诊断通信模式 (DOIP / DOCAN)
            **kwargs: 额外参数 (server_ip, timeout 等)
        """
        logger.info("连接 ECU：%s，模式：%s", ecu, mode)
        self.disconnect()

        # 从车型配置获取 ECU 的诊断参数
        diag_config = {}
        if self._vehicle_profile is not None:
            try:
                diag_config = self._vehicle_profile.get_diagnostic_config(ecu)
            except Exception:
                logger.exception("加载 ECU 诊断配置失败：%s", ecu)
                raise
        diag_config.update(kwargs)

        if mode == DiagMode.DOIP:
            self._transport = self._create_doip_transport(diag_config)
        elif mode == DiagMode.DOCAN:
            self._transport = self._create_docan_transport(diag_config)
        else:
            raise ValueError(f"未知诊断模式：{mode}")

        if self._transport is not None:
            try:
                self._transport.open(diag_config)
            except Exception:
                logger.exception("打开 ECU 诊断连接失败：%s", ecu)
                self.disconnect()
                raise
            self._current_ecu = ecu
            self._current_mode = mode
            logger.info("已连接 ECU：%s，模式：%s", ecu, mode.value)

    def disconnect(self) -> None:
        """断开诊断连接"""
        try:
            if self._transport is not None:
                self._transport.close()
        except Exception:
            logger.exception("断开 ECU 诊断连接失败")
            raise
        finally:
            self._transport = None
            self._current_ecu = None
        logger.info("诊断连接已断开")

    @property
    def is_connected(self) -> bool:
        return self._transport is not None and self._transport.is_open

    # ============================================================
    # UDS 诊断服务
    # ============================================================

    def session_control(self, session: DiagSession) -> DiagResponse:
        """诊断会话控制 (UDS 0x10)"""
        return self._send_uds(SID_DIAG_SESSION_CTRL, sub_function=session)

    def security_access(self, level: int,
                        algorithm: Any = None) -> DiagResponse:
        """
        安全访问 (UDS 0x27)

        两步流程：
        1. 发送 requestSeed (奇数 sub-function)
        2. 用 algorithm 计算 key 并发送 sendKey (偶数 sub-function)
        """
        # Step 1: Request Seed
        seed_resp = self._send_uds(SID_SECURITY_ACCESS, sub_function=level)
        if seed_resp.is_negative:
            return seed_resp

        seed = seed_resp.data[1:]
        if seed == b"\x00" * len(seed):
            logger.info("ECU already unlocked (zero seed)")
            return seed_resp

        # Step 2: Send Key
        if algorithm is not None:
            key = algorithm(seed, level)
        else:
            raise DiagnosticError(f"安全访问需要注入车型算法：{level}")

        return self._send_uds(
            SID_SECURITY_ACCESS,
            sub_function=level + 1,
            data=key,
        )

    def ecu_reset(self, reset_type: ResetType = ResetType.HARD_RESET
                  ) -> DiagResponse:
        """ECU 复位 (UDS 0x11)"""
        return self._send_uds(SID_ECU_RESET, sub_function=reset_type)

    def read_did(self, did: int, **kwargs: Any) -> DiagResponse:
        """读取数据标识符 (UDS 0x22)"""
        did_bytes = did.to_bytes(2, "big")
        return self._send_uds(SID_READ_DID, data=did_bytes)

    def write_did(self, did: int, data: bytes,
                  **kwargs: Any) -> DiagResponse:
        """写入数据标识符 (UDS 0x2E)"""
        did_bytes = did.to_bytes(2, "big")
        return self._send_uds(SID_WRITE_DID, data=did_bytes + data)

    def routine_control(self, routine_id: int, sub_function: int,
                        data: bytes = b"") -> DiagResponse:
        """例程控制 (UDS 0x31)"""
        rid_bytes = routine_id.to_bytes(2, "big")
        return self._send_uds(
            SID_ROUTINE_CTRL,
            sub_function=sub_function,
            data=rid_bytes + data,
        )

    def tester_present(self) -> DiagResponse:
        """TesterPresent (UDS 0x3E)"""
        return self._send_uds(SID_TESTER_PRESENT, sub_function=0x00)

    def communication_control(self, control_type: int,
                              comm_type: int) -> DiagResponse:
        """通信控制 (UDS 0x28)"""
        return self._send_uds(
            SID_COMM_CONTROL,
            sub_function=control_type,
            data=bytes([comm_type]),
        )

    def dtc_clear(self) -> DiagResponse:
        """清除 DTC (UDS 0x14)"""
        return self._send_uds(SID_CLEAR_DTC, data=b"\xFF\xFF\xFF")

    def dtc_read(self, sub_function: int = 0x01) -> DiagResponse:
        """读取 DTC (UDS 0x19)"""
        return self._send_uds(SID_READ_DTC, sub_function=sub_function)

    def io_control(self, did: int, control_param: int,
                   data: bytes = b"") -> DiagResponse:
        """IO 控制 (UDS 0x2F)"""
        did_bytes = did.to_bytes(2, "big")
        return self._send_uds(
            SID_IO_CONTROL,
            data=did_bytes + bytes([control_param]) + data,
        )

    def send_raw(self, data: bytes, timeout: float = None) -> DiagResponse:
        """发送原始诊断请求"""
        return self._send_and_receive(data, timeout or self._default_timeout)

    def check_all_ecu_active(self) -> Dict[str, bool]:
        """检查所有 ECU 是否在线（通过 TesterPresent）"""
        if self._vehicle_profile is None:
            return {}

        results: Dict[str, bool] = {}
        ecu_list = self._vehicle_profile.get_ecu_list()

        for ecu_name in ecu_list:
            try:
                self.connect(ecu_name, mode=self._current_mode or DiagMode.DOIP)
                resp = self.tester_present()
                results[ecu_name] = resp.is_positive
            except Exception:
                logger.exception("检查 ECU 在线状态失败：%s", ecu_name)
                results[ecu_name] = False
            finally:
                self.disconnect()

        return results

    # ============================================================
    # 内部方法
    # ============================================================

    def _send_uds(self, service_id: int, sub_function: int = None,
                  data: bytes = b"",
                  timeout: float = None) -> DiagResponse:
        """
        发送 UDS 请求并等待响应

        构建请求字节 → 发送 → 等待响应 → 解析 → 处理 ResponsePending
        """
        request_data = bytes([service_id])
        if sub_function is not None:
            request_data += bytes([sub_function])
        request_data += data

        return self._send_and_receive(
            request_data, timeout or self._default_timeout
        )

    def _send_and_receive(self, request_data: bytes,
                          timeout: float) -> DiagResponse:
        """发送原始请求并等待/解析响应"""
        if not self.is_connected:
            raise DiagnosticError("未连接 ECU")
        if not request_data:
            raise ValueError("诊断请求不能为空")
        if timeout <= 0:
            raise ValueError("诊断超时必须大于零")

        # 发送
        msg = BusMessage(msg_id=0, data=request_data, bus_type=self._transport.bus_type)
        self._transport.send_message(msg)

        # 等待响应 (处理 0x78 ResponsePending)
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(
                    f"UDS response timeout for SID 0x{request_data[0]:02X}"
                )

            resp_msg = self._transport.receive_message(min(remaining, 2.0))
            if resp_msg is None:
                continue

            resp_data = resp_msg.data if isinstance(resp_msg.data, bytes) \
                else bytes(resp_msg.data)

            if len(resp_data) < 1:
                continue

            # 检查否定响应
            if resp_data[0] == NRC_SID and len(resp_data) >= 3:
                if resp_data[1] != request_data[0]:
                    continue
                nrc = resp_data[2]
                if nrc == 0x78:  # ResponsePending
                    logger.debug("ECU 响应待处理，继续等待")
                    continue
                return DiagResponse(
                    service_id=resp_data[1],
                    data=resp_data[3:],
                    is_positive=False,
                    nrc=nrc,
                    raw_data=resp_data,
                    timestamp=time.time(),
                )

            # 正响应
            if resp_data[0] != request_data[0] + 0x40:
                continue
            service_id = resp_data[0] - 0x40
            return DiagResponse(
                service_id=service_id,
                sub_function=resp_data[1] if len(resp_data) > 1 else None,
                data=resp_data[1:],
                is_positive=True,
                raw_data=resp_data,
                timestamp=time.time(),
            )

    def _create_doip_transport(self,
                               config: Dict[str, Any]) -> Optional[ITransport]:
        """创建 DoIP 传输实例"""
        return self._transport_factory("doip", **config)

    def _create_docan_transport(self,
                                config: Dict[str, Any]) -> Optional[ITransport]:
        """创建 DoCAN 传输实例"""
        return self._transport_factory("docan", **config)
