# -*- coding: utf-8 -*-
"""
@File        : test_example_can_lin_fr.py
@Author      : shulin.yang@jiduatuo.com
@Time        : 2023/01/10 18:00 PM
@Description : description about this file
@Examples    : example of how to use it
"""

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
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu


@allure.feature("网络管理")
@allure.story("网络PNC路由测试")
class TestExample(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # Code Location

    def after_each_func(self, ecu):
        # Code Location
        sleep(10)
        super().after_each_func(ecu)

    def after_class(self, ecu):
        # Code Location
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        super().after_class(self, ecu)

    @allure.title("BodyexposedCANFD 路由测试")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/111781?projectId=46",
        name="Can_Lin Pdu Case Example 111781",
    )
    @pytest.mark.smoke
    @pytest.mark.verify
    def test_bodyexposedcanfd_caseid_111781(self):
        with allure.step(f"Test Step 1 发送 can_lin_fr 报文"):
            sleep(2)
        msg = [0x31, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        msg1 = [0x2A, 0x50, 0xFF, 0x7F, 0xF7, 0x02, 0x00, 0x00]
        self.ipdu.send_pdu("bodyexposedcanfd", 0x531, msg, cycle_time=1)
        sleep(3)
        t = time.time()
        flag = False
        while time.time() - t < 10:
            rec_data = self.ipdu.recv_pdu("bodyexposedcanfd", 0x52A)
            logger.info("rec_data is {}".format(rec_data))
            if rec_data:
                msg_id = rec_data[0]
                time_stamp = rec_data[1]
                msg_length = rec_data[2]
                pdu_data = rec_data[3]
                if msg1 == pdu_data:
                    flag = True
                    logger.info(f" ")
                    break
        assert flag
        sleep(3)

    @allure.title("adcanfd 路由测试")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/112771?projectId=46",
        name="Can_Lin Pdu Case Example 112771",
    )
    @pytest.mark.smoke
    def test_adcanfd_caseid_112771(self):
        with allure.step(f"Test Step 1 发送 can_lin_fr 报文"):
            sleep(2)
        msg = [0x02, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        msg1 = [0x01, 0x50, 0x44, 0x7D, 0xA4, 0x00, 0x00, 0x00]
        self.ipdu.send_pdu("adcanfd", 0x502, msg, cycle_time=1)
        sleep(3)
        t = time.time()
        flag = False
        while time.time() - t < 10:
            rec_data = self.ipdu.recv_pdu("adcanfd", 0x501)
            logger.info("rec_data is {}".format(rec_data))
            if rec_data:
                msg_id = rec_data[0]
                time_stamp = rec_data[1]
                msg_length = rec_data[2]
                pdu_data = rec_data[3]
                if msg1 == pdu_data:
                    flag = True
                    logger.info(f" ")
                    break
        assert flag
        sleep(3)

    @allure.title("passivesafetycan 路由测试")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/112768?projectId=46",
        name="Can_Lin Pdu Case Example 112768",
    )
    @pytest.mark.smoke
    def test_passivesafetycan_caseid_112768(self):
        with allure.step(f"Test Step 1 发送 can_lin_fr 报文"):
            sleep(2)
        msg = [0x0E, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        msg1 = [0x01, 0x50, 0xFF, 0x7F, 0xF3, 0x00, 0x00, 0x00]
        self.ipdu.send_pdu("passivesafetycan", 0x50E, msg, cycle_time=1)
        sleep(3)
        t = time.time()
        flag = False
        while time.time() - t < 10:
            rec_data = self.ipdu.recv_pdu("passivesafetycan", 0x501)
            logger.info("rec_data is {}".format(rec_data))
            if rec_data:
                msg_id = rec_data[0]
                time_stamp = rec_data[1]
                msg_length = rec_data[2]
                pdu_data = rec_data[3]
                if msg1 == pdu_data:
                    flag = True
                    logger.info(f" ")
                    break
        assert flag
        sleep(3)

    # @allure.title("propulsioncan 路由测试")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/111775?projectId=46",
    #     name="Can_Lin Pdu Case Example 111775",
    # )
    # @pytest.mark.smoke
    # def test_propulsioncan_caseid_111775(self):
    #     with allure.step(f"Test Step 1 发送 can_lin_fr 报文"):
    #         sleep(2)
    #     msg = [0x26, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    #     msg1 = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    #     self.ipdu.send_pdu("propulsioncan", 0x526, msg, cycle_time=1)
    #     sleep(3)
    #     t = time.time()
    #     flag = False
    #     while time.time() - t < 10:
    #         rec_data = self.ipdu.recv_pdu("propulsioncan", 0x501)
    #         logger.info("rec_data is {}".format(rec_data))
    #         if rec_data:
    #             msg_id = rec_data[0]
    #             time_stamp = rec_data[1]
    #             msg_length = rec_data[2]
    #             pdu_data = rec_data[3]
    #             if msg1 == pdu_data:
    #                 flag = True
    #                 logger.info(f" ")
    #                 break
    #     assert flag
    #     sleep(3)

    @allure.title("bodycan 路由测试")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/112769?projectId=46",
        name="Can_Lin Pdu Case Example 112769",
    )
    @pytest.mark.smoke
    def test_bodycan_caseid_112769(self):
        with allure.step(f"Test Step 1 发送 can_lin_fr 报文"):
            sleep(2)
        msg = [0x26, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        msg1 = [0x01, 0x50, 0xFF, 0xFF, 0xFF, 0x02, 0x00, 0x00]
        self.ipdu.send_pdu("bodycan", 0x502, msg, cycle_time=1)
        sleep(3)
        t = time.time()
        flag = False
        while time.time() - t < 10:
            rec_data = self.ipdu.recv_pdu("bodycan", 0x501)
            logger.info("rec_data is {}".format(rec_data))
            if rec_data:
                msg_id = rec_data[0]
                time_stamp = rec_data[1]
                msg_length = rec_data[2]
                pdu_data = rec_data[3]
                if msg1 == pdu_data:
                    flag = True
                    logger.info(f" ")
                    break
        assert flag
        sleep(3)

    @allure.title("bodycan 路由测试")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/112749?projectId=46",
        name="Can_Lin Pdu Case Example 112749",
    )
    @pytest.mark.smoke_1
    @pytest.mark.sanity
    def test_bodycan_caseid_112749(self):
        with allure.step(f"Test Step 1 发送 can_lin_fr 报文"):
            sleep(2)
        msg = [0x26, 0x40, 0x00, 0x00, 0x00, 0x02, 0x00, 0x02]
        msg1 = [0x01, 0x50, 0xFF, 0xFF, 0xFF, 0x02, 0x00, 0x00]
        self.ipdu.send_pdu("bodycan", 0x502, msg, cycle_time=1)
        sleep(3)
        t = time.time()
        flag = False
        while time.time() - t < 10:
            rec_data = self.ipdu.recv_pdu("bodycan", 0x501)
            logger.info("rec_data is {}".format(rec_data))
            if rec_data:
                msg_id = rec_data[0]
                time_stamp = rec_data[1]
                msg_length = rec_data[2]
                pdu_data = rec_data[3]
                if msg1 == pdu_data:
                    flag = True
                    logger.info(f" ")
                    break
        assert flag
        sleep(3)

    @allure.title("infocanfd 路由测试")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/112772?projectId=46",
        name="Can_Lin Pdu Case Example 112772",
    )
    @pytest.mark.smoke
    def test_infocanfd_caseid_112772(self):
        with allure.step(f"Test Step 1 发送 can_lin_fr 报文"):
            sleep(2)
        msg = [0x26, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        msg1 = [0x01, 0x50, 0xFF, 0xFF, 0xF7, 0x02, 0x00, 0x00]
        self.ipdu.send_pdu("infocanfd", 0x502, msg, cycle_time=1)
        sleep(3)
        t = time.time()
        flag = False
        while time.time() - t < 10:
            rec_data = self.ipdu.recv_pdu("infocanfd", 0x501)
            logger.info("rec_data is {}".format(rec_data))
            if rec_data:
                msg_id = rec_data[0]
                time_stamp = rec_data[1]
                msg_length = rec_data[2]
                pdu_data = rec_data[3]
                if msg1 == pdu_data:
                    flag = True
                    logger.info(f" ")
                    break
        assert flag
        sleep(3)

    @allure.title("connectivity 路由测试")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/115477?projectId=46",
        name="Can_Lin Pdu Case Example 115477",
    )
    @pytest.mark.smoke
    def test_connectivity_caseid_115477(self):
        with allure.step(f"Test Step 1 发送 can_lin_fr 报文"):
            sleep(2)
        msg = [0x09, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        msg1 = [0x33, 0x50, 0xFF, 0xFF, 0xFF, 0x03, 0x00, 0x00]
        self.ipdu.send_pdu("connectivitycanfd", 0x509, msg, cycle_time=1)
        sleep(3)
        t = time.time()
        flag = False
        while time.time() - t < 10:
            rec_data = self.ipdu.recv_pdu("connectivitycanfd", 0x533)
            logger.info("rec_data is {}".format(rec_data))
            if rec_data:
                msg_id = rec_data[0]
                time_stamp = rec_data[1]
                msg_length = rec_data[2]
                pdu_data = rec_data[3]
                if msg1 == pdu_data:
                    flag = True
                    logger.info(f" ")
                    break
        assert flag
        sleep(3)

    @allure.title("chassiscan1 路由测试")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/111777?projectId=46",
        name="Can_Lin Pdu Case Example 111777",
    )
    @pytest.mark.smoke
    def test_chassiscan1_caseid_111777(self):
        with allure.step(f"Test Step 1 发送 can_lin_fr 报文"):
            sleep(2)
        msg = [0x21, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        msg1 = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.ipdu.send_pdu("chassiscan1", 0x521, msg, cycle_time=1)
        sleep(3)
        t = time.time()
        flag = False
        while time.time() - t < 10:
            # rec_data = self.ipdu.recv_pdu("chassiscan1", 0x501)
            msgs = self.ipdu.check_bus_recv_message("chassiscan1")
            if msgs:
                flag = True
                logger.info(f" ")
                break
            continue

            logger.info("rec_data is {}".format(rec_data))
            if rec_data:
                msg_id = rec_data[0]
                time_stamp = rec_data[1]
                msg_length = rec_data[2]
                pdu_data = rec_data[3]
                if msg1 == pdu_data:
                    flag = True
                    logger.info(f" ")
                    break
        assert flag
        sleep(3)

    # @allure.title("chassiscan2 路由测试")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/111776?projectId=46",
    #     name="Can_Lin Pdu Case Example 111776",
    # )
    # @pytest.mark.smoke
    # def test_chassiscan2_caseid_111776(self):
    #     with allure.step(f"Test Step 1 发送 can_lin_fr 报文"):
    #         sleep(2)
    #     msg = [0x22, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    #     msg1 = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    #     self.ipdu.send_pdu("chassiscan2", 0x522, msg, cycle_time=1)
    #     sleep(3)
    #     t = time.time()
    #     flag = False
    #     while time.time() - t < 10:
    #         rec_data = self.ipdu.recv_pdu("chassiscan2", 0x501)
    #         logger.info("rec_data is {}".format(rec_data))
    #         if rec_data:
    #             msg_id = rec_data[0]
    #             time_stamp = rec_data[1]
    #             msg_length = rec_data[2]
    #             pdu_data = rec_data[3]
    #             if msg1 == pdu_data:
    #                 flag = True
    #                 logger.info(f" ")
    #                 break
    #     assert flag
    #     sleep(3)
