# -*- coding: utf-8 -*-
"""
@File        : test_flash_bgm
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/3/1 13:34
@Description :
需求链接
https://jiduauto.feishu.cn/docx/MWqJdhXnvotbQsxurGicSY1enDg
"""
import time
import pytest
import allure
import sys, os
import json

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

work_path_2 = os.path.join(os.getcwd().split("sat")[0], 'sat', 'ecu_simulator', 'interface')
sys.path.append(work_path_2)

import os
import sys

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

import pytest
import allure
from xat_ecu.legacy.common.logger import logger

from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig
from xat_ecu.legacy.config.path import CONFIG_DIR_PATH
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH

from xat_cases.legacy.bgm.mcu.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.sdk.sdk_tools import *

test_count = 0


@allure.feature("架构基础/网络架构")
@allure.story("诊断/诊断刷写")
class Test_Flash_Tcam(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        tb_path = os.path.join(CONFIG_DIR_PATH, "willow_bgm_flash_config.yaml")
        tb_config = ParseTBConfig(tb_path)
        self.sd_test_tb_config = tb_config.yaml_content
        self.sd_test = Sd_Tester(**self.sd_test_tb_config)
        # self.sd_test.update_serverdoipid(0x1002)
        self.sd_test.diagnostic_client_sim_start()
        self.sd_test.tester_present()
        self.bgm_ssh = BGM_SSH()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # Code Location

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)

    def after_class(self, ecu):
        # Code Location
        super().after_class(self, ecu)
        try:
            self.sd_test.stop_tester_present()
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info(f"str(e)=={str(e)}")

    def bgm_ping_tcam1(self, count=10, err_count=3, condition="boot 下"):
        '''

        @param count: 总共ping 几次
        @param err_count: 几次不通 报错
        @return:
        '''
        global test_count
        # todo 进入bgm ping tcam  10次
        err_count_index = 0
        for _ in range(count):
            ret = self.bgm_ssh.get_ping(ip='172.16.5.31', num=1)
            if not ret:
                logger.error(f"在{condition} bgm ping tcam 出现一次不通")
                err_count_index += 1

        with allure.step(
                f"第{test_count}轮 在{condition} bgm ping tcam {count}次，有{count - err_count_index}次可以ping通，{err_count_index}次ping不通"):
            pass
        # todo 如果有 次不通 则维持
        if err_count_index >= err_count:
            while 1:
                logger.error(
                    f"第{test_count}轮 在{condition} bgm ping tcam {count}次，有{count - err_count_index}次可以ping通，{err_count_index}次ping不通")
                try:
                    self.sd_test.send_data([0x22, 0xf1, 0x86])
                except Exception as e:
                    logger.info(f'发送0x22, 0xf1, 0x86 ==》》{str(e)}')
                time.sleep(5)

    def bgm_ping_tcam(self, count=10, err_count=3, condition="boot 下", dst_tar="tcam", ip='172.16.5.31'):
        '''

        @param count: 总共ping 几次
        @param err_count: 几次不通 报错
        @return:
        '''
        global test_count
        # todo 进入bgm ping tcam  10次
        err_count_index = 0
        for _ in range(count):
            ret = self.bgm_ssh.get_ping(ip=ip, num=1)
            if not ret:
                logger.error(f"在{condition} bgm ping {dst_tar} 出现一次不通")
                err_count_index += 1

        with allure.step(
                f"第{test_count}轮 在{condition} bgm ping {dst_tar} {count}次，有{count - err_count_index}次可以ping通，{err_count_index}次ping不通"):
            pass
        # todo 如果有 次不通 则维持
        if err_count_index >= err_count:
            while 1:
                logger.error(
                    f"第{test_count}轮 在{condition} bgm ping {dst_tar} {count}次，有{count - err_count_index}次可以ping通，{err_count_index}次ping不通")
                try:
                    self.sd_test.send_data([0x22, 0xf1, 0x86])
                except Exception as e:
                    logger.info(f'发送0x22, 0xf1, 0x86 ==》》{str(e)}')
                time.sleep(5)

    def diag_reset_and_ping_tcam_and_nup(self):
        '''
        诊断重启后，ping tcam 和 上位机
        @return:
        '''
        with allure.step(f"诊断重启 bgm ping tcam"):
            self.sd_test.stop_tester_present()
            self.sd_test.reset_ecu_functional_addressing()
            time.sleep(12)
            self.sd_test.tester_present()
            with allure.step(f"检查是会话状态"):
                self.sd_test.send_data([0x22, 0xf1, 0x86])
                result = self.sd_test.return_udsdata_and_check_and_print_response_result(
                    "Send  0xf1, 0x86 to get result")

            with allure.step(f" ping tcam 10 次"):
                logger.info("ping tcam")
                self.bgm_ping_tcam(count=10, err_count=3, condition="boot 下")

            with allure.step(f" ping 上位机 10 次"):
                logger.info("ping 上位机")
                self.bgm_ping_tcam(count=10, err_count=3, condition="诊断重启后", dst_tar="上位机",
                                   ip='172.16.5.21')

    def power_reset_and_ping(self):
        pass

    def under_boot_and_ping_tcam(self):
        '''
        在 boot 下ping tcam
        @return:
        '''
        with allure.step(f"在 boot 下 bgm ping tcam"):
            # todo 发送1082
            with allure.step(f"发送1082 进boot"):
                self.sd_test.stop_tester_present()
                self.sd_test.enter_program_session_functional_addressing()
                time.sleep(12)
                self.sd_test.tester_present()
            # todo 检查是否在boot 下
            with allure.step(f"检查是否在boot 下"):
                self.sd_test.send_data([0x22, 0xf1, 0x86])
                result = self.sd_test.return_udsdata_and_check_and_print_response_result(
                    "Send  0xf1, 0x06 to get result")
                if result[:4] != [0x62, 0xf1, 0x86, 0x02]:
                    assert 0, "未进入boot"
            # todo 进入bgm ping tcam  10次,3次以及以上则 维持现场
            with allure.step(f"在boot 模式ping tcam 10 次"):
                logger.info("在boot 模式ping tcam")
                self.bgm_ping_tcam(count=10, err_count=3, condition="boot 下")

    def undef_app_and_ping_tcam(self):
        '''
        在 app 下 ping tcam
        @return:
        '''
        with allure.step(f"在 app 下 bgm ping tcam"):
            # todo 发送1001  退出boot
            with allure.step(f"发送1001   退出boot"):
                self.sd_test.client_sim.send_data_functional_addressing([0x10, 0x01])
                result = self.sd_test.return_udsdata_and_check_and_print_response_result("Send  1001 to get result")
                time.sleep(20)
                self.sd_test.tester_present()
            # todo 检查是否退出boot
            self.sd_test.send_data([0x22, 0xf1, 0x86])
            result = self.sd_test.return_udsdata_and_check_and_print_response_result(
                "Send  0xf1, 0x06 to get result")
            if result[:4] != [0x62, 0xf1, 0x86, 0x01]:
                assert 0, "未退出boot"
            with allure.step(f"退出boot 模式再次ping tcam  10次"):
                logger.info("在非boot 模式ping tcam")
                # todo 进入bgm ping tcam  10次,3次以及以上则 维持现场
                self.bgm_ping_tcam(count=10, err_count=3, condition="退出 boot 下")

    @pytest.mark.repeat(10)
    @pytest.mark.bgm_ping_tcam
    def test_flow(self):
        global test_count
        test_count += 1
        iface_name = self.tc_config['bus']['eth_obd']
        self.sff = SniffPacket(iface=iface_name)
        self.sff.start_sniff()
        try:
            # 诊断重启后，ping tcam 和 上位机
            self.diag_reset_and_ping_tcam_and_nup()
            # 在 boot 下ping tcam
            self.under_boot_and_ping_tcam()
            # 在 app 下ping tcam
            self.undef_app_and_ping_tcam()
            #BGM断电上电后ping tcam 
            self.bgm_power_off_and_on(timeout=15)
            self.bgm_ping_tcam(count=10, err_count=3, condition="BGM断电上电后ping tcam")
            time.sleep(3)
            self.sff.stop_sniff()
        except Exception as e:
            logger.error(f"失败>>>{str(e)}")
            time.sleep(5)
            self.sff.stop_sniff()
            assert 0, str(e)
        finally:
            time.sleep(2)


if __name__ == "__main__":
    pytest.main()
    # pytest 00ltg/test_bgm_ping_tcam.py
