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

    @allure.title("467259_PNC20_Visibility VisyDefrstCtrlMgr_除霜ElecDefrstReqMirrDefrstReq")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.test1120
    @pytest.mark.PNC20
    def test_vfc_caseid_1985702(self):
        self.mix.clear_pnc(BGMPNC.PNC20)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_ElecDefrstReq_sts(MirrDefrstReq=0,WinDefrstReReq=0,WinDefrstFrntReq=0)
        sleep(1)
        self.bus_comm.set_ElecDefrstReq_sts(MirrDefrstReq=1,WinDefrstReReq=0,WinDefrstFrntReq=0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, 3.0, 2.0)
        self.bus_comm.set_ElecDefrstReq_sts(MirrDefrstReq=0,WinDefrstReReq=0,WinDefrstFrntReq=0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, 3.0, 2.0)

    @allure.title("车控车设_VFCPNC20_WinDefrstFrnt_激活后除霜")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC20
    def test_vfc_caseid_1985704(self):
        self.mix.clear_pnc(BGMPNC.PNC20)
        self.mix.set_rear_defrost_sts(sts=True)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, 3.0, 1.5)
        self.mix.set_rear_defrost_sts(sts=False)

    @allure.title("467259_PNC20_Visibility VisyDefrstCtrlMgr_除霜ElecDefrstReqWinDefrstReReq")
    @pytest.mark.smoke
    @pytest.mark.test1120
    @pytest.mark.PNC20
    def test_vfc_caseid_1985703(self):
        self.mix.clear_pnc(BGMPNC.PNC20)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_ElecDefrstReq_sts(MirrDefrstReq=0,WinDefrstReReq=0,WinDefrstFrntReq=0)
        sleep(1)
        self.bus_comm.set_ElecDefrstReq_sts(MirrDefrstReq=0,WinDefrstReReq=1,WinDefrstFrntReq=0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, 3.0, 2.0)
        self.bus_comm.set_ElecDefrstReq_sts(MirrDefrstReq=0,WinDefrstReReq=0,WinDefrstFrntReq=0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, 3.0, 2.0)

    @allure.title("车控车设_VFCPNC20_HmiDefrstElecReq_后视镜加热")
    @pytest.mark.smoke
    @pytest.mark.PNC20
    def test_vfc_caseid_1985705(self):
        self.mix.clear_pnc(BGMPNC.PNC20)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3,ccp={182: 5, 13: 4})
        self.soa.hmi_set_outview_heat_mode(sts=True)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, 3.0, 1.5)
        self.soa.hmi_set_outview_heat_mode(sts=False)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, 3.0, 1.5)

    

    @allure.title("车控车设_VFCPNC20_HmiDefrstrElecStsMirrr_后挡风加热开启")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC20
    def test_vfc_caseid_1985706(self):
        self.mix.clear_pnc(BGMPNC.PNC20)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3,ccp={182: 5, 13: 4})
        self.soa.hmi_set_outview_heat_mode(sts=True)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, NMSts.valid)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, NMSts.no_valid,timeout=3)
        self.soa.hmi_set_outview_heat_mode(sts=False)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, NMSts.no_valid)

    @allure.title("467259_PNC20_Visibility VisyDefrstCtrlMgr_除霜ElecDefrstReqWinDefrstFrntReq")
    @pytest.mark.smoke
    @pytest.mark.test1120
    @pytest.mark.PNC20
    def test_vfc_caseid_1999040(self):
        self.mix.clear_pnc(BGMPNC.PNC20)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_ElecDefrstReq_sts(MirrDefrstReq=0,WinDefrstReReq=0,WinDefrstFrntReq=0)
        sleep(1)
        self.bus_comm.set_ElecDefrstReq_sts(MirrDefrstReq=0,WinDefrstReReq=0,WinDefrstFrntReq=1)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, 3.0, 2.0)
        self.bus_comm.set_ElecDefrstReq_sts(MirrDefrstReq=0,WinDefrstReReq=0,WinDefrstFrntReq=0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, 3.0, 2.0)