
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
from xat_ecu.legacy.interface.bgm.bgm_ssh import *

Key_Disconnected = "Key Disconnected"
Entity_Key_battery_Low = "Entity Key battery Low"
BKA_Warn = "BKA Warn"
NKR_Warn = "NKR Warn"
NFC_BLE_Key_Legacy_Reminder = "NFC BLE Key Legacy Reminder"
NFC_UWB_Key_Legacy_On_Driver_Reminder = "NFC UWB Key Legacy On Driver Reminder"
NFC_UWB_Key_Legacy_On_Passenger_Reminder = __import__("os").environ.get('XAT_CREDENTIAL____SOA_INTERFACE_WTI_TEST_WTISERVICE_ENTRY_PY_NFC_UWB_KEY_LEGACY_ON_PASSENGER_REMINDER', "")
RKECTRL_SERVICE_SERVER = "RKECtrlService_server"
ENTRY_SERVICE_SERVER = "EntryService_server"

# Entry+CTD 相关
@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIService_Entry")
@pytest.mark.aqx
class TestEntryWTIService(TestBase):

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
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)   
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
        self.sd_tester.stop_tester_present()
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

    @allure.title("解闭锁提醒4(MsgUnlockReminder)_车外提示")
    @pytest.mark.sanity
    def test_caseid_1943208(self): 
        hint = 'Cannot unLock'
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.dk.set_door_sts([1, 0, 0, 0, 0]) # 开门主动上切至convenience
        sleep(0.5)
        self.sd_tester.change_usage_mode(2)
        self.dk.send_rke_close_door_and_lock() # 从inactive上切convenience后300ms后会主动上切active自检,自检完成后或5.5s再下切convenience  MSO-SREQ-21390
        # self.ck_NotifyLockWarning(0, 2, ck_horn=False)   
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '2'}]})
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)
        
    @allure.title("解闭锁提醒4(MsgUnlockReminder)_车内提示")
    @pytest.mark.sanity
    def test_caseid_1943209(self): 
        hint = 'Cannot unLock'
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.sd_tester.change_usage_mode(0xD)
        self.dk.set_drvr_seat_present()
        self.dk.set_four_door_unlock()
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3) 
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 498) 
        sleep(1.3)
        # self.ck_NotifyLockWarning(0, 1, ck_horn=False)   
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]})
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @allure.title("解闭锁提醒4(MsgUnlockReminder)_离车关门落锁提示_触发告警后超时恢复")
    @pytest.mark.full
    def test_caseid_1985356(self): # UpdateNotifyLockWarningEvent|Cannot unLock,info
        hint = 'Cannot unLock'
        self.dk.set_cenlock_sts(1)  
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        sleep(0.5)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_walk_away_lock_cmd() # 离车闭锁触发后，只能再间隔15s后，才可以再次触发reminder=7
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 3)
        self.partner.empty_all(8)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @allure.title("解闭锁提醒4(MsgUnlockReminder)_离车关门落锁提示_触发告警后关主驾门恢复")
    @pytest.mark.sanity
    def test_caseid_1985357(self): 
        hint = 'Cannot unLock'
        self.dk.set_cenlock_sts(1)  
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        sleep(0.5)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_walk_away_lock_cmd()
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 3)
        sleep(5)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @allure.title("解闭锁提醒4(MsgUnlockReminder)_离车关门落锁提示_触发告警后关副驾门恢复")
    @pytest.mark.full
    def test_caseid_1985359(self): 
        hint = 'Cannot unLock'
        self.dk.set_cenlock_sts(1)  
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        sleep(0.5)
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        sleep(1)
        self.dk.send_walk_away_lock_cmd()
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 3)
        sleep(5)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @allure.title("解闭锁提醒4(MsgUnlockReminder)_离车关门落锁提示_触发告警后关左后门恢复")
    @pytest.mark.full
    def test_caseid_1985360(self): 
        hint = 'Cannot unLock'
        self.dk.set_cenlock_sts(1)  
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        sleep(0.5)
        self.dk.set_door_sts([0, 0, 1, 0, 0])
        sleep(1)
        self.dk.send_walk_away_lock_cmd()
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 3)
        sleep(5)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @allure.title("解闭锁提醒4(MsgUnlockReminder)_离车关门落锁提示_触发告警后关右后门恢复")
    @pytest.mark.full
    def test_caseid_1985361(self): 
        hint = 'Cannot unLock'
        self.dk.set_cenlock_sts(1)  
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        sleep(0.5)
        self.dk.set_door_sts([0, 0, 0, 1, 0])
        sleep(1)
        self.dk.send_walk_away_lock_cmd()
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 3)
        sleep(5)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @allure.title("解闭锁提醒4(MsgUnlockReminder)_离车关门落锁提示_触发告警后触发车外提示")
    @pytest.mark.full
    def test_caseid_1985362(self): 
        hint = 'Cannot unLock'
        self.dk.set_cenlock_sts(1)  
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        sleep(0.5)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_walk_away_lock_cmd()
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 3)
        self.sd_tester.change_usage_mode(2)
        self.dk.send_rke_close_door_and_lock()
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '2'}]})
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0) 
        # todo 
        self.dk.send_walk_away_lock_cmd() # 再次触发离车闭锁，确认计时器停止
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 3)

    @allure.title("解闭锁提醒4(MsgUnlockReminder)_离车关门落锁提示_触发告警后触发车内提示")
    @pytest.mark.full
    def test_caseid_1985363(self): 
        hint = 'Cannot unLock'
        self.dk.set_cenlock_sts(1)  
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        sleep(0.5)
        self.dk.set_door_sts([1, 0, 0, 0, 0]) # 开门主动上切至convenience; 从inactive上切convenience后300ms后会主动上切active自检
        sleep(0.5)
        self.sd_tester.change_usage_mode(2)
        self.dk.send_walk_away_lock_cmd()
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 3)
        sleep(3)
        self.sd_tester.change_usage_mode(11)
        self.partner.send_method_request("DoorService_client", 'SetAutoCloseTrigger', {"trigger": 0}) #打开D档自动关门
        self.dk.set_chassis_service_gear('GearD')
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]})
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @allure.title("解闭锁提醒4(MsgUnlockReminder)_离车关门落锁提示_触发告警后关尾门不恢复")
    @pytest.mark.full
    def test_caseid_1985364(self): 
        hint = 'Cannot unLock'
        self.dk.set_cenlock_sts(1)  
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        sleep(0.5)
        self.dk.set_door_sts([1, 0, 0, 0, 1])      
        self.dk.send_walk_away_lock_cmd()
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 3)
        self.partner.empty_all(3)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.ck_no_specific_event_and_GetWarningMsgList(hint, 3, timeout=4)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @allure.title("解闭锁提醒4(MsgUnlockReminder)_离车关门落锁提示_开四门触发告警后依次关门")
    @pytest.mark.smoke
    def test_caseid_1985388(self): 
        hint = 'Cannot unLock'
        self.dk.set_cenlock_sts(1)  
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        sleep(0.5)
        self.dk.set_door_sts([1, 1, 1, 1, 0])      
        self.dk.send_walk_away_lock_cmd()
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 3)
        self.partner.empty_all(2)
        self.dk.set_door_sts([1, 1, 1, 0, 0]) 
        sleep(1)
        self.dk.set_door_sts([1, 1, 0, 0, 0]) 
        sleep(1)
        self.dk.set_door_sts([1, 0, 0, 0, 0]) 
        self.ck_no_specific_event_and_GetWarningMsgList(hint, 3, timeout=3)
        self.dk.set_door_sts([0, 0, 0, 0, 0]) 
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0, timeout=2) 

    @allure.title("解闭锁提醒4(MsgUnlockReminder)_服务启动默认值")
    @pytest.mark.full
    def test_caseid_1985389(self): 
        hint = 'Cannot unLock'
        self.dk.set_cenlock_sts(1)  
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        sleep(0.5)
        self.dk.set_door_sts([1, 0, 0, 0, 0])   
        self.dk.send_walk_away_lock_cmd()
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 3)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '0'}]}, timeout=3)

    @allure.title("获取&通知关门失败-请手动关门_lock=12_取值遍历")
    @pytest.mark.sanity
    def test_caseid_1943253(self):  
        hint = "Please Manual Close Door" 
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        #设置车门处于≤ 10%的位置
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrPercPosn', 1)
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetPosition", {"doors": [4]},{"out": [{"id": 0, "pos": 1}]}) # 获取开度百分比
        # targetPosition change to！=255 设置的值小于10
        self.partner.send_method_request('DoorService_client', 'SetPosition', {"doors": [{"id": 0, "pos": 0}]})
        tarPos=self.partner.send_request_and_return_resp(DOOR_SERVICE_CLIENT,"GetDoorActionRequest",{"doors":[4]})
        logger.info(f"打印门运动状态：{tarPos}") 
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetAntiPinch", {"doors": [0]}, {"out": [{"door": 0, "isAntiPinch": False}]}) # 获取防夹状态
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": [{"fault": 0, "faultMsg": "", "door": 4}]}) # 获取故障情况
        self.partner.empty_all()
        sleep(3) # 3s计时器
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetOpenCloseStatus",{"doors":[4]},{"out":[{"id":0,"isOpen":True}]})        
        self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", {"warnnings": {"lock": 12, "reminder": 0}})   
        self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", {"warnnings": {"lock": 0, "reminder": 0}})   
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": "1"}]})         
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)
        
    @allure.title("防盗报警信息")
    @pytest.mark.smoke
    def test_caseid_111622(self): # AlrmStsAlrmSt|Anti Theft
        hint = "Anti Theft"
        self.dk.set_cenlock_sts(1)
        sleep(2)
        self.dk.send_nfc_cmd() 
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmSt',1)
        self.partner.empty_all(32)
        self.dk.set_door_sts([0, 0, 0, 1, 0])
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorOpenerRiReSts', 5)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmSt',2)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorOpenerRiReSts', 1)
        sleep(285)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmSt',1)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)
        
    @allure.title("服务启动默认值")
    @pytest.mark.full
    def test_caseid_1983612(self):
        hint = "Anti Theft"
        self.dk.set_cenlock_sts(1)
        self.dk.send_nfc_cmd() 
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmSt',1)
        self.partner.empty_all(32)
        self.dk.set_door_sts([0, 0, 0, 1, 0])
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorOpenerRiReSts', 5)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmSt',2)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT, resume_all_bus=False)    
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": "0"}]})
        
