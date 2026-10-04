#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_service_exhibiton_mode_abc.py
@Author      : heng.wang@jiduauto.com
@Time        : 2024/1/29 13:20
@Description: BGM维修模式服务相关抽象接口用例
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
from xat_ecu.api.constants.common import *


@allure.feature("车控车设")
@allure.story("整车模式/展车模式")
class TestUsageMode(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["VehicleModeService_client", "VehicleSetStatusService_client"])
        time.sleep(5)

    def before_each_func(self, ecu):
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        self.bus_comm.set_epb_sts(sts=3)
        time.sleep(1)
        self.soa.set_maintain_mode(status=False)
        self.soa.check_maintain_mode(status=False)
        self.bus_comm.set_dtc_pre()
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        
        pass

    def after_each_func(self, ecu):
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.driver_seat_notpresent()
        self.bus_comm.set_secle_seat_notpresent()
        self.bus_comm.set_pass_seat_notpresent()
        self.io.hazard_light_close()
        self.io.bgm_diag_line_up()
        self.io.tcam_kl15_up()
        pass

    def after_class(self, ecu):
        self.soa.set_maintain_mode(status=False)
        self.soa.check_maintain_mode(status=False)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.io.bgm_diag_line_up()
        self.bus_comm.resume_all_bus_send()


    # ---------------------------->展车模式<---------------------------------------------
    @pytest.mark.smoke
    def test_caseid_118588(self):
        "服务进维修模式"
        self.soa.set_and_check_maintain_mode(status=True)
    
    @pytest.mark.smoke
    def test_caseid_118589(self):
        "服务退维修模式"
        self.soa.set_and_check_maintain_mode(status=True)
        self.soa.set_and_check_maintain_mode(status=False)
    
    @pytest.mark.sanity
    @pytest.mark.single_bgm
    @pytest.mark.nvm
    def test_caseid_118585(self):
        "bgm休眠唤醒保持维修模式"
        self.soa.set_and_check_maintain_mode(status=True)
        self.mix.network_sleep()
        self.io.bgm_diag_line_up()
        self.bus_comm.resume_all_bus_send()
        time.sleep(25)
        self.soa.check_maintain_mode(status=True)
    
    @pytest.mark.sanity
    @pytest.mark.nvm
    def test_caseid_118584(self):
        "bgm上下电保持维修模式"
        self.soa.set_and_check_maintain_mode(status=True)
        time.sleep(1)
        self.io.bgm_power_off()
        time.sleep(5)
        self.io.bgm_power_on()
        time.sleep(25)
        self.soa.check_maintain_mode(status=True)
    
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994576(self):
        "bgm诊断重启保持维修模式"
        self.soa.set_and_check_maintain_mode(status=True)
        time.sleep(1)
        self.sd_tester.reset_bgm()
        self.soa.check_maintain_mode(status=True)
    
    
    
    
    


   


    