#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_ChassisService.py
@Time         :2024/11/04
@Author       :qingxia.ai@jiduauto.com
@Description  :
"""
import allure
import pytest
import time
import random
from time import sleep
from xat_ecu.legacy.common.data_type_handing import logger
from xat_ecu.legacy.interface.nuc_app import get_obd_ip
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_cases.legacy.soa.case_helper.utils import *

@allure.feature("SOA服务接口")
@allure.story("运动控制/SuspensionService")
@pytest.mark.aqx
class TestSuspensionService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([(SUSPENSION_SERVICE_CLIENT),
                                     (CHASSIS_SERVICE_CLIENT)])
        self.partner.method_default_timeout = 0.1
        self.sd_tester.tester_present()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.partner.stop_operators()        
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkNotEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set_vehspd(0)
        sleep(1)
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        self.partner.empty_all()
        
    @allure.title("设置空气悬架便捷上下车功能开启关闭_参数取值遍历&下行以太网校验")
    @pytest.mark.smoke
    def test_caseid_1989267(self): 
        self.dk.set_chassis_service_gear("GearP")
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1) 
        for i in [0, 0, 1, 1]:
            self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionEasyEntryConfig", {"configCmd": {"isOn": bool(i)}})
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'EasyEntryEna', i, timeout=1)
            sleep(2)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        valuelist = [i for i in [0, 0, 1, 1] for _ in range(6)]
        self.bgm_eth_inter.ck_signal_values("EasyEntryEna", valuelist)
        self.bgm_eth_inter.ck_period_time("EasyEntryEna", 0.1, permit_fail_times=3)
        
    @allure.title("设置空气悬架便捷上下车功能开启关闭_接口返回校验")
    @pytest.mark.sanity
    def test_caseid_1989268(self):         
        self.sd_tester.change_usage_mode(random.choice([11, 13]))
        self.dk.set_chassis_service_gear("GearP")
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionEasyEntryConfig", {"configCmd": {"isOn": True}}, {"out": 0}) 
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'EasyEntryEna', 1, timeout=1)
        for gear in [1, 2, 3, 5]:    
            self.dk.set_chassis_service_gear(gear)    
            sleep(0.5)
            self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionEasyEntryConfig", {"configCmd": {"isOn": random.choice([True, False])}}, {"out": 14}) 
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'EasyEntryEna', 1, timeout=1)
            
    @allure.title("设置空气悬架便捷上下车功能开启关闭_打断逻辑_收到新接口调用&满足前置")
    @pytest.mark.full
    def test_caseid_1989269(self): # SUSPEN: |SetAirSuspensionEasyEntryConfig      
        self.dk.set_chassis_service_gear("GearP")
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1) 
        for i in [False, True]:
            self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionEasyEntryConfig", {"configCmd": {"isOn": True}})
            sleep(0.24)
            self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionEasyEntryConfig", {"configCmd": {"isOn": i}})
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'EasyEntryEna', int(i), timeout=1)
            sleep(2)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        result = self.bgm_eth_inter.get_signal_values("EasyEntryEna")
        assert len(result) > 14 and len(result) < 19, "打断逻辑有误"
        
    @allure.title("设置空气悬架便捷上下车功能开启关闭_打断逻辑_收到新接口调用&不满足前置")
    @pytest.mark.full
    def test_caseid_1989270(self):      
        self.sd_tester.change_usage_mode(random.choice([11, 13]))   
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1) 
        for i in [False, True]:          
            self.dk.set_chassis_service_gear("GearP")
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetGear", {}, {"out": 0})
            self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionEasyEntryConfig", {"configCmd": {"isOn": False}}, {"out": 0}) 
            sleep(0.1)
            self.dk.set_chassis_service_gear("GearD")
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetGear", {}, {"out": 3})
            self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionEasyEntryConfig", {"configCmd": {"isOn": i}}, {"out": 14}) 
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'EasyEntryEna', 0, timeout=1)
            sleep(2)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        result = self.bgm_eth_inter.get_signal_values("EasyEntryEna")
        assert len(result) == 12, "打断逻辑有误"

    @allure.title("设置空气悬架高度自动调节功能开启关闭_接口返回校验&参数取值遍历&下行以太网校验")
    @pytest.mark.smoke
    def test_caseid_1989275(self):    
        self.sd_tester.change_usage_mode(random.choice([11, 13]))     
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1) 
        for i in [0, 0, 1, 1]:
            self.dk.set_chassis_service_gear(random.choice([0, 1, 2, 3, 5]))
            sleep(1)
            self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightAutoAdjustConfig", {"configCmd": {"isOn": bool(i)}}, {"out": 0}) 
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, 'AutLvlInhb', i, timeout=1)
            sleep(2)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        valuelist = [i for i in [0, 0, 1, 1] for _ in range(6)]
        self.bgm_eth_inter.ck_signal_values("AutLvlInhb", valuelist)
        self.bgm_eth_inter.ck_period_time("AutLvlInhb", 0.1, permit_fail_times=3)

    @allure.title("设置空气悬架高度自动调节功能开启关闭_打断逻辑")
    @pytest.mark.full
    def test_caseid_1989276(self):         
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1) 
        for i in [False, True]:
            self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightAutoAdjustConfig", {"configCmd": {"isOn": True}})
            sleep(0.24)
            self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightAutoAdjustConfig", {"configCmd": {"isOn": i}})
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, 'AutLvlInhb', int(i), timeout=1)
            sleep(2)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        result = self.bgm_eth_inter.get_signal_values("AutLvlInhb")
        assert len(result) > 14 and len(result) < 19, "打断逻辑有误"
                
    @allure.title("获取&通知空气悬架配置信息_便捷上下车功能_取值遍历&下电记忆")
    @pytest.mark.sanity
    def test_caseid_1989334(self): 
        self.dk.set_chassis_service_gear("GearP")
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetGear", {}, {"out": 0})
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionEasyEntryConfig", {"configCmd": {"isOn": False}})
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionConfigurationInfo", {}, {"out": {"easyEntrySts": 0, "validity": 0}}, timeout=3)
        self.partner.empty_all(1)
        for i in [True, False]:
            self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionEasyEntryConfig", {"configCmd": {"isOn": i}}, timeout=5)
            self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionConfigurationInfo", 
                                           {"configurationInfo": {"easyEntrySts":int(i), "validity": 0}})  
            self.restart_bgm_and_connect_service(SUSPENSION_SERVICE_CLIENT) 
            self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionConfigurationInfo", 
                                           {"configurationInfo": {"easyEntrySts":int(i), "validity": 0}}, timeout=5) # 上电后需要主动通知一次
            
    @allure.title("获取&通知空气悬架配置信息_高度自动调节功能_取值遍历&下电记忆")
    @pytest.mark.full
    def test_caseid_1989350(self): 
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightAutoAdjustConfig", {"configCmd": {"isOn": False}})
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionConfigurationInfo", {}, {"out": {"heightAutoAdjustSts": 0, "validity": 0}}, timeout=3)
        self.partner.empty_all(1)        
        for cmd in [True, False]:
            self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightAutoAdjustConfig", {"configCmd": {"isOn": cmd}})
            self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionConfigurationInfo", 
                                           {"configurationInfo": {"heightAutoAdjustSts":int(cmd), "validity": 0}})  
            self.restart_bgm_and_connect_service(SUSPENSION_SERVICE_CLIENT) 
            self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionConfigurationInfo", 
                                           {"configurationInfo": {"heightAutoAdjustSts":int(cmd), "validity": 0}}, timeout=5) # 上电后需要主动通知一次
        
    @allure.title("获取&通知空气悬架配置信息_出厂默认值")
    @allure.title("获取&通知空气悬架刚度调节风格信息_出厂默认值")
    @pytest.mark.full
    def test_caseid_1989335_1989344_1989351(self):     
        self.dk.set_chassis_service_gear("GearP")
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetGear", {}, {"out": 0})
        # 便捷上下车功能
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionEasyEntryConfig", {"configCmd": {"isOn": False}})
        # 高度自动调节功能
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightAutoAdjustConfig", {"configCmd": {"isOn": False}})
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionConfigurationInfo", {}, 
                                              {"out": {"easyEntrySts":0, "heightAutoAdjustSts":0, "easyLoadingSts":1, "jackModeSts":0, "validity":0}}, timeout=3)
        # 空气悬架刚度调节风格信息
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionStiffnessStyleConfig",
                                         {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), "styleCmd": 3}})
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionStiffnessStyleInfo", {}, {"out": {"styleSts": 3}}, timeout=3)
        self.partner.empty_all(2)     
        self.del_s2s_db()  # 删除数据库
        sleep(2)
        self.restart_bgm_and_connect_service(SUSPENSION_SERVICE_CLIENT) # 上电后需要主动通知一次
        # 空气悬架配置信息
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionConfigurationInfo", 
                                       {"configurationInfo": {"easyEntrySts":1, "heightAutoAdjustSts":1, "easyLoadingSts":1, "jackModeSts":0, "validity":0}}, timeout=5) 
        # 空气悬架刚度调节风格信息
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionStiffnessStyleInfo", {"styleInfo": {"validity":0, "styleSts": 2}}) 

    @allure.title("获取&通知空气悬架配置信息_便捷上下车功能_set接口前置不满足时不处理")
    @pytest.mark.full
    def test_caseid_1989336(self):   
        self.sd_tester.change_usage_mode(random.choice([11, 13]))      
        self.dk.set_chassis_service_gear("GearP")    
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetGear", {}, {"out": 0})
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionEasyEntryConfig", {"configCmd": {"isOn": False}})
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionConfigurationInfo", {}, {"out": {"easyEntrySts": 0, "validity": 0}}, timeout=3)
        self.partner.empty_all(2)  
        for i in [True, False, True]:
            self.dk.set_chassis_service_gear(random.choice([1, 2, 3, 5]))  
            sleep(1)
            self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionEasyEntryConfig", {"configCmd": {"isOn": i}}, {"out": 14}) 
            sleep(1)
        self.partner.ck_no_event_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionConfigurationInfo", {"out": {"easyEntrySts": 0, "validity": 0}}, timeout=2)  
        self.restart_bgm_and_connect_service(SUSPENSION_SERVICE_CLIENT) 
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionConfigurationInfo", {"configurationInfo": {"easyEntrySts": 0, "validity": 0}}, timeout=5)

    @allure.title("设置空气悬架刚度调节风格_参数取值遍历&下行以太网校验")
    @pytest.mark.smoke
    def test_caseid_1989345(self): # failed
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1) 
        for cmd in [1, 2, 2, 3]:
            self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionStiffnessStyleConfig", 
                                             {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), 
                                                            "styleCmd": cmd}})
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'StfnlvlReq', cmd-1, timeout=1)
            sleep(2)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        valuelist = [i for i in [0, 1, 1, 2] for _ in range(6)]
        self.bgm_eth_inter.ck_signal_values("StfnlvlReq", valuelist)
        self.bgm_eth_inter.ck_period_time("StfnlvlReq", 0.1, permit_fail_times=3)
        
    @allure.title("设置空气悬架刚度调节风格_接口返回校验")
    @pytest.mark.sanity
    def test_caseid_1989346(self): 
        self.sd_tester.change_usage_mode(random.choice([11, 13]))  
        last_value=1
        for cmd in [1, 2, 4, 3, 5, 255]:
            self.dk.set_chassis_service_gear(random.choice([0, 1, 2, 3, 5]))    
            sleep(1)
            resp=0 if cmd in [1, 2, 3] else 1
            value=cmd-1 if cmd in [1, 2, 3] else last_value
            self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionStiffnessStyleConfig", 
                                                  {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), "styleCmd": cmd}}, 
                                                  {"out": resp}) 
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'StfnlvlReq', value, timeout=1)
            last_value=value
            
    @allure.title("设置空气悬架刚度调节风格_打断逻辑_收到新接口调用&满足前置")
    @pytest.mark.full
    def test_caseid_1989347(self):     
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)  
        for cmd in [1, 2, 3]:   
            self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionStiffnessStyleConfig", 
                                             {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), 
                                                            "styleCmd": 2}})
            sleep(0.24)
            self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionStiffnessStyleConfig", 
                                             {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), 
                                                            "styleCmd": cmd}})
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'StfnlvlReq', cmd-1, timeout=1)            
            sleep(2)        
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal() 
        result = self.bgm_eth_inter.get_signal_values("StfnlvlReq")
        assert len(result) > 23 and len(result) < 28, "打断逻辑有误"
           
    @allure.title("设置空气悬架刚度调节风格_打断逻辑_收到新接口调用&不满足前置")
    @pytest.mark.full
    def test_caseid_1989348(self):   
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)  
        for cmd in [4, 5, 255]:   
            self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionStiffnessStyleConfig", 
                                                  {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), "styleCmd": 2}}, 
                                                  {"out": 0}) 
            sleep(0.24)
            self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionStiffnessStyleConfig", 
                                                  {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), "styleCmd": cmd}}, 
                                                  {"out": 1}) 
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'StfnlvlReq', 1, timeout=1)
            sleep(2)        
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal() 
        result = self.bgm_eth_inter.get_signal_values("StfnlvlReq")
        assert len(result) == 18, "打断逻辑有误"
        
    @allure.title("获取&通知空气悬架刚度调节风格信息_取值遍历&下电记忆")
    @pytest.mark.sanity
    def test_caseid_1989349(self):  
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionStiffnessStyleConfig",
                                         {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), 
                                                        "styleCmd": 2}})
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionStiffnessStyleInfo", {}, {"out": {"styleSts": 2, "validity": 0}}, timeout=3)
        self.partner.empty_all(1)
        for cmd in [1, 2, 3]:
            self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionStiffnessStyleConfig", 
                                                 {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), "styleCmd": cmd}}, 
                                                 {"out": 0}, timeout=5) 
            self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionStiffnessStyleInfo",  
                                           {"styleInfo": {"validity":0, "styleSts": cmd}})  
            self.restart_bgm_and_connect_service(SUSPENSION_SERVICE_CLIENT) 
            self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionStiffnessStyleInfo",  
                                           {"styleInfo": {"validity":0, "styleSts": cmd}}) 
              
    @allure.title("空气悬架高度调节停止控制_参数取值遍历&下行以太网校验")
    @pytest.mark.smoke
    def test_caseid_1989352(self): 
        self.dk.set_chassis_service_gear("GearP")
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1) 
        for cmd in [False, True]:
            self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightStopCtrl", 
                                             {"stopCmd": {"sourceId": random.choice([10000, 20000, 2060001]), 
                                                          "isStop": cmd}})
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'EmgHeiStop', int(cmd), timeout=1)
            sleep(2)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        valuelist = [i for i in [0, 1] for _ in range(6)]
        self.bgm_eth_inter.ck_signal_values("EmgHeiStop", valuelist)
        self.bgm_eth_inter.ck_period_time("EmgHeiStop", 0.1, permit_fail_times=3)           
        
    @allure.title("空气悬架高度调节停止控制_接口返回校验")
    @pytest.mark.sanity
    def test_caseid_1989353(self):         
        self.sd_tester.change_usage_mode(random.choice([11, 13]))
        self.dk.set_chassis_service_gear("GearP")
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetGear", {}, {"out": 0})
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightStopCtrl", 
                                              {"stopCmd": {"sourceId": random.choice([10000, 20000, 2060001]), "isStop": True}}, 
                                              {"out": 0}) 
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'EmgHeiStop', 1, timeout=1)
        for gear in [1, 2, 3, 5]:    
            self.dk.set_chassis_service_gear(gear)    
            sleep(0.5)
            self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightStopCtrl",
                                                  {"stopCmd": {"sourceId": random.choice([10000, 20000, 2060001]), "isStop": False}}, 
                                                  {"out": 14}) 
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'EmgHeiStop', 1, timeout=1)

    @allure.title("空气悬架高度调节停止控制_打断逻辑_收到新接口调用&满足前置")
    @pytest.mark.full
    def test_caseid_1989354(self): # SUSPEN: |SetAirSuspensionEasyEntryConfig      
        self.dk.set_chassis_service_gear("GearP")
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1) 
        for cmd in [False, True]:
            self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightStopCtrl", 
                                             {"stopCmd": {"sourceId": random.choice([10000, 20000, 2060001]), "isStop": True}})
            sleep(0.24)
            self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightStopCtrl", 
                                             {"stopCmd": {"sourceId": random.choice([10000, 20000, 2060001]), "isStop": False}})
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'EmgHeiStop', int(cmd), timeout=1)
            sleep(2)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        result = self.bgm_eth_inter.get_signal_values("EmgHeiStop")
        assert len(result) > 14 and len(result) < 19, "打断逻辑有误"
        
    @allure.title("空气悬架高度调节停止控制_打断逻辑_收到新接口调用&不满足前置")
    @pytest.mark.full
    def test_caseid_1989355(self):      
        self.sd_tester.change_usage_mode(random.choice([11, 13]))   
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1) 
        for cmd in [False, True]:          
            self.dk.set_chassis_service_gear("GearP")
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetGear", {}, {"out": 0})
            self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightStopCtrl", 
                                                  {"stopCmd": {"sourceId": random.choice([10000, 20000, 2060001]), "isStop": True}}, 
                                                  {"out": 0}) 
            sleep(0.1)
            self.dk.set_chassis_service_gear("GearR")
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetGear", {}, {"out": 1})
            self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightStopCtrl", 
                                                  {"stopCmd": {"sourceId": random.choice([10000, 20000, 2060001]), "isStop": cmd}}, 
                                                  {"out": 14}) 
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'EmgHeiStop', 1, timeout=1)
            sleep(2)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        result = self.bgm_eth_inter.get_signal_values("EmgHeiStop")
        assert len(result) == 12, "打断逻辑有误"
                                
    @allure.title("获取&通知空气悬架高度等级及运动状态信息_source_StsModAct=0_遍历StsLvlReqRsn")
    @pytest.mark.smoke
    def test_caseid_1989356(self): 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', 5)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, 
                                              {"out": {"source": 5, "validity": 0}}, timeout=3)
        self.partner.empty_all(1)
        for i in range(8):
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', i)
            if i in range(7):
                self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                           {"heightMoveInfo": {"source": i, "validity": 0}})  
            else:
                self.partner.ck_no_event_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                     {"heightMoveInfo": {"source": 6, "validity": 0}})
            
    @allure.title("获取&通知空气悬架高度等级及运动状态信息_source_StsLvlReqRsn取随机值_遍历StsModAct")
    @pytest.mark.sanity
    def test_caseid_1989357(self): 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 3)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, 
                                              {"out": {"source": 9, "validity": 0}}, timeout=3)
        self.partner.empty_all(1)
        for i in range(1, 8):
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', random.choice(range(8)))
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', i)  
            self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                           {"heightMoveInfo": {"source": i+6, "validity": 0}})      
        
    @allure.title("获取&通知空气悬架高度等级及运动状态信息_frontLeftHeightMoveInfo.heightLevelSts_遍历FrntLeLvl")
    @pytest.mark.full
    def test_caseid_1989358(self): 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr08, 'FrntLeLvl', 4)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, 
                                              {"out": {"frontLeftHeightMoveInfo": {"heightLevelSts": 1}}}, timeout=3)
        last_value=1
        dict1={3:2, 4:1, 5:0, 6:20, 7:21}
        self.partner.empty_all(1)
        for i in range(16):
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr08, 'FrntLeLvl', i)
            value = dict1[i] if i in dict1 else last_value
            if value != last_value:
                 self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                {"heightMoveInfo": {"frontLeftHeightMoveInfo": {"heightLevelSts": value}}})
            else:
                self.partner.ck_no_event_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                     {"heightMoveInfo": {"frontLeftHeightMoveInfo": {"heightLevelSts": value}}})
            last_value=value

    @allure.title("获取&通知空气悬架高度等级及运动状态信息_frontLeftHeightMoveInfo.suspensionMoveSts_遍历FrntLeLvlAdjm和AsLvlMov")
    @pytest.mark.sanity
    def test_caseid_1989359(self): 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'FrntLeLvlAdjm', 1)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'AsLvlMov', 2)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, 
                                              {"out": {"frontLeftHeightMoveInfo": {"moveSts": 1}, "vehicleHeightMoveInfo": {"moveSts":1}}}, timeout=3)
        last_value_fr, last_value_veh = 1, 1
        self.partner.empty_all(1)
        for mov in range(4):
            for adjm in range(2):
                self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'FrntLeLvlAdjm', adjm)
                self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'AsLvlMov', mov)
                value_fr = mov-1 if (adjm == 1 and mov in [1, 2]) or (adjm == 0 and mov == 3) else last_value_fr
                value_veh = mov-1 if mov in range(1, 4) else last_value_fr
                logger.info(f"打印当前值: mov={mov}, adjm={adjm}, value_fr={value_fr}, value_veh={value_veh}")
                if value_fr != last_value_fr or value_veh != last_value_veh:
                    self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                   {"heightMoveInfo": {"frontLeftHeightMoveInfo": {"moveSts": value_fr}, 
                                                                       "vehicleHeightMoveInfo": {"moveSts":value_veh}}})
                else:
                    self.partner.ck_no_event_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                   {"heightMoveInfo": {"frontLeftHeightMoveInfo": {"moveSts": value_fr}, 
                                                                       "vehicleHeightMoveInfo": {"moveSts":value_veh}}})
                last_value_fr, last_value_veh = value_fr, value_veh

    @allure.title("获取&通知空气悬架高度等级及运动状态信息_frontRightHeightMoveInfo.heightLevelSts_遍历FrntRiLvl")
    @pytest.mark.smoke
    def test_caseid_1989360(self): 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr08, 'FrntRiLvl', 4)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, 
                                              {"out": {"frontRightHeightMoveInfo": {"heightLevelSts": 1}}}, timeout=3)
        last_value=1
        dict1={3:2, 4:1, 5:0, 6:20, 7:21}
        self.partner.empty_all(1)
        for i in range(16):
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr08, 'FrntRiLvl', i)
            value = dict1[i] if i in dict1 else last_value
            if value != last_value:
                 self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                {"heightMoveInfo": {"frontRightHeightMoveInfo": {"heightLevelSts": value}}})
            else:
                self.partner.ck_no_event_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                     {"heightMoveInfo": {"frontRightHeightMoveInfo": {"heightLevelSts": value}}})
            last_value=value

    @allure.title("获取&通知空气悬架高度等级及运动状态信息_frontRightHeightMoveInfo.suspensionMoveSts_遍历FrntRiLvlAdjm和AsLvlMov")
    @pytest.mark.full
    def test_caseid_1989361(self): 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'FrntRiLvlAdjm', 1)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'AsLvlMov', 2)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, 
                                              {"out": {"frontRightHeightMoveInfo": {"moveSts": 1}, "vehicleHeightMoveInfo": {"moveSts":1}}}, timeout=3)
        last_value_fr, last_value_veh = 1, 1
        self.partner.empty_all(1)
        for mov in range(4):
            for adjm in range(2):
                self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'FrntRiLvlAdjm', adjm)
                self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'AsLvlMov', mov)
                value_fr = mov-1 if (adjm == 1 and mov in [1, 2]) or (adjm == 0 and mov == 3) else last_value_fr
                value_veh = mov-1 if mov in range(1, 4) else last_value_fr
                if value_fr != last_value_fr or value_veh != last_value_veh:
                    self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                   {"heightMoveInfo": {"frontRightHeightMoveInfo": {"moveSts": value_fr}, 
                                                                       "vehicleHeightMoveInfo": {"moveSts":value_veh}}})
                else:
                    self.partner.ck_no_event_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                   {"heightMoveInfo": {"frontRightHeightMoveInfo": {"moveSts": value_fr}, 
                                                                       "vehicleHeightMoveInfo": {"moveSts":value_veh}}})
                last_value_fr, last_value_veh = value_fr, value_veh                    

    @allure.title("获取&通知空气悬架高度等级及运动状态信息_rearLeftHeightMoveInfo.heightLevelSts_遍历FrntRiLvl")
    @pytest.mark.full
    def test_caseid_1989362(self): 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr08, 'ReLeLvl', 4)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, 
                                              {"out": {"rearLeftHeightMoveInfo": {"heightLevelSts": 1}}}, timeout=3)
        last_value=1
        dict1={3:2, 4:1, 5:0, 6:20, 7:21}
        self.partner.empty_all(1)
        for i in range(16):
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr08, 'ReLeLvl', i)
            value = dict1[i] if i in dict1 else last_value
            if value != last_value:
                 self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                {"heightMoveInfo": {"rearLeftHeightMoveInfo": {"heightLevelSts": value}}})
            else:
                self.partner.ck_no_event_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                     {"heightMoveInfo": {"rearLeftHeightMoveInfo": {"heightLevelSts": value}}})
            last_value=value

    @allure.title("获取&通知空气悬架高度等级及运动状态信息_rearLeftHeightMoveInfo.suspensionMoveSts_遍历ReLeLvlAdjm和AsLvlMov")
    @pytest.mark.full
    def test_caseid_1989364(self): 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'ReLeLvlAdjm', 1)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'AsLvlMov', 2)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, 
                                              {"out": {"rearLeftHeightMoveInfo": {"moveSts": 1}, "vehicleHeightMoveInfo": {"moveSts":1}}}, timeout=3)
        last_value_fr, last_value_veh = 1, 1
        self.partner.empty_all(1)
        for mov in range(4):
            for adjm in range(2):
                self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'ReLeLvlAdjm', adjm)
                self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'AsLvlMov', mov)
                value_fr = mov-1 if (adjm == 1 and mov in [1, 2]) or (adjm == 0 and mov == 3) else last_value_fr
                value_veh = mov-1 if mov in range(1, 4) else last_value_fr
                if value_fr != last_value_fr or value_veh != last_value_veh:
                    self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                   {"heightMoveInfo": {"rearLeftHeightMoveInfo": {"moveSts": value_fr}, 
                                                                       "vehicleHeightMoveInfo": {"moveSts":value_veh}}})
                else:
                    self.partner.ck_no_event_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                   {"heightMoveInfo": {"rearLeftHeightMoveInfo": {"moveSts": value_fr}, 
                                                                       "vehicleHeightMoveInfo": {"moveSts":value_veh}}})
                last_value_fr, last_value_veh = value_fr, value_veh   

    @allure.title("获取&通知空气悬架高度等级及运动状态信息_rearRightHeightMoveInfo.heightLevelSts_遍历FrntRiLvl")
    @pytest.mark.full
    def test_caseid_1989363(self): 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr08, 'ReRiLvl', 4)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, 
                                              {"out": {"rearRightHeightMoveInfo": {"heightLevelSts": 1}}}, timeout=3)
        last_value=1
        dict1={3:2, 4:1, 5:0, 6:20, 7:21}
        self.partner.empty_all(1)
        for i in range(16):
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr08, 'ReRiLvl', i)
            value = dict1[i] if i in dict1 else last_value
            if value != last_value:
                 self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                {"heightMoveInfo": {"rearRightHeightMoveInfo": {"heightLevelSts": value}}})
            else:
                self.partner.ck_no_event_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                     {"heightMoveInfo": {"rearRightHeightMoveInfo": {"heightLevelSts": value}}})
            last_value=value

    @allure.title("获取&通知空气悬架高度等级及运动状态信息_rearRightHeightMoveInfo.suspensionMoveSts_遍历ReRiLvlAdjm和AsLvlMov")
    @pytest.mark.full
    def test_caseid_1989365(self): 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'ReRiLvlAdjm', 1)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'AsLvlMov', 2)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, 
                                              {"out": {"rearRightHeightMoveInfo": {"moveSts": 1}, "vehicleHeightMoveInfo": {"moveSts":1}}}, timeout=3)
        last_value_fr, last_value_veh = 1, 1
        self.partner.empty_all(1)
        for mov in range(4):
            for adjm in range(2):
                self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'ReRiLvlAdjm', adjm)
                self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'AsLvlMov', mov)
                value_fr = mov-1 if (adjm == 1 and mov in [1, 2]) or (adjm == 0 and mov == 3) else last_value_fr
                value_veh = mov-1 if mov in range(1, 4) else last_value_fr
                if value_fr != last_value_fr or value_veh != last_value_veh:
                    self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                   {"heightMoveInfo": {"rearRightHeightMoveInfo": {"moveSts": value_fr}, 
                                                                       "vehicleHeightMoveInfo": {"moveSts":value_veh}}})
                else:
                    self.partner.ck_no_event_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                   {"heightMoveInfo": {"rearRightHeightMoveInfo": {"moveSts": value_fr}, 
                                                                       "vehicleHeightMoveInfo": {"moveSts":value_veh}}})
                last_value_fr, last_value_veh = value_fr, value_veh   

    @allure.title("获取&通知空气悬架高度等级及运动状态信息_vehicleHeightMoveInfo.heightLevelSts_四个位置信号同时遍历")
    @pytest.mark.sanity
    def test_caseid_1989368(self): 
        for signal in ["FrntLeLvl", "FrntRiLvl", "ReLeLvl", "ReRiLvl"]:
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr08, signal, 6)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, 
                                              {"out": {"vehicleHeightMoveInfo": {"heightLevelSts":20}}}, timeout=3)
        self.partner.empty_all(1)
        last_value=20
        dict1={3:2, 4:1, 5:0, 6:20, 7:21}
        for i in range(16):
            for signal in ["FrntLeLvl", "FrntRiLvl", "ReLeLvl", "ReRiLvl"]:
                self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr08, signal, i)
            value = dict1[i] if i in dict1 else last_value
            if value != last_value:
                 self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                {"heightMoveInfo": {"vehicleHeightMoveInfo": {"heightLevelSts": value}}})
            else:
                self.partner.ck_no_event_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                     {"heightMoveInfo": {"vehicleHeightMoveInfo": {"heightLevelSts": value}}})
            last_value=value
            
    @allure.title("获取&通知空气悬架高度等级及运动状态信息_vehicleHeightMoveInfo.moveSts_遍历AsLvlMov")
    @pytest.mark.full
    def test_caseid_1989367(self): 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'AsLvlMov', 2)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, 
                                              {"out": {"vehicleHeightMoveInfo": {"moveSts":1}}}, timeout=3)
        self.partner.empty_all(1)
        for i in range(4):
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'AsLvlMov', i)
            if i == 0:
                self.partner.ck_no_event_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                                     {"heightMoveInfo": {"vehicleHeightMoveInfo": {"moveSts": 1}}})
            else:
                self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                               {"heightMoveInfo": {"vehicleHeightMoveInfo": {"moveSts": i-1}}})
                                                                        
    @allure.title("获取&通知空气悬架高度等级及运动状态信息_启动场景_启动后无任何信号上报")
    @pytest.mark.full
    def test_caseid_1989383(self): 
        for signal in ["FrntLeLvl", "FrntRiLvl", "ReLeLvl", "ReRiLvl"]:
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr08, signal, 6)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'AsLvlMov', 2)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 2)
        sleep(2)
        data=self.partner.send_request_and_return_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {})["out"]
        self.restart_bgm_and_connect_service(SUSPENSION_SERVICE_CLIENT, resume_all_bus=False) 
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, 
                                              {"out": {"source": 255, "validity": 1, 
                                                       "vehicleHeightMoveInfo": {"heightLevelSts": 255, "moveSts": 255},
                                                       "frontLeftHeightMoveInfo": {"heightLevelSts": 255, "moveSts": 255},
                                                       "frontRightHeightMoveInfo": {"heightLevelSts": 255, "moveSts": 255},
                                                       "rearLeftHeightMoveInfo": {"heightLevelSts": 255, "moveSts": 255},
                                                       "rearRightHeightMoveInfo": {"heightLevelSts": 255, "moveSts": 255}}}, timeout=5)
        self.ipdu.resume_all_bus_send()
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", {"heightMoveInfo": data}, timeout=5)
    
    @allure.title("获取&通知空气悬架高度控制禁用信息_inhibitSts_遍历SUMLvlInhb")
    @pytest.mark.sanity
    def test_caseid_1989385(self): 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'SUMLvlInhb', 2)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightInhibitInfo", {}, 
                                              {"out": {"inhibitSts":2, "validity":0}}, timeout=3)
        self.partner.empty_all(1)
        for i in range(4):
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'SUMLvlInhb', i)
            self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                           {"inhibitInfo": {"inhibitSts":i, "validity":0}})
        
    @allure.title("获取&通知空气悬架高度控制禁用信息_inhibitFunctionSts_遍历LvlCtrlInhbnDir")
    @pytest.mark.smoke
    def test_caseid_1989386(self): 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'LvlCtrlInhbnDir', 2)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightInhibitInfo", {}, 
                                              {"out": {"inhibitFunctionSts":2, "validity":0}}, timeout=3)  
        self.partner.empty_all(1)
        for i in range(16):
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'LvlCtrlInhbnDir', i)
            if i in range(9):
                self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                               {"inhibitInfo": {"inhibitFunctionSts":i, "validity":0}})
            else:
                self.partner.ck_no_event_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                                     {"inhibitInfo": {"inhibitFunctionSts":8, "validity":0}})

    @allure.title("获取&通知空气悬架高度控制禁用信息_validity=4_ChassisCAN2::0x213信号丢失")
    @pytest.mark.full
    def test_caseid_1989387(self): 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'SUMLvlInhb', 2)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'LvlCtrlInhbnDir', 2)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'LvlCtrlInhbnRsn', 2)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightInhibitInfo", {}, 
                                              {"out": {"inhibitSts":2, "inhibitFunctionSts":2, "inhibitReasonSts":2, "validity":0}}, timeout=3)     
        self.partner.empty_all(1)
        self.ipdu.pause_bus_send("chassiscan2")
        self.partner.ck_coming_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                       {"inhibitInfo": {"inhibitSts":2, "inhibitFunctionSts":2, "inhibitReasonSts":2, "validity":4}}, timeout=2.5)
        self.ipdu.resume_bus_send("chassiscan2")   
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                       {"inhibitInfo": {"inhibitSts":2, "inhibitFunctionSts":2, "inhibitReasonSts":2, "validity":0}}, timeout=3) 
    
    @allure.title("获取&通知空气悬架高度控制禁用信息_validity=1_启动后无任何信号上报&默认值校验")
    @pytest.mark.full
    def test_caseid_1989388(self): 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'SUMLvlInhb', 2)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'LvlCtrlInhbnDir', 2)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'LvlCtrlInhbnRsn', 2)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightInhibitInfo", {}, 
                                              {"out": {"inhibitSts":2, "inhibitFunctionSts":2, "inhibitReasonSts":2, "validity":0}}, timeout=3)     
        sleep(2)
        self.restart_bgm_and_connect_service(SUSPENSION_SERVICE_CLIENT, resume_all_bus=False) 
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightInhibitInfo", {}, 
                                              {"out": {"inhibitSts":255, "inhibitFunctionSts":255, "inhibitReasonSts":255, "validity":1}}, timeout=3)     
        self.ipdu.resume_all_bus_send()
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                       {"inhibitInfo": {"inhibitSts":2, "inhibitFunctionSts":2, "inhibitReasonSts":2, "validity":0}}, timeout=5)        
        
    def set_speed_and_source(self, speed=0.0, rsn=0, act=0, source=0, sleeptime=1):
        '''设置空气悬架高度等级 前置条件处理'''
        # 实际车速状态 SpeedChanged.speed
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', speed) #车速值给了0 输入浮点数  /0.00391=信号值 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetSpeed", {}, {"out": {"speed": speed, "isvalid": 1}}, timeout=3)
        # 空气悬架高度等级及运动状态信息 AirSuspensionHeightMoveInfo.heightMoveInfo.source 悬架当前控制源
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', act)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', rsn)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {},
                                              {"out": {"source": source, "validity": 0}}, timeout=3)
        sleep(sleeptime)
        
    @allure.title("设置空气悬架高度等级_前置条件判断SetResponse=1_参数suspensionId不在有效范围")
    @pytest.mark.full
    def test_caseid_1989479(self): 
        self.set_speed_and_source(speed=0.0, rsn=0, act=0, source=0, sleeptime=1)
        for id in list(range(1, 9)) + [255]:
            if id == 255: #当前仅255有效
                self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                                      {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), 
                                                                     "heightCmd": [{"suspensionId": id, "heightLevelCmd": random.choice([0, 1, 2, 20, 21])}]}}, 
                                                      {"out": 0})
            else:
                self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                                      {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), 
                                                                     "heightCmd": [{"suspensionId": id, "heightLevelCmd": random.choice([0, 1, 2, 20, 21])}]}}, 
                                                      {"out": 1})        
        # 补充 heightCmd 中既包含有效值，又包含无效值
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                                      {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), 
                                                                     "heightCmd": [{"suspensionId": 255, "heightLevelCmd": random.choice([0, 1, 2, 20, 21])},
                                                                                   {"suspensionId": random.choice(range(1, 9)), "heightLevelCmd": random.choice([0, 1, 2, 20, 21])}]}}, 
                                                      {"out": 1})                

    @allure.title("设置空气悬架高度等级_前置条件判断SetResponse=1_参数heightCmd不在有效范围")
    @pytest.mark.full
    def test_caseid_1989480(self): 
        self.set_speed_and_source(speed=0.0, rsn=0, act=0, source=0, sleeptime=1)         
        for cmd in list(range(0, 6)) + list(range(20, 25)) + [255]:
            if cmd in [0, 1, 2, 20, 21]:
                self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                                      {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), 
                                                                     "heightCmd": [{"suspensionId": 255, "heightLevelCmd": cmd}]}}, 
                                                      {"out": 0})
                sleep(1.5) # 防止接口被占用
            else:
                self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                                      {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), 
                                                                     "heightCmd": [{"suspensionId": 255, "heightLevelCmd": cmd}]}}, 
                                                      {"out": 1})      
                 
    @allure.title("设置空气悬架高度等级_前置条件判断SetResponse=13_请求的悬架高度与当前车速不匹配")
    @pytest.mark.full
    def test_caseid_1989488(self): # 35km/h=9.72m/s 110km/h=30.55m/s 5km/h=1.39m/s
        self.set_speed_and_source(speed=0.0, rsn=0, act=0, source=0, sleeptime=1)         
        for cmd in [0, 1, 2, 20, 21]:   
            for speed in [1.3, 30.5, 30.6, 1.4, 9.7, 9.8, 0.0]:
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', speed)
                self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetSpeed", {}, {"out": {"speed": speed, "isvalid": 1}}, timeout=3)
                if (cmd == 21 and speed >= 9.72) or (cmd == 2 and (speed >= 1.39 and speed <= 30.55)):
                    self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                                      {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), 
                                                                     "heightCmd": [{"suspensionId": 255, "heightLevelCmd": cmd}]}}, 
                                                      {"out": 13})
                else:    
                    self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                                      {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), 
                                                                     "heightCmd": [{"suspensionId": 255, "heightLevelCmd": cmd}]}}, 
                                                      {"out": 0})
                    sleep(1.5)

    @allure.title("设置空气悬架高度等级_前置条件判断SetResponse=9_当前控制源不在有效范围")
    @pytest.mark.sanity
    def test_caseid_1989491(self): 
        self.set_speed_and_source(speed=0.0, rsn=4, act=1, source=7, sleeptime=1) 
        for i in range(8): # AirSuspensionHeightMoveInfo.heightMoveInfo.source
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', i)
            sleep(2)
            self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                                  {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), 
                                                                 "heightCmd": [{"suspensionId": 255, "heightLevelCmd": random.choice([0, 1, 2, 20, 21])}]}}, 
                                                  {"out": 9})
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)
        for i in range(7):
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', i)
            sleep(2)
            if i == 4:
                self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                                  {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), 
                                                                 "heightCmd": [{"suspensionId": 255, "heightLevelCmd": random.choice([0, 1, 2, 20, 21])}]}}, 
                                                  {"out": 9})
            else:
                self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                                  {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), 
                                                                 "heightCmd": [{"suspensionId": 255, "heightLevelCmd": random.choice([0, 1, 2, 20, 21])}]}}, 
                                                  {"out": 0})
           
    @allure.title("设置空气悬架高度等级_前置条件判断SetResponse=9_高优先级占用&打断后优先级信号的发送逻辑校验")
    @pytest.mark.sanity
    def test_caseid_1989495(self): 
        self.set_speed_and_source(speed=0.0, rsn=0, act=0, source=0, sleeptime=1) 
        list1=["HeiReqOfFLHeightLevelPriority", "HeiReqOfFRHeightLevelPriority", "HeiReqOfRLHeightLevelPriority", "HeiReqOfRRHeightLevelPriority"]  
        for before_id in [10000, 20000, 2060001]:
            for last_id in [10000, 20000, 2060001]:
                self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                                  {"configCmd": {"sourceId": before_id, "heightCmd": [{"suspensionId": 255, "heightLevelCmd": random.choice([0, 1, 2, 20, 21])}]}}, 
                                                  {"out": 0})
                sleep(0.15)
                if before_id in [10000, 20000] and last_id == 2060001: # 优先级判断后，接口调用返回9
                    value = 5 if before_id == 2060001 else 2
                    self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                                    {"configCmd": {"sourceId": last_id, "heightCmd": [{"suspensionId": 255, "heightLevelCmd": random.choice([0, 1, 2, 20, 21])}]}}, 
                                                    {"out": 9})
                    for signal_name in list1:
                        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, signal_name, value, timeout=0.5)
                else: # 打断
                    value = 5 if last_id == 2060001 else 2
                    self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                                    {"configCmd": {"sourceId": last_id, "heightCmd": [{"suspensionId": 255, "heightLevelCmd": random.choice([0, 1, 2, 20, 21])}]}}, 
                                                    {"out": 0})
                    for signal_name in list1:
                        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, signal_name, value, timeout=0.5)
                    sleep(1.5)
        
    @allure.title("设置空气悬架高度等级_suspensionId=255_sourceId_参数取值遍历&下行以太网校验")
    @pytest.mark.smoke
    def test_caseid_1989505(self): 
        self.set_speed_and_source(speed=0.0, rsn=0, act=0, source=0, sleeptime=1)       
        list1=["HeiReqOfFLHeightLevelPriority", "HeiReqOfFRHeightLevelPriority", "HeiReqOfRLHeightLevelPriority", "HeiReqOfRRHeightLevelPriority"]    
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1) 
        for id in [10000, 20000, 2060001]:
            self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                             {"configCmd": {"sourceId": id, "heightCmd": [{"suspensionId": 255, "heightLevelCmd": random.choice([0, 1, 2, 20, 21])}]}})
            value = 5 if id == 2060001 else 2
            for signal_name in list1:
                self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, signal_name, value, timeout=0.5)
            sleep(2)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        valuelist = [i for i in [2, 2, 5] for _ in range(7)]
        for signal_name in list1:
            self.bgm_eth_inter.ck_signal_values(signal_name, valuelist)
            self.bgm_eth_inter.ck_period_time(signal_name, 0.1, permit_fail_times=3)           
        
    @allure.title("设置空气悬架高度等级_suspensionId=255_heightLevelCmd_参数取值遍历&下行以太网校验")
    @pytest.mark.smoke
    def test_caseid_1989506(self): 
        self.set_speed_and_source(speed=0.0, rsn=0, act=0, source=0, sleeptime=1)       
        list1=["HeiReqOfFLHeightLevelReq", "HeiReqOfFRHeightLevelReq", "HeiReqOfRLHeightLevelReq", "HeiReqOfRRHeightLevelReq"]    
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1) 
        dict1={0:5, 1:4, 2:3, 20:6, 21:7}
        for cmd	 in [0, 1, 2, 20, 21]:
            self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                             {"configCmd": {"sourceId": random.choice([10000, 20000, 2060001]), 
                                                            "heightCmd": [{"suspensionId": 255, "heightLevelCmd": cmd}]}})
            for signal_name in list1:
                self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, signal_name, dict1[cmd], timeout=0.5)
            sleep(2)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        valuelist = [5,5,5,5,5,5,15, 4,4,4,4,4,4,15, 3,3,3,3,3,3,15, 6,6,6,6,6,6,15, 7,7,7,7,7,7,15]
        for signal_name in list1:
            self.bgm_eth_inter.ck_signal_values(signal_name, valuelist)
            self.bgm_eth_inter.ck_period_time(signal_name, 0.1, permit_fail_times=4)             

    @allure.title("设置空气悬架高度等级_suspensionId=255_打断逻辑_收到新接口调用&满足前置")
    @pytest.mark.full
    def test_caseid_1989520(self): 
        self.set_speed_and_source(speed=0.0, rsn=0, act=0, source=0, sleeptime=1)   
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1) 
        for cmd	 in [0, 1]:
            self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                             {"configCmd": {"sourceId": 20000, "heightCmd": [{"suspensionId": 255, "heightLevelCmd": 1}]}})
            sleep(0.24)
            self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                             {"configCmd": {"sourceId": 10000, "heightCmd": [{"suspensionId": 255, "heightLevelCmd": cmd}]}})
            sleep(2)  
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        result1 = self.bgm_eth_inter.get_signal_values("HeiReqOfFLHeightLevelPriority")
        result2 = self.bgm_eth_inter.get_signal_values("HeiReqOfFLHeightLevelReq")
        assert len(result1) > 17 and len(result1) < 21, "打断逻辑有误"
        assert len(result2) > 17 and len(result2) < 21, "打断逻辑有误"

    @allure.title("设置空气悬架模式_前置条件判断SetResponse=1_参数modeCmd不在有效范围")
    @pytest.mark.full
    def test_caseid_1989524(self):
        # 空气悬架高度等级及运动状态信息 AirSuspensionHeightMoveInfo.heightMoveInfo.source 悬架当前控制源
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', 0)
        sleep(2)
        for cmd in range(5):
            if cmd in [1, 2, 0]:
                self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionModeConfig", {"configCmd": {"modeCmd": cmd}}, {"out": 0})
            else:
                self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionModeConfig", {"configCmd": {"modeCmd": cmd}}, {"out": 1})
                
    @allure.title("设置空气悬架模式_前置条件判断SetResponse=9_当前控制源不在有效范围")
    @pytest.mark.sanity
    def test_caseid_1989525(self):
        # 空气悬架高度等级及运动状态信息 AirSuspensionHeightMoveInfo.heightMoveInfo.source 悬架当前控制源
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 1)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', 4)
        sleep(2)                
        for i in range(8): # AirSuspensionHeightMoveInfo.heightMoveInfo.source
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', i)
            sleep(2)
            self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionModeConfig", {"configCmd": {"modeCmd": random.choice([0, 1, 2])}}, {"out": 9})
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)
        for i in range(7):
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', i)
            sleep(2)
            if i == 4:
                self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionModeConfig", {"configCmd": {"modeCmd": random.choice([0, 1, 2])}}, {"out": 9})
            else:
                self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionModeConfig", {"configCmd": {"modeCmd": random.choice([0, 1, 2])}}, {"out": 0})

    def set_ModeConfig(self, priority=2, heigh_config=20, stiffness_config=1, level_config=0):
        '''设置空气悬架模式后的接口调用'''
        # 设置空气悬架高度等级 SetAirSuspensionHeightConfig
        list1=["HeiReqOfFLHeightLevelPriority", "HeiReqOfFRHeightLevelPriority", "HeiReqOfRLHeightLevelPriority", "HeiReqOfRRHeightLevelPriority"]    
        list2=["HeiReqOfFLHeightLevelReq", "HeiReqOfFRHeightLevelReq", "HeiReqOfRLHeightLevelReq", "HeiReqOfRRHeightLevelReq"]    
        dict1={0:5, 1:4, 2:3, 20:6, 21:7, 15:15}
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, random.choice(list1), priority, timeout=0.5)
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, random.choice(list2), dict1[heigh_config], timeout=0.5)           
        # 设置空气悬架刚度调节风格信息 SetAirSuspensionStiffnessStyleConfig
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'StfnlvlReq', stiffness_config, timeout=1)    
        # 设置悬架减震阻尼等级 SetSuspensionLevel
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', level_config, timeout=1)     
                
    @allure.title("设置空气悬架模式_档位判断_D/R档下遍历modeCmd=1/2/3_立即执行配置项的接口调用")
    @pytest.mark.smoke
    def test_caseid_1989526(self):
        self.sd_tester.change_usage_mode(random.choice([11, 13]))
        # 空气悬架高度等级及运动状态信息 AirSuspensionHeightMoveInfo.heightMoveInfo.source 悬架当前控制源
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)         
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', 6)
        sleep(2)
        dict1={0:20, 1:0, 2:1}
        for gear in [1, 3]:
            self.dk.set_chassis_service_gear(gear)
            sleep(2)
            for cmd in range(3):
                self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionModeConfig", {"configCmd": {"modeCmd": cmd}})
                logger.info(f"打印当前返回值cmd={cmd},cmd-1={cmd-1}")
                self.set_ModeConfig(priority=2, heigh_config=dict1[cmd], stiffness_config=cmd, level_config=cmd)
                
    @allure.title("设置空气悬架模式_重启场景_D/R档下控制源为便捷上下车_调用接口再重启不下发记忆配置")
    @pytest.mark.full
    def test_caseid_1989528(self):
        self.sd_tester.change_usage_mode(random.choice([11, 13]))
        self.dk.set_chassis_service_gear(random.choice([1, 3]))
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)         
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', 6)
        sleep(2)
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionModeConfig", {"configCmd": {"modeCmd": 1}})
        self.set_ModeConfig(priority=2, heigh_config=0, stiffness_config=1, level_config=1)
        sleep(2)
        self.restart_bgm_and_connect_service(SUSPENSION_SERVICE_CLIENT, resume_all_bus=False) 
        sleep(5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1) 
        self.ipdu.resume_all_bus_send()
        sleep(5)
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 0, timeout=1)     
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("HeiReqOfFLHeightLevelReq", [])
        
    @allure.title("设置空气悬架模式_重启场景_D/R档下控制源满足条件_调用接口再重启需下发记忆配置")
    @pytest.mark.full
    def test_caseid_1989529(self):
        self.sd_tester.change_usage_mode(random.choice([11, 13]))
        self.dk.set_chassis_service_gear(random.choice([1, 3]))
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)         
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', 0)
        sleep(2)
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionModeConfig", {"configCmd": {"modeCmd": 2}})
        self.set_ModeConfig(priority=2, heigh_config=1, stiffness_config=2, level_config=2)
        sleep(2)
        self.restart_bgm_and_connect_service(SUSPENSION_SERVICE_CLIENT, resume_all_bus=False) 
        sleep(5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1) 
        self.ipdu.resume_all_bus_send()
        sleep(5)
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 2, timeout=1)     
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("HeiReqOfFLHeightLevelReq", [4,4,4,4,4,4,15])
        
    @allure.title("设置空气悬架模式_重启场景_D/R档下控制源满足条件_调用接口再重启_档位上来前控制源不满足_不下发记忆配置")
    @pytest.mark.full
    def test_caseid_1989530(self):
        self.sd_tester.change_usage_mode(random.choice([11, 13]))
        self.dk.set_chassis_service_gear(random.choice([1, 3]))
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)         
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', 0)
        sleep(2)
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionModeConfig", {"configCmd": {"modeCmd": 0}})
        self.set_ModeConfig(priority=2, heigh_config=20, stiffness_config=0, level_config=0)
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(3)
        self.restart_bgm_and_connect_service(SUSPENSION_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False) 
        sleep(5)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', 4)   
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, 
                                              {"out": {"source": 4, "validity": 0}}, timeout=5)             
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1) 
        self.ipdu.resume_all_bus_send()
        sleep(5)
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 0, timeout=1)     
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("HeiReqOfFLHeightLevelReq", [])

    @allure.title("设置空气悬架模式_D/R档下控制源满足条件_调用接口后修改控制源至不满足再到满足_不重复下发配置")
    @pytest.mark.full
    def test_caseid_1989592(self):
        self.sd_tester.change_usage_mode(random.choice([11, 13]))
        self.dk.set_chassis_service_gear(random.choice([1, 3]))
        sleep(2)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)         
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', 0)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, {"out": {"source": 0, "validity": 0}}, timeout=3)   
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionModeConfig", {"configCmd": {"modeCmd": 0}})
        self.set_ModeConfig(priority=2, heigh_config=20, stiffness_config=0, level_config=0)
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": 5})   
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 5, timeout=1)    
        for i in [4, 1]:
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', i)
            self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, {"out": {"source": i, "validity": 0}}, timeout=3)
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 5, timeout=1) 
              
    @allure.title("设置空气悬架模式_档位判断_P/N/NA档下遍历modeCmd=1/2/3_不执行配置项的接口调用")
    @pytest.mark.full
    def test_caseid_1989527(self):
        self.dk.set_chassis_service_gear("GearN")
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)         
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', 0)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, {"out": {"source": 0, "validity": 0}}, timeout=3)
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionStiffnessStyleConfig", {"configCmd": {"sourceId": 10000, "styleCmd": 3}})        
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                             {"configCmd": {"sourceId": 2060001, "heightCmd": [{"suspensionId": 255, "heightLevelCmd": 2}]}})
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": 5})   
        self.sd_tester.change_usage_mode(random.choice([11, 13]))
        self.bgm_eth_inter.start_bgm_tcpdump()
        for gear in [0, 2, 5]:
            self.dk.set_chassis_service_gear(gear)
            sleep(2)
            for cmd in range(3):
                self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionModeConfig", {"configCmd": {"modeCmd": cmd}})
                logger.info(f"打印当前返回值cmd={cmd},cmd-1={cmd-1}")
                self.set_ModeConfig(priority=5, heigh_config=15, stiffness_config=2, level_config=5)
    
    @allure.title("设置空气悬架模式_档位判断_档位不满足时设置悬架模式_多次切换至D/R档后均下发数据")
    @pytest.mark.full
    def test_caseid_1989551(self):
        self.sd_tester.change_usage_mode(random.choice([11, 13]))
        self.dk.set_chassis_service_gear(2)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)         
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', 1)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, {"out": {"source": 1, "validity": 0}}, timeout=3)
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": 5})   
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                             {"configCmd": {"sourceId": 2060001, "heightCmd": [{"suspensionId": 255, "heightLevelCmd": 2}]}})
        sleep(2)
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionModeConfig", {"configCmd": {"modeCmd": 0}})
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 5, timeout=1)     
        for gear in [0, 2, 5]:
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": 3})   
            self.dk.set_chassis_service_gear(gear)
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 3, timeout=1)     
            self.dk.set_chassis_service_gear(random.choice([1, 3]))
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 0, timeout=1)     
        
    @allure.title("设置空气悬架模式_档位判断_档位满足时设置悬架模式_切换档位仍满足时不重复下发数据")
    @pytest.mark.full
    def test_caseid_1989552(self):      
        self.sd_tester.change_usage_mode(random.choice([11, 13]))
        self.dk.set_chassis_service_gear(1) 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)         
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', 2)
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": 5})     
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, {"out": {"source": 2, "validity": 0}}, timeout=3)
        sleep(1)
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                             {"configCmd": {"sourceId": 2060001, "heightCmd": [{"suspensionId": 255, "heightLevelCmd": 2}]}})
        sleep(2)
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionModeConfig", {"configCmd": {"modeCmd": 0}})
        self.set_ModeConfig(priority=2, heigh_config=20, stiffness_config=0, level_config=0)
        for gear in [3, 1]:
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": 4})     
            self.dk.set_chassis_service_gear(gear)
            sleep(1)
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 4, timeout=1)

    @allure.title("设置空气悬架模式_档位判断_档位不满足时设置悬架模式_切换至D/R档后控制源取值遍历")
    @pytest.mark.sanity
    def test_caseid_1989553(self):      
        self.sd_tester.change_usage_mode(random.choice([11, 13]))
        self.dk.set_chassis_service_gear(0) 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)         
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', 6)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, {"out": {"source": 6, "validity": 0}}, timeout=3)
        sleep(1)
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionModeConfig", {"configCmd": {"modeCmd": 1}})
        sleep(2)
        for i in range(8): # AirSuspensionHeightMoveInfo.heightMoveInfo.source
            self.dk.set_chassis_service_gear(random.choice([0, 2, 5])) 
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', i) # 控制源均不满足
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": 4})     
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 4, timeout=1)
            sleep(1)
            self.dk.set_chassis_service_gear(random.choice([1, 3])) #切换D/R后不下发数据
            sleep(1)
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 4, timeout=1)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)
        for i in range(7):
            self.dk.set_chassis_service_gear(random.choice([0, 2, 5])) 
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', i)
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": 3})   
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 3, timeout=1)  
            sleep(1)
            self.dk.set_chassis_service_gear(random.choice([1, 3])) #切换D/R后不下发数据
            sleep(1)            
            if i in [4, 6]: # 控制源不满足
                self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 3, timeout=1)  
            else: # 控制源满足
                self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 1, timeout=1)  
                
    @allure.title("设置空气悬架模式_重启场景_档位不满足时设置悬架模式_重启后等待档位满足时下发记忆配置")
    @pytest.mark.full
    def test_caseid_1989575(self):
        self.sd_tester.change_usage_mode(random.choice([11, 13]))
        self.dk.set_chassis_service_gear(random.choice([0, 2, 5])) 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)         
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', 5)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, {"out": {"source": 5, "validity": 0}}, timeout=3)
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": 2})   
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 2, timeout=1)  
        sleep(1)
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionModeConfig", {"configCmd": {"modeCmd": 1}})
        sleep(2)
        self.restart_bgm_and_connect_service(SUSPENSION_SERVICE_CLIENT) 
        sleep(3)
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 0, timeout=1)  # 悬架阻尼上电初始=0
        self.dk.set_chassis_service_gear(random.choice([1, 3]))
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 1, timeout=2)                                                                  
        
    @allure.title("获取&通知空气悬架模式信息_参数取值遍历&下电记忆")
    @pytest.mark.sanity
    def test_caseid_1989579(self):
        self.sd_tester.change_usage_mode(random.choice([11, 13]))
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)         
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', 0)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, {"out": {"source": 0, "validity": 0}}, timeout=3)
        for cmd in range(5):
            self.dk.set_chassis_service_gear(random.choice([0, 1])) 
            self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionModeConfig", {"configCmd": {"modeCmd": cmd}}, timeout=1.5)
            sleep(2)
            self.restart_bgm_and_connect_service(SUSPENSION_SERVICE_CLIENT) 
            value = cmd if cmd < 3 else 2
            self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionModeInfo", {"modeInfo": {"modeSts": value}}) 
            
    @allure.title("获取&通知空气悬架模式信息_出厂默认值&档位满足时下发配置")
    @pytest.mark.full
    def test_caseid_1989580(self):
        self.sd_tester.change_usage_mode(random.choice([11, 13]))
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)         
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', 0)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, {"out": {"source": 0, "validity": 0}}, timeout=3)
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionModeConfig", {"configCmd": {"modeCmd": 2}})   
        self.partner.empty_all(2)     
        self.del_s2s_db()  # 删除数据库
        sleep(2)
        self.restart_bgm_and_connect_service(SUSPENSION_SERVICE_CLIENT) # 上电后需要主动通知一次
        # 空气悬架模式信息
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionModeInfo", {"modeInfo": {"modeSts": 1}}) 
        self.dk.set_chassis_service_gear(random.choice([1, 3])) 
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 1, timeout=2)          
  
                                                  
    # # 轻松载物功能4.0上 SOA-28806 
    # @allure.title("设置轻松载物功能开启关闭_参数取值遍历&下行以太网校验")
    # @pytest.mark.smoke
    # def test_caseid_1989271(self):      
    #     self.dk.set_chassis_service_gear("GearP")
    #     self.bgm_eth_inter.start_bgm_tcpdump()
    #     sleep(1) 
    #     for i in [0, 0, 1, 1]:
    #         self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetEasyLoadingConfig", {"configCmd": {"isOn": bool(i)}})
    #         self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'CargoReq', i, timeout=1)
    #         sleep(2)
    #     sleep(1)
    #     self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
    #     valuelist = [i for i in [0, 0, 1, 1] for _ in range(6)]
    #     self.bgm_eth_inter.ck_signal_values("CargoReq", valuelist)
    #     self.bgm_eth_inter.ck_period_time("CargoReq", 0.1, permit_fail_times=3)

    # @allure.title("设置轻松载物功能开启关闭_接口返回校验")
    # @pytest.mark.sanity
    # def test_caseid_1989272(self):         
    #     self.sd_tester.change_usage_mode(random.choice([11, 13]))
    #     self.dk.set_chassis_service_gear("GearP")
    #     self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetEasyLoadingConfig", {"configCmd": {"isOn": False}}, {"out": 0}) 
    #     self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'CargoReq', 0, timeout=1)
    #     for gear in [1, 2, 3, 5]:    
    #         self.dk.set_chassis_service_gear(gear)    
    #         sleep(0.5)
    #         self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetEasyLoadingConfig", {"configCmd": {"isOn": random.choice([True, False])}}, {"out": 14}) 
    #         self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'CargoReq', 0, timeout=1)

    # @allure.title("设置轻松载物功能开启关闭_打断逻辑_收到新接口调用&满足前置")
    # @pytest.mark.full
    # def test_caseid_1989273(self):         
    #     self.dk.set_chassis_service_gear("GearP")
    #     self.bgm_eth_inter.start_bgm_tcpdump()
    #     sleep(1) 
    #     for i in [True, False]:
    #         self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetEasyLoadingConfig", {"configCmd": {"isOn": False}})
    #         sleep(0.24)
    #         self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetEasyLoadingConfig", {"configCmd": {"isOn": i}})
    #         self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'CargoReq', int(i), timeout=1)
    #         sleep(2)
    #     sleep(1)
    #     self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
    #     result = self.bgm_eth_inter.get_signal_values("CargoReq")
    #     assert len(result) > 14 and len(result) < 19, "打断逻辑有误"
        
    # @allure.title("设置轻松载物功能开启关闭_打断逻辑_收到新接口调用&不满足前置")
    # @pytest.mark.full
    # def test_caseid_1989274(self):      
    #     self.sd_tester.change_usage_mode(random.choice([11, 13]))   
    #     self.bgm_eth_inter.start_bgm_tcpdump()
    #     sleep(1) 
    #     for i in [False, True]:          
    #         self.dk.set_chassis_service_gear("GearP")
    #         self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetGear", {}, {"out": 1})
    #         self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetEasyLoadingConfig", {"configCmd": {"isOn": True}}, {"out": 0}) 
    #         sleep(0.1)
    #         self.dk.set_chassis_service_gear("GearD")
    #         self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetGear", {}, {"out": 3})
    #         self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetEasyLoadingConfig", {"configCmd": {"isOn": i}}, {"out": 14}) 
    #         self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'CargoReq', 0, timeout=1)
    #         sleep(2)
    #     sleep(1)
    #     self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
    #     result = self.bgm_eth_inter.get_signal_values("CargoReq")
    #     assert len(result) == 12, "打断逻辑有误"   
        
    @allure.title("获取&通知空气悬架高度等级及运动状态信息_validity_ChassisCAN2::0x062信号丢失")
    @pytest.mark.full
    def test_caseid_1989369(self): # 0x062 FrntLeLvl      
        for signal in ["FrntLeLvl", "FrntRiLvl", "ReLeLvl", "ReRiLvl"]:
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr08, signal, 6)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 1)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, 
                                              {"out": {"source": 7, "validity": 0,
                                                       "vehicleHeightMoveInfo": {"heightLevelSts":20}}}, timeout=3)
        self.partner.empty_all(15) # 前置用例重启后，15s不检测信号丢失
        self.ipdu.stop_send_pdu("chassiscan2", 0x062)     
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                       {"heightMoveInfo": {"source": 7, "validity": 4,
                                                           "vehicleHeightMoveInfo": {"heightLevelSts":20}}})   
        sleep(2)   
        self.restart_bgm_and_connect_service(SUSPENSION_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False) 
        sleep(3)
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                       {"heightMoveInfo": {"source": 7, "validity": 0,
                                                           "vehicleHeightMoveInfo": {"heightLevelSts":255}}})      
        self.ipdu.resume_bus_send("chassiscan2")  
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo",
                                       {"heightMoveInfo": {"source": 7, "validity": 0,
                                                           "vehicleHeightMoveInfo": {"heightLevelSts":20}}})    
    
    @allure.title("获取&通知空气悬架高度等级及运动状态信息_validity_ChassisCAN2::0x213信号丢失")
    @pytest.mark.full
    def test_caseid_1989370(self): # 0x213 StsModAct/StsLvlReqRsn/AsLvlMov
        for signal in ["FrntLeLvl", "FrntRiLvl", "ReLeLvl", "ReRiLvl"]:
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr08, signal, 6)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 1) 
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, 
                                              {"out": {"source": 7, "validity": 0,
                                                       "vehicleHeightMoveInfo": {"heightLevelSts":20}}}, timeout=3)
        self.partner.empty_all(15) # 前置用例重启后，15s不检测信号丢失
        self.ipdu.stop_send_pdu("chassiscan2", 0x213)     
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                       {"heightMoveInfo": {"source": 7, "validity": 4,
                                                           "vehicleHeightMoveInfo": {"heightLevelSts":20}}})    
        sleep(2)  
        self.restart_bgm_and_connect_service(SUSPENSION_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False) 
        sleep(3)
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo",
                                       {"heightMoveInfo": {"source": 255, "validity": 0,
                                                           "vehicleHeightMoveInfo": {"heightLevelSts":20}}})      
        self.ipdu.resume_bus_send("chassiscan2")  
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                       {"heightMoveInfo": {"source": 7, "validity": 0,
                                                           "vehicleHeightMoveInfo": {"heightLevelSts":20}}})           
        
    @allure.title("获取&通知空气悬架高度等级及运动状态信息_validity_ChassisCAN2::0x2AF信号丢失")
    @pytest.mark.full
    def test_caseid_1989371(self): # 0x2AF FrntLeLvlAdjm
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'AsLvlMov', 3)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'FrntLeLvlAdjm', 0)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, 
                                              {"out": {"vehicleHeightMoveInfo": {"moveSts":2},
                                                       "frontLeftHeightMoveInfo": {"moveSts":2}, "validity": 0}}, timeout=3)
        self.partner.empty_all(15) # 前置用例重启后，15s不检测信号丢失
        self.ipdu.stop_send_pdu("chassiscan2", 0x2AF)     
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                       {"heightMoveInfo": {"vehicleHeightMoveInfo": {"moveSts":2},
                                                           "frontLeftHeightMoveInfo": {"moveSts":2}, "validity": 4}})      
        sleep(2)
        self.restart_bgm_and_connect_service(SUSPENSION_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False) 
        sleep(3)
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo",
                                       {"heightMoveInfo": {"vehicleHeightMoveInfo": {"moveSts":2},
                                                           "frontLeftHeightMoveInfo": {"moveSts":255}, "validity": 0}})      
        self.ipdu.resume_bus_send("chassiscan2")  
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightMoveInfo", 
                                       {"heightMoveInfo": {"vehicleHeightMoveInfo": {"moveSts":2},
                                                           "frontLeftHeightMoveInfo": {"moveSts":2}, "validity": 0}})      
        
    @allure.title("非Override->Override")
    @pytest.mark.sanity
    def test_caseid_1989656(self): # suspen: |jetlogd start|AirSuspensionHeightAutoAdjust|AirSuspensionHeight|SuspensionLevel|AirSuspensionMode|AirSuspensionStiffness|EventGearCallback
        self.sd_tester.change_usage_mode(random.choice([11, 13]))
        self.dk.set_chassis_service_gear(2)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightAutoAdjustConfig", {"configCmd": {"isOn": True}}, {"out": 0})
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, 'AutLvlInhb', 1, timeout=1) # 设置空气悬架高度自动调节功能开启关闭
        sleep(2) 
        self.restart_bgm_and_connect_service(SUSPENSION_SERVICE_CLIENT) 
        sleep(2)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)         
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', 1)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightMoveInfo", {}, {"out": {"source": 1, "validity": 0}}, timeout=3)
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": 5}) # 设置悬架减震阻尼等级  
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                             {"configCmd": {"sourceId": 2060001, "heightCmd": [{"suspensionId": 255, "heightLevelCmd": 2}]}}) # 设置空气悬架高度等级
        sleep(2)
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionModeConfig", {"configCmd": {"modeCmd": 0}}) # 设置悬架模式
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 5, timeout=1)     
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": 3})   
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 3, timeout=1)     
        self.dk.set_chassis_service_gear(random.choice([1, 3])) 
        # 执行设置悬架高度等级level=1的信号发送逻辑 SetAirSuspensionHeightConfig.sourceId=10000，suspensionId=255，heightLevelCmd=1
        # 但此时不进入Override，因为只执行信号发送逻辑，不是调用接口
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 0, timeout=1)   
        sleep(1) # 所以此时的AutLvlInhb仍为1
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, 'AutLvlInhb', 1, timeout=1)        
        # 主动调用设置悬架高度等级 sourceId=10000/20000
        self.set_speed_and_source(speed=0.0, rsn=0, act=0, source=0, sleeptime=1)
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                             {"configCmd": {"sourceId":  random.choice([10000, 20000]), 
                                                            "heightCmd": [{"suspensionId": 255, "heightLevelCmd": 2}]}}) # 设置空气悬架高度等级
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, 'AutLvlInhb', 0, timeout=1)
        sleep(10)
        self.restart_bgm_and_connect_service(SUSPENSION_SERVICE_CLIENT) 
        sleep(2)
        # 设置空气悬架高度自动调节功能开启关闭 记忆值不变，故重启后应该还是True
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, 'AutLvlInhb', 1, timeout=1)

    @allure.title("Init需求")
    @pytest.mark.full
    def test_caseid_1989655(self): 
        # 前置：D/R档
        self.sd_tester.change_usage_mode(random.choice([11, 13]))
        self.dk.set_chassis_service_gear(random.choice([1, 3]))
        # 前置：便捷上下车功能
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionEasyEntryConfig", {"configCmd": {"isOn": False}})
        # 前置：高度自动调节功能
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightAutoAdjustConfig", {"configCmd": {"isOn": False}})
        # 前置：空气悬架高度等级及运动状态信息 AirSuspensionHeightMoveInfo.heightMoveInfo.source=6 悬架当前控制源
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)         
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', 6)
        sleep(2)
        # 前置：设置空气悬架高度等级
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig", 
                                             {"configCmd": {"sourceId": 2060001, "heightCmd": [{"suspensionId": 255, "heightLevelCmd": 2}]}}) # 设置空气悬架高度等级
        # 前置：设置空气悬架刚度调节风格信息
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionStiffnessStyleConfig", {"configCmd": {"styleCmd": 3}})
        # 前置：设置悬架减震阻尼等级
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": 3})   
        self.set_ModeConfig(priority=5, heigh_config=2, stiffness_config=2, level_config=3)
        # 步骤1：设置空气悬架模式 @value(1) kMode2, //模式2（标准）
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionModeConfig", {"configCmd": {"modeCmd": 1}})
        self.set_ModeConfig(priority=2, heigh_config=0, stiffness_config=1, level_config=1) 
        sleep(2)
        # 步骤2：重启
        self.restart_bgm_and_connect_service(SUSPENSION_SERVICE_CLIENT)         
        sleep(2)
        # 步骤3：校验Init需求 不抓tcp的话，只能校验通知，总线信号上看不出来 todo 杀进程抓包
        # 通知空气悬架模式信息
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionModeInfo", {"modeInfo": {"modeSts": 1}}) 
        # 通知空气悬架配置信息:高度自动调节功能+便捷上下车功能+轻松载物功能+换胎模式功能
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionConfigurationInfo",
                                       {"configurationInfo": {"easyEntrySts":0, "heightAutoAdjustSts":0, "easyLoadingSts":1, "jackModeSts":0, "validity":0}}, timeout=5) 
        # 空气悬架刚度调节风格信息
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionStiffnessStyleInfo", {"styleInfo": {"validity":0, "styleSts": 2}}) 

######################################################################################################################################################## 

@allure.feature("SOA服务接口")
@allure.story("运动控制/SuspensionService")
@pytest.mark.aqx      
class TestSuspensionServiceMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21", enable_inter_service=True)
        self.partner = S2sBaseClass([(SUSPENSION_SERVICE_CLIENT),
                                     (DOOR_SERVICE_CLIENT),
                                     (TAILGATE_SERVICE_CLIENT)])
        self.partner.wait_for_service_reconnect(SUSPENSION_SERVICE_CLIENT) 
        sleep(10)

    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all(5)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        sleep(5)
        super().after_each_func(ecu)   

    def set_door_sts(self, door_sts=[2, 2, 2, 2, 2], sleeptime=1):
        ''' 设置五门的开关状态'''            
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', door_sts[0])
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', door_sts[1])  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', door_sts[2])  
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', door_sts[3]) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'TrSts', door_sts[4])
        sleep(sleeptime)
        
    @allure.title("获取&通知空气悬架高度控制禁用信息_inhibitReasonSts_五门关闭_遍历LvlCtrlInhbnRsn")
    @pytest.mark.smoke
    def test_caseid_1989394(self): 
        self.set_door_sts([2, 2, 2, 2, 2]) # 五门关闭
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'LvlCtrlInhbnRsn', 2)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightInhibitInfo", {}, 
                                              {"out": {"inhibitReasonSts":2, "validity": 0}}, timeout=3) 
        self.partner.empty_all(1)
        dict1={0:0, 1:1, 2:2, 4:5, 5:6}
        last_vlaue=2
        for i in range(8):
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'LvlCtrlInhbnRsn', i)
            value = dict1[i] if i in dict1 else last_vlaue
            if value!=last_vlaue:
                self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                               {"inhibitInfo": {"inhibitReasonSts":value, "validity": 0}})
            else:
                self.partner.ck_no_event_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                                     {"inhibitInfo": {"inhibitReasonSts":value, "validity": 0}})
            last_vlaue=value

    @allure.title("获取&通知空气悬架高度控制禁用信息_inhibitReasonSts_LvlCtrlInhbnRsn=3_五门单个开关遍历")
    @pytest.mark.smoke
    def test_caseid_1989397(self): 
        for i in range(5):
            list1=[2, 2, 2, 2, 2]
            self.set_door_sts(list1) # 五门关闭
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'LvlCtrlInhbnRsn', 2)
            self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightInhibitInfo", {}, 
                                                {"out": {"inhibitReasonSts":2, "validity": 0}}, timeout=3) 
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'LvlCtrlInhbnRsn', 3)
            self.partner.ck_no_event_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                                 {"inhibitInfo": {"inhibitReasonSts":2, "validity": 0}}, timeout=3)
            list1[i]=1
            self.set_door_sts(list1)
            if i==4: # 开尾门
                self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                               {"inhibitInfo": {"inhibitReasonSts":4, "validity": 0}}) 
            else: # 开四门
                self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                               {"inhibitInfo": {"inhibitReasonSts":3, "validity": 0}}) 

    @allure.title("获取&通知空气悬架高度控制禁用信息_inhibitReasonSts_LvlCtrlInhbnRsn=3_五门依次打开")
    @pytest.mark.sanity
    def test_caseid_1989398(self): 
        list1=[2, 2, 2, 2, 2]
        self.set_door_sts(list1) # 五门关闭
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'LvlCtrlInhbnRsn', 2)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightInhibitInfo", {}, 
                                              {"out": {"inhibitReasonSts":2, "validity": 0}}, timeout=3) 
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'LvlCtrlInhbnRsn', 3)
        # 五门依次打开 先开尾门
        for i in range(1, 6):
            list1[-i]=1
            self.set_door_sts(list1)
            if i==1: # 开尾门
                self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                               {"inhibitInfo": {"inhibitReasonSts":4, "validity": 0}}) 
            elif i==2: #第一次开四门
                self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                               {"inhibitInfo": {"inhibitReasonSts":3, "validity": 0}})
            else: # 依次开其他门
                self.partner.ck_no_event_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                                     {"inhibitInfo": {"inhibitReasonSts":3, "validity": 0}})

    @allure.title("获取&通知空气悬架高度控制禁用信息_inhibitReasonSts_LvlCtrlInhbnRsn=3_五门依次关闭")
    @pytest.mark.sanity
    def test_caseid_1989399(self): 
        list1=[1, 1, 1, 1, 1]
        self.set_door_sts(list1) # 五门全开
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'LvlCtrlInhbnRsn', 2)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightInhibitInfo", {}, 
                                              {"out": {"inhibitReasonSts":2, "validity": 0}}, timeout=3) 
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'LvlCtrlInhbnRsn', 3)
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                       {"inhibitInfo": {"inhibitReasonSts":3, "validity": 0}})
        self.partner.empty_all(1)
        # 五门依次关门，先关主驾门
        for i in range(5):
            list1[i]=2 
            self.set_door_sts(list1)
            value = 4 if i>=3 else 3
            if i==3: # 关第四个门后上报4
                self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                               {"inhibitInfo": {"inhibitReasonSts":value, "validity": 0}}) 
            else: 
                self.partner.ck_no_event_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                                     {"inhibitInfo": {"inhibitReasonSts":value, "validity": 0}})
                        
    @allure.title("获取&通知空气悬架高度控制禁用信息_inhibitReasonSts_LvlCtrlInhbnRsn=3_五门全开后validity依次从0变1")
    @pytest.mark.full
    def test_caseid_1989400(self): 
        list1=[1, 1, 1, 1, 1]
        self.set_door_sts(list1) # 五门全开
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'LvlCtrlInhbnRsn', 3)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightInhibitInfo", {}, 
                                              {"out": {"inhibitReasonSts":3, "validity": 0}}, timeout=3) 
        self.partner.empty_all(1)        
        for i in range(5):
            list1[i]=0
            self.set_door_sts(list1)
            value = 4 if i>=3 else 3
            if i==3: # 此时四门的validity都为1，仅尾门validity为0
                self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                               {"inhibitInfo": {"inhibitReasonSts":4, "validity": 0}}) 
            else:
                self.partner.ck_no_event_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                                     {"inhibitInfo": {"inhibitReasonSts":value, "validity": 0}})    

    @allure.title("获取&通知空气悬架高度控制禁用信息_inhibitReasonSts_LvlCtrlInhbnRsn=3_bodycan信号丢失")
    @pytest.mark.full
    def test_caseid_1989401(self):   
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'LvlCtrlInhbnRsn', 2)
        self.partner.send_request_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "GetAirSuspensionHeightInhibitInfo", {}, 
                                              {"out": {"inhibitReasonSts":2, "validity": 0}}, timeout=3) 
        self.set_door_sts([1, 1, 1, 1, 1]) # 五门全开
        self.partner.empty_all(1) 
        self.ipdu.pause_bus_send("bodycan")
        sleep(3)
        self.partner.send_request_and_ck_resp(TAILGATE_SERVICE_CLIENT, "GetOpenCloseStatusValidity",{}, {"out": {"value":True,"validity":4}})
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'LvlCtrlInhbnRsn', 3)
        self.partner.ck_no_event_and_ck_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                             {"inhibitInfo": {"inhibitReasonSts":2, "validity": 0}})            
        self.ipdu.resume_bus_send("bodycan")   
        self.partner.ck_event_and_resp(SUSPENSION_SERVICE_CLIENT, "AirSuspensionHeightInhibitInfo", 
                                       {"inhibitInfo": {"inhibitReasonSts":3, "validity": 0}}) 
              