#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class RtcAlarmClient:
    def __init__(self, connect_info):
        self.connect_info = connect_info
        logger.info("Call client start to connect to {}".format(self.connect_info))
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.info("Call Socket Status: {}".format(self.tcp_socket))
        time.sleep(5)
        self.start()

    def set_bookevent(self,sch_time=180):
        current_time = int(time.time())
        schedule_time = (current_time - current_time%60) + sch_time
        logger.info("当前时间：{0}".format(int(time.time())))
        book_event_info = {
            "serviceName": "low_temp_protect",
            "repeatType": 0,
            "weekDay": 0,
            "rtcTime": schedule_time,
            "timerFlag": "qwer",
            "bookInfo": {
                "bookType": "8",
                "repeatType": 0,
                "weekDay": 0,
                "startTime": schedule_time,
                "stopTime": 0
            },
            "timerHandler": "",
            "rtcFlag": True
            }
        req = {
        "action":"request",
        "function": "SetBookEvent",
        "args": json.dumps({"bookEventInfo": book_event_info})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
            logger.info("Set Rtc schedule time: {0}".format(book_event_info))
        except BrokenPipeError as e:
            logger.error(f"RtcAlarmClient: send set_bookevent failure with broken pipe: {str(e)}")
        return (schedule_time-current_time)

    def get_bookevent(self):
        req = {
        "action":"request",
        "function": "GetBookInfoList",
        "args": None
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"RtcAlarmClient: send set_bookevent failure with broken pipe: {str(e)}")

    def listenning_response(self, func_name="SetBookEvent",timeout=10.0):
        time_s = time.time()
        while time.time()-time_s<timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
                if req["function"] == func_name:
                    return True
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/rtc_client.py")
                continue
        return False

    def listenning_msg(self, timeout=10.0):
        time_s = time.time()
        while time.time()-time_s<timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "UpdateNotifyTimeUpEventInfoEvent":
                    logger.info("Received request: {}".format(req))
                    return True
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/rtc_client.py")
                continue
        return False

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
            self.tcp_socket.settimeout(1)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/rtc_client.py")
            logger.error(str(e))        
        logger.info("Satrt client of RtcAlarm service!!")