#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class NaviServer:
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sdmapmatchinfo = {
            "position": {
                            "x": 31.2313,
                            "y": 121.546237,
                            "z": 180.25728
                            },
            "speed": 0, # (m/s)
            "angle": 0, # (0~360)
            "timestamp": 0, # (ms)
            "probability": 0 # (0~1000)
            }
        time.sleep(5)
        self.start()

    def samapmatch_event_send(self):
        event = {
        "action":"event",
        "function": "UpdateNotifySDMapMatchInfoEvent",
        "args": json.dumps({"matchInfo": self.sdmapmatchinfo})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"NaviServer:NotifySDMapMatchInfo send periodic status failure with broken pipe: {str(e)}")

    def sdmapmatchino_response(self):
        while True:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
                if req["function"] == "GetSDMapMatchInfo":
                    logger.info("GetSDMapMatchInfo: {}".format(req))
                    resp = {
                        "action": "response",
                        "function": "GetSDMapMatchInfo",
                        "result": json.dumps({"out": self.sdmapmatchinfo})
                    }
                    logger.info("Send response: {}".format(json.dumps(resp)))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/navi_server.py")
                continue

    def start_sdmapmatchinfo_response(self):
        self.sdmapmatchinfo_response_thread = threading.Thread(name="Sdmapmatchinfo_Response", target=self.sdmapmatchino_response, )
        self.sdmapmatchinfo_response_thread.start()

    def stop_sdmapmatchinfo_response(self):
        self.sdmapmatchinfo_response_thread.join()

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/navi_server.py")
            logger.error(str(e))
        logger.info("Start to send response of Navi service")
    
    def start_response(self):
        self.start_sdmapmatchinfo_response()

    def stop_response(self):
        self.stop_sdmapmatchinfo_response()
        logger.info("Stop Navi service")