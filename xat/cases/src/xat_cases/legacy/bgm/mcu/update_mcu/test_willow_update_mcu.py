# -*- coding: utf-8 -*-
"""
@File        : test_update_mcu
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/10/10 20:10
@Description :

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
import time
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

import base64
import pytest
import allure
from xat_cases.legacy.bgm.mcu.case_helper.test_base import TestBase
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.ecu_sim_const import ECUSimConst
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_cases.legacy.bgm.mcu.case_helper.mcu_interface import *
from xat_ecu.legacy.sdk.sdk_tools import *

willow_path = get_willow_file_path()
if willow_path:
    path_json = os.path.join(willow_path, "task.json")
else:
    path_json = "task.json"

MCU_ZIP_URL = ''
logger.info(f'path_json {path_json}')
if os.path.exists(path_json):
    with open(path_json, "r") as f:
        task_dict = json.load(f)
        logger.info(f'task_dict ==>>{task_dict}')
        MCU_ZIP_URL = task_dict.get("mcu_zip_url")
        logger.info(f'接收 MCU_ZIP_URL ==>>{MCU_ZIP_URL}')
        inputTestScriptCMD = task_dict.get("inputTestScriptCMD")


@allure.feature("架构基础/网络架构")
@allure.story("mcu升级")
class Test_Willow_Flash_MCU(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.mcu_interface = MCU_Interface()
        self.mcu_interface.prepare_mcu_update_env()
        self.willow_update_mcu_time_path = r"/root/mcu_auto_update_time"
        self.set_time = ecu.get("ecu_time", 5)  # 单位为小时
        

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
        try:
            if not os.path.exists(self.willow_update_mcu_time_path):
                os.mkdir(self.willow_update_mcu_time_path)
            full_path = os.path.join(self.willow_update_mcu_time_path, "update_time.txt")
            with open(full_path, 'a', encoding="utf-8") as f:
                time1 = time.time()
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time1)))
                string = f"{otherStyleTime} time={time1}\n"
                f.write(string)
        except Exception as e:
            string = f"保存生成时间失败>>{str(e)}"
            logger.error(string)

        mcu_version, boot_version = self.mcu_interface.get_mcu_ver()
        with allure.step(f"升级前版本号 mcu_version={mcu_version}, boot_version={boot_version}"):
            pass

        mcu_version, boot_version=self.mcu_interface.update_mcu_flow(MCU_ZIP_URL)
        with allure.step(f"升级后版本号 mcu_version={mcu_version}, boot_version={boot_version}"):
            pass

    @pytest.mark.get_willow_update_mcu_time
    def test_mcu_update_time(self):
        '''
        在 指定时间
        @return:
        '''
        set_time = float(self.set_time)  # 单位为小时
        flag = True
        if not os.path.exists(self.willow_update_mcu_time_path):
            string = "未自动化升级mcu,需要跑定时冒烟测试"
            with allure.step(string):
                logger.info(string)
        else:
            try:
                full_path = os.path.join(self.willow_update_mcu_time_path, "update_time.txt")
                with open(full_path, 'r', encoding="utf-8") as f:
                    lines = f.readlines()
                    last_line = lines[-1]
                    mcu_auto_update_time = last_line.split('time=')[-1].strip()
                    string = f"mcu最近一次自动化升级时间为{last_line}"
                    with allure.step(string):
                        logger.info(string)
                    current = time.time()
                    tmep = current - float(mcu_auto_update_time)
                    if tmep > 1:  # set_time * 3600:
                        string = f"在{set_time}小时内未自动升级跑过冒烟测试，需要跑定时冒烟任务"
                    else:
                        flag = False
                        string = f"已经在{set_time}小时前自动升级跑过冒烟测试，不需要跑定时冒烟任务"
                    with allure.step(string):
                        logger.info(string)
            except Exception as e:
                string = f"读取mcu自动升级的时间失败>>{str(e)}"
                logger.error(string)
                flag = True
            assert flag, string



if __name__ == "__main__":
    pytest.main()
    # pytest update_mcu/test_update_mcu.py
