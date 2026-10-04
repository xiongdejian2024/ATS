#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :test_flash_bgm_distributed.py
@time         :5/27/24 15:48
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

from framework.automotive.core.common_test_base import CommonTestBase
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH

from framework.automotive.utils.conftest_helper import parent_dir
from framework.automotive.utils.data_type import EcuInfo


@allure.feature("架构基础/网络架构")
@allure.story("诊断/诊断刷写")
class Test_Flash_BGM(CommonTestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # Code Location
        self.tc_config['sd_tester_cfg']['ecu_name'] = "BGM"
        task_path = os.path.join(parent_dir, 'task.json')
        self.file_url = ''
        self.keyinfo = ''
        self.img_url_boot = ''
        self.keyinfo_boot = ''
        if os.path.exists(task_path):
            with open(task_path, "r") as f:
                task_dict = json.load(f)
                for update in task_dict.get("update"):
                    for update_type, update_info in update.items():
                        if update_type == "bgm":
                            self.file_url = update_info.get("img_url")
                            self.keyinfo = update_info.get("keyinfo")
                        if update_type == "boot":
                            self.img_url_boot = update_info.get("img_url_boot")
                            self.keyinfo_boot = update_info.get("keyinfo_boot")
        else:
            raise exception_error.ConfigError(f"{task_path}不存在，跳过升级")
        BGM_SSH().clear_coredump(2)
        self.sd_test = Sd_Tester(**self.tc_config)
        sleep(0.5)
        self.sd_test.diagnostic_client_sim_start()
        sleep(0.5)
        self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
        self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
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
        sleep(0.5)
        self.sd_test.diagnostic_client_sim_close()
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

    @allure.title("升级BGM boot")
    @pytest.mark.flaky
    def test_flash_bgm_boot(self, ecu: EcuInfo):
        except_version = self.get_version_by_url(self.img_url_boot)
        logger.info(f'bgm 期望的boot版本为{except_version}')
        if self.keyinfo_boot and self.img_url_boot:
            if ecu.env_properties_info.bgm_boot_version not in self.img_url_boot:
                logger.info(f"升级bgm boot ")
                with allure.step('平刷 boot '):
                    self.sd_test.upgrade_ecu(self.keyinfo_boot, self.img_url_boot, standard=True,
                                             check_data=except_version)
            else:
                logger.info(f"boot版本一致，跳过升级")

    @allure.title("升级BGM app")
    @pytest.mark.flaky
    def test_flash_bgm_app(self, ecu: EcuInfo):
        except_version = self.get_version_by_url(self.file_url)
        logger.info(f'bgm 期望的app版本为{except_version}')
        if self.keyinfo and self.file_url:
            bgm_ver = ecu.env_properties_info.get("software_version").get('BGM')
            if bgm_ver:
                if bgm_ver.replace(" ", "") not in self.file_url:
                    logger.info(f"升级bgm app ")
                    with allure.step('平刷 bgm '):
                        self.sd_test.upgrade_ecu(self.keyinfo, self.file_url, standard=True, check_data=except_version)
                else:
                    logger.info("app版本一致，跳过升级")
            else:
                logger.info("bgm_ver未获取到，跳过升级")


if __name__ == "__main__":
    pytest.main()
    # pytest ecu_flash/test_flash_bgm_guard.py --tbcfg="bench_config/soa_test_cabinet01.yaml"
