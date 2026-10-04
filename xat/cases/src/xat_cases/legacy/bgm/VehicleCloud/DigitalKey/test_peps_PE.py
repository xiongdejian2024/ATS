# -*- coding: utf-8 -*-
"""
@File        : test_rke_PE.py
@Author      : hui.zhao@jiduatuo.com
@Time        : 2024/03/23 18:00 PM
@Description : description about this file
@Examples    : example of how to use it
"""
from time import sleep
from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass import *

handle_ti = 0.5  # PE按下后寻钥匙
OutdSwtPsdTi = 2.5  # 长按闭锁时间


@allure.feature("互联服务")
@allure.story("数字钥匙和账号/PEPS/触碰解锁")
class TestDigitalKeyPepsPe(TestDigitalKey):
    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu)
        self.set_config_info(3, 1)
        self.dk.set_cenlock_sts(1)
    
    def after_each_func(self, ecu):
        """每个测试用例后置步骤"""
        super().after_each_func(ecu)

    """以下为PE解锁用例"""
    @allure.title("PE解锁成功_右后门_寻钥匙status=0x5")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112276?projectId=46')
    @pytest.mark.full
    def test_caseid_112276(self):
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


    @allure.title("PE解锁成功_右后门_寻钥匙status=0x6")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112298?projectId=46')
    @pytest.mark.full
    def test_caseid_112298(self):
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])
        self.dk.set_four_door_lock()
        self.dk.set_cenlock_sts(2)
        self.set_usage_mode(0xB)
        sleep(1)
        self.dk.press_door_outswitch(4, 0.5)
        self.dk.ck_search_key_req(1, 2,timeout=2)
        # self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        sleep(1)
        self.dk.ck_cenlock_sts(1, 2)
        # self.dk.ck_door_opener_cmd(4, 1)

    @allure.title("PE解锁成功_右后门_寻钥匙status=0xA")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112203?projectId=46')
    @pytest.mark.full
    def test_caseid_112203(self):
        self.dk.set_four_door_lock()
        self.set_usage_mode(0x1)
        self.dk.set_cenlock_sts(3)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0xA)])
        sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(4, 0.5)
        self.dk.ck_search_key_req(1, 2)
        # self.dk.ck_four_door_lock_cmd(1)
        # self.dk.ck_door_opener_cmd(4, 1)
        self.dk.set_four_door_unlock()
        sleep(1)
        self.dk.ck_cenlock_sts(1, 2)

    @allure.title("PE解锁成功_右后门_寻钥匙status=0xB")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112259?projectId=46')
    @pytest.mark.full
    def test_caseid_112259(self):
        self.dk.set_cenlock_sts(3)
        self.write_ccp({94: 0x02, 98: 0x2, 10: 0x2})
        self.dk.set_four_door_lock()
        self.set_usage_mode(0xB)
        self.dk.set_drvr_seat_notpresent()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0xB)])
        self.dk.empty_dk_data_queue()
        sleep(1)
        self.dk.press_door_outswitch(4, 0.5)
        self.dk.ck_search_key_req(1, 2)
        # self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        sleep(1)
        self.dk.ck_cenlock_sts(1, 2)
        # self.dk.ck_door_opener_cmd(4, 1)

    @allure.title("PE解锁成功_右后门_寻钥匙有多个钥匙")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112213?projectId=46')
    @pytest.mark.full
    def test_caseid_112213(self):
        self.dk.set_cenlock_sts(3)
        self.write_ccp({94: 0x02, 98: 0x2, 10: 0x2})
        self.dk.set_four_door_lock()
        self.set_usage_mode(0xB)
        self.dk.set_drvr_seat_notpresent()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x1), KeyInfo(KeyType.BLE_Key, key_id2, 0x3)])
        sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(4, 0.5)
        self.dk.ck_search_key_req(1, 2)
        # self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        sleep(1)
        self.dk.ck_cenlock_sts(1, 2)
        # self.dk.ck_door_opener_cmd(4, 1)

    @allure.title("PE解锁成功_右前门_寻钥匙status=0x4")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112212?projectId=46')
    @pytest.mark.sanity
    def test_caseid_112212(self):
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x4)])
        self.set_usage_mode(0x1)
        self.dk.set_four_door_lock()
        self.dk.set_cenlock_sts(3)
        sleep(3)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(2, 0.5)
        self.dk.ck_search_key_req(1, 2,timeout=2)
        self.dk.set_four_door_unlock()
        sleep(1)
        self.dk.ck_cenlock_sts(1, 2)

    @allure.title("PE解锁成功_左后门_寻钥匙status=0x2")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112289?projectId=46')
    @pytest.mark.sanity
    def test_caseid_112289(self):
        self.set_config_info(3, 1)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 2)])
        self.dk.set_four_door_lock()
        self.dk.set_cenlock_sts(3)
        sleep(3)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(3, 0.5)
        self.dk.ck_search_key_req(1, 2)
        # self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        sleep(1)
        self.dk.ck_cenlock_sts(1, 2)
        # self.dk.ck_door_opener_cmd(3, 1)

    @allure.title("PE解锁成功_左前门_寻钥匙status=0x3")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112245?projectId=46')
    @pytest.mark.full
    def test_caseid_112245(self):
        self.dk.set_four_door_lock()
        self.dk.set_cenlock_sts(3)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x3)])
        sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(1, 0.5)
        self.dk.ck_search_key_req(1, 2)
        # self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        sleep(1)
        self.dk.ck_cenlock_sts(1, 2)
        # self.dk.ck_door_opener_cmd(1, 1)

    @allure.title("PE解锁失败_右后门_ACTIVE+主驾占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112202?projectId=46')
    @pytest.mark.full
    def test_caseid_112202(self):
        self.write_ccp({94: 0x02, 98: 0x2, 10: 0x2})
        self.dk.set_four_door_lock()
        self.dk.set_cenlock_sts(3)
        self.set_usage_mode(0xB)
        self.dk.set_drvr_seat_present()
        sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(4, 0.5)
        self.dk.ck_bgm_not_send_cmd("Active+主驾占位, 不应该发出寻钥匙指令", self.dk.dk_data_queue_key_search)
        sleep(1)
        self.dk.ck_cenlock_sts(3)

    @allure.title("PE解锁失败_右后门_CONVENIENCE+主驾占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112271?projectId=46')
    @pytest.mark.full
    def test_caseid_112271(self):
        self.write_ccp({94: 0x02, 98: 0x2, 10: 0x2})
        self.dk.set_four_door_lock()
        self.dk.set_cenlock_sts(3)
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_present()
        self.dk.empty_dk_data_queue()
        sleep(1)
        self.dk.press_door_outswitch(4, 0.5)
        self.dk.ck_bgm_not_send_cmd("CONVENIENCE+主驾占位, 不应该发出寻钥匙指令", self.dk.dk_data_queue_key_search)
        sleep(1)
        self.dk.ck_cenlock_sts(3)

    @allure.title("PE解锁失败_右前门_车外无钥匙")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1988227?projectId=46')
    @pytest.mark.full
    def test_caseid_1988227(self):
        self.dk.set_four_door_lock()
        self.set_usage_mode(0x1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(2, 0.5)
        self.dk.ck_search_key_req(1, 2)
        self.dk.ck_four_door_lock_cmd(0)
        sleep(1)
        self.dk.ck_cenlock_sts(3)

    @allure.title("PE解锁失败_左后门_车外无钥匙")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1988228?projectId=46')
    @pytest.mark.full
    def test_caseid_1988228(self):
        self.dk.set_four_door_lock()
        self.set_usage_mode(0x1)
        self.dk.set_cenlock_sts(3)
        sleep(5)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(3, 0.5)
        self.dk.ck_search_key_req(1, 2)
        sleep(1)
        self.dk.ck_cenlock_sts(3)

    @allure.title("PE解锁失败_左前门_ccp#94=0x1")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112201?projectId=46')
    @pytest.mark.full
    def test_caseid_112201(self):
        self.dk.set_cenlock_sts(3)
        self.write_ccp({94: 0x01, 98: 0x2, 10: 0x2})
        self.dk.set_four_door_lock()
        self.dk.empty_dk_data_queue()
        sleep(1)
        self.dk.press_door_outswitch(1, 0.5)
        self.dk.ck_bgm_not_send_cmd("Active+主驾占位, 不应该发出寻钥匙指令", self.dk.dk_data_queue_key_search)
        self.dk.ck_cenlock_sts(3)

    @allure.title("PE解锁失败_左前门_DRIVING")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112225?projectId=46')
    @pytest.mark.full
    def test_caseid_112225(self):
        self.dk.set_four_door_lock()
        self.dk.set_cenlock_sts(3)
        self.set_usage_mode(0xD)
        self.dk.set_drvr_seat_notpresent()
        self.dk.empty_dk_data_queue()
        sleep(1)
        self.dk.press_door_outswitch(1, 0.5)
        self.dk.ck_bgm_not_send_cmd("DRIVING, 不应该发出寻钥匙指令", self.dk.dk_data_queue_key_search)
        self.dk.ck_cenlock_sts(3)

    """以下为PE解锁尾门"""
    """tips: 尾门打开要求standstill3，档位为P或N，为等待POT唤醒，会等待300ms-2000ms再发送开尾门指令"""
    @allure.title("PE解锁开尾门成功_ABANDONED")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112303?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112303(self):
        self.write_ccp({97:0x02, 98:0x2})
        self.dk.set_cenlock_sts(0x3)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x0B)])
        sleep(3)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(5, 0.5)
        self.dk.ck_search_key_req(0x01, 0x02)
        self.dk.ck_cenlock_sts(2, 2)

    @allure.title("PE解锁开尾门成功_CONVENIENCE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112222?projectId=46')
    @pytest.mark.sanity
    def test_caseid_112222(self):
        self.write_ccp({94: 0x02})
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0x2)
        self.dk.empty_dk_data_queue()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 5)])
        sleep(1)
        self.dk.press_door_outswitch(5, 0.1)
        self.dk.ck_search_key_req(0x01, 0x02)
        sleep(1)
        self.dk.ck_cenlock_sts(2, 2)
        # self.dk.ck_door_opener_cmd(5, 1)
 

    @allure.title("PE解锁开尾门成功_DRIVING")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112263?projectId=46')
    @pytest.mark.full
    def test_caseid_112263(self):
        self.write_ccp({94: 0x02})
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0xD)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x0B)])
        sleep(3)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(5, 0.5)
        self.dk.ck_search_key_req(0x01, 0x02)
        self.dk.ck_cenlock_sts(2, 2)

    @allure.title("PE解锁开尾门成功_ACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112261?projectId=46')
    @pytest.mark.full
    def test_caseid_112261(self):
        self.write_ccp({94: 0x02})
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0xB)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x0B)])
        sleep(3)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(5, 0.5)
        self.dk.ck_search_key_req(0x01, 0x02)
        self.dk.ck_cenlock_sts(2, 2)

    @allure.title("PE解锁开尾门成功_INACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112250?projectId=46')
    @pytest.mark.sanity
    def test_caseid_112250(self):
        self.write_ccp({94: 0x02})
        self.dk.set_cenlock_sts(0x3)
        self.set_usage_mode(0x1)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 5)])
        sleep(3)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(5, 0.1)
        self.dk.ck_search_key_req(0x01, 0x02)
        sleep(1)
        self.dk.ck_cenlock_sts(2, 2)
        # sleep(0.5)
        # self.dk.ck_door_opener_cmd(5, 1)

    @allure.title("PE解锁开尾门失败_车外无钥匙")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112283?projectId=46')
    @pytest.mark.full
    def test_caseid_1988351(self):
        self.dk.set_cenlock_sts(0x3)
        sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(5, 0.1)
        self.dk.ck_search_key_req(0x01, 0x02)
        sleep(0.5)
        #self.dk.ck_door_opener_cmd(5, 0, timeout=0.1)
        self.dk.ck_cenlock_sts(3)

    @allure.title("PE解锁开尾门失败_寻钥匙结果与目标区域不匹配")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1988352?projectId=46')
    @pytest.mark.full
    def test_caseid_1988352(self):
        self.dk.set_cenlock_sts(0x3)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 9)])
        sleep(3)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(5, 0.1)
        self.dk.ck_search_key_req(0x01, 0x02)
        sleep(0.5)
        self.dk.ck_cenlock_sts(3)

    """以下为长按闭锁用例，有门开则寻钥匙0x1 All,所有门关则寻钥匙0x2 AllExt"""
    @allure.title("PE长按闭锁成功_原中控锁 LockTrUnlckd_INACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112299?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112299(self):
        self.set_usage_mode(1)
        self.dk.set_cenlock_sts(1)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 4)])
        sleep(1)
        self.dk.press_door_outswitch(1, OutdSwtPsdTi)
        self.dk.ck_search_key_req(1, 2,timeout=2)
        #self.dk.ck_four_door_lock_cmd(2)
        sleep(1)
        self.dk.ck_cenlock_sts(3, 2)

    @allure.title("PE长按闭锁失败_DRIVING")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112295?projectId=46')
    @pytest.mark.full
    def test_caseid_112295(self):
        self.dk.set_cenlock_sts(1)
        self.set_usage_mode(0xD)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 4)])
        sleep(1)
        self.dk.press_door_outswitch(1, OutdSwtPsdTi)
        sleep(handle_ti)
        self.dk.ck_bgm_not_send_cmd("DRIVING, 不应该发出寻钥匙指令", self.dk.dk_data_queue_key_search)
        sleep(1)
        self.dk.ck_cenlock_sts(1)

    @allure.title("PE长按闭锁成功_原中控锁LockUnlckd_ABANDONED")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112294?projectId=46')
    @pytest.mark.sanity
    def test_caseid_112294(self):
        self.dk.set_cenlock_sts(1)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 4)])
        sleep(1)
        self.dk.press_door_outswitch(1, OutdSwtPsdTi)
        self.dk.ck_search_key_req(1, 2)
        #self.dk.ck_four_door_lock_cmd(2)
        sleep(1)
        self.dk.ck_cenlock_sts(3, 2)

    @allure.title("PE长按闭锁成功_原中控锁LockUnlckd_ACTIVE+主驾未占座_寻到单个钥匙")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112291?projectId=46')
    @pytest.mark.sanity
    def test_caseid_112291(self):
        self.dk.set_cenlock_sts(1)
        self.set_usage_mode(0xB)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 5)])
        sleep(1)
        self.dk.press_door_outswitch(1, OutdSwtPsdTi)
        self.dk.ck_search_key_req(1, 2)
        #self.dk.ck_four_door_lock_cmd(2)
        sleep(1)
        self.dk.ck_cenlock_sts(3, 2)


    @allure.title("PE长按关四门闭锁成功_原五门全开")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112282?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112282(self):
        self.dk.set_cenlock_sts(1)
        self.set_usage_mode(0xB)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.dk.set_door_opener_sts(5, 5, 5, 5)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0xA)])
        self.dk.update_keyinfos(6, [])
        sleep(1)
        self.dk.press_door_outswitch(1, OutdSwtPsdTi)
        self.dk.ck_search_key_req(1, 2,timeout=2)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_cenlock_sts(3, 2)

    @allure.title("PE长按关四门闭锁失败_DRIVING")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112277?projectId=46')
    @pytest.mark.full
    def test_caseid_112277(self):
        self.dk.set_cenlock_sts(1)
        self.set_usage_mode(0xD)
        sleep(1)
        self.dk.press_door_outswitch(1, OutdSwtPsdTi)
        sleep(handle_ti)
        self.dk.ck_bgm_not_send_cmd("DRIVING, 不应该发出寻钥匙指令", self.dk.dk_data_queue_key_search)
        sleep(1)
        self.dk.ck_cenlock_sts(1)

    @allure.title("PE长按关四门闭锁成功_仅主驾门开")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112264?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112264(self):
        self.dk.set_cenlock_sts(1)
        self.dk.set_door_sts([1, 1, 1, 1, 0])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0xA)])
        self.dk.update_keyinfos(6, [])
        sleep(2)
        self.dk.press_door_outswitch(1, OutdSwtPsdTi)
        self.dk.ck_search_key_req(1, 2,timeout=2)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(0.5)
        sleep(1)
        self.dk.ck_cenlock_sts(3, 2)

    @allure.title("PE长按闭锁失败_CONVENIENCE+主驾占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112244?projectId=46')
    @pytest.mark.full
    def test_caseid_112244(self):
        self.write_ccp({94: 0x02, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(1)
        self.set_usage_mode(0xB)
        self.dk.set_drvr_seat_present()
        self.dk.update_keyinfos(2, [])
        sleep(1)
        self.dk.press_door_outswitch(1, OutdSwtPsdTi)
        sleep(handle_ti)
        self.dk.ck_bgm_not_send_cmd("CONVENIENCE+主驾占位，不应该发送寻钥匙指令", self.dk.dk_data_queue_key_search)
        sleep(1)
        self.dk.ck_cenlock_sts(1)

    @allure.title("PE长按关四门闭锁失败_ccp#94=0x1")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112243?projectId=46')
    @pytest.mark.full
    def test_caseid_112243(self):
        self.write_ccp({94: 0x01, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(1)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        sleep(1)
        self.dk.press_door_outswitch(1, OutdSwtPsdTi)
        sleep(1)
        self.dk.ck_bgm_not_send_cmd("ccp#94=0x1, 不应该发出寻钥匙指令", self.dk.dk_data_queue_key_search)
        sleep(1)
        self.dk.ck_cenlock_sts(1)

    @allure.title("PE长按闭锁失败_寻钥匙结果与目标区域不匹配")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112233?projectId=46')
    @pytest.mark.full
    def test_caseid_112233(self):
        self.dk.set_cenlock_sts(1)
        self.set_usage_mode(0xB)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x9)])
        sleep(1)
        self.dk.press_door_outswitch(1, OutdSwtPsdTi)
        self.dk.ck_search_key_req(1, 2)
        self.dk.ck_bgm_not_send_cmd("寻钥匙结果与目标区域不匹配, 不应该再发送车内寻钥匙指令", self.dk.dk_data_queue_key_search)
        sleep(1)
        self.dk.ck_cenlock_sts(1)

    @allure.title("PE长按关四门闭锁失败_寻钥匙结果与目标区域不匹配")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112232?projectId=46')
    @pytest.mark.full
    def test_caseid_112232(self):
        self.write_ccp({94: 0x02, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(1)
        self.set_usage_mode(0xB)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x9)])
        sleep(1)
        self.dk.press_door_outswitch(1, OutdSwtPsdTi)
        self.dk.ck_search_key_req(1, 2)
        self.dk.ck_bgm_not_send_cmd("寻钥匙结果与目标区域不匹配，不应该再发送车内寻钥匙指令", self.dk.dk_data_queue_key_search)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.ck_cenlock_sts(1)

    @allure.title("PE长按闭锁失败_ccp#94=1")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112229?projectId=46')
    @pytest.mark.full
    def test_caseid_112229(self):
        self.write_ccp({94: 0x01, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.dk.press_door_outswitch(1, OutdSwtPsdTi)
        sleep(handle_ti)
        self.dk.ck_bgm_not_send_cmd("ccp#94=0x1，不应该发送寻钥匙指令", self.dk.dk_data_queue_key_search)
        sleep(1)
        self.dk.ck_cenlock_sts(1)

    @allure.title("PE长按闭锁成功_原中控锁LockTrUnlckd_ACTIVE+主驾未占座_寻到多个钥匙")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112220?projectId=46')
    @pytest.mark.full
    def test_caseid_112220(self):
        self.write_ccp({94: 0x02, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x2})
        self.dk.set_cenlock_sts(2)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0xB), KeyInfo(KeyType.BLE_Key, key_id2, 0x3)])
        sleep(3)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(1, OutdSwtPsdTi)
        self.dk.ck_search_key_req(1, 2)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_cenlock_sts(3, 2)

    @allure.title("PE长按关四门闭锁成功_四门关尾门开")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112218?projectId=46')
    @pytest.mark.sanity
    def test_caseid_112218(self):
        self.dk.set_cenlock_sts(2)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])
        sleep(3)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(1, OutdSwtPsdTi)
        self.dk.ck_search_key_req(1, 2)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_cenlock_sts(3, 2)

    @allure.title("PE长按闭锁失败_ACTIVE+主驾占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112216?projectId=46')
    @pytest.mark.full
    def test_caseid_112216(self):
        self.write_ccp({94: 0x02, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x2})
        self.dk.set_cenlock_sts(1)
        self.set_usage_mode(0xB)
        self.dk.set_drvr_seat_present()
        sleep(1)
        self.dk.press_door_outswitch(1, OutdSwtPsdTi)
        sleep(handle_ti)
        self.dk.ck_bgm_not_send_cmd("ccp#94=0x1, 不应该发出寻钥匙指令", self.dk.dk_data_queue_key_search)
        sleep(1)
        self.dk.ck_cenlock_sts(1)

    @allure.title("PE长按闭锁成功_原中控锁 LockUnlckd_CONVENIENCE+主驾未占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112210?projectId=46')
    @pytest.mark.sanity
    def test_caseid_112210(self):
        self.dk.set_cenlock_sts(1)
        self.set_usage_mode(0x2)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])
        sleep(2)
        self.dk.press_door_outswitch(1, OutdSwtPsdTi)
        self.dk.ck_search_key_req(1, 2)
        # self.dk.ck_four_door_lock_cmd(2)
        self.dk.ck_cenlock_sts(3, 2)


    @allure.title("PE长按右前门关四门闭锁成功_原五门全开")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/109812?projectId=46')
    @pytest.mark.sanity
    def test_caseid_109812(self):
        self.dk.set_cenlock_sts(1)
        self.set_usage_mode(0xB)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.dk.set_door_opener_sts(5, 5, 5, 5)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0xA)])
        sleep(3)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(2, OutdSwtPsdTi)
        self.dk.ck_search_key_req(1, 2)

        self.dk.set_door_sts([0, 0, 0, 0, 0])
        # self.dk.ck_four_door_lock_cmd(2)
        sleep(1)
        self.dk.ck_cenlock_sts(3, 2)

    @allure.title("PE长按左后门关四门闭锁成功_原五门全开")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/109776?projectId=46')
    @pytest.mark.full
    def test_caseid_109776(self):
        self.dk.set_cenlock_sts(1)
        self.set_usage_mode(0xB)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.dk.set_door_opener_sts(5, 5, 5, 5)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0xA)])
        # self.dk.update_keyinfos(6, [])
        sleep(1)
        self.dk.press_door_outswitch(3, OutdSwtPsdTi)
        self.dk.ck_search_key_req(1, 2)

        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(0.5)
        # self.dk.ck_search_key_req(6, 2)
        # sleep(0.5)
        # self.dk.ck_four_door_lock_cmd(2)
        sleep(1)
        self.dk.ck_cenlock_sts(3, 2)

    @allure.title("PE长按左右门关四门闭锁成功_原五门全开")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/109780?projectId=46')
    @pytest.mark.full
    def test_caseid_109780(self):
        self.dk.set_cenlock_sts(1)
        self.set_usage_mode(0xB)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.dk.set_door_opener_sts(5, 5, 5, 5)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0xA)])
        # self.dk.update_keyinfos(6, [])
        sleep(1)
        self.dk.press_door_outswitch(4, OutdSwtPsdTi)
        self.dk.ck_search_key_req(1, 2)

        self.dk.set_door_sts([0, 0, 0, 0, 0])
        # self.dk.ck_search_key_req(6, 2)
        # sleep(0.5)
        # self.dk.ck_four_door_lock_cmd(2)
        sleep(1)
        self.dk.ck_cenlock_sts(3, 2)

