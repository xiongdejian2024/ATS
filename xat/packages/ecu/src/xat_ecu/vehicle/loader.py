"""
Vehicle Data Loader - Load vehicle configurations from data directory
"""

import os
from typing import Dict, Any

from xat_ecu.core.types import EcuInfo, DiagMode
from xat_ecu.utils.file_utils import load_yaml
from xat_ecu.vehicle.base import VehicleProfile


class VehicleDataLoader:
    """
    负责从文件系统加载整车数据
    """
    
    def __init__(self, vehicle_type: str, version: str, data_dir: str):
        self.vehicle_type = vehicle_type
        self.version = version
        self.data_dir = data_dir
        
    def load_profile(self) -> VehicleProfile:
        """加载完整的车辆配置文件"""
        profile = VehicleProfile(self.vehicle_type, self.version)
        
        # Load ecu_network.yaml (or similar topology file)
        network_file = self._find_network_file()
        if network_file:
            self._parse_network_file(network_file, profile)
            
        return profile
        
    def _find_network_file(self) -> str:
        """Find the main network configuration file."""
        candidates = ["ecu_network.yaml", "test_network.yaml", "network.yaml"]
        for cand in candidates:
            path = os.path.join(self.data_dir, cand)
            if os.path.exists(path):
                return path
        return ""
        
    def _parse_network_file(self, file_path: str, profile: VehicleProfile) -> None:
        """解析网络拓扑文件，填充 profile 数据"""
        data = load_yaml(file_path)
        if isinstance(data, list):
            data = data[0] if data else {}
            
        profile.topology = data
        
        # 解析 ECU Map
        # 兼容旧格式:
        # ecu_map_id:
        #   BGM: [0x1002, 0x1634, 0x734, ~, ~, '172.16.5.1', ~]
        if 'ecu_map_id' in data:
            ecu_map = data['ecu_map_id']
            for ecu_name, info_list in ecu_map.items():
                if not isinstance(info_list, list) or len(info_list) < 7:
                    continue
                    
                # Helper to handle '~' (None in yaml)
                def parse_val(v):
                    return None if v == '~' else v
                    
                doip_id = parse_val(info_list[0])
                can_req = parse_val(info_list[1])
                can_res = parse_val(info_list[2])
                eth_ip = parse_val(info_list[5])
                
                # Determine primary diag mode based on available IDs
                diag_mode = DiagMode.DOCAN
                if doip_id is not None or eth_ip is not None:
                    diag_mode = DiagMode.DOIP
                
                ecu_info = EcuInfo(
                    name=ecu_name,
                    doip_id=doip_id,
                    can_req_id=can_req,
                    can_res_id=can_res,
                    eth_ip=eth_ip,
                    diag_mode=diag_mode
                )
                profile.ecu_map[ecu_name] = ecu_info
                
        # Parse Diagnostic configs (positive data, dtc tables, etc.)
        diag_config_keys = ['positive_data', 'dtc_code_table', 'dtc_snapshot_table', 'routine_control_table']
        for key in diag_config_keys:
            if key in data:
                for ecu, config in data[key].items():
                    if ecu not in profile.diagnostic_configs:
                        profile.diagnostic_configs[ecu] = {}
                    profile.diagnostic_configs[ecu][key] = config
