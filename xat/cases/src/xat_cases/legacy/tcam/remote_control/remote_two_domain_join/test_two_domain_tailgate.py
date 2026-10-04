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


@allure.feature("远程控制/远控两域联调测试/远控尾门")
@allure.story("远控尾门")
class TestRvcTailgate(TestABCBase):
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

    @allure.title("远程控制-RVCWindows_open_INACTIVE")
    @pytest.mark.join_smoke
    def test_open_tailgate_caseid_1980499(self):
        self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr02", 'TrOpenerReqTrOpenerReq')
        self.tsp.rvc_tailgate_control(1) 
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", 'TrOpenerSts', 5)
        self.bus_comm.check_signal_thread_stop('TrOpenerReqTrOpenerReq')
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVCtaildoor_Opened_abandoned")
    @pytest.mark.join_smoke
    def test_open_tailgate_caseid_1980505(self):
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr02", 'TrOpenerReqTrOpenerReq')
        self.tsp.rvc_tailgate_control(1) 
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", 'TrOpenerSts', 5)
        self.bus_comm.check_signal_thread_stop('TrOpenerReqTrOpenerReq')
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVCtaildoor_Cocked_Inactive")
    @pytest.mark.join_smoke
    def test_cocked_tailgate_caseid_1980498(self):
        self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr02", 'TrOpenerReqTrOpenerReq')
        self.tsp.rvc_tailgate_control(1,20) 
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", 'TrOpenerSts', 5)
        self.bus_comm.check_signal_thread_stop('TrOpenerReqTrOpenerReq')
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVCtaildoor_Cocked_abandoned")
    @pytest.mark.join_smoke
    def test_cocked_tailgate_caseid_1980504(self):
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr02", 'TrOpenerReqTrOpenerReq')
        self.tsp.rvc_tailgate_control(1,20) 
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", 'TrOpenerSts', 5)
        self.bus_comm.check_signal_thread_stop('TrOpenerReqTrOpenerReq')
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"   
                        
    @allure.title("远程控制-RVCtaildoor_Closed_abandoned")
    @pytest.mark.join_smoke
    def test_close_tailgate_caseid_1980507(self):
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        # self.sd_tester.change_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr02", 'TrOpenerReqTrOpenerReq')
        self.mix.network_sleep()
        self.tsp.rvc_tailgate_control() 
        self.bus_comm.set_singal("bodycan","PotBodyFr02","TrOpenerSts","TrOpenerSts1_FullClsd")
        self.bus_comm.check_signal_thread_stop("TrOpenerReqTrOpenerReq")
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"   
                          
 # pytest -vs -p no:warnings remote_control/remote_two_domain_join/test_two_domain_tailgate.py      