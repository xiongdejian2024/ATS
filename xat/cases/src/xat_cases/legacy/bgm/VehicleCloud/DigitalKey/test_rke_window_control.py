#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_rke_window_control.py
@Time         :2022/11/28 17:21:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import os
import sys
import allure
import time

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ""))
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass import *

PRECHECKTI = 0.15


@allure.feature("互联服务")
@allure.story("数字钥匙和账号/RKE/蓝牙车窗控制")
class TestDigitalKeyRkeWindowControl(TestDigitalKey):

    @allure.title("车窗控制_UsageModeFail_DRIVING")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359627?projectId=46')
    @pytest.mark.full
    def test_caseid_112168(self):
        time.sleep(10)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        self.set_usage_mode(0xD)
        time.sleep(1)
        self.dk.send_rke_window_control(100, 100, 100, 100)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 1, "UsageModeFail",exec_type=3)

    @allure.title("车窗控制_UsageModeFail_CONVENIENCE+DrvrSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112166?projectId=46')
    @pytest.mark.sanity 
    @pytest.mark.v140only 
    def test_caseid_112166(self):
        time.sleep(10)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        self.set_usage_mode(0xB)
        # self.dk.empty_dk_data_queue()
        self.dk.set_drvr_seat_present()
        time.sleep(1)
        self.dk.send_rke_window_control(20, 30, 40, 50)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(3, 1, "UsageModeFail",exec_type=3)

    @allure.title("车窗控制_UsageModeFail_ACTIVE+DrvrSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112184?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112184(self):
        time.sleep(10)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        self.set_usage_mode(0xB)
        self.dk.set_drvr_seat_present()
        time.sleep(1)
        self.dk.send_rke_window_control(50, 30, 50, 50)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(3, 1, "UsageModeFail",exec_type=3,timeout=7)

    @allure.title("车窗控制_DelayFail_ABANDONED")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112144?projectId=46')
    @pytest.mark.full
    def test_caseid_112144(self):
        self.set_usage_mode(0x1)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        self.dk.set_drvr_seat_present()
        time.sleep(1)
        self.dk.send_rke_window_control(100, 100, 100, 96)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.ck_window_opener_req(0x1A, 0x1A, 0x1A, 0x19)
        time.sleep(10)
        self.dk.ck_rke_resp(2, 1, "DelayFail",exec_type=3)


    @allure.title("车窗控制_DelayFail_INACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112169?projectId=46')
    @pytest.mark.full
    def test_caseid_112169(self):
        self.set_usage_mode(0x1)
        self.dk.set_window_position(0xA, 0xB, 0xC, 0xD)
        self.dk.set_drvr_seat_present()  # todo: inactive下主驾占座会寻钥匙
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_window_control(20, 20, 20, 20)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.ck_window_opener_req(0x6, 0x6, 0x6, 0x6)
        time.sleep(10)
        self.dk.ck_rke_resp(2, 1, "DelayFail",exec_type=3)

    @allure.title("车窗控制_DelayFail_CONVENIENCE+DrvrSeat_not_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112147?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_112147(self):
        time.sleep(10)
        self.dk.set_window_position(0x1A, 0x1A, 0x1A, 0x1A)
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(1)
        self.dk.send_rke_window_control(16, 20, 24, 28)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.ck_window_opener_req(0x5, 0x6, 0x7, 0x8)
        self.dk.set_window_position(0x5, 0x6, 0x7, 0x0)
        time.sleep(10)
        self.dk.ck_rke_resp(2, 1, "DelayFail",exec_type=3)

    @allure.title("车窗控制_DelayFail_ACTIVE+DrvrSeat_not_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112175?projectId=46')
    @pytest.mark.full1
    @pytest.mark.v140only
    def test_caseid_112175(self):
        time.sleep(10)
        self.dk.set_window_position(0x1A, 0x1A, 0x1A, 0x1A)
        self.set_usage_mode(0xB)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(1)
        self.dk.send_rke_window_control(0, 0, 0, 0)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.ck_window_opener_req(0x1, 0x1, 0x1, 0x1)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x0)
        time.sleep(8)
        self.dk.ck_rke_resp(2, 1, "DelayFail",exec_type=3)

    @allure.title("车窗控制_Success_ABANDONED")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112151?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112151(self):
        time.sleep(10)
        self.set_gear_pos(Gear.Park)
        self.set_usage_mode(0)
        self.dk.set_drvr_seat_present()
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        time.sleep(1)
        self.dk.send_rke_window_control(20, 100, 100, 20)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.ck_window_opener_req(0x6, 0x1A, 0x1A, 0x6)
        self.dk.set_window_position(0x6, 0x1A, 0x1A, 0x6)
        time.sleep(1.5)
        self.dk.ck_rke_resp(2, 0, "Success",exec_type=3)

    @allure.title("车窗控制_Success_INACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112185?projectId=46')
    @pytest.mark.smoke
    @pytest.mark.v140only
    def test_caseid_112185(self):
        time.sleep(10)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        self.set_usage_mode(0x1)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_window_control(80, 80, 80, 80)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.ck_window_opener_req(0x15, 0x15, 0x15, 0x15)
        self.dk.set_window_position(0x15, 0x15, 0x15, 0x15)
        time.sleep(1.5)
        self.dk.ck_rke_resp(2, 0, "Success",exec_type=3)

    @allure.title("车窗控制_Success_CONVENIENCE+DrvrSeat_not_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112176?projectId=46')
    @pytest.mark.smoke
    @pytest.mark.v140only
    # @pytest.mark.s2s_prebuild
    def test_caseid_112176(self):
        time.sleep(10)
        self.dk.set_window_position(0x1A, 0x1A, 0x1A, 0x1A)
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(1)
        self.dk.send_rke_window_control(0, 0, 0, 0)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.ck_window_opener_req(0x1, 0x1, 0x1, 0x1)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        time.sleep(1.5)
        self.dk.ck_rke_resp(2, 0, "Success",exec_type=3)

    @allure.title("车窗控制_Success_ACTIVE+DrvrSeat_not_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112197?projectId=46')
    @pytest.mark.sanity
    @pytest.mark.v140only
    def test_caseid_112197(self):
        time.sleep(10)
        self.dk.set_window_position(0x1A, 0x1A, 0x1A, 0x1A)
        self.set_usage_mode(0x1)
        time.sleep(1)
        self.dk.send_rke_window_control(60, 80, 80, 80)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.ck_window_opener_req(0x10, 0x15, 0x15, 0x15)
        self.dk.set_window_position(0x10, 0x15, 0x15, 0x15)
        time.sleep(1.5)
        self.dk.ck_rke_resp(2, 0, "Success",exec_type=3)

    @allure.title("车窗控制_Success_INACTIVE2")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112140?projectId=46')
    @pytest.mark.sanity
    @pytest.mark.v140only
    def test_caseid_112140(self):
        time.sleep(10)
        self.dk.set_window_position(0x5, 0x5, 0x5, 0x5)
        self.set_usage_mode(0x1)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(1)
        self.dk.send_rke_window_control(20, 20, 80, 80)
        self.dk.ck_window_opener_req(0x6, 0x6, 0x15, 0x15)
        self.dk.set_window_position(0x6, 0x6, 0x15, 0x15)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        time.sleep(1.5)
        self.dk.ck_rke_resp(2, 0, "Success",exec_type=3)

    @allure.title("车窗控制_BUSY_车窗控制指令执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112137?projectId=46')
    @pytest.mark.sanity
    def test_caseid_112137(self):
        time.sleep(10)
        self.set_gear_pos(Gear.Park)
        self.dk.set_window_position(0x5, 0x5, 0x5, 0x5)
        self.set_usage_mode(0x1)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(1)
        self.dk.send_rke_window_control(16, 24, 80, 80, slot_index=1)
        self.dk.ck_window_opener_req(0x5, 0x7, 0x15, 0x15)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.send_rke_window_control(0, 0, 0, 0, slot_index=2)
        sleep(1)
        self.dk.ck_rke_resp(2, 1, "SysBusy", exec_type=3, slot_index=2)
        self.dk.set_window_position(0x5, 0x7, 0x15, 0x15)
        time.sleep(1.5)
        self.dk.ck_rke_resp(2, 0, "Success",exec_type=3)

    @allure.title("车窗控制_UsageModeFail_CONVENIENCE+RowSecRiSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111824?projectId=46')
    @pytest.mark.full1
    @pytest.mark.v140only
    def test_caseid_111824(self):
        time.sleep(10)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        self.set_usage_mode(0x2)
        self.dk.set_secri_seat_present()
        time.sleep(1)
        self.dk.send_rke_window_control(20, 20, 20, 20)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 1, "UsageModeFail",exec_type=3)

    @allure.title("车窗控制_UsageModeFail_CONVENIENCE+RowSecLeSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111823?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111823(self):
        time.sleep(10)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        self.set_usage_mode(0x2)
        self.dk.set_secle_seat_present()
        time.sleep(1)
        self.dk.send_rke_window_control(40, 20, 20, 20)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 1, "UsageModeFail",exec_type=3)

    @allure.title("车窗控制_UsageModeFail_ACTIVE+RowSecRiSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111822?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111822(self):
        time.sleep(10)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        self.set_usage_mode(0xB)
        self.dk.set_secri_seat_present()
        time.sleep(1)
        self.dk.send_rke_window_control(20, 60, 20, 20)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 1, "UsageModeFail",exec_type=3)

    @allure.title("车窗控制_UsageModeFail_ACTIVE+RowSecMidSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111821?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111821(self):
        time.sleep(10)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        self.set_usage_mode(0xB)
        self.dk.set_secmid_seat_present()
        time.sleep(1)
        self.dk.send_rke_window_control(20, 20, 80, 20)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 1, "UsageModeFail",exec_type=3)

    @allure.title("车窗控制_UsageModeFail_ACTIVE+RowSecLeSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111820?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111820(self):
        time.sleep(10)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        self.set_usage_mode(0xB)
        self.dk.set_secle_seat_present()
        time.sleep(1)
        self.dk.send_rke_window_control(20, 20, 20, 100)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 1, "UsageModeFail",exec_type=3)

    @allure.title("车窗控制_UsageModeFail_ACTIVE+PassSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111819?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111819(self):
        time.sleep(10)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        self.set_usage_mode(0xB)
        self.dk.set_pass_seat_present()
        time.sleep(1)
        self.dk.send_rke_window_control(16, 20, 20, 20)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 1, "UsageModeFail",exec_type=3)

    @allure.title("车窗控制_UsageModeFail_CONVENIENCE+RowSecMidSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111818?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111818(self):
        time.sleep(10)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        self.set_usage_mode(0x2)
        self.dk.set_secmid_seat_present()
        time.sleep(1)
        self.dk.send_rke_window_control(20, 24, 20, 20)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 1, "UsageModeFail",exec_type=3)

    @allure.title("车窗控制_UsageModeFail_CONVENIENCE+PassSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111817?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111817(self):
        time.sleep(10)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        self.set_usage_mode(0x2)
        self.dk.set_pass_seat_present()
        time.sleep(1)
        self.dk.send_rke_window_control(20, 20, 96, 20)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 1, "UsageModeFail",exec_type=3)

    
    @allure.title("车窗控制_Success_Convenience+P当+主驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987283?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987283(self):
        time.sleep(10)
        self.set_usage_mode(0x2)
        self.set_gear_pos(Gear.Park)
        self.dk.set_drvr_seat_present()
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        time.sleep(1)
        self.dk.send_rke_window_control(100, 100, 100, 20)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.ck_window_opener_req(0x1A, 0x1A, 0x1A, 0x6)
        self.dk.set_window_position(0x1A, 0x1A, 0x1A, 0x6)
        time.sleep(1.5)
        self.dk.ck_rke_resp(2, 0, "Success",exec_type=3)

    
    @allure.title("车窗控制_Success_Inactive+P当+主驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987284?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987284(self):
        self.set_usage_mode(0x1)
        self.dk.set_drvr_seat_present()
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        time.sleep(1)
        self.dk.send_rke_window_control(16, 24, 80, 80)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.ck_window_opener_req(0x5, 0x7, 0x15, 0x15)
        self.dk.set_window_position(0x5, 0x7, 0x15, 0x15)
        time.sleep(1.5)
        self.dk.ck_rke_resp(2, 0, "Success",exec_type=3)
    
    @allure.title("车窗控制_Success_ABANDONED+P当+主驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987283?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987280(self):
        time.sleep(10)
        self.set_gear_pos(Gear.Park)
        self.set_usage_mode(0)
        self.dk.set_drvr_seat_present()
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        time.sleep(1)
        self.dk.send_rke_window_control(20, 100, 100, 20)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.ck_window_opener_req(0x6, 0x1A, 0x1A, 0x6)
        self.dk.set_window_position(0x6, 0x1A, 0x1A, 0x6)
        time.sleep(1.5)
        self.dk.ck_rke_resp(2, 0, "Success",exec_type=3)

    
    @allure.title("车窗控制_Success_ABANDONED+P当+主驾未占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987283?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987279(self):
        time.sleep(10)
        self.set_gear_pos(Gear.Park)
        self.set_usage_mode(0)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        time.sleep(1)
        self.dk.send_rke_window_control(100, 100, 20, 20)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.ck_window_opener_req(0x1A, 0x1A, 0x6, 0x6)
        self.dk.set_window_position(0x1A, 0x1A, 0x6, 0x6)
        time.sleep(1.5)
        self.dk.ck_rke_resp(2, 0, "Success",exec_type=3)

    
    @allure.title("车窗控制_Success_Convenience+P当+主驾未占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987283?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987282(self):
        time.sleep(10)
        self.set_gear_pos(Gear.Park)
        self.set_usage_mode(2)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        time.sleep(1)
        self.dk.send_rke_window_control(16, 24, 80, 80)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.ck_window_opener_req(0x5, 0x7, 0x15, 0x15)
        self.dk.set_window_position(0x5, 0x7, 0x15, 0x15)
        time.sleep(1.5)
        self.dk.ck_rke_resp(2, 0, "Success",exec_type=3)

    
    @allure.title("车窗控制_Success_Inactive+P当+主驾未占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987283?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987281(self):
        self.set_gear_pos(Gear.Park)
        self.dk.set_window_position(0x10, 0x10, 0x10, 0x10)
        time.sleep(1)
        self.dk.send_rke_window_control(20, 100, 100, 20)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.ck_window_opener_req(0x6, 0x1A, 0x1A, 0x6)
        self.dk.set_window_position(0x6, 0x1A, 0x1A, 0x6)
        time.sleep(1.5)
        self.dk.ck_rke_resp(2, 0, "Success",exec_type=3)

    
    @allure.title("车窗控制_UsageModeFail_Active")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359627?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987276(self):
        self.set_usage_mode(11)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        time.sleep(1)
        self.dk.send_rke_window_control(100, 100, 100, 100)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 1, "UsageModeFail",exec_type=3)

    
    @allure.title("车窗控制_UsageModeFail_Convenience+非P挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359627?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987277(self):
        self.set_usage_mode(2)
        self.set_gear_pos(Gear.Neut)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        time.sleep(1)
        self.dk.send_rke_window_control(80, 80, 80, 80)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 1, "UsageModeFail",exec_type=3)


    
    @allure.title("车窗控制_UsageModeFail_Inactive+D挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/2705744?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987541(self):
        self.set_usage_mode(0x1)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        self.set_gear_pos(Gear.Drv)
        time.sleep(1)
        self.dk.send_rke_window_control(16, 16, 80, 80)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.ck_window_opener_req(0x5, 0x5, 0x15, 0x15)
        self.dk.set_window_position(0x5, 0x5, 0x15, 0x15)
        time.sleep(1.5)
        self.dk.ck_rke_resp(2, 0, "Success",exec_type=3)

    
    @allure.title("车窗控制_UsageModeFail_Abandoned+R挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/2705742?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987540(self):
        self.set_usage_mode(0x0)
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        self.set_gear_pos(Gear.Rvs)
        time.sleep(1)
        self.dk.send_rke_window_control(100, 100, 100, 100)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.ck_window_opener_req(0x1A, 0x1A, 0x1A, 0x1A)
        self.dk.set_window_position(0x1A, 0x1A, 0x1A, 0x1A)
        time.sleep(1.5)
        self.dk.ck_rke_resp(2, 0, "Success",exec_type=3)

    
    @allure.title("车窗控制_DelayFail_CONVENIENCE+P挡+主驾未占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112169?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987278(self):
        self.dk.set_window_position(0xA, 0xB, 0xC, 0xD)
        self.set_usage_mode(0x2)
        self.set_gear_pos(Gear.Park)
        time.sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.send_rke_window_control(20, 20, 20, 20)
        time.sleep(PRECHECKTI)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.ck_window_opener_req(0x6, 0x6, 0x6, 0x6)
        self.dk.set_window_position(0xE, 0xD, 0xD, 0xD)
        time.sleep(10)
        self.dk.ck_rke_resp(2, 1, "DelayFail",exec_type=3)

