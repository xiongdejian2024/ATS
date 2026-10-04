#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_tailgate_ctrl.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/21 11:30
@Description: BGM车控车设尾门功能
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
@allure.story("尾门功能")
class TestTailGateCtrl(TestABCBase):
    def before_class(self, ecu):
        # logger.info("------------------>复位BGM")
        # self.io.bgm_power_off()
        # sleep(2)
        # self.io.bgm_power_on()
        # time.sleep(15)
        # logger.info("------------------>复位BGM结束")
        self.soa.update([
                        "TailGateService_client", 
                        "CentralLockService_client", 
                        "KeyService_client",
                        "VehicleModeService_client",
                        "VehicleSetStatusService_client",
                        "ChassisService_client",
                        "WTIService_client",

        ])
        sleep(2)

    def before_each_func(self, ecu):  
        self.sd_tester.write_ccp(ccp={211: 0x01, 564: 0x2, 94: 0x80, 142:0x83,98: 0x2, 97: 0x2, 98: 0x2})
        self.io.set_five_door_sts(Door.close)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2)
        self.check_and_trun_off_lamp_sts()
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        sleep(1)


    def after_each_func(self, ecu):
        self.sd_tester.send_request_and_recv_response([0x22, 0x70, 0X22])
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(3) 
    
    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        
    def check_and_trun_off_lamp_sts(self):
        # 检查双闪是否已经打开，如果打开先关闭
        ori_data = self.bus_comm.ipdu.check_signal(self.bus_comm.ipdu.bodycan.CemBodyFr03, 'ActvnOfIndcrIndcrOut', 3)
        check_result = check_signal_value_exist(ori_data, 3)
        if check_result:
            sleep(3)
            self.io.hazard_light_open()
            self.io.hazard_light_close()
            sleep(3)
            self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        else:
            check_result = check_signal_value_exist(ori_data, 1) or check_signal_value_exist(ori_data, 2)
            if check_result:
                self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
                sleep(6)

    def control_tailgate_by_rke(self,action:TailGateCmd):
        if action.name == "Open":
            self.bus_comm.dk.send_rke_tailgate_control(op=1,position=0)
            self.bus_comm.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
            self.bus_comm.dk.set_door_opener_sts(1, 1, 1, 1, 2)
            sleep(3)
            self.io.set_door(Trunk=Door.open)
            self.bus_comm.dk.set_door_opener_sts(1, 1, 1, 1, 4)
            sleep(2)
            self.bus_comm.dk.ck_rke_resp(4, 0, "Success", exec_type=3)
        elif action.name == "Close":
            self.bus_comm.dk.send_rke_tailgate_control(-1)
            self.bus_comm.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
            self.bus_comm.dk.ck_door_opener_cmd(5, 2, 6)
            self.bus_comm.dk.set_door_opener_sts(1, 1, 1, 1, 6)
            sleep(3)
            self.io.set_door(Trunk=Door.close)
            self.bus_comm.dk.set_door_opener_sts(1, 1, 1, 1, 1)
            sleep(2)
            self.bus_comm.dk.ck_rke_resp(4, 0, "Success", exec_type=3)


    def set_common_precondition_for_tailgate(self,car_mode:CarMode = CarMode.NORMAL,usage_mode:UsageMode = UsageMode.INACTIVE,vehmtnst:VehMtnSts = VehMtnSts.StandStillVal3,ccp:dict = {97: 0x02, 98: 0x20,94: 0x80},
                                             lock_type:LockCmd = LockCmd.UnLock,ctrl_type:LockSource = LockSource.NFC,wash_mode:isOn = isOn.Off,gear:Gear = Gear.Park,tr_opener:DoorOpenerSts = DoorOpenerSts.FullClsd):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.soa.hmi_set_wash_mode(sts=wash_mode)
        self.mix.set_common_precontion(car_mode = car_mode, usage_mode = usage_mode, vehmtnst = vehmtnst, ccp = ccp)   
        self.bus_comm.set_vehspd_gear(gear=gear)
        self.mix.ctrl_lock(lock_type=lock_type, ctrl_type=ctrl_type)     
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=tr_opener)   



    @allure.title("463005_v16_尾门释放_FACTORY&ABANDONED下释放背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110215(self):
        self.mix.set_common_precontion(CarMode.FACTORY)
        self.mix.set_common_precontion(UsageMode.ABANDONED)

        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
    
    @allure.title("463005_v16_尾门释放_Crash&ACTIVE下释放背门")
    @pytest.mark.full
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_110309(self):
        self.mix.set_common_precontion(UsageMode.ACTIVE, CarMode.CRASH)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        self.io.hazard_light_open()
        sleep(.1)
        self.io.hazard_light_close() 
        sleep(.2)

    @allure.title("463005_v16_尾门释放_Crash&Abdoned下释放背门")
    @pytest.mark.full
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_115493(self):
        self.mix.set_common_precontion(UsageMode.ABANDONED, CarMode.CRASH)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

        self.io.hazard_light_open()
        sleep(.1)
        self.io.hazard_light_close() 
        sleep(.2)

    @allure.title("463005_v16_尾门释放_Crash&Driving下释放背门")
    @pytest.mark.full
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_110244(self):
        self.mix.set_common_precontion(UsageMode.DRIVING, CarMode.CRASH)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        self.io.hazard_light_open()
        sleep(.1)
        self.io.hazard_light_close() 
        sleep(.2)        

    @allure.title("466314_v19_通过HMI开启尾门解锁_HMI闭锁开尾门")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110335(self):
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open)

    @allure.title("463005_v16_尾门释放_Crash&INactive下释放背门")
    @pytest.mark.sanity
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_110256(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE, CarMode.CRASH)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        self.io.hazard_light_open()
        sleep(.1)
        self.io.hazard_light_close() 
        sleep(.2)

    @allure.title("463005_v16_尾门释放_Dyno&abdonded下释放背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110232(self):
        self.mix.set_common_precontion(UsageMode.ABANDONED, CarMode.DYNO)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

    @allure.title("463005_v16_尾门释放_Dyno&ACTIVE下释放背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110254(self):
        self.mix.set_common_precontion(UsageMode.ACTIVE, CarMode.DYNO)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

    @allure.title("463005_v16_尾门释放_Dyno&Convenience下释放背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110280(self):
        self.mix.set_common_precontion(UsageMode.CONVENIENCE, CarMode.DYNO)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

    @allure.title("466314_v19_通过HMI开启尾门解锁_车辆非静止开尾门请求忽略")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110209(self):
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1) 
        self.bus_comm.set_vehmtn(VehMtnSts.FwdVal1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)

    @allure.title("463005_v16_尾门释放_Dyno&Driving下释放背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110272(self):
        self.mix.set_common_precontion(UsageMode.DRIVING, CarMode.DYNO)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

    @allure.title("463005_v16_尾门释放_CCP98不满足配置不释放背门")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110243(self):
        self.sd_tester.write_ccp(ccp={98: 0x01})
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)


    @allure.title("463005_v16_尾门释放_CCP97不满足配置不释放背门")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110233(self):
        self.sd_tester.write_ccp(ccp={97: 0x01})
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

    @allure.title("463005_v16_尾门释放_Fctory&Inactive下释放背门")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110267(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE, CarMode.FACTORY)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

    @allure.title("463005_v16_尾门释放_Fctory&Driving下释放背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110242(self):
        self.mix.set_common_precontion(UsageMode.DRIVING, CarMode.FACTORY)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

    @allure.title("463005_v16_尾门释放_Normal&Abandoned下释放背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110265(self):
        self.mix.set_common_precontion(UsageMode.ABANDONED, CarMode.NORMAL)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

    @allure.title("463005_v16_尾门释放_Fctory&convenience下释放背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_115494(self):
        self.mix.set_common_precontion(UsageMode.ABANDONED, CarMode.NORMAL)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

    @allure.title("463005_v16_尾门释放_关闭尾门电释放请求不发送")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110182(self):
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

    @allure.title("463005_v16_尾门释放_Dyno&Inavtive下释放背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110226(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE, CarMode.DYNO)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

    @allure.title("463005_v16_尾门释放_FACTORY&ACTIVE下释放背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110266(self):
        self.mix.set_common_precontion(UsageMode.ACTIVE, CarMode.FACTORY)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
    
    @allure.title("463005 v16_尾门释放_Nomal&Active下释放背门")
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_110238(self):
        self.mix.set_common_precontion(UsageMode.ACTIVE)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

    @allure.title("463005 v16_尾门释放_TRANSPORT背门不释放")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110287(self):
        self.mix.set_common_precontion(CarMode.TRANSPORT)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

    @allure.title("463005 v16_尾门释放_Nomal&Convenience下释放背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110189(self):
        self.mix.set_common_precontion(UsageMode.CONVENIENCE,CarMode.NORMAL)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

    @allure.title("463005 v16_尾门释放_Nomal&Driving下释放背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_111345(self):
        self.mix.set_common_precontion(UsageMode.DRIVING,CarMode.NORMAL)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

    @allure.title("463005 v16_尾门释放_Nomal&Inactive下释放背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110195(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE,CarMode.NORMAL)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

    @allure.title("463005_v16_尾门释放_Crash&Conveience下释放背门")
    @pytest.mark.sanity
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_110202(self):
        self.mix.set_common_precontion(UsageMode.ABANDONED, CarMode.CRASH)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        self.io.hazard_light_open()
        sleep(.1)
        self.io.hazard_light_close() 
        sleep(.2)

    @allure.title("466328 v11_尾门开关关闭和锁定_T_中控锁Unlock状态&&P档_底部开关关闭尾门")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110322(self):
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1) 
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 0)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        sleep(1)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 2)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr08", "TrLockSts", 1)

    @allure.title("466328 v11_尾门开关关闭和锁定_中控锁Unlock状态&&N档_底部开关关闭尾门")
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_110297(self):
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1) 
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 2)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        sleep(2)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 2)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr08", "TrLockSts", 1)

    @allure.title("466328 v11_尾门开关关闭和锁定_D档底部开关关闭尾门请求忽略")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110241(self):
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1) 
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 3)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        sleep(1)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 0)


    @allure.title("466328 v11_尾门开关关闭和锁定_内锁TrUnlock-Lock")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110229(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(3)  # 等待NVM存储
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.io.set_door(Trunk=Door.close)
        sleep(1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("466328 v11_尾门开关关闭和锁定_外部闭锁TrUnlock未搜到有效钥匙中控闭锁")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110188(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(3)  # 等待NVM存储
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x9)])
        sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("466328 v11_尾门开关关闭和锁定_远控闭锁钥匙在车外_TrUnlock-Lockd")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110192(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.Telm)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(3)  # 等待NVM存储
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])
        sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)

    @allure.title("466328 v11_尾门开关关闭和锁定_外部闭锁钥匙在车外LeftFnd_TrUnlock-Lock")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110269(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(3)  # 等待NVM存储
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x3)])
        sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("466328 v11_尾门开关关闭和锁定_车辆非静止尾门请求忽略")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110216(self):
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1) 
        self.bus_comm.set_vehmtn(VehMtnSts.FwdVal1)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        sleep(1)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 0)

    @allure.title("466328 v11_尾门开关关闭和锁定_外部闭锁钥匙在RightFnd_TrUnlock-Lock")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110251(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(3)  # 等待NVM存储
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x4)])
        sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("466328 v11_尾门开关关闭和锁定_外部闭锁钥匙在RearFnd_TrUnlock-Lock")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110211(self):
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(3)  # 等待NVM存储
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)

    @allure.title("466328 v11_尾门开关关闭和锁定_外部闭锁钥匙在车外区域_Trunlock-Lock")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110178(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(3)  # 等待NVM存储
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])
        sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)


    @allure.title("466328 v11_尾门开关关闭和锁定_TrUnlock服务关尾门整车Lock")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110228(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(3)  # 等待NVM存储
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.io.set_door(Trunk=Door.close)
        sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("466328 v11_尾门开关关闭和锁定_Crash&Inactive下关闭背门")
    @pytest.mark.full
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_110323(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE, CarMode.CRASH)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1) 
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        sleep(1)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 2)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 0)
        self.io.hazard_light_open()
        sleep(.1)
        self.io.hazard_light_close() 
        sleep(.2)

    @allure.title("466328 v11_尾门开关关闭和锁定_Dyno&Abandoned下关闭背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110187(self):
        self.mix.set_common_precontion(UsageMode.ABANDONED, CarMode.DYNO)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1) 
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        sleep(1)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 2)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 0)

    @allure.title("466328 v11_尾门开关关闭和锁定_NORMAL&Inactive下关闭背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110290(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1) 
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        sleep(1)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 2)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 0)

    @allure.title("466328 v11_尾门开关关闭和锁定_NORMAL&Drving下关闭背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110246(self):
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1) 
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        sleep(1)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 2)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 0)

    @allure.title("466328 v11_尾门开关关闭和锁定_Normal&Convenience下关闭背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110213(self):
        self.mix.set_common_precontion(UsageMode.CONVENIENCE)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1) 
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        sleep(1)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 2)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 0)

    @allure.title("466328 v11_尾门开关关闭和锁定_Normal&Active下关闭背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110222(self):
        self.mix.set_common_precontion(UsageMode.ACTIVE)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1) 
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        sleep(1)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 2)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 0)

    @allure.title("466328 v11_尾门开关关闭和锁定_Normal&Abandoned下关闭背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110308(self):
        self.mix.set_common_precontion(UsageMode.ABANDONED)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1) 
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        sleep(1)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 2)

    @allure.title("466328 v11_尾门开关关闭和锁定_INACTIVE&FACTORY下关闭背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_111340(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE, CarMode.FACTORY)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1) 
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        sleep(1)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 2)

    @allure.title("466328 v11_尾门开关关闭和锁定_CONVENIENCE&FACTORY下关闭背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110295(self):
        self.mix.set_common_precontion(UsageMode.CONVENIENCE, CarMode.FACTORY)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1) 
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        sleep(1)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 2)

    @allure.title("466328 v11_尾门开关关闭和锁定_ACTIVE&FACTORY下关闭背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110176(self):
        self.mix.set_common_precontion(UsageMode.ACTIVE, CarMode.FACTORY)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1) 
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        sleep(1)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 2)

    @allure.title("466328 v11_尾门开关关闭和锁定_ABANDONED&FACTORY下关闭背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110190(self):
        self.mix.set_common_precontion(CarMode.FACTORY, UsageMode.ABANDONED)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1) 
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        sleep(1)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 2)

    @allure.title("466328 v11_尾门开关关闭和锁定_R档开启尾门请求忽略")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110294(self):
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 1)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1) 
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        sleep(1)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 0)

    @allure.title("466328 v11_尾门开关关闭和锁定_Dyno&Driving下关闭背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110268(self):
        self.mix.set_common_precontion(UsageMode.DRIVING,CarMode.DYNO)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1) 
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        sleep(1)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 2)

    @allure.title("507789 通过HMI开启尾门到目标位置_尾门开启100%")
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_115492(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 2)
        sleep(1)
        self.soa.hmi_set_tailgate_postion(pos=100)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 3)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 4)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 100)
        sleep(.2)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 101)

    @allure.title("507789 通过HMI开启尾门到目标位置_MovgDwn-尾门开启20°")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110302(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 6)
        sleep(1)
        self.soa.hmi_set_tailgate_postion(pos=20)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 3)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 20)
        sleep(.2)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 101)

    @allure.title("507789 通过HMI开启尾门到目标位置_MovgUpBrkg-尾门开启10°")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110201(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 3)
        sleep(1)
        self.soa.hmi_set_tailgate_postion(pos=10)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 3)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 4)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 10)
        sleep(.2)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 101)

    @allure.title("507789 通过HMI开启尾门到目标位置_MovgDwnBrkg-尾门开启50°")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_111329(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 7)
        sleep(1)
        self.soa.hmi_set_tailgate_postion(pos=50)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 3)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 5)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 50)
        sleep(.2)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 101)

    @allure.title("507789 通过HMI开启尾门到目标位置_MovgDwnBrkg-尾门开启10°")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_118775(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 8)
        self.soa.hmi_set_tailgate_postion(pos=10)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 10)
        sleep(.2)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 101)

    @allure.title("507789 通过HMI开启尾门到目标位置_HalfClsd-尾门开启10°")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110321(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 9)
        self.soa.hmi_set_tailgate_postion(pos=10)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 10)
        sleep(.2)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 101)

    @allure.title("507789 通过HMI开启尾门到目标位置_StopMinPntForCls-尾门开启10°")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110230(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 10)
        self.soa.hmi_set_tailgate_postion(pos=10)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 10)
        sleep(.2)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 101)

    @allure.title("507789 通过HMI开启尾门到目标位置_目标位置等于9")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110274(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 9)
        self.soa.hmi_set_tailgate_postion(pos=9)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 9)
        sleep(.2)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 101)

    @allure.title("507789 通过HMI开启尾门到目标位置_实际位置<目标位置电释放请求On")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110223(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr03", "TrOpenPosn", 9)
        sleep(.5)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 10)
        self.soa.hmi_set_tailgate_postion(pos=10)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 10)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.2)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 101)

    @allure.title("507789 通过HMI开启尾门到目标位置_实际位置>目标位置电释放请求OFF")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110299(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr03", "TrOpenPosn", 10)
        sleep(.5)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 10)
        self.soa.hmi_set_tailgate_postion(pos=9)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 9)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        # self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)  # 发1是Bug
        sleep(.2)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 101)

    @allure.title("495067 v1 HMI关闭尾门_NFC闭锁TrUnlock_尾门关闭整车落锁")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_111349(self):
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(3)  # 等待NVM存储
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.io.set_door(Trunk=Door.close)
        sleep(1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)

    @allure.title("499022 v7 整车落锁过手动关闭后尾箱_解锁状态硬线关闭尾门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110258(self):
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr25", "TrSts", 2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("499022 v7手动关闭后背门上锁_内部上锁有关门请求发出整车落锁")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110332(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(3)  # 等待NVM存储
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.io.set_door(Trunk=Door.close)
        sleep(1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("499022 v7手动关闭后背门上锁_离车落锁硬线关尾门钥匙未遗留_中控落锁")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110217(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(.2)  # 等待配置生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(3)  # 等待NVM存储
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0xB)])
        sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)

    @allure.title("499022 v7手动关闭后背门上锁_Telm闭锁Trunlock_钥匙未遗留车内中控Lockd")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110316(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.Telm)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(3)  # 等待NVM存储
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x1)])
        sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)

    @allure.title("504063 远控打开尾门_尾门翘起15°")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_118776(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 1)
        sleep(.5)
        self.soa.hmi_set_tailgate_postion(pos=15)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 15)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)
        sleep(.2)  # 发送6帧在0.23s恢复默认值
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 101)

    @allure.title("504063 v3 远程打开背门_Trunlock远控重新关闭尾门无钥匙连接尾门外开关禁用")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110289(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.Telm)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(3)  # 等待NVM存储
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0xB)])
        sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.5)
        # self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open)  # 发Open是Bug
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)

    @allure.title("504063 v3 远程打开背门_Trunluck_无钥匙连接外开关不禁用")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110333(self):
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.5)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open)
        sleep(.9)  # 1s恢复默认值
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)

    @allure.title("466314 v9 HMI解锁开启后背门_中控解锁尾门开启")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110293(self):
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 6)
        sleep(.9)  # 1s恢复默认值
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)

    @allure.title("478910 v5 HMI暂停后背门_MovgUp状态暂停后背门")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110327(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 2)
        sleep(.5)  # 等待信号生效
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 6)
        sleep(.2)  # 200ms恢复默认值
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)

    @allure.title("478910 v5 HMI暂停后背门_MovgUp状态暂停后背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110181(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 6)
        sleep(.5)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 6)
        sleep(.2)  # 200ms恢复默认值
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)

    @allure.title("478910 v5 HMI暂停后背门_MovgUpBrkg状态暂停后背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110310(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 3)
        sleep(.5)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 6)
        sleep(.2)  # 200ms恢复默认值
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)

    @allure.title("478910 v5 HMI暂停后背门_MovgDownBrkg状态暂停后背门")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110199(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 7)
        sleep(.5)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 6)
        sleep(.2)  # 200ms恢复默认值
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)

    @allure.title("478910 v5 HMI暂停后背门_尾门非Moving状态Stop请求忽略")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110270(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 1)
        sleep(.5)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)
        # self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)  # 发stop是Bug
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)
        sleep(.2)  # 200ms恢复默认值
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)

    @allure.title("478910 v5 HMI暂停后背门_车辆非静止Stop请求忽略")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110200(self):
        self.bus_comm.set_vehmtn(VehMtnSts.FwdVal1)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 2)
        sleep(.5)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)
        # self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)  # 发stop是Bug
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)
        sleep(.2)  # 200ms恢复默认值
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)

    @allure.title("466321 v10_外部开关暂停尾门和行李箱_尾门开启过程中外开关按下暂停尾门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110284(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 3)
        sleep(.5)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.02)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)  # 暂停和开关被按下信号几乎同时触发
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 4)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 0)

    @allure.title("466321 v10_外部开关暂停尾门和行李箱_尾门MovgDwn外开关按下暂停尾门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110177(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 6)
        sleep(.5)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.02)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)  # 暂停和开关被按下信号几乎同时触发
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 4)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 0)

    @allure.title("466321 v10_外部开关暂停尾门和行李箱_尾门MovgDwn外开关按下暂停尾门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110249(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 7)
        sleep(.5)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.02)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)  # 暂停和开关被按下信号几乎同时触发
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 4)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 0)

    @allure.title("478448 v8 底部开关暂停后背门_尾门MovgUpBrkg底部开关按下暂停尾门")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110253(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 3)
        sleep(.5)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 5)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 0)

    @allure.title("478448 v8 底部开关暂停后背门_尾门MovgUp底部开关按下暂停尾门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110278(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 2)
        sleep(.5)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 5)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 0)

    @allure.title("478448 v8 底部开关暂停后背门_尾门MovgDwn底部开关按下暂停尾门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110250(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 6)
        sleep(.5)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 5)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 0)

    @allure.title("478448 v8 底部开关暂停后背门_尾门MovgDwnBrkg底部开关按下暂停尾门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110313(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 7)
        sleep(.5)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 5)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 0)

    @allure.title("478448 v8 底部开关暂停后背门_尾门非运动状态FullClsd不发Stop")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110220(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 1)
        sleep(.5)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)

    @allure.title("478448 v8 底部开关暂停后背门_尾门非运动状态StopDurgOpen不发Stop")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110203(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 4)
        sleep(.5)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)

    @allure.title("478448 v8 底部开关暂停后背门_车辆非静止底部开关请求忽略")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110282(self):
        self.bus_comm.set_vehmtn(VehMtnSts.FwdVal1)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 2)
        sleep(.5)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)

    @allure.title("459912 v5_接收端通信安全机制_车辆非静止尾门电释放请求TrRelsReq-OFF（1:StandStillVal1）")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110252(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal1)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        # self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)  # 发1是Bug
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

    @allure.title("459912 v5_接收端通信安全机制_车辆非静止尾门电释放请求TrRelsReq-OFF（1:StandStillVal1）")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110334(self):
        self.bus_comm.set_vehmtn(VehMtnSts.BackwVal2)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        # self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)  # 发1是Bug
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        sleep(.4)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)


    @allure.title("497516 v24 控制电动尾门和后尾箱_车辆静止控制尾门")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110261(self):
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 6)
        sleep(.9)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)

    # @allure.title("497516 v24 控制电动尾门和后尾箱_车辆静止控制尾门关闭")
    # @pytest.mark.update
    # @pytest.mark.full
    # def test_tailgate_ctrl_caseid_110292(self):
    #     self.io.set_door(Trunk=Door.open)
    #     self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 2)
    #     sleep(.2)  # 等前置条件生效
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
    #     self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Close)
    #     self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 6)
    #     sleep(.9)
    #     self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
    #     self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)

    @allure.title("497516 v24 控制电动尾门和后尾箱_底部开关暂停后背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110237(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 2)
        sleep(.5)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 5)
        sleep(.2)  # 200ms恢复默认值
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)

    @allure.title("497516 v24 控制电动尾门和后尾箱_车辆静止控制尾门")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110325(self):
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 1)
        sleep(.5)  # 等待前置条件生效
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        # self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open)  # 发open是Bug
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)

    @allure.title("526239 v19 开启尾门和后尾箱_非P 档 OR N档尾门开启请求忽略")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110221(self):
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 3)
        sleep(.5)  # 等待前置条件生效
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        # self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open)  # 发open是Bug
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)

    @allure.title("497516 v24 控制电动尾门和行李箱_Trnsp尾门开启禁用")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110248(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY)
        sleep(.5)  # 等待前置条件生效
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        # self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open)  # 发Open是Bug
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)


    @allure.title("476627 v7 控制动力侧门特殊case_TrOpenerSts=HalfClsd]服务开启尾门")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110276(self):
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.HalfClsd)
        sleep(.2)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 6)
        sleep(.9)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 0)

    @allure.title("497517 v6 后背门开启过程中中断_外部开关中断")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110257(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 2)
        sleep(.5)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.02)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)  
        sleep(.2)  # 200ms恢复默认值
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 0)

    @allure.title("497517 v6 后背门开启过程中中断_HMI中断后背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110303(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 3)
        # self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 1)  # 非运动状态，不发stop
        sleep(.5)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)
        sleep(.2)  # 200ms恢复默认值
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 0)

    @allure.title("497517 v6 背门打开期间被打断_底部开关ShutFace暂停")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110240(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 2)
        sleep(.5)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 5)
        sleep(.2)  # 200ms恢复默认值
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 0)

    @allure.title("497517 v6 后背门开启过程中中断_HMI中断尾门后再开启")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110312(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 3)
        sleep(.5)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)
        sleep(.2)  # 200ms恢复默认值
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 4)
        sleep(.3)  # 等待信号生效
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open)
        sleep(.9)  # 1000ms恢复默认值
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        
    @allure.title("449494 v18 外开关解锁开启尾门_中央闭锁状态&&有有效钥匙")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110330(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open)  # 发送开启尾门请求
        sleep(3)# 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("449494 v18 外开关解锁开启尾门_中央解锁尾门外开关开启尾门")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110263(self):
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.2)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open)  # 发送开启尾门请求
        sleep(.4)  # TrRelsReq 500ms恢复默认值
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        sleep(.5)  # openerreq 开启关闭1s恢复默认值
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)  

    @allure.title("476629 v3 后背门关闭过程中中断_HMI中断后背门")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110191(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 6)
        sleep(.5)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)
        sleep(.2)  # 200ms恢复默认值
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 0)

    @allure.title("476629 v3 后背门关闭过程中中断_外部开关中断后背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110285(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 7)
        sleep(.5)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.02)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)  
        sleep(.2)  # 200ms恢复默认值
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 0)

    @allure.title("476629 v3 后背门关闭过程中中断_底部开关ShutFace暂停")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110283(self):
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 6)
        sleep(.5)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 5)
        sleep(.2)  # 200ms恢复默认值
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 0)

    @allure.title("476629 v3 后背门关闭过程中中断_远控关闭尾门移动过程中底部开关暂停")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110218(self):
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.3)  # 等待前置条件生效
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Close)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 6)
        sleep(.2)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 5)
        sleep(.2)  # 200ms恢复默认值
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 0)

    @allure.title("466520 v12 后背门释放功能安全_Active&&StandStill==Ukwn电释放请求不发TrRelsReq-OFF")
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_110273(self):
        self.mix.set_common_precontion(UsageMode.ACTIVE)
        self.bus_comm.set_vehmtn(VehMtnSts.Ukwn)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_tailgate_without_opener_rels()

    @allure.title("466520 v12 后背门释放功能安全_Active&&StandStill==Ukwn电释放请求不发TrRelsReq-OFF")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110291(self):
        self.bus_comm.set_vehmtn(VehMtnSts.FwdVal1)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_tailgate_without_opener_rels()

    @allure.title("466520 v12 后背门释放功能安全_Active&&StandStill==Ukwn电释放请求不发TrRelsReq-OFF")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110319(self):
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)  # 500ms恢复默认值
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

    @allure.title("466520 v12 后背门释放功能安全_Covenience&&StandStill==Ukwn电释放请求不发TrRelsReq-OFF")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_111387(self):
        self.mix.set_common_precontion(UsageMode.CONVENIENCE)
        self.bus_comm.set_vehmtn(VehMtnSts.Ukwn)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        # self.bus_comm.check_tailgate_without_opener_rels(
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)  # 500ms恢复默认值
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)

    @allure.title("466520 v12 后背门释放功能安全_Inactive车辆非静止电释放请求不发TrRelsReq-OFF")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110224(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.set_vehmtn(VehMtnSts.BackwVal2)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_tailgate_without_opener_rels()

    @allure.title("466520 v12 后背门释放功能安全_无尾门开启请求不发电释放TrRelsReq-OFF")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110234(self):
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.bus_comm.check_tailgate_without_opener_rels()

    @allure.title("466520 v12 后背门释放功能安全_Drving模式&&车辆静止_尾门电释放请求On")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110331(self):
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        # self.bus_comm.check_tailgate_without_opener_rels()
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(.4)  # 500ms恢复默认值
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        
    @allure.title("466520 v12 后背门释放功能安全_Covenience&&StandStill==Ukwn电释放请求不发TrRelsReq-OFF")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_111387(self):
        self.mix.set_common_precontion(UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.Ukwn)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        
    # @allure.title("466520 v12 后背门释放功能安全_Drving模式&&车辆静止_尾门电释放请求On")
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_110331(self):
    #     self.mix.set_common_precontion(UsageMode.DRIVING,vehmtnst=VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
    #     sleep(.5)
    #     self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        
    # @allure.title("466520 v12 后背门释放功能安全_前置条件满足_开启尾门电释放TrRelsReq-On")
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_110319(self):
    #     self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)

    @allure.title("494881 v24 基于尾门和后备箱的KV解锁_中控上锁尾门外部开关解锁-无有效钥匙不解锁")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1985925(self):
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3,ccp={94: 0x02})
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.get_central_lock_sts(3)
        # self.bus_comm.set_singal("backbonefr", "CemBackBoneFr38", "TrHndlOutdOpenSts", 1)
        sleep(0.5)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1) 
        self.bus_comm.reset_bncm_digital_keyinfo()
        self.bus_comm.get_central_lock_sts(3)

    # @allure.title("497516 v24 控制电动尾门和后尾箱_底部开关暂停后背门")
    # @pytest.mark.full
    # def test_tailgate_ctrl_caseid_110237(self):
    #     self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)
    #     self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 1)
    #     self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 3)
    #     sleep(.2)
    #     self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrigSrc", 5)
        
    # @allure.title("466520 v12 后背门释放功能安全_Inactive车辆非静止电释放请求不发TrRelsReq-OFF")
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_110224(self):
    #     self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        
    # @allure.title("476629 v3 后背门关闭过程中中断_远控关闭尾门移动过程中底部开关暂停")
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_110218(self):
    #     self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        
    # @allure.title("497517 v6 后背门开启过程中中断_底部按钮开启尾门运行过程中蓝牙暂停尾门")
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_110212(self):
    #     self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
    #     self.bus_comm.set_singal("backbonefr", "CemBackBoneFr06", "LockgCenStsLockSt", 3)
    #     self.bus_comm.set_singal("bodycan", "CemBackBoneFr38", "TrHndlOutdOpenSts", 1)
    #     self.bus_comm.set_singal("bodycan", "CemBackBoneFr38", "TrHndlOutdOpenSts", 1)

    @allure.title("466322 v10 尾门学习_Active模式长按尾门ProgmReq=On")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110179(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        self.bus_comm.check_tailgate_upper_req(req=isOn.On)
        sleep(3)
        self.bus_comm.check_tailgate_upper_req(req=isOn.Off)

    @allure.title("466322 v10 尾门学习_尾门外开关按下不足3s_尾门学习请求OFF")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110281(self):
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(2.5)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        sleep(1)
        # self.bus_comm.check_singal("bodycan", "CEMBodyFr11", "TrPosnUpprProgmReq", 1) 发1是Bug
        self.bus_comm.check_tailgate_upper_req(req=isOn.Off)
        
    @allure.title("466322 v10 尾门记忆_Drving模式长按尾门ProgmReq=On")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110225(self):
        self.io.set_door(Trunk=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        self.bus_comm.check_tailgate_upper_req(req=isOn.On)
        sleep(3)
        self.bus_comm.check_tailgate_upper_req(req=isOn.Off)
        
    # @allure.title("466322 v10尾门记忆_convenience模式长按尾门ProgmReq=On")
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_110227(self):
    #     self.io.set_door(Trunk=Door.open)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
    #     self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
    #     self.bus_comm.check_tailgate_upper_req(req=isOn.On)
    #     sleep(3)
    #     self.bus_comm.check_tailgate_upper_req(req=isOn.Off)
        # self.bus_comm.set_singal("bodycan", "CEMBodyFr11", "TrPosnUpprProgmReq", 0)
        # self.bus_comm.set_singal("bodycan", "PotBodyFr02", "SwtTrClsSts", 0)
        # sleep(3)
        # self.bus_comm.check_singal("bodycan", "CEMBodyFr11", "TrPosnUpprProgmReq", 1)
        # sleep(1)
        # self.bus_comm.check_singal("bodycan", "CEMBodyFr11", "TrPosnUpprProgmReq", 0)
        
    @allure.title("466322 v10尾门记忆_尾门硬按键长按3s_尾门ProgmReq=OFF")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110304(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=3)
        self.bus_comm.check_tailgate_upper_req(req=isOn.Off)

    @allure.title("449494 外开关解锁开启尾门_RKE闭锁外开关开尾门尾门Open可释放")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_1987199(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open) # 发送开启尾门请求
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(3) # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("449494 外开关解锁开启尾门_RKE闭锁尾门解锁灯效反馈")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_1987200(self):
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "IndcrSts", 0)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "IndcrSts", 3)  # 解锁灯效反馈
        sleep(.4)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "IndcrSts", 0)

    @allure.title("449494 外开关解锁开启尾门_HMI闭锁_外开关开尾门禁用")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_1987202(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle) 
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        sleep(3) # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("449494 外开关解锁开启尾门_远控闭锁外开关开尾门尾门Open可释放")
    @pytest.mark.full
    def test_caseid_1987201(self):
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "IndcrSts", 0)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open) # 发送开启尾门请求
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(3) # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("449494 外开关解锁开启尾门_Telm闭锁外开关开尾门_TrUnlock有灯效")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_1987203(self):
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "IndcrSts", 0)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "IndcrSts", 3)  # 解锁灯效反馈
        sleep(.4)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "IndcrSts", 0)

    @allure.title("449494 外开关解锁开启尾门_PE闭锁外开关开尾门尾门Open可释放")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_1987204(self):
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        time.sleep(2)  # 避免防玩
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open) # 发送开启尾门请求
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(3) # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("449494 外开关解锁开启尾门_NFC闭锁外开关开尾门尾门Open可释放")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_1987205(self):
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open) # 发送开启尾门请求
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(3) # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)


    @allure.title("449494 外开关解锁开启尾门_PrkgCmftModTiCtrl!=0&外开关开尾门尾门Open可释放")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_1987207(self):
        self.mix.set_common_precontion(UsageMode.CONVENIENCE)
        self.soa.set_convenience_duration(time=1)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open) # 发送开启尾门请求
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
        sleep(3) # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)
        self.soa.set_convenience_duration(time=0)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 0)

    @allure.title("449494 外开关解锁开启尾门_内部其它方式闭锁&&维持上电模式关PrkgCmftModTiCtrl=0_尾门外部开关禁用")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_1987208(self):
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 0)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        time.sleep(2)  # 避免防玩触发
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle) 
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        time.sleep(3) # 延时3s获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)

    @allure.title("449494 外开关解锁开启尾门_车速落锁尾门外开关禁用")
    @pytest.mark.full
    def  test_tailgate_ctrl_caseid_1987210(self):
        self.mix.set_common_precontion(UsageMode.DRIVING)  
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdQf", 3)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdBrkPedlPsd", 1)
        self.bus_comm.set_vehspd(value=1.95)
        self.io.driver_seat_present()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", 2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Idle) 
        self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 2)
        time.sleep(3) # 延时3s获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)



    
    @allure.title("HMI控制尾门全关_Normal_Convenience")
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_118781(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Close)

    @allure.title("HMI控制尾门全开_Normal_Convenience")
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_118782(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open)

    @allure.title("HMI控制尾门暂停_Normal_Convenience")
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_118780(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)
        sleep(1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)
    
    @allure.title("HMI控制尾门开_Normal_Driving")
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_118779(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open)
    
    @allure.title("HMI控制尾门全关_Normal_Driving")
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_118778(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Close)
    
    @allure.title("HMI控制尾门暂停_Normal_Driving")
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_118777(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgIn)
        sleep(1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)
    
    @allure.title("尾门动作MovgDwn_stop")
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_118772(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgIn)
        sleep(1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)
    
    @allure.title("尾门动作MovgUp_stop")
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_118771(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)
        sleep(1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)


    @allure.title("尾门动作MovgUp_stop")
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_118771(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)
        sleep(1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Stop)

    @allure.title("尾门动作FullClsd_stop")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/118773?projectId=46",
        name="尾门动作FullClsd_stop",
    )
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_118773(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)
        self.bus_comm.check_tailgate_without_opener_req()

    @allure.title("尾门动作FullOpend_stop")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/118770?projectId=46",
        name="尾门动作FullOpend_stop",
    )
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_118770(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)
        self.bus_comm.check_tailgate_without_opener_req()

    @allure.title("尾门动作Ukwn_stop")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/118774?projectId=46",
        name="尾门动作FullOpend_stop",
    )
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_118774(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.Ukwn)
        sleep(1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)
        self.bus_comm.check_tailgate_without_opener_req()

