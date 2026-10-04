#!/usr/bin/python3

import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
import time

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class TailGateServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        logger.info("Here to Start TailGate Service")
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tailgate_status = 2
        self.openclosestatus = False
        time.sleep(2)
        self.start()

    def tailgate_openclosestatus_send(self):
        event = {
        "action":"event",
        "function": "UpdateOpenCloseStatusEvent",
        "args": json.dumps({"sts": self.openclosestatus})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"TailGateServer:UpdateOpenCloseStatusEvent send status failure with broken pipe: {str(e)}")

    def tailgate_openclosestatus_response(self, timeout=2.0):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
                if req["function"] == "GetOpenCloseStatus":
                    logger.info("GetOpenCloseStatus: {}".format(req))
                    resp = {
                        "action": "response",
                        "function": "GetOpenCloseStatus",
                        "result": json.dumps({"out": self.openclosestatus})
                    }
                    logger.info("Send response: {}".format(json.dumps(resp)))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/tailgate_server.py")
                continue

    def tailgate_status_send(self):
        event = {
        "action":"event",
        "function": "UpdateStatusEvent",
        "args": json.dumps({"sts": self.tailgate_status})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"TailGateServer:UpdateStatusEvent send status failure with broken pipe: {str(e)}")

    def tailgate_status_response(self, timeout=2.0):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
                if req["function"] == "GetStatus":
                    logger.info("GetStatus: {}".format(req))
                    resp = {
                        "action": "response",
                        "function": "GetStatus",
                        "result": json.dumps({"out": self.tailgate_status})
                    }
                    logger.info("Send response: {}".format(json.dumps(resp)))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/tailgate_server.py")
                continue

    def listen_settailgate_request(self, response=False, timeout=2.0):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "SetTailGate":
                    logger.info("SetTailGate: {}".format(req))
                    if response == True:
                        resp = {
                            "action": "response",
                            "function": "SetTailGate",
                            "result": json.dumps({"out": None})
                        }
                        logger.info("Send response: {}".format(json.dumps(resp)))
                        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
                    return req
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/tailgate_server.py")
                continue

    def listen_setposition_request(self, response=False, timeout=2.0):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "SetPosition":
                    logger.info("SetPosition: {}".format(req))
                    if response == True:
                        resp = {
                            "action": "response",
                            "function": "SetPosition",
                            "result": json.dumps({"out": None})
                        }
                        logger.info("Send response: {}".format(json.dumps(resp)))
                        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
                    return req
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/tailgate_server.py")
                continue


    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
            self.tcp_socket.settimeout(2)
            self.tailgate_status_response()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/tailgate_server.py")
            logger.error(str(e))
        logger.info("Start TailGateService")