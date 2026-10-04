"""
DoIP Payload Encoding/Decoding
"""

import struct
from typing import Tuple, Optional
import logging

from .types import DoipPayloadType, DoipProtocolVersion

logger = logging.getLogger(__name__)

class DoipPayloadBuilder:
    @staticmethod
    def build_header(version: int, payload_type: int, payload_length: int) -> bytes:
        inv_version = 0xFF ^ version
        return struct.pack("!BBHL", version, inv_version, payload_type, payload_length)
        
    @staticmethod
    def build_routing_activation(source_address: int, activation_type: int = 0x00, reserved: int = 0x00000000) -> bytes:
        return struct.pack("!HBI", source_address, activation_type, reserved)

    @staticmethod
    def build_diagnostic_message(source_address: int, target_address: int, user_data: bytes) -> bytes:
        return struct.pack("!HH", source_address, target_address) + user_data


class DoipPayloadParser:
    @staticmethod
    def parse_header(data: bytes) -> Optional[Tuple[int, int, int]]:
        """
        Parses DoIP Header.
        Returns Tuple of (ProtocolVersion, PayloadType, PayloadLength)
        """
        if len(data) < 8:
            return None
            
        version, inv_version, payload_type, payload_length = struct.unpack("!BBHL", data[:8])
        if version ^ inv_version != 0xFF:
            logger.error("Invalid DoIP Header inverse version")
            return None
            
        return version, payload_type, payload_length

    @staticmethod
    def parse_diagnostic_message(data: bytes) -> Optional[Tuple[int, int, bytes]]:
        """
        Parses Diagnostic Message Payload.
        Returns Tuple of (SourceAddress, TargetAddress, UserData)
        """
        if len(data) < 4:
            return None
            
        source_address, target_address = struct.unpack("!HH", data[:4])
        user_data = data[4:]
        
        return source_address, target_address, user_data
