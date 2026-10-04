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

class SeatServiceServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.seat_status = {
            "seatId": 0, # 0/1/4/5/6
            ""
            "occupiedStatus": 0 # 0:未占位, 1:已占位, 255:数据无效
        }
        self.seat_status_list = [
            {"seatId": 0, "rawSensorStatus": 0,"occupiedStatus": 0},
            {"seatId": 1, "rawSensorStatus": 0,"occupiedStatus": 0},
            {"seatId": 4, "rawSensorStatus": 0,"occupiedStatus": 0},
            {"seatId": 5, "rawSensorStatus": 0,"occupiedStatus": 0},
            {"seatId": 6, "rawSensorStatus": 0,"occupiedStatus": 0}
        ]
        # self.seat_heatvent_status = [{"id": 0, 
        #                              "status": {
        #                                 "heatLevel": 0,
        #                                 "heatTime": 0,
        #                                 "heatWorkStatus": 2,
        #                                 "ventLevel": 0,
        #                                 "ventTime": 0,
        #                                 "ventWorkStatus": 2}
        #                             }]
        self.seat_heatventsts_list = [
            {"id": 0, 
             "status": {
                "heatLevel": 0,
                "heatTime": 0,
                "heatWorkStatus": 2,
                "ventLevel": 0,
                "ventTime": 0,
                "ventWorkStatus": 2}
             },
            {"id": 1, 
             "status": {
                "heatLevel": 0,
                "heatTime": 0,
                "heatWorkStatus": 2,
                "ventLevel": 0,
                "ventTime": 0,
                "ventWorkStatus": 2}
             }
        ]
        self.seat_heatvent_status = {"id": 0, 
                                     "status": {
                                        "heatLevel": 0,
                                        "heatTime": 0,
                                        "heatWorkStatus": 2,
                                        "ventLevel": 0,
                                        "ventTime": 0,
                                        "ventWorkStatus": 2}
                                }
        self.start()

    def notify_seatoccupystatus_event(self):
        event = {
            "action": "event",
            "function": "UpdateSeatOccupyStatusEvent",
            "args": json.dumps({"infos": self.seat_status_list})
        }
        try:
            logger.info('Send SeatOccupyStatus: {}'.format(event))
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(
                f"SeatServer:UpdateSeatOccupyStatusEvent send status failure with broken pipe: {str(e)}")
            
    def notify_seatheatventstatus_event(self):
        event = {
            "action": "event",
            "function": "UpdateSeatHeatVentStatusEvent",
            "args": json.dumps(self.seat_heatvent_status)
        }
        try:
            logger.info('Send SeatHeatVentStatus: {}'.format(event))
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(
                f"SeatServer:SeatHeatVentStatus send status failure with broken pipe: {str(e)}")
            
    def seatoccupystatus_response(self, timeout=2):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "GetOccupied":
                    args = {"out": self.seat_status_list}
                    resp = {
                        "action": "response",
                        "function": "GetOccupied",
                        "result": json.dumps(args)
                    }
                    logger.info(json.dumps(resp))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
                    return True
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/seatservice_server.py")
                continue
        return False

    def getseatheatventstatus_response(self, timeout=2):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "GetSeatHeatVentStatus":
                    logger.info("Received request from TCAM: {0}".format(req))
                    args = {"out": self.seat_heatventsts_list}
                    resp = {
                        "action": "response",
                        "function": "GetSeatHeatVentStatus",
                        "result": json.dumps(args)
                    }
                    logger.info(json.dumps(resp))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
                    return True
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/seatservice_server.py")
                continue
        return False

    def start(self):
        try:
            self.tcp_socket.connect(self.connect_info)
            self.tcp_socket.settimeout(2)
            self.seatoccupystatus_response()
            self.getseatheatventstatus_response()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/seatservice_server.py")
            logger.error(str(e))
        logger.info("Start SeatService")
   