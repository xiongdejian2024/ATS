# -*- coding: utf-8 -*-
"""
@File        : test_LowVoltageService.py
@Author      : tao.cheng_ext@jiduatuo.com
@Time        : 2023/06/5 18:00 PM
@Description : Test SOA for LowVoltageService
"""

import os
import sys


from socket import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_cases.legacy.soa.case_helper.parse_excel import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.bgm.bgm_env.change_bgm_env import *

LOWVOLTAGE_SERVICE = "LowVoltageService_client"
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)


@allure.feature("SOA服务接口")
@allure.story("架构基础/LowVoltageService")
class TestLowVoltageService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("LowVoltageService", "client"), ("WTIService", "client")])
        self.partner.method_default_timeout = 0.1
        self.sd_tester.tester_present()

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        sleep(1)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        self.sd_tester.stop_tester_present()
        super().after_class(self, ecu)

    def BGM_down_up(self,X,Y,Z):
        """X代表总线停后等待时间 Y代表下电后电等待时间 Z代表上电后电等待时间"""
        self.ipdu.pause_all_bus_send()
        sleep(X)
        self.nucapp.bgm_power_off()
        sleep(Y)
        self.nucapp.bgm_power_on()
        sleep(Z)
        
    @allure.title("遍历_备用低压电池系统异常_通知和获取所有情况")
    @pytest.mark.sanity
    def test_caseid_1979654(self):
        for X in [0,2,3,4,5,6,7]:
            self.ipdu.set(self.ipdu.bodycan.IpmBodyFr01, 'IPMLVPwrSplyErrSts', 1)
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.bodycan.IpmBodyFr01, 'IPMLVPwrSplyErrSts', X)
            sleep(0.5)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"IPM Battery Fault Waring","info":"0"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{}, {"out":[{"name":"IPM Battery Fault Waring","info":"0"}]})
            self.ipdu.set(self.ipdu.bodycan.IpmBodyFr01, 'IPMLVPwrSplyErrSts', 1)
            sleep(0.5)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"IPM Battery Fault Waring","info":"1"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{}, {"out":[{"name":"IPM Battery Fault Waring","info":"1"}]})

    @allure.title("获取低压系统电压低报警信息_ULoWarnULoWarn=0")
    @pytest.mark.smoke
    def test_caseid_1978111(self):
        self.sd_tester.write_single_ccp(32, 9)
        for X in [1, 2, 11]:
            logger.info(f"使用者模式为{X}")
            self.sd_tester.change_usage_mode(X)
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetLowWarn", {}, {"out": 0})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                  {"out": [{"name": "Low Voltage Battery", "state": "0"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": "Low Battery Warning1", "info": "0"}]})

    @allure.title("获取和通知低压电池状态_rawVoltage_边界值")
    @pytest.mark.full
    def test_caseid_111056(self):
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr05, 'BattURaw', 10)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr05, 'BattURaw', 5.0)
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus", {"status": {"rawVoltage": 5.0}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"rawVoltage": 5.0}})

        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr05, 'BattURaw', 17.775)
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus", {"status": {"rawVoltage": 17.775}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"rawVoltage": 17.775}})

    @allure.title("获取和通知低压电池状态_BattSocRaw _边界值")
    @pytest.mark.full
    def test_caseid_111055(self):
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr05, 'BattSocRaw', 10)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr05, 'BattSocRaw', 50.0)
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus", {"status": {"rawSoc": 50.0}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"rawSoc": 50.0}})

        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr05, 'BattSocRaw', 100.0)
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus", {"status": {"rawSoc": 100}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"rawSoc": 100}})

    @allure.title("获取和通知低压电池状态_rawCurrent_边界值")
    @pytest.mark.full
    def test_caseid_111057(self):
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr01, 'BattIRaw', 10)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr01, 'BattIRaw', -512.0)
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus", {"status": {"rawCurrent": -512.0}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"rawCurrent": -512.0}})

        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr01, 'BattIRaw', 511.0)
        sleep(2)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus", {"status": {"rawCurrent": 511.0}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"rawCurrent": 511.0}})

    @allure.title("获取和通知低压电池状态_rawTemperature_边界值")
    @pytest.mark.full
    def test_caseid_111058(self):
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattTRaw', 10)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattTRaw', -70.0)
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus", {"status": {"rawTemperature": -70.0}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"rawTemperature": -70.0}})

        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattTRaw', 125.0)
        sleep(2)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus", {"status": {"rawTemperature": 125.0}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"rawTemperature": 125.0}})

    @allure.title("获取和通知低压电池状态_rawInternalResistance_边界值")
    @pytest.mark.full
    def test_caseid_111059(self):
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr04, 'BattRRaw', 10)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr04, 'BattRRaw', 0)
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus", {"status": {"rawInternalResistance": 0}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"rawInternalResistance": 0}})

        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr04, 'BattRRaw', 25.0)
        sleep(2)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus", {"status": {"rawInternalResistance": 25.0}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"rawInternalResistance": 25.0}})

    @allure.title("获取和通知低压电池状态__BattCpEstimdRaw__边界值")
    @pytest.mark.full
    def test_caseid_111060(self):
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattCpEstimdRaw', 10)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattCpEstimdRaw', 0)
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus", {"status": {"estimatedCapacity": 0}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"estimatedCapacity": 0}})

        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattCpEstimdRaw', 100.0)
        sleep(2)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus", {"status": {"estimatedCapacity": 100.0}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"estimatedCapacity": 100.0}})

    @allure.title("获取和通知低压电池状态_averageQuiescentCurrentLong_边界值")
    @pytest.mark.full
    def test_caseid_111061(self):
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattIQuiscFildLongRaw', -10.0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattIQuiscFildLongRaw', -511.0)
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus", {"status": {"averageQuiescentCurrentLong": -511}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"averageQuiescentCurrentLong": -511}})

        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattIQuiscFildLongRaw', 0.0)
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus", {"status": {"averageQuiescentCurrentLong": 0.0}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"averageQuiescentCurrentLong": 0.0}})

    @allure.title("获取和通知低压电池状态_averageQuiescentCurrentLevel_边界值")
    @pytest.mark.full
    def test_caseid_111062(self):
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattIQuiscAvgRaw', -10.0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattIQuiscAvgRaw', 0.0)
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus",
                                  {"status": {"averageQuiescentCurrentLevel": 0}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"averageQuiescentCurrentLevel": 0}})

        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattIQuiscAvgRaw', -2500.0)
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus", {"status": {"averageQuiescentCurrentLevel": -2500.0}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"averageQuiescentCurrentLevel": -2500.0}})

    @allure.title("获取和通知低压电池状态_openCircuitVoltage_边界值")
    @pytest.mark.full
    def test_caseid_111063(self):
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr04, 'BattCircOpenU', 0.0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr04, 'BattCircOpenU', 6.0)
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus",
                                  {"status": {"openCircuitVoltage": 6.0}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"openCircuitVoltage": 6.0}})

        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr04, 'BattCircOpenU', 13.75)
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus",
                                  {"status": {"openCircuitVoltage": 13.75}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"openCircuitVoltage": 13.75}})

    @allure.title("获取和通知低压电池状态_actualCurrentOutput_边界值")
    @pytest.mark.full
    def test_caseid_111065(self):
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr02, 'IDcDcActLoSideIDcDcActLoSide', 0.0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr02, 'IDcDcActLoSideIDcDcActLoSide', 10.0)
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus",
                                  {"status": {"actualCurrentOutput": 10.0}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"actualCurrentOutput": 10.0}})

        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr02, 'IDcDcActLoSideIDcDcActLoSide', 409.5)
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus",
                                  {"status": {"actualCurrentOutput": 409.5}})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                              {"out": {"actualCurrentOutput": 409.5}})
        
    @allure.title("获取和通知全部低压系统故障信息（带功能安全需求参数）")
    @pytest.mark.full
    def test_caseid_1978109(self):
        self.sd_tester.write_single_ccp(32, 9)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr05, 'BattURaw', 12.0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr15, 'FltTDcDc', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'DcDcActvd', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr21, 'FltElecDcDc', 0)
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 1)
        sleep(10)
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 1)
        sleep(10)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "LVFaultValidity",
                                      {"faults":[{"value":{"faultId": 5, "faultMsg":""},"faultIdValidity":0}]})
        try:
            self.ipdu.pause_bus_send("backbonefr")
            sleep(1)
            self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "LVFaultValidity",
                                      {"faults":[{"value":{"faultId": 5, "faultMsg":""},"faultIdValidity":4}]})
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetLVFaultValidity", {},
                                                  {"out":[{"value":{"faultId": 5, "faultMsg":""},"faultIdValidity":4}]})
        except Exception as error:
            self.ipdu.resume_bus_send("backbonefr")
            assert False, error
        else:
            self.ipdu.resume_bus_send("backbonefr")
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "LVFaultValidity",
                                  {"faults": [{"value": {"faultId": 5, "faultMsg":""}, "faultIdValidity": 0}]})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetLVFaultValidity", {},
                                              {"out": [{"value": {"faultId": 5, "faultMsg":""}, "faultIdValidity": 0}]})
        sleep(5) #恢复总线时影响到下一个case的tcpdump了
        
    @allure.title("设置低压补电间隔时间最大值_遍历")
    @pytest.mark.full
    def test_caseid_1984718(self):
        for type in range(4):
            for time in [0,100,20160]:
                logger.info(f"调用type{type}和time{time}")
                self.bgm_eth_inter.start_bgm_tcpdump()
                sleep(1)
                self.partner.send_request_and_ck_resp(LOWVLORAGE_SERVICE_CLIENT, "SetLowVoltageBatteryRechargeMaxTime",
                                                    {"info": {"type": type, "time" :time}},{"out":  1})
                sleep(2)
                self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
                self.bgm_eth_inter.ck_ordered_array("MaxTiLVBattReChargeReq", [time])
                sleep(2)
        self.bgm_eth_inter.start_bgm_tcpdump() #超范围值
        self.partner.send_request_and_ck_resp(LOWVLORAGE_SERVICE_CLIENT, "SetLowVoltageBatteryRechargeMaxTime",
                                            {"info": {"type": 3, "time" :20161}},{"out": 0})
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("MaxTiLVBattReChargeReq", [20160])

    @allure.title("设置低压补电间隔时间最小值_遍历")
    @pytest.mark.full
    def test_caseid_1984721(self):
        for type in range(4):
            for time in [0,100,120]:
                logger.info(f"调用type{type}和time{time}")
                self.bgm_eth_inter.start_bgm_tcpdump()
                self.partner.send_request_and_ck_resp(LOWVLORAGE_SERVICE_CLIENT, "SetLowVoltageBatteryChargeMinTime",
                                                    {"info": {"type": type, "time" :time}},{"out":  1})
                sleep(1)
                self.bgm_eth_inter.stop_tcpdump_and_parse_signal(1)
                self.bgm_eth_inter.ck_ordered_array("MinTiLVBattChargeReq", [time])
                sleep(2)
        self.bgm_eth_inter.start_bgm_tcpdump() #超范围值
        self.partner.send_request_and_ck_resp(LOWVLORAGE_SERVICE_CLIENT, "SetLowVoltageBatteryChargeMinTime",
                                            {"info": {"type": 3, "time" :130}},{"out": 0})
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("MinTiLVBattChargeReq", [120])

    @allure.title("设置低压补电间隔时间最大值_重启记忆")
    @pytest.mark.full
    def test_caseid_1984722(self):
        self.partner.send_request_and_ck_resp(LOWVLORAGE_SERVICE_CLIENT, "SetLowVoltageBatteryChargeMinTime",
                                                    {"info": {"type": 3, "time" :120}},{"out": 1})
        sleep(2) #数据库存储延时
        self.restart_bgm_and_connect_service(LOWVLORAGE_SERVICE_CLIENT)
        sleep(2)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("MinTiLVBattChargeReq", [120])
        self.partner.send_request_and_ck_resp(LOWVLORAGE_SERVICE_CLIENT, "SetLowVoltageBatteryChargeMinTime",
                                                    {"info": {"type": 3, "time" :130}},{"out": 0})
        sleep(2) #数据库存储延时
        self.restart_bgm_and_connect_service(LOWVLORAGE_SERVICE_CLIENT)
        sleep(2)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("MinTiLVBattChargeReq", [120])

    @allure.title("设置低压补电间隔时间最大值_重启记忆")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1984720(self):
        self.partner.send_request_and_ck_resp(LOWVLORAGE_SERVICE_CLIENT, "SetLowVoltageBatteryRechargeMaxTime",
                                                    {"info": {"type": 3, "time" :1000}},{"out": 1})
        sleep(2) #数据库存储延时
        self.restart_bgm_and_connect_service(LOWVLORAGE_SERVICE_CLIENT)
        sleep(2)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(1)
        self.bgm_eth_inter.ck_ordered_array("MaxTiLVBattReChargeReq", [1000])
        self.partner.send_request_and_ck_resp(LOWVLORAGE_SERVICE_CLIENT, "SetLowVoltageBatteryRechargeMaxTime",
                                                    {"info": {"type": 3, "time" :30000}},{"out": 0})
        sleep(2) #数据库存储延时
        self.restart_bgm_and_connect_service(LOWVLORAGE_SERVICE_CLIENT)
        sleep(2)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("MaxTiLVBattReChargeReq", [1000])
        
    @allure.title("设置低压补电间隔时间最大值和设置低压补电时间最小值_出厂设置值")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1984716(self):
        #删除数据库
        bgmssh = BGM_SSH()
        bgmssh.type_commands("sudo rm -rf /data/s2s_service/s2s_service.db3", root_permission=True)
        sleep(1)
        bgmssh.type_commands("ls -l /data/s2s_service")
        sleep(2)
        self.restart_bgm_and_connect_service(LOWVLORAGE_SERVICE_CLIENT)
        sleep(2)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time("MaxTiLVBattReChargeReq", 0.5, permit_fail_times=2)#重启波动
        self.bgm_eth_inter.ck_period_time("MinTiLVBattChargeReq", 0.5, permit_fail_times=2)
        self.bgm_eth_inter.ck_ordered_array("MaxTiLVBattReChargeReq", [360])
        self.bgm_eth_inter.ck_ordered_array("MinTiLVBattChargeReq", [30])
        
    @allure.title("低压服务启动默认值")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1984245(self):
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr02, 'IDcDcActLoSideIDcDcActLoSide', 0.0)
        self.BGM_down_up(2,3,10)
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "BatteryStatus",
                                {"status": {"rawVoltage": 0.0,"rawCurrent": 0.0, "rawTemperature": 0.0,
                                            "rawInternalResistance": 0.0, "estimatedCapacity": 0,
                                            "averageQuiescentCurrentShort": 0,
                                            "averageQuiescentCurrentLong": 0,
                                            "averageQuiescentCurrentLevel": 0, "openCircuitVoltage": 0,
                                            "bmsConsistencyFault": 0, "calculatedStatus": 0}})
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"LVBatteryRechargeReqSts",{"sts":0})
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "LowWarn", {"warn": 0})
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "LVFaultValidity",
                                                  {"faults":[{"value":{"faultId": 0, "faultMsg":""},"faultIdValidity":0}]})
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE, "LVFault",{"faults":[{"faultId":0, "faultMsg": ""}]})
        
    @allure.title("获取和通知低压电池状态_默认值")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_111052(self):
        try:
            self.BGM_down_up(2,3,10)
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetBatteryStatus", {},
                                                  {"out": {"rawSoc": -1.0, "rawVoltage": 0.0,
                                                           "rawCurrent": 0.0, "rawTemperature": 0.0,
                                                           "rawInternalResistance": 0.0, "estimatedCapacity": 0,
                                                           "averageQuiescentCurrentShort": 0,
                                                           "averageQuiescentCurrentLong": 0,
                                                           "averageQuiescentCurrentLevel": 0, "openCircuitVoltage": 0,
                                                           "bmsConsistencyFault": 0, "calculatedStatus": 0
                                                          }})
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetLowWarn", {}, {"out": 0})
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetLVFaultValidity", {},
                                                  {"out":[{"value":{"faultId": 0, "faultMsg":""},"faultIdValidity":0}]})
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,"GetLVFault",{},
                                                  {"out":[{"faultId":0, "faultMsg": ""}]})
        except Exception as error:
            self.ipdu.resume_all_bus_send()
            assert False
        else:
            self.ipdu.resume_all_bus_send()

