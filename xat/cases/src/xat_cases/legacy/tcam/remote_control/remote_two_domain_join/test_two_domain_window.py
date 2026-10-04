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
class TestRvcWindow(TestABCBase):
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
    def test_open_window_caseid_1980511(self):
        self.tsp.rvc_window_control()
        with allure.step('多线程监听车窗信号'):          
            self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr68","WinOpenDrvrReq")
            self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr68","WinOpenPassReq")
            self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr68","WinOpenReLeReq")
            self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr68","WinOpenReRiReq")
            
        with allure.step('关闭多线程车窗信号'):    
            self.bus_comm.check_signal_thread_stop('WinOpenDrvrReq')
            self.bus_comm.check_signal_thread_stop('WinOpenPassReq')
            self.bus_comm.check_signal_thread_stop('WinOpenReLeReq')
            self.bus_comm.check_signal_thread_stop('WinOpenReRiReq')
        
        self.bus_comm.set_singal("bodycan","DdmBodyFr04", "WinPosnStsAtDrvr", 26) 
        self.bus_comm.set_singal("bodycan","PdmBodyFr01", "WinPosnStsAtPass", 26)
        self.bus_comm.set_singal("bodycan","RrdmBodyFr01", "WinPosnStsAtReRi", 26)
        self.bus_comm.set_singal("bodycan","RldmBodyFr01", "WinPosnStsAtReLe", 26)
        
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVCWindows_open_abandon")
    @pytest.mark.join_smoke
    def test_open_window_caseid_1980510(self):
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.tsp.rvc_window_control()
        with allure.step('多线程监听车窗信号'):          
            self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr68","WinOpenDrvrReq")
            self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr68","WinOpenPassReq")
            self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr68","WinOpenReLeReq")
            self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr68","WinOpenReRiReq")
            
        with allure.step('关闭多线程车窗信号'):    
            self.bus_comm.check_signal_thread_stop('WinOpenDrvrReq')
            self.bus_comm.check_signal_thread_stop('WinOpenPassReq')
            self.bus_comm.check_signal_thread_stop('WinOpenReLeReq')
            self.bus_comm.check_signal_thread_stop('WinOpenReRiReq')
        
        self.bus_comm.set_singal("bodycan","DdmBodyFr04", "WinPosnStsAtDrvr", 26) 
        self.bus_comm.set_singal("bodycan","PdmBodyFr01", "WinPosnStsAtPass", 26)
        self.bus_comm.set_singal("bodycan","RrdmBodyFr01", "WinPosnStsAtReRi", 26)
        self.bus_comm.set_singal("bodycan","RldmBodyFr01", "WinPosnStsAtReLe", 26)
        
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVCWindows_Closed_INACTIVE")
    @pytest.mark.join_smoke
    def test_close_window_caseid_1980509(self):
        self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)  
        with allure.step('多线程监听车窗信号'):          
            self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr68","WinOpenDrvrReq")
            self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr68","WinOpenPassReq")
            self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr68","WinOpenReLeReq")
            self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr68","WinOpenReRiReq")
            
        with allure.step('关闭多线程车窗信号'):    
            self.bus_comm.check_signal_thread_stop('WinOpenDrvrReq')
            self.bus_comm.check_signal_thread_stop('WinOpenPassReq')
            self.bus_comm.check_signal_thread_stop('WinOpenReLeReq')
            self.bus_comm.check_signal_thread_stop('WinOpenReRiReq')
        
        self.bus_comm.set_singal("bodycan","DdmBodyFr04", "WinPosnStsAtDrvr", "WinAndRoofAndCurtPosnTyp_ClsFull") 
        self.bus_comm.set_singal("bodycan","PdmBodyFr01", "WinPosnStsAtPass", "WinAndRoofAndCurtPosnTyp_ClsFull")
        self.bus_comm.set_singal("bodycan","RrdmBodyFr01", "WinPosnStsAtReRi", "WinAndRoofAndCurtPosnTyp_ClsFull")
        self.bus_comm.set_singal("bodycan","RldmBodyFr01", "WinPosnStsAtReLe", "WinAndRoofAndCurtPosnTyp_ClsFull")
        
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVCWindows_Closed_abandon")
    @pytest.mark.join_smoke
    def test_close_window_caseid_1980508(self):
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)  
        with allure.step('多线程监听车窗信号'):          
            self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr68","WinOpenDrvrReq")
            self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr68","WinOpenPassReq")
            self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr68","WinOpenReLeReq")
            self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr68","WinOpenReRiReq")
            
        with allure.step('关闭多线程车窗信号'):    
            self.bus_comm.check_signal_thread_stop('WinOpenDrvrReq')
            self.bus_comm.check_signal_thread_stop('WinOpenPassReq')
            self.bus_comm.check_signal_thread_stop('WinOpenReLeReq')
            self.bus_comm.check_signal_thread_stop('WinOpenReRiReq')
        
        self.bus_comm.set_singal("bodycan","DdmBodyFr04", "WinPosnStsAtDrvr", "WinAndRoofAndCurtPosnTyp_ClsFull") 
        self.bus_comm.set_singal("bodycan","PdmBodyFr01", "WinPosnStsAtPass", "WinAndRoofAndCurtPosnTyp_ClsFull")
        self.bus_comm.set_singal("bodycan","RrdmBodyFr01", "WinPosnStsAtReRi", "WinAndRoofAndCurtPosnTyp_ClsFull")
        self.bus_comm.set_singal("bodycan","RldmBodyFr01", "WinPosnStsAtReLe", "WinAndRoofAndCurtPosnTyp_ClsFull")
        
        assert self.tsp.log_search(), f"TCAM远程控制上报到车云的结果校验失败"       
                        
                  
 # pytest -vs -p no:warnings remote_control/remote_two_domain_join/test_two_domain_window.py      