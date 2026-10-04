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

class VehicleModeServiceServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.usagemode = 0
        self.carmode = 0
        self.vehicle_mode_info = {
            "mode": 0,
            "displaySts": 6,
            "subMode": 0,
            "engergyLevel": 0,
            "engergySubSts": 0,
            "isHigh": False,
            "powerLevel": 1,
            "powerSubLevel": 1
        }
        time.sleep(5)
        self.start()

    def notify_carmodechanged_event(self):
        event = {
            "action": "event",
            "function": "UpdateCarModeChangedEvent",
            "args": json.dumps({"mode": self.carmode})
        }
        try:
            logger.info('Send CarModeChanged: {}'.format(event))
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(
                f"VehicleModeServer:UpdateCarModeChangedEvaent send status failure with broken pipe: {str(e)}")

    def notify_usagemodechanged_event(self):
        event = {
            "action": "event",
            "function": "UpdateUsageModeChangedEvent",
            "args": json.dumps({"mode": self.usagemode})
        }
        try:
            logger.info('Send UsageModeChanged: {}'.format(event))
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(
                f"VehicleModeServer:UpdateUsageModeChangedEvent send status failure with broken pipe: {str(e)}")

    def notify_vehiclemode_event(self):
        event = {
            "action": "event",
            "function": "UpdatevehicleModeInfoEvent",
            "args": json.dumps({"mode": self.vehicle_mode_info})
        }
        try:
            logger.info('Send vehicleModeInfo: {}'.format(event))
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(
                f"VehicleModeServer:UpdatevehicleModeInfoEvent send status failure with broken pipe: {str(e)}")

    def carmode_response(self, timeout=2):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "GetCarMode":
                    args = {"out": self.carmode}
                    resp = {
                        "action": "response",
                        "function": "GetCarMode",
                        "result": json.dumps(args)
                    }
                    logger.info(json.dumps(resp))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
                    return True
                else:
                    return False
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/vehicle_mode_service_server.py")
                continue

    def usagemode_response(self, timeout=2):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "GetUsageMode":
                    args = {"out": self.usagemode}
                    resp = {
                        "action": "response",
                        "function": "GetUsageMode",
                        "result": json.dumps(args)
                    }
                    logger.info(json.dumps(resp))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
                    return True
                else:
                    return False
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/vehicle_mode_service_server.py")
                continue

    def vehiclemode_response(self, timeout=2):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "GetUsageMode":
                    args = {"out": self.usagemode}
                    resp = {
                        "action": "response",
                        "function": "GetUsageMode",
                        "result": json.dumps(args)
                    }
                    logger.info(json.dumps(resp))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
                elif req["function"] == "GetCarMode":
                    args = {"out": self.carmode}
                    resp = {
                        "action": "response",
                        "function": "GetCarMode",
                        "result": json.dumps(args)
                    }
                    logger.info(json.dumps(resp))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/vehicle_mode_service_server.py")
                continue

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
            self.tcp_socket.settimeout(2)
            self.vehiclemode_response()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/vehicle_mode_service_server.py")
            logger.error(str(e))
        logger.info("Start vehiclemode service")   
