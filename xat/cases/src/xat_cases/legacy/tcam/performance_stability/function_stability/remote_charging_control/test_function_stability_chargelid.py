#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import allure
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("TCAM性能稳定性/业务稳定性/基础远控/远控充电口盖")
@allure.story("远控充电口盖")
class TestRvcChargeLid(TestABCBase):
    def before_class(self, ecu):
        pass

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.set_car_mode(car_mode=CarMode.NORMAL)
        sleep(2)
       
         
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.io.bgm_diag_line_up()
        logger.info(f'连接诊断激活线')
        self.io.tcam_kl15_up()
        sleep(10)
        self.sd_tester.sd_tester.tester_present()
        self.bus_comm.resume_all_bus_send()
        # self.bus_comm.check_four_door_and_tailgate_hood_sts(Door.close, DoorPos.All)


    def after_class(self, ecu):
        pass

    @allure.title("远程控制-RVC_远控控制充电口盖_关_ Driving和GearP压测1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1980534(self):
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr09", "ChrgLidRearSts")
        execid = self.tsp.rvc_charge_Lidgate(-1)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcActPosn2", 0) 
        self.bus_comm.check_signal_thread_stop('ChrgLidRearSts')
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远控控制充电口盖_关_ Active压测1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1980535(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr09", "ChrgLidRearSts")
        execid = self.tsp.rvc_charge_Lidgate(-1)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcActPosn2", 0) 
        self.bus_comm.check_signal_thread_stop('ChrgLidRearSts')
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_关_ Convenience压测1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1980536(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr09", "ChrgLidRearSts")
        execid = self.tsp.rvc_charge_Lidgate(-1)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcActPosn2", 0) 
        self.bus_comm.check_signal_thread_stop('ChrgLidRearSts')
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_关_ INACTIVE压测1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1980537(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr09", "ChrgLidRearSts")
        execid = self.tsp.rvc_charge_Lidgate(-1)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcActPosn2", 0) 
        self.bus_comm.check_signal_thread_stop('ChrgLidRearSts')
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远控控制充电口盖_关_ ABANDONED压测1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1980538(self):
        self.mix.network_sleep()
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr09", "ChrgLidRearSts")
        execid = self.tsp.rvc_charge_Lidgate(-1)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcActPosn2", 0) 
        self.bus_comm.check_signal_thread_stop('ChrgLidRearSts')
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_开_ Driving和GearP压测1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1980585(self):
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr09", "ChrgLidRearSts")
        execid = self.tsp.rvc_charge_Lidgate()
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcActPosn2", 100) 
        self.bus_comm.check_signal_thread_stop('ChrgLidRearSts')
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远控控制充电口盖_开_ Active压测1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1980586(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr09", "ChrgLidRearSts")
        execid = self.tsp.rvc_charge_Lidgate()
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcActPosn2", 100) 
        self.bus_comm.check_signal_thread_stop('ChrgLidRearSts')
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_开_ Convenience压测1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1980587(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr09", "ChrgLidRearSts")
        execid = self.tsp.rvc_charge_Lidgate()
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcActPosn2", 100) 
        self.bus_comm.check_signal_thread_stop('ChrgLidRearSts')
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_开_ INACTIVE压测1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1980588(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr09", "ChrgLidRearSts")
        execid = self.tsp.rvc_charge_Lidgate()
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcActPosn2", 100) 
        self.bus_comm.check_signal_thread_stop('ChrgLidRearSts')
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远控控制充电口盖_开_ ABANDONED压测1000次")
    @pytest.mark.longtime
    @pytest.mark.repeat(100)
    def test_caseid_1980589(self):
        self.mix.network_sleep()
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr09", "ChrgLidRearSts")
        execid = self.tsp.rvc_charge_Lidgate()
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcActPosn2", 100) 
        self.bus_comm.check_signal_thread_stop('ChrgLidRearSts')
        assert self.tsp.log_search_remote_vehicle_control(execid=execid), f"TCAM远程控制上报到车云的结果校验失败"
                                  
 # pytest -vs -p no:warnings remote_control/remote_two_domain_join/test_two_domain_chargelid.py      