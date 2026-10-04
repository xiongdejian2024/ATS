# -*- coding: utf-8 -*-
"""
@File        : 离线刷写台
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/11/27 13:11
@Description :

"""
import threading
import time
import pytest
import allure
import sys, os
import json

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

work_path_2 = os.path.join(os.getcwd().split("sat")[0], 'sat', 'soa_lib', 'interface')
sys.path.append(work_path_2)

from xat_cases.legacy.bgm.mcu.case_helper.test_base import TestBase

import os
import sys
import time
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.mcu.case_helper.test_base import TestBase
import pytest
import allure
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
from xat_ecu.legacy.driver.ssh_interface import command_send, file_download, file_upload

sniff_count = 0


@allure.feature("架构基础/网络架构")
@allure.story("诊断/诊断刷写")
class Test_Flash_BGM(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
        path = os.path.dirname(__file__)
        self.save_path = os.path.join(path, f'{otherStyleTime}_pcap_file')
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)

        self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
        self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        # 设置车速为 0
        self.ipdu.set_vehspd(0)
        # todo - 使用can报文 533#3350FFFFFFFFFFFF保持TCAM
        self.ipdu.send_pdu('connectivitycanfd', 0x533, [0x33, 0x50, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff],cycle_time=0.5)

        time.sleep(5)

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

        self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文

    def tcp_dump(self):
        global sniff_count
        sniff_count += 1
        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
        bord = self.tc_config.get("bus", {}).get("eth_vlan", "any")
        logger.info(f"bord={bord}")
        # path = os.path.dirname(__file__)

        # save_path = os.path.join(path, 'pcap_file')
        # if not os.path.exists(save_path):
        #     os.mkdir(save_path)

        file_path = f"{self.save_path}/{sniff_count}_update_bgm_{otherStyleTime}.pcap"
        logger.info(f"第{sniff_count} tcpdump 抓包保存路径为={file_path}")
        cmd = f"sudo tcpdump -i {bord}  -w {file_path}"
        os.system(cmd)

    def flash_func(self, keyinfo, file_url, standard=True, check_data=None):
        '''
        升级
        @param keyinfo:
        @param file_url:
        @param standard:
        @param check_data:
        @return:
        '''
        self.tc_config["sd_tester_cfg"]["ecu_name"] = "TCAM"
        self.sd_test = Sd_Tester(**self.tc_config)
        self.sd_test.diagnostic_client_sim_start()
        sleep(0.5)
        # 进行升级
        self.sd_test.upgrade_ecu_tcam(keyinfo, file_url, standard=standard, check_data=check_data)

        self.sd_test.stop_tester_present()
        self.sd_test.diagnostic_client_sim_close()

    def update_bgm_offline(self, bin_dic, new_bgm=False):
        with allure.step('**********************************离线刷写开始***********************************'):
            logger.info("离线刷写开始")

        self.ecu_name = "TCAM"

        self.sd_test = Sd_Tester(**self.tc_config)
        self.sd_test.diagnostic_client_sim_start()
        self.sd_test.tester_present()

        with allure.step('ECU信息读取'):
            self.sd_test.update_serverdoipid(0x1011, ecu=self.ecu_name)
            with allure.step('  - step1:给MPU(1011)发送 10 01 ----> 回复正响应：50 01 xx xx yy yy '):
                sleep(5)   # 新需求改动，发送公告后，大于5s后再发送 10 01
                self.sd_test.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])

            with allure.step('  - step2: 给MPU(1011)发送 22 F1AE ---> 回复正响应：62 F1 AE xx xx ... xx'):
                self.sd_test.send_request_and_recv_response(
                    [0x22, 0xF1, 0XAE],
                    recv=[0x62, 0xF1,
                          0XAE])

            with allure.step('  - step3: 给MPU(1011)发送 22 F1AA ---> 回复正响应：62 F1 AA xx xx ... xx'):
                err_code, send_22f1aa_recv_data_before_update = self.sd_test.send_request_and_recv_response(
                    [0x22, 0xF1, 0XAA],
                    recv=[0x62, 0xF1, 0XAA])

            with allure.step('  - step4: 给MPU(1011)发送 22 F18C ---> 回复正响应：62 F1 8C xx xx ... xx'):
                err_code, send_22f18c_recv_data_before_update = self.sd_test.send_request_and_recv_response(
                    [0x22, 0xF1, 0X8C],
                    recv=[0x62, 0xF1, 0X8C])

        with allure.step('来料检查'):
            with allure.step('  - MPU(0x1011) 信息检查'):
                self.sd_test.update_serverdoipid(0x1011, ecu=self.ecu_name)
                with allure.step('    - 检查前提条件：10 03 ---> 回复正响应：50 03 xx xx yy yy'):
                    self.sd_test.send_request_and_recv_response([0x10, 0x03], recv=[0x50, 0x03])

                with allure.step('- 检查public key写入状态：22 D0 3A ---> 回复负响应：NRC22'):
                    self.sd_test.send_request_and_recv_response([0x22, 0xD0, 0X3A], recv=[0x7F, 0x22,0x31])

                with allure.step('- 0E 80 ---> 1002 发送 27 05 ---> 回复：67 05 S1 S2 S3'):
                    self.sd_test.security_access_level_l3()

                with allure.step(
                        '- 检车证书状态：22 B1 63 ---> 回复正响应：62 B1 63 xx xx ... xx(16 bytes 全0x00 or 全 0xFF)'):
                    err_code, recv_data_list = self.sd_test.send_request_and_recv_response([0x22, 0xB1, 0X63],
                                                                                           recv=[0x62, 0xB1, 0X63])
                    check_data_list = [
                        [0x00] * 16,
                        [0xFF] * 16,
                    ]
                    rcv_data = recv_data_list[3:]
                    if new_bgm:
                        if rcv_data not in check_data_list:
                            assert 0, f"发送22 B1 63 获取的值应该为全0 或者全ff 实际为{rcv_data}"

                with allure.step('    - 防止安全常数被写入过：27 11 ---> 回复负响应：67 11 S1 S2 S3'):
                    self.sd_test.security_access_level_l6()

        # return
        with allure.step('刷写过程中'):
            self.sd_test.update_serverdoipid(0x1011, ecu=self.ecu_name)

            app_url = bin_dic.get('app_url')
            app_key_info = bin_dic.get('app_key_info')
            update_app_ver = None
            if app_url:
                with allure.step('刷写 app'):
                    update_app_ver = app_url[-16:-4]  # self.sd_test.get_version_by_url(app_url)
            with allure.step(f'刷写 app 版本号为》》{update_app_ver}'):
                self.sd_test.upgrade_ecu_tcam(app_key_info, app_url, read_ver=True, offline_flashing=True)

        # 开启 3E80
        self.sd_test.tester_present()

        with allure.step('刷写后'):

            with allure.step('- Step1:检查F1 AE/F1 AA/F18C 信息'):
                self.sd_test.update_serverdoipid(0x1011, ecu=self.ecu_name)
                time.sleep(1)
                with allure.step('- 0E 80 ---> 1001 发送 10 01 ---> 回复：50 01 xx xx yy yy'):
                    self.sd_test.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])

                with allure.step(
                        '- 0E 80 ---> 1001 发送 22 F1 AE ---> 回复：62 F1 AE xx xx ... xx（软件版本需要版本与刷写的版本一致）'):
                    mcu_ver = self.sd_test.get_soft_version()

                    if update_app_ver and str(update_app_ver).upper() != str(mcu_ver).upper().replace(" ", ''):
                        assert 0, f"升级的 app 版本为{update_app_ver} 实际读出来的版本为{mcu_ver}"

                with allure.step(
                        '    - 0E 80 ---> 1001 发送 22 F1 AA ---> 回复：62 F1 AA xx xx ... xx (需要与刷写前保持一致)'):
                    err_code, send_22f1aa_recv_data_after_update = self.sd_test.send_request_and_recv_response(
                        [0x22, 0xF1, 0XAA], recv=[0x62, 0xF1, 0XAA])
                    if send_22f1aa_recv_data_after_update != send_22f1aa_recv_data_before_update:
                        assert 0, "刷写前后22 F1 AA 读取的值不同 "

                with allure.step(
                        '- 0E 80 ---> 1001 发送 22 F1 8C ---> 回复：62 F1 8C xx xx ... xx (需要与刷写前保持一致) '):
                    err_code, send_22f18c_recv_data_after_update = self.sd_test.send_request_and_recv_response(
                        [0x22, 0xF1, 0X8C], recv=[0x62, 0xF1, 0X8C])
                    if send_22f18c_recv_data_after_update != send_22f18c_recv_data_before_update:
                        assert 0, "刷写前后22 F1 8c 读取的值不同 "

        try:
            self.sd_test.stop_tester_present()
            self.sd_test.diagnostic_client_sim_close()

        except Exception as e:
            logger.error(f">>>>error>>>{str(e)}")
            pass
        with allure.step('**********************************离线刷写结束***********************************'):
            logger.info("离线刷写结束")

    @pytest.mark.repeat(1)
    @pytest.mark.update_tcam_offline
    def test_update_tcam_offline(self):

        bin_dic_list = [
            {
                # 版本 1 罐装版本 v1.1EB

                'app_url': "https://repo.jidudev.com/artifactory/TCAMSoftware/Release/v1.1.0/6110110110EB/6110110110EB.bin",
                'app_key_info': __import__("os").environ.get('XAT_CREDENTIAL____TCAM_BASETECH_INDUSTRIALIZATION_TEST_FLASH_TCAM_PY_APP_KEY_INFO', "")
            },

            # {
            #     # 版本2 weekly版本
            #     'app_url': "https://repo.jidudev.com/artifactory/TCAMSoftware/Release/v1.3.0/6110110130AU/6110110130AU.bin",
            #     'app_key_info': "ZVpnvgyG5HxzLudNaBk0/dyEEJ3rZlpRQ4leDOhSYC1kOnlP9FNPNyx+rPpdEHlfYoXlOr8vF0vN0Voyhmn+YkJWgeBOt26TlILWR0VvHStqP1+r3LYxHGtZOFPYwT8fU0042cU1dvkADi/ognQViO4V9RLvDX3cImFbdlN0ICOh5Tk7TLfO2AYK+lzYMy9sD41NZvG8swhx74IYVMOXx+nqV6YTv1CRpcrE3MXxCYdBQU0+8WMBnIQj4/gAptQ0wxv20Xeo60uGyOQ0YyqPffCNrvSFtCSuIw7RQC/cT5/ru9Gfreq2MeuXIWzAcE5Bv7nz3nFGaRUsCFm42v32yg=="
            # },
        ]

        for bin_dic in bin_dic_list:
            if not bin_dic:
                continue
            try:
                self.update_bgm_offline(bin_dic, new_bgm=False)
            except Exception as e:
                logger.error(f"{str(e)}")

                tcam_ssh = TCAM_SSH()
                tcam_ssh.get_log()
                assert 0, str(e)
                

        # 只升级

        # # 升级app
        # app_key_info = bin_dic_list[0]['app_key_info']
        # app_url = bin_dic_list[0]['app_url']
        # self.flash_func(keyinfo=app_key_info, file_url=app_url)


if __name__ == "__main__":
    pytest.main()
    # pytest pressure/test_flash_tcam.py

    #  需求来源  https://jiduauto.feishu.cn/wiki/DyQcwAEw0iBF61kBYmEcDnOmnEf
