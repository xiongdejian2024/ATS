"""
DoIP Diagnostic Client
"""

import socket
import logging
import time
from typing import Any, Callable, Dict, Optional

from xat_ecu.core.interfaces import ITransport
from xat_ecu.core.types import BusMessage, BusType
from .types import DoipConstants, DoipPayloadType, DoipProtocolVersion
from .payload import DoipPayloadBuilder, DoipPayloadParser

logger = logging.getLogger(__name__)


class DoipClient(ITransport):
    """
    DoIP TCP Client
    """
    
    def __init__(self):
        self._socket: Optional[socket.socket] = None
        self._connected = False
        self._source_address = DoipConstants.DEFAULT_LOGICAL_ADDRESS
        self._target_address = DoipConstants.DEFAULT_TARGET_ADDRESS
        self._version = DoipProtocolVersion.ISO_13400_2012
        
    def open(self, config: Dict[str, Any]) -> None:
        ip = config.get("ip", "127.0.0.1")
        port = config.get("port", DoipConstants.TCP_DATA_PORT)
        self._source_address = config.get("logical_address", DoipConstants.DEFAULT_LOGICAL_ADDRESS)
        self._target_address = config.get("target_address", DoipConstants.DEFAULT_TARGET_ADDRESS)
        
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(config.get("timeout", 2.0))
        self._socket.connect((ip, port))
        self._connected = True
        
        # Perform routing activation
        self._activate_routing()
        
    def _activate_routing(self):
        payload = DoipPayloadBuilder.build_routing_activation(self._source_address)
        header = DoipPayloadBuilder.build_header(self._version, DoipPayloadType.ROUTING_ACTIVATION_REQUEST, len(payload))
        self._socket.sendall(header + payload)
        
        # Read response
        resp = self._socket.recv(1024)
        if not resp:
            raise ConnectionError("Routing activation failed: No response")
            
    def close(self) -> None:
        if self._socket:
            self._socket.close()
            self._socket = None
        self._connected = False
        
    def send_message(self, message: BusMessage) -> None:
        """通过 DoIP 发送诊断消息"""
        data = message.data if isinstance(message.data, bytes) \
            else bytes(message.data)
        payload = DoipPayloadBuilder.build_diagnostic_message(self._source_address, self._target_address, data)
        header = DoipPayloadBuilder.build_header(self._version, DoipPayloadType.DIAGNOSTIC_MESSAGE, len(payload))
        self._socket.sendall(header + payload)
        
    def receive_message(self, timeout: float = 1.0) -> Optional[BusMessage]:
        """通过 DoIP 接收诊断响应"""
        self._socket.settimeout(timeout)
        try:
            # Read header first
            header_data = self._socket.recv(8)
            if not header_data or len(header_data) < 8:
                return None
                
            parsed_header = DoipPayloadParser.parse_header(header_data)
            if not parsed_header:
                return None
                
            _, payload_type, payload_length = parsed_header
            
            # Read payload
            payload_data = b""
            while len(payload_data) < payload_length:
                chunk = self._socket.recv(payload_length - len(payload_data))
                if not chunk:
                    break
                payload_data += chunk
                
            if payload_type == DoipPayloadType.DIAGNOSTIC_MESSAGE:
                parsed_msg = DoipPayloadParser.parse_diagnostic_message(payload_data)
                if parsed_msg:
                    _, _, user_data = parsed_msg
                    return BusMessage(
                        msg_id=self._target_address,
                        data=user_data,
                        bus_type=BusType.ETHERNET,
                        timestamp=time.time(),
                    )
            
            return None
            
        except socket.timeout:
            return None
        except Exception as e:
            logger.error(f"DoIP Receive error: {e}")
            return None

    @property
    def bus_type(self) -> BusType:
        """当前传输层的总线类型"""
        return BusType.ETHERNET

    @property
    def is_open(self) -> bool:
        return self._connected
