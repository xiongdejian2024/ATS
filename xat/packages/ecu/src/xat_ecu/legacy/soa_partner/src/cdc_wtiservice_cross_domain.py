#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class CDCWTI:
    def __init__(self, connect_info, notifyvalue):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.notifyvalue = notifyvalue
        time.sleep(5)
        self.start()

    def notyfyvalue_event_send(self):
        event = {
        "action":"event",
        "function": "UpdateWarningMsgStatusEvent",
        "args": json.dumps({"values": self.notifyvalue})
        }
        logger.info("Send the wti msg: {0}".format(self.notifyvalue))
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))            
        except BrokenPipeError as e:
            logger.error(f"CDCWTI:UpdateWarningMsgStatusEvent send periodic status failure with broken pipe: {str(e)}")

    def notyfyvalue_response(self):
        while True:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
                if req["function"] == "GetWarningMsgStatus":
                    resp = {
                        "action": "response",
                        "function": "GetWarningMsgStatus",
                        "result": json.dumps({"out": self.notifyvalue})
                    }
                    logger.info("Send response: {}".format(json.dumps(resp)))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/cdc_wtiservice_cross_domain.py")
                continue

    def start_notyfyvalue_response(self):
        self.notyfyvalue_response = threading.Thread(name="warningmsglist", target=self.notyfyvalue_response,)
        self.notyfyvalue_response.start()

    def stop_notyfyvalue_response(self):
        self.notyfyvalue_response().join()

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/cdc_wtiservice_cross_domain.py")
            logger.error(str(e))
        logger.info("Start to send response of cdcwti service")
    
    def start_response(self):
        self.start_notyfyvalue_response()

    def stop_response(self):
        self.stop_notyfyvalue_response()
        logger.info("Stop cdcwti service!!!!")