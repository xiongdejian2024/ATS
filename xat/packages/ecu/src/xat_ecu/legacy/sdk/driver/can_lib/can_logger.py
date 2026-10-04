# -*- coding: utf-8 -*-
"""
@File        : cgw_logger.py
@Description : description about this file
@Examples    : example of how to use it
"""

import can
import time
from xat_ecu.legacy.common.logger import logger
from can.io.logger import Logger
import os
from pathlib import Path


class CanLogger:
    def __init__(self, bus_list, suite_name, can_id=None, log_type='.log'):
        """
        Initialize a CanListener object.
        This is mainly used to listen for non-cyclic messages being routed to
        a channel such as Diagnostic response messages.
        :param bus_list: bus list, such as 'bodycan', 'ept',['bodycan','ept']
        :param can_id: Can id of message to perform a listen
        :param suite_name: Test suite name called the Canlogger, such as TestEvm
        :param log_type: default is .log, support .asc, .blf,.csv,.db
         * .asc: :class:`can.ASCWriter`
          * .blf :class:`can.BLFWriter`
          * .csv: :class:`can.CSVWriter`
          * .db: :class:`can.SqliteWriter`
          * .log :class:`can.CanutilsLogWriter`
          * other: :class:`can.Printer`
        """
        try:
            self.can_id = can_id
            self.bus_list = bus_list
            # self.interface_bus = can.interface.Bus(bustype='socketcan',
            #                                        channel=self.channel)
            self.log_path = './logs/' + suite_name
            Path(self.log_path).mkdir(parents=True, exist_ok=True)
            # if can_id:
            #     self.interface_bus.set_filters([{'can_id': self.can_id,
            #                                      'can_mask': 0xffff}])

            local_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            # dir_path = os.path.dirname(os.path.realpath(__file__))

            log_file = os.path.join(self.log_path, '_' + local_time + log_type)
            self.logger = Logger(log_file)
            self.notifier = can.Notifier(self.bus_list, [self.logger])
            time.sleep(0.001)
        except OSError:
            logger.error('CanListener init error: {}'.format(self.bus_list))

    def remove_bus(self):
        pass

    def add_bus(self, bus_inst):
        self.notifier.add_bus(bus_inst)

    def zip_logger(self):
        pass

    def decode_logger(self):
        pass

    def close(self):
        """
        Close CanListener by stopping notifier, listener, and interface_bus
        :return:
        """
        # Need to close all bus firstly, it may depend on SocketCan
        self.notifier.stop()
