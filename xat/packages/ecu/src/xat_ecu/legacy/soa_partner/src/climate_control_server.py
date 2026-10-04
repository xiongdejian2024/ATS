#!/usr/bin/python3

import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
import time

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class ClimateControlServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        logger.info("Here to Start Climate Control Service")
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ambient_temprawdata  = {
            "temp": -23.1,
            "unit": 0,
            "isValid": True
        }
        self.defroststs = {
            "defrostMax": False,
            "climateDefrost": False
        } 
        self.faultinfo = [
            {"faultId": 0,"faultMsg": ""}
        ]
        self.remote_power_status = 0
        self.defroststs = {
            "defrostMax": False,
            "climateDefrost": False
        } 
        time.sleep(5)
        self.start()

    def ambienttemprawdata_send(self):
        event = {
        "action":"event",
        "function": "UpdateNotifyAmbientTempRawDataEvent",
        "args": json.dumps({"data": self.ambient_temprawdata})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"ClimateControlServer:UpdateNotifyAmbientTempRawDataEvent send status failure with broken pipe: {str(e)}")

    def remoteclimatehvstatus_send(self, remclihvsts=0):
        event = {
        "action":"event",
        "function": "UpdateRemoteClimateHVStatusEvent",
        "args": json.dumps({"sts": remclihvsts})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"ClimateControlServer:UpdateNotifyAmbientTempRawDataEvent send status failure with broken pipe: {str(e)}")

    def notifyacdefroststs_send(self):
        event = {
        "action":"event",
        "function": "UpdateNotifyACDefrostStsEvent",
        "args": json.dumps({"sts": self.defroststs})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"ClimateControlServer:UpdateNotifyAmbientTempRawDataEvent send status failure with broken pipe: {str(e)}")

    def climatefault_send(self):
        event = {
        "action":"event",
        "function": "UpdateClimateFaultEvent",
        "args": json.dumps({"faults": self.faultinfo})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"ClimateControlServer:UpdateNotifyAmbientTempRawDataEvent send status failure with broken pipe: {str(e)}")


    def ambienttemprawdata_response(self, timeout=2):
        time_s = time.time()
        while time.time() - time_s<timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
                if req["function"] == "getAmbientTempRawData":
                    logger.info("getAmbientTempRawData: {}".format(req))
                    resp = {
                        "action": "response",
                        "function": "getAmbientTempRawData",
                        "result": json.dumps({"out": self.maintenance_mode})
                    }
                    logger.info("Send response: {}".format(json.dumps(resp)))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
                    return True
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/climate_control_server.py")
                continue
        return False
    
    def listenning_SetRemoteClimateSwitchToHV_request(self, timeout=5.0):
        time_s = time.time()
        while True:
            print("current time: ", time.time(), "time_s: ", time_s)
            if time.time() - time_s > timeout:
                logger.info("Timeout to receive data!!")
                return False
            else:
                try:
                    recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                    logger.info("Here to recieve SetRemoteClimateSwitchToHV request")
                    logger.info("recv data: {0}".format(recv_data))
                    if len(recv_data) == 0:
                        continue
                    logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                    req = json.loads(recv_data.decode("utf-8"))
                    logger.info("Received request: {}".format( req))
                    if req["function"] == "SetRemoteClimateSwitchToHV":
                        return True
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/climate_control_server.py")
                    continue
                print("current time: ", time.time())

    def listenning_SetFastDefrostMode_request(self, timeout=5.0):
        time_s = time.time()
        while True:
            print("current time: ", time.time(), "time_s: ", time_s)
            if time.time() - time_s > timeout:
                logger.info("Timeout to receive data!!")
                return False
            else:
                try:
                    recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                    logger.info("Here to recieve SetFastDefrostMode request")
                    logger.info("recv data: {0}".format(recv_data))
                    if len(recv_data) == 0:
                        continue
                    logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                    req = json.loads(recv_data.decode("utf-8"))
                    logger.info("Received request: {}".format( req))
                    if req["function"] == "SetFastDefrostMode":
                        return True
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/climate_control_server.py")
                    continue
                print("current time: ", time.time())

    def getremotepowerstatus_response(self, timeout=2):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "GetRemotePowerStatus":
                    args = {"out": self.remote_power_status}
                    resp = {
                        "action": "response",
                        "function": "GetRemotePowerStatus",
                        "result": json.dumps(args)
                    }
                    logger.info(json.dumps(resp))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
                    return True
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/climate_control_server.py")
                continue
        return False

    def getdefroststs_response(self, timeout=2):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "GetDefrostSts":
                    args = {"out": self.defroststs}
                    resp = {
                        "action": "response",
                        "function": "GetDefrostSts",
                        "result": json.dumps(args)
                    }
                    logger.info(json.dumps(resp))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
                    return True
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/climate_control_server.py")
                continue
        return False

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
            self.tcp_socket.settimeout(2)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/climate_control_server.py")
            logger.error(str(e))
        logger.info("Start ClimateControlServer")