# -*- coding: utf-8 -*-
"""
@File        : test_soa_heat.py
@Author      : gang.liugang@jiduatuo.com
@Time        : 2024/01/11 15:00 PM
@Description : Test SOA for LogMasterService
"""

import os
import sys

from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_cases.legacy.soa.case_helper.parse_excel import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_cases.legacy.soa.case_helper.utils import *

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path.split("sat")[0], "sat"))
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.common.logger import logger

@allure.feature("SOA服务接口")
@allure.story("架构基础/LogMasterService")
class TestLogMasterService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("LogMasterService", "client"),
                                     ])
        self.partner.method_default_timeout = 0.1
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        
        self.io_obj = self.io.io_obj
        self.sd_tester.tester_present()
        sleep(2)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        sleep(0.5)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.partner.empty_all(0.5)
        logger.info(f"case开始运行")

    def after_each_func(self, ecu):
        logger.info(f"case结束运行")
        self.ipdu.resume_all_bus_send()  # 信号恢复
        self.bgmcli.stop_bgm_tcpdump()
        self.nucapp.bgm_diag_line_up()
        self.bgmcli.delete_bgm_tcpdump_file(bgm_log_name='*.pcap')
        if ecu.get("testresult") != "Pass":
            logger.error("case失败，需等待10s让环境恢复")
            sleep(10)
        else:
            logger.info("case成功，需等待3s让环境恢复")
            sleep(3)
        super().after_each_func(ecu, start=False)
 
    def after_class(self, ecu):
        self.partner.stop_operators()
        self.sd_tester.stop_tester_present()
        super().after_class(self, ecu)
    
    @pytest.mark.smoke
    @allure.title("设置通知获取日志上传信息")
    def test_caseid_1987786(self): 
        for source in [0,1,2,3,4,5]:
            self.partner.send_request_and_ck_resp(LOGMASTER_SERVICE_CLIENT, "ReqUploadLog",
                                        {"triggerSourceInfo":{"source":source,"event":"err_log","request_id":"123",
                                                            "uploadCtrl":{"domain":"BGM","ctrlParam":"123"}}},
                                        {"out": True})
            sleep(2)
        
     
    
        
        
       