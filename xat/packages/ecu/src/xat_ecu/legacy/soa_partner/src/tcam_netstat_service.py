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

class TcamNetStatService():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        netstatus_apn1 = {
            "ApnName": 1,
            "ApnSts": 0,
            "NetForm": 2,
            "SignalLevel": 4,
            "SignalBm": -50,
            "HasDataTransmission": True
        }
        netstatus_apn2 = {
            "ApnName": 2,
            "ApnSts": 0,
            "NetForm": 2,
            "SignalLevel": 4,
            "SignalBm": -50,
            "HasDataTransmission": True
        }
        netstatus_apn3 = {
            "ApnName": 3,
            "ApnSts": 0,
            "NetForm": 2,
            "SignalLevel": 4,
            "SignalBm": -50,
            "HasDataTransmission": True
        }
        netstatus_apn4 = {
            "ApnName": 4,
            "ApnSts": 0,
            "NetForm": 2,
            "SignalLevel": 4,
            "SignalBm": -50,
            "HasDataTransmission": True
        }
        netstsarr = [netstatus_apn1, netstatus_apn2, netstatus_apn3, netstatus_apn4]
        self.event_args_dict = {
            "UpdateNetWorkStsEvent": {"NetStsArr": netstsarr}
        }
        self.event_thread = {}
        self.stop_loop = False

    def event_send(self, func_name, args, interval=1):
        while not self.stop_loop:
            event = {
            "action":"event",
            "function": func_name,
            "args": json.dumps(args)
            }
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
            # logger.info("sending {}".format(json.dumps(event)))
            time.sleep(interval)

    def start_send_events(self):
        for fun_name, event in self.event_args_dict.items():
            self.start_event_thread(t_name=fun_name, event_args=event)

    
    def start_event_thread(self, t_name, event_args):
        t = threading.Thread(name=t_name, target=self.event_send, args=(t_name, event_args,))
        t.start()
        self.event_thread.update({t_name: t})

    def listening(self):
        while not self.stop_loop:
            recv_data = self.tcp_socket.recv(BUFFER_SIZE)
            if len(recv_data) == 0:
                break
            recv_data_json = json.loads(recv_data.decode('utf-8'))
            logger.info(recv_data_json)
            if recv_data_json.get("function") == "GetNetSts":
                self.on_GetNetSts()

    def on_GetNetSts(self):
        netstatus_apn1 = {
            "ApnName": 1,
            "ApnSts": 0,
            "NetForm": 2,
            "SignalLevel": 4,
            "SignalBm": -50,
            "HasDataTransmission": True
        }
        netstatus_apn2 = {
            "ApnName": 2,
            "ApnSts": 0,
            "NetForm": 2,
            "SignalLevel": 4,
            "SignalBm": -50,
            "HasDataTransmission": True
        }
        netstatus_apn3 = {
            "ApnName": 3,
            "ApnSts": 0,
            "NetForm": 2,
            "SignalLevel": 4,
            "SignalBm": -50,
            "HasDataTransmission": True
        }
        netstatus_apn4 = {
            "ApnName": 4,
            "ApnSts": 0,
            "NetForm": 2,
            "SignalLevel": 4,
            "SignalBm": -50,
            "HasDataTransmission": True
        }
        NetStatus = [netstatus_apn1, netstatus_apn2, netstatus_apn3, netstatus_apn4]
        args = {"out": NetStatus}
        resp = {
            "action": "response",
            "function": "GetNetSts",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))


    def start_listening(self):
        self.listening_thread = threading.Thread(name="VehicleModeServiceListening", target=self.listening,)
        self.listening_thread.start()

    def start(self):
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/tcam_netstat_service.py")
            logger.error(str(e))
        self.start_send_events()
        self.start_listening()
    
    def distroy(self):
        self.stop_loop = True
    
