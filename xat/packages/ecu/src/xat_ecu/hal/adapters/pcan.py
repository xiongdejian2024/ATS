import logging
from typing import Optional

try:
    import can
    from can.interfaces.pcan import PcanBus
except ImportError:
    can = None
    PcanBus = None

from xat_ecu.core.types import BusMessage
from xat_ecu.hal.adapter import BaseHardwareAdapter
from xat_ecu.hal.registry import AdapterRegistry

logger = logging.getLogger(__name__)

@AdapterRegistry.register("pcan")
class PCANAdapter(BaseHardwareAdapter):
    """
    PCAN硬件适配器。
    PCAN hardware adapter based on python-can.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if PcanBus is None:
            raise ImportError("python-can library with PCAN support is required for PCANAdapter")
        
        self.channel = self.config.get('channel', 'PCAN_USBBUS1')
        self.bitrate = self.config.get('bitrate', 500000)
        self.pcan_obj = None

    def _do_start(self) -> None:
        self.pcan_obj = PcanBus(channel=self.channel, bitrate=self.bitrate, **self.config)

    def _do_stop(self) -> None:
        if self.pcan_obj:
            self.pcan_obj.shutdown()
            self.pcan_obj = None

    def _do_send(self, msg: BusMessage) -> None:
        if self.pcan_obj is None:
            return
            
        can_msg = can.Message(
            arbitration_id=msg.msg_id,
            data=msg.data,
            is_extended_id=msg.msg_id > 0x7FF
        )
        self.pcan_obj.send(can_msg)

    def _do_recv(self, timeout: float) -> Optional[BusMessage]:
        if self.pcan_obj is None:
            return None
            
        can_msg = self.pcan_obj.recv(timeout=timeout)
        if can_msg is None:
            return None
            
        return BusMessage(
            msg_id=can_msg.arbitration_id,
            data=list(can_msg.data),
            timestamp=can_msg.timestamp,
            bus_name=self.channel,
            dlc=can_msg.dlc
        )