# 新用例，脚本   CCP       
        
    @allure.title("normal&&abandoned_通过HMI开启尾门_VehMtnSt=0x2")
    @pytest.mark.sanity
    # @pytest.mark.a99 
    @pytest.mark.edit
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992425(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)  
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED, vehmtnst=VehMtnSts.StandStillVal2)   #总线
        self.sd_tester.write_ccp(ccp={98: 0x2})
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.4)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)    
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off) 
              
              
    @allure.title("normal&&abandoned_通过HMI开启尾门_VehMtnSt=0x3")
    @pytest.mark.sanity
    # @pytest.mark.a99 
    @pytest.mark.edit
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992424(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED, vehmtnst=VehMtnSts.StandStillVal3)   #总线
        self.sd_tester.write_ccp(ccp={98: 0x80})
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)      
  
  
    @allure.title("normal&&inactive_通过HMI开启尾门_VehMtnSt=0x0")
    @pytest.mark.sanity
    # @pytest.mark.a99 
    @pytest.mark.edit
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992423(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.Ukwn)   #总线
        self.sd_tester.write_ccp(ccp={97: 0x2})
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)        
        
    @allure.title("normal&&inactive_通过HMI开启尾门_VehMtnSt=0x3")
    @pytest.mark.sanity
    # @pytest.mark.a99 
    @pytest.mark.edit
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992421(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)  
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal3)   #总线
        self.sd_tester.write_ccp(ccp={97: 0x2})
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off) 
  
  
    @allure.title("normal&&Active_通过HMI开启尾门_VehMtnSt=0x2")
    @pytest.mark.sanity
    # @pytest.mark.a99
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992420(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off) 
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, vehmtnst=VehMtnSts.StandStillVal2)   #总线
        self.sd_tester.write_ccp(ccp={98: 0x2})
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号 
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.4)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off) 
        
        
    @allure.title("normal&&Active_通过HMI开启尾门_VehMtnSt=0x3")
    @pytest.mark.sanity
    # @pytest.mark.a99
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992419(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)  
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, vehmtnst=VehMtnSts.StandStillVal3)   #总线
        self.sd_tester.write_ccp(ccp={98: 0x80})
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off) 
        

    @allure.title("normal&&Driving_通过HMI开启尾门_VehMtnSt=0x2")
    @pytest.mark.sanity
    # @pytest.mark.a99
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992418(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)  
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal2)   #总线
        self.sd_tester.write_ccp(ccp={98: 0x2})
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.4)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off) 
        
        
    @allure.title("normal&&Driving_通过HMI开启尾门_VehMtnSt=0x3")
    @pytest.mark.sanity
    # @pytest.mark.a99
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992417(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)  
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3)   #总线
        self.sd_tester.write_ccp(ccp={98: 0x80})
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)   
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off) 
        
        
    @allure.title("normal&&Convinience_通过HMI开启尾门_VehMtnSt=0x0")
    @pytest.mark.smoke
    # @pytest.mark.a99 
    @pytest.mark.edit
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992112(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)  
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.Ukwn)   #总线
        self.sd_tester.write_ccp(ccp={98: 0x2})
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.4)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off) 
        

        
        
    @allure.title("normal&&Convinience_尾门HalfClsd状态下_通过HMI开启尾门")
    @pytest.mark.smoke
    # @pytest.mark.a99
    def test_tailgate_ctrl_caseid_1992351(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2)   #总线
        self.sd_tester.write_ccp(ccp={98: 0x2})
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        # self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.HalfClsd)     #设POT总线信号
        sleep(.3) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)   
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        
    
    @allure.title("normal&&Convinience_通过HMI关闭尾门")
    @pytest.mark.smoke
    # @pytest.mark.a99
    def test_tailgate_ctrl_caseid_1992327(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)   #总线
        self.sd_tester.write_ccp(ccp={97: 0x2})
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)     #设POT总线信号
        sleep(.5)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        sleep(.5)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)


        
    @allure.title("normal&&Convinience_MovgUp状态下_HMI暂停后背门")
    @pytest.mark.smoke
    # @pytest.mark.a99
    def test_tailgate_ctrl_caseid_1992242(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2)   #总线
        self.sd_tester.write_ccp(ccp={98: 0x2})
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
        sleep(.5)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 

    @allure.title("normal&&Convinience_MovgDwn状态下_HMI暂停后背门")
    @pytest.mark.smoke
    # @pytest.mark.a99
    def test_tailgate_ctrl_caseid_1992189(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)   #总线
        self.sd_tester.write_ccp(ccp={98: 0x2})
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgIn)     #设POT总线信号
        sleep(.5)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 


