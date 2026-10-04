#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_CentralLockService.py
@Time         :2023/04/08 17:20:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import allure
import pytest
import time
from time import sleep
from copy import deepcopy
from xat_ecu.legacy.common.data_type_handing import logger
from xat_cases.legacy.soa.case_helper.test_base import TestBase, write_s2s_json, s2s_path
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_ecu.legacy.interface.bgm.bgm_env.change_bgm_env import change_bgm_config, recover_bgm_config

NotifyTi = 1
KEY_MATCH_INFO = {1: [2, 3, 4, 5, 6, 8, 0xA, 0xB],
                  2: [2, 3, 4, 5, 6, 0xA, 0xB],
                  3: [3, 6, 0xA],
                  4: [4, 6, 0xB],
                  6: [8],
                  7: [8],
                  8: [8]
                  }

default_ccp_list = DataTypeHanding.hexstr_to_inlist(
    "A3018006FD030101A302090304020102858B06010004050203000001048C800C0101010102010202010216010701010100030102028089020301010302736E03010101010101010302020202020A010103820201010102020103010201800202020201800000008182118003010103020102020302800102010102010104010101010101010203010103020101830201020201012902010402038002820103040128030A800104010201020203820402810101020101130301010101010205020101000302020304020202010101020001010101010101010180030A0101040607070A0A07070A0A00000400000201010101010280030301020000000202020102020200010102000000010300000100008100000000000000000000000000000080000000000000000000000100010100000200000080000000008403010100000000020100000000000000000002018001020101010101020103020180018002020101010101050380020601030110000002030100000000000000000000000000000000000000000000000000000002000000000001010301000000000200000000000000000000000000000000000000000000000000010201000000000085040102020201020202040301020201028004030101020201030101010202020101020101010101030000000180020201010202010202020102010302020101010101010101000103010201010502020204010101010301010402010201010101020101010101010100000000000001020301010109030101010202020101030104010401010101010201030105020001010101010101010101010101010101010101010101010202010101010102010101010201000001010401000000010100000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001030202080100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001010201020102020101020101010101010201010201010101010202010201010101020202020202010202010202010201010101020101010102010101000102010101000101010101020202010101020201010101010102020102010101010101010001010101010101020101010101020101010101010101010101010101010101010101020201020101010101010100000101010101010101020101010101010101010202000101010101010202020101010100000000000000000000000000000000000000000000000000000000000000000000020202020202020101010101010101020101010101010202020202010002020101020102020201020001")


