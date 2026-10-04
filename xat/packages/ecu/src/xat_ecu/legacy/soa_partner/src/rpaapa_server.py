#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class RPAAPAServer:
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pa_remote_status = {
            "paStatus": 0,
            "lastHandleType": 0,
            "lastHandleUid": 12334567
        }
        self.reminder = {
            "lastHandleType": 0,
            "type": 3
        }
        self.direction = 0


        time.sleep(5)
        self.start()

    def paremotestatus_event_send(self):
        event = {
        "action":"event",
        "function": "UpdateNotifyPARemoteStatusEvent",
        "args": json.dumps({"paRemoteStatus": self.pa_remote_status})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"RPAAPAService:UpdateNotifyPARemoteStatusEvent send periodic status failure with broken pipe: {str(e)}")

    def aparemotereminder_event_send(self):
        event = {
        "action":"event",
        "function": "UpdateNotifyAPARemoteReminderEvent",
        "args": json.dumps({"reminder": self.reminder})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"RPAAPAService:UpdateNotifyAPARemoteReminderEvent send periodic status failure with broken pipe: {str(e)}")

    def parkinglotdirection_event_send(self):
        event = {
        "action":"event",
        "function": "UpdateNotifyParkingLotDirectionEvent",
        "args": json.dumps({"derection": self.direction})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"RPAAPAService:UpdateNotifyParkingLotDirectionEvent send periodic status failure with broken pipe: {str(e)}")

    def start_paremotestatus_event_sending(self):
        self.paremotestatus_event_sending = threading.Thread(name="avpbutton", target=self.paremotestatus_event_send,)
        self.paremotestatus_event_sending.start()

    def stop_paremotestatus_event_sending(self):
        self.paremotestatus_event_sending.join()

    def start_aparemotereminder_event_sending(self):
        self.aparemotereminder_event_sending = threading.Thread(name="countdown", target=self.aparemotereminder_event_send,)
        self.aparemotereminder_event_sending.start()

    def stop_aparemotereminder_event_sending(self):
        self.aparemotereminder_event_sending().join()

    def start_parkinglotdirection_event_sending(self):
        self.parkinglotdirection_event_sending = threading.Thread(name="planningpathtrack", target=self.parkinglotdirection_event_send,)
        self.parkinglotdirection_event_sending.start()

    def stop_parkinglotdirection_event_sending(self):
        self.parkinglotdirection_event_sending().join()

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        # pass

        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/rpaapa_server.py")
            logger.error(str(e))
        # self.start_paremotestatus_event_sending()
        # self.start_aparemotereminder_event_sending()
        # self.start_parkinglotdirection_event_sending()
        logger.info("Satrt to send response of rpaaps service")
