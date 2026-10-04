#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_extilight.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/9 11:30
@Description: BGM车控车设外灯
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
@allure.story("后视镜功能")
class TestExltlightCtrlABC(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["LightService_client","CentralLockService_client","DoorService_client"])
        self.sd_tester.write_ccp(ccp={142: 0x83})
        sleep(2)

    def before_each_func(self, ecu):
        self.soa.start_get_light_inhibit_sts()
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()

    def after_each_func(self, ecu):
        self.soa.stop_get_light_inhibit_sts()
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)
        sleep(1)

    def after_class(self, ecu):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)

    def set_centrllock_to_lock(self):
        self.mix.set_all_seats_present_sts(seat_pres_sts=SeatPresSts.NoPres)
        self.io.set_five_door_sts(Door.close)
        # 设置bodycan上五个电动门均关闭
        self.bus_comm.set_door_opener_sts(DoorOpenerSts.FullClsd)
        self.io.trigger_all_doors_outswitch(OutSwitchPressSts.NoPress)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.NFC)
        sleep(1)
        cen_lock_sts = self.bus_comm.get_central_lock_sts()
        if cen_lock_sts == 1:
            logger.info(f"当前的中控锁状态为UnLock,需要先落锁再执行后续操作")
            self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.NFC)
            sleep(1)
            cen_lock_sts = self.bus_comm.get_central_lock_sts()
            if cen_lock_sts == 3:
                logger.info(f"当前的中控锁状态是否为Lock,闭锁成功")
            else:
                logger.info(f"当前的中控锁状态仍为UnLock,RKE闭锁失败")
        else:
            logger.info(f"当前的中控锁状态为Lock,不需要先落锁,可以直接执行后续操作")

    def check_outer_door_always_on_off(self,pos:DoorPos,OnOrOff:YesOrNo,last_time:Union[int,float]):
        if pos.name == "Dirver":
            result_ori_dri = self.bus_comm.ipdu.check_signal(self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightDrvrSwLight', last_time)
            logger.info(f"获取{last_time}秒内的StatusOfOuterDoorSwLightDrvrSwLight原始数据是:{result_ori_dri}")
            check_result = check_all_value_is(result_ori_dri, OnOrOff.value)
            logger.info(f"Check 结果是：{check_result}")
        elif pos.name == "Pass":
            result_ori_pass = self.bus_comm.ipdu.check_signal(self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightPassSwLight', last_time)
            logger.info(f"获取{last_time}秒内的StatusOfOuterDoorSwLightPassSwLight原始数据是:{result_ori_pass}")
            check_result = check_all_value_is(result_ori_pass, OnOrOff.value)
            logger.info(f"Check 结果是：{check_result}")
        elif pos.name == "RearLeft":
            result_ori_rl = self.bus_comm.ipdu.check_signal(self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightLeReSwLight', last_time)
            logger.info(f"获取{last_time}秒内的StatusOfOuterDoorSwLightLeReSwLight原始数据是:{result_ori_rl}")
            check_result = check_all_value_is(result_ori_rl, OnOrOff.value)
            logger.info(f"Check 结果是：{check_result}")
        elif pos.name == "RearRight":
            result_ori_rr = self.bus_comm.ipdu.check_signal(self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightRiReSwLight', last_time)
            logger.info(f"获取{last_time}秒内的StatusOfOuterDoorSwLightRiReSwLight原始数据是:{result_ori_rr}")
            check_result = check_all_value_is(result_ori_rr, OnOrOff.value)
            logger.info(f"Check 结果是：{check_result}")
        elif pos.name == "All":
            result_ori_dri = self.bus_comm.ipdu.check_signal(self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightDrvrSwLight', last_time)
            result_ori_pass = self.bus_comm.ipdu.check_signal(self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightPassSwLight', last_time)
            result_ori_rl = self.bus_comm.ipdu.check_signal(self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightLeReSwLight', last_time)
            result_ori_rr = self.bus_comm.ipdu.check_signal(self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightRiReSwLight', last_time)
            logger.info(f"获取{last_time}秒内的原始数据result_ori_dri:{result_ori_dri},result_ori_pass:{result_ori_pass},result_ori_rl{result_ori_rl},result_ori_rr:{result_ori_rr}")
            check_result_ori_dri = check_all_value_is(result_ori_dri, OnOrOff.value)
            logger.info(f"Check 结果是：{check_result_ori_dri}")
            check_result_ori_pass = check_all_value_is(result_ori_pass, OnOrOff.value)
            logger.info(f"Check 结果是：{check_result_ori_pass}")
            check_result_ori_rl = check_all_value_is(result_ori_rl, OnOrOff.value)
            logger.info(f"Check 结果是：{check_result_ori_rl}")
            check_result_ori_rr = check_all_value_is(result_ori_rr, OnOrOff.value)
            logger.info(f"Check 结果是：{check_result_ori_rr}")
            
    def push_door_outer_switch(self,pos:DoorPos = DoorPos.Dirver,time_interval:Union[int,float] = 2.5,pe_test:bool = False):
        if pe_test == False:
            self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])
            sleep(2)

        prompt_info = f"触发模拟按{pos.name}门外开关"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if pos.name == "Dirver":
                self.bus_comm.set("bodycan","DpodBodyFr01", "DoorDrvrOpenReqOutdSwt2", 1)
                self.bus_comm.set("bodycan","IpmBodyFr01", "DoorDrvrOpenReqOutdSwt3", 1)
                self.io.trigger_door_outswitch_sts(Drvr=OutSwitchPressSts.Press)
                sleep(time_interval)

            elif pos.name == "Pass":
                self.bus_comm.set("bodycan","PpodBodyFr01", 'DoorPassOpenReqOutdSwt2', 1)
                self.bus_comm.set("bodycan","IpmBodyFr01", "DoorPassOpenReqOutdSwt3", 1)
                self.io.trigger_door_outswitch_sts(Pass =OutSwitchPressSts.Press)
                sleep(time_interval)

            elif pos.name == "RearLeft":
                self.bus_comm.set("bodycan","LpodBodyFr01", 'DoorLeReOpenReqOutdSwt2', 1)
                self.bus_comm.set("bodycan","IpmBodyFr01", "DoorLeReOpenReqOutdSwt3", 1)
                self.io.trigger_door_outswitch_sts(LeRe =OutSwitchPressSts.Press)
                sleep(time_interval)

            elif pos.name == "RearRight":
                self.bus_comm.set("bodycan","RpodBodyFr01", 'DoorRiReOpenReqOutdSwt2', 1)
                self.bus_comm.set("bodycan","IpmBodyFr01", "DoorRiReOpenReqOutdSwt3", 1)
                self.io.trigger_door_outswitch_sts(RiRe =OutSwitchPressSts.Press)
                sleep(time_interval)

            elif pos.name == "Tailgate":
                self.io.trigger_door_outswitch_sts(Trunk = OutSwitchPressSts.Press)
                time.sleep(time_interval)
                
    def release_door_outer_switch(self,pos:DoorPos = DoorPos.Dirver,pe_test:bool = False):
        if pe_test == False:
            self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])
            sleep(2)

        prompt_info = f"触发模拟按{pos.name}门外开关"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if pos.name == "Dirver":
                self.bus_comm.set("bodycan","DpodBodyFr01", "DoorDrvrOpenReqOutdSwt2", 2)
                self.bus_comm.set("bodycan","IpmBodyFr01", "DoorDrvrOpenReqOutdSwt3", 0)
                self.io.trigger_door_outswitch_sts(Drvr=OutSwitchPressSts.NoPress)

            elif pos.name == "Pass":
                self.bus_comm.set("bodycan","PpodBodyFr01", 'DoorPassOpenReqOutdSwt2', 2)
                self.bus_comm.set("bodycan","IpmBodyFr01", "DoorPassOpenReqOutdSwt3", 0)
                self.io.trigger_door_outswitch_sts(Pass =OutSwitchPressSts.NoPress)

            elif pos.name == "RearLeft":
                self.bus_comm.set("bodycan","LpodBodyFr01", 'DoorLeReOpenReqOutdSwt2', 2)
                self.bus_comm.set("bodycan","IpmBodyFr01", "DoorLeReOpenReqOutdSwt3", 0)
                self.io.trigger_door_outswitch_sts(LeRe =OutSwitchPressSts.NoPress)

            elif pos.name == "RearRight":
                self.bus_comm.set("bodycan","RpodBodyFr01", 'DoorRiReOpenReqOutdSwt2', 2)
                self.bus_comm.set("bodycan","IpmBodyFr01", "DoorRiReOpenReqOutdSwt3", 0)
                self.io.trigger_door_outswitch_sts(RiRe =OutSwitchPressSts.NoPress)

            elif pos.name == "Tailgate":
                self.io.trigger_door_outswitch_sts(Trunk=OutSwitchPressSts.NoPress)

    # def check_outer_door_light_flash(self,pos:DoorPos,sts:isOn,last_time:int):
    #     start_time = time.time()
    #     logger.info(f"----------->Check Start{start_time}")
    #     for num in range(last_time):
    #         if sts.name == "On":
    #             if pos.name == "Dirver":
    #                 self.bus_comm.check_door_switch_light_sts(pos=DoorPos.Dirver,req=LampSts.On)
    #                 self.bus_comm.check_door_switch_light_sts(pos=DoorPos.Pass,req=LampSts.Off)
    #                 self.bus_comm.check_door_switch_light_sts(pos=DoorPos.RearLeft,req=LampSts.Off)
    #                 self.bus_comm.check_door_switch_light_sts(pos=DoorPos.RearRight,req=LampSts.Off)
    #             elif pos.name == "Pass":
    #                 self.bus_comm.check_door_switch_light_sts(pos=DoorPos.Dirver,req=LampSts.Off)
    #                 self.bus_comm.check_door_switch_light_sts(pos=DoorPos.Pass,req=LampSts.On)
    #                 self.bus_comm.check_door_switch_light_sts(pos=DoorPos.RearLeft,req=LampSts.Off)
    #                 self.bus_comm.check_door_switch_light_sts(pos=DoorPos.RearRight,req=LampSts.Off)
    #             elif pos.name == "RearLeft":
    #                 self.bus_comm.check_door_switch_light_sts(pos=DoorPos.Dirver,req=LampSts.Off)
    #                 self.bus_comm.check_door_switch_light_sts(pos=DoorPos.Pass,req=LampSts.Off)
    #                 self.bus_comm.check_door_switch_light_sts(pos=DoorPos.RearLeft,req=LampSts.On)
    #                 self.bus_comm.check_door_switch_light_sts(pos=DoorPos.RearRight,req=LampSts.Off)
    #             elif pos.name == "RearRight":
    #                 self.bus_comm.check_door_switch_light_sts(pos=DoorPos.Dirver,req=LampSts.Off)
    #                 self.bus_comm.check_door_switch_light_sts(pos=DoorPos.Pass,req=LampSts.Off)
    #                 self.bus_comm.check_door_switch_light_sts(pos=DoorPos.RearLeft,req=LampSts.Off)
    #                 self.bus_comm.check_door_switch_light_sts(pos=DoorPos.RearRight,req=LampSts.On)
    #             elif pos.name == "All":
    #                 self.bus_comm.check_door_switch_light_sts(pos=DoorPos.All,req=LampSts.On)

    #             self.bus_comm.check_door_switch_light_sts(pos=DoorPos.All,req=LampSts.Off)
                
    #         if sts.name == "Off":
    #             self.bus_comm.check_door_switch_light_sts(pos=DoorPos.All,req=LampSts.Off)
    #             sleep(0.3)
            
    #     stop_time = time.time()
    #     logger.info(f"----------->Check Stop{stop_time}")
    #     test_duration = stop_time - start_time 
    #     logger.info(f"----------->Check 信号跳变执行时间{test_duration},时间差为{test_duration - last_time}")
    #     if abs(test_duration - last_time) > 2:
    #         assert False
 
    @allure.title("主驾车门PE闭锁，（主驾）门板指示灯闪烁")
    @pytest.mark.smoke
    def test_caseid_1985899(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone2,sts=BLEKeyPrsntSts.Valid)
        self.io.set_hood_sts(HoodSts.Close)
        self.io.set_door(Drvr=Door.open)
        self.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.Dirver,req=LampSts.On)
        sleep(.3)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.Dirver,req=LampSts.Off)
        self.release_door_outer_switch(pos=DoorPos.Dirver)

    
    @allure.title("左后车门PE闭锁，（左后）门板指示灯闪烁")
    @pytest.mark.smoke
    @pytest.mark.new
    def test_caseid_1985901(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone2,sts=BLEKeyPrsntSts.Valid)
        self.io.set_hood_sts(HoodSts.Close)
        self.io.set_door(LeRe=Door.open)
        self.push_door_outer_switch(pos=DoorPos.RearLeft,time_interval=2.5)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.RearLeft,req=LampSts.On)
        sleep(.3)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.RearLeft,req=LampSts.Off)
        self.release_door_outer_switch(pos=DoorPos.RearLeft)
    
    @allure.title("副驾车门PE闭锁，（副驾）门板指示灯闪烁")
    @pytest.mark.full
    def test_caseid_1985900(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone2,sts=BLEKeyPrsntSts.Valid)
        self.io.set_hood_sts(HoodSts.Close)
        self.io.set_door(Pass=Door.open)
        self.push_door_outer_switch(pos=DoorPos.Pass,time_interval=2.5)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.Pass,req=LampSts.On)
        sleep(.3)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.Pass,req=LampSts.Off)
        self.release_door_outer_switch(pos=DoorPos.Pass)
    
    @allure.title("中控锁解锁_指示灯常亮_锁源远控")
    @pytest.mark.smoke
    @pytest.mark.new
    def test_caseid_1985484(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.Telm)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.All,req=LampSts.On)

    
    @allure.title("中控锁闭锁_指示灯熄灭_锁源HMI_normal convenience")
    @pytest.mark.sanity
    def test_caseid_1985483(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.HMI)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.All,req=LampSts.On)
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.All,req=LampSts.Off)

    
    @allure.title("中控锁闭锁_指示灯熄灭_锁源远控")
    @pytest.mark.smoke
    @pytest.mark.new
    def test_caseid_1985895(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.Telm)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.All,req=LampSts.On)
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.Telm)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.All,req=LampSts.Off)

    
    @allure.title("中控锁闭锁_指示灯熄灭_锁源NFC")
    @pytest.mark.sanity
    def test_caseid_1985894(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.All,req=LampSts.On)
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.All,req=LampSts.Off)

    
    @allure.title("中控锁闭锁_指示灯熄灭_锁源HMI_Crash driving")
    @pytest.mark.smoke
    @pytest.mark.new
    def test_caseid_1985869(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        sleep(15)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.HMI)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.All,req=LampSts.On)
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.All,req=LampSts.Off)

    
    @allure.title("normal inactive下，蓝牙钥匙进入Zone6 范围内未解锁，门板指示灯呼吸")
    @pytest.mark.sanity
    def test_caseid_1985866(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.io.driver_seat_notpresent()

        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone14,sts=BLEKeyPrsntSts.Valid)
        sleep(0.5)
        # self.bus_comm.check_door_switch_light_keep_sts(pos=DoorPos.All,req=LampSts.Off,last_time=6)
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone6,sts=BLEKeyPrsntSts.Valid)
        sleep(0.5)
        self.bus_comm.check_door_switch_light_keep_sts(pos=DoorPos.All,req=LampSts.On,last_time=6)

    @allure.title("normal inactive下，蓝牙钥匙进入Zone2范围内未解锁，门板指示灯呼吸")
    @pytest.mark.sanity
    def test_caseid_1985865(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.io.driver_seat_notpresent()
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone7,sts=BLEKeyPrsntSts.Valid)
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone2,sts=BLEKeyPrsntSts.Valid)
        sleep(0.5)
        self.bus_comm.check_door_switch_light_keep_sts(pos=DoorPos.All,req=LampSts.On,last_time=6)

    @allure.title("normal inactive下，蓝牙钥匙进入Zone6范围内锁车，门板指示灯呼吸")
    @pytest.mark.sanity
    def test_caseid_1985679(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.HMI)
        self.io.driver_seat_notpresent()
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone6,sts=BLEKeyPrsntSts.Valid)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
        sleep(0.5)
        self.bus_comm.check_door_switch_light_keep_sts(pos=DoorPos.All,req=LampSts.On,last_time=6)

    @allure.title("normal inactive下，主驾有占座，门板指示灯熄灭")
    @pytest.mark.full
    def test_caseid_1985864(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.set_centrllock_to_lock()
        self.io.driver_seat_notpresent()
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone7,sts=BLEKeyPrsntSts.Valid)
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone2,sts=BLEKeyPrsntSts.Valid)
        sleep(0.5)
        self.bus_comm.check_door_switch_light_keep_sts(pos=DoorPos.All,req=LampSts.On,last_time=6)
        self.io.driver_seat_present()
        sleep(0.5)
        self.check_outer_door_always_on_off(pos=DoorPos.All,OnOrOff=YesOrNo.No,last_time=6)
        # 恢复
        self.io.driver_seat_present()
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone2,sts=BLEKeyPrsntSts.NotValid)

    @allure.title("中控锁闭锁_指示灯熄灭_远控开尾门_保持熄灭")
    @pytest.mark.smoke
    @pytest.mark.new
    def test_caseid_1985862(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.Telm)
        self.mix.check_turn_lamp_flash(pos=DoorPos.All,sts=isOn.Off,last_time=6)

    
    @allure.title("normal inactive下，车辆非静止，门板指示灯熄灭")
    @pytest.mark.sanity
    def test_caseid_1985678(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
        self.io.driver_seat_notpresent()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.All,req=LampSts.On)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal1)
        self.bus_comm.set_vehspd(10.0)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.All,req=LampSts.Off)
        
    @allure.title("Normal Active mode_车辆静止_中控解锁_指示灯常亮")
    @pytest.mark.full
    def test_caseid_1994440(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.io.driver_seat_notpresent()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.NFC)
        sleep(1)
        self.check_outer_door_always_on_off(pos=DoorPos.All,OnOrOff=YesOrNo.Yes,last_time=6)

    @allure.title("指示灯常亮_下切至Abandoned指示灯熄灭")
    @pytest.mark.full
    def test_caseid_1994441(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.NFC)
        sleep(1)
        self.bus_comm.check_door_switch_light_keep_sts(pos=DoorPos.All,req=LampSts.On,last_time=6)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(1)
        self.check_outer_door_always_on_off(pos=DoorPos.All,OnOrOff=YesOrNo.No,last_time=6)

    @allure.title("门服务关闭门板指示灯_动态OuterDoorSwLightReq")
    @pytest.mark.full
    @pytest.mark.dl_new
    def test_caseid_1994442(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
        # self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetOutDoorSwitchLightMode", {"doors": 4, "mode": 1})
        self.soa.get_and_set_outerdoorswlight_mode(target_doorid=DoorId.kDoorAll,target_mode=OutDoorSwitchLightMode.kModeOff,target_sts=isOn.On)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.All,req=LampSts.On)

    @allure.title("门服务开启门板指示灯_动态OuterDoorSwLightReq")
    @pytest.mark.full
    @pytest.mark.dl_new
    def test_caseid_1994443(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
        # self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetOutDoorSwitchLightMode", {"doors": 4, "mode": 1})
        self.soa.get_and_set_outerdoorswlight_mode(target_doorid=DoorId.kDoorAll,target_mode=OutDoorSwitchLightMode.kOnDynamic,target_sts=isOn.On)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.All,req=LampSts.On)

    @allure.title("门服务关闭门板指示灯_静态OuterDoorSwLightReq")
    @pytest.mark.full
    @pytest.mark.dl_new
    def test_caseid_1994444(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
        # self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetOutDoorSwitchLightMode", {"doors": 4, "mode": 1})
        self.soa.get_and_set_outerdoorswlight_mode(target_doorid=DoorId.kDoorAll,target_mode=OutDoorSwitchLightMode.kModeOff,target_sts=isOn.On)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.All,req=LampSts.On)

    @allure.title("门服务开启门板指示灯_静态OuterDoorSwLightReq")
    @pytest.mark.full
    @pytest.mark.dl_new
    def test_caseid_1994445(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
        # self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetOutDoorSwitchLightMode", {"doors": 4, "mode": 1})
        self.soa.get_and_set_outerdoorswlight_mode(target_doorid=DoorId.kDoorAll,target_mode=OutDoorSwitchLightMode.kOnStatic,target_sts=isOn.On)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.All,req=LampSts.On)

    @allure.title("Dyno Convenience mode蓝牙钥匙离开Zone6范围内未解锁，门板指示灯熄灭")
    @pytest.mark.full
    def test_caseid_1994446(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.set_centrllock_to_lock()
        self.io.driver_seat_notpresent()
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone6,sts=BLEKeyPrsntSts.Valid)
        sleep(1)
        self.check_outer_door_always_on_off(pos=DoorPos.All,OnOrOff=YesOrNo.Yes,last_time=6)
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone6,sts=BLEKeyPrsntSts.NotValid)
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone2,sts=BLEKeyPrsntSts.NotValid)
        sleep(1)
        self.check_outer_door_always_on_off(pos=DoorPos.All,OnOrOff=YesOrNo.No,last_time=6)

    @allure.title("Crash Active mode蓝牙钥匙进入Zone6 范围内未解锁，门板指示灯呼吸")
    @pytest.mark.full
    @pytest.mark.dl_new
    def test_caseid_1994447(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.io.driver_seat_notpresent()
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone14,sts=BLEKeyPrsntSts.Valid)
        sleep(0.5)
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone6,sts=BLEKeyPrsntSts.Valid)
        sleep(0.5)
        self.bus_comm.check_door_switch_light_keep_sts(pos=DoorPos.All,req=LampSts.On,last_time=6)

    @allure.title("中控解锁指示灯常亮_主驾车门PE闭锁_主驾车门指示灯闪烁")
    @pytest.mark.full
    def test_caseid_1994449(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.check_outer_door_always_on_off(pos=DoorPos.All,OnOrOff=YesOrNo.Yes,last_time=6)
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone2,sts=BLEKeyPrsntSts.Valid)
        self.io.set_hood_sts(HoodSts.Close)
        self.io.set_door(Drvr=Door.open)
        self.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.Dirver,req=LampSts.On)
        sleep(.3)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.Dirver,req=LampSts.Off)
        self.release_door_outer_switch(pos=DoorPos.Dirver)
        # 恢复
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone2,sts=BLEKeyPrsntSts.NotValid)
        
    @allure.title("Normal Abandoned mode中控锁解锁_指示灯未亮")
    @pytest.mark.full
    def test_caseid_1994450(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(1)
        self.check_outer_door_always_on_off(pos=DoorPos.All,OnOrOff=YesOrNo.No,last_time=6)

    @allure.title("Transport Convenience mode中控锁解锁_指示灯未亮")
    @pytest.mark.full
    def test_caseid_1994451(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.set_centrllock_to_lock()
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(1)
        self.bus_comm.check_door_switch_light_keep_sts(pos=DoorPos.All,req=LampSts.Off,last_time=6)

    @allure.title("Factory Active mode中控锁解锁_指示灯未亮")
    @pytest.mark.full
    def test_caseid_1994452(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.set_centrllock_to_lock()
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(1)
        self.bus_comm.check_door_switch_light_keep_sts(pos=DoorPos.All,req=LampSts.Off,last_time=6)
    
    @allure.title("ccp#117!=02中控锁解锁_指示灯未亮")
    @pytest.mark.full
    def test_caseid_1994453(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={117:0x1})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.set_centrllock_to_lock()
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(1)
        self.bus_comm.check_door_switch_light_keep_sts(pos=DoorPos.All,req=LampSts.Off,last_time=6)
        self.mix.set_ccp({117:0x2})

    @allure.title("Dyno Active mode中控锁解锁_指示灯常亮")
    @pytest.mark.full
    def test_caseid_1994454(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(1)
        self.check_outer_door_always_on_off(pos=DoorPos.All,OnOrOff=YesOrNo.Yes,last_time=6)

    @allure.title("normal inactive下，蓝牙钥匙离开Zone2范围内未解锁，门板指示灯熄灭")
    @pytest.mark.sanity
    def test_caseid_1985863(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.io.driver_seat_notpresent()
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone7,sts=BLEKeyPrsntSts.Valid)
        sleep(1)
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone2,sts=BLEKeyPrsntSts.Valid)
        sleep(1)
        self.bus_comm.check_door_switch_light_keep_sts(pos=DoorPos.All,req=LampSts.On,last_time=6)
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone2,sts=BLEKeyPrsntSts.NotValid)
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone6,sts=BLEKeyPrsntSts.NotValid)
        sleep(1)
        self.check_outer_door_always_on_off(pos=DoorPos.All,OnOrOff=YesOrNo.No,last_time=6)

    @allure.title("右后车门PE闭锁，（右后）门板指示灯闪烁")
    @pytest.mark.sanity
    def test_caseid_1985902(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone2,sts=BLEKeyPrsntSts.Valid)
        self.io.set_hood_sts(HoodSts.Close)
        self.io.set_door(RiRe=Door.open)
        self.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.RearRight,req=LampSts.On)
        sleep(.3)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.RearRight,req=LampSts.Off)
        self.release_door_outer_switch(pos=DoorPos.RearRight)
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone2,sts=BLEKeyPrsntSts.NotValid)

    @allure.title("Normal Inactive mode_车辆静止_中控解锁_指示灯常亮")
    @pytest.mark.full
    def test_caseid_1994438(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.check_outer_door_always_on_off(pos=DoorPos.All,OnOrOff=YesOrNo.Yes,last_time=6)

    @allure.title("副驾车门PE闭锁_副驾门板指示灯闪烁_中控闭锁指示灯呼吸")
    @pytest.mark.full
    def test_caseid_1994448(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={117:2})
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_ble_key_prsnt_sts(zone=BLEKeyPrsntZone.Zone2,sts=BLEKeyPrsntSts.Valid)
        self.io.set_hood_sts(HoodSts.Close)
        self.io.set_door(Pass=Door.open)
        self.push_door_outer_switch(pos=DoorPos.Pass,time_interval=2.5)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.Pass,req=LampSts.On)
        sleep(.3)
        self.bus_comm.check_door_switch_light_sts(pos=DoorPos.Pass,req=LampSts.Off)
        self.release_door_outer_switch(pos=DoorPos.Pass)
        self.set_centrllock_to_lock()
        sleep(1)
        self.bus_comm.check_door_switch_light_keep_sts(pos=DoorPos.All,req=LampSts.On,last_time=6)

    @allure.title("Crash Driving mode_车辆静止_中控解锁_指示灯常亮")
    @pytest.mark.full
    def test_caseid_1994439(self):
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.bus_comm.check_door_switch_light_keep_sts(pos=DoorPos.All,req=LampSts.On,last_time=6)