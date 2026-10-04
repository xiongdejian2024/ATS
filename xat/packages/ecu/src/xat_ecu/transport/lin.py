import logging
from typing import Optional, Callable, Any
from xat_ecu.core.interfaces import ITransport, IHardwareAdapter
from xat_ecu.core.types import BusMessage

logger = logging.getLogger(__name__)

class LINTransport(ITransport):
    """
    LIN Transport Layer.
    Supports Master/Slave modes and schedule tables.
    """
    def __init__(self, adapter: IHardwareAdapter, is_master: bool = True, **kwargs):
        self.adapter = adapter
        self.is_master = is_master
        self.config = kwargs
        self._rx_callback: Optional[Callable[[Any], None]] = None
        self.is_connected = False
        self.schedule_tables = {}

    def connect(self) -> None:
        if not self.adapter.is_connected:
            self.adapter.start()
        self.is_connected = True
        logger.info(f"LINTransport connected (Master: {self.is_master}).")

    def disconnect(self) -> None:
        if self.adapter.is_connected:
            self.adapter.stop()
        self.is_connected = False
        logger.info("LINTransport disconnected.")

    def send(self, data: bytes, **kwargs) -> None:
        msg_id = kwargs.get('msg_id', 0)
        msg = BusMessage(
            msg_id=msg_id,
            data=list(data),
            timestamp=0.0,
            bus_name=kwargs.get('bus_name', 'lin'),
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

    def add_schedule_table(self, table_id: int, entries: list) -> None:
        """Add a LIN schedule table"""
        self.schedule_tables[table_id] = entries

    def start_schedule_table(self, table_id: int) -> None:
        """Start executing a schedule table"""
        if table_id in self.schedule_tables:
            logger.info(f"Started LIN schedule table {table_id}")
            # Stub for schedule table execution logic

    def stop_schedule_table(self) -> None:
        """Stop executing schedule table"""
        logger.info("Stopped LIN schedule table")
