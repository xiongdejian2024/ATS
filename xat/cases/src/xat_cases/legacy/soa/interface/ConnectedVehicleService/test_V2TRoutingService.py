# -*- coding: utf-8 -*-
"""
@File        : test_soa_heat.py
@Author      : gang.liugang@jiduatuo.com
@Time        : 2024/01/26 15:00 PM
@Description : Test SOA for V2TRoutingService
"""

import os
import sys
import time
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_cases.legacy.soa.case_helper.parse_excel import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_cases.legacy.soa.case_helper.utils import *
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path.split("sat")[0], "sat"))
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.common.logger import logger


@allure.feature("SOA服务接口")
@allure.story("架构基础/V2TRoutingService")
@pytest.mark.liugang
@pytest.mark.tcam
class TestV2TRoutingService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        sleep(1)
        self.partner = S2sBaseClass([("V2TRoutingService", "client"),
                                     ])
        self.partner.method_default_timeout = 0.1
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.partner.empty_all(0.5)
        logger.info(f"case开始运行*********************************************")

    def after_each_func(self, ecu):
        logger.info(f"case结束运行*********************************************")
        self.ipdu.resume_all_bus_send()  # 信号恢复
        super().after_each_func(ecu, start=False)
 
    def after_class(self, ecu):
        TCAM_SSH().type_commands('cat /dev/smd8 & echo -en "at+cfun=1\\r\\n" > /dev/smd8',timeout=3)
        self.partner.stop_operators()
        super().after_class(self, ecu)

    #接口定义与实际不符，需要确认
    @allure.title("请求调用云端服务_服务超时")
    @pytest.mark.smoke
    def test_caseid_1984270(self):
        TCAM_SSH().type_commands('cat /dev/smd8 & echo -en "at+cfun=0\\r\\n" > /dev/smd8',timeout=3)
        # 无网络回超时
        self.partner.send_request_and_ck_resp(V2TROUTING_SERVICE_CLIENT, "CallTspApi",
                                    {"srcService":"AA","destService":"BB","api":"CC","Payload":8,"timeout":3000,"traceId":"DD"},
                                    {"out":{"result": 2}}, timeout=5)
        
        TCAM_SSH().type_commands('cat /dev/smd8 & echo -en "at+cfun=1\\r\\n" > /dev/smd8',timeout=3)
        # 有网络回fail
        time.sleep(2)
        self.partner.send_request_and_ck_resp(V2TROUTING_SERVICE_CLIENT, "CallTspApi",
                                    {"srcService":"AA","destService":"BB","api":"CC","Payload":8,"timeout":3000,"traceId":"DD"},
                                    {"out":{"result": 1}}, timeout=5)          
    
    @allure.title("通知并获取车云连接状态")
    @pytest.mark.full
    def test_caseid_1984271(self):
        self.partner.empty_all(0.5)
        TCAM_SSH().type_commands('cat /dev/smd8 & echo -en "at+cfun=0\\r\\n" > /dev/smd8',timeout=3)
       
        self.partner.ck_s2s_event(V2TROUTING_SERVICE_CLIENT, "V2TConnectStatusNotify",
                                        {"status":1},timeout=30)  
        self.partner.send_request_and_ck_resp(V2TROUTING_SERVICE_CLIENT, "GetV2TConnectStatus",{},
                                        {"out":1})
        TCAM_SSH().type_commands('cat /dev/smd8 & echo -en "at+cfun=1\\r\\n" > /dev/smd8',timeout=3)
        self.partner.ck_s2s_event(V2TROUTING_SERVICE_CLIENT, "V2TConnectStatusNotify",
                                        {"status":0},timeout=30)  
        self.partner.send_request_and_ck_resp(V2TROUTING_SERVICE_CLIENT, "GetV2TConnectStatus",{},
                                        {"out":0})
             
    @allure.title("服务注册")
    @pytest.mark.sanity
    def test_caseid_1984272(self):   
        self.partner.send_request_and_ck_resp(V2TROUTING_SERVICE_CLIENT, "RegisterForwarder",
                                    {"forwarderSOAName":"AA","businessName":"BB"},
                                    {"out":0})
