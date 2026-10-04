# -*- coding: utf-8 -*-
"""
@File        : test_willow_flash_bgm.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022/08/26 18:00 PM
@Description : description about this file
@Examples    : example of how to use it
"""

import os
import sys
import time
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
sys.path.append(os.path.join(os.getcwd(), "../../../.."))
import os
import pytest
import allure
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from time import sleep
import inspect
from xat_ecu.legacy.common.logger import logger
# from ecu_simulator.interface.bgm.bgm_ssh import BGM_SSH
from threading import Thread
from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig
from xat_ecu.legacy.sdk.get_obd_ip import get_announcement_ip
from xat_ecu.legacy.sdk.i_signal_i_pdu import *
from xat_ecu.legacy.sdk.bus_app import BusApp

flash_count = 0


# @pytest.mark.flash
# @pytest.mark.diag
class TestUdsFlashDoipSimBgm():
    def __init__(self):
        self.bgm_file_url = "https://repo.jidudev.com/artifactory/BGMSoftware/release_build/6160110055BR.bin"
        self.keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_6D25F37F817B1D3C1142']
        tb_path = os.path.join(os.path.realpath(__file__).split("ecu_simulator")[0],
                               "ecu_simulator/config/willow_bgm_flash_config.yaml")
        tb_config = ParseTBConfig(tb_path)
        self.tb_config = tb_config.yaml_content
        try:
            self.veh_type = self.tb_config.get("veh_type")
            self.bl_ver = self.tb_config.get("bl_ver")
            if self.veh_type and self.bl_ver:
                self.cls_path = "sdk/data/{}/can_lin_fr_cls/{}".format(
                    self.veh_type, self.bl_ver
                )
                self.tn_config_path = "config/{}/{}/ecu_network.yaml".format(
                    self.veh_type, self.bl_ver
                )
            else:
                logger.error(
                    "Config error : self.veh_type is {}  self.bl_ver is {}".format(
                        self.veh_type, self.bl_ver
                    )
                )
            self.dut_ecu = self.tb_config.get("dut_ecu")
            set_sig_auto(self.cls_path)  # set sig auto version
            self.ipdu = ISignalIPdu(cls_path=self.cls_path, dut_ecu=self.dut_ecu)
            self.busapp = BusApp(self.ipdu, **self.tb_config)
            # self.bgm_ssh = BGM_SSH()
            # self.bgm_ssh.clear_coredump(2)
        except Exception as e:
            logger.warning(f"ipdu 初始化失败：{str(e)}")

    def get_bgm_mcu_and_boot_ver(self):
        '''
        获取 mcu boot 的版本 号
        @return:
        '''
        self.sd_test = Sd_Tester(**self.tb_config)
        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== 获取 mcu ver ==========================")
        self.sd_test.update_serverdoipid(0x1002)
        sleep(0.2)
        # 不校验 返回版本号 字符串

        try:
            mcu_version = self.sd_test.read_mcu_version_or_check()
        except Exception as e:
            logger.info("==================== 获取mcu 版本号异常 ==========================")
            logger.error(e)
            mcu_version = None
        try:
            boot_version = self.sd_test.read_boot_version_or_check()
        except Exception as e:
            logger.info("==================== 获取 boot 版本号异常  ==========================")
            logger.error(e)
            boot_version = None

        try:
            self.sd_test.stop_tester_present()
            sleep(0.5)
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info("==================== SdTester Stopped Error ==========================")
            logger.error(e)

        return mcu_version, boot_version

    def get_bgm_switch_ver(self):
        '''
        获取 switch 的版本 号
        @return:
        '''
        self.sd_test = Sd_Tester(**self.tb_config)
        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== 获取 mcu ver ==========================")
        self.sd_test.update_serverdoipid(0x1001)
        sleep(0.2)
        # 不校验 返回版本号 字符串

        try:
            switch_version = self.sd_test.read_switch_version_or_check()
        except Exception as e:
            logger.info("==================== 获取 switch 版本号异常 ==========================")
            logger.error(e)
            switch_version = None

        try:
            self.sd_test.stop_tester_present()
            sleep(0.5)
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info("==================== SdTester Stopped Error ==========================")
            logger.error(e)

        return switch_version

    def test_bgm_updata(self, standard=True):
        try:
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
            self.ipdu.set_vehspd(0)
            time.sleep(5)
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        except Exception as e:
            logger.info(f"==========设置车速为0失败========== {str(e)} ==========================")


        self.sd_test = Sd_Tester(**self.tb_config)
        self.sd_test.diagnostic_client_sim_start()

        self.sd_test.upgrade_ecu(keyinfo=self.keyinfo, file_url=self.bgm_file_url, standard=standard)

        try:
            self.sd_test.stop_tester_present()
            sleep(0.5)
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info("==================== SdTester Stopped Error ==========================")
            logger.error(e)

        logger.info("Multiple Flash Time Statistics is {}".format(self.sd_test.flash_time_total))

    def test_bgm(self):
        # flash bgm
        # p = BgwNucApp.start_tcpdump(self.network_card_name, self.tcpdumplog)
        self.flash_time_total = {}  # Multiple Flash Time Statistics
        self.network_card_name = "enp0s3.5"

        obd_ip = get_announcement_ip()
        if obd_ip:
            self.tb_config["gateway_ip"] = obd_ip

        self.sd_test = Sd_Tester(**self.tb_config)
        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== SdTester started ==========================")

        try:
            self.sd_test.information_check_f1ae()
        except Exception as e:
            logger.error(e)

        file_path = self.sd_test.download_file(self.bgm_file_url)
        self.uds_flash("BGM", 0x1001, file_path, self.keyinfo)

        try:
            self.sd_test.stop_tester_present()
            sleep(0.5)
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info("==================== SdTester Stopped Error ==========================")
            logger.error(e)

        logger.info("Multiple Flash Time Statistics is {}".format(self.flash_time_total))

    def uds_flash(self, ecu, doipip, bgm_uds_flash_file_path, keyinfo):
        # self.tcpdumplog = "/tmp/tcpdumplog.pcap"

        self.sd_test.update_serverdoipid(doipip)

        sleep(0.1)
        self.sd_test.tester_present()
        sleep(0.5)

        # result = self.sd_test.flash_single_standard_ecu(bgm_uds_flash_file_path, keyinfo, skip_step=[2])

        try:
            result = self.sd_test.flash_single_standard_ecu(bgm_uds_flash_file_path, keyinfo, target_step=2,
                                                            init_step=0)
        except Exception as e:
            logger.info("==================== flash_single_standard_ecu Error ==========================")
            logger.error(e)

        try:
            self.sd_test.stop_tester_present()
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info("==================== SdTester Stopped Error ==========================")
            logger.error(e)

        sleep(10)

        obd_ip = get_announcement_ip()
        if obd_ip:
            self.tb_config["gateway_ip"] = obd_ip

        self.sd_test = Sd_Tester(**self.tb_config)
        self.sd_test.diagnostic_client_sim_start()
        sleep(0.1)
        self.sd_test.tester_present()
        sleep(0.5)
        logger.info("==================== SdTester started ==========================")

        if result:
            # "At BGM's request, wait 20 s from 10 82 to 10 02"
            sleep(10)
            try:
                result = self.sd_test.flash_single_standard_ecu(bgm_uds_flash_file_path, keyinfo, target_step=13,
                                                                init_step=2)
            except Exception as e:
                logger.error(e)

        if not result:
            # wait bgm save log
            sleep(20)
            try:
                self.sd_test.reset_ecu_functional_addressing()
                logger.info("==================== bgm Flash Failed , Restart bgm ==========================")
            except Exception as e:
                logger.error(e)
                logger.warning("==================== BGM Flash Failed , Restart BGM Failed ==========================")

        self.sd_test.stop_tester_present()
        sleep(0.5)
        self.sd_test.diagnostic_client_sim_close()
        logger.info("==================== SdTester stopped ==========================")

        sleep(20)
        # BgwNucApp.stop_tcpdump(p)

        # if result:
        #     global flash_count
        #     flash_count += 1

        global flash_count
        flash_count += 1
        flash_count_name = "flash_count_{}".format(flash_count)
        self.flash_time_total[flash_count_name] = self.sd_test.flash_time_statistics
        logger.info("{} Flash Time statistics[transfer_data_total_int_time,pregramming_dependencies_total_int_time,"
                    "flash_total_int_time] is {}".format(flash_count_name, self.sd_test.flash_time_statistics))

        assert result, "bgm Flash >>>>>>>>>>>>>>>>  Failed"

    # ================================== special flash  ====================================================
    def flash_bgm_special(self):
        # flash bgm special
        # p = BgwNucApp.start_tcpdump(self.network_card_name, self.tcpdumplog)
        self.flash_time_total = {}  # Multiple Flash Time Statistics
        self.network_card_name = "enp0s3.5"

        obd_ip = get_announcement_ip()
        if obd_ip:
            self.tb_config["gateway_ip"] = obd_ip

        self.sd_test = Sd_Tester(**self.tb_config)
        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== SdTester started ==========================")
        try:
            self.sd_test.information_check_f1ae()
        except Exception as e:
            logger.error(e)

        file_path = self.sd_test.download_file(self.bgm_file_url)
        self.uds_flash_special("BGM", 0x1001, file_path, self.keyinfo)

        try:
            self.sd_test.stop_tester_present()
            sleep(0.5)
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info("==================== SdTester Stopped Error ==========================")
            logger.error(e)

        logger.info("Multiple Flash Time Statistics is {}".format(self.flash_time_total))

    def uds_flash_special(self, ecu, doipip, bgm_uds_flash_file_path, keyinfo):
        # For the purpose of improving the success rate of Flash, discard some checks
        # self.tcpdumplog = "/tmp/tcpdumplog.pcap"

        self.sd_test.update_serverdoipid(doipip)

        sleep(0.1)
        self.sd_test.tester_present_special()
        sleep(0.5)

        # result = self.sd_test.flash_single_standard_ecu(bgm_uds_flash_file_path, keyinfo, skip_step=[2])

        try:
            result = self.sd_test.flash_single_ecu_special(bgm_uds_flash_file_path, keyinfo, target_step=2, init_step=0)
        except Exception as e:
            logger.info("==================== flash_single_ecu_special Error ==========================")
            logger.error(e)
            result = False

        try:
            self.sd_test.stop_tester_present()
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info("==================== SdTester Stopped Error ==========================")
            logger.error(e)

        sleep(10)

        obd_ip = get_announcement_ip()
        if obd_ip:
            self.tb_config["gateway_ip"] = obd_ip

        self.sd_test = Sd_Tester(**self.tb_config)
        self.sd_test.diagnostic_client_sim_start()
        sleep(0.1)
        self.sd_test.tester_present_special()
        sleep(0.5)
        logger.info("==================== SdTester started ==========================")
        try:
            self.sd_test.information_check_f1ae()
        except Exception as e:
            logger.error(e)

        if result:
            # "At BGM's request, wait 20 s from 10 82 send"
            sleep(10)
            # For the success rate, wait one more minute
            sleep(60)
            try:
                result = self.sd_test.flash_single_ecu_special(bgm_uds_flash_file_path, keyinfo, target_step=13,
                                                               init_step=2)
            except Exception as e:
                logger.error(e)

        if not result:
            # wait bgm save log
            sleep(20)
            try:
                self.sd_test.reset_ecu_functional_addressing()
                logger.info("==================== bgm Flash Failed , Restart bgm ==========================")
            except Exception as e:
                logger.error(e)
                logger.warning("==================== BGM Flash Failed , Restart BGM Failed ==========================")

        self.sd_test.stop_tester_present()
        sleep(0.5)
        self.sd_test.diagnostic_client_sim_close()
        logger.info("==================== SdTester stopped ==========================")

        sleep(20)
        # BgwNucApp.stop_tcpdump(p)

        # if result:
        #     global flash_count
        #     flash_count += 1

        global flash_count
        flash_count += 1
        flash_count_name = "flash_count_{}".format(flash_count)
        self.flash_time_total[flash_count_name] = self.sd_test.flash_time_statistics
        logger.info("{} Flash Time statistics[transfer_data_total_int_time,pregramming_dependencies_total_int_time,"
                    "flash_total_int_time] is {}".format(flash_count_name, self.sd_test.flash_time_statistics))

        assert result, "bgm Flash >>>>>>>>>>>>>>>>  Failed"
    # ===========================================================================================================


if __name__ == "__main__":
    # work dir : ecu_simuator/
    # cmd: python3 testsdk/test_willow_flash_bgm.py --img_url="https://repo.jidudev.com/artifactory/BGMSoftware/release_build/6160110055BR.bin" --keyinfo="${XAT_CREDENTIAL_SCAN_0AA1445FDDE4807E1F16}" --flash_type="Special"

    from xat_ecu.legacy.common.logger import logger
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--img_url', help='image url',
        default="https://repo.jidudev.com/artifactory/BGMSoftware/release_build/6160110055BR.bin")
    argparser.add_argument(
        '--keyinfo', help='image keyinfo',
        default="${XAT_CREDENTIAL_SCAN_0AA1445FDDE4807E1F16}")
    argparser.add_argument(
        '--flash_type', help='flash type ---- Special, Normal',
        default="Special")
    args = argparser.parse_args()

    bgmflash = TestUdsFlashDoipSimBgm()
    bgmflash.bgm_file_url = args.img_url
    bgmflash.keyinfo = args.keyinfo
    flash_type = args.flash_type
    if flash_type == "Special":
        bgmflash.flash_bgm_special()
    else:
        bgmflash.test_bgm()
    os.system("rm ./*.bin")











