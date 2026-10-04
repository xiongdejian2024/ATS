#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_nfc_learning_abc.py
@Time         :2023/1/31 17:54:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import os
import sys

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ""))
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))

from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass_abc import *
from xat_ecu.api.abc_interface import *


@allure.feature("互联服务")
@allure.story("数字钥匙和账号/其他/白名单控制")
class TestDigitalKeyWhiteListConTrol(TestDigitalKeyBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)
    
    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu)
        self.bus_comm.dk.empty_dk_data_queue()
        sleep(2)
    
    def after_each_func(self, ecu):
        """每个测试用例后置步骤"""
        super().after_each_func(ecu)
        sleep(10)


    @allure.title("SOC主动同步白名单_Inactive>Driving")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111962?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111962(self):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_singal("connectivitycanfd","BncmConnectivityFr20", 'EntityKeyWhiteListVers', 0x0000000000000063)
        self.bus_comm.set_singal("connectivitycanfd","BncmConnectivityFr20", 'BLESlotKeyWhiteListVers', 0x0000000000000064)
        sleep(5)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        # sleep(5)
        # self.tsp.check_digital_key_result(func="WhiteListSync",keys=[self.tc_config.get('vid'),"SlotSyncReportUpLinkReq", "LastSyncTimeForBLE" , "LastSyncTimeForEntityKey"],target_value={"LastSyncTimeForBLE":100,"LastSyncTimeForEntityKey":99})
        assert self.tsp.check_digital_key_result_log(),f'SOC主动同步白名单失败'

    @allure.title("SOC主动同步白名单_Inactive>Convenience")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111972?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111972(self):
        entity_ver = 0x010203040506070F
        ble_ver = 0x000000000000000F
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_singal("connectivitycanfd","BncmConnectivityFr20", 'EntityKeyWhiteListVers', entity_ver)
        self.bus_comm.set_singal("connectivitycanfd","BncmConnectivityFr20", 'BLESlotKeyWhiteListVers', ble_ver)
        sleep(5)
        self.sd_tester.change_usage_mode(UsageMode.CONVENIENCE)
        target = [f"LastSyncTimeForBLE:{ble_ver}"]+[f"LastSyncTimeForEntityKey:{entity_ver}"]
        # sleep(5)
        # self.tsp.check_digital_key_result(func="WhiteListSync",keys=[self.tc_config.get('vid'),"SlotSyncReportUpLinkReq", "LastSyncTimeForBLE" , "LastSyncTimeForEntityKey"],target_value={"LastSyncTimeForBLE":int(ble_ver),"LastSyncTimeForEntityKey":int(entity_ver)})
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'


    @allure.title("SOC主动同步白名单_Inactive>Active")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111955?projectId=46')
    @pytest.mark.sanity
    def test_caseid_111955(self):
        entity_ver = 0xFFFFFFFFFFFFFFFF
        ble_ver = 0xFFFFFFFFFFFFFFFF
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_singal("connectivitycanfd","BncmConnectivityFr20", 'EntityKeyWhiteListVers', entity_ver)
        self.bus_comm.set_singal("connectivitycanfd","BncmConnectivityFr20", 'BLESlotKeyWhiteListVers', ble_ver)
        sleep(5)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        target = [f"LastSyncTimeForBLE:{ble_ver}"]+[f"LastSyncTimeForEntityKey:{entity_ver}"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # sleep(5)
        # self.tsp.check_digital_key_result(func="WhiteListSync",keys=[self.tc_config.get('vid'),"SlotSyncReportUpLinkReq", "LastSyncTimeForBLE" , "LastSyncTimeForEntityKey"],target_value={"LastSyncTimeForBLE":int(ble_ver),"LastSyncTimeForEntityKey":int(entity_ver)})

    @allure.title("SOC主动同步白名单_Abandoned>Driving")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111961?projectId=46')
    @pytest.mark.sanity
    def test_caseid_111961(self):
        entity_ver = 0x2122232425262728
        ble_ver = 0x000000000000000A
        self.sd_tester.change_usage_mode(UsageMode.ABANDONED)
        self.bus_comm.set_singal("connectivitycanfd","BncmConnectivityFr20", 'EntityKeyWhiteListVers', entity_ver)
        self.bus_comm.set_singal("connectivitycanfd","BncmConnectivityFr20", 'BLESlotKeyWhiteListVers', ble_ver)
        sleep(5)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        target = [f"LastSyncTimeForBLE:{ble_ver}"]+[f"LastSyncTimeForEntityKey:{entity_ver}"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # sleep(5)
        # self.tsp.check_digital_key_result(func="WhiteListSync",keys=[self.tc_config.get('vid'),"SlotSyncReportUpLinkReq", "LastSyncTimeForBLE" , "LastSyncTimeForEntityKey"],target_value={"LastSyncTimeForBLE":int(ble_ver),"LastSyncTimeForEntityKey":int(entity_ver)})


    @allure.title("SOC主动同步白名单_Abandoned>Convenience")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111953?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111953(self):
        entity_ver = 0x0102030405060708
        ble_ver = 0x0000000000000002
        self.sd_tester.change_usage_mode(UsageMode.ABANDONED)
        self.bus_comm.set_singal("connectivitycanfd","BncmConnectivityFr20", 'EntityKeyWhiteListVers', entity_ver)
        self.bus_comm.set_singal("connectivitycanfd","BncmConnectivityFr20", 'BLESlotKeyWhiteListVers', ble_ver)
        sleep(5)
        self.sd_tester.change_usage_mode(UsageMode.CONVENIENCE)
        target = [f"LastSyncTimeForBLE:{ble_ver}"]+[f"LastSyncTimeForEntityKey:{entity_ver}"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # sleep(5)
        # self.tsp.check_digital_key_result(func="WhiteListSync",keys=[self.tc_config.get('vid'),"SlotSyncReportUpLinkReq", "LastSyncTimeForBLE" , "LastSyncTimeForEntityKey"],target_value={"LastSyncTimeForBLE":int(ble_ver),"LastSyncTimeForEntityKey":int(entity_ver)})


    @allure.title("SOC主动同步白名单_Abandoned>Active")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111969?projectId=46')
    @pytest.mark.full
    def test_caseid_111969(self):
        entity_ver = 0x1112131415161718
        ble_ver = 0x0000000000000005
        self.sd_tester.change_usage_mode(UsageMode.ABANDONED)
        self.bus_comm.set_singal("connectivitycanfd","BncmConnectivityFr20", 'EntityKeyWhiteListVers', entity_ver)
        self.bus_comm.set_singal("connectivitycanfd","BncmConnectivityFr20", 'BLESlotKeyWhiteListVers', ble_ver)
        sleep(5)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        target = [f"LastSyncTimeForBLE:{ble_ver}"]+[f"LastSyncTimeForEntityKey:{entity_ver}"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # sleep(5)
        # self.tsp.check_digital_key_result(func="WhiteListSync",keys=[self.tc_config.get('vid'),"SlotSyncReportUpLinkReq", "LastSyncTimeForBLE" , "LastSyncTimeForEntityKey"],target_value={"LastSyncTimeForBLE":int(ble_ver),"LastSyncTimeForEntityKey":int(entity_ver)})


    # @allure.title("更新Slot白名单_更新失败")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111973?projectId=46')
    # @pytest.mark.full  # pass
    # def test_caseid_111973(self):
    #     self.bus_comm.dk.auto_ack_tsp_ble_sync_cmd = False
    #     self.create_bluetooth_digital_key()
    #     sleep(1)
    #     self.bus_comm.dk.ck_white_list_update_req(2, [key_id0])
    #     self.bus_comm.dk.send_while_list_update_resp(0x12, 0x01, self.dk.last_sync_time_ble - 1)
    #     # todo: 云端查看日志err = 1; errMsg = ""; last_sync_time=T1-1，V1.0会更新errMsg详细定义