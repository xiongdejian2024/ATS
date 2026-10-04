#!/usr/bin/python3

import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
import time

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class LightServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        logger.info("Here to Start Light Service")
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lightturnlamps_status = {
            "mode": 0,
            "priority": 1
        }
        self.lightshowactive = 2
        time.sleep(2)
        self.start()

    def notify_turnlampstatus(self):
        event = {
        "action":"event",
        "function": "UpdateNotifyTurnLampStatusEvent",
        "args": json.dumps({"sts": self.lightturnlamps_status})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"LightServer:NotifyTurnLampStatus send status failure with broken pipe: {str(e)}")

    def getlightshowactivatestatus_response(self, timeout=2.0):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
                if req["function"] == "GetLightShowActivateStatus":
                    logger.info("GetLightShowActivateStatus: {}".format(req))
                    resp = {
                        "action": "response",
                        "function": "GetLightShowActivateStatus",
                        "result": json.dumps({"out": self.lightshowactive})
                    }
                    logger.info("Send response: {}".format(json.dumps(resp)))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/light_server.py")
                continue

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
            self.tcp_socket.settimeout(2)
            self.getlightshowactivatestatus_response()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/light_server.py")
            logger.error(str(e))
        logger.info("Start LightService")