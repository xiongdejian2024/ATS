# -*- coding: utf-8 -*-
"""
@File        : test_flash_bgm
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/3/1 13:34
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

from xat_cases.legacy.bgm.case_helper.test_base import TestBase

import os
import sys
import time
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
import pytest
import allure
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig
from xat_ecu.legacy.config.path import CONFIG_DIR_PATH
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
from xat_ecu.legacy.sdk.get_obd_ip import get_announcement_ip
from xat_ecu.legacy.sdk.sdk_tools import *


# path_json = "../../../task.json"
willow_path=get_willow_file_path()
if willow_path:
    path_json=os.path.join(willow_path, "task.json")
else:
    path_json="task.json"
logger.info(f'path_json {path_json}')
if os.path.exists(path_json):
    with open(path_json, "r") as f:
        task_dict = json.load(f)
        file_url = task_dict.get("img_url")
        keyinfo = task_dict.get("keyinfo")
        file_url1 = task_dict.get("img_url1")
        keyinfo1 = task_dict.get("keyinfo1")
        flash_flag = task_dict.get("flash_flag")
        img_url_boot = task_dict.get("img_url_boot")
        keyinfo_boot = task_dict.get("keyinfo_boot")
        mcu_ver = task_dict.get("mcu_ver", '').upper().replace(' ', '')
        blt_ver = task_dict.get("blt_ver", '').upper().replace(' ', '')
        switch_ver = task_dict.get("switch_ver", '').upper().replace(' ', '')
        switch_ver_b = task_dict.get("switch_ver_b", '').upper().replace(' ', '')  # f 样以后
        inputTestScriptCMD = task_dict.get("inputTestScriptCMD")


@allure.feature("架构基础/网络架构")
@allure.story("诊断/诊断刷写")
class Test_Flash_BGM(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # Code Location
        self.tc_config['sd_tester_cfg']['ecu_name'] = "BGM"
        BGM_SSH().clear_coredump(2)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # Code Location

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)

    def after_class(self, ecu):
        # Code Location
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

    def flash_func(self, keyinfo, file_url, standard=True, check_data=None):
        '''
        升级
        @param keyinfo:
        @param file_url:
        @param standard:
        @param check_data:
        @return:
        '''

        self.sd_test = Sd_Tester(**self.tc_config)
        sleep(0.5)
        self.sd_test.diagnostic_client_sim_start()
        sleep(0.5)
        # 进行升级
        self.sd_test.upgrade_ecu(keyinfo, file_url, standard=standard, check_data=check_data)

        self.sd_test.stop_tester_present()
        sleep(0.5)
        self.sd_test.diagnostic_client_sim_close()
        sleep(5)

    def check_update_fun(self, keyinfo, file_url):

        # # 获取升级前的切面
        with allure.step('获取bgm升级前的切面'):
            ip = get_announcement_ip()
            hostname = ip if ip else None
            last_boot = BGM_SSH(hostname).get_surface()
            logger.info(f'bgm 升级前{last_boot}')

        # 获取 升级的版本
        with allure.step('获取即将升级的版本'):
            except_version = self.get_version_by_url(file_url)
            logger.info(f'bgm 期望的版本为{except_version}')

        with allure.step('bgm 升级过程 '):
            # 进行升级
            self.flash_func(keyinfo, file_url, standard=True, check_data=except_version)

        ip = get_announcement_ip()
        hostname = ip if ip else None

        #
        with allure.step('校验bgm升级后的switch版本'):
            self.check_bgm_switch_ver()

        # 获取升级后的 切面
        with allure.step('获取bgm升级后的切面'):
            updata_last_boot = BGM_SSH(hostname).get_surface()
            string = f"bgm 升级前为{last_boot}，升级后为{updata_last_boot}"
            logger.info(string)
            # 对比升级前后的切面 是否不同，相同则失败
            assert not last_boot == updata_last_boot, string

        with allure.step('判断bgm升级后是否能 ping 通百度'):
            result = BGM_SSH(hostname).get_ping_baidu()
            assert result, "bgm ping 不通百度"

        with allure.step('判断bgm升级后是否能 ping 8.8.8.8'):
            result = BGM_SSH(hostname).get_ping_8888()
            # assert result, "bgm ping不通8.8.8.8"

        with allure.step('判断bgm升级后是否时间同步'):
            # 看时间是否同步
            result, tim = BGM_SSH(hostname).get_date_time_and_check()
            assert result, "bgm 時間不同步"

    def check_bgm_switch_ver(self):
        '''
        获取 switch 的版本 号
        @return:
        '''

        self.sd_test = Sd_Tester(**self.tc_config)
        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== 获取 mcu ver ==========================")
        self.sd_test.update_serverdoipid(0x1001)
        sleep(0.2)
        # 不校验 返回版本号 字符串
        try:

            switch_version = self.sd_test.read_switch_version_or_check()
            with allure.step(f'获取bgm升级后的switch版本为{switch_version} 本应为{switch_ver}/{switch_ver_b}'):
                logger.info(f'获取bgm升级后的switch版本为{switch_version} 本应为{switch_ver}/{switch_ver_b}')
        except Exception as e:
            logger.info("==================== 获取 switch 版本号异常 ==========================")
            logger.error(e)
            switch_version = None

        try:
            self.sd_test.stop_tester_present()
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info("==================== SdTester Stopped Error ==========================")
            logger.error(e)

        # switch_ver
        if (switch_ver or switch_ver_b) and switch_version not in [switch_ver, switch_ver_b]:
            string=f" switch 的版本号不匹配，本应为{switch_ver}/{switch_ver_b}，实际获取的为{switch_version}"
            logger.error(string)
            assert 0,string


    @allure.title("发布版本平刷 ")
    @pytest.mark.guard
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1350127?projectId=46'
    )
    def test_flash_bgm_caseid_1350127(self):
        with allure.step('設置车速为0'):
            try:
                self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
                self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
                # 设置车速为 0
                self.ipdu.set_vehspd(0)
                time.sleep(5)
                self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
                self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
            except Exception as e:
                logger.warning(f"修改车速失败：{str(e)}")

        with allure.step('判断 boot 是否有升级文件路径'):
            assert file_url, "boot 没有升级路径"

        logger.info(f"升级bgm boot ")
        with allure.step('平刷 boot '):
            self.flash_func(keyinfo_boot, img_url_boot)

        logger.info(f"升级bgm app ")
        with allure.step('判断 bgm 是否有升级文件路径'):
            assert file_url, "bgm 没有升级路径"
        with allure.step('平刷 bgm '):
            self.check_update_fun(keyinfo, file_url)


if __name__ == "__main__":
    pytest.main()
    # pytest ecu_flash/test_flash_bgm_guard.py --tbcfg="bench_config/soa_test_cabinet01.yaml"
