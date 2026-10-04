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
        self.soa.update(["TailGateService_client","VehicleSetStatusService_client"])

    def before_each_func(self, ecu):
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr18", "TrsmParkLockdTrsmParkLockd", 'TrsmParkLock1_ParkEngd')
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr03", "GearLvrIndcn_1_EcmPropSignalIPdu24",'GearLvrIndcn2_ParkIndcn')  
         
    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        pass

    @allure.title("远程控制-打开尾门_INACTIVE")
    @pytest.mark.smoke
    def test_tailgate_caseid_1984892(self):
        self.mix.set_common_precontion()
        sleep(1)
        self.bus_comm.set_tailgate_opener_sts(DoorOpenerSts.FullClsd)
        #self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr02", 'TrOpenerReqTrOpenerReq')
        self.tsp.rvc_tailgate_control(1) 
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open)
        self.bus_comm.set_tailgate_opener_sts(DoorOpenerSts.FullOpend)
        self.soa.hmi_event_check_tailgate_movests(status=MoveSts.Opened)
        #self.bus_comm.check_signal_thread_stop('TrOpenerReqTrOpenerReq')
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-关闭尾门")
    @pytest.mark.smoke
    def test_tailgate_caseid_1984889(self):
        self.mix.set_common_precontion()
        sleep(1)
        self.bus_comm.set_tailgate_opener_sts(DoorOpenerSts.FullOpend)
        #self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr02", 'TrOpenerReqTrOpenerReq')
        self.tsp.rvc_tailgate_control(-1) 
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Close)
        self.bus_comm.set_tailgate_opener_sts(DoorOpenerSts.FullClsd)
        self.soa.hmi_event_check_tailgate_movests(status=MoveSts.Closed)
        #self.bus_comm.check_signal_thread_stop('TrOpenerReqTrOpenerReq')
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"   


    @allure.title("远程控制-尾门翘起")
    @pytest.mark.smoke
    def test_tailgate_caseid_1987614(self):
        self.mix.set_common_precontion()
        sleep(1)
        self.bus_comm.set_tailgate_opener_sts(DoorOpenerSts.FullClsd)
        #self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr02", 'TrOpenerReqTrOpenerReq')
        self.tsp.rvc_tailgate_control(1,20) 
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 20)
        self.bus_comm.set_tailgate_opener_sts(DoorOpenerSts.MovgOut)
        self.soa.hmi_event_check_tailgate_movests(status=MoveSts.Opening)
        # self.bus_comm.check_signal_thread_stop('TrOpenerReqTrOpenerReq')
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVCtaildoor_Opened_Success")
    @pytest.mark.smoke
    def test_tailgate_caseid_1984890(self):
        self.mix.set_common_precontion()
        sleep(1)
        self.bus_comm.set_tailgate_opener_sts(DoorOpenerSts.FullClsd)
        sleep(2)
        self.tsp.rvc_tailgate_control(1) 
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open)
        self.bus_comm.set_tailgate_opener_sts(DoorOpenerSts.FullOpend)
        self.soa.hmi_event_check_tailgate_movests(status=MoveSts.Opened)
        #self.bus_comm.check_signal_thread_stop('TrOpenerReqTrOpenerReq')
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVCtaildoor_Closed_Success")
    @pytest.mark.smoke
    def test_tailgate_caseid_1984893(self):
        self.mix.set_common_precontion()
        sleep(1)
        self.bus_comm.set_tailgate_opener_sts(DoorOpenerSts.FullOpend)
        sleep(2)
        self.tsp.rvc_tailgate_control(-1) 
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Close)
        self.bus_comm.set_tailgate_opener_sts(DoorOpenerSts.FullClsd)
        self.soa.hmi_event_check_tailgate_movests(status=MoveSts.Closed)
        #self.bus_comm.check_signal_thread_stop('TrOpenerReqTrOpenerReq')
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVCtaildoor_Cocked_convenience")
    @pytest.mark.smoke
    def test_tailgate_caseid_1984891(self):
        self.mix.set_common_precontion()
        sleep(1)
        self.bus_comm.set_tailgate_opener_sts(DoorOpenerSts.FullClsd)
        sleep(2)
        self.tsp.rvc_tailgate_control(1,10) 
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 10)
        self.bus_comm.set_tailgate_opener_sts(DoorOpenerSts.MovgOut)
        self.soa.hmi_event_check_tailgate_movests(status=MoveSts.Opening)
        # self.bus_comm.check_signal_thread_stop('TrOpenerReqTrOpenerReq')
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"