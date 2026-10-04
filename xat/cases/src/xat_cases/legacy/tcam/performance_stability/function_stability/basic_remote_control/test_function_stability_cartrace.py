#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import allure
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("远程控制/远控两域联调测试/远控寻车")
@allure.story("远控寻车")
class TestRvcCartrace(TestABCBase):
    def before_class(self, ecu):
        pass

    def before_each_func(self, ecu):
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr18", "TrsmParkLockdTrsmParkLockd", 'TrsmParkLock1_ParkEngd')
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr03", "GearLvrIndcn_1_EcmPropSignalIPdu24",'GearLvrIndcn2_ParkIndcn')  
       
         
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


    @allure.title("远程控制-RVC_远程寻车控制_闪灯鸣笛_ABANDONED压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1982651(self):
        self.mix.network_sleep()
        self.bus_comm.check_signal_thread_start("connectivitycanfd","VgmConnFr05", 'CarLoctrActvnSts')
        self.bus_comm.check_signal_thread_start("bodyexposedcanfd","CemBodyExpoFr51","ActvnOfIndcrIndcrOut")
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr18", "ActvOfHorn")  
        execid = self.tsp.rvc_find_vehicle()
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.bus_comm.check_signal_thread_stop('CarLoctrActvnSts')
        self.bus_comm.check_signal_thread_stop('ActvnOfIndcrIndcrOut')
        self.bus_comm.check_signal_thread_stop('ActvOfHorn')
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程寻车控制_闪灯鸣笛_INACTIVE压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1982650(self):
        self.bus_comm.check_signal_thread_start("connectivitycanfd","VgmConnFr05", 'CarLoctrActvnSts')
        self.bus_comm.check_signal_thread_start("bodyexposedcanfd","CemBodyExpoFr51","ActvnOfIndcrIndcrOut")
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr18", "ActvOfHorn")  
        execid = self.tsp.rvc_find_vehicle()
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.bus_comm.check_signal_thread_stop('CarLoctrActvnSts')
        self.bus_comm.check_signal_thread_stop('ActvnOfIndcrIndcrOut')
        self.bus_comm.check_signal_thread_stop('ActvOfHorn')
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程寻车控制_闪灯鸣笛_Convenience压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1982649(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.check_signal_thread_start("connectivitycanfd","VgmConnFr05", 'CarLoctrActvnSts')
        self.bus_comm.check_signal_thread_start("bodyexposedcanfd","CemBodyExpoFr51","ActvnOfIndcrIndcrOut")
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr18", "ActvOfHorn")  
        execid = self.tsp.rvc_find_vehicle()
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.bus_comm.check_signal_thread_stop('CarLoctrActvnSts')
        self.bus_comm.check_signal_thread_stop('ActvnOfIndcrIndcrOut')
        self.bus_comm.check_signal_thread_stop('ActvOfHorn')
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_ABANDONED压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1982648(self):
        self.mix.network_sleep()
        self.bus_comm.check_signal_thread_start("connectivitycanfd","VgmConnFr05", 'CarLoctrActvnSts')
        self.bus_comm.check_signal_thread_start("bodyexposedcanfd","CemBodyExpoFr51","ActvnOfIndcrIndcrOut")
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr18", "ActvOfHorn")  
        execid = self.tsp.rvc_find_vehicle(1)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.bus_comm.check_signal_thread_stop('CarLoctrActvnSts')
        self.bus_comm.check_signal_thread_stop('ActvnOfIndcrIndcrOut')
        self.bus_comm.check_signal_thread_stop('ActvOfHorn')
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_INACTIVE压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1982647(self):
        self.bus_comm.check_signal_thread_start("connectivitycanfd","VgmConnFr05", 'CarLoctrActvnSts')
        self.bus_comm.check_signal_thread_start("bodyexposedcanfd","CemBodyExpoFr51","ActvnOfIndcrIndcrOut")
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr18", "ActvOfHorn")  
        execid = self.tsp.rvc_find_vehicle(1)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.bus_comm.check_signal_thread_stop('CarLoctrActvnSts')
        self.bus_comm.check_signal_thread_stop('ActvnOfIndcrIndcrOut')
        self.bus_comm.check_signal_thread_stop('ActvOfHorn')
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_Convenience压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1982646(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.check_signal_thread_start("connectivitycanfd","VgmConnFr05", 'CarLoctrActvnSts')
        self.bus_comm.check_signal_thread_start("bodyexposedcanfd","CemBodyExpoFr51","ActvnOfIndcrIndcrOut")
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr18", "ActvOfHorn")  
        execid = self.tsp.rvc_find_vehicle(1)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.bus_comm.check_signal_thread_stop('CarLoctrActvnSts')
        self.bus_comm.check_signal_thread_stop('ActvnOfIndcrIndcrOut')
        self.bus_comm.check_signal_thread_stop('ActvOfHorn')
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"   