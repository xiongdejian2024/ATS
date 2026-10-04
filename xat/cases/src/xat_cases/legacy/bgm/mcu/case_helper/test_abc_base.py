# -*- coding: utf-8 -*-
"""
@File        : test_abc_base.py
@Author      : dejian.xiong@jiduauto.com
@Time        : 2023/11/3 14:30
@Description :
@Examples    :
"""

import os
import sys
import time

project_root = os.path.join(os.getcwd(), 'sat')
sys.path.append(project_root)

from xat_cases.legacy.common_abc_test_base import CommonABCTestBase
from xat_ecu.legacy.common.logger import *
from xat_ecu.legacy.sdk.sdk_tools import *


class TestABCBase(CommonABCTestBase):
    def before_class(self, ecu):
        try:
            self.boot_version, self.mpu_version = self.sd_tester.read_bgm_mpu_version()
            self.mcu_version = self.sd_tester.read_bgm_mcu_version()
            # boot_version=self.sd_tester.read_bgm_boot_version()
            self.case_start_bgm_uptime = self.ssh.get_bgm_uptime()
            self.case_start_time = time.time()
        except Exception as e:
            logger.info(f"读取时间失败！{str(e)}")
            self.boot_version, self.mpu_version, self.mcu_version = None, None, None
        try:
            self.mix.get_mcu_cpuload_save_data(mcu_version=self.mcu_version, boot_version=self.boot_version,
                                               mpu_version=self.mpu_version)
        except Exception as e:
            logger.warning(f"读取cpu load 失败{str(e)}")
        # 检查有没有cordump 文件产生
        try:
            self.pre_coredump_names_list = self.ssh.get_bgm_coredump_names()
        except Exception as e:
            self.pre_coredump_names_list = None
            logger.warning(f"运行前获取coredump 文件名称失败{str(e)}")

        self.save_name = 'obd_doip_'
        self.save_path = '/root/bgm_log/obd_doip_dump'
        self.iface = self.tc_config.get("bus", {}).get("eth_obd", any)  # ['bus']['eth_obd']  # 'enp114s0'
        self.obd_dump = False

    def before_each_func(self, ecu, obd_dump=False):
        # 是否需要obd 口抓包
        if obd_dump:
            self.obd_dump = True
            try:
                # 获取当前用例名字
                current_case = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
                self.save_name = current_case + '_'
                # 开始抓包
                self.base_sniff = SniffPacket(iface=self.iface, save_name=self.save_name, save_path=self.save_path)
                self.base_sniff.start_sniff()
            except Exception as e:
                logger.warning(f"开启OBD口抓包失败{str(e)}")

    def after_each_func(self, ecu):
        # 停止obd 口抓包
        if self.obd_dump:
            self.obd_dump = False
            try:
                self.base_sniff.stop_sniff()
                # 删除成功用例的抓包，减少占用空间
                # file_path=self.base_sniff.file_path
                # cmd=f"rm -rf {file_path}"
                # os.system(cmd)
            except Exception as e:
                logger.warning(f"停止抓包失败{str(e)}")

    def after_class(self, ecu):
        try:
            self.case_end_bgm_uptime = self.ssh.get_bgm_uptime()
            self.case_end_time = time.time()
            case_time = round(self.case_end_time - self.case_start_time, 2)
            bgm_time = (self.case_end_bgm_uptime - self.case_start_bgm_uptime) * 60
            if bgm_time < 0:
                logger.error("bgm 在用例执行中有重启，需关注下是否用例自身重启！！！！！！")
            else:
                string = f"用例执行时间{case_time}秒,bgm的时间{bgm_time}秒，相差{case_time - bgm_time}秒"
                if case_time - bgm_time > 60:
                    logger.error(string + "bgm 可能在用例执行过程中重启，需关注下是否用例自身重启！！！！！！")
                else:
                    logger.info(string)
        except Exception as e:
            logger.warning(f"读取时间失败！{str(e)}")
        # 检查有没有cordump 文件产生
        try:
            self.after_coredump_names_list = self.ssh.get_bgm_coredump_names()
        except Exception as e:
            self.after_coredump_names_list = None
            logger.warning(f"运行结束获取coredump 文件名称失败{str(e)}")
        try:
            if self.after_coredump_names_list is not None and self.pre_coredump_names_list is not None:
                if self.after_coredump_names_list != self.pre_coredump_names_list:
                    new_lis = [item for item in self.after_coredump_names_list if item not in self.pre_coredump_names_list]
                    logger.error(f"运行当前类产生coredump 文件{new_lis}")
        except Exception as e:
            logger.warning(f"判断coredump 流程失败{str(e)}")