@allure.feature("SOA服务接口")
@allure.story("整车控制/CentralLockService")
@pytest.mark.aqx
class TestCentralLockService(TestBase):

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("CentralLockService", "client"),
                                     ("KeyService", "client"),
                                     ("DoorService", "client"),
                                     ("TailGateService", "client"),
                                     ("BonnetService", "client"),
                                     ])
        self.partner.method_default_timeout = 0.1
        self.io.hood_door1_close()
        self.io.hood_door2_close()
        sleep(2)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 5, "value": 0}]})
        # 抓取tcpdump
        self.bgm_tcpdump = BGM_SSH()
        self.bgm_tcpdump.init_bgm_tcpdump()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        # todo 停止抓包
        self.bgm_tcpdump.stop_bgm_tcpdump()
        # todo 删除所有 pcap 文件
        self.bgm_tcpdump.delete_bgm_tcpdump_file(bgm_log_name='*.pcap')
        super().after_class(self, ecu)  

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.set_nopeople_incar()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 8) # SWSR：507156 防止不下发关门
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'EntityKeyWhiteListVers', self.dk.last_sync_time_entity)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BLESlotKeyWhiteListVers', self.dk.last_sync_time_ble)       
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')        
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd') # MCU侧档位
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1) # MPU侧档位
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)  
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4})
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        if ecu.get("testresult") != "Pass":
            logger.info("case失败，需等待5s让环境恢复")
            sleep(5)
        else:
            sleep(3)  # 避免防玩
        super().after_each_func(ecu, start=False)
    
    def set_vehicle_speed(self,X):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', X)
        sleep(1)

    def ck_LockActTriggerSource(self, src_id, timeout=1.0):
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockActTriggerSource", {"sourceId": src_id}, timeout)
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockActTriggerSource", {},
                                              {"out": src_id})

    def ck_CentralLockStatusInfo(self, lock_sts, trigger_srcid, timeout=1):
        info1 = {"sts": lock_sts, "triggerId": trigger_srcid, "updateEve": True}
        info0 = {"sts": lock_sts, "triggerId": trigger_srcid, "updateEve": False}
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info1}, timeout)
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetCentralLockSysInfo", {}, {"out": info1})

        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info0}, timeout=1.5)
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetCentralLockSysInfo", {}, {"out": info0})

    #设置5个电动门开关状态 1表示关，0表示开
    def five_door_open_close(self, drvr_door, pass_door, rire_door, lere_door, trunk_door):
        if drvr_door == 1:
            self.io.drvr_door_close()
        else:self.io.drvr_door_open()
        if pass_door == 1:
            self.io.pass_door_close()
        else:self.io.pass_door_open()
        if rire_door == 1:
            self.io.rire_door_close()
        else:self.io.rire_door_open()
        if lere_door == 1:
            self.io.lere_door_close()
        else:self.io.lere_door_open()
        if trunk_door == 1:
            self.io.trunk_door_close()
        else:self.io.trunk_door_open()
        
    #设置五门防夹状态 1表示防夹 0表示非防夹
    def five_door_antipnch(self, drvr_door, pass_door, rire_door, lere_door, trunk_door):
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', drvr_door)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassAntiPnch', pass_door) 
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReAntiPnch', rire_door) 
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeReAntiPnch', lere_door) 
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrAntiPnch', trunk_door)
        sleep(1)
    
    #设置五门运动状态
    def five_door_sts(self, drvr_door, pass_door, rire_door, lere_door, trunk_door, sleeptime=1):
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorOpenerDrvrSts", drvr_door)  
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorOpenerPassSts', pass_door)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorOpenerRiReSts', rire_door)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorOpenerLeReSts", lere_door)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', trunk_door)
        sleep(sleeptime)
        
    #确认当前四门运动状态
    def ck_door_sts(self, drvr_door, pass_door, rire_door, lere_door, trunk_door):
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetStatus", {"doors": [4]},
                                              {"out": [{"id": 0, "sts": drvr_door},{"id": 1, "sts": pass_door},
                                                       {"id": 2, "sts": lere_door},{"id": 3, "sts": rire_door}]},timeout = 0.5)
        self.partner.send_request_and_ck_resp(TAILGATE_SERVICE_CLIENT, 
                                                    "GetStatus", {}, {"out": trunk_door},timeout = 0.5)
       
             
    @allure.title("通知整车锁状态_解锁->四门上锁且尾门上锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683154?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105271(self):
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.dk.set_cenlock_sts(3)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockStatus", {"sts": 3})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 3, timeout=0.1)

    @allure.title("通知整车锁状态_四门上锁且尾门上锁->四门上锁但尾门解锁")
    @pytest.mark.sanity
    def test_caseid_105270(self):
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 2)])
        self.dk.press_door_outswitch(5, 0.5)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockStatus", {"sts": 2})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 2, timeout=0.1)

    @allure.title("通知整车锁状态_四门上锁且尾门上锁->解锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683080?projectId=46')
    @pytest.mark.smoke
    def test_caseid_105345(self):
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.dk.set_cenlock_sts(1)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockStatus", {"sts": 1})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 1, timeout=0.1)

    @allure.title("通知整车锁状态_四门上锁但尾门解锁->四门上锁且尾门上锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/16831004?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105325(self):
        self.dk.set_cenlock_sts(2)
        sleep(1)
        self.partner.empty_all()
        self.dk.send_rke_close_door_and_lock()
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockStatus", {"sts": 3})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 3, timeout=0.1)

    @allure.title("通知整车锁状态_四门上锁但尾门解锁->解锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683156?projectId=46')
    @pytest.mark.full
    def test_caseid_105269(self):
        self.dk.set_cenlock_sts(2)
        sleep(1)
        self.partner.empty_all()
        self.dk.send_nfc_cmd()
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockStatus", {"sts": 1})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 1, timeout=0.1)

    @allure.title("通知整车锁状态_下电及休眠唤醒记忆_解锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683081?projectId=46')
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_105344(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all()
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockStatus", {"sts": 1})

        self.partner.empty_all()
        self.bgm_sleep_and_awake()
        # self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockStatus", {"sts": 1}) # todo: 休眠唤醒搞不了

    @allure.title("通知整车锁状态_下电及休眠唤醒记忆_四门上锁且尾门上锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683130?projectId=46')
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_105295(self):
        self.dk.set_cenlock_sts(3)
        self.partner.empty_all()
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockStatus", {"sts": 3})

        self.partner.empty_all()
        self.bgm_sleep_and_awake()
        # self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockStatus", {"sts": 3}) # todo: 休眠唤醒搞不了

    @allure.title("通知整车锁状态_下电及休眠唤醒记忆_四门上锁但尾门解锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683160?projectId=46')
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_105265(self):
        self.dk.set_cenlock_sts(2)
        self.partner.empty_all()
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockStatus", {"sts": 2})

        self.partner.empty_all()
        self.bgm_sleep_and_awake()
        # self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockStatus", {"sts": 2}) # todo: 休眠唤醒搞不了

    @allure.title("获取整车锁状态_解锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683111?projectId=46')
    @pytest.mark.smoke
    def test_caseid_105314(self):
        self.dk.set_cenlock_sts(1)
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, 'GetLockStatus', {}, {"out": 1})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 1, timeout=0.1)

    @allure.title("获取整车锁状态_四门上锁且尾门上锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683138?projectId=46')
    @pytest.mark.smoke
    def test_caseid_1911983(self):
        self.dk.set_cenlock_sts(3)
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, 'GetLockStatus', {}, {"out": 3})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 3, timeout=0.1)

    @allure.title("获取整车锁状态_四门上锁但尾门解锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683133?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1911986(self):
        self.dk.set_cenlock_sts(2)
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, 'GetLockStatus', {}, {"out": 2})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 2, timeout=0.1)

    @allure.title("解闭锁成功触发源_12_NFC解锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683120?projectId=46')
    @pytest.mark.smoke
    def test_caseid_105305(self):
        self.dk.send_rke_lock()
        sleep(1)
        self.partner.empty_all()
        self.dk.send_nfc_cmd()
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 12})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {},
                                              {"out": 12})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 12)

    @allure.title("解闭锁成功触发源_12_NFC闭锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105318(self):
        self.dk.send_rke_unlock()
        sleep(1)
        self.partner.empty_all()
        self.dk.send_nfc_cmd()
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 12})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {},
                                              {"out": 12})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 12)

    @allure.title("解闭锁成功触发源_12_NFC闭锁失败")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683105?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105320(self):
        self.sd_tester.change_usage_mode(2)
        self.dk.send_rke_unlock()
        self.partner.empty_all(1.5)
        self.dk.send_nfc_cmd()
        self.partner.ck_no_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource")
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 1})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 1)
        sleep(4)

    @allure.title("解闭锁成功触发源_1_RKE解锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683103?projectId=46')
    @pytest.mark.smoke
    def test_caseid_105322(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.dk.send_rke_unlock()
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 1})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 1})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 1)

    @allure.title("解闭锁成功触发源_1_RKE闭锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683088?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105337(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.dk.send_rke_lock()
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 1})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 1})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 1)

    @allure.title("解闭锁成功触发源_2_PE解锁成功")
    @pytest.mark.smoke
    def test_caseid_105285(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(4, 0.5)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 2})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 2})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 2)

    @allure.title("解闭锁成功触发源_2_PE长按闭锁成功")
    @pytest.mark.sanity
    def test_caseid_105281(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(4, 2.2)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 2})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 2})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 2)

    @allure.title("解闭锁成功触发源_3_车内按钮解锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683137?projectId=46')
    @pytest.mark.smoke
    def test_caseid_105288(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 2})
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 3})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 3})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 3)

    @allure.title("解闭锁成功触发源_3_车内按钮闭锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683162?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105263(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2})
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 3})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 3})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 3)

    @allure.title("解闭锁成功触发源_4_车速自动闭锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683148?projectId=46')
    @pytest.mark.smoke
    def test_caseid_105277(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.sd_tester.change_usage_mode(0xD)
        self.dk.set_drvr_seat_present()
        self.dk.set_four_door_unlock()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 'GenQf1_AccurData')
        self.dk.set_door_opener_sts(1, 1)
        self.dk.set_door_opener_sts(2, 1)
        self.dk.set_door_opener_sts(3, 1)
        self.dk.set_door_opener_sts(4, 1)
        self.dk.set_door_opener_sts(5, 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0x2C27)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 4})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 4})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 4)

    @allure.title("解闭锁成功触发源_5_重上锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683128?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105297(self):
        logger.info("硬线J3-36接地(内部信号HoodSwt1")
        self.io.set_do_level("hood_ajar_2", True)
        sleep(1)
        logger.info("硬线J3-37接地(内部信号HoodSwt2)")
        self.io.set_do_level("hood_ajar_1", True)
        sleep(1)
        logger.info("Step:使硬线J3-36悬空")
        self.io.set_do_level("hood_ajar_2", False)

        self.dk.set_cenlock_sts(1)
        self.dk.send_rke_lock()
        sleep(1)
        self.dk.send_rke_unlock()
        sleep(1)

        # self.dk.set_cenlock_sts(1)
        # sleep(1)
        # self.dk.send_rke_lock()
        # # sleep(2)
        # # self.dk.ck_cenlock_sts(3)
        # self.dk.send_rke_unlock()
        # # sleep(2)
        # # self.dk.ck_cenlock_sts(1)
        # sleep(1)
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 1})  #获取前舱盖状态 1=关闭 0=打开
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 1})  #获取前舱盖状态 1=关闭 0=打开
        self.partner.send_request_and_ck_resp(TAILGATE_SERVICE_CLIENT, "GetOpenCloseStatusValidity", {}, {"out": {"value": False, "validity": 0}})  #尾门开关状态 false关 true打开
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetOpenCloseStatusValidity", {"doors": [4]},
                                                  {"out": [{"value":{"id":0,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":1,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":2,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":3,"isOpen":False},"isOpenValidity":0}]}) # DoorAll false关
        self.partner.empty_all()
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 5}, 31)
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 5})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 5)

    @allure.title("解闭锁成功触发源_7_远程解锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683153?projectId=46')
    @pytest.mark.smoke
    def test_caseid_105272(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 1})
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 7})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 7})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 7)

    @allure.title("解闭锁成功触发源_7_远程闭锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683095?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105330(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1})
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 7})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 7})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 7)

    @allure.title("解闭锁成功触发源_8_Crash解锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683116?projectId=46')
    @pytest.mark.smoke
    def test_caseid_105309(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.sd_tester.change_car_mode(0x3)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 8})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 8})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 8)

    @allure.title("解闭锁成功触发源_9_近车解锁成功")
    @allure.testcase('test_caseid_1911930')
    @pytest.mark.sanity
    def test_caseid_105298(self):
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 1, "value": 1}]})
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.dk.send_approach_unlock_cmd()
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 9})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 9})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 9)

    @allure.title("解闭锁成功触发源_9_离车自动闭锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683121?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105304(self):
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.dk.send_walk_away_lock_cmd()
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 9})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 9})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 9)

    @allure.title("解闭锁成功触发源_10_外部的其他方式闭锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683098?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105327(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3})
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 10})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {},
                                              {"out": 10})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 10)

    @allure.title("解闭锁成功触发源_11_内部的其他方式解锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683141?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105284(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 3})
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 11})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {},
                                              {"out": 11})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 11)

    @allure.title("解闭锁成功触发源_11_内部的其他方式闭锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683109?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105316(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 3})
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 11})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {},
                                              {"out": 11})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 11)

    @allure.title("解闭锁成功触发源_sourceId不跳变")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683104?projectId=46')
    @pytest.mark.full
    def test_caseid_105321(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.partner.empty_all()
        self.dk.send_nfc_cmd()
        self.partner.ck_no_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource")
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {},
                                              {"out": 12})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 12)

    @allure.title("解闭锁动作触发源_1_RKE解锁成功")    
    @pytest.mark.sanity
    def test_caseid_105328(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.dk.send_rke_unlock()
        try:
            self.ck_LockActTriggerSource(1)
            self.ck_LockActTriggerSource(0)
        except Exception as e:
            self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 1})
            pass       
        
    @allure.title("解闭锁动作触发源_1_RKE闭锁失败")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683161?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105264(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.sd_tester.change_usage_mode(2)
        self.dk.send_rke_lock()
        self.ck_LockActTriggerSource(1)
        self.ck_LockActTriggerSource(0)
        sleep(5)

    @allure.title("解闭锁动作触发源_2_PE解锁成功")
    @pytest.mark.sanity
    def test_caseid_105341(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(4, 0.5)
        try:
            self.ck_LockActTriggerSource(2)
            self.ck_LockActTriggerSource(0)
        except Exception as e:
            self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 2})
            pass   

    @allure.title("解闭锁动作触发源_2_PE长按闭锁失败")
    @pytest.mark.full
    def test_caseid_105331(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.sd_tester.change_usage_mode(2)
        self.dk.press_door_outswitch(4, 2.01)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr38, 'LockgEventTrigsrc', 2)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockActTriggerSource", {"sourceId": 2}, timeout=1)
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockActTriggerSource", {},
                                              {"out": 2})
        self.ck_LockActTriggerSource(0)
        sleep(5)

    @allure.title("解闭锁动作触发源_3_车内按钮解锁成功")    
    @pytest.mark.sanity
    def test_caseid_105276(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 2})
        try:
            self.ck_LockActTriggerSource(3)
            self.ck_LockActTriggerSource(0)
        except Exception as e:
            self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 3})
            pass  

    @allure.title("解闭锁动作触发源_3_车内按钮闭锁失败")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683118?projectId=46')
    @pytest.mark.full
    def test_caseid_105307(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2})
        self.ck_LockActTriggerSource(3)
        self.ck_LockActTriggerSource(0)
        sleep(5)

    @allure.title("解闭锁动作触发源_4_车速自动闭锁失败")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683117?projectId=46')
    @pytest.mark.full
    def test_caseid_105308(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.dk.set_drvr_seat_present()
        self.dk.set_four_door_unlock()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 'GenQf1_AccurData')
        self.dk.set_door_opener_sts(1, 1)
        self.dk.set_door_opener_sts(2, 1)
        self.dk.set_door_opener_sts(3, 1)
        self.dk.set_door_opener_sts(4, 1)
        self.dk.set_door_opener_sts(5, 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0x2C27)
        self.ck_LockActTriggerSource(4, timeout=2)
        self.ck_LockActTriggerSource(0)

    @allure.title("解闭锁动作触发源_5_重上锁失败")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683113?projectId=46')
    @pytest.mark.full
    def test_caseid_105312(self):
        logger.info("硬线J3-36接地(内部信号HoodSwt1")
        self.io.set_do_level("hood_ajar_2", True)
        sleep(1)
        logger.info("硬线J3-37接地(内部信号HoodSwt2)")
        self.io.set_do_level("hood_ajar_1", True)
        sleep(1)
        logger.info("Step:使硬线J3-36悬空")
        self.io.set_do_level("hood_ajar_2", False)

        self.dk.set_cenlock_sts(1)
        self.dk.send_rke_lock()
        sleep(1)
        self.dk.send_rke_unlock()
        sleep(1)
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 1})  #获取前舱盖状态 1=关闭 0=打开
        self.partner.send_request_and_ck_resp(TAILGATE_SERVICE_CLIENT, "GetOpenCloseStatusValidity", {}, {"out": {"value": False, "validity": 0}})  #尾门开关状态 false关 true打开
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetOpenCloseStatusValidity", {"doors": [4]},
                                                  {"out": [{"value":{"id":0,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":1,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":2,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":3,"isOpen":False},"isOpenValidity":0}]}) # DoorAll false关
        self.partner.empty_all()
        self.sd_tester.change_usage_mode(2)
        self.sd_tester.tester_present() # 一直发3e80  保持会话
        try:
            self.ck_LockActTriggerSource(5, timeout=31)
            self.ck_LockActTriggerSource(0)
        except Exception as e:
            self.sd_tester.stop_tester_present()
            assert False, e
        else:
            self.sd_tester.stop_tester_present()

    @allure.title("解闭锁动作触发源_7_远程解锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683143?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105282(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 1})
        self.ck_LockActTriggerSource(7)
        self.ck_LockActTriggerSource(0)

    @allure.title("解闭锁动作触发源_7_远程闭锁失败")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683131?projectId=46')
    @pytest.mark.full
    def test_caseid_105294(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1})
        self.ck_LockActTriggerSource(7)
        self.ck_LockActTriggerSource(0)
        sleep(5)

    @allure.title("解闭锁动作触发源_8_Crash解锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683086?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105339(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.sd_tester.enter_extended_session()
        sleep(0.1)
        self.sd_tester.security_access_level_l2()
        self.sd_tester.io_control_car_mode_control(3)
        self.ck_LockActTriggerSource(8)
        self.ck_LockActTriggerSource(0)
        sleep(5)

    @allure.title("解闭锁动作触发源_9_近车解锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683101?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105324(self):
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 1, "value": 1}]})
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.dk.send_approach_unlock_cmd()
        self.ck_LockActTriggerSource(9)
        self.ck_LockActTriggerSource(0)

    @allure.title("解闭锁动作触发源_9_离车自动闭锁失败")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683091?projectId=46')
    @pytest.mark.full
    def test_caseid_105334(self):
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.set_vehicle_speed(0.0)
        self.sd_tester.change_usage_mode(2)
        self.dk.send_walk_away_lock_cmd()
        self.ck_LockActTriggerSource(9)
        self.ck_LockActTriggerSource(0)

    @allure.title("解闭锁动作触发源_10_外部的其他方式闭锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683115?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1912014(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.set_vehicle_speed(0.0)
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3})
        self.ck_LockActTriggerSource(10)
        self.ck_LockActTriggerSource(0)

    @allure.title("解闭锁动作触发源_11_内部的其他方式解锁成功")
    @pytest.mark.sanity
    def test_caseid_105266(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 3})
        # self.ck_LockActTriggerSource(11)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockActTriggerSource", {"sourceId": 11}, timeout=1.0)
        self.ck_LockActTriggerSource(0)

    @allure.title("解闭锁动作触发源_12_内部的其他方式闭锁失败")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683090?projectId=46')
    @pytest.mark.full
    def test_caseid_105335(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.set_vehicle_speed(0.0)
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 3})
        self.ck_LockActTriggerSource(11)
        self.ck_LockActTriggerSource(0)

    @allure.title("解闭锁动作触发源_12_NFC解锁成功")    
    @pytest.mark.sanity
    def test_caseid_105273(self):
        self.dk.send_rke_lock()
        self.partner.empty_all(1)
        self.dk.send_nfc_cmd()
        try:
            self.ck_LockActTriggerSource(12)
            self.ck_LockActTriggerSource(0)
        except Exception as e:
            self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 12})
            pass  

    @allure.title("解闭锁动作触发源_12_NFC闭锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683145?projectId=46')
    @pytest.mark.full
    def test_caseid_105280(self):
        self.dk.send_rke_unlock()
        sleep(1)
        self.partner.empty_all()
        self.sd_tester.change_usage_mode(2)
        self.dk.send_nfc_cmd()
        self.ck_LockActTriggerSource(12)
        self.ck_LockActTriggerSource(0)

    @allure.title("设置整车上锁解锁_RKE解锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683129?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105296(self):
        self.dk.set_cenlock_sts(0x3)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 0})
        sleep(1)
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.ck_cenlock_sts(0x1, 0x1)

    @allure.title("设置整车上锁解锁_RKE闭锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683083?projectId=46')
    @pytest.mark.smoke
    def test_caseid_105342(self):
        self.dk.set_cenlock_sts(0x1)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 0})
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.ck_cenlock_sts(0x3, 0x1)

    @allure.title("设置整车上锁解锁_RKE关门且闭锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683147?projectId=46')
    @pytest.mark.full
    def test_caseid_105278(self):
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        self.dk.set_door_opener_sts(1, 5, 1, 1, 1)
        time.sleep(1)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 0})
        self.dk.ck_door_opener_cmd(2, 2, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.ck_cenlock_sts(0x3, 0x1)

    @allure.title("设置整车上锁解锁_远控解锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683123?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105302(self):
        self.dk.set_cenlock_sts(0x3)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 1})
        sleep(1)
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.ck_cenlock_sts(0x1, 0x7)

    @allure.title("设置整车上锁解锁_远控闭锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683082?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105343(self):
        self.dk.set_cenlock_sts(0x1)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1})
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.ck_cenlock_sts(0x3, 0x7)

    @allure.title("设置整车上锁解锁_远控关门且闭锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683134?projectId=46')
    @pytest.mark.full
    def test_caseid_105291(self):
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        self.dk.set_door_opener_sts(1, 5, 1, 1, 1)
        sleep(1)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 1})
        self.dk.ck_door_opener_cmd(2, 2, 3)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.ck_cenlock_sts(0x3, 0x7)

    @allure.title("设置整车上锁解锁_HMI解锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683114?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105311(self):
        self.dk.set_cenlock_sts(0x3)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 2})
        sleep(1)
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.ck_cenlock_sts(0x1, 0x3)

    @allure.title("设置整车上锁解锁_HMI闭锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683102?projectId=46')
    @pytest.mark.full
    def test_caseid_105323(self):
        self.dk.set_cenlock_sts(0x1)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2})
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.ck_cenlock_sts(0x3, 0x3)

    @allure.title("设置整车上锁解锁_Others解锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683099?projectId=46')
    @pytest.mark.full
    def test_caseid_105326(self):
        self.dk.set_cenlock_sts(0x3)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 3})
        sleep(1)
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.ck_cenlock_sts(0x1, 0xB)

    @allure.title("设置整车上锁解锁_Others闭锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683093?projectId=46')
    @pytest.mark.full
    def test_caseid_105332(self):
        self.dk.set_cenlock_sts(0x1)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 3})
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.ck_cenlock_sts(0x3, 0xB)

    @allure.title("设置整车上锁解锁_Others闭锁且设防")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683139?projectId=46')
    @pytest.mark.full
    def test_caseid_105286(self):
        self.dk.set_cenlock_sts(0x1)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3})
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.ck_cenlock_sts(0x3, 0xA)

    @allure.title("触发中控解闭锁动作事件更新状态_解锁")
    @pytest.mark.sanity
    def test_caseid_105315(self):
        self.dk.set_cenlock_sts(0x3)
        self.partner.empty_all(1.5)
        self.dk.send_nfc_cmd()
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CenLckUpdEve", {"sts": 1})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetCenLckUpdEve", {}, {"out": 1})
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CenLckUpdEve", {"sts": 0})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetCenLckUpdEve", {}, {"out": 0}, timeout=3)

    @allure.title("触发中控解闭锁动作事件更新状态_闭锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683122?projectId=46')
    @pytest.mark.full
    def test_caseid_105303(self):
        self.dk.set_cenlock_sts(0x1)
        self.partner.empty_all(2)
        self.dk.send_nfc_cmd()
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CenLckUpdEve", {"sts": 1})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetCenLckUpdEve", {}, {"out": 1})
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CenLckUpdEve", {"sts": 0})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetCenLckUpdEve", {}, {"out": 0})

    @allure.title("中控锁状态提醒_1_锁车失败，需要NFC长刷")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683132?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105293(self):
        self.dk.set_cenlock_sts(0x1)
        sleep(1)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_Detected')
        self.dk.send_nfc_cmd()
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_NotDetected')
        # self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr21, 'LockSysStsPrmt', 1)  # todo: 3帧1之后变0捕捉不到
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"reminder": 1})
        # self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetCentralLockReminder", {}, {"out": 1}) # 报完1后回0，批量跑会存在get不到1的情况
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"reminder": 0}, timeout=1)
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetCentralLockReminder", {}, {"out": 0})

    @allure.title("中控锁状态提醒_3_未检测到钥匙")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683150?projectId=46')
    @pytest.mark.full
    def test_caseid_105275(self):
        self.dk.set_cenlock_sts(0x1)
        self.partner.empty_all()
        self.dk.press_door_outswitch(1, 2.005)
        # self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr21, 'LockSysStsPrmt', 3)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"reminder": 3})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetCentralLockReminder", {}, {"out": 3})
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"reminder": 0}, timeout=1)
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetCentralLockReminder", {}, {"out": 0})

    @allure.title("中控锁系统状态_1_RKE解锁成功")
    @pytest.mark.full
    def test_caseid_105333(self):
        self.dk.set_cenlock_sts(3)
        self.partner.empty_all(1)
        self.dk.send_rke_unlock()
        self.dk.ck_cenlock_sts(1, 1)
        self.ck_CentralLockStatusInfo(1, 1)
        
    @allure.title("中控锁系统状态_1_重启后RKE解锁成功")
    @pytest.mark.full
    def test_caseid_1984080(self):
        self.dk.set_cenlock_sts(3)
        self.partner.empty_all(2)
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        self.dk.send_rke_unlock()
        info0 = {"sts": 3, "triggerId": 12, "updateEve": False}
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info0})
        info1 = {"sts": 1, "triggerId": 1, "updateEve": True}
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info1})
        info2 = {"sts": 1, "triggerId": 1, "updateEve": False}
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info2})
        self.partner.ck_no_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo")
        
    @allure.title("中控锁系统状态_1_RKE闭锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683106?projectId=46')
    @pytest.mark.full
    def test_caseid_105319(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all()
        self.dk.send_rke_lock()
        self.dk.ck_cenlock_sts(3, 1)
        self.ck_CentralLockStatusInfo(3, 1)

    @allure.title("中控锁系统状态_2_PE解锁成功")
    @pytest.mark.sanity
    def test_caseid_1918642(self):
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(4, 0.5)
        self.ck_CentralLockStatusInfo(1, 2)

    @allure.title("中控锁系统状态_2_PE长按闭锁成功")
    @pytest.mark.full
    def test_caseid_105299(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all()
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(4, 2.2)
        self.ck_CentralLockStatusInfo(3, 2)

    @allure.title("中控锁系统状态_3_车内按钮解锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683089?projectId=46')
    @pytest.mark.full
    def test_caseid_105336(self):
        self.dk.set_cenlock_sts(3)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 2})
        self.ck_CentralLockStatusInfo(1, 3)

    @allure.title("中控锁系统状态_3_车内按钮闭锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683125?projectId=46')
    @pytest.mark.full
    def test_caseid_105300(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2})
        self.ck_CentralLockStatusInfo(3, 3)

    @allure.title("中控锁系统状态_4_车速自动闭锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683142?projectId=46')
    @pytest.mark.full
    def test_caseid_105283(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all()
        self.set_vehicle_speed(0.0)
        self.sd_tester.change_usage_mode(0xD)
        self.dk.set_drvr_seat_present()
        self.dk.set_four_door_unlock()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 'GenQf1_AccurData')
        self.dk.set_door_opener_sts(1, 1)
        self.dk.set_door_opener_sts(2, 1)
        self.dk.set_door_opener_sts(3, 1)
        self.dk.set_door_opener_sts(4, 1)
        self.dk.set_door_opener_sts(5, 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0x2C27)
        self.ck_CentralLockStatusInfo(3, 4)
        sleep(5)

    @allure.title("中控锁系统状态_5_重上锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683157?projectId=46')
    @pytest.mark.full
    def test_caseid_105268(self):
        logger.info("硬线J3-36接地(内部信号HoodSwt1")
        self.io.set_do_level("hood_ajar_2", True)
        sleep(1)
        logger.info("硬线J3-37接地(内部信号HoodSwt2)")
        self.io.set_do_level("hood_ajar_1", True)
        sleep(1)

        logger.info("Step:使硬线J3-36悬空")
        self.io.set_do_level("hood_ajar_2", False)

        self.dk.set_cenlock_sts(1)
        self.dk.send_rke_lock()
        sleep(1)
        self.dk.send_rke_unlock()
        sleep(1)
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 1})  #获取前舱盖状态 1=关闭 0=打开
        self.partner.send_request_and_ck_resp(TAILGATE_SERVICE_CLIENT, "GetOpenCloseStatusValidity", {}, {"out": {"value": False, "validity": 0}})  #尾门开关状态 false关 true打开
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetOpenCloseStatusValidity", {"doors": [4]},
                                                  {"out": [{"value":{"id":0,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":1,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":2,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":3,"isOpen":False},"isOpenValidity":0}]}) # DoorAll false关
        self.partner.empty_all()
        self.ck_CentralLockStatusInfo(3, 5, timeout=31)

    @allure.title("中控锁系统状态_7_远程解锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683119?projectId=46')
    @pytest.mark.full
    def test_caseid_105306(self):
        self.dk.set_cenlock_sts(3)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 1})
        self.ck_CentralLockStatusInfo(1, 7)

    @allure.title("中控锁系统状态_7_远程闭锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683087?projectId=46')
    @pytest.mark.smoke
    def test_caseid_105338(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1})
        # self.ck_CentralLockStatusInfo(3, 7)
        info1 = {"sts": 3, "triggerId": 7, "updateEve": True}
        info0 = {"sts": 3, "triggerId": 7, "updateEve": False}
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info1}, timeout=3)
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetCentralLockSysInfo", {}, {"out": info1})

        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info0}, timeout=3)
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetCentralLockSysInfo", {}, {"out": info0})

    @allure.title("中控锁系统状态_8_Crash解锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683124?projectId=46')
    @pytest.mark.full
    def test_caseid_105301(self):
        self.dk.set_cenlock_sts(3)
        self.partner.empty_all()
        self.set_vehicle_speed(0.0)
        self.sd_tester.change_car_mode(0x3)
        self.ck_CentralLockStatusInfo(1, 8)

    @allure.title("中控锁系统状态_9_近车解锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683135?projectId=46')
    @pytest.mark.full
    def test_caseid_1911930(self):
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 1, "value": 1}]})
        self.dk.set_cenlock_sts(3)
        self.partner.empty_all()
        self.dk.send_approach_unlock_cmd()
        self.ck_CentralLockStatusInfo(1, 9)

    @allure.title("中控锁系统状态_9_离车自动闭锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683136?projectId=46')
    @pytest.mark.full
    def test_caseid_105289(self):
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.send_walk_away_lock_cmd()
        self.ck_CentralLockStatusInfo(3, 9)

    @allure.title("中控锁系统状态_10_外部的其他方式闭锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683085?projectId=46')
    @pytest.mark.full
    def test_caseid_105340(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3})
        self.ck_CentralLockStatusInfo(3, 10)

    @allure.title("中控锁系统状态_11_内部的其他方式解锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683146?projectId=46')
    @pytest.mark.full
    def test_caseid_105279(self):
        self.dk.set_cenlock_sts(3)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 3})
        self.ck_CentralLockStatusInfo(1, 11)

    @allure.title("中控锁系统状态_11_内部的其他方式闭锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683151?projectId=46')
    @pytest.mark.full
    def test_caseid_105274(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 3})
        self.ck_CentralLockStatusInfo(3, 11)

    @allure.title("中控锁系统状态_NFC解锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683158?projectId=46')
    @pytest.mark.full
    def test_caseid_105267(self):
        self.dk.set_cenlock_sts(3)
        self.partner.empty_all(1.5)
        self.dk.send_nfc_cmd()
        self.ck_CentralLockStatusInfo(1, 12)

    @allure.title("中控锁系统状态_12_NFC闭锁成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683096?projectId=46')
    @pytest.mark.full
    def test_caseid_105329(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all()
        self.dk.send_nfc_cmd()
        self.ck_CentralLockStatusInfo(3, 12)

    @allure.title("下行PDU_SetDoorCloseLock_多帧报文验证")
    @pytest.mark.full
    def test_caseid_1912609(self): 
        file_path, save_name = self.bgm_tcpdump.start_bgm_tcpdump()        
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2}) 
        # S2S发送一帧CenLockHmiReq=2 = LockgCenReq2_Lock, 间隔100ms，发送一帧CenLockHmiReq=0 = LockgCenReq2_Idle；
        sleep(5)        
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 0}) 
        #   kUnlock时，S2S发送一帧MobDevCenLockReq=1 = Unlock, 间隔100ms，发送一帧MobDevCenLockReq=0 = No Request；
        sleep(5)        
         # todo 停止抓包
        self.bgm_tcpdump.stop_bgm_tcpdump()
        # todo 拉取日志 单个日志 不打包
        file_path=self.bgm_tcpdump.scp_bgm_log_to_local(bgm_log_name=save_name)
        # todo 删除所有 pcap 文件
        self.bgm_tcpdump.delete_bgm_tcpdump_file(bgm_log_name='*.pcap')
        
        #停止和删除 也在aftercase中增加进去
        # 列表里面为元祖（pdu的id，数据长度，信号起始bit位，信号长度，信号值），可以 是多个元祖
        data_list = [(5406, 1, 1, 2, 2),(5406, 1, 1, 2, 0),(6353, 1, 2, 3, 1),(6353, 1, 2, 3, 0)]
        ret, res_dict = check_pdu(data_list, file_path)
        if ret==False :
             assert False, f"对应信号不存在"             
        
        # data_list 格式 为列表，列表里面为元祖（pdu的id，数据长度，信号起始bit未，信号长度），可以 是多个元祖
        data_list = [(5406, 1, 1, 2),(6353, 1, 2, 3)]
        res_dict=get_pdu_value_and_time(data_list, file_path)    
        
    @allure.title("设置整车上锁解锁_APA闭锁设防&不寻钥匙")
    @pytest.mark.full
    def test_caseid_1983162(self): # central_lock_service_imp
        self.dk.set_cenlock_sts(0x1)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3, "findKeyType":0}) #若未传参，默认findKeyType=0
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.ck_cenlock_sts(0x3, 0xA)
        self.dk.ck_bgm_not_send_cmd("请求Idle=0无效", self.dk.dk_data_queue_key_search)
        
    @allure.title("设置整车上锁解锁_APA闭锁设防&车外寻钥匙_2s内寻到钥匙")
    @pytest.mark.full
    def test_caseid_1983164(self): 
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)]) 
        self.dk.set_cenlock_sts(0x1)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3, "findKeyType":1})
        self.dk.ck_search_key_req(1, 6)
        self.dk.ck_cenlock_sts(0x3, 0xA)

    @allure.title("设置整车上锁解锁_APA闭锁设防&车外寻钥匙_2s内未寻到钥匙")
    @pytest.mark.full
    def test_caseid_1983168(self):  
        self.dk.set_cenlock_sts(0x1)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3, "findKeyType":1})
        self.dk.ck_search_key_req(1, 6)
        self.dk.ck_cenlock_sts(0x1, 0xC)
        
    @allure.title("设置整车上锁解锁_APA闭锁设防&车内寻钥匙_2s内寻到钥匙")
    @pytest.mark.full
    def test_caseid_1983170(self): 
        self.dk.set_cenlock_sts(0x1)        
        self.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)]) # Location=6，status=8
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3, "findKeyType":2})        
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.ck_search_key_req(6, 6)
        self.dk.ck_cenlock_sts(0x3, 0xA)
        
    @allure.title("设置整车上锁解锁_APA闭锁设防&车内寻钥匙_2s内未寻到钥匙")
    @pytest.mark.full
    def test_caseid_1983171(self): 
        self.dk.set_cenlock_sts(0x1)   
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3, "findKeyType":2})
        self.dk.ck_search_key_req(6, 6)
        self.dk.ck_cenlock_sts(0x1, 0xC)        
        
    @allure.title("设置整车上锁解锁_APA闭锁设防&车外和车内寻钥_车外未寻到钥匙")
    @pytest.mark.full
    def test_caseid_1983173(self): 
        self.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)]) # 仅车内有钥匙
        self.dk.set_cenlock_sts(0x1)   
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3, "findKeyType":3})
        self.dk.ck_search_key_req(1, 6)
        self.dk.ck_cenlock_sts(0x1, 0xC) 
        
    @allure.title("设置整车上锁解锁_APA闭锁设防&车外和车内寻钥_车外寻到钥匙&车内未寻到钥匙")
    @pytest.mark.full
    def test_caseid_1983174(self): 
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])  # 仅车外有钥匙
        self.dk.set_cenlock_sts(0x1)           
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3, "findKeyType":3})
        self.dk.ck_search_key_req(1, 6)
        self.dk.ck_search_key_req(6, 6, timeout=3)
        self.dk.ck_cenlock_sts(0x1, 0xC)    

    @allure.title("设置整车上锁解锁_APA闭锁设防&车外和车内寻钥_车外寻到钥匙&车内寻到钥匙")
    @pytest.mark.sanity
    def test_caseid_1983175(self): 
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)]) 
        self.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])
        self.dk.set_cenlock_sts(0x1)  
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3, "findKeyType":3})
        self.dk.ck_search_key_req(1, 6)
        self.dk.ck_search_key_req(6, 6, timeout=3)
        self.dk.ck_four_door_lock_cmd(2, timeout=3) 
        self.dk.ck_cenlock_sts(0x3, 0xA, timeout=3)
              
    @allure.title("设置整车上锁解锁_APA闭锁设防_2s内多次调用不响应")
    @pytest.mark.full
    def test_caseid_1983177(self): 
        self.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)]) # 仅车内有钥匙
        self.dk.set_cenlock_sts(0x1)     
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3, "findKeyType":2}) # 车内
        sleep(0.1)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3, "findKeyType":1}) # 车外
        try: 
            self.dk.ck_search_key_req(1, 6)
        except Exception as e:
            pass
        else:
            assert False, "不应该有车外寻钥匙请求"
        self.dk.ck_cenlock_sts(0x3, 0xA)  

    @allure.title("启动场景event")
    @pytest.mark.full
    def test_caseid_1984745(self):
        self.dk.set_cenlock_sts(3)
        self.partner.empty_all(3)
        self.dk.send_rke_unlock()
        self.ck_CentralLockStatusInfo(1, 1) # NotifyCentralLockSysInfo
        self.partner.empty_all(10)
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        # 通知解闭锁动作触发源
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockActTriggerSource", {"sourceId": 0}) # LockgEventTrigsrc
        # 通知解闭锁成功触发源
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 1}) # LockgCenStsTrigSrc
        # 通知整车锁状态
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockStatus", {"sts": 1})
        # 通知中控锁状态提醒
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"reminder": 0}) # LockSysStsPrmt
        # 通知触发中控解闭锁动作事件更新状态
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CenLckUpdEve", {"sts": 0})
        # 通知中控锁系统状态
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", 
                                  {"info": {"sts": 1, "triggerId": 1, "updateEve": False}})
             
    @allure.title("设置整车上锁解锁10s内_调用后五门全关_下发闭锁")
    @pytest.mark.sanity
    def test_caseid_1985439(self): 
        self.five_door_antipnch(0,0,0,0,0)
        self.five_door_sts(0,0,0,0,0)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 2})
        t1 = time.time()
        logger.error(f"t1 = {t1}")
        sleep(8)
        self.five_door_sts(1,1,1,1,1)
        self.ck_door_sts(2,2,2,2,2)
        self.partner.send_request_and_ck_resp(TAILGATE_SERVICE_CLIENT, "GetLiftgateSysSts", {}, {"out": {"isAntiPinchOn": False,"motionSts": 1}})
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()        
        result = self.bgm_eth_inter.get_signal_items("CenLockHmiReq")
        logger.error(f"result = {result}")
        t2 = result[0][1]
        self.bgm_eth_inter.ck_period_time("CenLockHmiReq",period=0.1)
        assert (result[0][2]== [2] and result[1][2]) == 0
        assert float(t2) - float(t1) < 10

    @allure.title("设置整车上锁解锁_副驾和左后悬停状态_调用set后关副驾_10s内关五门_下发闭锁")
    @pytest.mark.sanity
    def test_caseid_1986220(self): # 可在200BP复现问题   
        self.bgm_eth_inter.start_bgm_tcpdump()     
        self.dk.set_door_opener_sts(1, 2, 4, 1, 1) 
        sleep(1)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 2})
        sleep(5)
        self.dk.set_door_opener_sts(1, 1, 4, 1, 1)
        sleep(1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1) 
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [2, 0]) 

    @allure.title("设置整车上锁解锁_五门全关后调用")
    @pytest.mark.full
    def test_caseid_1985889(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(2)
        self.five_door_antipnch(0,0,0,0,0)
        self.five_door_sts(1,1,1,1,1)
        self.ck_door_sts(2,2,2,2,2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 2})
        self.dk.ck_cenlock_sts(0x3, 0x3)   # 五门全关时调用set 会立即闭锁 此时校验不到关门指令 
        
    @allure.title("设置整车上锁解锁_五门依次关闭")
    @pytest.mark.full
    def test_caseid_1985890(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(2)
        self.five_door_antipnch(0,0,0,0,0)        
        self.five_door_sts(0,0,0,0,0)
        list1=[0,0,0,0,0]
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 2})
        self.dk.ck_door_opener_cmd(1, 2) #校验关门指令
        self.dk.ck_door_opener_cmd(2, 2)
        self.dk.ck_door_opener_cmd(3, 2)
        self.dk.ck_door_opener_cmd(4, 2)
        self.dk.ck_door_opener_cmd(5, 2)
        for i in range(4):
            list1[i]=1
            self.five_door_sts(list1[0], list1[1], list1[2], list1[3], list1[4], sleeptime=0)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 1, timeout=2)
        self.five_door_sts(1,1,1,1,1)  
        self.dk.ck_cenlock_sts(0x3, 0x3)     
                 
    @allure.title("设置整车上锁解锁10s超时_五门中任意门未关")
    @pytest.mark.full
    def test_caseid_1985441(self): 
        self.five_door_antipnch(0,0,0,0,0)        
        self.five_door_sts(1,1,1,1,1)
        self.ck_door_sts(2,2,2,2,2)
        self.partner.send_request_and_ck_resp(TAILGATE_SERVICE_CLIENT, "GetLiftgateSysSts", {}, {"out": {"isAntiPinchOn": False,"motionSts": 1}})
        dic ={0:"Drvr", 1:"Pass", 2:"RiRe", 3:"LeRe",}
        self.bgm_eth_inter.start_bgm_tcpdump()
        #[0,2,3,4,5,6,7,8,9,10]选择其中几个 否则pcap解析会花费很长时间
        for i in [0,5,10]:
            self.five_door_sts(1,1,1,1,1)
            self.ck_door_sts(2,2,2,2,2)
            for door_id, door_sig in dic.items():
                self.ipdu.set(eval(f"self.ipdu.bodycan.{door_sig[0:1]}podBodyFr01"), f'DoorOpener{door_sig}Sts', i)
                sleep(0.5)
                self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 2, "findKeyType":1})
                sleep(10.2)         
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', i)
            sleep(0.5)
            self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 2})
            sleep(10.2)  
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [])  
      
    @allure.title("设置整车上锁解锁_10s被打断后重新触发")
    @pytest.mark.full
    def test_caseid_1985443(self): 
        self.five_door_antipnch(0,0,0,0,0)
        self.five_door_sts(0,0,0,0,0)
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 2, "findKeyType":1})
        self.five_door_sts(1,1,1,1,1)
        self.ck_door_sts(2,2,2,2,2)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [2,0])
        self.bgm_eth_inter.ck_period_time("CenLockHmiReq",period=0.1)
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.five_door_antipnch(0,0,0,0,0)
        self.five_door_sts(0,0,0,0,0)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 2, "findKeyType":1})
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrAntiPnch', 1) 
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrAntiPnch', 0)
        sleep(0.5)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 2, "findKeyType":1})
        sleep(9)
        self.five_door_sts(1,1,1,1,1)
        #防止抓包停止太早，校验不到数据
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [2,0])
        self.bgm_eth_inter.ck_period_time("CenLockHmiReq",period=0.1)
        
    @allure.title("设置整车上锁解锁_任意一个电动门运动状态由其他值跳变为正在开启中或悬停状态")
    @pytest.mark.full
    def test_caseid_1985444(self): 
        self.five_door_antipnch(0,0,0,0,0)
        self.five_door_sts(0,0,0,0,0)        
        dic ={0:"Drvr", 1:"Pass", 2:"RiRe", 3:"LeRe",}
        self.bgm_eth_inter.start_bgm_tcpdump()
        for i in [2,4]:
            for door_id, door_sig in dic.items():
                self.five_door_sts(0,0,0,0,0)
                self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 2, "findKeyType":1})
                self.ipdu.set(eval(f"self.ipdu.bodycan.{door_sig[0]}podBodyFr01"), f'DoorOpener{door_sig}Sts', i)
                sleep(1)
                self.five_door_sts(1,1,1,1,1)
                self.ck_door_sts(2,2,2,2,2)
                sleep(10.2) 
            #尾门从其他值跳到悬停不会取消定时器
            self.five_door_sts(0,0,0,0,0)
            self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 2, "findKeyType":1})  
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', i)
            sleep(0.5)
            self.five_door_sts(1,1,1,1,1)
            self.ck_door_sts(2,2,2,2,2)
            sleep(10.1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [2,0,2,0]) 
            
    @allure.title("设置整车上锁解锁_触发防夹")
    @pytest.mark.full
    def test_caseid_1985445(self): 
        self.five_door_antipnch(0,0,0,0,0)
        self.five_door_sts(0,0,0,0,0)
        
        dic ={0:"Drvr", 1:"Pass", 2:"RiRe", 3:"LeRe",}
        self.bgm_eth_inter.start_bgm_tcpdump()
        for door_id, door_sig in dic.items():
            self.five_door_sts(0,0,0,0,0)
            self.five_door_antipnch(0,0,0,0,0)
            sleep(0.5)
            self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 2, "findKeyType":1})
            self.ipdu.set(eval(f"self.ipdu.bodycan.{door_sig[0]}podBodyFr01"), f'Door{door_sig}AntiPnch', 1)
            sleep(0.5)
            self.five_door_sts(1,1,1,1,1)
            self.ck_door_sts(2,2,2,2,2)
            sleep(10.1) 
        self.five_door_sts(0,0,0,0,0)  
        self.five_door_antipnch(0,0,0,0,0)
        sleep(0.5)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 2, "findKeyType":1})
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrAntiPnch', 1) 
        sleep(0.5)
        self.five_door_sts(1,1,1,1,1)
        self.ck_door_sts(2,2,2,2,2)
        sleep(10.1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", []) 
        
    @allure.title("设置整车上锁解锁_运行完之前不响应过程中接收到的新调用")
    @pytest.mark.full
    def test_caseid_1985446(self): 
        self.five_door_sts(0,0,0,0,0)       
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)]) 
        self.dk.set_cenlock_sts(0x1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 2, "findKeyType":1}) 
        self.dk.ck_bgm_not_send_cmd("请求Idle=0无效", self.dk.dk_data_queue_key_search) 
        for source in [0, 1, 3, 2]:
            for cmd in range(4):
                self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": cmd, "source": source}) 
                sleep(0.5)
        sleep(3)
        self.five_door_sts(1,1,1,1,1) # 10s后关门，不下发闭锁 
        self.ck_door_sts(2,2,2,2,2)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [])  
        self.bgm_eth_inter.ck_signal_values("MobDevCenLockReq", [])  
        self.bgm_eth_inter.ck_signal_values("TelmCenLockReq", [])  
        self.bgm_eth_inter.ck_signal_values("VehPrkgLockTheftReq", [])  
        
    @allure.title("设置整车上锁解锁_任意条件下调用SetDoorCloseLock均使四个电动门关闭")
    @pytest.mark.full
    def test_caseid_1985485(self): 
        self.five_door_open_close(1,1,1,1,1)
        self.five_door_antipnch(0,0,0,0,0)
        self.five_door_sts(0,0,0,0,0)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 2, "findKeyType":1})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        a = self.bgm_eth_inter.get_signal_values("DoorDrvrOpenHmiReqDoorOpenerReq1")
        b = self.bgm_eth_inter.get_signal_values("DoorPassOpenHmiReqDoorOpenerReq1")
        c = self.bgm_eth_inter.get_signal_values("DoorLeReOpenHmiReqDoorOpenerReq1")
        d = self.bgm_eth_inter.get_signal_values("DoorRiReOpenHmiReqDoorOpenerReq1")
        e = self.bgm_eth_inter.get_signal_values("TrunkOpenHmiReq")
        assert 2 in a and 2 in b and 2 in c and 2 in d and 2 in e
    
    @allure.title("RKE解闭锁下行pdu校验")
    @pytest.mark.full
    def test_caseid_1987458(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 0})
        self.dk.ck_cenlock_sts(0x1)
        sleep(0.2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 0})
        self.dk.ck_cenlock_sts(0x3)
        sleep(0.2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 0})
        self.dk.ck_cenlock_sts(0x1)
        sleep(0.2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 0})
        self.dk.ck_cenlock_sts(0x3)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("MobDevCenLockReq", [1,0,2,0,1,0,3,0])
        
    @allure.title("解远程解闭锁下行pdu校验")
    @pytest.mark.full
    def test_caseid_1987459(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 1})
        self.dk.ck_cenlock_sts(0x1)
        sleep(0.2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1})
        self.dk.ck_cenlock_sts(0x3)
        sleep(0.2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 1})
        self.dk.ck_cenlock_sts(0x1)
        sleep(0.2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 1})
        self.dk.ck_cenlock_sts(0x3)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("TelmCenLockReq", [1,0,2,0,1,0,3,0])
         
    @allure.title("kHmi解闭锁下行pdu校验")
    @pytest.mark.full
    def test_caseid_1987460(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 2})
        self.dk.ck_cenlock_sts(0x1)
        sleep(0.2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2})
        self.dk.ck_cenlock_sts(0x3)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [1,0,2,0])
        
    @allure.title("kAPA解闭锁下行pdu校验")
    @pytest.mark.full
    def test_caseid_1987461(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 3})
        self.dk.ck_cenlock_sts(0x1)
        sleep(0.2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 3})
        self.dk.ck_cenlock_sts(0x3)
        sleep(0.2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3, "findKeyType":0})
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)]) 
        self.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])
        sleep(1)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3, "findKeyType":1})
        sleep(2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3, "findKeyType":2})
        sleep(2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3, "findKeyType":3})
        sleep(4)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("VehPrkgLockTheftReq", [3, 0, 1, 0, 2, 0, 2, 0, 2, 0, 2, 0])
        
    @allure.title("设置整车上锁解锁_参数不满足时不进行pdu下发")
    @pytest.mark.full
    def test_caseid_1987662(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 0}) 
        sleep(2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 1})
        sleep(2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 2}) 
        sleep(2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 3}) 
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal() 
        self.bgm_eth_inter.ck_signal_values("MobDevCenLockReq", [])
        self.bgm_eth_inter.ck_signal_values("TelmCenLockReq", [])
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [])
        self.bgm_eth_inter.ck_signal_values("VehPrkgLockTheftReq", [])
        
    @allure.title("RKE解闭锁两帧报文下发过程中不能被打断")
    @pytest.mark.full
    def test_caseid_1987663(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        #下发周期内被同source打断，两帧报文不被打断，且后续不会响应100ms内的动作
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 0})
        sleep(0.02)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 0})
        sleep(1)
        #下发周期内被不同source打断，两帧报文不被打断，且后续不会响应100ms内的动作
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 0})
        sleep(0.02)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1})
        sleep(0.02)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2})
        sleep(0.02)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 3})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("MobDevCenLockReq", [1,0,1,0])
        
    @allure.title("远程解闭锁两帧报文下发过程中不能被打断")
    @pytest.mark.full
    def test_caseid_1987664(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        #下发周期内被同source打断，两帧报文不被打断，且后续不会响应100ms内的动作
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 1})
        sleep(0.02)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1})
        sleep(1)
        #下发周期内被同source打断，两帧报文不被打断，且后续不会响应100ms内的动作
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 1})
        sleep(0.02)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 0})
        sleep(0.02)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2})
        sleep(0.02)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 3})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("TelmCenLockReq", [1,0,1,0])
        
    @allure.title("kHmi解闭锁两帧报文下发过程中不能被打断")
    @pytest.mark.full
    def test_caseid_1987665(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        #下发周期内被同source打断，两帧报文不被打断,且后续不会响应100ms内的动作
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 2})
        sleep(0.02)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2})
        sleep(1)
        #下发周期内被不同source打断，两帧报文不被打断，且后续不会响应100ms内的动作
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 2})
        sleep(0.02)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 0})
        sleep(0.02)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1})
        sleep(0.02)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 3})
        sleep(2)
        
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [1,0,2,0])
        
    @allure.title("kAPA解闭锁两帧报文下发过程中不能被打断")
    @pytest.mark.full
    def test_caseid_1987666(self):
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)]) 
        self.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])
        self.bgm_eth_inter.start_bgm_tcpdump()
        #下发周期内被同source打断，两帧报文不被打断,且后续不会响应100ms内的动作
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 3})
        sleep(0.02)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 3})
        sleep(1)
        #下发周期内被不同source打断，两帧报文不被打断，且后续不会响应100ms内的动作
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3, "findKeyType":1})
        sleep(0.02)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 0})
        sleep(0.02)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1})
        sleep(0.02)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("VehPrkgLockTheftReq", [3, 0, 2, 0])
        
