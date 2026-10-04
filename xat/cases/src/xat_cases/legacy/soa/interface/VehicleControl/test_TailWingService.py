#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_TailWingService.py
@Time         :2023/12/19 10:07:31
@Author       :peipei.yang_ext@jiduauto.com
@Description  :
"""
import os
import sys
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_cases.legacy.soa.case_helper.utils import *
from xat_ecu.legacy.interface.bgm.bgm_env.change_bgm_env import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *#中控锁


@allure.feature("SOA服务接口")
@allure.story("整车控制/TailWingService")
@pytest.mark.ypp
class TestTailWingService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)#中控锁
        self.partner = S2sBaseClass([("TailWingService", "client"),
                                     ("CentralLockService", "client"),
                                     ("KeyService", "client"),
                                     ("DoorService", "client"),
                                     ("BonnetService", "client"),
                                     ("TailGateService", "client")])
        self.partner.method_default_timeout = 0.1
        self.io.hood_door1_close()
        self.io.hood_door2_close()
        self.ipdu.lin1_wakeup()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.set_nopeople_incar()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')        
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set_vehspd(0)
        sleep(0.5)
        self.sd_tester.change_car_mode(0)  # 故障1清除
        self.sd_tester.change_usage_mode(1)  # 故障2清除
        self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrMotBlk', 0)  # 故障3清除
        self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrIceBreakFaild', 0)  # 故障4清除 # 设置尾门关闭
        self.partner.send_method_request('TailWingService_client', 'SetTailwingMode', {"mode": 0})  # 设置尾翼收回#故障5清除
        self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4})
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.partner.empty_all(0.5)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()  # 恢复所有总线
        super().after_each_func(ecu, start=False)
    
    @allure.title("设置尾翼禁用&获取尾翼禁用状态&通知尾翼禁用状态_超时恢复")
    @pytest.mark.sanity
    def test_caseid_108817(self):
        for usage_mode in [1, 2, 11, 13]:
            logger.info(f"打印{usage_mode}")
            self.sd_tester.change_usage_mode(usage_mode)
            sleep(1)
            self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingInhibit', {"isOn": True})
            self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'TailwingInhibit', {"isOn": True})
            self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, 'GetTailwingInhibit', {}, {"out": True})
            self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'TailwingInhibit', {"isOn": False}, timeout=2.2)
            self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, 'GetTailwingInhibit', {}, {"out": False}, timeout=2.2)
            self.partner.empty_all(1)
            
    @allure.title("设置尾翼禁用&获取尾翼禁用状态&通知尾翼禁用状态_前置条件从满足到不满足恢复")
    @pytest.mark.full
    def test_caseid_111618(self):
        for usage_mode in [1, 2, 11, 13]:
            logger.info(f"打印{usage_mode}")
            self.sd_tester.change_usage_mode(usage_mode)
            sleep(1)
            self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingInhibit', {"isOn": True})
            self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'TailwingInhibit', {"isOn": True})
            self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, 'GetTailwingInhibit', {}, {"out": True})
            self.sd_tester.change_usage_mode(0)
            self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'TailwingInhibit', {"isOn": False}, timeout=0.5)
            self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, 'GetTailwingInhibit', {}, {"out": False})
    
    @allure.title("设置尾翼禁用&获取尾翼禁用状态&通知尾翼禁用状态_前置条件不满足")
    @pytest.mark.full
    def test_caseid_111619(self):
        self.sd_tester.change_usage_mode(0)
        sleep(1)
        self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingInhibit', {"isOn": True})
        self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, 'GetTailwingInhibit', {}, {"out": False})
    
    @allure.title("设置尾翼禁用&获取尾翼禁用状态&通知尾翼禁用状态_两次调用接口")
    @pytest.mark.full
    def test_caseid_111410(self):
        for usage_mode in [1, 2, 11, 13]:
            logger.info(f"打印{usage_mode}")
            self.sd_tester.change_usage_mode(usage_mode)
            sleep(1)
            self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingInhibit',
                                            {"isOn": True}) 
            self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'TailwingInhibit', {"isOn": True}) 
            sleep(1)  
            self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingInhibit',
                                            {"isOn": True})  
            self.partner.empty_all(1)   
            self.partner.ck_no_event(TAILWING_SERVICE_CLIENT, 'TailwingInhibit',timeout=0.5)
            self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, 'GetTailwingInhibit', {},
                                                {"out": True}) 
            sleep(1)  
            self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'TailwingInhibit', {"isOn": False})  # 通知事件为false
            self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, 'GetTailwingInhibit', {}, {"out": False})
    
    @allure.title("设置尾翼禁用 _下行pdu校验")
    @pytest.mark.full
    def test_caseid_1978714(self):
        for usage_mode in [1, 2, 11, 13]:
            logger.info(f"打印{usage_mode}")
            self.sd_tester.change_usage_mode(usage_mode)
            sleep(0.5)
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingInhibit', {"isOn": True})
            self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingMode', {"mode": 1})
            self.partner.ck_no_event(TAILWING_SERVICE_CLIENT,"Mode")
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_signal_values("ActvReSplrSeldCmd", [0])
            self.bgm_eth_inter.ck_period_time("ActvReSplrSeldCmd", 1)
    
    @allure.title("设置尾翼工作模式&获取尾翼模式&通知尾翼模式_前提条件满足")
    @pytest.mark.sanity
    def test_caseid_1903493(self):
        self.sd_tester.write_single_ccp(564, 2)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingInhibit', {"isOn": False})
        self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, 'GetTailwingInhibit', {}, {"out": False})
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [0, 1, 2]: 
            self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingMode', {"mode": mode})
            sleep(1)
            self.partner.ck_s2s_event('TailWingService_client', 'Mode',{"mode": mode})  
            self.partner.send_request_and_ck_resp('TailWingService_client', 'GetTailwingMode', {}, {"out": mode})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('ActvReSplrSeldCmd', [0, 1, 2])        
    
    @allure.title("设置尾翼工作模式&获取尾翼模式&通知尾翼模式_休眠下电")
    @pytest.mark.full
    def test_caseid_1903474(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)#ActvReSplrStsAvlStsForCDC=1(carmode=normal,usagemode!=Abandoned)
        self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingInhibit', {"isOn": False})
        for mode in [1, 2]: 
            self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingMode',
                                         {"mode": mode})
            self.restart_bgm_and_connect_service(TAILWING_SERVICE_CLIENT)
            self.partner.send_request_and_ck_resp('TailWingService_client', 'GetTailwingMode', {},
                                              {"out": 0})
            
    @allure.title("设置尾翼工作模式&获取尾翼模式&通知尾翼模式_前提条件不满足")
    @pytest.mark.full
    def test_caseid_1903469(self):
        self.sd_tester.change_car_mode(0)  
        self.sd_tester.change_usage_mode(1)  
        self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingInhibit', {"isOn": False})
        self.partner.send_request_and_ck_resp('TailWingService_client', 'GetTailwingMode', {},
                                              {"out": 0})  
    
    @allure.title("设置尾翼工作模式&获取尾翼模式&通知尾翼模式_Last Value")
    @pytest.mark.full
    def test_caseid_1982928(self):
        self.sd_tester.write_single_ccp(564, 2)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingInhibit', {"isOn": False})
        self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingMode',
                                         {"mode": 1})
        self.partner.ck_s2s_event('TailWingService_client', 'Mode',
                                {"mode": 1})  
        self.partner.send_request_and_ck_resp('TailWingService_client', 'GetTailwingMode', {},
                                              {"out": 1})
        self.sd_tester.change_car_mode(1)
        self.partner.send_request_and_ck_resp('TailWingService_client', 'GetTailwingMode', {},
                                              {"out": 1})
    
    @allure.title("设置尾翼工作模式&获取尾翼模式&通知尾翼模式(解闭锁成功触发源_1_RKE解锁成功)")
    @pytest.mark.full
    def test_caseid_1984755(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all()
        self.sd_tester.write_single_ccp(564, 2)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingInhibit', {"isOn": False})
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.dk.set_cenlock_sts(3)
        sleep(1)
        for mode in [0, 1, 2]: 
            self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingMode', {"mode": mode})
            sleep(1)
            self.partner.ck_s2s_event('TailWingService_client', 'Mode',{"mode": mode})  
            self.partner.send_request_and_ck_resp('TailWingService_client', 'GetTailwingMode', {}, {"out": mode})
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('ActvReSplrSeldCmd', [0, 1, 2])
        
    @allure.title("获取尾翼状态&通知尾翼状态")
    @pytest.mark.sanity
    def test_caseid_108866(self):
        self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrPosn', 0)
        self.partner.empty_all(0.5)
        for posn in [5, 1, 6, 2, 7, 3, 5, 4, 6, 0] :
            logger.info(f"打印{posn}")
            self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrPosn', posn)
            sleep(0.5)
            if posn in [5]:
                self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'Status', {"sts": 1})
                self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, 'GetTailWingStatus', {}, {"out": 1})
            elif posn in [6, 7]:
                self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'Status', {"sts": 2})
                self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, 'GetTailWingStatus', {}, {"out": 2})
            else:
                self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'Status', {"sts": 0})
                self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, 'GetTailWingStatus', {}, {"out": 0})
    
    @allure.title("获取尾翼状态&通知尾翼状态_默认值")#重启后信号值为0,没有event事件
    @pytest.mark.full
    def test_caseid_108867(self):
        for posn in [5, 0]:
            self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrPosn', posn)
            self.partner.empty_all(0.5)
            self.restart_bgm_and_connect_service(TAILWING_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, 'GetTailWingStatus', {}, {"out": 0})
            self.ipdu.resume_all_bus_send()
            if posn in [5]:
                self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'Status', {"sts": 1})
                self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, 'GetTailWingStatus', {}, {"out": 1})
            else:
                self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'Status', {"sts": 0})
                self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, 'GetTailWingStatus', {}, {"out": 0})

    @allure.title("获取尾翼状态&通知尾翼状态_重启场景")
    @pytest.mark.full
    def test_caseid_1988856(self):
        for sts in [ 5, 0, 1, 5, 6, 2, 3, 7, 4, 5]:
            logger.info(f"当前sts循环到.{sts}")
            self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrPosn', sts)
            sleep(1)
            self.restart_bgm_and_connect_service(TAILWING_SERVICE_CLIENT)
            sleep(0.5)
            if sts in [ 0, 1, 2, 3, 4]:
                self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, "Status", {"sts": 0})
            elif sts == 5:
                self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, "Status", {"sts": 1})
            else:
                self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, "Status", {"sts": 2})
            self.partner.empty_all(0.5)

    @allure.title("获取尾翼位置&通知尾翼位置")
    @pytest.mark.sanity
    def test_caseid_108860(self):
        self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrPosn', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrPosn', 1)
        self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'Position', {"pos": 0})
        self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, 'GetPosition', {}, {"out": 0})
        self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrPosn', 5)
        self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'Position', {"pos": 4})
        self.partner.send_request_and_ck_resp('TailWingService_client', 'GetPosition', {}, {"out": 4})
        self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrPosn', 2)
        self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'Position', {"pos": 1})
        self.partner.send_request_and_ck_resp('TailWingService_client', 'GetPosition', {}, {"out": 1})
        self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrPosn', 6)
        self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'Position', {"pos": 4})
        self.partner.send_request_and_ck_resp('TailWingService_client', 'GetPosition', {}, {"out": 4})
        self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrPosn', 3)
        self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'Position', {"pos": 2})
        self.partner.send_request_and_ck_resp('TailWingService_client', 'GetPosition', {}, {"out": 2})
        self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrPosn', 7)
        self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'Position', {"pos": 4})
        self.partner.send_request_and_ck_resp('TailWingService_client', 'GetPosition', {}, {"out": 4})
        self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrPosn', 4)
        self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'Position', {"pos": 3})
        self.partner.send_request_and_ck_resp('TailWingService_client', 'GetPosition', {}, {"out": 3})
        self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrPosn', 0)
        self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'Position', {"pos": 5})
        self.partner.send_request_and_ck_resp('TailWingService_client', 'GetPosition', {}, {"out": 5})
    
    @allure.title("获取尾翼位置&通知尾翼位置_默认值")
    @pytest.mark.full
    def test_caseid_1980283(self):
        for posn in [1, 0] :
            self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrPosn', posn)
            self.partner.empty_all(0.5)
            self.restart_bgm_and_connect_service(TAILWING_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp('TailWingService_client', 'GetPosition', {}, {"out": 5})
            self.ipdu.resume_all_bus_send()
            if posn in [1]:
                self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'Position', {"pos": 0})
                self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, 'GetPosition', {}, {"out": 0})
            else:
                self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'Position', {"pos": 5})
                self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, 'GetPosition', {}, {"out": 5})
        
    @allure.title("获取尾翼初始化状态&通知尾翼初始化状态")
    @pytest.mark.smoke
    def test_caseid_108861(self):
        self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'CalStsAWM', 0)
        self.partner.empty_all(0.5)
        for sAWM in [1, 2, 3, 0] :
            self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'CalStsAWM', sAWM)
            self.partner.ck_s2s_event('TailWingService_client', 'InitStatus', {"sts": sAWM})
            self.partner.send_request_and_ck_resp('TailWingService_client', 'GetInitStatus', {}, {"out": sAWM})
    
    @allure.title(" 获取尾翼初始化状态&通知尾翼初始化状态_默认值")
    @pytest.mark.full
    def test_caseid_108822(self):
        for sAWM in [1, 0] :
            self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'CalStsAWM', sAWM)
            self.partner.empty_all(0.5)
            self.restart_bgm_and_connect_service(TAILWING_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp('TailWingService_client', 'GetInitStatus', {}, {"out": 255})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event('TailWingService_client', 'InitStatus', {"sts": sAWM})
            self.partner.send_request_and_ck_resp('TailWingService_client', 'GetInitStatus', {}, {"out": sAWM})

@pytest.mark.jishu
@allure.feature("SOA服务接口")
@allure.story("整车控制/TailWingService")
@pytest.mark.mock_tcp
class TestTailWingServiceMockMcu(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu, tcp_down_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("TailWingService", "client")])
        self.partner.wait_for_service_reconnect(TAILWING_SERVICE_CLIENT)
        sleep(10)
    
    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
    
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.bgm_eth_inter.set_signal("ActvReSplrStsNotAvlEve", 0, send_pdu_immediately=True)
        self.bgm_eth_inter.set_signal("ActvReSplrStsAvlStsForCDC", 1, send_pdu_immediately=True) 
        self.partner.empty_all()
    
    @allure.title("获取尾翼故障信息&通知尾翼故障信息_ActvReSplrStsNotAvlEve")
    @pytest.mark.sanity
    def test_caseid_1982931(self): # 
        self.bgm_eth_inter.set_signal("ActvReSplrStsAvlStsForCDC", 0, send_pdu_immediately=True) 
        for NotAvlEve in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0,]:
            logger.info(f"当前循环到.{NotAvlEve}")
            self.bgm_eth_inter.set_signal("ActvReSplrStsNotAvlEve", NotAvlEve, send_pdu_immediately=True)#列表第三个信号ActvReSplrStsNotAvlEve
            sleep(1)
            if NotAvlEve in[8, 9]:
                self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, "GetFaultInfo", {},
                                                {"out": [{"fault": 7, "faultMsg": ""}]})
            elif NotAvlEve in[0]:
                self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, "GetFaultInfo", {},
                                                {"out": [{"fault": 8, "faultMsg": ""}]})
            else:
                self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, "TailWingFault", {"faults": [{"fault": NotAvlEve, "faultMsg": ""}]})
                self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": NotAvlEve, "faultMsg": ""}]})
        self.bgm_eth_inter.set_signal("ActvReSplrStsAvlStsForCDC", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, "TailWingFault", {"faults": [{"fault": 0, "faultMsg": ""}]})
                
    @allure.title("设置尾翼工作模式&设置尾翼禁用_通知尾翼开启后,设置CDC信号为False")
    @pytest.mark.full
    def test_caseid_1988895(self):
        self.sd_tester.write_single_ccp(564, 2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 11)
        self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingMode', {"mode": 1})
        self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingInhibit', {"isOn": True})
        self.partner.ck_s2s_event('TailWingService_client', 'Mode',{"mode": 0})  
        sleep(2)
        self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, 'TailwingInhibit', {"isOn": False},timeout=1) 
        self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingMode', {"mode": 1})
        self.partner.ck_s2s_event('TailWingService_client', 'Mode',{"mode": 1}) 
        self.bgm_eth_inter.set_signal("ActvReSplrStsAvlStsForCDC", 0, send_pdu_immediately=True) 
        self.partner.send_request_and_ck_resp('TailWingService_client', 'GetTailwingMode',{},{"out": 1},timeout=1) 

    
    @allure.title("设置尾翼工作模式&设置尾翼禁用_设置CDC信号为关闭开启后产生故障")
    @pytest.mark.full
    def test_caseid_1988897(self):
        self.sd_tester.write_single_ccp(564, 2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 11)
        self.bgm_eth_inter.set_signal("ActvReSplrStsNotAvlEve", 1, send_pdu_immediately=True)
        self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, "TailWingFault", {"faults": [{"fault": 1, "faultMsg": ""}]},timeout=1)
        self.bgm_eth_inter.set_signal("ActvReSplrStsAvlStsForCDC", 0, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, "TailWingFault", {"faults": [{"fault": 8, "faultMsg": ""},{"fault": 1, "faultMsg": ""}]},timeout=1)
        self.partner.empty_all(0.5)
        self.bgm_eth_inter.set_signal("ActvReSplrStsNotAvlEve", 8, send_pdu_immediately=True)
        self.partner.ck_no_event(TAILWING_SERVICE_CLIENT, "TailWingFault")
        self.bgm_eth_inter.set_signal("ActvReSplrStsNotAvlEve", 5, send_pdu_immediately=True)
        self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, "TailWingFault", {"faults": [{"fault": 8, "faultMsg": ""},{"fault": 5, "faultMsg": ""}]},timeout=1)
        self.bgm_eth_inter.set_signal("ActvReSplrStsAvlStsForCDC", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, "TailWingFault", {"faults": [{"fault": 5, "faultMsg": ""}]},timeout=1)
        
    @allure.title("获取尾翼故障信息&通知尾翼故障信息_ActvReSplrStsAvlStsForCDC")#故障8
    @pytest.mark.sanity
    def test_caseid_110867(self):
        for sForCDC in [0, 1]:
            self.bgm_eth_inter.set_signal("ActvReSplrStsAvlStsForCDC", sForCDC, send_pdu_immediately=True)#4表示pdu长度,列表里面第一位是第一个信号
            sleep(1)
            sts=8 if sForCDC in [0] else 0
            self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, "TailWingFault", {"faults": [{"fault": sts, "faultMsg": ""}]})
            self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": sts, "faultMsg": ""}]})
    
    @allure.title("获取尾翼故障信息&通知尾翼故障信息_默认+other值")#默认值
    @pytest.mark.full
    def test_caseid_110868(self):
        self.restart_bgm_and_connect_service(TAILWING_SERVICE_CLIENT, resume_all_bus=False)
        sleep(5)
        self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 0, "faultMsg": ""}]})
        self.bgm_eth_inter.set_signal("ActvReSplrStsNotAvlEve", 2, send_pdu_immediately=True)
        self.partner.ck_s2s_event(TAILWING_SERVICE_CLIENT, "TailWingFault", {"faults": [{"fault": 2, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 2, "faultMsg": ""}]})

    @allure.title("设置尾翼工作模式_前提条件不满足不响应调用")
    @pytest.mark.full
    def test_caseid_1985785(self):
        self.bgm_eth_inter.set_signal("ActvReSplrStsAvlStsForCDC", 0, send_pdu_immediately=True) 
        self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingInhibit', {"isOn": False})
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(TAILWING_SERVICE_CLIENT, 'SetTailwingMode',
                                         {"mode": 1})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("ActvReSplrSeldCmd", [])
        
