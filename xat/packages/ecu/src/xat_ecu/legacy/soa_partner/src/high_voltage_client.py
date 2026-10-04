#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class HighVoltageClient:
    def __init__(self, connect_info):
        self.connect_info = connect_info
        logger.info("Central lock client start to connect to {}".format(self.connect_info))
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.info("Central lock Socket Status: {}".format(self.tcp_socket))
        self.maxsoc = 89
        self.current_range_info = {
            "type": 0,
            "CLTCRange": 801,
            "estimatedRange":802
        }
        self.power = 10.1
        time.sleep(5)
        self.start()

    def set_maxchargsoc(self):
        req = {
        "action":"request",
        "function": "SetChargeSoc",
        "args": json.dumps({"soc": self.maxsoc})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"HighVoltageClient: send set_maxchargsoc failure with broken pipe: {str(e)}")

    def set_averagepowerconsume(self):
        req = {
        "action":"request",
        "function": "SetAveragePowerConsume",
        "args": json.dumps({"power": self.power})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"HighVoltageClient: send set_averagepowerconsume failure with broken pipe: {str(e)}")

    def set_range(self):
        req = {
        "action":"request",
        "function": "SetRange",
        "args": json.dumps({"infos": self.current_range_info})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"HighVoltageClient: send set_range failure with broken pipe: {str(e)}")

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/high_voltage_client.py")
            logger.error(str(e))
        logger.info("Satrt client of HighVoltageService")