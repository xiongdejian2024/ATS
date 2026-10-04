#!/usr/bin/python3

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




class CdcFotaMasterClient():
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

    def get_release_note_request(self):
        args = {}
        req = {
            "action":"request",
            "function": "GetTaskInfo",
            "args":json.dumps(args)
        }
        self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
    
    def start_download(self):
        args = {}
        req = {
            "action": "request",
            "function": "StartDownload",
            "args": json.dumps(args)
        }
        self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))

    def start_update(self):
        args = {}
        req = {
            "action": "request",
            "function": "StartUpdate",
            "args": json.dumps(args)
        }
        self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        

    def start_listening(self):
        self.listening_thread = threading.Thread(name="FotaMasterClientListening", target=self.listening,)
        self.listening_thread.start()

    def start(self):
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/lvmanagement_serice_client.py")
            logger.error(str(e))
        self.start_listening()

    
    def distroy(self):
        self.stop_loop = True