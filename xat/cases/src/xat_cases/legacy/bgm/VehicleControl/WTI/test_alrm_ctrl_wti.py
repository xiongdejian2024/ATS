#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_alrm_ctrl_abc.py
@Author      : xiangyue.li@jiduauto.com
@Time        : 2023/12/7 11:30
@Description: BGM车控车设车辆防盗
"""
import random

import allure
import pytest
import copy
from time import sleep
from random import randint
from xat_ecu.legacy.common.data_type_handing import logger
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_cases.legacy.bgm.case_helper.test_base import TestBase


@allure.feature("车控车设")
@allure.story("车辆防盗报警")
class TestAlrmCtrl(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        partner_process_check()
        self.partner = S2sBaseClass([("WTIService", "client"),
                                     ("LightService", "client"),
                                     ("WiperService", "client"),
                                     ("AutoHighBeamControlService", "server"),
                                     ("ChassisService", "client"),
                                     ("ClimateControlService", "client"),
                                     ("PedalService", "client"),
                                     ("VehicleModeService", "client")
                                     ])
        self.ipdu.start_all_time_control()
        self.busapp.start_all_cyclic_msg()
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.diagnostic_client_sim_start()
        self.sd_tester.tester_present()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        self.partner.stop_operators()
        self.sd_tester.stop_tester_present()
        self.sd_tester.diagnostic_client_sim_close()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.backbonefr_vddmbackbonefr03_gearlvrindcn_gearlvrindcn2_parkindcn()
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 0)
        sleep(1)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.partner.empty_all(0.5)
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def ck_WarningMsgList_and_GetWarningMsgList(self, hint, info, timeout=3):
        """校验指定warningMsgList事件，并请求WarningMsgList获取结果"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint, "info": str(info)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})
        
    @allure.title("触发防盗后报警动画显示")
    @pytest.mark.full
    @pytest.mark.longtime
    def test_caseid_1982533(self): 
        hint = "Anti Theft"
        self.dk.set_cenlock_sts(1)
        self.dk.send_nfc_cmd() 
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmSt',1)
        self.partner.empty_all(32)
        self.dk.set_door_sts([0, 0, 0, 1, 0])
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorOpenerRiReSts', 5)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmSt',2)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorOpenerRiReSts', 1)
        sleep(285)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmSt',1)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)
        
    # @allure.title("触发防盗后报警动画显示") 
    # @pytest.mark.full_1
    # def test_caseid_1982534(self):
    #     self.dk.set_cenlock_sts(1)
    #     sleep(1)
    #     self.partner.empty_all()
    #     sleep(0.5)
    #     self.dk.send_nfc_cmd()
    #     self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorOpenerRiReSts', 5)
    #     self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmSt',2)
    #     self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Anti Theft", "info": "1"}]})
    #     self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorOpenerRiReSts', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmSt',1)
    #     sleep(285)
    #     self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Anti Theft", "info": "0"}]})
    #     self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorOpenerRiReSts', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmSt',0)
    #     sleep(285)
    #     self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Anti Theft", "info": "0"}]})