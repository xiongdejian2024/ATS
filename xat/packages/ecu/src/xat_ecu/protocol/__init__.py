"""
Protocol Module - 协议实现层

该模块包含汽车相关的通信协议实现：
- UDS (ISO 14229)
- DoIP (ISO 13400)
- DoCAN (ISO 15765)
- SOME/IP
"""

# UDS Protocol
from .uds.services import UdsServiceRegistry, ProtocolMeta
from .uds.parser import UdsParser
from .uds.builder import UdsBuilder
from .uds.security import SecurityManager
from .uds.data import UdsDataConstants

# DoIP Protocol
from .doip.client import DoipClient
from .doip.server import DoipServer
from .doip.payload import DoipPayloadParser, DoipPayloadBuilder
from .doip.types import DoipPayloadType, DoipProtocolVersion

# DoCAN Protocol
from .docan.client import DocanClient
from .docan.server import DocanServer

# SOME/IP Protocol
from .someip.service import SomeipService

__all__ = [
    "UdsServiceRegistry",
    "ProtocolMeta",
    "UdsParser",
    "UdsBuilder",
    "SecurityManager",
    "UdsDataConstants",
    "DoipClient",
    "DoipServer",
    "DoipPayloadParser",
    "DoipPayloadBuilder",
    "DoipPayloadType",
    "DoipProtocolVersion",
    "DocanClient",
    "DocanServer",
    "SomeipService",
]