################################################ 0930 ##################     
        
    @allure.title("normal&&Convinience_通过HMI开启尾门_VehMtnSt=0x3")
    @pytest.mark.sanity
    @pytest.mark.a0930
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992427(self):
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal3, ccp={98: 0x80})   #总线
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号  
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(1)      
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
               
    @allure.title("normal&&abandoned_通过HMI开启尾门_VehMtnSt=0x2")
    @pytest.mark.sanity
    @pytest.mark.a0930
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992425(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x02})   #总线
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号  
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.5)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(.5)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        

        
        
    @allure.title(" normal&&inactive_通过HMI开启尾门_VehMtnSt=0x0")
    @pytest.mark.sanity
    @pytest.mark.a0930
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992423(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.Ukwn, ccp={97: 0x02})   #总线
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号  
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(1)      
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        
    @allure.title(" normal&&inactive_通过HMI开启尾门_VehMtnSt=0x3")
    @pytest.mark.sanity
    @pytest.mark.a0930
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992421(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal3, ccp={97: 0x02})   #总线
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号  
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(1)      
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        
        
    @allure.title(" normal&&Active_通过HMI开启尾门_VehMtnSt=0x2")
    @pytest.mark.sanity
    @pytest.mark.a0930
    def test_tailgate_ctrl_caseid_1992420(self):

        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)     
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)  
        sleep(.1)    
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.5)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(.5)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)


    @allure.title(" normal&&Active_通过HMI开启尾门_VehMtnSt=0x3")
    @pytest.mark.sanity
    @pytest.mark.a0930
    def test_tailgate_ctrl_caseid_1992419(self):

        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, vehmtnst=VehMtnSts.StandStillVal3, ccp={98: 0x80})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)      
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)     
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(1)      
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)

    @allure.title("normal&&Driving_通过HMI开启尾门_VehMtnSt=0x2")
    @pytest.mark.sanity
    @pytest.mark.a0930
    def test_tailgate_ctrl_caseid_1992418(self):

        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)     
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1)      
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.5)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(.5)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)



    @allure.title("normal&&Driving_通过HMI开启尾门_VehMtnSt=0x3")
    @pytest.mark.sanity
    @pytest.mark.a0930
    def test_tailgate_ctrl_caseid_1992417(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3, ccp={98: 0x80})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)      
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)  
        sleep(.1)      
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(1)      
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)

 
    @allure.title("factory&&Convinience_通过HMI开启尾门")
    @pytest.mark.sanity
    @pytest.mark.a0930
    def test_tailgate_ctrl_caseid_1992416(self):

        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)     
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)   
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.5)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(.5)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
      
        

        
    @allure.title("Dyno&&Convinience_通过HMI开启尾门")
    @pytest.mark.sanity
    @pytest.mark.a0930
    def test_tailgate_ctrl_caseid_1992412(self):

        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)     
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)   
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.5)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(.5)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 


    @allure.title("反例_normal&&Convinience_车辆非静止，HMI开门请求忽略")
    @pytest.mark.sanity
    @pytest.mark.a0930
    def test_tailgate_ctrl_caseid_1992410(self):

        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.FwdVal1, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)     
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd) 
        sleep(.1)     
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        

        
    @allure.title("反例_normal&&Convinience_CCP不满足，HMI开门请求忽略（CCP97=0x1&&CCP98=0x3）")
    @pytest.mark.sanity
    @pytest.mark.a0930
    def test_tailgate_ctrl_caseid_1992405(self):

        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x01, 98: 0x03})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)      
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)  
        sleep(.1)      
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        
        
    @allure.title("反例_normal&&Driving_通过HMI开启尾门请求忽略_VehMtnSt=0x0")  
    @pytest.mark.sanity
    @pytest.mark.a0930
    def test_tailgate_ctrl_caseid_1992404(self):

        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.Ukwn, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)       
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd) 
        sleep(.1)     
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)    
        
        
    @allure.title("反例_normal&&Active_通过HMI开启尾门请求忽略_VehMtnSt=0x0")  
    @pytest.mark.sanity
    @pytest.mark.a0930
    def test_tailgate_ctrl_caseid_1992403(self):

        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, vehmtnst=VehMtnSts.Ukwn, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)       
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)   
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)    
        
        
    @allure.title("反例_normal&&Convinience_通过HMI开启尾门请求忽略_VehMtnSt=0x1")  
    @pytest.mark.sanity
    @pytest.mark.a0930
    def test_tailgate_ctrl_caseid_1992402(self):

        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal1, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)       
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)   
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        
     
        
    @allure.title("反例_normal&&Driving_通过HMI开启尾门请求忽略_VehMtnSt=0x0")  
    @pytest.mark.sanity
    @pytest.mark.a09301
    def test_tailgate_ctrl_caseid_1992404(self):

        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.Ukwn, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)       
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        
        
    @allure.title("反例_normal&&Active_通过HMI开启尾门请求忽略_VehMtnSt=0x0")  
    @pytest.mark.sanity
    @pytest.mark.a09301
    def test_tailgate_ctrl_caseid_1992403(self):

        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, vehmtnst=VehMtnSts.Ukwn, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)       
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.1)      
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        
        
    @allure.title("反例_normal&&Convinience_通过HMI开启尾门请求忽略_VehMtnSt=0x1")  
    @pytest.mark.sanity
    @pytest.mark.a09301
    def test_tailgate_ctrl_caseid_1992402(self):

        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal1, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)       
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)    
        sleep(.1)  
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        
        
    @allure.title("normal&&abandoned_尾门HalfClsd状态下_通过HMI开启尾门")
    @pytest.mark.sanity
    @pytest.mark.a09301
    def test_tailgate_ctrl_caseid_1992350(self):

        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        # self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)     
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.HalfClsd)  
        sleep(.1)    
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.5)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(.5)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)



    @allure.title("Dyno&&Convinience_尾门HalfClsd状态下_通过HMI开启尾门")
    @pytest.mark.sanity
    @pytest.mark.a09301
    def test_tailgate_ctrl_caseid_1992347(self):

        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.HalfClsd) 
        sleep(.1)     
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        # self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(1)      
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
        
    @allure.title("normal&&Convinience_尾门HalfClsd状态下_尾门StopMinPntForCls状态下_通过HMI开启尾门")
    @pytest.mark.sanity
    @pytest.mark.a09301
    def test_tailgate_ctrl_caseid_1992346(self):

        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
   
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopDurgCls)   
        sleep(.1)   
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.5)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(.5)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
      
        
    @allure.title("normal&&abandoned_尾门StopMinPntForCls状态下_通过HMI开启尾门")
    @pytest.mark.sanity
    @pytest.mark.a09301
    def test_tailgate_ctrl_caseid_1992345(self):

        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)   
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopDurgCls) 
        sleep(.1)     
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.5)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(.5)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)     
        
        
    @allure.title("Crash&&Convinience_尾门StopMinPntForCls状态下_通过HMI开启尾门")
    @pytest.mark.sanity
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992343(self):

        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)   
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopDurgCls)    
        sleep(.1)  
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)   
        sleep(1)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)     
        self.io.hazard_light_open()
        sleep(.1)
        self.io.hazard_light_close() 
        sleep(.2)         

    @allure.title("反例_Transport&&Convinience_尾门HalfClsd状态下_通过HMI开启尾门请求忽略")
    @pytest.mark.sanity
    @pytest.mark.a09301
    def test_tailgate_ctrl_caseid_1992341(self):

        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)   
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.HalfClsd)   
        sleep(.1)   
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)  
        
        
    @allure.title("反例_Transport&&Convinience_尾门StopMinPntForCls状态下_通过HMI开启尾门请求忽略")
    @pytest.mark.sanity
    @pytest.mark.a09301
    def test_tailgate_ctrl_caseid_1992340(self):

        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)   
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopDurgCls)  
        sleep(.1)    
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
       
    @allure.title("factory&&INACTIVE_通过ShutFace关闭尾门")    #edit1203
    @pytest.mark.sanity
    @pytest.mark.a1203
    def test_tailgate_ctrl_caseid_1992296(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.INACTIVE, ccp={98: 0x80})   #总线
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)   
        

    @allure.title("Dyno&&Convinience_通过ShutFace关闭尾门")    
    @pytest.mark.sanity
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992295(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x80})   #总线
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)   
        
        
    @allure.title("反例_Transport&&Convinience_通过ShutFace关闭尾门请求忽略")    
    @pytest.mark.sanity
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992280(self):
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x2})   #总线
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)   
        
        
    @allure.title("反例_normal&&Convinience_CCP不满足_通过ShutFace关闭尾门请求忽略（CCP98=0x3）")    
    @pytest.mark.sanity
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992279(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x3})   #总线
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)   
                

    @allure.title("反例_normal&&Convinience_在R档下，通过ShutFace关闭尾门请求忽略")    
    @pytest.mark.sanity
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992278(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x80})   #总线
        self.bus_comm.set_vehspd_gear(gear=Gear.Rvs)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)   
                        
                        
    @allure.title("反例_normal&&Convinience_在尾门close下，通过ShutFace关闭尾门请求忽略")    
    @pytest.mark.sanity
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992277(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x2})   #总线
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)   
        
        
    @allure.title("反例_factory&&Convinience_在R档下，通过ShutFace关闭尾门请求忽略")    
    @pytest.mark.full
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992276(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x80})   #总线
        self.bus_comm.set_vehspd_gear(gear=Gear.Rvs)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)           
        
        
    @allure.title("反例_Crash&&Convinience_在D档下，通过ShutFace关闭尾门请求忽略")    
    @pytest.mark.full
    @pytest.mark.a1017
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992275(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x80})   #总线
        self.bus_comm.set_vehspd_gear(gear=Gear.Drv)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)    
        self.io.hazard_light_open()
        sleep(.1)
        self.io.hazard_light_close() 
        sleep(.2)       
                
    @allure.title("normal&&abandoned_MovgUp状态下_ShutFace暂停后背门")    
    @pytest.mark.sanity
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992222(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x80})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        
        
    @allure.title("normal&&Driving_MovgUpBrkg状态下_ShutFace暂停后背门")    
    @pytest.mark.sanity
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992221(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOutBrkg)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
                
        
    @allure.title("factory&&Convinience_MovgUpBrkg状态下_ShutFace暂停后背门")    
    @pytest.mark.sanity
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992220(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal3, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOutBrkg)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)         
        
  
          
    @allure.title("Crash&&Convinience_MovgUp状态下_ShutFace暂停后背门")    
    @pytest.mark.sanity
    @pytest.mark.a1017
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992219(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x80})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)         
        self.io.hazard_light_open()
        sleep(.1)
        self.io.hazard_light_close() 
        sleep(.2)              
              
    @allure.title("Dyno&&Convinience_MovgUpBrkg状态下_ShutFace暂停后背门")    
    @pytest.mark.full
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992218(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOutBrkg)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)         
                     
              
    @allure.title("反例_Transport&&Convinience_MovgUp状态下_ShutFace暂停后背门请求忽略")    
    @pytest.mark.sanity
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992217(self):
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal3, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)                 
        
        
              
    @allure.title("反例_normal&&Convinience_MovgUp状态下_CCP不满足_ShutFace暂停后背门请求忽略（CCP98=0x4）")    
    @pytest.mark.sanity
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992216(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal3, ccp={98: 0x4})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)                 
                
        
    @allure.title("反例_normal&&Convinience_MovgUp状态下_车辆非静止_ShutFace暂停后背门请求忽略")    
    @pytest.mark.sanity
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992215(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.BackwVal2, ccp={98: 0x80})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)           
        
        
        
    @allure.title("反例_factory&&Convinience_Ukwn状态下_ShutFace暂停后背门请求忽略")    
    @pytest.mark.sanity
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992214(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE,ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.Ukwn)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)                   
        
        
        
    @allure.title("反例_normal&&Convinience_FullClsd状态下_ShutFace暂停后背门请求忽略")    
    @pytest.mark.sanity
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992213(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)           
                
        
    @allure.title("normal&&Convinience_StopDurgOpen状态下_ShutFace暂停后背门请求忽略")    
    @pytest.mark.full
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992212(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopDurgOpen)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)           
                        
        
    @allure.title("反例_Crash&&Convinience_FullOpend状态下_ShutFace暂停后背门请求忽略")    
    @pytest.mark.full
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992211(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)           
            
                                
    @allure.title("反例_Dyno&&Convinience_StopDurgCls状态下_ShutFace暂停后背门请求忽略")    
    @pytest.mark.full
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992210(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopDurgCls)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)           
                                        
    @allure.title("反例_normal&&Convinience_HalfClsd状态下_ShutFace暂停后背门请求忽略")    
    @pytest.mark.sanity
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992209(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.HalfClsd)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)           
                                                
                                        
    @allure.title("反例_normal&&Convinience_StopMinPntForCls状态下_ShutFace暂停后背门请求忽略")    
    @pytest.mark.full
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992208(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopMinPntForCls)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)           
                                                        
        
    @allure.title("normal&&Convinience_MovgDwn状态下_ShutFace暂停后背门")    
    @pytest.mark.smoke
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992183(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgIn)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)           
        
    @allure.title("normal&&abandoned_MovgDwn状态下_ShutFace暂停后背门")    
    @pytest.mark.sanity
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992182(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED, ccp={98: 0x80})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgIn)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)           
                
    @allure.title("normal&&Driving_MovgDwnBrkg状态下_ShutFace暂停后背门")    
    @pytest.mark.sanity
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992181(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgInBrkg)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)           
                        
        
    @allure.title("factory&&Convinience_MovgDwnBrkg状态下_ShutFace暂停后背门")    
    @pytest.mark.full
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992180(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgInBrkg)     #设POT总线信号
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)           
                                
        
         
    @allure.title("Crash&&Convinience_MovgDwn状态下_ShutFace暂停后背门")    
    @pytest.mark.full
    @pytest.mark.a1017
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992179(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x80})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgIn)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)           
        self.io.hazard_light_open()
        sleep(.1)
        self.io.hazard_light_close() 
        sleep(.2)                                       
        
                
    @allure.title("Dyno&&Convinience_MovgDwnBrkg状态下_ShutFace暂停后背门")    
    @pytest.mark.sanity
    @pytest.mark.a1017
    def test_tailgate_ctrl_caseid_1992178(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgInBrkg)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)           
                                
 

    @allure.title("Dyno&&abandoned_通过HMI开启尾门")
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992411(self):

        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.ABANDONED, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)     
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)  
        sleep(.1)    
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.5)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(.5)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
    @allure.title("反例_normal&&Convinience_通过HMI开启尾门请求忽略_VehMtnSt=0x4")
    @pytest.mark.full
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992401(self):

        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.FwdVal1, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)     
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)  
        sleep(.1)    
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        
        
    @allure.title("反例_normal&&Convinience_通过HMI开启尾门请求忽略_VehMtnSt=0x5")
    @pytest.mark.full
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992400(self):

        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.FwdVal2, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)     
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd) 
        sleep(.1)     
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        
        
    @allure.title("反例_normal&&Convinience_通过HMI开启尾门请求忽略_VehMtnSt=0x6")
    @pytest.mark.full
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992399(self):

        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.BackwVal1, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)     
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd) 
        sleep(.1)     
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)  
        
        
    @allure.title("反例_normal&&Convinience_通过HMI开启尾门请求忽略_VehMtnSt=0x7")
    @pytest.mark.full
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992398(self):

        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.BackwVal2, ccp={98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)     
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd) 
        sleep(.1)     
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)  
        
        
    @allure.title("factory&&Convinience_尾门HalfClsd状态下_通过HMI开启尾门")
    @pytest.mark.full
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992349(self):

        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x80})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
     
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.HalfClsd)   
        sleep(.1)     
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(1)      
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
   
    @allure.title("factory&&Convinience_尾门StopMinPntForCls状态下_通过HMI开启尾门")
    @pytest.mark.full
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992344(self):

        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x80})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
     
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopMinPntForCls) 
        sleep(.1)       
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(1)      
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)


        
    @allure.title("Dyno&&Convinience_尾门StopMinPntForCls状态下_通过HMI开启尾门")
    @pytest.mark.full
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992342(self):

        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x2})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
     
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopMinPntForCls)
        sleep(.1)        
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(1)      
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)



    @allure.title("normal&&Driving_通过HMI关闭尾门")
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992326(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={98: 0x80})   
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.RKE)     

        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)  
        sleep(.1)              
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        sleep(1)      
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)   
        
        

    @allure.title("normal&&abandoned_通过HMI关闭尾门")
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992325(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={97: 0x2})   
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.RKE)     

        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)  
        sleep(.1)                   
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        sleep(1)      
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)   
       
       
    @allure.title("factory&&Convinience_通过HMI关闭尾门")
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992324(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x80})   
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.RKE)     

        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)  
        sleep(.1)                       
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        sleep(1)      
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)   


       
    @allure.title("Crash&&Convinience_通过HMI关闭尾门")
    @pytest.mark.sanity
    @pytest.mark.a1020
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992323(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x80})   
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)     

        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)  
        sleep(.1)                       
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        sleep(1)      
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)   
        self.io.hazard_light_open()
        sleep(.1)
        self.io.hazard_light_close() 
        sleep(.2)

    @allure.title("Dyno&&Convinience_通过HMI关闭尾门")
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992322(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={97: 0x02})   
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)      
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)   
        sleep(.1)        
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        sleep(1)      
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)        



      
    @allure.title("反例_normal&&driving_档位为R档，HMI开门请求忽略")  #edit1203
    @pytest.mark.sanity
    @pytest.mark.a1203
    def test_tailgate_ctrl_caseid_1992409(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3, ccp={98: 0x80})   
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.soa.get_gear_level(gear=Gear.Rvs)
        
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)      
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd) 
        sleep(.1)       
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_without_tailgate_action_req()   
        
         
    @allure.title("反例_normal&&driving_档位为ManModeIndcn档，HMI开门请求忽略") #edit1203
    @pytest.mark.sanity
    @pytest.mark.a1203
    def test_tailgate_ctrl_caseid_1992408(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3, ccp={98: 0x80})   
        self.bus_comm.set_gear_pos(gear=Gear.ManMode)
        sleep(.2)
        self.soa.get_gear_level(gear=Gear.Resd1)
        
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)      
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)     
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_without_tailgate_action_req()  
               
        
    @allure.title("反例_normal&&driving_档位为Undefd档，HMI开门请求忽略")
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992407(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3, ccp={98: 0x80})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Undefd)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)      
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)  
        sleep(.1)      
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)   
                            
                            
        

        
    @allure.title("反例_Transport&&Convinience_通过HMI关闭尾门请求忽略")
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992306(self):
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.CONVENIENCE, ccp={97: 0x2})   
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.RKE)     

        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)  
        sleep(.1) 
                   
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 
        
        
    @allure.title("反例_normal&&Convinience_CCP不满足，通过HMI关闭尾门请求忽略（CCP97=0x1）")
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992305(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={97: 0x1})   
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.RKE)     

        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1)   
                   
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  
        
        
    @allure.title("反例_normal&&Convinience_CCP不满足，通过HMI关闭尾门请求忽略（CCP98=0x3）")
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992304(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x3})   
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.RKE)     

        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend) 
        sleep(.1)  
                   
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  
        
                
    @allure.title("反例_factory&&Convinience_CCP不满足，通过HMI关闭尾门请求忽略（CCP97=0x1）")
    @pytest.mark.full
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992303(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x1})   
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.RKE)     

        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend) 
        sleep(.1)  
                   
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  
        
                        
    @allure.title("Crash&&Convinience_CCP不满足，通过HMI关闭尾门请求忽略（CCP98=0x3）")
    @pytest.mark.full
    @pytest.mark.a1020
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992302(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x3})   
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)     

        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1)   
                   
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  
        self.io.hazard_light_open()
        sleep(.1)
        self.io.hazard_light_close() 
        sleep(.2)       
        
                        
    @allure.title("normal&&Convinience_在尾门close下，通过HMI关闭尾门请求忽略")
    @pytest.mark.sanity
    @pytest.mark.a1020
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992301(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE, ccp={97: 0x2, 98: 0x80})   
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)     

        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)  
        sleep(.1) 
                   
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  
        self.io.hazard_light_open()
        sleep(.1)
        self.io.hazard_light_close() 
        sleep(.2)        
        
                                
    @allure.title("Dyno&&Convinience_在尾门close下，通过HMI关闭尾门请求忽略")
    @pytest.mark.full
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992300(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={97: 0x2})   
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.RKE)     

        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend) 
        sleep(.1)  
                   
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 
        
        
    @allure.title("normal&&abandoned_MovgUp状态下_HMI暂停后背门")    
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992241(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED, vehmtnst=VehMtnSts.StandStillVal3, ccp={98: 0x80})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
        sleep(.1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)   
        
               
        
    @allure.title("normal&&abandoned_MovgUp状态下_HMI暂停后背门")    
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992240(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOutBrkg)     #设POT总线信号
        sleep(.1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)   
        
                       
        
    @allure.title("factory&&Convinience_MovgUpBrkg状态下_HMI暂停后背门")    
    @pytest.mark.full
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992239(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOutBrkg)     #设POT总线信号
        sleep(.1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)   
        
        
    @allure.title("Crash&&Convinience_MovgUp状态下_HMI暂停后背门")    
    @pytest.mark.sanity
    @pytest.mark.a1020
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992238(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x80})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
        sleep(.1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)   
        self.io.hazard_light_open()
        sleep(.1)
        self.io.hazard_light_close() 
        sleep(.2)        
         
    @allure.title("Dyno&&Convinience_MovgUpBrkg状态下_HMI暂停后背门")    
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992237(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal3, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOutBrkg)     #设POT总线信号
        sleep(.1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)   
        
         
    @allure.title("反例_Transport&&Convinience_MovgUp状态下_HMI暂停后背门请求忽略")    
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992236(self):
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
         
    @allure.title("反例_Normal&&Convinience_MovgUp状态下_CCP不满足_HMI暂停后背门请求忽略（CCP98=0x3）")    
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992235(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x3})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
            
                                     
    @allure.title("反例_Normal&&Convinience_MovgUp状态下_车辆非静止_HMI暂停后背门请求忽略(VehMtnSt=RollgFwdVal1)")    
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992234(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.FwdVal1, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
    @allure.title("反例_normal&&Driving_MovgUp状态下_车辆非静止_HMI暂停后背门请求忽略(Driving&&VehMtnSt=Ukwn)")    
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992233(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.Ukwn, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
                                           
 
    @allure.title("反例_normal&&Active_MovgUp状态下_车辆非静止_HMI暂停后背门请求忽略(Active&&VehMtnSt=Ukwn)")    
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992232(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, vehmtnst=VehMtnSts.Ukwn, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
                                             
 
    @allure.title("反例_normal&&Active_MovgUp状态下_车辆非静止_HMI暂停后背门请求忽略（VehMtnSt=RollgBackwVal1）")    
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992231(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, vehmtnst=VehMtnSts.BackwVal1, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
                                             
 
    @allure.title("反例_factory&&Convinience_Ukwn状态下_HMI暂停后背门请求忽略")    
    @pytest.mark.full
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992230(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.Ukwn, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
                                             
 
    @allure.title("反例_normal&&Convinience_FullClsd状态下_HMI暂停后背门请求忽略")    
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992229(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
                                             
 
    @allure.title("normal&&Convinience_StopDurgOpen状态下_HMI暂停后背门请求忽略")    
    @pytest.mark.full
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992228(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopDurgOpen)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
                                             
 
    @allure.title("反例_Crash&&Convinience_FullOpend状态下_HMI暂停后背门请求忽略")    
    @pytest.mark.sanity
    @pytest.mark.a1020
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992227(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.io.hazard_light_open()
        sleep(.1)
        self.io.hazard_light_close() 
        sleep(.2)                                             
 
    @allure.title("反例_Dyno&&Convinience_StopDurgCls状态下_HMI暂停后背门请求忽略")    
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992226(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopDurgCls)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
                                             
 
    @allure.title("反例_normal&&Convinience_HalfClsd状态下_HMI暂停后背门请求忽略")    
    @pytest.mark.full
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992225(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.HalfClsd)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
                                             
 
    @allure.title("反例_normal&&Convinience_StopMinPntForCls状态下_HMI暂停后背门请求忽略")    
    @pytest.mark.full
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992224(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopMinPntForCls)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
                                             
       
    @allure.title("normal&&abandoned_MovgDwn状态下_HMI暂停后背门")    
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992188(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED,  ccp={98: 0x80})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgIn)     #设POT总线信号
        sleep(.1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)   
        
       
    @allure.title("normal&&Driving_MovgDwnBrkg状态下_HMI暂停后背门")    
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992187(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING,  ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgInBrkg)     #设POT总线信号
        sleep(.1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)   
               
       
    @allure.title("Crash&&Convinience_MovgDwn状态下_HMI暂停后背门")    
    @pytest.mark.full
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992186(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE,  ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgInBrkg)     #设POT总线信号
        sleep(.1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)   
        
       
    @allure.title("Crash&&Convinience_MovgDwn状态下_HMI暂停后背门")    
    @pytest.mark.full
    @pytest.mark.a1020
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992185(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE,  ccp={98: 0x80})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgIn)     #设POT总线信号
        sleep(.1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)   
        self.io.hazard_light_open()
        sleep(.1)
        self.io.hazard_light_close() 
        sleep(.2)       
       
    @allure.title("Dyno&&Convinience_MovgDwnBrkg状态下_HMI暂停后背门")    
    @pytest.mark.sanity
    @pytest.mark.a1020
    def test_tailgate_ctrl_caseid_1992184(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE,  ccp={98: 0x2})   #总线       #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgInBrkg)     #设POT总线信号
        sleep(.1)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Stop)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)   
       

        
                             
    @allure.title("normal&&Convinience_通过TrHndlOutd开启尾门（CCP98!=0x1&&CCP97!=0x1）")
    @pytest.mark.sanity
    @pytest.mark.a1021 
    @pytest.mark.edit 
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992375(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x02,97: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)       
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
          
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.5)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(.5)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)         
        
                            
    @allure.title("normal&&Convinience_通过TrHndlOutd开启尾门（CCP98=0x2&&CCP97=0x2）")
    @pytest.mark.sanity
    @pytest.mark.a1021 
    @pytest.mark.edit 
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992374(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x02,97: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)       
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
          
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.5)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(.5)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  

    @allure.title("normal&&Driving_通过TrHndlOutd开启尾门（CCP98=0x3&&CCP97=0x2）")
    @pytest.mark.sanity
    @pytest.mark.a1021 
    @pytest.mark.edit 
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992373(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x03,97: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)       
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
          
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.5)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(.5)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  
                

    @allure.title("normal&&Driving_通过TrHndlOutd开启尾门（CCP98=0x3&&CCP97=0x2）")
    @pytest.mark.sanity
    @pytest.mark.a1021 
    @pytest.mark.edit 
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992372(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3, ccp={98: 0x04,97: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)       
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
          
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.5)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(.5)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  
        
        

    @allure.title("factory&&Convinience_通过TrHndlOutd开启尾门（CCP98=0x2&&CCP97=0x2）")
    @pytest.mark.sanity
    @pytest.mark.a1021 
    @pytest.mark.edit 
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992371(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x02,97: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)       
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
          
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.5)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(.5)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)    
        
 

    @allure.title("normal&&Driving_通过TrHndlOutd开启尾门（CCP98!=0x1&&CCP97!=0x1）")
    @pytest.mark.sanity
    @pytest.mark.a1021 
    @pytest.mark.edit 
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992368(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x04,97: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)       
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
          
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.5)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(.5)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  
        
        

    @allure.title("Dyno&&Convinience_尾门HalfClsd状态下_通过TrHndlOutd开启尾门")
    @pytest.mark.sanity
    @pytest.mark.a1021 
    @pytest.mark.edit 
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992335(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x04,97: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)       
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.HalfClsd)   
        sleep(.1)
          
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        sleep(1)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 
        
        

    @allure.title("normal&&Inactive_尾门StopMinPntForCls状态下_通过TrHndlOutd开启尾门")
    @pytest.mark.sanity
    @pytest.mark.a1021 
    @pytest.mark.edit 
    @pytest.mark.edit1025
    def test_tailgate_ctrl_caseid_1992332(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x04,97: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)       
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopMinPntForCls)   
        sleep(.1)
          
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        sleep(1)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 
        
        
##################################### 未调通 ##################################

    # @allure.title("507789 通过HMI开启尾门到目标位置_MovgDwn-尾门开启20°")
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_110302(self):
    #     self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 6)
    #     sleep(1)
    #     self.soa.hmi_set_tailgate_postion(pos=20)
    #     self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 3)
    #     self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 0)
    #     self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 20)
    #     sleep(.2)
    #     self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 0)
    #     self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 101)
        
       
    # @allure.title("Dyno&&Convinience_MovgDwnBrkg状态下_HMI暂停后背门")    
    # @pytest.mark.sanity
    # @pytest.mark.a1011
    # def test_tailgate_ctrl_caseid_1992199(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2,  ccp={98: 0x2})   #总线       #SOA服务
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
    #     self.soa.hmi_set_tailgate_postion(pos=20)

    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
    #     sleep(.25)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)   
    
 
    # @allure.title("Crash&&Driving_通过TrHndlOutd开启尾门（CCP98=0x3&&CCP97=0x2）")   #有灯效
    # @pytest.mark.sanity
    # @pytest.mark.a1021
    # def test_tailgate_ctrl_caseid_1992370(self):
    #     self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
    #     self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3, ccp={98: 0x03,97: 0x02})   
    #     self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
    #     self.soa.hmi_set_wash_mode(sts=isOn.Off)
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)       
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
    #     sleep(.1)
          
    #     self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
    #     self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
    #     sleep(.5)    
    #     self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
    #     sleep(.5)    
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
    #     self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)         
        

    # @allure.title("Crash&&Driving_通过TrHndlOutd开启尾门（CCP98=0x3&&CCP97=0x2）")
    # @pytest.mark.sanity
    # @pytest.mark.a1021
    # def test_tailgate_ctrl_caseid_1992369(self):
    #     self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
    #     self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3, ccp={98: 0x04,97: 0x02})   
    #     self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
    #     self.soa.hmi_set_wash_mode(sts=isOn.Off)
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)       
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
    #     sleep(.1)
          
    #     self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
    #     self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
    #     sleep(.5)    
    #     self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
    #     sleep(.5)    
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
    #     self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  
  
        
    # @allure.title("normal&&Convinience_MovgDwn状态下_ShutFace暂停后背门")
    # # @pytest.mark.smoke
    # @pytest.mark.a99  #pass
    # def test_tailgate_ctrl_caseid_1992183(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2)   #总线
    #     self.sd_tester.write_ccp(ccp={98: 0x2})
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgIn)     #设POT总线信号
    #     sleep(.5)
    #     # self.bus_comm.check_singal("connectivitycanfd", "VgmConnFr09", "TrOpenerSts", 6)
    #     self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
    #     sleep(.5)
    #     self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
    #     sleep(.5)
    #     # self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
    #     sleep(.25)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 


    # @allure.title("Normal&&Convinience_MovgUp状态下_尾门记忆")
    # # @pytest.mark.smoke
    # @pytest.mark.a99
    # def test_tailgate_ctrl_caseid_1992128(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)   #总线
    #     self.sd_tester.write_ccp(ccp={98: 0x2})

    #     # self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgIn)     #设POT总线信号
    #     sleep(.5)
    #     self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
    #     # sleep(5)
    #     # self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
    #     # self.bus_comm.check_tailgate_upper_req(req=isOn.On)
    #     self.bus_comm.check_tailgate_upper_req(req=isOn.On)
    #     sleep(1.1)
    #     self.bus_comm.check_tailgate_upper_req(req=isOn.Off)
        
        
    # @allure.title("Normal&&Convinience_MovgUp状态下_尾门防夹")
    # # @pytest.mark.smoke
    # @pytest.mark.a99
    # def test_tailgate_ctrl_caseid_1991856(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)   #总线
    #     self.sd_tester.write_ccp(ccp={98: 0x2})
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
    #     sleep(.5)
    #     # self.bus_comm.set_tailgate_TrObstclDetn(sts=isOn.On)
    #     self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrObstclDetn", 1)
    #     sleep(2)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop) 
    #     sleep(.25)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle) 
        
        
    # @allure.title("Normal&&Convinience_MovgUp状态下_尾门防夹")
    # # @pytest.mark.smoke
    # @pytest.mark.a99
    # def test_tailgate_ctrl_caseid_19999(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)   #总线
    #     self.sd_tester.write_ccp(ccp={98: 0x2})
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgIn)     #设POT总线信号
    #     sleep(.5)
    #     # self.bus_comm.set_tailgate_TrObstclDetn(sts=isOn.On)
    #     self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrAntiPnch", 1)
    #     sleep(2)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop) 
    #     sleep(.25)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle) 

            

         
    # @allure.title("normal&&abandoned_通过HMI开启尾门_VehMtnSt=0x3")
    # @pytest.mark.sanity
    # @pytest.mark.a0930
    # def test_tailgate_ctrl_caseid_1992424(self):
    #     self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED, vehmtnst=VehMtnSts.StandStillVal3, ccp={98: 0x80})   #总线
    #     self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)        #SOA服务
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号  
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
    #     self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
    #     sleep(1)      
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
    #     self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)    
    # 
    # 
        
    # @allure.title("反例_normal&&driving_档位为R档，HMI开门请求忽略")  ###########http://172.18.128.177:8080/2024_09_30_14_01_52
    # @pytest.mark.sanity
    # @pytest.mark.a0930
    # def test_tailgate_ctrl_caseid_1992409(self):

    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3, ccp={98: 0x80})   
    #     self.bus_comm.set_vehspd_gear(gear=Gear.Rvs)
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)      
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)       
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
    #     self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        
        
        
    # @allure.title("反例_normal&&driving_档位为Undefd档，HMI开门请求忽略")   #####http://172.18.128.177:8080/2024_09_30_14_06_54
    # @pytest.mark.sanity
    # @pytest.mark.a0930
    # def test_tailgate_ctrl_caseid_1992407(self):

    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3, ccp={98: 0x80})   
    #     self.bus_comm.set_vehspd_gear(gear=Gear.Undefd)
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)      
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)       
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
    #     self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        

    # @allure.title("反例_transport&&inactive_car mode不满足，HMI开门请求忽略")  ############http://172.18.128.177:8080/2024_09_30_14_49_39
    # @pytest.mark.sanity
    # @pytest.mark.a0930
    # def test_tailgate_ctrl_caseid_1992406(self):

    #     self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.Ukwn, ccp={97: 0x02})   
    #     self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)       
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
 
    #     self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
         
    # @allure.title("normal&&Driving_通过HMI关闭尾门")
    # @pytest.mark.sanity
    # @pytest.mark.a10171
    # def test_tailgate_ctrl_caseid_1992326(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={98: 0x80})   
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)      
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)       
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI)
    #     sleep(1)      
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)
        
        
    # @allure.title("normal&&abandoned_通过HMI关闭尾门")
    # @pytest.mark.sanity
    # @pytest.mark.a10171
    # def test_tailgate_ctrl_caseid_1992325(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED, ccp={97: 0x02})   
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)      
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)       
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI)
    #     sleep(1)      
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)
        
        
    # @allure.title("factory&&Convinience_通过HMI关闭尾门")
    # @pytest.mark.sanity
    # @pytest.mark.a10171
    # def test_tailgate_ctrl_caseid_1992324(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x80})   
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)      
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)       
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI)
    #     sleep(1)      
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)
        



    # @allure.title("466328 v11_尾门开关关闭和锁定_外部闭锁服务关闭尾门中控上锁")   暂时屏蔽0912
    # @pytest.mark.full
    # def test_tailgate_ctrl_caseid_110329(self):
    #     self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
    #     sleep(3)  # 等待NVM存储
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.io.set_door(Trunk=Door.open)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
    #     self.io.set_door(Trunk=Door.close)
    #     sleep(3)  # 延时获取锁状态
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)

    # @allure.title("466328 v11_尾门开关关闭和锁定_Telm闭锁车内无钥匙车外左后位置_TrUnlock-Lockd") 暂时屏蔽0912
    # @pytest.mark.full
    # def test_tailgate_ctrl_caseid_110311(self):
    #     self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.Telm)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
    #     sleep(3)  # 等待NVM存储
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.io.set_door(Trunk=Door.open)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
    #     self.io.set_door(Trunk=Door.close)
    #     self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0xA)])
    #     sleep(3)  # 延时3s获取锁状态
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)



    # @allure.title("466328 v11_尾门开关关闭和锁定_外部闭锁TrUnlock钥匙遗留车内不闭锁")  暂时屏蔽0912
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_111307(self):
    #     self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
    #     sleep(3)  # 等待NVM存储
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.io.set_door(Trunk=Door.open)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
    #     self.io.set_door(Trunk=Door.close)
    #     self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])
    #     sleep(3)  # 延时获取锁状态
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)


    # @allure.title("466328 v11_尾门开关关闭和锁定_外部闭锁TrUnlock钥匙位置未更新Idel状态中控闭锁")  暂时屏蔽0912
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_110214(self):
    #     self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
    #     sleep(3)  # 等待NVM存储
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.io.set_door(Trunk=Door.open)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
    #     self.io.set_door(Trunk=Door.close)
    #     self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x1)])
    #     sleep(3)  # 延时获取锁状态
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)



    # @allure.title("495067 v1 HMI关闭尾门_内部方式闭锁TrUnlock_HMI关闭尾门整车落锁IntrSwt")   暂时屏蔽0912
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_110301(self):
    #     self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
    #     sleep(3)  # 等待NVM存储
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.io.set_door(Trunk=Door.open)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
    #     self.io.set_door(Trunk=Door.close)
    #     sleep(1)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)

    # @allure.title("495067 v1 HMI关闭尾门_HMI闭锁关尾门硬线关尾门落锁")   暂时屏蔽0912
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_110184(self):
    #     self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
    #     sleep(3)  # 等待NVM存储
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.io.set_door(Trunk=Door.open)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
    #     self.io.set_door(Trunk=Door.close)
    #     sleep(1)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)

    # @allure.title("495067 v1 HMI关闭尾门_蓝牙闭锁TrUnlock_硬线关尾门整车落锁")   暂时屏蔽
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_110193(self):
    #     self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
    #     sleep(3)  # 等待NVM存储
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.io.set_door(Trunk=Door.open)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
    #     self.io.set_door(Trunk=Door.close)
    #     sleep(1)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
    

    # @allure.title("499022 v7手动关闭后背门上锁_内部上锁无请求发出硬线关闭尾门_Lockd")   暂时屏蔽0912
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_111383(self):
    #     self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
    #     sleep(3)  # 等待NVM存储
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.io.set_door(Trunk=Door.open)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
    #     self.io.set_door(Trunk=Door.close)
    #     sleep(1)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)

    # @allure.title("499022 v7手动关闭后背门上锁_TrUnlock尾门无状态跳变_中控不落锁")  暂时屏蔽0912
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_110260(self):
    #     self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
    #     sleep(3)  # 等待NVM存储
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
    #     self.io.set_door(Trunk=Door.close)
    #     sleep(1)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)


    # @allure.title("499022 v7手动关闭后背门上锁_内部方式闭锁钥匙遗留_中控落锁")    暂时屏蔽0912
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_110307(self):
    #     self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
    #     sleep(3)  # 等待NVM存储
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.io.set_door(Trunk=Door.open)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
    #     self.io.set_door(Trunk=Door.close)
    #     self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])
    #     sleep(3)  # 延时获取锁状态
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)


    # @allure.title("494881 v24 基于尾门和后备箱的KV解锁_中控上锁尾门外部开关解锁-TrUnlock")  暂时屏蔽0912
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_110279(self):
    #     self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
    #     self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5)
    #     self.bus_comm.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])
    #     sleep(3)# 延时获取锁状态
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)     
  
    # @allure.title("449494 外开关解锁开启尾门_重锁外开关开尾门尾门Open可释放")   ##屏蔽1023
    # @pytest.mark.full
    # def test_tailgate_ctrl_caseid_1987206(self):
    #     self.io.set_hood_sts(HoodSts.Close)
    #     self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
    #     self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
    #     time.sleep(30)  
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
    #     self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
    #     self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open) # 发送开启尾门请求
    #     self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
    #     sleep(3) # 延时获取锁状态
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)     

    # @allure.title("449494 外开关解锁开启尾门_离车落锁外开关开尾门尾门Open可释放")  ###屏蔽1023
    # @pytest.mark.full
    # @pytest.mark.update
    # def  test_tailgate_ctrl_caseid_1987211(self):
    #     self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)      
    #     self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 2)  
    #     self.bus_comm.send_walk_away_lock_cmd()
    #     self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch, timeout=3)
    #     self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
    #     self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open) # 发送开启尾门请求
    #     self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls, timeout=3)    
    
 
    # @allure.title("normal&&Convinience_在FullClsd状态下_通过HMI开启尾门到目标位置_目标位置等于70")
    # @pytest.mark.smoke
    # def test_tailgate_ctrl_caseid_1992159(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x02})   #总线
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
    #     self.soa.hmi_set_tailgate_postion(pos=70)
    #     self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 70)
    #     self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 70)
    #     self.bus_comm.check_singal("bodycan", "BgmBodyFr01", "TrRelsReq", 1)
    #     sleep(.2)
    #     self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 101)
        
        # self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 3)
        # self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 4)
        # self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 70)
        # sleep(.2)
        # self.bus_comm.check_singal("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 0)
        # self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 101)


        
               
    # @allure.title("normal&&Active_在HMI开尾门情况下，通过HMI关闭尾门_LockgCenStsTrigSrc=TmrAut")#############屏蔽1023
    # @pytest.mark.sanity
    # @pytest.mark.a10171
    # def test_tailgate_ctrl_caseid_1992319(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, ccp={98: 0x2}, vehmtnst=VehMtnSts.StandStillVal2 )   
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.TmrAut)     
    #     self.bus_comm.set_vehspd_gear(gear=Gear.Park) 
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)  
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
    #     self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
    #     sleep(.5)    
    #     self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
    #     sleep(.5)    
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
                    
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI)
    #     sleep(1)      
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)   
    #     self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn) 

    #     self.io.hazard_light_open()
    #     sleep(.1)
    #     self.io.hazard_light_close() 
    #     sleep(.2)
        
    # @allure.title(" Crash&&Convinience_在HMI开尾门情况下，通过HMI关闭尾门_LockgCenStsTrigSrc=OutsOth")    #############屏蔽1023
    # @pytest.mark.sanity
    # @pytest.mark.a1014
    # def test_tailgate_ctrl_caseid_1992315(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE, ccp={98: 0x2}, vehmtnst=VehMtnSts.StandStillVal2 )   
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.OutsOth)     
    #     self.bus_comm.set_vehspd_gear(gear=Gear.Park) 
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)  
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])    
            
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
    #     self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
    #     sleep(.5)    
    #     self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
    #     sleep(.5)    
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
                    
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI)
    #     sleep(1)      
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)   
    #     self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)    
    #     self.io.hazard_light_open()
    #     sleep(.1)
    #     self.io.hazard_light_close() 
    #     sleep(.2)    
    
    
    # @allure.title("normal&&Convinience_在HMI开尾门情况下，通过ShutFace关闭尾门_LockgCenStsTrigSrc=KeyRem_找到钥匙")    #############屏蔽1023
    # @pytest.mark.sanity
    # @pytest.mark.a10171
    # def test_tailgate_ctrl_caseid_1992294(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE,ccp={98: 0x80}, vehmtnst=VehMtnSts.StandStillVal2)  
    #     self.bus_comm.set_vehspd_gear(gear=Gear.Park)
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.RKE)  #http://172.18.128.177:8080/2024_10_17_10_33_13    
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)  
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
    #     sleep(1)      
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
    #     self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
    #     sleep(1)
    #     self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
    #     #寻钥匙
        
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
    #     sleep(1)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock)
               
