#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000
import datetime
import time

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class TimemanagementServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.current_status = ""
        time_now = str(datetime.datetime.now())
        [day, time_str] = time_now.split(" ")
        day_list = day.split('-')
        utc_day = int(day_list[2]+day_list[1]+day_list[0][2:])
        utc_time = time_str.replace(':','').replace('.','')[:9]
        time_now = time.time()
        logger.info("当前日期：{0}".format(utc_day))
        self.current_time = {
            "UTCData": utc_day,
            "UTCTime": int(time.time()),
            "TimeZone": 8,
            "SynchronizationStatus": 3,
            "politicalTimeZone": "Asia/Shanghai"
        }
        time.sleep(5)
        self.start()

    def send_response(self):
        while True:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
                if req["function"] == "GetVehicleTimeInfo":
                    resp = {
                        "action": "response",
                        "function": "GetVehicleTimeInfo",
                        "result": json.dumps({"out": self.current_time})
                    }
                    logger.info("Send response: {}".format(json.dumps(resp)))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
                    break
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/vehicle_time_server.py")
                continue

    def notify_time_info(self):
        event = {
            "action": "event",
            "function": "UpdateVehicleTimeInfoEvent",
            "args": json.dumps({"info": self.current_time})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(
                f"TimemanagementServer:UpdateVehicleTimeInfoEvent send periodic status failure with broken pipe: {str(e)}")

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/vehicle_time_server.py")
            logger.error(str(e))