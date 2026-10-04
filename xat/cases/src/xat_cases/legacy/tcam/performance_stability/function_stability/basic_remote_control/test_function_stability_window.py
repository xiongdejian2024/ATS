#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import allure
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("TCAM性能稳定性/业务稳定性/基础远控/四门解锁")
@allure.story("四门解锁")
class TestRvcChargeLid(TestABCBase):
    def before_class(self, ecu):
        pass

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.set_car_mode(car_mode=CarMode.NORMAL)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr18", "TrsmParkLockdTrsmParkLockd", 'TrsmParkLock1_ParkEngd')
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr03", "GearLvrIndcn_1_EcmPropSignalIPdu24",'GearLvrIndcn2_ParkIndcn')
        sleep(2)
       
         
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        if ecu.testresult == 'Failure':
            logger.info('用例执行失败')
            sleep(12)
        self.io.bgm_diag_line_up()
        logger.info(f'连接诊断激活线')
        self.io.tcam_kl15_up()
        sleep(10)
        self.bus_comm.resume_all_bus_send()

        # self.bus_comm.check_four_door_and_tailgate_hood_sts(Door.close, DoorPos.All)


    def after_class(self, ecu):
        pass


    @allure.title("远程控制-RVC_远程车窗控制_关_ Convenience压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_lock_caseid_1982350(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_singal("bodycan","DdmBodyFr04", "WinPosnStsAtDrvr", 26) 
        self.bus_comm.set_singal("bodycan","PdmBodyFr01", "WinPosnStsAtPass", 26)
        self.bus_comm.set_singal("bodycan","RrdmBodyFr01", "WinPosnStsAtReRi", 26)
        self.bus_comm.set_singal("bodycan","RldmBodyFr01", "WinPosnStsAtReLe", 26)
        sleep(2)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)  
        self.bus_comm.set_singal("bodycan","DdmBodyFr04", "WinPosnStsAtDrvr", 1) 
        self.bus_comm.set_singal("bodycan","PdmBodyFr01", "WinPosnStsAtPass", 1)
        self.bus_comm.set_singal("bodycan","RrdmBodyFr01", "WinPosnStsAtReRi", 1)
        self.bus_comm.set_singal("bodycan","RldmBodyFr01", "WinPosnStsAtReLe", 1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程车窗控制_关_ INACTIVE压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_lock_caseid_1982351(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_singal("bodycan","DdmBodyFr04", "WinPosnStsAtDrvr", 26) 
        self.bus_comm.set_singal("bodycan","PdmBodyFr01", "WinPosnStsAtPass", 26)
        self.bus_comm.set_singal("bodycan","RrdmBodyFr01", "WinPosnStsAtReRi", 26)
        self.bus_comm.set_singal("bodycan","RldmBodyFr01", "WinPosnStsAtReLe", 26)
        sleep(2)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)  
        self.bus_comm.set_singal("bodycan","DdmBodyFr04", "WinPosnStsAtDrvr", 1) 
        self.bus_comm.set_singal("bodycan","PdmBodyFr01", "WinPosnStsAtPass", 1)
        self.bus_comm.set_singal("bodycan","RrdmBodyFr01", "WinPosnStsAtReRi", 1)
        self.bus_comm.set_singal("bodycan","RldmBodyFr01", "WinPosnStsAtReLe", 1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_关_ ABANDONED压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_lock_caseid_1982352(self):
        self.mix.network_sleep()
        self.bus_comm.set_singal("bodycan","DdmBodyFr04", "WinPosnStsAtDrvr", 26) 
        self.bus_comm.set_singal("bodycan","PdmBodyFr01", "WinPosnStsAtPass", 26)
        self.bus_comm.set_singal("bodycan","RrdmBodyFr01", "WinPosnStsAtReRi", 26)
        self.bus_comm.set_singal("bodycan","RldmBodyFr01", "WinPosnStsAtReLe", 26)
        sleep(2)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)  
        self.bus_comm.set_singal("bodycan","DdmBodyFr04", "WinPosnStsAtDrvr", 1) 
        self.bus_comm.set_singal("bodycan","PdmBodyFr01", "WinPosnStsAtPass", 1)
        self.bus_comm.set_singal("bodycan","RrdmBodyFr01", "WinPosnStsAtReRi", 1)
        self.bus_comm.set_singal("bodycan","RldmBodyFr01", "WinPosnStsAtReLe", 1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    

    @allure.title("远程控制-RVC_远程车窗控制_开_ Convenience压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_lock_caseid_1982353(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_singal("bodycan","DdmBodyFr04", "WinPosnStsAtDrvr", 1) 
        self.bus_comm.set_singal("bodycan","PdmBodyFr01", "WinPosnStsAtPass", 1)
        self.bus_comm.set_singal("bodycan","RrdmBodyFr01", "WinPosnStsAtReRi", 1)
        self.bus_comm.set_singal("bodycan","RldmBodyFr01", "WinPosnStsAtReLe", 1)
        sleep(2)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        execid = self.tsp.rvc_window_control(win_fl=100, win_fr=100, win_rl=100, win_rr=100)  
        self.bus_comm.set_singal("bodycan","DdmBodyFr04", "WinPosnStsAtDrvr", 26) 
        self.bus_comm.set_singal("bodycan","PdmBodyFr01", "WinPosnStsAtPass", 26)
        self.bus_comm.set_singal("bodycan","RrdmBodyFr01", "WinPosnStsAtReRi", 26)
        self.bus_comm.set_singal("bodycan","RldmBodyFr01", "WinPosnStsAtReLe", 26)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程车窗控制_开_ INACTIVE压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_lock_caseid_1982354(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_singal("bodycan","DdmBodyFr04", "WinPosnStsAtDrvr", 1) 
        self.bus_comm.set_singal("bodycan","PdmBodyFr01", "WinPosnStsAtPass", 1)
        self.bus_comm.set_singal("bodycan","RrdmBodyFr01", "WinPosnStsAtReRi", 1)
        self.bus_comm.set_singal("bodycan","RldmBodyFr01", "WinPosnStsAtReLe", 1)
        sleep(2)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        execid = self.tsp.rvc_window_control(win_fl=100, win_fr=100, win_rl=100, win_rr=100)   
        self.bus_comm.set_singal("bodycan","DdmBodyFr04", "WinPosnStsAtDrvr", 26) 
        self.bus_comm.set_singal("bodycan","PdmBodyFr01", "WinPosnStsAtPass", 26)
        self.bus_comm.set_singal("bodycan","RrdmBodyFr01", "WinPosnStsAtReRi", 26)
        self.bus_comm.set_singal("bodycan","RldmBodyFr01", "WinPosnStsAtReLe", 26)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_开_ ABANDONED压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_lock_caseid_1982355(self):
        self.mix.network_sleep()
        self.bus_comm.set_singal("bodycan","DdmBodyFr04", "WinPosnStsAtDrvr", 1) 
        self.bus_comm.set_singal("bodycan","PdmBodyFr01", "WinPosnStsAtPass", 1)
        self.bus_comm.set_singal("bodycan","RrdmBodyFr01", "WinPosnStsAtReRi", 1)
        self.bus_comm.set_singal("bodycan","RldmBodyFr01", "WinPosnStsAtReLe", 1)
        sleep(2)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        execid = self.tsp.rvc_window_control(win_fl=100, win_fr=100, win_rl=100, win_rr=100)  
        self.bus_comm.set_singal("bodycan","DdmBodyFr04", "WinPosnStsAtDrvr", 26) 
        self.bus_comm.set_singal("bodycan","PdmBodyFr01", "WinPosnStsAtPass", 26)
        self.bus_comm.set_singal("bodycan","RrdmBodyFr01", "WinPosnStsAtReRi", 26)
        self.bus_comm.set_singal("bodycan","RldmBodyFr01", "WinPosnStsAtReLe", 26)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"