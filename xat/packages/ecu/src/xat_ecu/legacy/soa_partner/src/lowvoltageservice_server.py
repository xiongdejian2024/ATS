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

class LowVoltageServiceServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.event_args_dict = {"UpdateBatteryStatusEvent": {"status": {"voltage": 24.0,
                       "rawSoc": 80.0,
                       "rawVoltage": 24.0,
                       "rawCurrent": 2.5,
                       "rawTemperature": 38.0,
                       "rawInternalResistance": 120.0,
                       "estimatedCapacity": 35,
                       "averageQuiescentCurrentShort": 32,
                       "averageQuiescentCurrentLong": 28,
                       "averageQuiescentCurrentLevel": 8,
                       "openCircuitVoltage": 24.0,
                       "bmsConsistencyFault": 0
                     }},
                                 "UpdatelvSysStsEvent": {"sts": 0}
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
            if recv_data_json.get("function") == "GetBatteryStatus":
                self.on_lv_battery_sts()
            if recv_data_json.get("function") == "getLVSysSts":
                self.on_lv_sys_sts()

    def on_lv_battery_sts(self):
        args = {
                "out":{"voltage": 24.0,
                       "rawSoc": 80.0,
                       "rawVoltage": 24.0,
                       "rawCurrent": 2.5,
                       "rawTemperature": 38.0,
                       "rawInternalResistance": 120.0,
                       "estimatedCapacity": 35,
                       "averageQuiescentCurrentShort": 32,
                       "averageQuiescentCurrentLong": 28,
                       "averageQuiescentCurrentLevel": 8,
                       "openCircuitVoltage": 24.0,
                       "bmsConsistencyFault": 0
                     }
            }
        resp = {
            "action": "response",
            "function": "GetBatteryStatus",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
    
    def on_lv_sys_sts(self):
        args = {"out": 0}
        resp = {
            "action": "response",
            "function": "getLVSysSts",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))

    def start_listening(self):
        self.listening_thread = threading.Thread(name="LVManagementServiceListening", target=self.listening,)
        self.listening_thread.start()

    def start(self):
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/lowvoltageservice_server.py")
            logger.error(str(e))
        self.start_send_events()
        self.start_listening()
    
    def distroy(self):
        self.stop_loop = True
    
