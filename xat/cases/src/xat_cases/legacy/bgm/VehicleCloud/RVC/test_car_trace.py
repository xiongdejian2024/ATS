#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import time
import pytest
import allure
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
import threading 

times_light = 0
times_horn = 0

@allure.feature("远程控制/远控两域联调测试/远控寻车")
@allure.story("远控寻车")
class TestRvcTailgate(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["LightService_client","KeyService_client"])
        sleep(3)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        times_light = 0
        times_horn = 0
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr18", "TrsmParkLockdTrsmParkLockd", 'TrsmParkLock1_ParkEngd')
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr03", "GearLvrIndcn_1_EcmPropSignalIPdu24",'GearLvrIndcn2_ParkIndcn')  
        sleep(2) 

    def after_each_func(self, ecu):
        sleep(5)
        super().after_each_func(ecu)

    def start_thread_check_lamp(self):
        global times_light
        times_light = self.bus_comm.ipdu.check_event(self.bus_comm.ipdu.bodyexposedcanfd.CemBodyExpoFr51,'ActvnOfIndcrIndcrOut', 0,3)

    def start_thread_check_horn(self):
        global times_horn
        times_horn = self.bus_comm.ipdu.check_event(self.bus_comm.ipdu.backbonefr.CemBackBoneFr18,'ActvOfHorn', 0,1)

    def after_class(self, ecu):
        pass

    def check_car_location_sts(self,sts:CarLocalTraceReq,last_time:int = 1):
        global times_light,times_horn
        promt_info = f"---------------->检查总线寻车的状态是否为{sts.name},检测的持续时间为{last_time}"
        with allure.step(promt_info):
            logger.info(promt_info)

        thread_lamp = threading.Thread(target=self.start_thread_check_lamp, args=())
        thread_lamp.setDaemon(True)
        thread_horn = threading.Thread(target=self.start_thread_check_horn, args=())
        thread_horn.setDaemon(True)
        thread_lamp.start()
        thread_horn.start()
        sleep(6)
          
        if sts.name == "kLiReq":
            if times_light != 0 and times_horn ==0:
                logger.info("检测到有闪灯,没有鸣笛")
                promt_info = f"---------------->检测到有闪灯,没有鸣笛"
                assert True
            else:
                logger.info("没有检测到闪灯")
                assert False
        elif sts.name == "kHornLiReq":
            if times_light != 0 and times_horn !=0:
                logger.info("检测到有闪灯鸣笛")
                promt_info = f"---------------->检测到有闪灯鸣笛"
                assert True
            else:
                logger.info("没有检测到闪灯和鸣笛")
                assert False

    @allure.title("RVCpanicVehicle_FlashWhist_Success")
    @pytest.mark.smoke
    def test_car_trace_caseid_1984899(self):
        self.mix.set_common_precontion()
        sleep(1)
        self.tsp.rvc_find_vehicle(op=1)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.All,sts=PosnLampSts.On)
        self.check_car_location_sts(sts=CarLocalTraceReq.kHornLiReq)
        self.soa.event_check_NotifyCarLocalTraceActiveStatus(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("RVCpanicVehicle_Flash_Successs")
    @pytest.mark.smoke
    def test_car_trace_caseid_1984898(self):
        self.mix.set_common_precontion()
        sleep(1)
        self.tsp.rvc_find_vehicle(op=2)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.All,sts=PosnLampSts.On)
        self.check_car_location_sts(sts=CarLocalTraceReq.kLiReq)
        self.soa.event_check_NotifyCarLocalTraceActiveStatus(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"  