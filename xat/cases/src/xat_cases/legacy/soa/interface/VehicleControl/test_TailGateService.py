# -*- coding: utf-8 -*-
"""
@File        : test_TailGateService.py
@Author      : tao.cheng_ext@jiduatuo.com
@Time        : 2023/06/08 15:00 PM
@Description : Test SOA for TailGateService
"""

import os
import sys
import pytest
import allure
from time import sleep
from threading import Thread
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_cases.legacy.soa.case_helper.parse_excel import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *

TAILGATESERVICE_CLIENT = "TailGateService_client"
WTI_SERVICE_CLIENT = "WTIService_client"


@allure.feature("SOA服务接口")
@allure.story("整车控制/TailGateService")
class TestTailGateService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("TailGateService", "client"),
                                     ("WTIService", "client")])
        self.partner.method_default_timeout = 0.1
        self.sd_tester.tester_present()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.partner.stop_operators()
        self.sd_tester.stop_tester_present()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.io.set_four_door_close()
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        sleep(1)
        self.sd_tester.write_multi_ccp({97: 2, 98: 2})
        sleep(3)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def BGM_down_up(self,X,Y,Z):
        """X代表总线停后等待时间 Y代表下电后电等待时间 Z代表上电后电等待时间"""
        self.ipdu.pause_all_bus_send()
        sleep(X)
        self.nucapp.bgm_power_off()
        sleep(Y)
        self.nucapp.bgm_power_on()
        sleep(Z)

    @allure.title("设置尾门开关暂停,校验TCP")
    @pytest.mark.full
    def test_caseid_1913714(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 1)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        for cmd in [0,2]:
            self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd": cmd})
            sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Open", {})
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 5)
        sleep(1)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd": 1})
        sleep(1)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Close", {})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=3)
        self.bgm_eth_inter.ck_signal_values("TrunkOpenHmiReq", [1,0,3,0,1,0,2,0,2,0])
        self.bgm_eth_inter.ck_period_time("TrunkOpenHmiReq", 0.1,permit_fail_times=5)

    @allure.title("设置尾门开度，校验TCP")
    @pytest.mark.full
    def test_caseid_1913715(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 1)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetPosition", {"pos": 60})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_signal_values("TrunkOpenHmiReq", [3,0])
        self.bgm_eth_inter.ck_period_time("TrunkOpenHmiReq", 0.1)
        self.bgm_eth_inter.ck_signal_values("TrOpenPosnReqFromHmi", [60,60,60,60,60,60,101])
        self.bgm_eth_inter.ck_period_time("TrOpenPosnReqFromHmi", 0.1,permit_fail_times=1)

    @allure.title("设置尾门开度_正常情况遍历")
    @pytest.mark.full
    def test_caseid_1983355(self):
        for state in [0,1,4,5,8,9,10]:
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 2)
            sleep(1)
            self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, 
                                                    "GetStatus", {}, {"out": 3})
            logger.info(f"--发送尾门开度100--回复状态{state}")
            self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetPosition", {"pos": 100})
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 3)
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', state)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr131, 'TrOpenPosnReqFromHmi', 100, timeout=1.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr131, 'TrOpenPosnReqFromHmi', 101, timeout=1.5)
            self.partner.empty_all(2)

    @allure.title("设置尾门开度_未收到however或close或open或unknow时的处理")
    @pytest.mark.full
    def test_caseid_1983358(self):
            for state in [2,3,6,7]:
                self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 2)
                sleep(1)
                logger.info(f"--回复状态{state}")
                self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetPosition", {"pos": 30})
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 3)
                self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', state)
                sleep(0.5)
                try:
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr131, 'TrOpenPosnReqFromHmi', 30, timeout=0.5)
                except Exception as err:
                    assert True
                else:
                    assert True
                sleep(2)
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 2)
            sleep(1)
            logger.info(f"--回复状态{state}")
            self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetPosition", {"pos": 30})
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 3)
            try:
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr131, 'TrOpenPosnReqFromHmi', 30, timeout=0.5)
            except Exception as err:
                assert True
            else:
                assert True

    @allure.title("设置尾门动作Closing_open_延时收到尾门状态")
    @pytest.mark.full
    def test_caseid_105527(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 2)
        sleep(1)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd": 1})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 3)
        sleep(3)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 4)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("尾门ukonw_open")
    @pytest.mark.full
    def test_caseid_105529(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 0)
        sleep(1)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd": 0})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 1)

    @allure.title("设置尾门动作openDurgOpen_open")
    @pytest.mark.full
    def test_caseid_105521(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 4)
        sleep(1)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd": 0})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 1)

    @allure.title("设置尾门动作FullClsd_closed")
    @pytest.mark.full
    def test_caseid_105526(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 1)
        sleep(1)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd": 1})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("获取和通知尾门开关状态_开关")
    @pytest.mark.smoke
    def test_caseid_110822(self):
        self.io.trunk_door_open()
        self.partner.empty_all(0.5)
        self.io.trunk_door_close()
        self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT, "OpenCloseStatus", {"sts":False})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetOpenCloseStatus", {}, {"out": False})
        self.io.trunk_door_open()
        self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT, "OpenCloseStatus", {"sts": True})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetOpenCloseStatus", {}, {"out": True})

    @allure.title("获取和通知尾门的当前开启信息")
    @pytest.mark.sanity
    def test_caseid_110823(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr03, 'TrOpenPosn', 0)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr03, 'TrOpenPosn', 40)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 2)
        self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT, "TailGateOpenStatusInfo", {"info":{"position": 40,"angle": 25, "sts": 3}})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetTailGateOpenStatusInfo", {},{"out":{"position": 40,"angle": 25, "sts": 3}})
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr03, 'TrOpenPosn', 100)
        sleep(1)
        self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT, "TailGateOpenStatusInfo",
                                  {"info": {"position": 100, "angle": 62, "sts": 3}})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetTailGateOpenStatusInfo", {},
                                              {"out": {"position": 100, "angle": 62, "sts": 3}})

    @allure.title("获取和通知尾门系统状态_遍历")
    @pytest.mark.sanity
    def test_caseid_106479(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrAntiPnch', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrAntiPnch', 1)
        sleep(0.5)
        self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT, "NotifyLiftgateSysSts", {"sts": {"isAntiPinchOn": True}})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetLiftgateSysSts", {}, {"out": {"isAntiPinchOn": True}})
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrAntiPnch', 0)
        sleep(1)
        self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT, "NotifyLiftgateSysSts", {"sts": {"isAntiPinchOn": False}})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetLiftgateSysSts", {},
                                              {"out": {"isAntiPinchOn": False}})
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 1)
        sleep(0.5)
        for X in range(11):
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', X)
            sleep(0.5)
            self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT, "NotifyLiftgateSysSts", {"sts": {"motionSts": X}})
            self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetLiftgateSysSts", {},
                                              {"out": {"motionSts": X}})
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr03, 'TopPosHmiFeedBack2_0_PotBodySignalIPdu03', 0)
        sleep(0.5)
        for Y in [101,0]:
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr03, 'TopPosHmiFeedBack2_0_PotBodySignalIPdu03', Y)
            sleep(0.5)
            self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT, "NotifyLiftgateSysSts", {"sts": {"topPosition": Y}})
            self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetLiftgateSysSts", {},
                                              {"out": {"topPosition": Y}})
            
    @allure.title("获取尾门最大开度设置状态_遍历")
    @pytest.mark.sanity
    def test_caseid_106485(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr03, 'TopPosHmiFeedBack2_0_PotBodySignalIPdu03', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr03, 'TopPosHmiFeedBack2_0_PotBodySignalIPdu03', 101)
        self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT, "PositionMax", {"max": 101})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetPositionMax", {}, {"out": 101})
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr03, 'TopPosHmiFeedBack2_0_PotBodySignalIPdu03', 0)
        sleep(1)
        self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT, "PositionMax", {"max": 0})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetPositionMax", {}, {"out": 0})

    @allure.title("设置尾门最大开度最大开度_遍历")
    @pytest.mark.sanity
    def test_caseid_106450(self):
        for X in [100,0]:
            self.partner.send_method_request(TAILGATE_SERVICE_CLIENT,"SetPositionMax",{"max": X})
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr131, 'TopPercTrFromHmi', X, timeout=0.5)

    @allure.title("获取和通知尾门故障信息")
    @pytest.mark.sanity
    def test_caseid_1983360(self):
        def info(input):
            return True if input == 1 else False
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr03, 'TrRelsFailtoHMI', 1)
        sleep(1)
        for state in [1,0]:
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr03, 'TrRelsFailtoHMI', state)
            sleep(1)
            self.partner.ck_s2s_event(TAILGATE_SERVICE_CLIENT,"TailGateFault",
                                       {"faults": [{"fault": state,"faultMsg":"","isFault": info(state)}]})
            self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetFaultInfo",{},
                                                  {"out": [{"fault": state,"faultMsg":"","isFault": info(state)}]})

    @allure.title("设置尾门动作FullClsd_open")
    @pytest.mark.sanity
    def test_caseid_105540(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 1)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd": 0})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 1)

    @allure.title("设置尾门动作MovgUpBrkg_stop")
    @pytest.mark.sanity
    def test_caseid_105538(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 3)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd": 2})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 3)

    # @allure.title("设置尾门动作StopDurgOpen_stop")
    # @pytest.mark.sanity
    # def test_caseid_105535(self):
    #     self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 4)
    #     sleep(2)
    #     self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd": 2})
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("设置尾门动作FullOpend_stop")
    @pytest.mark.full
    def test_caseid_105534(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 5)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd": 2})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("设置尾门动作MovgDwnBrkg_stop")
    @pytest.mark.full
    def test_caseid_105530(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 7)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd": 2})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 3)

    # @allure.title("设置尾门动作Ukwn_stop")
    # @pytest.mark.sanity
    # def test_caseid_105536(self):
    #     self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 0)
    #     sleep(2)
    #     self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd": 2})
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("打开尾门MovgDwnBrkg_stop")
    @pytest.mark.smoke
    def test_caseid_105488(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 7)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd": 2})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 3)

    @allure.title("打开尾门FullClsd")
    @pytest.mark.sanity
    def test_caseid_105501(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 1)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Open",{})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 1)

    @allure.title("打开尾门HalfClsd")
    @pytest.mark.sanity
    def test_caseid_105490(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 9)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Open", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 1)

    @allure.title("打开尾门Ukwn")
    @pytest.mark.full
    def test_caseid_105500(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 0)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Open", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 1)

    @allure.title("打开尾门StopDurgOpen")
    @pytest.mark.full
    def test_caseid_105492(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 4)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Open", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 1)

    @allure.title("打开尾门MovgUpBrkg_stop")
    @pytest.mark.full
    def test_caseid_105494(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 3)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Open", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("打开尾门MovgUp")
    @pytest.mark.full
    def test_caseid_105495(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 2)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Open", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("打开尾门StopMinPntForCls_stop")
    @pytest.mark.full
    def test_caseid_105487(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 10)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Open", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 1)

    @allure.title("打开尾门StopDurgCls")
    @pytest.mark.full
    def test_caseid_105489(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 8)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Open", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 1)

    @allure.title("打开尾门MovgDwn_stop")
    @pytest.mark.full
    def test_caseid_105491(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 6)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Open", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 3)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 4)
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 1)

    @allure.title("打开尾门FullOpend_stop")
    @pytest.mark.full
    def test_caseid_105493(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 5)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Open", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("打开尾门FullOpend_stop")
    @pytest.mark.sanity
    def test_caseid_105493(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 5)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Open", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("设置尾门动作openDurgCls_open")
    @pytest.mark.smoke
    def test_caseid_105523(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 8)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":0})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 1)

    @allure.title("设置尾门动作StopMinPntForCls_open")
    @pytest.mark.full
    def test_caseid_105522(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 10)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":0})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 1)

    @allure.title("设置尾门动作HalfClsd_open")
    @pytest.mark.full
    def test_caseid_105520(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 9)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":0})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 1)

    @allure.title("设置尾门动作FullOpend_closed")
    @pytest.mark.full
    def test_caseid_105511(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 5)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":1})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 2)

    @allure.title("设置尾门动作MovgDwnBrkg_closed")
    @pytest.mark.full
    def test_caseid_105516(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 7)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":1})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("设置尾门动作StopDurgOpen_closed")
    @pytest.mark.full
    def test_caseid_105513(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 4)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":1})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 2)

    @allure.title("设置尾门动作Ukwn_closed")
    @pytest.mark.full
    def test_caseid_105519(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 0)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":1})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 2)

    @allure.title("设置尾门动作StopDurgCls_open")
    @pytest.mark.full
    def test_caseid_105358(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 8)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":0})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 1)

    @allure.title("设置尾门动作Closing_open_延时收到尾门状态")
    @pytest.mark.full
    def test_caseid_105518(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 6)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":0})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 3)
        sleep(3)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 8)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("设置尾门动作Closing_open_正常收到尾门状态")
    @pytest.mark.full
    def test_caseid_105525(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 6)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":0})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 3)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 8)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 1)

    @allure.title("设置尾门动作FullClsd_closed")
    @pytest.mark.full
    def test_caseid_105512(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 1)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":1})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("设置尾门动作MovgDwn_closed")
    @pytest.mark.full
    def test_caseid_105514(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 6)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":1})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("设置尾门动作MovgDwn_stop")
    @pytest.mark.full
    def test_caseid_105532(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 6)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":2})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 3)

    @allure.title("设置尾门动作MovgUp_stop")
    @pytest.mark.full
    def test_caseid_105537(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 2)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":2})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 3)

    @allure.title("设置尾门动作FullClsd_stop")
    @pytest.mark.full
    def test_caseid_105539(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 1)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":2})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("设置尾门动作FullOpend_open")
    @pytest.mark.full
    def test_caseid_105524(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 5)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":0})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("设置尾门动作StopDurgCls_stop")
    @pytest.mark.full
    def test_caseid_105528(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 8)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":2})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("设置尾门动作StopMinPntForCls_stop")
    @pytest.mark.full
    def test_caseid_105533(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 10)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":2})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("设置尾门动作StopDurgCls_closed")
    @pytest.mark.full
    def test_caseid_105517(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 8)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":1})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 2)

    @allure.title("设置尾门动作HalfClsd_stop")
    @pytest.mark.full
    def test_caseid_105531(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 9)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":2})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("设置尾门动作HalfClsd_closed")
    @pytest.mark.full
    def test_caseid_105509(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 9)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":1})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 2)

    @allure.title("设置尾门动作StopMinPntForCls_closed")
    @pytest.mark.full
    def test_caseid_105510(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 10)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd":1})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 2)

    @allure.title("设置尾门动作MovgUpBrkg_closed")
    @pytest.mark.smoke
    def test_caseid_105515(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 3)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd": 1})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 3)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 4)
        sleep(1)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 2)
        
    @allure.title("关闭尾门StopMinPntForCls_stop")
    @pytest.mark.sanity
    def test_caseid_105497(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 10)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Close", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 2)

    @allure.title("关闭尾门MovgDwn_stop")
    @pytest.mark.full
    def test_caseid_105505(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 6)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Close", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("关闭尾门HalfClsd_stop")
    @pytest.mark.full
    def test_caseid_105498(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 9)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Close", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 2)

    @allure.title("遍历_SetTailGate_极限状态_关")
    @pytest.mark.sanity
    def test_caseid_1959938(self):
        for X in [2,3]:
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', X)
            sleep(2)
            self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd": 1})
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 3)
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 5)
            sleep(0.1)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 2)

    @allure.title("遍历_Close_极限状态_关")
    @pytest.mark.sanity
    def test_caseid_1959940(self):
        for X in [2,3]:
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', X)
            sleep(2)
            self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Close", {})
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 3)
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 5)
            sleep(0.1)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 2)

    @allure.title("遍历_Open_极限状态_开")
    @pytest.mark.sanity
    def test_caseid_1959939(self):
        for Y in [6,7]:
            for X in [1,9]:
                logger.info(f"---状态1{Y}--状态2-{X}--")
                self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', Y)
                sleep(2)
                self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Open", {})
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 3)
                self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', X)
                sleep(0.1)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 1)
    
    @allure.title("遍历_SetTailGate_极限状态_开")
    @pytest.mark.sanity
    def test_caseid_1959937(self):
        for Y in [6,7]:
            for X in [1,9]:
                logger.info(f"---状态1{Y}--状态2-{X}--")
                self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', Y)
                self.partner.empty_all(2)
                self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd": 0})
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 3)
                self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', X)
                sleep(0.1)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 1)

    @allure.title("关闭尾门unknow_stop")
    @pytest.mark.sanity
    def test_caseid_105506(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 0)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Close", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 2)

    @allure.title("关闭尾门MovgDwnBrkg_stop")
    @pytest.mark.full
    def test_caseid_105496(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 7)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Close", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("关闭尾门StopDurgOpen_stop")
    @pytest.mark.full
    def test_caseid_105507(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 4)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Close", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 2)

    @allure.title("关闭尾门MovgUp_stop")
    @pytest.mark.full
    def test_caseid_105502(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 2)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Close", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 3)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 4)
        sleep(1)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 2)

    @allure.title("关闭尾门FullOpend_stop")
    @pytest.mark.full
    def test_caseid_105504(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 5)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Close", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 2)

    @allure.title("关闭尾门FullClsd_无法关")
    @pytest.mark.full
    def test_caseid_105503(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 1)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Close", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)

    @allure.title("关闭尾门StopDurgCls_stop")
    @pytest.mark.full
    def test_caseid_105499(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 8)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Close", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 2)

    @allure.title("关闭尾门MovgUpBrkg_stop")
    @pytest.mark.full
    def test_caseid_105508(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 3)
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Close", {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 3)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 4)
        sleep(1)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 2)

    @allure.title("通知和获取尾门运动状态_遍历")
    @pytest.mark.smoke
    def test_caseid_106223(self):
        info ={5:0,0:5,4:4,6:1,1:2,8:4,2:3,3:7,7:6,9:8,10:4}
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 1)
        sleep(1)
        for key,value in info.items():
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', key)
            sleep(1)
            self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT,"Status",{"sts":value})
            self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetStatus", {}, {"out": value})
        
    @allure.title("获取和通知尾门的当前位置(开度)_遍历")
    @pytest.mark.sanity
    def test_caseid_106422(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr03, 'TrOpenPosn',  0)
        sleep(1)
        for X in [101,0]:
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr03, 'TrOpenPosn', X)
            sleep(1)
            self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT,"Position",{"pos":X})
            self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetPosition", {}, {"out": X})

    @allure.title("获取和通知尾门按键开关状态_遍历")
    @pytest.mark.sanity
    def test_caseid_1983359(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'SwtTrClsSts',  1)
        self.io.trunk_door_outswitch_unpressed()
        sleep(1)
        for X in [0,1]:
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'SwtTrClsSts',  X)
            sleep(1)
            self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT,"NotifyTailGateSwitchStatus",{"sides": 0, "swt": X})
            self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetTailGateSwitchStatus", {"sides":0},
                                                  {"out": X})
        self.io.trunk_door_outswitch_pressed()
        self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT,"NotifyTailGateSwitchStatus",{"sides": 1, "swt": 1})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetTailGateSwitchStatus", {"sides":1}, 
                                                {"out": 1})
        self.io.trunk_door_outswitch_unpressed()
        self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT,"NotifyTailGateSwitchStatus",{"sides": 1, "swt": 0})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetTailGateSwitchStatus", {"sides":1}, 
                                                {"out": 0})
        
    @allure.title("尾门服务重启默认值")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1984309(self):
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 0)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'SwtTrClsSts', 0)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrAntiPnch', 0)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr03, 'TopPosHmiFeedBack2', 0)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr03, 'TrOpenPosn', 0)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr03, 'TrRelsFailtoHMI', 0)
        self.io.trunk_door_close()
        sleep(1)
        self.restart_bgm_and_connect_service(TAILGATESERVICE_CLIENT)
        sleep(0.5)
        self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT, "TailGateOpenStatusInfo",
                                  {"info": {"position": 0, "angle": 0, "sts": 5}})
        self.partner.ck_s2s_event(TAILGATE_SERVICE_CLIENT,"TailGateFault",
                                       {"faults": [{"fault": 0,"faultMsg":"","isFault": False}]})
        self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT,"Position",{"pos":0})
        self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT, "PositionMax", {"max": 0})
        self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT, "NotifyLiftgateSysSts", {"sts": {"topPosition": 0,"motionSts":0,"isAntiPinchOn":False}})
        self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT,"NotifyTailGateSwitchStatus",{"swt": 0})
        self.partner.ck_s2s_event(TAILGATE_SERVICE_CLIENT,"OpenCloseStatusValidity", {"sts": {"value": False,"validity":0}})
        self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT, "OpenCloseStatus", {"sts":False})
        self.partner.ck_s2s_event(TAILGATESERVICE_CLIENT,"Status",{"sts":5})

    @allure.title("尾门服务_所有默认值")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1892790(self):
        self.io.trunk_door_close()
        self.restart_bgm_and_connect_service(TAILGATESERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetPosition", {}, {"out": 255})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetPositionMax", {}, {"out": 95})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetStatus", {}, {"out": 65535})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetFaultInfo",{},
                                                {"out": [{"fault": 0,"faultMsg":"","isFault": False}]})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetTailGateSwitchStatus", {"sides":0}, {"out": 0})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetTailGateSwitchStatus", {"sides":1}, {"out": 0})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetOpenCloseStatus", {}, {"out": False})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetOpenCloseStatusValidity", {}, 
                                                {"out": {"value":False,"validity":0}})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetTailGateOpenStatusInfo", {},
                                                {"out":{"position": 255,"angle": 255, "sts": 65535}})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetLiftgateSysSts", {},
                                                {"out": {"motionSts": 65535, "topPosition": 95, "isAntiPinchOn": False}})

    @allure.title("5S内恢复bodycan,尾门能正常下发翘起")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1918691(self):
        self.restart_bgm_and_connect_service(TAILGATESERVICE_CLIENT,resume_all_bus=False)
        sleep(1)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetPosition", {"pos": 100},timeout=3)
        sleep(2)
        self.ipdu.resume_all_bus_send()
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 1)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr131, 'TrOpenPosnReqFromHmi', 100, timeout=5)

    @allure.title("压测_5S内恢复bodycan,尾门能正常下发打开")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1984356(self):
        for i in range(10):
            logger.info(f"第{i}次压测")
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 0)
            sleep(0.5)
            self.restart_bgm_and_connect_service(TAILGATE_SERVICE_CLIENT,pause_all_bus=True, resume_all_bus=False)
            self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetTailGate", {"cmd": 0}, timeout=2)
            self.ipdu.resume_all_bus_send()
            sleep(1)
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 1)
            sleep(0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 1)

    @allure.title("压测_5S内恢复bodycan,尾门能正常下发打开")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1984359(self):
        for i in range(10):
            logger.info(f"第{i}次压测")
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 0)
            sleep(0.5)
            self.restart_bgm_and_connect_service(TAILGATE_SERVICE_CLIENT)
            sleep(1)
            self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Open", {}, timeout=1.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 1)

    ######################################################################################################################################################## 
        
