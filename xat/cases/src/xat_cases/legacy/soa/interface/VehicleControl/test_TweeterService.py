# -*- coding: utf-8 -*-
"""
@File        : test_soa_tweeter.py
@Author      : hui.zhao@jiduatuo.com
@Time        : 2023/05/12 1:00 PM
@Description : Test s2s interface about tweeter function
"""

import pytest
import allure

from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *


@allure.feature("SOA服务接口")
@allure.story("整车控制/TweeterService")
@pytest.mark.jishu
class TestTweeterService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("TweeterService", "client")])
        self.partner.method_default_timeout = 0.1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,'VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3') # 切UsageMode的前置条件
        self.ipdu.lin4_wakeup()
        sleep(2)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu, start=False) 

    def after_class(self, ecu):
        self.partner.stop_operators()#partner关闭
        super().after_class(self, ecu)
    
    def set_TweeterStatus_signal(self, LeftElevator=0, RightElevator=0):
        logger.info(f"设置信号---{LeftElevator,RightElevator}")
        self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'LeftElevatorStatus', LeftElevator)
        self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'RightElevatorStatus', RightElevator)
        
    @allure.title("设置可升降高音扬声器状态_遍历扬声器状态stop/rise/fall/reserved")
    @pytest.mark.smoke
    def test_caseid_1979619(self):
        for sts in range(4):
            self.partner.send_method_request('TweeterService_client',"SetTweeterStatus", {"zondId": 0, "command": sts})
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr02, 'RiseOrFallControl', sts, timeout=0.5)

    @allure.title("通知/获取可升降高音扬声器同步状态_遍历yes/no")
    @pytest.mark.sanity
    def test_caseid_109802(self):
        self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'RiseorFallSyncStatus', 1)
        self.partner.empty_all(1)
        for sts in range(2):
            self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'RiseorFallSyncStatus', sts)
            sleep(0.5)
            self.partner.ck_s2s_event('TweeterService_client', "SyncStatus", {"syncsts": sts+1})
            self.partner.send_request_and_ck_resp('TweeterService_client',"GetSyncStatus",{},
                                                {"out": sts+1})
            
    allure.title("通知/获取可升降高音扬声器同步状态_上下电校验默认值")
    @pytest.mark.full
    def test_caseid_109786(self):
        self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'RiseorFallSyncStatus', 1)
        self.restart_bgm_and_connect_service(TWEETER_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)
        self.partner.send_request_and_ck_resp('TweeterService_client',"GetSyncStatus",{},
                                                {"out": 0})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event('TweeterService_client', "SyncStatus", {"syncsts": 2})
        self.partner.send_request_and_ck_resp('TweeterService_client',"GetSyncStatus",{},
                                                {"out": 2})
   
    @allure.title("通知可升降高音扬声器状态_重启后event上报")
    @pytest.mark.full
    def test_caseid_1985324(self):
        self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'RightElevatorStatus', 4)
        self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'LeftElevatorStatus', 5)
        self.restart_bgm_and_connect_service(TWEETER_SERVICE_CLIENT)
        self.partner.ck_s2s_event('TweeterService_client', "TweeterStatus", {"sts": [{"zoneId": 1, "status": 5},{"zoneId": 2, "status": 4}]})

    @allure.title("获取可升降高音扬声器状态_服务上线获取默认值")
    @pytest.mark.full
    def test_caseid_1960124(self):
        #恢复信号默认值，防止受上条case影响
        self.set_TweeterStatus_signal()
        self.restart_bgm_and_connect_service(TWEETER_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp('TweeterService_client', 'GetStatus', {"tweeters": [0]},
                                        {"out": [{"zoneId": 1, "status": 0},{"zoneId": 2, "status": 0}]})
       
    @allure.title("获取可升降高音扬声器状态_信号丢失(初始化65535)")
    @pytest.mark.full
    def test_caseid_109404(self):
        self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'LeftElevatorStatus', 2)
        self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'RightElevatorStatus', 2)
        self.restart_bgm_and_connect_service(TWEETER_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)
        self.partner.send_request_and_ck_resp('TweeterService_client', 'GetStatus', {"tweeters": [0]},
                                        {"out": [{"zoneId": 1, "status": 65535},
                                        {"zoneId": 2, "status": 65535}]})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event('TweeterService_client', "TweeterStatus", {"sts": [{"zoneId": 1, "status": 2},{"zoneId": 2, "status": 2}]})
        self.partner.send_request_and_ck_resp('TweeterService_client', "GetStatus", {"tweeters": [0]},
                                                {"out": [{"zoneId": 1, "status": 2}, {"zoneId": 2, "status": 2}]}) 
          
    @allure.title("遍历通知/获取可升降高音扬声器状态_遍历左右(0-7)") # v1.4新增
    @pytest.mark.sanity
    def test_caseid_1983354(self):
        self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'LeftElevatorStatus', 2)
        self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'RightElevatorStatus', 2)
        self.partner.empty_all(1)
        last = -1
        dic = {0 : 0, 1 : 1, 2 : 2, 3 : 3, 4 : 4 , 5 : 5, 6 : 0, 7 : 0 }
        for sig , sts1 in dic.items():  
            logger.info(f"当前信号.{sig},当前返回值.{sts1}")
            self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'LeftElevatorStatus', sig)
            self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'RightElevatorStatus', sig)
            if sig ==5:
                sleep(1)
                self.partner.send_request_and_ck_resp('TweeterService_client', "GetStatus", {"tweeters": [0]},
                                                    {"out": [{"zoneId": 1, "status": sts1},{"zoneId": 2, "status": sts1}]})
            else:
                self.partner.send_request_and_ck_resp('TweeterService_client', "GetStatus", {"tweeters": [0]},
                                                    {"out": [{"zoneId": 1, "status": sts1},{"zoneId": 2, "status": sts1}]})
                if last != sts1:
                    self.partner.ck_s2s_event('TweeterService_client', "TweeterStatus", {"sts": [{"zoneId": 1, "status": sts1},{"zoneId": 2, "status": sts1}]}) 
                else:       
                    self.partner.ck_no_event('TweeterService_client', "TweeterStatus") 
                last = sts1
                self.partner.empty_all(0.5)
            
    @allure.title("遍历通知/获取可升降高音扬声器状态_左右上下电校验默认值") # v1.4新增
    @pytest.mark.sanity
    def test_caseid_1983606(self):
        self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'LeftElevatorStatus', 2)
        self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'RightElevatorStatus', 2)
        self.restart_bgm_and_connect_service(TWEETER_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)
        self.partner.send_request_and_ck_resp('TweeterService_client', 'GetStatus', {"tweeters": [0]},
                                        {"out": [{"zoneId": 1, "status": 65535},
                                        {"zoneId": 2, "status": 65535}]})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event('TweeterService_client', "TweeterStatus", {"sts": [{"zoneId": 1, "status": 2},{"zoneId": 2, "status": 2}]}) 
        self.partner.send_request_and_ck_resp('TweeterService_client', 'GetStatus', {"tweeters": [0]},
                                        {"out": [{"zoneId": 1, "status": 2},
                                        {"zoneId": 2, "status": 2}]})
        
    @allure.title("遍历通知/获取可升降高音扬声器状态_左右不同信号值停发总线校验默认值&恢复信号值") # v1.4新增
    @pytest.mark.sanity
    def test_caseid_1985494(self):
        self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'LeftElevatorStatus', 2)
        self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'RightElevatorStatus', 7)
        self.partner.empty_all(0.5)
        self.restart_bgm_and_connect_service(TWEETER_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)
        self.partner.ck_no_event('TweeterService_client', "TweeterStatus")
        self.partner.send_request_and_ck_resp('TweeterService_client', 'GetStatus', {"tweeters": [0]},
                                        {"out": [{"zoneId": 1, "status": 65535},
                                        {"zoneId": 2, "status": 65535}]})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event('TweeterService_client', "TweeterStatus", {"sts": [{"zoneId": 1, "status": 2},{"zoneId": 2, "status": 0}]}) 
        self.partner.send_request_and_ck_resp('TweeterService_client', 'GetStatus', {"tweeters": [0]},
                                        {"out": [{"zoneId": 1, "status": 2},
                                        {"zoneId": 2, "status": 0}]}) 
            
    @allure.title("通知/获取可升降高音扬声器状态_1s计时器内信号保持为5时") 
    @pytest.mark.full
    def test_caseid_1985393(self):
        self.set_TweeterStatus_signal(1, 1)
        self.partner.empty_all(0.5)
        self.set_TweeterStatus_signal(5, 5)
        self.partner.ck_no_event('TweeterService_client', "TweeterStatus", timeout=0.2)
        self.partner.send_request_and_ck_resp('TweeterService_client', "GetStatus", {"tweeters": [0]},
                                                {"out": [{"zoneId": 1, "status": 1},{"zoneId": 2, "status": 1}]})
        self.partner.ck_coming_event('TweeterService_client', "TweeterStatus",
                                  {"sts": [{"zoneId": 1, "status": 5},{"zoneId": 2, "status": 5}]}, timeout=0.8, deviation=0.2)
        self.partner.send_request_and_ck_resp('TweeterService_client', "GetStatus", {"tweeters": [0]},
                                                {"out": [{"zoneId": 1, "status": 5},{"zoneId": 2, "status": 5}]})
    
    @allure.title("通知/获取可升降高音扬声器状态_1s计时器内信号为其他值时") 
    @pytest.mark.full
    def test_caseid_1985396(self):
        self.set_TweeterStatus_signal(1, 1)
        self.partner.empty_all(0.5)
        self.set_TweeterStatus_signal(5, 5)
        self.partner.ck_no_event('TweeterService_client', "TweeterStatus", timeout=0.2)
        self.partner.send_request_and_ck_resp('TweeterService_client', "GetStatus", {"tweeters": [0]},
                                                {"out": [{"zoneId": 1, "status": 1},{"zoneId": 2, "status": 1}]})
        self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'LeftElevatorStatus', 4)
        self.partner.ck_coming_event('TweeterService_client', "TweeterStatus",
                                  {"sts": [{"zoneId": 1, "status": 4},{"zoneId": 2, "status": 1}]},timeout=0.5)
        self.partner.send_request_and_ck_resp('TweeterService_client', "GetStatus", {"tweeters": [0]},
                                                {"out": [{"zoneId": 1, "status": 4},{"zoneId": 2, "status": 1}]})
        self.partner.ck_coming_event('TweeterService_client', "TweeterStatus",
                                  {"sts": [{"zoneId": 1, "status": 4},{"zoneId": 2, "status": 5}]}, timeout=0.8, deviation=0.2)
        self.partner.send_request_and_ck_resp('TweeterService_client', "GetStatus", {"tweeters": [0]},
                                                {"out": [{"zoneId": 1, "status": 4},{"zoneId": 2, "status": 5}]})
    
    @allure.title("通知/获取可升降高音扬声器状态_单个信号计时器逻辑") 
    @pytest.mark.full
    def test_caseid_1985411(self):
        self.set_TweeterStatus_signal(1, 1)
        self.partner.empty_all(0.5)
        self.set_TweeterStatus_signal(5, 4)
        self.partner.ck_coming_event('TweeterService_client', "TweeterStatus",
                                  {"sts": [{"zoneId": 1, "status": 1},{"zoneId": 2, "status": 4}]}, timeout=0.4)
        self.partner.send_request_and_ck_resp('TweeterService_client', "GetStatus", {"tweeters": [0]},
                                                {"out": [{"zoneId": 1, "status": 1},{"zoneId": 2, "status": 4}]})
        self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'RightElevatorStatus', 5)
        self.partner.ck_coming_event('TweeterService_client', "TweeterStatus",
                                  {"sts": [{"zoneId": 1, "status": 5},{"zoneId": 2, "status": 4}]}, timeout=1, deviation=0.2)
        self.partner.send_request_and_ck_resp('TweeterService_client', "GetStatus", {"tweeters": [0]},
                                                {"out": [{"zoneId": 1, "status": 5},{"zoneId": 2, "status": 4}]})
        self.partner.ck_coming_event('TweeterService_client', "TweeterStatus",
                                  {"sts": [{"zoneId": 1, "status": 5},{"zoneId": 2, "status": 5}]}, timeout=0.4)
        self.partner.send_request_and_ck_resp('TweeterService_client', "GetStatus", {"tweeters": [0]},
                                                {"out": [{"zoneId": 1, "status": 5},{"zoneId": 2, "status": 5}]})
        self.ipdu.set(self.ipdu.cem_lin4.TlcmCem_Lin4Fr01, 'RightElevatorStatus', 5)
        self.partner.ck_no_event('TweeterService_client', "TweeterStatus", timeout=0.6)
        self.partner.send_request_and_ck_resp('TweeterService_client', "GetStatus", {"tweeters": [0]},
                                                {"out": [{"zoneId": 1, "status": 5},{"zoneId": 2, "status": 5}]})
    
    @allure.title("通知/获取可升降高音扬声器状态_无效值+停发总线计时器逻辑") 
    @pytest.mark.full
    def test_caseid_1985416(self):
        self.set_TweeterStatus_signal(7, 7)
        self.partner.empty_all(0.5)
        self.set_TweeterStatus_signal(5, 5)
        self.partner.ck_no_event('TweeterService_client', "TweeterStatus", timeout=0.4)
        self.partner.send_request_and_ck_resp('TweeterService_client', "GetStatus", {"tweeters": [0]},
                                                {"out": [{"zoneId": 1, "status": 0},{"zoneId": 2, "status": 0}]})
        self.partner.ck_coming_event('TweeterService_client', "TweeterStatus",
                                  {"sts": [{"zoneId": 1, "status": 5},{"zoneId": 2, "status": 5}]}, timeout=0.7, deviation=0.2)
        self.partner.send_request_and_ck_resp('TweeterService_client', "GetStatus", {"tweeters": [0]},
                                                {"out": [{"zoneId": 1, "status": 5},{"zoneId": 2, "status": 5}]})
        self.set_TweeterStatus_signal(4, 4)
        sleep(0.5)
        self.set_TweeterStatus_signal(5, 5)
        self.ipdu.pause_all_bus_send()
        logger.info(f"当前信号已丢失..............................")
        sleep(2)
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event('TweeterService_client', "TweeterStatus",
                                  {"sts": [{"zoneId": 1, "status": 5},{"zoneId": 2, "status": 5}]})
        self.partner.send_request_and_ck_resp('TweeterService_client', "GetStatus", {"tweeters": [0]},
                                                {"out": [{"zoneId": 1, "status": 5},{"zoneId": 2, "status": 5}]})
    
       
    
   



