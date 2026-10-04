#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_DrivingAssistService.py
@Time         :2023/12/12 10:07:44
@Author       :peipei.yang_ext@jiduauto.com
@Description  :
"""
import os
import sys
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *


@pytest.mark.ypp
@allure.feature("SOA服务接口")
@allure.story("整车控制/DrivingAssistService")
class TestDrivingAssistService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("DrivingAssistService", "client")])
        self.partner.method_default_timeout = 0.1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,'VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3') # 切UsageMode的前置条件
        self.sd_tester.tester_present()

    def after_class(self, ecu):
        self.partner.stop_operators()
        self.sd_tester.stop_tester_present()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set_vehspd(0)  # 车速
        sleep(0.5)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.partner.empty_all(0.5)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()  # 信号恢复
        if ecu.get("testresult") != "Pass":
            logger.error("case失败，需等待10s让环境恢复")
            sleep(10)
        else:
            logger.info("case成功，需等待3s让环境恢复")
            sleep(3)
        super().after_each_func(ecu, start=False)

    @allure.title("设置CDC备用行驶里程")
    @pytest.mark.sanity
    def test_caseid_1981283(self):
        for tance in [100, 1000, 10000, 100000, 1000000, 10000000, 200000000, 2000000000, 0]:
            # todo 开始抓包
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(DRIVINGASSIST_SERVICE_CLIENT, "SetDistanceBackup", {"distance": tance})
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_signal_values('DstTrvldFromCDC', [tance])

    @allure.title("设置CDC备用行驶里程_超范围值")
    @pytest.mark.full
    def test_caseid_1981358(self):
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(DRIVINGASSIST_SERVICE_CLIENT, "SetDistanceBackup", {"distance": 2000000001})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('DstTrvldFromCDC', [])

    @allure.title("获取驾驶员HandsOFF状态&通知驾驶员HandsOFF状态")
    @pytest.mark.smoke
    def test_caseid_1981316(self):
        self.ipdu.set(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionHandsOnStatus', 0)
        self.ipdu.set(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionErrorStatus', 0)
        self.partner.empty_all(0.5)
        for onSts in [1, 2, 3, 0]:
            logger.info(f"打印{onSts}")
            self.ipdu.set(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionHandsOnStatus', onSts)
            for errSts in [1, 2, 3, 4, 5, 6, 7, 0]:
                logger.info(f"打印{errSts}")
                self.ipdu.set(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionErrorStatus', errSts)
                self.partner.ck_s2s_event(DRIVINGASSIST_SERVICE_CLIENT, "handOFFSts",
                                          {"sts": {"onSts": onSts, "errSts": errSts}})
                self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "getHandOFFSts", {},
                                                      {"out": {"onSts": onSts, "errSts": errSts}})

    @allure.title("获取驾驶员HandsOFF状态&通知驾驶员HandsOFF状态_默认值")
    @pytest.mark.full
    def test_caseid_1981319(self):
        for sts in [1, 0]:
            self.ipdu.set(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionHandsOnStatus', sts)
            self.ipdu.set(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionErrorStatus', sts)
            self.partner.empty_all(0.5)
            self.restart_bgm_and_connect_service(DRIVINGASSIST_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "getHandOFFSts", {},
                                                {"out": {"onSts": 0, "errSts": 0}})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(DRIVINGASSIST_SERVICE_CLIENT, "handOFFSts",
                                    {"sts": {"onSts": sts, "errSts": sts}})
            self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "getHandOFFSts", {},
                                                {"out": {"onSts": sts, "errSts": sts}})

    @allure.title("获取驾驶员HandsOFF状态&通知驾驶员HandsOFF状态_通信故障")
    @pytest.mark.sanity
    def test_caseid_1981321(self):
        sleep(10)
        self.ipdu.set(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionHandsOnStatus', 1)
        self.ipdu.set(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionErrorStatus', 1)
        self.partner.empty_all(0.5)
        self.ipdu.pause_ecu_send("cem_lin4","HOD")
        sleep(1)
        self.partner.ck_s2s_event(DRIVINGASSIST_SERVICE_CLIENT, "handOFFSts",
                                  {"sts": {"onSts": 1, "errSts": 3}})
        self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "getHandOFFSts", {},
                                              {"out": {"onSts": 1, "errSts": 3}})
        self.ipdu.resume_ecu_send("cem_lin4","HOD")
        self.partner.ck_s2s_event(DRIVINGASSIST_SERVICE_CLIENT, "handOFFSts",
                                  {"sts": {"onSts": 1, "errSts": 1}}, timeout=1)
        self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "getHandOFFSts", {},
                                              {"out": {"onSts": 1, "errSts": 1}}, timeout=1)

    @allure.title("获取驾驶员HandsOFF状态&通知驾驶员HandsOFF状态_E2E故障")
    @pytest.mark.full
    def test_caseid_1981325(self):
        self.ipdu.set(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionHandsOnStatus', 1)
        self.ipdu.set(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionErrorStatus', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set_no_crc(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionHandsOnStatus')
        self.partner.ck_s2s_event(DRIVINGASSIST_SERVICE_CLIENT, "handOFFSts",
                                  {"sts": {"onSts": 1, "errSts": 3}})
        self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "getHandOFFSts", {},
                                              {"out": {"onSts": 1, "errSts": 3}})
        self.ipdu.restore_crc(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionHandsOnStatus')
        self.partner.ck_s2s_event(DRIVINGASSIST_SERVICE_CLIENT, "handOFFSts",
                                  {"sts": {"onSts": 1, "errSts": 1}}, timeout=1)
        self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "getHandOFFSts", {},
                                              {"out": {"onSts": 1, "errSts": 1}}, timeout=1)
    
    # @allure.title("获取驾驶员HandsOFF状态&通知驾驶员HandsOFF状态(E2E校验失败+信号丢失)")#
    # @pytest.mark.full
    # def test_caseid_qqqq(self):
    #     self.ipdu.set(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionHandsOnStatus', 1)
    #     self.ipdu.set(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionErrorStatus', 1)
    #     self.partner.empty_all(0.5)
    #     self.ipdu.set_no_crc(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionHandsOnStatus')
    #     sleep(1)
    #     self.partner.ck_s2s_event(DRIVINGASSIST_SERVICE_CLIENT, "handOFFSts",
    #                               {"sts": {"onSts": 1, "errSts": 3}})
    #     self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "getHandOFFSts", {},
    #                                           {"out": {"onSts": 1, "errSts": 3}})
    #     # self.ipdu.pause_ecu_send("cem_lin4","HOD")
    #     # self.ipdu.pause_bus_send("cem_lin4")
    #     self.ipdu.pause_all_bus_send()
    #     sleep(1)
    #     self.partner.ck_no_event(DRIVINGASSIST_SERVICE_CLIENT, "handOFFSts")
    #     self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "getHandOFFSts", {},
    #                                           {"out": {"onSts": 1, "errSts": 3}})
    #     self.ipdu.resume_ecu_send("cem_lin4","HOD")
    #     sleep(2)
    #     self.partner.ck_no_event(DRIVINGASSIST_SERVICE_CLIENT, "PedalFault")
    #     self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "getHandOFFSts", {},
    #                                           {"out": {"onSts": 1, "errSts": 3}})
    #     self.ipdu.restore_crc(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionHandsOnStatus')
    #     self.partner.ck_s2s_event(DRIVINGASSIST_SERVICE_CLIENT, "handOFFSts",
    #                               {"sts": {"onSts": 1, "errSts": 1}}, timeout=1)
    #     self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "getHandOFFSts", {},
    #                                           {"out": {"onSts": 1, "errSts": 1}}, timeout=1)


@pytest.mark.ypp
@allure.feature("SOA服务接口")
@allure.story("整车控制/DrivingAssistService")
class TestDrivingAssistServiceMockMcu(TestBase):

    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([DRIVINGASSIST_SERVICE_CLIENT])

    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.partner.empty_all(1)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    @pytest.mark.sanity
    @allure.title("获取行驶里程&通知行驶里程")
    def test_caseid_1943379(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr10, 'TotDstTrvldHiResl', 0)
        self.partner.empty_all(0.5)
        for hiResl in [1, 100, 1000, 50000, 100000, 1000000, 10000000, 200000000, 2000000000, 4294967295, 0]:
            logger.info(f"打印{hiResl}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr10, 'TotDstTrvldHiResl', hiResl)
            self.partner.ck_s2s_event(DRIVINGASSIST_SERVICE_CLIENT, "NotifyTraveledDistance", {"distance": hiResl})
            self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "GetTraveledDistance", {},
                                                  {"out": hiResl})

    @pytest.mark.full
    @allure.title("获取行驶里程&通知行驶里程_默认值")
    def test_caseid_1981313(self):
        for sts in [1, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr10, 'TotDstTrvldHiResl', sts)
            self.partner.empty_all(0.5)
            self.restart_bgm_and_connect_service(DRIVINGASSIST_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "GetTraveledDistance", {},
                                                {"out": -1}, timeout=6)
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(DRIVINGASSIST_SERVICE_CLIENT, "NotifyTraveledDistance", {"distance": sts})
            self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "GetTraveledDistance", {},
                                                {"out": sts})
