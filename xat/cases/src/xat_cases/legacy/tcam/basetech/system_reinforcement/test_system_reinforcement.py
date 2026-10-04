#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : test_system_reinforcement.py
@time         : 2024/8/13
@author       : xiaoqiang.hu.jiduauto.com
@description  : 
'''

import pytest
import allure
from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature('TCAM BaseTech/数字安全/系统安全')
@allure.story('系统加固')
class TestSystemHardening(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self,ecu)
        logger.info("before_class")

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        self.sd_tester.exit_muc_boot()
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        logger.info("after_class")
        super().after_class(self, ecu)

    @pytest.mark.smoke
    @allure.title('1989539_用户登录')
    def test_caseid_1989539(self):
        data=self.ssh.type_commands(DeviceName.TCAM,"whoami")
        logger.info(f'{data}')
    
    @pytest.mark.sanity
    @allure.title('1989538_获取root权限')
    def test_caseid_1989538(self):
        data=self.ssh.type_commands(DeviceName.TCAM,"whoami")
        logger.info(f'{data}')
        assert data == "root","获取root权限失败"

    @pytest.mark.full
    @allure.title('1989535_系统信息_无内核版本')
    def test_caseid_1989535(self):
        data=self.ssh.type_commands(DeviceName.TCAM,"cat /etc/issue")
        assert "auto" in data,"无内核版本"
        #assert data == 'auto 1619 \n \l',"有内核版本"

    @pytest.mark.full
    @allure.title('1989534_系统信息_无发行版本')
    def test_caseid_1989534(self):
        data=self.ssh.type_commands(DeviceName.TCAM,"cat /etc/issue.net")
        assert "auto" in data,"无发行版本"
        #assert data == 'auto 1619 %h',"有发行版本"

    @pytest.mark.full
    @allure.title('1989533_系统信息_硬件版本信息')
    def test_caseid_1989533(self):
        data=self.ssh.type_commands(DeviceName.TCAM,"cat /etc/*-release")
        logger.info(f'{data}')
        assert 'PRETTY_NAME' in data, "无硬件版本"
        # assert data == 'ID="auto"' \
        #     'NAME="auto"' \
        #     'VERSION="202407111611"' \
        #     'VERSION_ID="202407111611"' \
        #     'PRETTY_NAME="auto 202407111611"', "有硬件版本"

    
