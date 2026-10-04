"""
Vehicle Registry - Auto-discover and register vehicle profiles
"""

import os
from typing import Dict, List, Tuple, Any, Optional
from xat_ecu.core.interfaces import IVehicleProfile


class VehicleRegistry:
    """
    车型注册表
    
    支持按照 (车型, 版本) 动态发现和加载车型数据文件。
    """
    
    def __init__(self, data_dir: str):
        """
        Args:
            data_dir: 存放所有车型数据的根目录，例如 `config/vehicle_data`
        """
        self.data_dir = data_dir
        self._profiles: Dict[Tuple[str, str], IVehicleProfile] = {}
        
    def register(self, profile: IVehicleProfile) -> None:
        """注册一个实例化好的车型配置"""
        key = (profile.vehicle_type, profile.version)
        self._profiles[key] = profile

    def load(self, vehicle_type: str, version: str) -> IVehicleProfile:
        """
        加载指定车型和版本的配置
        
        如果在注册表中找不到，则尝试动态实例化（依赖于 vehicle 模块中的 Loader）
        
        Args:
            vehicle_type: 车型 (如 'mars1')
            version: 版本 (如 'v_3_0_0')
            
        Returns:
            实例化后的 IVehicleProfile
            
        Raises:
            ValueError: 如果找不到对应的配置
        """
        key = (vehicle_type, version)
        if key in self._profiles:
            return self._profiles[key]
            
        # 尝试动态加载
        # 这里延迟导入以避免循环依赖
        from xat_ecu.vehicle.loader import VehicleDataLoader
        
        vehicle_dir = os.path.join(self.data_dir, vehicle_type, version)
        if not os.path.isdir(vehicle_dir):
            raise ValueError(f"Vehicle data directory not found for {vehicle_type} {version}: {vehicle_dir}")
            
        loader = VehicleDataLoader(vehicle_type, version, vehicle_dir)
        profile = loader.load_profile()
        self.register(profile)
        return profile

    def list_vehicles(self) -> List[str]:
        """
        列出所有已知的车型
        
        扫描 data_dir 获取第一级目录。
        """
        if not os.path.exists(self.data_dir):
            return []
            
        return [
            d for d in os.listdir(self.data_dir)
            if os.path.isdir(os.path.join(self.data_dir, d))
        ]

    def list_versions(self, vehicle_type: str) -> List[str]:
        """
        列出指定车型的所有已知版本
        
        扫描 data_dir/<vehicle_type> 获取版本目录。
        """
        veh_dir = os.path.join(self.data_dir, vehicle_type)
        if not os.path.exists(veh_dir):
            return []
            
        return [
            d for d in os.listdir(veh_dir)
            if os.path.isdir(os.path.join(veh_dir, d))
        ]
