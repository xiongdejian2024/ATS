#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_charge_pile_open_charge_lid.py
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
from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass import *

PRECHECKTI = 1


@allure.feature("互联服务")
@allure.story("数字钥匙和账号/账号控制与同步/白名单控制")
class TestDigitalKeyWhiteListConTrol(TestDigitalKey):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.tsp = DigitalKeyManager(self.tc_config.get('vid'),
                                     self.tc_config.get('tel'),
                                     "jiduapp/0.9.3 (iOS; 16.0; apple; jdcomiphone; iPhone 12; NULL; BF983636-D3F2-4805-90B4-77C3DC75D433; aVBob25l)")
    
    def after_class(self, ecu):
        super().after_class(self, ecu)

    def tsp_ble_slot_sync(self):
        with allure.step("模拟App触发蓝牙钥匙白名单更新"):
            self.tsp.create_bluetooth_digital_key()

    def tsp_nfc_learning(self):
        with allure.step("模拟App触发NFC学卡"):
            self.tsp.nfc_learning()

    # def empty_event_list(self):
    #     with allure.step("清空S2S缓存数据"):
    #         self.partner.empty_event_list()
 

    def tsp_entity_slot_sync(self, nfc_card, action, key_category=1):
        """
        实体卡白名单更新, 模拟app端触发tsp下发实体卡白名单更新
        :param nfc_card: nfc卡id， intlist
        :param action: action=5-禁用/6-恢复
        :param key_category: 1: NFC 卡, 2: UWB 智能钥匙
        :return:
        """
        with allure.step("模拟App触发实体卡白名单更新"):
            self.tsp.key_entity_status_manage(nfc_card, key_category, action)

    
    @allure.title("更新Slot白名单_更新失败")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111973?projectId=46')
    @pytest.mark.full  # pass
    def test_caseid_111973(self):
        self.dk.auto_ack_tsp_ble_sync_cmd = False
        self.tsp_ble_slot_sync()
        sleep(PRECHECKTI)
        self.dk.ck_white_list_update_req(2, [key_id0])
        self.dk.send_while_list_update_resp(0x12, 0x01, self.dk.last_sync_time_ble - 1)
        # todo: 云端查看日志err = 1; errMsg = ""; last_sync_time=T1-1，V1.0会更新errMsg详细定义

    @allure.title("更新KeyID白名单_更新成功_原仅key2激活_禁用key2")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111965?projectId=46')
    @pytest.mark.smoke  # pass
    def test_caseid_111964(self):
        self.tsp_ble_slot_sync()
        sleep(PRECHECKTI)
        self.dk.ck_white_list_update_req(2, [key_id0])
        self.dk.send_while_list_update_resp(0x12, 0x00, self.dk.last_sync_time_ble)
        # todo: 云端查看日志err = 0; errMsg = Success; last_sync_time=T1

    @allure.title("更新Slot白名单_更新超时")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111957?projectId=46')
    @pytest.mark.full  # pass
    def test_caseid_111957(self):
        self.tsp_ble_slot_sync()
        sleep(PRECHECKTI)
        self.dk.ck_white_list_update_req(2, [key_id0])
        # todo: 云端查看日志err = 0; errMsg = DelayFail; last_sync_time=T1

    @allure.title("更新Slot白名单_VFC RemoteKeyFunctionality activate for 20s")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111960?projectId=46')
    @pytest.mark.full  # pass
    def test_caseid_111960(self):
        self.nucapp.bgm_diag_line_down()
        self.nucapp.tcam_kl15_down()
        sleep(10)
        self.tsp_ble_slot_sync()
        sleep(1)
        self.ck_pnc23(1)
        # self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC21, 3.0)
        # self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 10, 1)
        sleep(18)
        self.ck_pnc23(1)
        # self.nm.ck_pnc(21, 1)
        sleep(2)
        self.ck_pnc23(1)
        # self.nm.ck_pnc(21, 0)
        sleep(8)
        self.ck_pnc23(1)
        sleep(2)
        self.ck_pnc23(0)

    @allure.title("更新KeyID白名单_更新失败_原三个钥匙均激活_禁用key1")
    @pytest.mark.full  # pass
    def test_caseid_111956(self):
        # self.tsp_entity_slot_sync(key_id1, 5)
        self.tsp_ble_slot_sync()
        sleep(2)
        self.dk.ck_white_list_update_req(2, [key_id2, key_id3])
        self.dk.send_while_list_update_resp(0x11, 0x01, self.dk.last_sync_time_entity + 2)
        # todo: err = 1; errMsg = DelayFail; last_sync_time=T1+2

    @allure.title("更新KeyID白名单_更新失败_原key2和key3激活_激活key1")
    @pytest.mark.full   # condiction_pass, 当前超时5s代码实现为3s
    def test_caseid_111966(self):
        self.tsp_ble_slot_sync()
        sleep(2)
        self.dk.ck_white_list_update_req(2, [key_id1, key_id2, key_id3])
        self.dk.send_while_list_update_resp(0x11, 0x01, self.dk.last_sync_time_entity - 1)
        # todo: err = 1; errMsg = DelayFail; last_sync_time=T1-1

    @allure.title("更新KeyID白名单_更新成功_原三个钥匙均禁用_激活key3")
    @pytest.mark.full  # pass
    def test_caseid_111970(self):
        self.dk.auto_ack_tsp_ble_sync_cmd = False
        self.tsp_ble_slot_sync()
        sleep(2)
        self.dk.ck_white_list_update_req(2, [key_id3])
        self.dk.send_while_list_update_resp(0x11, 0x00, self.dk.last_sync_time_entity)
        # todo: err = 0; errMsg = Success; last_sync_time=T1

    @allure.title("更新KeyID白名单_更新成功_原三个钥匙均激活_禁用key1")
    @pytest.mark.full  # pass
    def test_caseid_111963(self):
        self.dk.auto_ack_tsp_ble_sync_cmd = False
        self.tsp_ble_slot_sync()
        sleep(2)
        self.dk.ck_white_list_update_req(2, [key_id2, key_id3])
        self.dk.send_while_list_update_resp(0x11, 0x00, self.dk.last_sync_time_entity)
        # todo: err = 0; errMsg = Success; last_sync_time=T1

    # @allure.title("更新KeyID白名单_更新成功_原仅key2激活_禁用key2")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111965?projectId=46')
    # @pytest.mark.full  # pass
    # def test_caseid_111965(self):
    #     self.tsp_entity_slot_sync(key_id2, 5)
    #     sleep(2)
    #     self.dk.ck_white_list_update_req(1, [key_id0])  # BNCM不支持写入全0的key，故无钥匙时云端下发写入全0的一个key
    #     self.dk.send_while_list_update_resp(0x11, 0x00, self.dk.last_sync_time_entity)
    #     # todo: err = 0; errMsg = Success; last_sync_time=T1

    @allure.title("更新KeyID白名单_更新成功_原key2和key3激活_激活key1")
    @pytest.mark.sanity  # pass
    def test_caseid_111968(self):
        self.tsp_ble_slot_sync()
        sleep(2)
        self.dk.ck_white_list_update_req(2, [key_id1, key_id2, key_id3])
        self.dk.send_while_list_update_resp(0x11, 0x00, self.dk.last_sync_time_entity)
        # todo: err = 0; errMsg = Success; last_sync_time=T1

    @allure.title("更新KeyID白名单_更新超时_原三个钥匙均激活_禁用key1")
    @pytest.mark.full  # pass
    def test_caseid_111958(self):
        self.tsp_ble_slot_sync()
        sleep(PRECHECKTI)
        self.dk.ck_white_list_update_req(2, [key_id2, key_id3])
        sleep(2)
        # todo: err = 1; errMsg = bncm timeout; last_sync_time=T1

    @allure.title("更新KeyID白名单_更新超时_原仅key3激活_禁用key3")
    @pytest.mark.full  # pass
    def test_caseid_111967(self):
        self.dk.auto_ack_tsp_ble_sync_cmd = False
        self.tsp_ble_slot_sync()
        sleep(PRECHECKTI)
        self.dk.ck_white_list_update_req(2, [key_id0])
        sleep(2)
        # todo: err = 2; errMsg = bncm timeout; last_sync_time=T1

    @allure.title("更新KeyID白名单_VFC RemoteKeyFunctionality activate for 20s")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111954?projectId=46')
    @pytest.mark.full  # pass
    def test_caseid_111954(self):
        self.nucapp.bgm_diag_line_down()
        self.nucapp.tcam_kl15_down()
        sleep(10)
        self.tsp_ble_slot_sync()
        sleep(1)
        self.ck_pnc23(1)
        # self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC23, 10, 2)
        # self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC21, 20.0, 3.0)
        # self.nm.ck_pnc(21, 1)
        sleep(21)
        self.ck_pnc23(0)

    # @allure.title("更新KeyID白名单_VFC RemoteKeyFunctionality activate for 20s")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111954?projectId=46')
    # @pytest.mark.full  # pass
    # def test_caseid_111954(self):
    #     # 模拟TSP下发更新KeyID白名单请求
    #     self.partner.send_request_and_return_resp("V2TRoutingForwarder_client_V2TOTAFotaForwarder","CallVehicleApi",{"api":'ota',
    #                                                                                             'payload': [0,1,2,3],
    #     self.bus_comm.dk.empty_dk_data_queue()

    #     self.mix.clear_pnc(BGMPNC.PNC21)
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
    #                                                                                                                                                                                     'traceId': "123"})["out"]
    #     #check BGM发送给BNCM消息

    #     #模拟BNCM发送给BGM消息

    #     # check BGM发送给Tcam消息
    #     self.partner.send_request_and_ck_resp

    # @allure.title("多个白名单控制指令_更新KeyID白名单+更新KeyID白名单")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111971?projectId=46')
    # @pytest.mark.full
    # def test_caseid_111971(self):
    #     # key1， key2，key3均处于激活状态
    #     self.tsp_entity_slot_sync(key_id1, 5)
    #     sleep(PRECHECKTI)
    #     self.dk.ck_white_list_update_req(1, [key_id2, key_id3])
    #     self.tsp_entity_slot_sync(key_id2, 5)
    #     sleep(PRECHECKTI)
    #     try:
    #         self.dk_data_queue_external.get_nowait()
    #     except Exception:
    #         pass
    #     else:
    #         assert False, "第二条指令需pending，等第一条完成后执行"
    #     self.dk.send_while_list_update_resp(0x11, 0x00, self.dk.last_sync_time_entity)
    #     # todo: err = 0; errMsg = Success; last_sync_time=T1
    #     sleep(PRECHECKTI)
    #     # self.dk.ck_white_list_update_req(1, [key_id3])
    #     self.dk.send_while_list_update_resp(0x11, 0x00, self.dk.last_sync_time_ble)
    #     # todo: err = 0; errMsg = Success; last_sync_time=T1

    # @allure.title("多个白名单控制指令_更新KeyID白名单+Slot白名单")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111959?projectId=46')
    # @pytest.mark.full
    # def test_caseid_111959(self):
    #     # key1， key2，key3均处于激活状态
    #     self.tsp_entity_slot_sync(key_id1, 5)
    #     sleep(PRECHECKTI)
    #     self.dk.ck_white_list_update_req(1, [key_id2, key_id3])
    #     self.tsp_entity_slot_sync(key_id2, 5)
    #     sleep(PRECHECKTI)
    #     try:
    #         self.dk_data_queue_external.get_nowait()
    #     except Exception:
    #         pass
    #     else:
    #         assert False, "第二条指令需pending，等第一条完成后执行"
    #     self.dk.send_while_list_update_resp(0x11, 0x00, self.dk.last_sync_time_entity)
    #     # todo: err = 0; errMsg = Success; last_sync_time=T1
    #     sleep(PRECHECKTI)
    #     self.dk.ck_white_list_update_req(2, [key_id0])
    #     self.dk.send_while_list_update_resp(0x12, 0x00, self.dk.last_sync_time_ble)
        # todo: err = 0; errMsg = Success; last_sync_time=T1

    @allure.title("多个白名单控制指令_更新KeyID白名单+更新KeyID白名单")
    @pytest.mark.full  # pass
    def test_caseid_111971(self):
        self.tsp_ble_slot_sync()
        sleep(PRECHECKTI)
        self.dk.ck_white_list_update_req(2, [key_id2, key_id3])
        self.dk.send_while_list_update_resp(0x12, 0x00, self.dk.last_sync_time_ble)

    @allure.title("更新KeyID白名单_更新成功_原仅key2激活_禁用key2")
    @pytest.mark.full  # pass
    def test_caseid_111965(self):
        self.tsp_ble_slot_sync()
        sleep(PRECHECKTI)
        self.dk.ck_white_list_update_req(2, [key_id0])
        self.dk.send_while_list_update_resp(0x12, 0x00, self.dk.last_sync_time_ble)

    @allure.title("多个白名单控制指令_更新KeyID白名单+Slot白名单")
    @pytest.mark.full
    def test_caseid_111959(self):
        # key1， key2，key3均处于激活状态
        self.tsp_ble_slot_sync()
        sleep(PRECHECKTI)
        self.dk.ck_white_list_update_req(2, [key_id2, key_id3])