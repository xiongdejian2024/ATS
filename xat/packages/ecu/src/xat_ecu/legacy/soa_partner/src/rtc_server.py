#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class RtcAlarmServer:
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bookinfo_list = [{
            "bookType": 1,
            "repeatType": 2,
            "startTime": int(time.time()*1000),
            "stopTime": int((time.time()+2000)*100)
            }]
        time.sleep(5)
        self.start()

    def bookinfo_event_send(self):
        event = {
        "action":"event",
        "function": "UpdateNotifyBookInfoListEvent",
        "args": json.dumps({"bookInfoList": self.bookinfo_list})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"RtcAlarmServer:NotifyBookInfoList send periodic status failure with broken pipe: {str(e)}")

    def bookinfo_response(self):
        while True:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
                if req["function"] == "GetBookInfoList":
                    logger.info("GetBookInfoList: {}".format(req))
                    resp = {
                        "action": "response",
                        "function": "GetBookInfoList",
                        "result": json.dumps({"out": self.bookinfo_list})
                    }
                    logger.info("Send response: {}".format(json.dumps(resp)))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/rtc_server.py")
                continue

    def start_bookinfo_response(self):
        self.bookinfo_response_thread = threading.Thread(name="Bookinfo_Response", target=self.bookinfo_response, )
        self.bookinfo_response_thread.start()

    def stop_bookinfo_response(self):
        self.bookinfo_response_thread.start()

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        # pass
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/rtc_server.py")
            logger.error(str(e))
        logger.info("Satrt to send response of RTCAlarm service")
    
    def start_response(self):
        self.start_bookinfo_response()

    def stop_response(self):
        self.stop_bookinfo_response()
        logger.info("Stop RTCAlarm service")