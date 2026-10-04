# -*- coding: utf-8 -*-
"""
@File        : test_example_can_lin_fr.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2023/01/10 18:00 PM
@Description : description about this file
@Examples    : example of how to use it
"""

import os
import re
import sys
import time
import threading

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from xat_cases.legacy.bgm.case_helper.test_base import TestBase
import pytest
import allure
from xat_ecu.legacy.common.logger import logger
from case_helper.monkey import Monkey, monkey_thread_start
from case_helper.pcap import Pcap, pcap_thread_start
from case_helper.tcam_handle import tcam_thread_start, TcamLogCollect
from xat_cases.legacy.perstable.case_helper.constant import testParameter
from case_helper.log_parser import LogParser
from xat_ecu.legacy.interface.bgm.bgm_env.change_bgm_env import change_bgm_config, recover_bgm_config
from case_helper.constant import LOG_PATH, BGM_LOG_PATH, TCAM_LOG_PATH, BGM_COREDUMP_PATH, TCAM_COREDUMP_PATH
from case_helper.utils import *
from xat_ecu.api.interface.ssh import Ssh


@allure.feature("Per-Stable Test")
@allure.story("Test Stability")
class TestPerStable(TestBase):
    def before_class(self, ecu):
        logger.info("Change bgm config")
        change_bgm_config(debug_path="config/debug.sh", s2s_path='config/s2s.json',
                          bgm_app_env_path='config/bgm_app_env.sh')
        super().before_class(self, ecu)
        self.monkey = Monkey()
        self.pcap = Pcap()
        self.tcam_stop_event = threading.Event()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.test_duration = testParameter.get("test_duration", 12) * 3600
        self.log_collect_interval = testParameter.get("collect_interval", 5) * 3600
        self.tcam_log_handle = TcamLogCollect()

    def after_each_func(self, ecu):
        time.sleep(10)
        super().after_each_func(ecu)
        logger.info('停止monkey')
        self.monkey.stop_monkey() if testParameter.get("run_monkey", False) == "true" else ''
        logger.info('停止pcap回放')
        self.pcap.stop_pcap()
        logger.info('停止tcam下发车辆控制指令')
        self.tcam_stop_event.set()

    def after_class(self, ecu):
        super().after_class(self, ecu)
        logger.info("Recover bgm config")
        recover_bgm_config()

    @pytest.mark.parametrize("pcap_file", get_pcap_file(), ids=get_pcap_file(ids=True))
    @pytest.mark.soa_stable
    def test_stable(self, pcap_file):
        with allure.step("记录测试开始时间"):
            start_time = time.time()
            logger.info(f"测试开始时间： {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")

        with allure.step("记录测试版本"):
            self.tcamcli = Ssh("four_domain").tcam_ssh
            with open(os.path.join(LOG_PATH, "version.txt"), "w") as fw:
                bgm_version = self.bgmcli.get_version()
                tcam_version = self.tcamcli.get_version()
                version = "BGM_Version\nbuild_version = " + bgm_version.get("build_version", '') + "\nversion_release = " \
                          + bgm_version.get("version_release", '') + "\n\nTCAM_Version\nversion = " + str(tcam_version)
                fw.write(version)
                allure.attach(version, name="version info", attachment_type=allure.attachment_type.TEXT)

        with allure.step("清除BGM和TCAM的所有log，包括core dump和tcp dump文件"):
            logger.info("清除BGM的所有log，包括core dump和tcp dump文件")
            if str(testParameter.get("clear_bgm_log", "True")).lower() == "true":
                self.bgmcli.clear_log()
                self.bgmcli.clear_coredump(1)
                self.bgmcli.delete_bgm_tcpdump_file()

            logger.info("清除TCAM的所有log，包括core dump文件")
            if str(testParameter.get("clear_tcam_log", "True")).lower() == "true":
                self.tcamcli.clear_log()
                self.tcamcli.clear_coredump(1)

        with allure.step("拉起monkey、pcap、tcam线程"):
            logger.info("开始拉起monkey线程")
            monkey_thread_start() if str(testParameter.get("run_monkey", "False")).lower() == "true" else ''
            logger.info("开始拉起pacap线程")
            assert os.path.exists(pcap_file), f"没有{pcap_file}数据文件存在于/root/test_data文件夹中"
            pcap_thread_start(pcap_file)
            logger.info("开始拉起tcam线程")
            tcam_thread_start(self.tcam_stop_event)

        with allure.step("拉取BGM和TCAM上的jetlog"):
            logger.info("拉取BGM和TCAM上的jetlog")
            current_time = time.time()

            while time.time() - start_time < float(self.test_duration):
                if time.time() - current_time >= float(self.log_collect_interval):
                    current_time = time.time()
                    scp_bgm_file_to_local(bgm_ssh=self.bgmcli, src_path="/log", dest_path=BGM_LOG_PATH)
                    self.tcam_log_handle.copy_tcam_jetlog(tcam_log_path=TCAM_LOG_PATH)

                time.sleep(5)
                print_run_time(time.time() - start_time)
            else:
                scp_bgm_file_to_local(bgm_ssh=self.bgmcli, src_path="/log", dest_path=BGM_LOG_PATH)
                self.tcam_log_handle.copy_tcam_jetlog(tcam_log_path=TCAM_LOG_PATH)

        with allure.step("解析BGM测试log"):
            logger.info("开始解析BGM测试log")
            log_parser = LogParser(bgm_log_path=BGM_LOG_PATH, tcam_log_path=TCAM_LOG_PATH, logger=logger)
            log_parser.handle_bgm_logs()
            test_result = log_parser.parser_test_result(domain="bgm")
            assert test_result.get("mcu", -1) < 1, f"mcu测试失败，发现有{test_result.get('mcu', -1)}次结果不符合预期"
            assert test_result.get("cpu", -1) < 1, f'mcu测试失败，发现有{test_result.get("cpu", -1)}次结果不符合预期'
            assert test_result.get("mem", -1) < 1, f'mcu测试失败，发现有{test_result.get("mem", -1)}次结果不符合预期'

        with allure.step("解析TCAM测试log"):
            logger.info("开始解析TCAM测试log")
            log_parser.handle_tcam_logs()
            test_result = log_parser.parser_test_result(domain="tcam")
            assert test_result.get("cpu", -1) < 1, f'cpu测试失败，发现有{test_result.get("cpu", -1)}次结果不符合预期'
            assert test_result.get("mem", -1) < 1, f'mem测试失败，发现有{test_result.get("mem", -1)}次结果不符合预期'

        with allure.step("检查BGM上的coredump文件"):
            logger.info("检查BGM上的coredump文件")
            bgm_coredump = self.bgmcli.get_bgm_coredump()
            assert len(bgm_coredump) == 0, "bgm有coredump文件生成"
            if len(bgm_coredump):
                logger.info(f"bgm coredump: {','.join(bgm_coredump)}")
                self.bgmcli.copy_coredump(dump_file=None, bench_tmp_path=BGM_COREDUMP_PATH)

        with allure.step("检查TCAM上的coredump文件"):
            logger.info("检查TCAM上的coredump文件")
            assert not self.tcam_log_handle.copy_tcam_coredump(TCAM_COREDUMP_PATH), "TCAM有coredump文件生成"

        with allure.step("检查BGM系统测试过程中是否有重启"):
            logger.info("检查BGM系统测试过程中是否有重启")
            reboot, file, line = is_bgm_reboot()
            assert not reboot, f"BGM系统有重启过。具体请参{file}里面的{line}"
