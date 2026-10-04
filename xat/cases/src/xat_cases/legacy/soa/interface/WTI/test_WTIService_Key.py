
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_WTIService.py
@Time         :2023/10/08 17:20:31
@Author       :qingxia@jiduauto.com
@Description  :
"""
import random
import time
import allure
import pytest
import copy
from time import sleep
from random import randint
from xat_ecu.legacy.common.data_type_handing import logger
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester

Key_Disconnected = "Key Disconnected"
Entity_Key_battery_Low = "Entity Key battery Low"
BKA_Warn = "BKA Warn"
NKR_Warn = "NKR Warn"
NFC_BLE_Key_Legacy_Reminder = "NFC BLE Key Legacy Reminder"
NFC_UWB_Key_Legacy_On_Driver_Reminder = "NFC UWB Key Legacy On Driver Reminder"
NFC_UWB_Key_Legacy_On_Passenger_Reminder = __import__("os").environ.get('XAT_CREDENTIAL____SOA_INTERFACE_WTI_TEST_WTISERVICE_KEY_PY_NFC_UWB_KEY_LEGACY_ON_PASSENGER_REMINDER', "")


@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIService_Key")
@pytest.mark.aqx
class TestKeyWTIService(TestBase):

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("WTIService", "client"),
                                     ("EntryService", "client"),
                                     ("CentralLockService", "client"),
                                     ("ChassisService", "client"),
                                     ("DoorService", "client"),
                                     ("KeyService", "client"),
                                     ("VehicleModeService", "client"),
                                     ("ClimateControlService", "client")
                                     ])
        self.partner.method_default_timeout = 0.1

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.set_nopeople_incar()
        self.sd_tester.tester_present()
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'EntityKeyWhiteListVers', self.dk.last_sync_time_entity)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BLESlotKeyWhiteListVers', self.dk.last_sync_time_ble)       
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_False')
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.ipdu.set_vehspd(0)
        sleep(1)
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        if ecu.get("testresult") != "Pass":
            sleep(5)
        super().after_each_func(ecu, start=False)

    def set_digital_key_connect_info(self, slot, key_type, zone, battwarn=0, connect_sts=None, recover_other=False):
        """
        再封装一层给WTIService用
        :param slot:   钥匙槽1,2,3,4
        :param key_type: 0-9
        :param zone:  0-16
        :param battwarn: 低电量报警
        :param connect_sts: 连接状态
        :param recover_other: 是否恢复其他slot为默认值
        :return:
        """
        keyids = [key_id1, key_id2, key_id3, key_id4]
        self.dk.set_single_digital_key_connect_info(slot,
                                                    connect_sts=randint(0, 1) if connect_sts is None else connect_sts,
                                                    keyid=keyids[slot - 1], zone=zone, key_type=key_type,
                                                    battwarn=battwarn)
        if recover_other:
            for i in range(1, 5):
                if slot == i:
                    continue
                self.dk.set_single_digital_key_connect_info(i)
                
    def ck_no_specific_event_and_GetWarningMsgList(self, hint, info, timeout=1):
        """校验无指定warningMsgList事件，并请求WarningMsgList获取结果"""
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})

    def ck_WarningMsgList_and_GetWarningMsgList(self, hint, info, timeout=3):
        """校验指定warningMsgList事件，并请求WarningMsgList获取结果"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint, "info": str(info)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})

    def ck_no_specific_event_and_GetTelltaleList(self, hint, state, timeout=1):
        """校验无指定TelltaleList事件，并请求TelltaleList获取结果"""
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "TelltaleList", hint, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": hint, "state": str(state)}]})

    def ck_TelltaleList_and_GetTelltaleList(self, hint, state, timeout=3):
        """校验指定TelltaleList事件，并请求TelltaleList获取结果"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                  {"list": [{"name": hint, "state": str(state)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": hint, "state": str(state)}]})
        
    @allure.title("NFC锁车-UWB和蓝牙钥匙同时遗留")
    @pytest.mark.sanity
    def test_caseid_1943207(self): 
        hint = "NFC Key Legacy Reminder"
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.set_digital_key_connect_info(1, 3, 6, recover_other=True)  #UWB
        self.set_digital_key_connect_info(3, 5, 6, recover_other=False) #蓝牙
        sleep(1)
        self.dk.send_nfc_cmd() 
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)   
        sleep(4)                 
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)   
        
    @allure.title("NFC锁车-钥匙遗留提醒_服务启动默认值")
    @pytest.mark.full
    def test_caseid_1943206(self):
        hint = "NFC Key Legacy Reminder"
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.set_digital_key_connect_info(3, 5, 6, recover_other=True)
        sleep(1)
        self.dk.send_nfc_cmd() 
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)     
        self.ipdu.pause_all_bus_send()        
        self.nucapp.bgm_power_off()
        sleep(2)
        self.nucapp.bgm_power_on()
        self.partner.wait_for_service_reconnect(WTI_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]})                            

    @allure.title("NFC锁车-蓝牙钥匙遗留提醒_告警产生&解锁恢复")
    @pytest.mark.full
    def test_caseid_1943205(self):
        hint = "NFC Key Legacy Reminder"  
        self.dk.set_cenlock_sts(1)
        self.dk.reset_bncm_digital_keyinfo() #无钥匙
        self.partner.empty_all(1)
        self.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.set_digital_key_connect_info(4, 5, 6, recover_other=True)
        sleep(1)
        self.dk.send_nfc_cmd() 
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)        
        self.dk.reset_bncm_digital_keyinfo() #无钥匙 闭锁 恢复告警
        sleep(1)
        self.dk.set_cenlock_sts(1) # 触发上报中控解锁事件
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)     
        
    @allure.title("NFC锁车-蓝牙钥匙遗留提醒_告警产生&超时恢复")
    @pytest.mark.sanity
    def test_caseid_1943204(self): # 
        hint = "NFC Key Legacy Reminder"   
        self.dk.set_cenlock_sts(1)
        self.dk.reset_bncm_digital_keyinfo() #无钥匙
        self.partner.empty_all(1)
        self.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.set_digital_key_connect_info(1, 4, 6, recover_other=True)
        sleep(1)
        self.dk.send_nfc_cmd() 
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)   
        self.partner.empty_all(0.5)  
        self.dk.press_door_outswitch(5, 0.5)
        self.dk.ck_cenlock_sts(2, timeout=2) # 中控锁状态=2 不能恢复
        self.ck_no_specific_event_and_GetWarningMsgList(hint, 1)
        sleep(2)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)    
        
    @allure.title("NFC锁车-UWB钥匙遗留提醒_告警产生&超时恢复")
    @pytest.mark.sanity
    def test_caseid_1943203(self): # 需求逻辑本身不能命中reset
        hint = "NFC Key Legacy Reminder"               
        self.dk.set_cenlock_sts(1)
        self.dk.reset_bncm_digital_keyinfo() #无钥匙
        self.partner.empty_all(1)
        self.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.set_digital_key_connect_info(1, 3, 6, recover_other=True)
        sleep(1)
        self.dk.send_nfc_cmd() 
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 2)
        self.partner.empty_all(0.5)  
        self.dk.press_door_outswitch(5, 0.5)
        self.dk.ck_cenlock_sts(2, timeout=2) # 中控锁状态=2 不能恢复
        self.ck_no_specific_event_and_GetWarningMsgList(hint, 2)
        sleep(2)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0) 
        
    @allure.title("NFC锁车-UWB钥匙遗留提醒_告警产生&解锁恢复")
    @pytest.mark.sanity
    def test_caseid_1943202(self): 
        hint = "NFC Key Legacy Reminder" 
        self.dk.set_cenlock_sts(1)
        self.dk.reset_bncm_digital_keyinfo() #无钥匙
        self.partner.empty_all(1)
        self.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.set_digital_key_connect_info(2, 3, 6, recover_other=True)
        sleep(1)
        self.dk.send_nfc_cmd() 
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 2)        
        self.dk.reset_bncm_digital_keyinfo() #无钥匙 闭锁 恢复告警
        sleep(1)
        self.dk.set_cenlock_sts(1) # 触发上报中控解锁事件
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0) 

    @allure.title("解闭锁提醒5(MsgUnlockReminder)_服务启动默认值")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1943195(self):
        hint = 'No Key Present'
        self.dk.set_cenlock_sts(1)
        self.dk.reset_bncm_digital_keyinfo() # 所有区域无钥匙 
        self.dk.press_door_outswitch(1, 2.01)
        # NotifyLockWarning.warnnings.lock = @value(3)        kNoKey
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        sleep(1)
        self.ipdu.pause_all_bus_send()        
        self.nucapp.bgm_power_off()
        sleep(2)
        self.nucapp.bgm_power_on()
        self.partner.wait_for_service_reconnect(WTI_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},  {"out": [{"name": hint, "info": '0'}]})

    @allure.title("解闭锁提醒5(MsgUnlockReminder)_告警产生闭锁恢复")
    @pytest.mark.full
    def test_caseid_1939980(self):
        hint = 'No Key Present'
        self.dk.set_cenlock_sts(1)
        self.dk.reset_bncm_digital_keyinfo() # 所有区域无钥匙 
        self.dk.press_door_outswitch(1, 2.01)
        # NotifyLockWarning.warnnings.lock = @value(3)        kNoKey
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        sleep(2)
        self.dk.set_cenlock_sts(3)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)     
        
    @allure.title("解闭锁提醒5(MsgUnlockReminder)_告警重复产生超时恢复")
    @pytest.mark.sanity
    def test_caseid_1939979(self):
        hint = 'No Key Present'
        self.dk.set_cenlock_sts(1)
        self.dk.reset_bncm_digital_keyinfo() # 所有区域无钥匙 
        self.dk.press_door_outswitch(1, 2.01)
        # NotifyLockWarning.warnnings.lock = @value(3)        kNoKey
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        sleep(1)
        # 再次触发 
        self.dk.press_door_outswitch(1, 2.01)
        self.ck_no_specific_event_and_GetWarningMsgList(hint, 1)
        # 超时恢复
        sleep(3.5)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)  
        
    @allure.title("解闭锁提醒2(MsgUnlockReminder)_服务启动默认值")
    @pytest.mark.full   
    @pytest.mark.restart
    def test_caseid_1939978(self):
        hint = 'Door Cannot Closed Reminder'
        self.dk.set_cenlock_sts(1)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_Detected')  # nkr detected给bgm 是否检测到NFC设备
        sleep(0.1)
        self.dk.send_nfc_cmd()  
        logger.info(f"NFC刷卡 主驾门开 关门闭锁失败场景：")
        sleep(2.1) # 长刷
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_NotDetected')
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_TRUE')#触发防夹 
        # NotifyLockWarning.warnnings.lock = @value(9)    kCloseFailByNfcPe
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        sleep(1)
        self.ipdu.pause_all_bus_send()        
        self.nucapp.bgm_power_off()
        sleep(2)
        self.nucapp.bgm_power_on()
        self.partner.wait_for_service_reconnect(WTI_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},  {"out": [{"name": hint, "info": '0'}]})

    @allure.title("解闭锁提醒2(MsgUnlockReminder)_告警产生闭锁恢复")
    @pytest.mark.full
    def test_caseid_1939977(self):
        hint = 'Door Cannot Closed Reminder'
        self.dk.set_cenlock_sts(1)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_Detected') # nkr detected给bgm 是否检测到NFC设备
        sleep(0.1)
        self.dk.send_nfc_cmd()  
        logger.info(f"NFC刷卡 主驾门开 关门闭锁失败场景：")
        sleep(2.1) # 长刷
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_NotDetected')
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_TRUE') #触发防夹 
        # NotifyLockWarning.warnnings.lock = @value(9)    kCloseFailByNfcPe
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        self.partner.empty_all(2)
        # 闭锁
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.dk.set_cenlock_sts(3)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",  {"list": [{"name": hint, "info": '0'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},  {"out": [{"name": hint, "info": '0'}]})

    @allure.title("解闭锁提醒2(MsgUnlockReminder)_告警重复产生超时恢复")
    @pytest.mark.sanity
    def test_caseid_1939976(self): 
        hint = 'Door Cannot Closed Reminder'
        self.dk.set_cenlock_sts(1)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_Detected')  # nkr detected给bgm 是否检测到NFC设备
        sleep(0.1)
        self.dk.send_nfc_cmd()  # 关门 闭锁 --失败
        logger.info(f"NFC刷卡 主驾门开 关门闭锁失败场景：")
        sleep(2.1) # 长刷
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_NotDetected')
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_TRUE')  #触发防夹 
        # NotifyLockWarning.warnnings.lock = @value(9)    kCloseFailByNfcPe
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockActTriggerSource", {"sourceId": 12})
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        
        self.partner.empty_all()
        #再次触发告警 无event事件上报
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_FALSE')
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_Detected')
        sleep(0.1)
        self.dk.send_nfc_cmd()  # 再次NFC关门失败
        logger.info(f"NFC刷卡 主驾门开 再次验证关门闭锁失败场景：")
        sleep(2.1)
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_NotDetected')
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_TRUE')
        self.ck_no_specific_event_and_GetWarningMsgList(hint, 1) #4s内的话
        
        sleep(2.5)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)            
        
    @allure.title("解闭锁提醒1(MsgUnlockReminder)_服务启动默认值")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1939973(self): 
        hint = 'Unlock Reminder'
        self.dk.set_cenlock_sts(1)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.dk.send_nfc_cmd() # NotifyLockWarning.warnnings.lock = @value(1)    kLockFailByNFC
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        sleep(1)
        self.ipdu.pause_all_bus_send()        
        self.nucapp.bgm_power_off()
        sleep(2)
        self.nucapp.bgm_power_on()
        self.partner.wait_for_service_reconnect(WTI_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},  {"out": [{"name": hint, "info": '0'}]})

    @allure.title("解闭锁提醒1(MsgUnlockReminder)_告警产生闭锁恢复")
    @allure.testcase("test_caseid_1939972")
    @pytest.mark.sanity
    def test_caseid_1939972(self): 
        hint = 'Unlock Reminder'
        self.dk.set_cenlock_sts(1)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.dk.send_nfc_cmd() # NotifyLockWarning.warnnings.lock = @value(1)    kLockFailByNFC
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        self.partner.empty_all(2)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.dk.set_cenlock_sts(3)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @allure.title("解闭锁提醒1(MsgUnlockReminder)_告警重复产生超时恢复")
    @pytest.mark.sanity
    def test_caseid_1939970(self):
        hint = 'Unlock Reminder'
        self.dk.set_cenlock_sts(1)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_nfc_cmd() # NotifyLockWarning.warnnings.lock = @value(1)    kLockFailByNFC
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        self.partner.empty_all(1.5)
        # 再次触发 warning info无跳变 WTI无event事件上报
        self.dk.send_nfc_cmd()
        self.ck_no_specific_event_and_GetWarningMsgList(hint, 1)
        sleep(2) # timer时间内 
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": '1'}]})
        sleep(0.5) # 超时后
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)
        
    @allure.title("钥匙断连提醒(MsgKey DisconnectedReminder)_锁车之前断开的钥匙，锁车之后，不提示")
    @pytest.mark.full
    def test_caseid_1903605(self): # digkeyconnectInfo|Key Disconnected|wti current mode|FrntLeftDoorSts,isOpen
        # 场景1：
        self.sd_tester.change_usage_mode(0x2)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.set_digital_key_connect_info(1, 1, 2, 0, 1, recover_other=True)  # 钥匙连接
        sleep(0.5)
        self.set_digital_key_connect_info(1, 1, 2, 0, 0)  # 钥匙断连
        sleep(1.5)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        sleep(0.5)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": Key_Disconnected,
                                             "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": Key_Disconnected,
                                                        "info": '1'}]})
        self.set_digital_key_connect_info(1, 1, 2, 0, 1)  # 钥匙连接
        sleep(0.5)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": Key_Disconnected,
                                             "info": '0'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": Key_Disconnected,
                                                        "info": '0'}]})

        # 场景2
        self.sd_tester.change_usage_mode(0x1)
        sleep(1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(0.5)
        self.set_digital_key_connect_info(1, 1, 2, 0, 0)  # 钥匙断连
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        sleep(0.5)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": Key_Disconnected,
                                                        "info": '0'}]})
        # 场景3
        self.set_digital_key_connect_info(1, 1, 2, 0, 1)  # 钥匙连接
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(0.5)
        self.sd_tester.change_usage_mode(0x2)
        self.set_digital_key_connect_info(1, 1, 2, 0, 0)  # 钥匙断连
        self.sd_tester.change_usage_mode(0x1)
        sleep(1)
        self.sd_tester.change_usage_mode(0x2)
        sleep(1)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        sleep(0.5)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", Key_Disconnected)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": Key_Disconnected,
                                                        "info": '0'}]})
        
    @allure.title("钥匙断连提醒(MsgKey DisconnectedReminder)_故障确认状态后，钥匙连接")
    @pytest.mark.full
    def test_caseid_111723(self):
        self.dk.set_cenlock_sts(1)  # 中控解锁  digkeyconnectInfo|Key Disconnected
        for usage_mode in [0x2, 0xB, 0xD]:
            self.set_digital_key_connect_info(1, 1, 2, 0, 1)  # 钥匙连接
            self.dk.set_door_sts([0, 0, 0, 0, 0])
            self.sd_tester.change_usage_mode(usage_mode)
            self.dk.set_digital_key_connect_info()
            sleep(1)
            self.dk.set_door_sts([1, 1, 1, 1, 1])
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                      {"list": [{"name": Key_Disconnected,
                                                 "info": '1'}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": Key_Disconnected,
                                                            "info": '1'}]})
            self.set_digital_key_connect_info(3, 1, 2, 0, 1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                      {"list": [{"name": Key_Disconnected,
                                                 "info": '0'}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": Key_Disconnected,
                                                            "info": '0'}]})
            self.dk.set_door_sts([0, 0, 0, 0, 0])

    @allure.title("实体钥匙电量低(MsgEntityKeyBattLow)_告警不会重复触发")
    @pytest.mark.sanity
    def test_caseid_1913312(self):
        key_type = 3
        self.dk.set_digital_key_connect_info()
        sleep(0.5)
        battwarn_list = [0, 0, 0, 0]
        exp_info = '0'
        for battwarn in [1, 0]:
            for slot in range(1, 4):
                for zone in range(slot, 16, 5):
                    last_exp_info = exp_info
                    last_battwarn_list = copy.deepcopy(battwarn_list)
                    battwarn_list[slot] = battwarn
                    exp_info = str(battwarn_list[0] | battwarn_list[1] | battwarn_list[2] | battwarn_list[3])
                    logger.info(f"battern: {battwarn}, slot:{slot}, zone: {zone}")
                    logger.info(f"last_battwarn_list: {last_battwarn_list}, battwarn_list: {battwarn_list}")
                    self.partner.empty_all()
                    self.set_digital_key_connect_info(slot, key_type, zone, battwarn, 1)
                    logger.info((exp_info, last_exp_info))
                    if exp_info == last_exp_info:
                        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", Entity_Key_battery_Low)
                    else:
                        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                  {"list": [{"name": Entity_Key_battery_Low,
                                                             "info": exp_info}]})
                    self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                          {"out": [{"name": Entity_Key_battery_Low,
                                                                    "info": exp_info}]})
                    sleep(0.5)

    @allure.title("数字钥匙天线故障(MsgBKAWarn)_信号遍历")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1703397?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1913309(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BKAWarnSts', 'LvlWarn2_NoWarn')
        sleep(0.5)
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BKAWarnSts', 'LvlWarn2_Lvl1')
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": BKA_Warn, "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": BKA_Warn, "info": '1'}]})

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BKAWarnSts', 'LvlWarn2_NoWarn')
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": BKA_Warn, "info": '0'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": BKA_Warn, "info": '0'}]})

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BKAWarnSts', 'LvlWarn2_Lvl2')
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", BKA_Warn)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": BKA_Warn, "info": '0'}]})

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BKAWarnSts', 'LvlWarn2_Lvl3')
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", BKA_Warn)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": BKA_Warn, "info": '0'}]})

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BKAWarnSts', 'LvlWarn2_Lvl1')
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": BKA_Warn, "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": BKA_Warn, "info": '1'}]})
        
    @allure.title("钥匙断连提醒(MsgKeyDisconnectedReminder)_仅钥匙全部断开才上报告警")
    @pytest.mark.sanity 
    def test_caseid_1959653(self): # "Key Disconnected|KeyConnectSts|wti current mode|openclosestatus"
        self.dk.set_cenlock_sts(1)  # 中控解锁
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        for usage_mode in [0x2, 0xB, 0xD]:
            self.sd_tester.change_usage_mode(usage_mode)
            self.set_digital_key_connect_info(1, randint(1, 9), randint(1, 16), 0, 1)
            self.set_digital_key_connect_info(2, randint(1, 9), randint(1, 16), 0, 1)
            self.set_digital_key_connect_info(3, randint(1, 9), randint(1, 16), 0, 1)
            self.set_digital_key_connect_info(4, randint(1, 9), randint(1, 16), 0, 1)
            sleep(0.5)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": Key_Disconnected,
                                                            "info": '0'}]})
            for slot in range(1, 5):
                logger.info(f"usage mode:{usage_mode}, slot:{slot}")
                self.set_digital_key_connect_info(slot, randint(1, 9), randint(1, 16), 0, 0)
                self.partner.empty_all(1)
                self.dk.set_door_sts([1, 0, 0, 0, 0])
                if slot != 4:
                    self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", Key_Disconnected)
                    self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                          {"out": [{"name": Key_Disconnected,
                                                                    "info": '0'}]})
                else:
                    self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                              {"list": [{"name": Key_Disconnected,
                                                         "info": '1'}]})
                    self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                          {"out": [{"name": Key_Disconnected,
                                                                    "info": '1'}]})
                self.dk.set_door_sts([0, 0, 0, 0, 0])
                sleep(0.5)
 
    @allure.title("实体钥匙电量低(MsgEntityKeyBattLow)_任一钥匙可以触发低电量告警")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1703418?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1913311(self):
        key_type = 3
        self.dk.set_digital_key_connect_info()
        sleep(0.5)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": Entity_Key_battery_Low,
                                                        "info": '0'}]})
        sleep(3)
        for slot in range(1, 4):
            for battwarn in [1, 0]:
                logger.info(f"battern: {battwarn}, slot:{slot}")
                self.partner.empty_all()
                self.set_digital_key_connect_info(slot, key_type, randint(1, 16), battwarn, 1)
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                          {"list": [{"name": Entity_Key_battery_Low,
                                                     "info": '1' if battwarn else '0'}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                      {"out": [{"name": Entity_Key_battery_Low,
                                                                "info": '1' if battwarn else '0'}]})
                sleep(0.5)      
                
    @allure.title("解闭锁提醒3(MsgCannotUnLockReminder)_告警产生恢复")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1703429?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1913313(self):
        hint = 'Cannot unLock Reminder'
        self.dk.set_cenlock_sts(3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 0)
        sleep(1)
        self.dk.press_door_inswitch(3, 0.5)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": "1"}]})
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)                
                
    @allure.title("钥匙断连提醒(MsgKeyDisconnectedReminder)_Convenience&Active&Driving_主驾门打开后会触发告警")
    @pytest.mark.full
    def test_caseid_110798(self): # KeyConnectSts|doordrvrsts|wti current mode|Key Disconnected
        for usage_mode in [0x2, 0xB, 0xD]:
            self.dk.set_cenlock_sts(1)
            self.dk.set_door_sts([0, 0, 0, 0, 0])
            self.sd_tester.change_usage_mode(usage_mode)
            self.dk.set_digital_key_connect_info()
            sleep(0.5)
            for slot in range(1, 4):
                for connect_sts in [1, 0]:
                    logger.info(f"slot:{slot}, connect_sts: {connect_sts}")
                    self.partner.empty_all()
                    self.set_digital_key_connect_info(slot, randint(1, 9), randint(1, 16), 0, connect_sts)
                    sleep(1)
                    self.dk.set_cenlock_sts(1)
                    self.dk.set_door_sts([1, 0, 0, 0, 0])  # 开主驾门
                    if connect_sts:
                        if not (usage_mode == 2 and slot == 1):  # 第一次执行时无跳变，无提醒event
                            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                      {"list": [{"name": Key_Disconnected,
                                                                 "info": '0'}]})
                        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                              {"out": [{"name": Key_Disconnected,
                                                                        "info": '0'}]})
                    else:
                        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                  {"list": [{"name": Key_Disconnected,
                                                             "info": '1'}]})
                        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                              {"out": [{"name": Key_Disconnected,
                                                                        "info": '1'}]})
                    self.dk.set_door_sts([0, 0, 0, 0, 0])
                    sleep(0.5)                
                
    @allure.title("车外NFC读卡故障(MsgNKRWarn)_信号遍历")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1703432?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1913320(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'NKRWarnSts', 'LvlWarn2_NoWarn')
        sleep(0.5)
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'NKRWarnSts', 'LvlWarn2_Lvl1')
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": NKR_Warn, "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": NKR_Warn, "info": '1'}]})

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'NKRWarnSts', 'LvlWarn2_NoWarn')
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": NKR_Warn, "info": '0'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": NKR_Warn, "info": '0'}]})

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'NKRWarnSts', 'LvlWarn2_Lvl2')
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", NKR_Warn)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": NKR_Warn, "info": '0'}]})

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'NKRWarnSts', 'LvlWarn2_Lvl3')
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", NKR_Warn)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": NKR_Warn, "info": '0'}]})

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'NKRWarnSts', 'LvlWarn2_Lvl1')
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": NKR_Warn, "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": NKR_Warn, "info": '1'}]})

    @allure.title("数字钥匙模块故障(MsgBNCMWarn)_信号遍历")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1703440?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1913310(self):
        hint = "BNCM Warn"
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BNCMWarnSts', 'LvlWarn2_NoWarn')
        sleep(0.5)
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BNCMWarnSts', 'LvlWarn2_Lvl1')
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint, "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '1'}]})

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BNCMWarnSts', 'LvlWarn2_NoWarn')
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint, "info": '0'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '0'}]})

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BNCMWarnSts', 'LvlWarn2_Lvl2')
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '0'}]})

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BNCMWarnSts', 'LvlWarn2_Lvl3')
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '0'}]})

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BNCMWarnSts', 'LvlWarn2_Lvl1')
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint, "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '1'}]})

    @allure.title("车内NFC读卡故障(MsgWPCWarn)_信号遍历")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1703462?projectId=46')
    @pytest.mark.sanity
    def test_caseid_110786(self):
        hint = "WPC Warn"
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'WPCWarnSts', 'LvlWarn2_NoWarn')
        sleep(0.5)
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'WPCWarnSts', 'LvlWarn2_Lvl1')
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint, "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '1'}]})

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'WPCWarnSts', 'LvlWarn2_NoWarn')
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "WPC Warn", "info": '0'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '0'}]})

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'WPCWarnSts', 'LvlWarn2_Lvl2')
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '0'}]})

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'WPCWarnSts', 'LvlWarn2_Lvl3')
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '0'}]})

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'WPCWarnSts', 'LvlWarn2_Lvl1')
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint, "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '1'}]})

    @allure.title("钥匙断连提醒(MsgKey DisconnectedReminder)_Convenience&Active&Driving_非主驾门开_不触发告警")
    @allure.testcase('test_caseid_110783')
    @pytest.mark.full
    def test_caseid_110783(self):
        self.dk.set_cenlock_sts(1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        for usage_mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            self.dk.set_digital_key_connect_info()
            sleep(0.5)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": Key_Disconnected,
                                                            "info": '0'}]})
            for slot in range(1, 4):
                for connect_sts in [1, 0]:
                    logger.info(f"slot:{slot}, connect_sts: {connect_sts}")
                    self.partner.empty_all()
                    self.set_digital_key_connect_info(slot, randint(1, 9), randint(1, 16), 0, connect_sts)
                    self.dk.set_door_sts([0, 1, 1, 1, 1])
                    self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", Key_Disconnected)
                    self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                          {"out": [{"name": Key_Disconnected,
                                                                    "info": '0'}]})
                    self.dk.set_door_sts([0, 0, 0, 0, 0])
                    sleep(0.5)

    @allure.title("钥匙断连提醒(MsgKeyDisconnectedReminder)_vmm下切再上切")
    @allure.testcase('caseid_1703471')
    @pytest.mark.full
    def test_caseid_110781(self):
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": Key_Disconnected,
                                                        "info": '0'}]}, timeout=2.2)
        for usage_mode in [0x0, 0x1]:
            self.sd_tester.change_usage_mode(0x2)
            self.dk.set_cenlock_sts(1)  # 中控解锁
            self.dk.set_door_sts([1, 0, 0, 0, 0])
            self.dk.set_digital_key_connect_info()
            self.set_digital_key_connect_info(1, randint(1, 9), randint(1, 16), 0, 1)
            sleep(1)
            self.partner.empty_event_list(WTI_SERVICE_CLIENT)
            # 断开槽1的钥匙连接 主驾门提前打开无事件上报
            self.set_digital_key_connect_info(1, randint(1, 9), randint(1, 16), 0, 0)
            self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", Key_Disconnected)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": Key_Disconnected,
                                                            "info": '0'}]}, timeout=2.2)

            self.dk.set_door_sts([0, 0, 0, 0, 0])
            # 主驾门硬线打开 触发事件上报
            # self.dk.set_cenlock_sts(1)  #中控解锁
            self.dk.set_door_sts([1, 0, 0, 0, 0])
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                      {"list": [{"name": Key_Disconnected,
                                                 "info": '1'}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": Key_Disconnected,
                                                            "info": '1'}]})
            # 车辆模式下切
            self.sd_tester.change_usage_mode(usage_mode)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                      {"list": [{"name": Key_Disconnected,
                                                 "info": '0'}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": Key_Disconnected,
                                                            "info": '0'}]})
        # 通过开门自动从0切到1
        self.dk.set_cenlock_sts(1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.sd_tester.change_usage_mode(0x0)
        self.dk.set_digital_key_connect_info()
        self.set_digital_key_connect_info(1, randint(1, 9), randint(1, 16), 0, 1)
        sleep(1)
        self.partner.empty_all()
        # 断开槽1的钥匙连接 无事件上报
        self.set_digital_key_connect_info(1, randint(1, 9), randint(1, 16), 0, 0)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", Key_Disconnected)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": Key_Disconnected,
                                                        "info": '0'}]}, timeout=2.2)
        # 主驾门硬线打开 无事件上报
        self.dk.set_cenlock_sts(1)  # 中控解锁
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", Key_Disconnected)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": Key_Disconnected,
                                                        "info": '0'}]}, timeout=2.2)

        # 车辆模式上切
        self.sd_tester.change_usage_mode(0x2)  # 再将主驾门由关闭到打开时才可以触发事件
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", Key_Disconnected)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": Key_Disconnected,
                                                        "info": '0'}]})                

######################################################################################################################################################## 
        
class TestKeyWTIServiceMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("WTIService", "client")])

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
           
    def ck_WarningMsgList_and_GetWarningMsgList(self, hint, info, timeout=3):
        """校验指定warningMsgList事件，并请求WarningMsgList获取结果"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint, "info": str(info)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})   
                
    def ck_no_specific_event_and_GetWarningMsgList(self, hint, info, timeout=1):
        """校验无指定warningMsgList事件，并请求WarningMsgList获取结果"""
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})
     
    @allure.title("无钥匙提醒信息_UsgMod遍历&信号值遍历")
    @pytest.mark.sanity
    def test_caseid_1983981(self):  # updateMsg name:No Key,info|
        hint= "No Key"
        for usgMod in [13, 11, 2, 1, 0]:            
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', usgMod) # UsgMod信号
            sleep(2)
            for signal in [1, 0]:
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr14, 'KeyNotPrsntMsgToDrvr', signal)
                value=1 if signal==1 and usgMod !=0 else 0
                logger.info(f"打印当前返回值 usgMod={usgMod} signal={signal}")
                if usgMod !=0:
                    self.ck_WarningMsgList_and_GetWarningMsgList(hint, value) 
                else:
                    self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": "0"}]})     
                                                                                    