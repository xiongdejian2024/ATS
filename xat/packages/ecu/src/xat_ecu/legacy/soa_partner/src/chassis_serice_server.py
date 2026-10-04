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

class ChassisServiceServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        VehicleSpeed = {
            "speed": 0.0,
            "isVaild": True
        }
        self.event_args_dict = {"UpdateSpeedChangedEvent": {"SpeedFloat": VehicleSpeed}}
        self.gear = 0
        self.event_thread = {}
        self.stop_loop = False
        time.sleep(2)
        self.start()

    def notify_gear_event(self):
        event = {
            "action": "event",
            "function": "UpdateGearEvent",
            "args": json.dumps({"gear": self.gear})
        }
        try:
            logger.info('Send gear status: {}'.format(event))
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(
                f"ChassisServer:UpdateGearEvent send status failure with broken pipe: {str(e)}")
            
    def gear_response(self, timeout=2):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "GetGear":
                    args = {"out": self.gear}
                    resp = {
                        "action": "response",
                        "function": "GetGear",
                        "result": json.dumps(args)
                    }
                    logger.info(json.dumps(resp))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
                    return True
                else:
                    return False
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/chassis_serice_server.py")
                continue


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
            if recv_data_json.get("function") == "GetSpeed":
                self.on_get_veh_speed()
            elif recv_data_json.get("function") == "GetGear":
                self.on_GetGear()

    def on_get_veh_speed(self):
        VehicleSpeed = {
            "speed": 0.0,
            "isVaild": True
        }
        args = {"out": VehicleSpeed}  # <3km/h
        resp = {
            "action": "response",
            "function": "GetSpeed",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))

    def on_GetGear(self):
        args = {"out": 0}  # P
        resp = {
            "action": "response",
            "function": "GetGear",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))


    def start_listening(self):
        self.listening_thread = threading.Thread(name="ChassisServiceServerListening", target=self.listening,)
        self.listening_thread.start()

    def start(self):
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/chassis_serice_server.py")
            logger.error(str(e))
        # self.start_send_events()
        # self.start_listening()
    
    def distroy(self):
        self.stop_loop = True
    
