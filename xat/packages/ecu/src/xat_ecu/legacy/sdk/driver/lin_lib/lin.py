import can
import time
from xat_ecu.legacy.common.logger import logger

can.rc['interface'] = 'socketcan_native'


class Lin:
    def __init__(self, bus_name, channel):
        """Initialize a Lin object.  Will initialize a can interface for Lin traffic to be forwarded to.
            Need a physical can interface, since LIN traffic will be forwarded from the PCAN-LIN module to
            a CAN interface.

        Args:
            channel: Can channel to use for Lin forwarding. Will not work with vcan.
        """
        try:
            self.bus_name = bus_name
            self.channel = channel
        except OSError:
            print('LIN init error: {}'.format(self.bus_name))

    def read_single_msg_from_obj(self, msg_obj, timeout=0.2):
        return self.read_single_msg(msg_obj.msg_id, wait=msg_obj.msg_cyc, timeout=timeout)

    def read_single_msg(self, lin_id, wait, timeout, log_error=True):
        """Read a message from the can interface (forwarded from PCAN-LIN physical device)

        Args:
            lin_id: Lin id of message to read
            wait: Wait time for new message data to propagate.
            timeout: Time before function returns if there is no data on bus or message with lin_id is not found.
            log_error: In class BusCmd, the higher layers will log the error, so no need to do it here.
        """
        try:
            time.sleep(wait)
            interface_bus = can.interface.Bus(bustype='socketcan_native', channel=self.channel)
            interface_bus.set_filters([{"can_id": lin_id, "can_mask": 0xff}])

            msg = None
            start_time = time.time()

            while msg is None or msg.arbitration_id != lin_id:
                msg = interface_bus.recv(timeout=timeout)
                elapsed_time = time.time() - start_time

                # timeout if no messages are read after elapsed time
                if elapsed_time > timeout and msg is None:
                    if log_error:
                        logger.error("LIN read timeout: {} not found on {}".format(hex(lin_id), self.bus_name))

                    return None
                else:
                    time.sleep(0.001)  # loop timing
            interface_bus.shutdown()
        except AttributeError:
            logger.error("AttributeError: Message {} not on bus {}".format(hex(lin_id), self.bus_name))

            return None

        return msg

    def write_single_msg(self, lin_id, data, wait=0.2):
        """Write a message to the can interface (forwarded to PCAN-LIN physical device)

        Args:
            lin_id: Lin id of message being written.
            data: list of values being written. Length of message should match length of LIN id message in ldf file.
            wait: time to wait after writing message.  This value is usually the lin message cycle time.
        """
        try:
            interface_bus = can.interface.Bus(bustype='socketcan_native', channel=self.channel)
            # The PCAN-LIN device requires fixed offset of 0x40 to update LIN data via CAN.
            # See PCAN-LIN user manual for more details.
            pcanlin_offset = 0x40
            msg = can.Message(arbitration_id=lin_id + pcanlin_offset,
                              data=data,
                              is_extended_id=False)
            interface_bus.send(msg)
            # LIN is scheduled base.  Need write data to propagate
            # Wait after data modification
            time.sleep(wait)
            interface_bus.shutdown()
        except AttributeError:
            print('LIN write error: {} on {}'.format(hex(lin_id), self.bus_name))


if __name__ == '__main__':
    lin1_bus = Lin('LIN1', 'can10')
    lin2_bus = Lin('LIN2', 'can11')
    lin3_bus = Lin('LIN3', 'can12')
    lin4_bus = Lin('LIN4', 'can13')
    lin5_bus = Lin('LIN5', 'can14')
    lin8_bus = Lin('LIN8', 'can15')
    try:
        while True:
            temp = int(input('input'))
            if temp == 1:
                lin1_bus.write_single_msg(lin_id=0x18, data=[0xaa, 0xbb, 0xcc, 0xdd])
            elif temp == 2:
                lin2_bus.write_single_msg(lin_id=0x14, data=[0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff])
            elif temp == 3:
                lin3_bus.write_single_msg(lin_id=0x2b, data=[0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88])
            elif temp == 4:
                lin4_bus.write_single_msg(lin_id=0x21, data=[0xaa, 0xbb, 0xcc])
            elif temp == 5:
                lin5_bus.write_single_msg(lin_id=0x20, data=[0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88])
            elif temp == 6:
                lin8_bus.write_single_msg(lin_id=0x31, data=[0xab])
    except KeyboardInterrupt:
        time.sleep(1)
