#!/usr/bin/python3

import threading
import time
import socket
import sys
import os
import json
project_path = os.path.join(os.path.realpath(__file__).split("soa_partner")[0], 'soa_partner')
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class FotaMasterServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        logger.info("Connect info: {0}".format(self.connect_info))
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.current_status = ""
        self.status_args = {
            "status": {
                "taskId": int(time.time()),
                "state": 0,  # idle
                "errorCode": 0
            }
        }
        self.process = {
            "taskId": int(time.time()),
            "state": 0,
            "progress": 0,
            "leftTime": 152,
            "errorCode": 0
        }
        time.sleep(5)
        self.start()

    def update_process(self):
        event = {
        "action":"event",
        "function": "UpdateUpdateProcessEvent",
        "args": json.dumps({"updateProgress": self.process})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"fota master send status failure with broken pipe: {str(e)}")

    def status_send(self):
        event = {
        "action":"event",
        "function": "UpdateStatusEvent",
        "args": json.dumps(self.status_args)
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"fota master send status failure with broken pipe: {str(e)}")

    def status_response(self, timeout=2):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "GetStatus":
                    args = {"out": self.door_status_list}
                    resp = {
                        "action": "response",
                        "function": "GetStatus",
                        "result": json.dumps(args)
                    }
                    logger.info(json.dumps(resp))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
                    return True
                else:
                    return False
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/fota_master_server.py")
                continue

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
            self.tcp_socket.settimeout(2)
            self.status_response()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/fota_master_server.py")
            logger.error(str(e))
        logger.info("Start Fota master service: {0}".format(self.tcp_socket))   