##################################### 未调通 ##################################

    @allure.title("449494 外开关解锁开启尾门_外部其它方式闭锁外开关开尾门尾门Open可释放")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_1987209(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.2)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open) # 发送开启尾门请求
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(3) # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("466328 v11_尾门开关关闭和锁定_Dyno&Active下关闭背门")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110206(self):
        self.bus_comm.set_fr_gear_pos(gear=Gear.Park)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO, vehmtnst=VehMtnSts.StandStillVal3)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.1)
        self.bus_comm.set_tailgate_switch_sts(sts= FoldHmiReq.Psd)
        sleep(.5)
        self.bus_comm.set_tailgate_switch_sts(sts= FoldHmiReq.NotPsd)
        self.bus_comm.check_door_opener_req(tr_opener=DoorPos.Tailgate, door_req= DoorOpenerReq.Close)
       
    @allure.title("499022 v7手动关闭后背门上锁_NFC闭锁Trunlock_硬线关尾门钥匙遗留不闭锁")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110210(self):
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        sleep(3)  # 等待NVM存储
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])  # 尾门寻钥匙区域车内，对应要是遗留不闭锁
        sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("499022 v7手动关闭后背门上锁_离车落锁硬线关尾门_钥匙遗留中控不落锁")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110314(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(.2)  # 等待配置生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req(tr_opener=DoorPos.Tailgate, door_req= DoorOpenerReq.Open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])
        sleep(3)  #  等待NVM存储
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("Crash&&Convinience_尾门HalfClsd状态下_通过HMI开启尾门")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992348(self):
        self.mix.set_common_precontion()   
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.HalfClsd)     
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal3)   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI, timeout=2)
        sleep(.5)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.Ukwn)     

    @allure.title("normal&&abandoned_通过HMI开启尾门_VehMtnSt=0x0")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992426(self):
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED, vehmtnst=VehMtnSts.Ukwn, ccp={98: 0x80})   #总线
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd) 
        sleep(.1)   
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI, timeout=2)
        sleep(.5)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)

    @allure.title("normal&&Convinience_MovgUp状态下_ShutFace暂停后背门")
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_1992223(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2)   #总线
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
        sleep(.1)    
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.2)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrShutFace, timeout=2) 
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 

    @allure.title("normal&&Convinience_通过HMI开启尾门_VehMtnSt=0x2")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992428(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x02})   #总线
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号  
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        sleep(.5)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
    
    @allure.title("normal&&Driving_通过ShutFace关闭尾门")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992297(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={98: 0x2})   #总线
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)     #设POT总线信号
        sleep(.2) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.3)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrShutFace, timeout=2) 
        sleep(.5)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        
    @allure.title("normal&&inactive_通过HMI开启尾门_VehMtnSt=0x2")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992422(self):
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x02})   #总线
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)    
        sleep(.1)  
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        sleep(.5)    
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)

    @allure.title("外开关解锁开启尾门_中央闭锁状态&&钥匙遗留车内可开尾门不区分车内外")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110204(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd, timeout=2)
        sleep(.5)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)

    @allure.title("466321 v10_外部开关暂停尾门和行李箱_尾门MovgUp外开关按下暂停尾门")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110196(self):
        self.bus_comm.set_door_opener_sts(tr_opener=TailGateOpenerSts.MovgUp)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal3)   
        sleep(.5)
        self.bus_comm.check_signal_thread_start('bodycan', 'CemBodyFr02', 'TrOpenerReqTrOpenerReq')  
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.2, pe_test=True)
        result_ori = self.bus_comm.check_signal_thread_stop('TrOpenerReqTrOpenerReq')  
        logger.info(f'获取到的原始数据TrOpenerReqTrOpenerReq为{result_ori}')
        result = get_signal_times_interval(result_ori, 3)
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] !=0
        self.bus_comm.ipdu.reset_check_results()
        self.bus_comm.set_door_opener_sts(tr_opener=TailGateOpenerSts.Ukwn)

    @allure.title("基于尾门和后备箱的KV解锁_中控上锁尾门外部开关解锁-钥匙遗留尾门解锁")
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_110275(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])  # 不区分车内外
        sleep(.2)
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)  

    @allure.title("466322 v10 尾门记忆_Inactive模式长按尾门ProgmReq=On")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110296(self): 
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(3.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_tailgate_upper_req(req=isOn.On)
        self.bus_comm.check_tailgate_upper_req(req=isOn.Off)

    @allure.title("HMI关闭尾门_HMI控制尾门关闭关尾门")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_110255(self):
        self.bus_comm.set_door_opener_sts(tr_opener=TailGateOpenerSts.FullOpend)
        sleep(.2)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI, timeout=2)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.Ukwn)

    @allure.title("Crash&&abandoned_外按键开尾门HMI关闭尾门_钥匙未遗留车内锁源恢复上一个锁源及锁状态NFC")   
    @pytest.mark.update1
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992314(self): 
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.ABANDONED, vehmtnst=VehMtnSts.StandStillVal3)
        sleep(15)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC) 
         
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd, timeout=2)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)  
        
        self.io.set_door(Trunk=Door.open)
        
        # self.soa.hmi_set_tailgate_mode(TailGateMode.Close)   
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI, timeout=5)
        # sleep(1)
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        self.io.set_door(Trunk=Door.close)
        sleep(.5)
        
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)  
        
        
####################### 1111



    @allure.title("Crash&&Convinience_尾门HalfClsd状态下_通过HMI开启尾门")
    @pytest.mark.sanity
    @pytest.mark.a1111
    def test_tailgate_ctrl_caseid_1992348(self):
        self.mix.set_common_precontion()   
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.HalfClsd)     
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal3)   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI, timeout=2)
        sleep(.5)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.Ukwn)           
        
        
    @allure.title("466322 v10 尾门记忆_Inactive模式长按尾门ProgmReq=On")
    @pytest.mark.sanity
    @pytest.mark.a1111
    def test_tailgate_ctrl_caseid_110296(self): 
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(3.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_tailgate_upper_req(req=isOn.On)
        self.bus_comm.check_tailgate_upper_req(req=isOn.Off)
        
        
    @allure.title("基于尾门和后备箱的KV解锁_中控上锁尾门外部开关解锁-钥匙遗留尾门解锁")
    @pytest.mark.full
    @pytest.mark.a1111
    def test_tailgate_ctrl_caseid_110275(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])  # 不区分车内外
        sleep(.2)
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)  
        
        
    @allure.title("HMI关闭尾门_HMI控制尾门关闭关尾门")
    @pytest.mark.sanity
    @pytest.mark.a1111
    def test_tailgate_ctrl_caseid_110255(self):
        self.bus_comm.set_door_opener_sts(tr_opener=TailGateOpenerSts.FullOpend)
        sleep(.2)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI, timeout=2)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.Ukwn)
        
        
    @allure.title("外开关解锁开启尾门_中央闭锁状态&&钥匙遗留车内可开尾门不区分车内外")
    @pytest.mark.full
    @pytest.mark.a1111
    def test_tailgate_ctrl_caseid_110204(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd, timeout=2)
        sleep(.5)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
    
    
    #-------------------------------------------------------->Sam add<---------------------------------------------------------------------------------
    
    @allure.title("normal&&Driving_通过TrHndlOutd开启尾门（CCP98=0x1&&CCP97=0x2）")    
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_1992396(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3, ccp={98: 0x04,97: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)       
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
          
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        sleep(1)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 
        
    
    @allure.title("normal&&Convinience_通过ShutFace关闭尾门")    ####屏蔽1023
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_1992299(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)   #总线
        self.sd_tester.write_ccp(ccp={98: 0x2})
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)     #设POT总线信号
        sleep(1)        
        # self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)
    
    
    @allure.title("normal&&Convinience_MovgUp状态下_HndlOutd暂停后背门")    ####屏蔽1023
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_1992207(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x02})   #总线
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
        sleep(1)        
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.02)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
    
    
    @allure.title("Crash&&Driving_通过HMI开启尾门")  
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992414(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02})   
        sleep(15)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)  
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)       
        sleep(1)
           
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)  
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)

        
    
    @allure.title(" Crash&&Inactive_通过HMI开启尾门")
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992413(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.Ukwn, ccp={97: 0x02})   
        sleep(15)
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        # self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)           
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)  
        sleep(1)
           
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)  
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
    
    @allure.title("反例_transport&&inactive_car mode不满足，HMI开门请求忽略")
    @pytest.mark.sanity
    @pytest.mark.a1021
    def test_tailgate_ctrl_caseid_1992406(self):
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x2})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd) 
        sleep(1)      
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_without_tailgate_action_req()


    @allure.title("factory&&driving_通过HMI开启尾门")#############屏蔽1023
    @pytest.mark.full
    def test_tailgate_ctrl_caseid_1992415(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3, ccp={98: 0x80})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd) 
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)      
        sleep(3)    
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)   
        sleep(1)      
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)     

    
    @allure.title("normal&&Convinience_通过TrHndlOutd开启尾门（CCP97=0x1）")    
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_1992397(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal3, ccp={97: 0x01})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)       
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
          
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        sleep(1)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 


    @allure.title("factory&&Convinience_通过TrHndlOutd开启尾门")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992395(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x01})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)       
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
          
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        sleep(1)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 
    
    @allure.title("normal&&abandone通过TrHndlOutd开启尾门")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992394(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x80,94: 0x80})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)       
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
          
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        sleep(1)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 


    @allure.title("normal&&convenience通过TrHndlOutd开启尾门")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992393(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x80,94: 0x80})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)       
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        sleep(1)    
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 

    
    @allure.title("normal&&inactive__OutsOth闭锁下，钥匙没找到")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992392(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.KV_PEPS)   
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.KV_PEPS)     
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
        self.bus_comm.dk.stop_dk()
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_without_tailgate_action_req()
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock) 
        self.bus_comm.dk.start_dk()

    
    @allure.title("normal&&inactive_Telm闭锁下，通过TrHndlOutd开启尾门")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992391(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.KV_PEPS)   
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.Telm)     
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock) 
    

    @allure.title("normal&&inactive_Keyls闭锁下，通过TrHndlOutd开启尾门")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992390(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.KV_PEPS)   
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal3, ccp={97: 0x02, 98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.Apprch)     
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock) 
    

    @allure.title("normal&&inactive_NFC闭锁下，通过TrHndlOutd开启尾门")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992389(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.KV_PEPS)   
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal3, ccp={97: 0x02, 98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)     
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock) 

    

    @allure.title("normal&&inactive_Apprch闭锁下，通过TrHndlOutd开启尾门")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992388(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.KV_PEPS)   
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal3, ccp={97: 0x02, 98: 0x02})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.Apprch)     
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock) 

    
    @allure.title("normal&&inactive__NFC闭锁下，钥匙没找到")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992383(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.KV_PEPS)   
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal3, ccp={97: 0x02, 98: 0x80,94: 0x80})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)     
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
        self.bus_comm.dk.stop_dk()
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_without_tailgate_action_req()
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock) 
        self.bus_comm.dk.start_dk()


    @allure.title("反例_Transport&&Convinience_TrHndlOutd开启尾门请求忽略")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992380(self):
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal3, ccp={97: 0x02, 98: 0x80})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.KV_PEPS)   
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_without_tailgate_action_req()
    

    @allure.title("反例_normal&&Inactive_通过TrHndlOutd开启尾门_VehMtnSt=0x1")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992379(self):
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal1, ccp={97: 0x02, 98: 0x80})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.KV_PEPS)   
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_without_tailgate_action_req()

    
    @allure.title("反例_nomal&&Convinience_档位D档_TrHndlOutd开启尾门请求忽略")   #edit1203 
    @pytest.mark.sanity
    @pytest.mark.a1203
    def test_tailgate_ctrl_caseid_1992378(self):

        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x80}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)  
        # self.bus_comm.set_vehspd_gear(gear=Gear.Drv)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        sleep(.2)
        self.soa.get_gear_level(gear=Gear.Drv)
        
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)   
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_without_tailgate_action_req()

    
    @allure.title("反例_nomal&&Convinience_档位Resd1档_TrHndlOutd开启尾门请求忽略")   #edit1203 
    @pytest.mark.sanity
    @pytest.mark.a1203
    def test_tailgate_ctrl_caseid_1992377(self):
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x80})   
        # self.bus_comm.set_vehspd_gear(gear=Gear.Resd1)
        self.bus_comm.set_gear_pos(gear=Gear.Resd1)
        sleep(.2)
        self.soa.get_gear_level(gear=Gear.Resd1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)   
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_without_tailgate_action_req()

    
    @allure.title("反例_normal&&Convinience_档位Resd2档_TrHndlOutd开启尾门请求忽略")    #edit1203
    @pytest.mark.sanity
    @pytest.mark.a1203
    def test_tailgate_ctrl_caseid_1992376(self):
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal3, ccp={97: 0x02, 98: 0x80})   
        self.bus_comm.set_gear_pos(gear=Gear.Resd2)
        sleep(.2)
        self.soa.get_gear_level(gear=Gear.Resd1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)   
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_without_tailgate_action_req()


    @allure.title("Dyno&&Driving_通过TrHndlOutd开启尾门")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992369(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3, ccp={97: 0x02, 98: 0x40})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)     
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 


    @allure.title("normal&&drving通过TrHndlOutd开启尾门")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992367(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL
                                       , usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3, ccp={97: 0x02, 98: 0x40})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)     
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 
    
    @allure.title("Dyno&&Driving_通过TrHndlOutd开启尾门")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992364(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal3, ccp={97: 0x02, 98: 0x40})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)     
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 


    @allure.title("反例_normal&&inactive_KeyRem闭锁下，TrHndlOutd开启尾门请求忽略（CCP94=0x01）")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992356(self):
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal3, ccp={97: 0x02, 98: 0x80,94: 0x01})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)   
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_without_tailgate_action_req()

    @allure.title("反例_normal&&inactive_KeyRem闭锁下，TrHndlOutd开启尾门请求忽略（CCP94=0x01）")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992354(self):
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x80,94: 0x80})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)   
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_without_tailgate_action_req()

    
    @allure.title("normal&&Convinience_尾门HalfClsd状态下_通过TrHndlOutd开启尾门")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992339(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x40})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)     
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.HalfClsd)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 

    @allure.title("normal&&Inactive_尾门HalfClsd状态下_通过TrHndlOutd开启尾门")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992338(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x40})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)     
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.HalfClsd)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 


    @allure.title("factory&&Convinience_尾门HalfClsd状态下_通过TrHndlOutd开启尾门")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992337(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x40})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)     
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.HalfClsd)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 

    
    @allure.title("Crash&&Convinience_尾门HalfClsd状态下_通过TrHndlOutd开启尾门")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992336(self):
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x40})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        sleep(15)
        self.check_and_trun_off_lamp_sts()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)     
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.HalfClsd)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 


    @allure.title("反例_Transport&&Convinience_尾门HalfClsd状态下_通过TrHndlOutd开启尾门请求忽略")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992334(self):
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x80,94: 0x80})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)   
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.HalfClsd)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_without_tailgate_action_req()


    @allure.title("normal&&Convinience_尾门StopMinPntForCls状态下_通过TrHndlOutd开启尾门")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992333(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x40})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)     
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopMinPntForCls)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 



    @allure.title("factory&&Convinience_尾门StopMinPntForCls状态下_通过TrHndlOutd开启尾门")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992331(self):
        self.set_common_precondition_for_tailgate(car_mode=CarMode.FACTORY,usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2,ctrl_type=LockSource.HMI,tr_opener=DoorOpenerSts.StopMinPntForCls)
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 

    
    @allure.title("Crash&&Convinience_尾门StopMinPntForCls状态下_通过TrHndlOutd开启尾门")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992330(self):
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x40})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        sleep(15)
        self.check_and_trun_off_lamp_sts()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)     
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopMinPntForCls)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 



    @allure.title("Dyno&&Convinience_尾门StopMinPntForCls状态下_通过TrHndlOutd开启尾门")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992329(self):
        self.set_common_precondition_for_tailgate(car_mode=CarMode.DYNO,usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2,ctrl_type=LockSource.HMI,tr_opener=DoorOpenerSts.StopMinPntForCls)
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 


    @allure.title("反例_Transport&&Convinience_尾门StopMinPntForCls状态下_通过TrHndlOutd开启尾门请求忽略")    
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992328(self):
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x80,94: 0x80})   
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)   
        sleep(3)  
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopMinPntForCls)   
        sleep(.1)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_without_tailgate_action_req()



    # @allure.title("normal&&Convinience_在HMI开尾门情况下，通过HMI关闭尾门_LockgCenStsTrigSrc=KeyRem")
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_1992321(self):
    #     self.set_common_precondition_for_tailgate(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x80,94: 0x80})
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.Telm)     

    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)
    #     self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)  
    #     self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)      
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)   
    #     sleep(3)    
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI)
    #     self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)  
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd) 
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)   
             

    # @allure.title("normal&&inactive_在TrHndlOutdOpenSts开尾门情况下，通过HMI关闭尾门_LockgCenStsTrigSrc=Keyls")
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_1992320(self):
    #     self.set_common_precondition_for_tailgate(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, lock_type=LockCmd.Lock,ccp={97: 0x02, 98: 0x80,94: 0x80})
    #     self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)  
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
    #     sleep(3)    
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI)
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd) 
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)   


    # @allure.title("normal&&Active_在HMI开尾门情况下，通过HMI关闭尾门_LockgCenStsTrigSrc=TmrAut")
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_1992319(self):
    #     self.set_common_precondition_for_tailgate(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, vehmtnst=VehMtnSts.StandStillVal2, lock_type=LockCmd.Lock,ccp={97: 0x02, 98: 0x80,94: 0x80})
    #     self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)  
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
    #     sleep(3)    
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)   



    # @allure.title("normal&&inactive_在HMI开尾门情况下，通过HMI关闭尾门_LockgCenStsTrigSrc=NFC")
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_1992313(self):
    #     self.set_common_precondition_for_tailgate(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, lock_type=LockCmd.Lock,ccp={97: 0x02, 98: 0x80,94: 0x80})
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)   
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
    #     sleep(3)    
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI)
    #     self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)   



    # @allure.title("normal&&inactive_在TrHndlOutdOpenSts开尾门情况下，通过HMI关闭尾门_LockgCenStsTrigSrc=OutsOth")
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_1992311(self):
    #     self.set_common_precondition_for_tailgate(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x80,94: 0x80})
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.KV_PEPS)     

    #     self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)   
    #     sleep(1)
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)   
    #     sleep(1)    
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI)
    #     # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)  
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)  
    #     self.io.set_door(Trunk=Door.close)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)   


    # @allure.title("normal&&inactive_在HMI开尾门情况下，通过HMI关闭尾门_LockgCenStsTrigSrc=IntrSwt")
    # @pytest.mark.sanity
    # def test_tailgate_ctrl_caseid_1992310(self):
    #     self.set_common_precondition_for_tailgate(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x80,94: 0x80})
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.KV_PEPS)     

    #     self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)   
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)   
    #     sleep(1)
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)   
    #     sleep(1)    
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI)
    #     # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)  
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)  
    #     self.io.set_door(Trunk=Door.close)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)   


    @allure.title("normal&&Inactive_通过ShutFace关闭尾门") 
    def test_tailgate_ctrl_caseid_1992298(self):
        self.set_common_precondition_for_tailgate(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98: 0x80,94: 0x80})
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)     #设POT总线信号
  
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)  
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)   


    @allure.title("normal&&inactive_在HMI开尾门情况下，通过ShutFace关闭尾门_LockgCenStsTrigSrc=Telm_找到钥匙")  
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992290(self):
        self.set_common_precondition_for_tailgate(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, lock_type=LockCmd.Lock, ctrl_type=LockSource.Telm,ccp={97: 0x02, 98: 0x80,94: 0x80})
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)   
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(3)    

        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)  
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock)   


    @allure.title("Crash&&abandoned_离车落锁HMI开尾门有有效钥匙尾门关闭锁状态恢复上一个状态")  
    @pytest.mark.sanity
    def test_tailgate_ctrl_caseid_1992289(self):
        self.set_common_precondition_for_tailgate(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, lock_type=LockCmd.Lock, ctrl_type=LockSource.Apprch,ccp={97: 0x02, 98: 0x80,94: 0x80})
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)   
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(3)    

        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)  
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock)   


    @allure.title("normal&&Convinience_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x1&&CCP98=0x1）")    ####屏蔽1023
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_1992274(self):
        self.set_common_precondition_for_tailgate(usage_mode=UsageMode.CONVENIENCE,ctrl_type=LockSource.HMI,ccp={97: 0x01, 98: 0x01},tr_opener=DoorOpenerSts.FullOpend) 
        sleep(.1)        
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.5)
        self.bus_comm.check_without_tailgate_action_req()
        sleep(1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)


    @allure.title("normal&&Inactive_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x1&&CCP98=0x1）")    ####屏蔽1023
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_1992273(self):
        self.set_common_precondition_for_tailgate(usage_mode=UsageMode.INACTIVE,ccp={97: 0x01, 98: 0x01},tr_opener=DoorOpenerSts.FullOpend) 
        sleep(.1)        
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.5)
        self.bus_comm.check_without_tailgate_action_req()
        sleep(1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)

    @allure.title("normal&&Driving_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x1&&CCP98=0x1）")    ####屏蔽1023
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_1992272(self):
        self.set_common_precondition_for_tailgate(usage_mode=UsageMode.DRIVING,ctrl_type=LockSource.HMI,ccp={97: 0x01, 98: 0x01},tr_opener=DoorOpenerSts.FullOpend) 
        sleep(.1)        
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.5)
        self.bus_comm.check_without_tailgate_action_req()
        sleep(1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)
    
    
    @allure.title("factory&&Convinience_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x1&&CCP98=0x1）")    ####屏蔽1023
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_1992271(self):
        self.set_common_precondition_for_tailgate(car_mode=CarMode.FACTORY,usage_mode=UsageMode.CONVENIENCE,ctrl_type=LockSource.HMI,ccp={97: 0x01, 98: 0x01},tr_opener=DoorOpenerSts.FullOpend) 
        sleep(.1)        
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.5)
        self.bus_comm.check_without_tailgate_action_req()
        sleep(1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)


    @allure.title("Dyno&&Convinience_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x1&&CCP98=0x80）")    ####屏蔽1023
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_1992270(self):
        self.set_common_precondition_for_tailgate(car_mode=CarMode.DYNO,usage_mode=UsageMode.CONVENIENCE,ctrl_type=LockSource.HMI,ccp={97: 0x01, 98: 0x80},tr_opener=DoorOpenerSts.FullOpend) 
        sleep(.1)        
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.5)
        self.bus_comm.check_without_tailgate_action_req()
        sleep(1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)

    
    @allure.title("normal&&Convinience_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x2&&CCP98=0x1）")    ####屏蔽1023
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_1992269(self):
        self.set_common_precondition_for_tailgate(usage_mode=UsageMode.CONVENIENCE,ctrl_type=LockSource.HMI,ccp={97: 0x02, 98: 0x01},tr_opener=DoorOpenerSts.FullOpend) 
        sleep(.1)        
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.5)
        self.bus_comm.check_without_tailgate_action_req()
        sleep(1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)
    

    @allure.title("normal&&Inactive_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x2&&CCP98=0x1）")    ####屏蔽1023
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_1992268(self):
        self.set_common_precondition_for_tailgate(ccp={97: 0x02, 98: 0x01},tr_opener=DoorOpenerSts.FullOpend) 
        sleep(.1)        
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.5)
        self.bus_comm.check_without_tailgate_action_req()
        sleep(1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)
    
    @allure.title("normal&&Driving_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x2&&CCP98=0x1）")    ####屏蔽1023
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_1992267(self):
        self.set_common_precondition_for_tailgate(usage_mode=UsageMode.CONVENIENCE,ctrl_type=LockSource.HMI,ccp={97: 0x02, 98: 0x01},tr_opener=DoorOpenerSts.FullOpend) 
        sleep(.1)        
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.5)
        self.bus_comm.check_without_tailgate_action_req()
        sleep(1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)
    
    @allure.title("Dyno&&Convinience_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x1&&CCP98=0x80）")    ####屏蔽1023
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_1992266(self):
        self.set_common_precondition_for_tailgate(car_mode=CarMode.FACTORY,usage_mode=UsageMode.CONVENIENCE,ctrl_type=LockSource.HMI,ccp={97: 0x02, 98: 0x01},tr_opener=DoorOpenerSts.FullOpend) 
        sleep(.1)        
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.5)
        self.bus_comm.check_without_tailgate_action_req()
        sleep(1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)

    @allure.title("Dyno&&Convinience_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x2&&CCP98=0x1）")    ####屏蔽1023
    @pytest.mark.smoke
    def test_tailgate_ctrl_caseid_1992265(self):
        self.set_common_precondition_for_tailgate(car_mode=CarMode.DYNO,usage_mode=UsageMode.CONVENIENCE,ctrl_type=LockSource.HMI,ccp={97: 0x02, 98: 0x01},tr_opener=DoorOpenerSts.FullOpend) 
        sleep(.1)        
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.5)
        self.bus_comm.check_without_tailgate_action_req()
        sleep(1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)


    @allure.title("normal&&inactive_在HMI开尾门情况下，通过手动关闭尾门_LockgCenStsTrigSrc=KeyRem_找到钥匙（CCP97=0x2&&CCP98=80）") 
    def test_tailgate_ctrl_caseid_1992264(self):
        self.set_common_precondition_for_tailgate(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2,lock_type=LockCmd.Lock,ctrl_type=LockSource.Telm, ccp={97: 0x02, 98: 0x80,94: 0x80})
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)   
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock)   
        sleep(3)    
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate, time_interval=0.25)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)  
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock)   















    # ---------------------------------------------------------->HMI尾门控制开启需求 <----------------------------------------------------------
    def test_tailgate_ctrl_caseid_0000001(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.Ukwn, ccp={97: 0x02})   
        
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)   
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)     
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)  
        sleep(1)
           
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI)  
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)


    
    # ---------------------------------------------------------->HMI控制尾门关闭需求 case1 <----------------------------------------------------------
    def test_tailgate_ctrl_caseid_0000002(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.Ukwn, ccp={97: 0x02})   
        
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)   
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)     
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)  
        sleep(1)
           
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI)  
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 

    # ---------------------------------------------------------->HMI控制尾门关闭需求 case2 <----------------------------------------------------------
    def test_tailgate_ctrl_caseid_0000003(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.Ukwn, ccp={97: 0x02})   
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)  
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)   
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)     
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)  
        sleep(1)
           
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI)  
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock) 
    
    # ---------------------------------------------------------->HMI控制尾门关闭需求 case3 <----------------------------------------------------------
    def test_tailgate_ctrl_caseid_0000004(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.Ukwn, ccp={97: 0x02})   
        # self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)  
        # sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)   
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)     
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)  
        sleep(1)
           
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI)  
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock) 
    
    # ---------------------------------------------------------->HMI控制尾门关闭需求 case4 <----------------------------------------------------------
    def test_tailgate_ctrl_caseid_0000005(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)  
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.Ukwn, ccp={97: 0x02})   
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd) 
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI) 
        sleep(3)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)  
        sleep(3)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off) 
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock) 

    
    # ---------------------------------------------------------->HMI控制尾门关闭需求 case4 <----------------------------------------------------------
    def test_tailgate_ctrl_caseid_0000006(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)  
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.Ukwn, ccp={97: 0x02})   
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd) 
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC) 
        sleep(3)
        self.control_tailgate_by_rke(action=TailGateCmd.Open)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)  
        sleep(3)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off) 
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock) 
        
   
   
        
######################### 上传 整理脚本