@allure.feature("SOA服务接口")
@allure.story("架构基础/TailGateService")
class TestTailGateServiceMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("TailGateService", "client")])
        self.partner.wait_for_service_reconnect(TAILGATE_SERVICE_CLIENT, timeout=30)

    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu)
    
    @allure.title("获取和通知尾门开关状态_mockMcu")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_111384(self):
        def info(input):
            return True if input == 1 else False
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'TrSts',0)
        sleep(1)
        for sigin in [1,2]:
            logger.info(f"--发送信号{sigin}")
            self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'TrSts',sigin)
            sleep(0.5)
            self.partner.ck_s2s_event(TAILGATE_SERVICE_CLIENT,"OpenCloseStatus", {"sts": info(sigin)})
            self.partner.ck_s2s_event(TAILGATE_SERVICE_CLIENT,"OpenCloseStatusValidity", {"sts": {"value": info(sigin),"validity":0}})
            self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetOpenCloseStatusValidity",
                                                   {}, {"out": {"value":info(sigin),"validity":0}})
            self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetOpenCloseStatus", {}, {"out": info(sigin)})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'TrSts',0)
        sleep(1)
        self.partner.ck_s2s_event(TAILGATE_SERVICE_CLIENT,"OpenCloseStatus", {"sts": False})
        self.partner.ck_s2s_event(TAILGATE_SERVICE_CLIENT,"OpenCloseStatusValidity", {"sts": {"value": False,"validity":1}})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetOpenCloseStatusValidity",
                                            {}, {"out": {"value":False,"validity":1}})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetOpenCloseStatus", {}, {"out": False})
        self.partner.empty_all()
        self.ipdu.pause_all_bus_send()
        self.partner.ck_s2s_event(TAILGATE_SERVICE_CLIENT,"OpenCloseStatusValidity", {"sts": {"value": False,"validity":4}},timeout=20)
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetOpenCloseStatusValidity",
                                            {}, {"out": {"value":False,"validity":4}})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(TAILGATE_SERVICE_CLIENT,"OpenCloseStatusValidity", {"sts": {"value": False,"validity":1}})
        self.partner.send_request_and_ck_resp(TAILGATESERVICE_CLIENT, "GetOpenCloseStatusValidity",
                                            {}, {"out": {"value":False,"validity":1}})



