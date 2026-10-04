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
class TestDoorOpenerCtrlAbc(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["CentralLockService_client",
                         "DoorService_client", 
                         "VehicleSetStatusService_client", 
                         "EntryService_client",
                         "KeyService_client",
                         ])
        sleep(2)

    def before_each_func(self, ecu):
        self.sd_tester.write_ccp(ccp={211: 0x01, 564: 0x2, 94: 0x80, 142:0x83, 10: 0x2})
        self.io.set_five_door_sts(Door.close)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        sleep(3)  # 防止开关触发热保护

    def after_each_func(self, ecu):
        sleep(2)

    def after_class(self, ecu):
        self.bus_comm.centrl_lock_pre_msg_send_ctrl(sts=MsgSendContrl.Start)
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
            # self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    @allure.title("484029 v2 Active模式下车辆非静止无开门请求不发Stop")
    @pytest.mark.smoke
    @pytest.mark.verify
    @pytest.mark.mcu_test
    def test_caseid_1983212(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_vehmtn(VehMtnSts.FwdVal1)
        sleep(.2)  # 大概发送3帧standstill==3
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Idle)
        sleep(.1)
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Idle)
        sleep(2)

    @allure.title("484029 v2 Active模式下车辆非静止主驾有开门请求主驾触发Stop")
    @pytest.mark.smoke
    def test_caseid_1983211(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open)
        self.bus_comm.set_vehmtn(VehMtnSts.FwdVal1)
        sleep(.1)  # 大概发送3帧standstill==3
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Stop, timeout=2)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Pass, door_req=DoorOpenerReq.Idle)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.RearLeft, door_req=DoorOpenerReq.Idle)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.RearRight, door_req=DoorOpenerReq.Idle)
        sleep(.2)
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Idle)
        

    @allure.title("Drving模式下车辆状态丢失有开门请求四门触发功能安全")
    @pytest.mark.smoke
    def test_caseid_1983213(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Open)
        self.bus_comm.set_vehmtn(VehMtnSts.Ukwn)
        sleep(.1)  # 大概发送3帧standstill==3
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Stop, timeout=2)  # 200ms四门同时拿不到
        sleep(.2)
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Idle)
            

    @allure.title("Drving模式下车辆静止有开门请求四门不发Stop")
    @pytest.mark.smoke
    @pytest.mark.mcu_test
    def test_caseid_1983324(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        sleep(.2)  # 大概发送3帧standstill==3
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Idle)
        sleep(.2)
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Idle)
        

    @allure.title("Active模式&&CarMode=Crash车辆状态丢失有开门请求不发Stop可以开门")
    @pytest.mark.sanity
    @pytest.mark.mcu_test
    def test_caseid_1983325(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Stop)
        sleep(15)  # Crash 车门15s处于Stop状态
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        self.bus_comm.set_vehmtn(VehMtnSts.Ukwn)
        sleep(.2)  # 发送3帧
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Idle)
        

    @allure.title("Convenience模式下车辆不触发功能安全")
    @pytest.mark.sanity
    @pytest.mark.mcu_test
    def test_caseid_1983214(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Open)
        self.bus_comm.set_vehmtn(VehMtnSts.Ukwn)
        sleep(.2)  # 大概发送3帧
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Idle)
        sleep(.2)
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Idle)
        

    @allure.title("Convenience模式下无开门动作车辆非静止不发Stop")
    @pytest.mark.smoke
    @pytest.mark.mcu_test
    def test_caseid_1983215(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        self.bus_comm.set_vehmtn(VehMtnSts.BackwVal1)
        sleep(.2)  # 大概发送3帧standstill==3
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Idle)
        sleep(.2)
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Idle)
        
    @allure.title("Drving模式下车辆非静止无开门请求四门不发Stop")
    @pytest.mark.sanity
    @pytest.mark.mcu_test
    def test_caseid_1983216(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_vehmtn(VehMtnSts.BackwVal2)
        sleep(.2)  # 大概发送3帧standstill==3
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle)
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Idle)
        # self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Stop)  #  不应该会有Stop发出
        

    @allure.title("484029 v2 ABONDONED模式下车辆非静止有开门请求四门不发Stop")
    @pytest.mark.sanity
    @pytest.mark.mcu_test
    def test_caseid_1983326(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open)
        self.bus_comm.set_vehmtn(VehMtnSts.BackwVal2)
        sleep(.2)  # 大概发送3帧standstill==3
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Idle)
        sleep(.2)
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Idle)   

    @allure.title("466494_HMI控制右前门open")
    @pytest.mark.smoke
    def test_caseid_115486(self):
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req=DoorOpenerReq.Open)
        self.bus_comm.check_door_trigger_source(door_pos=DoorId.kDoorFrontRight, trigger_source=DoorOpenSource.HMI)

    @allure.title("480418_HMI控制电动门关闭_右前门clsd")
    @pytest.mark.smoke
    def test_caseid_114408(self):
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req=DoorOpenerReq.Close)
        self.bus_comm.check_door_trigger_source(door_pos=DoorId.kDoorFrontRight, trigger_source=DoorOpenSource.HMI)

    @allure.title("480418_HMI控制电动门关闭_左前门clsd")
    @pytest.mark.smoke
    def test_caseid_114404(self):
        self.sd_tester.change_car_mode(car_mode=CarMode.NORMAL)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.io.set_five_door_sts(sts=Door.open)
        self.bus_comm.set_five_door_opener_sts(door_opener=DoorOpenerSts.FullOpend)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Close, trigger_src=DoorOpenSource.HMI)

    @allure.title("466210_电动侧门开启关闭状态监测_主驾门Open")
    @pytest.mark.smoke
    def test_caseid_115486(self):
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open, trigger_src=LockSource.HMI)

    @allure.title("466210_电动侧门开启关闭状态_副驾门开信号监测")
    @pytest.mark.smoke
    def test_caseid_114386(self):
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)

    @allure.title("Driving模式车辆静止_设置四门开_副驾门及左后门开信号监测")
    @pytest.mark.smoke
    def test_caseid_114384(self):
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)


    @allure.title("526240_内开关禁用_中控闭锁四门硬线开启四门内开关不禁用")
    @pytest.mark.full
    def test_caseid_114378(self):
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Close)
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Idle, trigger_src=LockTrigerSource.NoTrigSrc)
        self.io.set_five_door_sts(sts=Door.open)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Close)
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Close, trigger_src=LockSource.HMI)

    @allure.title("466494_HMI控制电动侧门开启_左前门clsd")
    @pytest.mark.smoke
    def test_caseid_114343(self):
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Close)
        self.bus_comm.check_door_trigger_source(door_pos=DoorId.kDoorFrontLeft, trigger_source=DoorOpenSource.HMI)

    @allure.title("466494_HMI控制电动侧门开启_右前门open")
    @pytest.mark.smoke
    def test_caseid_114299(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req=DoorOpenerReq.Close)
        self.bus_comm.check_door_trigger_source(door_pos=DoorId.kDoorFrontRight, trigger_source=DoorOpenSource.HMI)

    @allure.title("466494_HMI控制电动侧门开启_右后门open")
    @pytest.mark.sanity
    def test_caseid_114610(self):
        self.bus_comm.set_vehmtn(VehMtnSts.Ukwn)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req=DoorOpenerReq.Close)
        self.bus_comm.check_door_trigger_source(door_pos=DoorId.kDoorRearRight, trigger_source=DoorOpenSource.HMI)

    @allure.title("466494_HMI控制电动侧门开启_左后门open")
    @pytest.mark.sanity
    def test_caseid_114345(self):
        self.bus_comm.set_vehmtn(VehMtnSts.Ukwn)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req=DoorOpenerReq.Close)
        self.bus_comm.check_door_trigger_source(door_pos=DoorId.kDoorRearLeft, trigger_source=DoorOpenSource.HMI)

    @allure.title("466210_HMI控制电动侧门开启_All Door Open")
    @pytest.mark.sanity
    def test_caseid_114333(self):
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Open, trigger_src=LockSource.HMI)

    @allure.title("466210_HMI控制电动侧门开启_All Door Open")
    @pytest.mark.sanity
    def test_caseid_114333(self):
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Open, trigger_src=LockSource.HMI)

    @allure.title("HMI控制动力侧门_副驾门MovgOutBrkg过程中Stop")
    @pytest.mark.sanity
    def test_caseid_115753(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.MovgOutBrkg)
        sleep(.2)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req=DoorOpenerReq.Stop,
                                            trigger_src=DoorTrigerSource.HMI, timeout=2)

    @allure.title("466496_HMI控制动力侧门_主驾门MovgOut过程中Stop")
    @pytest.mark.sanity
    def test_caseid_1983534(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgOut)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Stop,
                                            trigger_src=LockSource.HMI)

    @allure.title("466496_HMI控制动力侧门_右后门MovgIn过程中Stop")
    @pytest.mark.sanity
    def test_caseid_1983535(self):
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.MovgIn)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req=DoorOpenerReq.Stop,
                                            trigger_src=LockSource.HMI)

    @allure.title("466496_HMI控制动力侧门_四门MovgInBrkg过程中Stop")
    @pytest.mark.sanity
    def test_caseid_1983536(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_five_door_opener_sts(door_opener=DoorOpenerSts.MovgInBrkg)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Stop)
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Stop, trigger_src=LockSource.HMI)

    @allure.title("466496_HMI控制动力侧门_非运动过程中，Stop忽略")
    @pytest.mark.sanity
    def test_caseid_1983537(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_five_door_opener_sts(door_opener=DoorOpenerSts.StopDurgOpen)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Stop)
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Idle, trigger_src=LockTrigerSource.NoTrigSrc)

    @allure.title("457939 v3 动力侧门不得无意打开_车辆静止&&CarMod==Drving有开门动作电释放请求On")
    @pytest.mark.sanity
    @pytest.mark.mcu_test
    def test_caseid_1980937(self):
        self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.soa.hmi_set_door_opener_sts(DoorId.kDoorAll, DoorOpenSts.Open)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.On, Pass=DoorRelsReq.On, ReLe=DoorRelsReq.On,
                                        RiRe=DoorRelsReq.On)

    @allure.title("457939 v3 动力侧门不得无意打开_车辆非静止&&CarMod==Active不发电释放请求")
    @pytest.mark.sanity
    @pytest.mark.mcu_test
    def test_caseid_1980938(self):
        self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
        self.mix.set_common_precontion(UsageMode.ACTIVE)  # standstill2
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal1)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off)

    @allure.title("457939 v3 动力侧门不得无意打开_车辆静止&&CarMod==Active&&CarMode=Crash发电释放请求")
    @pytest.mark.sanity
    def test_caseid_1983729(self):
        self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
        self.mix.set_common_precontion(UsageMode.ACTIVE, CarMode.CRASH)
        time.sleep(15)  # crash发生，15s门不可控
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off, Pass=DoorRelsReq.Off, ReLe=DoorRelsReq.Off,
                                        RiRe=DoorRelsReq.Off)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off, Pass=DoorRelsReq.Off, ReLe=DoorRelsReq.Off,
                                        RiRe=DoorRelsReq.On)

    @allure.title("457939 v3 侧门释放安全管理_stanstill状态丢失&&CarMod==Active&&CarMode=Crash发电释放请求")
    @pytest.mark.smoke
    @pytest.mark.mcu_test
    def test_caseid_114725(self):
        self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
        self.mix.set_common_precontion(UsageMode.ACTIVE, CarMode.CRASH)
        time.sleep(15)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off, Pass=DoorRelsReq.Off, ReLe=DoorRelsReq.Off,
                                        RiRe=DoorRelsReq.Off)
        self.bus_comm.set_vehmtn(VehMtnSts.Ukwn)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.On, Pass=DoorRelsReq.On, ReLe=DoorRelsReq.On,
                                        RiRe=DoorRelsReq.On)

    @allure.title("457939 v3 动力侧门不得无意打开_车辆非静止&&CarMod==Active&&CarMode=Crash发电释放请求")
    @pytest.mark.sanity
    @pytest.mark.mcu_test
    def test_caseid_1983538(self):
        self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
        self.mix.set_common_precontion(UsageMode.ACTIVE, CarMode.CRASH)
        time.sleep(15)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off, Pass=DoorRelsReq.Off, ReLe=DoorRelsReq.Off,
                                        RiRe=DoorRelsReq.Off)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal1)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off, Pass=DoorRelsReq.Off, ReLe=DoorRelsReq.Off,
                                        RiRe=DoorRelsReq.Off)

    @allure.title("动力侧门不得无意打开_车辆静止&&CarMod==Drving&&CarMode=Crash 不发电释放请求")
    @pytest.mark.sanity
    def test_caseid_1983730(self):
        self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.mix.set_common_precontion(UsageMode.ACTIVE, CarMode.CRASH)
        self.mix.set_common_precontion(UsageMode.DRIVING, CarMode.CRASH)
        time.sleep(15)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off, Pass=DoorRelsReq.Off, ReLe=DoorRelsReq.Off,
                                        RiRe=DoorRelsReq.Off)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off, Pass=DoorRelsReq.Off, ReLe=DoorRelsReq.Off,
                                        RiRe=DoorRelsReq.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        sleep(2)  # Crash 发生后过电动门安全状态

    @allure.title(" 动力侧门不得无意打开_车辆静止&&CarMod==CONVENIENCE&&CarMode=Crash发电释放请求")
    @pytest.mark.smoke
    def test_caseid_1983731(self):
        self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
        self.mix.set_common_precontion(UsageMode.ACTIVE, CarMode.CRASH)
        self.mix.set_common_precontion(UsageMode.CONVENIENCE, CarMode.CRASH)
        time.sleep(13)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off, Pass=DoorRelsReq.Off, ReLe=DoorRelsReq.Off,
                                        RiRe=DoorRelsReq.Off)
        time.sleep(2)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off, Pass=DoorRelsReq.Off, ReLe=DoorRelsReq.Off,
                                        RiRe=DoorRelsReq.Off)
        self.bus_comm.set_vehmtn(VehMtnSts.Ukwn)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.On, Pass=DoorRelsReq.On, ReLe=DoorRelsReq.On,
                                        RiRe=DoorRelsReq.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        sleep(2)  # Crash 发生后过电动门安全状态
        
    @allure.title(" _HMI控制动力侧门_副驾门MovgOutBrkg过程中Stop")
    @pytest.mark.full
    def test_caseid_115752(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal1)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.MovgIn)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req=DoorOpenerReq.Idle,
                                            trigger_src=LockTrigerSource.NoTrigSrc)

    @allure.title("HMI动力侧门移动中停止_Drving模式下standstill状态丢失车辆非静止Stop请求忽略")
    @pytest.mark.full
    def test_caseid_115744(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_vehmtn(VehMtnSts.Ukwn)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.MovgOut)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req=DoorOpenerReq.Idle,
                                            trigger_src=LockTrigerSource.NoTrigSrc)

    @allure.title("480418_HMI控制动力侧门关闭_车辆非静止关门请求忽略")
    @pytest.mark.full
    def test_caseid_115479(self):
        self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
        self.mix.set_common_precontion(UsageMode.ACTIVE)
        self.bus_comm.set_vehmtn(VehMtnSts.Ukwn)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Close)
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Idle, trigger_src=LockTrigerSource.NoTrigSrc)

    @allure.title("480418_HMI控制动力侧门关闭_车辆静止车身翻转角不在[+-0.20]范围内")
    @pytest.mark.full
    def test_caseid_114331(self):
        self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr13", "RollAgGlbQf_0_BcmVddmBackBoneSignalIPdu13", 1)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr13", "RollAgGlbVal_0_BcmVddmBackBoneSignalIPdu13", 0.25)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Close)
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Idle, trigger_src=LockTrigerSource.NoTrigSrc)  # 有timer
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr13", "RollAgGlbVal_0_BcmVddmBackBoneSignalIPdu13", 0)
        time.sleep(1)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Close)
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Close, trigger_src=LockSource.HMI)

    @allure.title("480418_HMI控制动力侧门关闭_车辆静止车身横摆角不在[+-0.20]范围内")
    @pytest.mark.full
    def test_caseid_115478(self):
        self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "RoadInclnQly", 1)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "RoadInclnRoadIncln", 0.25)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Close)
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Idle, trigger_src=LockTrigerSource.NoTrigSrc)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "RoadInclnRoadIncln", 0)
        time.sleep(1)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Close)
        self.bus_comm.check_four_door_opener_req(DoorOpenerReq.Close, trigger_src=LockSource.HMI)

    @allure.title("480418_HMI控制动力侧门关闭_关门过程中触发防夹")
    @pytest.mark.full
    def test_caseid_114412(self):
        self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrAntiPnch", 1)
        self.bus_comm.check_door_opener_req(drv_opener=DoorOpenerReq.Idle, trigger_src=LockTrigerSource.NoTrigSrc)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrAntiPnch", 0)

    @allure.title("497930 v2 Crash事件开关门请求动作监测_15s车门处于Stop")
    @pytest.mark.full
    @pytest.mark.mcu_test
    def test_caseid_1959801(self):
        self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.CRASH)
        time.sleep(11)
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Stop, trigger_src=LockTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off, Pass=DoorRelsReq.Off, ReLe=DoorRelsReq.Off,
                                        RiRe=DoorRelsReq.Off)
        time.sleep(4)
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Idle, trigger_src=LockTrigerSource.NoTrigSrc)

    @allure.title("657334_洗车模式激活_CDC联动五门全开校验关门请求是否发出")
    @pytest.mark.sanity
    def test_caseid_1980939(self):
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.io.set_five_door_sts(sts=Door.open)
        self.soa.hmi_set_wash_mode(isOn.On)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Close)
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Close, trigger_src=LockSource.HMI)
        self.soa.hmi_set_wash_mode(isOn.Off)

    @allure.title("505177_电动侧门释放_前置条件四门全开，电释放请求不发")
    @pytest.mark.full
    def test_caseid_115418(self):
        self.io.set_five_door_sts(sts=Door.open)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off, Pass=DoorRelsReq.Off, ReLe=DoorRelsReq.Off,
                                          RiRe=DoorRelsReq.Off)

    @allure.title("505177_动力侧门释放_右后门[FullyClsd]电释放请求监测")
    @pytest.mark.full
    def test_caseid_115417(self):
        self.io.set_five_door_sts(sts=Door.close)
        self.bus_comm.set_singal("bodycan", "RrdmBodyFr01", "DoorRiReLatPosn", 3)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_rels_req(RiRe=DoorRelsReq.On)
        sleep(.4)  #  500ms off
        self.bus_comm.check_door_rels_req(RiRe=DoorRelsReq.Off)

    @allure.title("505177_电动侧门释放_中控上锁RelsReq==OFF")
    @pytest.mark.full
    def test_caseid_115416(self):
        self.bus_comm.set_singal("bodycan", "RrdmBodyFr01", "DoorRiReLatPosn", 3)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off)
        sleep(.3)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off)

    @allure.title("505177_电动侧门释放_LatPosn=[Secondary position]_RelsReq==On")
    @pytest.mark.full
    def test_caseid_114726(self):
        self.bus_comm.set_singal("bodycan", "RrdmBodyFr01", "DoorRiReLatPosn", 2)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_rels_req(Pass=DoorRelsReq.On)
        sleep(.4)
        self.bus_comm.check_door_rels_req(Pass=DoorRelsReq.Off)

    @allure.title("505177_电动侧门释放_车窗未短降超时1800ms侧门不释放")
    @pytest.mark.full
    def test_caseid_114329(self):
        self.bus_comm.set_singal("bodycan", "RrdmBodyFr01", "DoorRiReLatPosn", 2)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open)
        self.bus_comm.set_singal("bodycan", "DdmBodyFr01", "ShortDropWinDrvrSts", 2)
        self.bus_comm.check_door_rels_req(Pass=DoorRelsReq.Off)
        time.sleep(2)
        self.bus_comm.check_door_rels_req(Pass=DoorRelsReq.Off)

    @allure.title("640621_HMI控制侧门释放_主驾门RelsReq==On")
    @pytest.mark.full
    def test_caseid_114328(self):
        self.bus_comm.set_singal("bodycan", "RrdmBodyFr01", "DoorRiReLatPosn", 2)
        self.soa.hmi_set_door_postion(DoorPos.Dirver, 10)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.On)
        time.sleep(.4)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off)

    @allure.title("640621_HMI控制侧门释放_左后门目标位置50_RelsReq==On")
    @pytest.mark.full
    def test_caseid_114325(self):
        self.bus_comm.set_singal("bodycan", "RrdmBodyFr01", "DoorRiReLatPosn", 2)
        self.soa.hmi_set_door_postion(DoorPos.RearLeft, 50)
        self.bus_comm.check_door_rels_req(ReLe=DoorRelsReq.On)
        time.sleep(.4)
        self.bus_comm.check_door_rels_req(ReLe=DoorRelsReq.Off)

    @allure.title("640621_HMI控制侧门释放_左后门目标位置101无效值_RelsReq==OFF")
    @pytest.mark.full
    def test_caseid_114323(self):
        self.bus_comm.set_singal("bodycan", "RrdmBodyFr01", "DoorRiReLatPosn", 2)
        self.soa.hmi_set_door_postion(DoorPos.RearLeft, 101)
        self.bus_comm.check_door_rels_req(ReLe=DoorRelsReq.Off)
        time.sleep(.4)
        self.bus_comm.check_door_rels_req(ReLe=DoorRelsReq.Off)

    # @allure.title("洗车模式未激活_HMI控制所有侧门Open")
    # @pytest.mark.sanity
    # def test_caseid_119088(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
    #     self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
    #     self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Open, trigger_src=LockSource.HMI)

    @allure.title("657334_洗车模式激活_外部开关短按小于2.5s开门请求忽略")
    @pytest.mark.sanity
    def test_caseid_119090(self):
        self.soa.hmi_set_wash_mode(isOn.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.mix.push_door_outer_switch(DoorPos.Dirver, 2)
        self.io.trigger_door_outswitch_sts(Drvr=OutSwitchPressSts.Press)
        time.sleep(2)
        self.io.trigger_door_outswitch_sts(Drvr=OutSwitchPressSts.NoPress)
        self.bus_comm.check_door_opener_req(drv_opener=DoorOpenerReq.Idle, trigger_src=LockTrigerSource.NoTrigSrc)
        self.soa.hmi_set_wash_mode(isOn.Off)

    @allure.title("489523_主驾门状态与质量因数_开启 OR 关闭")
    @pytest.mark.sanity
    def test_caseid_114291(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_driver_door_QF_sts(sts=FacQlyDoorSts.Open)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_driver_door_QF_sts(sts=FacQlyDoorSts.Close)

    # @allure.title("657334_打开电动门_洗车模式激活_外部开关长按2.5s主驾门开信号监测")
    # @pytest.mark.sanity_1
    # def test_caseid_114291(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal2)
    #     self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
    #     self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "RoadInclnQly", 0.10)
    #     self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr13", "RollAgGlbQf_0_BcmVddmBackBoneSignalIPdu13", 0.10)
       
        
    @allure.title("470583_电动门外部按键控制_左前门Clsd")
    @pytest.mark.sanity
    def test_caseid_115750(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr00", "EngSt1WdStsEngSt1WdSts", 8)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Opened, isopen=False, antipinch=False)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.2)
        # self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "DoorDrvrOpenReqOutdLogic", 1)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Close, door_trigsrc=DoorTrigerSource.OutdSwt)

    @allure.title("470583_电动门外部按键控制_右后门Clsd")
    @pytest.mark.sanity
    def test_caseid_115749(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr00", "EngSt1WdStsEngSt1WdSts", 8)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.StopDurgCls)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Hover,isopen=False, antipinch=False)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=0.2)
        # self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "DoorRiReOpenReqOutdLogic", 1)
        self.bus_comm.check_door_opener_req_and_trigsrc(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Close, door_trigsrc=DoorTrigerSource.OutdSwt)

    @allure.title("470582_电动门外部按键控制_左前门FullClsd_外按键控制左前门open")
    @pytest.mark.full
    def test_caseid_115747(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr00", "EngSt1WdStsEngSt1WdSts", 8)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Closed, isopen=False, antipinch=False)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.2)
        # self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "DoorDrvrOpenReqOutdLogic", 1)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.OutdSwt)

    @allure.title("470582_电动门外部按键控制_左前门HalfClsd_外按键控制左前门open")
    @pytest.mark.full
    def test_caseid_1986210(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr00", "EngSt1WdStsEngSt1WdSts", 8)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.HalfClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.HalfClosed, isopen=False, antipinch=False)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.2)
        # self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "DoorDrvrOpenReqOutdLogic", 1)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.OutdSwt)

    @allure.title("470582_电动门外部按键控制_左前门HalfClsd_外按键控制左前门open")
    @pytest.mark.full
    def test_caseid_1986211(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr00", "EngSt1WdStsEngSt1WdSts", 8)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.StopMinPntForCls)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Hover, isopen=False, antipinch=False)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.2)
        # self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "DoorDrvrOpenReqOutdLogic", 1)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.OutdSwt)

    @allure.title("466210 动力侧门运动状态_FullClsd||MovgOut||MovgOutBrkg||FullOpend")
    @pytest.mark.smoke
    def test_caseid_114389(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Closed, isopen=False, antipinch=False)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.MovgOut)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntRightDoorSts, doormovests=DoorMoveStatus.Opening, isopen=False, antipinch=False)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.MovgOutBrkg)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearLeftDoorSts, doormovests=DoorMoveStatus.OpeningBreak, isopen=False, antipinch=False)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullOpend)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Opened, isopen=False, antipinch=False)

    @allure.title("466210 动力侧门运动状态ukwn||HalfClsd||StopMinPntForCls")
    @pytest.mark.smoke
    def test_caseid_1986214(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.Ukwn)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.NA, isopen=False, antipinch=False)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.HalfClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntRightDoorSts, doormovests=DoorMoveStatus.HalfClosed, isopen=False, antipinch=False)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.StopMinPntForCls)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearLeftDoorSts, doormovests=DoorMoveStatus.Hover, isopen=False, antipinch=False)

    @allure.title("466210 动力侧门运动状态StopDurgOpen||MovgIn||MovgInBrkg||StopDurgCls||")
    @pytest.mark.smoke
    def test_caseid_1986212(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgOut)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Opening, isopen=False, antipinch=False)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.MovgOut)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntRightDoorSts, doormovests=DoorMoveStatus.Opening, isopen=False, antipinch=False)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.MovgOut)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearLeftDoorSts, doormovests=DoorMoveStatus.Opening, isopen=False, antipinch=False)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.MovgOut)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Opening, isopen=False, antipinch=False)

    @allure.title("466210 动力侧门运动状态_2：MovgOut")
    @pytest.mark.smoke
    def test_caseid_1986213(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.StopDurgOpen)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Hover, isopen=False, antipinch=False)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.MovgIn)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntRightDoorSts, doormovests=DoorMoveStatus.Closing, isopen=False, antipinch=False)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.MovgInBrkg)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearLeftDoorSts, doormovests=DoorMoveStatus.ClosingBreak, isopen=False, antipinch=False)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.StopDurgCls)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Hover,isopen=False, antipinch=False)

    @allure.title("电动门内部按键控制_MovgInBrkg状态左后门stop")
    @pytest.mark.smoke
    def test_caseid_115485(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgInBrkg)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.ClosingBreak, isopen=False, antipinch=False)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)  
        self.bus_comm.set_singal("bodycan", "DdmBodyFr04", "DoorDrvrOpenReqInsdSwt1", 1) 
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrOpenReqInsdSwt2", 1)   
        time.sleep(.2)
        self.bus_comm.set_singal("bodycan", "DdmBodyFr04", "DoorDrvrOpenReqInsdSwt1", 0) 
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Stop, door_trigsrc=DoorTrigerSource.InsdSwt)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrOpenReqInsdSwt2", 0)   

    @allure.title("470581_内部按键控制_MovgOutBrkg状态下左前门stop")
    @pytest.mark.smoke
    def test_caseid_115603(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgOutBrkg)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.OpeningBreak, isopen=False, antipinch=False)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)  
        self.bus_comm.set_singal("bodycan", "DdmBodyFr04", "DoorDrvrOpenReqInsdSwt1", 1) 
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrOpenReqInsdSwt2", 1)   
        time.sleep(.2)
        self.bus_comm.set_singal("bodycan", "DdmBodyFr04", "DoorDrvrOpenReqInsdSwt1", 0) 
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Stop, door_trigsrc=DoorTrigerSource.InsdSwt)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrOpenReqInsdSwt2", 0)   

    @allure.title("电动门内部按键控制_右后门clsd")
    @pytest.mark.full
    def test_caseid_115452(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.StopDurgCls)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)  
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Hover, isopen=False, antipinch=False)
        self.bus_comm.press_door_inside_switch(DoorPos.RearRight, time_interval=0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Close, door_trigsrc=DoorTrigerSource.InsdSwt)

    @allure.title("电动门内部按键控制_左后门clsd")
    @pytest.mark.sanity
    def test_caseid_115450(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullOpend)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearLeftDoorSts, doormovests=DoorMoveStatus.Opened, isopen=False, antipinch=False)
        self.bus_comm.press_door_inside_switch(DoorPos.RearLeft, time_interval=0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Close, door_trigsrc=DoorTrigerSource.InsdSwt)

    @allure.title("电动门内部按键控制_右前门clsd")
    @pytest.mark.full
    def test_caseid_115454(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.StopDurgCls)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0) 
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntRightDoorSts, doormovests=DoorMoveStatus.Hover, isopen=False, antipinch=False)
        self.bus_comm.press_door_inside_switch(DoorPos.Pass, time_interval=0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Close, door_trigsrc=DoorTrigerSource.InsdSwt)        

    @allure.title("电动门内部按键控制_左前门clsd")
    @pytest.mark.full
    def test_caseid_115451(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.StopDurgCls)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Hover, isopen=False, antipinch=False)
        self.bus_comm.press_door_inside_switch(DoorPos.Dirver, time_interval=0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Close, door_trigsrc=DoorTrigerSource.InsdSwt) 

    @allure.title("电动门内部按键控制_MovgOut状态右后门stop")
    @pytest.mark.sanity
    def test_caseid_115754(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.MovgOut)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0) 
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Opening, isopen=False, antipinch=False)
        self.bus_comm.press_door_inside_switch(DoorPos.RearRight, time_interval=0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Stop, door_trigsrc=DoorTrigerSource.InsdSwt) 

    @allure.title("478438 _电动门外部按键控制_MovgOut状态左前门stop")
    @pytest.mark.smoke
    def test_caseid_115757(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgOut)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0) 
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Opening, isopen=False, antipinch=False)
        self.bus_comm.press_door_inside_switch(DoorPos.Dirver, time_interval=0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Stop, door_trigsrc=DoorTrigerSource.InsdSwt) 
        
    @allure.title("501126 Door status_四门两盖状态IO控制")
    @pytest.mark.full
    def test_caseid_1986689(self):
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorDrvrSts", 2)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorLeReSts", 2)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorRiReSts", 2)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorPassSts", 2)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorDrvrSts", 1)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorPassSts", 1)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorLeReSts", 1)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorRiReSts", 1)
        self.io.set_five_door_sts(Door.close)

    @allure.title("501126 Door status_尾门及引擎盖状态")
    @pytest.mark.full
    def test_caseid_1986690(self):
        self.io.set_hood_sts(HoodSts.Close)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 2)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr25", "TrSts", 2)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 1)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr25", "TrSts", 1)
        self.io.set_hood_sts(HoodSts.Close)
        self.io.set_door(Trunk=Door.close)

    @allure.title("434377 主驾门状态_DoorDrvrStsWithFacQlyDoorSts")
    @pytest.mark.sanity
    def test_caseid_1986691(self):
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorDrvrSts", 2)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "DoorDrvrStsWithFacQlyDoorSts", 2)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorDrvrSts", 1)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "DoorDrvrStsWithFacQlyDoorSts", 1)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "DoorDrvrStsWithFacQlyDoorSts", 2)

    @allure.title("480095 HW-SW硬线开关交互")
    @pytest.mark.full
    @pytest.mark.mcu_test
    def test_caseid_1986692(self):
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "TrHndlOutdOpenSts", 0)
        self.io.trunk_door_release_switch_pressed()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "TrHndlOutdOpenSts", 1)
        self.io.trunk_door_release_switch_unpressed()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "TrHndlOutdOpenSts", 0)

    @allure.title("460918 HW-SW硬线开关交互_四门外开关控制")
    @pytest.mark.full
    @pytest.mark.mcu_test
    def test_caseid_1986693(self):
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "DoorDrvrOpenReqOutdLogic", 2)
        self.io.trigger_door_outswitch_sts(Drvr=OutSwitchPressSts.Press)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrOpenReqOutdSwt2", 1)   
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "DoorDrvrOpenReqOutdLogic", 1)  
        self.io.trigger_door_outswitch_sts(Drvr=OutSwitchPressSts.NoPress) 
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrOpenReqOutdSwt2", 2)   
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "DoorDrvrOpenReqOutdLogic", 2)  

    @allure.title("设置踩刹车自动关门启用_主驾Clsd")
    @pytest.mark.smoke
    def test_caseid_115758(self):
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)  
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0) 
        self.soa.hmi_set_and_get_braking_close_the_door(isOn=False)    
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)         
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Close, door_trigsrc=DoorTrigerSource.HMI, timeout=3) 
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)

    @allure.title("设置踩刹车自动关门禁用_主驾门无动作")
    @pytest.mark.smoke
    def test_caseid_114367(self):
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        self.soa.hmi_set_and_get_braking_close_the_door(isOn=True)             
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)    
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)      
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)

    @allure.title("电动门内部按键控制_MovgIn状态右前门stop")
    @pytest.mark.full
    def test_caseid_115487(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.MovgIn)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntRightDoorSts, doormovests=DoorMoveStatus.Closing, isopen=False, antipinch=False, time_wait=2)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0) 
        self.bus_comm.press_door_inside_switch(DoorPos.Pass, time_interval=0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Stop, door_trigsrc=DoorTrigerSource.InsdSwt, timeout=3) 

    # @allure.title("484152 内部开关Swt1和Swt2输入条件")
    # @pytest.mark.full
    # def test_caseid_1988695(self):
    #     self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
    #     self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)  
    #     self.bus_comm.press_door_inside_switch(DoorPos.Dirver, time_interval=0.3)
    #     self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "DoorDrvrOpenReqInsdLogic", 1) 
    #     self.bus_comm.set_singal("bodycan", "RpodBodyFr01", "DoorRiReOpenReqInsdSwt2", 1)   
    #     self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "DoorRiReOpenReqInsdLogic", 2) 

    @allure.title("左前门侧方开门保护状态触发_车门关闭阻力撤销")
    @pytest.mark.full
    def test_caseid_1989513(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.event_check_side_door_open_protection_sts(frontleft= True, frontrigiht= False, rearleft= False,rearright= False)
        self.io.set_door(Drvr=Door.close)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, frontrigiht= False, rearleft= False,rearright= False)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.SubtResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("右侧车门开门保护触发右侧车门关闭阻力撤销")
    @pytest.mark.full
    def test_caseid_1989512(self):
        self.io.set_door(Pass=Door.open, RiRe=Door.open)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.check_door_opener_req_and_trigsrc(pass_opener=DoorPos.Pass, rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, frontrigiht= False, rearleft= True,rearright= True)
        self.io.set_door(Pass=Door.close, RiRe=Door.close)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, frontrigiht= False, rearleft= False,rearright= False)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.SubtResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("右侧车门开门保护触发右侧车门预警消失计时2s阻力撤销")
    @pytest.mark.full
    def test_caseid_1989511(self):
        self.io.set_door(Pass=Door.open, RiRe=Door.open)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.check_door_opener_req_and_trigsrc(pass_opener=DoorPos.Pass, rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, frontrigiht= False, rearleft= True,rearright= True)
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.NoLcmaWarn, time_wait=2)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, frontrigiht= False, rearleft= False,rearright= False)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.SubtResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)


    @allure.title("两侧车门开门保护触发_两侧车门预警消失2s阻力撤销")
    @pytest.mark.full
    def test_caseid_1989510(self):
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, frontrigiht= False, rearleft= True,rearright= True)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.LcmaWarnLvl1, time_wait=2)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, frontrigiht= False, rearleft= False,rearright= False)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.SubtResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("左前门侧方开门保护触发车门延时2s后关闭阻力撤销")
    @pytest.mark.full
    def test_caseid_1989509(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.event_check_side_door_open_protection_sts(frontleft= True, frontrigiht= False, rearleft= False,rearright= False)
        self.io.set_door(Drvr=Door.close)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, frontrigiht= False, rearleft= False,rearright= False)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.SubtResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("右侧车门开门保护触发右侧车门预警消失计时不足2s阻力不撤销")
    @pytest.mark.full
    def test_caseid_1989508(self):
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.check_door_opener_req_and_trigsrc(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, frontrigiht= False, rearleft= False,rearright= True)
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.NoLcmaWarn, time_wait=0.7)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, frontrigiht= False, rearleft= False,rearright= True)
        self.bus_comm.check_without_door_resist_cmd(timeout=1.3)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("主驾内部方式先开门+左后外按键控制开门手动开门阻力监测")
    @pytest.mark.full
    def test_caseid_1989507(self):
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.mix.push_door_outer_switch(pos=DoorPos.RearLeft,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.OutdSwt) 
        self.bus_comm.check_without_door_resist_cmd()
        self.mix.set_and_check_door_resist_cmd(resist=ResistMode.DoorOpenWarning)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("外按键开启右后门触发开门告警后内按键开启右前门手动开门阻力监测")
    @pytest.mark.full
    def test_caseid_1989506(self):
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntRightDoorSts, doormovests=DoorMoveStatus.Closed, isopen=False, antipinch=False)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.OutdSwt) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_without_door_resist_cmd()
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc( rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI)
        self.bus_comm.check_without_door_resist_cmd()
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("车内方式开主驾触发开门预警后车内方式开左后手动开门阻力监测")
    @pytest.mark.full
    def test_caseid_1989505(self):
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc( lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.check_without_door_resist_cmd()
        self.mix.set_and_check_door_resist_cmd(resist=ResistMode.DoorOpenWarning)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("仅主驾门内部按键控制触发阻力控制")
    @pytest.mark.full
    def test_caseid_1989421(self):
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.press_door_inside_switch(DoorPos.Dirver, time_interval=0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.InsdSwt) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.mix.set_and_check_door_resist_cmd(resist=ResistMode.DoorOpenWarning)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("车内控制四门开&&两侧车门有障碍物_开门阻力触发两侧车门开门预警恢复后阻力撤销")
    @pytest.mark.smoke
    def test_caseid_1989651(self):
        self.io.set_five_door_sts(sts=Door.open)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.LcmaWarnLvl1, time_wait=2)        
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.SubtResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("两侧车门有障碍物_开门阻力触发四门关闭后阻力撤销")
    @pytest.mark.smoke
    def test_caseid_1989648(self):
        self.io.set_five_door_sts(sts=Door.open)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.io.set_five_door_sts(sts=Door.close)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.SubtResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("仅主驾门内部按键控制触发阻力控制")
    @pytest.mark.full
    def test_caseid_1989553(self):
        self.io.set_door(Drvr= Door.open, LeRe=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI, timeout=2) 
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc(lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI, timeout=2) 
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist, time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.mix.set_and_check_door_resist_cmd(resist=ResistMode.DoorOpenWarning)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("两侧车门先触发开门阻力后两侧开门预警消失_侧方开门保护恢复")
    @pytest.mark.full
    def test_caseid_1989552(self):
        self.io.set_door(Drvr= Door.open, Pass=Door.open, LeRe=Door.open, RiRe=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.event_check_side_door_open_protection_sts(frontleft= True, frontrigiht= True, rearleft= True,rearright= True)
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl1, time_wait=2)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, frontrigiht= False, rearleft= True,rearright= True)
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.LcmaWarnLvl1, time_wait=2)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, frontrigiht= False, rearleft= False,rearright= False)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.SubtResist, time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("左侧先触发开门阻力_左后及右前门开_左侧开门预警消失后侧方开门保护恢复")
    @pytest.mark.full
    def test_caseid_1989551(self):
        self.io.set_door(Pass=Door.open, LeRe=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc( pass_opener=DoorPos.Pass,lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI, timeout=2) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist, time_wait=1)
        self.soa.event_check_side_door_open_protection_sts(frontrigiht= False, rearleft= True)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl1, time_wait=2)
        self.soa.event_check_side_door_open_protection_sts(frontrigiht= False, rearleft= False)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.SubtResist, time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("两侧车门触发开门阻力_四门关闭侧方开门保护恢复")
    @pytest.mark.full
    def test_caseid_1989550(self):
        self.io.set_door(Drvr= Door.open, Pass=Door.open, LeRe=Door.open, RiRe=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI, timeout=2) 
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist, time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.event_check_side_door_open_protection_sts(frontleft= True, frontrigiht= True, rearleft= True,rearright= True)
        self.io.set_door(Drvr=Door.close)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, frontrigiht= True, rearleft= True,rearright= True)
        self.io.set_door(Pass=Door.close)
        time.sleep(2)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, frontrigiht= False, rearleft= True,rearright= True)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.io.set_door(LeRe=Door.close, RiRe=Door.close)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, frontrigiht= False, rearleft= False,rearright= False)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.SubtResist, time_wait=1)  # 1s置位
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("右侧触发开门阻力_右侧车门从开到关_侧方开门保护状态恢复")
    @pytest.mark.full
    def test_caseid_1989549(self):
        self.io.set_door(Pass=Door.open, RiRe=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.check_door_opener_req_and_trigsrc(pass_opener=DoorPos.Pass, rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist, time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.event_check_side_door_open_protection_sts(frontrigiht= True,rearright= True)
        self.io.set_door(Pass=Door.close)
        self.soa.event_check_side_door_open_protection_sts(frontrigiht= False,rearright= True)
        self.io.set_door(RiRe=Door.close)
        self.soa.event_check_side_door_open_protection_sts(frontrigiht= False,rearright= False)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.SubtResist, time_wait=1)  # 1s置位
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("右侧触发开门阻力_左前及右后门开启后关闭_侧方开门保护恢复")
    @pytest.mark.full
    def test_caseid_1989548(self):
        self.io.set_door(Drvr=Door.open, RiRe=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver,rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist, time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.event_check_side_door_open_protection_sts(frontleft= True,rearright= True)
        self.io.set_door(Drvr=Door.close)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, rearright= True)
        self.io.set_door(RiRe=Door.close)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, rearright= False)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.SubtResist, time_wait=1)  # 1s置位
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("四门开两侧车门触发阻力_仅单侧车门预警消失及单侧车门关闭_侧方开门保护不恢复四门关闭后恢复")
    @pytest.mark.full
    def test_caseid_1989546(self):
        self.io.set_door(Drvr= Door.open, Pass=Door.open, LeRe=Door.open, RiRe=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.event_check_side_door_open_protection_sts(frontleft= True, frontrigiht= True, rearleft= True,rearright= True)
        self.io.set_door(Drvr= Door.close, LeRe=Door.close)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, frontrigiht= True, rearleft= False,rearright= True)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, frontrigiht= False, rearleft= True,rearright= True)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle, time_wait=1)
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.LcmaWarnLvl1, time_wait=2)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False, frontrigiht= False, rearleft= False,rearright= False)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle, time_wait=2)  # 四门未全关不发撤销阻力
        self.io.set_door(Pass= Door.close, RiRe=Door.close)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.SubtResist, time_wait=1)  # 1s置位
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("车门阻力控制功能需求_左侧右侧flag置位1_左右两测分别触发开门告警-触发开门阻力")
    @pytest.mark.full
    def test_caseid_1989543(self):
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc( pass_opener=DoorPos.Pass,lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI, timeout=2) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.mix.set_and_check_door_resist_cmd(resist=ResistMode.DoorOpenWarning)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("内按键仅左后门触发阻力控制")
    @pytest.mark.full
    def test_caseid_1989536(self):
        self.bus_comm.set_singal("bodycan", "RldmBodyFr01", "ChdLockLeftSts", 2) 
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.press_door_inside_switch(pos= DoorPos.RearLeft, time_interval= 0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.InsdSwt) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.mix.set_and_check_door_resist_cmd(resist=ResistMode.DoorOpenWarning)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        
    @allure.title("副驾门车内语音控制指定开度触发阻力")
    @pytest.mark.full
    def test_caseid_1989527(self):
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.set_door_perc_position(doorpos= DoorPos.Pass, perc_position=0)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_postion(door_pos= DoorPos.Pass, pos= 10, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=10, door_trigsrc=DoorOpenSource.NoTrigSrc)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=101, door_trigsrc=DoorOpenSource.NoTrigSrc)
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.mix.set_and_check_door_resist_cmd(resist=ResistMode.DoorOpenWarning)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("内按键仅右前门触发阻力控制")
    @pytest.mark.full
    def test_caseid_1989535(self):
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.press_door_inside_switch(pos= DoorPos.Pass, time_interval= 0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.InsdSwt) 
        self.bus_comm.check_door_opener_req_and_trigsrc(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.mix.set_and_check_door_resist_cmd(resist=ResistMode.DoorOpenWarning)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("内按键仅右后门触发阻力控制")
    @pytest.mark.full
    def test_caseid_1989534(self):
        self.bus_comm.set_singal("bodycan", "RrdmBodyFr01", "ChdLockRightSts", 2) 
        self.bus_comm.set_child_lock_sts(side=Side.Right, childlockstatus=OnOffSafe1.OnOffSafeOff)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.bus_comm.press_door_inside_switch(pos= DoorPos.RearRight, time_interval= 0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.InsdSwt) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.mix.set_and_check_door_resist_cmd(resist=ResistMode.DoorOpenWarning)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("主驾门车内语音控制触发阻力")
    @pytest.mark.full
    def test_caseid_1989533(self):
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist, time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.event_check_side_door_open_protection_sts(frontleft= False)
        self.mix.set_and_check_door_resist_cmd(resist=ResistMode.DoorOpenWarning)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("左后门车内语音控制触发阻力")
    @pytest.mark.full
    def test_caseid_1989532(self):
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc( lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist, time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.event_check_side_door_open_protection_sts(rearleft= False)
        self.mix.set_and_check_door_resist_cmd(resist=ResistMode.DoorOpenWarning)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        
    @allure.title("副驾车内语音控制触发阻力")
    @pytest.mark.full
    def test_caseid_1989531(self):
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc( pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist, time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.event_check_side_door_open_protection_sts(rearright= False)
        self.mix.set_and_check_door_resist_cmd(resist=ResistMode.DoorOpenWarning)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("右后门车内语音控制触发阻力")
    @pytest.mark.full
    def test_caseid_1989530(self):
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc( rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist, time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.event_check_side_door_open_protection_sts(rearright= False)
        self.mix.set_and_check_door_resist_cmd(resist=ResistMode.DoorOpenWarning)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        
    @allure.title("同时触发开门告警触发阻力")
    @pytest.mark.full
    def test_caseid_1989523(self):
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc( rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist, time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.event_check_side_door_open_protection_sts(frontleft=False, frontrigiht= False, rearleft=False, rearright= False)
        self.mix.set_and_check_door_resist_cmd(resist=ResistMode.DoorOpenWarning)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("主驾门车内语音控制指定开度触发阻力")
    @pytest.mark.full
    def test_caseid_1989529(self):
        self.bus_comm.set_door_perc_position(doorpos= DoorPos.Dirver, perc_position=0)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_postion(door_pos= DoorPos.Dirver, pos= 10, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Dirver, position=10, door_trigsrc=DoorOpenSource.NoTrigSrc)
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.mix.set_and_check_door_resist_cmd(resist=ResistMode.DoorOpenWarning)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("左后门车内语音控制指定开度触发阻力")
    @pytest.mark.full
    def test_caseid_1989528(self):
        self.bus_comm.set_door_perc_position(doorpos= DoorPos.RearLeft, perc_position=0)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_postion(door_pos= DoorPos.RearLeft, pos= 10, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearLeft, position=10, door_trigsrc=DoorOpenSource.NoTrigSrc)
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.mix.set_and_check_door_resist_cmd(resist=ResistMode.DoorOpenWarning)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        
    @allure.title("右后门车内语音控制指定开度触发阻力")
    @pytest.mark.full
    def test_caseid_1989526(self):
        self.io.set_door(Pass= Door.open)
        self.bus_comm.set_door_perc_position(doorpos= DoorPos.RearRight, perc_position=0)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_postion(door_pos= DoorPos.RearRight, pos= 10, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearRight, position=10, door_trigsrc=DoorOpenSource.NoTrigSrc)
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.mix.set_and_check_door_resist_cmd(resist=ResistMode.DoorOpenWarning)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("主驾门+右后门开左侧车门预警触发阻力")
    @pytest.mark.full
    def test_caseid_1989525(self):
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver,door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver,rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.mix.set_and_check_door_resist_cmd(resist=ResistMode.DoorOpenWarning)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        
    @allure.title("副驾门+左后门开左侧车门预警触发阻力")
    @pytest.mark.full
    def test_caseid_1989524(self):
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc(lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.check_door_opener_req_and_trigsrc( pass_opener=DoorPos.Pass,lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.AddResist,time_wait=1)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.mix.set_and_check_door_resist_cmd(resist=ResistMode.DoorOpenWarning)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        
    @allure.title("主驾门外按键控制开不触发阻力")
    @pytest.mark.full
    def test_caseid_1989522(self):
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.mix.set_inside_open_door_flag(scene=VehicleInsideOutside.VehicleOutSide)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.OutdSwt) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_without_door_resist_cmd()
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("右后门车外语音控制不触发阻力")
    @pytest.mark.full
    def test_caseid_1989521(self):
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.mix.set_inside_open_door_flag(scene=VehicleInsideOutside.VehicleOutSide)  # 防止上一条case flag未清除
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleOutSide)
        self.bus_comm.check_door_opener_req_and_trigsrc( rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_without_door_resist_cmd()
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("左后门车外语音控制指定开度不触发阻力")
    @pytest.mark.full
    def test_caseid_1989520(self):
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.mix.set_inside_open_door_flag(scene=VehicleInsideOutside.VehicleOutSide)
        self.bus_comm.set_door_perc_position(doorpos= DoorPos.RearLeft, perc_position=0)
        self.bus_comm.set_door_perc_position(doorpos= DoorPos.RearRight, perc_position=0)
        self.soa.hmi_set_door_postion(door_pos= DoorPos.RearRight, pos= 10, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearRight, position=10, door_trigsrc=DoorOpenSource.NoTrigSrc)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_postion(door_pos= DoorPos.RearLeft, pos= 10, scene=VehicleInsideOutside.VehicleOutSide)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearLeft, position=10, door_trigsrc=DoorOpenSource.NoTrigSrc)
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_without_door_resist_cmd()
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("车外语音控制四门开左侧触发告警无阻力")
    @pytest.mark.full
    def test_caseid_1989519(self):
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.mix.set_inside_open_door_flag(scene=VehicleInsideOutside.VehicleOutSide)
        self.bus_comm.set_door_perc_position(doorpos= DoorPos.All, perc_position=0)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_postion(door_pos= DoorId.kDoorAll, pos= 10, scene=VehicleInsideOutside.VehicleOutSide)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Dirver, position=10, door_trigsrc=DoorOpenSource.NoTrigSrc)
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_without_door_resist_cmd()
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("车外语音控制四门开两侧触发告警无阻力")
    @pytest.mark.full
    def test_caseid_1989518(self):
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.mix.set_inside_open_door_flag(scene=VehicleInsideOutside.VehicleOutSide)
        self.bus_comm.set_door_perc_position(doorpos= DoorPos.RearLeft, perc_position=0)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_postion(door_pos= DoorId.kDoorAll, pos= 10, scene=VehicleInsideOutside.VehicleOutSide)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Dirver, position=10, door_trigsrc=DoorOpenSource.NoTrigSrc, timeout=2)
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_without_door_resist_cmd()
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("车内语音控制四门开开门告警无跳变无阻力")
    @pytest.mark.full
    def test_caseid_1989517(self):
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.LcmaWarnLvl2)
        self.mix.set_inside_open_door_flag(scene=VehicleInsideOutside.VehicleOutSide)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc( rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_without_door_resist_cmd()
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("左侧开门Flag=1&&右侧车门触发告警_无阻力")
    @pytest.mark.full
    def test_caseid_1989516(self):
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.mix.set_inside_open_door_flag(scene=VehicleInsideOutside.VehicleOutSide)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Open, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc( lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_without_door_resist_cmd()
        self.bus_comm.set_door_open_warn_sts(side=Side.Right, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("车内语音控制四门关闭_无阻力")
    @pytest.mark.full
    def test_caseid_1989515(self):
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.mix.set_inside_open_door_flag(scene=VehicleInsideOutside.VehicleOutSide)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Close, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc( rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Close, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_without_door_resist_cmd()
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("车内语音控制四门暂停&&触发开门告警_无阻力")
    @pytest.mark.full
    def test_caseid_1989514(self):
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.mix.set_inside_open_door_flag(scene=VehicleInsideOutside.VehicleOutSide)
        self.bus_comm.set_four_door_opener_sts(door_opener=DoorOpenerSts.MovgInBrkg)
        self.bus_comm.check_door_open_resistcmd_sts(resistcmd=DoorOpenResistCmd.Idle)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Stop, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_opener_req_and_trigsrc( lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Stop, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_without_door_resist_cmd()
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("车门阻力控制功能需求_PE解锁开门无阻力")
    @pytest.mark.full
    def test_caseid_1989503(self):
        self.mix.set_common_precontion(ccp={94: 0x80})
        self.mix.set_inside_open_door_flag(scene=VehicleInsideOutside.VehicleOutSide)  # 默认flag == 1有阻力先清除阻力
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.2)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, trigger_src=DoorTrigerSource.OutdSwt, timeout=5) 
        self.bus_comm.set_door_open_warn_sts(side=Side.Left, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_without_door_resist_cmd()
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("车门阻力控制功能需求_近车解锁开门")
    @pytest.mark.full
    def test_caseid_1989502(self):
        self.mix.set_inside_open_door_flag(scene=VehicleInsideOutside.VehicleOutSide)  # 默认flag == 1有阻力先清除阻力
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.NoLcmaWarn)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        sleep(.5)  # 等待配置生效
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7, valid=Validity.Valid)
        sleep(1)  # 等待前置条件生效
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, trigger_src=DoorTrigerSource.KeyRem, timeout=5) 
        self.bus_comm.set_door_open_warn_sts(side=Side.All, warn= LcmaIndcn.LcmaWarnLvl2)
        self.bus_comm.check_without_door_resist_cmd()
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7, valid=Validity.NotValid)

    @allure.title("控制动力侧门_车门开启指定角度联动内按键开门触发源校验")
    @pytest.mark.sanity
    def test_caseid_1994618(self):
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)  
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Pass, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=101, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        sleep(.5)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Pass, time_interval=0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc( pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.InsdSwt) 
        self.bus_comm.check_door_opener_req_and_trigsrc( pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("控制动力侧门_车门开启指定角度联动外按键开门触发源校验")
    @pytest.mark.sanity
    def test_caseid_1994619(self):
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)  
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Pass, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=101, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        sleep(.5)
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.OutdSwt)   
        self.bus_comm.check_door_opener_req_and_trigsrc( pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("503044 控制动力侧门_组合场景车门动作请求及触发源监测")
    @pytest.mark.full
    def test_caseid_1994617(self):
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc( pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.check_door_opener_req_and_trigsrc( pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Pass, time_interval=0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc( pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.InsdSwt) 
        self.bus_comm.check_door_opener_req_and_trigsrc( pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.io.set_door(Pass=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)  # 开门导致UsageMode上切
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.KeyRem, timeout=5)  # 闭锁联动关门有延时
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc)  
        self.io.set_door(Pass=Door.close)
        self.bus_comm.set_door_perc_position(doorpos=DoorPos.Pass, perc_position=0, timeout=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)   
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Pass, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=101, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)   
        sleep(.5)
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_opener_req_and_trigsrc(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.OutdSwt) 
        self.bus_comm.check_door_opener_req_and_trigsrc( pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.io.set_door(Pass=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)  # 开门导致UsageMode上切
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.Telm, timeout=5) 
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc) 
        self.io.set_door(Pass=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)  
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
