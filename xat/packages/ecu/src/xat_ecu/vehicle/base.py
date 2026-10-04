"""
Vehicle Profile - Implementation of IVehicleProfile
"""

from typing import Dict, List, Any

from xat_ecu.core.interfaces import IVehicleProfile, ISignalDatabase
from xat_ecu.core.types import EcuInfo, DiagMode


class VehicleProfile(IVehicleProfile):
    """
    具体的车型配置实现类
    
    加载自 vehicle_data 下的具体文件。
    """
    
    def __init__(self, vehicle_type: str, version: str):
        self._vehicle_type = vehicle_type
        self._version = version
        
        self.ecu_map: Dict[str, EcuInfo] = {}
        self.topology: Dict[str, Any] = {}
        self.diagnostic_configs: Dict[str, Any] = {}
        self.signal_db: ISignalDatabase = None
        
    @property
    def vehicle_type(self) -> str:
        return self._vehicle_type

    @property
    def version(self) -> str:
        return self._version

    def get_ecu_list(self) -> List[str]:
        return list(self.ecu_map.keys())

    def get_ecu_info(self, ecu_name: str) -> EcuInfo:
        if ecu_name not in self.ecu_map:
            raise KeyError(f"ECU '{ecu_name}' not found in {self._vehicle_type} {self._version}.")
        return self.ecu_map[ecu_name]

    def get_bus_config(self, bus_name: str) -> Dict[str, Any]:
        # Return raw bus configuration if available from topology
        # This can be expanded based on specific needs
        if 'bus' in self.topology and bus_name in self.topology['bus']:
            return self.topology['bus'][bus_name]
        return {}

    def get_network_topology(self) -> Dict[str, Any]:
        return self.topology

    def get_signal_database(self) -> ISignalDatabase:
        if not self.signal_db:
            raise ValueError(f"Signal database not loaded for {self._vehicle_type} {self._version}.")
        return self.signal_db

    def get_diagnostic_config(self, ecu_name: str) -> Dict[str, Any]:
        return self.diagnostic_configs.get(ecu_name, {})
