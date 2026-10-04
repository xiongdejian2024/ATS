#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File         :test_peps_approach.py
@Time         :2022/11/24 17:13:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
'''
from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass import *


@allure.feature("互联服务")
@allure.story("数字钥匙和账号/PEPS/近车自动解锁")
class TestDigitalKeyApproach(TestDigitalKey):
    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu)
        self.set_config_info(1, 1)
        sleep(2)
    
    def after_each_func(self, ecu):
        """每个测试用例后置步骤"""
        super().after_each_func(ecu)


    @allure.title("近车解锁_解锁成功_LockSts_LockLockd+INACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112297?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112297(self):
        self.dk.set_cenlock_sts(3)
        self.set_usage_mode(0x1)
        # self.set_config_info(1, 1)
        self.set_config_info(3, 0)
        # # self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        # self.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])
        self.dk.set_drvr_seat_present()
        self.dk.empty_dk_data_queue()
        self.dk.send_approach_unlock_cmd()
        # self.dk.ck_door_opener_cmd(1, 4, 1)
        # self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        # time.sleep(1)
        # self.dk.ck_four_door_lock_cmd(0)
        self.dk.ck_cenlock_sts(1, 9)

    @allure.title("近车解锁_解锁+自动开门_钥匙未进入zone7")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112273?projectId=46')
    @pytest.mark.full
    def test_caseid_112273(self):
        self.dk.set_cenlock_sts(3)
        self.set_usage_mode(0x1)
        # self.set_config_info(1, 1)
        self.set_config_info(3, 1)
        # self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.send_approach_unlock_cmd()
        self.dk.ck_door_opener_cmd(1, 4)
        self.dk.set_door_opener_sts(2, 1, 1, 1, 1)
        # 实BGM发送ack后10ms左右开始发送四门解锁，持续1s后恢复idle
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        time.sleep(1)
        self.dk.ck_four_door_lock_cmd(0)
        self.dk.ck_cenlock_sts(1, 9)

        with allure.step("BGM应该未发出主驾开门指令"):
            st = time.time()
            while time.time() - st < 30:
                try:
                    self.dk.ck_door_opener_cmd(1, 1)
                except Exception:
                    time.sleep(1)
                else:
                    assert False, "30s内BGM异常发出主驾开门指令"
            self.dk.ck_door_opener_cmd(1, 0)

    @allure.title("近车解锁_前置条件不满足_LockSts_LockUnlckd")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112257?projectId=46')
    @pytest.mark.full
    def test_caseid_112257(self):
        # self.set_config_info(1, 1)
        self.set_config_info(1, 0)
        self.dk.set_cenlock_sts(1)
        # self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_drvr_seat_present()
        self.dk.send_approach_unlock_cmd()
        try:
            self.dk.ck_four_door_lock_cmd(1)
        except Exception:
            pass
        else:
            assert False, "前置条件不满足，不应该解锁"

    @allure.title("近车解锁_解锁+自动开门_钥匙进入zone7")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112254?projectId=46')
    @pytest.mark.sanity
    def test_caseid_112254(self):
        # self.set_config_info(1, 1)
        self.set_config_info(3, 1)
        self.dk.set_cenlock_sts(3)
        # self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.set_usage_mode(0x1)
        self.dk.set_drvr_seat_notpresent()
        self.dk.send_approach_unlock_cmd()
        self.dk.ck_door_opener_cmd(1, 4, 1)
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        time.sleep(1)
        self.dk.ck_four_door_lock_cmd(0)
        self.dk.set_door_opener_sts(9, 1, 1, 1, 1)
        self.dk.ck_cenlock_sts(1, 9)


    @allure.title("近车解锁_前置条件不满足_DRIVING")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112252?projectId=46')
    @pytest.mark.full
    def test_caseid_112252(self):
        # self.set_config_info(1, 1)
        self.set_config_info(3, 0)
        self.dk.set_cenlock_sts(3)
        # self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.set_usage_mode(0xD)
        time.sleep(1)
        self.dk.send_approach_unlock_cmd()
        self.dk.ck_four_door_lock_cmd(0)
        self.dk.ck_cenlock_sts(3)

    @allure.title("近车解锁_前置条件不满足_CONVENIENCE+DrvrSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112246?projectId=46')
    @pytest.mark.full
    def test_caseid_112246(self):
        # self.set_config_info(1, 1)
        self.set_config_info(3, 0)
        self.dk.set_cenlock_sts(3)
        # self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_present()
        time.sleep(4)
        self.dk.send_approach_unlock_cmd()
        try:
            self.dk.ck_four_door_lock_cmd(1)
        except Exception:
            pass
        else:
            assert False, "前置条件不满足，不应该解锁"
        self.dk.ck_cenlock_sts(3)

    @allure.title("近车解锁_解锁+自动开门_钥匙30s后进入zone7")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112240?projectId=46')
    @pytest.mark.sanity
    def test_caseid_112240(self):
        self.set_usage_mode(0x0)
        # self.set_config_info(1, 1)
        self.set_config_info(3, 1)
        # self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_drvr_seat_notpresent()

        self.dk.set_cenlock_sts(3)
        self.dk.send_approach_unlock_cmd()
        self.dk.ck_door_opener_cmd(1, 4)
        # 实BGM发送ack后10ms左右开始发送四门解锁，持续1s后恢复idle
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        time.sleep(1)
        self.dk.ck_four_door_lock_cmd(0)
        self.dk.ck_cenlock_sts(1, 9)

        with allure.step("BGM应该未发出主驾开门指令"):
            st = time.time()
            while time.time() - st < 30:
                try:
                    self.dk.ck_door_opener_cmd(1, 1)
                except Exception:
                    time.sleep(1)
                else:
                    assert False, "30s内BGM异常发出主驾开门指令"
        with allure.step("32s后设置0x198 Zone7=Valid"):
            time.sleep(32)
            self.ipdu.connectivitycanfd_bncmconnectivityfr17_blekeyprsntstszone7_0_bncmconnectivitysignalipdu17_validity_valid()
            time.sleep(0.2)
        with allure.step("BGM应该未发出主驾开门指令"):
            st = time.time()
            while time.time() - st < 5:
                try:
                    self.dk.ck_door_opener_cmd(1, 1)
                except Exception:
                    time.sleep(1)
                else:
                    assert False, "5s内BGM异常发出主驾开门指令"

    @allure.title("近车解锁_前置条件不满足_ccp#94!=0x80")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112236?projectId=46')
    @pytest.mark.full
    def test_caseid_112236(self):
        # self.set_config_info(1, 1)
        self.set_config_info(3, 0)
        self.dk.set_cenlock_sts(3)
        self.write_ccp({94: 0x1, 98: 0x2, 10: 0x2})
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_notpresent()
        time.sleep(1)
        self.dk.send_approach_unlock_cmd()
        try:
            self.dk.ck_four_door_lock_cmd(1)
        except Exception:
            pass
        else:
            assert False, "前置条件不满足，不应该解锁"
        self.dk.ck_cenlock_sts(3)

    @allure.title("近车解锁_前置条件不满足_ACTIVE+DrvrSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112227?projectId=46')
    @pytest.mark.full
    def test_caseid_112227(self):
        # self.set_config_info(1, 1)
        self.set_config_info(3, 0)
        self.dk.set_cenlock_sts(3)
        # self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.set_usage_mode(0xB)
        self.dk.set_drvr_seat_present()
        time.sleep(4)
        self.dk.send_approach_unlock_cmd()
        try:    
            self.dk.ck_four_door_lock_cmd(1)
        except Exception:
            pass
        else:
            assert False, "前置条件不满足，不应该解锁"
        self.dk.ck_cenlock_sts(3)
