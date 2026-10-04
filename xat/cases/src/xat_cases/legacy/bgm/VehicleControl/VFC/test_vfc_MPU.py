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
         
    @allure.title("云端唤醒条件不满足BGMlog_PNC23置位1分钟")
    @pytest.mark.full
    @pytest.mark.PNC23
    def test_caseid_1986435(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.tsp.rvs_log_wakeup()
        # self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.valid, 10)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, NMSts.no_valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 10, 2)
    
    @allure.title("云端唤醒BGMlog_PNC23置位5分钟")
    @pytest.mark.full
    @pytest.mark.PNC23
    def test_caseid_1986110(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.tsp.rvs_log_wakeup()
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, NMSts.no_valid)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.valid, 5.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 300.0, 2.0)

    @allure.title("云端唤醒TCAMlog_PNC23置位10分钟")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1986111(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.tsp.rvs_log_wakeup(ecus="tcam")
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, NMSts.no_valid)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.valid, 3.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 600.0, 2.0)

    @allure.title("云端唤醒TCAM BGM log_PNC23置位10分钟")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1986112(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.tsp.rvs_log_wakeup(ecus="tcam,BGM")
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, NMSts.no_valid)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.valid, 3.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 600.0, 2.0)

    @allure.title("云端唤醒TCAM CDC log_PNC23置位10分钟")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1986116(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.tsp.rvs_log_wakeup(ecus="tcam,cdc")
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.valid, 2.0)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, NMSts.valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, 60.0, 2.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 540.0, 4.0)

    @allure.title("云端唤醒TCAM ACU log_PNC23置位10分钟")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1986117(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.tsp.rvs_log_wakeup(ecus="tcam,acu")
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.valid, 2.0)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, NMSts.valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, 60.0, 2.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 540.0, 4.0)

    @allure.title("云端唤醒CDC log_PNC27置位1分钟")
    @pytest.mark.smoke
    @pytest.mark.PNC27
    def test_caseid_1986113(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.tsp.rvs_log_wakeup(ecus="cdc")
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, 60.0, 2.0)
        
    @allure.title("云端唤醒ACU log_PNC27置位1分钟")
    @pytest.mark.smoke
    @pytest.mark.PNC27
    def test_caseid_1986114(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.tsp.rvs_log_wakeup(ecus="acu")
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, 60.0, 2.0)

    @allure.title("云端唤醒CDC ACU log_PNC27置位1分钟")
    @pytest.mark.sanity
    @pytest.mark.PNC27
    def test_caseid_1986115(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.tsp.rvs_log_wakeup(ecus="cdc,acu")
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 10.0, 2.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, 50.0, 4.0)

    @allure.title("云端唤醒BGM ACU log_PNC27置位1分钟")
    @pytest.mark.sanity
    @pytest.mark.PNC27
    def test_caseid_1986118(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.tsp.rvs_log_wakeup(ecus="bgm,acu")
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.valid, 2.0)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, NMSts.valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, 60.0, 2.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 240.0, 4.0)

    @allure.title("云端唤醒BGM CDC log_PNC27置位1分钟")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1986119(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.tsp.rvs_log_wakeup(ecus="bgm,cdc")
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.valid, 2.0)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, NMSts.valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, 60.0, 2.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 240.0, 4.0)
        
    @allure.title("云端唤醒TCAM BGM CDC log_PNC27置位1分钟")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1986120(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.tsp.rvs_log_wakeup(ecus="tcam,bgm,cdc")
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.valid,2.0)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, NMSts.valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, 60.0, 2.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 540.0, 4.0)

    @allure.title("云端唤醒TCAM BGM ACU log_PNC27置位1分钟")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1986121(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.tsp.rvs_log_wakeup(ecus="tcam,bgm,acu")
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.valid, 2.0)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, NMSts.valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, 60.0, 2.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 540.0, 4.0)

    @allure.title("云端唤醒仅BGM充电情况TCAM BGM ACU log_PNC27置位1分钟")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1986121(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.tsp.rvs_log_wakeup(ecus="tcam,bgm,acu")
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.valid)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, NMSts.valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, 60.0, 2.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 540.0, 6.0)

    @allure.title("云端唤醒仅BGM未充电情况BGM log_PNC23置位5分钟")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1986124(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.Default)
        self.bus_comm.set_batterylow_mode(DCChrgnHndlSts=DCChrgnHndlSts.ConnectedWithPower,DispHvBattLvlOfChrg=20.0)
        self.tsp.rvs_log_wakeup(ecus="bgm")
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 300.0, 2.0)
    
    @allure.title("云端唤醒仅BGM未充电情况先TCAM在ACU log_PNC23置位5分钟")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1986125(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.Default)
        self.bus_comm.set_batterylow_mode(DCChrgnHndlSts=DCChrgnHndlSts.ConnectedWithPower,DispHvBattLvlOfChrg=20.0)
        self.tsp.rvs_log_wakeup(ecus="tcam")
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.valid, 2.0)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, NMSts.no_valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 60.0, 6.0)
        self.tsp.rvs_log_wakeup(ecus="acu")
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.valid)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, NMSts.valid, 2.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, 60.0, 4.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 180.0, 6.0)

    @allure.title("云端唤醒仅BGM未充电情况先TCAM在cdc log_PNC23置位5分钟")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1986126(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.Default)
        self.bus_comm.set_batterylow_mode(DCChrgnHndlSts=DCChrgnHndlSts.ConnectedWithPower,DispHvBattLvlOfChrg=20.0)
        self.tsp.rvs_log_wakeup(ecus="tcam")
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.valid, 2.0)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, NMSts.no_valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 60.0, 6.0)
        self.tsp.rvs_log_wakeup(ecus="cdc")
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.valid, 2.0)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, NMSts.valid, 2.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, 60.0, 4.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 180.0, 6.0)

    @allure.title("云端唤醒仅BGM未充电情况先TCAM在cdc log_PNC23置位5分钟")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1986126(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.Default)
        self.bus_comm.set_batterylow_mode(DCChrgnHndlSts=DCChrgnHndlSts.ConnectedWithPower,DispHvBattLvlOfChrg=20.0)
        self.tsp.rvs_log_wakeup(ecus="tcam")
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.valid, 2.0)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, NMSts.no_valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 60.0, 6.0)
        self.tsp.rvs_log_wakeup(ecus="cdc")
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.valid, 2.0)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, NMSts.valid, 2.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, 60.0, 4.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 180.0, 6.0)

    
    @allure.title("云端唤醒仅BGM未充电情况先TCAM在BGM2 log_PNC23置位10分钟")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1986127(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.Default)
        self.bus_comm.set_batterylow_mode(DCChrgnHndlSts=DCChrgnHndlSts.ConnectedWithPower,DispHvBattLvlOfChrg=20.0)
        self.tsp.rvs_log_wakeup(ecus="tcam")
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 120.0, 6.0)
        self.tsp.rvs_log_wakeup(ecus="bgm")
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 480.0, 6.0)

    @allure.title("云端唤醒仅BGM未充电情况先TCAM在BGM1 log_PNC23置位10分钟")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1986128(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.Default)
        self.bus_comm.set_batterylow_mode(DCChrgnHndlSts=DCChrgnHndlSts.ConnectedWithPower,DispHvBattLvlOfChrg=20.0)
        self.tsp.rvs_log_wakeup(ecus="tcam")
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 300.0, 6.0)
        self.tsp.rvs_log_wakeup(ecus="bgm")
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 300.0, 6.0)

    @allure.title("云端唤醒仅BGM未充电情况先TCAM在BGM log_PNC23置位12分钟")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1986129(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.Default)
        self.bus_comm.set_batterylow_mode(DCChrgnHndlSts=DCChrgnHndlSts.ConnectedWithPower,DispHvBattLvlOfChrg=20.0)
        self.tsp.rvs_log_wakeup(ecus="tcam")
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 420.0, 6.0)
        self.tsp.rvs_log_wakeup(ecus="bgm")
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 300.0, 6.0)

    @allure.title("云端唤醒仅BGM未充电情况先TCAM下发两次 log_PNC23置位12分钟")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1986130(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.Default)
        self.bus_comm.set_batterylow_mode(DCChrgnHndlSts=DCChrgnHndlSts.ConnectedWithPower,DispHvBattLvlOfChrg=20.0)
        self.tsp.rvs_log_wakeup(ecus="tcam")
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 120.0, 6.0)
        self.tsp.rvs_log_wakeup(ecus="tcam")
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 600.0, 2.0)

    @allure.title("云端唤醒仅BGM充电情况TCAM BGM CDC ACU log_PNC27置位1分钟")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1986131(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.tsp.rvs_log_wakeup(ecus="tcam,bgm,cdc,acu")
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.valid)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, NMSts.valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, 60.0, 2.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 540.0, 6.0)

    @allure.title("云端唤醒仅BGM充电情况TCAM CDC ACU log_PNC27置位1分钟")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1986132(self):
        self.mix.clear_pnc(BGMPNC.PNC23)
        self.mix.clear_pnc(BGMPNC.PNC27)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.tsp.rvs_log_wakeup(ecus="tcam,cdc,acu")
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, NMSts.valid, 2.0)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, NMSts.valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC27, 60.0, 2.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 540.0, 6.0)


