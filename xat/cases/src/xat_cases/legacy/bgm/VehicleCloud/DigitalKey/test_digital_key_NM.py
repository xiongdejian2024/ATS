#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_rke_window_control.py
@Time         :2022/11/28 17:21:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass import *


@allure.feature("互联服务")
@allure.story("数字钥匙和账号/DK网络管理")
@pytest.mark.run(order=-1)
class TestDigitalKeyNM(TestDigitalKey):
    @allure.title("VFC_IPWakeUp_Deactive_NoBleKey_ACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112134?projectId=46')
    @pytest.mark.sanity
    def test_caseid_112134(self):
        self.dk.set_digital_key_connect_info()
        self.set_usage_mode(0xB)
        self.ck_pnc23(0)
        self.dk.set_digital_key_connect_info(connect_sts1=1, type1=2, keyid1=bytes([0x11] * 16),
                                          connect_sts2=1, type2=1, keyid2=bytes([0x22] * 16))
        time.sleep(20)
        self.ck_pnc23(1)
        self.dk.set_digital_key_connect_info(connect_sts2=1, type2=1, keyid2=bytes([0x22] * 16))
        time.sleep(1)
        self.ck_pnc23(0)

    @allure.title("VFC_IPWakeUp_Deactive_NoBleKey_ABANDON")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112133?projectId=46')
    @pytest.mark.full
    def test_caseid_112133(self):
        self.dk.set_digital_key_connect_info()
        self.set_usage_mode(0x0)
        self.ck_pnc23(0)
        self.dk.set_digital_key_connect_info(connect_sts1=1, type1=2, keyid1=bytes([0x01] * 16),
                                          connect_sts2=1, type2=1, keyid2=bytes([0x22] * 16),
                                          connect_sts3=1, type3=3, keyid3=bytes([0x33] * 16),
                                          connect_sts4=1, type4=5, keyid4=bytes([0x44] * 16))
        time.sleep(10)
        self.ck_pnc23(1)
        self.dk.set_digital_key_connect_info(connect_sts1=1, type1=9, keyid1=bytes([0x11] * 16),
                                          connect_sts2=1, type2=1, keyid2=bytes([0x22] * 16),
                                          connect_sts3=1, type3=3, keyid3=bytes([0x33] * 16),
                                          connect_sts4=1, type4=5, keyid4=bytes([0x44] * 16))
        time.sleep(1)
        self.ck_pnc23(0)

    @allure.title("VFC_IPWakeUp_ACTIVE+DIgitalKeyConnectivity[2].type == 2 kBleKey")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112132?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112132(self):
        self.dk.set_digital_key_connect_info()
        self.set_usage_mode(0xB)
        self.ck_pnc23(0)
        self.dk.set_digital_key_connect_info(connect_sts1=1, type1=2, keyid1=bytes([0x20] * 16))
        time.sleep(1)
        self.ck_pnc23(1)
        time.sleep(60 * 4)
        self.ck_pnc23(1)
        time.sleep(70)
        self.ck_pnc23(0)

    @allure.title("VFC_IPWakeUp_WakeAlive_Ti_reset_Inactive2Abandon")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112131?projectId=46')
    @pytest.mark.sanity
    # @pytest.mark.longtime
    def test_caseid_112131(self):
        self.dk.set_digital_key_connect_info()
        self.set_usage_mode(0x1)
        self.ck_pnc23(0)
        self.dk.set_digital_key_connect_info(connect_sts1=1, type1=2, keyid1=bytes([0x11] * 16))
        time.sleep(1)
        self.ck_pnc23(1)
        time.sleep(60 * 4)
        self.set_usage_mode(0)
        time.sleep(60 * 29)
        self.ck_pnc23(1)
        time.sleep(70)
        self.ck_pnc23(0)

    @allure.title("VFC_IPWakeUp_ABANDON+DIgitalKeyConnectivity[4].type == 2 kBleKey")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112130?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112130(self):
        # RVS会一直拉IPwakeUp，所以只能看RVC日志来判断是否按要求拉起和释放了
        # https://jama.jiduauto.com/perspective.req#/items/975723?projectId=46
        self.dk.set_digital_key_connect_info()
        self.set_usage_mode(0x0)
        self.ck_pnc23(0)
        self.dk.set_digital_key_connect_info(connect_sts1=1, type1=2, keyid1=bytes([0x13] * 16))
        time.sleep(100)
        self.ck_pnc23(1)
        time.sleep(60 * 4)
        self.ck_pnc23(1)
        time.sleep(70)
        self.ck_pnc23(0)

    @allure.title("掉电之后测试近车解锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112297?projectId=46')
    @pytest.mark.full
    def test_caseid_1987548(self):
        logger.info("------------------>复位BGM")
        self.nucapp.bgm_power_off()
        time.sleep(2)
        self.nucapp.bgm_power_on()
        time.sleep(15)
        logger.info("------------------>复位BGM结束")
        self.dk.set_cenlock_sts(3)
        self.set_usage_mode(0x1)
        self.set_config_info(3, 0)
        self.dk.set_drvr_seat_present()
        self.dk.empty_dk_data_queue()
        self.dk.send_approach_unlock_cmd()
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(1, 9)

    @allure.title("休眠之后测试近车解锁")
    @pytest.mark.full
    def test_caseid_1987555(self):
        self.bgm_power_off_and_on(timeout=15)#重启BGM代替休眠唤醒
        self.dk.set_cenlock_sts(3)
        self.set_usage_mode(0x1)
        self.set_config_info(3, 0)
        self.dk.set_drvr_seat_present()
        self.dk.empty_dk_data_queue()
        self.dk.send_approach_unlock_cmd()
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(1, 9)

    @allure.title("休眠之后测试PE解锁")
    @pytest.mark.full
    def test_caseid_1987554(self):
        self.bgm_power_off_and_on(timeout=15)#重启BGM代替休眠唤醒
        self.set_config_info(3, 1)
        self.dk.set_cenlock_sts(1)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.set_usage_mode(0x1)
        self.dk.set_four_door_lock()
        self.dk.set_cenlock_sts(3)
        sleep(3)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(4, 0.5)
        self.dk.ck_search_key_req(1, 2,timeout=2)
        self.dk.set_four_door_unlock()
        sleep(1)
        self.dk.ck_cenlock_sts(1, 2)

    @allure.title("休眠之后RKE解闭锁")
    @pytest.mark.full
    def test_caseid_1987553(self):
        self.bgm_power_off_and_on(timeout=15)#重启BGM代替休眠唤醒
        self.set_config_info(3, 1)
        self.dk.set_cenlock_sts(1)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.set_usage_mode(0x1)
        self.dk.set_four_door_lock()
        self.dk.set_cenlock_sts(3)
        sleep(3)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(4, 0.5)
        self.dk.ck_search_key_req(1, 2,timeout=2)
        self.dk.set_four_door_unlock()
        sleep(1)
        self.dk.ck_cenlock_sts(1, 2)

    @allure.title("休眠之后RKE窗户控制")
    @pytest.mark.full
    def test_caseid_1987552(self):
        self.bgm_power_off_and_on(timeout=15)#重启BGM代替休眠唤醒
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        self.dk.send_rke_window_control(100, 100, 100, 20)
        time.sleep(0.15)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.ck_window_opener_req(0x1A, 0x1A, 0x1A, 0x6)
        self.dk.set_window_position(0x1A, 0x1A, 0x1A, 0x6)
        time.sleep(10)
        self.dk.ck_rke_resp(2, 0, "Success",exec_type=3)

    @allure.title("掉电之后测试PE解锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112297?projectId=46')
    @pytest.mark.full
    def test_caseid_1987547(self):
        logger.info("------------------>复位BGM")
        self.nucapp.bgm_power_off()
        time.sleep(2)
        self.nucapp.bgm_power_on()
        time.sleep(15)
        logger.info("------------------>复位BGM结束")
        self.set_config_info(3, 1)
        self.dk.set_cenlock_sts(1)

        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.set_usage_mode(0x1)
        self.dk.set_four_door_lock()
        self.dk.set_cenlock_sts(3)
        sleep(3)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(4, 0.5)
        self.dk.ck_search_key_req(1, 2,timeout=2)
        self.dk.set_four_door_unlock()
        sleep(1)
        self.dk.ck_cenlock_sts(1, 2)

    @allure.title("掉电之后RKE窗户控制")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112297?projectId=46')
    @pytest.mark.full
    def test_caseid_1987545(self):
        logger.info("------------------>复位BGM")
        self.nucapp.bgm_power_off()
        time.sleep(2)
        self.nucapp.bgm_power_on()
        time.sleep(15)
        logger.info("------------------>复位BGM结束")
        self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
        self.dk.send_rke_window_control(100, 100, 100, 20)
        time.sleep(0.15)
        self.dk.ck_rke_resp(2, 0, "PreConditionOK",exec_type=2)
        self.dk.ck_window_opener_req(0x1A, 0x1A, 0x1A, 0x6)
        self.dk.set_window_position(0x1A, 0x1A, 0x1A, 0x6)
        time.sleep(10)
        self.dk.ck_rke_resp(2, 0, "Success",exec_type=3)

    # @allure.title("VFC_IPWakeUp_INACTIVE+DIgitalKeyConnectivity[3].type == 2 kBleKey")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359667?projectId=46')
    # @pytest.mark.smoke1
    # def test_caseid_1359667(self):
    #     self.dk.set_digital_key_connect_info()
    #     self.set_usage_mode(0x1)
    #     self.ck_pnc23(0)
    #     self.dk.set_digital_key_connect_info(connect_sts1=1, type1=2, keyid1=bytes([0x11] * 16))
    #     time.sleep(1)
    #     self.ck_pnc23(1)
    #     time.sleep(60 * 4)
    #     self.ck_pnc23(1)
    #     time.sleep(70)
    #     self.ck_pnc23(0)
    #
    # @allure.title("VFC_IPWakeUp_CONVENIENCE+DIgitalKeyConnectivity[4].type == 2 kBleKey")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359668?projectId=46')
    # @pytest.mark.full1
    # def test_caseid_1359668(self):
    #     self.dk.set_digital_key_connect_info()
    #     self.set_usage_mode(0x2)
    #     self.ck_pnc23(0)
    #     self.dk.set_digital_key_connect_info(connect_sts1=1, type1=2, keyid1=bytes([0x10] * 16))
    #     time.sleep(1)
    #     self.ck_pnc23(1)
    #     time.sleep(60 * 4)
    #     self.ck_pnc23(1)
    #     time.sleep(70)
    #     self.ck_pnc23(0)
    #
    # @allure.title("VFC_IPWakeUp_DRIVING+DIgitalKeyConnectivity[1].type == 2 kBleKey")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359669?projectId=46')
    # @pytest.mark.sanity1
    # def test_caseid_1359669(self):
    #     self.dk.set_digital_key_connect_info()
    #     self.set_usage_mode(0xD)
    #     self.ck_pnc23(0)
    #     self.dk.set_digital_key_connect_info(connect_sts1=1, type1=2, keyid1=bytes([0x11] * 16))
    #     time.sleep(1)
    #     self.ck_pnc23(1)
    #     time.sleep(60 * 4)
    #     self.ck_pnc23(1)
    #     time.sleep(70)
    #     self.ck_pnc23(0)
    #
    # @allure.title("VFC_IPWakeUp_WakeAlive_Ti_reset_Abandon2Convience")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359670?projectId=46')
    # @pytest.mark.full1
    # def test_caseid_1359670(self):
    #     self.dk.set_digital_key_connect_info()
    #     self.set_usage_mode(0x0)
    #     self.ck_pnc23(0)
    #     self.dk.set_digital_key_connect_info(connect_sts1=1, type1=2, keyid1=bytes([0x11] * 16))
    #     time.sleep(1)
    #     self.ck_pnc23(1)
    #     time.sleep(60 * 6)
    #     self.ck_pnc23(1)
    #     self.set_usage_mode(0x2)
    #     time.sleep(60 * 4)
    #     self.ck_pnc23(1)
    #     time.sleep(70)
    #     self.ck_pnc23(0)
    #
    # @allure.title("VFC_IPWakeUp_Deactive_NoBleKey_DRIVING")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359671?projectId=46')
    # @pytest.mark.full1
    # def test_caseid_1359671(self):
    #     self.dk.set_digital_key_connect_info()
    #     self.set_usage_mode(0xD)
    #     self.ck_pnc23(0)
    #     self.dk.set_digital_key_connect_info(connect_sts1=1, type1=2, keyid1=bytes([0x11] * 16))
    #     time.sleep(1)
    #     self.ck_pnc23(1)
    #     self.dk.set_digital_key_connect_info()
    #     time.sleep(1)
    #     self.ck_pnc23(0)
    #
    # @allure.title("VFC_IPWakeUp_WakeAlive_Ti_reset_Driving2Active")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359672?projectId=46')
    # @pytest.mark.full1
    # def test_caseid_1359672(self):
    #     self.dk.set_digital_key_connect_info()
    #     self.set_usage_mode(0xD)
    #     self.ck_pnc23(0)
    #     self.dk.set_digital_key_connect_info(connect_sts1=1, type1=2, keyid1=bytes([0x11] * 16))
    #     time.sleep(1)
    #     self.ck_pnc23(1)
    #     time.sleep(60 * 4)
    #     self.set_usage_mode(0xB)
    #     time.sleep(70)
    #     self.ck_pnc23(0)
    #
    # @allure.title("VFC_IPWakeUp_Deactive_NoBleKey_CONVENIENCE")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359673?projectId=46')
    # @pytest.mark.smoke1
    # def test_caseid_1359673(self):
    #     self.dk.set_digital_key_connect_info()
    #     self.set_usage_mode(0x2)
    #     self.ck_pnc23(0)
    #     self.dk.set_digital_key_connect_info(connect_sts1=1, type1=2, keyid1=bytes([0x11] * 16),
    #                                       connect_sts2=1, type2=1, keyid2=bytes([0x22] * 16),
    #                                       connect_sts3=1, type3=3, keyid3=bytes([0x33] * 16),
    #                                       connect_sts4=1, type4=5, keyid4=bytes([0x44] * 16))
    #     time.sleep(3)
    #     self.ck_pnc23(1)
    #     self.dk.set_digital_key_connect_info(connect_sts2=1, type2=1, keyid2=bytes([0x22] * 16),
    #                                       connect_sts3=1, type3=3, keyid3=bytes([0x33] * 16),
    #                                       connect_sts4=1, type4=5, keyid4=bytes([0x44] * 16))
    #     time.sleep(3)
    #     self.ck_pnc23(0)
    #
    # @allure.title("VFC_IPWakeUp_Deactive_NoBleKey_INACTIVE")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359674?projectId=46')
    # @pytest.mark.full1
    # def test_caseid_1359674(self):
    #     self.dk.set_digital_key_connect_info()
    #     self.set_usage_mode(0x1)
    #     self.ck_pnc23(0)
    #     self.dk.set_digital_key_connect_info(connect_sts1=1, type1=2, keyid1=bytes([0x11] * 16),
    #                                       connect_sts2=1, type2=1, keyid2=bytes([0x22] * 16),
    #                                       connect_sts3=1, type3=3, keyid3=bytes([0x33] * 16))
    #     time.sleep(1)
    #     self.ck_pnc23(1)
    #     self.dk.set_digital_key_connect_info(connect_sts2=1, type2=1, keyid2=bytes([0x22] * 16),
    #                                       connect_sts3=1, type3=3, keyid3=bytes([0x33] * 16))
    #     time.sleep(1)
    #     self.ck_pnc23(0)

    @allure.title("VFC_IPWakeUp_ABANDON+有蓝牙钥匙连接+RKE模块未初始化完成")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112035?projectId=46')
    @pytest.mark.full
    def test_caseid_112035(self):  # todo：
        self.dk.set_digital_key_connect_info()
        self.set_usage_mode(0x0)
        self.ck_pnc23(0)
        # 1.设置UsageMode=DRIVING，手动将BGM的RVS进程kill
        self.dk.set_digital_key_connect_info(connect_sts1=1, type1=2, keyid1=bytes([0x11] * 16))
        time.sleep(1)
        self.ck_pnc23(0)

    @allure.title("VFC_IPWakeUp_DRIVING+有蓝牙钥匙连接+RKE模块未初始化完成")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112034?projectId=46')
    @pytest.mark.full
    def test_caseid_112034(self):  # todo：
        self.dk.set_digital_key_connect_info()
        self.set_usage_mode(0xD)
        self.ck_pnc23(0)
        # 1.设置UsageMode=DRIVING，手动将BGM的RVS进程kill
        self.dk.set_digital_key_connect_info(connect_sts1=1, type1=2, keyid1=bytes([0x11] * 16))
        time.sleep(1)
        self.ck_pnc23(1)



    

    


    


    
    

    

