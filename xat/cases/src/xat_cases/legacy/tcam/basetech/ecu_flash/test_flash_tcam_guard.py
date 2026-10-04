# -*- coding: utf-8 -*-
"""
@File        : test_flash_bgm
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/3/1 13:34
@Description :

"""
import sys, os
import json

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

work_path_2 = os.path.join(os.getcwd().split("sat")[0], 'sat', 'ecu_simulator', 'interface')
sys.path.append(work_path_2)

import os
import sys
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
import pytest
import allure
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
from xat_ecu.legacy.sdk.sdk_tools import *

# path_json = "../../../task.json"
willow_path = get_willow_file_path()
if willow_path:
    path_json = os.path.join(willow_path, "task.json")
else:
    path_json = "task.json"
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
class Test_Flash_Tcam(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # Code Location
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
        if self.domain.single_tcam:
            self.sd_test.upgrade_ecu_tcam(keyinfo, file_url, standard=standard, check_data=check_data)
        else:
            self.sd_test.upgrade_ecu(keyinfo, file_url, standard=standard, check_data=check_data)
        self.sd_test.stop_tester_present()
        sleep(0.5)
        self.sd_test.diagnostic_client_sim_close()
        sleep(5)

    def check_update_fun(self, keyinfo, file_url):

        # # 获取升级前的切面
        with allure.step('获取 tcam 升级前的切面'):
            last_boot = TCAM_SSH().get_surface()
            logger.info(f'tcam 升级前{last_boot}')

        # 获取 升级的版本
        with allure.step('获取即将升级的版本'):
            except_version = self.get_version_by_url(file_url)
            logger.info(f'tcam 期望的版本为{except_version}')

        with allure.step('tcam 升级过程 '):
            # 进行升级
            self.flash_func(keyinfo, file_url, standard=True, check_data=except_version)

        # 获取升级后的 切面
        with allure.step('获取tcam升级后的切面'):
            updata_last_boot = TCAM_SSH().get_surface()
            string = f"tcam 升级前为{last_boot}，升级后为{updata_last_boot}"
            logger.info(string)
            # 对比升级前后的切面 是否不同，相同则失败
            assert not last_boot == updata_last_boot, string

        with allure.step('判断tcam升级后是否能 ping 通百度'):
            result = TCAM_SSH().get_ping_baidu()
            assert result, "tcam ping 不通百度"

        with allure.step('判断bgm升级后是否能 ping 8.8.8.8'):
            result = TCAM_SSH().get_ping_8888()
            # assert result, "tcam ping不通8.8.8.8"

        with allure.step('判断tcam升级后是否时间同步'):
            # 看时间是否同步
            result, tim = TCAM_SSH().get_date_time_and_check()
            assert result, "tcam 時間不同步"

    @allure.title("tcam版本平刷 ")
    @pytest.mark.guard
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1348327?projectId=46'
    )
    def test_flash_tcam_caseid_1348327(self):
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

        logger.info(f"升级 tcam app ")
        with allure.step('判断 tcam 是否有升级文件路径'):
            assert file_url, "tcam 没有升级路径"

        with allure.step('平刷 tcam '):
            self.check_update_fun(keyinfo, file_url)


if __name__ == "__main__":
    pytest.main()
    # pytest ecu_flash/test_flash_tcam_guard.py
