#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class CallClient:
    def __init__(self, connect_info):
        self.connect_info = connect_info
        logger.info("Call client start to connect to {}".format(self.connect_info))
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.info("Call Socket Status: {}".format(self.tcp_socket))
        self.call_operate_cmd = 0
        self.call_req_src = 1
        time.sleep(5)
        self.start()

    def set_ecall_mode(self):
        req = {
        "action":"request",
        "function": "SetECallMode",
        "args": json.dumps({"Cmd": self.call_operate_cmd, "Src": self.call_req_src})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"CallService: send call request request failure with broken pipe: {str(e)}")

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/call_client.py")
            logger.error(str(e))        
        logger.info("Satrt client of call service!!")