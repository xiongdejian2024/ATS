# -*- coding: utf-8 -*-
"""
@File        : test_example_can_lin_fr.py
@Author      : quan.sun@jiduatuo.com
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


@allure.feature("Example Cases")
@allure.story("Test Example can lin fr Set")
class TestExample(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # Code Location
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

    @allure.title("Format test can lin example")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196965?projectId=46',
        name='Can_Lin Case Example 1196965',
    )
    @pytest.mark.example_lin
    def test_format_example_can_lin_caseid_1196965(self):
        '''
        Test related example, Show the format
        '''
        with allure.step(f"Test Step 1 can_lin_fr 设置信号"):
            sleep(2)
            # can
            self.ipdu.bodycan_ppodbodyfr01_doorpassopenreqoutdswt2_psdnotpsd3_psd()
            self.ipdu.set(
                self.ipdu.bodycan.PpodBodyFr01,
                'DoorPassOpenReqOutdSwt2',
                'PsdNotPsd3_Psd',
            )
            self.ipdu.bodycan_rldmbodyvfcvectorfr_vfcvectorrldmblockid_value(1)

            # lin 0x20
            self.ipdu.cem_lin6_awmcem_lin6fr01_actvresplrintfltactrflt2_flt_fault()

        with allure.step(f"Test Step 2 can_lin_fr 检查信号"):
            # can
            sleep(2)
            result, realvalue, expectedvalue = self.ipdu.check(
                self.ipdu.bodycan.CemBodyFr121, 'InteCleanUnpleSmell', 'OnOff1_Off'
            )  # 0x114
            logger.info(
                "result {}, realvalue {}, expectedvalue {}".format(
                    result, realvalue, expectedvalue
                )
            )

            # lin
            # sleep(2)
            # result, realvalue, expectedvalue = self.ipdu.check(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrIntFltActrFlt2', 1)  # 0x20
            # logger.info("result {}, realvalue {}, expectedvalue {}".format(result, realvalue, expectedvalue))

        result = True

        assert result

    @allure.title("Format test can lin pdu example")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196965?projectId=46',
        name='Can_Lin Pdu Case Example 1196965',
    )
    @pytest.mark.example2
    def test_format_example_can_lin_pdu_caseid_1196965(self):
        '''
        Test related example, Show the format
        '''
        with allure.step(f"Test Step 1 发送 can_lin_fr 报文"):
            sleep(2)
            # # can
            self.ipdu.send_pdu(
                "bodycan",
                0x53F,
                [0x3F, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
                cycle_time=1,
            )

            self.ipdu.send_pdu(
                "bodycan", 0x125, [0x00, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
            )

            self.ipdu.preheat_msg(
                "connectivitycanfd", "BncmConnectivityFr07"
            )  # 非周期函数提前预热(发送一次的msg)
            sleep(2)
            self.ipdu.send_pdu("connectivitycanfd", 0x166, [0x01] * 64)  # 发送
            sleep(0.1)
            self.ipdu.remove_preheating(
                "connectivitycanfd", "BncmConnectivityFr07"
            )  # 解除预热

        with allure.step(f"Test Step 2 接收 can_lin_fr 报文"):
            # can
            sleep(2)

            # 阻塞型
            self.ipdu.rx_flag_reset_bus("bodycan")
            rec_data = self.ipdu.recv_pdu("bodycan", 0x114)
            logger.info("rec_data is {}".format(rec_data))

            # rec_data = self.ipdu.recv_pdu("connectivitycanfd", 0x260)
            # logger.info("rec_data is {}".format(rec_data))

            # 起线程
            self.ipdu.rx_flag_reset_bus("connectivitycanfd")
            self.ipdu.recv_pdu_thread_start("connectivitycanfd", 0x260, self.func)
            self.ipdu.recv_pdu_thread_all_stop()

        result = True

        assert result

    @allure.title("Format test can crc example")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196965?projectId=46',
        name='Can_Lin crc Case Example 1196965',
    )
    @pytest.mark.example2
    def test_format_example_can_crc_caseid_1196965(self):
        '''
        Test related example, Show the format
        '''
        with allure.step(f"Test Step 1 can_lin_fr 设置信号"):
            sleep(2)
            # can   某一正常的CRC [0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC9, 0x81, 0xFF, 0x28, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
            self.ipdu.send_pdu(
                "connectivitycanfd",
                0xF0,
                [
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0xC9,
                    0x81,
                    0xFF,
                    0x28,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                ],
            )

            sleep(10)

        result = True

        assert result

    def func(self, data):
        logger.info("rec_data is {}".format(data))

    @allure.title("Format test fr example")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1502340?projectId=46',
        name='Can_Lin Pdu Case Example 1502340',
    )
    @pytest.mark.examplefr
    def test_format_example_fr_caseid_1502340(self):
        '''
        Test related example, Show the format
        '''

        sleep(10)

        self.ipdu.backbonefr_srsbackbonefr04_passseatsts_0_srsbackbonesignalipdu04_passseatsts1_occptlrg()

        sleep(10)
        self.ipdu.backbonefr_srsbackbonefr04_passseatsts_0_srsbackbonesignalipdu04_passseatsts1_fmale()
        # self.busapp.stop_all_cyclic_msgs()
        # logger.info(
        #     "-------------------------------------------------------------------"
        # )
        sleep(10)

        result = True

        assert result

    @allure.title("check event example")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1502340?projectId=46',
        name='Can_Lin Pdu Case Example 1502340',
    )
    @pytest.mark.examplece
    def test_check_event_caseid_1502340(self):
        '''
        Test related example, check_event
        '''
        self.ipdu.reset_check_event_results()  # 确保无之前获取的数据记录

        self.ipdu.check_event_thread_start(
            self.ipdu.bodycan.CemBodyFr03, "ActvnOfIndcrIndcrOutCntr", 1, 2, timeout=20
        )

        # action

        event_time = self.ipdu.check_event_thread_stop(
            "ActvnOfIndcrIndcrOutCntr", timeout=20
        )  # timeout与上面 一致

        logger.info("事件发生次数为  {}".format(event_time))
        result = event_time

        assert result

    @allure.title("Format test can lin pause")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1502340?projectId=46',
        name='can lin pause Case Example 1502340',
    )
    @pytest.mark.lin_pause
    def test_can_lin_pause_caseid_1502340(self):
        '''
        Test related example, Show the format
        '''

        sleep(10)

        self.ipdu.pause_all_bus_send()
        logger.info("===========   暂停 can lin  send    ==============")

        sleep(10)

        logger.info("===========    恢复 can lin  send     ==============")
        self.ipdu.resume_all_bus_send()
        sleep(10)

        result = True

        assert result

    @allure.title("Format test fr pause")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1502340?projectId=46',
        name='can lin pause Case Example 1502340',
    )
    @pytest.mark.fr_pause
    def test_fr_pause_caseid_1502340(self):
        '''
        Test related example, Show the format
        '''

        sleep(10)

        self.ipdu.pause_bus_send("backbonefr")
        logger.info("===========   暂停 fr  send    ==============")

        sleep(10)

        logger.info("===========    恢复 fr  send     ==============")
        self.ipdu.resume_bus_send("backbonefr")
        sleep(10)

        result = True

        assert result

    # @allure.title("Format test fr pause")
    # @allure.testcase(
    #     'https://jama.jiduauto.com/perspective.req#/testCases/1502340?projectId=46',
    #     name='fr pause Case Example 1502340',
    # )
    # @pytest.mark.fr_pause
    # def test_fr_pause_caseid_1502340(self):
    #     '''
    #     Test related example, Show the format
    #     '''

    #     sleep(10)
    #     self.busapp.bus_dict["backbonefr"].stop_flexray()
    #     logger.info("===========   暂停 FR    ==============")

    #     sleep(10)

    #     logger.info("===========    恢复 FR    ==============")
    #     self.busapp.bus_dict["backbonefr"].start_flexray()
    #     sleep(10)

    #     result = True

    #     assert result
