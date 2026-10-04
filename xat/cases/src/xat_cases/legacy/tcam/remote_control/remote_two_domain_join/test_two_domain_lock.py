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


@allure.feature("远程控制/远控两域联调测试/远控解闭锁")
@allure.story("远控解闭锁")
class TestRvcLock(TestABCBase):
    def before_class(self, ecu):
        pass

    def before_each_func(self, ecu):
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr18", "TrsmParkLockdTrsmParkLockd", 'TrsmParkLock1_ParkEngd')
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr03", "GearLvrIndcn_1_EcmPropSignalIPdu24",'GearLvrIndcn2_ParkIndcn')  
        self.bus_comm.set_singal("bodycan","DpodBodyFr01", "DoorOpenerDrvrSts_0_DpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","LpodBodyFr01", "DoorOpenerLeReSts_0_LpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","PpodBodyFr01", "DoorOpenerPassSts_0_PpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","RpodBodyFr01", "DoorOpenerRiReSts_0_RpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","PotBodyFr02", "TrOpenerSts_0_PotBodySignalIPdu02","TrOpenerSts1_FullClsd") 
         
    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        pass

    @allure.title("远程控制-RVClock_Lock_Inactive")
    @pytest.mark.join_smoke
    def test_lock_Inactive_caseid_1980492(self, ecu):
        self.io.set_five_door_sts(Door.close)
        # self.mix.set_open_close_door_precondition(DoorPos.All,DoorStatus.kClosed)
        self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search(),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVClock_Lock_abandon")
    @pytest.mark.join_smoke
    def test_lock_Inactive_caseid_1980501(self, ecu):
        self.io.set_five_door_sts(Door.close)
        # self.mix.set_open_close_door_precondition(DoorPos.All,DoorStatus.kClosed)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search(),f"TCAM远程控制上报到车云的结果校验失败"
            
    @allure.title("远程控制-RVClock_UnLock_abandoned")
    @pytest.mark.join_smoke
    def test_unlock_Inactive_caseid_1980491(self, ecu):
        self.io.set_five_door_sts(Door.open)
        # self.mix.set_open_close_door_precondition(DoorPos.All,DoorStatus.kOpened)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        # self.sd_tester.change_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.mix.network_sleep()
        self.tsp.rvc_lock_control(1)

        assert self.tsp.log_search(),f"TCAM远程控制上报到车云的结果校验失败"      
                        
        
    @allure.title("远程控制-RVClock_UnLock_Inactive")
    @pytest.mark.join_smoke
    def test_unlock_Inactive_caseid_1980493(self, ecu):
        # self.mix.set_open_close_door_precondition(DoorPos.All,DoorStatus.kOpened)
        self.io.set_five_door_sts(Door.open)
        self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search(),f"TCAM远程控制上报到车云的结果校验失败"   

 # pytest -vs -p no:warnings remote_control/remote_two_domain_join/test_two_domain_lock.py      