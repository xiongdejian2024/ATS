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
@allure.story("灯光秀功能")
class TestExltlightCtrlABC(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["LightService_client"])
        sleep(2)
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)


    def before_each_func(self, ecu):
        self.soa.start_get_light_inhibit_sts()
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()
        self.bus_comm.set_vehspd_gear(vehspd=0)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)

    def after_each_func(self, ecu):
        self.soa.stop_get_light_inhibit_sts()
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=0)
        sleep(1)

    def after_class(self, ecu):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)

    @allure.title("车外闭锁灯舞自动关闭（CDC逻辑）")#车外闭锁灯舞自动关闭 
    @pytest.mark.smoke
    def test_caseid_1959953(self):
        self.soa.hmi_set_light_show_active(status=False)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.soa.set_light_show_file(sequence_id='SEQUENCE_DANCE_A',act=SequenceAction.kSequenceStart)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        
    @allure.title("用户挂R挡打断灯舞")#用户挂R挡打断灯舞 
    @pytest.mark.smoke
    def test_caseid_1959954(self):
        self.soa.hmi_set_light_show_active(status=False)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.DISABLE)


    @allure.title("用户挂D挡打断灯舞")#用户挂D挡打断灯舞 
    @pytest.mark.smoke
    def test_caseid_1959955(self):
        self.soa.hmi_set_light_show_active(status=False)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.DISABLE)

    @allure.title("用户触发近光灯暂停灯舞（CDC逻辑）")#用户触发近光灯暂停灯舞 
    @pytest.mark.smoke
    def test_caseid_1959956(self):
        self.soa.hmi_set_light_show_active(status=False)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.soa.set_light_show_file(sequence_id='SEQUENCE_DANCE_A',act=SequenceAction.kSequenceStart)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.soa.send_method_request("LightService_client", "SetExteriorLightMode", {"mode": 3}) #外灯模式打开
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)

    @allure.title("设置灯光秀暂停")
    @pytest.mark.smoke
    def test_caseid_1959957(self):
        self.soa.hmi_set_light_show_active(status=False)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.soa.set_light_show_file(sequence_id='SEQUENCE_DANCE_A',act=SequenceAction.kSequenceStart)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.soa.set_light_show_file(sequence_id='SEQUENCE_DANCE_A',act=SequenceAction.kSequenceStop)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)

    @allure.title("设置灯舞关闭")#设置灯舞关闭 
    @pytest.mark.smoke
    def test_caseid_1959958(self):
        self.soa.hmi_set_light_show_active(status=False)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.soa.set_light_show_file(sequence_id='SEQUENCE_DANCE_A',act=SequenceAction.kSequenceStart)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.soa.set_light_show_file(sequence_id='SEQUENCE_DANCE_A',act=SequenceAction.kSequencePause)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.soa.hmi_set_light_show_active(status=False)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)

    @allure.title("设置灯舞激活")#设置灯舞激活 
    @pytest.mark.smoke
    def test_caseid_1959959(self):
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.soa.set_light_show_file(sequence_id='SEQUENCE_DANCE_A',act=SequenceAction.kSequenceStart)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)

    @allure.title("电量25%解锁后AI灯1s内流水点亮并保持-车速大于0或闭锁AI灯熄灭")
    @pytest.mark.full
    def test_caseid_1913449(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_25',act=SequenceAction.kSequenceStart)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,0.0,0.0,0.0],[100.0,0.0,0.0,0.0])
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_25',act=SequenceAction.kSequenceStop)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0])

    @allure.title("电量25%解锁后AI灯1s内流水点亮并保持-挡位非P挡AI灯熄灭")
    @pytest.mark.full
    def test_caseid_1913450(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_25',act=SequenceAction.kSequenceStart)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,0.0,0.0,0.0],[100.0,0.0,0.0,0.0])
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,0.0,0.0,0.0],[100.0,0.0,0.0,0.0])
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_Off)
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_25',act=SequenceAction.kSequenceStop)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0])


    @allure.title("电量50%解锁后AI灯1s内流水点亮并保持-车速大于0或闭锁AI灯熄灭")
    @pytest.mark.full
    def test_caseid_1913452(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_50',act=SequenceAction.kSequenceStart)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,100.0,0.0,0.0],[100.0,100.0,0.0,0.0])
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_50',act=SequenceAction.kSequenceStop)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0])

    @allure.title("电量75%解锁后AI灯1s内流水点亮并保持-车速大于0或闭锁AI灯熄灭")
    @pytest.mark.full
    def test_caseid_1913453(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_75',act=SequenceAction.kSequenceStart)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,100.0,100.0,0.0],[100.0,100.0,100.0,0.0])
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_75',act=SequenceAction.kSequenceStop)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0])

    @allure.title("电量100%解锁后AI灯1s内流水点亮并保持-车速大于0或闭锁AI灯熄灭")
    @pytest.mark.full
    def test_caseid_1913454(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_100',act=SequenceAction.kSequenceStart)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,100.0,100.0,100.0],[100.0,100.0,100.0,100.0])
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_100',act=SequenceAction.kSequenceStop)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0])

    @allure.title("电量50%解锁后AI灯1s内流水点亮并保持-挡位非P挡AI灯熄灭")
    @pytest.mark.full
    def test_caseid_1913455(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_50',act=SequenceAction.kSequenceStart)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,100.0,0.0,0.0],[100.0,100.0,0.0,0.0])
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,100.0,0.0,0.0],[100.0,100.0,0.0,0.0])
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_Off)
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_50',act=SequenceAction.kSequenceStop)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0])

    @allure.title("电量75%解锁后AI灯1s内流水点亮并保持-挡位非P挡AI灯熄灭")
    @pytest.mark.full
    def test_caseid_1913456(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_75',act=SequenceAction.kSequenceStart)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,100.0,100.0,0.0],[100.0,100.0,100.0,0.0])
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,100.0,100.0,0.0],[100.0,100.0,100.0,0.0])
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_Off)
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_75',act=SequenceAction.kSequenceStop)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0])

    @allure.title("电量100%解锁后AI灯1s内流水点亮并保持-挡位非P挡AI灯熄灭")
    @pytest.mark.full
    def test_caseid_1913457(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_100',act=SequenceAction.kSequenceStart)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,100.0,100.0,100.0],[100.0,100.0,100.0,100.0])
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,100.0,100.0,100.0],[100.0,100.0,100.0,100.0])
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_Off)
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_100',act=SequenceAction.kSequenceStop)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0])

    @allure.title("电量25%充电触发AI灯动态流水点亮并保持-30s后熄灭")
    @pytest.mark.sanity
    def test_caseid_1913458(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_25',act=SequenceAction.kSequenceStart)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,0.0,0.0,0.0],[100.0,0.0,0.0,0.0])
        sleep(30)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,0.0,0.0,0.0],[100.0,0.0,0.0,0.0])
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_25',act=SequenceAction.kSequenceStop)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0])

    @allure.title("电量50%充电触发AI灯动态流水点亮并保持-30s后熄灭")
    @pytest.mark.sanity
    def test_caseid_1913459(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_50',act=SequenceAction.kSequenceStart)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,100.0,0.0,0.0],[100.0,100.0,0.0,0.0])
        sleep(30)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,100.0,0.0,0.0],[100.0,100.0,0.0,0.0])
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_50',act=SequenceAction.kSequenceStop)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0])

    @allure.title("电量75%充电触发AI灯动态流水点亮并保持-30s后熄灭")
    @pytest.mark.sanity
    def test_caseid_1913460(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_75',act=SequenceAction.kSequenceStart)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,100.0,100.0,0.0],[100.0,100.0,100.0,0.0])
        sleep(30)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,100.0,100.0,0.0],[100.0,100.0,100.0,0.0])
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_75',act=SequenceAction.kSequenceStop)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0])
    
    @allure.title("电量100%充电触发AI灯动态流水点亮并保持-30s后熄灭")
    @pytest.mark.sanity
    def test_caseid_1913461(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_100',act=SequenceAction.kSequenceStart)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,100.0,100.0,100.0],[100.0,100.0,100.0,100.0])
        sleep(30)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([100.0,100.0,100.0,100.0],[100.0,100.0,100.0,100.0])
        self.soa.set_light_show_file(sequence_id='AI_CHARGE_DONE_100',act=SequenceAction.kSequenceStop)
        self.bus_comm.check_AI_Inter_actionLamp_Sts([0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0])

    @allure.title("灯光秀状态故障_当StsOfLedFrntLampLe2==0x02")
    @pytest.mark.full
    def test_caseid_1990184(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.bus_comm.set_singal("bodyexposedcanfd","RcmlBodyExpoFr01","StsOfLedReLampLe2",2)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_Err)
        # 恢复
        self.bus_comm.set_singal("bodyexposedcanfd","RcmlBodyExpoFr01","StsOfLedReLampLe2",1)

    @allure.title("灯光秀状态故障_当StsOfLedFrntLampLe1==0x02")
    @pytest.mark.full
    def test_caseid_1990185(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.bus_comm.set_singal("bodyexposedcanfd","HcmlBodyExpoFr02","StsOfLedFrntLampLe1",2)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_Err)
        # 恢复
        self.bus_comm.set_singal("bodyexposedcanfd","HcmlBodyExpoFr02","StsOfLedFrntLampLe1",1)

    @allure.title("灯光秀状态故障_当StsOfLedFrntLampMid1==0x02")
    @pytest.mark.full
    def test_caseid_1990186(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.bus_comm.set_singal("bodyexposedcanfd","HcmlBodyExpoFr02","StsOfLedFrntLampMid1",2)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_Err)
        # 恢复
        self.bus_comm.set_singal("bodyexposedcanfd","HcmlBodyExpoFr02","StsOfLedFrntLampMid1",1)

    @allure.title("灯光秀状态故障_当StsOfLedFrntLampRi2==0x02")
    @pytest.mark.full
    def test_caseid_1990187(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.bus_comm.set_singal("bodyexposedcanfd","HcmrBodyExpoFr02","StsOfLedFrntLampRi2",2)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_Err)
        # 恢复
        self.bus_comm.set_singal("bodyexposedcanfd","HcmrBodyExpoFr02","StsOfLedFrntLampRi2",1)

    @allure.title("灯光秀状态故障_当StsOfLedFrntLampRi1==0x02")
    @pytest.mark.full
    def test_caseid_1990188(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.bus_comm.set_singal("bodyexposedcanfd","HcmrBodyExpoFr02","StsOfLedFrntLampRi1",2)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_Err)
        # 恢复
        self.bus_comm.set_singal("bodyexposedcanfd","HcmrBodyExpoFr02","StsOfLedFrntLampRi1",1)

    @allure.title("灯光秀状态故障_当StsOfLedReLampRi2==0x02")
    @pytest.mark.full
    def test_caseid_1990189(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.bus_comm.set_singal("bodyexposedcanfd","RcmrBodyExpoFr01","StsOfLedReLampRi2",2)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_Err)
        # 恢复
        self.bus_comm.set_singal("bodyexposedcanfd","RcmrBodyExpoFr01","StsOfLedReLampRi2",1)

    @allure.title("灯光秀状态故障_当StsOfLedReLampRi1==0x02")
    @pytest.mark.full
    def test_caseid_1990190(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.bus_comm.set_singal("bodyexposedcanfd","RcmrBodyExpoFr01","StsOfLedReLampRi1",2)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_Err)
        # 恢复
        self.bus_comm.set_singal("bodyexposedcanfd","RcmrBodyExpoFr01","StsOfLedReLampRi1",1)

    @allure.title("灯光秀故障_当StsOfLedReLampLe1==0x02")
    @pytest.mark.full
    def test_caseid_1990192(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.bus_comm.set_singal("bodyexposedcanfd","RcmlBodyExpoFr01","StsOfLedReLampLe1",2)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_Err)
        # 恢复
        self.bus_comm.set_singal("bodyexposedcanfd","RcmlBodyExpoFr01","StsOfLedReLampLe1",1)

    @allure.title("灯光秀故障_当StsOfLedReLampLe2==0x02")
    @pytest.mark.full
    def test_caseid_1990193(self):
        self.sd_tester.write_ccp({950 : 0x1})
        self.soa.hmi_set_light_show_active(status=False)
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ENABLE)
        self.soa.hmi_set_light_show_active(status=True)  # 设置灯光秀激活状态
        self.bus_comm.check_static_lighting_mode_en(static_lighting_mode_en=StaticLightingModeEn.ACTIVATED)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_On)
        self.bus_comm.set_singal("bodyexposedcanfd","RcmlBodyExpoFr01","StsOfLedReLampLe2",2)
        self.bus_comm.check_ExtrLtgStsStaticLtgShow(ExtrLtgStsStaticLtgShow=ExtrLtgStsStaticLtgShow.DevSts4_Err)
        # 恢复
        self.bus_comm.set_singal("bodyexposedcanfd","RcmlBodyExpoFr01","StsOfLedReLampLe2",1)