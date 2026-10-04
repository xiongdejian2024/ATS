import logging
import socket
from typing import Optional, Callable, Any
from xat_ecu.core.interfaces import ITransport

logger = logging.getLogger(__name__)

class EthernetTransport(ITransport):
    """
    Ethernet Transport Layer (TCP/UDP).
    Base for DoIP and SOME/IP transport layers.
    """
    def __init__(self, host: str, port: int, protocol: str = 'tcp', **kwargs):
        self.host = host
        self.port = port
        self.protocol = protocol.lower()
        self.config = kwargs
        self._rx_callback: Optional[Callable[[Any], None]] = None
        self.is_connected = False
        self.sock: Optional[socket.socket] = None

    def connect(self) -> None:
        try:
            if self.protocol == 'tcp':
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, self.port))
            elif self.protocol == 'udp':
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                # For UDP server mode if binding is needed
                if self.config.get('bind', False):
                    self.sock.bind((self.host, self.port))
            self.is_connected = True
            logger.info(f"EthernetTransport connected to {self.host}:{self.port} ({self.protocol})")
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/transport/ethernet.py")
            logger.error(f"Failed to connect EthernetTransport: {e}")
            raise

    def disconnect(self) -> None:
        if self.sock:
            self.sock.close()
            self.sock = None
        self.is_connected = False
        logger.info("EthernetTransport disconnected.")

    def send(self, data: bytes, **kwargs) -> None:
        if not self.is_connected or not self.sock:
            raise RuntimeError("EthernetTransport is not connected")
            
        if self.protocol == 'tcp':
            self.sock.sendall(data)
        elif self.protocol == 'udp':
            dest = kwargs.get('dest', (self.host, self.port))
            self.sock.sendto(data, dest)

    def receive(self, timeout: float) -> Optional[bytes]:
        if not self.is_connected or not self.sock:
            return None
            
        self.sock.settimeout(timeout)
        try:
            if self.protocol == 'tcp':
                data = self.sock.recv(4096)
                if not data:
                    self.disconnect()
                    return None
            elif self.protocol == 'udp':
                data, _ = self.sock.recvfrom(4096)
                
            if self._rx_callback and data:
                self._rx_callback(data)
            return data
        except socket.timeout:
            return None
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/transport/ethernet.py")
            logger.error(f"Error receiving data: {e}")
            return None

    def set_receive_callback(self, callback: Callable[[Any], None]) -> None:
        self._rx_callback = callback
