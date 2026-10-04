#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import time
import threading
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("TCAM性能稳定性/业务稳定性/远控设置SOC值")
@allure.story("远控设置SOC值-稳定性测试")
class TestMaxSOCRepeat(TestABCBase):
    def before_class(self, ecu):
        # self.soa.update(['VehicleSetStatusService_server'])
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])


    def before_each_func(self, ecu):
        self.mix.set_car_mode(CarMode.NORMAL)
        time.sleep(1)
        
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        # self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        
        # 2域环境也通过soa发送维修模式
        # self.soa.s2s_set_mntnmode(False)
        self.bus_comm.set_gear_pos(Gear.Park)
        # self.mix.back_fota_to(FOTAMasteSts.IDLE)
        self.bus_comm.set_charging_sts(ChargingSts.ACCharging)
        # 设置SOC值 为 100%
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb", 100)
        

    def after_each_func(self, ecu):
        # self.mix.network_wakeup()
        self.io.bgm_diag_line_up()
        logger.info(f'连接诊断激活线')
        self.io.tcam_kl15_up()
        sleep(10)
        self.sd_tester.sd_tester.tester_present()
        self.bus_comm.resume_all_bus_send()
        # self.bus_comm.check_four_door_and_tailgate_hood_sts(Door.close, DoorPos.All)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        time.sleep(10)

    def after_class(self, ecu):
        pass

    @allure.title("远程控制-RVC_远程设置SOC_inactive两域联调")
    @pytest.mark.join_smoke
    def test_max_soc_caseid_1982919(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_thread_start("backbonefr","IHUBackBoneFr12","LocalBookChrgnTarVal",500, timeout=20)
        with allure.step('模拟发送远程设置SOC值为80%'):
            execid = self.tsp.rvc_charge_soc_settings(max_soc=500)
        with allure.step('TCAN已发送设置SOC值的请求,BGM发送CAN报文:'):
            result = self.bus_comm.check_thread_stop('LocalBookChrgnTarVal',timeout=60)
            logger.info(f'CAN——LocalBookChrgnTarVal抓取结果: {result}')
            assert result[0]
        with allure.step('正常上报设置结果为成功'):
            self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb", 50.0)
            assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程设置SOC_abandoned两域联调")
    @pytest.mark.join_smoke
    def test_max_soc_caseid_1982920(self):
        self.mix.network_sleep()
        self.bus_comm.check_thread_start("backbonefr","IHUBackBoneFr12","LocalBookChrgnTarVal",500, timeout=10)
        with allure.step('模拟发送远程设置SOC值为80%'):
            execid = self.tsp.rvc_charge_soc_settings(max_soc=500)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        with allure.step('TCAN已发送设置SOC值的请求,BGM发送CAN报文:'):
            result = self.bus_comm.check_thread_stop('LocalBookChrgnTarVal')
            logger.info(f'CAN——LocalBookChrgnTarVal抓取结果: {result}')
            assert result[0]
        with allure.step('正常上报设置结果为成功'):
            self.bus_comm.resume_all_bus_send()
            self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb", 50.0)
            assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

