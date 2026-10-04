#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class CentralLockClient:
    def __init__(self, connect_info):
        self.connect_info = connect_info
        logger.info("Central lock client start to connect to {}".format(self.connect_info))
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.info("Central lock Socket Status: {}".format(self.tcp_socket))
        self.lock_cmd = 0
        self.lockreq_source = 2
        time.sleep(5)
        self.start()

    def lock_request_send(self):
        req = {
        "action":"request",
        "function": "SetDoorCloseLock",
        "args": json.dumps({"cmd": self.lock_cmd, "source": self.lockreq_source})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"CentralLockClient: send lock request failure with broken pipe: {str(e)}")

    def lock_response(self):
        while True:
            try:
                recv_data = conn.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/central_lock_client.py")
                continue

    def start_recieving_lock_response(self):
        self.lock_response_thread = threading.Thread(name="Lock_Response", target=self.lock_response, )
        self.lock_response_thread.start()

    def stop_recieving_lock_response(self):
        self.lock_response_thread.join()

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        # pass
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/central_lock_client.py")
            logger.error(str(e))        
        logger.info("Satrt client of central lock client")

    def stop_recieving(self):
        self.start_recieving_lock_response()

    def stop_recieving(self):
        self.stop_recieving_lock_response()
        logger.info("Stop central lock client!!!")