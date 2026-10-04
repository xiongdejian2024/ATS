#!/usr/bin/python3

import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
import time

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class VehicleSetStatusServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        logger.info("Here to Start VehicleSetStatus Service")
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.maintenance_mode = False
        time.sleep(5)
        self.start()

    def maintenancemode_send(self):
        event = {
        "action":"event",
        "function": "UpdateNotifyMaintenanceModeEvent",
        "args": json.dumps({"mode": self.maintenance_mode})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"VehicleSetStatusServer:NotifyMaintenanceMode send status failure with broken pipe: {str(e)}")

    def maintenancemode_response(self, timeout=2):
        time_s = time.time()
        while time.time() - time_s<timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
                if req["function"] == "GetMaintenanceMode":
                    logger.info("GetMaintenanceMode: {}".format(req))
                    resp = {
                        "action": "response",
                        "function": "GetMaintenanceMode",
                        "result": json.dumps({"out": self.maintenance_mode})
                    }
                    logger.info("Send response: {}".format(json.dumps(resp)))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/vehicle_setstatus_server.py")
                continue

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
            self.tcp_socket.settimeout(2)
            self.maintenancemode_response()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/vehicle_setstatus_server.py")
            logger.error(str(e))
        logger.info("Start VehicleSetStatusService")