#!/usr/bin/python3

import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
import time

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class OuterRearviewServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        logger.info("Here to Start Climate Control Service")
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(5)
        self.start()

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
            self.tcp_socket.settimeout(2)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/outer_rearview_server.py")
            logger.error(str(e))
        logger.info("Start OuterRearviewServer")