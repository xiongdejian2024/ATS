#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class SteerWheelServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        socket.setdefaulttimeout(5)
        logger.info("Central lock Server start to connect to {}".format(self.connect_info))
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.info("Central lock Socket Status: {}".format(self.tcp_socket))
        self.heat_level = 0
        self.steerheatavailiable = 0
        self.heat_level = 0
        time.sleep(5)
        self.start()

    def steerheatavailiable_send(self):
        event = {
        "action":"event",
        "function": "UpdateSteerHeatAvailiableEvent",
        "args": json.dumps({"status": self.steerheatavailiable})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"SteerWheelServer:UpdateSteerHeatAvailiabEvent send status failure with broken pipe: {str(e)}")

    def heat_status_send(self, heat_level=0):
        event = {
        "action":"event",
        "function": "UpdateHeatEvent",
        "args": json.dumps({"sts": heat_level})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"SteerWheelServer:UpdateHeatEvent send status failure with broken pipe: {str(e)}")

    def listenning_setheat_request(self, timeout=5.0):
        time_s = time.time()
        while True:
            print("current time: ", time.time(), "time_s: ", time_s)
            if time.time() - time_s > timeout:
                logger.info("Timeout to receive data!!")
                return False
            else:
                try:
                    recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                    logger.info("Here to recieve SetHeat request")
                    logger.info("recv data: {0}".format(recv_data))
                    if len(recv_data) == 0:
                        continue
                    logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                    req = json.loads(recv_data.decode("utf-8"))
                    logger.info("Received request: {}".format( req))
                    if req["function"] == "SetHeat":
                        return True
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/steerwheel_server.py")
                    continue
                print("current time: ", time.time())

    def getheat_response(self, timeout=2):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "GetHeat":
                    args = {"out": self.heat_level}
                    resp = {
                        "action": "response",
                        "function": "GetHeat",
                        "result": json.dumps(args)
                    }
                    logger.info(json.dumps(resp))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
                    return True
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/steerwheel_server.py")
                continue
        return False

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
            self.tcp_socket.settimeout(1)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/steerwheel_server.py")
            logger.error(str(e))
        logger.info("Satrt SteerWheel server")