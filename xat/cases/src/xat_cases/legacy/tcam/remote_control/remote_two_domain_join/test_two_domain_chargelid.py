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


@allure.feature("远程控制/远控两域联调测试/远控充电口盖")
@allure.story("远控充电口盖")
class TestRvcChargeLid(TestABCBase):
    def before_class(self, ecu):
        pass

    def before_each_func(self, ecu):
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr18", "TrsmParkLockdTrsmParkLockd", 'TrsmParkLock1_ParkEngd')
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr03", "GearLvrIndcn_1_EcmPropSignalIPdu24",'GearLvrIndcn2_ParkIndcn')  
         
    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        pass

    @allure.title("远程控制-RVCChargeCover_Closed_abandoned")
    @pytest.mark.join_smoke
    def test_open_ChargeLid_caseid_1980495(self):
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr09", "ChrgLidRearSts")
        self.tsp.rvc_charge_Lidgate()
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE) 
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcActPosn2", 100) 
        self.bus_comm.check_signal_thread_stop('ChrgLidRearSts')
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVCChargeCover_Opened_inactive")
    @pytest.mark.join_smoke
    def test_open_ChargeLid_caseid_1980497(self):
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr09", "ChrgLidRearSts")
        self.tsp.rvc_charge_Lidgate()   
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcActPosn2", 100) 
        self.bus_comm.check_signal_thread_stop('ChrgLidRearSts')
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVCChargeCover_Closed_abandoned")
    @pytest.mark.join_smoke
    def test_close_ChargeLid_caseid_1980496(self):
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr09", "ChrgLidRearSts")
        self.tsp.rvc_charge_Lidgate(-1)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcActPosn2", 0) 
        self.bus_comm.check_signal_thread_stop('ChrgLidRearSts')
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVCChargeCover_Closed_inactive")
    @pytest.mark.join_smoke
    def test_close_ChargeLid_caseid_1980494(self):
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr09", "ChrgLidRearSts")
        self.tsp.rvc_charge_Lidgate(-1)   
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcActPosn2", 0) 
        self.bus_comm.check_signal_thread_stop('ChrgLidRearSts')
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"   
                                  
 # pytest -vs -p no:warnings remote_control/remote_two_domain_join/test_two_domain_chargelid.py      