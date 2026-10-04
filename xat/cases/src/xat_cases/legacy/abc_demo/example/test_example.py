#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : test_basetechdemo.py
@time         : 2023/11/23 14:19
@author       : quan.sun@jiduauto.com
@description  : 
'''

import os
import sys
import time

import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("Demon")
@allure.story("example Demo")
class TestExampleAbstract(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        logger.info("before_class")

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("before_each_func")

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu):
        super().after_class(self, ecu)
        logger.info("after_class")

    @allure.title("写 ccp mars1")
    def test_caseid_01(self):
        self.sd_tester.write_ccp({950: 0x1})  # mars1

    @allure.title("写 ccp")
    def test_caseid_011(self):
        self.sd_tester.write_ccp({950: 0x2})  # venus

    @allure.title("切换到Abandoned")
    def test_caseid_100000(self):
        self.bus_comm.set('backbonefr', 'BcmVddmBackBoneFr00', 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.sd_tester.change_usage_mode(UsageMode.ABANDONED)
        time.sleep(60)

    @allure.title("切换到Inactive")
    def test_caseid_100001(self):
        self.bus_comm.set('backbonefr', 'BcmVddmBackBoneFr00', 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        time.sleep(60)

    @allure.title("切换到Convenience")
    def test_caseid_100002(self):
        self.bus_comm.set('backbonefr', 'BcmVddmBackBoneFr00', 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.sd_tester.change_usage_mode(UsageMode.CONVENIENCE)
        time.sleep(60)

    @allure.title("切换到Active")
    def test_caseid_100003(self):
        self.bus_comm.set('backbonefr', 'BcmVddmBackBoneFr00', 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        time.sleep(60)

    @allure.title("切换到Driving")
    def test_caseid_100004(self):
        self.bus_comm.set('backbonefr', 'BcmVddmBackBoneFr00', 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        time.sleep(60)

    # @allure.title("读取 ccp")
    # @pytest.mark.parametrize('value_list')
    # def test_caseid_100005(self, value_list):
    #     r1, r2 = self.sd_tester.read_ccp()
    #     for i in value_list:
    #         logger.info(f"读取第：{i}个字节值是：{r2[i - 1]}")
    #
    # @allure.title("写入 ccp")
    # @pytest.mark.parametrize('value_dict')
    # def test_caseid_100006(self, value_dict):
    #     r1, r2 = self.sd_tester.write_ccp(value_dict)
    #     assert r1

    @allure.title("测试 get_lin_scheduleTable 是否 ok")
    def test_caseid_02(self):
        lin_scheduleTable = self.bus_comm.get_lin_scheduleTable("cem_lin1")
        logger.info(f"lin_scheduleTable:{lin_scheduleTable}")

    @allure.title("测试ecu doip mock")
    def test_caseid_03(self):
        # 此case需要使用专门的tccfg  --tccfg=config/local_diag_config.yaml    
        # pytest 也需辅以  --disable_env=true
        self.diag_mock.update_0x22_data(ecu_name="ACU", did="F1AE", data_info_update=[0xFF, 0xFF, 0x00, 0xFF])
        self.diag_mock.update_0x22_data(ecu_name="ACU", did="F1AA", data_info_update=[0xFF, 0xFF, 0x00, 0xFF])
        self.diag_mock.update_0x22_data(ecu_name="ACU", did="F101", data_info_update={"NRC": 0x11})
        self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={
            "0206": {1: [0x10, 0x01], 2: [0x10, 0x01], 3: {"NRC": 0x11}}})
        self.sd_tester.update_serverdoipid(0x1401, ecu="ACU")
        self.sd_tester.send_data([0x22, 0xF1, 0xAE])
        sleep(1)
        self.sd_tester.send_data([0x22, 0xF1, 0xAA])
        sleep(1)
        self.sd_tester.send_data([0x22, 0xF1, 0x01])
        sleep(1)
        self.sd_tester.send_data([0x31, 0x01, 0x02, 0x06, 0xFF])
        sleep(1)
        self.sd_tester.send_data([0x31, 0x03, 0x02, 0x06, 0xFF])
        sleep(5)

    @allure.title("测试ecu docan mock")
    def test_caseid_04(self):
        # 此case需要使用专门的tccfg   --tccfg=config/diag_docan_config.yaml   
        # pytest 也需辅以  --disable_env=true  
        self.diag_mock.update_0x22_data(ecu_name="BNCM", did="F1AE", data_info_update=[0xFF, 0xFF, 0x00, 0xFF])
        self.diag_mock.update_0x22_data(ecu_name="BNCM", did="F1AA", data_info_update=[0xFF, 0xFF, 0x00, 0xFF])
        self.diag_mock.update_0x22_data(ecu_name="BNCM", did="F101", data_info_update={"NRC": 0x11})
        self.diag_mock.update_0x31_data(ecu_name="BNCM", routine_control_data={
            "0206": {1: [0x10, 0x01], 2: [0x10, 0x01], 3: {"NRC": 0x11}}})
        self.sd_tester.update_serverdoipid(0x1023, ecu="BNCM")
        self.sd_tester.send_data([0x22, 0xF1, 0xAE])
        sleep(1)
        self.sd_tester.send_data([0x22, 0xF1, 0xAA])
        sleep(1)
        self.sd_tester.send_data([0x22, 0xF1, 0x01])
        sleep(1)
        self.sd_tester.send_data([0x31, 0x01, 0x02, 0x06, 0xFF])
        sleep(1)
        self.sd_tester.send_data([0x31, 0x03, 0x02, 0x06, 0xFF])
        sleep(5)

    @allure.title("测试ecu mock send_candata")
    def test_caseid_05(self):
        # 此case需要使用专门的tccfg   --tccfg=config/diag_docan_config.yaml   
        # pytest 也需辅以  --disable_env=true  

        self.diag_mock.update_0x22_data(ecu_name="BNCM", did="F101", data_info_update={"NRC": 0x78})
        self.sd_tester.update_serverdoipid(0x1023, ecu="BNCM")

        self.sd_tester.send_data([0x22, 0xF1, 0x01])
        sleep(1)
        self.diag_mock.send_candata(bus_name="connectivitycanfd", ecu_name="BNCM", res_ecu_canid=0x623,
                                    data=[0x04, 0x62, 0xF1, 0x01, 0xFF, 0x00, 0x00, 0x00])
        sleep(5)

    @allure.title("测试")
    def test_caseid_06(self):
        sleep(1)
        self.bus_comm.set(bus_name="backbonefr", msg_name="VddmBackboneNmFr01", signal_name="HvBattCellUInfoU2",
                          sig_value_name=2)
        sleep(5)

    @allure.title("测试ecu doip mock")
    def test_caseid_07(self):
        # 此case需要使用专门的tccfg  --tccfg=config/local_diag_config.yaml
        # pytest 也需辅以  --disable_env=true
        self.diag_mock.update_0x10_data(ecu_name="ACU",
                                        session_mode={0x01: [0x01, 0x02, 0x03, 0x04], 0x02: [0x05, 0x06, 0x07, 0x8],
                                                      0x03: {"NRC": 0x11}})
        # self.diag_mock.update_0x10_data(ecu_name="ACU", session_mode={"NRC": 0x11})
        self.diag_mock.update_0x11_data(ecu_name="ACU", reset_type={0x01: [], 0x03: {"NRC": 0x11}})
        self.diag_mock.update_0x36_data(ecu_name="ACU", block_sequence_counter_nrc_config={2: 0x78, 18: 0x11})

        # 37服务不需要设置其他参数会自动响应77，但可以模拟否定响应
        self.diag_mock.update_0x37_data(ecu_name="ACU", data={"NRC": 0x11})
        # 27设置的返回服务带seed，表示需要模拟回复的种子数据，如下是模拟27第一次请求后67服务回复的010203种子
        self.diag_mock.update_0x27_data(ecu_name="ACU",
                                        data_info={0x01: [0x01, 0x02, 0x03], 0x02: [], 0x03: {"NRC": 0x11}})

        # length_format_identifier高4位表示max_number_of_block_length数组中一共有多少字节
        # max_number_of_block_length中每一个字节表示每次传入请求中包含的最大字节数
        self.diag_mock.update_0x34_data(ecu_name="ACU", data=[0x20, 0x20, 0x20])
        self.sd_tester.update_serverdoipid(0x1401, ecu="ACU")
        self.sd_tester.send_data([0x10, 0x01])
        sleep(1)
        self.sd_tester.send_data([0x11, 0x02])
        sleep(1)
        self.sd_tester.send_data([0x27, 0x62])
        sleep(1)
        self.sd_tester.send_data([0x34, 0x11, 0x11, 0x1, 0x1])
        sleep(1)
        self.sd_tester.send_data([0x36, 0x02, 0x3, 0x4])
        sleep(1)
        self.sd_tester.send_data([0x37, 0x02])

    @allure.title("测试 BrkPedlPsd_UB设置无效")
    def test_caseid_08(self):
        logger.info("======================开始===================")
        sleep(4)
        self.bus_comm.set(bus_name="backbonefr", msg_name="BcmVddmBackBoneFr00", signal_name="BrkPedlPsdQf",
                          sig_value_name=1, ub_flag=False)
        logger.info("======================结束===================")
        sleep(20)

    @allure.title("测试 lin 暂停和启动")
    def test_caseid_09(self):
        logger.info("======================暂停===================")
        self.bus_comm.pause_bus_send("cem_lin4")
        sleep(10)
        self.bus_comm.resume_bus_send("cem_lin4")
        logger.info("======================恢复===================")
        sleep(5)

    @allure.title("测试 Tx check")
    def test_caseid_10(self):
        logger.info("======================开始发送 fr===================")
        self.bus_comm.set(bus_name="backbonefr", msg_name="BcmVddmBackBoneFr00", signal_name="BrkPedlPsdQf",
                          sig_value_name=1)
        logger.info("======================开始check fr===================")
        self.bus_comm.check(bus_name="backbonefr", msg_name="BcmVddmBackBoneFr00", signal_name="BrkPedlPsdQf",
                            sig_value_name=1)

        logger.info("======================开始发送 can===================")
        self.bus_comm.set(bus_name="connectivitycanfd", msg_name="BncmConnectivityFr17",
                          signal_name="UsgModChgReqFromBLE", sig_value_name=1)
        logger.info("======================开始check can===================")
        self.bus_comm.check(bus_name="connectivitycanfd", msg_name="BncmConnectivityFr17",
                            signal_name="UsgModChgReqFromBLE", sig_value_name=1)

        logger.info("======================开始发送 lin===================")
        self.bus_comm.set(bus_name="cem_lin2", msg_name="AIILLCem_Lin2Fr01", signal_name="StsOfLedLeftAIILY1",
                          sig_value_name=0)
        logger.info("======================开始check lin===================")
        self.bus_comm.check(bus_name="cem_lin2", msg_name="AIILLCem_Lin2Fr01", signal_name="StsOfLedLeftAIILY1",
                            sig_value_name=0)

        logger.info("===============check结束==========================")
        sleep(20)
        logger.info("==================end=======================")

    @allure.title("测试 释放cpu")
    def test_caseid_11(self):
        self.bus_comm.pause_cycle_tx_rx_d()
        logger.info("======================  释放 cpu  ===================")
        sleep(30)
        self.bus_comm.resume_cycle_tx_rx_d()
        logger.info("======================  释放 cpu  ===================")
        sleep(30)

    @allure.title("测试mock不存在的ecu")
    def test_caseid_100(self):
        self.diag_mock.update_0x22_data(ecu_name="BNCM1", did="F101", data_info_update={"NRC": 0x78})
        self.sd_tester.update_serverdoipid(0x1023, ecu="BNCM1")
        self.sd_tester.send_data([0x22, 0xF1, 0x01])
        sleep(5)

    @allure.title("测试mock正常的ecu")
    def test_caseid_101(self):
        self.diag_mock.update_0x22_data(ecu_name="BNCM", did="F101", data_info_update={"NRC": 0x78})
        self.sd_tester.update_serverdoipid(0x1023, ecu="BNCM")
        self.sd_tester.send_data([0x22, 0xF1, 0x01])
        sleep(5)

    @allure.title("测试mock回复ecu数据的类型错误")
    def test_caseid_102(self):
        self.diag_mock.update_0x22_data(ecu_name="BNCM", did="F101", data_info_update={"NRC": [0x78]})
        self.sd_tester.update_serverdoipid(0x1023, ecu="BNCM")
        self.sd_tester.send_data([0x22, 0xF1, 0x01])
        sleep(5)

    def write_vin(self, vin_str):
        """写入vin码"""
        self.sd_tester.sd_tester.enter_extended_session()
        self.sd_tester.sd_tester.return_udsdata_and_check_and_print_response_result("Send 1003 to get result")
        self.sd_tester.sd_tester.security_access_level_l3()
        self.sd_tester.sd_tester.write_vin(vin_str)
        self.sd_tester.sd_tester.return_udsdata_and_check_and_print_response_result("Send 2EF190 to get result")
        return list(bytes(vin_str, encoding="ascii"))

    @allure.title("测试mock写VIN码")
    def test_caseid_103(self):
        self.sd_tester.update_serverdoipid(0x1002)
        self.tc_vin_list = self.write_vin(self.tc_config['vin'])
        sleep(5)

    @allure.title("测试mock写vid码")
    def test_caseid_104(self):
        yaml_vid = self.tc_config['vid']
        # self.sd_tester = SdTest(**self.tc_config)
        # self.sd_tester.start_sd_tester()
        # time.sleep(1)
        self.sd_tester.write_did_and_check(TA.BGM_SOC, 0xb163, SESSION.EXTENDED, UnLock.L7, yaml_vid,
                                           '62b163' + yaml_vid, check_method=Check_Method.reset,
                                           recover=False)
        logger.info(f"已经恢复台架VID为：{yaml_vid}")

    @allure.title("测试mock关于Lin的调度表")
    def test_caseid_105(self):
        time.sleep(5)
        # 检查cem_lin1路上，Cem_Lin1Schedule01_CEM_LIN1的调度表的第一个信号的位置为:0;名字为:CemCem_Lin1Fr01;message_id:61;长度为8;周期为：0.015秒
        self.bus_comm.check_lin_schedule_table("cem_lin1", "$.Cem_Lin1Schedule01_CEM_LIN1[0][0]", 0)
        self.bus_comm.check_lin_schedule_table("cem_lin1", "$.Cem_Lin1Schedule01_CEM_LIN1[0][1]", "CemCem_Lin1Fr01")
        self.bus_comm.check_lin_schedule_table("cem_lin1", "$.Cem_Lin1Schedule01_CEM_LIN1[0][2]", 61)
        self.bus_comm.check_lin_schedule_table("cem_lin1", "$.Cem_Lin1Schedule01_CEM_LIN1[0][3]", 8)
        self.bus_comm.check_lin_schedule_table("cem_lin1", "$.Cem_Lin1Schedule01_CEM_LIN1[0][4]", 0.015)

        # 检查cem_lin1路上，Cem_Lin1Schedule01_CEM_LIN1的调度表的第二个信号的位置为:1;名字为:CemCem_Lin1Fr01;message_id:61;长度为8;周期为：0.015秒
        self.bus_comm.check_lin_schedule_table("cem_lin1", "$.Cem_Lin1Schedule01_CEM_LIN1[1][0]", 1)
        self.bus_comm.check_lin_schedule_table("cem_lin1", "$.Cem_Lin1Schedule01_CEM_LIN1[1][1]", "CemCem_Lin1Fr01")
        self.bus_comm.check_lin_schedule_table("cem_lin1", "$.Cem_Lin1Schedule01_CEM_LIN1[1][2]", 61)
        self.bus_comm.check_lin_schedule_table("cem_lin1", "$.Cem_Lin1Schedule01_CEM_LIN1[1][3]", 8)
        self.bus_comm.check_lin_schedule_table("cem_lin1", "$.Cem_Lin1Schedule01_CEM_LIN1[1][4]", 0.015)

        # 检查cem_lin1路上，Cem_Lin1Schedule01_CEM_LIN1的调度表的第三个信号的位置为:1;名字为:CemCem_Lin1Fr01;message_id:61;长度为8;周期为：0.015秒
        self.bus_comm.check_lin_schedule_table("cem_lin1", "$.Cem_Lin1Schedule01_CEM_LIN1[2][0]", 1)
        self.bus_comm.check_lin_schedule_table("cem_lin1", "$.Cem_Lin1Schedule01_CEM_LIN1[2][1]", "CemCem_Lin1Fr01")
        self.bus_comm.check_lin_schedule_table("cem_lin1", "$.Cem_Lin1Schedule01_CEM_LIN1[2][2]", 61)
        self.bus_comm.check_lin_schedule_table("cem_lin1", "$.Cem_Lin1Schedule01_CEM_LIN1[2][3]", 8)
        self.bus_comm.check_lin_schedule_table("cem_lin1", "$.Cem_Lin1Schedule01_CEM_LIN1[2][4]", 0.015)

    @allure.title("测试mock关于Lin的调度表new")
    def test_caseid_106(self):
        lin_scheduleTable = self.bus_comm.get_lin_scheduleTable("cem_lin6")
        logger.info(f"lin_scheduleTable:{lin_scheduleTable}")
        self.bus_comm.bus_app.check_lin_schedule_table("cem_lin1", "Cem_Lin6Schedule01_CEM_LIN6")
