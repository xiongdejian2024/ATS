"""
Config Manager - Unified configuration loading
"""

import os
from typing import Any, Dict, Optional, Tuple
import yaml
from pathlib import Path

from xat_ecu.core.types import VehicleConfig, BusChannelConfig, EcuInfo, DiagMode, BusType
from xat_ecu.utils.file_utils import load_yaml
from xat_ecu.config.vehicle_registry import VehicleRegistry


class ConfigManager:
    """
    配置管理类
    
    负责加载试验台（Testbed）配置和整车网络拓扑配置。
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_dir: 配置文件夹的根路径。默认为当前工作目录下的 config 目录。
        """
        self.config_dir = config_dir or str(Path(__file__).resolve().parents[1] / "vehicle" / "data")
        self.testbed_config: Dict[str, Any] = {}
        self.vehicle_config: Optional[VehicleConfig] = None
        self.vehicle_registry = VehicleRegistry(os.path.join(self.config_dir, 'vehicle_data'))

    def load_testbed_config(self, config_file: str) -> None:
        """
        加载试验台配置文件 (如 default_config.yaml 或 tb_config.yaml)
        
        Args:
            config_file: 配置文件路径
        """
        data = load_yaml(config_file)
        if isinstance(data, list):
            data = data[0] if data else {}
            
        self.testbed_config = data

    def load_vehicle_config(self, vehicle_type: str, version: str) -> VehicleConfig:
        """
        加载特定车型和版本的整车网络拓扑配置
        
        Args:
            vehicle_type: 车型标识 (如 'mars1')
            version: 版本标识 (如 'v_3_0_0')
            
        Returns:
            加载并解析后的 VehicleConfig 对象
        """
        profile = self.vehicle_registry.load(vehicle_type, version)
        
        # Build VehicleConfig from profile
        config = VehicleConfig(
            vehicle_type=vehicle_type,
            version=version,
        )
        
        ecu_list = profile.get_ecu_list()
        config.ecu_list = ecu_list
        
        for ecu_name in ecu_list:
            config.ecu_info[ecu_name] = profile.get_ecu_info(ecu_name)
            
        self.vehicle_config = config
        return config

    def get_bus_config(self, bus_name: str) -> Optional[BusChannelConfig]:
        """
        获取指定总线的通道配置
        
        首先查找 testbed_config 中的配置，如果没有，再看是否存在于 vehicle_config
        
        Args:
            bus_name: 总线名称
            
        Returns:
            总线通道配置对象或 None
        """
        if self.testbed_config and 'bus' in self.testbed_config:
            bus_data = self.testbed_config['bus'].get(bus_name)
            if bus_data:
                # Basic parsing based on old format
                channel = bus_data
                if isinstance(bus_data, list):
                    channel = bus_data[1]  # Mock logic
                    
                return BusChannelConfig(
                    name=bus_name,
                    bus_type=BusType.CAN, # Default guess, should be refined
                    channel=str(channel)
                )
                
        return None

    def get_ecu_config(self, ecu_name: str) -> Optional[EcuInfo]:
        """
        获取指定 ECU 的详细配置信息
        
        Args:
            ecu_name: ECU 名称
            
        Returns:
            ECU 配置对象或 None
        """
        if self.vehicle_config and ecu_name in self.vehicle_config.ecu_info:
            return self.vehicle_config.ecu_info[ecu_name]
        return None
