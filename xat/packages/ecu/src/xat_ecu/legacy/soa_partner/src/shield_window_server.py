#!/usr/bin/python3

import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
import time

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class ShieldWindowServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        logger.info("Here to Start Climate Control Service")
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(5)
        self.heat_status = {
            "id": 2, #取值范围0,1,2
            "status": 0,#取值范围0,1,2
        }
        self.heatsts = {
            "id": 2, #取值范围0,1,2
            "status": 0,#取值范围0,1,2
        }       
        self.start()

    def heat_status_send(self):
        event = {
        "action":"event",
        "function": "UpdateHeatStatusEvent",
        "args": json.dumps({"sts": self.heat_status})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"SteerWheelServer:UpdateHeatStatusEvent send status failure with broken pipe: {str(e)}")

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
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/shield_window_server.py")
                    continue
                print("current time: ", time.time())

    def listen_getheat_request(self, response=True, timeout=2.0):
        time_s = time.time()
        while time.time()-time_s<timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "GetHeat":
                    logger.info("getheat: {}".format(req))
                    if response == True:
                        CheckMethodRequest(self.tcp_socket, 'GetHeat', self.heatsts)
                    return True
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/shield_window_server.py")
                continue
        return False

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
            self.tcp_socket.settimeout(2)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/shield_window_server.py")
            logger.error(str(e))
        logger.info("Start ShieldWindowServer")
