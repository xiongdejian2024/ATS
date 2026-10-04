#!/usr/bin/python3

import threading
import time
import socket
import sys
import os
import json
import sys

from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger

DEFAULT_PORT = 16789
BUFFER_SIZE = 1024 * 1000

class GB32960Server():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        logger.info('connect_info of BgmGB32960Server: {}'.format(self.connect_info))
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.veh_status = {
            "InfoTyp": 1, # 'VEH_STATUS',
            'VehSts': 1, # 'POWER_ON'
            'ChrgnStsInfo': 1, # 'UNCHARGED'
            'PrpnMode': 1, # 'ELECTRIC'
            'VehSpeed': 23, # range(min=0, max=2200)
            'AccumMilg': 3450, # range(min=0, max=9999999)
            'HvBattSocToltalU': 480, # range(min=0, max=10000)
            'HvBattSocToltalI': 1025, # range(min=0, max=20000)
            'HvBattSocInfo': 90, # range(min=0, max=100)
            'DcDcSts': 1, # 'WORKING'
            'GearSts': 46, # 00101110
            'InsulationR': 20000, # range(min=0, max=60000)
            'AccPedlTrvlVal': 50, # range(min=0, max=100)
            'BrkPedlStsInfo': 0xFE, # range(min=0, max=101)
            }
        self.drive_motor_data = {
            'InfoTyp': 2, # 'DRIVE_MOTOR_DATA'
            'DrvMotQnty': 2, # range(min=1, max=253) default 1
            'DrvMotList': [
                        {
                            'DrvMotSeqNr': 1, # range(min=1, max=253), default 1
                            'DrvMotSts': 1, # 'POWER_CONSUMPTION'
                            'DrvMotCtrlrT': 64, # @range(min=0, max=250)
                            'DrvMotSpeed': 2333, # range(min=0, max=65531)
                            "DrvMotTorque": 2013,#range(min=0, max=65531)
                            'DrvMotT': 58, # range(min=0, max=250)
                            'MotCtrlrInpUDc': 468, # range(min=0, max=60000)
                            'MotCtrlrIDc': 39, # range(min=0, max=20000)
                        },
                        {
                            'DrvMotSeqNr': 2, # range(min=1, max=253), default 1
                            'DrvMotSts': 1, # 'POWER_CONSUMPTION'
                            'DrvMotCtrlrT': 64, # @range(min=0, max=250)
                            'DrvMotSpeed': 2333, # range(min=0, max=65531)
                            "DrvMotTorque": 2000,#range(min=0, max=65531)
                            'DrvMotT': 58, # range(min=0, max=250)
                            'MotCtrlrInpUDc': 472, # range(min=0, max=60000)
                            'MotCtrlrIDc': 41, # range(min=0, max=20000)
                        }],

        }
        self.veh_position_data = {
            'InfoTyp': 5, # 'VEH_POSITION_DATA'
            'LocationSts': 0, # 00000000, 东经, 北纬, 有效定位
            'Longitude': 39.916527,
            'Latitude': 116.397128
        }
        self.extreme_data = {
            'InfoTyp': 6, # 'EXTREME_DATA'
            'MaxHvBattUSubSysNr': 1,
            'MaxHvBattCellUCod': 39,
            'MaxHvBattCellUVal': 4.02,
            'MinHvBattUSubSysNr': 1,
            'MinHvBattCellUCod': 23,
            'MinHvBattCellUVal': 3.90,

            'MaxHvBattTSubSysNr': 1,
            'MaxHvBattCellTCod': 21, # 最高温度探针序号
            'MaxHvBattCellTVal': 80,
            'MinHvBattTSubSysNr': 1,
            'MinHvBattCellTCod': 31, # 最低温度探针序号
            'MinHvBattCellTVal': 89
        }
        self.warning_data = {
            'InfoTyp': 7,  # 'WARNING_DATA'
            'HvCellTDifFltPrm': 0, # NO_FAULT  0~3  /3
            'HvCellTOverFltPrm': 0, # NO_FAULT  0~3 /3
            'HvPackUOverFltPrm': 0, # NO_FAULT  0~3 /3
            'HvPackUUnderFltPrm': 0, # NO_FAULT 0~3 /3
            'HvSocLoFltPrm': 0, # NO_FAULT  0~3 /3
            'HvCellUOverFltPrm': 0, # NO_FAULT  0~3 /3
            'HvCellUUnderFltPrm': 0, # NO_FAULT  0~3 /3
            'HvSocHiFltPrm': 0, # NO_FAULT  0~3 /3
            'HvSocHopFltPrm': 0, # FAULT_LEVELI  0~3 /3
            'HvBattMismatchFltPrm': 0, # NO_FAULT  0~1 /2
            'HvCellUDifFltPrm': 0, # NO_FAULT  0~3 /3
            'HvlsoFltPrm': 0, # NO_FAULT  0~3 /3
            'FltTDcDcPrm': 0, # NO_FAULT  0~1 /1
            'EscWarnIndcnReqPrm': 0, # NO_FAULT 0~3 0/1
            'BrkWarnIndcnReqPrm': 1, # NO_FAULT 0~1 0/3
            'AbsWarnIndcnReqPrm': 0, # NO_FAULT 0~3 0/2
            'BrkSysWarnIndcnReqPrm': 1, # FAULT_LEVELII  0~1 0/2
            'BrkSysWarnIndcnReqSecPrm': 1, # NO_FAULT 0~1 0/2
            'BrkFldLvlPrm': 0,
            'FltElecDcDcPrm': 0, # NO_FAULT 0~1 1/2
            'IemGenericInvrtTAlrmStPrm': 0, # NO_FAULT  0~1 1/2
            'IgmGenericInvrtTAlrmStPrm': 0, # NO_FAULT  0~1 1/2
            'HvilFltPrm': 0, # NO_FAULT  usage mode=driving, HvilFlt=0x01, level 1. usage mode !=driving, HvilFlt=0x01, level 2.
            'IemGenericMotTAlrmStPrm': 0, # NO_FAULT 0~1 1/2
            'IgmGenericMotTAlrmStPrm': 0, # NO_FAULT 0~1 1/2
            'HvPackOverChrgFltPrm': 3 # FAULT_LEVELIII  0~3 /3
        }
        self.hvbattery_voltage_data = {
            'InfoTyp': 8, # 'HV_BATTERY_VOLTAGE_DATA'
            'ReChrglEgyStorgSubSysQnty': 1, # range(min=1, max=250)
            'ReChrglEgyStorgSubSysList': [{"ReChrglEgyStorgSubSysSeqNr":1, 'ReChrglEgyStorgU':220, \
                                         'ReChrglEgyStorgI':5, 'BattCellesTotNr':64, \
                                          'BgngCellSeqNrofThisFrm':1, 'TotCellNrofThisFrm':64,
                                          'CellUVal':[4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                                                      4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                                                      4000, 4000, 4000, 4000, 4000, 4000, 3900, 4000,
                                                      4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                                                      4000, 4000, 4000, 4000, 4000, 4000, 4020, 4000,
                                                      4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                                                      4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                                                      4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,]}]
        }
        self.hvbattery_temperature_data = {
            'InfoTyp': 9, # 'HV_BATTERY_TEMPERATURE_DATA'
            'ReChrglEgyStorgSubSysQnty': 1,
            'ReChrglEgyStorgSubSysList': [{"ReChrglEgyStorgSubSysSeqNr":1, 'TotTProbeNr':32, \
                                          "ProbeTVal":[85, 80, 86, 85, 81, 81, 83, 81,
                                                      81, 81, 81, 84, 84, 83, 81, 82,
                                                      85, 86, 86, 83, 89, 83, 82, 81,
                                                      80, 85, 81, 83, 85, 82, 80, 85]}]
        }
        self.gb32960_data = {
            'VehStatus': self.veh_status,
            'DriveMotorData': self.drive_motor_data,
            'VehPositionData': self.veh_position_data,
            'ExtremeData': self.extreme_data,
            'WarningData': self.warning_data,
            'HVBatteryVoltageData': self.hvbattery_voltage_data,
            'HVBatteryTemperatureData': self.hvbattery_temperature_data
        }
        self.warning_signal = [{'id': 1,'value': 0},{'id': 2,'value': 0},{'id': 3,'value': 0},
                               {'id': 4,'value': 0},{'id': 5,'value': 0},{'id': 6,'value': 0},
                               {'id': 7,'value': 0},{'id': 8,'value': 0},{'id': 9,'value': 0},
                               {'id': 10,'value': 0},{'id': 11,'value': 0},{'id': 12,'value': 0},
                               {'id': 13,'value': 0},{'id': 14,'value': 0},{'id': 15,'value': 0},
                               {'id': 16,'value': 0},{'id': 17,'value': 0},{'id': 18,'value': 0},
                               {'id': 19,'value': 0}]
        self.gb32960_stop_loop = False
        self.warning_stop_loop = False
        time.sleep(2)
        self.start()

    def notify_gb32960_data(self):
        event = {
            "action": "event",
            "function": "UpdateGB32960DataEvent",
            "args": json.dumps({"info": self.gb32960_data})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'), )
        except BrokenPipeError as e:
            logger.error(f"GBT32960 send periodic status failure with broken pipe: {str(e)}")

    def cmn_warning_info_periodic_send(self, interval=1):
        while not self.warning_stop_loop:
            event = {
                "action": "event",
                "function": "UpdateCmnWarningInfoEvent",
                "args": json.dumps(self.warning_signal)
            }
            try:
                self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
                # logger.info('Here to send Warning Data')
            except BrokenPipeError as e:
                logger.error(f"GB32960 send periodic download process failure with broken pipe: {str(e)}")
            time.sleep(interval)
            
    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))   
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/gb32960_server.py")
            logger.error(str(e))

    def start_sending_data(self):
        self.start_sending_gb32960_data()
        # time.sleep(60)
        # self.start_sending_warning_signal()

    def start_sending_gb32960_data(self):
        self.gb32960_data_sending_thread = threading.Thread(name="Gb32960DataSending", target=self.notify_gb32960_data,)
        self.gb32960_data_sending_thread.start()

    def start_sending_warning_signal(self):
        self.warning_sending_thread = threading.Thread(name="CmnWarningInfo", target=self.cmn_warning_info_periodic_send,)
        self.warning_sending_thread.start()

    def stop_sending_warning_signal(self):
        self.warning_stop_loop = True
        time.sleep(2)
        self.warning_sending_thread.join()
        logger.info('Stop sending warning signal')

    def stop_sending_gb32960_data(self):
        self.gb32960_stop_loop = True
        time.sleep(2)
        self.gb32960_data_sending_thread.join()
        logger.info("Stop sending gb32960 data")

    def stop_sending_data(self):
        self.stop_sending_gb32960_data()
        self.stop_sending_warning_signal()
        self.tcp_socket.close()
