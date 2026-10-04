import logging
from typing import Optional, Callable, Any
from xat_ecu.core.interfaces import ITransport, IHardwareAdapter
from xat_ecu.core.types import BusMessage

logger = logging.getLogger(__name__)

class FlexRayTransport(ITransport):
    """
    FlexRay Transport Layer.
    Supports static and dynamic segment management, slot IDs, and cycles.
    """
    def __init__(self, adapter: IHardwareAdapter, **kwargs):
        self.adapter = adapter
        self.config = kwargs
        self._rx_callback: Optional[Callable[[Any], None]] = None
        self.is_connected = False

    def connect(self) -> None:
        if not self.adapter.is_connected:
            self.adapter.start()
        self.is_connected = True
        logger.info("FlexRayTransport connected.")

    def disconnect(self) -> None:
        if self.adapter.is_connected:
            self.adapter.stop()
        self.is_connected = False
        logger.info("FlexRayTransport disconnected.")

    def send(self, data: bytes, **kwargs) -> None:
        slot_id = kwargs.get('slot_id', 0)
        cycle = kwargs.get('cycle', 0)
        channel = kwargs.get('channel', 'A') # A or B or AB
        
        # Mapping slot_id to msg_id for generic adapter
        msg = BusMessage(
            msg_id=slot_id,
            data=list(data),
            timestamp=0.0,
            bus_name=f"flexray_{channel}",
            dlc=len(data)
        )
        self.adapter.send(msg)

    def receive(self, timeout: float) -> Optional[bytes]:
        msg = self.adapter.recv(timeout)
        if msg:
            if self._rx_callback:
                self._rx_callback(msg)
            return bytes(msg.data)
        return None

    def set_receive_callback(self, callback: Callable[[Any], None]) -> None:
        self._rx_callback = callback