######################### WTI
    @allure.title("尾门开门报警信息_P档")
    @pytest.mark.sanity
    @pytest.mark.a1128
    def test_caseid_1982536(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2)   #总线
 
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_gear_pos(Gear.Park)
        self.soa.event_check_warning_info_list(name = "Tail", info="4")
        self.soa.get_warning_msg_List(name="Tail", info="4")

        self.io.set_door(Trunk=Door.close)
        time.sleep(.2)
        self.soa.get_warning_info_list(name = "Tail", info="0")
        
        
    @allure.title("尾门开门报警信息_D档")
    @pytest.mark.sanity
    @pytest.mark.a1128
    def test_caseid_1982537(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.soa.get_gear_level(gear=Gear.Drv)
        
        self.soa.event_check_warning_info_list(name = "Tail", info="5")
        self.soa.get_warning_msg_List(name="Tail", info="5")

        self.io.set_door(Trunk=Door.close)
        time.sleep(.2)
        self.soa.get_warning_info_list(name = "Tail", info="0")
        
        
    @allure.title("尾门开门报警信息_R档")
    @pytest.mark.sanity
    @pytest.mark.a1128
    def test_caseid_1982538(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3)  

        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.soa.get_gear_level(gear=Gear.Rvs)
        
        self.io.set_door(Trunk=Door.open)
        
        self.soa.event_check_warning_info_list(name = "Tail", info="5")
        self.soa.get_warning_msg_List(name="Tail", info="5")

        self.io.set_door(Trunk=Door.close)
        time.sleep(.2)
        self.soa.get_warning_info_list(name = "Tail", info="0")
        
    
#############1128   开始466322
    @allure.title("Normal&&Convinience_FullOpend状态下_尾门记忆")   #未上传，待整理脚本
    @pytest.mark.sanity
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992126(self): 
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE,  ccp={98: 0x2})
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)  
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(3.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_tailgate_upper_req(req=isOn.On)
        sleep(1)
        self.bus_comm.check_tailgate_upper_req(req=isOn.Off)       
        
        
    @allure.title("Normal&&abandoned_MovgIn状态下_尾门记忆")
    @pytest.mark.sanity
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992122(self): 
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED,  ccp={98: 0x80}) 
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgIn)  
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(3.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_tailgate_upper_req(req=isOn.Off)
        sleep(1)
        self.bus_comm.check_tailgate_upper_req(req=isOn.Off)    
        
    @allure.title("Normal&&Convinience_StopDurgOpen状态下_尾门记忆请求")
    @pytest.mark.sanity
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992116(self): 
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE,  ccp={98: 0x2}) 
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopDurgOpen)  
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(3.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_tailgate_upper_req(req=isOn.On)
        sleep(1)
        self.bus_comm.check_tailgate_upper_req(req=isOn.Off) 
        
    @allure.title("反例_Normal&&Convinience_Ukwn状态下_尾门记忆请求忽略")
    @pytest.mark.sanity
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992118(self): 
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE,  ccp={98: 0x80}) 
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.Ukwn)  
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(3.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_tailgate_upper_req(req=isOn.Off)
        sleep(1)
        self.bus_comm.check_tailgate_upper_req(req=isOn.Off)   
        
        
    @allure.title("Normal&&Convinience_StopDurgCls状态下_尾门记忆请求")
    @pytest.mark.sanity
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992115(self): 
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE,  ccp={98: 0x80}) 
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopDurgCls)  
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(3.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_tailgate_upper_req(req=isOn.On)
        sleep(1)
        self.bus_comm.check_tailgate_upper_req(req=isOn.Off) 
        
    @allure.title("Normal&&Convinience_StopMinPntForCls状态下_尾门记忆请求")
    @pytest.mark.sanity
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992113(self): 
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopMinPntForCls)  
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(3.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_tailgate_upper_req(req=isOn.On)
        sleep(1)
        self.bus_comm.check_tailgate_upper_req(req=isOn.Off) 
        
        
    @allure.title("Normal&&Convinience_HalfClsd状态下_尾门记忆请求")
    @pytest.mark.sanity
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992114(self): 
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.HalfClsd)  
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(3.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_tailgate_upper_req(req=isOn.On)
        sleep(1)
        self.bus_comm.check_tailgate_upper_req(req=isOn.Off) 
       
       
    @allure.title("Dyno&&Convinience_MovgUp状态下_尾门记忆")
    @pytest.mark.sanity
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992123(self): 
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE,  ccp={98: 0x80}) 
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)  
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(3.1)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_tailgate_upper_req(req=isOn.Off)
        sleep(1)
        self.bus_comm.check_tailgate_upper_req(req=isOn.Off)    
        
        
