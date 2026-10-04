#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_WTIService_Light.py
@Time         :2023/10/26 17:20:31
@Author       :peipei.yang_ext@jiduauto.com
@Description  :
"""
import random
import time

import allure
import pytest
import copy
from time import sleep
from random import randint
from xat_ecu.legacy.common.data_type_handing import logger
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.soa.case_helper.test_base import TestBase, s2s_path, write_s2s_json
from xat_cases.legacy.soa.case_helper.utils import ck_pdu_period_time
from xat_ecu.legacy.interface.bgm.bgm_env.change_bgm_env import change_bgm_config, recover_bgm_config


@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIService_Light")
@pytest.mark.ypp
class TestLightWTIService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("WTIService", "client"),
                                     ("LightService", "client"),
                                     ("AutoHighBeamControlService", "server")])
        self.partner.method_default_timeout = 0.1

        self.ipdu.send_pdu('chassiscan1', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('chassiscan2', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('propulsioncan', 0x516, [0x16, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.sd_tester.tester_present()
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'EntityKeyWhiteListVers', self.dk.last_sync_time_entity)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BLESlotKeyWhiteListVers', self.dk.last_sync_time_ble)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr29, 'DCChrgnHndlSts', 'OnBdChrgrHndlSts_ConnectedWithPower') # lin唤醒
        self.ipdu.set(self.ipdu.connectivitycanfd.TcamConnectivityFr12, 'RemHvStrtActvReq', 'OnOffNoReq_On')
        self.ipdu.set(self.ipdu.connectivitycanfd.TcamConnectivityFr12, 'RemDCChrgLidTelmReq', 'OnOffNoReq_On')
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForFlt', 0)
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        # self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.ipdu.set_vehspd(0)
        sleep(1)
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.sd_tester.stop_tester_present()
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu, start=False)

    def ck_no_specific_event_and_GetWarningMsgList(self, hint, info, timeout=1):
        """校验无指定warningMsgList事件,并请求WarningMsgList获取结果"""
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})

    def ck_WarningMsgList_and_GetWarningMsgList(self, hint, info, timeout=3):
        """校验指定warningMsgList事件,并请求WarningMsgList获取结果"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint, "info": str(info)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})

    def ck_no_specific_event_and_GetTelltaleList(self, hint, state, timeout=1):
        """校验无指定warningMsgList事件,并请求WarningMsgList获取结果"""
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "TelltaleList", hint, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": hint, "state": str(state)}]})

    def ck_TelltaleList_and_GetTelltaleList(self, hint, state, timeout=3):
        """校验指定TelltaleList事件，并请求TelltaleList获取结果"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                  {"list": [{"name": hint, "state": str(state)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": hint, "state": str(state)}]})

    @allure.title("近光指示灯 (TelltaleLightLB)")
    @pytest.mark.smoke
    def test_caseid_108227(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 0})
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedLoBeamLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedLoBeamRi', 0)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedLoBeamLe', 1)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedLoBeamRi', 1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList", {"list": [{'name': 'LB', 'state': '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{'name': 'LB', 'state': '1'}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 0})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList", {"list": [{'name': 'LB', 'state': '0'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{'name': 'LB', 'state': '0'}]})

    @allure.title("自动远光灰色指示灯(TelltaleLightAutoHBGrey)")
    @pytest.mark.full
    @pytest.mark.YPP1
    def test_caseid_1983340(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})  # 设置外灯模式
        self.partner.send_event_notify(AUTOHIGHBEAMCONTROL_SERVICE_SERVER, "NotifyAHBCFunctionSts",
                                       {"allAHBCFunctionSts": {"switchSts": 2, "faultSts": 0,
                                                               "glareTelltale": False}})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                  {"list": [{"name": "AHB Grey", "state": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": "AHB Grey", "state": "1"}]})
        self.partner.send_event_notify(AUTOHIGHBEAMCONTROL_SERVICE_SERVER, "NotifyAHBCFunctionSts",
                                       {"allAHBCFunctionSts": {"switchSts": 0, "faultSts": 0,
                                                               "glareTelltale": False}})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                  {"list": [{'name': 'AHB Grey', 'state': 0}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{'name': 'AHB Grey', 'state': 0}]})

    @allure.title("自动远光蓝色指示灯(TelltaleLightAutoHBGrey)")
    @pytest.mark.sanity
    @pytest.mark.YPP1
    def test_caseid_107145(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})  # 设置外灯模式
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedLoBeamLe', 1)  # 发送信号，设置远光灯打开
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedLoBeamRi', 1)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamContro",
                                         {"info": {"cmd": 0, "clientId": 1}})  # 调用灯服务，设置远光灯关闭
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamContro",
                                         {"info": {"cmd": 255, "clientId": 1}})  # 释放远光优先级
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', 0)
        self.partner.send_event_notify(AUTOHIGHBEAMCONTROL_SERVICE_SERVER, "NotifyAHBCFunctionSts",
                                       {"allAHBCFunctionSts": {"switchSts": 0, "faultSts": 0,
                                                               "glareTelltale": False}})
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', 1)  # 发送信号，设置远光灯打开
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', 1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                         {"info": {"cmd": 2, "clientId": 5}}, timeout=0.5)  # 激活远光灯
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', 1)  # 检
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                  {'list': [{'name': 'HB', 'state': 1}]})  # WTI通知远光灯远光
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{'name': 'HB', 'state': 1}]})  # 检查远光灯状
        # 自动远光蓝色指示灯打开
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', 1)
        sleep(0.5)
        self.partner.send_event_notify(AUTOHIGHBEAMCONTROL_SERVICE_SERVER, "NotifyAHBCFunctionSts",
                                       {"allAHBCFunctionSts": {"switchSts": 3, "faultSts": 0,
                                                               "glareTelltale": False}})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', 1)  #
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                  {"list": [{"name": "AHB Blue", "state": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": "AHB Blue", "state": "1"}]})
        # 自动远光蓝色(点亮到熄灭)
        self.partner.send_event_notify(AUTOHIGHBEAMCONTROL_SERVICE_SERVER, "NotifyAHBCFunctionSts",
                                       {"allAHBCFunctionSts": {"switchSts": 0, "faultSts": 0,
                                                               "glareTelltale": False}})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', 1)  #
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                  {"list": [{'name': 'AHB Blue', 'state': 0}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{'name': 'AHB Blue', 'state': 0}]})

    @allure.title("后雾灯指示灯(TelltaleLightPO)")
    @pytest.mark.smoke
    def test_caseid_108505(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReFogLampLe1', 1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 4, "zoneId": 10}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReFogLampLe1', 1)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{'name': 'Rear Fog', 'state': '1'}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                  {"list": [{'name': 'Rear Fog', 'state': '1'}]})
        # 设置后雾灯关闭
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                         {"lights": [{"light": {"type": 4, "zoneId": 10},
                                                      "mode": 0, "brightness": 0,
                                                      "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{'name': 'Rear Fog', 'state': '0'}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                  {"list": [{'name': 'Rear Fog', 'state': '0'}]})

    @allure.title("大灯高度调节电机故障信息（MsgLightLevelingMotor)")
    @pytest.mark.sanity
    def test_caseid_1983339(self):
        hint = "Leveling Motor"
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLvlgLeStsOfLvlgLe', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLvlgLeStsOfLvlgLe', 2)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        sleep(1)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLvlgLeStsOfLvlgLe', 1)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @allure.title("近光灯故障提示信息(MsgLBFailure)")
    @pytest.mark.sanity
    def test_caseid_108453(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 0})
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedLoBeamLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedLoBeamRi', 0)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedLoBeamLe', 2)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedLoBeamRi', 2)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{'name': 'LB Failure', 'info': '1'}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{'name': 'LB Failure', 'info': '1'}]})
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedLoBeamLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedLoBeamRi', 0)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{'name': 'LB Failure', 'info': '0'}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{'name': 'LB Failure', 'info': '0'}]})

    @allure.title("远光灯故障提示信息(MsgHBFailure)")
    @pytest.mark.sanity
    def test_caseid_107146(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)  # 设置外灯模式
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})  # 设置外灯模式
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', 1)  # 发送信号，设置远光灯打开
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', 1)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamContro",
                                         {"info": {"cmd": 0, "clientId": 1}})  # 调用灯服务，设置远光灯关闭
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamContro",
                                         {"info": {"cmd": 255, "clientId": 1}})  # 释放远光优先级
        self.partner.send_event_notify(AUTOHIGHBEAMCONTROL_SERVICE_SERVER, "allAHBCFunctionSts",
                                       {"switchSts": 0, "faultSts": 0, "glareTelltale": False})  # 发送evente
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                         {"info": {"cmd": 2, "clientId": 5}}, timeout=0.5)  # 激活远光灯

        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', 2)  # 发送信号，设置远光灯打开
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', 2)

        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {'list': [{'name': 'HB Failure', 'info': 1}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{'name': 'HB Failure', 'info': 1}]})
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', 1)  # 发送信号，设置远光灯打开
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', 1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {'list': [{'name': 'HB Failure', 'info': 0}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{'name': 'HB Failure', 'info': 0}]})

    @allure.title("超车灯故障提示信息(MsgOvertakeLightFailure)")
    @pytest.mark.sanity
    def test_caseid_108413(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)  # 设置外灯模式
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})  # 设置外灯模式
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', 1)  # 发送信号，设置远光灯打开
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', 1)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamContro",
                                         {"info": {"cmd": 0, "clientId": 1}})  # 调用灯服务，设置远光灯关闭
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamContro",
                                         {"info": {"cmd": 255, "clientId": 1}})  # 释放远光优先级
        self.partner.send_event_notify(AUTOHIGHBEAMCONTROL_SERVICE_SERVER, "allAHBCFunctionSts",
                                       {"switchSts": 0, "faultSts": 0, "glareTelltale": False})  # 发送evente
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                         {"info": {"cmd": 1, "clientId": 5}}, timeout=0.5)  # 激活远光灯

        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', 2)  # 发送信号，设置远光灯打开
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', 2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFlash', 2)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {'list': [{'name': 'Overtake Light Failure', 'info': 1}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{'name': 'Overtake Light Failure', 'info': 1}]})

        sleep(10)
        # self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', 1)  # 发送信号，设置远光灯打开
        # self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', 1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {'list': [{'name': 'Overtake Light Failure', 'info': 0}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{'name': 'Overtake Light Failure', 'info': 0}]})

    @allure.title("倒车灯故障提示信息(MsgReverseLightFailure)")
    @pytest.mark.sanity
    def test_caseid_108464(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr10, 'DrvrDesDirDrvrDesDir', 2)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedRvsgLampRi1', 2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', 2)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {'list': [{'name': 'Reverse Light Failure', 'info': 1}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{'name': 'Reverse Light Failure', 'info': 1}]})
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr10, 'DrvrDesDirDrvrDesDir', 2)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedRvsgLampRi1', 1)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', 1)

        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {'list': [{'name': 'Reverse Light Failure', 'info': 0}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{'name': 'Reverse Light Failure', 'info': 0}]})

    @allure.title("位置灯故障提示信息(MsgPOFailure)")
    @pytest.mark.sanity
    def test_caseid_108322(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 1})
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLedFrntPosnLampLe', 2)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedPosnLampLe1', 2)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{'name': 'PO Failure', 'info': '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{'name': 'PO Failure', 'info': '1'}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 0})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{'name': 'PO Failure', 'info': '0'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{'name': 'PO Failure', 'info': '0'}]})

    @allure.title("后雾灯故障提示信息(MsgRearFogFailure)")
    @pytest.mark.sanity
    def test_caseid_107148(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReFogLampLe1', 1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                         {"lights": [{"light": {"type": 4, "zoneId": 10},
                                                      "mode": 1, "brightness": 0,
                                                      "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})

        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReFogLampLe1', 2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 2)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, 'LightFault',
                                         {"faults": [
                                             {"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 0}}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{'name': 'Rear Fog Failure', 'info': '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{'name': 'Rear Fog Failure', 'info': '1'}]})
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReFogLampLe1', 1)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, 'LightFault',
                                         {"faults": [
                                             {"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 0}}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{'name': 'Rear Fog Failure', 'info': '0'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{'name': 'Rear Fog Failure', 'info': '0'}]})

    @allure.title("左转向灯故障提示信息(MsgLeftTIFailure)")
    @pytest.mark.sanity
    def test_caseid_107150(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 47}})
        sleep(0.2)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 255}})
        sleep(0.2)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLedFrntTurnIndcrLe', 2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 2)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {'list': [{'name': 'Left TI Failure', 'info': 1}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{'name': 'Left TI Failure', 'info': 1}]})

        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLedFrntTurnIndcrLe', 1)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {'list': [{'name': 'Left TI Failure', 'info': 0}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{'name': 'Left TI Failure', 'info': 0}]})

    @allure.title("HDC陡坡缓降指示灯灰色(TelltaleHDCGrey)_模式满足+信号置0恢复")
    @pytest.mark.full
    def test_caseid_1903621(self):
        for usage_mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', 0)
            self.partner.empty_all(0.5)
            hint = "HDC Grey"
            for sts in [1, 0, 1, 4, 1, 5, 1, 6, 1, 7]:
                sleep(0.5)
                logger.info(f"打印信号: {sts}")
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', sts)
                self.ck_TelltaleList_and_GetTelltaleList(hint, 1 if sts == 1 else 0)
    
    @allure.title("获取HDC陡坡缓降指示灯灰色&通知HDC陡坡缓降指示灯灰色_2/11/13-0")
    @pytest.mark.full
    def test_caseid_1983957(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', 0)
        self.partner.empty_all(0.5)
        hint = "HDC Grey"
        for usage_mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', 1)
            sleep(0.5)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
            self.sd_tester.change_usage_mode(0)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
    
    @allure.title("获取HDC陡坡缓降指示灯灰色&通知HDC陡坡缓降指示灯灰色_2/11/13-1")
    @pytest.mark.full
    def test_caseid_1983958(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', 0)
        self.partner.empty_all(0.5)
        hint = "HDC Grey"
        for usage_mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', 1)
            sleep(0.5)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
            self.sd_tester.change_usage_mode(1)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
    
    @allure.title("获取HDC陡坡缓降指示灯绿色&通知HDC陡坡缓降指示灯绿色_模式满足+信号置0恢复")
    @pytest.mark.full
    def test_caseid_1983959(self):
        for usage_mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', 0)
            self.partner.empty_all(0.5)
            hint = "HDC Green"
            for sts in [2, 0, 2, 4, 2, 5, 2, 6, 2, 7]:
                logger.info(f"sts: {sts}")
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', sts)
                self.ck_TelltaleList_and_GetTelltaleList(hint, 1 if sts == 2 else 0)
    
    @allure.title("获取HDC陡坡缓降指示灯绿色&通知HDC陡坡缓降指示灯绿色_2/11/13-0")
    @pytest.mark.full
    def test_caseid_1983960(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', 0)
        self.partner.empty_all(0.5)
        hint = "HDC Green"
        for usage_mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', 2)
            sleep(0.5)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
            self.sd_tester.change_usage_mode(0)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
    
    @allure.title("获取HDC陡坡缓降指示灯绿色&通知HDC陡坡缓降指示灯绿色_2/11/13-1")
    @pytest.mark.full
    def test_caseid_1983961(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', 0)
        self.partner.empty_all(0.5)
        hint = "HDC Green"
        for usage_mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', 2)
            sleep(0.5)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
            self.sd_tester.change_usage_mode(1)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
    
    @allure.title("获取HDC陡坡缓降指示灯黄色&通知HDC陡坡缓降指示灯黄色_模式满足+信号置0恢复")
    @pytest.mark.sanity
    def test_caseid_1983963(self):
        for usage_mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', 0)
            self.partner.empty_all(0.5)
            hint = "HDC Yellow"
            for sts in [3, 0, 3, 4, 3, 5, 3, 6, 3, 7]:
                logger.info(f"sts: {sts}")
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', sts)
                self.ck_TelltaleList_and_GetTelltaleList(hint, 1 if sts == 3 else 0)
    
    @allure.title("获取HDC陡坡缓降指示灯绿色&通知HDC陡坡缓降指示灯绿色_2/11/13-0")
    @pytest.mark.full
    def test_caseid_1983964(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', 0)
        self.partner.empty_all(0.5)
        hint = "HDC Yellow"
        for usage_mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', 3)
            sleep(0.5)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
            self.sd_tester.change_usage_mode(0)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
    
    @allure.title("获取HDC陡坡缓降指示灯绿色&通知HDC陡坡缓降指示灯绿色_2/11/13-1")
    @pytest.mark.full
    def test_caseid_1983965(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', 0)
        self.partner.empty_all(0.5)
        hint = "HDC Yellow"
        for usage_mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', 3)
            sleep(0.5)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
            self.sd_tester.change_usage_mode(1)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
    
    @allure.title(" 获取转向系统故障指示灯黄色&通知转向系统故障指示灯黄色_故障到恢复")
    @pytest.mark.sanity
    def test_caseid_111467(self):
        hint = "Yellow Steering Failed"
        for usage_mode in [11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
            self.partner.empty_all(0.5)
            for sts in [1, 0, 3, 5, 4, 6, 1, 7]:
                logger.info(f"sts: {sts}")
                self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', sts)
                if sts in [1, 3, 4]:
                    self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
                else:
                    self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
    
    @allure.title("获取转向系统故障指示灯黄色&通知转向系统故障指示灯黄色_模式切换")
    @pytest.mark.full
    def test_caseid_1983966(self):
        hint = "Yellow Steering Failed"
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 1)
        sleep(3)
        self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
        self.sd_tester.change_usage_mode(0)
        self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 3)
        sleep(3)
        self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
        self.sd_tester.change_usage_mode(1)
        self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 3)
        sleep(3)
        self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
        self.sd_tester.change_usage_mode(2)
        self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
    
    @allure.title("转向系统故障指示灯黄色(TelltaleSteeringSysFailedYellow _信号丢失)")
    @pytest.mark.full
    def test_caseid_1983967(self):
        hint = "Yellow Steering Failed"
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.partner.empty_all(0.5)
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 6)
        sleep(0.5)
        self.ipdu.pause_bus_send("chassiscan1")
        sleep(5)
        self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
        self.ipdu.resume_bus_send("chassiscan1")
        sleep(0.5)
        self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                      {"out": [{"name": "Yellow Steering Failed", "state": "0"}]})
    
    @allure.title("转向系统故障指示灯黄色(TelltaleSteeringSysFailedYellow _信号丢失_没有event)")
    @pytest.mark.full
    def test_caseid_1983968(self):
        hint = "Yellow Steering Failed"
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.partner.empty_all(0.5)
        self.sd_tester.change_usage_mode(11)
        for sts in[1, 3, 4]:
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', sts)
            sleep(0.5)
            self.ipdu.pause_bus_send("chassiscan1")
            sleep(5)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                      {"out": [{"name": "Yellow Steering Failed", "state": "1"}]})
            self.ipdu.resume_bus_send("chassiscan1")
            sleep(0.5)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                      {"out": [{"name": "Yellow Steering Failed", "state": "1"}]})
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
    
    @allure.title(" 获取转向系统故障指示灯红色&通知转向系统故障指示灯红色_故障到恢复")
    @pytest.mark.full
    def test_caseid_111472(self):
        hint = "Red Steering Failed"
        for usage_mode in [11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
            self.partner.empty_all(0.5)
            for sts in [2, 0, 2, 5, 2, 6, 2, 7]:
                logger.info(f"sts: {sts}")
                self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', sts)
                if sts in [2]:
                    self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
                else:
                    self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
    
    @allure.title("获取转向系统故障指示灯红色&通知转向系统故障指示灯红色_模式切换")
    @pytest.mark.full
    def test_caseid_1960025(self):
        hint = "Red Steering Failed"
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.partner.empty_all(0.5)
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 2)
        sleep(3)
        self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
        self.sd_tester.change_usage_mode(0)
        self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 2)
        sleep(3)
        self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
        self.sd_tester.change_usage_mode(1)
        self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 2)
        sleep(3)
        self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
        self.sd_tester.change_usage_mode(2)
        self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
    
    @allure.title("获取转向系统故障指示灯红色&通知转向系统故障指示灯红色_信号丢失_没有event")
    @pytest.mark.full
    def test_caseid_1979816(self):
        hint = "Red Steering Failed"
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.partner.empty_all(0.5)
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 2)
        sleep(0.5)
        self.ipdu.pause_bus_send("chassiscan1")
        sleep(5)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                          {'list': [{"name": "Red Steering Failed", "state": "0"},
                                                    {'name': 'Yellow Steering Failed', "state": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                    {"out": [{"name": "Red Steering Failed", "state": "0"},
                                                             {"name": "Yellow Steering Failed", "state": "1"}]})
        self.ipdu.resume_bus_send("chassiscan1")
        sleep(0.5)
        self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                    {"out": [{"name": "Red Steering Failed", "state": "1"}]})
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
    
    @allure.title("获取行人保护装置故障指示灯&通知行人保护装置故障指示灯_UsgMod=2/11/13")
    @pytest.mark.sanity
    def test_caseid_1985212(self):
        hint = "Pedestrian Protection Error"
        for usage_mode in [2, 11, 13]:
            logger.info(f"打印模式: {usage_mode}")
            self.sd_tester.change_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForFlt', 2)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForFlt', 1)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 0)

    @allure.title("获取行人保护装置故障指示灯&通知行人保护装置故障指示灯_UsgMod=0/1")
    @pytest.mark.full
    def test_caseid_1985213(self):
        hint = "Pedestrian Protection Error"
        for usage_mode in [0, 1]:
            logger.info(f"打印模式: {usage_mode}")
            self.sd_tester.change_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForFlt', 2)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                    {"out": [{"name": "Pedestrian Protection Error", "state": "0"}]})
    
    @allure.title("获取行人保护装置故障指示灯&通知行人保护装置故障指示灯_UsgMod=2/11/13")
    @pytest.mark.full
    def test_caseid_1985214(self):
        hint = "Pedestrian Protection Error"
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForFlt', 2)
        for i in [2, 11, 13]:
            logger.info(f"打印模式: {i}")
            for j in [0, 1]:
                logger.info(f"打印模式: {j}")
                self.sd_tester.change_usage_mode(i)
                self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
                self.sd_tester.change_usage_mode(j)
                self.ck_TelltaleList_and_GetTelltaleList(hint, 0)

    
@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIService_Light")
@pytest.mark.ypp
class TestLightWTIServiceMockMcu(TestBase):

    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([WTI_SERVICE_CLIENT, LIGHT_SERVICE_CLIENT])

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
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu)

    def set_usage_mode(self, mode):
        """通过模拟mcu cdd打包总线数据来输入usage mode给到S2S"""
        logger.info(f"设置usage mode: {mode}")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', mode)
    
    def ck_no_specific_event_and_GetWarningMsgList(self, hint, info, timeout=1):
        """校验无指定warningMsgList事件,并请求WarningMsgList获取结果"""
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})

    def ck_WarningMsgList_and_GetWarningMsgList(self, hint, info, timeout=3):
        """校验指定warningMsgList事件,并请求WarningMsgList获取结果"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint, "info": str(info)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})
    
    def ck_no_specific_event_and_GetTelltaleList(self, hint, state, timeout=1):
        """校验无指定warningMsgList事件,并请求WarningMsgList获取结果"""
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "TelltaleList", hint, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": hint, "state": str(state)}]})

    def ck_TelltaleList_and_GetTelltaleList(self, hint, state, timeout=3):
        """校验指定TelltaleList事件,并请求TelltaleList获取结果"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                  {"list": [{"name": hint, "state": str(state)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": hint, "state": str(state)}]})

    @allure.title("远光指示灯(TelltaleLightHB)_单独一个信号")
    @pytest.mark.smoke
    def test_caseid_108219(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFlash', 0)
        self.partner.empty_all(0.5)
        for beam in [1, 2, 1, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', beam)
            sleep(0.5)
            if beam in [1]:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                        {"list": [{'name': 'HB', 'state': 1}]})  # WTI通知远光灯远光打开
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                    {"out": [{'name': 'HB', 'state': 1}]})
            else:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                        {"list": [{'name': 'HB', 'state': 0}]})  # WTI通知远光灯远光关闭
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                    {"out": [{'name': 'HB', 'state': 0}]})
        for flash in [1, 2, 1, 3, 1, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFlash', flash)
            sleep(0.5)
            if flash in [1]:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                        {"list": [{'name': 'HB', 'state': 1}]})  # WTI通知远光灯远光打开
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                    {"out": [{'name': 'HB', 'state': 1}]})
            else:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                        {"list": [{'name': 'HB', 'state': 0}]})  # WTI通知远光灯远光关闭
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                    {"out": [{'name': 'HB', 'state': 0}]})
    
    @allure.title("远光指示灯(TelltaleLightHB)_两个信号同时置位")
    @pytest.mark.full
    def test_caseid_1983945(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFlash', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', 1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFlash', 1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                        {"list": [{'name': 'HB', 'state': 1}]})  # WTI通知远光灯远光打开
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                    {"out": [{'name': 'HB', 'state': 1}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFlash', 0)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                        {"list": [{'name': 'HB', 'state': 0}]})  # WTI通知远光灯远光关闭
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                    {"out": [{'name': 'HB', 'state': 0}]})
    
    @allure.title("位置灯指示灯(TelltaleLightPO)_单独一个信号")
    @pytest.mark.smoke
    def test_caseid_108333(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe', 0)
        self.partner.empty_all(0.5)
        for LiFrnt in [1, 2, 1, 3, 1, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', LiFrnt)
            sleep(0.5)
            if LiFrnt in [1]:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList", 
                                          {"list": [{'name': 'PO', 'state': '1'}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                    {"out": [{'name': 'PO', 'state': '1'}]})
            else:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList", 
                                          {"list": [{'name': 'PO', 'state': '0'}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                    {"out": [{'name': 'PO', 'state': '0'}]})
        for LiRe in [1, 2, 1, 3, 1, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe', LiRe)
            sleep(0.5)
            if LiRe in [1]:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList", 
                                          {"list": [{'name': 'PO', 'state': '1'}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                    {"out": [{'name': 'PO', 'state': '1'}]})
            else:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList", 
                                          {"list": [{'name': 'PO', 'state': '0'}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                    {"out": [{'name': 'PO', 'state': '0'}]})
    
    @allure.title("位置灯指示灯(TelltaleLightPO)_两个信号同时置位")
    @pytest.mark.full
    def test_caseid_1983946(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', 1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe', 1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList", 
                                          {"list": [{'name': 'PO', 'state': '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                    {"out": [{'name': 'PO', 'state': '1'}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe', 0)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList", 
                                          {"list": [{'name': 'PO', 'state': '0'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                    {"out": [{'name': 'PO', 'state': '0'}]})
    
    @allure.title("后雾灯与近光灯联动关闭提示(MsgRearFogAndLowBeamOff_后雾灯开启——近光灯从开启到关闭显示信息)V1.3 ")# 超时故障恢复
    @pytest.mark.full
    def test_caseid_1943281(self):
        hint = "Rear Fog And Low Beam Off"
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 1)  # 后雾灯
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', 1)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', 0)#近光灯开启到关闭
        sleep(0.5)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        sleep(4)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)  

    @allure.title("后雾灯与近光灯联动关闭提示(MsgRearFogAndLowBeamOff——后雾灯开启——近光灯从开启到关闭显示信息)V1.3 ")# 近光灯打开提示消失
    @pytest.mark.full
    def test_caseid_1943282(self):
        hint = "Rear Fog And Low Beam Off"
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 1)  # 后雾灯
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', 1)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', 0)#近光灯开启到关闭
        sleep(0.5)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', 1)
        sleep(1)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)  

    @allure.title("后雾灯与近光灯联动关闭提示(MsgRearFogAndLowBeamOff)V1.3 ")#flag=1& 超时故障恢复
    @pytest.mark.full
    def test_caseid_1943283(self):
        hint = "Rear Fog And Low Beam Off"
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 1)  # 后雾灯
        sleep(0.1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 0)  # 后雾灯
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', 1)
        sleep(0.1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', 0)#近光灯开启到关闭
        sleep(0.5)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        sleep(4)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0) 

    @allure.title("后雾灯与近光灯联动关闭提示(MsgRearFogAndLowBeamOff)V1.3 ")#flag=1& 近光灯打开
    @pytest.mark.full
    def test_caseid_1943284(self):
        hint = "Rear Fog And Low Beam Off"
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 1)  # 后雾灯
        sleep(0.1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 0)  # 后雾灯
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', 1)
        sleep(0.1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', 0)#近光灯开启到关闭
        sleep(0.5)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', 1)#近光灯开启
        sleep(0.2)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0) 

    @allure.title("后雾灯与近光灯联动关闭提示(MsgRearFogAndLowBeamOff)V1.4 ")#flag=1& #flag=0(=0时不做处理)
    @pytest.mark.full
    def test_caseid_1982551(self):
        hint = "Rear Fog And Low Beam Off"
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 1)  # 后雾灯
        sleep(0.05)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 0)  # 后雾灯
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', 1)
        sleep(0.05)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', 0)#近光灯开启到关闭
        sleep(0.1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 1)
        sleep(0.05)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', 0)#近光灯开启
        sleep(4)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0) 
    
    @allure.title("右转向灯故障提示信息(MsgRightTIFailure)")
    @pytest.mark.sanity
    def test_caseid_107149(self):
        for IndrRi in [2, 1, 2, 0]:
            logger.info(f"发送信号: {IndrRi}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', IndrRi)  # 右转向
            if IndrRi in [2]:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                        {'list': [{'name': 'Right TI Failure', 'info': 1}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                    {"out": [{'name': 'Right TI Failure', 'info': 1}]})
            else:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                        {'list': [{'name': 'Right TI Failure', 'info': 0}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                    {"out": [{'name': 'Right TI Failure', 'info': 0}]})

    def set_light_fault_combine(self, fault=False):
        value = 2 if fault else random.randint(0, 1)
        logger.info(f"Fault value: {value}")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsAHL', value)         #大灯高度调节电机故障
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', value)      #近光灯故障
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', value)      #远光灯故障
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFlash', value)       #超车灯故障
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', value)   #倒车灯故障
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', value)   #位置灯故障
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', value)       #后雾灯故障
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', value)  #左转向灯故障
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', value)  #右转向灯故障
        sleep(0.2)

    @allure.title("灯故障提示信息组合测试")
    @pytest.mark.full
    def test_caseid_1988216(self):
        self.set_light_fault_combine(fault=False)
        self.set_light_fault_combine(fault=True)

        self.partner.ck_wti_warning_and_resp('Leveling Motor', 1)
        self.partner.ck_wti_warning_and_resp('LB Failure', 1)
        self.partner.ck_wti_warning_and_resp('HB Failure', 1)
        self.partner.ck_wti_warning_and_resp('Overtake Light Failure', 1)
        self.partner.ck_wti_warning_and_resp('Reverse Light Failure', 1)
        self.partner.ck_wti_warning_and_resp('PO Failure', 1)
        self.partner.ck_wti_warning_and_resp('Rear Fog Failure', 1)
        self.partner.ck_wti_warning_and_resp('Left TI Failure', 1)
        self.partner.ck_wti_warning_and_resp('Right TI Failure', 1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", {"faults": 
                                   [{"fault": 1, "faultMsg": "", "light": {"type": 37,"zoneId": 0}},
                                    {"fault": 1, "faultMsg": "", "light": {"type": 6,"zoneId": 0}},
                                    {"fault": 1, "faultMsg": "", "light": {"type": 5,"zoneId": 0}},
                                    {"fault": 1, "faultMsg": "", "light": {"type": 32,"zoneId": 0}},
                                    {"fault": 1, "faultMsg": "", "light": {"type": 8,"zoneId": 0}},
                                    {"fault": 1, "faultMsg": "", "light": {"type": 11,"zoneId": 9}},
                                    {"fault": 1, "faultMsg": "", "light": {"type": 4,"zoneId": 10}},
                                    {"fault": 1, "faultMsg": "", "light": {"type": 10,"zoneId": 12}},
                                    {"fault": 1, "faultMsg": "", "light": {"type": 10,"zoneId": 13}}]}, timeout=5)
        
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": 
                                   [{"fault": 1, "faultMsg": "", "light": {"type": 37, "zoneId": 0}},
                                    {"fault": 1, "faultMsg": "", "light": {"type": 6, "zoneId": 0}},
                                    {"fault": 1, "faultMsg": "", "light": {"type": 5, "zoneId": 0}},
                                    {"fault": 1, "faultMsg": "", "light": {"type": 32, "zoneId": 0}},
                                    {"fault": 1, "faultMsg": "", "light": {"type": 8, "zoneId": 0}},
                                    {"fault": 1, "faultMsg": "", "light": {"type": 11, "zoneId": 9}},
                                    {"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 10}},
                                    {"fault": 1, "faultMsg": "", "light": {"type": 10, "zoneId": 12}},
                                    {"fault": 1, "faultMsg": "", "light": {"type": 10, "zoneId": 13}}]}, timeout=5)

        self.set_light_fault_combine(fault=False)

        self.partner.ck_wti_warning_and_resp('Leveling Motor', 0)
        self.partner.ck_wti_warning_and_resp('LB Failure', 0)
        self.partner.ck_wti_warning_and_resp('HB Failure', 0)
        self.partner.ck_wti_warning_and_resp('Overtake Light Failure', 0)
        self.partner.ck_wti_warning_and_resp('Reverse Light Failure', 0)
        self.partner.ck_wti_warning_and_resp('PO Failure', 0)
        self.partner.ck_wti_warning_and_resp('Rear Fog Failure', 0)
        self.partner.ck_wti_warning_and_resp('Left TI Failure', 0)
        self.partner.ck_wti_warning_and_resp('Right TI Failure', 0)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", {"faults": 
                                [{"fault": 0, "faultMsg": "", "light": {"type": 100,"zoneId": 0}}]}, timeout=5)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": 
                                [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]}, timeout=5)
