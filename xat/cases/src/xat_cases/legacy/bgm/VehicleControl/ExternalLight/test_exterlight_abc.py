#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_extilight.py
@Author      : daidi.liang@jiduauto.com
@Time        : 2024/03/26 11:30
@Description: BGM车控车设外灯
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
from xat_ecu.legacy.soa_partner.src.base_partner import S2sBaseClass
from xat_ecu.api.abc_interface import *

# KEY_SERVICE_CLIENT = "KeyService_client"
@allure.feature("车控车设")
@allure.story("外灯/倒车灯")
class TestExltlightCtrlABC(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["LightService_client",'KeyService_client','CentralLockService_client','VehicleModeService_client','WTIService_client'])
        self.sd_tester.set_ccp(ccp_vlaue={274:0x80})
        self.sd_tester.set_ccp(ccp_vlaue={508:0x03})
        sleep(2)
    
    def before_each_func(self, ecu):
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()

    def after_each_func(self, ecu):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)

    def after_class(self, ecu):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)


    def check_hwl_lamp_flash_sts(self,flash_time:int,indcrdisp:IndcrSts=None):
        for num in range(flash_time):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=indcrdisp)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.Off)
    
    def check_turn_lamp_flash_sts(self,act_sts_le:PosnLampSts,act_sts_ri:PosnLampSts,pos:IndcrSts):
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=act_sts_le,act_sts_ri=act_sts_ri,pos_sts=pos)
            self.bus_comm.check_turn_lamp_act_req(sts=pos,act_sts=pos)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=pos,act_sts=IndcrSts.Off)

    def set_centrllock_to_lock(self,locksource:LockSource):
        self.mix.set_all_seats_present_sts(seat_pres_sts=SeatPresSts.NoPres)
        self.io.set_five_door_sts(Door.close)
        # 设置bodycan上五个电动门均关闭
        self.bus_comm.set_door_opener_sts(DoorOpenerSts.FullClsd)
        self.io.set_hood1_sts(sts1=HoodSts.Close)
        self.io.set_hood2_sts(sts2=HoodSts.Close)
        self.io.trigger_all_doors_outswitch(OutSwitchPressSts.NoPress)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.NFC)
        sleep(1)
        cen_lock_sts = self.bus_comm.get_central_lock_sts()
        if cen_lock_sts == 1:
            logger.info(f"当前的中控锁状态为UnLock,需要先落锁再执行后续操作")
            self.soa.hmi_set_door_close_lock(LockCmd.Lock, locksource)
            sleep(1)
            cen_lock_sts = self.bus_comm.get_central_lock_sts()
            if cen_lock_sts == 3:
                logger.info(f"当前的中控锁状态是否为Lock,闭锁成功")
            else:
                logger.info(f"当前的中控锁状态仍为UnLock,闭锁失败")
        else:
            logger.info(f"当前的中控锁状态为Lock,不需要先落锁,可以直接执行后续操作")

    def check_indicator_lamp_flash(self, indcr_sts: IndcrSts, timeout=10):
        result_ori = self.bus_comm.get_active_indicator_lamp_req_data(timeout)
        logger.info("result_original {}".format(result_ori))
        result_1 = get_signal_times_interval(result_ori, indcr_sts.value)
        logger.info("result_1(信号值为3):{}".format(result_1))
        if result_1[0] > 17 and result_1[0] < 23:
            assert True
        else:
            assert False

        result_2 = get_signal_times_interval(result_ori, 0)
        logger.info("result_2(信号值为0):{}".format(result_2))
        if result_2[0] > 17 and result_2[0] < 23:
            assert True
        else:
            assert False

    def alrm_notactive(self):
        try:
            self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        except:
            self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)

    def Armd(self):
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        
    def Actv(self):
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        
    def Disarmd(self):
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)

    def ck_no_specific_event_and_GetWarningMsgList(self, hint, info, timeout=1):
        """校验无指定warningMsgList事件,并请求WarningMsgList获取结果"""
        self.soa.ck_no_specific_event("WTIService_client", "WarningMsgList", hint, timeout=timeout)
        self.soa.send_request_and_ck_resp("WTIService_client", "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})

    def ck_WarningMsgList_and_GetWarningMsgList(self, hint, info, timeout=3):
        """校验指定warningMsgList事件,并请求WarningMsgList获取结果"""
        self.soa.ck_s2s_event("WTIService_client", "WarningMsgList",
                                  {"list": [{"name": hint, "info": str(info)}]}, timeout=timeout)
        self.soa.send_request_and_ck_resp("WTIService_client", "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})

    @allure.title("Normal Driving mode 自动紧急制动(AEB)请求信号丢失通过ReqBkp请求HWL")
    @pytest.mark.full
    def test_caseid_115136(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.pause_bus_send('backbonefr')
        sleep(1)
        self.bus_comm.set_aeb_bkp_brake_req(req=AsySftyHWLReq.TurnOn)
        for num in range(3):
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.Off)
        # 恢复
        self.bus_comm.set_aeb_bkp_brake_req(req=AsySftyHWLReq.TurnOff)
        self.bus_comm.resume_bus_send('backbonefr')
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("RELOCKING闭锁关闭前位置灯")
    @pytest.mark.full
    def test_caseid_1994368(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.set_centrllock_to_lock(locksource=LockSource.TmrAut)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("RELOCKING闭锁关闭后位置灯")
    @pytest.mark.full
    def test_caseid_1994395(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.set_centrllock_to_lock(locksource=LockSource.TmrAut)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("REMOTE_KEY闭锁关闭前位置灯")
    @pytest.mark.full
    def test_caseid_1994370(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.set_centrllock_to_lock(locksource=LockSource.RKE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("REMOTE_KEY闭锁关闭后位置灯")
    @pytest.mark.full
    def test_caseid_1994396(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.set_centrllock_to_lock(locksource=LockSource.RKE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("后位置灯激活条件_NFC解锁开启后位置灯")
    @pytest.mark.full
    def test_caseid_1994371(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.set_centrllock_to_lock(locksource=LockSource.RKE)
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("后位置灯激活条件_OUTSIDE_OTHERS闭锁后NFC解锁开启后位置灯")
    @pytest.mark.full
    def test_caseid_1994372(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.set_centrllock_to_lock(locksource=LockSource.OutsOth)
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("后位置灯激活条件_APPROACH解锁开启后位置灯")
    @pytest.mark.full
    def test_caseid_1994373(self):
        self.sd_tester.write_ccp(ccp={94:0x80})
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.set_centrllock_to_lock(locksource=LockSource.NFC)
        sleep(1)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(3)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_APPROACH解锁开启前位置灯")
    @pytest.mark.full
    def test_caseid_1994399(self):
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("后位置灯激活条件_TELEMATICS解锁开启后位置灯")
    @pytest.mark.full
    def test_caseid_1994374(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.set_centrllock_to_lock(locksource=LockSource.RKE)
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.Telm)
        sleep(3)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("后位置灯激活条件_KEYLESS_PASSIVE解锁开启后位置灯")
    @pytest.mark.full
    def test_caseid_1994375(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.set_centrllock_to_lock(locksource=LockSource.RKE)
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.KV_PEPS)
        sleep(3)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_KEYLESS_PASSIVE解锁开启前位置灯")
    @pytest.mark.full
    def test_caseid_1994401(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL,usage_mode=UsageMode.INACTIVE)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.set_centrllock_to_lock(locksource=LockSource.RKE)
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.KV_PEPS)
        sleep(3)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_NFC解锁开启前位置灯")
    @pytest.mark.full
    def test_caseid_1994397(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.set_centrllock_to_lock(locksource=LockSource.RKE)
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_OUTSIDE_OTHERS闭锁后NFC解锁开启前位置灯")
    @pytest.mark.full
    def test_caseid_1994398(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.set_centrllock_to_lock(locksource=LockSource.OutsOth)
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_REMOTE_KEY解锁开启前位置灯_Normal Abandoned mode")
    @pytest.mark.full
    def test_caseid_1994404(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL,usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock(locksource=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.RKE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_TELEMATICS解锁开启前位置灯")
    @pytest.mark.full
    def test_caseid_1994400(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.set_centrllock_to_lock(locksource=LockSource.RKE)
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.Telm)
        sleep(3)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("当StsOfLedReLampRi == 0x02时，不影响倒车灯")
    @pytest.mark.full
    @pytest.mark.new_beam
    def test_caseid_1990191(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={508:3,259:2})
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Rvs)
        sleep(.25)
        self.bus_comm.set_reverse_lamp_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.Error)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)
        # 恢复
        self.bus_comm.set_reverse_lamp_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.On)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Undefd)

    @allure.title("后位置灯激活条件_REMOTE_KEY解锁开启后位置灯_Normal Abandoned mode")
    @pytest.mark.full
    def test_caseid_1994378(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL,usage_mode=UsageMode.ABANDONED)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.set_centrllock_to_lock(locksource=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.RKE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("位置灯故障提示信息_GetTelltaleList")
    @pytest.mark.full
    def test_caseid_1982694(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Front,pos=GeneralPos.All,sts=PosnLampSts.Error)
        self.soa.event_check_and_get_hv_batt_thermy_sts(sts=HvBattThermReq.Cooling,info="PO Failure")
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Front,pos=GeneralPos.All,sts=PosnLampSts.On)
        self.soa.event_check_and_get_hv_batt_thermy_sts(sts=HvBattThermReq.Idle,info="PO Failure")

    @allure.title("倒车灯故障提示信息GetTelltaleList")
    @pytest.mark.full
    def test_caseid_1982723(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Rvs)
        sleep(.25)
        self.bus_comm.set_reverse_lamp_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.Error)
        self.soa.event_check_and_get_hv_batt_thermy_sts(sts=HvBattThermReq.Cooling,info="Reverse Light Failure")
        sleep(2)
        self.bus_comm.set_reverse_lamp_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.On)
        self.soa.event_check_and_get_hv_batt_thermy_sts(sts=HvBattThermReq.Idle,info="Reverse Light Failure")

    @allure.title("右转向灯故障提示信息GetTelltaleList")
    @pytest.mark.fully
    def test_caseid_1982722(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=PosnLampSts.Error)
        self.soa.event_check_and_get_hv_batt_thermy_sts(sts=HvBattThermReq.Cooling,info="Right TI Failure")
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=PosnLampSts.On)
        self.soa.event_check_and_get_hv_batt_thermy_sts(sts=HvBattThermReq.Idle,info="Right TI Failure")

    @allure.title("后雾灯故障提示信息_GetTelltaleList")
    @pytest.mark.full
    def test_caseid_1982717(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.set_rear_fog_fault_sts(pos=GeneralPos.Left,sts=ExtrLtgSts.Err)
        self.soa.event_check_and_get_hv_batt_thermy_sts(sts=HvBattThermReq.Cooling,info="Rear Fog Failure")
        self.bus_comm.set_rear_fog_fault_sts(pos=GeneralPos.Left,sts=ExtrLtgSts.On)
        self.soa.event_check_and_get_hv_batt_thermy_sts(sts=HvBattThermReq.Idle,info="Rear Fog Failure")
        
    @allure.title("大灯高度调节电机故障信息")
    @pytest.mark.full
    def test_caseid_1982720(self):
        hint = "Leveling Motor"
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_ahl_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.Error)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        self.bus_comm.set_ahl_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.On)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @allure.title("左转向灯故障提示信息GetTelltaleList")
    @pytest.mark.full
    def test_caseid_1982721(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=PosnLampSts.Error)
        self.soa.event_check_and_get_hv_batt_thermy_sts(sts=HvBattThermReq.Cooling,info="Left TI Failure")
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=PosnLampSts.On)
        self.soa.event_check_and_get_hv_batt_thermy_sts(sts=HvBattThermReq.Idle,info="Left TI Failure")

    @allure.title("超车灯故障提示信息_GetTelltaleList")
    @pytest.mark.full
    def test_caseid_1982706(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.Error)
        self.soa.event_check_and_get_hv_batt_thermy_sts(sts=HvBattThermReq.Cooling,info="Overtake Light Failure")
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.On)
        self.soa.event_check_and_get_hv_batt_thermy_sts(sts=HvBattThermReq.Idle,info="Overtake Light Failure")

    @allure.title("近光灯故障提示信息_GetTelltaleList")
    @pytest.mark.full
    def test_caseid_1982610(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.Error)
        self.soa.event_check_and_get_hv_batt_thermy_sts(sts=HvBattThermReq.Cooling,info="LB Failure")
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.On)
        self.soa.event_check_and_get_hv_batt_thermy_sts(sts=HvBattThermReq.Idle,info="LB Failure")

    @allure.title("远光灯故障提示信息_GetTelltaleList")
    @pytest.mark.full
    def test_caseid_1982594(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.Error)
        self.soa.event_check_and_get_hv_batt_thermy_sts(sts=HvBattThermReq.Cooling,info="HB Failure")
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.On)
        self.soa.event_check_and_get_hv_batt_thermy_sts(sts=HvBattThermReq.Idle,info="HB Failure")

    # @allure.title("前位置灯激活条件_REMOTE_KEY解锁开启前位置灯_Crash Abandoned mode")
    # @pytest.mark.full
    # def test_caseid_1994402(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.ABANDONED)
    #     self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
    #     self.set_centrllock_to_lock(locksource=LockSource.RKE)
    #     sleep(1)
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.RKE)
    #     self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
    #     sleep(3)
    #     self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
    
    # @allure.title("前位置灯激活条件_REMOTE_KEY解锁开启前位置灯_Factory Inactive mode")
    # @pytest.mark.full
    # def test_caseid_1994403(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.FACTORY,usage_mode=UsageMode.INACTIVE)
    #     self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
    #     self.set_centrllock_to_lock(locksource=LockSource.NFC)
    #     sleep(1)
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.RKE)
    #     self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
    #     sleep(3)
    #     self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    # @allure.title("后位置灯激活条件_REMOTE_KEY解锁开启后位置灯_Crash Abandoned mode")
    # @pytest.mark.full
    # @pytest.mark.full1
    # def test_caseid_1994376(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.ABANDONED)
    #     self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
    #     self.set_centrllock_to_lock(locksource=LockSource.NFC)
    #     sleep(1)
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.RKE)
    #     self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
    #     sleep(3)
    #     self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    # @allure.title("后位置灯激活条件_REMOTE_KEY解锁开启后位置灯_Factory Inactive mode")
    # @pytest.mark.full
    # @pytest.mark.full1
    # def test_caseid_1994377(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.FACTORY,usage_mode=UsageMode.INACTIVE)
    #     self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
    #     self.set_centrllock_to_lock(locksource=LockSource.NFC)
    #     sleep(1)
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.RKE)
    #     sleep(3)
    #     self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)