############################# 开始449494
        
    @allure.title("normal&&Inactive_通过TrHndlOutd开启尾门_KeyRem")
    @pytest.mark.full
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992397(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.5)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        sleep(.5)        
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc = LockTrigerSource.Keyls)  
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        
    
        
    @allure.title("normal&&Inactive_通过TrHndlOutd开启尾门_Telm")   #pass
    @pytest.mark.full
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992396(self):    
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x80, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.Telm)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        sleep(.5)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        sleep(.5)        
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc = LockTrigerSource.Keyls)  
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        
        
    @allure.title("normal&&Inactive_通过TrHndlOutd开启尾门_NFC")
    @pytest.mark.full
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992395(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x80, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC) 
        # self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.NFC)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        sleep(.5)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        sleep(.5)        
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc = LockTrigerSource.Keyls)  
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        
        
        
    @allure.title("normal&&Inactive_通过TrHndlOutd开启尾门_Keyls")
    @pytest.mark.full
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992394(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x80, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)

        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.KV_PEPS)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        sleep(.5)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        sleep(.5)        
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc = LockTrigerSource.Keyls)  
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        
        
        
    @allure.title("normal&&Inactive_通过TrHndlOutd开启尾门_Apprch")
    @pytest.mark.full
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992393(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x80, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)       
        
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(.2)  # 等待配置生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        

        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        sleep(.5)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        sleep(.5)        
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc = LockTrigerSource.Keyls)  
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        
        
        
    @allure.title("normal&&Inactive_通过TrHndlOutd开启尾门_TmrAut")  
    @pytest.mark.full
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992392(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])  # 更新钥匙在车外区域
        time.sleep(32)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.5)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        sleep(.5)        
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc = LockTrigerSource.Keyls)  
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
                

        
    @allure.title("normal&&Inactive_通过TrHndlOutd开启尾门_OutsOth")
    @pytest.mark.full
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992391(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        
        # self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.OutsOth) 
        # # self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.OutsOth)
        # self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.5)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        sleep(.5)        
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc = LockTrigerSource.Keyls)  
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        
        
        
    @allure.title("normal&&Inactive_通过TrHndlOutd开启尾门_InsOth&& PrkgCmftModTiCtrl!=0")  #pass
    @pytest.mark.full
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992390(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        
        self.soa.set_convenience_duration(time=1)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        

        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On)
        sleep(.5)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        sleep(.5)        
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc = LockTrigerSource.Keyls)  
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        
        
        
    @allure.title("normal&&Inactive_通过TrHndlOutd开启尾门_Telm上锁_钥匙没找到")    
    @pytest.mark.full
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992389(self):    
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x80, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.Telm)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x1)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        sleep(.5)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        sleep(.5)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)  
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        
        
        
    
    @allure.title("normal&&CONVENIENCE_Unlock_通过TrHndlOutd开启尾门")    
    @pytest.mark.sanity
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992388(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x80, 94:0x80})   #总线
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        
        sleep(.2) 
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        sleep(.5)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        sleep(.5)        
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        
        
    @allure.title("反例_normal&&CONVENIENCE_通过TrHndlOutd开启尾门_CCP不满足（97:0x01）")    
    @pytest.mark.full
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992387(self):    
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x01, 98:0x80, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        
        
    @allure.title("反例_normal&&CONVENIENCE_通过TrHndlOutd开启尾门_CCP不满足（98:0x01）")    
    @pytest.mark.full
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992386(self):    
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x1, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        
        
    @allure.title("反例_normal&&CONVENIENCE_通过TrHndlOutd开启尾门_洗车模式开")    
    @pytest.mark.full
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992385(self):    
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.On)
        
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        
    @allure.title("normal&&Inactive_内锁下PE解锁不可用")  
    @pytest.mark.full
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992384(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        
        
    @allure.title("反例_normal&&CONVENIENCE_通过TrHndlOutd开启尾门_CCP不满足（94:0x01）")    
    @pytest.mark.full
    @pytest.mark.a1128
    def test_tailgate_ctrl_caseid_1992383(self):    
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x1, 94:0x1}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        
##############开始466320 
       
    @allure.title("TrAntiPnch=true，触发尾门防夹")    
    @pytest.mark.sanity
    @pytest.mark.a01127
    def test_tailgate_ctrl_caseid_1991885(self):   
 
        self.bus_comm.set_tailgate_AntiPinch_sts(AntiPinch=True)
        self.soa.event_check_tailgate_AntiPinch_sts(sts=True)
        self.soa.get_tailgate_AntiPinch_sts(sts=True)
        

    @allure.title("反例_TrAntiPnch=false，不触发尾门防夹")    
    @pytest.mark.sanity
    @pytest.mark.a01127
    def test_tailgate_ctrl_caseid_1991884(self):   
 
        self.bus_comm.set_tailgate_AntiPinch_sts(AntiPinch=False)
        self.soa.event_check_tailgate_AntiPinch_sts(sts=False)
        self.soa.get_tailgate_AntiPinch_sts(sts=False)

