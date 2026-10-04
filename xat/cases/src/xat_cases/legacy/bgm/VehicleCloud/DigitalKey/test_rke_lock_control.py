#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_peps_approach.py
@Time         :2022/11/24 17:13:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass import *


@allure.feature("互联服务") 
@allure.story("数字钥匙和账号/RKE/蓝牙解闭锁")
class TestDigitalKeyRkeLockControl(TestDigitalKey):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        logger.info("------------------>复位BGM")
        self.nucapp.bgm_power_off()
        time.sleep(2)
        self.nucapp.bgm_power_on()
        time.sleep(15)
        logger.info("------------------>复位BGM结束")
    
    def after_class(self, ecu):
        super().after_class(self, ecu)
    
    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu)
        sleep(5)
    
    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    

    @allure.title("RKE闭锁_UsageModeFail_CONVENIENCE+DrvrSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112180(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_present()
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 1, "UsageModeFail", exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("RKE闭锁_UsageModeFail_ACTIVE+DrvrSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112173?projectId=46')
    @pytest.mark.sanity
    @pytest.mark.v140only
    def test_caseid_112173(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0xB)
        self.dk.set_drvr_seat_present()
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 1, "UsageModeFail", exec_type=3)
        self.dk.ck_cenlock_sts(0x1)


    @allure.title("RKE闭锁_Success_CONVENIENCE+DrvrSeat_not_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112154?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112154(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(3)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_lock()
        self.dk.ck_cenlock_sts(0x3, 0x1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("RKE闭锁_Success_ACTIVE+DrvrSeat_not_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112152?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112152(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0xB)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(3)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_lock()
        self.dk.ck_cenlock_sts(0x3, 0x1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)


    @allure.title("RKE闭锁_DelayFail_INACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112198?projectId=46')
    @pytest.mark.full
    def test_caseid_112198(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x1)
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(0x3, 0x1)
        sleep(1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("RKE闭锁_DelayFail_CONVENIENCE+DrvrSeat_not_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112148?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112148(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(3)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(0x3, 0x1)
        sleep(1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("RKE闭锁_DelayFail_CONVENIENCE+DrvrSeat_not_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112188?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112188(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(3)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(0x3, 0x1)
        sleep(1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    # @allure.title("RKE闭锁_DelayFail_ACTIVE+DrvrSeat_not_occupied")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359647?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1359647(self):
    #     self.dk.set_cenlock_sts(0x1)
    #     self.set_usage_mode(0xB)
    #     self.dk.set_drvr_seat_notpresent()
    #     time.sleep(4)
    #     self.dk.empty_dk_data_queue()
    #     self.dk.send_rke_lock()
    #     time.sleep(0.5)
    #     self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
    #     self.dk.ck_four_door_lock_cmd(2)
    #     self.dk.set_four_door_unlock()
    #     sleep(1)
    #     self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)
    #     self.dk.ck_cenlock_sts(0x3, 0x1)

    @allure.title("RKE闭锁_DelayFail_ABANDONED")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112182?projectId=46')
    @pytest.mark.full
    def test_caseid_112182(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x0)
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(0x3, 0x1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    
    @allure.title("解锁_ReqFail_ ABANDONED")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112165?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112165(self):
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0x0)
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(0x1, 0x1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("RKE闭锁_BUSY_闭锁指令执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112157?projectId=46')
    @pytest.mark.full
    def test_caseid_112157(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x1)
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.send_rke_lock(slot_index=2)
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_rke_resp(1, 1, "SysBusy", exec_type=3, slot_index=2)

    @allure.title("RKE闭锁_BUSY_解锁指令执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112193?projectId=46')
    @pytest.mark.full
    def test_caseid_112193(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.send_rke_lock(slot_index=2)
        time.sleep(1)
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_rke_resp(1, 1, "SysBusy", exec_type=3, slot_index=2)

    @allure.title("RKE解锁_UsageModeFail_CONVENIENCE+DrvrSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112145?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112145(self):
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_present()
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.ck_rke_resp(1, 1, 'UsageModeFail',exec_type=3)
        self.dk.ck_cenlock_sts(0x3)

    @allure.title("RKE解锁_UsageModeFail_ACTIVE+DrvrSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112155?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112155(self):
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0xB)
        self.dk.set_drvr_seat_present()
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.ck_rke_resp(1, 1, 'UsageModeFail',exec_type=3)
        self.dk.ck_cenlock_sts(0x3)


    @allure.title("RKE解锁_Success_CONVENIENCE+DrvrSeat_not_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112191?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112191(self):
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(0x1, 0x1)
        sleep(1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("RKE解锁_Success_ ACTIVE+DrvrSeat_not_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112136?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112136(self):
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0x11)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(0x1, 0x1)
        sleep(1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("RKE解锁_DelayFail_INACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112167?projectId=46')
    @pytest.mark.full
    def test_caseid_112167(self):
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0x1)
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_lock()
        self.dk.ck_cenlock_sts(0x1, 0x1)
        sleep(1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("RKE解锁_DelayFail_CONVENIENCE+DrvrSeat_not_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112174?projectId=46')
    @pytest.mark.full
    def test_caseid_112174(self):
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0x2)
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_lock()
        self.dk.ck_cenlock_sts(0x1, 0x1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("RKE解锁_DelayFail_ACTIVE+DrvrSeat_not_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112172?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112172(self):
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0xB)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_lock()
        self.dk.ck_cenlock_sts(0x1, 0x1)
        sleep(1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    # @allure.title("RKE解锁_DelayFail_ABANDONED")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359630?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1359630(self):
    #     self.dk.set_cenlock_sts(0x3)
    #     self.set_usage_mode(0xB)
    #     self.dk.set_drvr_seat_notpresent()
    #     time.sleep(1)
    #     self.dk.send_rke_unlock()
    #     self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
    #     self.dk.ck_four_door_lock_cmd(1)
    #     self.dk.set_four_door_lock()
    #     self.dk.ck_cenlock_sts(0x1, 0x1)
    #     sleep(1)
    #     self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("RKE解锁_BUSY_闭锁指令执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112163?projectId=46')
    @pytest.mark.full
    def test_caseid_112163(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x1)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.send_rke_unlock(slot_index=2)
        sleep(0.4)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_rke_resp(1, 1, "SysBusy", exec_type=3, slot_index=2)
        self.dk.set_four_door_lock()
        self.dk.ck_cenlock_sts(0x3, 0x1)
        sleep(1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("RKE解锁_BUSY_解锁指令执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112187?projectId=46')
    @pytest.mark.full
    def test_caseid_112187(self):
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0x0)
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.send_rke_unlock(slot_index=2)
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_rke_resp(1, 1, "SysBusy", exec_type=3, slot_index=2)
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_lock()
        self.dk.ck_cenlock_sts(0x1, 0x1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("联动关门_BUSY_联动关门指令执行中下发解锁指令")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112160?projectId=46')
    @pytest.mark.full
    def test_caseid_1987291(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x1)
        time.sleep(3)
        self.dk.send_rke_lock()
        self.dk.send_rke_lock(slot_index=2)
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_rke_resp(1, 1, "SysBusy", exec_type=3, slot_index=2)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_lock()
        self.dk.ck_cenlock_sts(0x3, 0x1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("RKE联动关门_UsageModeFail_CONVENIENCE+DrvrSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112158?projectId=46')
    @pytest.mark.sanity
    @pytest.mark.v140only
    def test_caseid_112158(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0xD)
        self.dk.set_drvr_seat_present()
        time.sleep(1)
        self.dk.send_rke_close_door_and_lock()
        self.dk.ck_rke_resp(1, 1, 'UsageModeFail',exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("RKE联动关门_UsageModeFail_ACTIVE+DrvrSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112179?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112179(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0xB)
        self.dk.set_drvr_seat_present()
        time.sleep(1)
        self.dk.send_rke_close_door_and_lock()
        self.dk.ck_rke_resp(1, 1, 'UsageModeFail',exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("联动关门_ReqFail_ INACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112146?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112146(self):
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0x1)
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(0x1, 0x1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("RKE联动关门_Success_CONVENIENCE+DrvrSeat_not_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112156?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112156(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_notpresent()
        self.dk.set_door_sts([0, 0, 1, 0, 0])
        self.dk.set_door_opener_sts(1, 1, 5, 1, 1)
        time.sleep(3)
        self.dk.send_rke_close_door_and_lock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(3, 2, 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        time.sleep(0.5)
        # curr_usage_mode = self.doip.read_did(0xDD0A)[0]
        # assert 0x1 == curr_usage_mode, f"usage mode未下切至INACTIVE，当前为{curr_usage_mode}"
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_lock()
        sleep(1)
        self.dk.ck_cenlock_sts(0x3, 0x1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("RKE联动关门_Success_ACTIVE+DrvrSeat_not_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112183?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112183(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0xB)
        self.dk.set_drvr_seat_notpresent()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        time.sleep(3)  # todo: 等待为了5s超时自动退诊断会话，usage mode下切
        self.dk.send_rke_close_door_and_lock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(5, 2, 0)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        # curr_usage_mode = self.doip.read_did(0xDD0A)[0]
        # assert 0x1 == curr_usage_mode, f"usage mode未下切至INACTIVE，当前为{curr_usage_mode}"
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_lock()
        sleep(1)
        self.dk.ck_cenlock_sts(0x3, 0x1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("RKE联动关门_DelayFail_INACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987326?projectId=46')
    @pytest.mark.full
    def test_caseid_1987326(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x1)
        time.sleep(1)
        self.dk.send_rke_close_door_and_lock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(0x3, 0x1)
        sleep(1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("RKE联动关门_DelayFail_CONVENIENCE+DrvrSeat_not_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112162?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112162(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(3)
        self.dk.send_rke_close_door_and_lock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(0x3, 0x1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("RKE联动关门_DelayFail_ACTIVE+DrvrSeat_not_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112170?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112170(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0xB)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(3)
        self.dk.send_rke_close_door_and_lock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(0x3, 0x1)
        sleep(1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("RKE联动关门_DelayFail_ABANDONED")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112153?projectId=46')
    @pytest.mark.full
    def test_caseid_112153(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x0)
        time.sleep(1)
        self.dk.send_rke_close_door_and_lock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(0x3, 0x1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)


    @allure.title("RKE联动关门_BUSY_闭锁指令执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112138?projectId=46')
    @pytest.mark.full
    def test_caseid_112138(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x1)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.send_rke_close_door_and_lock(slot_index=2)
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_rke_resp(1, 1, "SysBusy", exec_type=3, slot_index=2)

    @allure.title("RKE联动关门_BUSY_解锁指令执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112177?projectId=46')
    @pytest.mark.full
    def test_caseid_112177(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x0)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.send_rke_close_door_and_lock(slot_index=2)
        time.sleep(1)
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_rke_resp(1, 1, "SysBusy", exec_type=3, slot_index=2)

    @allure.title("RKE联动关门_BUSY_联动关门指令执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112189?projectId=46')
    @pytest.mark.full
    def test_caseid_112189(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x1)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(1)
        self.dk.send_rke_close_door_and_lock()
        self.dk.send_rke_close_door_and_lock(slot_index=2)
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_rke_resp(1, 1, "SysBusy", exec_type=3, slot_index=2)

    # @allure.title("RKE闭锁_关窗指令执行中")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1360151?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1360151(self):
    #     self.dk.set_window_position(0x1A, 0x1A, 0x1A, 0x1A)
    #     self.dk.set_cenlock_sts(0x1)
    #     self.set_usage_mode(0x0)
    #     time.sleep(1)
    #     self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
    #     self.dk.send_rke_window_control(0, 0, 0, 0)
    #     self.dk.ck_window_opener_req(0x1, 0x1, 0x1, 0x1)
    #     self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
    #     self.dk.send_rke_lock(slot_index=2)
    #     self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2, slot_index=2)
    #     self.dk.ck_four_door_lock_cmd(2)
    #     self.dk.set_four_door_lock()
    #     self.dk.ck_rke_resp(1, 0, "Success", exec_type=3, slot_index=2)
    #     self.dk.ck_cenlock_sts(0x3, 0x1)
    #     self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
    #     self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("RKE解锁_UsageModeFail_ACTIVE+RowSecMidSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111810?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111810(self):
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0xB)
        self.dk.set_secmid_seat_present()
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.ck_rke_resp(1, 1, 'UsageModeFail',exec_type=3)
        self.dk.ck_cenlock_sts(0x3)

    @allure.title("RKE闭锁_UsageModeFail_ACTIVE+RowSecRiSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111809?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111809(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0xB)
        self.dk.set_secri_seat_present()
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 1, "UsageModeFail", exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("RKE联动关门_UsageModeFail_ACTIVE+PassSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111808?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111808(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0xB)
        self.dk.set_pass_seat_present()
        time.sleep(1)
        self.dk.send_rke_close_door_and_lock()
        self.dk.ck_rke_resp(1, 1, 'UsageModeFail',exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("RKE闭锁_UsageModeFail_ACTIVE+PassSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111807?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111807(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0xB)
        self.dk.set_pass_seat_present()
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 1, "UsageModeFail", exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("RKE闭锁_UsageModeFail_ACTIVE+RowSecMidSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111806?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111806(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0xB)
        self.dk.set_secmid_seat_present()
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 1, "UsageModeFail", exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("RKE联动关门_UsageModeFail_CONVENIENCE+RowSecRiSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111805?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111805(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x2)
        self.dk.set_secri_seat_present()
        time.sleep(1)
        self.dk.send_rke_close_door_and_lock()
        self.dk.ck_rke_resp(1, 1, 'UsageModeFail',exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("RKE解锁_UsageModeFail_CONVENIENCE+RowSecRiSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111804?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111804(self):
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0x2)
        self.dk.set_secri_seat_present()
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.ck_rke_resp(1, 1, 'UsageModeFail',exec_type=3)
        self.dk.ck_cenlock_sts(0x3)

    @allure.title("RKE联动关门_UsageModeFail_CONVENIENCE+RowSecLeSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111803?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111803(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x2)
        self.dk.set_secle_seat_present()
        time.sleep(1)
        self.dk.send_rke_close_door_and_lock()
        self.dk.ck_rke_resp(1, 1, 'UsageModeFail',exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("RKE解锁_UsageModeFail_ACTIVE+RowSecLeSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111802?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111802(self):
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0xB)
        self.dk.set_secle_seat_present()
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.ck_rke_resp(1, 1, 'UsageModeFail',exec_type=3)
        self.dk.ck_cenlock_sts(0x3)

    @allure.title("RKE解锁_UsageModeFail_ACTIVE+PassSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111801?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111801(self):
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0xB)
        self.dk.set_pass_seat_present()
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.ck_rke_resp(1, 1, 'UsageModeFail',exec_type=3)
        self.dk.ck_cenlock_sts(0x3)

    @allure.title("RKE联动关门_UsageModeFail_ACTIVE+RowSecRiSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111800?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111800(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0xB)
        self.dk.set_secri_seat_present()
        time.sleep(1)
        self.dk.send_rke_close_door_and_lock()
        self.dk.ck_rke_resp(1, 1, 'UsageModeFail',exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("RKE联动关门_UsageModeFail_ACTIVE+RowSecLeSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111799?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111799(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0xB)
        self.dk.set_secle_seat_present()
        time.sleep(1)
        self.dk.send_rke_close_door_and_lock()
        self.dk.ck_rke_resp(1, 1, 'UsageModeFail',exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    

    @allure.title("RKE联动关门_UsageModeFail_CONVENIENCE+RowSecMidSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111797?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111797(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x2)
        self.dk.set_secmid_seat_present()
        time.sleep(1)
        self.dk.send_rke_close_door_and_lock()
        self.dk.ck_rke_resp(1, 1, 'UsageModeFail',exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("RKE闭锁_UsageModeFail_ACTIVE+RowSecLeSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111796?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111796(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0xB)
        self.dk.set_secle_seat_present()
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 1, "UsageModeFail", exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("RKE解锁_UsageModeFail_ACTIVE+RowSecRiSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111795?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111795(self):
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0xB)
        self.dk.set_secri_seat_present()
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.ck_rke_resp(1, 1, 'UsageModeFail',exec_type=3)
        self.dk.ck_cenlock_sts(0x3)

    

    @allure.title("RKE闭锁_UsageModeFail_CONVENIENCE+RowSecRiSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111793?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111793(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x2)
        self.dk.set_secri_seat_present()
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 1, "UsageModeFail", exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("RKE联动关门_UsageModeFail_CONVENIENCE+PassSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111792?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111792(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x2)
        self.dk.set_pass_seat_present()
        time.sleep(1)
        self.dk.send_rke_close_door_and_lock()
        self.dk.ck_rke_resp(1, 1, 'UsageModeFail',exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("RKE闭锁_UsageModeFail_CONVENIENCE+RowSecLeSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111791?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111791(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x2)
        self.dk.set_secle_seat_present()
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 1, "UsageModeFail", exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("RKE闭锁_UsageModeFail_CONVENIENCE+RowSecMidSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111790?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111790(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x2)
        self.dk.set_secmid_seat_present()
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 1, "UsageModeFail", exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("RKE解锁_UsageModeFail_CONVENIENCE+RowSecMidSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111789?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111789(self):
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0x2)
        self.dk.set_secmid_seat_present()
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.ck_rke_resp(1, 1, 'UsageModeFail',exec_type=3)
        self.dk.ck_cenlock_sts(0x3)

    @allure.title("RKE闭锁_UsageModeFail_CONVENIENCE+PassSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111788?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111788(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0xB)
        self.dk.set_pass_seat_present()
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 1, "UsageModeFail", exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("RKE闭锁_UsageModeFail_DRIVING+左前门开")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112195?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112195(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0xD)
        self.dk.set_pass_seat_present()
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 1, "UsageModeFail", exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("RKE联动关门_UsageModeFail_ACTIVE+RowSecMidSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111787?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111787(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0xB)
        self.dk.set_secmid_seat_present()
        time.sleep(1)
        self.dk.send_rke_close_door_and_lock()
        self.dk.ck_rke_resp(1, 1, 'UsageModeFail',exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    
    @allure.title("掉电之后RKE解闭锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112297?projectId=46')
    @pytest.mark.full
    def test_caseid_1987546(self):
        logger.info("------------------>复位BGM")
        self.nucapp.bgm_power_off()
        time.sleep(2)
        self.nucapp.bgm_power_on()
        time.sleep(15)
        logger.info("------------------>复位BGM结束")
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(3)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_lock()
        self.dk.ck_cenlock_sts(0x3, 0x1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("联动关门_BUSY_闭锁指令执行中执行闭锁")
    @pytest.mark.full
    def test_caseid_1987296(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x1)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.send_rke_close_door_and_lock(slot_index=2)
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_rke_resp(1, 1, "SysBusy", exec_type=3, slot_index=2)

    @allure.title("联动关门_BUSY_闭锁指令执行中执行解锁")
    @pytest.mark.full
    def test_caseid_1987295(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x1)
        time.sleep(3)
        self.dk.send_rke_lock()
        self.dk.send_rke_lock(slot_index=2)
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_rke_resp(1, 1, "SysBusy", exec_type=3, slot_index=2)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_lock()
        self.dk.ck_cenlock_sts(0x3, 0x1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("联动关门_BUSY_解锁指令执行中执行闭锁")
    @pytest.mark.full
    def test_caseid_1987294(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x0)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.send_rke_close_door_and_lock(slot_index=2)
        time.sleep(1)
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_rke_resp(1, 1, "SysBusy", exec_type=3, slot_index=2)

    @allure.title("联动关门_BUSY_解锁指令执行中执行解锁")
    @pytest.mark.full
    def test_caseid_1987293(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x1)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.send_rke_close_door_and_lock(slot_index=2)
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_rke_resp(1, 1, "SysBusy", exec_type=3, slot_index=2)

    @allure.title("联动关门_BUSY_联动关门指令执行中执行闭锁")
    @pytest.mark.full
    def test_caseid_1987292(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x1)
        time.sleep(3)
        self.dk.send_rke_lock()
        self.dk.send_rke_lock(slot_index=2)
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_rke_resp(1, 1, "SysBusy", exec_type=3, slot_index=2)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_lock()
        self.dk.ck_cenlock_sts(0x3, 0x1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("闭锁_BUSY_联动关门指令执行中")
    @pytest.mark.full
    def test_caseid_112194(self):
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0x1)
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_lock()
        self.dk.send_rke_lock(slot_index=2)
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_rke_resp(1, 1, "SysBusy", exec_type=3, slot_index=2)

    @allure.title("解锁_BUSY_联动关门指令执行中")
    @pytest.mark.full
    def test_caseid_112160(self):
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0x0)
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.send_rke_unlock(slot_index=2)
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_rke_resp(1, 1, "SysBusy", exec_type=3, slot_index=2)
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_lock()
        self.dk.ck_cenlock_sts(0x1, 0x1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)