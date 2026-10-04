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

import pytest
import allure
from xat_cases.legacy.basetech.case_helper.test_base import TestBase
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.basetech.case_helper.diag_case_helper.DiagTestBase import *
from xat_ecu.legacy.sdk.sdk_tools import *
flash_count=0

class TestBgm(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.b_cli = DiagTestBase(self.ipdu,self.busapp,self.tc_config)
        self.flash_time = Flashtime()
        with allure.step("连接BGM"):
            self.b_cli.connect(0x1001,'BGM')

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("Test running ...")
        with allure.step("开始刷写时间计算"):
            self.flash_time.start_time()

    def after_each_func(self, ecu):
        logger.info("Test ending ...")
        with allure.step("结束刷写时间计算"):
            self.flash_time.stop_time()
        with allure.step("刷写失败 取BGM日志"):
            if ecu.get("testresult") != "Pass":
                self.b_cli.get_bgm_log(self.log_path)
        super().after_each_func(ecu)
       
    def after_class(self, ecu):
        with allure.step("关闭BGM连接"):
            self.b_cli.close()
        super().after_class(self, ecu)
       
    @pytest.mark.repeat(100)
    def test_caseid_1984948_1984949(self):
        #罐装版本 v1.3BR
        boot_keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_256CCFFC5CF2D02EC75B']
        boot_file_url = "https://repo.jidudev.com/artifactory/BGMSoftware/Release/v1.3.0/6160110130BR/2960110130AD.bin"     

        keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_CFD007D7CB44C62B6D84'] 
        file_url = "https://repo.jidudev.com/artifactory/BGMSoftware/Release/v1.3.0/6160110130BR/6160110130BR.bin"
        with allure.step("v1.3BR:开始刷写boot"):
            self.b_cli.flash_bgm(boot_keyinfo,boot_file_url, sniff_packet=False)
        with allure.step("v1.3BR:开始刷写APP"):
            self.b_cli.flash_bgm(keyinfo,file_url, sniff_packet=False)
        
        #用户版本 v1.4BN
        keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_8C43C5BF776669D38642']
        file_url = "https://repo.jidudev.com/artifactory/BGMSoftware/Release/v1.4.0/6160110140BN/6160110140BN.bin"
        
        boot_keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_F9325E6A974874993ADA'] 
        boot_file_url = "https://repo.jidudev.com/artifactory/BGMSoftware/Release/v1.4.0/6160110140BN/2960110130AD.bin"
        with allure.step("v1.4BN:开始刷写boot"):
            self.b_cli.flash_bgm(boot_keyinfo,boot_file_url, sniff_packet=False)
        with allure.step("v1.4BN:开始刷写APP"):
            self.b_cli.flash_bgm(keyinfo,file_url, sniff_packet=False)
        
        #weekly版本
        keyinfo = "dN3D0SXgjrg58tbNc6Bk4iA59YNR/qlrICdhljUN3ArMpzncTqhhdZUejlh4zBLyx650cof6q/Rs530eSCHy9SA4te5d0uDkuulbiULB57Xgrfo4aGO6c1h69CTZn76VA/mxWUokLrjyjDUsw2UVvOdmJKsqG1HPMKfMqxwT/auRAEyc5oTS0uyJflOqgkE5TaIppNiAaHQEpy06a4xipdtErAot1VRGu/SnU9kTwWohExXZorUIvvFGUcL+XKgqk3f2ZcL4zP8d61Zg73ze89Y8B7Y0Qcd+SpUipvZc91FgsfwRtCvUjin7r8XG3G6mu+yBXDIKzXQDteEcgre1HA=="
        file_url = "https://repo.jidudev.com/artifactory/BGMSoftware/Release/v1.3.0/6160110130AW/6160110130AW.bin"
        
        boot_keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_65DA95A6DB887654CE6A'] 
        boot_file_url = "https://repo.jidudev.com/artifactory/BGMSoftware/Release/v1.3.0/6160110130AV/2960110130AA.bin"
        with allure.step("weekly version:开始刷写boot"):
            self.b_cli.flash_bgm(boot_keyinfo,boot_file_url, sniff_packet=False)
        with allure.step("weekly version:开始刷写APP"):
            self.b_cli.flash_bgm(keyinfo,file_url, sniff_packet=False)

            
#cd /root/wenyu.liang/sat/xat_cases/legacy/basetech
#. ./venv/bin/activate
#cd /root/wenyu.liang/sat/xat_cases/legacy/basetech
#pytest stress/test_flash_bgm.py --disable_partner='true'
#172.18.128.182:8080/2023_08_10_11_36_30
