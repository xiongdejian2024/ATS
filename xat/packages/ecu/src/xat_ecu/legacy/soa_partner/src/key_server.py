#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class KeyServer:
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sts = 3
        time.sleep(5)
        self.start()

    def listen_setcarlocaltrace_request(self, response=False, timeout=2.0):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "SetCarLocalTraceRequest":
                    logger.info("SetCarLocalTraceRequest: {}".format(req))
                    if response == True:
                        resp = {
                            "action": "response",
                            "function": "SetCarLocalTraceRequest",
                            "result": json.dumps({"out": None})
                        }
                        logger.info("Send response: {}".format(json.dumps(resp)))
                        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
                    return req
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/key_server.py")
                continue

    def findme_event_send(self):
        event = {
        "action":"event",
        "function": "UpdateNotifyCarLocalTraceActiveStatusEvent",
        "args": json.dumps({"sts": self.sts})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"KeyServer:NotifyCarLocalTraceActiveStatus send periodic status failure with broken pipe: {str(e)}")

    def findme_response(self):
        while True:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
                if req["function"] == "GetCarLocalTraceActiveStatus":
                    logger.info("GetCarLocalTraceActiveStatus: {}".format(req))
                    resp = {
                        "action": "response",
                        "function": "GetCarLocalTraceActiveStatus",
                        "result": json.dumps({"out": self.sts})
                    }
                    logger.info("Send response: {}".format(json.dumps(resp)))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/key_server.py")
                continue

    def start_findme_response(self):
        self.findme_response_thread = threading.Thread(name="Findme_Response", target=self.findme_response, )
        self.findme_response_thread.start()

    def stop_findme_response(self):
        self.findme_response_thread.join()

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/key_server.py")
            logger.error(str(e))
        logger.info("Satrt to send response of key service")
    
    def start_response(self):
        self.start_findme_response()

    def stop_response(self):
        self.stop_findme_response()
        logger.info("Stop key service!!!")