######################################################################################################################################################## 

@allure.feature("SOA服务接口")
@allure.story("整车控制/CentralLockService")
@pytest.mark.aqx
class TestSpecificCentralLockService(TestBase):
    """针对需要修改BGM S2S配置的测试用例，单独新增一个类"""
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        write_s2s_json({})
        change_bgm_config(nucapp=self.nucapp, s2s_path=s2s_path)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("CentralLockService", "client"),
                                     ("KeyService", "client"),
                                     ("DoorService", "client"),
                                     ("TailGateService", "client"),
                                     ("BonnetService", "client"),
                                     ])
        self.partner.method_default_timeout = 0.1
        self.io.hood_door1_close()
        self.io.hood_door2_close()
        sleep(2)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 5, "value": 0}]})

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        recover_bgm_config()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.sd_tester.change_car_mode(0)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'EntityKeyWhiteListVers', self.dk.last_sync_time_entity)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BLESlotKeyWhiteListVers', self.dk.last_sync_time_ble)  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3') 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0) 
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4})
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.dk.set_cenlock_sts(0x3)  
        self.partner.empty_all(2)

    def after_each_func(self, ecu):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        if ecu.get("testresult") != "Pass":
            logger.info("case失败，需等待5s让环境恢复")
            sleep(5)
        else:
            sleep(3)  # 避免防玩
        # 修改/data/app/s2s.json中30506端口改为30501
        self.update_bgm_s2s_json({})
        self.sd_tester.update_serverdoipid(0x1002)
        super().after_each_func(ecu, start=False)    
                             
    @allure.title("设置整车上锁解锁_APA闭锁设防&车内寻钥匙_2s超时&GetFindKeyResult.(zone=5&result=0)")
    @pytest.mark.full
    def test_caseid_1983172(self):   # central_lock_service_imp
        self.dk.set_cenlock_sts(0x1)
        #改变端口号，使MCU与MPU断开连接，此时会寻钥超时 
        #使用不匹配位置的钥匙 会返回找不到钥匙 
        self.update_bgm_s2s_json({"tcpReqClientPort": 30506, "tcpReqServerPort": 30506,
                                  "tcpResClientPort": 30506, "tcpResServerPort": 30506},partner_key=CENTRALLOCK_SERVICE_CLIENT)
        sleep(15)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3, "findKeyType":2}, timeout=2)
        self.dk.ck_bgm_not_send_cmd("请求Idle=0无效", self.dk.dk_data_queue_key_search)
        self.dk.ck_cenlock_sts(0x1, 0xC) 
                        
    @allure.title("设置整车上锁解锁_APA闭锁设防&车外寻钥匙_2s超时&GetFindKeyResult.(zone=0&result=0)")
    @pytest.mark.full
    def test_caseid_1983169(self): 
        self.dk.set_cenlock_sts(0x1)  
        self.update_bgm_s2s_json({"tcpReqClientPort": 30506, "tcpReqServerPort": 30506,
                                  "tcpResClientPort": 30506, "tcpResServerPort": 30506})
        sleep(15)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3, "findKeyType":1}, timeout=2)  
        self.dk.ck_bgm_not_send_cmd("请求Idle=0无效", self.dk.dk_data_queue_key_search)
        self.dk.ck_cenlock_sts(0x1, 0xC) 
        