##################开始507789  

    @allure.title("normal&&Convinience_MovgDwn_尾门开启70°_尾门stop")    
    @pytest.mark.sanity
    @pytest.mark.a1129
    def test_tailgate_ctrl_caseid_1992166(self):   
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE,  vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x2})   #总线
 
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgIn)     #设POT总线信号
        sleep(1)
        self.soa.hmi_set_tailgate_postion(pos=70)
        # self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 101)        
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 

    
    @allure.title("normal&&Convinience_MovgDwnBrkg_尾门开启70°_尾门stop")    
    @pytest.mark.sanity
    @pytest.mark.a1129
    def test_tailgate_ctrl_caseid_1992165(self):   
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE,  vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x2})   #总线
 
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgInBrkg)     #设POT总线信号
        sleep(1)
        self.soa.hmi_set_tailgate_postion(pos=70)
        # self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 101)        
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 

    
    @allure.title("normal&&Convinience_MovgUp_尾门开启70°_尾门stop")    
    @pytest.mark.sanity
    @pytest.mark.a1129
    def test_tailgate_ctrl_caseid_1992169(self):   
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE,  vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x80})   #总线
 
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)     #设POT总线信号
        sleep(1)
        self.soa.hmi_set_tailgate_postion(pos=70)
        # self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 101)        
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        
    
    @allure.title("normal&&Convinience_MovgUpBrkg_尾门开启70°_尾门stop")    
    @pytest.mark.sanity
    @pytest.mark.a1129
    def test_tailgate_ctrl_caseid_1992167(self):   
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE,  vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x80})   #总线
 
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOutBrkg)     #设POT总线信号
        sleep(1)
        self.soa.hmi_set_tailgate_postion(pos=70)
        # self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 101)        
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        

    @allure.title("normal&&Convinience_FullOpend_尾门开启70°")    
    @pytest.mark.sanity
    @pytest.mark.a1129
    def test_tailgate_ctrl_caseid_1992142(self):   
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x2})   #总线
 
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)     #设POT总线信号
        sleep(1)
        self.soa.hmi_set_tailgate_postion(pos=70)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        self.bus_comm.check_tailgate_Position(Position=101)    
        sleep(.2)   
        self.bus_comm.check_tailgate_Position(Position=101)   
        sleep(.3)  
        self.bus_comm.check_tailgate_Position(Position=101) 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        


    
    @allure.title("normal&&Convinience_Ukwn_尾门开启70°")    
    @pytest.mark.sanity
    @pytest.mark.a1129
    def test_tailgate_ctrl_caseid_1992160(self):   
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x2})   #总线

        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.Ukwn)     #设POT总线信号
        sleep(1)
        self.soa.hmi_set_tailgate_postion(pos=70)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        self.bus_comm.check_tailgate_Position(Position=70)    
        sleep(.2)  
        self.bus_comm.check_tailgate_Position(Position=70)   
        sleep(.3)  
        self.bus_comm.check_tailgate_Position(Position=101) 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
    
    
    @allure.title("normal&&Convinience_FullClsd_尾门开启100°")    
    @pytest.mark.sanity
    @pytest.mark.a1129
    def test_tailgate_ctrl_caseid_1992159(self):   
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x80})   #总线

        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(1)
        self.soa.hmi_set_tailgate_postion(pos=100)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        self.bus_comm.check_tailgate_Position(Position=100)    
        sleep(.2)   
        self.bus_comm.check_tailgate_Position(Position=100)   
        sleep(.3)  
        self.bus_comm.check_tailgate_Position(Position=101) 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 

    
    # @allure.title("normal&&Convinience_HalfClsd_尾门开启99°")     #待解决，整理脚本 
    # @pytest.mark.sanity
    # @pytest.mark.a1129
    # def test_tailgate_ctrl_caseid_1992156(self):   
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x2})   #总线

    #     self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.HalfClsd)     #设POT总线信号
    #     sleep(1)
    #     self.soa.hmi_set_tailgate_postion(pos=99)
    #     self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On) 
    #     self.bus_comm.check_tailgate_Position(Position=99)    
    #     sleep(.2)  
    #     self.bus_comm.check_tailgate_Position(Position=99)   
    #     sleep(.3)  
    #     self.bus_comm.check_tailgate_Position(Position=101) 
    #     self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
 
    
    @allure.title("normal&&Convinience_StopDurgCls_尾门开启10°")    
    @pytest.mark.sanity
    @pytest.mark.a1129
    def test_tailgate_ctrl_caseid_1992157(self):   
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x80})   #总线
       
        self.bus_comm.set_tailgate_TrOpenPosn(TrOpenPosn=9)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopDurgCls)     #设POT总线信号
        sleep(1)
        self.soa.hmi_set_tailgate_postion(pos=10)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        self.bus_comm.check_tailgate_Position(Position=10)   #开度值发6帧，觉得帧数不对，可查看jet log 
        sleep(.2)   
        self.bus_comm.check_tailgate_Position(Position=10)   
        sleep(.3)  
        self.bus_comm.check_tailgate_Position(Position=101)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
               

    @allure.title("normal&&Convinience_StopDurgOpen_尾门开启50°")    
    @pytest.mark.sanity
    @pytest.mark.a1129
    def test_tailgate_ctrl_caseid_1992158(self):   
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x2})   #总线

        self.bus_comm.set_tailgate_TrOpenPosn(TrOpenPosn=5)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopDurgOpen)     #设POT总线信号
        sleep(1)
        self.soa.hmi_set_tailgate_postion(pos=50)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On) 
        self.bus_comm.check_tailgate_Position(Position=50)    
        sleep(.2)   
        self.bus_comm.check_tailgate_Position(Position=50)   
        sleep(.3)  
        self.bus_comm.check_tailgate_Position(Position=101) 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
               
    
    @allure.title("normal&&Convinience_StopMinPntForCls_尾门开启25°")    
    @pytest.mark.sanity
    @pytest.mark.a1129
    def test_tailgate_ctrl_caseid_1992149(self):   
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x2})   #总线

        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopMinPntForCls)     #设POT总线信号
        sleep(1)
        self.soa.hmi_set_tailgate_postion(pos=25)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.On) 
        self.bus_comm.check_tailgate_Position(Position=25)    
        sleep(.2)   
        self.bus_comm.check_tailgate_Position(Position=25)   
        sleep(.3)  
        self.bus_comm.check_tailgate_Position(Position=101) 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
     

    @allure.title("反例_尾门开启25°，CCP不满足(CCP98=0x3),请求忽略")    
    @pytest.mark.sanity
    @pytest.mark.a1129
    def test_tailgate_ctrl_caseid_1992136(self):   
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x3})   #总线

        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(1)
        self.soa.hmi_set_tailgate_postion(pos=25)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        self.bus_comm.check_tailgate_Position(Position=101)    
        sleep(.2)   
        self.bus_comm.check_tailgate_Position(Position=101)   
        sleep(.3)  
        self.bus_comm.check_tailgate_Position(Position=101) 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        
        

    @allure.title("反例_尾门开启101°,请求忽略")    
    @pytest.mark.sanity
    @pytest.mark.a1129
    def test_tailgate_ctrl_caseid_1992138(self):   
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x2})   #总线

        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(1)
        self.soa.hmi_set_tailgate_postion(pos=101)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        self.bus_comm.check_tailgate_Position(Position=101)    
        sleep(.2)   
        self.bus_comm.check_tailgate_Position(Position=101)   
        sleep(.3)  
        self.bus_comm.check_tailgate_Position(Position=101) 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        
        

    @allure.title("反例_尾门开启9°,请求忽略")    
    @pytest.mark.sanity
    @pytest.mark.a1129
    def test_tailgate_ctrl_caseid_1992140(self):   
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x2})   #总线

        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(1)
        self.soa.hmi_set_tailgate_postion(pos=9)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        self.bus_comm.check_tailgate_Position(Position=101)    
        sleep(.2)   
        self.bus_comm.check_tailgate_Position(Position=101)   
        sleep(.3)  
        self.bus_comm.check_tailgate_Position(Position=101) 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        
        
    @allure.title("反例，actual position大于9°，请求尾门开启，请求忽略")    
    @pytest.mark.sanity
    @pytest.mark.a1129
    def test_tailgate_ctrl_caseid_1992137(self):   
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={98: 0x2})   #总线

        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopDurgOpen)     #设POT总线信号
        self.bus_comm.set_tailgate_TrOpenPosn(TrOpenPosn=20)
        
        sleep(1)
        self.soa.hmi_set_tailgate_postion(pos=90)
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off) 
        self.bus_comm.check_tailgate_Position(Position=101)    
        sleep(.2)   
        self.bus_comm.check_tailgate_Position(Position=101)   
        sleep(.3)  
        self.bus_comm.check_tailgate_Position(Position=101) 
        self.bus_comm.check_door_rels_req(Tr=DoorRelsReq.Off)
        
        
##################### 开始495067
        
  
    @allure.title("Keyls上锁，TrHndlOutd开尾门，HMI关尾门")#pass1020
    @pytest.mark.full
    @pytest.mark.a1201
    def test_tailgate_ctrl_caseid_1992321(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2, 94:0x80}) 
        
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.KV_PEPS)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        
        self.io.set_door(Trunk=Door.open)
        sleep(.5)
        
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        self.io.set_door(Trunk=Door.close)

        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        
    @allure.title("Apprch上锁，TrHndlOutd开尾门，HMI关尾门")#pass1020
    @pytest.mark.full
    @pytest.mark.a1201
    def test_tailgate_ctrl_caseid_1992320(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x80, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        
        
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(.2)  # 等待配置生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        

        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        
        self.io.set_door(Trunk=Door.open)
        sleep(.5)
        
        # self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        # sleep(1)
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        self.io.set_door(Trunk=Door.close)

        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
       
       
    @allure.title("OutsOth上锁，TrHndlOutd开尾门，HMI关尾门")  #pass1020
    @pytest.mark.full
    @pytest.mark.a1201
    def test_tailgate_ctrl_caseid_1992318(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2,  ccp={97: 0x02, 98:0x2, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd, timeout=2)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
            
        self.io.set_door(Trunk=Door.open)
        sleep(.5)
        
        # self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        # sleep(1)
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        self.io.set_door(Trunk=Door.close)

        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        
       
    @allure.title("NFC上锁，TrHndlOutd开尾门，HMI关尾门")  #pass1020
    @pytest.mark.full
    @pytest.mark.a1201
    def test_tailgate_ctrl_caseid_1992312(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x02, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC) 
        # self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.NFC)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd, timeout=2)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
            
        self.io.set_door(Trunk=Door.open)
        sleep(.5)
        
        # self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        # sleep(1)
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        self.io.set_door(Trunk=Door.close)

        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)


    @allure.title("KeyRem上锁，HMI开尾门，HMI关尾门") #pass1020
    @pytest.mark.full
    @pytest.mark.a1201
    def test_tailgate_ctrl_caseid_1992317(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2}) 
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.soa.get_gear_level(gear=Gear.Neut)
        
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
       
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI, timeout=2)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.io.set_door(Trunk=Door.open)
        sleep(.5)
        
        # self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        # sleep(1)
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        self.io.set_door(Trunk=Door.close)

        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        
        
    @allure.title("Telm上锁，HMI开尾门，HMI关尾门")   #pass1020
    @pytest.mark.full
    @pytest.mark.a1201
    def test_tailgate_ctrl_caseid_1992316(self):    
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.soa.get_gear_level(gear=Gear.Neut)
        
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.Telm)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
       
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI, timeout=2)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.io.set_door(Trunk=Door.open)
        sleep(.5)
        
        # self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        # sleep(1)
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        self.io.set_door(Trunk=Door.close)

        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        
        
    @allure.title("TmrAut上锁，HMI开尾门，HMI关尾门") #pass1020
    @pytest.mark.full
    @pytest.mark.a1201
    def test_tailgate_ctrl_caseid_1992313(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])  # 更新钥匙在车外区域
        time.sleep(32)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
       
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI, timeout=2)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.io.set_door(Trunk=Door.open)
        sleep(.5)
        
        # self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        # sleep(1)
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        self.io.set_door(Trunk=Door.close)

        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)       
    
    
    @allure.title("InsOth上锁，HMI开尾门，HMI关尾门")    #pass
    @pytest.mark.full
    @pytest.mark.a1201
    def test_tailgate_ctrl_caseid_1992311(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x80})   #总线

        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.2) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.io.set_door(Trunk=Door.open)
        sleep(.2)
        
        # self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        # sleep(1)
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        self.io.set_door(Trunk=Door.close)

        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        
    
    
    @allure.title("SpdAut上锁，HMI开尾门，HMI关尾门")    
    @pytest.mark.full
    @pytest.mark.a1201
    def test_tailgate_ctrl_caseid_1992310(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2})   #总线
 
        # self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)
        # self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdQf", 3)
        # self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdBrkPedlPsd", 1)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.bus_comm.set_vehspd(value=1.95)
        self.io.driver_seat_present()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", 2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)
        

        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.2) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.io.set_door(Trunk=Door.open)
        sleep(.2)
        
        # self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        # sleep(1)
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        self.io.set_door(Trunk=Door.close)

        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
    
    
    @allure.title("IntrSwt上锁，HMI开尾门，HMI关尾门")    
    @pytest.mark.full
    @pytest.mark.a1201
    def test_tailgate_ctrl_caseid_1992309(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2})   #总线
 
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        

        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.2) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.io.set_door(Trunk=Door.open)
        sleep(.2)
        
        # self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        # sleep(1)
        # self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        self.io.set_door(Trunk=Door.close)

        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        
        
    @allure.title("反例_HMI关尾门，CCP不满足（CCP97=0x1）") #pass1020
    @pytest.mark.sanity
    @pytest.mark.a1201
    def test_tailgate_ctrl_caseid_1992308(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal3, ccp={97: 0x01, 98:0x2})   #总线
        self.sd_tester.write_ccp(ccp={98: 0x01})

        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        
    @allure.title("反例_HMI关尾门，CCP不满足（CCP98=0x1）")  #pass1020
    @pytest.mark.sanity
    @pytest.mark.a1201
    def test_tailgate_ctrl_caseid_1992307(self):
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)  
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal3, ccp={97: 0x02, 98:0x1})   #总线
        self.sd_tester.write_ccp(ccp={97: 0x01})

        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)     #设POT总线信号
        sleep(.1) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
       