@allure.feature("SOA服务接口")
@allure.story("架构基础/LowVoltageService")   
class TestLowVoltageServiceMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("LowVoltageService", "client")])
        self.bgm_tcpdump = BGM_SSH()
        self.bgm_tcpdump.init_bgm_tcpdump()

    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        self.bgm_tcpdump.stop_bgm_tcpdump()
        self.bgm_tcpdump.delete_bgm_tcpdump_file(bgm_log_name='*.pcap')
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu)

    @allure.title("通知和获取低压电池智能补电请求状态_遍历") 
    @pytest.mark.sanity
    def test_caseid_1980696(self):
        sleep(5)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdDevFr01, 'LVBattCnvnReq', 0)
        sleep(0.5)
        for sigin in [1,0]:
            self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdDevFr01, 'LVBattCnvnReq', sigin)
            sleep(0.5)
            self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"LVBatteryRechargeReqSts",{"sts":sigin})
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,"GetLVBatteryRechargeReqSts",{},{"out":sigin})
        for sigin1 in range(2,8):
            self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdDevFr01, 'LVBattCnvnReq', sigin1)
            sleep(0.5)
            self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"LVBatteryRechargeReqSts",{"sts":2})
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,"GetLVBatteryRechargeReqSts",{},{"out":2})
            self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdDevFr01, 'LVBattCnvnReq', 1)
            sleep(1)

    @allure.title("MOCKMCU_获取低压系统电压低报警信息_遍历") 
    @pytest.mark.full
    def test_caseid_111067(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn', 1)
        sleep(1)
        for sigin in range(3):
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn', sigin)
            sleep(1)
            self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"LowWarn",{"warn":sigin})
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,"GetLowWarn",{},{"out":sigin})
        self.ipdu.set_no_crc(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn')
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"LowWarn",{"warn":3})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,"GetLowWarn",{},{"out":3})
        self.ipdu.restore_crc(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn')
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"LowWarn",{"warn":2})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,"GetLowWarn",{},{"out":2})

    @allure.title("MOCKMCU_获取低压系统电压低报警信息_E2E校验失败时改变信号") 
    @pytest.mark.full
    def test_caseid_1984297(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn', 1)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,"GetLowWarn",{},{"out":1})
        self.ipdu.set_no_crc(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn')
        sleep(0.5)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"LowWarn",{"warn":3})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn', 2)
        sleep(1)
        self.partner.ck_no_event(LOWVOLTAGE_SERVICE,"LowWarn")
        self.ipdu.restore_crc(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn')
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"LowWarn",{"warn":2})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,"GetLowWarn",{},{"out":2})

    @allure.title("MOCKMCU_获取和通知全部低压系统故障信息_遍历") 
    @pytest.mark.full
    def test_caseid_111074(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts', 15)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"LVFault",
                                      {"faults":[{"faultId":9, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,"GetLVFault",{},
                                                  {"out":[{"faultId":9, "faultMsg": ""}]})
        for sigin in [0,1,2,4,5,6,7,8]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts', sigin)
            sleep(1)
            self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"LVFault",
                                      {"faults":[{"faultId":sigin, "faultMsg": ""}]})
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,"GetLVFault",{},
                                                  {"out":[{"faultId":sigin, "faultMsg": ""}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts', 3)
        self.partner.empty_all(0.5)
        for sigin in [3,9,10,11,12,13,14]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts', sigin)
            sleep(1)
            self.partner.ck_no_event(LOWVOLTAGE_SERVICE,"LVFault")
            self.partner.ck_no_event(LOWVOLTAGE_SERVICE,"LVFaultValidity")
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,"GetLVFault",{},
                                                  {"out":[{"faultId":11, "faultMsg": ""}]})

    @allure.title("获取和通知低压电池状态_voltage_边界值") 
    @pytest.mark.full
    def test_caseid_111053(self):
        def info(value):
            return True if value == 1 else False
        def info2(value):
            return True if value == 3 else False
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'VehBattUSysU', 10.0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'ChrgnUReq', 11.0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'VehBattUSysUQf', 3)
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr04, 'BattIQuiscFildShoRaw', 10.0)
        self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr04, 'BattSnsrCalcnNotVldRaw', 0)
        self.partner.empty_all(1) # voltage
        for sigin1 in [0.0,25.0]: 
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'VehBattUSysU', sigin1)
            sleep(0.5)
            self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"BatteryStatus",{"status":{"voltage":sigin1}})
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,"GetBatteryStatus",{},{"out":{"voltage":sigin1}})
        self.partner.empty_all(1) #  averageQuiescentCurrentShort
        for sigin2 in [-511.0,0.0]:
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr04, 'BattIQuiscFildShoRaw', sigin2)
            sleep(0.5)
            self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"BatteryStatus",{"status":{"averageQuiescentCurrentShort":sigin2}})
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,
                                                  "GetBatteryStatus",{},{"out":{"averageQuiescentCurrentShort":sigin2}})
        self.partner.empty_all(1) #  bmsConsistencyFault
        for sigin3 in [1,0]:
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr04, 'BattSnsrCalcnNotVldRaw', sigin3)
            sleep(0.5)
            self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"BatteryStatus",{"status":{"bmsConsistencyFault":info(sigin3)}})
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,
                                                  "GetBatteryStatus",{},{"out":{"bmsConsistencyFault":info(sigin3)}})
        self.partner.empty_all(1) #  requestChargingVoltage
        for sigin4 in [10.6,16.0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'ChrgnUReq', sigin4)
            sleep(0.5)
            self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"BatteryStatus",{"status":{"requestChargingVoltage":sigin4}})
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,
                                                  "GetBatteryStatus",{},{"out":{"requestChargingVoltage":sigin4}}) 
        self.partner.empty_all(1) #  requestChargingVoltage
        for sigin5 in range(3):
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'VehBattUSysUQf', sigin5)
            sleep(0.5)
            self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"BatteryStatus",{"status":{"isValid":info2(sigin5)}})
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,
                                                  "GetBatteryStatus",{},{"out":{"isValid":info2(sigin5)}})
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'VehBattUSysUQf', 3)
            sleep(0.5)
            self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"BatteryStatus",{"status":{"isValid":True}})
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,
                                                  "GetBatteryStatus",{},{"out":{"isValid":True}})
        
