#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :test_flash_tcam_distributed.py
@time         :5/27/24 15:56
@author       :dejian.xiong@jiduauto.com
@description  :
"""
import json
import os
import time
from time import sleep

import allure
import pytest
from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH

from framework.automotive.core.common_test_base import CommonTestBase
from framework.automotive.utils.conftest_helper import parent_dir
from framework.automotive.utils.data_type import EcuInfo


@allure.feature("架构基础/网络架构")
@allure.story("诊断/诊断刷写")
class Test_Flash_Tcam(CommonTestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # Code Location
        task_path = os.path.join(parent_dir, 'task.json')
        self.file_url = ''
        self.keyinfo = ''
        if os.path.exists(task_path):
            with open(task_path, "r") as f:
                task_dict = json.load(f)
                for update in task_dict.get("update"):
                    for update_type, update_info in update.items():
                        if update_type == "tcam":
                            self.file_url = update_info.get("img_url")
                            self.keyinfo = update_info.get("keyinfo")
        else:
            raise exception_error.ConfigError(f"{task_path}不存在，跳过升级")
        self.domain = ecu.domain
        if self.domain.single_tcam:
            self.tcam_ssh = TCAM_SSH(connect_type='vlan')
        elif self.domain.single_bgm:
            raise Exception("单域BGM无法升级TCAM")
        elif self.domain.two_domain:
            self.tc_config['sd_tester_cfg']['ecu_name'] = "TCAM"
            self.tc_config['gateway_ip'] = "169.254.19.1"
            self.tc_config['server_doip_id'] = 0x1001
            self.tc_config['server_ip'] = ""
            self.tcam_ssh = TCAM_SSH(connect_type='obd')
        elif self.domain.four_domain:
            self.tc_config['sd_tester_cfg']['ecu_name'] = "TCAM"
            self.tc_config['gateway_ip'] = "169.254.19.1"
            self.tc_config['server_doip_id'] = 0x1001
            self.tc_config['server_ip'] = ""
            self.tcam_ssh = TCAM_SSH(connect_type='obd')
        self.tcam_ssh.clear_coredump(2)
        with allure.step('升级前重启一下TCAM'):
            self.tcam_ssh.type_commands(commands='reboot -f')
        self.sd_test = Sd_Tester(**self.tc_config)
        sleep(0.5)
        self.sd_test.diagnostic_client_sim_start()
        sleep(0.5)
        with allure.step('設置车速为0'):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
            # 设置车速为 0
            self.ipdu.set_vehspd(0)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # Code Location

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)

    def after_class(self, ecu):
        # Code Location
        self.sd_test.stop_tester_present()
        sleep(1)
        self.sd_test.diagnostic_client_sim_close()
        sleep(1)
        self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        super().after_class(self, ecu)

    @allure.title('根据url 获取版本名称')
    def get_version_by_url(self, file_url):
        '''
        根据url 获取版本名称
        @param file_url:
        @return:
        '''
        if isinstance(file_url, str):
            try:
                version = file_url.split('/')[-1].split('.')[0]
            except Exception as e:
                logger.error(f"根据 url 路径获取版本号失败：{str(e)}")
                version = None
        else:
            version = None
        return version

    @allure.title("tcam版本平刷")
    @pytest.mark.flaky
    def test_flash_tcam_caseid_1348327(self, ecu: EcuInfo):
        if self.keyinfo and self.file_url:
            tcam_ver = ecu.env_properties_info.get("software_version").get('TCAM')
            if tcam_ver:
                if tcam_ver.replace(" ", "") not in self.file_url:
                    logger.info(f"升级 tcam app ")
                    # 获取 升级的版本
                    with allure.step('获取即将升级的版本'):
                        except_version = self.get_version_by_url(self.file_url)
                        logger.info(f'tcam 期望的版本为{except_version}')
                    with allure.step('tcam 升级过程'):
                        # 进行升级
                        if self.domain.single_tcam:
                            self.sd_test.upgrade_ecu_tcam(self.keyinfo, self.file_url, standard=True,
                                                          check_data=except_version)
                        else:
                            self.sd_test.upgrade_ecu(self.keyinfo, self.file_url, standard=True,
                                                     check_data=except_version)
                else:
                    logger.info("app版本相同，跳过升级")
            else:
                logger.info("tcam_ver未获取到，跳过升级")


if __name__ == "__main__":
    pytest.main()
    # pytest ecu_flash/test_flash_tcam_guard.py
