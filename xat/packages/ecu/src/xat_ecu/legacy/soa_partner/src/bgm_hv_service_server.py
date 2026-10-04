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

class HighVoltageServiceServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.event_args_dict = {
                                "UpdateHVSOCInfoEvent": {"HVSOCInfo": {"realSoc": 80.5, "displaySoc": 90.0}}
                                }
        self.event_thread = {}
        self.stop_loop = False
        self.hv_flag = None

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
            try:
                recv_data_json = json.loads(recv_data.decode('utf-8'))
                logger.info(recv_data_json)
                # if recv_data_json.get("function") == "getGear":
                #     self.on_get_gear()
                if recv_data_json.get("function") == "GetHVSOCInfo":
                    self.on_get_hv_soc()
                if recv_data_json.get("function") == "getHVBatteryVoltage":
                    self.on_get_hv_battery_volt()
                if recv_data_json.get("function") == "GetHVThermalOutOfControl":
                    self.on_get_hv_thermal_errsts()
                if recv_data_json.get("function") == "GetHVBatterySOH":
                    self.on_get_hv_battery_soh()
                if recv_data_json.get("function") == "GetOutput":
                    if self.hv_flag:
                        self.on_getHVActiveSts()
                    else:
                        self.on_getHVActiveSts_off()
            except Exception:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/bgm_hv_service_server.py")
                logger.error("Receive error messge")

    # def on_get_gear(self):
    #     args = {"out": 0}  # GEAR_P
    #     resp = {
    #         "action": "response",
    #         "function": "getGear",
    #         "result": json.dumps(args)
    #     }
    #     logger.info(json.dumps(resp))
    #     self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))

    def on_getHVActiveSts_off(self):
        # hv down
        args = {"out": False}
        resp = {
            "action": "response",
            "function": "GetOutput",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))

    def on_getHVActiveSts(self):
        # hv up
        args = {"out": True}
        resp = {
            "action": "response",
            "function": "GetOutput",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
    
    def on_get_hv_battery_volt(self):
        args = {"out": 20.0}
        resp = {
            "action": "response",
            "function": "getHVBatteryVoltage",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
    
    def on_get_hv_battery_soh(self):
        args = {"out": 80.0}
        resp = {
            "action": "response",
            "function": "GetHVBatterySOH",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
    
    def on_get_hv_thermal_errsts(self):
        args = {"out": False}
        resp = {
            "action": "response",
            "function": "GetHVThermalOutOfControl",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
    
    def on_get_hv_soc(self):
        args = {
                "out":{
                    "realSoc": 80.5,
                    "displaySoc": 90.0
                }
            }
        resp = {
            "action": "response",
            "function": "GetHVSOCInfo",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))

    def start_listening(self):
        self.listening_thread = threading.Thread(name="HighVoltageServiceServerListening", target=self.listening,)
        self.listening_thread.start()

    def start(self):
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/bgm_hv_service_server.py")
            logger.error(str(e))
        self.start_send_events()
        self.start_listening()
    
    def distroy(self):
        self.stop_loop = True
    
