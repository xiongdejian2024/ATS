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
        self.bus_comm.set_singal("bodycan","DpodBodyFr01", "DoorOpenerDrvrSts_0_DpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","LpodBodyFr01", "DoorOpenerLeReSts_0_LpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","PpodBodyFr01", "DoorOpenerPassSts_0_PpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","RpodBodyFr01", "DoorOpenerRiReSts_0_RpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","PotBodyFr02", "TrOpenerSts_0_PotBodySignalIPdu02","TrOpenerSts1_FullClsd") 
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


    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_ Convenience压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_lock_caseid_1982164(self):
        self.bus_comm.set_singal("bodycan","DpodBodyFr01", "DoorOpenerDrvrSts_0_DpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","LpodBodyFr01", "DoorOpenerLeReSts_0_LpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","PpodBodyFr01", "DoorOpenerPassSts_0_PpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","RpodBodyFr01", "DoorOpenerRiReSts_0_RpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","PotBodyFr02", "TrOpenerSts_0_PotBodySignalIPdu02","TrOpenerSts1_FullClsd")
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(2)
        execid=self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_ INACTIVE压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_lock_caseid_1982165(self):
        self.bus_comm.set_singal("bodycan","DpodBodyFr01", "DoorOpenerDrvrSts_0_DpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","LpodBodyFr01", "DoorOpenerLeReSts_0_LpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","PpodBodyFr01", "DoorOpenerPassSts_0_PpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","RpodBodyFr01", "DoorOpenerRiReSts_0_RpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","PotBodyFr02", "TrOpenerSts_0_PotBodySignalIPdu02","TrOpenerSts1_FullClsd") 
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(2)
        execid=self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_ ABANDONED压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_lock_caseid_1982166(self):
        self.bus_comm.set_singal("bodycan","DpodBodyFr01", "DoorOpenerDrvrSts_0_DpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","LpodBodyFr01", "DoorOpenerLeReSts_0_LpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","PpodBodyFr01", "DoorOpenerPassSts_0_PpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","RpodBodyFr01", "DoorOpenerRiReSts_0_RpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","PotBodyFr02", "TrOpenerSts_0_PotBodySignalIPdu02","TrOpenerSts1_FullClsd") 
        self.mix.network_sleep()
        sleep(2)
        execid=self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_ Convenience压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_lock_caseid_1982170(self, ecu):
        self.bus_comm.set_singal("bodycan","DpodBodyFr01", "DoorOpenerDrvrSts_0_DpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","LpodBodyFr01", "DoorOpenerLeReSts_0_LpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","PpodBodyFr01", "DoorOpenerPassSts_0_PpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","RpodBodyFr01", "DoorOpenerRiReSts_0_RpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","PotBodyFr02", "TrOpenerSts_0_PotBodySignalIPdu02","TrOpenerSts1_FullClsd") 
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(2)
        execid=self.tsp.rvc_lock_control(2)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_ INACTIVE压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_lock_caseid_1982171(self, ecu):
        self.bus_comm.set_singal("bodycan","DpodBodyFr01", "DoorOpenerDrvrSts_0_DpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","LpodBodyFr01", "DoorOpenerLeReSts_0_LpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","PpodBodyFr01", "DoorOpenerPassSts_0_PpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","RpodBodyFr01", "DoorOpenerRiReSts_0_RpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","PotBodyFr02", "TrOpenerSts_0_PotBodySignalIPdu02","TrOpenerSts1_FullClsd") 
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(2)
        execid=self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_ ABANDONED压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_lock_caseid_1982172(self):
        self.bus_comm.set_singal("bodycan","DpodBodyFr01", "DoorOpenerDrvrSts_0_DpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","LpodBodyFr01", "DoorOpenerLeReSts_0_LpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","PpodBodyFr01", "DoorOpenerPassSts_0_PpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","RpodBodyFr01", "DoorOpenerRiReSts_0_RpodBodySignalIPdu01","DoorOpenerSts_FullClsd")
        self.bus_comm.set_singal("bodycan","PotBodyFr02", "TrOpenerSts_0_PotBodySignalIPdu02","TrOpenerSts1_FullClsd") 
        self.mix.network_sleep()
        sleep(2)
        execid=self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_ Convenience压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_lock_caseid_1982167(self, ecu):
        self.bus_comm.set_singal("bodycan","DpodBodyFr01", "DoorOpenerDrvrSts_0_DpodBodySignalIPdu01","DoorOpenerSts_FullOpend")
        self.bus_comm.set_singal("bodycan","LpodBodyFr01", "DoorOpenerLeReSts_0_LpodBodySignalIPdu01","DoorOpenerSts_FullOpend")
        self.bus_comm.set_singal("bodycan","PpodBodyFr01", "DoorOpenerPassSts_0_PpodBodySignalIPdu01","DoorOpenerSts_FullOpend")
        self.bus_comm.set_singal("bodycan","RpodBodyFr01", "DoorOpenerRiReSts_0_RpodBodySignalIPdu01","DoorOpenerSts_FullOpend")
        self.bus_comm.set_singal("bodycan","PotBodyFr02", "TrOpenerSts_0_PotBodySignalIPdu02","TrOpenerSts1_FullOpend") 
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(2)
        execid=self.tsp.rvc_lock_control(3)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_ INACTIVE压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_lock_caseid_1982168(self, ecu):
        self.bus_comm.set_singal("bodycan","DpodBodyFr01", "DoorOpenerDrvrSts_0_DpodBodySignalIPdu01","DoorOpenerSts_FullOpend")
        self.bus_comm.set_singal("bodycan","LpodBodyFr01", "DoorOpenerLeReSts_0_LpodBodySignalIPdu01","DoorOpenerSts_FullOpend")
        self.bus_comm.set_singal("bodycan","PpodBodyFr01", "DoorOpenerPassSts_0_PpodBodySignalIPdu01","DoorOpenerSts_FullOpend")
        self.bus_comm.set_singal("bodycan","RpodBodyFr01", "DoorOpenerRiReSts_0_RpodBodySignalIPdu01","DoorOpenerSts_FullOpend")
        self.bus_comm.set_singal("bodycan","PotBodyFr02", "TrOpenerSts_0_PotBodySignalIPdu02","TrOpenerSts1_FullOpend") 
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(2)
        execid=self.tsp.rvc_lock_control(3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_ ABANDONED压测试1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_lock_caseid_1982169(self):
        self.mix.network_sleep()
        self.bus_comm.set_singal("bodycan","DpodBodyFr01", "DoorOpenerDrvrSts_0_DpodBodySignalIPdu01","DoorOpenerSts_FullOpend")
        self.bus_comm.set_singal("bodycan","LpodBodyFr01", "DoorOpenerLeReSts_0_LpodBodySignalIPdu01","DoorOpenerSts_FullOpend")
        self.bus_comm.set_singal("bodycan","PpodBodyFr01", "DoorOpenerPassSts_0_PpodBodySignalIPdu01","DoorOpenerSts_FullOpend")
        self.bus_comm.set_singal("bodycan","RpodBodyFr01", "DoorOpenerRiReSts_0_RpodBodySignalIPdu01","DoorOpenerSts_FullOpend")
        self.bus_comm.set_singal("bodycan","PotBodyFr02", "TrOpenerSts_0_PotBodySignalIPdu02","TrOpenerSts1_FullOpend") 
        sleep(2)
        execid=self.tsp.rvc_lock_control(3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"