##################### 开始466328

    @allure.title("Keyls上锁，TrHndlOutd开尾门，ShutFace关尾门")#
    @pytest.mark.full
    @pytest.mark.a01129
    def test_tailgate_ctrl_caseid_1992299(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.KV_PEPS)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        
        self.io.set_door(Trunk=Door.open)
        sleep(.5)
        
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.3)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
       
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x1)])
        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        

    @allure.title("Apprch上锁，TrHndlOutd开尾门，ShutFace关尾门")#
    @pytest.mark.full
    @pytest.mark.a01129
    def test_tailgate_ctrl_caseid_1992298(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x80, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        
        
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(.2)  # 等待配置生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        

        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        
        self.io.set_door(Trunk=Door.open)
        sleep(1)
        
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.3)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
       
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x1)])
        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
       
       
    @allure.title("OutsOth上锁，TrHndlOutd开尾门，ShutFace关尾门")  #
    @pytest.mark.full
    @pytest.mark.a01129
    def test_tailgate_ctrl_caseid_1992293(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.soa.get_gear_level(gear=Gear.Neut)
        
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd, timeout=2)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
            
        self.io.set_door(Trunk=Door.open)
        sleep(.5)
        
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.3)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
       
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x1)])
        sleep(1)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        
       
    @allure.title("NFC上锁，TrHndlOutd开尾门，ShutFace关尾门")  #
    @pytest.mark.full
    @pytest.mark.a01129
    def test_tailgate_ctrl_caseid_1992289(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x02, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.soa.get_gear_level(gear=Gear.Neut)
        
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC) 
        # self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.NFC)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd, timeout=2)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
            
        self.io.set_door(Trunk=Door.open)
        sleep(1)
        
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.3)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
       
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  

        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)


    @allure.title("KeyRem上锁，HMI开尾门，ShutFace关尾门") #
    @pytest.mark.full
    @pytest.mark.a01129
    def test_tailgate_ctrl_caseid_1992292(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2}) 
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.soa.get_gear_level(gear=Gear.Neut)
        
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
       
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI, timeout=2)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.io.set_door(Trunk=Door.open)
        sleep(.5)
        
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.3)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
       
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)]) 
        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        
        
    @allure.title("Telm上锁，HMI开尾门，ShutFace关尾门")   #
    @pytest.mark.full
    @pytest.mark.a01129
    def test_tailgate_ctrl_caseid_1992291(self):    
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.soa.get_gear_level(gear=Gear.Neut)
        
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.Telm)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
       
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI, timeout=2)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.io.set_door(Trunk=Door.open)
        sleep(.5)
        
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.3)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
       
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)]) 
        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        
        
    @allure.title("TmrAut上锁，HMI开尾门，ShutFace关尾门") #
    @pytest.mark.full
    @pytest.mark.a01129
    def test_tailgate_ctrl_caseid_1992290(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])  # 更新钥匙在车外区域
        time.sleep(32)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)

        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
       
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI, timeout=2)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.io.set_door(Trunk=Door.open)
        sleep(.5)
        
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.3)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
       
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x1)])
        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)       
    
    
    @allure.title("InsOth上锁，HMI开尾门，ShutFace关尾门")    #pass
    @pytest.mark.full
    @pytest.mark.a01129
    def test_tailgate_ctrl_caseid_1992288(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x80})   #总线
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.2) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.io.set_door(Trunk=Door.open)
        sleep(.2)
        
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.3)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
       
        self.io.set_door(Trunk=Door.close)

        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        
    
    
    @allure.title("SpdAut上锁，HMI开尾门，ShutFace关尾门")    
    @pytest.mark.full
    @pytest.mark.a01129
    def test_tailgate_ctrl_caseid_1992287(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2})   #总线
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
         
        # self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)
        # self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdQf", 3)
        # self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdBrkPedlPsd", 1)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.bus_comm.set_vehspd(value=1.95)
        self.io.driver_seat_present()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", 2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)
        

        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.2) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.io.set_door(Trunk=Door.open)
        sleep(.2)
        
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.3)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
       
        self.io.set_door(Trunk=Door.close)

        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
    
    
    @allure.title("IntrSwt上锁，HMI开尾门，ShutFace关尾门")    
    @pytest.mark.full
    @pytest.mark.a01129
    def test_tailgate_ctrl_caseid_1992286(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2})   #总线
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
         
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        

        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.2) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.io.set_door(Trunk=Door.open)
        sleep(.2)
        
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.3)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close, trunk_trigsrc=TailgateTrigerSource.TrShutFace) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
       
        self.io.set_door(Trunk=Door.close)

        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        
        

    @allure.title("反例_ShutFace关尾门，CCP不满足（CCP98=0x1）")  #
    @pytest.mark.sanity
    @pytest.mark.a01129
    def test_tailgate_ctrl_caseid_1992285(self):
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)  
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal3, ccp={97: 0x02, 98:0x1})   #总线
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)

        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.3)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 


    @allure.title("反例_ShutFace关尾门，挡位不满足_R挡位")  #
    @pytest.mark.sanity
    @pytest.mark.a01129
    def test_tailgate_ctrl_caseid_1992284(self):
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)  
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3, ccp={97: 0x02, 98:0x2})   #总线
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.soa.get_gear_level(gear=Gear.Rvs)

        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.3)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        


    @allure.title("反例_ShutFace关尾门，挡位不满足_D挡位")  #
    @pytest.mark.sanity
    @pytest.mark.a01129
    def test_tailgate_ctrl_caseid_1992283(self):
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)  
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3, ccp={97: 0x02, 98:0x2})   #总线
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.soa.get_gear_level(gear=Gear.Drv)

        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)        #SOA服务
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)     #设POT总线信号
        sleep(.1) 
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        sleep(.3)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.NotPsd)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
        

#################################### 开始466321     
       
    @allure.title("normal&&Convinience_MovgUp状态下_HndlOutd暂停后背门")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992207(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98:0x02}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
     
       
    @allure.title("normal&&abandoned_MovgUp状态下_HndlOutd暂停后背门")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992206(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED, ccp={98:0x80}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
       
    @allure.title("normal&&Driving_MovgUpBrkg状态下_HndlOutd暂停后背门")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992205(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={98:0x2}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOutBrkg)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
     
     
       
    @allure.title("factory&&INACTIVE_MovgUpBrkg状态下_HndlOutd暂停后背门")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992204(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.INACTIVE, ccp={98:0x2}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOutBrkg)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
     
       
    @allure.title("Crash&&INACTIVE_MovgUp状态下_HndlOutd暂停后背门")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992203(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.INACTIVE, ccp={98:0x80}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
     
       
    @allure.title("Dyno&&Convinience_MovgUpBrkg状态下_HndlOutd暂停后背门")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992202(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={98:0x2}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOutBrkg)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
    @allure.title("反例_normal&&Convinience_MovgUp状态下_CCP不满足_HndlOutd暂停后背门请求忽略（CCP98=0x4）")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992200(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={98:0x4}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
    @allure.title("反例_normal&&Convinience_Ukwn状态下_HndlOutd暂停后背门请求忽略")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992197(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98:0x2}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.Ukwn)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
        
    @allure.title("反例_normal&&Convinience_FullClsd状态下_HndlOutd暂停后背门请求忽略")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992196(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98:0x80}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
        
        
    @allure.title("normal&&Convinience_StopDurgOpen状态下_HndlOutd暂停后背门请求忽略")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992195(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98:0x80}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopDurgOpen)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
        
    @allure.title("反例_Crash&&Convinience_FullOpend状态下_HndlOutd暂停后背门请求忽略")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992194(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98:0x80}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
        
    @allure.title("反例_normal&&Convinience_StopDurgCls状态下_HndlOutd暂停后背门请求忽略")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992193(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98:0x80}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopDurgCls)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
        
    @allure.title("反例_normal&&Convinience_HalfClsd状态下_HndlOutd暂停后背门请求忽略")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992192(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98:0x80}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopDurgCls)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
        
        
    @allure.title("反例_normal&&Convinience_StopMinPntForCls状态下_HndlOutd暂停后背门请求忽略")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992191(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98:0x80}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.StopMinPntForCls)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
        
    @allure.title("normal&&abandoned_MovgUp状态下_洗车模式_HndlOutd暂停后背门请求忽略")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992190(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED, ccp={98:0x80}) 
        self.soa.hmi_set_wash_mode(sts=isOn.On)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
    @allure.title("反例_Transport&&Convinience_MovgUp状态下_HndlOutd暂停后背门请求忽略")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992201(self):
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.CONVENIENCE, ccp={98:0x2}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgOut)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
       
    @allure.title("normal&&Convinience_MovgDwn状态下_HndlOutd暂停后背门")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992177(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={98:0x2}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgIn)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
        
       
    @allure.title("normal&&abandoned_MovgDwn状态下_HndlOutd暂停后背门")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992176(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED, ccp={98:0x80}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgIn)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
       
    @allure.title("normal&&Driving_MovgDwnBrkg状态下_HndlOutd暂停后背门")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992175(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={98:0x2}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgInBrkg)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
       
    @allure.title("factory&&INACTIVE_MovgDwnBrkg状态下_HndlOutd暂停后背门")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992174(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.INACTIVE, ccp={98:0x2}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgInBrkg)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
       
    @allure.title("Crash&&INACTIVE_MovgDwn状态下_HndlOutd暂停后背门")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992173(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.INACTIVE, ccp={98:0x2}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgIn)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
       
    @allure.title("Dyno&&Convinience_MovgDwnBrkg状态下_HndlOutd暂停后背门")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992172(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={98:0x2}) 
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgInBrkg)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Stop, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd)
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        
        
        
       
    @allure.title("反例_normal&&Convinience_MovgDwn状态下_洗车模式_HndlOutd暂停后背门请求忽略")  
    @pytest.mark.full
    @pytest.mark.a1202
    def test_tailgate_ctrl_caseid_1992171(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={98:0x2}) 
        self.soa.hmi_set_wash_mode(sts=isOn.On)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.MovgIn)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)  
    
        
 ##############################################################################
       
    @allure.title("657219 外开关禁用_洗车模式尾门外开关禁用")  
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1991614(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE) 
        self.soa.hmi_set_wash_mode(sts=isOn.On)
        sleep(.3) 

        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.02, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        sleep(.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc) 
        
        
####### 开始499022    
        
    @allure.title("normal&&Convinience_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x1&&CCP98=0x1）")
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992274(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE,ccp={97: 0x01, 98:0x1}) 
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        
        self.io.set_door(Trunk=Door.close)

        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  
        
        
        
    @allure.title("normal&&Inactive_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x1&&CCP98=0x2）")
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992273(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE,ccp={97: 0x01, 98:0x2}) 
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        
        self.io.set_door(Trunk=Door.close)

        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  

        
        
    @allure.title("normal&&Driving_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x1&&CCP98=0x3）")
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992272(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING,ccp={97: 0x01, 98:0x3}) 
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        
        self.io.set_door(Trunk=Door.close)

        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)   
        
        
        
    @allure.title("factory&&INACTIVE_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x1&&CCP98=0x4）")
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992271(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.INACTIVE,ccp={97: 0x01, 98:0x4}) 
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        
        self.io.set_door(Trunk=Door.close)

        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  

        
    @allure.title("Dyno&&Convinience_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x1&&CCP98=0x80）")
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992270(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE,ccp={97: 0x01, 98:0x80}) 
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        
        self.io.set_door(Trunk=Door.close)

        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  
        
        
        
    @allure.title("normal&&Convinience_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x2&&CCP98=0x1）")
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992269(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE,ccp={97: 0x02, 98:0x1}) 
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        
        self.io.set_door(Trunk=Door.close)

        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  


        
    @allure.title("normal&&Inactive_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x2&&CCP98=0x2）")
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992268(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE,ccp={97: 0x02, 98:0x2}) 
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        
        self.io.set_door(Trunk=Door.close)

        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  
                
        
    @allure.title("normal&&Driving_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x2&&CCP98=0x3）")
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992267(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING,ccp={97: 0x02, 98:0x3}) 
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        
        self.io.set_door(Trunk=Door.close)

        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  
        
        
    @allure.title("factory&&Convinience_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x2&&CCP98=0x4）")
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992266(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.INACTIVE,ccp={97: 0x02, 98:0x4}) 
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        
        self.io.set_door(Trunk=Door.close)

        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  
                    
        
    @allure.title("Dyno&&Convinience_在尾门解锁状态下_通过手动关闭尾门（CCP97=0x2&&CCP98=0x80）")
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992265(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE,ccp={97: 0x02, 98:0x80}) 
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        
        self.io.set_door(Trunk=Door.close)

        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  


    @allure.title("normal&&INACTIVE_在HMI开尾门情况下，通过手动关闭尾门_LockgCenStsTrigSrc=KeyRem_找到钥匙（CCP97=0x2&&CCP98=80）") 
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992264(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
       
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI, timeout=2)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.io.set_door(Trunk=Door.open)
        sleep(.5)
        
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])  # 尾门PE寻钥匙寻1区域
        sleep(.5)
        
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock)
        
        

    @allure.title("normal&&INACTIVE_在HMI开尾门情况下，通过手动关闭尾门_LockgCenStsTrigSrc=Keyls_钥匙没找到（CCP97=0x2&&CCP98=80）") 
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992263(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.KV_PEPS)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
       
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI, timeout=2)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.io.set_door(Trunk=Door.open)
        sleep(.5)
        
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0xB)])
        sleep(.5)
        
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        
        
        
    @allure.title("normal&&INACTIVE_在HMI开尾门情况下，通过手动关闭尾门_LockgCenStsTrigSrc=TmrAut_找到钥匙（CCP97=0x2&&CCP98=0x2）") #
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992262(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])  # 更新钥匙在车外区域
        time.sleep(32)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)

        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
       
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI, timeout=2)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.io.set_door(Trunk=Door.open)
        sleep(.5)
        

        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)]) 
        
        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock)
     
     
        
    @allure.title("normal&&INACTIVE_在HMI开尾门情况下，通过手动关闭尾门_LockgCenStsTrigSrc=Telm_找到钥匙（CCP97=0x2&&CCP98=0x2）")   
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992260(self):    
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.Telm)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
       
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI, timeout=2)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.io.set_door(Trunk=Door.open)
        sleep(.5)
        
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)]) 
        sleep(.5)
        
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock)
        
        

    # @allure.title("normal&&INACTIVE_在HMI开尾门情况下，硬线关闭尾门钥匙未遗留锁状态及锁源恢复上一个状态Apprch")    #待解决  换个台架测
    # @pytest.mark.full
    # @pytest.mark.a01202
    # def test_tailgate_ctrl_caseid_1992259(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x80}) 
    #     self.bus_comm.set_gear_pos(gear=Gear.Neut)
    #     self.soa.get_gear_level(gear=Gear.Neut)
        
        
    #     self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
    #     sleep(.2)  # 等待配置生效
    #     self.bus_comm.send_walk_away_lock_cmd()
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        

    #     self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
       
    #     self.soa.hmi_set_tailgate_mode(TailGateMode.Open)

    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI, timeout=2)
    #     sleep(1)
    #     self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
    #     self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
    #     self.io.set_door(Trunk=Door.open)
    #     sleep(.5)
        
    #     self.io.set_door(Trunk=Door.close)
    #     self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0xB)]) 
    #     sleep(.5)
        
    #     self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        
        
       
    @allure.title("normal&&INACTIVE_在HndlOutd开尾门情况下，通过手动关闭尾门_LockgCenStsTrigSrc=OutsOth_找到钥匙（CCP97=0x1&&CCP98=0x2）")  #
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992258(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.soa.get_gear_level(gear=Gear.Neut)
        
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd, timeout=2)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
            
        self.io.set_door(Trunk=Door.open)
        sleep(.5)
        
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])
        sleep(1)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn, act_sts=IndcrSts.LeAndRiOn)
        
        
        
       
    @allure.title("normal&&INACTIVE_在HndlOutd开尾门情况下，通过手动关闭尾门_LockgCenStsTrigSrc=NFC_钥匙没找到（CCP97=0x1&&CCP98=0x3）")  #
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992257(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x03, 94:0x80}) 
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC) 
        # self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.NFC)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])  # 尾门PE寻钥匙寻1区域
        sleep(.2)  # 等钥匙更新区域
        self.mix.push_door_outer_switch(DoorPos.Tailgate, time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHndlOutd, timeout=2)
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
            
        self.io.set_door(Trunk=Door.open)
        sleep(1)
        
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0xB)])  

        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)


 ###################   
    @allure.title("normal&&INACTIVE_在HMI开尾门情况下，通过手动关闭尾门_LockgCenStsTrigSrc=InsOth（CCP97=0x2&&CCP98=80）")    #pass
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992247(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x80})   #总线
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.2) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.io.set_door(Trunk=Door.open)
        sleep(.2)
        
        self.io.set_door(Trunk=Door.close)

        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off, act_sts=IndcrSts.Off)
        
    
    
    @allure.title("normal&&INACTIVE_在HMI开尾门情况下，通过手动关闭尾门_LockgCenStsTrigSrc=SpdAut（CCP97=0x2&&CCP98=0x2）")    
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992248(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x2})   #总线
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
         
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.bus_comm.set_vehspd(value=1.95)
        self.io.driver_seat_present()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", 2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)
        
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.2) 
        
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.io.set_door(Trunk=Door.open)
        sleep(.2)
        
        self.io.set_door(Trunk=Door.close)

        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)
 
    
    
    @allure.title("normal&&INACTIVE_在HMI开尾门情况下，通过手动关闭尾门_LockgCenStsTrigSrc=IntrSwt（CCP97=0x2&&CCP98=80）")    
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992249(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2, ccp={97: 0x02, 98:0x80})   #总线
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
         
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)     #设POT总线信号
        sleep(.2) 
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)

        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Open, trunk_trigsrc=TailgateTrigerSource.TrHMI) 
        sleep(1)
        self.bus_comm.check_door_opener_req_and_trigsrc(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Idle, trunk_trigsrc=TailgateTrigerSource.TrNoTrigSrc)
       
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        
        self.io.set_door(Trunk=Door.open)
        sleep(.2)
        
        self.io.set_door(Trunk=Door.close)

        sleep(.5)
        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)


        
    @allure.title("反例_normal&&Convinience_在尾门Clsd状态下_通过手动关闭尾门（CCP97=0x1&&CCP98=0x1）")
    @pytest.mark.full
    @pytest.mark.a01202
    def test_tailgate_ctrl_caseid_1992243(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE,ccp={97: 0x01, 98:0x1}) 
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        
        self.io.set_door(Trunk=Door.close)

        self.bus_comm.check_tailgate_lock_status(sterm_lock=LockSts2.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 
        
        
