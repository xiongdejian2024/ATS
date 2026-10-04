#!/usr/bin/python3

import socket
import sys
import os
import threading
import json

project_path = os.path.join(os.path.realpath(__file__).split("soa_partner")[0], 'soa_partner')
from xat_ecu.legacy.common.logger import logger

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000


class TcamTaskExecServiceService():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        logger.info(self.connect_info)
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stop_loop = False

    def listening(self):
        while not self.stop_loop:
            recv_data = self.tcp_socket.recv(BUFFER_SIZE)
            if len(recv_data) == 0:
                break
            recv_data_json = json.loads(recv_data.decode('utf-8'))
            logger.info(recv_data_json)

            if recv_data_json.get("function") == "sendProcessRecord":
                logger.info("receiving sendProcessRecord from client")
                self.on_sendprocessrecord()
            elif recv_data_json.get("function") == "setSubTaskExecResult":
                logger.info("receiving setSubTaskExecResult from client")
                self.on_setsubtaskexecresult()


    def start_listening(self):
        self.listening_thread = threading.Thread(name="TcamTaskExecServiceService", target=self.listening, )
        self.listening_thread.start()

    def on_sendprocessrecord(self):
        args = {
            "out": 0
        }
        resp = {
            "action": "response",
            "function": "sendProcessRecord",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        try:
            self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(e)

    def on_setsubtaskexecresult(self):
        args = {}
        resp = {
            "action": "response",
            "function": "setSubTaskExecResult",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        try:
            self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(e)

    def start(self):
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/tcam_task_exec_service.py")
            logger.error(str(e))
        self.start_listening()

    def distroy(self):
        self.stop_loop = True