@allure.feature("SOA服务接口")
@allure.story("整车控制/CentralLockService")
@pytest.mark.aqx                          
class TestCentralLockServiceMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("CentralLockService", "client")])

    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu)        
        
    @allure.title("MockMCU启动场景_LockgCenStsTrigSrc=0")
    @pytest.mark.full
    def test_caseid_1984084(self): # LockgCenStsTrigSrc|LockgCenStsLockSt|LockgCenStsUpdEve|NotifyCentralLockSysInfoEvent
        sleep(13)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 0) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 1) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsUpdEve', 1) 
        sleep(3)
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        sleep(10)
        info0 = {"sts": 1, "triggerId": 0, "updateEve": True}
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetCentralLockSysInfo", {}, {"out": info0})
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info0})
        
    @allure.title("MockMCU启动场景_LockgCenStsLockSt=0")
    @pytest.mark.full
    def test_caseid_1984085(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 1) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 0) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsUpdEve', 1) 
        sleep(3)
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        sleep(10)
        info0 = {"sts": 0, "triggerId": 1, "updateEve": True}
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetCentralLockSysInfo", {}, {"out": info0})
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info0})       
        
    @allure.title("MockMCU启动场景_LockgCenStsUpdEve=0")
    @pytest.mark.full
    def test_caseid_1984086(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 1) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 1) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsUpdEve', 0) 
        sleep(3)
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        sleep(10)
        info0 = {"sts": 1, "triggerId": 1, "updateEve": False}
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetCentralLockSysInfo", {}, {"out": info0})
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info0})     

    @allure.title("获取&通知中控锁状态提醒_MockMcu遍历LockSysStsPrmt")
    @pytest.mark.full
    def test_caseid_1985164(self):
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr21, 'LockSysStsPrmt', 3) 
        self.partner.empty_all(2)
        for signal in range(16):
            self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr21, 'LockSysStsPrmt', signal) 
            sleep(1)
            if signal<8:
                self.partner.ck_event_and_resp(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"reminder": signal})
            else:
                self.partner.ck_no_event_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"out":7})
                
    @allure.title("启动场景_通知解闭锁动作触发源_默认值")
    @pytest.mark.full
    def test_caseid_1988672(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr38, 'LockgEventTrigsrc', 0) 
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockActTriggerSource", {"sourceId": 0}, timeout=10)
        
    @allure.title("启动场景_通知解闭锁动作触发源_非默认值")
    @pytest.mark.full
    def test_caseid_1988673(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr38, 'LockgEventTrigsrc', 1) 
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockActTriggerSource", {"sourceId": 1}, timeout=10)
        
    @allure.title("启动场景_通知解闭锁成功触发源_默认值")
    @pytest.mark.full
    def test_caseid_1988674(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 0) 
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 0}, timeout=10)
        
    @allure.title("启动场景_通知解闭锁成功触发源_非默认值")
    @pytest.mark.full
    def test_caseid_1988675(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 1) 
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 1}, timeout=10)
        
    @allure.title("启动场景_通知整车锁状态_默认值")
    @pytest.mark.full
    def test_caseid_1988676(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 0) 
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        #SOA-28258 偏差接受
        self.partner.ck_no_event(CENTRALLOCK_SERVICE_CLIENT, "LockStatus")
        
    @allure.title("启动场景_通知整车锁状态_非默认值")
    @pytest.mark.full
    def test_caseid_1988677(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 1) 
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockStatus", {"sts": 1}, timeout=10)
        
    @allure.title("启动场景_通知中控锁状态提醒_默认值")
    @pytest.mark.full
    def test_caseid_1988678(self):
        #LockSysStsPrmt 非周期信号
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr21, 'LockSysStsPrmt', 0) 
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        sleep(15)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr21, 'LockSysStsPrmt', 0) 
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"reminder": 0}, timeout=10)
        
    @allure.title("启动场景_通知中控锁状态提醒_非默认值")
    @pytest.mark.full
    def test_caseid_1988680(self):
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr21, 'LockSysStsPrmt', 1) 
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        sleep(15)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr21, 'LockSysStsPrmt', 1) 
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"reminder": 1}, timeout=10)
        
    @allure.title("启动场景_通知触发中控解闭锁动作事件更新状态_默认值")
    @pytest.mark.full
    def test_caseid_1988681(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsUpdEve', 0) 
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CenLckUpdEve", {"sts": 0}, timeout = 10)
        
    @allure.title("启动场景_通知触发中控解闭锁动作事件更新状态_非默认值")
    @pytest.mark.full
    def test_caseid_1988682(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsUpdEve', 1) 
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CenLckUpdEve", {"sts": 1}, timeout = 10)
        
    @allure.title("启动场景_通知中控锁系统状态_默认值")
    @pytest.mark.full
    def test_caseid_1988683(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 0) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 0) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsUpdEve', 0) 
        sleep(3)
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        info0 = {"sts": 0, "triggerId": 0, "updateEve": False}
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info0}, timeout = 10) 
        
    