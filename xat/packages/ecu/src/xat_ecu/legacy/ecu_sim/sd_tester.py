# -*- coding: utf-8 -*-
"""
@File        : sd_tester.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021/11/08 4:16 PM
@Description : description about this file
@Examples    : example of how to use it
"""

import os
import sys
import time
from time import sleep
import base64
import xlrd
import json
import re


from xat_ecu.legacy.sdk.diagnostic_odx_client_simulator_app import (
    Diagnostic_Odx_Client_Sim_App,
)
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.ecu_sim.parse_tn_config import ParseTNConfig
from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig
from xat_ecu.legacy.sdk.ecu_sim_const import ECUSimConst
from xat_ecu.legacy.config.path import CONFIG_DIR_PATH
from xat_ecu.legacy.sdk.get_obd_ip import get_announcement_ip
from xat_ecu.legacy.common.data_type_handing import *
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.common.parse_vbf import get_vbf_payload, get_vbf_sw_signature, get_block_info, get_vbf_erase_info, get_vbf_call
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH

# from ecu_simulator.tools.ccp.generate_json_from_excel import Generate_Json_From_Excel

flash_count = 0


class Sd_Tester(Diagnostic_Odx_Client_Sim_App):
    def __init__(self, **cfg):
        """
        :param cfg: dict

        cfg = {
            dut_ecu: ["BGM"]
            gateway_ip: "169.254.1.1"
            bus:{
                  eth_obd: "enx000ec64a8e4c"
                  eth_vlan5: "eth0.5"
                  eth_vlan9: "eth0.9"
                  bodycan: 'can0'
                }，
            sd_tester_cfg:{
                    diag_mode: "doip"
                    is_via_gateway: True
                    ecu_name: "BGM"
                    dig_bus: "bodycan"
                    server_ip:
                    }，
            veh_type: 'mars1'
            bl_ver: 'v_1_0_0'

            }
        """
        tb_default_path = str(CONFIG_DIR_PATH.joinpath("default_config.yaml"))
        tb_default_config = ParseTBConfig(tb_default_path)
        self.sniff_packet = None

        if cfg:
            self.cfg = cfg
        else:
            self.cfg = tb_default_config.get_yaml()
        try:
            obdip = get_announcement_ip()
            if obdip:
                self.cfg["gateway_ip"] = obdip
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
            logger.warning("当前台架获取公告IP异常：" + e.__repr__())

        gateway_ip = self.cfg.get("gateway_ip")
        bus_channel = self.cfg.get("bus")
        sd_tester_config = self.cfg.get("sd_tester_cfg")
        dig_bus = self.cfg.get("dig_bus")
        sec_con = self.cfg.get("sec_con")

        self.diag_mode = sd_tester_config.get("diag_mode")
        self.is_via_gateway = sd_tester_config.get("is_via_gateway")
        gatway_ecu = ECUSimConst.GATEWAY_ECU
        self.ecu_name = sd_tester_config.get("ecu_name")
        server_ip = sd_tester_config.get("server_ip")

        self.veh_type = self.cfg.get("veh_type")
        self.bl_ver = self.cfg.get("bl_ver")
        if self.veh_type and self.bl_ver:
            # self.cls_path = "sdk/data/{}/can_lin_fr_cls/{}".format(self.veh_type, self.bl_ver)
            tn_config_path = "config/{}/{}/ecu_network.yaml".format(
                self.veh_type, self.bl_ver
            )
        else:
            logger.error(
                "Config error : self.veh_type is {}  self.bl_ver is {}".format(
                    self.veh_type, self.bl_ver
                )
            )
        tn_config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))), tn_config_path
        )
        self.tn_config = ParseTNConfig(tn_config_path)

        self.ccp_json_path = "../sdk/data/{}/ccp/{}/ccp.json".format(self.veh_type, self.bl_ver)
        self.ccp_json_path = os.path.join(CONFIG_DIR_PATH, self.ccp_json_path)

        self.ccp_xlsx_path = "../sdk/data/{}/ccp/{}/ccp.xlsx".format(self.veh_type, self.bl_ver)
        self.ccp_xlsx_path = os.path.join(CONFIG_DIR_PATH, self.ccp_xlsx_path)

        self.can_req_id = self.tn_config.get_can_req_id(self.ecu_name)
        if server_ip:
            self.server_ip = server_ip
        else:
            self.server_ip = self.tn_config.get_eth_dig_ip(self.ecu_name)
        self.server_doip_id = self.tn_config.get_ecu_doip(self.ecu_name)
        gw_can = self.tn_config.get_gw_can()
        self.channel = bus_channel.get(dig_bus)
        self.flash_result = None
        self.pregramming_dependencies_start = 0
        self.pregramming_dependencies_end = 0
        self.tcam_redundancy_time = 0
        logger.info(self.is_via_gateway)
        if self.is_via_gateway:
            if self.diag_mode == "doip":
                self.server_ip = gateway_ip
                logger.info("it is doip and via_gateway")
            elif self.diag_mode == "docan":
                self.channel = bus_channel.get(gw_can)
        else:
            if self.diag_mode == "doip":
                logger.info("it is doip and no via_gateway")
        logger.info("Sd_Tester server_ip is {}".format(self.server_ip))
        logger.info("Sd_Tester server_doip_id is {}".format(self.server_doip_id))
        super().__init__(
            self.ecu_name,
            self.diag_mode,
            self.server_ip,
            self.server_doip_id,
            self.can_req_id,
            self.channel,
            sec_con=sec_con,
        )

    def all_ecu_is_active(self):
        '''
        请求对象是网关
        '''

        # init all ecu active dict
        all_ecu_is_active_dict = {}
        for ecu in self.tn_config.all_ecu_list:
            all_ecu_is_active_dict[ecu] = {"active": None}

        self.update_serverdoipid(0x1fff)
        self.diagnostic_session_check_functional_addressing_not_wait()

        recv_sa_id_list = self.get_recv_sa_id_list()

        if recv_sa_id_list:
            for sa_id in recv_sa_id_list:
                logger.info(sa_id)
                ecu = self.tn_config.get_ecu_from_doip_id(sa_id)
                if ecu:
                    all_ecu_is_active_dict[ecu] = {"active": True}
        else:
            logger.warning("未收到任何doip回复")

        return all_ecu_is_active_dict

    def download_file_fixed_updatebin(self, file_url):
        username = base64.b64decode(ECUSimConst.SOA_PUBLIC.encode()).decode()
        password = base64.b64decode(ECUSimConst.SOA_PUBLIC_PD.encode()).decode()
        download_cmd = "curl -o update.bin -u {0}:{1} {2}".format(
            username, password, file_url
        )
        os.system(download_cmd)
        file_path = "./update.bin"
        return file_path

    def download_file(self, file_url):
        '''
        根据路径下载升级所需的  文件
        @param file_url: 升级的bin 文件路径 如 "https://repo.jidudev.com/artifactory/TCAMSoftware/Release_build/6110110055BD.bin"
        @return:
        '''
        username = base64.b64decode(ECUSimConst.SOA_PUBLIC.encode()).decode()
        password = base64.b64decode(ECUSimConst.SOA_PUBLIC_PD.encode()).decode()
        file_name = file_url.split("/")[-1]
        file_path = "./{}".format(file_name)
        if os.path.isfile(file_path):
            logger.info("Path: {} is exit, need not to download".format(file_path))
        else:
            download_cmd = "curl -O -u {0}:{1} {2}".format(username, password, file_url)
            os.system(download_cmd)
        return file_path

    def download_and_check_bin_file(self, file_url, offline=False, **kwargs):
        '''
        下载 bin 文件 并 校验下载的文件是否完整
        @param file_url:
        @param offline:是否需要下载文件，离线状态就不需要下载，但是仍需要 传递
        @return:
        '''
        # 如果下载的bin 文件不对，则尝试下载的次数，默认3次
        repeat = kwargs.get("repeat", 3)
        username = base64.b64decode(ECUSimConst.SOA_PUBLIC.encode()).decode()
        password = base64.b64decode(ECUSimConst.SOA_PUBLIC_PD.encode()).decode()
        cmd = f"curl -u {username}:{password} {file_url}.sha256"
        web_sha256 = os.popen(cmd).read()
        logger.info(f"JFrog上的{file_url}的bin文件的sha256值是{web_sha256}")

        for _ in range(repeat):
            file_path = self.download_file(file_url)
            if offline:
                # 如果是离线状态 则直接返回地址，需要把下载好的 bin文件放进响应的路径
                return file_path
            sha256_value = get_sha256(file_path)
            # 如果一致，则跳出循环
            if sha256_value == web_sha256:
                return file_path
            logger.warning(f"下载的文件残缺sha256_value={sha256_value}")
            # 删除 残缺文件,否则不会重新下载
            os.system("rm ./*.bin")
            os.system("rm ./*.keyinfo")
            time.sleep(5)

        return None

    def flash_single_standard_ecu(
            self,
            file_path,
            key_info,
            target_step=14,
            init_step=0,
            skip_step=[0],
            check_data=None,
            compression_encryption_method=0x00,
            offline_flashing=False,
            read_timeout=None,
            restart_wait_time=None):
        '''
        标准的升级流程，默认会执行 0 到 14 步
        @param keyinfo:  如 "HacdLlcI1suuaQgb5NYeXSVob7bCxVO8mEN6poxblq76bim0VunQUHvpvkdJzGysy4jUso7AR7L07jEd3cadbyiWPeyoVqdSTVuln3xZyUZxcFvd0ewc2/u1GZKrRwWPF4deM0l+b18lL2zcbmdnO2KX+OqIf4loBaOhQ8OGiOV+DoIYsjXUC/zghbO+Fpz9rkxMH1T7+m33mZo0EwY7uYnmc5CPmIQg2wC/fmnFS91mdqn7pjcwsTKqjKR2eDkTApanNZmwD6HlYlYQDfQEIzBS8sZ/e2e27WRHXLNCynF3lgVzdWmvZZx9yHLLfMx+bBsU4MUTyfcIfselexCLZg=="
        @param file_url: 升级的bin 文件路径 如 "https://repo.jidudev.com/artifactory/TCAMSoftware/Release_build/6110110055BD.bin"
        @param target_step: 结束步骤 （最大为 14）
        @param init_step: 开始步骤  （最小为 0）
        @param skip_step: 要跳过的步骤， 为列表格式
        @param check_data: 版本 字符串类型  如 6160110110AAC 或者6110110055 BD
        @return:
        '''
        self.flash_result = True
        step = init_step
        sub_step = 1
        self.transfer_data_total_int_time = 0
        self.pregramming_dependencies_total_int_time = 0
        self.flash_total_int_time = 0
        self.flash_start = time.time()
        # Start Flash... Active ECU
        logger.info("====== Start Flash... Active ECU ======")
        while self.flash_result and (step != target_step):
            step += 1
            if step in skip_step:
                logger.info("Skip the step {}".format(step))
            else:
                # =====================================   Enter Program Mode  =========================================
                if step == 1:
                    # Step 1  Check Program Pre-condition
                    self.check_program_pre_condition_functional_addressing()
                    sleep(1.5)
                    # self.flash_result = self.check_and_print_response_result("Step 1  Check Program Pre-condition")

                elif step == 2:
                    self.stop_tester_present()
                    # Step 2  Enter Program Mode
                    self.enter_program_session_functional_addressing()
                    # self.flash_result = self.check_and_print_response_result("Step 2  Enter Program Mode")

                elif step == 3:
                    # Step 3  Confirm Program Mode
                    if offline_flashing:
                        sleep(5)    # 离线刷写新需求： 1082之后由立即发送1002变更为等待5s之后再发送1002
                    self.enter_programming_session()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 3  Confirm Program Mode"
                    )

                elif step == 4:
                    # Step 4  Diagnostic Session Check
                    self.diagnostic_session_check()
                    if offline_flashing:
                        # 离线刷写台新需求：进入boot后，22F186返回1后由工具立刻返回错误终于刷写流程变更为工具等待1s重试发1002进boot
                        result_data = self.return_udsdata_and_check_and_print_response_result(
                            "Step 4  Diagnostic Session Check"
                        )
                        if result_data == [0x62, 0xF1, 0x86, 0x01]:
                            sleep(1)
                            self.diagnostic_session_check()
                            self.flash_result = self.check_and_print_response_result(
                            "Step 4  Diagnostic Session Check"
                            )
                        elif result_data == [0x62, 0xF1, 0x86, 0x02]:
                            self.flash_result=True
                        else:
                            self.flash_result=False
                    else:
                        self.flash_result = self.check_and_print_response_result(
                            "Step 4  Diagnostic Session Check"
                        )

                elif step == 5 and sub_step == 1:
                    # Note: 在step5 information check, 诊断仪可能会使用读取DID F1AA/F1AB/F18C 代替读取DID ED20，而获取版本信息
                    # Step 5  Information Check
                    self.information_check_ed20()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 5  Information Check ED20"
                    )
                    sub_step += 1
                    step -= 1

                elif step == 5 and sub_step == 2:
                    # Step 5  Information Check
                    self.information_check_f1aa()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 5  Information Check F1AA"
                    )
                    sub_step += 1
                    step -= 1

                elif step == 5 and sub_step == 3:
                    # Step 5  Information Check
                    self.information_check_f1ab()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 5  Information Check F1AB"
                    )
                    sub_step += 1
                    step -= 1

                elif step == 5 and sub_step == 4:
                    # Step 5  Information Check
                    self.information_check_f18c()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 5  Information Check F18C"
                    )

                # =====================================   Pre-programming Sequence  =====================================
                elif step == 6:
                    # Step 6  Public Key Status Check
                    self.public_key_status_check()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 6  Public Key Status Check"
                    )
                    # force to pass
                    self.flash_result = True
                    step -= 0.5

                elif step == 6.5:
                    # float There may be a problem  !!!
                    # Step 6.5 Unlock For Download
                    self.security_access_level_l1()
                    self.flash_result = self.assert_security_access("L1")
                    step -= 0.5
                    step = int(step)

                # =====================================   Download data file(s)  =====================================
                elif step == 7:
                    # Step 7  RoutineControl-Erase Memory
                    self.erase_memory(file_path)
                    self.flash_result = self.check_and_print_response_result(
                        "Step 7  RoutineControl-Erase Memory"
                    )

                elif step == 8:
                    # Step 8  Request Download
                    # compression method and encryption method
                    self.request_download(
                        file_path, compression_encryption_method=[compression_encryption_method]
                    )
                    self.flash_result = self.check_and_print_response_result(
                        "Step 8  Request Download"
                    )

                elif step == 9:
                    # Step 9  Transfer Data
                    self.transfer_data_start = time.time()

                    self.transfer_data(file_path)
                    self.flash_result = self.check_and_print_response_result(
                        "Step 9  Transfer Data"
                    )

                    self.transfer_data_end = time.time()
                    self.transfer_data_total_time = (
                            self.transfer_data_end - self.transfer_data_start
                    )
                    self.transfer_data_total_int_time = int(
                        self.transfer_data_total_time
                    )
                    self.transfer_data_total_time_minute = (
                            self.transfer_data_total_int_time // 60
                    )
                    self.transfer_data_total_time_second = (
                            self.transfer_data_total_int_time % 60
                    )
                    logger.info(
                        "self.transfer_data_total_time is {} minutes  {} seconds".format(
                            self.transfer_data_total_time_minute,
                            self.transfer_data_total_time_second,
                        )
                    )

                elif step == 10:
                    # Step 10  Request Transfer Exit
                    self.request_transfer_exit()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 10  Request Transfer Exit"
                    )
                    logger.info(
                        " ===========================   UDS Transfer Date Complete   ==========================="
                    )

                elif step == 11:
                    # Step 11  Transfer Key Info
                    # key_info = "${XAT_CREDENTIAL_SCAN_883E080423C846F09463} HEMEq1LBLl1UXmmnEX6Eyk1SgRMPaK1xKPpq94/jqs X/DbSkaypQZkn3rPBi TISliJ3FeJYB /q0FAaC5cNTycRcD0PQrH/F02DFYpxwkwtWMGPfnkIwAgQDitdfQ7g=="
                    # key_info = "${XAT_CREDENTIAL_SCAN_3730811E08AC4BE3A2ED}"
                    # TCAM gongcheng AG key_info = "ZZis1PH6rsAc5FV8qaoKUDw4lzLE2SXHSMsIJ2cARyuWAtKmJADJYqE4g4LzX01VE0fUvfvHnVm0HDO0pmMXKrtGjvIbQuP6TNIuxt7xrOodk8Cwn5q+WSFmMd2pf6i1N0YPznbo+7Niw4AhJznwbKMQDaYl4Eeia5K7mjZ2MWl9E33VjXLh/NfYNu4vLQzCyMvkV91YNh4WmHR+tIdmJ3iRKxkQMtpkKZKYGAu3FfjnZXYHqvQHcmzFPUFFIVWkVZsh8DwjL7WZi/LskSTQZNSgZF++wfb43hOSteKrCgCZVNCJyhTOp3rT21TtXJ5bRewFBiBksPm3Fb+mfAEp3Q=="
                    key_info = key_info.encode("utf-8")
                    key_info = list(key_info)
                    self.transfer_key_info(key_info)
                    self.flash_result = self.check_and_print_response_result(
                        "Step 11  Transfer Key Info"
                    )

                # =====================================   Post-programming =========================================
                elif step == 12:
                    # Step 12  Verify Software Integrity
                    self.pregramming_dependencies_start = time.time()
                    self.verify_software_integrity()
                    result = self.return_udsdata_and_check_and_print_response_result(
                        "Step 12  Verify Software Integrity"
                    )
                    self.flash_result = result == [
                        0x71,
                        0x01,
                        0x02,
                        0x05,
                        0x10,
                        0x00,
                        0x00,
                        0x00,
                        0x00,
                    ]
                    if self.flash_result:
                        logger.info(
                            "====================   Step 12  ecu self Flash success  =========================="
                        )
                    else:
                        logger.info(
                            "====================   Step 12  ecu self Flash Failed  =========================="
                        )

                    self.pregramming_dependencies_end = time.time()
                    self.pregramming_dependencies_total_time = (
                            self.pregramming_dependencies_end
                            - self.pregramming_dependencies_start
                    )
                    self.pregramming_dependencies_total_int_time = int(
                        self.pregramming_dependencies_total_time
                    )
                    self.pregramming_dependencies_total_time_minute = (
                            self.pregramming_dependencies_total_int_time // 60
                    )
                    self.pregramming_dependencies_total_time_second = (
                            self.pregramming_dependencies_total_int_time % 60
                    )
                    logger.info(
                        "self.pregramming_dependencies_total_time is {} minutes  {} seconds".format(
                            self.pregramming_dependencies_total_time_minute,
                            self.pregramming_dependencies_total_time_second,
                        )
                    )

                elif step == 13:
                    if self.sniff_packet:
                        #重启之前停止抓包
                        BGM_SSH().stop_bgm_tcpdump()
                        logger.info('stop sniff packet eth0')
                        
                    self.stop_tester_present()
                    # Step 13  ECU Reset
                    self.reset_ecu_functional_addressing()
                    rs_start_time = time.time()
                    if self.cfg.get("dut_ecu") == ["TCAM"]:
                        self.flash_result = self.check_and_print_response_result(
                            "Step 13  ECU Reset")
                    rs_end_time = time.time()
                    self.tcam_redundancy_time = rs_end_time - rs_start_time
                    if self.flash_result is False:
                        raise AssertionError(f"诊断回复负响应。")

                    self.flash_end = time.time()
                    self.flash_total_time = self.flash_end - self.flash_start
                    self.flash_total_int_time = int(self.flash_total_time)
                    self.flash_total_time_minute = self.flash_total_int_time // 60
                    self.flash_total_time_second = self.flash_total_int_time % 60
                    logger.info(
                        "flash_total_time is {} minutes  {} seconds".format(
                            self.flash_total_time_minute, self.flash_total_time_second
                        )
                    )
                elif step == 14:
                    logger.info(
                        f" ===========================  step 14 校验版本号 ==========================="
                    )
                    # Step 14  校验 升级后的版本
                    # sleep(15)
                    # 读取版本号
                    self.flash_result, version = self.__get_flash_done_version(
                        check_data=check_data, file_path=file_path, read_timeout=read_timeout, restart_wait_time=restart_wait_time
                    )
                    if check_data is None:
                        logger.info(
                            f" =================Doip Flash Done  Current Version  {version} ================="
                        )
                    sleep(1)
                    logger.info(
                        " ===========================   Doip Flash Complete   ==========================="
                    )

        if step != target_step:
            logger.info(
                "=======================   Flash Failed    ========================================"
            )
            # self.reset_ecu_functional_addressing()
            # self.enter_default_session_functional_addressing()
            # self.enter_extended_session_functional_addressing()
            # self.enable_normal_communication_functional_addressing()
            # self.start_setting_of_dtc_functional_addressing()
            # self.enter_default_session_functional_addressing()

        self.flash_time_statistics = [
            self.transfer_data_total_int_time,
            self.pregramming_dependencies_total_int_time,
            self.flash_total_int_time,
        ]

        return self.flash_result

    def flash_single_ecu_special(
            self,
            file_path,
            key_info,
            target_step=14,
            init_step=0,
            skip_step=[0],
            check_data=None,
            read_timeout=None,
            restart_wait_time=None
    ):
        '''
        specl 升级流程，共14步，会跳过第五步
        @param keyinfo:  如 "HacdLlcI1suuaQgb5NYeXSVob7bCxVO8mEN6poxblq76bim0VunQUHvpvkdJzGysy4jUso7AR7L07jEd3cadbyiWPeyoVqdSTVuln3xZyUZxcFvd0ewc2/u1GZKrRwWPF4deM0l+b18lL2zcbmdnO2KX+OqIf4loBaOhQ8OGiOV+DoIYsjXUC/zghbO+Fpz9rkxMH1T7+m33mZo0EwY7uYnmc5CPmIQg2wC/fmnFS91mdqn7pjcwsTKqjKR2eDkTApanNZmwD6HlYlYQDfQEIzBS8sZ/e2e27WRHXLNCynF3lgVzdWmvZZx9yHLLfMx+bBsU4MUTyfcIfselexCLZg=="
        @param file_url: 升级的bin 文件路径 如 "https://repo.jidudev.com/artifactory/TCAMSoftware/Release_build/6110110055BD.bin"
        @param target_step: 结束步骤 （最大为 14）
        @param init_step: 开始步骤  （最小为 0）
        @param skip_step: 要跳过的步骤， 为列表格式
        @param check_data: 版本 字符串类型  如 6160110110AAC 或者6110110055 BD
        @return:
        '''

        # For the purpose of improving the success rate of Flash, discard some checks
        self.flash_result = True
        step = init_step
        sub_step = 1
        self.transfer_data_total_int_time = 0
        self.pregramming_dependencies_total_int_time = 0
        self.flash_total_int_time = 0
        self.flash_start = time.time()
        # Start Flash... Active ECU
        logger.info("====== Start Flash ---- Special        ... Active ECU ======")
        while self.flash_result and (step != target_step):
            step += 1
            if step in skip_step:
                logger.info("Skip the step {}".format(step))
            else:
                # =====================================   Enter Program Mode  =========================================
                if step == 1:
                    # Step 1  Check Program Pre-condition
                    self.check_program_pre_condition_functional_addressing()
                    sleep(1.5)
                    # self.flash_result = self.check_and_print_response_result("Step 1  Check Program Pre-condition")

                elif step == 2:
                    # Step 2  Enter Program Mode
                    self.stop_tester_present()
                    self.enter_program_session_functional_addressing()
                    sleep(1)
                    # self.flash_result = self.check_and_print_response_result("Step 2  Enter Program Mode")

                elif step == 3:
                    # Step 3  Confirm Program Mode
                    self.enter_programming_session()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 3  Confirm Program Mode"
                    )
                    sleep(1)

                elif step == 4:
                    # Step 4  Diagnostic Session Check
                    self.diagnostic_session_check()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 4  Diagnostic Session Check"
                    )
                    sleep(1)

                elif step == 5 and sub_step == 1:
                    # Note: 在step5 information check, 诊断仪可能会使用读取DID F1AA/F1AB/F18C 代替读取DID ED20，而获取版本信息
                    # Step 5  Information Check
                    # self.information_check_ed20()
                    # self.flash_result = self.check_and_print_response_result("Step 5  Information Check ED20")
                    sub_step += 1
                    step -= 1

                elif step == 5 and sub_step == 2:
                    # Step 5  Information Check
                    # self.information_check_f1aa()
                    # self.flash_result = self.check_and_print_response_result("Step 5  Information Check F1AA")
                    sub_step += 1
                    step -= 1

                elif step == 5 and sub_step == 3:
                    # Step 5  Information Check
                    # self.information_check_f1ab()
                    # self.flash_result = self.check_and_print_response_result("Step 5  Information Check F1AB")
                    sub_step += 1
                    step -= 1

                elif step == 5 and sub_step == 4:
                    # Step 5  Information Check
                    # self.information_check_f18c()
                    # self.flash_result = self.check_and_print_response_result("Step 5  Information Check F18C")
                    pass

                # =====================================   Pre-programming Sequence  =====================================
                elif step == 6:
                    # Step 6  Public Key Status Check
                    self.public_key_status_check()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 6  Public Key Status Check"
                    )
                    # force to pass
                    self.flash_result = True
                    step -= 0.5

                elif step == 6.5:
                    # float There may be a problem  !!!
                    # Step 6.5 Unlock For Download
                    self.security_access_level_l1()
                    self.flash_result = self.assert_security_access("L1")
                    step -= 0.5
                    step = int(step)
                    sleep(1)

                # =====================================   Download data file(s)  =====================================
                elif step == 7:
                    # Step 7  RoutineControl-Erase Memory
                    sleep(1)
                    self.erase_memory(file_path)
                    self.flash_result = self.check_and_print_response_result(
                        "Step 7  RoutineControl-Erase Memory"
                    )
                    sleep(1)

                elif step == 8:
                    # Step 8  Request Download
                    # compression method and encryption method
                    self.request_download(
                        file_path, compression_encryption_method=[0x00]
                    )
                    self.flash_result = self.check_and_print_response_result(
                        "Step 8  Request Download"
                    )
                    sleep(1)

                elif step == 9:
                    # Step 9  Transfer Data
                    self.transfer_data_start = time.time()

                    self.transfer_data_special(file_path)
                    self.flash_result = self.check_and_print_response_result(
                        "Step 9  Transfer Data special"
                    )

                    self.transfer_data_end = time.time()
                    self.transfer_data_total_time = (
                            self.transfer_data_end - self.transfer_data_start
                    )
                    self.transfer_data_total_int_time = int(
                        self.transfer_data_total_time
                    )
                    self.transfer_data_total_time_minute = (
                            self.transfer_data_total_int_time // 60
                    )
                    self.transfer_data_total_time_second = (
                            self.transfer_data_total_int_time % 60
                    )
                    logger.info(
                        "self.transfer_data_total_time is {} minutes  {} seconds".format(
                            self.transfer_data_total_time_minute,
                            self.transfer_data_total_time_second,
                        )
                    )

                    sleep(1)

                elif step == 10:
                    # Step 10  Request Transfer Exit
                    self.request_transfer_exit()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 10  Request Transfer Exit"
                    )
                    logger.info(
                        " ===========================   UDS Transfer Date Complete   ==========================="
                    )
                    sleep(1)

                elif step == 11:
                    # Step 11  Transfer Key Info
                    key_info = key_info.encode("utf-8")
                    key_info = list(key_info)
                    self.transfer_key_info(key_info)
                    self.flash_result = self.check_and_print_response_result(
                        "Step 11  Transfer Key Info"
                    )
                    sleep(1)

                # =====================================   Post-programming =========================================
                elif step == 12:
                    # Step 12  Verify Software Integrity
                    self.pregramming_dependencies_start = time.time()
                    self.verify_software_integrity()
                    result = self.return_udsdata_and_check_and_print_response_result(
                        "Step 12  Verify Software Integrity"
                    )
                    self.flash_result = result == [
                        0x71,
                        0x01,
                        0x02,
                        0x05,
                        0x10,
                        0x00,
                        0x00,
                        0x00,
                        0x00,
                    ]
                    if self.flash_result:
                        logger.info(
                            "====================   Step 12  ecu self Flash success  =========================="
                        )
                    else:
                        logger.info(
                            "====================   Step 12  ecu self Flash Failed  =========================="
                        )

                    self.pregramming_dependencies_end = time.time()
                    self.pregramming_dependencies_total_time = (
                            self.pregramming_dependencies_end
                            - self.pregramming_dependencies_start
                    )
                    self.pregramming_dependencies_total_int_time = int(
                        self.pregramming_dependencies_total_time
                    )
                    self.pregramming_dependencies_total_time_minute = (
                            self.pregramming_dependencies_total_int_time // 60
                    )
                    self.pregramming_dependencies_total_time_second = (
                            self.pregramming_dependencies_total_int_time % 60
                    )
                    logger.info(
                        "self.pregramming_dependencies_total_time is {} minutes  {} seconds".format(
                            self.pregramming_dependencies_total_time_minute,
                            self.pregramming_dependencies_total_time_second,
                        )
                    )
                    sleep(1)

                elif step == 13:
                    self.stop_tester_present()
                    # Step 13  ECU Reset
                    self.reset_ecu_functional_addressing()
                    # self.flash_result = self.check_and_print_response_result(
                    #     "Step 13  ECU Reset")

                    self.flash_end = time.time()
                    self.flash_total_time = self.flash_end - self.flash_start
                    self.flash_total_int_time = int(self.flash_total_time)
                    self.flash_total_time_minute = self.flash_total_int_time // 60
                    self.flash_total_time_second = self.flash_total_int_time % 60
                    logger.info(
                        "flash_total_time is {} minutes  {} seconds".format(
                            self.flash_total_time_minute, self.flash_total_time_second
                        )
                    )
                elif step == 14:
                    logger.info(
                        f" ===========================  step 14 校验版本号 ==========================="
                    )
                    # Step 14  校验 升级后的版本
                    # sleep(15)
                    # 读取版本号
                    self.flash_result, version = self.__get_flash_done_version(
                        check_data=check_data, file_path=file_path, read_timeout=read_timeout, restart_wait_time=restart_wait_time
                    )
                    if check_data is None:
                        logger.info(
                            f" =================Doip Flash Done  Current   Version  {version} ================="
                        )
                    sleep(1)
                    logger.info(
                        " ===========================   Doip Flash Complete   ==========================="
                    )

        if step != target_step:
            logger.info(
                "=======================   Flash Failed    ========================================"
            )
            # self.reset_ecu_functional_addressing()
            # self.enter_default_session_functional_addressing()
            # self.enter_extended_session_functional_addressing()
            # self.enable_normal_communication_functional_addressing()
            # self.start_setting_of_dtc_functional_addressing()
            # self.enter_default_session_functional_addressing()

        self.flash_time_statistics = [
            self.transfer_data_total_int_time,
            self.pregramming_dependencies_total_int_time,
            self.flash_total_int_time,
        ]

        return self.flash_result
    
    def flash_single_standard_ecu_vbf(
            self,
            sbl_file_path,
            app_file_path: list,
            target_step=25,
            init_step=0,
            skip_step=[0],
            check_data=None,
            compression_encryption_method=0x00,
            offline_flashing=False
    ):
        '''
        标准的升级流程，默认会执行 0 到 14 步
        @param keyinfo:  如 "HacdLlcI1suuaQgb5NYeXSVob7bCxVO8mEN6poxblq76bim0VunQUHvpvkdJzGysy4jUso7AR7L07jEd3cadbyiWPeyoVqdSTVuln3xZyUZxcFvd0ewc2/u1GZKrRwWPF4deM0l+b18lL2zcbmdnO2KX+OqIf4loBaOhQ8OGiOV+DoIYsjXUC/zghbO+Fpz9rkxMH1T7+m33mZo0EwY7uYnmc5CPmIQg2wC/fmnFS91mdqn7pjcwsTKqjKR2eDkTApanNZmwD6HlYlYQDfQEIzBS8sZ/e2e27WRHXLNCynF3lgVzdWmvZZx9yHLLfMx+bBsU4MUTyfcIfselexCLZg=="
        @param sbl_file_path: 升级的bin 文件路径 如 "/root/quansun_new3/aicomate/PTZ_sbl.VBF"
        @param app_file_path: 升级的bin 文件路径 如 ["/root/quansun_new3/aicomate/PTZ_Upd.VBF"]
        @param target_step: 结束步骤 （最大为 25）
        @param init_step: 开始步骤  （最小为 0）
        @param skip_step: 要跳过的步骤， 为列表格式
        @param check_data: 版本 字符串类型  如 6160110110AAC 或者6110110055 BD
        @return:
        '''
        self.flash_result = True
        step = init_step
        sub_step = 1
        self.transfer_data_total_int_time = 0
        self.pregramming_dependencies_total_int_time = 0
        self.flash_total_int_time = 0
        self.flash_start = time.time()
        # Start Flash... Active ECU
        logger.info("====== Start Flash... Active ECU ======")
        while self.flash_result and (step != target_step):
            step += 1
            if step in skip_step:
                logger.info("Skip the step {}".format(step))
            else:
                # =====================================   Enter Program Mode  =========================================
                if step == 1:
                    # Step 1  Check Program Pre-condition
                    self.check_program_pre_condition_functional_addressing()
                    sleep(1.5)
                    # self.flash_result = self.check_and_print_response_result("Step 1  Check Program Pre-condition")
                elif step == 2:
                    # Step 2  enter extended session
                    self.enter_extended_session_functional_addressing()
                    sleep(0.5)
                    # self.flash_result = self.check_and_print_response_result("Step 2  enter extended session")

                elif step == 3:
                    # Step 3  
                    self.stop_setting_of_dtc_functional_addressing_vbf()
                    sleep(0.5)

                elif step == 4: 
                    self.disable_normal_communication_functional_addressing()
                    sleep(0.5)

                elif step == 5:
                    # Step 5  Enter Program Mode
                    self.stop_tester_present()
                    self.enter_programming_session()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 5  Confirm Program Mode"
                    )

                # =====================================   Pre-programming Sequence  =====================================
                elif step == 6:
                    # Step 6  Diagnostic Session Check
                    self.diagnostic_session_check()
                    if offline_flashing:
                        # 离线刷写台新需求：进入boot后，22F186返回1后由工具立刻返回错误终于刷写流程变更为工具等待1s重试发1002进boot
                        result_data = self.return_udsdata_and_check_and_print_response_result(
                            "Step 4  Diagnostic Session Check"
                        )
                        if result_data == [0x62, 0xF1, 0x86, 0x01]:
                            sleep(1)
                            self.diagnostic_session_check()
                            self.flash_result = self.check_and_print_response_result(
                            "Step 4  Diagnostic Session Check"
                            )
                        elif result_data == [0x62, 0xF1, 0x86, 0x02]:
                            self.flash_result=True
                        else:
                            self.flash_result=False
                    else:
                        self.flash_result = self.check_and_print_response_result(
                            "Step 4  Diagnostic Session Check"
                        )

                elif step == 7 and sub_step == 1:
                    # Note: 在step5 information check, 诊断仪可能会使用读取DID F1AA/F1AB/F18C 代替读取DID ED20，而获取版本信息
                    # Step 7  Information Check

                    # 无
                    # self.information_check_ed20()
                    # self.flash_result = self.check_and_print_response_result(
                    #     "Step 7  Information Check ED20"
                    # )

                    sub_step += 1
                    step -= 1

                elif step == 7 and sub_step == 2:
                    # Step 7  Information Check
                    self.information_check_f1aa()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 7  Information Check F1AA"
                    )
                    sub_step += 1
                    step -= 1

                elif step == 7 and sub_step == 3:
                    # Step 7  Information Check

                    # 无
                    # self.information_check_f1ab()
                    # self.flash_result = self.check_and_print_response_result(
                    #     "Step 7  Information Check F1AB"
                    # )

                    sub_step += 1
                    step -= 1

                elif step == 7 and sub_step == 4:
                    # Step 7  Information Check
                    self.information_check_f18c()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 7  Information Check F18C"
                    )

                
                elif step == 8:
                    # Step 8  Public Key Status Check
                    self.public_key_status_check()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 8  Public Key Status Check"
                    )
                    # force to pass
                    self.flash_result = True

                elif step == 9:
                    # Step 9 Unlock For Download
                    self.security_access_level_l1()
                    self.flash_result = self.assert_security_access("L1")

                # =====================================   Programming Sequence Download and activete SBL  =====================================
                elif step == 10:
                    sw_signature = get_vbf_sw_signature(sbl_file_path)
                    vbf_payload = get_vbf_payload(sbl_file_path)
                    vbf_block_infos = get_block_info(vbf_payload)
                    vbf_call = get_vbf_call(sbl_file_path)
                    for block_info in vbf_block_infos:
                        # Step 10  Request Download
                        self.request_download_vbf(list(block_info["start_addr"]), list(block_info["length"]))
                        self.flash_result = self.check_and_print_response_result(
                            "Step 10  Request Download"
                        )
                        if self.flash_result:
                            logger.info("Step 10 Request Download Success")
                        else:
                            logger.error("Step 10  Request Download Failed")
                            break

                        # Step 11  Transfer Data
                        self.flash_result = self.transfer_data_vbf(block_info["data"])
                        if self.flash_result:
                            logger.info("Step 11  Transfer Data Success")
                        else:
                            logger.error("Step 11  Transfer Data Failed")
                            break

                        # Step 12  Request Transfer Exit
                        self.request_transfer_exit()
                        self.flash_result = self.check_and_print_response_result(
                            "Step 12  Request Transfer Exit"
                        )
                        if self.flash_result:
                            logger.info("Step 12  Request Transfer Exit Success")
                        else:
                            logger.error("Step 12  Request Transfer Exit Failed")
                            break
                    logger.info(
                        " ===========================   UDS Transfer SBL Date Complete   ==========================="
                    )
                    step += 2
                elif step == 13:
                    # Step 13 Verify Autherticity
                    self.verify_utherticity(sw_signature)
                    self.flash_result = self.check_and_print_response_result(
                            "Step 13  Verify Autherticity"
                        )
                    # result = self.return_udsdata_and_check_and_print_response_result(
                    #     "Step 13  Verify Autherticity"
                    # )
                    # self.flash_result = result == [
                    #     0x71,
                    #     0x01,
                    #     0x02,
                    #     0x12,
                    #     0x10,
                    #     0x00
                    # ]
                    
                elif step == 14:
                    # Step 14 Activate SBL
                    self.activate_sbl(vbf_call)
                    result = self.return_udsdata_and_check_and_print_response_result(
                        "Step 14  Activate SBL"
                    )
                    self.flash_result = result == [
                        0x71,
                        0x01,
                        0x03,
                        0x01,
                        0x10
                    ]

                # =====================================   Programming Sequence Download flash file(s)  =====================================
                elif step == 15:
                    for file_path in app_file_path:
                        sw_signature = get_vbf_sw_signature(file_path)
                        vbf_erase_info = get_vbf_erase_info(file_path)
                        vbf_payload = get_vbf_payload(file_path)
                        vbf_block_infos = get_block_info(vbf_payload)

                        # Step 15  RoutineControl-Erase Memory
                        self.erase_memory_vbf(vbf_erase_info[0], vbf_erase_info[1])
                        self.flash_result = self.check_and_print_response_result(
                            "Step 15  RoutineControl-Erase Memory"
                        )
                        if self.flash_result:
                            logger.info("Step 15 RoutineControl-Erase Memory Success")
                        else:
                            logger.error("Step 15  RoutineControl-Erase Memory Failed")
                            break

                        for block_info in vbf_block_infos:
                            # Step 16  Request Download
                            self.request_download_vbf(list(block_info["start_addr"]), list(block_info["length"]))
                            self.flash_result = self.check_and_print_response_result(
                                "Step 16  Request Download"
                            )
                            if self.flash_result:
                                logger.info("Step 16 Request Download Success")
                            else:
                                logger.error("Step 16  Request Download Failed")
                                break

                            # Step 17  Transfer Data
                            self.flash_result = self.transfer_data_vbf(block_info["data"])
                            if self.flash_result:
                                logger.info("Step 17  Transfer Data Success")
                            else:
                                logger.error("Step 17  Transfer Data Failed")
                                break

                            # Step 18  Request Transfer Exit
                            self.request_transfer_exit()
                            self.flash_result = self.check_and_print_response_result(
                                "Step 18  Request Transfer Exit"
                            )
                            if self.flash_result:
                                logger.info("Step 18  Request Transfer Exit Success")
                            else:
                                logger.error("Step 18  Request Transfer Exit Failed")
                                break
                        logger.info(
                            " ===========================   Programming Sequence Download flash file(s) Complete   ==========================="
                        )
                        
                        # Step 19 Verify Autherticity
                        self.verify_utherticity(sw_signature)
                        self.flash_result = self.check_and_print_response_result(
                                "Step 19  Verify Autherticity"
                            )
                        if self.flash_result:
                            logger.info("Step 15 RoutineControl-Erase Memory Success")
                        else:
                            logger.error("Step 15  RoutineControl-Erase Memory Failed")
                            break
                    logger.info(
                            " ===========================   UDS Transfer ALL APP Date Complete   ==========================="
                        )
                    step += 4

                # =====================================   Post-programming  sequence =========================================
                elif step == 20:
                    # Step 20  Verify Software Integrity
                    self.verify_software_integrity()
                    result = self.return_udsdata_and_check_and_print_response_result(
                        "Step 20  Verify Software Integrity"
                    )
                    self.flash_result = result == [
                        0x71,
                        0x01,
                        0x02,
                        0x05,
                        0x10,
                        0x00,
                        0x00,
                        0x00,
                        0x00,
                    ]

                    if self.flash_result:
                        logger.info(
                            "====================   Step 20  ecu self Flash success  =========================="
                        )
                    else:
                        logger.info(
                            "====================   Step 20  ecu self Flash Failed  =========================="
                        )

                elif step == 21:
                    # Step 21  ECU Reset
                    self.stop_tester_present()
                    self.reset_ecu()
                    self.flash_result = self.check_and_print_response_result(
                            "Step 21  ECU Reset")
                    sleep(1)

                elif step == 22:
                    # Step 22 Enter Extended Session
                    self.enter_extended_session_functional_addressing()
                    sleep(0.5)
                    # self.flash_result = self.check_and_print_response_result("Step 2  enter extended session")
                
                elif step == 23:
                    # Step 23  communication control
                    self.enable_normal_communication_functional_addressing()
                    # self.flash_result = self.check_and_print_response_result(
                    #         "Step 23  communication control")
                    sleep(0.5)

                elif step == 24:
                    # Step 24  Disable DTC Setting
                    self.start_setting_of_dtc_functional_addressing_vbf()
                    # self.flash_result = self.check_and_print_response_result(
                    #         "Step 24  Disable DTC Setting")
                    sleep(0.5)

                elif step == 25:
                    # Step 25  Enter Default Session
                    self.enter_default_session_functional_addressing()
                    # self.flash_result = self.check_and_print_response_result(
                    #         "Step 25  Enter Default Session")
                    sleep(0.5)
  
        if step != target_step:
            logger.info(
                "=======================   Flash Failed    ========================================"
            )
            # self.reset_ecu_functional_addressing()
            # self.enter_default_session_functional_addressing()
            # self.enter_extended_session_functional_addressing()
            # self.enable_normal_communication_functional_addressing()
            # self.start_setting_of_dtc_functional_addressing()
            # self.enter_default_session_functional_addressing()

        return self.flash_result

    def request_bluetoothkey_whitelist(self, target_step=3, init_step=0, skip_step=[0]):
        '''
        读蓝牙钥匙白名单，如果读到值返回一个列表，否则返回None
        @param target_step:
        @param init_step:
        @param skip_step:
        @return:
        '''
        self.flash_result = True
        step = init_step
        sub_step = 1
        result = None
        result_hexstr = ''
        # Start Flash... Active ECU
        logger.info("====== Start Flash... Active ECU ======")
        while self.flash_result and (step != target_step):
            step += 1
            if step in skip_step:
                logger.info("Skip the step {}".format(step))
            else:
                # =====================================   Enter Program Mode  =========================================

                if step == 1:
                    # Step 1
                    self.enter_extended_session()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 1  enter_extended_session"
                    )

                elif step == 2:
                    # 对应的 0x05，0x06 ， 有时也称呼为 L5， 这里函数以L3显示；
                    self.security_access_level_l3()
                    self.flash_result = self.assert_security_access("L3")

                elif step == 3:
                    self.read_data_by_identifier(0xD90F)
                    result = self.return_udsdata_and_check_and_print_response_result(
                        "step 3 读蓝牙钥匙白名单 read_data_by_identifier"
                    )
                    result_hexstr = DataTypeHanding.intlist_to_hexstr(result)
        return result_hexstr

    def request_entitykey_whitelist(self, target_step=3, init_step=0, skip_step=[0]):
        '''
        获取实体钥匙白名单，如果读到值返回一个列表，否则返回None
        @param target_step:
        @param init_step:
        @param skip_step:
        @return:
        '''
        self.flash_result = True
        step = init_step
        sub_step = 1
        result = None
        result_hexstr = ''
        # Start Flash... Active ECU
        logger.info("====== Start Flash... Active ECU ======")
        while self.flash_result and (step != target_step):
            step += 1
            if step in skip_step:
                logger.info("Skip the step {}".format(step))
            else:
                # =====================================   Enter Program Mode  =========================================

                if step == 1:
                    # Step 1
                    self.enter_extended_session()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 1  enter_extended_session"
                    )

                elif step == 2:
                    # 对应的 0x05，0x06 ， 有时也称呼为 L5， 这里函数以L3显示；
                    self.security_access_level_l3()
                    self.flash_result = self.assert_security_access("L3")

                elif step == 3:
                    self.read_data_by_identifier(0xD90E)
                    result = self.return_udsdata_and_check_and_print_response_result(
                        "step 3 读实体钥匙白名单 read_data_by_identifier"
                    )
                    result_hexstr = DataTypeHanding.intlist_to_hexstr(result)
        return result_hexstr

    def __get_flash_done_version(self, check_data=None, **kwargs):
        '''
        获取升级完后的版本，根据 check_data 来判断是否校验
        若 check_data =None 默认不校验  返回获取的版本号，为字符串类型
        若 check_data =“版本号” /[]   返回比较结果 True 或者 False
        版本号格式 S61101100AR
        @param check_data: 默认为 None 不校验，
        '''
        # boot 重启要时间久一些
        file_path = kwargs.get('file_path', None)
        restart_wait_time = kwargs.get('restart_wait_time', None)
        read_timeout = kwargs.get('read_timeout')
        # sleep(20)
        # # 重新链接
        # self.__init__(**self.cfg)
        # self.update_serverdoipid(self.server_doip_id)
        # # 启动
        # self.diagnostic_client_sim_start()
        # sleep(0.5)
        self.tester_present()
        # tcam 升级完成后启动的比较慢 所以要延时久一些
        if self.server_doip_id == 0x1001:
            # bgm
            # boot 重启要时间久一些
            logger.info(f"BGM重启中等待20s")
            sleep(20)
            # timeout = 20
        else:
            # tcam  本应2分钟，实际需要更长时间
            if restart_wait_time is None:
                restart_wait_time = 180
            logger.info(f"TCAM重启中等待{restart_wait_time-self.tcam_redundancy_time}s")
            sleep(restart_wait_time-self.tcam_redundancy_time)
            # timeout = 160
        # # 读取下诊断会话状态
        # t = time.time()
        # # 读取状态 [0x22, 0xF1, 0x86]
        # while time.time() - t < timeout:
        #     try:
        #         self.diagnostic_session_check()
        #         res = self.return_udsdata_and_check_and_print_response_result("read diagnostic_session")
        #         if res[0] == 0x62:
        #             logger.info(f"重启后延时{time.time() - t}s读取到诊断响应")
        #             break
        #         time.sleep(2)
        #     except Exception as e:
        #         logger.info(f"重启后延时{time.time() - t}s未读取到诊断响应》》{str(e)}")
        #         raise Exception(f"重启后延时{time.time() - t}s未读取到诊断响应》》{str(e)}")
        # sleep(1)
        # 读取版本号
        try:
            if file_path is None or file_path.startswith("./2"):
                self.update_serverdoipid(0x1002)
                sleep(2)
                boot_ver = self.read_boot_version_or_check()
                if check_data and boot_ver.upper() != check_data.upper():
                    ret, version = False, boot_ver
                else:
                    ret, version = True, boot_ver
            else:
                # 升级app 校验版本号
                ret, version = self.read_version_or_check(check_data=check_data, read_timeout=read_timeout)

        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
            logger.error(f"读取 版本号失败:{str(e)}")
            ret, version = 0, ''
            # 关闭3E80
            self.stop_tester_present()
            # self.diagnostic_client_sim_close()
        self.update_serverdoipid(0x1001)
        sleep(1)

        return ret, version

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
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                logger.error(f"根据 url 路径获取版本号失败：{str(e)}")
                version = None
        else:
            version = None
        return version

    def get_path_url(self, ver="1.1.0", name="IM"):
        '''
        获取文件路径
        @param ver:
        @param name: 如果是app 则直接填写app 名字，如果是boot  则需要填写app名字_boot名字 （IM_AR  指 IM版本下的boot为AR）
        @return:
        '''
        if "_" in name:
            name = name.strip().upper().split("_")
            app_name = name[0]
            boot_name = name[1]
            ver_string = ver.strip()
            ver_name = "6160110" + ver_string.replace('.', '') + app_name
            boot_ver_name = "2960110110" + boot_name
            url_bin = f"https://repo.jidudev.com/artifactory/BGMSoftware/Release/v{ver}/{ver_name}/{boot_ver_name}.bin"
            url_keyinfo = f"https://repo.jidudev.com/artifactory/BGMSoftware/Release/v{ver}/{ver_name}/{boot_ver_name}.keyinfo"
            logger.info(f"生成boot bin文件路径为{url_bin}")
            logger.info(f"生成boot keyinfo文件路径为{url_keyinfo}")
            return url_bin, url_keyinfo
        else:
            ver_string = ver.strip()
            if self.server_doip_id == 0x1001:
                ver_name = "6160110" + ver_string.replace('.', '') + name.strip().upper()
                url_bin = f"https://repo.jidudev.com/artifactory/BGMSoftware/Release/v{ver}/{ver_name}/{ver_name}.bin"
                url_keyinfo = f"https://repo.jidudev.com/artifactory/BGMSoftware/Release/v{ver}/{ver_name}/{ver_name}.keyinfo"
            elif self.server_doip_id == 0x1011:
                ver_name = "6110110" + ver_string.replace('.', '') + name.strip().upper()
                url_bin = f"https://repo.jidudev.com/artifactory/TCAMSoftware/Release/v{ver}/{ver_name}/{ver_name}.bin"
                url_keyinfo = f"https://repo.jidudev.com/artifactory/TCAMSoftware/Release/v{ver}/{ver_name}/{ver_name}.keyinfo"
            else:
                url_bin = None
                url_keyinfo = None
            logger.info(f"生成app bin文件路径为{url_bin}")
            logger.info(f"生成app keyinfo文件路径为{url_keyinfo}")
            return url_bin, url_keyinfo

    def check_is_update(self, file_url):
        hard_version = self.get_hard_version()
        china_softversion_end = ['A', "B", "C", "D"]
        not_china_softversion_end = ["O"]
        if hard_version is None:
            self.stop_tester_present()
            sleep(0.5)
            self.diagnostic_client_sim_close()
            sleep(5)
            assert False, "获取硬件版本失败，检查是否是GSO版本"
        release_version = file_url.replace(".bin", "")
        if hard_version[-1] in china_softversion_end and release_version[-2] in not_china_softversion_end:
            self.stop_tester_present()
            sleep(0.5)
            self.diagnostic_client_sim_close()
            sleep(5)
            assert False, "台架硬件版本为国内版本，不支持GSO软件版本升级"

    def upgrade_ecu_cdc(
            self, keyinfo, file_url, standard=True, check_data=None, skip_step=[0], offline=False, read_ver=True,
            sniff_packet=False, compression_encryption_method=0x00, offline_flashing=False
    ):
        '''
        对 ecu 进行升级，默认是一个完整的升级流程，
        @param keyinfo:  如 "HacdLlcI1suuaQgb5NYeXSVob7bCxVO8mEN6poxblq76bim0VunQUHvpvkdJzGysy4jUso7AR7L07jEd3cadbyiWPeyoVqdSTVuln3xZyUZxcFvd0ewc2/u1GZKrRwWPF4deM0l+b18lL2zcbmdnO2KX+OqIf4loBaOhQ8OGiOV+DoIYsjXUC/zghbO+Fpz9rkxMH1T7+m33mZo0EwY7uYnmc5CPmIQg2wC/fmnFS91mdqn7pjcwsTKqjKR2eDkTApanNZmwD6HlYlYQDfQEIzBS8sZ/e2e27WRHXLNCynF3lgVzdWmvZZx9yHLLfMx+bBsU4MUTyfcIfselexCLZg=="
        @param file_url: 升级的bin 文件路径 如 "https://repo.jidudev.com/artifactory/TCAMSoftware/Release_build/6110110055BD.bin"
        @param standard: 是否为标准升级流程（默认是 标准流程），为false 表示按special 方式升级
        @param check_data: 版本 字符串类型  如 6160110110AAC 或者6110110055 BD
        @param skip_step: 要跳过的步骤， 为列表格式
        @param offline_flashing: type: bool    是否为离线刷写
        @return:
        '''
        # 如果不传参数，则根据 url 路径获取 版本号
        # self.check_is_update(file_url)
        self.sniff_packet = None
        logger.info(f"cdc 直刷 ")
        if check_data is None:
            check_data = self.get_version_by_url(file_url)
        name = "standard flash" if standard else "special flash"
        logger.info(f"cdc 当前的升级流程为 {name}")
        # 先读取下原来的版本号
        self.update_serverdoipid(doipid=0x1201, ecu='CDC')
        sleep(0.1)
        if standard:
            self.tester_present()
        else:
            self.tester_present_special()
        sleep(0.5)

        # 下载文件，要放在开启3e80 后面，防止下载时间久，会超时拆链接
        file_path = self.download_and_check_bin_file(file_url)
        if file_path is None:
            try:
                self.stop_tester_present()
                self.diagnostic_client_sim_close()
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                logger.info("==================== bin 文件下载异常 ==========================")
                logger.error(e)
            assert 0, "bin 文件下载异常"
        # 读取状态 [0x22, 0xF1, 0x86]
        self.diagnostic_session_check()
        result = self.return_udsdata_and_check_and_print_response_result("read diagnostic_session")
        # [0x62, 0xF1, 0x86,0x01/0x02]
        logger.info("==================== SdTester started ==========================")
        if read_ver:
            end_step = 14
        else:
            end_step = 13
        try:
            if standard:
                result = self.flash_single_standard_ecu(
                    file_path,
                    keyinfo,
                    target_step=2,
                    init_step=0,
                    check_data=check_data,
                    skip_step=skip_step,
                    compression_encryption_method=compression_encryption_method
                )
            else:
                result = self.flash_single_ecu_special(
                    file_path,
                    keyinfo,
                    target_step=2,
                    init_step=0,
                    skip_step=skip_step,
                )
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
            logger.error(e)
            result = 0
            if not result:
                try:
                    self.send_request_and_recv_response([0x10, 0x01])
                    self.send_request_and_recv_response([0x10, 0x03])
                    self.send_request_and_recv_response([0x11, 0x03])
                    logger.info(
                        "====================  Flash Failed , Restart  =========================="
                    )
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                    logger.error(f"cdc 重启失败 {str(e)}")
                    logger.warning(
                        "====================  Flash Failed , Restart  Failed =========================="
                    )
                    result=0
        if result:
            self.reset_positive_ack()
            # self.enter_program_session_functional_addressing()
            try:
                recv_data_list = self.return_udsdata_and_check_and_print_response_result(f"接收1082 的响应")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                logger.warning(f"未接收到 1082 的响应 {str(e)}")
            try:
                if standard:
                    result = self.flash_single_standard_ecu(
                        file_path,
                        keyinfo,
                        target_step=end_step,
                        init_step=2,
                        check_data=check_data,
                        skip_step=skip_step,
                        compression_encryption_method=compression_encryption_method,
                        offline_flashing=offline_flashing,
                    )
                else:
                    result = self.flash_single_ecu_special(
                        file_path,
                        keyinfo,
                        target_step=end_step,
                        init_step=2,
                        skip_step=skip_step,
                    )
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                logger.error(e)
                result = 0
                if not result:
                    try:
                        self.send_request_and_recv_response([0x10, 0x01])
                        self.send_request_and_recv_response([0x10, 0x03])
                        self.send_request_and_recv_response([0x11, 0x03])
                        logger.info(
                            "====================  Flash Failed , Restart  =========================="
                        )
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                        logger.error(f"cdc 重启失败 {str(e)}")
                        logger.warning(
                            "====================  Flash Failed , Restart  Failed =========================="
                        )
                        result = 0

        try:
            self.stop_tester_present()
            # self.diagnostic_client_sim_close()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
            logger.info("==================== SdTester Stopped Error ==========================")
            logger.error(e)
        logger.info("==================== SdTester stopped ==========================")

        assert result, "CDC 升级失败"

    def upgrade_ecu_tcam(
            self, keyinfo, file_url, standard=True, check_data=None, skip_step=[0], offline=False, read_ver=True,
            sniff_packet=False, compression_encryption_method=0x00, offline_flashing=False, restart_wait_time=None, read_timeout=None
    ):
        '''
        对 ecu 进行升级，默认是一个完整的升级流程，
        @param keyinfo:  如 "HacdLlcI1suuaQgb5NYeXSVob7bCxVO8mEN6poxblq76bim0VunQUHvpvkdJzGysy4jUso7AR7L07jEd3cadbyiWPeyoVqdSTVuln3xZyUZxcFvd0ewc2/u1GZKrRwWPF4deM0l+b18lL2zcbmdnO2KX+OqIf4loBaOhQ8OGiOV+DoIYsjXUC/zghbO+Fpz9rkxMH1T7+m33mZo0EwY7uYnmc5CPmIQg2wC/fmnFS91mdqn7pjcwsTKqjKR2eDkTApanNZmwD6HlYlYQDfQEIzBS8sZ/e2e27WRHXLNCynF3lgVzdWmvZZx9yHLLfMx+bBsU4MUTyfcIfselexCLZg=="
        @param file_url: 升级的bin 文件路径 如 "https://repo.jidudev.com/artifactory/TCAMSoftware/Release_build/6110110055BD.bin"
        @param standard: 是否为标准升级流程（默认是 标准流程），为false 表示按special 方式升级
        @param check_data: 版本 字符串类型  如 6160110110AAC 或者6110110055 BD
        @param skip_step: 要跳过的步骤， 为列表格式
        @param offline_flashing: type: bool    是否为离线刷写
        @return:
        '''
        # 如果不传参数，则根据 url 路径获取 版本号
        self.check_is_update(file_url)
        self.sniff_packet = None
        logger.info(f"tcam 直刷 ")
        if check_data is None:
            check_data = self.get_version_by_url(file_url)
        name = "standard flash" if standard else "special flash"
        logger.info(f"tcam 当前的升级流程为 {name}")
        # 先读取下原来的版本号
        self.update_serverdoipid(doipid=0x1011, ecu='TCAM')
        sleep(0.1)
        if standard:
            self.tester_present()
        else:
            self.tester_present_special()
        sleep(0.5)

        # 下载文件，要放在开启3e80 后面，防止下载时间久，会超时拆链接
        if file_url.startswith('https:'):
            file_path = self.download_and_check_bin_file(file_url)
            if file_path is None:
                try:
                    self.stop_tester_present()
                    self.diagnostic_client_sim_close()
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                    logger.info("==================== bin 文件下载异常 ==========================")
                    logger.error(e)
                assert 0, "bin 文件下载异常"
        else:
            url_bin, url_keyinfo = self.get_path_url(ver=keyinfo, name=file_url)
            # 下载文件，要放在开启3e80 后面，防止下载时间久，会超时拆链接 下载 keyinfo 文件
            url_keyinfo_path = self.download_and_check_bin_file(url_keyinfo, offline)
            if url_keyinfo_path is None:
                try:
                    self.stop_tester_present()
                    # self.diagnostic_client_sim_close()
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                    logger.info("==================== keyinfo 文件下载异常 ==========================")
                    logger.error(e)
                assert 0, "keyinfo 文件下载异常"
            else:
                with open(url_keyinfo_path, "r") as f:
                    lines = f.readlines()
                    lines_list = [i.strip().replace("\n", '') for i in lines if i.strip()]
                    keyinfo = lines_list[-1].split(":")[-1]
                    logger.info(f"获取的keyinfo=》{keyinfo}")
            if check_data == file_url:
                check_data = self.get_version_by_url(url_bin)
            file_path = self.download_and_check_bin_file(url_bin, offline)
            if file_path is None:
                try:
                    self.stop_tester_present()
                    # self.diagnostic_client_sim_close()
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                    logger.info("==================== bin 文件下载异常 ==========================")
                    logger.error(e)
                assert 0, "bin 文件下载异常"
        # 读取状态 [0x22, 0xF1, 0x86]
        self.diagnostic_session_check()
        result = self.return_udsdata_and_check_and_print_response_result("read diagnostic_session")
        # [0x62, 0xF1, 0x86,0x01/0x02]
        logger.info("==================== SdTester started ==========================")
        if read_ver:
            end_step = 14
        else:
            end_step = 13
        try:
            if standard:
                result = self.flash_single_standard_ecu(
                    file_path,
                    keyinfo,
                    target_step=2,
                    init_step=0,
                    check_data=check_data,
                    skip_step=skip_step,
                    compression_encryption_method=compression_encryption_method,
                    read_timeout=read_timeout,
                    restart_wait_time=restart_wait_time
                )
            else:
                result = self.flash_single_ecu_special(
                    file_path,
                    keyinfo,
                    target_step=2,
                    init_step=0,
                    skip_step=skip_step,
                    read_timeout=read_timeout,
                    restart_wait_time=restart_wait_time
                )
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
            logger.error(e)
            result = 0
            if not result:
                try:
                    self.send_request_and_recv_response([0x10, 0x01])
                    self.send_request_and_recv_response([0x10, 0x03])
                    self.send_request_and_recv_response([0x11, 0x03])
                    logger.info(
                        "====================  Flash Failed , Restart  =========================="
                    )
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                    logger.error(f"tcam 重启失败 {str(e)}")
                    logger.warning(
                        "====================  Flash Failed , Restart  Failed =========================="
                    )
                    result=0
        if result:
            self.reset_positive_ack()
            # self.enter_program_session_functional_addressing()
            try:
                recv_data_list = self.return_udsdata_and_check_and_print_response_result(f"接收1082 的响应")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                logger.warning(f"未接收到 1082 的响应 {str(e)}")
            try:
                if standard:
                    result = self.flash_single_standard_ecu(
                        file_path,
                        keyinfo,
                        target_step=end_step,
                        init_step=2,
                        check_data=check_data,
                        skip_step=skip_step,
                        compression_encryption_method=compression_encryption_method,
                        offline_flashing=offline_flashing,
                        read_timeout=read_timeout,
                        restart_wait_time=restart_wait_time
                    )
                else:
                    result = self.flash_single_ecu_special(
                        file_path,
                        keyinfo,
                        target_step=end_step,
                        init_step=2,
                        skip_step=skip_step,
                        read_timeout=read_timeout,
                        restart_wait_time=restart_wait_time
                    )
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                logger.error(e)
                result = 0
                if not result:
                    try:
                        self.send_request_and_recv_response([0x10, 0x01])
                        self.send_request_and_recv_response([0x10, 0x03])
                        self.send_request_and_recv_response([0x11, 0x03])
                        logger.info(
                            "====================  Flash Failed , Restart  =========================="
                        )
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                        logger.error(f"tcam 重启失败 {str(e)}")
                        logger.warning(
                            "====================  Flash Failed , Restart  Failed =========================="
                        )
                        result = 0

        try:
            self.stop_tester_present()
            # self.diagnostic_client_sim_close()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
            logger.info("==================== SdTester Stopped Error ==========================")
            logger.error(e)
        logger.info("==================== SdTester stopped ==========================")

        assert result, "TCAM 升级失败"

    def upgrade_ecu(
            self, keyinfo, file_url, standard=True, check_data=None, skip_step=[0], offline=False, save_packet=False,sniff_packet=False,save_path='.', restart_wait_time=None, read_timeout=None
    ):
        '''
        对 ecu 进行升级，默认是一个完整的升级流程，
        file_url 可以为url 路径或者 为 app 的名字(IM)，或者app名字_boot名字（IM_AR）
        keyinfo 为 keyinfo字符串 或者为 1.1.0；1.3.0  和file_url 对应
        
        @param keyinfo:  如 "HacdLlcI1suuaQgb5NYeXSVob7bCxVO8mEN6poxblq76bim0VunQUHvpvkdJzGysy4jUso7AR7L07jEd3cadbyiWPeyoVqdSTVuln3xZyUZxcFvd0ewc2/u1GZKrRwWPF4deM0l+b18lL2zcbmdnO2KX+OqIf4loBaOhQ8OGiOV+DoIYsjXUC/zghbO+Fpz9rkxMH1T7+m33mZo0EwY7uYnmc5CPmIQg2wC/fmnFS91mdqn7pjcwsTKqjKR2eDkTApanNZmwD6HlYlYQDfQEIzBS8sZ/e2e27WRHXLNCynF3lgVzdWmvZZx9yHLLfMx+bBsU4MUTyfcIfselexCLZg=="
        @param file_url: 升级的bin 文件路径 如 "https://repo.jidudev.com/artifactory/TCAMSoftware/Release_build/6110110055BD.bin"
        @param standard: 是否为标准升级流程（默认是 标准流程），为false 表示按special 方式升级
        @param check_data: 版本 字符串类型  如 6160110110AAC 或者6110110055 BD
        @param skip_step: 要跳过的步骤， 为列表格式
        @param offline: 是否离线刷写，默认在线刷写，离线刷写 需要吧 对应的bin 文件放在执行目录下，tcam 则放在sat/xat_cases/legacy/tcam ；bgm则放在sat/xat_cases/legacy/bgm
        @param save_packet: 是否要保存抓包数据
        @param sniff_packet: 是否要保存tcpdump抓包数据
        @param save_path: 保存tcpdump抓包数据的路径
        @param restart_wait_time: 域控重启等待时间
        @param read_timeout: 读取22 f1 ae的超时时间
        @return:
        '''
        self.check_is_update(file_url)
        self.sniff_packet = sniff_packet
        
        if self.sniff_packet:
            BGM_SSH().init_bgm_tcpdump()
            
        if save_packet:
            self.sff = SniffPacket(iface='169.254.1.200')
            # 设置抓包保存名字，可以不设置，有默认值，保存的文件都会带有时间
            self.sff.set_save_name('诊断升级')
            # 开启抓包
            self.sff.start_sniff()
        try:
            # 如果不传参数，则根据 url 路径获取 版本号
            if check_data is None:
                check_data = self.get_version_by_url(file_url)
            name = "standard flash" if standard else "special flash"
            logger.info(f"当前的升级流程为 {name}")
            doipip = self.server_doip_id
            # doipip = 0x1002
            self.flash_time_total = {}
            # 先读取下原来的版本号
            self.update_serverdoipid(doipip)
            sleep(0.1)
            if standard:
                self.tester_present()
            else:
                self.tester_present_special()
            sleep(0.5)

            if file_url.startswith('https:'):
                # 下载文件，要放在开启3e80 后面，防止下载时间久，会超时拆链接
                file_path = self.download_and_check_bin_file(file_url, offline)
                if file_path is None:
                    try:
                        self.stop_tester_present()
                        # self.diagnostic_client_sim_close()
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                        logger.info("==================== bin 文件下载异常 ==========================")
                        logger.error(e)
                    assert 0, "bin 文件下载异常"
            else:
                url_bin, url_keyinfo = self.get_path_url(ver=keyinfo, name=file_url)
                # 下载文件，要放在开启3e80 后面，防止下载时间久，会超时拆链接 下载 keyinfo 文件
                url_keyinfo_path = self.download_and_check_bin_file(url_keyinfo, offline)
                if url_keyinfo_path is None:
                    try:
                        self.stop_tester_present()
                        # self.diagnostic_client_sim_close()
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                        logger.info("==================== keyinfo 文件下载异常 ==========================")
                        logger.error(e)
                    assert 0, "keyinfo 文件下载异常"
                else:
                    with open(url_keyinfo_path, "r") as f:
                        lines = f.readlines()
                        lines_list = [i.strip().replace("\n", '') for i in lines if i.strip()]
                        keyinfo = lines_list[-1].split(":")[-1]
                        logger.info(f"获取的keyinfo=》{keyinfo}")
                if check_data == file_url:
                    check_data = self.get_version_by_url(url_bin)
                # 下载文件，要放在开启3e80 后面，防止下载时间久，会超时拆链接
                file_path = self.download_and_check_bin_file(url_bin, offline)
                if file_path is None:
                    try:
                        self.stop_tester_present()
                        # self.diagnostic_client_sim_close()
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                        logger.info("==================== bin 文件下载异常 ==========================")
                        logger.error(e)
                    assert 0, "bin 文件下载异常"


            # 读取状态 [0x22, 0xF1, 0x86]
            self.diagnostic_session_check()
            result = self.return_udsdata_and_check_and_print_response_result("read diagnostic_session")
            # [0x62, 0xF1, 0x86,0x01/0x02]
            diagnostic_session = result[-1]
            sleep(0.5)
            # 判断是boot 升级 还是app
            if diagnostic_session == 1:
                # app 升级
                self.read_version_or_check()
            else:
                self.update_serverdoipid(0x1002)
                sleep(2)
                self.read_boot_version_or_check()

            self.update_serverdoipid(doipip)
            sleep(1)
            try:
                if standard:
                    result = self.flash_single_standard_ecu(
                        file_path,
                        keyinfo,
                        target_step=2,
                        init_step=0,
                        check_data=check_data,
                        skip_step=skip_step,
                        read_timeout=read_timeout,
                        restart_wait_time=restart_wait_time
                    )
                else:
                    result = self.flash_single_ecu_special(
                        file_path, keyinfo, target_step=2, init_step=0, skip_step=skip_step, read_timeout=read_timeout, restart_wait_time=restart_wait_time
                    )
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                logger.info(
                    "==================== flash_single_standard_ecu Error =========================="
                )
                logger.error(e)
                result = 0
                try:
                    self.stop_tester_present()
                    # self.diagnostic_client_sim_close()
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                    logger.info(
                        "==================== SdTester Stopped Error =========================="
                    )
                    logger.error(e)

            sleep(10)
            # 重新建立链接
            # self.__init__(**self.cfg)
            # self.update_serverdoipid(doipip)
            # # 启动
            # self.diagnostic_client_sim_start()
            # sleep(0.1)
            if standard:
                self.tester_present()
            else:
                self.tester_present_special()
            sleep(0.5)
         
            
            logger.info("==================== SdTester started ==========================")
            if result:
                # "At BGM's request, wait 20 s from 10 82 to 10 02"
                sleep(10)
                   
                if self.sniff_packet:
                    tcpdump_file_path,tcpdump_save_name = BGM_SSH().start_bgm_tcpdump(iface='eth0',name='eth0_',path='/data',eth_len=128)
                    logger.info('starting to sniff eth0 packet')
                
                if self.server_doip_id== 0x1011:
                    self.update_serverdoipid(0x1011,'TCAM')
                else:
                    self.update_serverdoipid(self.server_doip_id,'BGM')
                        
                try:
                    if standard:
                        result = self.flash_single_standard_ecu(
                            file_path,
                            keyinfo,
                            target_step=14,
                            init_step=2,
                            check_data=check_data,
                            skip_step=skip_step,
                            read_timeout=read_timeout,
                            restart_wait_time=restart_wait_time
                        )
                    else:
                        result = self.flash_single_ecu_special(
                            file_path,
                            keyinfo,
                            target_step=14,
                            init_step=2,
                            skip_step=skip_step,
                            read_timeout=read_timeout,
                            restart_wait_time=restart_wait_time
                        )
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                    if self.sniff_packet:
                        BGM_SSH().stop_bgm_tcpdump()
                        logger.info('stop sniff packet eth0')
                        
                    logger.error(e)
                    result = 0

            if not result:
                # wait bgm save log
                sleep(20)
                try:
                    self.stop_tester_present()
                    # self.diagnostic_client_sim_close()
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                    logger.error(e)
                try:
                    if self.server_doip_id == 0x1001:
                        self.reset_ecu_functional_addressing()
                        sleep(20)
                        logger.info('BGM刷写失败 重启BGM并等待20s')
                    else:
                        logger.info('TCAM刷写失败 重启TCAM并等待180s')
                        self.enter_default_session()
                        result = self.return_udsdata_and_check_and_print_response_result()
                        assert result[0:2]==[0x50,0x01]
                        self.enter_extended_session()
                        result = self.return_udsdata_and_check_and_print_response_result()
                        assert result[0:2]==[0x50,0x03]
                        self.reset_ecu3()
                        result = self.return_udsdata_and_check_and_print_response_result()
                        assert result[0:2]==[0x51,0x03]
                        sleep(180)
                    logger.info("==========  Flash Failed , Restart  =======")
                    result = 0
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                    logger.error(str(e))
                    logger.warning("====  Flash Failed , Restart  Failed =========")
                    result = 0
            try:
                self.stop_tester_present()
                # self.diagnostic_client_sim_close()
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                logger.info("==================== SdTester Stopped Error ==========================")
                logger.error(e)

            logger.info("==================== SdTester stopped ==========================")
            # sleep(20)
            global flash_count
            flash_count += 1
            flash_count_name = "flash_count_{}".format(flash_count)
            self.flash_time_total[flash_count_name] = self.flash_time_statistics
            logger.info(
                "{} Flash Time statistics[transfer_data_total_int_time,pregramming_dependencies_total_int_time,"
                "flash_total_int_time] is {}".format(
                    flash_count_name, self.flash_time_statistics
                )
            )
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
            logger.error(f'升级失败{str(e)}')
            sleep(10)
            result = 0

        if save_packet:
            #  停止抓抓包
            self.sff.stop_sniff()
        
        if self.sniff_packet:
            #把抓包数据下下载到本地 下载完成后删除
            BGM_SSH().scp_bgm_file_to_local(bgm_file_pah=tcpdump_file_path,local_path=save_path,del_flag=True)
            logger.info(f'download sniff packet /{tcpdump_save_name} to {save_path} ...')
            
        assert result, " Flash >>>>>>>>>>>>>>>>  Failed"

    def upgrade_ecu_zip(self, keyinfo, file_url, skip_step=[0],save_packet=False):
        '''
        刷写 zip 包
         @param keyinfo: 默认全部是0  [0] * 344
         @param file_url: 文件路径

        @param skip_step: 要跳过的步骤， 为列表格式
        @return:
        '''
        if save_packet:
            self.sff = SniffPacket(iface='169.254.1.200')
            # 设置抓包保存名字，可以不设置，有默认值，保存的文件都会带有时间
            self.sff.set_save_name('诊断升级')
            # 开启抓包
            self.sff.start_sniff()
        try:
            doipip = self.server_doip_id
            self.flash_time_total = {}
            # 下载文件
            file_path = file_url
            self.update_serverdoipid(doipip)
            sleep(0.1)
            self.tester_present()
            sleep(0.5)
            try:
                result = self.flash_ecu_zip(
                    file_path,
                    keyinfo,
                    target_step=2,
                    init_step=0,
                    skip_step=skip_step,
                )

            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                logger.info(
                    "==================== flash_single_standard_ecu_zip Error =========================="
                )
                logger.error(e)
                result = 0
                try:
                    self.stop_tester_present()
                    # self.diagnostic_client_sim_close()
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                    logger.info(
                        "==================== SdTester Stopped Error =========================="
                    )
                    logger.error(e)

            sleep(10)
            # 重新建立链接
            # self.__init__(**self.cfg)
            # self.update_serverdoipid(doipip)
            # # 启动
            # self.diagnostic_client_sim_start()
            # sleep(0.1)
            self.tester_present()
            sleep(0.5)
            logger.info("==================== SdTester started ==========================")
            if result:
                # "At BGM's request, wait 20 s from 10 82 to 10 02"
                sleep(10)
                try:
                    result = self.flash_ecu_zip(
                        file_path,
                        keyinfo,
                        target_step=13,
                        init_step=2,

                        skip_step=skip_step,
                    )

                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                    logger.error(e)
                    result = 0

            if not result:
                # wait bgm save log
                sleep(20)
                try:
                    self.stop_tester_present()
                    # self.diagnostic_client_sim_close()
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                    logger.error(e)
                try:
                    self.reset_ecu_functional_addressing()
                    logger.info(
                        "====================  Flash Failed , Restart  =========================="
                    )
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                    logger.error(str(e))
                    logger.warning(
                        "====================  Flash Failed , Restart  Failed =========================="
                    )

            try:
                self.stop_tester_present()
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
                logger.info("==================== SdTester Stopped Error ==========================")
                logger.error(e)

            logger.info("==================== SdTester stopped ==========================")
            # sleep(20)
            global flash_count
            flash_count += 1
            flash_count_name = "flash_count_{}".format(flash_count)
            self.flash_time_total[flash_count_name] = self.flash_time_statistics
            logger.info(
                "{} Flash Time statistics[transfer_data_total_int_time,pregramming_dependencies_total_int_time,"
                "flash_total_int_time] is {}".format(
                    flash_count_name, self.flash_time_statistics
                )
            )
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
            logger.error(f'升级失败{str(e)}')
            sleep(10)
            result = 0
            #  停止抓抓包
        if save_packet:
            self.sff.stop_sniff()

        assert result, " Flash zip >>>>>>>>>>>>>>>>  Failed"

    def flash_ecu_zip(self, file_path, key_info=None, target_step=13, init_step=0, skip_step=[0]):
        '''
        刷写 zip 包

         @param keyinfo: 默认全部是0  [0] * 344
         @param file_url: 文件路径
        @param target_step: 结束步骤 （最大为 13）
        @param init_step: 开始步骤  （最小为 0）
        @param skip_step: 要跳过的步骤， 为列表格式
        @param check_data: 版本 字符串类型  如 6160110110AAC 或者6110110055 BD
        @return:
        '''
        self.flash_result = True
        step = init_step
        sub_step = 1
        self.transfer_data_total_int_time = 0
        self.pregramming_dependencies_total_int_time = 0
        self.flash_total_int_time = 0
        self.flash_start = time.time()
        # Start Flash... Active ECU
        logger.info("====== Start Flash... Active ECU ======")
        while self.flash_result and (step != target_step):
            step += 1
            if step in skip_step:
                logger.info("Skip the step {}".format(step))
            else:
                # =====================================   Enter Program Mode  =========================================
                if step == 1:
                    # Step 1  Check Program Pre-condition
                    self.check_program_pre_condition_functional_addressing()
                    sleep(1.5)
                    # self.flash_result = self.check_and_print_response_result("Step 1  Check Program Pre-condition")

                elif step == 2:
                    self.stop_tester_present()
                    # Step 2  Enter Program Mode
                    self.enter_program_session_functional_addressing()
                    # self.flash_result = self.check_and_print_response_result("Step 2  Enter Program Mode")

                elif step == 3:
                    # Step 3  Confirm Program Mode
                    self.enter_programming_session()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 3  Confirm Program Mode"
                    )

                elif step == 4:
                    # Step 4  Diagnostic Session Check
                    self.diagnostic_session_check()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 4  Diagnostic Session Check"
                    )

                elif step == 5 and sub_step == 1:
                    # Note: 在step5 information check, 诊断仪可能会使用读取DID F1AA/F1AB/F18C 代替读取DID ED20，而获取版本信息
                    # Step 5  Information Check
                    self.information_check_ed20()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 5  Information Check ED20"
                    )
                    sub_step += 1
                    step -= 1

                elif step == 5 and sub_step == 2:
                    # Step 5  Information Check
                    # self.information_check_f1aa()
                    # self.flash_result = self.check_and_print_response_result(
                    #     "Step 5  Information Check F1AA"
                    # )
                    sub_step += 1
                    step -= 1

                elif step == 5 and sub_step == 3:
                    # Step 5  Information Check
                    # self.information_check_f1ab()
                    # self.flash_result = self.check_and_print_response_result(
                    #     "Step 5  Information Check F1AB"
                    # )
                    sub_step += 1
                    step -= 1

                elif step == 5 and sub_step == 4:
                    # Step 5  Information Check
                    # self.information_check_f18c()
                    # self.flash_result = self.check_and_print_response_result(
                    #     "Step 5  Information Check F18C"
                    # )
                    pass

                # =====================================   Pre-programming Sequence  =====================================
                elif step == 6:
                    # Step 6  Public Key Status Check
                    # self.public_key_status_check()
                    # self.flash_result = self.check_and_print_response_result(
                    #     "Step 6  Public Key Status Check"
                    # )
                    # force to pass
                    self.flash_result = True
                    step -= 0.5

                elif step == 6.5:
                    # float There may be a problem  !!!
                    # Step 6.5 Unlock For Download
                    self.security_access_level_l1()
                    self.flash_result = self.assert_security_access("L1")
                    step -= 0.5
                    step = int(step)

                # =====================================   Download data file(s)  =====================================
                elif step == 7:
                    # Step 7  RoutineControl-Erase Memory
                    self.erase_memory(file_path)
                    self.flash_result = self.check_and_print_response_result(
                        "Step 7  RoutineControl-Erase Memory"
                    )

                elif step == 8:
                    # Step 8  Request Download
                    # compression method and encryption method
                    self.request_download(
                        file_path, compression_encryption_method=[0x00], first_address=1
                    )
                    self.flash_result = self.check_and_print_response_result(
                        "Step 8  Request Download"
                    )

                elif step == 9:
                    # Step 9  Transfer Data
                    self.transfer_data_start = time.time()

                    self.transfer_data(file_path)
                    self.flash_result = self.check_and_print_response_result(
                        "Step 9  Transfer Data"
                    )

                    self.transfer_data_end = time.time()
                    self.transfer_data_total_time = (
                            self.transfer_data_end - self.transfer_data_start
                    )
                    self.transfer_data_total_int_time = int(
                        self.transfer_data_total_time
                    )
                    self.transfer_data_total_time_minute = (
                            self.transfer_data_total_int_time // 60
                    )
                    self.transfer_data_total_time_second = (
                            self.transfer_data_total_int_time % 60
                    )
                    logger.info(
                        "self.transfer_data_total_time is {} minutes  {} seconds".format(
                            self.transfer_data_total_time_minute,
                            self.transfer_data_total_time_second,
                        )
                    )

                elif step == 10:
                    # Step 10  Request Transfer Exit
                    self.request_transfer_exit()
                    self.flash_result = self.check_and_print_response_result(
                        "Step 10  Request Transfer Exit"
                    )
                    logger.info(
                        " ===========================   UDS Transfer Date Complete   ==========================="
                    )

                elif step == 11:
                    # Step 11  Transfer Key Info
                    # key_info = "${XAT_CREDENTIAL_SCAN_883E080423C846F09463} HEMEq1LBLl1UXmmnEX6Eyk1SgRMPaK1xKPpq94/jqs X/DbSkaypQZkn3rPBi TISliJ3FeJYB /q0FAaC5cNTycRcD0PQrH/F02DFYpxwkwtWMGPfnkIwAgQDitdfQ7g=="
                    # key_info = "${XAT_CREDENTIAL_SCAN_3730811E08AC4BE3A2ED}"
                    # TCAM gongcheng AG key_info = "ZZis1PH6rsAc5FV8qaoKUDw4lzLE2SXHSMsIJ2cARyuWAtKmJADJYqE4g4LzX01VE0fUvfvHnVm0HDO0pmMXKrtGjvIbQuP6TNIuxt7xrOodk8Cwn5q+WSFmMd2pf6i1N0YPznbo+7Niw4AhJznwbKMQDaYl4Eeia5K7mjZ2MWl9E33VjXLh/NfYNu4vLQzCyMvkV91YNh4WmHR+tIdmJ3iRKxkQMtpkKZKYGAu3FfjnZXYHqvQHcmzFPUFFIVWkVZsh8DwjL7WZi/LskSTQZNSgZF++wfb43hOSteKrCgCZVNCJyhTOp3rT21TtXJ5bRewFBiBksPm3Fb+mfAEp3Q=="
                    # key_info = key_info.encode("utf-8")
                    # key_info = list(key_info)
                    if key_info is None:
                        key_info = [0] * 344
                    elif isinstance(key_info, str):
                        # 如果是字符串，转化为 列表
                        key_info = [int(key_info[i:i + 2]) for i in range(0, len(key_info), 2)]
                        pass

                    self.transfer_key_info(key_info)
                    self.flash_result = self.check_and_print_response_result(
                        "Step 11  Transfer Key Info"
                    )

                # =====================================   Post-programming =========================================
                elif step == 12:
                    # Step 12  Verify Software Integrity
                    self.pregramming_dependencies_start = time.time()
                    self.verify_software_integrity()
                    result = self.return_udsdata_and_check_and_print_response_result(
                        "Step 12  Verify Software Integrity"
                    )
                    self.flash_result = result == [
                        0x71,
                        0x01,
                        0x02,
                        0x05,
                        0x10,
                        0x00,
                        0x00,
                        0x00,
                        0x00,
                    ]
                    if self.flash_result:
                        logger.info(
                            "====================   Step 12  ecu self Flash success  =========================="
                        )
                    else:
                        logger.info(
                            "====================   Step 12  ecu self Flash Failed  =========================="
                        )

                    self.pregramming_dependencies_end = time.time()
                    self.pregramming_dependencies_total_time = (
                            self.pregramming_dependencies_end
                            - self.pregramming_dependencies_start
                    )
                    self.pregramming_dependencies_total_int_time = int(
                        self.pregramming_dependencies_total_time
                    )
                    self.pregramming_dependencies_total_time_minute = (
                            self.pregramming_dependencies_total_int_time // 60
                    )
                    self.pregramming_dependencies_total_time_second = (
                            self.pregramming_dependencies_total_int_time % 60
                    )
                    logger.info(
                        "self.pregramming_dependencies_total_time is {} minutes  {} seconds".format(
                            self.pregramming_dependencies_total_time_minute,
                            self.pregramming_dependencies_total_time_second,
                        )
                    )

                elif step == 13:
                    self.stop_tester_present()
                    # Step 13  ECU Reset
                    self.reset_ecu_functional_addressing()
                    # self.flash_result = self.check_and_print_response_result(
                    #     "Step 13  ECU Reset")

                    self.flash_end = time.time()
                    self.flash_total_time = self.flash_end - self.flash_start
                    self.flash_total_int_time = int(self.flash_total_time)
                    self.flash_total_time_minute = self.flash_total_int_time // 60
                    self.flash_total_time_second = self.flash_total_int_time % 60
                    logger.info(
                        "flash_total_time is {} minutes  {} seconds".format(
                            self.flash_total_time_minute, self.flash_total_time_second
                        )
                    )
                    logger.info(
                        " ===========================   Doip Flash Complete   ==========================="
                    )

        if step != target_step:
            logger.info(
                "=======================   Flash Failed    ========================================"
            )
            # self.reset_ecu_functional_addressing()
            # self.enter_default_session_functional_addressing()
            # self.enter_extended_session_functional_addressing()
            # self.enable_normal_communication_functional_addressing()
            # self.start_setting_of_dtc_functional_addressing()
            # self.enter_default_session_functional_addressing()

        self.flash_time_statistics = [
            self.transfer_data_total_int_time,
            self.pregramming_dependencies_total_int_time,
            self.flash_total_int_time,
        ]

        return self.flash_result

    def make_ccp_according_id_and_data(self, name, input):
        # name_mode=1,input_mode=1  中文名称-值
        # name_mode=2,input_mode=2  中文名称-值描述
        # name_mode=2,input_mode=1  英文名称-值
        # name_mode=2,input_mode=2  英文名称-值描述
        # name_mode=3,input_mode=1  数字名称-值
        # name_mode=3,input_mode=2  数字名称-值描述

        data_handle = DataTypeHanding()

        if data_handle.is_chinese(name):
            name_mode = 1
        elif name.isdigit():
            name_mode = 3
        elif data_handle.is_English_no_spcae(name):
            name_mode = 2

        if len(input) == 2:
            input_mode = 1
        else:
            input_mode = 2

        with open(self.ccp_json_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            json_data = json.loads(file_content)
            ccp_dict = {}
            ccp_list = []
            ccp = ""
            data = ''
            ccp = ""
            value = {}

            English_describe_dict = {}
            English_describe_list = []

            Chinese_describe_dict = {}
            Chinese_describe_list = []

            id_value_dict = {}
            id_value_list = []

        # file.close()

        for i in range(1558):
            English_describe_dict[i] = json_data[i]["CCP英文描述"]
            English_describe_list.append(English_describe_dict[i])

        for i in range(1558):
            Chinese_describe_dict[i] = json_data[i]["CCP中文描述"]
            Chinese_describe_list.append(Chinese_describe_dict[i])

        for i in range(1558):
            id_value_dict[i] = json_data[i]['待写入CCP值']
            id_value_list.append(id_value_dict[i])

        # 中文名称-值
        if name_mode == 1 and input_mode == 1:
            print("name=", name)
            index = Chinese_describe_list.index(name)
            print("index=", index)
            print("input=", input)
            json_data[index]["待写入CCP值"] = input

        # 中文名称-值描述
        elif name_mode == 1 and input_mode == 2:

            index = Chinese_describe_list.index(name)
            print('index=', index)
            for i in json_data[index]["CCP取值"].split('\n'):
                value[i.split('=')[1]] = i.split('=')[0]

            print('value=', value)
            input = value[input]
            # print('data=',data)
            json_data[index]["待写入CCP值"] = input

        # 英文名称-值
        elif name_mode == 2 and input_mode == 1:
            index = English_describe_list.index(name)
            print('index=', index)
            json_data[index]["待写入CCP值"] = input

        # 英文名称-值描述
        elif name_mode == 2 and input_mode == 2:
            index = English_describe_list.index(name)
            # print('index=', index)
            for i in json_data[index]["CCP取值"].split('\n'):
                value[i.split('=')[1]] = i.split('=')[0]

            # print('value=', value)
            input = value[input]
            # print('data=',data)
            json_data[index]["待写入CCP值"] = input

        # 数字名称-值
        elif name_mode == 3 and input_mode == 1:
            index = int(name)
            json_data[index - 1]["待写入CCP值"] = input

        # 数字名称-值描述
        elif name_mode == 3 and input_mode == 2:
            index = int(name)
            # print('index=', index)
            for i in json_data[index - 1]["CCP取值"].split('\n'):
                value[i.split('=')[1]] = i.split('=')[0]
            # print('value=', value)
            input = value[input]
            # print('data=',data)
            json_data[index - 1]["待写入CCP值"] = input

        # 把值修改完之后生成对应的json文件
        js = json.dumps(json_data, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ':'))
        # ccp_json_path = os.path.join(os.path.abspath(__file__).split("sd_tester.py")[0],'..','sdk','data','ccp','ccp.json')
        # jsFile = open(self.ccp_json_path, "w+", encoding='utf-8')
        with open(self.ccp_json_path, "w+", encoding='utf-8') as jsFile:
            jsFile.write(js)
            jsFile.close()

        # 从json文件里面获取ccp数据
        # ccp_json_path = os.path.join(os.path.abspath(__file__).split("sd_tester.py")[0],'..','sdk','data','ccp','ccp.json')
        # file = open(self.ccp_json_path, 'r', encoding='utf-8')

        with open(self.ccp_json_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            json_data = json.loads(file_content)
            ccp_dict = {}
            ccp_list = []
            ccp = ""
            # file.close()

        # 生成CCP数据
        for i in range(1558):
            ccp_dict[i] = json_data[i]["待写入CCP值"]
            ccp_list.append(ccp_dict[i])

        ccp = "".join(ccp_list)

        # 根据ccp原1556个字节计算出最后的两个CRC校验和字节
        if isinstance(ccp[:-4], str):
            data = [int(x, 16) for x in re.findall('\w{2}', ccp[:-4].replace(" ", ""))]
            crctab = [
                0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50A5, 0x60C6, 0x70E7,
                0x8108, 0x9129, 0xA14A, 0xB16B, 0xC18C, 0xD1AD, 0xE1CE, 0xF1EF,
                0x1231, 0x0210, 0x3273, 0x2252, 0x52B5, 0x4294, 0x72F7, 0x62D6,
                0x9339, 0x8318, 0xB37B, 0xA35A, 0xD3BD, 0xC39C, 0xF3FF, 0xE3DE,
                0x2462, 0x3443, 0x0420, 0x1401, 0x64E6, 0x74C7, 0x44A4, 0x5485,
                0xA56A, 0xB54B, 0x8528, 0x9509, 0xE5EE, 0xF5CF, 0xC5AC, 0xD58D,
                0x3653, 0x2672, 0x1611, 0x0630, 0x76D7, 0x66F6, 0x5695, 0x46B4,
                0xB75B, 0xA77A, 0x9719, 0x8738, 0xF7DF, 0xE7FE, 0xD79D, 0xC7BC,
                0x48C4, 0x58E5, 0x6886, 0x78A7, 0x0840, 0x1861, 0x2802, 0x3823,
                0xC9CC, 0xD9ED, 0xE98E, 0xF9AF, 0x8948, 0x9969, 0xA90A, 0xB92B,
                0x5AF5, 0x4AD4, 0x7AB7, 0x6A96, 0x1A71, 0x0A50, 0x3A33, 0x2A12,
                0xDBFD, 0xCBDC, 0xFBBF, 0xEB9E, 0x9B79, 0x8B58, 0xBB3B, 0xAB1A,
                0x6CA6, 0x7C87, 0x4CE4, 0x5CC5, 0x2C22, 0x3C03, 0x0C60, 0x1C41,
                0xEDAE, 0xFD8F, 0xCDEC, 0xDDCD, 0xAD2A, 0xBD0B, 0x8D68, 0x9D49,
                0x7E97, 0x6EB6, 0x5ED5, 0x4EF4, 0x3E13, 0x2E32, 0x1E51, 0x0E70,
                0xFF9F, 0xEFBE, 0xDFDD, 0xCFFC, 0xBF1B, 0xAF3A, 0x9F59, 0x8F78,
                0x9188, 0x81A9, 0xB1CA, 0xA1EB, 0xD10C, 0xC12D, 0xF14E, 0xE16F,
                0x1080, 0x00A1, 0x30C2, 0x20E3, 0x5004, 0x4025, 0x7046, 0x6067,
                0x83B9, 0x9398, 0xA3FB, 0xB3DA, 0xC33D, 0xD31C, 0xE37F, 0xF35E,
                0x02B1, 0x1290, 0x22F3, 0x32D2, 0x4235, 0x5214, 0x6277, 0x7256,
                0xB5EA, 0xA5CB, 0x95A8, 0x8589, 0xF56E, 0xE54F, 0xD52C, 0xC50D,
                0x34E2, 0x24C3, 0x14A0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
                0xA7DB, 0xB7FA, 0x8799, 0x97B8, 0xE75F, 0xF77E, 0xC71D, 0xD73C,
                0x26D3, 0x36F2, 0x0691, 0x16B0, 0x6657, 0x7676, 0x4615, 0x5634,
                0xD94C, 0xC96D, 0xF90E, 0xE92F, 0x99C8, 0x89E9, 0xB98A, 0xA9AB,
                0x5844, 0x4865, 0x7806, 0x6827, 0x18C0, 0x08E1, 0x3882, 0x28A3,
                0xCB7D, 0xDB5C, 0xEB3F, 0xFB1E, 0x8BF9, 0x9BD8, 0xABBB, 0xBB9A,
                0x4A75, 0x5A54, 0x6A37, 0x7A16, 0x0AF1, 0x1AD0, 0x2AB3, 0x3A92,
                0xFD2E, 0xED0F, 0xDD6C, 0xCD4D, 0xBDAA, 0xAD8B, 0x9DE8, 0x8DC9,
                0x7C26, 0x6C07, 0x5C64, 0x4C45, 0x3CA2, 0x2C83, 0x1CE0, 0x0CC1,
                0xEF1F, 0xFF3E, 0xCF5D, 0xDF7C, 0xAF9B, 0xBFBA, 0x8FD9, 0x9FF8,
                0x6E17, 0x7E36, 0x4E55, 0x5E74, 0x2E93, 0x3EB2, 0x0ED1, 0x1EF0
            ]

            crc = 0xFFFF
            for a in data:
                tmp = (crc >> 8) ^ a
                crc = ((crc << 8) ^ crctab[tmp]) & 0xFFFF

            ccp = ccp[:-4] + str(hex(crc)[2:])

            # 返回最后的CCP值
            # print("CRC算出来的len(ccp)=",len(ccp))
            return ccp

    def get_bgm_soft_hard_version(self, **kwargs):
        '''
        读取 bgm的 软件版本号，硬件版本号
        @param kwargs:
        @return: 软件号 （app  boot ），硬件号
        '''
        logger.info("读取 bgm 的软件版本号")
        self.update_serverdoipid(0x1001)
        soft_version = self.get_soft_version()
        if isinstance(soft_version, tuple):
            app_ver = soft_version[0]
            boot_ver = soft_version[1]
        else:
            app_ver = None
            boot_ver = None
        logger.info("读取 bgm 的硬件版本号")
        hard_ver = self.get_hard_version()
        logger.info(f"读取 bgm 软件的 boot版本号为{boot_ver},app 软件版本号为{app_ver},硬件版本号为{hard_ver}")
        self.update_serverdoipid(self.server_doip_id)
        return app_ver, boot_ver, hard_ver

    def get_tcam_soft_hard_version(self, **kwargs):
        '''
        读取 tcam 的 软件版本号，硬件版本号
        @param kwargs:
        @return: 软件号 ，硬件号
        '''

        logger.info("读取 tcam 的软件版本号")
        self.update_serverdoipid(0x1011)
        soft_version = self.get_soft_version()
        logger.info("读取 tcam 的硬件版本号")
        hard_ver = self.get_hard_version()
        logger.info(f"读取 tcam 软件的版本号为{soft_version},硬件版本号为{hard_ver}")
        self.update_serverdoipid(self.server_doip_id)
        return soft_version, hard_ver

    def get_cdc_soft_hard_version(self, **kwargs):
        '''
        读取 cdc 的 软件版本号，硬件版本号
        @param kwargs:
        @return: 软件号 ，硬件号
        '''

        logger.info("读取 cdc 的软件版本号")
        self.update_serverdoipid(0x1201)
        soft_version = self.get_soft_version()
        logger.info("读取 cdc 的硬件版本号")
        hard_ver = self.get_hard_version()
        logger.info(f"读取 cdc 软件的版本号为{soft_version},硬件版本号为{hard_ver}")
        self.update_serverdoipid(self.server_doip_id)
        return soft_version, hard_ver

    def get_acu_soft_hard_version(self, **kwargs):
        '''
        读取 acu 的 软件版本号，硬件版本号
        @param kwargs:
        @return: 软件号 ，硬件号
        '''

        logger.info("读取 acu 的软件版本号")
        self.update_serverdoipid(0x1401)
        soft_version = self.get_soft_version()
        logger.info("读取 acu 的硬件版本号")
        hard_ver = self.get_hard_version()
        logger.info(f"读取 acu 软件的版本号为{soft_version},硬件版本号为{hard_ver}")
        self.update_serverdoipid(self.server_doip_id)
        return soft_version, hard_ver

    def send_request_and_recv_response(self, msg, msg1=None, recv=True, do_assert=True, **kwargs):
        '''
        发送数据可以传递一个字符串，一个是列表，随机组合
        发送数据，是否接收返回值，根据recv 决定，是否直接报错 根据do_assert 决定
        @param msg: 发送的数据，可以是列表[0x10,0x01]，可以是16进制字符串1001/10 01，
         @param msg1: 发送的数据，可以是列表[0x10,0x01]，可以是16进制字符串1001/10 01，
        @param recv: 格式为字符串，列表 布尔 ；对接收的数据是否校验，True 只校验是否为正响应，传入具体的值，则会比较值是否相等
        @param do_assert:
        @param kwargs:
        @return: True/False ，[]
        '''

        if isinstance(msg, list):
            send_data_list = msg
        elif isinstance(msg, str):
            msg = msg.strip().replace(" ", "")
            if len(msg) % 2 != 0:
                string = f"msg 的长度不对，长度应该为偶数"
                logger.error(string)
                assert 0, string
            send_data_list = [int(msg[i:i + 2], 16) for i in range(0, len(msg), 2)]
        else:
            string = f"msg 格式不对，应该为列表或者字符串"
            logger.error(string)
            assert 0, string
        # 判断
        if msg1 is not None:
            if isinstance(msg1, list):
                send_data_list1 = msg1
            elif isinstance(msg1, str):
                msg1 = msg1.strip().replace(" ", "")
                if len(msg1) % 2 != 0:
                    string = f"msg 的长度不对，长度应该为偶数"
                    logger.error(string)
                    assert 0, string
                send_data_list1 = [int(msg1[i:i + 2], 16) for i in range(0, len(msg1), 2)]
            else:
                string = f"msg 格式不对，应该为列表或者字符串"
                logger.error(string)
                assert 0, string
            # 拼接 两个
            send_data_list += send_data_list1
        # 发送报文
        self.send_data(send_data_list)
        # 是否收报文
        if recv:
            err_code = True
            recv_data_list = self.return_udsdata_and_check_and_print_response_result(
                f" 发送{bytes(send_data_list).hex()}")
            if isinstance(recv, list):
                recv_data_string = bytes(recv_data_list).hex().upper()
                check_msg = bytes(recv).hex().upper()
                if check_msg != recv_data_string[:len(check_msg)]:
                    err_code = False
                    if do_assert:
                        string = f"接收的数据不是期望的数据,期望是{check_msg}实际是{recv_data_string}"
                        logger.error(string)
                        assert 0, string
            elif isinstance(recv, str):
                check_msg = recv.strip().replace(" ", "").upper()
                recv_data_string = bytes(recv_data_list).hex().upper()
                if check_msg != recv_data_string[:len(check_msg)]:
                    err_code = False
                    if do_assert:
                        string = f"接收的数据不是期望的数据,期望是{check_msg}实际是{recv_data_string}"
                        logger.error(string)
                        assert 0, string
            else:
                # 只校验是不是正响应
                send_servic_id = send_data_list[0]
                recv_servic_id = send_servic_id + 0x40
                if recv_data_list[0] != recv_servic_id:
                    err_code = False
                    if do_assert:
                        string = f"接收的数据是负响应"
                        logger.error(string)
                        assert 0, string
            return err_code, recv_data_list
        return True, None


if __name__ == "__main__":
    # work dir: ecu_simulator
    # cmd: python3 ecu_sim/sd_tester.py

    from xat_ecu.legacy.sdk.ecu_simulator_app import Ecu_Sim_App
    from xat_ecu.legacy.sdk.get_obd_ip import get_announcement_ip

    # 获取配置
    tc_path = str(CONFIG_DIR_PATH.joinpath("bncm_whitelist_test_config.yaml"))
    tccfg = ParseTBConfig(tc_path)
    tc_config = tccfg.yaml_content
    logger.info("tc_config: {}".format(tc_config))
    logger.info("=================================================================")

    # 获取 obd ip
    obdip = get_announcement_ip()
    tc_config["gateway_ip"] = obdip
    # mock BNCM
    # ecu_sims = Ecu_Sim_App(**tc_config)
    # ecu_sims.all_ecu_start()

    # 启动诊断仪
    sd_test = Sd_Tester(**tc_config)
    sd_test.diagnostic_client_sim_start()
    logger.info("==================== SdTester started ==========================")
    sd_test.tester_present()

    ccp = sd_test.make_ccp_according_id_and_data('车型', '01')
    print("CCP 1-1 的值=", ccp)

    # ccp = sd_test.make_ccp_according_id_and_data('车型','V542 V90')
    # print("CCP 1-2 的值=",ccp)

    # ccp = sd_test.make_ccp_according_id_and_data('VEHICLE TYPE','03')
    # print("CCP 2-1 的值=",ccp)

    # ccp = sd_test.make_ccp_according_id_and_data('VEHICLE TYPE','V526 XC90')
    # print("CCP 2-2 的值=",ccp)

    # ccp = sd_test.make_ccp_according_id_and_data("1",'05')
    # print("CCP 3-1 的值=",ccp)

    # ccp = sd_test.make_ccp_according_id_and_data('1','V541 S90')
    # print("CCP 3-2 的值=",ccp)

    sd_test.write_ccp(ccp)

    sleep(5)

    # # 请求白名单
    # result1 = sd_test.request_bluetoothkey_whitelist()
    # logger.info(result1)
    # sleep(5)

    # result2 = sd_test.request_entitykey_whitelist()
    # logger.info(result2)
    # sleep(5)

    # 关闭诊断仪
    try:
        sd_test.stop_tester_present()
        sleep(0.5)
        sd_test.diagnostic_client_sim_close()
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/ecu_sim/sd_tester.py")
        logger.info(
            "==================== SdTester Stopped Error =========================="
        )
        logger.error(e)
    # ecu_sims.all_ecu_close()  # mock BNCM
