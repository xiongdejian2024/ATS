#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class WTI_Autodrive:
    def __init__(self, connect_info, warningmsglist, telltalelist):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.warningmsglist = warningmsglist
        self.telltalelist = telltalelist
        time.sleep(5)
        self.start()

    def telltalelist_event_send(self):
        event = {
        "action":"event",
        "function": "UpdateTelltaleListEvent",
        "args": json.dumps({"list": self.telltalelist})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"WTIAutoDriveServer:UpdateTelltaleListEvent send periodic status failure with broken pipe: {str(e)}")

    def telltalelist_response(self):
        while True:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
                if req["function"] == "GetTelltaleList":
                    resp = {
                        "action": "response",
                        "function": "GetTelltaleList",
                        "result": json.dumps({"out": self.telltalelist})
                    }
                    logger.info("Send response: {}".format(json.dumps(resp)))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/wti_autodrive_server.py")
                continue

    def warningmsglist_event_send(self):
        event = {
        "action":"event",
        "function": "UpdateWarningMsgListEvent",
        "args": json.dumps({"list": self.warningmsglist})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"WTIAutoDriveServer:UpdateWarningMsgListEvent send periodic status failure with broken pipe: {str(e)}")

    def warningmsglist_response(self):
        while True:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
                if req["function"] == "GetWarningMsgList":
                    resp = {
                        "action": "response",
                        "function": "GetWarningMsgList",
                        "result": json.dumps({"out": self.warningmsglist})
                    }
                    logger.info("Send response: {}".format(json.dumps(resp)))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/wti_autodrive_server.py")
                continue

    def start_telltalelist_response(self):
        self.telltalelist_response = threading.Thread(name="telltalelist", target=self.telltalelist_response,)
        self.telltalelist_response.start()

    def stop_telltalelist_response(self):
        self.telltalelist_response.join()

    def start_warningmsglist_response(self):
        self.warningmsglist_response = threading.Thread(name="warningmsglist", target=self.warningmsglist_response,)
        self.warningmsglist_response.start()

    def stop_warningmsglist_response(self):
        self.warningmsglist_response().join()

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/wti_autodrive_server.py")
            logger.error(str(e))
        logger.info("Start to send response of wti service")

    def stop_response(self):
        self.start_telltalelist_response()
        self.start_warningmsglist_response()

    def stop_response(self):
        self.stop_telltalelist_response()
        self.stop_warningmsglist_response()
        logger.info("Stop wti auto service!!")