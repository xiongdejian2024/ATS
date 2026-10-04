#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import allure
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
import random

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


    def after_class(self, ecu):
        pass


    @allure.title("远程控制-RVC_远控尾门控制_翘起_ CONVENIENCE压测1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1982478(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_singal("bodycan","PotBodyFr02","TrOpenerSts","TrOpenerSts1_FullClsd")
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        sleep(2)
        execid = self.tsp.rvc_tailgate_control(1,50) 
        TrOpenerSts_list = [4,5,8,10]
        # 在列表中随机取值
        TrOpenerSts = random.choice(TrOpenerSts_list)
        self.bus_comm.set_singal("bodycan","PotBodyFr02","TrOpenerSts",TrOpenerSts)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远控尾门控制_翘起_ INACTIVE压测1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1982479(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_singal("bodycan","PotBodyFr02","TrOpenerSts","TrOpenerSts1_FullClsd")
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        sleep(2)
        execid = self.tsp.rvc_tailgate_control(1,50) 
        TrOpenerSts_list = [4,5,8,10]
        # 在列表中随机取值
        TrOpenerSts = random.choice(TrOpenerSts_list)
        self.bus_comm.set_singal("bodycan","PotBodyFr02","TrOpenerSts",TrOpenerSts)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_翘起_ ABANDONED压测1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1982480(self):
        self.mix.network_sleep()
        self.bus_comm.set_singal("bodycan","PotBodyFr02","TrOpenerSts","TrOpenerSts1_FullClsd")
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        sleep(2)
        execid = self.tsp.rvc_tailgate_control(1,50) 
        TrOpenerSts_list = [4,5,8,10]
        # 在列表中随机取值
        TrOpenerSts = random.choice(TrOpenerSts_list)
        self.bus_comm.set_singal("bodycan","PotBodyFr02","TrOpenerSts",TrOpenerSts)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_关_ CONVENIENCE压测1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1982532(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_singal("bodycan","PotBodyFr02","TrOpenerSts",3)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        sleep(2)
        execid = self.tsp.rvc_tailgate_control() 
        TrOpenerSts_list = [1]
        # 在列表中随机取值
        TrOpenerSts = random.choice(TrOpenerSts_list)
        self.bus_comm.set_singal("bodycan","PotBodyFr02","TrOpenerSts",TrOpenerSts)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远控尾门控制_关_ INACTIVE压测1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1982533(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_singal("bodycan","PotBodyFr02","TrOpenerSts",3)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        sleep(2)
        execid = self.tsp.rvc_tailgate_control() 
        TrOpenerSts_list = [1]
        # 在列表中随机取值
        TrOpenerSts = random.choice(TrOpenerSts_list)
        self.bus_comm.set_singal("bodycan","PotBodyFr02","TrOpenerSts",TrOpenerSts)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_关_ ABANDONED压测1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1982534(self):
        self.mix.network_sleep()
        self.bus_comm.set_singal("bodycan","PotBodyFr02","TrOpenerSts",3)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        sleep(2)
        execid = self.tsp.rvc_tailgate_control() 
        TrOpenerSts_list = [1]
        # 在列表中随机取值
        TrOpenerSts = random.choice(TrOpenerSts_list)
        self.bus_comm.set_singal("bodycan","PotBodyFr02","TrOpenerSts",TrOpenerSts)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_开_ CONVENIENCE压测1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1982582(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_singal("bodycan","PotBodyFr02","TrOpenerSts",3)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        sleep(2)
        execid = self.tsp.rvc_tailgate_control() 
        TrOpenerSts_list = [100]
        # 在列表中随机取值
        TrOpenerSts = random.choice(TrOpenerSts_list)
        self.bus_comm.set_singal("bodycan","PotBodyFr02","TrOpenerSts",TrOpenerSts)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远控尾门控制_开_ INACTIVE压测1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1982583(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_singal("bodycan","PotBodyFr02","TrOpenerSts",3)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        sleep(2)
        execid = self.tsp.rvc_tailgate_control() 
        TrOpenerSts_list = [100]
        # 在列表中随机取值
        TrOpenerSts = random.choice(TrOpenerSts_list)
        self.bus_comm.set_singal("bodycan","PotBodyFr02","TrOpenerSts",TrOpenerSts)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_开_ ABANDONED压测1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1982584(self):
        self.mix.network_sleep()
        self.bus_comm.set_singal("bodycan","PotBodyFr02","TrOpenerSts",3)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        sleep(2)
        execid = self.tsp.rvc_tailgate_control() 
        TrOpenerSts_list = [100]
        # 在列表中随机取值
        TrOpenerSts = random.choice(TrOpenerSts_list)
        self.bus_comm.set_singal("bodycan","PotBodyFr02","TrOpenerSts",TrOpenerSts)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"