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


@allure.feature("远程控制/远控两域联调测试/远控车窗")
@allure.story("远控车窗")
class TestRvcTailgate(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["WindowService_client","VehicleSetStatusService_client"])

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

    @allure.title("RVCWindows_Opened_success")
    @pytest.mark.smoke
    def test_window_caseid_1984894(self):
        self.mix.set_common_precontion()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        sleep(1)
        self.tsp.rvc_window_control(win_fl=100, win_fr=100, win_rl=100, win_rr=100)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.percent_100)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.event_check_windows_postion(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("RVCWindows_Closed_success")
    @pytest.mark.smoke
    def test_window_caseid_1984895(self):
        self.mix.set_common_precontion()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        sleep(1)
        self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.event_check_windows_postion(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"   
    
    @allure.title("RVCWindows_ClosedSuccess_inactive")
    @pytest.mark.smoke
    def test_window_caseid_1984896(self):
        self.mix.set_common_precontion()
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        sleep(1)
        self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.event_check_windows_postion(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("RVCWindows_ClosedSuccess_convenience")
    @pytest.mark.smoke
    def test_window_caseid_1984897(self):
        self.mix.set_common_precontion()
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        sleep(1)
        self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.event_check_windows_postion(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败" 