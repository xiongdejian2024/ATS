# !/usr/bin/python3

import threading
import time
import socket
import sys
import os
import json
project_path = os.path.join(os.path.realpath(__file__).split("soa_partner")[0], 'soa_partner')
from xat_ecu.legacy.common.logger import logger
from src.socket_recv import *

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000
MESSAGE_LENGTH_BYTES = 4

class TcamTaskExecForwarderClient():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        logger.info(self.connect_info)
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stop_loop = False
        self.engine_taskid = 100

    def listening(self):
        while not self.stop_loop:
            recv_data = self.tcp_socket.recv(BUFFER_SIZE)
            if len(recv_data) == 0:
                break
            recv_data_json = json.loads(recv_data.decode('utf-8'))

            if recv_data_json.get("function") == "execTask":
                logger.info("receiving execTask from Server")
            logger.info(recv_data_json)

    def send_exectask(self):
        # ExecCmdResult execTask(int64 taskId,int32 subTaskId, string name,TaskDetail detail,string executor,string api)
        detail = {"baseLineVer": "6100000050 AA", "batterySoc": 10, "downloadNetType": 3, "dstBaseLineVer": "6100001298 AM",
         "ecusInfo": [{"appPkg": [
             {"dstName": "6160110050AB.vbf", "dstVer": "6160110050 AB", "keyId": "7174bfdfeec24b4dbd21599b3e342099",
              "keyInfo": __import__("os").environ['XAT_CREDENTIAL_SCAN_5A59FD0A46EA9BCFA772'],
              "packageType": 1,
              "signature": "MEUCIQCOIZKb4lE7q2sSX8GqAtGDA0H9sjxjwOqqD+jKh/srEwIgA80pRAWe84iqo+3OTA3G76zS7mPibmksGA7d+COqL5M=",
              "size": 465435936,
              "verUrl": "https://t-ivs-fota.cdn.bcebos.com/test/encrypt/artifactory-ha/filestore/84/84a08f635871f1a192a27ec64cd9ae9db6d27470/6160110050AB.vbf?authorization=bce-auth-v1%2F289a3f3e82b34da4973652d035b59cc3%2F2022-04-25T06%3A23%3A31Z%2F-1%2F%2Fb32f79c0eb582d6febd0f886def2543b6502a7159373fb2cc8f211dbb2c4888a"}],
                        "ecuGroup": 1, "ecuHWpn": "SDUI6010000001", "ecuName": "BGM", "ecuOrder": 1, "otherPkg": [],
                       "sblPkg": []}], "installMode": 1, "releaseNote": "123", "smallBatterySoc": 70, "taskId": 123,
         "taskName": "测试BGM", "type": 6}
        args = {
            "taskId": self.engine_taskid,
            "subTaskId": 1,
            "name": "engine100",
            "detail": detail,
            "executor": "v.ota.fota",
            "api": "CreateCallback"
        }
        req = {
            "action": "request",
            "function": "execTask",
            "args": json.dumps(args)
        }
        self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))

    def start_listening(self):
        self.listening_thread = threading.Thread(name="TcamTaskExecForwarderClient", target=self.listening, )
        self.listening_thread.start()

    def start(self):
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/tcam_task_exec_forwarder_client.py")
            logger.error(str(e))
        self.start_listening()

    def distroy(self):
        self.stop_loop = True