######################################################################################################################################################## 
   
@allure.feature("SOA服务接口")
@allure.story("架构基础/LowVoltageService")
@pytest.mark.mock_tcp     
class TestLowVoltageService1MockMcu(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu, tcp_down_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass(
            [("LowVoltageService", "client")])
        self.partner.wait_for_service_reconnect(LOWVLORAGE_SERVICE_CLIENT)
    
    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
    
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu)

    @allure.title("MOCKMCU_获取和通知低压电池状态_遍历") 
    @pytest.mark.full
    def test_caseid_1983973(self):
        self.bgm_eth_inter.set_signal("BattSoc2Sts", 0, send_pdu_immediately=True)
        sleep(1)
        for sigin in [1,2,3,0]:
            logger.info(f"发送BattSoc2Sts信号值{sigin}")
            self.bgm_eth_inter.set_signal("BattSoc2Sts", sigin, send_pdu_immediately=True)
            sleep(1)
            self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"BatteryStatus",{"status":{"calculatedStatus":sigin}})
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,
                                                  "GetBatteryStatus",{},{"out":{"calculatedStatus":sigin}})
        for sigin1 in [100.0,0]:
            logger.info(f"发送BattSocRaw2信号值{sigin1}")
            self.bgm_eth_inter.set_signal("BattSocRaw2", sigin1, send_pdu_immediately=True)
            sleep(1)
            self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"BatteryStatus",{"status":{"calculatedSoc":sigin1}})
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,
                                                  "GetBatteryStatus",{},{"out":{"calculatedSoc":sigin1}})
        for sigin2 in [100.0,0]:
            logger.info(f"发送BattSohRaw2信号值{sigin2}")
            self.bgm_eth_inter.set_signal("BattSohRaw2", sigin2, send_pdu_immediately=True)
            sleep(1)
            self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"BatteryStatus",{"status":{"calculatedSoh":sigin2}})
            self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,
                                                  "GetBatteryStatus",{},{"out":{"calculatedSoh":sigin2}})



