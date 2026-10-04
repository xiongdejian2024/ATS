#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_rvs.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/12/1 11:30
@Description: BGM RVS功能测试
"""

import os
import sys
import pytest
import allure
from time import sleep
import threading
import math

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.tsp.rvs_client import RvsClient
from signal_value_mapping import *

@allure.feature("BGM车云")
@allure.story("基础数据上报")
@pytest.mark.order_last
class TestRVS(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["ClimateControlService_client","CentralLockService_client","TailWingService_client","SteerWheelService_client","TyreService_client","ChargeLidService_client","OuterRearViewService_client","ShieldWindowService_client","VehicleModeService_client","VehicleSetStatusService_client","HighVoltageService_client"])
        sleep(3)
        self.vid = self.tb_config["vid"]
        self.rvs_client = RvsClient(vid=self.vid)
        logger.info("VID: {0}".format(self.vid))
        sleep(2)

    def before_each_func(self, ecu):
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        self.sd_tester.write_ccp({225: 7, 226: 7}) 
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass


    @pytest.mark.sanity
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1350901?projectId=46',
        name='RVS Case 1918463',
    )
    def test_display_soc_info_caseid_1918463(self):
        self.bus_comm.set_singal("propulsioncan","BecmPropFr01", 'HvSysRlyStsHvSysRlySts', 1)
        self.bus_comm.set_SOC_display_value(100.0)
        sleep(1)
        for soc_value in [90, 0, 100, 77] :
            logger.info("---------------->{soc_value}")
            self.bus_comm.set_SOC_display_value(float(soc_value))
            self.tsp.check_rvs_data_update_new(
                block=BlockName.GISAndTravel, keys=["socInfo", "displaySoc"], target_value=float(soc_value),timeout=8
            )

    @pytest.mark.full
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1350902?projectId=46',
        name='RVS Case 112365',
    )
    def test_real_soc_info_caseid_112365(self):
        self.bus_comm.set_HV_SOC_value(100.0)
        sleep(1)
        for soc_value in [90, 0, 100, 88] :
            logger.info("---------------->{soc_value}")
            self.bus_comm.set_HV_SOC_value(float(soc_value))
            self.tsp.check_rvs_data_update_new(
                block=BlockName.GISAndTravel, keys=["socInfo", "realSoc"], target_value=float(soc_value),timeout=7
            )

        
    @pytest.mark.sanity
    @pytest.mark.fail
    def test_vehicle_spd_caseid_112367(self):
        self.bus_comm.set_tailgate_opener_sts(sts=DoorOpenerSts.FullClsd)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_vehspd_gear(vehspd=5.0)
        sleep(1)
        self.bus_comm.set_vehspd_gear(vehspd=10.0)
        self.tsp.check_rvs_data_update_new(
                 block=BlockName.GISAndTravel,keys=["speed","speed"],target_value=(38),timeout=10
                )
        self.bus_comm.set_vehspd_gear(vehspd=28.0)
        self.tsp.check_rvs_data_update_new(
                 block=BlockName.GISAndTravel,keys=["speed","speed"],target_value=(106),timeout=10
                )
    
    @pytest.mark.full
    @pytest.mark.fail
    def test_HVBatterySOH_caseid_1983498(self):
        self.bus_comm.set_singal("propulsioncan","BecmPropFr04","HvBattEgyCdn",80.0)
        sleep(3)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr04","HvBattEgyCdn",90.0)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.GISAndTravel,keys=["hvSOH"],target_value=90.0,timeout=7
            )
        sleep(3)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr04","HvBattEgyCdn",100.0)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.GISAndTravel,keys=["hvSOH"],target_value=100.0,timeout=7
            )


    @pytest.mark.full
    def test_estimatedAEC_caseid_1983454(self):
        estimatedAEC = [-100,50,100]
        for key in estimatedAEC:
            self.soa.send_method_request("HighVoltageService_client", "SetAveragePowerConsume", {"power":key})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.GISAndTravel,keys=["travelMileage","estimatedAEC"],target_value=key,timeout=7
            )


    @pytest.mark.sanity
    def test_CLTCRange_caseid_1986516(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950: 1,966:1})
        self.bus_comm.set_singal("propulsioncan","BecmPropFr04","HvBattEgyCdn",100.0)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr04", 'DispHvBattLvlOfChrg', 90.0)
        sleep(1)
        for key in [0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0]:
            sleep(5)
            self.bus_comm.set_singal("propulsioncan","EcmPropFr04", 'DispHvBattLvlOfChrg', key)
            self.tsp.check_rvs_data_update_new(
                block=BlockName.GISAndTravel,keys=["travelMileage","cltcResidueMileage"],target_value=key*0.01*780,timeout=8
            )


    @pytest.mark.full
    def test_estimatedRange_caseid_112327(self):
        self.soa.send_method_request("HighVoltageService_client", "SetRange",
                                         {"infos": {"type": 1, "CLTCRange":999, "estimatedRange": 200}})
        estimatedRange= [0,500,501,999]
        for key in estimatedRange:
            self.soa.send_method_request("HighVoltageService_client", "SetRange",
                                         {"infos": {"type": 1, "CLTCRange":999, "estimatedRange": key}})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.GISAndTravel,keys=["travelMileage","estimatedResidueMileage"],target_value=key,timeout=8
            )

    # @pytest.mark.full
    # def test_distance_caseid_1983455(self):
    #     self.bus_comm.set_singal("backbonefr","CemBackBoneFr10", 'TotDstTrvldHiResl', 0)
    #     for key in [1, 100, 1000, 50000, 100000, 1000000, 10000000, 200000000, 2000000000, 4294967295, 0]:
    #         logger.info(f"打印{key}")
    #         self.bus_comm.set_singal("backbonefr","CemBackBoneFr10", 'TotDstTrvldHiResl', key)
    #         self.tsp.check_rvs_data_update_new(
    #             block=BlockName.GISAndTravel,keys=["travelMileage","currentMileage"],target_value=key,timeout=7,sleep_time=15
    #         )


    # @allure.title("车速超过120km/h提醒(针对GSO),WTI-2412")
    # @pytest.mark.full
    # def test_caseid_1997108(self):
    #     self.sd_tester.write_multi_ccp({948:1})
    #     self.bus_comm.set_tailgate_opener_sts(sts=DoorOpenerSts.FullClsd)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
    #     self.bus_comm.set_vehspd_gear(vehspd=10.0)
    #     sleep(1)
    #     self.bus_comm.set_vehspd_gear(vehspd=33.0)
    #     assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgVehSpdOver120",wtiFlag=1)
    #     sleep(1)
    #     self.bus_comm.set_vehspd_gear(vehspd=31.0)
    #     assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgVehSpdOver120",wtiFlag=0)
            