import logging
from typing import Optional, Callable, Any

try:
    import serial
except ImportError:
    serial = None

from xat_ecu.core.interfaces import ITransport

logger = logging.getLogger(__name__)

class SerialTransport(ITransport):
    """
    Serial Port Transport Layer.
    """
    def __init__(self, port: str, baudrate: int = 115200, **kwargs):
        if serial is None:
            raise ImportError("pyserial library is required for SerialTransport")
            
        self.port = port
        self.baudrate = baudrate
        self.config = kwargs
        self._rx_callback: Optional[Callable[[Any], None]] = None
        self.is_connected = False
        self.serial_conn: Optional[serial.Serial] = None

    def connect(self) -> None:
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.config.get('timeout', 1.0),
                bytesize=self.config.get('bytesize', serial.EIGHTBITS),
                parity=self.config.get('parity', serial.PARITY_NONE),
                stopbits=self.config.get('stopbits', serial.STOPBITS_ONE)
            )
            self.is_connected = True
            logger.info(f"SerialTransport connected to {self.port} at {self.baudrate} baud.")
        except Exception as e:
            logger.error(f"Failed to connect SerialTransport: {e}")
            raise

    def disconnect(self) -> None:
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
        self.serial_conn = None
        self.is_connected = False
        logger.info("SerialTransport disconnected.")

    def send(self, data: bytes, **kwargs) -> None:
        if not self.is_connected or not self.serial_conn:
            raise RuntimeError("SerialTransport is not connected")
        self.serial_conn.write(data)

    def receive(self, timeout: float) -> Optional[bytes]:
        if not self.is_connected or not self.serial_conn:
            return None
            
        self.serial_conn.timeout = timeout
        try:
            # Try reading whatever is available
            data = self.serial_conn.read(self.serial_conn.in_waiting or 1)
            if data:
                if self._rx_callback:
                    self._rx_callback(data)
                return data
            return None
        except Exception as e:
            logger.error(f"Error receiving serial data: {e}")
            return None

    def set_receive_callback(self, callback: Callable[[Any], None]) -> None:
        self._rx_callback = callback
