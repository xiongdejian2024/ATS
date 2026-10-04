"""
Automotive SDK - 通用车企 ECU 模拟与诊断测试 SDK

提供标准化的接口用于：
- CAN/LIN/FlexRay/Ethernet 总线通信
- UDS/DoIP/DoCAN 诊断协议
- ECU 模拟与刷写
- 信号级操作

Usage:
    from xat_ecu import VehicleSDK

    sdk = VehicleSDK(vehicle_type="mars1", version="v_3_0_0")
    sdk.diagnostic.connect(ecu="BGM", mode="doip")
    response = sdk.diagnostic.read_did(0xF190)
"""

__version__ = "1.0.0"
__author__ = "Automotive SDK Team"

from xat_ecu.facade import VehicleSDK

__all__ = ["VehicleSDK"]
