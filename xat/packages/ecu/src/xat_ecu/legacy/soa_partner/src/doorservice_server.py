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

class DoorServiceServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # to do
        self.event_args_dict = {"UpdatelvBatteryStsEvent": {"sts": {"volt": 24.0,
                                                                    "vaild": 3,
                                                                    "battSocRaw": 80.0,
                                                                    "battURaw": 24.0,
                                                                    "battCurrentRaw": 2.5,
                                                                    "battTRaw": 38.0,
                                                                    "battRRaw": 120.0,
                                                                    "battCpEstimdRaw": 35,
                                                                    "battIQuiscFildShoRaw": 32,
                                                                    "battIQuiscFildLongRaw": 28,
                                                                    "battIQuiscAvgRaw": 8,
                                                                    "battCircOpenU": 24.0,
                                                                    "faultSts": False
                                                                    }},
                                 "UpdatelvSysStsEvent": {"sts": 0}
                                }
        self.event_thread = {}
        self.stop_loop = False
        self.openclose_status = {
            "id": 0,
            "isOpen": False # 1:True, 2:False, 0/255:last value
        }
        self.openclose_status_list = [
            {"id": 0, "isOpen": False},
            {"id": 1, "isOpen": False},
            {"id": 2, "isOpen": False},
            {"id": 3, "isOpen": False},
            {"id": 4, "isOpen": False}
        ]
        self.status_list = [
            {"id": 0, "sts": 2},
            {"id": 1, "sts": 2},
            {"id": 2, "sts": 2},
            {"id": 3, "sts": 2},
            {"id": 4, "sts": 2}
        ]
        self.status = {"id": 0,
                       "sts": 2}
        time.sleep(2)
        self.start()

    def notify_openclosestatus_event(self):
        event = {
            "action": "event",
            "function": "UpdateOpenCloseStatusEvent",
            "args": json.dumps({"sts":self.openclose_status})
        }
        try:
            logger.info('Send OpenCloseStatus: {}'.format(event))
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(
                f"DoorServiceServer:UpdateOpenCloseStatusEvent send status failure with broken pipe: {str(e)}")
            
    def openclosestatus_response(self, timeout=2):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "GetOpenCloseStatus":
                    args = {"out": self.openclose_status_list}
                    resp = {
                        "action": "response",
                        "function": "GetOpenCloseStatus",
                        "result": json.dumps(args)
                    }
                    logger.info(json.dumps(resp))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
                    return True
                else:
                    return False
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/doorservice_server.py")
                continue

    def notify_status_event(self):
        event = {
            "action": "event",
            "function": "UpdateStatusEvent",
            "args": json.dumps({"sts":self.status})
        }
        try:
            logger.info('Send Status: {}'.format(event))
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(
                f"DoorServiceServer:UpdateStatusEvent send status failure with broken pipe: {str(e)}")

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
                    args = {"out": self.status_list}
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
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/doorservice_server.py")
                continue
    # def event_send(self, func_name, args, interval=1):
    #     pass
    #     # while not self.stop_loop:
    #     #     event = {
    #     #     "action":"event",
    #     #     "function": func_name,
    #     #     "args": json.dumps(args)
    #     #     }
    #     #     self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
    #     #     # logger.info("sending {}".format(json.dumps(event)))
    #     #     time.sleep(interval)

    # def start_send_events(self):
    #     for fun_name, event in self.event_args_dict.items():
    #         self.start_event_thread(t_name=fun_name, event_args=event)

    
    # def start_event_thread(self, t_name, event_args):
    #     t = threading.Thread(name=t_name, target=self.event_send, args=(t_name, event_args,))
    #     t.start()
    #     self.event_thread.update({t_name: t})

    # def listening(self):
    #     while not self.stop_loop:
    #         recv_data = self.tcp_socket.recv(BUFFER_SIZE)
    #         if len(recv_data) == 0:
    #             break
    #         recv_data_json = json.loads(recv_data.decode('utf-8'))
    #         logger.info(recv_data_json)
    #         if recv_data_json.get("function") == "LockChildLock":
    #             self.on_LockChildLock()
    #         elif recv_data_json.get("function") == "UnLockChildLock":
    #             self.on_UnLockChildLock()
    #         elif recv_data_json.get("function") == "GetChildLock":
    #             self.on_GetChildLock()
    #         elif recv_data_json.get("function") == "GetStatus":
    #             self.on_GetStatus()
    #         # if recv_data_json.get("function") == "GetStatus":
    #         #     self.on_GetStatus()

    # def on_LockChildLock(self):
    #     args = {
    #             "out": None
    #         }
    #     resp = {
    #         "action": "response",
    #         "function": "LockChildLock",
    #         "result": json.dumps(args)
    #     }
    #     logger.info(json.dumps(resp))
    #     self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
    
    # def on_UnLockChildLock(self):
    #     args = {"out": None}
    #     resp = {
    #         "action": "response",
    #         "function": "UnLockChildLock",
    #         "result": json.dumps(args)
    #     }
    #     logger.info(json.dumps(resp))
    #     self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))

    # def on_GetChildLock(self):
    #     LockInfo = [{
    #         "id": 2,
    #         "isLocked": False
    #     },
    #         {
    #             "id": 3,
    #             "isLocked": False
    #         }
    #     ]

    #     args = {"out": LockInfo}
    #     resp = {
    #         "action": "response",
    #         "function": "GetChildLock",
    #         "result": json.dumps(args)
    #     }
    #     logger.info(json.dumps(resp))
    #     self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))

    # def on_GetStatus(self):
    #     StatusInfo = {
    #         "id": 0,
    #         "sts": 4
    #     }
    #     StatusInfo_list = [{"id": 0, "sts": 4}, {"id": 1, "sts": 4}, {"id": 2, "sts": 4}, {"id": 3, "sts": 4}, {"id": 4, "sts": 4}]
    #     args = {"out": StatusInfo_list}
    #     resp = {
    #         "action": "response",
    #         "function": "GetStatus",
    #         "result": json.dumps(args)
    #     }
    #     logger.info(json.dumps(resp))
    #     self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))

    # def start_listening(self):
    #     self.listening_thread = threading.Thread(name="DoorServiceListening", target=self.listening,)
    #     self.listening_thread.start()

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/doorservice_server.py")
            logger.error(str(e))
        self.status_response()
        logger.info("Start Doorservice")
    
    def distroy(self):
        self.stop_loop = True
    
