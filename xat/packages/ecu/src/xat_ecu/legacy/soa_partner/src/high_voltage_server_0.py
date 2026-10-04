#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
import time

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class HighVoltageServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hvsoc_info = {
            'realSoc': 90.5,
            'displaySoc': 90,
            "calculateDTESOC": 90.2
             }
        self.charging_msg = {
            'chargingState': 1, # CHARGING
            'chargingSpeed': 10,
            'remainChargingTime': 30,
            "isConnect": False,
            "isTempHigh": False,
            "bookChargeResp": 1,
            "bookStateFeedBack": 1,
            "chargeTargetSoc": 95.0,
            'pluggerStatus': 1,
            "chargePower": 1200,
            "totalChargeEnergy": 31526200,
            "chargeEnergyThisTime": 13500,
            "chargeSpeedCalculate": 1300,
            "recentChargeStartTime": int(time.time()) - 1200,
            "recentChargeEndTime": int(time.time()),
            "chargingCompleteStatus": True,
            "bookChargests": 2,
            "isChargingPreparing": False
        }
        self.battery_temperature_info = {
            "maxTemperature": -17.5,
            "minTemperature": -31.5,
            "averageTemperature": -18.0
        }
        self.equipment_info = {
            "maxCurrent": 35.0,
            "actualCurrent": 16.9,
            "equipmentTypes": [1]
        }
        self.battery_heating_info = {
            "currentState": 2,
            "reqState": 1,
            "estimateTime": 35
        }
        self.start()
        self.send_response(timeout=100.0)

    def send_response(self, timeout=5.0):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/high_voltage_server_0.py")
                continue

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/high_voltage_server_0.py")
            logger.error(str(e))