@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIService_Entry")
@pytest.mark.lg
class TestEntryRKEWTIService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu, enable_inter_service=True)
        for process_name in ["monitor_em2.sh", "em2", "rke", "service_monitor"]:
            res = command_send(
                device_name="BGM",
                cmd=f"ps -ef |grep app |grep {process_name} |grep -v grep",
                timeout=60,
            )[1]
            pid = res.split()[1]
            command_send(device_name="BGM", cmd=f"kill -9 {pid}")
        sleep(2)
        command_send(device_name="BGM", cmd='su - service_monitor -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;/app/bin/service_monitor  -c /data/app/etc/service_monitor.json &"', timeout=15)
        self.partner = S2sBaseClass([("RKECtrlService", "server"),
                                     ("WTIService", "client"),
                                     ("KeyService", "client")])
        self.partner.method_default_timeout = 3
        self.partner.wait_for_service_reconnect(RKECTRL_SERVICE_SERVER)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.partner.empty_all(0.5)
    
    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)
        
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
        
    @allure.title("解闭锁提醒4_基于REK服务")
    @pytest.mark.sanity
    def test_caseid_1988375(self):
        hint = "Cannot unLock"
        self.partner.send_event_notify(RKECTRL_SERVICE_SERVER, "DigitalKeyReminderInfo",
                                              {"info": {"closeDoorOutsideReminder": False}})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(0)}]})
        
        self.partner.send_event_notify(RKECTRL_SERVICE_SERVER, "DigitalKeyReminderInfo",
                                              {"info":{"closeDoorOutsideReminder":True}})
 
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 2)
        self.partner.send_event_notify(RKECTRL_SERVICE_SERVER, "DigitalKeyReminderInfo",
                                              {"info": {"closeDoorOutsideReminder": False}})
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)
        
    @allure.title("解闭锁提醒4状态机_基于REK服务")
    @pytest.mark.full
    def test_caseid_1988376(self):
        hint = "Cannot unLock"
        self.partner.send_event_notify(RKECTRL_SERVICE_SERVER, "DigitalKeyReminderInfo",
                                              {"info": {"closeDoorOutsideReminder": False}})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(0)}]})
        
        self.dk.set_cenlock_sts(1)  
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        self.partner.empty_all(0.5)
        self.dk.set_door_sts([1, 0, 0, 0, 0])   
        self.dk.send_walk_away_lock_cmd()
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 3)
        
        self.partner.send_event_notify(RKECTRL_SERVICE_SERVER, "DigitalKeyReminderInfo",
                                              {"info": {"closeDoorOutsideReminder": False}})
        self.ck_no_specific_event_and_GetWarningMsgList(hint, 3, timeout=3)
        self.partner.send_event_notify(RKECTRL_SERVICE_SERVER, "DigitalKeyReminderInfo",
                                              {"info": {"closeDoorOutsideReminder": True}})
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 2)
        self.partner.send_event_notify(RKECTRL_SERVICE_SERVER, "DigitalKeyReminderInfo",
                                              {"info": {"closeDoorOutsideReminder": False}})
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)
        
    @allure.title("解闭锁提醒4_基于REK&Entry服务")
    @pytest.mark.full
    def test_caseid_1988377(self):
        hint = "Cannot unLock"
        self.partner.send_event_notify(RKECTRL_SERVICE_SERVER, "DigitalKeyReminderInfo",
                                              {"info": {"closeDoorOutsideReminder": False}})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(0)}]})
        
        self.partner.send_event_notify(RKECTRL_SERVICE_SERVER, "DigitalKeyReminderInfo",
                                              {"info": {"closeDoorOutsideReminder": True}})
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 2)
        
        #通过entry设置Cannot unLock = 2
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.dk.set_door_sts([1, 0, 0, 0, 0]) # 开门主动上切至convenience
        sleep(0.5)
        self.sd_tester.change_usage_mode(2)
        self.dk.send_rke_close_door_and_lock() # 
        self.ck_no_specific_event_and_GetWarningMsgList(hint, 2, timeout=3)
        
        self.partner.send_event_notify(RKECTRL_SERVICE_SERVER, "DigitalKeyReminderInfo",
                                              {"info": { "closeDoorOutsideReminder": False}})
        #Entry NotifyLockWarning.warnnings.reminder 有回0机制，因此不会因为设置的reminder = 2，保持Cannot unLock = 2
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)
        #测试Cannot unLock = 1 - 2跳变逻辑
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.sd_tester.change_usage_mode(0xD)
        self.dk.set_drvr_seat_present()
        self.dk.set_four_door_unlock()
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3) 
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 498) 
        sleep(1.3)
        # self.ck_NotifyLockWarning(0, 1, ck_horn=False)   
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]})
        self.partner.send_event_notify(RKECTRL_SERVICE_SERVER, "DigitalKeyReminderInfo",
                                              {"info": {"closeDoorOutsideReminder": True}})
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 2)
        self.partner.send_event_notify(RKECTRL_SERVICE_SERVER, "DigitalKeyReminderInfo",
                                              {"info": {"closeDoorOutsideReminder": False}})
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)
        
        