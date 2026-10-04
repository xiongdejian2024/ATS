#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_PassiveSafetyService.py
@Time         :2023/05/17 08:07:44
@Author       :peipei.yang_ext@jiduauto.com
@Description  :
"""
import allure
import pytest
from time import sleep
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("整车控制/PassiveSafetyService")
@pytest.mark.ypp
class TestPassiveSafetyService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("PassiveSafetyService", "client")])
        self.partner.method_default_timeout = 0.1

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashFrnt', 0)  # 前碰撞状态
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashRe', 0)  # 后碰撞状态
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashRollovr', 0)  # 倾翻状态
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashSideLe', 0)  # 左碰撞状态
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashSideRi', 0)  # 右碰撞状态
        
    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()  # 恢复所有总线
        super().after_each_func(ecu, start=False)

    def set_VehicleCrashStatus_signal(self, Frnt=0, Re=0, Rollovr=0, SideLe=0, SideRi=0):
        logger.info(f"设置信号---{Frnt,Re, Rollovr, SideLe, SideRi}")
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashFrnt', Frnt)  # 前碰撞状态
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashRe', Re)  # 后碰撞状态
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashRollovr', Rollovr)  # 倾翻状态
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashSideLe', SideLe)  # 左碰撞状态
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashSideRi', SideRi) # 右碰撞状态
    
    def set_AirbagWarning_signal(self, LampReq=0, MsgReq=0):
        logger.info(f"设置信号---{LampReq, MsgReq}")
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', LampReq)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', MsgReq)
        sleep(1)
    
    def set_PedestrianProtectionWarning_signal(self, Flt=0, Impct=0):
        logger.info(f"设置信号---{Flt, Impct}")
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForFlt', Flt)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForImpct', Impct)
        sleep(1)
    
    @allure.title("获取安全气囊系统(乘员保护系统)报警信息&通知安全气囊系统(乘员保护系统)报警信息_默认值")
    @pytest.mark.full
    def test_caseid_1983350(self):
        for usage_mode in [0, 1, 2]:
            logger.info(f"打印{usage_mode}")
            self.sd_tester.change_usage_mode(usage_mode)
            for sts in [1, 0]:
                self.set_AirbagWarning_signal(sts, sts)
                self.partner.empty_all(0.5)
                self.restart_bgm_and_connect_service(PASSIVESAFETY_SERVICE_CLIENT, resume_all_bus=False)   
                self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetAirbagWarning", {},
                                                    {"out": {"troubleLightStatus": 0, "isFault": False, "isValid": True}})
                self.ipdu.resume_all_bus_send()
                if sts in [1]:
                    self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "AirbagWarning",
                                            {"warn": {"troubleLightStatus": 1, "isFault": False, "isValid": True}})
                    self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetAirbagWarning", {},
                                                {"out": {"troubleLightStatus": 1, "isFault": False, "isValid": True}})
                elif sts in [0]:
                    self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "AirbagWarning",
                                            {"warn": {"troubleLightStatus": 0, "isFault": False, "isValid": False}})
                    self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetAirbagWarning", {},
                                                {"out": {"troubleLightStatus": 0, "isFault": False, "isValid": False}})                                                          

    @allure.title("获取安全气囊系统(乘员保护系统)报警信息&通知安全气囊系统(乘员保护系统)报警信息_8S内禁止上报")
    @pytest.mark.sanity
    def test_caseid_108805(self):
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 2)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 2)
        for usage_mode in [11, 13]:
            for ori_usage_mode in [0, 1, 2]:
                logger.info(f"打印{usage_mode}")
                self.sd_tester.change_usage_mode(ori_usage_mode)
                self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetAirbagWarning", {},
                                                  {"out": {"troubleLightStatus": 2, "isFault": True, "isValid": True}})

                self.sd_tester.change_usage_mode(usage_mode)
                self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "AirbagWarning",
                                            {"warn": {"troubleLightStatus": 0, "isFault": True, "isValid": True}})
                self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetAirbagWarning", {},
                                                {"out": {"troubleLightStatus": 0, "isFault": True, "isValid": True}})

                self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "AirbagWarning",
                                            {"warn": {"troubleLightStatus": 2, "isFault": True, "isValid": True}}, timeout=8)

    @allure.title("获取安全气囊系统(乘员保护系统)报警信息&通知安全气囊系统(乘员保护系统)报警信息_8S内立即上报")
    @pytest.mark.full
    def test_caseid_108806(self):
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 2)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 2)
        for usage_mode in [11, 13]:
            logger.info(f"打印{usage_mode}")
            for ori_usage_mode in [0, 1, 2]:
                logger.info(f"打印{ori_usage_mode}")
                self.sd_tester.change_usage_mode(ori_usage_mode)
                self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetAirbagWarning", {},
                                                  {"out": {"troubleLightStatus": 2, "isFault": True, "isValid": True}})

                self.sd_tester.change_usage_mode(usage_mode)
                self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "AirbagWarning",
                                            {"warn": {"troubleLightStatus": 0, "isFault": True, "isValid": True}})
                self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetAirbagWarning", {},
                                                {"out": {"troubleLightStatus": 0, "isFault": True, "isValid": True}})
                
                self.sd_tester.change_usage_mode(ori_usage_mode)#再次切回来
                self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "AirbagWarning",
                                            {"warn": {"troubleLightStatus": 2, "isFault": True, "isValid": True}}, timeout=0.5)
    
    @allure.title("获取安全气囊系统(乘员保护系统)报警信息&通知安全气囊系统(乘员保护系统)报警信息_计时器多次打断")
    @pytest.mark.full
    def test_caseid_1985234(self):
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 2)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 2)
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.tester_present()#拉起诊断
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetAirbagWarning", {},
                                            {"out": {"troubleLightStatus": 2, "isFault": True, "isValid": True}})
        sleep(1)
        self.sd_tester.change_usage_mode(11)#计时器开始
        self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "AirbagWarning",
                                            {"warn": {"troubleLightStatus": 0, "isFault": True, "isValid": True}})
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetAirbagWarning", {},
                                        {"out": {"troubleLightStatus": 0, "isFault": True, "isValid": True}})
        self.partner.ck_coming_event(PASSIVESAFETY_SERVICE_CLIENT, "AirbagWarning",
                                            {"warn": {"troubleLightStatus": 2, "isFault": True, "isValid": True}}, timeout=8, deviation=0.5)
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetAirbagWarning", {},
                                        {"out": {"troubleLightStatus": 2, "isFault": True, "isValid": True}})
        self.sd_tester.change_usage_mode(0)#取消计时器
        sleep(1)
        self.sd_tester.change_usage_mode(13)#计时器开始
        sleep(1)
        self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "AirbagWarning",
                                            {"warn": {"troubleLightStatus": 0, "isFault": True, "isValid": True}})
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetAirbagWarning", {},
                                        {"out": {"troubleLightStatus": 0, "isFault": True, "isValid": True}})
        self.partner.ck_coming_event(PASSIVESAFETY_SERVICE_CLIENT, "AirbagWarning",
                                            {"warn": {"troubleLightStatus": 2, "isFault": True, "isValid": True}}, timeout=7, deviation=0.5)
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetAirbagWarning", {},
                                        {"out": {"troubleLightStatus": 2, "isFault": True, "isValid": True}})
        self.sd_tester.stop_tester_present()#断开诊断

    @pytest.mark.full
    @allure.title("获取安全气囊系统(乘员保护系统)报警信息&通知安全气囊系统(乘员保护系统)报警信息_无模式切换")
    def test_caseid_108804(self):
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 0)
        self.partner.empty_all(0.5)
        for usage_mode in [0, 1, 2]:
            logger.info(f"打印{usage_mode}")
            self.sd_tester.change_usage_mode(usage_mode)
            for sLampReq in [1, 2, 3, 0]:
                time.sleep(2)
                logger.info(f"打印信号{sLampReq}")
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', sLampReq)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 1)
                self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "AirbagWarning",
                                            {"warn": {"troubleLightStatus": sLampReq, "isFault": False, "isValid": True}})
                self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetAirbagWarning", {},
                                                {"out": {"troubleLightStatus": sLampReq, "isFault": False, "isValid": True}})
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 0)
                self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "AirbagWarning",
                                            {"warn": {"troubleLightStatus": sLampReq, "isFault": False, "isValid": False}})
                self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetAirbagWarning", {},
                                                {"out": {"troubleLightStatus": sLampReq, "isFault": False, "isValid": False}})
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 2)
                self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "AirbagWarning",
                                            {"warn": {"troubleLightStatus": sLampReq, "isFault": True, "isValid": True}})
                self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetAirbagWarning", {},
                                                {"out": {"troubleLightStatus": sLampReq, "isFault": True, "isValid": True}})
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 3)
                self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "AirbagWarning",
                                            {"warn": {"troubleLightStatus": sLampReq, "isFault": True, "isValid": False}})
                self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetAirbagWarning", {},
                                                {"out": {"troubleLightStatus": sLampReq, "isFault": True, "isValid": False}})
    
    @pytest.mark.full
    @allure.title("获取安全气囊系统(乘员保护系统)报警信息&通知安全气囊系统(乘员保护系统)报警信息_8s内信号变化")
    def test_caseid_1985467(self):
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 2)
        self.partner.empty_all(1)
        self.sd_tester.tester_present()#拉起诊断
        self.sd_tester.change_usage_mode(0)
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 1)
        self.partner.ck_no_event(PASSIVESAFETY_SERVICE_CLIENT, "AirbagWarning")
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetAirbagWarning", {},
                                                {"out": {"troubleLightStatus": 0, "isFault": True, "isValid": True}})
        self.partner.ck_coming_event(PASSIVESAFETY_SERVICE_CLIENT, "AirbagWarning",
                                            {"warn": {"troubleLightStatus": 1, "isFault": True, "isValid": True}}, timeout=7, deviation=1)
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetAirbagWarning", {},
                                                {"out": {"troubleLightStatus": 1, "isFault": True, "isValid": True}})
        self.sd_tester.stop_tester_present()#断开诊断
    
    @pytest.mark.sanity
    @allure.title("获取行人保护报警提示&通知行人保护报警提示_PedProtnMsgReqForImpct=1时")
    def test_caseid_1985207(self):
        self.set_PedestrianProtectionWarning_signal(0, 0)
        self.partner.empty_all(1)
        self.set_PedestrianProtectionWarning_signal(1, 1)
        self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "PedestrianProtectionWarning",
                                   {"warn": {"isSysFault": False, "isImpactWarning": True, "isValid": True}}, timeout=1)
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetPedestrianProtectionWarning", {}, 
                                              {"out": {"isSysFault": False, "isImpactWarning": True, "isValid": True}})
        self.set_PedestrianProtectionWarning_signal(0, 1)
        self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "PedestrianProtectionWarning",
                                   {"warn": {"isSysFault": False, "isImpactWarning": True, "isValid": False}}, timeout=1)
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetPedestrianProtectionWarning", {}, 
                                              {"out": {"isSysFault": False, "isImpactWarning": True, "isValid": False}})
        self.set_PedestrianProtectionWarning_signal(2, 1)
        self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "PedestrianProtectionWarning",
                                   {"warn": {"isSysFault": True, "isImpactWarning": True, "isValid": True}}, timeout=1)
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetPedestrianProtectionWarning", {}, 
                                              {"out": {"isSysFault": True, "isImpactWarning": True, "isValid": True}})
        self.set_PedestrianProtectionWarning_signal(3, 1)
        self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "PedestrianProtectionWarning",
                                   {"warn": {"isSysFault": True, "isImpactWarning": True, "isValid": False}}, timeout=1)
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetPedestrianProtectionWarning", {}, 
                                              {"out": {"isSysFault": True, "isImpactWarning": True, "isValid": False}})
        self.set_PedestrianProtectionWarning_signal(0, 1)
        sleep(0.5)
        self.partner.ck_no_event(PASSIVESAFETY_SERVICE_CLIENT, "PedestrianProtectionWarning")
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetPedestrianProtectionWarning", {}, 
                                              {"out": {"isSysFault": True, "isImpactWarning": True, "isValid": False}})
    
    @pytest.mark.full
    @allure.title("获取行人保护报警提示&通知行人保护报警提示_PedProtnMsgReqForImpct=0时")
    def test_caseid_1985208(self):
        self.set_PedestrianProtectionWarning_signal(0, 0)
        self.partner.empty_all(1)
        self.set_PedestrianProtectionWarning_signal(1, 0)
        self.partner.ck_event_and_resp(PASSIVESAFETY_SERVICE_CLIENT, "PedestrianProtectionWarning", 
                                       {"warn": {"isSysFault": False, "isImpactWarning": False, "isValid": True}},
                                       "GetPedestrianProtectionWarning", {})
        self.set_PedestrianProtectionWarning_signal(0, 0)
        self.partner.ck_event_and_resp(PASSIVESAFETY_SERVICE_CLIENT, "PedestrianProtectionWarning", 
                                       {"warn": {"isSysFault": False, "isImpactWarning": False, "isValid": False}},
                                       "GetPedestrianProtectionWarning", {})
        self.set_PedestrianProtectionWarning_signal(2, 0)
        self.partner.ck_event_and_resp(PASSIVESAFETY_SERVICE_CLIENT, "PedestrianProtectionWarning", 
                                       {"warn": {"isSysFault": True, "isImpactWarning": False, "isValid": True}},
                                       "GetPedestrianProtectionWarning", {})
        self.set_PedestrianProtectionWarning_signal(3, 0)
        self.partner.ck_event_and_resp(PASSIVESAFETY_SERVICE_CLIENT, "PedestrianProtectionWarning", 
                                       {"warn": {"isSysFault": True, "isImpactWarning": False, "isValid": False}},
                                       "GetPedestrianProtectionWarning", {})
    
    @pytest.mark.full
    @allure.title("获取|通知行人保护报警提示_PedProtnMsgReqForImpct从1到0_1s内PedProtnMsgReqForFlt无变化")
    def test_caseid_1985209(self):
        self.set_PedestrianProtectionWarning_signal(0, 1)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForFlt', 1)
        self.partner.ck_event_and_resp(PASSIVESAFETY_SERVICE_CLIENT, "PedestrianProtectionWarning", 
                                       {"warn": {"isSysFault": False, "isImpactWarning": True, "isValid": True}},
                                       "GetPedestrianProtectionWarning", {})
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForImpct', 0)
        self.partner.ck_no_event(PASSIVESAFETY_SERVICE_CLIENT, "PedestrianProtectionWarning")
        self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "PedestrianProtectionWarning",
                                  {"warn": {"isSysFault": False, "isImpactWarning": False, "isValid": True}}, timeout=1)
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetPedestrianProtectionWarning", {}, 
                                              {"out": {"isSysFault": False, "isImpactWarning": False, "isValid": True}})
    
    @pytest.mark.full
    @allure.title("获取|通知行人保护报警提示_PedProtnMsgReqForImpct从1到0_1s内PedProtnMsgReqForFlt变化")
    def test_caseid_1985210(self):
        self.set_PedestrianProtectionWarning_signal(1, 1)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForImpct', 0)
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForFlt', 2)
        self.partner.ck_event_and_resp(PASSIVESAFETY_SERVICE_CLIENT, "PedestrianProtectionWarning", 
                                       {"warn": {"isSysFault": True, "isImpactWarning": True, "isValid": True}},
                                       "GetPedestrianProtectionWarning", {})
        sleep(0.8)
        self.partner.ck_event_and_resp(PASSIVESAFETY_SERVICE_CLIENT, "PedestrianProtectionWarning", 
                                       {"warn": {"isSysFault": True, "isImpactWarning": False, "isValid": True}},
                                       "GetPedestrianProtectionWarning", {})
    
    @pytest.mark.full
    @allure.title("获取|通知行人保护报警提示_PedProtnMsgReqForImpct从1到0_1s内PedProtnMsgReqForImpct变化")
    def test_caseid_1985235(self):
        self.set_PedestrianProtectionWarning_signal(1, 1)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForImpct', 0)
        sleep(0.8)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForImpct', 1)
        sleep(1)
        self.partner.ck_no_event(PASSIVESAFETY_SERVICE_CLIENT, "PedestrianProtectionWarning")
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetPedestrianProtectionWarning", {}, 
                                              {"out": {"isSysFault": False, "isImpactWarning": True, "isValid": True}})
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForImpct', 0)
        sleep(1)
        self.partner.ck_event_and_resp(PASSIVESAFETY_SERVICE_CLIENT, "PedestrianProtectionWarning", 
                                       {"warn": {"isSysFault": False, "isImpactWarning": False, "isValid": True}},
                                       "GetPedestrianProtectionWarning", {})
    
    @pytest.mark.full
    @allure.title("获取|通知行人保护报警提示_重启无记忆到有记忆")
    def test_caseid_1985211(self):
        self.del_s2s_db()  # 删除数据库
        self.kill_s2s_and_reconnect_service(PASSIVESAFETY_SERVICE_CLIENT)
        sleep(10)
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetPedestrianProtectionWarning", {}, 
                                              {"out": {"isSysFault": False, "isImpactWarning": False, "isValid": True}})
        sleep(5)
        self.set_PedestrianProtectionWarning_signal(0, 1)
        self.restart_bgm_and_connect_service(PASSIVESAFETY_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.empty_all(5)
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetPedestrianProtectionWarning", {}, 
                                              {"out": {"isSysFault": False, "isImpactWarning": True, "isValid": False}})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_event_and_resp(PASSIVESAFETY_SERVICE_CLIENT, "PedestrianProtectionWarning", 
                                       {"warn": {"isSysFault": False, "isImpactWarning": True, "isValid": False}},
                                       "GetPedestrianProtectionWarning", {})

    @pytest.mark.smoke
    @allure.title("获取|通知车辆碰撞状态")
    def test_caseid_108802(self):
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashFrnt', 0)#前碰撞状态
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashRe', 0)  # 后碰撞状态
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashRollovr', 0)  # 倾翻状态
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashSideLe', 0)  # 左碰撞状态
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashSideRi', 0)  # 右碰撞状态
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetVehicleCrashStatus", {}, {"out": [
            {"RollOverCrash": False, "FrontCrash": False, "RearCrash":False, "LeftCrash": False,
             "RightCrash": False}]})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashFrnt', 1)  # 前碰撞状态
        self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "NotifyVehicleCrashStatus",
                                  {"crash": {"RollOverCrash": False, "FrontCrash": True, "RearCrash": False, "LeftCrash": False,"RightCrash": False}})
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetVehicleCrashStatus", {}, {"out": [
            {"RollOverCrash": False, "FrontCrash": True, "RearCrash": False, "LeftCrash": False,
             "RightCrash": False}]})
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashRe', 0)  # 后碰撞状态
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashRe', 1)  # 后碰撞状态
        self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "NotifyVehicleCrashStatus", {
            "crash": {"RollOverCrash": False, "FrontCrash": True, "RearCrash": True, "LeftCrash": False,
                      "RightCrash": False}})
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetVehicleCrashStatus", {}, {"out": [
            {"RollOverCrash": False, "FrontCrash": True, "RearCrash": True, "LeftCrash": False,
             "RightCrash": False}]})
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashRollovr', 0)#倾翻状态
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashRollovr', 1)  # 倾翻状态
        self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "NotifyVehicleCrashStatus", {
            "crash": {"RollOverCrash": True, "FrontCrash": True, "RearCrash": True, "LeftCrash": False,
                      "RightCrash": False}})
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetVehicleCrashStatus", {}, {"out": [
            {"RollOverCrash": True, "FrontCrash": True, "RearCrash": True, "LeftCrash": False,
             "RightCrash": False}]})
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashSideLe', 0)#左碰撞状态
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashSideLe', 1)  # 左碰撞状态
        self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "NotifyVehicleCrashStatus", {
            "crash": {"RollOverCrash": True, "FrontCrash": True, "RearCrash": True, "LeftCrash": True,
                      "RightCrash": False}})
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetVehicleCrashStatus", {}, {"out": [
            {"RollOverCrash": True, "FrontCrash": True, "RearCrash": True, "LeftCrash": True,
             "RightCrash": False}]})
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashSideRi', 0)#右碰撞状态
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashSideRi', 1)  # 右碰撞状态
        self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "NotifyVehicleCrashStatus", {
            "crash": {"RollOverCrash": True, "FrontCrash": True, "RearCrash": True, "LeftCrash": True,
                      "RightCrash": True}})
        self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetVehicleCrashStatus", {}, {"out": [
            {"RollOverCrash": True, "FrontCrash": True, "RearCrash": True, "LeftCrash": True,
             "RightCrash": True}]})

    @pytest.mark.sanity
    @allure.title("获取车辆碰撞状态&通知车辆碰撞状态_默认值")
    def test_caseid_1959959(self):
        for CrashFrnt in [1, 0]:
            self.set_VehicleCrashStatus_signal(CrashFrnt,CrashFrnt,CrashFrnt,CrashFrnt,CrashFrnt)
            self.partner.empty_all(0.5)
            self.restart_bgm_and_connect_service("PassiveSafetyService_client", resume_all_bus=False)
            self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetVehicleCrashStatus", {}, {"out": [
                {"RollOverCrash": False, "FrontCrash": False, "RearCrash": False, "LeftCrash": False,
                "RightCrash": False}]})
            self.ipdu.resume_all_bus_send()
            if CrashFrnt in [1]:
                self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "NotifyVehicleCrashStatus", 
                                          {"crash": {"RollOverCrash": True, "FrontCrash": True, 
                                                     "RearCrash": True, "LeftCrash": True,"RightCrash": True}})
                self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetVehicleCrashStatus", {}, 
                                                      {"out": [{"RollOverCrash": True, "FrontCrash": True, 
                                                                "RearCrash": True, "LeftCrash": True,"RightCrash": True}]})
            elif CrashFrnt in [0]:
                self.partner.ck_s2s_event(PASSIVESAFETY_SERVICE_CLIENT, "NotifyVehicleCrashStatus",
                                  {"crash": {"RollOverCrash": False, "FrontCrash": False, 
                                             "RearCrash": False, "LeftCrash": False,"RightCrash": False}})
                self.partner.send_request_and_ck_resp(PASSIVESAFETY_SERVICE_CLIENT, "GetVehicleCrashStatus", {}, 
                                                      {"out": [{"RollOverCrash": False, "FrontCrash": False, 
                                                                "RearCrash": False, "LeftCrash": False,"RightCrash": False}]})


