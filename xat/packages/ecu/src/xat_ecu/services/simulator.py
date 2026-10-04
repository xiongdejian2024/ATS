"""
Simulator Service - ECU 模拟服务

替代原有的 ecu_simulator_app.py，管理 ECU 模拟的生命周期、
Mock 响应数据和 NRC 设置。
"""

import logging
import threading
import time
from typing import Any, Dict, List, Optional

from xat_ecu.core.interfaces import IVehicleProfile
from xat_ecu.core.types import BusMessage, BusType, DiagResponse

logger = logging.getLogger(__name__)

# UDS NRC SID
NRC_SID = 0x7F


class MockResponseConfig:
    """单个 ECU 的模拟响应配置"""

    def __init__(self, ecu_name: str):
        self.ecu_name = ecu_name
        # service_id -> response_data
        self._positive_responses: Dict[int, bytes] = {}
        # service_id -> nrc_code
        self._nrc_responses: Dict[int, int] = {}

    def set_response(self, service_id: int, response_data: bytes) -> None:
        self._positive_responses[service_id] = response_data
        self._nrc_responses.pop(service_id, None)

    def set_nrc(self, service_id: int, nrc_code: int) -> None:
        self._nrc_responses[service_id] = nrc_code
        self._positive_responses.pop(service_id, None)

    def get_response(self, service_id: int) -> Optional[bytes]:
        """获取模拟响应（NRC 优先）"""
        if service_id in self._nrc_responses:
            nrc = self._nrc_responses[service_id]
            return bytes([NRC_SID, service_id, nrc])

        if service_id in self._positive_responses:
            return bytes([service_id + 0x40]) + \
                self._positive_responses[service_id]

        # 默认正响应
        return bytes([service_id + 0x40])


class SimulatorService:
    """
    ECU 模拟服务

    管理模拟 ECU 的生命周期和响应配置。
    """

    def __init__(self, vehicle_profile: IVehicleProfile):
        self._vehicle_profile = vehicle_profile
        self._running: bool = False
        self._simulated_ecus: Dict[str, MockResponseConfig] = {}
        self._excluded_ecus: List[str] = []

    def start_simulation(self, ecus: List[str] = None,
                         exclude_dut: List[str] = None) -> None:
        """
        启动 ECU 模拟

        Args:
            ecus: 要模拟的 ECU 列表（None = 全部）
            exclude_dut: 排除的 ECU 列表（通常是被测件）
        """
        self._excluded_ecus = exclude_dut or []

        if ecus is not None:
            target_ecus = ecus
        elif self._vehicle_profile is not None:
            target_ecus = self._vehicle_profile.get_ecu_list()
        else:
            target_ecus = []

        for ecu_name in target_ecus:
            if ecu_name not in self._excluded_ecus:
                self._simulated_ecus[ecu_name] = MockResponseConfig(ecu_name)

        self._running = True
        logger.info(
            f"Simulation started for {len(self._simulated_ecus)} ECUs, "
            f"excluded: {self._excluded_ecus}"
        )

    def stop_simulation(self) -> None:
        """停止 ECU 模拟"""
        self._running = False
        self._simulated_ecus.clear()
        logger.info("Simulation stopped.")

    def set_mock_response(self, ecu: str, service_id: int,
                          response_data: bytes) -> None:
        """
        设置模拟正响应

        Args:
            ecu: ECU 名称
            service_id: UDS 服务 ID
            response_data: 响应数据（不含 SID+0x40 前缀）
        """
        if ecu not in self._simulated_ecus:
            self._simulated_ecus[ecu] = MockResponseConfig(ecu)
        self._simulated_ecus[ecu].set_response(service_id, response_data)
        logger.info(
            f"Mock response set for {ecu}: SID=0x{service_id:02X}, "
            f"data={response_data.hex()}"
        )

    def set_nrc(self, ecu: str, service_id: int, nrc_code: int) -> None:
        """
        设置否定响应码

        Args:
            ecu: ECU 名称
            service_id: UDS 服务 ID
            nrc_code: NRC 码
        """
        if ecu not in self._simulated_ecus:
            self._simulated_ecus[ecu] = MockResponseConfig(ecu)
        self._simulated_ecus[ecu].set_nrc(service_id, nrc_code)
        logger.info(
            f"NRC set for {ecu}: SID=0x{service_id:02X}, NRC=0x{nrc_code:02X}"
        )

    def get_response_for(self, ecu: str, service_id: int) -> Optional[bytes]:
        """获取指定 ECU 和服务的模拟响应"""
        config = self._simulated_ecus.get(ecu)
        if config is None:
            return None
        return config.get_response(service_id)

    def get_simulated_ecus(self) -> List[str]:
        """获取当前被模拟的 ECU 列表"""
        return list(self._simulated_ecus.keys())

    @property
    def is_running(self) -> bool:
        return self._running
