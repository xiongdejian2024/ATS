# -*- coding: utf-8 -*-
"""
@File        : test_update_bgm.py
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/5/31 14:01
@Description : 升级bgm    boot 或者app

"""
import time
import pytest
import allure
import sys, os
import json

from xat_ecu.legacy.sdk.sdk_tools import get_willow_file_path

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
import threading


@allure.feature("架构基础/网络架构")
@allure.story("诊断/诊断刷写")
class Test_Flash_BGM(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.tc_config['sd_tester_cfg']['ecu_name'] = "BGM"
        self.sdb_version = ecu.get('sdb_version')
        if not self.sdb_version:
            raise Exception('缺少--sdb_version=版本号，无法升级')
        self.release_version = ecu.get('release_version')
        if not self.release_version:
            raise Exception('缺少--release_version=版本号，无法升级')
        BGM_SSH().clear_coredump(2)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # Code Location
        # 开启tcpdump 抓包
        t = threading.Thread(target=self.tcp_dump)
        t.setDaemon(True)
        t.start()
        time.sleep(2)

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)
        # 停止抓包
        time.sleep(10)
        cmd = "ps -ef | grep tcpdump| awk '{print $2}' | xargs kill -9"
        os.system(cmd)

    def after_class(self, ecu):
        # Code Location
        super().after_class(self, ecu)

    def tcp_dump(self):
        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
        bord = self.tc_config.get("bus", {}).get("eth_obd", "any")
        logger.info(f"bord={bord}")
        path = os.path.dirname(__file__)

        logger.info(f"tcpdump 抓包保存路径为={path}")

        cmd = f"sudo tcpdump -i {bord}  -w {path}/update_bgm{otherStyleTime}.cap"
        os.system(cmd)

    def flash_func(self, keyinfo, file_url, standard=True, check_data=None, update_type=None):
        '''
        升级
        @param keyinfo:
        @param file_url:
        @param standard:
        @param check_data:
        @param update_type:
        @return:
        '''

        self.sd_test = Sd_Tester(**self.tc_config)
        sleep(0.5)
        self.sd_test.diagnostic_client_sim_start()
        sleep(0.5)
        # 进行升级
        if update_type == 'boot':
            self.sd_test.update_serverdoipid(0x1002)
            boot_version = self.sd_test.read_boot_version_or_check()
            self.sd_test.update_serverdoipid(0x1001)
            app_ver, boot_ver = file_url.split('_')
            if boot_ver not in boot_version:
                self.sd_test.upgrade_ecu(keyinfo, file_url, standard=standard, check_data=check_data)
            else:
                logger.info('boot版本一致，无需升级')
            logger.info('升级bgm app ')
            self.sd_test.upgrade_ecu(keyinfo, app_ver, standard=standard, check_data=check_data)
        else:
            self.sd_test.upgrade_ecu(keyinfo, file_url, standard=standard, check_data=check_data)
        self.sd_test.stop_tester_present()
        self.sd_test.diagnostic_client_sim_close()

    def test_flash_bgm_caseid_0000(self):
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
        """
        pytest bgm_tools/test_update_bgm.py --sdb_version=1.3.0 --release_version=AU_AT
        release_version参数如果只升级app 直接指定版本 例如AU
        release_version参数如果只升级app和boot 直接指定版本 使用下划线隔开 例如AU_AT (第一个为app版本 第二个为boot版本)
        如果boot版本一致 则不升级boot
        """
        if '_' in self.release_version:
            logger.info(f"升级bgm boot ")
            self.flash_func(self.sdb_version, self.release_version, update_type='boot')
        else:
            logger.info(f"升级bgm app ")
            self.flash_func(self.sdb_version, self.release_version)


if __name__ == "__main__":
    pytest.main()
    # pytest bgm_tools/test_update_bgm.py --sdb_version=1.3.0 --release_version=AC_BH
