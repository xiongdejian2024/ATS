# -*- coding: utf-8 -*-
"""
@File        : can_listener.py
@Author      : quan.sun@jiduauto.com
@Time        : 2019-12-25 13:50
@Description : can listener class, porting from Alpha2 project
@Examples    :

"""

import can
import time
from xat_ecu.legacy.common.logger import logger


class CanListener:
    def __init__(self, bus_name, channel, can_id=None):
        """
        Initialize a CanListener object.
        This is mainly used to listen for non-cyclic messages being routed to
        a channel such as Diagnostic response messages.
        :param bus_name: bus name, such as 'bodycan', 'ept'
        :param channel: Channel to to listen on. such as 'can0'
        :param can_id: Can id of message to perform a listen
        """
        try:
            self.can_id = can_id
            self.bus_name = bus_name
            self.channel = channel
            self.interface_bus = can.interface.Bus(bustype='socketcan',
                                                   channel=self.channel)
            # add a flag that indicate socketcan is closed or not
            self.exit_flag = False
            if can_id:
                self.interface_bus.set_filters([{'can_id': self.can_id,
                                                 'can_mask': 0xffff}])
            else:
                pass
                # Just do nothing in this case, as can_filters is unexpected in this case.
                # self.interface_bus.set_filters(can_filters=None)
            self.listener = can.BufferedReader()
            self.async_listener = can.AsyncBufferedReader()
            self.notifier = can.Notifier(self.interface_bus, [self.listener])
            time.sleep(0.001)
        except OSError:
            logger.error('CanListener init error: {}'.format(self.bus_name))

    def get_msg(self, timeout):
        """
        Get a message from the listener buffered reader.
        :param timeout: Time before function returns if there is no
                        data on bus or message with can_id is not found
        :return:
        """
        try:
            start_time = time.time()
            msg = None
            while msg is None or (self.can_id is not None
                                  and msg.arbitration_id != self.can_id):
                msg = self.listener.get_message(timeout=timeout)
                if msg is not None:
                    return msg
                elapsed_time = time.time() - start_time

                # Timeout if no messages arrive within the elapsed time.
                #
                if elapsed_time > timeout and msg is None:
                    msg_id = "next_msg_id" if self.can_id is None else hex(self.can_id)

                    logger.error("CanListener read timeout: {} not found on {}".format(msg_id, self.bus_name))

                    return None
                else:
                    time.sleep(0.001)  # loop timing
        except AttributeError:
            return None
        return msg

    def get_msg_with_can_id(self, can_id, timeout):
        """
        Get a message from the listener buffered reader.
        :param timeout: Time before function returns if there is no
                        data on bus or message with can_id is not found
        :return:
        """
        try:
            start_time = time.time()
            msg = None
            while msg is None or (self.can_id is not None
                                  and msg.arbitration_id != self.can_id):
                msg = self.listener.get_message(timeout=timeout)
                if msg is not None:
                    if msg.arbitration_id == can_id:
                        return msg
                elapsed_time = time.time() - start_time
                # timeout if no messages are read after elapsed time
                if elapsed_time > timeout and msg is None:
                    # TODO: Restore this back to .error() soonest!
                    logger.warning('CanListener read timeout: \
                        {} not found on {}'.format(hex(self.can_id), self.bus_name))
                    return None
                else:
                    time.sleep(0.001)  # loop timing
        except AttributeError:
            return None
        return msg

    def get_all_messages_in_time_range(self, time_range=1):
        """
        Get all messages with the ID in time range
        :param time_range: The time range for capturing all messages
        :return:
        """
        try:
            start_time = time.time()
            msg = None
            while msg is None or (self.can_id is not None
                                  and msg.arbitration_id != self.can_id):
                msg = self.async_listener.get_message()

                if msg is not None:
                    return msg
                elapsed_time = time.time() - start_time
                if elapsed_time > time_range and msg is None:
                    logger.error('CanListener read timeout: \
                        {} not found on {}'.format(hex(self.can_id), self.bus_name))
                    return None
                else:
                    time.sleep(0.001)
        except AttributeError:
            return None
        return msg

    def close(self):
        """
        Close CanListener by stopping notifier, listener, and interface_bus
        :return:
        """
        try:
            self.listener.stop()
            self.notifier.stop()
            if self.async_listener:
                self.async_listener.stop()
            self.interface_bus.socket.close()
            self.interface_bus.shutdown()
        except AttributeError:
            logger.error('CanListener close error: \
            {}'.format(self.bus_name))
        else:
            self.exit_flag = True