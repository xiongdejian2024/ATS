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
@allure.story("近光灯功能")
class TestExltlightCtrlABC(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["LightService_client","CentralLockService_client"])
        self.sd_tester.set_ccp(ccp_vlaue={274:0x80})
        sleep(2)

    def before_each_func(self, ecu):
        self.soa.start_get_light_inhibit_sts()
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()
        self.bus_comm.resume_all_bus_send()

    def after_each_func(self, ecu):
        self.soa.stop_get_light_inhibit_sts()
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)
        sleep(1)

    def after_class(self, ecu):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)

    @allure.title("active下近光关CDC断连BGM主动设置外灯Auto")
    @pytest.mark.sanity
    def test_caseid_113531(self):
       self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
       self.mix.set_lb_off_and_night_mode_sped0()
       self.soa.stop_get_light_inhibit_sts()
       sleep(.5)
       self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
       self.soa.start_get_light_inhibit_sts()

    @allure.title("Factory active mode_夜晚自动切手动近光继续被点亮")
    @pytest.mark.full
    def test_caseid_114761(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_night_mode(wait_time=2)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Normal abandoned mode_休眠唤醒近光_5S内不点亮")
    @pytest.mark.full
    def test_caseid_1982363(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.io.io_reset_bgm()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        sleep(15)

    @allure.title("功能安全_白天黑夜信号OutdBri丢失超过500ms，默认为黑夜模式")
    @pytest.mark.full
    def test_caseid_1988607(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_day_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.pause_bus_send("cem_lin1")
        sleep(.6)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.resume_bus_send("cem_lin1")

    @allure.title("安全要求近光与光传感器(RLSM)通信_夜晚模式自动近光CRC正确LIN信号只有一个")
    @pytest.mark.full
    def test_caseid_1988608(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_twilight_sensor_sts(OutdBri=OutdBriSts.Day)
        self.bus_comm.set_twilight_sensor_sts(OutdBri=OutdBriSts.Ukwn)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)


    @allure.title("功能安全_StsOfLedLoBeamRi故障时使能ActnOfLedLoBeam不应被关闭")
    @pytest.mark.full
    def test_caseid_1988614(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={274:0x80})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.Error)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.On)

    @allure.title("功能安全StsOfLedLoBeamLe故障时使能ActnOfLedLoBeam不应被关闭")
    @pytest.mark.full
    def test_caseid_1988615(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={274:0x80})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.Error)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.On)

    @allure.title("功能安全_Normal Driving mode_信号“OutdBri”E2E校验失败，近光亮")
    @pytest.mark.full
    def test_caseid_1988616(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={274:0x80})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.ipdu.set_no_crc(self.bus_comm.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'OutdBriSts')
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.ipdu.restore_crc(self.bus_comm.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'OutdBriSts')

    @allure.title("左侧近光灯故障，右侧近光灯状态不受影响")
    @pytest.mark.full
    def test_caseid_1990177(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={274:0x80})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.Error)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.On)

    @allure.title("左日行灯因故障关闭时，右日行灯一同关闭")
    @pytest.mark.full
    def test_caseid_1990178(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={274:0x80})
        self.soa.get_and_set_extilight_mode(ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_drl_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.Error)
        self.bus_comm.check_drl_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.set_drl_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.Off)

    @allure.title("位置灯开启，RCMM节点丢失，位置灯状态故障")
    @pytest.mark.full
    def test_caseid_1990179(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_singal("bodyexposedcanfd","CEMBodyExpoCommonFr06","ExtrLiRlyPwrDwn",0)
        sleep(1.5)
        self.bus_comm.stop_send_pdu('bodyexposedcanfd','RcmmBodyExpoFr02')
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.resume_bus_send('bodyexposedcanfd')

    @allure.title("位置灯开启，RCMR节点丢失，近光灯状态故障")
    @pytest.mark.full
    def test_caseid_1990180(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.stop_send_pdu('bodyexposedcanfd','RcmrBodyExpoFr01')
        sleep(1.5)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.resume_bus_send('bodyexposedcanfd')

    @allure.title("位置灯开启，RCML节点丢失，近光灯状态故障")
    @pytest.mark.full
    def test_caseid_1990181(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.stop_send_pdu('bodyexposedcanfd','RcmlBodyExpoFr01')
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.resume_bus_send('bodyexposedcanfd')

    @allure.title("近光灯开启，HCMR节点丢失，近光灯状态故障")
    @pytest.mark.full
    def test_caseid_1990182(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.stop_send_pdu('bodyexposedcanfd','HcmrBodyExpoFr02')
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.resume_bus_send('bodyexposedcanfd')

    @allure.title("近光灯开启，HCML节点丢失，近光灯状态故障")
    @pytest.mark.full
    def test_caseid_1990183(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.stop_send_pdu('bodyexposedcanfd','HcmlBodyExpoFr02')
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.resume_bus_send('bodyexposedcanfd')

    @allure.title("功能安全_Normal Driving mode_信号“VehSpdLgt”E2E校验失败，近光亮")
    @pytest.mark.full
    def test_caseid_1987189(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.bus_comm.set_day_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.ipdu.set_no_crc(self.bus_comm.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06')
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.ipdu.restore_crc(self.bus_comm.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06')