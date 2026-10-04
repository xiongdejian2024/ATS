#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_rvs.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/12/1 11:30
@Description: BGM RVS功能测试
"""

import os
import sys
import pytest
import allure
from time import sleep
import threading

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.legacy.tsp.proto_parse import ProtoParse
from xat_ecu.api.abc_interface import *
from google.protobuf.json_format import MessageToJson
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.digital_key_s2s import DigitalKeyPartner
# from test_case.soa.case_helper.gnss_server import *
# from test_case.soa.case_helper.utils import *
# from ecu_simulator.interface.bgm.bgm_ssh import *
# from test_case.soa.case_helper.test_base import *

RKECTRL_SERVICE_SERVER = "RKECtrlService_server"
RPAAPA_SERVICE_SERVER = "RPAAPAService_server"
AVP_SERVICE_SERVER = "AVPService_server"
ACC_SERVICE_SERVER = "ACCService_server"
BACU_SERVICE_SERVER = "BACUService_server"
INTERACTIVE_SERVICE_SERVER = "InteractiveService_server"


running_flag = True

def calc_buma(num, length):
    """计算补码"""
    if num < 0:
        inverse_code = abs(int(num)) ^ ((1 << (length - 1)) - 1) + (
                1 << (length - 1)
        )
        num = inverse_code + 1  # 负数返回 补码
    return num




@allure.feature("BGM车云")
@allure.story("蓝牙数据上报")
# @pytest.mark.flaky(reruns=1, reruns_delay=1)
@pytest.mark.order_last
class TestBle(TestABCBase):
    def before_class(self, ecu):
        running_flag = True
        self.rev_msg_list = []
        self.protoparse = ProtoParse()
        # self.bus_comm.blue_data_preheat_start()
        self.bus_comm.start_dk()
        sleep(1)
        self.bus_comm.set_door_open_angle_sts(door_pos=DoorId.kDoorAll,angle=1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_4,pos_pass=WinPos.percent_4,pos_lere=WinPos.percent_4,pos_rire=WinPos.percent_4)
        self.bus_comm.set_batterylow_mode(DCChrgnHndlSts=DCChrgnHndlSts.Init,DispHvBattLvlOfChrg=0)
        self.bus_comm.set_bluetooth_key_connect_sts(key_num=1,type=BlueType.BLE_Key,con_sts=ConnSts.Connect)
        self.bus_comm.get_ble_bytes_thread_start()
        super().before_class(self, ecu)
        # self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = DigitalKeyPartner([
            RPAAPA_SERVICE_SERVER,
            AVP_SERVICE_SERVER,
            ACC_SERVICE_SERVER,
            BACU_SERVICE_SERVER,
            INTERACTIVE_SERVICE_SERVER
        ])
        self.partner.register_callback(RPAAPA_SERVICE_SERVER, self.partner.on_GetAPAStatus)
        # receiver_thread = threading.Thread(target=self.send_AvpApaMainSts,args=())
        # receiver_thread.start()
        # self.ipdu.send_pdu('chassiscan1', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        # self.ipdu.send_pdu('chassiscan2', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        sleep(3)


    def before_each_func(self, ecu):
        # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
        #                                    {'isAlive': True})
        self.flage = True
        logger.info('开始测试') 
        self.t1 = threading.Thread(target=self.event_NotifyPASetResponse,)
        self.t1.start()
        logger.info('开始测试！！') 
        pass

    def after_each_func(self, ecu):
        self.flage = False
        self.t1.join()
        self.bus_comm.clear_all_bus_buffer()
        # self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 0)
        if ecu.get("testresult") != "Pass":
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER,
                                           "NotifyPASetResponse", {"paSetResponse": 2})
            sleep(1)
        # super().after_each_func(ecu, start=False)
        sleep(1)


    def after_class(self, ecu):
        # pass
        running_flag = False
        self.bus_comm.get_ble_bytes_thread_stop()
        # self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        super().after_class(self, ecu)
        # self.bus_comm.blue_data_preheat_stop()
        
        

    def event_NotifyPASetResponse(self):
        logger.info('进来了！！')
        try:
            while self.flage:
                try:
                    self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
                                        {'isAlive': True})
                    sleep(1)
                except Exception as e:
                    logger.info(e)
                    logger.info('1 报错了！！')
        except Exception as e:
            logger.info(e)
            logger.info('2 报错了！！')
        logger.info('出去了！！')

    def get_ble_bytes(self, msg_list, blockid:BlockName):
        ble_bytes = None
        if msg_list == None:
            logger.info(f"获取的总线报文为空,没有触发响应的蓝牙数据")
            assert False
        else:
            for msg in msg_list:
                logger.info(f'msg_block_id:{self.protoparse.get_vehicle_mode(bytes(msg)).head.blockID}')
                if self.protoparse.get_vehicle_mode(bytes(msg)).head.blockID == blockid.value:
                    ble_bytes = bytes(msg)
            return ble_bytes
    
    
    
    @pytest.mark.full
    def test_parkOutFrontLeft_caseid_112059(self):
        # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
        #                                    {'isAlive': True})
        sleep(5)
        self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutFrontLeft': 2}})
        for key in range(4):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutFrontLeft': key}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.button.parkOutFrontLeft == key

    
    @pytest.mark.full
    def test_parkOutFrontRight_caseid_112058(self):
        sleep(5)
        self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutFrontRight': 2}})
        for key in range(4):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutFrontRight': key}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.button.parkOutFrontRight == key


    @pytest.mark.full
    def test_parkOutRearLeft_caseid_112057(self):
        sleep(5)
        self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutRearLeft': 2}})
        for key in range(4):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutRearLeft': key}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.button.parkOutRearLeft == key


    @pytest.mark.full
    def test_parkOutRearRight_caseid_112056(self):
        sleep(5)
        self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutRearRight': 2}})
        for key in range(4):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutRearRight': key}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.button.parkOutRearRight == key


    @pytest.mark.full
    def test_parkOutLeftFront_caseid_112055(self):
        sleep(5)
        self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutLeftFront': 2}})
        for key in range(4):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutLeftFront': key}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.button.parkOutLeftFront == key



    @pytest.mark.full
    def test_parkOutRightFront_caseid_112054(self):
        sleep(5)
        self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutRightFront': 2}})
        for key in range(4):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutRightFront': key}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.button.parkOutRightFront == key


    
    @pytest.mark.full
    def test_parkOutFront_caseid_112053(self):
        sleep(5)
        self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutFront': 2}})
        for key in range(4):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutFront': key}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.button.parkOutFront == key


    @pytest.mark.full
    def test_parkOutRear_caseid_112052(self):
        sleep(5)
        self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutRear': 2}})
        for key in range(4):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutRear': key}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.button.parkOutRear == key


    @pytest.mark.full
    def test_RPAFront_caseid_112063(self):
        sleep(5)
        self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'RPAFront': 2}})
        for key in range(4):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'RPAFront': key}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.button.RPAFront == key


    @pytest.mark.full
    def test_RPARear_caseid_112062(self):
        sleep(5)
        self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'RPARear': 2}})
        for key in range(4):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'RPARear': key}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.button.RPARear == key
    
    
    @pytest.mark.full
    def test_RPALeftTurn_caseid_112061(self):
        sleep(5)
        self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'RPALeftTurn': 2}})
        for key in range(4):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'RPALeftTurn': key}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.button.RPALeftTurn == key


    @pytest.mark.full
    def test_RPARightTurn_caseid_112060(self):
        sleep(5)
        self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'RPARightTurn': 2}})
        for key in range(4):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'RPARightTurn': key}})
            start_time = time.time()
            while time.time() - start_time < 2:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
                get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
                get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
                logger.info(f'get_data_dict: {get_data_dict}')
                if get_data.button.RPARightTurn == key:
                    assert get_data.button.RPARightTurn == key
                    break
                sleep(0.5)
            # ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            # get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            # get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            # logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.button.RPARightTurn == key


    @pytest.mark.full
    def test_button1_caseid_112051(self):
        sleep(5)
        self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'button1': 2}})
        for key in range(4):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'button1': key}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.button.button1 == key



    @pytest.mark.full
    def test_button2_caseid_112050(self):
        sleep(5)
        self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'button2': 2}})
        for key in range(4):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'button2': key}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.button.button2 == key


    @pytest.mark.full
    def test_button3_caseid_112049(self):
        sleep(5)
        self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'button3': 2}})
        for key in range(4):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'button3': key}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.button.button3 == key


    @pytest.mark.full
    def test_button4_caseid_112048(self):
        sleep(5)
        self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'button4': 2}})
        for key in range(4):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'button4': key}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.button.button4 == key

    @pytest.mark.full
    def test_timerCount_caseid_112047(self):
        sleep(5)
        self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyCountdown", {"timerCount": 0})
        for key in [180, 100, 0]:
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyCountdown", {"timerCount": key})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.timeCount == key


    @pytest.mark.full
    def test_parkLotType_caseid_112046(self):
        sleep(5)
        self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyPlanningPathTrack",
                                       {"pathTrack": {"targetLotLocation": {"parkLotForm": 1}}})
        for key in range(3):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyPlanningPathTrack",
                                       {"pathTrack": {"targetLotLocation": {"parkLotForm": key}}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.parkLotType == key
    


    @pytest.mark.smoke
    def test_PAStatus_caseid_112045(self):
        # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
        #                                    {'isAlive': True})
        sleep(5)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 3}})
        for key in range(0,15):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": key}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.paRemoteStatus.paStatus == key


    @pytest.mark.sanity
    def test_lastHandleType_caseid_112044(self):
        sleep(5)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, 'NotifyPARemoteStatus',
                                           {"paRemoteStatus": {'lastHandleType': 3}})
        for key in range(5):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, 'NotifyPARemoteStatus',
                                           {"paRemoteStatus": {'lastHandleType': key}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.paRemoteStatus.lastHandleType == key

    
    @allure.title("增加枚举值255")
    @pytest.mark.full
    @pytest.mark.v210
    def test_lastHandleType_caseid_1993529(self):
        sleep(5)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, 'NotifyPARemoteStatus',
                                           {"paRemoteStatus": {'lastHandleType': 3}})
        for key in [0,255]:
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, 'NotifyPARemoteStatus',
                                           {"paRemoteStatus": {'lastHandleType': key}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.paRemoteStatus.lastHandleType == key

    
    @pytest.mark.sanity
    def test_lastHandleUid_caseid_112043(self):
        sleep(5)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPARemoteStatus",
                                {"paRemoteStatus": {'lastHandleUid': 0}})
        sleep(0.5)
        self.bus_comm.clear_block_bytes()
        # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
        #                                    {'isAlive': True})
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPARemoteStatus",
                                {"paRemoteStatus": {'lastHandleUid': 0x0102030405060708}})
        ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
        get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
        get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
        logger.info(f'get_data_dict: {get_data_dict}')
        assert get_data.paRemoteStatus.lastHandleUid == 72623859790382856


    @pytest.mark.sanity
    def test_source_caseid_112042(self):
        sleep(5)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                           {"reminder": {"lastHandleType": 2}})
        for last_handle_type in range(5):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                           {"reminder": {"lastHandleType": last_handle_type}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.APARemoteReminder.source == last_handle_type


    @pytest.mark.sanity
    def test_type_caseid_112041(self):     
        sleep(5)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                           {"reminder": {"type": 1, "lastHandleType": 2}})
        sleep(1)
        for key in range(55):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                           {"reminder": {"type": key, "lastHandleType": 2}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.APARemoteReminder.type == key


    @pytest.mark.sanity
    def test_Direction_caseid_112040(self):
        sleep(5)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyParkingLotDirection", {"derection": 2})
        sleep(1)
        for key in range(3):
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyParkingLotDirection", {"derection": key})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.direction == key


    @pytest.mark.full
    def test_RemoteInfo_caseid_112039(self):
        sleep(5)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteInfo", {"apaRemoteInfo":{"remoteInfo": 1,"lastHandleUid":0x0102030405060708}})
        for key in [0, 100, 255]:
            self.bus_comm.clear_block_bytes()
            # self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
            #                                {'isAlive': True})
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteInfo", {"apaRemoteInfo":{"remoteInfo": key,"lastHandleUid":0x0102030405060708}})
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
            get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            assert get_data.remoteInfo == key


    @pytest.mark.full
    def test_APAOutReminder_caseid_112038(self):
        '''赛博坦查看WTI提示 '''
        sleep(5)
        self.partner.send_event_notify(BACU_SERVICE_SERVER, "NotifyBACUWTI", {"reminder":{"APAReminder":0}})
        sleep(1)
        self.partner.send_event_notify(BACU_SERVICE_SERVER, "NotifyBACUWTI", {"reminder":{"APAReminder":1}})
        sleep(1)
        self.partner.send_event_notify(BACU_SERVICE_SERVER, "NotifyBACUWTI", {"reminder":{"APAReminder":0}})
        # for key in range(3):
        #     self.bus_comm.clear_block_bytes()
        #     self.partner.send_event_notify(AVP_SERVICE_SERVER, 'AvpApaMainSts',
        #                                    {'isAlive': True})
        #     self.partner.send_event_notify(BACU_SERVICE_SERVER, "NotifyBACUWTI", {"reminder":{"APAReminder":key}})
        #     ble_bytes = self.bus_comm.get_block_bytes(BlockName.APA)
        #     get_data = self.protoparse.get_vehicle_messages("19001",bytes(ble_bytes))
        #     get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
        #     logger.info(f'get_data_dict: {get_data_dict}')
        #     assert get_data.BACUAPAOutReminder == key
