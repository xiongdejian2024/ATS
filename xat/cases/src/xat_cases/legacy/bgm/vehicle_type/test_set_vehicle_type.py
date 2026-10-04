# -*- coding:utf-8 -*-
"""
@File        :test_window_ctrl.py
@Author      :hui.zhao@jiduatuo.com
@Time        :2023/08/16 11:00 AM
@Description :Test body control test case about window
"""

import os
import sys
from time import sleep
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
sys.path.append(os.path.join(os.getcwd(), "../../../.."))

from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester

ccp_file_Mars1 = "Mars1_CCP.txt"
ccp_file_Venus_gernal = "Venus_CCP_P1P3.txt"         #标准续航版P1P3_智驾开
ccp_file_Mars1_performance = "Venus_CCP_P2.txt"      #性能版P2_智驾开


@allure.feature("车型设置")
@allure.story("车型设置")
# @pytest.mark.smoke
# @pytest.mark.checklist
# @pytest.mark.full
# @pytest.mark.run(order=1)
class TestExample(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.veh_type_ccp = ecu.get("veh_type")
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.sd_tester.diagnostic_client_sim_start()
        with allure.step("Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟(数据库周期性报文和调度表)
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动,总线开始收发报文
        
        self.sd_tester.tester_present()
        sleep(0.5)
        self.sd_tester.update_serverdoipid(0x1002)
        sleep(0.5)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # raise RuntimeError("前置处理错误")  # case 和 后置就不会run了

        # Code Location

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)

    def after_class(self, ecu):
        self.ipdu.time_control_stop()  # 停止数据模拟(数据库周期性报文和调度表)
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动,总线开始收发报文
        sleep(0.5)
        self.sd_tester.stop_tester_present()
        sleep(0.5)
        self.sd_tester.diagnostic_client_sim_close()
        super().after_class(self, ecu)

    def read_ccp_content(self, file_name):
        current_file_path = os.path.realpath(__file__)
        pos = current_file_path.rfind(r'/')
        file_ccp = current_file_path[: pos + 1] + file_name
        logger.info("车辆CCP配置文件是:{}".format(file_ccp))
        file_obj = open(file_ccp, mode='r')
        file_content = file_obj.readlines()
        return file_content[0]

    @allure.title("通过CCP配置车型")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1502340?projectId=46',
        name='Fota Case Example 1502340',
    )
    # @pytest.mark.smoke
    # @pytest.mark.full
    # @pytest.mark.run(order=1)
    @pytest.mark.write
    def test_set_vehicle_type_caseid_000000001(self):
        vehicletype = self.veh_type_ccp
        if vehicletype == "mars1":
            ccp_file = ccp_file_Mars1
        elif vehicletype == "venus_p1_p3":
            ccp_file = ccp_file_Venus_gernal
        elif vehicletype == "venus_p2":
            ccp_file = ccp_file_Mars1_performance
        else:
            ccp_file = ccp_file_Mars1
            logger.error(
                "设置的车型参数不正确，或者没有指定车型.设置为默认车型:Mars1"
            )

        ccp_data = self.read_ccp_content(ccp_file)
        sleep(0.5)
        self.sd_tester.write_ccp(ccp_data)
        sleep(5)
        self.bgm_power_off_and_on()
        sleep(15)

        # ccp_read_result = self.sd_tester.read_ccp()
        self.sd_tester.information_check_f106()
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
            "发送 22F106 读取ccp"
        )
        ret_data = bytes(result).hex()[6:]
        logger.info("获取的CCP配置为:{}".format(ret_data))
        if ccp_data.upper() == ret_data.upper():
            logger.info("设置车型为{}成功".format(vehicletype))
            assert True
        else:
            logger.info("设置车型为{}失败".format(vehicletype))
            assert False

    @pytest.mark.read
    def test_set_vehicle_type_caseid_000000002(self):
        ccp_file_content_Mars1 = self.read_ccp_content(ccp_file_Mars1)
        ccp_file_content_Venus_P1_P3 = self.read_ccp_content(ccp_file_Venus_gernal)
        ccp_file_content__Venus_P2 = self.read_ccp_content(ccp_file_Mars1_performance)
        sleep(1)
        self.sd_tester.information_check_f106()
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
            "发送 22F106 读取ccp"
        )
        ret_data = bytes(result).hex()[6:]
        logger.info("获取的CCP配置为:{}".format(ret_data))
        if ccp_file_content_Mars1.upper() == ret_data.upper():
            logger.info("-------------------------> 当前车型为:Mars1")
            assert True
        elif ccp_file_content_Venus_P1_P3.upper() == ret_data.upper():
            logger.info("------------------------->当前车型为:Venus标准续航版P1+P3+智驾开")
            assert True
        elif ccp_file_content__Venus_P2.upper() == ret_data.upper():
            logger.info("------------------------->当前车型为:Venus性能版P2+智驾开")
            assert True
        else:
            logger.error("------------------------->车型未知")
            assert False