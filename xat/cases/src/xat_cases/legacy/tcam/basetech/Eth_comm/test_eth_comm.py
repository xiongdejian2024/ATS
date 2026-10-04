#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: test_eth_comm.py
@Time: 2022/10/20 09:08
@Author: lei.tao
@Software: PyCharm
@Description: 以太网通信测试用例
@Examples:
"""
import os
import sys
import allure
import pytest

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("TCAM BaseTech/通信")
@allure.story("以太网通信")
class Test_Eth_ARP(TestABCBase):

    def before_class(self, ecu):
        super().before_class(self, ecu)
        global bgm_ip
        bgm_ip = self.tc_config.get('gateway_ip')

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN9_172.16.9.1的测试用例")
    def test_caseid_101587(self):
        vlan_ip = "172.16.9.1"
        mac_address = '02:00:00:00:10:01'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN5_172.16.5.1的测试用例")
    def test_caseid_101604(self):
        vlan_ip = "172.16.5.1"
        mac_address = '02:00:00:00:10:01'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)
        
    @pytest.mark.sanity
    @allure.title("TCAM_VLAN32_172.16.32.1的测试用例")
    def test_caseid_101592(self):
        vlan_ip = "172.16.32.1"
        mac_address = '02:00:00:00:10:01'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN32_172.16.32.11的测试用例")
    def test_caseid_101591(self):
        vlan_ip = "172.16.32.11"
        mac_address = '02:00:00:00:10:11'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN32_172.16.32.13的测试用例")
    def test_caseid_101590(self):
        vlan_ip = "172.16.32.13"
        mac_address = '02:00:00:00:10:13'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN32_172.16.32.21的测试用例")
    def test_caseid_101589(self):
        vlan_ip = "172.16.32.21"
        mac_address = '02:00:00:00:10:21'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN32_172.16.32.23的测试用例")
    def test_caseid_101588(self):
        vlan_ip = "172.16.32.23"
        mac_address = '02:00:00:00:10:23'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN9_172.16.9.11的测试用例")
    def test_caseid_101585(self):
        vlan_ip = "172.16.9.11"
        mac_address = '02:00:00:00:10:11'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN5_172.16.5.11的测试用例")
    def test_caseid_101602(self):
        vlan_ip = "172.16.5.11"
        mac_address = '02:00:00:00:10:11'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN30_172.16.30.11的测试用例")
    def test_caseid_101596(self):
        vlan_ip = "172.16.30.11"
        mac_address = '02:00:00:00:10:11'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN11_172.16.11.11的测试用例")
    def test_caseid_101598(self):
        vlan_ip = "172.16.11.11"
        mac_address = '02:00:00:00:10:11'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN9_172.16.9.13的测试用例")
    def test_caseid_101583(self):
        vlan_ip = "172.16.9.13"
        mac_address = '02:00:00:00:10:13'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN5_172.16.5.13的测试用例")
    def test_caseid_101601(self):
        vlan_ip = "172.16.5.13"
        mac_address = '02:00:00:00:10:13'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN30_172.16.30.13的测试用例")
    def test_caseid_101595(self):
        vlan_ip = "172.16.30.13"
        mac_address = '02:00:00:00:10:13'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN11_172.16.11.13的测试用例")
    def test_caseid_101597(self):
        vlan_ip = "172.16.11.13"
        mac_address = '02:00:00:00:10:13'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN9_172.16.9.12的测试用例")
    def test_caseid_101584(self):
        vlan_ip = "172.16.9.12"
        mac_address = '02:00:00:00:10:12'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN9_172.16.9.21的测试用例")
    def test_caseid_101582(self):
        vlan_ip = "172.16.9.21"
        mac_address = '02:00:00:00:10:21'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN5_172.16.5.21的测试用例")
    def test_caseid_101600(self):
        vlan_ip = "172.16.5.21"
        mac_address = '02:00:00:00:10:21'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN11_172.16.11.21的测试用例")
    def test_caseid_1198051(self):
        vlan_ip = "172.16.11.21"
        mac_address = '02:00:00:00:10:21'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN9_172.16.9.23的测试用例")
    def test_caseid_101581(self):
        vlan_ip = "172.16.9.23"
        mac_address = '02:00:00:00:10:23'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN5_172.16.5.23的测试用例")
    def test_caseid_101599(self):
        vlan_ip = "172.16.5.23"
        mac_address = '02:00:00:00:10:23'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN11_172.16.11.23的测试用例")
    def test_caseid_1198052(self):
        vlan_ip = "172.16.11.23"
        mac_address = '02:00:00:00:10:23'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN9_172.16.9.25的测试用例")
    def test_caseid_1198069(self):
        vlan_ip = "172.16.9.25"
        mac_address = '02:00:00:00:10:25'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN9_172.16.9.26的测试用例")
    def test_caseid_1198070(self):
        vlan_ip = "172.16.9.26"
        mac_address = '02:00:00:00:10:26'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

    @pytest.mark.sanity
    @allure.title("TCAM_VLAN9_172.16.9.27的测试用例")
    def test_caseid_1198071(self):
        vlan_ip = "172.16.9.27"
        mac_address = '02:00:00:00:10:27'
        self.ssh.check_vlan_conn(bgm_ip,vlan_ip,mac_address)

# pytest basetech/Eth_comm/test_eth_comm.py