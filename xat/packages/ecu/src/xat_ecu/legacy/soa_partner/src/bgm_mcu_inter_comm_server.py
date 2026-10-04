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

class BgmMcuInterCommService():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        vin = "LSTEST6R9F2086650"
        vin = tuple(bytes(vin, encoding="utf-8"))
        self.event_args_dict = {"UpdateNotifyVINEvent": {"vinCode": {"vin": vin}}
                                }
        self.event_thread = {}
        self.stop_loop = False
        self.fota_status = None

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
                if recv_data_json:
                    if recv_data_json.get("function") == "SetFotaSts":
                        self.on_SetFotaSts()
                        args_json = recv_data_json.get("args")
                        args = json.loads(args_json)
                        state = args.get("sts")
                        self.fota_status = state
                    elif recv_data_json.get("function") == "SetVFCReqDiagnostic":
                        self.on_SetVFCReqDiagnostic()
                    elif recv_data_json.get("function") == "SetVFCReqTelematicsConnectivity":
                        self.on_SetVFCReqTelematicsConnectivity()

            except Exception:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/bgm_mcu_inter_comm_server.py")
                logger.error("Receive error Message")

            # if recv_data_json.get("function") == "getHVBatterySOC":
            #     self.on_get_hv_soc()
            # if recv_data_json.get("function") == "getHVBatteryVoltage":
            #     self.on_get_hv_battery_volt()
            # if recv_data_json.get("function") == "getHVThermalErrSts":
            #     self.on_get_hv_thermal_errsts()
            # if recv_data_json.get("function") == "getBatterySOH":
            #     self.on_get_hv_battery_soh()

    def on_SetVFCReqDiagnostic(self):
        args = {"out": None}
        resp = {
            "action": "response",
            "function": "SetVFCReqDiagnostic",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))

    def on_SetVFCReqTelematicsConnectivity(self):
        args = {"out": None}
        resp = {
            "action": "response",
            "function": "SetVFCReqTelematicsConnectivity",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))

    def on_SetFotaSts(self):
        args = {"out": None}
        resp = {
            "action": "response",
            "function": "SetFotaSts",
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
            "function": "getBatterySOH",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
    
    def on_get_hv_thermal_errsts(self):
        args = {"out": False}
        resp = {
            "action": "response",
            "function": "getHVThermalErrSts",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
    
    def on_get_hv_soc(self):
        args = {
                "out":{
                    "realSOC": 80.5,
                    "displaySoc": 90.0
                }
            }
        resp = {
            "action": "response",
            "function": "getHVBatterySOC",
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
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/bgm_mcu_inter_comm_server.py")
            logger.error(str(e))
        self.start_send_events()
        self.start_listening()
    
    def distroy(self):
        self.stop_loop = True
    
