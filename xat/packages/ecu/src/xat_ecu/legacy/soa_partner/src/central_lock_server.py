#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class CentralLockServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        socket.setdefaulttimeout(5)
        logger.info("Central lock Server start to connect to {}".format(self.connect_info))
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.info("Central lock Socket Status: {}".format(self.tcp_socket))
        self.lock_status = 0
        time.sleep(5)
        self.start()

    def lock_status_send(self):
        event = {
        "action":"event",
        "function": "UpdateLockStatusEvent",
        "args": json.dumps({"sts": self.lock_status})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"CentralLockServer:UpdateLockStatusEvent send status failure with broken pipe: {str(e)}")

    def listenning_lock_request(self, timeout=5.0):
        time_s = time.time()
        while True:
            print("current time: ", time.time(), "time_s: ", time_s)
            if time.time() - time_s > timeout:
                logger.info("Timeout to receive data!!")
                return False
            else:
                try:
                    recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                    logger.info("Here to recieve lock request")
                    logger.info("recv data: {0}".format(recv_data))
                    if len(recv_data) == 0:
                        continue
                    logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                    req = json.loads(recv_data.decode("utf-8"))
                    logger.info("Received request: {}".format(req))
                    if req["function"] == "SetDoorCloseLock":
                        return True
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/central_lock_server.py")
                    continue
                print("current time: ", time.time())

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
            self.tcp_socket.settimeout(1)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/central_lock_server.py")
            logger.error(str(e))        
        logger.info("Satrt central lock server")