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

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.ecu_sim_const import ECUSimConst
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_cases.legacy.bgm.mcu.case_helper.mcu_interface import *
from xat_cases.legacy.bgm.mcu.case_helper.test_base import TestBase

@allure.feature("架构基础/网络架构")
@allure.story("mcu升级")
class Test_Flash_MCU(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)   
        self.mcu_interface = MCU_Interface()
        self.mcu_interface.prepare_mcu_update_env()
        os.system("ifconfig")

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

    @pytest.mark.update_mcu
    def test_update_mcu(self):
        '''
        升级 mcu
        @return:
        '''
        mcu_version, boot_version = self.mcu_interface.get_mcu_ver()
        with allure.step(f"升级前版本号 mcu_version={mcu_version}, boot_version={boot_version}"):
            pass

        # 第一种升级方式，需要自己下载好vbf 包，放在路径下，需要三个包
        local_path = f"/root/shulin/sat/xat_cases/legacy/bgm/mcu/licheng/300CDC"
        mcu_version, boot_version=self.mcu_interface.update_mcu_flow(local_path,)
        with allure.step(f"升级后版本号 mcu_version={mcu_version}, boot_version={boot_version}"):
            pass

        # local_path="https://repo.jidudev.com/artifactory/BGM_Aptiv/APTIV-to-JIDU/FormalRelease/V1.4/JIDU_BGM_V1.4_bfV6.0_MCU(AM_11.13_CS9498)-BTL(AD_10.04_CS555)-Switch(A0509%26B0206)-20240220.zip"
        # mcu_version, boot_version=self.mcu_interface.update_mcu_flow(local_path)
        # with allure.step(f"升级后版本号 mcu_version={mcu_version}, boot_version={boot_version}"):
        #     pass
        
        # # 第二种，直接复制vbf的zip 包路径，和willow上的路径一样
        # local_path = "https://repo.jidudev.com/artifactory/BGM_Aptiv/APTIV-to-JIDU/FormalRelease/V1.3/JIDU_BGM_V1.3_bfV3.5_MCU(AJ_09.10_CS8339)-BTL(AT_07.19_CS515)-Switch(A0509%26B0204)-20231016.zip"
        # mcu_version, boot_version = self.mcu_interface.update_mcu_flow(local_path)
        # with allure.step(f"升级后版本号 mcu_version={mcu_version}, boot_version={boot_version}"):
        #     pass
        
        # local_path = "/root/ltg02/sat/xat_cases/legacy/mcu/logs/JIDU_BGM_V1.3_bfV6.5hf1_MCU(MY_09.21_CS8794)-BTL(AC_10.03_CS548)-Switch(A0509&B0206)-20231124.zip"
        # mcu_version, boot_version = self.mcu_interface.update_mcu_flow(local_path)
        # with allure.step(f"升级后版本号 mcu_version={mcu_version}, boot_version={boot_version}"):
        #     pass

    # @pytest.mark.willow_update_daliy_mcu_latest_version
    # def test_update_daliy_mcu_latest_version(self):
    #     '''
    #     升级当前 daliy 版本的 最新版本
    #     @return:
    #     '''
    #     url_list = self.mcu_interface.get_mcu_zip_url()
    #     if url_list:
    #         url_dict = {}
    #         ver_list = set()
    #         for item in url_list:
    #             if not item.strip():
    #                 continue
    #             # JIDU_BGM_0200_CS10005_20240523
    #             version_time = int(os.path.basename(item)[:-4].split("_")[-1])
    #             url_dict[version_time] = item
    #             ver_list.add(version_time)
    #         last_ver_time = max(ver_list)
    #         # print(url_dict.get(last_ver_time))

    #         last_url = url_dict.get(last_ver_time)
    #         logger.info(f"当前最新升级包路径为{last_url}")
    #         mcu_version, boot_version = self.mcu_interface.get_mcu_ver()
    #         with allure.step(f"升级前版本号 mcu_version={mcu_version}, boot_version={boot_version}"):
    #             pass

    #         mcu_version, boot_version = self.mcu_interface.update_mcu_flow(last_url)
    #         with allure.step(f"升级后版本号 mcu_version={mcu_version}, boot_version={boot_version}"):
    #             pass

    #     else:
    #         assert 0, "获取升级包路径失败"


if __name__ == "__main__":
    pytest.main()
    # pytest mcu/update_mcu/test_update_mcu.py
