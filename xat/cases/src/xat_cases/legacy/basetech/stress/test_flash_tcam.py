# -*- coding: utf-8 -*-
"""
@File        : test_uds_bgm_app.py
@Author      : o_wenyu.liang_ext@jiduauto.com
@Author      : o_wenyu.liang_ext@jiduauto.com
@Time        : 2022/11/17
@Description :

"""
import pytest
import allure
import sys, os

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

work_path_2 = os.path.join(os.getcwd().split("sat")[0], 'sat', 'ecu_simulator', 'interface')
sys.path.append(work_path_2)

from xat_cases.legacy.basetech.case_helper.test_base import TestBase
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.basetech.case_helper.diag_case_helper.DiagTestBase import *
from xat_ecu.legacy.sdk.sdk_tools import *
flash_count=0

class TestTcam(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.t_cli = DiagTestBase(self.ipdu,self.busapp,self.tc_config)
        self.flash_time = Flashtime()
        with allure.step("连接TCAM"):
            self.t_cli.connect(0x1011,'TCAM')

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("Test running ...")
        with allure.step("开始刷写时间计算"):
            self.flash_time.start_time()

    def after_each_func(self, ecu):
        logger.info("Test ending ...")
        with allure.step("结束刷写时间计算"):
            self.flash_time.stop_time()
        logger.info(f"当前的用例运行状态是：{ecu.get('testresult')}")
        with allure.step("刷写失败 取BGM TCAM日志"):
            if ecu.get("testresult") != "Pass":
                self.t_cli.get_bgm_log(self.log_path)
                self.t_cli.get_tcam_log(self.log_path, connect_type='obd')
        super().after_each_func(ecu)
    
    def after_class(self, ecu):
        with allure.step("关闭TCAM连接"):
            self.t_cli.close()
        super().after_class(self, ecu)
       
    @pytest.mark.repeat(1)
    def test_fota_caseid_1983069(self):
        get_log_data_whether_timeout()
        #用户版本 v1.4AR
        get_log_data_whether_timeout()
        keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_7D4FCB9451663F1A319F'] 
        file_url = "https://repo.jidudev.com/artifactory/TCAMSoftware/Release/v2.1.0/6110110210AQ/6110110210AQ.bin"      
        with allure.step("v2.1AQ:开始刷写TCAM"):    
            self.t_cli.flash_tcam(keyinfo,file_url)
            logger.info("v2.1AQ 版本刷写结束")
        check_tcam_network_and_time_sync()
        get_log_data_whether_timeout()
        
        # #weekly版本    
        keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_9B32DE6080DBD9721B0F'] 
        file_url = "https://repo.jidudev.com/artifactory/TCAMSoftware/Release/v3.0.0/6110110300AF/6110110300AF.bin" 
        with allure.step("3.0AF weekly version:开始刷写TCAM"):  
            self.t_cli.flash_tcam(keyinfo,file_url)
            logger.info("3.0AF 第1次版本刷写结束")
        check_tcam_network_and_time_sync()
        get_log_data_whether_timeout()
        
        # # #weekly版本    
        keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_578B67E60B101856C816'] 
        file_url = "https://repo.jidudev.com/artifactory/TCAMSoftware/Release/v3.0.0/6110110300AF/6110110300AF.bin" 
        with allure.step("3.0AF weekly version:开始刷写TCAM"):  
            self.t_cli.flash_tcam(keyinfo,file_url)
            logger.info("3.0AF 第1次版本刷写结束")
        check_tcam_network_and_time_sync()
        get_log_data_whether_timeout()



#cd /root/wenyu.liang/sat/xat_cases/legacy/basetech
#. ./venv/bin/activate 
#cd /root/wenyu.liang/sat/xat_cases/legacy/basetech
#pytest stress/test_flash_tcam.py --disable_partner='true'
