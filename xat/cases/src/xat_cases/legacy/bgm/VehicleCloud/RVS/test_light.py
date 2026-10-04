#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_rvs.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/12/1 11:30
@Description: BGM RVS功能测试
"""

import os
import sys
import pytest
import allure
from time import sleep
import threading
import math

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.tsp.rvs_client import RvsClient
from signal_value_mapping import *

@allure.feature("BGM车云")
@allure.story("基础数据上报")
@pytest.mark.order_last
class TestRVS(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["VehicleModeService_client","VehicleSetStatusService_client","LightService_client"])
        sleep(3)
        self.vid = self.tb_config["vid"]
        self.rvs_client = RvsClient(vid=self.vid)
        logger.info("VID: {0}".format(self.vid))
        sleep(2)

    def before_each_func(self, ecu):
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()
        self.io.hazard_light_close()

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={950:1})
        self.sd_tester.write_ccp({225: 7, 226: 7}) 
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass


    @pytest.mark.sanity
    @pytest.mark.fail
    def test_caseid_112838_116051(self):
        '''开启近光灯 '''
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.mix.set_and_check_low_beam(sts=isOn.Off)
        sleep(2)
        self.mix.set_and_check_low_beam(sts=isOn.On)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["light","zoneId==0","type==6","status"],target_value=1
            )
        # self.tsp.check_rvs_data_update_new(
        #         block=BlockName.Light,keys=["light","zoneId==0","type==3","status"],target_value=1
        #     )
        
        

    @pytest.mark.full
    def test_caseid_116061(self):
        '''开启刹车灯 '''
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={508:3})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["light","zoneId==0","type==0","status"],target_value=1
            )
        sleep(2)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["light","zoneId==0","type==0","status"],target_value=0
            )
        
    @pytest.mark.sanity
    def test_caseid_112836(self):
        '''开启左转灯 '''
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={629:6})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(2)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["turnLampMode"],target_value=1
            )
        sleep(2)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["turnLampMode"],target_value=0
            )

    @pytest.mark.sanity
    def test_caseid_112835(self):
        '''开启右转灯 '''
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={629:6})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(2)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["turnLampMode"],target_value=2
            )
        sleep(2)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["turnLampMode"],target_value=0
            )
        
    @pytest.mark.full
    def test_caseid_116046(self):
        '''危险报警灯'''
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={629:6})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(2)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["turnLampMode"],target_value=3
            )
        sleep(2)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["turnLampMode"],target_value=0
            )

    @pytest.mark.full
    def test_caseid_116055_116057(self):
        '''开启前位置灯 '''
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        sleep(2)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["light","zoneId==9","type==11","status"],target_value=1
            )
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        
    @pytest.mark.full
    def test_caseid_116050(self):
        '''开启倒车灯 '''
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={259:2,508:3})
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Rvs)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["light","zoneId==0","type==8","status"],target_value=1
            )
        sleep(2)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Fwd)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["light","zoneId==0","type==8","status"],target_value=0
            )

    @pytest.mark.full
    def test_caseid_116049(self):
        '''后雾灯'''
        self.mix.set_ccp({225:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.Off)
        sleep(2)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["light","zoneId==10","type==4","status"],target_value=1
            )
        sleep(2)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.Off)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["light","zoneId==10","type==4","status"],target_value=0
            )
        

    @pytest.mark.sanity
    def test_caseid_112837(self):
        '''远光灯'''
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        sleep(2)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["highBeamStatus"],target_value=1)
        sleep(2)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["highBeamStatus"],target_value=0)
        

    @pytest.mark.full
    @pytest.mark.v210
    def test_caseid_1990888(self):
        '''左adas灯'''
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={950:2})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.set_car_mode(CarMode.NORMAL)
        self.bus_comm.set_singal("bodyexposedcanfd","HcmlBodyExpoFr02", 'StsOfLedFrntWheelLampLe', 0)
        sleep(2)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.mix.set_car_mode(CarMode.NORMAL)
        self.bus_comm.set_singal("bodyexposedcanfd","HcmlBodyExpoFr02", 'StsOfLedFrntWheelLampLe', 1)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["light","zoneId==12","type==40","status"],target_value=1
            )
        sleep(2)
        self.bus_comm.set_singal("bodyexposedcanfd","HcmlBodyExpoFr02", 'StsOfLedFrntWheelLampLe', 0)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["light","zoneId==12","type==40","status"],target_value=0
            )
        

    @pytest.mark.full
    @pytest.mark.v210
    def test_caseid_1990887(self):
        '''右adas灯'''
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={950:2})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.set_car_mode(CarMode.NORMAL)
        self.bus_comm.set_singal("bodyexposedcanfd","RcmrBodyExpoFr01", 'StsOfLedReWheelLampRi',0)
        sleep(2)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.mix.set_car_mode(CarMode.NORMAL)
        self.bus_comm.set_singal("bodyexposedcanfd","RcmrBodyExpoFr01", 'StsOfLedReWheelLampRi', 1)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["light","zoneId==13","type==40","status"],target_value=1
            )
        sleep(2)
        self.bus_comm.set_singal("bodyexposedcanfd","RcmrBodyExpoFr01", 'StsOfLedReWheelLampRi', 0)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["light","zoneId==13","type==40","status"],target_value=0
            )
        


    @pytest.mark.full
    @pytest.mark.v210
    def test_caseid_1990890(self):
        '''前adas灯'''
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={950:2})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.set_car_mode(CarMode.NORMAL)
        self.bus_comm.set_singal("bodyexposedcanfd","HcmrBodyExpoFr02", 'StsOfLedFrntWheelLampRi', 0)
        sleep(2)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.mix.set_car_mode(CarMode.NORMAL)
        self.bus_comm.set_singal("bodyexposedcanfd","HcmrBodyExpoFr02", 'StsOfLedFrntWheelLampRi', 1)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["light","zoneId==9","type==40","status"],target_value=1
            )
        sleep(2)
        self.bus_comm.set_singal("bodyexposedcanfd","HcmrBodyExpoFr02", 'StsOfLedFrntWheelLampRi', 0)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["light","zoneId==9","type==40","status"],target_value=0
            )
        

    @pytest.mark.full
    @pytest.mark.v210
    def test_caseid_1990889(self):
        '''后adas灯'''
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={950:2})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.set_car_mode(CarMode.NORMAL)
        self.bus_comm.set_singal("bodyexposedcanfd","RcmlBodyExpoFr01", 'StsOfLedReWheelLampLe', 0)
        sleep(2)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.mix.set_car_mode(CarMode.NORMAL)
        self.bus_comm.set_singal("bodyexposedcanfd","RcmlBodyExpoFr01", 'StsOfLedReWheelLampLe', 1)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["light","zoneId==10","type==40","status"],target_value=1
            )
        sleep(2)
        self.bus_comm.set_singal("bodyexposedcanfd","RcmlBodyExpoFr01", 'StsOfLedReWheelLampLe', 0)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.Light,keys=["light","zoneId==10","type==40","status"],target_value=0
            )
    
        

