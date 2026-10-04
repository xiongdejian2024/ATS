#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_charge_pile_open_charge_lid.py
@Time         :2023/1/31 17:54:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import os
import sys
import hashlib
from queue import Queue

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ""))
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
PRECHECKTI = 1

from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass_abc import *
from xat_ecu.api.abc_interface import *

pdu_1 = [0x01,0x00,0x01,0x00,0x00,0x00,0x9E,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]

pdu_2 = [0x02,0x0B,0x9E,0x48,0x50,0xCC,0xA4,0xE7,0x4A,0x6C,0xD1,0x22,0x7A,0x96,0x9C,0x56,
            0x3F,0x6B,0x10,0xDE,0x95,0x19,0x4B,0x1C,0xD6,0x9A,0xB6,0x2C,0xAB,0x39,0xAD,0xE9,
            0x6F,0x88,0x01,0x20,0x74,0x9E,0x94,0x65,0xBB,0x90,0x1A,0x74,0x32,0x67,0x9B,0xA8,
            0xD9,0x8F,0xDF,0xA5,0xD7,0xE6,0xAA,0x7B,0xEA,0x08,0x89,0x7C,0x66,0xCD,0x0F,0x00]

pdu_3 = [0x03,0x0A,0xAF,0x4C,0xE4,0x53,0xFE,0x31,0xC6,0x3E,0x9B,0xEE,0x7B,0xFE,0xAB,0xF8,
            0x58,0xE2,0x4B,0xDD,0x27,0xFB,0xE6,0xA6,0xAE,0xA4,0xF9,0x85,0x89,0xE4,0xB2,0x14,
            0xD5,0x13,0x2F,0x70,0xF5,0xD4,0x5F,0xD5,0x1E,0x5F,0xFB,0x6B,0x38,0xCB,0x73,0xAA,
            0xD3,0xB1,0xCD,0x8C,0xB8,0xAE,0xA5,0x9F,0xDB,0x77,0xA4,0x2A,0xDE,0x21,0x92,0x00]

pdu_4 = [0x04,0x9A,0x5F,0x63,0x77,0x0A,0x58,0x24,0x28,0xAB,0x0A,0x6C,0x2E,0x61,0x99,0xE0,
            0x3F,0x77,0x68,0xAE,0x3B,0x05,0x45,0x01,0xBA,0x7C,0x3E,0x74,0x6E,0xA4,0xC2,0xFD,
            0x23,0xFA,0x11,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]

