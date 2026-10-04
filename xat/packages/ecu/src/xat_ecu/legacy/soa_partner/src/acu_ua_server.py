#!/usr/bin/python3


import threading
import time
import socket
import sys
import os
import json
project_path = os.path.join(os.path.realpath(__file__).split("soa_partner")[0], 'soa_partner')
from xat_ecu.legacy.common.logger import logger

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class AcuUaServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stop_loop = False
        self.status_args = {
                            "status": {
                                "status": 1,  # download
                                "downloadStatus": {
                                    "downloadFileSize": 2345,
                                    "totalFileSize": 4567,
                                    "downloadSpeed": 20,
                                    "status": 0
                                },
                                "updateStatus": {
                                    "updateFileSize": 0,
                                    "totalFileSize": 4567,
                                    "status": 255
                                },
                                "errorCode": 0
                            }
                        }
    
    def listening(self):
        while not self.stop_loop:
            recv_data = self.tcp_socket.recv(BUFFER_SIZE)
            if len(recv_data) == 0:
                break

            try:
                recv_data_json = json.loads(recv_data.decode('utf-8'))
                logger.info(recv_data_json)
                if recv_data_json.get("function") == "StartDownload":
                    self.on_start_download()
                if recv_data_json.get("function") == "CancelDownload":
                    self.on_cancle_download()
                if recv_data_json.get("function") == "Activate":
                    self.on_activate()
                if recv_data_json.get("function") == "StartUpdate":
                    self.on_start_update()
            except Exception:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/acu_ua_server.py")
                logger.error("Receive error Message")
    
    def start_listening(self):
        self.listening_thread = threading.Thread(name="UpgradeAgentServerListening", target=self.listening,)
        self.listening_thread.start()

    def start(self):
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/acu_ua_server.py")
            logger.error(str(e))
        self.start_listening()

    def update_download_status_100(self):
        self.status_args["status"]["downloadStatus"]["downloadFileSize"] = 4567
        self.status_args["status"]["downloadStatus"]["downloadSpeed"] = 0
        self.status_args["status"]["downloadStatus"]["status"] = 1
    
    def update_download_status_ready_to_install(self):
        self.status_args["status"]["status"] = 2

    def update_ua_status_to_installing(self):
        self.status_args["status"]["status"] = 3
        self.status_args["status"]["updateStatus"]["updateFileSize"] = 1234
        self.status_args["status"]["updateStatus"]["status"] = 0

    def update_ua_status_to_update_finish(self):
        self.status_args["status"]["status"] = 4
        self.status_args["status"]["updateStatus"]["updateFileSize"] = 4567
        self.status_args["status"]["updateStatus"]["status"] = 3
        

    def on_start_update(self):
        args = {
                "out":{
                    "errorCode": 0
                }
            }
        resp = {
            "action": "response",
            "function": "StartUpdate",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
    
    def on_cancle_download(self):
        args = {
                "out":{
                    "errorCode": 0
                }
            }
        resp = {
            "action": "response",
            "function": "CancelDownload",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
    
    def on_start_download(self):
        args = {
                "out":{
                    "errorCode": 0
                }
            }
        resp = {
            "action": "response",
            "function": "StartDownload",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
    
    def on_activate(self):
        args = {
                "out":{
                    "errorCode": 0
                }
            }
        resp = {
            "action": "response",
            "function": "Activate",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))

    def start_sending_status(self):
        self.status_thread = threading.Thread(name="UpgradeAgentServerStatusSending", target=self.status_periodic_send,)
        self.status_thread.start()

    def status_periodic_send(self, interval=1):
        while not self.stop_loop:
            event = {
            "action":"event",
            "function": "UpdateStatusEvent",
            "args": json.dumps(self.status_args)
            }
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
            logger.info("sending {}".format(json.dumps(event)))
            time.sleep(interval)

    def distroy(self):
        self.stop_loop = True
