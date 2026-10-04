#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_climate_ctrl_abc.py
@Author      : xiangyue.li@jiduauto.com
@Time        : 2023/12/7 11:30
@Description: BGM车控车设空调
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
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_cases.legacy.bgm.case_helper.test_base import TestBase


@allure.feature("车控车设")
@allure.story("空调报警")
class TestClimateCtrl(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        partner_process_check()
        self.partner = S2sBaseClass([("WTIService", "client"),("ClimateControlService", "client"),])
        self.ipdu.start_all_time_control()
        self.busapp.start_all_cyclic_msg()
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.diagnostic_client_sim_start()
        self.sd_tester.tester_present()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
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

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    @allure.title("空调系统故障_CmprFbCmprSts2") 
    @pytest.mark.full
    def test_caseid_1982587(self):
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr07, 'CmprFbCmprSts2', 2)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr07, 'CmprFbCmprSts2', 1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Climate System Error", "info": "0"}]})

    @allure.title("空调系统故障_HvCooltHeatrWarnSigFltInCom") 
    @pytest.mark.full
    def test_caseid_1982585(self):
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'HvCooltHeatrWarnSigFltInCom', 0)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'HvCooltHeatrWarnSigFltInCom', 1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Climate System Error", "info": "0"}]})
        
    @allure.title("空调系统故障_HvCooltHeatrWarnSigFltPrsnt") 
    @pytest.mark.full
    def test_caseid_1982586(self):
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'HvCooltHeatrWarnSigFltPrsnt', 0)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'HvCooltHeatrWarnSigFltPrsnt', 1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Climate System Error", "info": "0"}]})
        
    @allure.title("前排出风口调节故障_VentnActr0XElecErr") 
    @pytest.mark.full
    def test_caseid_1982566(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr62, 'VentnActr01ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr62, 'VentnActr02ElecErr',0)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Front Vent Adjustment Error", "info": "0"}]})
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr62, 'VentnActr01ElecErr',1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr62, 'VentnActr02ElecErr',1)
        sleep(60)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Front Vent Adjustment Error", "info": "1"}]})
