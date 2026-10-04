#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class AVPServer:
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.button_type = {
            "RPAFront": 0,
            "RPARear": 0,
            "RPALeftTurn": 0,
            "RPARightTurn": 0,
            "parkOutFrontLeft": 0,
            "parkOutFrontRight": 0,
            "parkOutRearLeft": 0,
            "parkOutRearRight": 0,
            "parkOutLeftFront": 0,
            "parkOutRightFront": 0,
            "parkOutFront": 0,
            "parkOutRear": 0,
            "button1": 0,
            "button2": 0,
            "button3": 0,
            "button4": 0
        }
        self.timer_count = 0
        self.path_track = {
            "pathTrack": [],
            "targetLotLocation": {
                "parkLotId": 2313,
                "parkLotType": 0,
                "parkLotSts": 0,
                "markFlag": 0,
                "parkLotForm": 0,
                "specialFlag": 0,
                "occupySts": 0,
                "cornerPoint1": {
                    "location_X": 0.0,
                    "location_Y": 0.0,
                    "location_Z": 0.0
                },
                "cornerPoint2": {
                    "location_X": 0.0,
                    "location_Y": 0.0,
                    "location_Z": 0.0
                },
                "cornerPoint3": {
                    "location_X": 0.0,
                    "location_Y": 0.0,
                    "location_Z": 0.0
                },
                "cornerPoint4": {
                    "location_X": 0.0,
                    "location_Y": 0.0,
                    "location_Z": 0.0
                },
                "timeStamp": 1673171709077
            }
        }
        time.sleep(5)
        self.start()

    def avpbutton_event_send(self):
        event = {
        "action":"event",
        "function": "UpdateNotifyAVPButtonStatusEvent",
        "args": json.dumps({"buttonSts": self.button_type})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"AVPServer:UpdateNotifyAVPButtonStatusEvent send periodic status failure with broken pipe: {str(e)}")

    def avpstatus_response(self):
        while True:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
                if req["function"] == "GetAVPButtonStatus":
                    resp = {
                        "action": "response",
                        "function": "GetAVPButtonStatus",
                        "result": json.dumps({"out": self.button_type})
                    }
                    logger.info("Send response: {}".format(json.dumps(resp)))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/avp_server.py")
                continue

    def countdown_event_send(self):
        event = {
        "action":"event",
        "function": "UpdateNotifyCountdownEvent",
        "args": json.dumps({"timerCount": self.timer_count})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"AVPServer:UpdateNotifyCountdownEvent send periodic status failure with broken pipe: {str(e)}")

    def planningpathtrack_event_send(self):
        event = {
        "action":"event",
        "function": "UpdateNotifyPlanningPathTrackEvent",
        "args": json.dumps({"pathTrack": self.path_track})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"AVPServer:NotifyPlanningPathTrack send periodic status failure with broken pipe: {str(e)}")

    def start_avpbutton_event_sending(self):
        self.avpbutton_event_sending = threading.Thread(name="avpbutton", target=self.avpbutton_event_send,)
        self.avpbutton_event_sending.start()

    def stop_avpbutton_event_sending(self):
        self.avpbutton_event_sending.join()

    def start_countdown_event_sending(self):
        self.countdown_event_sending = threading.Thread(name="countdown", target=self.countdown_event_send,)
        self.countdown_event_sending.start()

    def stop_countdown_event_sending(self):
        self.countdown_event_sending().join()

    def start_planningpathtrack_event_sending(self):
        self.planningpathtrack_event_sending = threading.Thread(name="planningpathtrack", target=self.planningpathtrack_event_send,)
        self.planningpathtrack_event_sending.start()

    def stop_planningpathtrack_event_sending(self):
        self.planningpathtrack_event_sending().join()

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        # pass
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/avp_server.py")
            logger.error(str(e))
        # self.start_avpbutton_event_sending()
        # self.start_countdown_event_sending()
        # self.start_planningpathtrack_event_sending()
        logger.info("Satrt to send response of avp service")
