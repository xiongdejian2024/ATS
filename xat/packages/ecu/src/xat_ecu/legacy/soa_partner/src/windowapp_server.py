#!/usr/bin/python3

import threading
import time
import socket
import sys
import os
import json
project_path = os.path.join(os.path.realpath(__file__).split("soa_partner")[0], 'soa_partner')
from xat_ecu.legacy.common.logger import logger

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class WindowAppServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.start()
        logger.info("Start WindowAppServer!!")

    def listen_setspecificwindowposition_request(self, response=False, timeout=2.0):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "SetSpecificWindowPosition":
                    logger.info("SetSpecificWindowPosition: {}".format(req))
                    if response == True:
                        resp = {
                            "action": "response",
                            "function": "SetSpecificWindowPosition",
                            "result": json.dumps({"out": None})
                        }
                        logger.info("Send response: {}".format(json.dumps(resp)))
                        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
                    return req
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/windowapp_server.py")
                continue

    def start(self):
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/windowapp_server.py")
            logger.error(str(e))