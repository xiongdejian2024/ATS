#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_service_usagemode_abc.py
@Author      : heng.wang@jiduauto.com
@Time        : 2024/1/9 13:20
@Description: BGMusagmode服务相关抽象接口用例
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
from framework.automotive.utils.data_type import EcuInfo
from xat_ecu.api.abc_interface import *
from xat_ecu.api.constants.common import *


@allure.feature("车控车设")
@allure.story("整车模式/使用模式")
class TestUsageMode(TestABCBase):
    @staticmethod
    def change_bench_config(ecu:EcuInfo) -> EcuInfo:
        ecu.domain.single_bgm = True
        ecu.domain.two_domain = False
        ecu.tc_config["dut_ecu"] = ["BGM"]
        return ecu
    def before_class(self, ecu):
        self.soa.update(["VehicleModeService_client", "TailGateService_client", "VehicleSetStatusService_client", "LightService_client"])
        self.io.tcam_power_off()
        time.sleep(5)

    def before_each_func(self, ecu):
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        time.sleep(1)
        self.bus_comm.set_dtc_pre()
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        pass

    def after_each_func(self, ecu):
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.driver_seat_notpresent()
        self.bus_comm.set_secle_seat_notpresent()
        self.bus_comm.set_pass_seat_notpresent()
        self.io.hazard_light_close()
        self.io.bgm_diag_line_up()
        self.mix.set_precon_to_abandon()
        pass

    def after_class(self, ecu):
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        self.io.tcam_power_on()
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)


    # ---------------------------->abandon<---------------------------------------------
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_1984566(self):
        "SetConvenienceForAppAction_非inactive功能无效_abandon"
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        time.sleep(1)
        self.mix.SetConvenienceForAppAction_and_check_usagemode(time1=1, usagemode=UsageMode.ABANDONED)
        self.mix.wait_time_in_usagemde(num=1, usagemode=UsageMode.ABANDONED)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_1978204(self):
        '''abandon_to_inactive ClimaOvrHeatPrtSts'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.bus_comm.set_singal("bodycan", "CcmBodyFr34", "ClimaOvrHeatPrtSts", 1)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.sanity
    @pytest.mark.abandon
    def test_usage_mode_caseid_1912999(self):
        '''abandon_to_inactive 主驾门打开'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.io.set_door(Drvr=Door.open, Pass=Door.close, RiRe=Door.close, LeRe=Door.close, Trunk=Door.close)
        time.sleep(.3)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.sanity
    @pytest.mark.abandon
    def test_usage_mode_caseid_1912998(self):
        '''abandon_to_inactive 收到制动踏板开关请求'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.sanity
    @pytest.mark.abandon
    def test_usage_mode_caseid_1912997(self):
        '''主驾内门开按钮请求,内门间隔时间要短'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.bus_comm.set_singal("bodycan", "DdmBodyFr04", "DoorDrvrOpenReqInsdSwt1", 1)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrOpenReqInsdSwt2", 1)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.sanity
    @pytest.mark.abandon
    def test_usage_mode_caseid_1912996(self):
        '''abandon_to_inactive 主驾外门按钮打开'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.io.trigger_door_outswitch_sts(Drvr=OutSwitchPressSts.NoPress)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrOpenReqOutdSwt2", 2)
        self.io.trigger_door_outswitch_sts(Drvr=OutSwitchPressSts.Press)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrOpenReqOutdSwt2", 1)
        time.sleep(.3)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrOpenReqOutdSwt2", 2)
        self.io.trigger_door_outswitch_sts(Drvr=OutSwitchPressSts.NoPress)
    
    @pytest.mark.sanity
    @pytest.mark.abandon
    def test_usage_mode_caseid_1912995(self):
        '''用户携带钥匙接近'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr17", "UsgModChgReqFromBLE", 1)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        
    @pytest.mark.sanity
    @pytest.mark.abandon
    def test_usage_mode_caseid_1912994(self):
        '''触发补电'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.bus_comm.set_low_volt_power_supply()
        time.sleep(3)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_110157(self):
        '''从Abandoned进入Inactive,HvEgyLoadFctReq高压请求'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr09", "HvEgyLoadFctReq", 1)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_110136(self):
        '''从Abandoned进入Inactive,通过[IF: HvOnMaiReq]判断动力系统有高压请求'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr28", "HvOnMaiReq", 1)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_110073(self):
        '''从Abandoned进入Inactive,通过[IF: SwtLiHzrdWarn] 收到危险警告灯操作请求'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.io.hazard_light_open()
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.single_bgm
    @pytest.mark.abandon
    def test_usage_mode_caseid_110062(self):
        '''从Abandoned进入Inactive,通过[IF: TelmFctReq] 判断车辆有远程工作需求'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.bus_comm.set_singal("connectivitycanfd", "TcamConnectivityFr35", "TelmFctReq", 1)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_110059(self):
        '''abandon_to_inactive 左后门被打开'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.io.set_door(Drvr=Door.close, Pass=Door.close, RiRe=Door.close, LeRe=Door.open, Trunk=Door.close)
        time.sleep(.3)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)

    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_110046(self):
        '''从Abandoned进入Inactive,通过[IF: AlrmSts] 收到车辆解防或者设防状态'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_110045(self):
        '''abandon_to_inactive 通过[IF: DoorLeReOpenReqOutdLogic]判断左后外门开按钮请求'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.io.trigger_door_outswitch_sts(LeRe=OutSwitchPressSts.NoPress)
        self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DoorLeReOpenReqOutdSwt2", 2)
        self.io.trigger_door_outswitch_sts(LeRe=OutSwitchPressSts.Press)
        self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DoorLeReOpenReqOutdSwt2", 1)
        time.sleep(.3)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_110043(self):
        '''从Abandoned进入Inactive,通过[IF: EpbLampReqSec] 收到EPB备份开关操作请求'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.bus_comm.set_singal("backbonefr", "BbmBackBoneFr04", "EpbLampReqSecEpbLampReq", 1)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_110032(self):
        '''从Abandoned进入Inactive,通过[IF: DoorRiReOpenReqInsdLogic]判断右后内门开按钮请求'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.bus_comm.set_singal("bodycan", "RrdmBodyFr01", "DoorRiReOpenReqInsdSwt1", 1)
        self.bus_comm.set_singal("bodycan", "RpodBodyFr01", "DoorRiReOpenReqInsdSwt2", 1)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_110024(self):
        '''从Abandoned进入Inactive,通过[IF: EpbLampReq] 收到EPB开关操作请求'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr39", "EpbLampReqEpbLampReq", 1)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.sanity
    @pytest.mark.abandon
    @pytest.mark.nvm
    def test_usage_mode_caseid_110016(self):
        '''abandon存储恢复'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        time.sleep(1)
        self.io.bgm_power_off()
        time.sleep(5)
        self.io.bgm_power_on()
        time.sleep(20)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ABANDONED)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_110015(self):
        '''从Abandoned进入Inactive,通过[IF: MmedHdPwrMod] 判断娱乐系统有工作需求'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.bus_comm.set_singal("infocanfd", "CdcInfoCanFdFr03", "MmedHdPwrMod", 5)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_109998(self):
        '''abandon_to_inactive 通过[IF: TrSts]判断尾门被打开'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.io.set_door(Drvr=Door.close, Pass=Door.close, RiRe=Door.close, LeRe=Door.close, Trunk=Door.open)
        time.sleep(.3)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_109991(self):
        '''abandon_to_inactive 通过[IF: DoorPassSts]判断副驾门被打开'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.io.set_door(Drvr=Door.close, Pass=Door.open, RiRe=Door.close, LeRe=Door.close, Trunk=Door.close)
        time.sleep(.3)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_109986(self):
        '''从Abandoned进入Inactive,通过[IF: DoorLeReOpenReqInsdLogic]判断左后内门开按钮请求'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.bus_comm.set_singal("bodycan", "RldmBodyFr01", "DoorLeReOpenReqInsdSwt1", 1)
        self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DoorLeReOpenReqInsdSwt2", 1)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)

    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_109977(self):
        '''abandon_to_inactive 通过[IF: IndcrSts] 收到危险警告灯开关状态（处于打开状态）'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.io.hazard_light_open()
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_109976(self):
        '''abandon_to_inactive 通过[IF: PtCoolgPostRunActv] 判断车辆有动力系统热管理工作需求'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr00", "PtCoolgPostRunActv", 1)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_109952(self):
        '''abandon_to_inactive 通过[IF: RemHvStrtActvReq]判断互联子系统有高压请求'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.bus_comm.set_singal("connectivitycanfd", "TcamConnectivityFr12", "RemHvStrtActvReq", 1)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_109936(self):
        '''abandon_to_inactive 通过[IF: DrvrGearShiftParkReq]判断P挡按钮被按下'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.bus_comm.set_singal("propulsioncan", "EgsmPropFr01", "DrvrGearShiftParkReq1", 1)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_109929(self):
        '''abandon_to_inactive 通过[IF: DoorRiReSts]判断右后门被打开'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.io.set_door(Drvr=Door.close, Pass=Door.close, RiRe=Door.open, LeRe=Door.close, Trunk=Door.close)
        time.sleep(.3)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_109911(self):
        '''abandon_to_inactive 通过[IF: TrOpenerReq] 收到车辆尾门操作请求'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.soa.send_method_request( 'TailGateService_client','Close',{})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_109909(self):
        '''abandon_to_inactive 通过[IF: DoorPassOpenReqOutdLogic]判断副驾外门开按钮请求'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.io.trigger_door_outswitch_sts(Pass=OutSwitchPressSts.NoPress)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DoorPassOpenReqOutdSwt2", 2)
        self.io.trigger_door_outswitch_sts(Pass=OutSwitchPressSts.Press)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DoorPassOpenReqOutdSwt2", 1)
        time.sleep(.3)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_109905(self):
        '''abandon_to_inactive 通过[IF: AlrmSts] 判断车辆防盗报警触发'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.io.set_door(Drvr=Door.open, Pass=Door.close, RiRe=Door.close, LeRe=Door.close, Trunk=Door.close)
        time.sleep(.3)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_109903(self):
        '''从Abandoned进入Inactive,通过[IF: DoorPassOpenReqInsdLogic]判断副驾内门开按钮请求'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.bus_comm.set_singal("bodycan", "PdmBodyFr01", "DoorPassOpenReqInsdSwt1", 1)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DoorPassOpenReqInsdSwt2", 1)
        time.sleep(.3)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)

    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_109891(self):
        '''abandon_to_inactive 通过[IF: DoorRiReOpenReqOutdLogic]判断右后外外门开按钮请求'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.io.trigger_door_outswitch_sts(RiRe=OutSwitchPressSts.NoPress)
        self.bus_comm.set_singal("bodycan", "RpodBodyFr01", "DoorRiReOpenReqOutdSwt2", 2)
        self.io.trigger_door_outswitch_sts(RiRe=OutSwitchPressSts.Press)
        self.bus_comm.set_singal("bodycan", "RpodBodyFr01", "DoorRiReOpenReqOutdSwt2", 1)
        time.sleep(.3)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_109890(self):
        '''从Abandoned进入Inactive,通过[IF: LockgCenSts]判断车辆锁状态变更'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        


    