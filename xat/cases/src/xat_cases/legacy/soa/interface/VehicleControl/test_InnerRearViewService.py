#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_EntryService.py
@Time         :2023/04/30 19:07:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import allure
import pytest
from time import sleep
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *

@allure.feature("SOA服务接口")
@allure.story("整车控制/InnerRearViewService")
@pytest.mark.aqx
class TestInnerRearViewService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("InnerRearViewService", "client")])
        self.partner.method_default_timeout = 0.1
        self.sd_tester.tester_present()
             
    def after_class(self, ecu):
        self.partner.stop_operators()   
        self.sd_tester.stop_tester_present()  
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkNotEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set_vehspd(0)
        self.sd_tester.change_car_mode(0)   
        self.partner.empty_all(1)

    def after_each_func(self, ecu):   
        super().after_each_func(ecu, start=False)
        
    @allure.title("设置内后视镜自动防眩目功能开启关闭_报文校验")
    @pytest.mark.sanity
    def test_caseid_1984588(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(3)       
        for isOn in [True, True, False, False]:
            self.partner.send_method_request("InnerRearViewService_client","SetAutoBlindingProof",{"isOn":isOn})
            sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("HMIMirrDimmEn", [1, 1, 0, 0])
               
    @allure.title("获取&通知内后视镜自动防眩目功能开启关闭")
    @pytest.mark.smoke
    def test_caseid_1984589(self):
        self.partner.send_method_request("InnerRearViewService_client","SetAutoBlindingProof",{"isOn":False})
        self.partner.empty_all(2)
        for isOn in [True, False]:
            self.partner.send_method_request("InnerRearViewService_client","SetAutoBlindingProof",{"isOn":isOn})
            self.partner.ck_s2s_event("InnerRearViewService_client", "AutoBlindingProofStatus",{"isOn":isOn})
            self.partner.send_request_and_ck_resp("InnerRearViewService_client", "GetAutoBlidingProof",{},{"out":isOn}) 
               
    @allure.title("服务启动默认值")
    @pytest.mark.full
    def test_caseid_1984590(self):
        for isOn in [True, False]:
            self.partner.send_method_request("InnerRearViewService_client","SetAutoBlindingProof",{"isOn":isOn})
            self.partner.send_request_and_ck_resp("InnerRearViewService_client", "GetAutoBlidingProof",{},{"out":isOn}, timeout=2)
            self.partner.empty_all()
            self.restart_bgm_and_connect_service("InnerRearViewService_client")
            self.partner.send_request_and_ck_resp("InnerRearViewService_client", "GetAutoBlidingProof",{},{"out":isOn}, timeout=1) # 记忆值
            self.partner.ck_s2s_event("InnerRearViewService_client", "AutoBlindingProofStatus",{"isOn":isOn})       

    @allure.title("BGM首次下线默认配置")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1943413(self):
        # 删除数据库
        bgmssh = BGM_SSH()
        bgmssh.type_commands("sudo rm -rf /data/s2s_service/s2s_service.db3", root_permission=True)
        sleep(1)
        bgmssh.type_commands("ls -l /data/s2s_service")
        sleep(5)
        self.ipdu.pause_all_bus_send()  # 停掉总线
        self.nucapp.bgm_power_off()
        sleep(7)
        self.partner.empty_all()
        self.nucapp.bgm_power_on()
        self.partner.wait_for_service_reconnect(INNERREARVIEW_SERVICE_CLIENT)   
        # 获取内后视镜自动防眩目功能开启关闭状态，默认ison
        self.partner.ck_s2s_event("InnerRearViewService_client", "AutoBlindingProofStatus",{"isOn":True})
        self.partner.send_request_and_ck_resp(INNERREARVIEW_SERVICE_CLIENT, "GetAutoBlidingProof", {}, {"out": True})

    @allure.title("设置内后视镜自动防眩目功能开启关闭_服务启动默认值")
    @pytest.mark.full
    def test_caseid_1985514(self):
        for isOn in [True, False]:
            self.partner.send_method_request("InnerRearViewService_client","SetAutoBlindingProof",{"isOn":isOn})
            sleep(1)
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.kill_s2s_and_reconnect_service("InnerRearViewService_client")
            sleep(5)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_signal_values("HMIMirrDimmEn", [isOn])
    
    @allure.title("设置内后视镜自动防眩目功能开启关闭_首次下线默认值")
    @pytest.mark.full
    def test_caseid_1985520(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.del_s2s_db()  # 删除数据库
        self.kill_s2s_and_reconnect_service("InnerRearViewService_client")
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("HMIMirrDimmEn", [1])