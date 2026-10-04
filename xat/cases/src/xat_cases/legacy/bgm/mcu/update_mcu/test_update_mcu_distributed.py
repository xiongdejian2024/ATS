#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :test_update_mcu_distributed.py
@time         :6/4/24 13:19
@author       :dejian.xiong@jiduauto.com
@description  :
"""
import json
import os

import pytest
import allure
from xat_ecu.legacy.common import exception_error

from framework.automotive.utils.conftest_helper import parent_dir
from xat_cases.legacy.bgm.mcu.case_helper.mcu_interface import MCU_Interface
from xat_cases.legacy.bgm.mcu.case_helper.test_base import TestBase


@allure.feature("架构基础/网络架构")
@allure.story("mcu升级")
class Test_Willow_Flash_MCU(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        task_path = os.path.join(parent_dir, 'task.json')
        self.MCU_ZIP_URL = ''
        if os.path.exists(task_path):
            with open(task_path, "r") as f:
                task_dict = json.load(f)
                for update in task_dict.get("update"):
                    for update_type, update_info in update.items():
                        if update_type == "mcu":
                            self.MCU_ZIP_URL = task_dict.get("mcu_zip_url")
        else:
            raise exception_error.ConfigError(f"{task_path}不存在，跳过升级")
        self.mcu_interface = MCU_Interface()
        self.mcu_interface.prepare_mcu_update_env()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # Code Location

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)

    def after_class(self, ecu):
        # Code Location
        super().after_class(self, ecu)
        self.mcu_interface.restore_mcu_update_env()

    @pytest.mark.willow_update_mcu
    def test_update_mcu(self):
        '''
        升级 mcu
        @return:
        '''
        # 保存 升级时间
        if self.MCU_ZIP_URL:
            mcu_version, boot_version = self.mcu_interface.get_mcu_ver()
            with allure.step(f"升级前版本号 mcu_version={mcu_version}, boot_version={boot_version}"):
                pass

            mcu_version, boot_version = self.mcu_interface.update_mcu_flow(self.MCU_ZIP_URL)
            with allure.step(f"升级后版本号 mcu_version={mcu_version}, boot_version={boot_version}"):
                pass


if __name__ == "__main__":
    pytest.main()
    # pytest update_mcu/test_update_mcu.py
