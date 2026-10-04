#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_dooropener_ctrl_abc.py
@Author      : qian.feng@jiduauto.com
@Time        : 2023/12/7 11:30
@Description: BGM车控车设电动门
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


@allure.feature("车控车设")
@allure.story("电动门控制")
class TestDoorOpenerCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(
            [
                "CentralLockService_client",
                "DoorService_client",
                "KeyService_client",
                "VehicleSetStatusService_client",
                "EntryService_client", 
                "TailGateService_client", 

            ]
        )
        sleep(2)

    def before_each_func(self, ecu):
        self.sd_tester.write_ccp(ccp={481: 0x0A})
        self.io.set_five_door_sts(Door.close)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock,  source=LockReqSource.Ble_Rke)
        sleep(3)  # 防止开关触发热保护

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
            # self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
            self.bus_comm.set_four_door_anti_pnch_sts(anti_pnch_sts=False)
            self.soa.hmi_set_wash_mode(sts=isOn.Off)  # 洗车模式关闭
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    @allure.title("电动门外部按键控制_右前门Clsd")
    @pytest.mark.smoke
    def test_caseid_114607(self):
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_opener_req( pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.OutdSwt) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("电动门外部按键控制_左后门Clsd")
    @pytest.mark.smoke
    def test_caseid_115751(self):
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.StopDurgCls)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.push_door_outer_switch(pos=DoorPos.RearLeft,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_opener_req( lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.OutdSwt) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("478438 外部按键暂停动力侧门_[MovgoutBrkg]状态左后门stop")
    @pytest.mark.smoke
    def test_caseid_1900115(self):
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.MovgOutBrkg)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.push_door_outer_switch(pos=DoorPos.RearLeft,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_opener_req( lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Stop, trigger_src=DoorTrigerSource.OutdSwt) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("外部按键暂停动力侧门_MovgIn状态右前门stop")
    @pytest.mark.smoke
    def test_caseid_115756(self):
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.MovgIn)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_opener_req( pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Stop, trigger_src=DoorTrigerSource.OutdSwt) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("外部按键暂停动力侧门_MovgInBrkg状态右后门stop")
    @pytest.mark.smoke
    def test_caseid_115745(self):
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.MovgInBrkg)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Stop, trigger_src=DoorTrigerSource.OutdSwt) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("开关输入保护_右前门外部按键输入有效Clsd")
    @pytest.mark.smoke
    def test_caseid_114414(self):
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.OutdSwt) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("开关输入保护_左后门外部按键输入无效PsdTime > 1000ms")
    @pytest.mark.smoke
    def test_caseid_114354(self):
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.io.trigger_door_outswitch_sts(LeRe=OutSwitchPressSts.Press)
        time.sleep(1.5)
        self.bus_comm.set_singal("bodycan","LpodBodyFr01", 'DoorLeReOpenReqOutdSwt2', 1)
        self.bus_comm.check_door_without_open_req(lere_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("内部按键持续开关输入保护_PsdTime超过1000ms按下_车门请求不发")
    @pytest.mark.smoke
    def test_caseid_114356(self):
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_singal("bodycan","PdmBodyFr01", 'DoorPassOpenReqInsdSwt1', 1)
        self.io.trigger_door_outswitch_sts(LeRe=OutSwitchPressSts.Press)
        time.sleep(1.5)
        self.bus_comm.set_singal("bodycan","PpodBodyFr01", 'DoorPassOpenReqInsdSwt2', 1)
        self.bus_comm.check_door_without_open_req(pass_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    # @allure.title("DID 42 F2 读取后主驾门状态")
    # @pytest.mark.full
    # @pytest.mark.update
    # def test_caseid_1987040(self):
    #     self.io.set_door(Drvr=Door.open)
    #     self.sd_tester.did_check_ajar_sts(pos=AjarSwitchPos.LeftFront, sts=OpenCloseSts.Close)
    #     self.io.set_door(Drvr=Door.close)
    #     self.sd_tester.did_check_ajar_sts(pos=AjarSwitchPos.LeftFront, sts=OpenCloseSts.Open)

    # @allure.title("DID 42 F2 读取副驾门状态")
    # @pytest.mark.full
    # @pytest.mark.update
    # def test_caseid_1987041(self):
    #     self.io.set_door(Pass=Door.open)
    #     self.sd_tester.did_check_ajar_sts(pos=AjarSwitchPos.RightFront, sts=OpenCloseSts.Close)
    #     self.io.set_door(Pass=Door.close)
    #     self.sd_tester.did_check_ajar_sts(pos=AjarSwitchPos.RightFront, sts=OpenCloseSts.Open)

    # @allure.title("501126 DID 42 F2 读取右后门状态")
    # @pytest.mark.full
    # @pytest.mark.update
    # def test_caseid_1987043(self):
    #     self.io.set_door(RiRe=Door.open)
    #     self.sd_tester.did_check_ajar_sts(pos=AjarSwitchPos.RightRear, sts=OpenCloseSts.Close)
    #     self.io.set_door(RiRe=Door.close)
    #     self.sd_tester.did_check_ajar_sts(pos=AjarSwitchPos.RightRear, sts=OpenCloseSts.Open)

    # @allure.title("501126 DID 42 F2 读取后备箱Ajar开关")
    # @pytest.mark.full
    # @pytest.mark.update
    # def test_caseid_1987039(self):
    #     self.io.set_door(Trunk=Door.open)
    #     self.sd_tester.did_check_ajar_sts(pos=AjarSwitchPos.TailGate, sts=OpenCloseSts.Close)
    #     self.io.set_door(Trunk=Door.close)
    #     self.sd_tester.did_check_ajar_sts(pos=AjarSwitchPos.TailGate, sts=OpenCloseSts.Open)

    # @allure.title("DID 42 F2 读取左后门状态")
    # @pytest.mark.full
    # @pytest.mark.update
    # def test_caseid_1987042(self):
    #     self.io.set_door(LeRe=Door.open)
    #     self.sd_tester.did_check_ajar_sts(pos=AjarSwitchPos.LeftRear, sts=OpenCloseSts.Close)
    #     self.io.set_door(LeRe=Door.close)
    #     self.sd_tester.did_check_ajar_sts(pos=AjarSwitchPos.LeftRear, sts=OpenCloseSts.Open)

    @allure.title("电动门外部按键控制_右后门DoorPos_右后门SecondaryPosition外按键控制门开")
    @pytest.mark.smoke
    def test_caseid_115746(self):
        self.bus_comm.set_child_lock_sts(side=Side.Right, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.Ukwn)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.set_door_latch_posn(doorid= DoorId.kDoorRearRight, latposn= LatPosition.SecondaryPosition)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, trigger_src=DoorTrigerSource.OutdSwt) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("内按键控制动力侧门开启_左前门仅开关状态处于Close_内按键开主驾门")
    @pytest.mark.smoke
    def test_caseid_115760(self):
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.Ukwn)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.NA, isopen=False, antipinch=False)
        self.bus_comm.set_door_latch_posn(doorid= DoorId.kDoorFrontLeft, latposn= LatPosition.Undefined)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Dirver, time_interval=0.2)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, trigger_src=DoorTrigerSource.InsdSwt) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("破冰场景下控制前排车门开启最小角度5%")
    @pytest.mark.smoke
    def test_caseid_1913507(self):
        self.bus_comm.set_door_active_ice_sts(Drvr = False, Pass = False)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_active_ice_sts(Drvr = True)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Dirver, position=5, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.set_door_active_ice_sts(Pass = True)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=5, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.set_door_active_ice_sts(Drvr = False, Pass = False)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("破冰场景下控制后排车门开启最小角度7%")
    @pytest.mark.smoke
    def test_caseid_1913505(self):
        self.bus_comm.set_door_active_ice_sts(LeRe = False, RiRe = False)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_active_ice_sts(LeRe = True)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearLeft, position=7, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.set_door_active_ice_sts(RiRe = True)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearRight, position=7, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.set_door_active_ice_sts(LeRe = False, RiRe = False)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("492101 挂挡自动关门启用_D挡自动关门")
    @pytest.mark.smoke
    def test_caseid_114366(self):
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 0)  
        self.soa.hmi_set_auto_close_door_by_drive_gear()  
        self.soa.hmi_get_automatic_door_closing(TriggerType.enable)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal2)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)  
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 3)  
        self.bus_comm.check_singal("bodycan", "CemBodyFr78", "DoorOpenerDrvrReqDoorOpenerReq2", 2)  
        self.bus_comm.check_singal("bodycan", "CemBodyFr78", "DoorOpenerDrvrReqTrigSrc", 0)  
 
    @allure.title("492101 挂挡自动关门启用_R挡自动关门")
    @pytest.mark.sanity
    def test_caseid_1980994(self):
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 0)  
        self.soa.hmi_set_auto_close_door_by_drive_gear()  
        self.soa.hmi_get_automatic_door_closing(TriggerType.enable)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)  
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 1)  
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req=DoorOpenerReq.Close,trigger_src=DoorTrigerSource.NoTrigSrc)

    @allure.title("492101 挂挡自动关门禁用_R挡车门无动作")
    @pytest.mark.sanity
    def test_caseid_1980995(self):
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 0)  
        self.soa.cancel_auto_close_door_by_gear_driving()
        self.soa.hmi_get_automatic_door_closing(TriggerType.disable)
        sleep(2)  # 等设置项生效
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)  
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 1)  
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.All, door_req= DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc) 

    @allure.title("492101 挂挡自动关门禁用_R挡车门无动作")
    @pytest.mark.full
    def test_caseid_1993525(self):
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 0)  
        self.soa.cancel_auto_close_door_by_gear_driving()
        self.soa.hmi_get_automatic_door_closing(TriggerType.disable)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)  
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 1)  
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.All, door_req= DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("外按键控制动力侧门开启_FullCsd主驾门Open")
    @pytest.mark.full
    def test_caseid_1991786(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.set_door_latch_posn(doorid= DoorId.kDoorFrontLeft, latposn= LatPosition.FullyOpen)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, trigger_src=DoorTrigerSource.OutdSwt) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("外按键控制动力侧门开启_HaldClsd副驾门Open")
    @pytest.mark.full
    def test_caseid_1991785(self):
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.HalfClsd)
        self.bus_comm.set_door_latch_posn(doorid= DoorId.kDoorFrontRight, latposn= LatPosition.FullyOpen)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Open, trigger_src=DoorTrigerSource.OutdSwt) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("外按键控制动力侧门开启_外按键Swt1和Swt2超360ms按下_BGM不响应")
    @pytest.mark.full
    def test_caseid_1991781(self):
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.io.trigger_door_outswitch_sts(RiRe=OutSwitchPressSts.Press)
        time.sleep(0.4)
        self.bus_comm.set_singal("bodycan","RpodBodyFr01", 'DoorRiReOpenReqOutdSwt2', 1)
        self.bus_comm.check_singal("backbonefr","CemBackBoneFr38", 'DoorRiReOpenReqOutdLogic', 2)
        self.bus_comm.check_door_without_open_req(rire_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("外按键控制动力侧门开启_洗车模式On短按请求忽略")
    @pytest.mark.full
    def test_caseid_1991783(self):
        self.soa.hmi_set_wash_mode(sts=isOn.On)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.StopMinPntForCls)
        self.bus_comm.set_door_latch_posn(doorid= DoorId.kDoorRearRight, latposn= LatPosition.FullyClosed)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_without_open_req(rire_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)

    @allure.title("电动门外部按键控制动力侧门关闭_StopDugCls右前门Clsd")
    @pytest.mark.sanity
    def test_caseid_1991780(self):
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.StopDurgCls)
        self.bus_comm.set_door_latch_posn(doorid= DoorId.kDoorFrontRight, latposn= LatPosition.Undefined)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.OutdSwt) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("470583 电动门外部按键控制动力侧门关闭_洗车模式On_外开关禁用")
    @pytest.mark.sanity
    def test_caseid_1991779(self):
        self.soa.hmi_set_wash_mode(sts=isOn.On)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_without_open_req(pass_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)

    @allure.title("外开关Swt1和Swt2输入条件")
    @pytest.mark.full
    def test_caseid_1988698(self):
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.check_signal_thread_start('backbonefr', 'CemBackBoneFr38', 'DoorPassOpenReqOutdLogic')  
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=0.4, pe_test=True)
        result_ori = self.bus_comm.check_signal_thread_stop('DoorPassOpenReqOutdLogic')  
        logger.info(f'获取到的原始数据DoorPassOpenReqOutdLogic为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] !=0
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.ipdu.reset_check_results()

    @allure.title("踩刹车关门设置项开&&踏板信号未跳变_不发关门请求")
    @pytest.mark.smoke
    def test_caseid_1988537(self):
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)         
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)  
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0) 
        self.soa.hmi_set_and_get_braking_close_the_door(isOn=False)    
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)

    @allure.title("外按键控制动力侧门开启_条件满足电释放请求On")
    @pytest.mark.full
    def test_caseid_1991782(self):
        self.bus_comm.set_door_lock_sts(rire_lock=LockSts.Unlocked)
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorRearRight, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.StopMinPntForCls)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_rels_req(RiRe=DoorRelsReq.On)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        
    @allure.title("外按键控制动力侧门开启_StopMinPntForCls左后门Open")
    @pytest.mark.full
    def test_caseid_1991784(self):
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.StopMinPntForCls)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)
        self.mix.push_door_outer_switch(pos=DoorPos.RearLeft,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Open, trigger_src=DoorTrigerSource.OutdSwt) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("控制动力侧门_CCP481=02控制主驾门开")
    @pytest.mark.full
    def test_caseid_1991824(self):
        self.sd_tester.write_ccp(ccp={481: 0x02})
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("控制动力侧门_CCP481=03控制副驾门开")
    @pytest.mark.full
    def test_caseid_1991823(self):
        self.sd_tester.write_ccp(ccp={481: 0x03})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.TRANSPORT, vehmtnst=VehMtnSts.StandStillVal2)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("控制动力侧门_CCP481=04控制左后门暂停")
    @pytest.mark.full
    def test_caseid_1991822(self):
        self.sd_tester.write_ccp(ccp={481: 0x04})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.FACTORY, vehmtnst=VehMtnSts.StandStillVal2)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.MovgOut)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Stop, trigger_src=DoorTrigerSource.HMI) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("控制动力侧门_CCP481=08控制副驾门开")
    @pytest.mark.full
    def test_caseid_1991821(self):
        self.sd_tester.write_ccp(ccp={481: 0x08})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO, vehmtnst=VehMtnSts.StandStillVal2)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("控制动力侧门_CCP481=09控制右后门开")
    @pytest.mark.full
    def test_caseid_1991820(self):
        self.sd_tester.write_ccp(ccp={481: 0x09})
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("控制动力侧门_CCP481=0A控制四门")
    @pytest.mark.full
    def test_caseid_1991819(self):
        self.bus_comm.set_five_door_opener_sts(door_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI) 
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("控制动力侧门_CCP481不满足_关门请求不发")
    @pytest.mark.full
    def test_caseid_1991818(self):
        self.sd_tester.write_ccp(ccp={481: 0x00})
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_without_open_req(pass_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.sd_tester.write_ccp(ccp={481: 0x0A})

    @allure.title("控制动力侧门_Convenience模式下EgyLvlElecMai= 1侧门不开启")
    @pytest.mark.full
    def test_caseid_1991817(self):
        self.sd_tester.write_ccp(ccp={481: 0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, vehmtnst= VehMtnSts.StandStillVal2)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x03, SESSION.EXTENDED, UnLock.L0, '1000', '6f429d', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_egylvlelec(mai=1, subtype=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429d', check_method=Check_Method.response, recover=False)

    @allure.title("关闭动力侧门_Driving模式关闭主驾门")
    @pytest.mark.full
    def test_caseid_1991814(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x03, SESSION.EXTENDED, UnLock.L0, '1000', '6f429d', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_egylvlelec(mai=1, subtype=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, vehmtnst= VehMtnSts.StandStillVal2)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.HMI) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429d', check_method=Check_Method.response, recover=False)

    @allure.title("关闭动力侧门_Active模式EgyLvlElecMai==1关闭副驾门")
    @pytest.mark.sanity
    def test_caseid_1991813(self):
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x03, SESSION.EXTENDED, UnLock.L0, '1000', '6f429d', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_egylvlelec(mai=1, subtype=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, vehmtnst= VehMtnSts.StandStillVal2)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.HMI) 
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429d', check_method=Check_Method.response, recover=False)

    @allure.title("Convenience模式关闭左后门")
    @pytest.mark.full
    def test_caseid_1991812(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, vehmtnst= VehMtnSts.Ukwn)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.HMI) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("关闭动力侧门_Inactive模式关闭右后门")
    @pytest.mark.full
    def test_caseid_1991811(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst= VehMtnSts.Ukwn)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.HMI) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("关闭动力侧门_Abandoned模式关闭主驾门")
    @pytest.mark.full
    def test_caseid_1991810(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, vehmtnst= VehMtnSts.StandStillVal3)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ABANDONED)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.HMI) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("关闭动力侧门_Inactive模式车身能量受限关门请求忽略")
    @pytest.mark.full
    def test_caseid_1991809(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst= VehMtnSts.StandStillVal2)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x03, SESSION.EXTENDED, UnLock.L0, '1000', '6f429d', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_egylvlelec(mai=1, subtype=0)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_without_open_req(rire_opener=DoorOpenerReq.Idle)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429d', check_method=Check_Method.response, recover=False)

    @allure.title("关闭动力侧门_主驾触发防夹关门请求忽略")
    @pytest.mark.full
    def test_caseid_1991808(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst= VehMtnSts.StandStillVal2)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_door_anti_pnch_sts(Drvr=True)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_door_anti_pnch_sts(Drvr=False)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("关闭动力侧门_道路倾斜角小于-0.20")
    @pytest.mark.full
    def test_caseid_1991807(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst= VehMtnSts.StandStillVal2)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_vehicle_rollover_and_inclination_angles(rangetype=RangeType.RoadIncln, incln=-0.210)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_vehicle_rollover_and_inclination_angles(rangetype=RangeType.RoadIncln, incln=0)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("关闭动力侧门_道路倾斜角大于0.2")
    @pytest.mark.full
    def test_caseid_1991806(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst= VehMtnSts.StandStillVal2)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_vehicle_rollover_and_inclination_angles(rangetype=RangeType.RoadIncln, incln=0.210)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_vehicle_rollover_and_inclination_angles(rangetype=RangeType.RoadIncln, incln=0)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("关闭动力侧门_车身翻转角小于-0.20")
    @pytest.mark.full
    def test_caseid_1991805(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst= VehMtnSts.StandStillVal2)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_vehicle_rollover_and_inclination_angles(rangetype=RangeType.RollAgGlb, roll=-0.210)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_vehicle_rollover_and_inclination_angles(rangetype=RangeType.RollAgGlb, roll=0)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("关闭动力侧门_道路倾斜角大于0.2")
    @pytest.mark.full
    def test_caseid_1991804(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst= VehMtnSts.StandStillVal2)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_vehicle_rollover_and_inclination_angles(rangetype=RangeType.RollAgGlb, roll=0.210)
        sleep(1)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_vehicle_rollover_and_inclination_angles(rangetype=RangeType.RollAgGlb, roll=0)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        
    @allure.title("主驾门close状态与质量因数")
    @pytest.mark.sanity
    def test_caseid_114295(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, vehmtnst= VehMtnSts.StandStillVal2)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_singal("backbonefr","CemBackBoneFr06", 'DoorDrvrStsWithFacQlyDoorSts', 1)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_singal("backbonefr","CemBackBoneFr06", 'DoorDrvrStsWithFacQlyDoorSts', 2)

    @allure.title("主驾门Open状态与质量因数")
    @pytest.mark.full
    def test_caseid_114292(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, vehmtnst= VehMtnSts.StandStillVal2)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_singal("backbonefr","CemBackBoneFr06", 'DoorDrvrStsWithFacQlyDoorSts', 2)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_singal("backbonefr","CemBackBoneFr06", 'DoorDrvrStsWithFacQlyDoorSts', 1)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_singal("backbonefr","CemBackBoneFr06", 'DoorDrvrStsWithFacQlyDoorSts', 2)

    @allure.title("后排儿童锁上锁")
    @pytest.mark.sanity
    def test_caseid_108640(self):
        self.bus_comm.check_child_lock_unlock_req(childlockside=RotateDirec.All, lockreq=LockgCenReq2.Idle)
        self.soa.set_child_lock_unlock_req(doorid=DoorId.kDoorRearLeft, childlockreq= ChildLockReq.Lock)
        self.bus_comm.check_child_lock_unlock_req(childlockside=RotateDirec.Left, lockreq=LockgCenReq2.Lock)
        self.soa.set_child_lock_unlock_req(doorid=DoorId.kDoorRearRight, childlockreq= ChildLockReq.Lock)
        self.bus_comm.check_child_lock_unlock_req(childlockside=RotateDirec.Right, lockreq=LockgCenReq2.Lock)
        self.bus_comm.check_child_lock_unlock_req(childlockside=RotateDirec.All, lockreq=LockgCenReq2.Idle, time_wait=1)

    @allure.title("后排儿童锁解锁")
    @pytest.mark.sanity
    def test_caseid_108638(self):
        self.bus_comm.check_child_lock_unlock_req(childlockside=RotateDirec.All, lockreq=LockgCenReq2.Idle)
        self.soa.set_child_lock_unlock_req(doorid=DoorId.kDoorRearLeft, childlockreq= ChildLockReq.UnLock)
        self.bus_comm.check_child_lock_unlock_req(childlockside=RotateDirec.Left, lockreq=LockgCenReq2.UnLock)
        self.soa.set_child_lock_unlock_req(doorid=DoorId.kDoorRearRight, childlockreq= ChildLockReq.UnLock)
        self.bus_comm.check_child_lock_unlock_req(childlockside=RotateDirec.Left, lockreq=LockgCenReq2.UnLock)
        self.bus_comm.check_child_lock_unlock_req(childlockside=RotateDirec.All, lockreq=LockgCenReq2.Idle, time_wait=1)

    @allure.title("后排儿童锁上锁解锁")
    @pytest.mark.full
    def test_caseid_108636(self):
        self.bus_comm.check_child_lock_unlock_req(childlockside=RotateDirec.All, lockreq=LockgCenReq2.Idle)
        self.soa.set_child_lock_unlock_req(doorid=DoorId.kDoorRearLeft, childlockreq= ChildLockReq.Lock)
        self.bus_comm.check_child_lock_unlock_req(childlockside=RotateDirec.Left, lockreq=LockgCenReq2.Lock)
        self.soa.set_child_lock_unlock_req(doorid=DoorId.kDoorRearRight, childlockreq= ChildLockReq.Lock)
        self.bus_comm.check_child_lock_unlock_req(childlockside=RotateDirec.Left, lockreq=LockgCenReq2.Lock)
        self.bus_comm.check_child_lock_unlock_req(childlockside=RotateDirec.All, lockreq=LockgCenReq2.Idle, time_wait=1)
        self.soa.set_child_lock_unlock_req(doorid=DoorId.kDoorRearLeft, childlockreq= ChildLockReq.UnLock)
        self.bus_comm.check_child_lock_unlock_req(childlockside=RotateDirec.Left, lockreq=LockgCenReq2.UnLock)
        self.soa.set_child_lock_unlock_req(doorid=DoorId.kDoorRearRight, childlockreq= ChildLockReq.UnLock)
        self.bus_comm.check_child_lock_unlock_req(childlockside=RotateDirec.Left, lockreq=LockgCenReq2.UnLock)
        self.bus_comm.check_child_lock_unlock_req(childlockside=RotateDirec.All, lockreq=LockgCenReq2.Idle, time_wait=1)

    @allure.title("电动侧门释放_副驾门锁处于Lock副驾门外按键控制忽略不释放")
    @pytest.mark.full
    def test_caseid_1991776(self):
        self.sd_tester.write_ccp(ccp={481: 0x0A})
        self.bus_comm.set_door_lock_status(doorid=DoorId.kDoorFrontRight, lock_sts=Locksts.Lockd)
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorFrontRight, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_rels_req(Pass=DoorRelsReq.Off)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("电动侧门释放_CCP不满足")
    @pytest.mark.full
    def test_caseid_1991775(self):
        self.sd_tester.write_ccp(ccp={481: 0x00})
        self.bus_comm.set_door_lock_status(doorid=DoorId.kDoorFrontRight, lock_sts=Locksts.Unlckd)
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorFrontRight, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_rels_req(Pass=DoorRelsReq.Off)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.sd_tester.write_ccp(ccp={481: 0x0A})

    @allure.title("电动侧门释放_1.8s内前置条件满足_侧门释放")
    @pytest.mark.full
    def test_caseid_1991774(self):
        self.io.set_door(Pass=Door.open)
        self.bus_comm.set_door_lock_status(doorid=DoorId.kDoorFrontRight, lock_sts=Locksts.Unlckd)
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorFrontRight, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open)
        sleep(.8)
        self.io.set_door(Pass=Door.close)
        self.bus_comm.check_door_rels_req(Pass=DoorRelsReq.On)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI控制侧门开启到目标位置_CCP481== 0x02_电动门释放On")
    @pytest.mark.full
    def test_caseid_1991773(self):
        self.sd_tester.write_ccp(ccp={481: 0x02})
        self.bus_comm.set_door_perc_position(doorpos=DoorPos.Dirver, perc_position=0)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_door_latch_posn(doorid=DoorId.kDoorFrontLeft, latposn=LatPosition.FullyClosed)
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorFrontLeft, shortdropsts=ShortDropSts.WindowDown)
        sleep(1)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Dirver, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Dirver, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.On)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("中控闭锁对应侧门锁上锁开关未禁用SecondaryPosition_电动门释放On")
    @pytest.mark.full
    def test_caseid_1991771(self):
        self.sd_tester.write_ccp(ccp={481: 0x03})
        self.bus_comm.set_door_lock_status(doorid=DoorId.kDoorFrontLeft, lock_sts=Locksts.Lockd)
        self.bus_comm.set_door_latch_posn(doorid=DoorId.kDoorFrontLeft, latposn=LatPosition.FullyClosed)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorFrontLeft, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Dirver, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Dirver, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.On)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI控制侧门开启到目标位置_CCP481== 0x04_电动门释放On")
    @pytest.mark.full
    def test_caseid_1991770(self):
        self.sd_tester.write_ccp(ccp={481: 0x04, 561: 0x02})
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorFrontLeft, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Dirver, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Dirver, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.On)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI控制侧门开启到目标位置_CCP481== 0x08_电动门释放On")
    @pytest.mark.full
    def test_caseid_1991769(self):
        self.sd_tester.write_ccp(ccp={481: 0x08, 561: 0x02})
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorFrontRight, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Pass, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_rels_req(Pass=DoorRelsReq.On)
        sleep(.5)
        self.bus_comm.check_door_rels_req(Pass=DoorRelsReq.Off)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI控制侧门开启到目标位置_CCP481== 0x09_电动门释放On")
    @pytest.mark.full
    def test_caseid_1991768(self):
        self.sd_tester.write_ccp(ccp={481: 0x09, 561: 0x02})
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorRearRight, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_postion(door_pos=DoorPos.RearRight, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearRight, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_rels_req(RiRe=DoorRelsReq.On)
        sleep(.5)
        self.bus_comm.check_door_rels_req(RiRe=DoorRelsReq.Off)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI控制侧门开启到目标位置_CCP481== 0x0A_电动门释放On")
    @pytest.mark.full
    def test_caseid_1991767(self):
        self.sd_tester.write_ccp(ccp={481: 0x0A, 561: 0x02})
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorRearRight, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_postion(door_pos=DoorPos.RearRight, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearRight, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_rels_req(RiRe=DoorRelsReq.On)
        sleep(.5)
        self.bus_comm.check_door_rels_req(RiRe=DoorRelsReq.Off)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI控制侧门开启到目标位置_CCP561== 0x02车窗未短降_电动门不释放")
    @pytest.mark.full
    def test_caseid_1991766(self):
        self.sd_tester.write_ccp(ccp={481: 0x0A, 561: 0x02})
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorRearRight, shortdropsts=ShortDropSts.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_postion(door_pos=DoorPos.RearRight, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearRight, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_rels_req(RiRe=DoorRelsReq.Off)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI控制侧门开启到目标位置_车门开启_电动门不释放")
    @pytest.mark.full
    def test_caseid_1991765(self):
        self.sd_tester.write_ccp(ccp={481: 0x0A, 561: 0x02})
        self.bus_comm.set_door_latch_posn(doorid=DoorId.kDoorFrontLeft, latposn=LatPosition.Undefined)        
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorFrontLeft, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Dirver, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Dirver, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.io.set_door(Drvr=Door.close)

    @allure.title("HMI控制侧门开启到目标位置_车门不处于关闭状态FullyOpen")
    @pytest.mark.full
    def test_caseid_1991764(self):
        self.sd_tester.write_ccp(ccp={481: 0x0A, 561: 0x02})
        self.bus_comm.set_door_latch_posn(doorid=DoorId.kDoorRearRight, latposn=LatPosition.FullyOpen)        
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorRearRight, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_postion(door_pos=DoorPos.RearRight, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearRight, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_rels_req(RiRe=DoorRelsReq.Off)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.io.set_door(RiRe=Door.close)

    @allure.title("HMI控制侧门开启到目标位置_车门不处于关闭状态Undefined")
    @pytest.mark.full
    def test_caseid_1991763(self):
        self.sd_tester.write_ccp(ccp={481: 0x0A, 561: 0x02})
        self.bus_comm.set_door_latch_posn(doorid=DoorId.kDoorRearRight, latposn=LatPosition.Undefined)        
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorRearRight, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_postion(door_pos=DoorPos.RearRight, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearRight, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_rels_req(RiRe=DoorRelsReq.Off)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.io.set_door(RiRe=Door.close)

    @allure.title("HMI控制侧门开启到目标位置_CCP481不满足")
    @pytest.mark.full
    def test_caseid_1991762(self):
        self.sd_tester.write_ccp(ccp={481: 0x00, 561: 0x02})
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorRearRight, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_postion(door_pos=DoorPos.RearRight, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearRight, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_rels_req(RiRe=DoorRelsReq.Off)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.sd_tester.write_ccp(ccp={481: 0x0A})

    @allure.title("HMI控制侧门开启到目标位置_CCP481不满足")
    @pytest.mark.full
    def test_caseid_1991761(self):
        self.sd_tester.write_ccp(ccp={481: 0x0A, 561: 0x02})
        self.bus_comm.set_door_latch_posn(doorid=DoorId.kDoorRearRight, latposn=LatPosition.Undefined)        
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorRearRight, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_postion(door_pos=DoorPos.RearRight, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearRight, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_rels_req(RiRe=DoorRelsReq.On)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI控制侧门开启到目标位置_车门释放500ms恢复")
    @pytest.mark.full
    def test_caseid_1991760(self):
        self.sd_tester.write_ccp(ccp={481: 0x0A, 561: 0x02})
        self.bus_comm.set_door_latch_posn(doorid=DoorId.kDoorRearLeft, latposn=LatPosition.Undefined)        
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorRearLeft, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.soa.hmi_set_door_postion(door_pos=DoorPos.RearLeft, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearLeft, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_rels_req(ReLe=DoorRelsReq.On)
        sleep(.5)
        self.bus_comm.check_door_rels_req(ReLe=DoorRelsReq.Off)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        
    @allure.title("左后门儿童锁On左后门内按键忽略")
    @pytest.mark.full
    def test_caseid_1991791(self):
        self.bus_comm.set_child_lock_sts(side=Side.Left, childlockstatus= OnOffSafe1.OnOffSafeOn)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.bus_comm.press_door_inside_switch(pos=DoorPos.RearLeft, time_interval=0.2)
        self.bus_comm.check_door_without_open_req(lere_opener=DoorOpenerReq.Idle) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_child_lock_sts(side=Side.Left, childlockstatus= OnOffSafe1.OnOffSafeOff)

    @allure.title("内按键控制动力侧门开启_右后门儿童锁On右后门内按键忽略")
    @pytest.mark.full
    def test_caseid_1991790(self):
        self.bus_comm.set_child_lock_sts(side=Side.Right, childlockstatus= OnOffSafe1.OnOffSafeOn)
        self.bus_comm.set_door_latch_posn(doorid= DoorId.kDoorRearRight, latposn= LatPosition.Undefined)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.bus_comm.press_door_inside_switch(pos=DoorPos.RearRight, time_interval=0.2)
        self.bus_comm.check_door_without_open_req(rire_opener=DoorOpenerReq.Idle) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_child_lock_sts(side=Side.Right, childlockstatus= OnOffSafe1.OnOffSafeOff)

    @allure.title("内按键控制动力侧门开启_整车闭锁对应侧门闭锁侧门开电释放信号监测")
    @pytest.mark.full
    def test_caseid_1991789(self):
        self.sd_tester.write_ccp(ccp={481: 0x0A, 561: 0x02})
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_door_lock_status(doorid=DoorId.kDoorFrontLeft, lock_sts=Locksts.Lockd)
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorFrontLeft, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Dirver, time_interval=0.2)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.On)
        sleep(.5)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("挂挡自动关门启用_R挡切N档车门不动作")
    @pytest.mark.sanity
    def test_caseid_1991778(self):
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 1)  
        self.soa.hmi_set_auto_close_door_by_drive_gear()  
        self.soa.hmi_get_automatic_door_closing(TriggerType.enable)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)  
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 2)  
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        
    @allure.title("挂挡自动关门启用_3s超时上Driving")
    @pytest.mark.sanity
    def test_caseid_1991777(self):
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 0)  
        self.soa.hmi_set_auto_close_door_by_drive_gear()  
        self.soa.hmi_get_automatic_door_closing(TriggerType.enable)
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 1)  
        sleep(3.1)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13) 
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("D档自动关门_挡位切换联动尾门关闭")
    @pytest.mark.full
    def test_caseid_109439(self):
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 0)  
        self.soa.hmi_set_auto_close_door_by_drive_gear()  
        self.soa.hmi_get_automatic_door_closing(TriggerType.enable)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13) 
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 3)  
        self.bus_comm.check_tailgate_opener_req(req=SetTailGatePos.Close)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("内按键控制动力侧门开启_FullCsd左后门open")
    @pytest.mark.full
    def test_caseid_1991796(self):
        self.bus_comm.set_child_lock_sts(side=Side.Left, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearLeftDoorSts, isopen=True, doormovests=DoorMoveStatus.Closed, antipinch=False)
        self.bus_comm.set_door_latch_posn(doorid= DoorId.kDoorRearLeft, latposn= LatPosition.Undefined)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.RearLeft, time_interval=0.2)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Open, trigger_src=DoorTrigerSource.InsdSwt) 
        sleep(.5)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.io.set_door(LeRe=Door.close)

    @allure.title("498899 内按键控制动力侧门开启_HaldClsd右后门open")
    @pytest.mark.full
    def test_caseid_1991795(self):
        self.bus_comm.set_child_lock_sts(side=Side.Right, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.HalfClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, isopen=True, doormovests=DoorMoveStatus.HalfClosed, antipinch=False)
        self.bus_comm.set_door_latch_posn(doorid= DoorId.kDoorRearRight, latposn= LatPosition.Undefined)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.RearRight, time_interval=0.2)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, trigger_src=DoorTrigerSource.InsdSwt) 
        sleep(.5)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.io.set_door(RiRe=Door.close)

    @allure.title("内按键控制动力侧门开启_主驾门DoorDrvrSts=Clsd运动状态Ukwn左前门open")
    @pytest.mark.full
    def test_caseid_1991792(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.Ukwn)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, isopen=False, doormovests=DoorMoveStatus.NA, antipinch=False)
        self.bus_comm.set_door_latch_posn(doorid= DoorId.kDoorFrontLeft, latposn= LatPosition.Undefined)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等待前置条件生效
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Dirver, time_interval=0.2)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, trigger_src=DoorTrigerSource.InsdSwt) 
        sleep(.5)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.io.set_door(RiRe=Door.close)

    @allure.title("内按键控制动力侧门开启_洗车模式开_小角度开门")
    @pytest.mark.full
    def test_caseid_1991788(self):
        self.soa.hmi_set_wash_mode(sts=isOn.On)
        self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr21", 'WashModeSts', 1)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等待前置条件生效
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Dirver, time_interval=0.2)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.OpenMinang, trigger_src=DoorTrigerSource.InsdSwt) 
        sleep(.5)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr21", 'WashModeSts', 0)

    @allure.title("防夹状态通知")
    @pytest.mark.smoke
    def test_caseid_115743(self):
        self.bus_comm.set_four_door_anti_pnch_sts(anti_pnch_sts=False)
        self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
        self.bus_comm.set_door_anti_pnch_sts(Drvr=True)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, isopen=False, doormovests=DoorMoveStatus.Closed, antipinch=True)
        self.bus_comm.set_door_anti_pnch_sts(Pass=True)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntRightDoorSts, isopen=False, doormovests=DoorMoveStatus.Closed, antipinch=True)
        self.bus_comm.set_door_anti_pnch_sts(LeRe=True)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearLeftDoorSts, isopen=False, doormovests=DoorMoveStatus.Closed, antipinch=True)
        self.bus_comm.set_door_anti_pnch_sts(RiRe=True)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, isopen=False, doormovests=DoorMoveStatus.Closed, antipinch=True)
        self.bus_comm.set_four_door_anti_pnch_sts(anti_pnch_sts=False)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.All, isopen=False, doormovests=DoorMoveStatus.Closed, antipinch=False)
        
    @allure.title("HMI控制侧门开启到目标位置_CCP481== 0x03_电动门释放On")
    @pytest.mark.full
    def test_caseid_1991772(self):
        self.sd_tester.write_ccp(ccp={481: 0x03})
        self.bus_comm.set_door_perc_position(doorpos=DoorPos.Pass, perc_position=0)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.set_door_latch_posn(doorid=DoorId.kDoorFrontRight, latposn=LatPosition.SecondaryPosition)
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorFrontRight, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等待前置条件生效
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Pass, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_rels_req(Pass=DoorRelsReq.On)
        self.io.set_door(Pass=Door.close)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI控制动力侧门暂停_非运动过程中StopMinPntForCls_Stop忽略")
    @pytest.mark.full
    def test_caseid_1991799(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.StopDurgCls)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, isopen=False, doormovests=DoorMoveStatus.Hover, antipinch=False, time_wait=2)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等待前置条件生效
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("498899 内按键控制动力侧门开启_HaldClsd右后门open")
    @pytest.mark.full
    def test_caseid_1991794(self):
        self.bus_comm.set_child_lock_sts(side=Side.Right, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.HalfClsd)
        self.io.set_door(RiRe=Door.open)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, isopen=True, doormovests=DoorMoveStatus.HalfClosed, antipinch=False)
        self.bus_comm.set_door_latch_posn(doorid= DoorId.kDoorRearRight, latposn= LatPosition.Undefined)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等待前置条件生效
        self.bus_comm.press_door_inside_switch(pos=DoorPos.RearRight, time_interval=0.2)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, trigger_src=DoorTrigerSource.InsdSwt) 
        sleep(.5)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.io.set_door(RiRe=Door.close)

    @allure.title("电动门内部按键控制_车门非关闭状态_内按键控制不发Open请求")
    @pytest.mark.full
    def test_caseid_1991787(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等待前置条件生效
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Dirver, time_interval=0.2)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.io.set_door(Drvr=Door.close)

    @allure.title("HMI控制动力侧门暂停_非运动过程中Ukwn_Stop忽略")
    @pytest.mark.full
    def test_caseid_1991803(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.Ukwn)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, isopen=False, doormovests=DoorMoveStatus.NA, antipinch=False)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等待前置条件生效
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI控制动力侧门暂停_非运动过程中FullClsd_Stop忽略")
    @pytest.mark.full
    def test_caseid_1991802(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, isopen=False, doormovests=DoorMoveStatus.Closed, antipinch=False)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等待前置条件生效
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        
    @allure.title("HMI控制动力侧门暂停_非运动过程中FullClsd_Stop忽略")
    @pytest.mark.full
    def test_caseid_1991801(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, isopen=False, doormovests=DoorMoveStatus.Opened, antipinch=False)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI控制动力侧门暂停_非运动过程中StopMinPntForCls_Stop忽略")
    @pytest.mark.full
    def test_caseid_1991800(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.StopMinPntForCls)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, isopen=False, doormovests=DoorMoveStatus.Hover, antipinch=False)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等待前置条件生效
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI控制动力侧门暂停_非运动过程中StopMinPntForCls_Stop忽略")
    @pytest.mark.full
    def test_caseid_1991798(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.HalfClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, isopen=False, doormovests=DoorMoveStatus.HalfClosed, antipinch=False)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等待前置条件生效
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("控制动力侧门_动力侧门开关停打断逻辑")
    @pytest.mark.full
    def test_caseid_1994506(self):
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgInBrkg)
        sleep(.1)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Stop, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        sleep(.1)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Close, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgInBrkg)
        sleep(.1)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Stop, door_trigsrc=DoorTrigerSource.HMI) 

    @allure.title("内按键控制动力侧门开启_SecondaryPosition右前门open")
    @pytest.mark.full
    def test_caseid_1991797(self):
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.Ukwn)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntRightDoorSts, isopen=False, doormovests=DoorMoveStatus.NA, antipinch=False)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.set_door_latch_posn(doorid= DoorId.kDoorFrontRight, latposn= LatPosition.SecondaryPosition)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Pass, time_interval=0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.InsdSwt) 
        sleep(.5)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.io.set_door(Pass=Door.close)

    @allure.title("内按键控制动力侧门开启_主驾门DoorDrvrSts=Clsd左前门open")
    @pytest.mark.full
    def test_caseid_1991793(self):
        self.mix.set_and_get_wash_mode_sts(sts=isOn.Off)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Dirver, time_interval=0.2)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, trigger_src=DoorTrigerSource.InsdSwt) 
        sleep(.5)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("Crash事件门状态反馈_CrashStsSafe== Crash_15s电释放Off车门动作维持Stop")
    @pytest.mark.sanity
    def test_caseid_1991759(self):
        self.bus_comm.set_crashsts_safests(CrashSts= crashsts.NoCrash)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off, Pass=DoorRelsReq.Off, ReLe=DoorRelsReq.Off, RiRe=DoorRelsReq.Off)
        self.io.set_five_door_sts(sts=Door.close)
        self.bus_comm.set_crashsts_safests(CrashSts= crashsts.Crash)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.CRASH)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Stop, trigger_src=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off, Pass=DoorRelsReq.Off, ReLe=DoorRelsReq.Off, RiRe=DoorRelsReq.Off)
        sleep(10)  
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Stop, trigger_src=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off, Pass=DoorRelsReq.Off, ReLe=DoorRelsReq.Off, RiRe=DoorRelsReq.Off)
        sleep(5)
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.set_crashsts_safests(CrashSts= crashsts.NoCrash)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.NORMAL)

    @allure.title("VehMtnSt接收端通信安全机制_Convenience非静止侧门不释放")
    @pytest.mark.sanity
    def test_caseid_114727(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst= VehMtnSts.StandStillVal1)
        self.bus_comm.set_door_lock_status(doorid=DoorId.kDoorFrontRight, lock_sts=Locksts.Lockd)
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorFrontRight, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Pass, time_interval=0.2)
        self.bus_comm.check_door_rels_req(Pass=DoorRelsReq.Off)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
       
    @allure.title("外开关禁用_洗车模式激活四门外开关禁用")
    @pytest.mark.full
    def test_caseid_1991615(self):
        self.mix.set_and_get_wash_mode_sts(sts=isOn.On)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle)
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_without_open_req(pass_opener=DoorOpenerReq.Idle)
        self.mix.push_door_outer_switch(pos=DoorPos.RearLeft,time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_without_open_req(lere_opener=DoorOpenerReq.Idle)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_without_open_req(rire_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.mix.set_and_get_wash_mode_sts(sts=isOn.Off)

    @allure.title("外开关禁用_洗车模式激活内开关仅小角度开门")
    @pytest.mark.full
    def test_caseid_1991613(self):
        self.mix.set_and_get_wash_mode_sts(sts=isOn.On)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等待前置条件生效
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Dirver, time_interval=0.2)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.OpenMinang, trigger_src=DoorTrigerSource.InsdSwt) 
        sleep(.5)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.mix.set_and_get_wash_mode_sts(sts=isOn.Off)

    @allure.title("外开关禁用_洗车模式激活内开关仅小角度开门")
    @pytest.mark.full
    def test_caseid_1991612(self):
        self.mix.set_and_get_wash_mode_sts(sts=isOn.On)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等待前置条件生效
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.OpenMinang, trigger_src=DoorTrigerSource.HMI) 
        sleep(.5)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.mix.set_and_get_wash_mode_sts(sts=isOn.Off)

    @allure.title("外开关禁用_洗车模式激活内开关仅小角度开门")
    @pytest.mark.full
    def test_caseid_1991464(self):
        self.mix.set_and_get_wash_mode_sts(sts=isOn.On)
        self.bus_comm.set_door_lock_status(doorid=DoorId.kDoorRearRight, lock_sts=Locksts.Unlckd)
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorRearRight, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.check_signal_thread_start('bodycan', 'CemBodyFr01', 'DoorRiReRelsReq')  
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5, pe_test=True)
        result_ori = self.bus_comm.check_signal_thread_stop('DoorRiReRelsReq')  
        logger.info(f'获取到的原始数据DoorRiReRelsReq为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] !=0
        self.mix.set_and_get_wash_mode_sts(sts=isOn.Off)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.ipdu.reset_check_results()

    @allure.title("洗车模式下外按键控制侧门开启_左后门FullClsd左后门Open")
    @pytest.mark.full
    def test_caseid_119092(self):
        self.mix.set_and_get_wash_mode_sts(sts=isOn.On)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.set_door_lock_status(doorid=DoorId.kDoorRearLeft, lock_sts=Locksts.Unlckd)
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorRearLeft, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1) # 等前置条件生效
        self.bus_comm.check_signal_thread_start('bodycan', 'CemBodyFr78', 'DoorOpenerLeReReqDoorOpenerReq2')  
        self.mix.push_door_outer_switch(pos=DoorPos.RearLeft,time_interval=2.5, pe_test=True)
        result_ori = self.bus_comm.check_signal_thread_stop('DoorOpenerLeReReqDoorOpenerReq2')  
        logger.info(f'获取到的原始数据DoorOpenerLeReReqDoorOpenerReq2为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] !=0
        self.mix.set_and_get_wash_mode_sts(sts=isOn.Off)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.io.set_door(LeRe=Door.close)
        self.bus_comm.ipdu.reset_check_results()

    @allure.title("洗车模式下外部按键控制动力侧门开_主驾门锁舌位置 Fully closed电释放信号On")
    @pytest.mark.full
    def test_caseid_119089(self):
        self.mix.set_and_get_wash_mode_sts(sts=isOn.On)
        self.bus_comm.set_door_lock_status(doorid=DoorId.kDoorFrontLeft, lock_sts=Locksts.Unlckd)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.Ukwn)
        self.bus_comm.set_door_latch_posn(doorid= DoorId.kDoorFrontLeft, latposn= LatPosition.SecondaryPosition)
        self.bus_comm.set_windows_short_drop_sts(doorid=DoorId.kDoorFrontLeft, shortdropsts=ShortDropSts.WindowDown)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1) # 等前置条件生效
        self.bus_comm.check_signal_thread_start('bodycan', 'CemBodyFr01', 'DoorDrvrRelsReq')  
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5, pe_test=True)
        result_ori = self.bus_comm.check_signal_thread_stop('DoorDrvrRelsReq')  
        logger.info(f'获取到的原始数据DoorDrvrRelsReq为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] !=0
        self.mix.set_and_get_wash_mode_sts(sts=isOn.Off)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.ipdu.reset_check_results()

    @allure.title("洗车模式下外按键控制侧门开启_闭锁外开关禁用")
    @pytest.mark.full
    def test_caseid_119091(self):
        self.mix.set_and_get_wash_mode_sts(sts=isOn.On)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1) # 等前置条件生效
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=2.5, pe_test=True)  
        self.bus_comm.check_door_without_open_req(pass_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.mix.set_and_get_wash_mode_sts(sts=isOn.Off)
        
    @allure.title("D档自动关门_挡位切换联动尾门关闭")
    @pytest.mark.full
    def test_caseid_1993525(self):
        self.bus_comm.set_fr_gear_pos(gear=Gear.Park)
        self.soa.hmi_set_auto_close_door_by_drive_gear()  
        self.soa.hmi_get_automatic_door_closing(TriggerType.enable)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.set_fr_gear_pos(gear=Gear.Neut)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle, pass_opener=DoorOpenerReq.Idle, lere_opener=DoorOpenerReq.Idle, rire_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI控制动力侧门暂停_非运动过程中Ukwn_Stop忽略")
    @pytest.mark.full
    def test_caseid_1991803(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.Ukwn)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst= VehMtnSts.StandStillVal3)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI控制动力侧门暂停_非运动过程中FullClsd_Stop忽略")
    @pytest.mark.full
    def test_caseid_1991802(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst= VehMtnSts.StandStillVal3)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI控制动力侧门暂停_非运动过程中FullOpend_Stop忽略")
    @pytest.mark.full
    def test_caseid_1991801(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst= VehMtnSts.StandStillVal3)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI控制动力侧门暂停_非运动过程中StopMinPntForCls_Stop忽略")
    @pytest.mark.full
    def test_caseid_1991800(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.StopMinPntForCls)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst= VehMtnSts.StandStillVal3)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI控制动力侧门暂停_非运动过程中StopDurgCls_Stop忽略")
    @pytest.mark.full
    def test_caseid_1991799(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.StopDurgCls)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst= VehMtnSts.StandStillVal3)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI控制动力侧门暂停_非运动过程中HalfClsd_Stop忽略")
    @pytest.mark.full
    def test_caseid_1991798(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.HalfClsd)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst= VehMtnSts.StandStillVal3)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("远控闭锁关门_关门请求及触发源校验")
    @pytest.mark.full
    def test_caseid_115761(self):
        self.io.set_five_door_sts(sts=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1) # 等前置条件生效
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.Telm, timeout=5) 
        self.io.set_five_door_sts(sts=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)      
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("门锁联动_五门全开PEPS关门闭锁")
    @pytest.mark.full
    def test_caseid_1979664(self):
        self.io.set_door(Pass=Door.open)
        self.sd_tester.write_ccp(ccp={94: 0x80})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1) # 等前置条件生效
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.OutdSwt, timeout=5)    
        sleep(2)
        self.io.set_door(Pass=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)      
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("RKE闭锁_RKE闭锁联动关门")
    @pytest.mark.full
    def test_caseid_1979662(self):
        self.io.set_door(LeRe=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1) # 等前置条件生效
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.KeyRem, timeout=5) 
        self.io.set_door(LeRe=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)      
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("洗车模式下外按键控制侧门开启_主驾门Open")
    @pytest.mark.full
    def test_caseid_119087(self):
        self.mix.set_and_get_wash_mode_sts(sts=isOn.On, time_wait=3)
        self.soa.hmi_set_wash_mode(sts=isOn.On, time_wait=1)
        self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr21", 'WashModeSts', 1, check_time=3)

        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1) # 等前置条件生效
        self.bus_comm.check_signal_thread_start('bodycan', 'CemBodyFr78', 'DoorOpenerDrvrReqDoorOpenerReq2')  
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5, pe_test=True)
        result_ori = self.bus_comm.check_signal_thread_stop('DoorOpenerDrvrReqDoorOpenerReq2')  
        logger.info(f'获取到的原始数据DoorOpenerDrvrReqDoorOpenerReq2为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] !=0
        self.bus_comm.ipdu.reset_check_results()
        self.mix.set_and_get_wash_mode_sts(sts=isOn.Off)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.io.set_door(Drvr=Door.close)
        
    @allure.title("远控闭锁关门_关门请求及触发源校验")
    @pytest.mark.full
    def test_caseid_1979663(self):
        self.io.set_five_door_sts(sts=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.io.driver_seat_notpresent()
        sleep(1) # 等前置条件生效
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.Telm, timeout=5)  # 同时拿四门拿不到
        self.io.set_five_door_sts(sts=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)      
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("右后门触发破冰小角度开门请求信号检测7%")
    @pytest.mark.full
    def test_caseid_1913506(self):
        self.bus_comm.set_door_active_ice_sts(RiRe= False)
        self.bus_comm.set_door_active_ice_sts(RiRe = True)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearRight, position=7, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearRight, position=101, door_trigsrc=DoorTrigerSource.NoTrigSrc, timeout=1.5)
        self.bus_comm.set_door_active_ice_sts(RiRe= False)
