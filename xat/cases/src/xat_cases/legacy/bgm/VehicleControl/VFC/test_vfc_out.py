#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_npc_vfc.py
@Author      : shulin.zheng@jiduauto.com
@Time        : 2023/11/9 11:30
@Description : BGM车控车设VFC
"""

import os
import sys
import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.common.data_handle import *


@allure.feature("车控车设")
@allure.story("VFC")
class TestHVAlarmCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["HighVoltageService_client","CentralLockService_client","SteerWheelService_client",
                         "LightService_client",'ClimateControlService_client',"VehicleModeService_client",
                         "WiperService_client","ChargeLidService_client","TailWingService_client",
                         "KeyService_client","WindowAppService_client","GloveBoxService_client",
                         "OuterRearViewService_client","DoorService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
    
    @allure.title("车控车设_VFCPNC25_CnvnAllwd触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC25
    def test_vfc_caseid_109644(self):
        self.mix.clear_pnc(BGMPNC.PNC25)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.mix.set_low_volt_servse_mode(low_volt=True)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC25, 3.0)
        self.mix.set_low_volt_servse_mode(low_volt=False)

    @allure.title("车控车设_VFCPNC25_CnvnAllwd触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC25
    def test_vfc_caseid_1984820(self):
        self.mix.clear_pnc(BGMPNC.PNC25)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC25, 3.0)
    
    @allure.title("方向盘加热_PNC26置位1")
    @pytest.mark.full
    @pytest.mark.PNC26
    def test_caseid_1986102(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL,ccp={186: 0x02, 13: 0x4})
        self.mix.clear_pnc(BGMPNC.PNC26)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_steer_wheel_heat_level(HeatLevel.High,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC26, 10.0, 3.0)
        self.soa.hmi_set_steer_wheel_heat_level(HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC26, NMSts.no_valid)

    @allure.title("车控车设_VFCPNC26_BrkPedlPsdBrkPedlPsd触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC26
    def test_vfc_caseid_1993245(self):
        self.mix.clear_pnc(BGMPNC.PNC26)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","BrkPedlPsdQf", 3)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","BrkPedlPsdBrkPedlPsd", 1)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC26, NMSts.valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC26, 10.0, 3.0)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","BrkPedlPsdBrkPedlPsd", 0)

    @allure.title("车控车设_VFCPNC26_BrkPedlrRat触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC26
    def test_vfc_caseid_1985711(self):
        self.mix.clear_pnc(BGMPNC.PNC26)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr08","BrkPedlrRatPerc", 12800)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC26, NMSts.valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC26, 10.0, 3.0)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr08","BrkPedlrRatPerc", 0)

    @allure.title("车控车设_VFCPNC26_VehSpdLgt大于1.3m/s触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC26
    def test_vfc_caseid_1985729(self):
        self.mix.clear_pnc(BGMPNC.PNC26)
        self.bus_comm.set_vehspd(10.0)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC26, NMSts.valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC26, 10.0, 3.0)
        self.bus_comm.set_vehspd(0.0)

    @allure.title("车控车设_VFCPNC33_BrkPedlSnsrSt触发120")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC33
    def test_vfc_caseid_1985395(self):
        self.mix.clear_pnc(BGMPNC.PNC33)
        self.io.brake_light_close()
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC33, NMSts.valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC33, 120.0, 5.0)
        self.io.brake_light_open()
        
    @allure.title("车控车设_VFCPNC33_BrkPedlSnsrSt触发60")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC33
    def test_vfc_caseid_1985396(self):
        self.mix.clear_pnc(BGMPNC.PNC33)
        self.io.brake_light_close()
        self.io.brake_light_open()
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC33, NMSts.valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC33, 55.0, 5.0)
    