#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class CarConfigServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.current_status = ""
        self.vin = "LSTEST6R9F2086644"
        self.vin_info = {}
        vin_code = []
        for ch in self.vin:
            vin_code.append(ord(ch))
        self.vin_info["vin"] = vin_code
        self.notify_vincode_loop = True

    def notify_vin(self):
        event = {
        "action":"event",
        "function": "UpdateNotifyVINEvent",
        "args": json.dumps({"vin": self.vin_info})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
            logger.info("Send out vincode from carconfig service")
        except BrokenPipeError as e:
            logger.error(f"CarConfigServer:UpdateNotifyVINEvent send periodic status failure with broken pipe: {str(e)}")

    def listen_getvin(self, response=True, timeout=5):
        time_start = time.time()
        while time.time() - time_start < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
                if req["function"] == "GetVIN":
                    resp = {
                        "action": "response",
                        "function": "GetVIN",
                        "result": json.dumps({"out": self.vin_info})
                    }
                    logger.info("Send response: {}".format(json.dumps(resp)))
                    if response:
                        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
                        return True
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/carconfig_server.py")
                continue
        return False

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
            self.tcp_socket.settimeout(1)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/carconfig_server.py")
            logger.error(str(e))
        logger.info("Satrt to send response and vin code")
