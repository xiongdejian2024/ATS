# -*- coding: utf-8 -*-
"""
@File        : test_willow_flash_tcam.py
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

import pytest
import allure
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from time import sleep
import inspect
from xat_ecu.legacy.common.logger import logger
# from ecu_simulator.interface.tcam.tcam_ssh import TCAM_SSH
from threading import Thread
from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig
from xat_ecu.legacy.sdk.get_obd_ip import get_announcement_ip
from xat_ecu.legacy.sdk.i_signal_i_pdu import *
from xat_ecu.legacy.sdk.bus_app import BusApp
flash_count = 0


# @pytest.mark.flash
# @pytest.mark.diag
class TestUdsFlashDoipSimTcam():
    def __init__(self):
        self.tcam_file_url = "https://repo.jidudev.com/artifactory/TCAMSoftware/Release_build/6110110055BD.bin"
        self.keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_F4C9317FBC2199619B79']
        tb_path = os.path.join(os.path.realpath(__file__).split("ecu_simulator")[0],
                               "ecu_simulator/config/willow_tcam_flash_config.yaml")
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
            # self.tcam_ssh = TCAM_SSH()
            # self.tcam_ssh.clear_coredump(2)
        except Exception as e:
            logger.warning(f"ipdu 初始化失败：{str(e)}")

    def test_tcam_updata(self, standard=True):
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

        self.sd_test.upgrade_ecu(keyinfo=self.keyinfo, file_url=self.tcam_file_url, standard=standard)

        try:
            self.sd_test.stop_tester_present()
            sleep(0.5)
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info("==================== SdTester Stopped Error ==========================")
            logger.error(e)

        logger.info("Multiple Flash Time Statistics is {}".format(self.sd_test.flash_time_total))

    def test_tcam(self):
        # p = BgwNucApp.start_tcpdump(self.network_card_name, self.tcpdumplog)
        self.flash_time_total = {}  # Multiple Flash Time Statistics
        self.network_card_name = "enp0s3.5"

        obd_ip = get_announcement_ip()
        if obd_ip:
            self.tb_config["gateway_ip"] = obd_ip

        self.sd_test = Sd_Tester(**self.tb_config)
        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== SdTester started ==========================")
        self.sd_test.information_check_f1ae()

        file_path = self.sd_test.download_file(self.tcam_file_url)
        self.uds_flash("TCAM", 0x1011, file_path, self.keyinfo)

        try:
            self.sd_test.stop_tester_present()
            sleep(0.5)
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info("==================== SdTester Stopped Error ==========================")
            logger.error(e)

        logger.info("Multiple Flash Time Statistics is {}".format(self.flash_time_total))

    def uds_flash(self, ecu, doipip, tcam_uds_flash_file_path, keyinfo):
        # self.tcpdumplog = "/tmp/tcpdumplog.pcap"

        self.sd_test.update_serverdoipid(doipip)

        sleep(0.1)
        self.sd_test.tester_present()
        sleep(0.5)

        # result = self.sd_test.flash_single_standard_ecu(tcam_uds_flash_file_path, keyinfo, skip_step=[2])

        try:
            result = self.sd_test.flash_single_standard_ecu(tcam_uds_flash_file_path, keyinfo, target_step=2,
                                                            init_step=0)
        except Exception as e:
            logger.info("==================== flash_single_standard_ecu Error ==========================")
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
        self.sd_test.tester_present()
        sleep(0.5)
        logger.info("==================== SdTester started ==========================")
        self.sd_test.information_check_f1ae()

        if result:
            # "At BGM's request, wait 20 s from 10 82 to 10 02"
            sleep(10)
            try:
                result = self.sd_test.flash_single_standard_ecu(tcam_uds_flash_file_path, keyinfo, target_step=13,
                                                                init_step=2)
            except Exception as e:
                logger.error(e)

        if not result:
            # wait bgm save log
            sleep(20)
            try:
                self.sd_test.reset_ecu3()
                logger.info("==================== TCAM Flash Failed , Restart TCAM ==========================")
            except Exception as e:
                logger.error(e)
                logger.warning(
                    "==================== TCAM Flash Failed , Restart TCAM Failed ==========================")

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

        assert result, "TCAM Flash >>>>>>>>>>>>>>>>  Failed"

    # ================================== special flash  ====================================================
    def flash_tcam_special(self):
        # flash tcam special
        # p = BgwNucApp.start_tcpdump(self.network_card_name, self.tcpdumplog)
        self.flash_time_total = {}  # Multiple Flash Time Statistics
        self.network_card_name = "enp0s3.5"

        obd_ip = get_announcement_ip()
        if obd_ip:
            self.tb_config["gateway_ip"] = obd_ip

        self.sd_test = Sd_Tester(**self.tb_config)
        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== SdTester started ==========================")

        file_path = self.sd_test.download_file(self.tcam_file_url)
        self.uds_flash_special("TCAM", 0x1011, file_path, self.keyinfo)

        try:
            self.sd_test.stop_tester_present()
            sleep(0.5)
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info("==================== SdTester Stopped Error ==========================")
            logger.error(e)

        logger.info("Multiple Flash Time Statistics is {}".format(self.flash_time_total))

    def uds_flash_special(self, ecu, doipip, tcam_uds_flash_file_path, keyinfo):
        # self.tcpdumplog = "/tmp/tcpdumplog.pcap"

        self.sd_test.update_serverdoipid(doipip)

        sleep(0.1)
        self.sd_test.tester_present_special()
        sleep(0.5)

        # result = self.sd_test.flash_single_standard_ecu(tcam_uds_flash_file_path, keyinfo, skip_step=[2])

        try:
            result = self.sd_test.flash_single_ecu_special(tcam_uds_flash_file_path, keyinfo, target_step=2,
                                                           init_step=0)
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

        if result:
            # "At BGM's request, wait 20 s from 10 82 to 10 02"
            sleep(10)
            try:
                result = self.sd_test.flash_single_ecu_special(tcam_uds_flash_file_path, keyinfo, target_step=13,
                                                               init_step=2)
            except Exception as e:
                logger.error(e)

        if not result:
            # wait bgm save log
            sleep(20)
            try:
                self.sd_test.reset_ecu3()
                logger.info("==================== TCAM Flash Failed , Restart TCAM ==========================")
            except Exception as e:
                logger.error(e)
                logger.warning(
                    "==================== TCAM Flash Failed , Restart TCAM Failed ==========================")

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

        assert result, "TCAM Flash >>>>>>>>>>>>>>>>  Failed"
        # ===========================================================================================================


if __name__ == "__main__":
    # work dir : ecu_simuator/
    # cmd: python3 testsdk/test_willow_flash_tcam.py --img_url="https://repo.jidudev.com/artifactory/TCAMSoftware/Release_build/v0.5.5/2022082921/6110110055BH.bin" --keyinfo="${XAT_CREDENTIAL_SCAN_2D47DC0D16C56010BF0B}" --flash_type="Special"

    from xat_ecu.legacy.common.logger import logger
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--img_url', help='image url',
        default="https://repo.jidudev.com/artifactory/TCAMSoftware/Release_build/v0.5.5/2022082921/6110110055BH.bin")
    argparser.add_argument(
        '--keyinfo', help='image keyinfo',
        default="${XAT_CREDENTIAL_SCAN_2D47DC0D16C56010BF0B}")
    argparser.add_argument(
        '--flash_type', help='flash type ---- Special, Normal',
        default="Special")
    args = argparser.parse_args()

    tcamflash = TestUdsFlashDoipSimTcam()
    tcamflash.tcam_file_url = args.img_url
    tcamflash.keyinfo = args.keyinfo
    flash_type = args.flash_type
    if flash_type == "Special":
        tcamflash.flash_tcam_special()
    else:
        tcamflash.test_tcam()
    os.system("rm ./*.bin")











