#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : test_system_hardening.py
@time         : 2024/3/21
@author       : o_jingyuan.chen@external.jiduauto.com
@description  : 
'''

import pytest
import allure
from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature('BGM BaseTech/数字安全/系统安全')
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
    @allure.title('109889_用户登录')
    def test_caseid_109889(self):
        data=self.ssh.type_commands(DeviceName.BGM,"whoami")
        logger.info(f'{data}')

    @pytest.mark.full
    @allure.title('109884_系统信息_无内核版本')
    def test_caseid_109884(self):
        data=self.ssh.type_commands(DeviceName.BGM,"cat /etc/issue")
        assert data == "JiDu BGM Release Distro 1.0 \\n \\l\n","有内核版本"

    @pytest.mark.full
    @allure.title('109883_系统信息_无发行版本')
    def test_caseid_109883(self):
        data=self.ssh.type_commands(DeviceName.BGM,"cat /etc/issue.net")
        assert data == "JiDu BGM Release Distro 1.0 %h\n","有发行版本"

    @pytest.mark.full
    @allure.title('109882_系统信息_硬件版本信息')
    def test_caseid_109882(self):
        data=self.ssh.type_commands(DeviceName.BGM,"cat /etc/*-release")
        logger.info(f'{data}')
        assert data == 'ID=jidu-bgm-mars1\n' \
               'NAME="JiDu BGM Release Distro"\n' \
               'VERSION="1.0"\n' \
               'VERSION_ID=1.0\n' \
               'PRETTY_NAME="JiDu BGM Release Distro 1.0"\n' \
               'DISTRO_CODENAME="mars1"', "有硬件版本"

    @pytest.mark.sanity
    @allure.title('109887_获取root权限')
    def test_caseid_109887(self):
        data=self.ssh.type_commands(DeviceName.BGM,"whoami")
        logger.info(f'{data}')

    @pytest.mark.sanity
    @allure.title('109888_默认用户无root权限')
    def test_caseid_109888(self):
        data=self.ssh.type_commands(DeviceName.BGM,"who")
        assert data == ""
        
#pytest BaseTech/InformationSecurity/test_system_hardening.py::TestSystemHardening::test_caseid_109882
