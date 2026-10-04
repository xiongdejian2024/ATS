# -*- coding: utf-8 -*-
"""
@File        : test_bgm_soc_.py
@Author      : tanggeng.li@jiduauto.com
@Time        : 2024/1/25 10:40
@Description :

"""
import os
import random
import sys
import time

import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("BGM BaseTech/工业化")
@allure.story("MPU EOL流程")
class TestBgmSocProductionlinedemand(TestABCBase):
    def before_class(self, ecu):
        self.iface = self.tc_config['bus']['eth_obd']  # 'enp114s0'

        self.ssh.init_bgm_tcpdump()  # 初始化，只需要执行一次

        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.bgm_soc_enter_ecu_eol_mode()


    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        self.sd_tester.bgm_soc_quit_ecu_eol_mode()
        self.ssh.delete_bgm_tcpdump_file()

    @pytest.mark.sanity
    @pytest.mark.full
    def test_ddr_caseid_1985020(self):
        '''

        @return:
        '''
        self.sd_tester.bgm_soc_ddr()

    @pytest.mark.sanity
    @pytest.mark.full
    def test_emmc_caseid_1985022(self):
        '''

        @return:
        '''
        self.sd_tester.bgm_soc_emmc()

    @pytest.mark.sanity
    @pytest.mark.full
    def test_emmc_checksum_verify_caseid_1985023(self):
        '''

        @return:
        '''
        self.sd_tester.bgm_soc_emmc_checksum_verify()

    @pytest.mark.sanity
    @pytest.mark.full
    def test_switch_port_caseid_1985027(self):
        # self.sd_tester.bgm_soc_switch_port(iface=self.iface)
        self.mix.bgm_soc_switch_port(iface=self.iface)

    @pytest.mark.sanity
    @pytest.mark.full
    def test_gpio_caseid_1985024(self):
        self.sd_tester.bgm_soc_gpio()

    @pytest.mark.sanity
    @pytest.mark.full
    def test_check_secure_boot_status_caseid_1985025(self):
        self.sd_tester.bgm_soc_check_secure_boot_status()

    @pytest.mark.sanity
    @pytest.mark.full
    def test_check_mcu_mpu_comm_link_status_caseid_1985026(self):
        # self.sd_tester.bgm_soc_check_mcu_mpu_comm_link_status()
        self.mix.bgm_soc_check_mcu_mpu_comm_link_status()


@allure.feature("BGM BaseTech/工业化")
@allure.story("MPU EOL流程")
class TestBgmSocProductionlinedemand_NACK(TestABCBase):
    def before_class(self, ecu):
        self.iface = self.tc_config['bus']['eth_obd']  # 'enp114s0'
        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.bgm_soc_quit_ecu_eol_mode()

    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        logger.info("after_each_func")

    def after_class(self, ecu):
        logger.info("after_class")

    @pytest.mark.sanity
    @pytest.mark.full
    def test_ddr_nack_caseid_1985032(self):
        '''
        @return:
        '''
        self.sd_tester.bgm_soc_send_data_and_check([0x31, 0x01, 0xDC, 0x01], [0x7F, 0x31, 0x31])

    @pytest.mark.sanity
    @pytest.mark.full
    def test_emmc_nack_caseid_1985031(self):
        '''
        @return:
        '''
        self.sd_tester.bgm_soc_send_data_and_check([0x31, 0x01, 0xDC, 0x02], [0x7F, 0x31, 0x31])

    @pytest.mark.sanity
    @pytest.mark.full
    def test_emmc_checksum_verify_nack_caseid_1985030(self):
        '''
        @return:
        '''
        self.sd_tester.bgm_soc_send_data_and_check([0x31, 0x01, 0xDC, 0x03], [0x7F, 0x31, 0x31])

    @pytest.mark.sanity
    @pytest.mark.full
    def test_switch_port_nack_caseid_1985029(self):
        self.sd_tester.bgm_soc_send_data_and_check([0x31, 0x01, 0xDC, 0x05], [0x7F, 0x31, 0x31])
        self.sd_tester.bgm_soc_send_data_and_check([0x31, 0x02, 0xDC, 0x05], [0x7F, 0x31, 0x31])

    @pytest.mark.sanity
    @pytest.mark.full
    def test_gpio_nack_caseid_1985033(self):
        self.sd_tester.bgm_soc_send_data_and_check([0x22, 0xDA, 0x02], [0x7F, 0x22, 0x31])

    @pytest.mark.sanity
    @pytest.mark.full
    def test_check_secure_boot_status_nack_caseid_1985028(self):
        self.sd_tester.bgm_soc_send_data_and_check([0x22, 0xDA, 0x00], [0x7F, 0x22, 0x31])

    @pytest.mark.sanity
    @pytest.mark.full
    def test_check_mcu_mpu_comm_link_status_nack_caseid_1985034(self):
        self.sd_tester.bgm_soc_send_data_and_check([0x22, 0xDA, 0x01], [0x7F, 0x22, 0x31])

# pytest mcu/00ltg/test_bgm_soc_production_line_demand.py