@allure.feature("互联服务")
@allure.story("数字钥匙通信")
class TestDigitalKeyComm(TestDigitalKeyBase):

    def before_class(self,ecu):
        super().before_class(self, ecu)
        self.bus_comm.ipdu.recv_pdu_thread_all_stop()
       

    def after_class(self, ecu):
        # self.bus_comm.start_dk()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        sleep(2)
        while not self.bus_comm.dk.dk_raw_data.empty():
            self.bus_comm.dk.dk_raw_data.get_nowait()
        sleep(1)
    
    def after_each_func(self, ecu):
        self.bus_comm.ipdu.recv_pdu_thread_all_stop()
        sleep(1)
        
    def check_bgm_error_feedback(self,error_type:DkAlertType,timeout = 3):
        run_time = 0
        while run_time < timeout:
            try:
                data = self.bus_comm.dk.dk_raw_data.get(timeout=0.02)
                msg_data = data[3]
                header = msg_data[0]
                logger.info(f"接收到BGM反馈的数据帧类,Header为{header}")
                if header == 0xFF: 
                    logger.info(f"接收到BGM反馈的错误帧,接收的错误类型为{msg_data[62]},期望的错误类型为{error_type.value}")
                    if int(error_type.value) == int(msg_data[62]):
                        assert True
                        return
                    else:
                        assert False
                elif header == 0x00:
                    continue
            except Exception as e:
                run_time += 0.1
                sleep(0.1)
                continue
        logger.info(f"{timeout}内没有接收到BGM反馈的错误帧")
        assert False
    
    def check_bgm_normal_msg(self,check_id = 0xFF,timeout = 3):
        run_time = 0
        pdu_error = [0xff,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x02,0x00]
        self.bus_comm.dk.connectivity_send_pdu(0x166, pdu_1)
        sleep(0.05)
        self.bus_comm.dk.connectivity_send_pdu(0x166, pdu_2)
        sleep(0.05)
        self.bus_comm.dk.connectivity_send_pdu(0x166, pdu_error)
        while run_time < timeout:
            try:
                data = self.bus_comm.dk.dk_raw_data.get(timeout=0.02)
                msg_data = data[3]
                header = msg_data[0]
                logger.info(int(msg_data[-1]))
                if int(header) == 0 and int(msg_data[-1]) == 255: 
                    assert True
                    return
            except Exception as e:
                run_time += 0.1
                sleep(0.1)
                continue
        logger.info(f"{timeout}内没有接收到BGM发送的报文")
        assert False


    
    def check_bgm_req(self,rev_data):
        msg_id = rev_data[0]
        msg_data = rev_data[3]
        header = msg_data[0]
        if header != 0xFF: 
            logger.info(f"接收到BGM反馈的数据帧类,Header为{header}")
            

    @allure.title("验证BGM收到告警帧之后会回复ACK")
    @pytest.mark.full
    def test_caseid_1987510(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.ipdu.recv_pdu_thread_start('connectivitycanfd', 'VgmConnFr16', self.bus_comm.dk.wait_for_bgm_dk_data)
        sleep(3)
        #self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.check_bgm_normal_msg()
        sleep(3)
        
    @allure.title("验证BGM能正确发出Out of order告警帧")
    @pytest.mark.full
    def test_caseid_1987516(self):
        self.bus_comm.ipdu.recv_pdu_thread_start('connectivitycanfd', 'VgmConnFr16', self.bus_comm.dk.wait_for_bgm_dk_data)
        sleep(1)
        self.bus_comm.dk.connectivity_send_pdu(0x166, pdu_1)
        sleep(0.03)
        self.bus_comm.dk.connectivity_send_pdu(0x166, pdu_3)
        self.check_bgm_error_feedback(error_type=DkAlertType.OutOrder)


    @allure.title("验证BGM能正确发出Packet timeout告警帧")
    @pytest.mark.full
    def test_caseid_1987515(self):
        self.bus_comm.ipdu.recv_pdu_thread_start('connectivitycanfd', 'VgmConnFr16', self.bus_comm.dk.wait_for_bgm_dk_data)
        sleep(1)
        self.bus_comm.dk.connectivity_send_pdu(0x166, pdu_1)
        sleep(0.03)
        self.bus_comm.dk.connectivity_send_pdu(0x166, pdu_2)
        sleep(1)
        self.check_bgm_error_feedback(error_type=DkAlertType.PacketTimeout)



    @allure.title("验证BGM能正确发出Overflow告警帧")
    @pytest.mark.full
    def test_caseid_1987517(self):
        pdu_1_1 = [0x01,0x00,0x01,0x00,0x00,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        
        self.bus_comm.ipdu.recv_pdu_thread_start('connectivitycanfd', 'VgmConnFr16', self.bus_comm.dk.wait_for_bgm_dk_data)
        sleep(1)
        self.bus_comm.dk.connectivity_send_pdu(0x166, pdu_1_1)
        self.check_bgm_error_feedback(error_type=DkAlertType.OverFlow)
    
    @allure.title("验证BGM能正确发出EncrptErr告警帧")
    @pytest.mark.full
    def test_caseid_1987513(self):
        pdu_4_1 = [0x04,0x9A,0x5F,0x63,0x77,0x0A,0x58,0x24,0x28,0xAB,0x0A,0x6C,0x2E,0x61,0x99,0xE0,
            0x3F,0x77,0x68,0xAE,0x3B,0x05,0x45,0x01,0xBA,0x7C,0x3E,0x74,0x6E,0x00,0x00,0x00,
            0x00,0xFA,0x11,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        
        self.bus_comm.ipdu.recv_pdu_thread_start('connectivitycanfd', 'VgmConnFr16', self.bus_comm.dk.wait_for_bgm_dk_data)
        sleep(1)
        self.bus_comm.dk.connectivity_send_pdu(0x166, pdu_1)
        sleep(0.03)
        self.bus_comm.dk.connectivity_send_pdu(0x166, pdu_2)
        sleep(0.03)
        self.bus_comm.dk.connectivity_send_pdu(0x166, pdu_3)
        sleep(0.03)
        self.bus_comm.dk.connectivity_send_pdu(0x166, pdu_4_1)
        sleep(0.1)
        self.check_bgm_error_feedback(error_type=DkAlertType.EncrptErr)


    
    @allure.title("验证BGM能正确发出InputError告警帧")
    @pytest.mark.full
    def test_caseid_1987512(self):
        self.bus_comm.ipdu.recv_pdu_thread_start('connectivitycanfd', 'VgmConnFr16', self.bus_comm.dk.wait_for_bgm_dk_data)
        sleep(1)
        self.bus_comm.dk.connectivity_send_pdu(0x166, pdu_1)
        sleep(0.03)
        self.bus_comm.dk.connectivity_send_pdu(0x166, pdu_2)
        sleep(1)
        self.check_bgm_error_feedback(error_type=DkAlertType.PacketTimeout)

    @allure.title("BGM正确解析BNCM数据")
    @pytest.mark.smoke
    def test_caseid_1988826(self):
        self.bus_comm.ipdu.recv_pdu_thread_start('connectivitycanfd', 'VgmConnFr16', self.bus_comm.dk.wait_for_bgm_dk_data)
        sleep(1)
        self.bus_comm.dk.connectivity_send_pdu(0x166, pdu_1)
        sleep(0.03)
        self.bus_comm.dk.connectivity_send_pdu(0x166, pdu_2)
        sleep(0.03)
        self.bus_comm.dk.connectivity_send_pdu(0x166, pdu_3)
        sleep(0.03)
        self.bus_comm.dk.connectivity_send_pdu(0x166, pdu_4)
        
    