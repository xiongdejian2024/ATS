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
from xat_ecu.api.abc_interface import *


@allure.feature("车控车设")
@allure.story("外灯/倒车灯")
class TestExltlightCtrlABC(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(
            ["CentralLockService_client", "CTDService_client", "TailGateService_client","LightService_client",'KeyService_client']
        )
        sleep(2)
        self.sd_tester.write_ccp(
            ccp={
                94: 0x80,
                98: 0x2,
                97: 0x2,
                10: 0x2,
                481: 0x4,
                578: 0x4,
                142: 0x83,  # 解闭锁相关
                64: 3,  # With Alarm Using Vehicle Horn 即siren，警报器
                543: 1,  # Without Battery Backed-Up Sounder 即BBS
                66: 1,  # Without inclination sensor 即IS倾斜传感器
                65: 1,  # Without Interior Motion Sensor 即内部运动传感器
                1: 0xA3,  # 适用配置了舒适泊车模式的车型，对应设防准备时间 30s
                69: 1,  # Re-trig次数，一个报警周期30s鸣笛停止10s
                70: 1,  # 无被动设防
                13: 4,  # 动力类型Battery electric vehicle，上切Active或Driving可解防
            }
        )
        # 设置车辆静止
        self.bus_comm.set_vehspd_gear(vehspd=0, gear=Gear.Park)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)

        # 检查双闪是否已经打开，如果打开先关闭
        ori_data = self.bus_comm.ipdu.check_signal(self.bus_comm.ipdu.bodycan.CemBodyFr03, 'ActvnOfIndcrIndcrOut', 3)
        check_result = check_signal_value_exist(ori_data, 3)
        if check_result:
            logger.info("---------->双闪被开启，执行关闭操作")
            sleep(3)
            self.io.hazard_light_open()
            self.io.hazard_light_close()
            sleep(3)
            self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        else:
            check_result = check_signal_value_exist(ori_data, 1) or check_signal_value_exist(ori_data, 2)
            if check_result:
                logger.info("---------->转向灯被开启，执行关闭操作")
                self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
                sleep(6)
    
    def before_each_func(self, ecu):
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()
        # self.mix.write_vehicle_model_ccp(vehicle_model = VehicleType.Mars, vehicle_mca = VehicleMca.Mca_400v)
        
        self.bus_comm.resume_all_bus_send()
        # 检查双闪是否已经打开，如果打开先关闭
        ori_data = self.bus_comm.ipdu.check_signal(self.bus_comm.ipdu.bodycan.CemBodyFr03, 'ActvnOfIndcrIndcrOut', 3)
        check_result = check_signal_value_exist(ori_data, 3)
        if check_result:
            self.io.hazard_light_open()
            self.io.hazard_light_close()
            sleep(.5)
            self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        else:
            check_result = check_signal_value_exist(ori_data, 1) or check_signal_value_exist(ori_data, 2)
            if check_result:
                self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
                sleep(6)

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

    def check_hwl_lamp_err_flash_sts(self,act_sts_le:PosnLampSts,act_sts_ri:PosnLampSts):
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=act_sts_le,act_sts_ri=act_sts_ri)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=act_sts_le,act_sts_ri=act_sts_ri)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.Off)
        for num in range(3):
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 3)
            sleep(.2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)
    
    def check_turn_lamp_flash_sts(self,act_sts_le:PosnLampSts,act_sts_ri:PosnLampSts,pos:IndcrSts):
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=act_sts_le,act_sts_ri=act_sts_ri,pos_sts=pos)
            self.bus_comm.check_turn_lamp_act_req(sts=pos,act_sts=pos)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=pos,act_sts=IndcrSts.Off)

    def set_centrllock_to_lock(self):
        self.mix.set_all_seats_present_sts(seat_pres_sts=SeatPresSts.NoPres)
        self.io.set_five_door_sts(Door.close)
        # 设置bodycan上五个电动门均关闭
        self.bus_comm.set_door_opener_sts(DoorOpenerSts.FullClsd)
        self.io.trigger_all_doors_outswitch(OutSwitchPressSts.NoPress)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        sleep(1)
        cen_lock_sts = self.bus_comm.get_central_lock_sts()
        if cen_lock_sts == 1:
            logger.info(f"当前的中控锁状态为UnLock,需要先落锁再执行后续操作")
            self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
            sleep(1)
            cen_lock_sts = self.bus_comm.get_central_lock_sts()
            if cen_lock_sts == 3:
                logger.info(f"当前的中控锁状态是否为Lock,闭锁成功")
            else:
                logger.info(f"当前的中控锁状态仍为UnLock,RKE闭锁失败")
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


    @allure.title("ccp#114==[02]，Dyno Driving mode 紧急制动以低速制动时制动灯(EBL)请求点亮HWL")
    @pytest.mark.full
    def test_caseid_115113(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={114:2})
        self.bus_comm.set_brake_pedal()
        sleep(.3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("ccp#114==[02]，Normal Driving mode 紧急制动以低速制动时制动灯(EBL)请求点亮HWL后按压HWL开关关闭HWL")
    @pytest.mark.smoke
    def test_caseid_114983(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:2})
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_brake_pedal()
        sleep(.3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Driving mode 自动紧急制动(AEB)请求HWL")
    @pytest.mark.smoke
    def test_caseid_113312(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(.5)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOn)
        sleep(.5)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
    

    @allure.title("ccp#114==[02]，Normal Driving mode 自动紧急制动以低速制动时制动灯(EBL)请求点亮HWL后按压HWL开关关闭HWL")
    @pytest.mark.smoke
    def test_caseid_114962(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:2})
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(.5)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOn)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)


    @allure.title("Normal Driving mode 按压一次HWL开关激活HWL")
    @pytest.mark.smoke
    def test_caseid_114871(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Driving mode 已激活HWL按压一次HWL开关失活HWL")
    @pytest.mark.smoke
    def test_caseid_114753(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Driving mode 碰撞后制动(PIB)激活HWL")
    @pytest.mark.smoke
    def test_caseid_115043(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Driving mode 碰撞后制动(PIB)手动按压HWL开关关闭HWL")
    @pytest.mark.smoke
    def test_caseid_115122(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Driving mode 退出碰撞后制动(PIB)使HWL失活")
    @pytest.mark.smoke
    def test_caseid_114934(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Driving mode 退出自动紧急制动(AEB)失活HWL")
    @pytest.mark.smoke
    def test_caseid_115049(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(1)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOn)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Driving mode 自动紧急制动(AEB)请求HWL按压HWL开关关闭HWL")
    @pytest.mark.smoke
    def test_caseid_115079(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(1)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOn)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)

    @allure.title("CCP#153==[02]or[04] Normal Driving mode 解除后碰撞预警(RCW)失活HWL")
    @pytest.mark.smoke
    def test_caseid_113322(self):
        self.mix.set_ccp({153:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.check_hwl_lamp_flash_sts(flash_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)


    @allure.title("ccp#114==[02]，Normal Driving mode 自动紧急制动以低速制动时制动灯(EBL)请求点亮HWL")
    @pytest.mark.smoke
    def test_caseid_114737(self):
        self.mix.set_ccp({114:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        # 恢复
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("CCP#153==[02]or[04] Normal Driving mode 后碰撞预警(RCW)请求HWL")
    @pytest.mark.smoke
    def test_caseid_115104(self):
        self.mix.set_ccp({153:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.check_hwl_lamp_flash_sts(flash_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)
        # 恢复
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("CCP#153==[02]or[04] Normal Driving mode 后碰撞预警(RCW)请求HWL发送周期大于4s")
    @pytest.mark.full
    def test_caseid_115084(self):
        self.mix.set_ccp({153:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        sleep(5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("Normal Driving mode 电池热失控下退出热失控失活HWL")
    @pytest.mark.smoke
    def test_caseid_115095(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Active mode 退出碰撞后制动(PIB)使HWL失活")
    @pytest.mark.full
    def test_caseid_111381(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("ccp#114==[02]，Dyno Driving mode 自动紧急制动以低速制动时制动灯(EBL)请求点亮HWL刹稳后提速到更高速")
    @pytest.mark.full
    def test_caseid_111356(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={114:2})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Driving mode 防盗请求HWL")
    @pytest.mark.full
    def test_caseid_1912467(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 退出防盗
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal mode 通过服务请求HWL后按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_111313(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Convenience mode 碰撞后制动(PIB)手动按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_111311(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)

    @allure.title("Dyno Driving mode 已激活HWL按压一次HWL开关失活HWL")
    @pytest.mark.full
    def test_caseid_111305(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal mode 通过服务请求HWL变为请求右转灯")
    @pytest.mark.full
    def test_caseid_115135(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=95)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        sleep(5)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        # 恢复
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Transport Driving mode 退出碰撞后制动(PIB)使HWL失活")
    @pytest.mark.full
    def test_caseid_115125(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Active mode 电池热失控激活HWL")
    @pytest.mark.smoke
    def test_caseid_115124(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Transport Driving mode 退出碰撞后制动(PIB)使HWL失活")
    @pytest.mark.full
    def test_caseid_115120(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Driving mode 退出碰撞后制动(PIB)使HWL失活")
    @pytest.mark.full
    def test_caseid_115118(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Convenience mode 电池热失控下退出热失控失活HWL")
    @pytest.mark.smoke
    def test_caseid_115117(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Crash Driving mode 寻车模式下按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_115110(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Convenience mode 碰撞后制动(PIB)手动按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_115107(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Driving mode 退出碰撞后制动(PIB)使HWL失活")
    @pytest.mark.full
    def test_caseid_115102(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Convenience mode 退出碰撞后制动(PIB)使HWL失活")
    @pytest.mark.full
    def test_caseid_115099(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("ccp#114==[02]，Crash Driving mode 自动紧急制动以低速制动时制动灯(EBL)请求点亮HWL后按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_115096(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH,ccp={114:2})
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Convenience mode 碰撞后制动(PIB)手动按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_115093(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Convenience mode 碰撞后制动(PIB)激活HWL")
    @pytest.mark.full
    def test_caseid_115088(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Convenience mode 碰撞事件激活HWL")
    @pytest.mark.full
    def test_caseid_115086(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO)
        sleep(1)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Transport Inactive mode 碰撞后制动(PIB)手动按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_115082(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("ccp#114==[02]，Crash Driving mode 紧急制动以低速制动时制动灯(EBL)请求点亮HWL")
    @pytest.mark.full
    def test_caseid_115081(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH,ccp={114:2})
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_brake_pedal()
        sleep(.3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Abandoned mode 防盗请求HWL")
    @pytest.mark.full
    def test_caseid_115078(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.ABANDONED)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 退出防盗
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Active mode 寻车模式激活后取消寻车失活HWL")
    @pytest.mark.full
    def test_caseid_115076(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kNoReq)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("ccp#114==[02]，Crash Driving mode 紧急制动以低速制动时制动灯(EBL)请求点亮HWL")
    @pytest.mark.full
    def test_caseid_115066(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_brake_pedal()
        sleep(.3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Active mode 碰撞后制动(PIB)手动按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_115063(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Driving mode 按压一次HWL开关激活HWL")
    @pytest.mark.full
    def test_caseid_115061(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Transport Active mode 碰撞事件激活HWL")
    @pytest.mark.full
    def test_caseid_115057(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        sleep(1)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Abandoned mode 防盗请求HWL")
    @pytest.mark.full
    def test_caseid_115055(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复无防盗状态
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Crash Driving mode 寻车模式激活后取消寻车失活HWL")
    @pytest.mark.full
    def test_caseid_115054(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.set_carloctr_req(req=CarLocalTraceReq.kNoReq)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("危险警示灯(HWL)激活过程_HWL开关请求HWL_左1和右前转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_115050(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=ExtrLtgSts.Err)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearLeft,sts=ExtrLtgSts.Err)
        self.check_hwl_lamp_err_flash_sts(act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Error) 
        # 恢复
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=ExtrLtgSts.On)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearLeft,sts=ExtrLtgSts.On)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Crash Active mode 寻车模式下按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_115047(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("危险警示灯(HWL)激活过程_HWL开关请求HWL_左前和右前转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_115046(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=ExtrLtgSts.Err)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=ExtrLtgSts.Err)
        self.check_hwl_lamp_err_flash_sts(act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Error) 
        # 恢复
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=ExtrLtgSts.On)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=ExtrLtgSts.On)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Inactive mode 退出碰撞后制动(PIB)使HWL失活")
    @pytest.mark.full
    def test_caseid_115045(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Crash Inactive mode 已激活HWL按压一次HWL开关失活HWL")
    @pytest.mark.full
    def test_caseid_115042(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.LeAndRiOn)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("Crash Active mode 碰撞事件已激活HWL手动按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_115039(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.LeAndRiOn)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("Dyno Active mode 碰撞后制动(PIB)激活HWL")
    @pytest.mark.full
    def test_caseid_115035(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)

    @allure.title("Dyno Inactive mode 按压一次HWL开关激活HWL")
    @pytest.mark.full
    def test_caseid_115034(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.LeAndRiOn)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("Normal Active mode 电池热失控下按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_115032(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hvbatt(0)

    @allure.title("ccp#114==[02]，Crash Driving mode 紧急制动以低速制动时制动灯(EBL)请求点亮HWL刹稳后车辆提速到更高速度")
    @pytest.mark.full
    def test_caseid_115031(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH,ccp={114:2})
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Inactive mode 电池热失控激活HWL")
    @pytest.mark.full
    def test_caseid_115029(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Transport Inactive mode 碰撞后制动(PIB)激活HWL")
    @pytest.mark.full
    def test_caseid_115027(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)

    @allure.title("Factory Inactive mode 已激活HWL按压一次HWL开关失活HWL")
    @pytest.mark.full
    def test_caseid_115026(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.LeAndRiOn)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("Normal Convenience mode 退出碰撞后制动(PIB)使HWL失活")
    @pytest.mark.full
    def test_caseid_115023(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Crash Inactive mode 碰撞事件已激活HWL手动按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_115019(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.LeAndRiOn)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("Transport Inactive mode 退出碰撞后制动(PIB)使HWL失活")
    @pytest.mark.full
    def test_caseid_115010(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Inactive mode 碰撞后制动(PIB)手动按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_115007(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Crash Active mode 寻车模式激活后取消寻车失活HWL")
    @pytest.mark.full
    def test_caseid_115006(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.set_carloctr_req(req=CarLocalTraceReq.kNoReq)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Convenience mode 按压一次HWL开关激活HWL")
    @pytest.mark.full
    def test_caseid_115002(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("Dyno Inactive mode 碰撞事件激活HWL")
    @pytest.mark.full
    def test_caseid_115000(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO)
        sleep(.4)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("Crash Convenience mode 已激活HWL按压一次HWL开关失活HWL")
    @pytest.mark.full
    def test_caseid_114998(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("Normal Convenience mode 寻车模式激活后取消寻车失活HWL")
    @pytest.mark.full
    def test_caseid_114997(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kNoReq)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Convenience mode 退出碰撞后制动(PIB)使HWL失活")
    @pytest.mark.full
    def test_caseid_114991(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Active mode 碰撞事件激活HWL")
    @pytest.mark.full
    def test_caseid_114987(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        sleep(.4)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("Factory Convenience mode 碰撞事件激活HWL")
    @pytest.mark.full
    def test_caseid_114982(self):

        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        sleep(.4)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("ccp#114==[02]，Dyno Driving mode 自动紧急制动以低速制动时制动灯(EBL)请求点亮HWL后按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_114979(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={114:2})
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        # 恢复
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("危险警示灯(HWL)激活过程_HWL开关请求HWL_满足HWL激活条件转灯状态信号正常")
    @pytest.mark.full
    def test_caseid_114978(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.LeAndRiOn)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("ccp#114==[02]，Normal Driving mode 自动紧急制动以低速制动时制动灯(EBL)请求点亮HWL刹稳后提速到更高速")
    @pytest.mark.full
    def test_caseid_114976(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={114:2})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal mode 通过服务请求HWL变为请求左转灯")
    @pytest.mark.full
    def test_caseid_114975(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=95)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        sleep(5)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.LeOn)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("锁车事件请求HWL到请求结束_条件过程_左前和右前转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_114974(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr08", 'LockgCenStsForUsrFb', 3)
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=ExtrLtgSts.Err)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=ExtrLtgSts.Err)
        for num in range(3):
            self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 3)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrLe', 2)
            sleep(.4)
            self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 0)
        for num in range(3):
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 3)
            sleep(.2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)

    @allure.title("Transport Convenience mode 碰撞后制动(PIB)激活HWL")
    @pytest.mark.full
    def test_caseid_114973(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)


    @allure.title("Factory Driving mode 碰撞事件激活HWL")
    @pytest.mark.full
    def test_caseid_114970(self):

        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        sleep(.4)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("Dyno Driving mode 碰撞事件激活HWL")
    @pytest.mark.full
    def test_caseid_114968(self):

        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        sleep(.4)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("Dyno Active mode 碰撞后制动(PIB)手动按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_114966(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Transport Driving mode 碰撞后制动(PIB)激活HWL")
    @pytest.mark.full
    def test_caseid_114960(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)

    @allure.title("ccp#114==[02]，Normal Driving mode 紧急制动以低速制动时制动灯(EBL)请求点亮HWL刹稳后车辆提速到更高")
    @pytest.mark.full
    def test_caseid_114958(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:2})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("ccp#114==[02]，Normal Driving mode 紧急制动以低速制动时制动灯(EBL)请求点亮HWL刹稳后车辆提速到更高")
    @pytest.mark.full
    def test_caseid_114954(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={114:2})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("Normal Convenience mode 防盗请求HWL")
    @pytest.mark.full
    def test_caseid_114950(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复无防盗状态
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Active mode 碰撞后制动(PIB)激活HWL")
    @pytest.mark.full
    def test_caseid_114948(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)

    @allure.title("ccp#114==[02]，Dyno Driving mode 自动紧急制动以低速制动时制动灯(EBL)请求点亮HWL")
    @pytest.mark.full
    def test_caseid_114946(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={114:2})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3)
        # 恢复
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Inactive mode 退出碰撞后制动(PIB)使HWL失活")
    @pytest.mark.full
    def test_caseid_114944(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Active mode 碰撞事件激活HWL")
    @pytest.mark.full
    def test_caseid_114942(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        sleep(.4)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("Normal mode 通过服务请求HWL后服务停止HWL失活")
    @pytest.mark.full
    def test_caseid_114941(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=95)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        sleep(5)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("Factory Convenience mode 碰撞后制动(PIB)激活HWL")
    @pytest.mark.full
    def test_caseid_114940(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)

    @allure.title("Dyno Driving mode 碰撞后制动(PIB)激活HWL")
    @pytest.mark.full
    def test_caseid_114938(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)

    @allure.title("Crash Convenience mode 碰撞事件已激活HWL手动按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_114933(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        sleep(.4)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("Transport Convenience mode 碰撞后制动(PIB)手动按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_114924(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Active mode 防盗请求HWL")
    @pytest.mark.full
    def test_caseid_1912472(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复无防盗状态
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Crash Driving mode 碰撞事件已激活HWL手动按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_114918(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        sleep(.4)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("Normal Driving mode 按压一次HWL开关激活HWL")
    @pytest.mark.full
    def test_caseid_114913(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.LeAndRiOn)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("Transport Convenience mode 碰撞事件激活HWL")
    @pytest.mark.full
    def test_caseid_114907(self):

        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT)
        sleep(.4)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("Crash Driving mode 已激活HWL按压一次HWL开关失活HWL")
    @pytest.mark.full
    def test_caseid_114906(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("Normal Convenience mode 碰撞事件激活HWL")
    @pytest.mark.full
    def test_caseid_114905(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        sleep(1)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Transport Driving mode 碰撞事件激活HWL")
    @pytest.mark.full
    def test_caseid_114904(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        sleep(1)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Active mode 已激活HWL按压一次HWL开关失活HWL")
    @pytest.mark.full
    def test_caseid_114903(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Convenience mode 按压一次HWL开关激活HWL")
    @pytest.mark.full
    def test_caseid_114902(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Inactive mode 碰撞事件激活HWL")
    @pytest.mark.full
    def test_caseid_114900(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT)
        sleep(1)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("危险警示灯(HWL)激活过程_HWL开关请求HWL_左1转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_114892(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearLeft,sts=ExtrLtgSts.Err)
        self.check_hwl_lamp_err_flash_sts(act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.On) 
        # 恢复
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearLeft,sts=ExtrLtgSts.On)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Crash Inactive mode 按压一次HWL开关激活HWL")
    @pytest.mark.full
    def test_caseid_114890(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.CRASH)
        # 关闭crash开启的HWL
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("危险警示灯(HWL)激活过程_HWL开关请求HWL_左前和右1转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_114883(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=ExtrLtgSts.Err)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearRight,sts=ExtrLtgSts.Err)
        self.check_hwl_lamp_err_flash_sts(act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Error) 
        # 恢复
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=ExtrLtgSts.On)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearRight,sts=ExtrLtgSts.On)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Crash Active mode 已激活HWL按压一次HWL开关失活HWL")
    @pytest.mark.full
    def test_caseid_114877(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.LeAndRiOn)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("危险警示灯(HWL)激活过程_HWL开关请求HWL_右1转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_114873(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearRight,sts=ExtrLtgSts.Err)
        self.check_hwl_lamp_err_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Error) 
        # 恢复
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearRight,sts=ExtrLtgSts.On)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("危险警示灯(HWL)激活过程_HWL开关请求HWL_左前转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_114862(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=ExtrLtgSts.Err)
        self.check_hwl_lamp_err_flash_sts(act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.On) 
        # 恢复
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=ExtrLtgSts.On)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Active mode 已激活HWL按压一次HWL开关失活HWL")
    @pytest.mark.full
    def test_caseid_114859(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.LeAndRiOn)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("Normal Active mode 碰撞事件激活HWL")
    @pytest.mark.full
    def test_caseid_114857(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        sleep(1)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("危险警示灯(HWL)激活过程_HWL开关关闭HWL_满足HWL失活条件转灯状态信号正常")
    @pytest.mark.full
    def test_caseid_114855(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("Transport Inactive mode 碰撞事件激活HWL")
    @pytest.mark.full
    def test_caseid_114853(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT)
        sleep(1)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("Dyno Active mode 按压一次HWL开关激活HWL")
    @pytest.mark.full
    def test_caseid_114850(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("Normal Inactive mode 碰撞事件激活HWL")
    @pytest.mark.full
    def test_caseid_114840(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        sleep(1)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("Dyno Convenience mode 已激活HWL按压一次HWL开关失活HWL")
    @pytest.mark.full
    def test_caseid_114837(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.LeAndRiOn)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("Dyno Inactive mode 已激活HWL按压一次HWL开关失活HWL")
    @pytest.mark.full
    def test_caseid_114835(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.LeAndRiOn)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("Normal Convenience mode 已激活HWL按压一次HWL开关失活HWL")
    @pytest.mark.full
    def test_caseid_114833(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.LeAndRiOn)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("Dyno Convenience mode 碰撞后制动(PIB)激活HWL")
    @pytest.mark.full
    def test_caseid_114822(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)

    @allure.title("Transport Convenience mode 退出碰撞后制动(PIB)使HWL失活")
    @pytest.mark.full
    def test_caseid_114820(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Transport Driving mode  碰撞后制动(PIB)手动按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_114816(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Inactive mode 退出碰撞后制动(PIB)使HWL失活")
    @pytest.mark.full
    def test_caseid_114812(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Transport Active mode 退出碰撞后制动(PIB)使HWL失活")
    @pytest.mark.full
    def test_caseid_114805(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("危险警示灯(HWL)激活过程_HWL开关请求HWL_左1和右1转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_114801(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearLeft,sts=ExtrLtgSts.Err)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearRight,sts=ExtrLtgSts.Err)
        self.check_hwl_lamp_err_flash_sts(act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Error) 
        # 恢复
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearLeft,sts=ExtrLtgSts.On)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearRight,sts=ExtrLtgSts.On)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Active mode 已激活HWL按压一次HWL开关失活HWL")
    @pytest.mark.full
    def test_caseid_114798(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Driving mode 碰撞后制动(PIB)手动按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_114796(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Inactive mode 碰撞后制动(PIB)手动按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_114794(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("危险警示灯(HWL)激活过程_HWL开关请求HWL_右前转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_114790(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=ExtrLtgSts.Err)
        self.check_hwl_lamp_err_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Error) 
        # 恢复
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=ExtrLtgSts.On)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Inactive mode 已激活HWL按压一次HWL开关失活HWL")
    @pytest.mark.full
    def test_caseid_114788(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.LeAndRiOn)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("Normal Inactive mode 按压一次HWL开关激活HWL")
    @pytest.mark.full
    def test_caseid_114783(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("锁车事件请求HWL到请求结束_条件过程_左前和右1转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_114781(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=ExtrLtgSts.Err)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearRight,sts=ExtrLtgSts.Err)
        for num in range(3):
            self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 3)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrLe', 2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 2)
            sleep(.4)
            self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrLe', 0)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 0)
        for num in range(3):
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 3)
            sleep(.2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)

    @allure.title("Normal Active mode 碰撞后制动(PIB)激活HWL")
    @pytest.mark.full
    def test_caseid_114779(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)

    @allure.title("Transport Active mode 碰撞后制动(PIB)激活HWL")
    @pytest.mark.full
    def test_caseid_114776(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)

    @allure.title("Normal Active mode 退出碰撞后制动(PIB)使HWL失活")
    @pytest.mark.full
    def test_caseid_114774(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Active mode 退出碰撞后制动(PIB)使HWL失活")
    @pytest.mark.full
    def test_caseid_114770(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("ccp#114==[02]，Crash Driving mode 紧急制动以低速制动时制动灯(EBL)请求点亮HWL后按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_114768(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH,ccp={114:2})
        self.bus_comm.set_brake_pedal()
        sleep(.3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.LeAndRiOn)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)

    @allure.title("Transport Active mode 碰撞后制动(PIB)手动按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_114766(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Driving mode 碰撞后制动(PIB)手动按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_114764(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Inactive mode 防盗请求HWL")
    @pytest.mark.full
    def test_caseid_114760(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO)
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复无防盗状态
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Inactive mode 碰撞后制动(PIB)激活HWL")
    @pytest.mark.full
    def test_caseid_114755(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)

    @allure.title("Dyno Driving mode 按压一次HWL开关激活HWL")
    @pytest.mark.full
    def test_caseid_114742(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("ccp#114==[02]，Crash Driving mode 自动紧急制动以低速制动时制动灯(EBL)请求点亮HWL")
    @pytest.mark.full
    def test_caseid_114739(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH,ccp={114:2})
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("ccp#114==[02]，Crash Driving mode 自动紧急制动以低速制动时制动灯(EBL)请求点亮HWL刹稳后提速到更高速")
    @pytest.mark.full
    def test_caseid_114736(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH,ccp={114:2})
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Driving mode 已激活HWL按压一次HWL开关失活HWL")
    @pytest.mark.full
    def test_caseid_114735(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.LeAndRiOn)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("Normal Active mode 按压一次HWL开关激活HWL")
    @pytest.mark.full
    def test_caseid_114729(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.LeAndRiOn)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)


    @allure.title("Normal CONVENIENCE mode 电池热失控下退出热失控失活HWL")
    @pytest.mark.full
    def test_caseid_113403(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
    
    @allure.title("Normal Inactive mode 电池热失控下退出热失控失活HWL")
    @pytest.mark.full
    def test_caseid_113392(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Active mode 电池热失控下退出热失控失活HWL")
    @pytest.mark.full
    def test_caseid_113383(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Inactive mode 电池热失控下按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_113373(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hvbatt(0)

    @allure.title("Normal Convenience mode 电池热失控下按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_113368(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hvbatt(0)

    @allure.title("Normal mode 通过服务请求HWL")
    @pytest.mark.full
    def test_caseid_113269(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)

    @allure.title("Dyno Abandoned mode 防盗激活通过解锁车辆解除防盗HWL闪2次失活")
    @pytest.mark.full
    def test_caseid_113253(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.DYNO)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)

    @allure.title("Dyno Inactive mode 防盗激活通过解锁车辆解除防盗HWL闪2次失活")
    @pytest.mark.full
    def test_caseid_113247(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)


    @allure.title("Normal Inactive mode 寻车模式请求HWL根据本地配置闪烁3次HWL失活")
    @pytest.mark.full
    def test_caseid_113501(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Abandoned mode 防盗激活通过锁定车辆解除防盗HWL闪1次失活")
    @pytest.mark.full
    def test_caseid_113517(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        sleep(30)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        self.io.set_door(Drvr=Door.open)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)

    @allure.title("Dyno Abandoned mode 防盗激活通过锁定车辆解除防盗HWL闪1次失活")
    @pytest.mark.full
    def test_caseid_113507(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.DYNO)
        self.set_centrllock_to_lock()
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        sleep(30)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        self.io.set_door(Drvr=Door.open)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)

    @allure.title("Normal Inactive mode 防盗激活通过解锁车辆解除防盗HWL闪2次失活")
    @pytest.mark.full
    def test_caseid_115108(self):
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        sleep(30)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        self.io.set_door(Drvr=Door.open)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        for num in range(2):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)

    @allure.title("Dyno Inactive mode 防盗关失活HWL")
    @pytest.mark.full
    def test_caseid_115105(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)

    @allure.title("Normal Driving mode 自动紧急制动(AEB)请求信号丢失通过ReqBkp请求HWL按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_115087(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.pause_bus_send('backbonefr')
        sleep(1)
        self.bus_comm.set_aeb_bkp_brake_req(req=AsySftyHWLReq.TurnOn)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.Off)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.resume_bus_send('backbonefr')
        sleep(1)

    @allure.title("Normal Inactive mode 防盗关失活HWL")
    @pytest.mark.full
    def test_caseid_1912475(self):
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)

    @allure.title("锁车事件请求HWL到请求结束_条件过程_右前转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_114994(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=ExtrLtgSts.Err)
        self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 3)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrLe', 2)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 2)
        sleep(.4)
        self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 0)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrLe', 0)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 3)
        sleep(.2)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)

    @allure.title("Normal Abandoned mode 防盗关失活HWL")
    @pytest.mark.full
    def test_caseid_114964(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        sleep(30)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        self.io.set_door(Drvr=Door.open)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)

    @allure.title("锁车事件请求HWL到请求结束_条件过程_右前转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_114909(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=ExtrLtgSts.Err)
        self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 3)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrLe', 2)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 2)
        sleep(.4)
        self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 0)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrLe', 0)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 3)
        sleep(.2)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)

    @allure.title("锁车事件请求HWL到请求结束_条件过程_左1转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_114896(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearLeft,sts=ExtrLtgSts.Err)
        self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 3)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrLe', 2)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 2)
        sleep(.4)
        self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 0)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrLe', 0)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 3)
        sleep(.2)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)

    @allure.title("锁车事件请求HWL到请求结束_条件过程_左前转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_114887(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=ExtrLtgSts.Err)
        self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 3)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrLe', 2)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 2)
        sleep(.4)
        self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 0)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrLe', 0)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 3)
        sleep(.2)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)

    @allure.title("解锁事件请求HWL到请求结束_条件过程_左前和右前转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_114881(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=ExtrLtgSts.Err)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=ExtrLtgSts.Err)
        for num in range(2):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Error)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Error)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.Off)
        for num in range(2):
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 3)
            sleep(.2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0) 
        # 恢复
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=ExtrLtgSts.On)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=ExtrLtgSts.On)

    @allure.title("锁车事件请求HWL到请求结束_条件过程_左1和右前转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_114875(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearLeft,sts=ExtrLtgSts.Err)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=ExtrLtgSts.Err)
        self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 3)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrLe', 2)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 2)
        sleep(.4)
        self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 0)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrLe', 0)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 3)
        sleep(.2)
        self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)

    @allure.title("解锁事件请求HWL到请求结束_条件过程_左1转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_114825(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(0.3)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=ExtrLtgSts.Err)
        for num in range(2):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.Off)
        for num in range(2):
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 3)
            sleep(.2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0) 
        # 恢复
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=ExtrLtgSts.On)

    @allure.title("Normal Driving mode 寻车模式下按压HWL开关关闭HWL")
    @pytest.mark.smoke
    def test_caseid_115040(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Driving mode 电池热失控下按压HWL开关关闭HWL")
    @pytest.mark.smoke
    def test_caseid_115036(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hvbatt(0)

    @allure.title("Normal Driving mode 寻车模式请求HWL根据本地配置闪烁3次HWL失活")
    @pytest.mark.smoke
    def test_caseid_114989(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Driving mode 寻车模式激活后取消寻车失活HWL")
    @pytest.mark.smoke
    def test_caseid_114985(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kNoReq)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("CRASH Driving mode 碰撞事件激活HWL")
    @pytest.mark.smoke
    def test_caseid_114910(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        sleep(.5)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("ccp#114==[02]，Normal Driving mode 紧急制动以低速制动时制动灯(EBL)请求点亮HWL")
    @pytest.mark.smoke
    def test_caseid_114750(self):
        self.sd_tester.set_ccp(ccp_vlaue={114:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        sleep(.3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)

    @allure.title("Normal Driving mode 电池热失控激活HWL")
    @pytest.mark.smoke
    def test_caseid_113397(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)


    @allure.title("ccp#114==[02]，Dyno Driving mode 紧急制动以低速制动时制动灯(EBL)请求点亮HWL后按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_114956(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={114:2})
        self.bus_comm.set_brake_pedal()
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)

    @allure.title("解锁事件请求HWL到请求结束_条件过程_左1和右前转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_111378(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.set_centrllock_to_lock()
        sleep(.5)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=ExtrLtgSts.Err)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearLeft,sts=ExtrLtgSts.Err)
        for num in range(2):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Error)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Error)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.Off)
        for num in range(2):
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 3)
            sleep(.2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0) 
        # 恢复
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearLeft,sts=ExtrLtgSts.On)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=ExtrLtgSts.On)
    
    @allure.title("锁车事件请求HWL到请求结束_条件过程_左1和右1转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_111310(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearLeft,sts=ExtrLtgSts.Err)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearRight,sts=ExtrLtgSts.Err)
        sleep(.2)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Error)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.LeAndRiOn)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Error)
        # self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.Off)
        

    @allure.title("Normal Inactive mode 碰撞后制动(PIB)手动按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_111322(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Convenience mode 按压一次HWL开关激活HWL")
    def test_caseid_111331(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复环境
        self.io.hazard_light_open()
        self.io.hazard_light_close()

    
    @allure.title("Normal Driving mode 退出紧急制动(AEB)请求信号丢失通过ReqBkp失活HWL")
    @pytest.mark.full
    def test_caseid_111347(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOn)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Crash Inactive mode 寻车模式下按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_111354(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Inactive mode 按压一次HWL开关激活HWL")
    @pytest.mark.full
    def test_caseid_111372(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复环境
        self.io.hazard_light_open()
        self.io.hazard_light_close()

    @allure.title("Normal Convenience mode 防盗关失活HWL")
    @pytest.mark.full
    def test_caseid_114733(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        for num in range(2):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
        sleep(2)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Driving mode 防盗请求HWL")
    @pytest.mark.full
    def test_caseid_114746(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复无防盗状态
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        
    @allure.title("Dyno Active mode 防盗关失活HWL")
    @pytest.mark.full
    def test_caseid_114748(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        for num in range(2):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
        sleep(2)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Convenience mode 已激活HWL按压一次HWL开关失活HWL")
    @pytest.mark.full
    def test_caseid_114894(self):
        # self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Inactive mode 寻车模式激活后取消寻车失活HWL")
    @pytest.mark.full
    def test_caseid_114977(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kNoReq)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Active mode 防盗请求HWL")
    @pytest.mark.full
    def test_caseid_114922(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复无防盗状态
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Crash Driving mode 防盗请求HWL")
    @pytest.mark.full
    def test_caseid_114928(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复无防盗状态
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        
    @allure.title("Dyno Convenience mode 防盗请求HWL")
    @pytest.mark.full
    def test_caseid_115051(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复无防盗状态
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Driving mode下CCP 274！=80 or 81无法手动激活HWL")
    @pytest.mark.full
    def test_caseid_1990228(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={274:0x01})
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
        # 恢复
        self.mix.sd_tester.set_ccp({274:0x80})
        self.io.hazard_light_open()
        self.io.hazard_light_close()

    @allure.title("Abandoned下无法手动激活HWL")
    @pytest.mark.full
    def test_caseid_1990229(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL,ccp={274:80})
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
    
    @allure.title("Transport模式下无法手动激活HWL")
    @pytest.mark.full
    def test_caseid_1990230(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT,ccp={274:80})
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()

    @allure.title("Crash Driving mode后碰撞预警（RCW）无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994305(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH,ccp={153:2})
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("Dyno Driving mode后碰撞预警（RCW）无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994306(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={153:2})
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("Transport Driving mode后碰撞预警（RCW）无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994307(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT,ccp={153:2})
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)
    
    @allure.title("Factory Driving mode后碰撞预警（RCW）无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994308(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY,ccp={153:2})
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("Normal Active mode后碰撞预警（RCW）无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994309(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={153:2})
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("Normal Convenience mode后碰撞预警（RCW）无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994310(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={153:2})
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("Normal Inactive mode后碰撞预警（RCW）无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994311(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={153:2})
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("Normal Abandoned mode后碰撞预警（RCW）无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994312(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL,ccp={153:2})
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("RCW激活HWL不足4sHWL继续闪烁")
    @pytest.mark.full
    def test_caseid_1994313(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        sleep(.8)
        self.check_hwl_lamp_flash_sts(flash_time=1)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("ccp#153！= 02 or 04时后碰撞预警(RCW)无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994322(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={153:3})
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={153:4})

    @allure.title("Transport Active mode 电池热失控激活HWL")
    @pytest.mark.full
    def test_caseid_1994324(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Convenience mode 电池热失控激活HWL")
    @pytest.mark.full
    def test_caseid_1994325(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        
    @allure.title("Dyno Inactive mode 电池热失控激活HWL")
    @pytest.mark.full
    def test_caseid_1994326(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
    
    @allure.title("Crash Driving mode 电池热失控激活HWL")
    @pytest.mark.full
    def test_caseid_1994327(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        # 关闭crash开启的HWL
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Active模式下紧急制动以低速制动时制动灯(EBL)无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994328(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        sleep(.3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)

    @allure.title("Convenience模式下紧急制动以低速制动时制动灯(EBL)无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994329(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        sleep(.3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)

    @allure.title("Inactive模式下紧急制动以低速制动时制动灯(EBL)无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994330(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        sleep(.3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)

    @allure.title("Abandoned模式下紧急制动以低速制动时制动灯(EBL)无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994331(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        sleep(.3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)

    @allure.title("Transport模式下紧急制动以低速制动时制动灯(EBL)无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994332(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_brake_pedal()
        sleep(.3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)

    @allure.title("Factory模式下紧急制动以低速制动时制动灯(EBL)无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994333(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_brake_pedal()
        sleep(.3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)

    @allure.title("Normal Driving mode下CCP 114 != 02紧急制动以低速制动时制动灯(EBL)无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994334(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:3})
        self.bus_comm.set_brake_pedal()
        sleep(.3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
    
    @allure.title("Abandoned模式下碰撞后制动（PIB）无法激活HWL")
    @pytest.mark.full
    def test_caseid_1994335(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)

    @allure.title("CC#508 != 03无法手动激活HWL")
    @pytest.mark.full
    def test_caseid_1994338(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={508:1})
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()

    @allure.title("Crash模式下碰撞后制动（PIB）无法激活HWL")
    @pytest.mark.full
    def test_caseid_1994336(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)

    @allure.title("进入crash模式激活HWL_语音无法关闭HWL")
    @pytest.mark.full
    def test_caseid_1994337(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()

    @allure.title("寻车打开HWL_打开灯光秀播放灯光秀")
    @pytest.mark.full
    def test_caseid_1994766(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        # 关闭灯关秀
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)

    @allure.title("寻车打开HWL_进入AEB_退出AEB_HWL关闭")
    @pytest.mark.full
    def test_caseid_1994767(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=2,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(.5)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOn)
        sleep(.5)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(2)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("寻车打开HWL_语音关闭")
    @pytest.mark.full
    def test_caseid_1994768(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(2)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("PIB打开HWL_取消寻车关闭失败")
    @pytest.mark.full
    def test_caseid_1994769(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kNoReq)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(2)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("PIB打开HWL_语音关闭")
    @pytest.mark.full
    def test_caseid_1994770(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=6)

    @allure.title("热失控打开HWL_取消寻车关闭失败")
    @pytest.mark.full
    def test_caseid_1994771(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(value=128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kNoReq)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hvbatt(value=0)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        
    @allure.title("解锁打开HWL_进入PIB_退出PIB_HWL闪两个周期关闭")
    @pytest.mark.full
    def test_caseid_1994772(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        for num in range(2):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("解锁打开HWL_等待2s_按键打开HWL")
    @pytest.mark.full
    def test_caseid_1994773(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(2)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("碰撞打开HWL_取消寻车关闭失败")
    @pytest.mark.full
    def test_caseid_1994774(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kNoReq)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        
    @allure.title("按键打开HWL_进入RCW_退出RCW_HWL继续开")
    @pytest.mark.full
    def test_caseid_1994775(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        sleep(1)
        self.bus_comm.set_rcw_req(req=RcwReq.No)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("按键打开HWL_语音关闭失败")
    @pytest.mark.full
    def test_caseid_1994776(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=6)

    @allure.title("Crash Driving mode 防盗关失活HWL")
    @pytest.mark.full
    def test_caseid_114740(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        for num in range(2):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
        # crash模式HWL闪烁
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Crash Inactive mode 防盗关失活HWL")
    @pytest.mark.full
    def test_caseid_114785(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.CRASH)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        for num in range(2):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
        # crash模式HWL闪烁
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("锁车事件请求HWL到请求结束_条件过程_满足HWL激活条件转灯状态信号正常")
    @pytest.mark.full
    def test_caseid_114818(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(0.2)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Abandoned mode 防盗关失活HWL")
    @pytest.mark.full
    def test_caseid_115060(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.DYNO)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        self.check_hwl_lamp_flash_sts(flash_time=2)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Inactive mode 碰撞后制动(PIB)激活HWL")
    @pytest.mark.full
    def test_caseid_115090(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复环境
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("按键打开HWL_闭锁关闭失败")
    @pytest.mark.full
    def test_caseid_1994777(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("RCW对主动安全的反馈")
    @pytest.mark.full
    def test_caseid_1988697(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={153:0x02})
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.check_hwl_lamp_flash_sts(flash_time=3)
        sleep(2)
        self.bus_comm.set_rcw_req(req=RcwReq.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
    
    @allure.title("Normal Convenience mode 寻车模式下按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_115021(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Convenience mode 寻车模式下按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_115024(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Crash Active mode 防盗请求HWL")
    @pytest.mark.full
    def test_caseid_115070(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复无防盗状态
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Inactive mode 寻车模式下按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_115092(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Crash Convenience mode 防盗请求HWL")
    @pytest.mark.full
    def test_caseid_115115(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复无防盗状态
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Abandoned mode 防盗激活通过解锁车辆解除防盗HWL闪2次失活")
    @pytest.mark.full
    def test_caseid_115121(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
        
    @allure.title("Normal Inactive mode 寻车模式激活后取消寻车失活HWL")
    @pytest.mark.full
    def test_caseid_115128(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kNoReq)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
    
    @allure.title("Dyno Inactive mode 寻车模式下按压HWL开关关闭HWL")
    @pytest.mark.full
    def test_caseid_115133(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("手动按压双闪开关，双闪打开/关闭无延迟")
    @pytest.mark.full
    def test_caseid_1989027(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(0.06)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(0.06)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("左侧HWL故障，右侧HWL不受影响")
    @pytest.mark.full
    def test_caseid_1990174(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearLeft,sts=PosnLampSts.Error)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=PosnLampSts.Error)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.Off)
        for num in range(3):
            self.bus_comm.check("backbonefr","CemBackBoneFr06", 'IndcrDisp', 3)
            sleep(.2)
            self.bus_comm.check("backbonefr","CemBackBoneFr06", 'IndcrDisp', 2)
            sleep(.4)
            self.bus_comm.check("backbonefr","CemBackBoneFr06", 'IndcrDisp', 1)
            sleep(.2)
            self.bus_comm.check("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearLeft,sts=PosnLampSts.On)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=PosnLampSts.On)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("退出热失控_热失控信号丢失_HWL不闪烁")
    @pytest.mark.full
    def test_caseid_1994295(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hvbatt(value=128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hvbatt(value=0)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.pause_bus_send('backbonefr')
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.io.io_reset_bgm()
        sleep(15)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.resume_bus_send('backbonefr')
    

    @allure.title("热失控激活HWL_热失控信号丢失HWL继续闪烁")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994296_1995541(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(value=128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.pause_bus_send('backbonefr')
        sleep(1)
        for num in range(3):
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.Off)
        self.io.io_reset_bgm()
        sleep(15)
        self.bus_comm.resume_bus_send('backbonefr')
        self.bus_comm.set_hvbatt(value=128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.pause_bus_send('backbonefr')
        sleep(1)
        for num in range(3):
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.Off)
        self.bus_comm.resume_bus_send('backbonefr')
        sleep(1)
        self.bus_comm.set_hvbatt(value=0)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("开启左转_EBL触发HWL失败")
    @pytest.mark.full
    def test_caseid_1994297(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={114:0x2})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.LeOn)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.LeOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.Off)
        self.bus_comm.set_brake_pedal()
        sleep(.3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.LeOn)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.LeOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.Off)
        # 恢复
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(6)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("EBL触发HWL_开启左转HWL被打断")
    @pytest.mark.full
    def test_caseid_1994298(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:2})
        self.bus_comm.set_brake_pedal()
        sleep(.3)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.LeOn)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.LeOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.Off)
        # 关闭左转HWL
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(6)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("进入crash模式激活HWL_按键开启右转失败")
    @pytest.mark.full
    def test_caseid_1994299(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:0x2})
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 关闭HWL
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("进入crash模式激活HWL_开启左转失败")
    @pytest.mark.full
    def test_caseid_1994300(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:0x2})
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 关闭HWL
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Crash Driving mode通过服务无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994301(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        sleep(6)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Abandoned mode通过服务无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994302(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.DYNO)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        sleep(6)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Transport Inactive mode通过服务无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994303(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        sleep(6)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Convenience mode通过服务无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994304(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        sleep(6)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        
    @allure.title("Abandoned模式下电池热失控无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994323(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(128)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hvbatt(0)

    @allure.title("请求开HWL_语音开启右转闪烁_按键关右转_HWL继续闪烁")
    @pytest.mark.full
    def test_caseid_1995558(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.RiOn)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.RiOn,act_sts=IndcrSts.RiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.RiOn,act_sts=IndcrSts.Off)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("请求开HWL_按键开右转闪烁_语音开左转闪烁_按键关闭左转_HWL继续闪烁")
    @pytest.mark.full
    def test_caseid_1995557(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.RiOn)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.RiOn,act_sts=IndcrSts.RiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.RiOn,act_sts=IndcrSts.Off)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.LeOn)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.LeOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.Off)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("请求开HWL_开启关闭左转_请求关闭HWL_HWL熄灭")
    @pytest.mark.full
    def test_caseid_1995556(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.LeOn)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.LeOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.Off)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("语音开启关闭左转_HzrdLiIndcnReq请求开启关闭HWL")
    @pytest.mark.full
    def test_caseid_1995555(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("按键开左转_HzrdLiIndcnReq请求开HWL失败左转继续闪烁")
    @pytest.mark.full
    def test_caseid_1995554(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("诊断复位_双闪频率")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995543(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:0x02})
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.sd_tester.reset_bgm()
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("io复位_双闪频率")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995545(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:0x02})
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.io_reset_bgm()
        sleep(15)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("休眠唤醒_双闪频率")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995547(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:0x02})
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Crash Driving Mode通过HzrdLiIndcnReq请求HWL失败")
    @pytest.mark.full
    def test_caseid_1995284(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Driving Mode通过HzrdLiIndcnReq请求HWL失败")
    @pytest.mark.full
    def test_caseid_1995285(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Transport Driving Mode通过HzrdLiIndcnReq请求HWL失败")
    @pytest.mark.full
    def test_caseid_1995286(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Driving Mode通过HzrdLiIndcnReq请求HWL失败")
    @pytest.mark.full
    def test_caseid_1995287(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Active Mode通过HzrdLiIndcnReq请求HWL失败")
    @pytest.mark.full
    def test_caseid_1995288(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Convenience Mode通过HzrdLiIndcnReq请求HWL失败")
    @pytest.mark.full
    def test_caseid_1995289(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Inactive Mode通过HzrdLiIndcnReq请求HWL失败")
    @pytest.mark.full
    def test_caseid_1995290(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Abandoned Mode通过HzrdLiIndcnReq请求HWL失败")
    @pytest.mark.full
    def test_caseid_1995291(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Driving Mode通过HzrdLiIndcnReq关闭HWL")
    @pytest.mark.full
    def test_caseid_1995292(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Driving Mode通过HzrdLiIndcnReq请求HWL")
    @pytest.mark.full
    def test_caseid_1995293(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("HzrdLiIndcnReq请求开HWL_按键开启左转闪烁_语音关左转_HWL继续闪烁")
    @pytest.mark.full
    def test_caseid_1995559(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:0x04})
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Crash Driving mode后碰撞预警（RCW）无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994314(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("Dyno Driving mode后碰撞预警（RCW）无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994315(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("Transport Driving mode后碰撞预警（RCW）无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994316(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("Factory Driving mode后碰撞预警（RCW）无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994317(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("Normal Active mode后碰撞预警（RCW）无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994318(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("Normal Convenience mode后碰撞预警（RCW）无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994319(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("Normal Inactive mode后碰撞预警（RCW）无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994320(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("Normal Abandoned mode后碰撞预警（RCW）无法点亮HWL")
    @pytest.mark.full
    def test_caseid_1994321(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("按键开左转_47服务开HWL_47服务关HWL后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1997006(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("按键开右转_79服务开HWL_79服务关HWL后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1997005(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=79)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("按键开右转_111服务开HWL失败")
    @pytest.mark.full
    def test_caseid_1997004(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("按键开左转_PIB请求HWL失败")
    @pytest.mark.full
    def test_caseid_1997003(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("按键开右转_RCW请求HWL失败")
    @pytest.mark.full
    def test_caseid_1997002(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_rcw_req(req=RcwReq.No)
        sleep(1)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
    
    @allure.title("按键开左转_EBL请求HWL失败")
    @pytest.mark.full
    def test_caseid_1997001(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)

    @allure.title("按键开右转_AEB请求HWL失败")
    @pytest.mark.full
    def test_caseid_1997000(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(1)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOn)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("按键开左转_灯光秀激活失败")
    @pytest.mark.full
    def test_caseid_1996999(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        # 关闭灯关秀
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)

    @allure.title("111开左转_按键激活HWL闪烁_按键关闭HWL左转继续闪烁")
    @pytest.mark.full
    def test_caseid_1996997(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=111)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("111开右转_crash激活HWL闪烁_按键关闭HWL熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996996(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.mix.set_car_mode(car_mode=CarMode.CRASH)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("111开左转_防盗激活HWL闪烁_退出防盗熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996995(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(2)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("111开左转_闭锁HWL闪烁一个周期后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996994(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("111开右转_热失控激活HWL失败")
    @pytest.mark.full
    def test_caseid_1996993(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_hvbatt(128)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=111)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("111开左转_47服务开HWL_47服务关HWL后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996992(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("111开右转_79服务开HWL_79服务关HWL后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996991(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=79)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("111开左转_95服务开HWL_95服务关HWL后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996990(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=95)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("111开右转_111服务开HWL_95服务关HWL后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996989(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=111)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("111开右转_HzrdLiIndcnReq请求开HWL失败")
    @pytest.mark.full
    def test_caseid_1996988(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=111)
        sleep(1)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("111开左转_PIB请求HWL失败")
    @pytest.mark.full
    def test_caseid_1996987(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=111)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("111开右转_RCW请求HWL失败")
    @pytest.mark.full
    def test_caseid_1996986(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_rcw_req(req=RcwReq.No)
        sleep(1)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=111)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
    
    @allure.title("111开左转_EBL请求HWL失败")
    @pytest.mark.full
    def test_caseid_1996985(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=111)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)

    @allure.title("111开右转_AEB请求HWL失败")
    @pytest.mark.full
    def test_caseid_1996984(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(1)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOn)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=111)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("111开左转_灯光秀激活失败")
    @pytest.mark.full
    def test_caseid_1996983(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=111)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        # 关闭灯关秀
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)

    @allure.title("crash激活HWL闪烁_47开左转失败")
    @pytest.mark.full
    def test_caseid_1996981(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_car_mode(car_mode=CarMode.CRASH)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("crash激活HWL闪烁_79开右转失败")
    @pytest.mark.full
    def test_caseid_1996980(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_car_mode(car_mode=CarMode.CRASH)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("crash激活HWL闪烁_111开左转失败")
    @pytest.mark.full
    def test_caseid_1996979(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_car_mode(car_mode=CarMode.CRASH)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("防盗激活HWL闪烁_47开左转失败")
    @pytest.mark.full
    def test_caseid_1996978(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(2)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("防盗激活HWL闪烁_79开右转失败")
    @pytest.mark.full
    def test_caseid_1996977(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(2)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("防盗激活HWL闪烁_语音开左转失败")
    @pytest.mark.full
    def test_caseid_1996976(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(2)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("防盗激活HWL闪烁_按键开右转失败")
    @pytest.mark.full
    def test_caseid_1996975(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(2)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("防盗激活HWL闪烁_111开左转失败")
    @pytest.mark.full
    def test_caseid_1996974(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(2)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("47开左转_按键激活HWL闪烁_按键关闭HWL左转继续闪烁")
    @pytest.mark.full
    def test_caseid_1997056(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("47开右转_crash激活HWL闪烁_按键关闭HWL熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1997055(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.mix.set_car_mode(car_mode=CarMode.CRASH)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("47开左转_防盗激活HWL闪烁_退出防盗熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1997054(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(2)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("47开左转_闭锁HWL闪烁一个周期后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1997053(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("47开右转_热失控激活HWL失败")
    @pytest.mark.full
    def test_caseid_1997052(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_hvbatt(128)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("47开左转_47服务开HWL_47服务关HWL后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1997051(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("47开右转_79服务开HWL失败")
    @pytest.mark.full
    def test_caseid_1997050(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("47开左转_95服务开HWL失败")
    @pytest.mark.full
    def test_caseid_1997049(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("47开右转_111服务开HWL失败")
    @pytest.mark.full
    def test_caseid_1997048(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("47开右转_HzrdLiIndcnReq请求开HWL失败")
    @pytest.mark.full
    def test_caseid_1997047(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("47开左转_PIB请求HWL失败")
    @pytest.mark.full
    def test_caseid_1997046(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("47开右转_RCW请求HWL失败")
    @pytest.mark.full
    def test_caseid_1997045(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_rcw_req(req=RcwReq.No)
        sleep(1)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)
    
    @allure.title("47开左转_EBL请求HWL失败")
    @pytest.mark.full
    def test_caseid_1997044(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(5)

    @allure.title("47开右转_AEB请求HWL失败")
    @pytest.mark.full
    def test_caseid_1997043(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(1)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOn)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("47开左转_激活关闭灯光秀后左转继续闪烁")
    @pytest.mark.full
    def test_caseid_1997042(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("79开左转_按键激活HWL闪烁_按键关闭HWL左转继续闪烁")
    @pytest.mark.full
    def test_caseid_1997040(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("79开右转_crash激活HWL闪烁_按键关闭HWL熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1997039(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.mix.set_car_mode(car_mode=CarMode.CRASH)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("79开左转_防盗激活HWL闪烁_退出防盗熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1997038(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(2)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("79开左转_闭锁HWL闪烁一个周期后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1997037(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("79开右转_热失控激活HWL失败")
    @pytest.mark.full
    def test_caseid_1997036(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_hvbatt(128)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("79开左转_47服务开HWL_47服务关HWL后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1997035(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("79开右转_79服务开HWL_79服务关HWL后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1997034(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=79)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("79开左转_95服务开HWL失败")
    @pytest.mark.full
    def test_caseid_1997033(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("79开右转_111服务开HWL失败")
    @pytest.mark.full
    def test_caseid_1997032(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("79开右转_HzrdLiIndcnReq请求开HWL失败")
    @pytest.mark.full
    def test_caseid_1997031(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("79开左转_PIB请求HWL失败")
    @pytest.mark.full
    def test_caseid_1997030(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("79开右转_RCW请求HWL失败")
    @pytest.mark.full
    def test_caseid_1997029(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_rcw_req(req=RcwReq.No)
        sleep(1)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)
    
    @allure.title("79开左转_EBL请求HWL失败")
    @pytest.mark.full
    def test_caseid_1997028(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(5)

    @allure.title("79开右转_AEB请求HWL失败")
    @pytest.mark.full
    def test_caseid_1997027(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(1)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOn)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("79开左转_灯光秀激活失败")
    @pytest.mark.full
    def test_caseid_1997026(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)


    @allure.title("语音开右转_crash激活HWL闪烁_按键关闭HWL熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1997024(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.mix.set_car_mode(car_mode=CarMode.CRASH)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("语音开左转_防盗激活HWL闪烁_退出防盗熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1997023(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(2)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("语音开左转_闭锁HWL闪烁一个周期后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1997022(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("语音开右转_热失控激活HWL失败")
    @pytest.mark.full
    def test_caseid_1997021(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_hvbatt(128)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("语音开左转_47服务开HWL_47服务关HWL后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1997020(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("语音开右转_79服务开HWL_79服务关HWL后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1997019(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=79)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("语音开右转_111服务开HWL失败")
    @pytest.mark.full
    def test_caseid_1997018(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("语音开右转_HzrdLiIndcnReq请求开HWL失败")
    @pytest.mark.full
    def test_caseid_1997017(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("语音开左转_PIB请求HWL失败")
    @pytest.mark.full
    def test_caseid_1997016(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("语音开右转_RCW请求HWL失败")
    @pytest.mark.full
    def test_caseid_1997015(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_rcw_req(req=RcwReq.No)
        sleep(1)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
    
    @allure.title("语音开左转_EBL请求HWL失败")
    @pytest.mark.full
    def test_caseid_1997014(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)

    @allure.title("语音开右转_AEB请求HWL失败")
    @pytest.mark.full
    def test_caseid_1997013(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(1)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOn)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("语音开左转_灯光秀激活失败")
    @pytest.mark.full
    def test_caseid_1997012(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)

    @allure.title("按键开右转_crash激活HWL闪烁_按键关闭HWL右转继续闪烁")
    @pytest.mark.full
    def test_caseid_1997010(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.mix.set_car_mode(car_mode=CarMode.CRASH)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("按键开左转_防盗激活HWL闪烁_退出防盗熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1997009(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("按键开左转_闭锁HWL闪烁一个周期后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1997008(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("按键开右转_热失控激活HWL失败")
    @pytest.mark.full
    def test_caseid_1997007(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.set_hvbatt(128)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hvbatt(0)

    @allure.title("热失控激活HWL闪烁_47开左转_47关闭左转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996968(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hvbatt(0)
        sleep(5)

    @allure.title("热失控激活HWL闪烁_79开右转_79关闭有转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996967(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hvbatt(0)
        sleep(5)

    @allure.title("热失控激活HWL闪烁_语音开左转_语音关闭左转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996966(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hvbatt(0)

    @allure.title("热失控激活HWL闪烁_按键开右转_按键关闭右转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996965(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_hvbatt(0)

    @allure.title("热失控激活HWL闪烁_111开左转失败")
    @pytest.mark.full
    def test_caseid_1996964(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.set_hvbatt(128)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        
    @allure.title("47开HWL_47开左转_47关左转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996963(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("47开HWL_79开右转")
    @pytest.mark.full
    def test_caseid_1996962(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("47开HWL_语音开左转")
    @pytest.mark.full
    def test_caseid_1996961(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)
        
    @allure.title("47开HWL_按键开右转")
    @pytest.mark.full
    def test_caseid_1996960(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("47开HWL_111开左转失败")
    @pytest.mark.full
    def test_caseid_1996959(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("79开HWL_47开左转_47关左转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996958(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=79)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("79开HWL_79开左转_79关左转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996957(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=79)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("79开HWL_语音开左转")
    @pytest.mark.full
    def test_caseid_1996956(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=79)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("79开HWL_按键开右转")
    @pytest.mark.full
    def test_caseid_1996955(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=79)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("79开HWL_111开左转失败")
    @pytest.mark.full
    def test_caseid_1996954(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=79)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("111开HWL_47开左转_47关左转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996953(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=111)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("111开HWL_79开左转_79关左转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996952(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=111)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("111开HWL_语音开左转_语音关左转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996951(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=111)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("111开HWL_按键开右转_按键关右转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996950(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=111)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("111开HWL_111开左转失败")
    @pytest.mark.full
    def test_caseid_1996949(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=111)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("HzrdLiIndcnReq请求开HWL_47开左转_47关闭左转之后HWL继续闪烁")
    @pytest.mark.full
    def test_caseid_1996948(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("HzrdLiIndcnReq请求开HWL_79开右转_79关闭右转之后HWL继续闪烁")
    @pytest.mark.full
    def test_caseid_1996947(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)

    @allure.title("HzrdLiIndcnReq请求开HWL_111开左转失败")
    @pytest.mark.full
    def test_caseid_1996946(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.Yes)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_hzrdLiIndcn_req(req=YesOrNo.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("PIB激活HWL_47开左转_47关左转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996945(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)

    @allure.title("PIB激活HWL_79开右转_79关右转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996944(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)

    @allure.title("PIB激活HWL_语音开左转_语音关左转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996943(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)

    @allure.title("PIB激活HWL_按键开右转_按键关右转之后HWL继续闪烁")
    @pytest.mark.full
    def test_caseid_1996942(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("PIB激活HWL_111开左转失败")
    @pytest.mark.full
    def test_caseid_1996941(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.Active)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_pib_sts(pib_sts=DiagActLineSts.DisActive)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("RCW激活HWL_47开左转_47关左转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996940(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_rcw_req(req=RcwReq.No)
        sleep(1)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.check_hwl_lamp_flash_sts(flash_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("RCW激活HWL_79开右转_79关右转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996939(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_rcw_req(req=RcwReq.No)
        sleep(1)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.check_hwl_lamp_flash_sts(flash_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("RCW激活HWL_语音开左转_语音关左转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996938(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_rcw_req(req=RcwReq.No)
        sleep(1)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.check_hwl_lamp_flash_sts(flash_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)

    @allure.title("RCW激活HWL_按键开右转_按键关右转之后HWL继续闪烁")
    @pytest.mark.full
    def test_caseid_1996937(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_rcw_req(req=RcwReq.No)
        sleep(1)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.check_hwl_lamp_flash_sts(flash_time=1)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        for num in range(1):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.RiOn)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.RiOn,act_sts=IndcrSts.RiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.RiOn,act_sts=IndcrSts.Off)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_hwl_lamp_flash_sts(flash_time=1)
        self.bus_comm.set_rcw_req(req=RcwReq.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        
    @allure.title("RCW激活HWL_111开左转失败")
    @pytest.mark.full
    def test_caseid_1996936(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_rcw_req(req=RcwReq.No)
        sleep(1)
        self.bus_comm.set_rcw_req(req=RcwReq.Yes)
        self.check_hwl_lamp_flash_sts(flash_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_hwl_lamp_flash_sts(flash_time=3)
        self.bus_comm.set_rcw_req(req=RcwReq.No)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("EBL激活HWL_47开左转_47关左转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996935(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)

    @allure.title("EBL激活HWL_79开右转_79关右转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996934(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)

    @allure.title("EBL激活HWL_语音开左转_语音关左转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996933(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)

    @allure.title("EBL激活HWL_按键开右转_按键关右转之后HWL继续闪烁")
    @pytest.mark.full
    def test_caseid_1996932(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("EBL激活HWL_111开左转失败")
    @pytest.mark.full
    def test_caseid_1996931(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("AEB激活HWL_47开左转_47关左转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996930(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(1)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOn)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)

    @allure.title("AEB激活HWL_79开右转_79关右转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996929(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(1)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOn)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(5)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)

    @allure.title("AEB激活HWL_语音开左转_语音关左转之后熄灭所有转向灯")
    @pytest.mark.full
    def test_caseid_1996928(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(1)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOn)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)

    @allure.title("AEB激活HWL_按键开右转_按键关右转之后HWL继续闪烁")
    @pytest.mark.full
    def test_caseid_1996927(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(1)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOn)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("AEB激活HWL_111开左转失败")
    @pytest.mark.full
    def test_caseid_1996926(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(1)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOn)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_aeb_brake_req(req=AsySftyHWLReq.TurnOff)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("灯光秀开启_47开左转_47关左转之后灯光秀仍开开启")
    @pytest.mark.full
    def test_caseid_1996925(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        sleep(5)

    @allure.title("灯光秀开启_79开右转_79关右转之后灯光秀仍开开启")
    @pytest.mark.full
    def test_caseid_1996924(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        sleep(5)

    @allure.title("灯光秀开启_语音开左转_语音关左转之后灯光秀仍开开启")
    @pytest.mark.full
    def test_caseid_1996923(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)

    @allure.title("灯光秀开启_按键开右转_按键关右转之后灯光秀仍开开启")
    @pytest.mark.full
    def test_caseid_1996922(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)

    @allure.title("灯光秀开启_111开左转_111关左转之后灯光秀仍开开启")
    @pytest.mark.full
    def test_caseid_1996921(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=111)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)

    @allure.title("寻车开HWL_111开左转失败")
    @pytest.mark.full
    def test_caseid_1996916(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("寻车开HWL_按键开右转")
    @pytest.mark.full
    def test_caseid_1996917(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("寻车开HWL_语音开左转")
    @pytest.mark.full
    def test_caseid_1996918(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("寻车开HWL_79开右转")
    @pytest.mark.full
    def test_caseid_1996919(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("寻车开HWL_47开左转")
    @pytest.mark.full
    def test_caseid_1996920(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_hwl_lamp_flash_sts(flash_time=1,indcrdisp=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("解锁HWL闪烁两个周期_111开启左转")
    @pytest.mark.full
    def test_caseid_1996969(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.check_hwl_lamp_flash_sts(flash_time=2)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        sleep(3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=111)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("解锁HWL闪烁两个周期_按键开启右转")
    @pytest.mark.full
    def test_caseid_1996970(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.check_hwl_lamp_flash_sts(flash_time=2)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("解锁HWL闪烁两个周期_语音开启左转")
    @pytest.mark.full
    def test_caseid_1996971(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.check_hwl_lamp_flash_sts(flash_time=2)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("解锁HWL闪烁两个周期_79开启右转")
    @pytest.mark.full
    def test_caseid_1996972(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.check_hwl_lamp_flash_sts(flash_time=2)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("解锁HWL闪烁两个周期_47开启左转")
    @pytest.mark.full
    def test_caseid_1996973(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.check_hwl_lamp_flash_sts(flash_time=2)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
    
    @allure.title("111开右转_寻车请求HWL失败")
    @pytest.mark.full
    def test_caseid_1996982(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=111)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("按键开右转_寻车请求HWL失败")
    @pytest.mark.full
    def test_caseid_1996998(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("语音开右转_寻车请求HWL失败")
    @pytest.mark.full
    def test_caseid_1997011(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("79开右转_寻车请求HWL失败")
    @pytest.mark.full
    def test_caseid_1997025(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
    
    @allure.title("47开右转_寻车请求HWL失败")
    @pytest.mark.full
    def test_caseid_1997041(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)