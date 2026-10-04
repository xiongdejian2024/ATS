#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class TyreServer:
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pressure_info = {
            "id": 0,
            "pressure": 200
            }
        self.temp_info = {
            "id": 0,
            "temperature": 35
            }
        time.sleep(5)
        self.start()

    def tyrepress_event_send(self):
        event = {
        "action":"event",
        "function": "UpdatePressureEvent",
        "args": json.dumps({"sts": self.pressure_info})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"TyreServer:UpdatePressureEvent send periodic status failure with broken pipe: {str(e)}")

    def tyretemp_event_send(self):
        event = {
        "action":"event",
        "function": "UpdateTemperatureEvent",
        "args": json.dumps({"sts": self.temp_info})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"TyreServer:UpdateTemperatureEvent send periodic status failure with broken pipe: {str(e)}")

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        # pass
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/tyre_server.py")
            logger.error(str(e))
        logger.info("Satrt to send response of centrallock service")
