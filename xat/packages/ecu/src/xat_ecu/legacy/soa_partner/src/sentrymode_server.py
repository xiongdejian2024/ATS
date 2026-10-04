#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class SentryModeServer:
    def __init__(self, connect_info):
        self.connect_info = connect_info
        logger.info("Here to Start Account Service")
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sentry_modests = {"mainSts": 1,
                               "workSts": 2,
                               "perceptionSts": 4,
                               "functionErr": 0}
        time.sleep(5)
        self.start()

    def sentry_event_send(self):
        event = {
        "action":"event",
        "function": "UpdateNotifySentryModeStsEvent",
        "args": json.dumps({"sentryModeSts": self.sentry_modests})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"SentryModeServer:NotifySentryModeSts send periodic status failure with broken pipe: {str(e)}")

    def sentry_response(self):
        while True:
            try:
                recv_data = conn.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
                if req["function"] == "GetSentryModeSts":
                    logger.info("GetSentryModeSts: {}".format(req))
                    resp = {
                        "action": "response",
                        "function": "GetSentryModeSts",
                        "result": json.dumps({"out": self.sentry_modests})
                    }
                    logger.info("Send response: {}".format(json.dumps(resp)))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/sentrymode_server.py")
                continue

    def start_sentry_response(self):
        self.sentry_response_thread = threading.Thread(name="Sentry_Response", target=self.sentry_response, )
        self.sentry_response_thread.start()

    def stop_sentry_response(self):
        self.sentry_response_thread.join()

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/sentrymode_server.py")
            logger.error(str(e))
        logger.info("Start to send response of sentry mode service")

    def stop_response(self):
        self.start_sentry_response()

    def stop_response(self):
        self.stop_sentry_response()
        logger.info("Stop sentry mode service")

