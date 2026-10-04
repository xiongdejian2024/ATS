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


class BgmVTaskExecForwarderService():
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

            if recv_data_json.get("function") == "execTask":
                logger.info("receiving execTask from client")
                self.on_response_exectask()

    def start_listening(self):
        self.listening_thread = threading.Thread(name="BgmVTaskExecForwarderService", target=self.listening, )
        self.listening_thread.start()

    def on_response_exectask(self):
        '''
        enum ExecCmdResult
        {
        @value(100) EXEC_CMD_SUCCESS ,
        @value(200) EXEC_CMD_FAIL ,
        @value(201) EXEC_CMD_REFUSE ,
        @value(202) EXEC_CMD_TIMEOUT
        };
        '''

        args = {
            "out": 100
        }
        resp = {
            "action": "response",
            "function": "CallVehicleApi",
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
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/bgm_task_exec_forwarder_service.py")
            logger.error(str(e))
        self.start_listening()

    def distroy(self):
        self.stop_loop = True
