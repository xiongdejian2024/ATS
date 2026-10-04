#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : test_certificate.py
@time         : 2024/3/18
@author       : o_kaijin.yao@external.jiduauto.com
'''

import os
import sys
import allure
import pytest
from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH


@allure.feature("信息安全/证书管理")
class TestCertificate(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        global ip
        ip = self.tc_config.get('gateway_ip')

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu) 

    @allure.title('101556_ECU SK证书预置_001')
    @pytest.mark.smoke
    def test_caseid_101556(self):
        failed = []
        TCAMSk = TCAM_SSH().exec("ls -l /oemapp/etc/certificate/ | grep TCAMSk.key" + " | awk '{print $5}' ", ip).strip()
        allure.step("查看TCAMSk.key文件是否存在")
        if TCAMSk:
            logger.info("TCAMSk.key文件存在")
            allure.attach("TCAMSk.key文件存在", "查询TCAMSk.key")
            allure.step("查看TCAMSk.key文件的大小")
            if TCAMSk != '1217':
                logger.info("TCAMSk.key文件大小不为1217")
                allure.attach(0, "查询TCAMSk大小")
                failed.append("大小不为1217")
            else:
                logger.info(f"TCAMSk.key文件大小为:{TCAMSk}")
                allure.attach(f"{TCAMSk}", "查询TCAMSk大小")
        else:
            logger.info("TCAMSk.key文件不存在")
            allure.attach("TCAMSk.key文件不存在", "查询TCAMSk.key")
            failed.append("文件不存在")
        assert len(failed) == 0

    @allure.title('101557_根证书预置_001')   
    @pytest.mark.smoke
    def test_caseid_101557(self):
        failed = []
        rootCA = TCAM_SSH().exec("ls -l /oemapp/etc/certificate/ | grep rootCA.crt" + " | awk '{print $5}' ", ip).strip()
        allure.step("查看rootCA.crt文件是否存在")
        if rootCA:
            logger.info("rootCA.crt文件存在")
            allure.attach("rootCA.crt文件存在", "查询rootCA.crt")
            allure.step("查看rootCA.crt文件的大小")
            if rootCA != '615':
                logger.info("TCAMSk.key文件大小不为615")
                allure.attach(0, "查询rootCA.crt大小")
                failed.append("大小不为615")
            else:
                logger.info(f"rootCA.crt文件大小为:{rootCA}")
                allure.attach(f"{rootCA}", "查询rootCA.crt大小")
        else:
            logger.info("rootCA.crt文件不存在")
            allure.attach("rootCA.crt文件不存在", "查询rootCA.crt")
            failed.append("文件不存在")
        assert len(failed) == 0

    @allure.title('101558_默认VID')   
    @pytest.mark.full
    def test_caseid_101558(self):
        self.sd_tester.send_data_and_check(TA.TCAM, [0x10, 0x01], '5001', diagnostic_action="enter_default_session")
        self.sd_tester.send_data_and_check(TA.TCAM, [0x10, 0x03], '5003', diagnostic_action="enter_extended_session")
        self.sd_tester.update_serverdoipid(TA.TCAM, ecu='TCAM')
        self.sd_tester.security_access_level(UnLock.L5)
        self.sd_tester.read_did_and_check(TA.TCAM,0xB163,SESSION.EMPTY,'62b163',check_length=38)


    @allure.title('101577_解锁L7安全访问')   
    @pytest.mark.sanity
    def test_caseid_101577(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,check_data='6708')

    @allure.title('101561_解锁L5 VID读取')   
    @pytest.mark.full
    def test_caseid_101561(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L5,check_data='6706')
        self.sd_tester.read_did_and_check(TA.TCAM,0xB163,SESSION.EMPTY,'62b163',check_length=38)

    @allure.title('101562_解锁L7 VID写入和读取')   
    @pytest.mark.full
    def test_caseid_101562(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,check_data='6708')
        data=self.sd_tester.read_did_and_check(TA.TCAM,0xb163,SESSION.EMPTY,'62b163',check_length=38)[6:]
        self.sd_tester.write_did_and_check(TA.TCAM,0xb163,SESSION.EMPTY,UnLock.L0,data,f'62b163{data}',check_method=Check_Method.read,recover=False)

    @allure.title('101563_数字证书颁发_前提条件')   
    @pytest.mark.full
    def test_caseid_101563(self):
        allure.step("读取BGM的SN和VIN DID")
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xF18C,SESSION.DEFAULT,'62f18c',check_length=14)
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xF190,SESSION.DEFAULT,'62f190',check_length=40)
        allure.step("读取TCAM的SN和ICCID DID")
        self.sd_tester.read_did_and_check(TA.TCAM,0xF18C,SESSION.DEFAULT,'62f18c',check_length=14)
        self.sd_tester.read_did_and_check(TA.TCAM,0xF190,SESSION.DEFAULT,'62f190',check_length=40)
        self.sd_tester.read_did_and_check(TA.TCAM,0x41AE,SESSION.DEFAULT,'6241ae',check_length=46)

    @allure.title('1978640_一键切换Staging')   
    @pytest.mark.full
    def test_caseid_1978640(self):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM,0x2100,0x01,session=SESSION.EXTENDED,unlock_level=UnLock.L5,check_data='710121001000')
        time.sleep(1)
        cmdresult = TCAM_SSH().exec("cd /mnt/sdcard/persistent/config_service/ ", ip)
        assert "No such file or directory" in cmdresult, f"config_service文件清除失败"

