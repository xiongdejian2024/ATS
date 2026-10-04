
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
import math
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
NFC_UWB_Key_Legacy_On_Passenger_Reminder = __import__("os").environ.get('XAT_CREDENTIAL____SOA_INTERFACE_WTI_TEST_WTISERVICE_CHASSIS_PY_NFC_UWB_KEY_LEGACY_ON_PASSENGER_REMINDER', "")


@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIService_Chassis")
@pytest.mark.aqx
class TestChassisWTIService(TestBase):

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("WTIService", "client"),
                                     ("EntryService", "client"),
                                     ("CentralLockService", "client"),
                                     ("ChassisService", "client"),
                                     ("KeyService", "client"),
                                     ("VehicleModeService", "client"),
                                     ("ClimateControlService", "client"),
                                     ("BonnetService", "client"),
                                     ("SteerWheelService", "client"),
                                     ("PedalService", "client")
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
        self.sd_tester.tester_present()
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'EntityKeyWhiteListVers', self.dk.last_sync_time_entity)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BLESlotKeyWhiteListVers', self.dk.last_sync_time_ble)       
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
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
                                              {"out": [{"name": hint, "info": str(info)}]}, timeout=1)

    def ck_WarningMsgList_and_GetWarningMsgList(self, hint, info, timeout=3):
        """校验指定warningMsgList事件，并请求WarningMsgList获取结果"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint, "info": str(info)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]}, timeout=timeout)

    def ck_no_specific_event_and_GetTelltaleList(self, hint, state, timeout=1):
        """校验无指定TelltaleList事件，并请求TelltaleList获取结果"""
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "TelltaleList", hint, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": hint, "state": str(state)}]}, timeout=timeout)

    def ck_TelltaleList_and_GetTelltaleList(self, hint, state, timeout=3):
        """校验指定TelltaleList事件，并请求TelltaleList获取结果"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                  {"list": [{"name": hint, "state": str(state)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": hint, "state": str(state)}]}, timeout=timeout)

    def reset_JiduVehicle_and_AirSuspens(self, value, sleeptime):
        '''修改车辆配置 value=1 Mars1, 2 Venus, 3 Other'''
        self.sd_tester.write_single_ccp(59, 2) # 默认均为高配 kCCPAirSuspens=2
        sleep(2)
        self.sd_tester.write_single_ccp(950, value) # kCCPJiduVehicleType
        sleep(2)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(sleeptime)
                
    def setNoPowerOutput(self, signal=[0, 0, 0, 0], sleeptime=0):
        '''无动力输出'''    
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', signal[0]) # 0/1
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', signal[1])
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', signal[2])
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', signal[3])  
        sleep(sleeptime)
        
    def boon_all_open_close(self, swith):
        '''前舱盖开关状态 swith=0 开  swith=1 关 '''
        if swith == 0:
            self.io.hood_door1_open()
            self.io.hood_door2_open()
        else:
            self.io.hood_door1_close()
            self.io.hood_door2_open()
        sleep(1)
        
    def set_Launch_Mode_Operation_Reminder(self, status, fault, brk, acc, road, info, sleeptime=1):
        ''' 
        弹射起步引导提示信息 前置条件处理
        status = LaunchMode.info.status  
        fault = LaunchMode.info.fault
        brk=BrkPedlTrvlAct, acc=AccrPedlRatAccrPedlRat, road=RoadInclnRoadIncln
        '''
        dict={0:1, 1:2, 2:3, 3:4, 4:0, 5:5} # status:信号值
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg', fault)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  dict[status]) # LaunchMode.info.status
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', brk) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', acc) 
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr11, 'RoadInclnRoadIncln', road)
        sleep(sleeptime)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, 
                                              {"out": [{"name": "Launch Mode Operation Reminder" , "info": str(info)}]}, timeout=3)     
        self.partner.empty_all()

    @allure.title("获取&通知ABS故障指示灯_debounce确认_UsgMod从0切至13_debounce时间内命中故障2")  
    @pytest.mark.full
    def test_caseid_1984421(self): # 接受到BrkAndAbsWarnIndcnReqAbsWarnIndcnReq=1时，无需debounce
        hint = "ABS Failed"
        self.sd_tester.change_usage_mode(0) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 3)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 1)
        self.sd_tester.change_usage_mode(13) 
        self.ck_TelltaleList_and_GetTelltaleList(hint, 2) # 命中故障2，没有debounce

    @allure.title("获取&通知ABS故障指示灯_debounce确认_UsgMod从1切至11_debounce时间内命中故障1")  
    @pytest.mark.full
    def test_caseid_1984423(self):
        hint = "ABS Failed"
        self.sd_tester.change_usage_mode(1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 3)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]}, timeout=3) 
        self.partner.empty_all() 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 0)
        self.sd_tester.change_usage_mode(11) 
        self.ck_TelltaleList_and_GetTelltaleList(hint, 1) # 2s后上报      
        
    @allure.title("获取&通知ABS故障指示灯_debounce确认_UsgMod从2切至11_debounce时间内命中故障0")  
    @pytest.mark.full
    def test_caseid_1984420(self):
        hint = "ABS Failed"
        self.sd_tester.change_usage_mode(2) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 0)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "1"}]}, timeout=3) 
        self.partner.empty_all() 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 3)
        self.sd_tester.change_usage_mode(11) 
        self.ck_TelltaleList_and_GetTelltaleList(hint, 0) # 命中故障0，没有debounce
                
    @allure.title("获取&通知ABS故障指示灯_debounce确认_UsgMod从2切至11_无异常上报")  
    @pytest.mark.full
    def test_caseid_1984416(self):
        hint = "ABS Failed"
        self.sd_tester.change_usage_mode(2) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 0)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "1"}]}, timeout=3) 
        self.partner.empty_all() 
        self.sd_tester.change_usage_mode(11) 
        self.ck_no_specific_event_and_GetTelltaleList(hint, 1)   
        
    @allure.title("获取&通知ABS故障指示灯_debounce确认_UsgMod从0/1/2切至11/13")  
    @pytest.mark.full
    def test_caseid_1943259(self):
        hint = "ABS Failed"
        self.sd_tester.change_usage_mode(1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 4)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 0)
        for usgMod1 in [0, 1, 2]:             
            for usgMod2 in [11, 13]:                      
                self.sd_tester.change_usage_mode(usgMod1)   
                self.partner.empty_all(2)   
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})  
                self.sd_tester.change_usage_mode(usgMod2) 
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]}) 
                self.ck_TelltaleList_and_GetTelltaleList(hint, 1) # 2s后上报  

    @allure.title("获取&通知ABS故障指示灯_UsgMod=0/1/2_不处理信号丢失")   
    @pytest.mark.full
    def test_caseid_1943264(self): 
        hint = "ABS Failed"
        self.sd_tester.change_usage_mode(1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "2"}]}, timeout=3)
        self.partner.empty_all()
        for UsgMod in [2, 1, 0]: 
            self.sd_tester.change_usage_mode(UsgMod)  
            self.ipdu.pause_bus_send("backbonefr")
            sleep(2) 
            self.ck_no_specific_event_and_GetTelltaleList(hint, 2)  # 不处理信号丢失
            self.ipdu.resume_bus_send("backbonefr")    
            self.ck_no_specific_event_and_GetTelltaleList(hint, 2) 
        
    @allure.title("获取&通知ABS故障指示灯_UsgMod=11/13_处理信号丢失")   
    @pytest.mark.sanity 
    def test_caseid_1943266(self): # fr BrkAndAbsWarnIndcnReqAbsWarnIndcnReq|fr BrkMsgWarnReq|ABS Failed|wti current mode|AutHldSoftSwtEnaSts timeout
        hint = "ABS Failed"
        self.sd_tester.change_usage_mode(11)        
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "2"}]}, timeout=3)
        self.partner.empty_all()
        for UsgMod in [13, 11]: 
            self.sd_tester.change_usage_mode(UsgMod)  
            logger.info(f"打印当前返回值usgMod={UsgMod}")
            self.ipdu.pause_bus_send("backbonefr")
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)  # 信号丢失 Req=0
            self.ipdu.resume_bus_send("backbonefr")  
            self.ck_TelltaleList_and_GetTelltaleList(hint, 2) 

    @allure.title("获取&通知ABS故障指示灯_UsgMod=2/11/13_E2E校验失败")   
    @pytest.mark.full
    def test_caseid_1943268(self): # fr BrkAndAbsWarnIndcnReqAbsWarnIndcnReq|fr BrkMsgWarnReq|ABS Failed|wti current mode|BrkAndAbsWarnIndcnReqAbsWarnIndcnReq_1
        hint = "ABS Failed"
        self.sd_tester.change_usage_mode(random.choice([2, 11, 13]))   
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 1) # 1/2/3
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 1) # BrkAndAbsWarnIndcnReqAbsWarnIndcnReq_1
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "2"}]}, timeout=3)
        self.partner.empty_all(2)
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq')
            sleep(2)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)         
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 2)
            self.ck_no_specific_event_and_GetTelltaleList(hint, 1, timeout=3)    
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq')
        self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
        
    @allure.title("获取&通知ABS故障指示灯_UsgMod从0/1/2切至11/13_BrkAndAbsWarnIndcnReqAbsWarnIndcnReq=0")   
    @pytest.mark.full
    def test_caseid_1984021(self): # fr BrkAndAbsWarnIndcnReqAbsWarnIndcnReq|fr BrkMsgWarnReq|ABS Failed|wti current mode
        hint = "ABS Failed"
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 0) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 0)
        for UsgMod1 in [0, 1, 2]: 
            for UsgMod2 in [11, 13]: 
                self.sd_tester.change_usage_mode(UsgMod1)  
                sleep(2)
                self.sd_tester.change_usage_mode(UsgMod2) 
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
                self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
                self.sd_tester.change_usage_mode(UsgMod1)  
                
    @allure.title("获取&通知ABS故障指示灯_UsgMod遍历13/11/1/0_BrkAndAbsWarnIndcnReqAbsWarnIndcnReq=0")   
    @pytest.mark.smoke
    def test_caseid_1984022(self): # fr BrkAndAbsWarnIndcnReqAbsWarnIndcnReq|fr BrkMsgWarnReq|ABS Failed|wti current mode
        hint = "ABS Failed"
        self.sd_tester.change_usage_mode(11)  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 0) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 0)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "1"}]}, timeout=3)
        self.partner.empty_all()
        for UsgMod in [13, 11, 1, 0]: 
            self.sd_tester.change_usage_mode(UsgMod)  
            value=1 if UsgMod in [11, 13] else 0
            if UsgMod == 1:
                self.ck_TelltaleList_and_GetTelltaleList(hint, value)
            else:
                self.ck_no_specific_event_and_GetTelltaleList(hint, value)

    @allure.title("获取&通知ABS故障指示灯_UsgMod=2_BrkAndAbsWarnIndcnReqAbsWarnIndcnReq=0_BrkMsgWarnReq遍历")   
    @pytest.mark.full
    def test_caseid_1984023(self): # fr BrkAndAbsWarnIndcnReqAbsWarnIndcnReq|fr BrkMsgWarnReq|ABS Failed|wti current mode
        hint = "ABS Failed"
        self.sd_tester.change_usage_mode(2)  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 0) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 0)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]}, timeout=3)
        self.partner.empty_all()
        for i in range(8):
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', i)     
            value=1 if i in [1, 2, 3] else 0
            if i in [1, 4]:
                self.ck_TelltaleList_and_GetTelltaleList(hint, value)
            else:
                self.ck_no_specific_event_and_GetTelltaleList(hint, value)

    @allure.title("获取&通知ABS故障指示灯_UsgMod遍历_BrkAndAbsWarnIndcnReqAbsWarnIndcnReq=1")   
    @pytest.mark.full
    def test_caseid_1984024(self): # fr BrkAndAbsWarnIndcnReqAbsWarnIndcnReq|fr BrkMsgWarnReq|ABS Failed|wti current mode
        hint = "ABS Failed"
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 2) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "2"}]}, timeout=3)
        self.partner.empty_all()
        for UsgMod in [0, 1, 2, 11, 13]: 
            self.sd_tester.change_usage_mode(UsgMod)  
            self.ck_no_specific_event_and_GetTelltaleList(hint, 2)
            
    @allure.title("获取&通知ABS故障指示灯_故障从2至1至0")   
    @pytest.mark.sanity
    def test_caseid_1984025(self): # fr BrkAndAbsWarnIndcnReqAbsWarnIndcnReq|fr BrkMsgWarnReq|ABS Failed|wti current mode
        hint = "ABS Failed"
        self.sd_tester.change_usage_mode(11)  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "2"}]}, timeout=3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 0)  
        self.ck_TelltaleList_and_GetTelltaleList(hint, 1)  
        self.sd_tester.change_usage_mode(1)  
        self.ck_TelltaleList_and_GetTelltaleList(hint, 0)  

    def set_DisplayReqSts(self, signal=[0, 0, 2, 2], value=[0, 0], sleep_time=2):
        # 设置EPB显示请求状态，默认设0
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', signal[0])
        self.ipdu.set(self.ipdu.backbonefr.BbmVcuBackBoneFr02, 'EpbDrvrDispSec', signal[1])
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq', signal[2])
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq', signal[3])  
        sleep(sleep_time)
        self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": value[0], "lowPriSts": value[1]}}, timeout=3)
                
    @allure.title("EPB警告信息_UsgMod=11_故障值遍历")
    @pytest.mark.sanity
    def test_caseid_1960038(self): # EPB Warning1|wti current mode|fr EpbDrvrDisp|EPBDisplayReqSts,sts
        hint = "EPB Warning1"
        self.sd_tester.change_usage_mode(11)
        self.set_DisplayReqSts()
        dict1={3:1, 1:2, 4:3, 15:4, 6:5, 8:6, 14:7, 7:8, 2:9, 13:10, 5:11, 11:0, 9:13, 0:0, 10:0, 12:0} # 信号值=11时，highPriSts=12，只有usgMod=1时，参数才为12
        self.partner.empty_all()
        for key, value in dict1.items():
            self.ipdu.set(self.ipdu.backbonefr.BbmVcuBackBoneFr02, 'EpbDrvrDispSec', key)
            if key in [10, 12]:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, value)
            else:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, value)
                    
    @allure.title("EPB警告信息_UsgMod遍历_info=1")
    @pytest.mark.full
    def test_caseid_1984030(self): # EPB Warning1|wti current mode|fr EpbDrvrDisp|EPBDisplayReqSts,sts
        hint = "EPB Warning1"
        self.set_DisplayReqSts()
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 3)
            if UsgMod in [13, 11]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
            
    @allure.title("EPB警告信息_UsgMod遍历_info=2")
    @pytest.mark.full
    def test_caseid_1984033(self): # EPB Warning1|wti current mode|fr EpbDrvrDisp|EPBDisplayReqSts,sts
        hint = "EPB Warning1"
        self.set_DisplayReqSts()
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 1)
            if UsgMod in [13, 11]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 2)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
            
    @allure.title("EPB警告信息_UsgMod遍历_info=3")
    @pytest.mark.full
    def test_caseid_1984034(self): 
        hint = "EPB Warning1"
        self.set_DisplayReqSts()
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 4)
            if UsgMod in [13, 11, 2, 1]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 3)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
            
    @allure.title("EPB警告信息_UsgMod遍历_info=4")
    @pytest.mark.full
    def test_caseid_1984035(self): 
        hint = "EPB Warning1"
        self.set_DisplayReqSts()
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 15)
            if UsgMod in [13, 11]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 4)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
            
    @allure.title("EPB警告信息_UsgMod遍历_info=5")
    @pytest.mark.full
    def test_caseid_1984036(self):
        hint = "EPB Warning1"
        self.set_DisplayReqSts()
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 6)
            if UsgMod in [13, 11, 2, 1]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 5)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
            
    @allure.title("EPB警告信息_UsgMod遍历_info=6")
    @pytest.mark.full
    def test_caseid_1984037(self):
        hint = "EPB Warning1"
        self.set_DisplayReqSts()
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 8)
            if UsgMod in [13, 11]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 6)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)

    @allure.title("EPB警告信息_UsgMod遍历_info=7")
    @pytest.mark.smoke
    def test_caseid_1984038(self):
        hint = "EPB Warning1"
        self.set_DisplayReqSts()
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 14)
            if UsgMod in [13, 11]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 7)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
                        
    @allure.title("EPB警告信息_UsgMod遍历_info=8")
    @pytest.mark.full
    def test_caseid_1984039(self):
        hint = "EPB Warning1"
        self.set_DisplayReqSts()
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 7)
            if UsgMod in [13, 11, 2, 1]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 8)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
            
    @allure.title("EPB警告信息_UsgMod遍历_info=9")
    @pytest.mark.full
    def test_caseid_1984040(self):
        hint = "EPB Warning1"
        self.set_DisplayReqSts()
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 2)
            if UsgMod in [13, 11, 2, 1]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 9)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
            
    @allure.title("EPB警告信息_UsgMod遍历_info=10")
    @pytest.mark.full
    def test_caseid_1984041(self):
        hint = "EPB Warning1"
        self.set_DisplayReqSts()
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 13)
            if UsgMod in [13, 11]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 10)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
            
    @allure.title("EPB警告信息_UsgMod遍历_info=11")
    @pytest.mark.full
    def test_caseid_1984042(self):
        hint = "EPB Warning1"
        self.set_DisplayReqSts()
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 5)
            if UsgMod in [13, 11]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 11)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
            
    @allure.title("EPB警告信息_UsgMod遍历_info=12")
    @pytest.mark.full
    def test_caseid_1984043(self):
        hint = "EPB Warning1"
        self.set_DisplayReqSts()
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 11)
            if UsgMod in [1]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 12)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
            
    @allure.title("EPB警告信息_UsgMod遍历_info=13")
    @pytest.mark.full
    def test_caseid_1984044(self):
        hint = "EPB Warning1"
        self.set_DisplayReqSts()
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 9)
            if UsgMod in [13, 11]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 13)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
            
    @allure.title("EPB警告信息MsgEPBWarning2_UsgMod遍历_info=2")
    @pytest.mark.full
    def test_caseid_1984046(self): # EPB Warning1|EPB Warning2|wti current mode|fr EpbDrvrDisp|EPBDisplayReqSts,sts
        hint = "EPB Warning2"
        self.set_DisplayReqSts(signal=[3, 3, 2, 2], value=[1, 0])
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 1)
            if UsgMod in [13, 11]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 2)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)

    @allure.title("EPB警告信息MsgEPBWarning2_UsgMod遍历_info=3")
    @pytest.mark.full
    def test_caseid_1984050(self): # EPB Warning1|EPB Warning2|wti current mode|fr EpbDrvrDisp|EPBDisplayReqSts,sts
        hint = "EPB Warning2"
        self.set_DisplayReqSts(signal=[3, 3, 2, 2], value=[1, 0])
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 4)
            if UsgMod in [13, 11, 2, 1]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 3)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
           
    @allure.title("EPB警告信息MsgEPBWarning2_UsgMod遍历_info=4")
    @pytest.mark.full
    def test_caseid_1984052(self): # EPB Warning1|EPB Warning2|wti current mode|fr EpbDrvrDisp|EPBDisplayReqSts,sts
        hint = "EPB Warning2"
        self.set_DisplayReqSts(signal=[3, 3, 2, 2], value=[1, 0])
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 15)
            if UsgMod in [13, 11]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 4)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)

    @allure.title("EPB警告信息MsgEPBWarning2_UsgMod遍历_info=5")
    @pytest.mark.full
    def test_caseid_1984053(self): # EPB Warning1|EPB Warning2|wti current mode|fr EpbDrvrDisp|EPBDisplayReqSts,sts
        hint = "EPB Warning2"
        self.set_DisplayReqSts(signal=[3, 3, 2, 2], value=[1, 0])
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 6)
            if UsgMod in [13, 11, 2, 1]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 5)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
       
    @allure.title("EPB警告信息MsgEPBWarning2_UsgMod遍历_info=6")
    @pytest.mark.smoke
    def test_caseid_1984054(self): # EPB Warning1|EPB Warning2|wti current mode|fr EpbDrvrDisp|EPBDisplayReqSts,sts
        hint = "EPB Warning2"
        self.set_DisplayReqSts(signal=[3, 3, 2, 2], value=[1, 0])
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 8)
            if UsgMod in [13, 11]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 6)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
            
    @allure.title("EPB警告信息MsgEPBWarning2_UsgMod遍历_info=7")
    @pytest.mark.full
    def test_caseid_1984055(self): # EPB Warning1|EPB Warning2|wti current mode|fr EpbDrvrDisp|EPBDisplayReqSts,sts
        hint = "EPB Warning2"
        self.set_DisplayReqSts(signal=[3, 3, 2, 2], value=[1, 0])
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 14)
            if UsgMod in [13, 11]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 7)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)

    @allure.title("EPB警告信息MsgEPBWarning2_UsgMod遍历_info=8")
    @pytest.mark.full
    def test_caseid_1984061(self): # EPB Warning1|EPB Warning2|wti current mode|fr EpbDrvrDisp|EPBDisplayReqSts,sts
        hint = "EPB Warning2"
        self.set_DisplayReqSts(signal=[3, 3, 2, 2], value=[1, 0])
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 7)
            if UsgMod in [13, 11, 2, 1]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 8)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)            
            
    @allure.title("EPB警告信息MsgEPBWarning2_UsgMod遍历_info=9")
    @pytest.mark.full
    def test_caseid_1984062(self): # EPB Warning1|EPB Warning2|wti current mode|fr EpbDrvrDisp|EPBDisplayReqSts,sts
        hint = "EPB Warning2"
        self.set_DisplayReqSts(signal=[3, 3, 2, 2], value=[1, 0])
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 2)
            if UsgMod in [13, 11, 2, 1]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 9)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
            
    @allure.title("EPB警告信息MsgEPBWarning2_UsgMod遍历_info=10")
    @pytest.mark.full
    def test_caseid_1984063(self): # EPB Warning1|EPB Warning2|wti current mode|fr EpbDrvrDisp|EPBDisplayReqSts,sts
        hint = "EPB Warning2"
        self.set_DisplayReqSts(signal=[3, 3, 2, 2], value=[1, 0])
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 13)
            if UsgMod in [13, 11]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 10)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)      
                        
    @allure.title("EPB警告信息MsgEPBWarning2_UsgMod遍历_info=11")
    @pytest.mark.full
    def test_caseid_1984064(self): # EPB Warning1|EPB Warning2|wti current mode|fr EpbDrvrDisp|EPBDisplayReqSts,sts
        hint = "EPB Warning2"
        self.set_DisplayReqSts(signal=[3, 3, 2, 2], value=[1, 0])
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 5)
            if UsgMod in [13, 11]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 11)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)  
            
    @allure.title("EPB警告信息MsgEPBWarning2_UsgMod遍历_info=12")
    @pytest.mark.sanity
    def test_caseid_1984065(self): # EPB Warning1|EPB Warning2|wti current mode|fr EpbDrvrDisp|EPBDisplayReqSts,sts
        hint = "EPB Warning2"
        self.set_DisplayReqSts(signal=[3, 3, 2, 2], value=[1, 0])
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 11)
            if UsgMod in [1]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 12)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)        
                        
    @allure.title("EPB警告信息MsgEPBWarning2_UsgMod遍历_info=13")
    @pytest.mark.full
    def test_caseid_1984066(self): # EPB Warning1|EPB Warning2|wti current mode|fr EpbDrvrDisp|EPBDisplayReqSts,sts
        hint = "EPB Warning2"
        self.set_DisplayReqSts(signal=[3, 3, 2, 2], value=[1, 0])
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 9)
            if UsgMod in [13, 11]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 13)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)  

    @allure.title("EPB警告信息MsgEPBWarning2_UsgMod=11_故障值遍历")
    @pytest.mark.sanity
    def test_caseid_1984077(self): # EPB Warning1|wti current mode|fr EpbDrvrDisp|EPBDisplayReqSts,sts
        hint = "EPB Warning2"
        self.sd_tester.change_usage_mode(11)
        self.set_DisplayReqSts(signal=[3, 3, 2, 2], value=[1, 0])
        dict1={1:2, 4:3, 15:4, 6:5, 8:6, 14:7, 7:8, 2:9, 13:10, 5:11, 11:0, 9:13, 0:0, 10:0, 12:0} # 信号值=11时，highPriSts=12，只有usgMod=1时，参数才为12
        self.partner.empty_all()
        for key, value in dict1.items():
            self.ipdu.set(self.ipdu.backbonefr.BbmVcuBackBoneFr02, 'EpbDrvrDispSec', key)
            if key in [10, 12]:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, value)
            else:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, value)
                
    @allure.title("EPB警告信息_服务启动默认值")
    @pytest.mark.full
    def test_caseid_1984078_1984079(self): # EPB Warning1|EPB Warning2|wti current mode|fr EpbDrvrDisp|EPBDisplayReqSts,sts
        self.sd_tester.change_usage_mode(11)
        self.set_DisplayReqSts(signal=[3, 1, 2, 2], value=[1, 2])
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": "EPB Warning1", "info": "1"}]}, timeout=3)  
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": "EPB Warning2", "info": "2"}]}, timeout=3)  
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": "EPB Warning1", "info": "0"}]}, timeout=3)  
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": "EPB Warning2", "info": "0"}]}, timeout=3)  
                                                                                                  
    @allure.title("获取&通知ESC故障指示灯_UsgMod从0/1/2切换至11/13_debounce确认_故障2")  
    @pytest.mark.full
    def test_caseid_1943270(self):
        hint = "ESC Failed"
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 0) # 1 or 2 or 3 or 4 or 5  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 1)
        for usgMod1 in [0, 1, 2]:             
            for usgMod2 in [11, 13]:                      
                self.sd_tester.change_usage_mode(usgMod1)      
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]}, timeout=3) 
                self.partner.empty_all(1)    
                self.sd_tester.change_usage_mode(usgMod2) 
                self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "TelltaleList", hint, timeout=1.5)
                self.ck_TelltaleList_and_GetTelltaleList(hint, 2) # 2s后上报
                
    @allure.title("获取&通知ESC故障指示灯_UsgMod从0/1/2切换至11/13_debounce确认_故障1")  
    @pytest.mark.full
    def test_caseid_1984449(self):
        hint = "ESC Failed"
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 0) # 1 or 2 or 3 or 4 or 5  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 0)
        for usgMod1 in [0, 1, 2]:             
            for usgMod2 in [11, 13]:                      
                self.sd_tester.change_usage_mode(usgMod1)      
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]}, timeout=3) 
                self.partner.empty_all()    
                self.sd_tester.change_usage_mode(usgMod2) 
                self.ck_no_specific_event_and_GetTelltaleList(hint, 0, timeout=1.5)
                self.ck_TelltaleList_and_GetTelltaleList(hint, 1) # 2s后上报                
        
    @allure.title("获取&通知ESC故障指示灯_debounce确认_UsgMod从2切至11_debounce时间内命中故障0")  
    @pytest.mark.full
    def test_caseid_1984450(self): # ESC Failed|fr EscWarnIndcnReqEscWarnIndcnReq|fr BrkMsgWarnReq|wti current mode
        hint = "ESC Failed"
        self.sd_tester.change_usage_mode(2) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 0)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "1"}]}, timeout=3) 
        self.partner.empty_all()
        self.sd_tester.change_usage_mode(11) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 3)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "TelltaleList", hint, timeout=1.5)
        self.ck_TelltaleList_and_GetTelltaleList(hint, 0) # 2s后上报
        
    @allure.title("获取&通知ESC故障指示灯_debounce确认_UsgMod从1切至11_debounce时间内命中故障1")  
    @pytest.mark.full
    def test_caseid_1984451(self): # ESC Failed|fr EscWarnIndcnReqEscWarnIndcnReq|fr BrkMsgWarnReq|wti current mode
        hint = "ESC Failed"
        self.sd_tester.change_usage_mode(1) 
        self.partner.empty_all(2) 
        self.sd_tester.change_usage_mode(11) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 0)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]}) 
        self.ck_no_specific_event_and_GetTelltaleList(hint, 1, timeout=1.5)   
        self.ck_TelltaleList_and_GetTelltaleList(hint, 1) # 2s后上报
        
    @allure.title("获取&通知ESC故障指示灯_debounce确认_UsgMod从2切至13_debounce时间内命中故障2")  
    @pytest.mark.full
    def test_caseid_1984452(self): # ESC Failed|fr EscWarnIndcnReqEscWarnIndcnReq|fr BrkMsgWarnReq|wti current mode
        hint = "ESC Failed"
        self.sd_tester.change_usage_mode(2) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 1)
        self.partner.empty_all(3) 
        self.sd_tester.change_usage_mode(13) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]}) 
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "TelltaleList", hint, timeout=1.5)
        self.ck_TelltaleList_and_GetTelltaleList(hint, 2) # 2s后上报
        
    @allure.title("获取&通知ESC故障指示灯_UsgMod=0/1/2_不处理信号丢失")  
    @pytest.mark.full
    def test_caseid_1943277(self):
        hint = "ESC Failed"
        self.sd_tester.change_usage_mode(random.choice([0, 1, 2]))    
        sleep(2)  # brkSysWarnMsgDisplayReqSts.sts=1 or 2 or 3 or 4 or 5   UsgMod =2超过2s  req=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 1) # 信号值0-7 与参数值一一映射
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]}, timeout=3)
        self.partner.empty_all()
        self.ipdu.pause_bus_send("backbonefr")
        self.ck_no_specific_event_and_GetTelltaleList(hint, 0, timeout=2.5)  # 不处理信号丢失 如果处理了，req=0，会触发1
        self.ipdu.resume_bus_send("backbonefr") 
        
    @allure.title("获取&通知ESC故障指示灯_UsgMod=11/13_处理信号丢失")  
    @pytest.mark.full
    def test_caseid_1943278(self): 
        hint = "ESC Failed"
        self.sd_tester.change_usage_mode(random.choice([11, 13]))     
        sleep(2)  # UsgMod =13超过2s  req=1 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 1)
        self.ck_TelltaleList_and_GetTelltaleList(hint, 2)
        self.ipdu.pause_bus_send("backbonefr") #信号丢失后，按照req=0处理 EscWarnIndcnReqEscWarnIndcnReq timeout
        self.ck_TelltaleList_and_GetTelltaleList(hint, 1, timeout=2.5)
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_TelltaleList_and_GetTelltaleList(hint, 2)    
            
    @allure.title("获取&通知ESC故障指示灯_UsgMod=2_E2E校验失败")  
    @pytest.mark.full
    def test_caseid_1943279(self): # fr BrkMsgWarnReq|EscWarnIndcnReqEscWarnIndcnReq|ESC Failed|wti current mode
        hint = "ESC Failed"
        self.sd_tester.change_usage_mode(2)    
        sleep(2)   
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 1)
        self.partner.empty_all(2)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq')
            sleep(2)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)  #  Req=0    
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 3)
            self.ck_no_specific_event_and_GetTelltaleList(hint, 1, timeout=3)   
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq')
        self.ck_TelltaleList_and_GetTelltaleList(hint, 0) 
        
    @allure.title("获取&通知ESC故障指示灯_UsgMod=11/13_E2E校验失败")  
    @pytest.mark.full
    def test_caseid_1960071(self):
        hint = "ESC Failed"
        self.sd_tester.change_usage_mode(random.choice([11, 13]))     
        sleep(2)   
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 1)
        self.partner.empty_all(2)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "2"}]})
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq')
            sleep(2)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)  #  Req=0  
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 3)
            self.ck_no_specific_event_and_GetTelltaleList(hint, 1, timeout=3)        
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq')
        self.ck_TelltaleList_and_GetTelltaleList(hint, 0) 
        
    @allure.title("获取&通知ESC故障指示灯_UsgMod=0/1_E2E校验失败")  
    @pytest.mark.full
    def test_caseid_1943280(self): 
        hint = "ESC Failed"
        self.sd_tester.change_usage_mode(random.choice([0, 1]))    
        self.partner.empty_all(2)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq')
            sleep(2)
            self.ck_no_specific_event_and_GetTelltaleList(hint, 0)  
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq')
        self.ck_no_specific_event_and_GetTelltaleList(hint, 0) 
 
    @allure.title("获取&通知EPB制动故障灯黄色_UsgMod出现跳变0-2-11")
    @pytest.mark.sanity
    def test_caseid_1943285(self): # 0切2 debounce之前满足置1  UsgMod出现跳变0-2-11  
        # fr BrkSysWarnIndcnReq|fr BrkSysWarnIndcnReqSec|fr BrkAndAbsWarnIndcnReqBrkWarnIndcnReq|fr BrkFldLvl|brkSysWarnIndicateReqSts|wti current mode|lastUM|Yellow Braking System Failed
        hint = "Yellow Braking System Failed"
        self.sd_tester.change_usage_mode(0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 1)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1) 
        sleep(1)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 1}) 
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
        # UsgMod从1切至2，如果 从1切至11/13，黄色故障灯逻辑 2s内，BrkSysWarnIndicateReqSts=0，2s后，才再次变为1
        self.sd_tester.change_usage_mode(2)  # 1s后上报1
        self.ck_TelltaleList_and_GetTelltaleList(hint, 1)  # debounce时间确认后才可以上报  
        self.partner.empty_all(1)   
        self.sd_tester.change_usage_mode(11)  # 2s计时器内，@value(0) Off ；2s后，@value(1) YELLOW
        self.ck_TelltaleList_and_GetTelltaleList(hint, 0)  # 2切11，立即上报0
        self.ck_TelltaleList_and_GetTelltaleList(hint, 1)  # 2切11，2s后上报1
           
    @allure.title("获取&通知EPB制动故障灯黄色_UsgMod出现跳变1-2-13_debounce时间内故障灯变为黄色")
    @pytest.mark.full
    def test_caseid_1960002(self): # 1切2 debounce时间内满足置1
        hint = "Yellow Braking System Failed"
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 1)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 0) 
        sleep(1) 
        # self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 1}) 
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
        self.sd_tester.change_usage_mode(2) # 开启debounce
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1)    
        self.ck_TelltaleList_and_GetTelltaleList(hint, 1)           
        self.sd_tester.change_usage_mode(13)  # 2s计时器内，@value(0) Off ；2s后，@value(1) YELLOW
        self.ck_TelltaleList_and_GetTelltaleList(hint, 0)  # 立即上报0 
        self.ck_TelltaleList_and_GetTelltaleList(hint, 1)  # 2s后上报1
        
    @allure.title("获取&通知EPB制动故障灯黄色_UsgMod出现跳变_0/1切换至11/13")
    @pytest.mark.full
    def test_caseid_1979752(self): 
        hint = "Yellow Braking System Failed"
        self.sd_tester.change_usage_mode(random.choice([0,1]))
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 1)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1) 
        sleep(1)  
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 1}) 
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
        self.sd_tester.change_usage_mode(random.choice([11,13])) # 2s计时器内，@value(0) Off ；2s后，@value(1) YELLOW
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
        self.ck_TelltaleList_and_GetTelltaleList(hint, 1)  #  2s后上报1
        
    @allure.title("获取&通知EPB制动故障灯黄色_UsgMod遍历")
    @pytest.mark.smoke
    def test_caseid_1903518(self):  # brkSysWarnIndicateReqSts
        # fr BrkSysWarnIndcnReq|fr BrkSysWarnIndcnReqSec|fr BrkAndAbsWarnIndcnReqBrkWarnIndcnReq|fr BrkFldLvl|brkSysWarnIndicateReqSts|wti current mode|lastUM|Yellow Braking System Failed
        hint = "Yellow Braking System Failed"
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 1)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1) 
        sleep(2) 
        for UsgMod1 in [0, 1]: 
            self.sd_tester.change_usage_mode(UsgMod1)  
            sleep(2)
            for UsgMod2 in [2, 11, 13]:
                self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 0)
                self.partner.empty_all(2)  
                self.sd_tester.change_usage_mode(UsgMod2)
                if UsgMod2==2:
                    self.ck_TelltaleList_and_GetTelltaleList(hint, 1) # 1s
                else: 
                    self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
                    self.ck_TelltaleList_and_GetTelltaleList(hint, 1) # 2s
                self.sd_tester.change_usage_mode(UsgMod1)  
                self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 1)  # 出现brkSysWarnIndicateReqSts事件
                sleep(2)        
                
    @allure.title("获取&通知EPB制动故障灯黄色_UsgMod下切遍历")
    @pytest.mark.full
    def test_caseid_1903588(self): 
        hint = "Yellow Braking System Failed"
        self.sd_tester.change_usage_mode(11)  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 0)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1) 
        sleep(1) 
        for usgMod in [13,11,2,1,0]:
            self.sd_tester.change_usage_mode(usgMod) 
            self.partner.empty_all(2) 
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 1)
            sleep(2)
            logger.info(f"打印当前循环值: usgMod={usgMod}")
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 0)
            sleep(2)
            if usgMod in [2, 11, 13]:
                self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
            else:
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
            self.partner.empty_all(1)     
    
    @allure.title("获取&通知EPB制动故障灯红色_UsgMod出现跳变1-2-13")
    @pytest.mark.sanity
    def test_caseid_1943368(self):   
        # fr BrkAndAbsWarnIndcnReqBrkWarnIndcnReq|fr BrkMsgWarnReq|Red Braking System Failed|BrkSysWarnMsgDisReqSts|BrkSysWarnIndicateReqSts|lastUM|wto current mode
        hint = "Red Braking System Failed"
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 0) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 0)
        sleep(3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 1)
        sleep(2)        
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 2}) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnMsgDisReqSts", {}, {"out": 1}, timeout=3)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
        self.sd_tester.change_usage_mode(2) 
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
        self.ck_TelltaleList_and_GetTelltaleList(hint, "1")  # debounce时间确认后才可以上报 
        self.sd_tester.change_usage_mode(13)  # 2s计时器内，@value(0) Off ；2s后，@value(2) RED
        self.ck_TelltaleList_and_GetTelltaleList(hint, 0)  # 立即上报0
        self.ck_TelltaleList_and_GetTelltaleList(hint, 1)  # 2s后上报1
        
    @allure.title("获取&通知EPB制动故障灯红色_UsgMod出现跳变0-2-11_debounce时间内故障灯变为红色")
    @pytest.mark.sanity
    def test_caseid_1979753(self):   
        hint = "Red Braking System Failed"
        self.sd_tester.change_usage_mode(0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 0)  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 7)
        sleep(3)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnMsgDisReqSts", {}, {"out": 7}, timeout=3)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 2}) 
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
        self.partner.empty_all() 
        self.sd_tester.change_usage_mode(2) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 1)  # 0-7
        self.ck_TelltaleList_and_GetTelltaleList(hint, "1")  # debounce时间确认后才可以上报 如果信号在切换的1s之后才发出去，则是立马上报
        self.sd_tester.change_usage_mode(11)  # 2s计时器内，@value(0) Off ；2s后，@value(2) RED
        self.ck_TelltaleList_and_GetTelltaleList(hint, 0)  # 立即上报0
        self.ck_TelltaleList_and_GetTelltaleList(hint, 1)  # 2s后上报1
        
    @allure.title("获取&通知EPB制动故障灯红色_UsgMod出现跳变_0/1切换至11/13")
    @pytest.mark.sanity
    def test_caseid_1979754(self):   
        hint = "Red Braking System Failed"
        self.sd_tester.change_usage_mode(random.choice([0,1]))
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 0)  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 0)  # 0-7
        sleep(3)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnMsgDisReqSts", {}, {"out": 0}, timeout=3)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 2}, timeout=3) 
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]}, timeout=3)
        self.partner.empty_all(2) 
        self.sd_tester.change_usage_mode(random.choice([11,13]))  # 2s计时器内，@value(0) Off ；2s后，@value(2) RED
        self.ck_no_specific_event_and_GetTelltaleList(hint, 0)  # 1s后上报0
        self.ck_TelltaleList_and_GetTelltaleList(hint, 1)  # 再过1s后上报1
        
    @allure.title("获取&通知EPB制动故障灯红色_UsgMod遍历")
    @pytest.mark.sanity
    def test_caseid_1979829(self):  
        # fr BrkSysWarnIndcnReq|fr BrkSysWarnIndcnReqSec|fr BrkAndAbsWarnIndcnReqBrkWarnIndcnReq|fr BrkFldLvl|brkSysWarnIndicateReqSts|wti current mode|lastUM|Red Braking System Failed
        hint = "Red Braking System Failed"
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 0)  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 0)  # 0-7
        sleep(3) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1)  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 1)  # 0-7
        self.partner.empty_all(2)  
        for UsgMod1 in [0, 1]: 
            self.sd_tester.change_usage_mode(UsgMod1)  
            sleep(2)
            for UsgMod2 in [2, 11, 13]:
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 0)  
                self.partner.empty_all(3)  
                self.sd_tester.change_usage_mode(UsgMod2)
                if UsgMod2==2:
                    self.ck_TelltaleList_and_GetTelltaleList(hint, 1) # 1s
                else: 
                    self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
                    self.ck_TelltaleList_and_GetTelltaleList(hint, 1) # 2s
                self.sd_tester.change_usage_mode(UsgMod1)  
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1)    # 出现brkSysWarnIndicateReqSts事件
                sleep(2)     
                
    @allure.title("获取&通知EPB制动故障灯红色_UsgMod下切遍历")
    @allure.testcase('test_caseid_1943285')
    @pytest.mark.sanity
    def test_caseid_1979833(self): 
        hint = "Red Braking System Failed"
        self.sd_tester.change_usage_mode(11)  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 0)  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 0)  # 0-7
        sleep(3) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 1)  # 0-7
        self.partner.empty_all(2)  
        for usgMod in [13,11,2,1,0]:
            self.sd_tester.change_usage_mode(usgMod) 
            self.partner.empty_all(2) 
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1)  
            sleep(2)
            logger.info(f"打印当前循环值: usgMod={usgMod}")
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]}, timeout=3)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 0)  
            sleep(2)
            if usgMod in [2, 11, 13]:
                self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
            else:
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
            self.partner.empty_all(1)                  
                        
    @allure.title("获取&通知ESC关闭指示灯_UsgMod出现跳变_0/1切换至2/11/13_debounce确认")
    @allure.testcase('test_caseid_1943370')
    @pytest.mark.sanity
    def test_caseid_1943370(self): #  todo  DrvModEscOffDrvModEscOff|EscStEscSt|ESC Off|wti curent mode
        hint = "ESC Off"
        self.sd_tester.change_usage_mode(random.choice([0,1]))
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DrvModEscOffDrvModEscOff', 1) # DrvModEscOffDrvModEscOf = 1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 1) #或者 EscStEscSt = 0 or 4
        sleep(1)
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "escOffIndicateLightSts", {"sts": True})    
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
        self.sd_tester.change_usage_mode(2)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
        self.ck_TelltaleList_and_GetTelltaleList(hint, "1")  # 1s后才可以上报   
        self.sd_tester.change_usage_mode(random.choice([11,13]))  
        self.ck_no_specific_event_and_GetTelltaleList(hint, "1") 
        
    @allure.title("获取&通知ESC关闭指示灯_UsgMod切换遍历")
    @allure.testcase('test_caseid_1943285')
    @pytest.mark.full
    def test_caseid_1960014(self):  
        hint = "ESC Off"
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DrvModEscOffDrvModEscOff', 0) # DrvModEscOffDrvModEscOf = 1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0) #或者 EscStEscSt = 0 or 4 
        self.partner.empty_all(2)  
        for UsgMod1 in [0, 1]: 
            self.sd_tester.change_usage_mode(UsgMod1)  
            sleep(2)
            for UsgMod2 in [2, 11, 13]: 
                self.partner.empty_all(3)  
                self.sd_tester.change_usage_mode(UsgMod2) 
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
                self.ck_TelltaleList_and_GetTelltaleList(hint, 1) # 1s
                self.sd_tester.change_usage_mode(UsgMod1)  
                self.ck_TelltaleList_and_GetTelltaleList(hint, 0) 
                sleep(2)     
                
    @allure.title("获取&通知ESC关闭指示灯_UsgMod依次下切")
    @pytest.mark.smoke
    def test_caseid_1979844(self): 
        hint = "ESC Off"
        self.sd_tester.change_usage_mode(11)  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DrvModEscOffDrvModEscOff', 0) # DrvModEscOffDrvModEscOf = 1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0) #或者 EscStEscSt = 0 or 4  
        self.partner.empty_all(2)
        for usgMod in [13,11,2,1,0]:
            self.sd_tester.change_usage_mode(usgMod) 
            logger.info(f"打印当前循环值: usgMod={usgMod}")
            if usgMod in [2, 11, 13]: 
                self.ck_no_specific_event_and_GetTelltaleList(hint, 1)
            elif usgMod==1:
                self.ck_TelltaleList_and_GetTelltaleList(hint, 0) 
            elif usgMod==0:
                self.ck_no_specific_event_and_GetTelltaleList(hint, 0)  
            self.partner.empty_all(1)                                                         
        
    @allure.title("获取&通知减速和滑行提示信息_取值遍历")
    @pytest.mark.smoke
    def test_caseid_1943222(self): 
        hint = "EPedal Function Indication"        
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr38, 'EPedlDrvrIndcnMsg', 1)
        sleep(1)
        for i in range(4):
            logger.info(f"当前信号值：{i}")
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr38, 'EPedlDrvrIndcnMsg', i)
            sleep(0.5)
            self.ck_WarningMsgList_and_GetWarningMsgList(hint, i)        
        
    @allure.title("获取&通知EPB故障信息/驻车系统故障_信号值为1_UsgMod遍历")
    @pytest.mark.sanity
    def test_caseid_1943225(self):   #  fr BrkRelsWarnReq|EPB Sys Failure|wti current mode
        hint = "EPB Sys Failure"    
        self.sd_tester.change_usage_mode(0) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkRelsWarnReq', 1)      
        sleep(2)  
        for usgMod1 in [0, 1]:   
            self.partner.empty_all(1)             
            self.sd_tester.change_usage_mode(usgMod1) 
            for usgMod2 in [2, 11, 13]:     
                self.partner.empty_all(1)           
                self.sd_tester.change_usage_mode(usgMod2) # 上切
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)  # 需要debounce确认           
                self.partner.empty_all(1)
                self.sd_tester.change_usage_mode(usgMod1) # 下切
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)  # 不需要debounce确认

    @allure.title("获取&通知EPB故障信息/驻车系统故障_信号值为0_UsgMod遍历")
    @pytest.mark.sanity
    def test_caseid_1943256(self):   #  fr BrkRelsWarnReq|EPB Sys Failure|wti current mode|lastUM  1.3 重复上报偏差接受 1.4无重复上报
        hint = "EPB Sys Failure"    
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkRelsWarnReq', 0)  
        sleep(2)      
        for usgMod1 in [0, 1]:             
            self.sd_tester.change_usage_mode(usgMod1) 
            for usgMod2 in [2, 11, 13]:     
                self.partner.empty_all(2)           
                self.sd_tester.change_usage_mode(usgMod2) # 上切
                # self.ck_no_specific_event_and_GetWarningMsgList(hint, 0) # 重复上报
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=2)
                self.sd_tester.change_usage_mode(usgMod1) # 下切
                # self.ck_no_specific_event_and_GetWarningMsgList(hint, 0) # 重复上报
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=2)       
                
    @allure.title("获取&通知EPB故障信息/驻车系统故障_UsgMod遍历_信号遍历")
    @allure.testcase('test_caseid_1979815')
    @pytest.mark.sanity
    def test_caseid_1979815(self):  # fr BrkRelsWarnReq|EPB Sys Failure|wti current mode|lastUM
        hint = "EPB Sys Failure" 
        self.sd_tester.change_usage_mode(1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkRelsWarnReq', 0)
        sleep(2)
        for usgMod in [0, 1, 2, 11, 13]: 
            self.sd_tester.change_usage_mode(usgMod) 
            self.partner.empty_all(2) 
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkRelsWarnReq', 0)
            sleep(2)
            logger.info(f"打印当前循环值: usgMod={usgMod}")
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkRelsWarnReq', 1)
            sleep(2)
            if usgMod in [2, 11, 13]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
            else:
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]})
            self.partner.empty_all(1)
                
    @allure.title("获取&通知EPB故障信息/驻车系统故障_信号丢失")
    @allure.testcase('test_caseid_1943226')
    @pytest.mark.full
    def test_caseid_1943226(self):  # BrkRelsWarnReq|EPB Sys Failure|wti current mode
        hint = "EPB Sys Failure" 
        self.sd_tester.change_usage_mode(0) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkRelsWarnReq', 0)
        sleep(2)
        for usgMod in [0, 1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usgMod) 
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]})
            self.partner.empty_all(2)   
            try:
                self.ipdu.pause_bus_send("backbonefr")
                if usgMod in [0, 1]:
                    sleep(2)
                    self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]})
                else:
                    self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1, timeout=2.5) 
            except Exception as error:
                self.ipdu.resume_bus_send("backbonefr")
                assert False,error
            else:
                self.ipdu.resume_bus_send("backbonefr") 
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}) 
        
    @allure.title("弹射起步失败提示信息_Status.sts=1_LaunchMode.info.fault&status遍历")
    @pytest.mark.sanity
    def test_caseid_1988498(self): # LaunchMode,fault|Launch Mode Prompt
        hint = 'Launch Mode Prompt'
        self.boon_all_open_close(1) # 前舱盖状态关闭 BonnetService Status
        dict={0:4, 1:0, 2:1, 3:2, 4:3, 5:5, 6:5, 7:5}
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg', 10)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', 7)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "10"}]}, timeout=3)  
        last_value=10       
        for signal_fault in range(16):
            for signal_status in range(8):
                self.partner.empty_all()
                self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg', signal_fault)
                self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', signal_status)
                if signal_fault in [1, 2, 3, 10, 11, 12]:
                    value=signal_fault
                elif signal_fault in [13, 15] and dict[signal_status] not in [0, 1]:
                    value=signal_fault
                elif signal_fault in [7, 8, 9] and dict[signal_status] in [2, 3, 5]:
                    value=signal_fault
                elif signal_fault == 6 and dict[signal_status] in [2, 5]:
                    value=signal_fault
                else:
                    value=0
                logger.info(f"打印当前返回值: fault={signal_fault}, signal_status={signal_status}, status={dict[signal_status]}, last_value={last_value}, value={value}")
                if last_value==value:
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, value)  
                else:
                    self.partner.ck_wti_warning_and_resp(hint, value)                 
                last_value=value

    @allure.title("弹射起步失败提示信息_info=9_fault!=9_遍历Status.sts=0/1")
    @pytest.mark.full
    def test_caseid_1988499(self): # LaunchMode,fault|Launch Mode Prompt|wti_service
        hint = 'Launch Mode Prompt'
        self.boon_all_open_close(1) # 前舱盖状态关闭 BonnetService Status
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg', 0)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', 3) # LaunchMode.info.status=2
        sleep(1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)  
        self.partner.empty_all() 
        last_value=0
        dict={0:4, 1:0, 2:1, 3:2, 6:2, 4:3, 5:5, 7:5}
        for key, status in dict.items():
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', key)
            sleep(1)
            for sts in [0, 1]:
                self.boon_all_open_close(sts)                
                value = 9 if status in [2, 3, 5] and sts == 0 else 0
                logger.info(f"打印当前返回值: value={value}, last_value={last_value}, signal_status=={key}, status={status}, sts={sts}")
                if last_value==value:
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, value)  
                else:
                    self.partner.ck_wti_warning_and_resp(hint, value)                   
                last_value=value 

    @allure.title("弹射起步失败提示信息_优先级判断_同时映射info=9和其他值")
    @pytest.mark.sanity
    def test_caseid_1988501(self): # UpdateLaunchModeEvent 
        hint = 'Launch Mode Prompt'
        self.boon_all_open_close(0)  
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  3) # LaunchMode.info.status=2
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg',  9) 
        sleep(1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "9"}]}, timeout=3)  
        self.partner.empty_all() 
        last_value=9
        for fault in range(16):
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg', fault)
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  random.choice([3, 5])) # LaunchMode.info.status=2
            logger.info(f"打印当前fault={fault}")
            value = fault if fault in [1, 2, 3, 6, 7, 8] else 9
            if last_value==value:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, value)    
            else:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, value)
            last_value=value
                
    @allure.title("弹射起步失败提示信息_info=9_fault!=9_Status.sts=65535")
    @pytest.mark.full
    def test_caseid_1985983(self): # # LaunchMode,fault|Launch Mode Prompt|handleLunchIndicator,status
        hint = 'Launch Mode Prompt'
        self.boon_all_open_close(1) 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', 3) # LaunchMode.info.status=2
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg', 10)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "10"}]}, timeout=3)  
        self.ipdu.pause_bus_send("backbonefr") 
        self.partner.empty_all(3) 
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 65535})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, 
                                              {"out": [{"name": hint, "info": "9"}]}, timeout=3)  # 重启后上报的event可能会上报了 但是校验不到
        self.ipdu.resume_all_bus_send()
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 10)         
                    
    @allure.title("弹射起步失败提示信息_服务启动默认值")
    @pytest.mark.full
    def test_caseid_1985982(self):
        hint = 'Launch Mode Prompt'
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg',  1) 
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "1"}]}, timeout=3)
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]})     
        self.ipdu.resume_all_bus_send()
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)      
                                                                                        
    @allure.title("获取&通知制动液位信息_UsgMod依次下切_信号遍历)")
    @pytest.mark.smoke
    def test_caseid_1979846(self): # fr BrkFldLvl|Braking Fluid|wti current mode|lastUM
        hint = "Braking Fluid"
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
        last_value=0
        for UsgMod in [13, 11, 2, 1, 0]:
            for i in [1, 0]: 
                self.sd_tester.change_usage_mode(UsgMod)  
                self.partner.empty_all(2)
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', i)
                sleep(1)
                value = 1 if i==1 and UsgMod in [2, 11, 13] else 0
                logger.info(f"打印当前返回值：usgmod={UsgMod}, value={value}")
                if last_value!= value:
                    self.ck_WarningMsgList_and_GetWarningMsgList(hint, value)
                else:
                    # self.ck_no_specific_event_and_GetWarningMsgList(hint, value) # 重复上报
                    self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": value}]})
                last_value=value
                
    @allure.title("获取&通知制动液位信息_UsgMod切换遍历")
    @pytest.mark.sanity
    def test_caseid_1979847(self):  
        hint = "Braking Fluid"
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0)
        sleep(2) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 1)
        sleep(1)
        for UsgMod1 in [0, 1]: 
            self.sd_tester.change_usage_mode(UsgMod1)  
            for UsgMod2 in [2, 11, 13]: 
                self.partner.empty_all(2)  
                self.sd_tester.change_usage_mode(UsgMod2) 
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]})
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1) # 1s后
                self.sd_tester.change_usage_mode(UsgMod1)  
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)  
        
    @allure.title("获取&通知制动液位信息_信号丢失")
    @pytest.mark.full  # fail todo UsgMod从0切11，误报1
    def test_caseid_1979848(self):  # DispMsgByVehHld,BrkRelsWarnReq,BrkFldLvl,BrkAndAbsWarnIndcnReq timeout|fr BrkFldLvl|NotifyBrkFldLvlWarnMsgStatus|Braking Fluid
        hint = "Braking Fluid"
        sleep(5)
        # self.sd_tester.change_usage_mode(11) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
        self.partner.empty_all()  
        for UsgMod in [13, 11, 2, 1]:
            self.sd_tester.change_usage_mode(UsgMod) 
            self.partner.empty_all(2)  
            self.ipdu.pause_bus_send("backbonefr") 
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "NotifyBrkFldLvlWarnMsgStatus", {"msg": 1}, timeout=2.5)
            if UsgMod in [2, 11, 13]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
            else:
                sleep(2)
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
            self.ipdu.resume_bus_send("backbonefr")  
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "NotifyBrkFldLvlWarnMsgStatus", {"msg": 0})  
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)     
            
    @allure.title("获取&通知换挡器故障信息_UsgMod依次下切_信号遍历")
    @pytest.mark.smoke
    def test_caseid_1979851(self): # GearLvrFaultIndcn|Gear Failure|wti current mode|lastUM 
        hint = "Gear Failure"
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr09, 'GearLvrFaultIndcn', 0)
        sleep(2)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr09, 'GearLvrFaultIndcn', 2)
        sleep(2)
        last_value=2
        for UsgMod in [13, 11, 2, 1, 0]:
            for i in range(8): 
                self.sd_tester.change_usage_mode(UsgMod)
                self.partner.empty_all(2)
                self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr09, 'GearLvrFaultIndcn', i)
                sleep(1)
                value = i if i in range(6) and UsgMod in [2, 11, 13] else 0
                logger.info(f"打印当前循环值:UsgMod={UsgMod},i={i},last_value={last_value},value={value}")
                if last_value!= value:
                    self.ck_WarningMsgList_and_GetWarningMsgList(hint, value)
                else:
                    # self.ck_no_specific_event_and_GetWarningMsgList(hint, value) # 重复上报
                    self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": value}]})
                last_value=value
                
    @allure.title("获取&通知换挡器故障信息_UsgMod切换遍历")
    @pytest.mark.sanity
    def test_caseid_1979852(self):  
        hint = "Gear Failure"
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr09, 'GearLvrFaultIndcn', 0)
        sleep(2)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr09, 'GearLvrFaultIndcn', 2)
        sleep(2)
        for UsgMod1 in [0, 1]: 
            self.sd_tester.change_usage_mode(UsgMod1)  
            for UsgMod2 in [2, 11, 13]: 
                value = random.randint(1, 5)
                self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr09, 'GearLvrFaultIndcn', value)
                self.partner.empty_all(2)  
                self.sd_tester.change_usage_mode(UsgMod2) 
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]})
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, value) # 1s后
                self.sd_tester.change_usage_mode(UsgMod1)  
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)  

    @allure.title("获取&通知换挡器故障信息_信号丢失")
    @pytest.mark.full
    def test_caseid_1979853(self):  
        hint = "Gear Failure"
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr09, 'GearLvrFaultIndcn', 0)
        sleep(2)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr09, 'GearLvrFaultIndcn', 2)
        sleep(2)
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod) 
            i = random.randint(0, 7)
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr09, 'GearLvrFaultIndcn', i)
            value = i if i in range(6) and UsgMod in [2, 11, 13] else 0
            self.partner.empty_all(2) 
            try:
                self.ipdu.pause_bus_send("chassiscan1") 
                if UsgMod in [2, 11, 13]:
                    if value==5:
                        self.ck_no_specific_event_and_GetWarningMsgList(hint, 5)
                    else:
                        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 5)
                else:
                    sleep(2)
                    self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]})
            except Exception as error:
                self.ipdu.resume_bus_send("chassiscan1")
                assert False, error
            else:
                self.ipdu.resume_bus_send("chassiscan1")                    
                                      
    @allure.title("获取&通知Autohold警告信息_UsgMod依次下切_信号遍历")
    @pytest.mark.full
    def test_caseid_1979871(self): # DispMsgByVehHld|Autohold Warning|wti current mode|lastUM 
        hint = "Autohold Warning"
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DispMsgByVehHld', 0) # len=3
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DispMsgByVehHld', 1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "1"}]}, timeout=3)
        last_value=1
        for UsgMod in [13, 11, 2, 1, 0]:
            for i in range(8): 
                self.sd_tester.change_usage_mode(UsgMod)
                self.partner.empty_all(2)
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DispMsgByVehHld', i)
                sleep(2)
                value = i if i in range(6) and UsgMod in [11, 13] else 0
                logger.info(f"打印当前循环值:UsgMod={UsgMod},i={i},last_value={last_value},value={value}")
                if last_value!= value:
                    self.ck_WarningMsgList_and_GetWarningMsgList(hint, value)
                else:
                    # self.ck_no_specific_event_and_GetWarningMsgList(hint, value) # 重复上报
                    self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]})
                last_value=value
                sleep(2)
                
    @allure.title("获取&通知Autohold警告信息_UsgMod从0/1/2切至11/13_debounce确认")
    @pytest.mark.sanity
    def test_caseid_1979872(self):  # DispMsgByVehHld|Autohold Warning|wti current mode|lastUM 
        hint = "Autohold Warning"
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DispMsgByVehHld', 0)
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DispMsgByVehHld', 7)
        sleep(2)
        for UsgMod1 in [0, 1, 2]: 
            self.sd_tester.change_usage_mode(UsgMod1)  
            for UsgMod2 in [11, 13]: 
                value = random.randint(1, 5)
                logger.info(f"打印当前循环值:UsgMod={UsgMod1},UsgMod2={UsgMod2},value={value}")
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DispMsgByVehHld', value)
                self.partner.empty_all(3)  
                self.sd_tester.change_usage_mode(UsgMod2) 
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]})
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, value) # 1s后
                self.sd_tester.change_usage_mode(UsgMod1)  
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)  
                sleep(2)

    @allure.title("获取&通知Autohold警告信息_信号丢失")
    @pytest.mark.full
    def test_caseid_1979873(self): # Autohold Warning|DispMsgByVehHld|wti current mode
        hint = "Autohold Warning"
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DispMsgByVehHld', 0)
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DispMsgByVehHld', 2)
        sleep(2)
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod) 
            i = random.randint(0, 7)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DispMsgByVehHld', i)
            value = i if i in range(6) and UsgMod in [11, 13] else 0
            logger.info(f"打印当前返回值 usgMod={UsgMod}, i={i}, value={value}")
            self.partner.empty_all(2) 
            self.ipdu.pause_bus_send("backbonefr") 
            if UsgMod in [11, 13]:
                if value==2:
                    self.ck_no_specific_event_and_GetWarningMsgList(hint, 2)
                else:
                    self.ck_WarningMsgList_and_GetWarningMsgList(hint, 2)
            else:
                sleep(2)
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]})
            self.ipdu.resume_bus_send("backbonefr")     
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": str(value)}]}, timeout=3)  
        
    @allure.title("获取&通知悬架故障信息_其他车型")
    @pytest.mark.full
    def test_caseid_1981070(self): 
        self.reset_JiduVehicle_and_AirSuspens(value=3, sleeptime=8)
        hint = "Suspension Failed Warning"
        self.sd_tester.change_usage_mode(11)   
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 1)        
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 0)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 3)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
        
    @allure.title("获取&通知悬架故障信息_Mars1_UsgMod依次下切_SuspensionFailureSts.value=1&validity=2")
    @pytest.mark.sanity
    def test_caseid_1987191(self): # lastUM|SuspensionFailureSts|Suspension Failed Warning|vehicleType
        self.reset_JiduVehicle_and_AirSuspens(value=1, sleeptime=5) 
        hint = "Suspension Failed Warning"
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 2) # SuspensionFailureSts.validity=2
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 3) # SuspensionFailureSts.value=1
        self.partner.empty_all(2) 
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            value = 1 if UsgMod in [11, 13] else 0
            if UsgMod in [13, 2]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, value)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, value)
                
    @allure.title("获取&通知悬架故障信息_Mars1_UsgMod=11/13_SuspensionFailureSts.value=0/1&validity=0")
    @pytest.mark.full
    def test_caseid_1987192(self):             
        self.reset_JiduVehicle_and_AirSuspens(value=1, sleeptime=5) 
        hint = "Suspension Failed Warning"
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 3) # SuspensionFailureSts.validity=0
        for UsgMod in [13, 11]:
            self.partner.empty_all(2) 
            self.sd_tester.change_usage_mode(UsgMod)
            for sts in [3, 1]:
                self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', sts) # SuspensionFailureSts.value=0/1
                value=1 if sts==3 else 0   
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, value)

    @allure.title("获取&通知悬架故障信息_Mars1_UsgMod依次下切_SuspensionFailureSts.value=0&validity=6")
    @pytest.mark.sanity
    def test_caseid_1980775(self):           
        self.reset_JiduVehicle_and_AirSuspens(value=1, sleeptime=5) 
        hint = "Suspension Failed Warning"
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 1) # SuspensionFailureSts.validity=6
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 2) # SuspensionFailureSts.value=0
        for UsgMod in [13, 11, 2, 1, 0]:
            self.partner.empty_all(2) 
            self.sd_tester.change_usage_mode(UsgMod)
            value = 1 if UsgMod in [11, 13] else 0
            if UsgMod in [13, 2]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, value)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, value)
        
    @allure.title("获取&通知悬架故障信息_Mars1_UsgMod=11/13_SuspensionFailureSts.value=0&validity=0/2/6/8")
    @pytest.mark.smoke
    def test_caseid_1980776(self):           
        self.reset_JiduVehicle_and_AirSuspens(value=1, sleeptime=5) 
        hint = "Suspension Failed Warning"
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 1) # SuspensionFailureSts.value=1
        for UsgMod in [13, 11]:
            self.partner.empty_all(2) 
            self.sd_tester.change_usage_mode(UsgMod)
            for qf in range(4):
                self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', qf) # SuspensionFailureSts.validity=0/2/6/8
                value=1 if qf in [0, 1] else 0   
                if qf in [0, 2]:
                    self.ck_WarningMsgList_and_GetWarningMsgList(hint, value)   
                else:
                    self.ck_no_specific_event_and_GetWarningMsgList(hint, value)

    @allure.title("获取&通知悬架故障信息_Mars1_UsgMod=11/13_SuspensionFailureSts.value=1&validity=0/2/6/8")
    @pytest.mark.full
    def test_caseid_1987193(self):           
        self.reset_JiduVehicle_and_AirSuspens(value=1, sleeptime=5) 
        hint = "Suspension Failed Warning"
        self.sd_tester.change_usage_mode(random.choice([11, 13]))
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 0)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 3) # SuspensionFailureSts.value=1
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '1'}]}, timeout=2)
        self.partner.empty_all() 
        for qf in range(4):
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', qf) # SuspensionFailureSts.validity=0/2/6/8
            self.ck_no_specific_event_and_GetWarningMsgList(hint, 1)

    @allure.title("获取&通知悬架故障信息_Mars1_UsgMod=11/13_SuspensionFailureSts.value=1&validity=4")
    @pytest.mark.full
    def test_caseid_1987194(self): 
        self.reset_JiduVehicle_and_AirSuspens(value=1, sleeptime=15) # 信号丢失场景
        hint = "Suspension Failed Warning"
        self.sd_tester.change_usage_mode(random.choice([11, 13]))
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 2) # SuspensionFailureSts.validity=2
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 4) # SuspensionFailureSts.value=1
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '1'}]}, timeout=2)
        self.partner.empty_all() 
        self.ipdu.pause_bus_send("chassiscan2")
        sleep(2.5)   
        self.ipdu.resume_bus_send("chassiscan2")
        self.ck_no_specific_event_and_GetWarningMsgList(hint, 1)  
        
    @allure.title("获取&通知悬架故障信息_Mars1_UsgMod=11/13_SuspensionFailureSts.value=0&validity=4")
    @pytest.mark.full
    def test_caseid_1980777(self): 
        self.reset_JiduVehicle_and_AirSuspens(value=1, sleeptime=15) # 信号丢失场景
        hint = "Suspension Failed Warning"
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 2) # SuspensionFailureSts.validity=2
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 2) # SuspensionFailureSts.value=0
        for UsgMod in [13, 11]:
            self.partner.empty_all(2) 
            self.sd_tester.change_usage_mode(UsgMod)
            self.ipdu.pause_bus_send("chassiscan2")
            self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)   
            self.ipdu.resume_bus_send("chassiscan2")
            self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)   
            
    @allure.title("获取&通知悬架故障信息_Mars1_UsgMod切换遍历_debounce确认")
    @pytest.mark.full
    def test_caseid_1980814(self):   
        self.reset_JiduVehicle_and_AirSuspens(value=1, sleeptime=5) 
        hint = "Suspension Failed Warning" 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 1) # SuspensionFailureSts.validity=6
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 3) # SuspensionFailureSts.value=1   
        for usgMod1 in [0, 1, 2]:             
            self.sd_tester.change_usage_mode(usgMod1) 
            for usgMod2 in [11, 13]:     
                self.partner.empty_all(2)           
                self.sd_tester.change_usage_mode(usgMod2) 
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]})
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)   
                self.sd_tester.change_usage_mode(usgMod1) 
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @allure.title("获取&通知悬架故障信息_Mars1_服务启动默认值")
    @pytest.mark.full
    def test_caseid_1980932(self):    
        self.reset_JiduVehicle_and_AirSuspens(value=1, sleeptime=5) 
        hint = "Suspension Failed Warning"    
        self.sd_tester.change_usage_mode(13) 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 1) 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 1) # SuspensionFailureSts.validity=6
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 3) # SuspensionFailureSts.value=1   
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "1"}]}, timeout=3)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT, resume_all_bus=False)
        # self.sd_tester.change_usage_mode(13) 
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
                
    @allure.title("获取&通知悬架故障信息_Venus_UsgMod依次下切_SuspensionFailureSts.value=2&validity=0")
    @pytest.mark.sanity
    def test_caseid_1980780(self): # kCCPJiduVehicleType|kCCPAirSuspens   lastUM|SuspensionFailureSts|Suspension Failed Warning
        self.reset_JiduVehicle_and_AirSuspens(value=2, sleeptime=5) 
        hint = "Suspension Failed Warning"
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 1)  # SuspensionFailureSts.value=2  validity=0
        for UsgMod in [13, 11, 2, 1, 0]:
            self.partner.empty_all(2) 
            self.sd_tester.change_usage_mode(UsgMod)
            value = 2 if UsgMod in [11, 13] else 0
            if UsgMod in [13, 2]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, value)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, value)
                
    @allure.title("获取&通知悬架故障信息_Venus_UsgMod依次下切_SuspensionFailureSts.value=3&validity=0")
    @pytest.mark.full
    def test_caseid_1980782(self): 
        self.reset_JiduVehicle_and_AirSuspens(value=2, sleeptime=5) 
        hint = "Suspension Failed Warning"
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 2)  # SuspensionFailureSts.value=3  validity=0
        for UsgMod in [13, 11, 2, 1, 0]:
            self.partner.empty_all(2) 
            self.sd_tester.change_usage_mode(UsgMod)
            value = 3 if UsgMod in [11, 13] else 0
            if UsgMod in [13, 2]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, value)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, value)
         
    @allure.title("获取&通知悬架故障信息_Venus_UsgMod=11/13_SuspensionFailureSts.value取值遍历&validity=0")
    @pytest.mark.sanity
    def test_caseid_1980783(self):             
        self.reset_JiduVehicle_and_AirSuspens(value=2, sleeptime=5) 
        hint = "Suspension Failed Warning"
        for UsgMod in [13, 11]:
            self.partner.empty_all(2) 
            self.sd_tester.change_usage_mode(UsgMod)
            dict1={2:3, 0:0, 3:3, 1:2}
            for key,value in dict1.items():
                logger.info(f"打印当前循环值 key={key}, value={value}, usgMod={UsgMod}")
                self.partner.empty_all()
                self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', key)
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, value)

    @allure.title("获取&通知悬架故障信息_Venus_UsgMod依次下切_SuspensionFailureSts.value=0&validity取值遍历")
    @pytest.mark.smoke
    def test_caseid_1980812(self):  # kCCPJiduVehicleType|kCCPAirSuspens   lastUM|SuspensionFailureSts|Suspension Failed Warning    
        self.reset_JiduVehicle_and_AirSuspens(value=2, sleeptime=15) 
        hint = "Suspension Failed Warning"
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 0)
        for UsgMod in [13, 11, 2, 1]: # abandon下不检测信号丢失
            self.partner.empty_all(3) 
            self.sd_tester.change_usage_mode(UsgMod)
            logger.info(f"打印当前返回值：UsgMod={UsgMod}")
            self.ipdu.pause_bus_send("chassiscan2")  
            if UsgMod in [11, 13]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 3)
            else: 
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)
            self.ipdu.resume_bus_send("chassiscan2")
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
        
    @allure.title("获取&通知悬架故障信息_Venus_UsgMod切换遍历_debounce确认")
    @pytest.mark.full
    def test_caseid_1980813(self):      
        self.reset_JiduVehicle_and_AirSuspens(value=2, sleeptime=15) 
        hint = "Suspension Failed Warning"
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 3)
        for usgMod1 in [0, 1, 2]:             
            self.sd_tester.change_usage_mode(usgMod1) 
            for usgMod2 in [11, 13]:     
                self.partner.empty_all(2)           
                self.sd_tester.change_usage_mode(usgMod2) 
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]})
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 3)   
                self.sd_tester.change_usage_mode(usgMod1) 
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)  
                
    @allure.title("获取&通知悬架故障信息_Venus_服务启动默认值")
    @pytest.mark.full
    def test_caseid_1980939(self): 
        self.reset_JiduVehicle_and_AirSuspens(value=2, sleeptime=8) 
        hint = "Suspension Failed Warning"
        self.sd_tester.change_usage_mode(13) 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 1)        
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 3)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 3)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "2"}]}, timeout=3)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
                
    @allure.title("获取&通知悬架故障信息_NotifyCarConfigInfo.info.config[59] != 2")
    @pytest.mark.full
    def test_caseid_1981072(self):  
        hint = "Suspension Failed Warning"
        self.sd_tester.write_single_ccp(59, 1) # 低配 kCCPActiveSuspension=1
        sleep(2)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 1)        
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 3)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 3)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": "0"}]}, timeout=3)
                
    @allure.title("获取&通知悬架故障指示灯_Mars1_UsgMod依次下切_SuspensionFailureSts.value=1&validity=2")
    @pytest.mark.sanity
    def test_caseid_1980836(self):  
        self.reset_JiduVehicle_and_AirSuspens(value=1, sleeptime=5) 
        hint = "Suspension Failed Telltale"        
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 2) # SuspensionFailureSts.validity=2
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 3) # SuspensionFailureSts.value=1   
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSuspensionFailureSts", {}, {"out": {"value": 1, "validity": 2}}, timeout=3)
        for UsgMod in [13, 11, 2, 1, 0]: 
            self.partner.empty_all(2) 
            self.sd_tester.change_usage_mode(UsgMod)         
            value = 1 if UsgMod in [11, 13] else 0
            if UsgMod in [13, 2]:
                self.ck_TelltaleList_and_GetTelltaleList(hint, value)
            else: 
                self.ck_no_specific_event_and_GetTelltaleList(hint, value)
        
    @allure.title("获取&通知悬架故障指示灯_Mars1_UsgMod依次下切_SuspensionFailureSts.value=0&validity=6")
    @pytest.mark.full
    def test_caseid_1980837(self):  
        self.reset_JiduVehicle_and_AirSuspens(value=1, sleeptime=5) 
        hint = "Suspension Failed Telltale"   
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 1) # SuspensionFailureSts.validity=6
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 2) # SuspensionFailureSts.value=0   
        for UsgMod in [13, 11, 2, 1, 0]: 
            self.partner.empty_all(2) 
            self.sd_tester.change_usage_mode(UsgMod)         
            value = 1 if UsgMod in [11, 13] else 0
            if UsgMod in [13, 2]:
                self.ck_TelltaleList_and_GetTelltaleList(hint, value)
            else: 
                self.ck_no_specific_event_and_GetTelltaleList(hint, value)
        
    @allure.title("获取&通知悬架故障指示灯_Mars1_UsgMod=11/13_SuspensionFailureSts.value=0&validity=0/2/6/8")
    @pytest.mark.sanity
    def test_caseid_1980838(self):  
        self.reset_JiduVehicle_and_AirSuspens(value=1, sleeptime=5) 
        hint = "Suspension Failed Telltale"         
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 1) # SuspensionFailureSts.value=0       
        for UsgMod in [13, 11]:
            self.partner.empty_all(2) 
            self.sd_tester.change_usage_mode(UsgMod)
            for qf in range(4):
                self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', qf)
                value=1 if qf in [0, 1] else 0
                if qf in [0, 2]:
                    self.ck_TelltaleList_and_GetTelltaleList(hint, value)
                else: 
                    self.ck_no_specific_event_and_GetTelltaleList(hint, value)
            
    @allure.title("获取&通知悬架故障指示灯_Mars1_UsgMod=11/13_SuspensionFailureSts.value=0/1&validity=0")
    @pytest.mark.full
    def test_caseid_1980839(self):  
        self.reset_JiduVehicle_and_AirSuspens(value=1, sleeptime=5) 
        hint = "Suspension Failed Telltale"        
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 3)  
        for UsgMod in [13, 11]:
            self.partner.empty_all(2) 
            self.sd_tester.change_usage_mode(UsgMod)
            for sts in [3, 2, 4, 0]:
                self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', sts)
                value=1 if sts in [3, 4] else 0
                self.ck_TelltaleList_and_GetTelltaleList(hint, value)
                    
    @allure.title("获取&通知悬架故障指示灯_Mars1_UsgMod切换遍历_debounce确认")
    @pytest.mark.sanity
    def test_caseid_1980842(self):  
        self.reset_JiduVehicle_and_AirSuspens(value=1, sleeptime=5) 
        hint = "Suspension Failed Telltale"    
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 1)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 3)
        sleep(2)
        for usgMod1 in [0, 1, 2]:             
            self.sd_tester.change_usage_mode(usgMod1) 
            for usgMod2 in [11, 13]:     
                self.partner.empty_all(2)           
                self.sd_tester.change_usage_mode(usgMod2)         
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": '0'}]})
                self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
                self.sd_tester.change_usage_mode(usgMod1) 
                self.ck_TelltaleList_and_GetTelltaleList(hint, 0)  
                                        
    @allure.title("获取&通知悬架故障指示灯_Venus_UsgMod=11/13_SuspensionFailureSts.value!=3&validity=0/4")
    @pytest.mark.sanity
    def test_caseid_1980829(self):  
        self.reset_JiduVehicle_and_AirSuspens(value=2, sleeptime=15) 
        hint = "Suspension Failed Telltale"    
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 1)    
        for usgMod in [11, 13]:     
            self.partner.empty_all(2)           
            self.sd_tester.change_usage_mode(usgMod) 
            self.ipdu.pause_bus_send("chassiscan2")
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)   
            self.ipdu.resume_bus_send("chassiscan2")
            self.ck_TelltaleList_and_GetTelltaleList(hint, 0)    
                        
    @allure.title("获取&通知悬架故障指示灯_Venus_UsgMod依次下切_SuspensionFailureSts.value!=3&validity=4")
    @pytest.mark.full
    def test_caseid_1980831(self):  
        self.reset_JiduVehicle_and_AirSuspens(value=2, sleeptime=15) 
        hint = "Suspension Failed Telltale"     
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 0)    
        for UsgMod in [13, 11, 2, 1]:
            self.partner.empty_all(2) 
            self.sd_tester.change_usage_mode(UsgMod)    
            self.ipdu.pause_bus_send("chassiscan2")   
            if UsgMod in [11, 13]:
                self.ck_TelltaleList_and_GetTelltaleList(hint, 1)   
            else:
                self.ck_no_specific_event_and_GetTelltaleList(hint, 0)
            self.ipdu.resume_bus_send("chassiscan2")  
            if UsgMod in [11, 13]:
                self.ck_TelltaleList_and_GetTelltaleList(hint, 0)   
            else:
                self.ck_no_specific_event_and_GetTelltaleList(hint, 0)         

    @allure.title("获取&通知悬架故障指示灯_Venus_UsgMod=11/13_SuspensionFailureSts.value=0/2/3&validity=0")
    @pytest.mark.sanity
    def test_caseid_1980833(self):  
        self.reset_JiduVehicle_and_AirSuspens(value=2, sleeptime=5) 
        hint = "Suspension Failed Telltale"     
        for UsgMod in [13, 11]:
            self.partner.empty_all(2) 
            self.sd_tester.change_usage_mode(UsgMod)
            dict1={2:1, 0:0, 3:1, 1:0}
            for key,value in dict1.items():
                self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', key)
                self.ck_TelltaleList_and_GetTelltaleList(hint, value)   
                
    @allure.title("获取&通知悬架故障指示灯_Venus_UsgMod依次下切_SuspensionFailureSts.value=3&validity=0")
    @pytest.mark.full
    def test_caseid_1980835(self):  
        self.reset_JiduVehicle_and_AirSuspens(value=2, sleeptime=5) 
        hint = "Suspension Failed Telltale" 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 3)   
        for UsgMod in [13, 11, 2, 1, 0]:
            self.partner.empty_all(2)           
            self.sd_tester.change_usage_mode(UsgMod) 
            value=1 if UsgMod in [11, 13] else 0
            if UsgMod in [13, 2]:
                self.ck_TelltaleList_and_GetTelltaleList(hint, value)  
            else:
                self.ck_no_specific_event_and_GetTelltaleList(hint, value)  
                
    @allure.title("获取&通知悬架故障指示灯_Venus_UsgMod切换遍历_debounce确认")
    @pytest.mark.full
    def test_caseid_1980840(self):  
        self.reset_JiduVehicle_and_AirSuspens(value=2, sleeptime=5) 
        hint = "Suspension Failed Telltale"  
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 2)   
        sleep(2)
        for usgMod1 in [0, 1, 2]:             
            self.sd_tester.change_usage_mode(usgMod1) 
            for usgMod2 in [11, 13]:     
                self.partner.empty_all(2)           
                self.sd_tester.change_usage_mode(usgMod2)         
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": '0'}]})
                self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
                self.sd_tester.change_usage_mode(usgMod1) 
                self.ck_TelltaleList_and_GetTelltaleList(hint, 0)      
                
    @allure.title("获取&通知悬架故障指示灯_Venus_服务启动默认值")
    @pytest.mark.full
    def test_caseid_1980938(self):  
        self.reset_JiduVehicle_and_AirSuspens(value=2, sleeptime=5) 
        hint = "Suspension Failed Telltale"      
        self.sd_tester.change_usage_mode(13)                
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 2)        
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 3)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 3)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "1"}]}, timeout=3)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]}, timeout=3)
        
    @allure.title("获取&通知悬架故障指示灯_其他车型")
    @pytest.mark.full
    def test_caseid_1981069(self):    
        self.reset_JiduVehicle_and_AirSuspens(value=3, sleeptime=5) 
        hint = "Suspension Failed Telltale"      
        self.sd_tester.change_usage_mode(11)   
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 2)        
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 1)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 3)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]}, timeout=3)
     
    @allure.title("获取&通知悬架故障指示灯_Mars_服务启动默认值")
    @pytest.mark.full
    def test_caseid_1980931(self):    
        self.reset_JiduVehicle_and_AirSuspens(value=1, sleeptime=5) 
        hint = "Suspension Failed Telltale"      
        self.sd_tester.change_usage_mode(11) 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 3) 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 1) # SuspensionFailureSts.validity=6
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 3) # SuspensionFailureSts.value=1   
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "1"}]}, timeout=3)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]}, timeout=3)
        
    @allure.title("获取&通知悬架故障指示灯_NotifyCarConfigInfo.info.config[59] != 2")
    @pytest.mark.full
    def test_caseid_1981071(self): 
        hint = "Suspension Failed Telltale"          
        self.sd_tester.write_single_ccp(59, 1) # 低配 kCCPAirSuspens=1
        sleep(2)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 3)        
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 2)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 3)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]}, timeout=3)                                                                              
    
    @allure.title("EPB指示灯_epbIndicatorLightReqStsValidity.value=0/1/2&validity=0")
    @pytest.mark.sanity 
    def test_caseid_1983619(self): # fr EpbLampReq|EPB Working,state|lastUM|epbIndicatorLightReqStsValidity
        self.sd_tester.change_usage_mode(1)
        hint = "EPB Working"          
        for epb_lamp in [1, 0]:
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',epb_lamp)    
            for sec_epb_lamp in [1, 0]:  
                self.partner.empty_all(1) 
                self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',sec_epb_lamp)  
                sleep(2)
                if epb_lamp==0 and sec_epb_lamp==0:                        
                    self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
                elif epb_lamp==1 and sec_epb_lamp==1: 
                    self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
                else: 
                    self.ck_TelltaleList_and_GetTelltaleList(hint, 2)  
                
    @allure.title("EPB指示灯_UsgMod遍历_epbIndicatorLightReqStsValidity.value=1&validity=0")
    @pytest.mark.smoke
    def test_caseid_1983620(self):
        hint = "EPB Working"
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq', 0)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq', 0)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": '1'}]}, timeout=3)
        for usgmod in [1, 2, 0, 11, 13]:
            self.partner.empty_all() 
            self.sd_tester.change_usage_mode(usgmod)
            sleep(2)
            value=0 if usgmod==0 else 1     
            logger.info(f"打印当前返回值：usgmod={usgmod}，value={value}")       
            if usgmod in [0, 11]:
                self.ck_TelltaleList_and_GetTelltaleList(hint, value)
            else:   
                self.ck_no_specific_event_and_GetTelltaleList(hint, value)   

    @allure.title("EPB指示灯_UsgMod遍历_epbIndicatorLightReqStsValidity.value=0&validity=4")
    @pytest.mark.full
    def test_caseid_1983624(self): 
        self.sd_tester.change_usage_mode(0)# 前置用例UsgMod切到了13，如果直接切1的话会有10s计时器，导致用例失败
        hint = "EPB Working"
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',1)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',1) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":0,"validity":0}}, timeout=3)  
        self.partner.empty_all(2)     
        for usgmod in [1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usgmod)  
            self.partner.empty_all(2)    
            self.ipdu.pause_bus_send("backbonefr")   
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":0,"validity":4}}) 
            if usgmod==1:
                self.ck_no_specific_event_and_GetTelltaleList(hint, 0) 
            else:  
                self.ck_TelltaleList_and_GetTelltaleList(hint, 2) 
            self.ipdu.resume_bus_send("backbonefr") 
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": '0'}]}, timeout=3)
            
    @allure.title("EPB指示灯_UsgMod遍历_epbIndicatorLightReqStsValidity.value=1&validity=7")
    @pytest.mark.full
    def test_caseid_1983625(self): # fr EpbLampReq|EPB Working,state|lastUM|EPBIndicatorLightReqStsValidity,value|wti current mode
        hint = "EPB Working"
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',0)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',0) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":1,"validity":0}}, timeout=3)  
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": '1'}]}, timeout=3)
        for usgmod in [0, 1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usgmod)  
            self.partner.empty_all(2)    
            try:
                self.ipdu.set_no_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq')
                sleep(2)
                self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":1,"validity":7}})         
                if usgmod==0:
                    self.ck_no_specific_event_and_GetTelltaleList(hint, 0) 
                elif usgmod==1:
                    self.ck_no_specific_event_and_GetTelltaleList(hint, 1) 
                else:  
                    self.ck_TelltaleList_and_GetTelltaleList(hint, 2) 
            except Exception as error:
                self.ipdu.restore_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq')
                assert False, error
            else:
                self.ipdu.restore_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq')
                
    @allure.title("EPB指示灯_UsgMod从0上切至2/11/13_debounce确认")
    @pytest.mark.full
    def test_caseid_1983626(self): # fr EpbLampReq|EPB Working,state|lastUM|EPBIndicatorLightReqStsValidity,value|wti current mode
        hint = "EPB Working"
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',1)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',0) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":2,"validity":0}}, timeout=3)  
        for usgMod2 in [2, 11, 13]:    
            self.sd_tester.change_usage_mode(0)  
            self.partner.empty_all(2)           
            self.sd_tester.change_usage_mode(usgMod2) 
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": '0'}]})
            self.ck_TelltaleList_and_GetTelltaleList(hint, 2)
            
    @allure.title("EPB指示灯_UsgMod从2/11/13下切至1_10s确认")
    @pytest.mark.sanity
    def test_caseid_1983627(self): # fr EpbLampReq|EPB Working,state|lastUM|EPBIndicatorLightReqStsValidity,value|wti current mode
        hint = "EPB Working"                
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',0)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',0) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":1,"validity":0}}, timeout=3)  
        for usgMod2 in [2, 11, 13]:    
            self.sd_tester.change_usage_mode(usgMod2) 
            sleep(2)     
            self.sd_tester.change_usage_mode(1)
            self.partner.empty_all(2)       
            self.ipdu.pause_bus_send("backbonefr")   
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":1,"validity":4}}) 
            self.ck_TelltaleList_and_GetTelltaleList(hint, 2) 
            sleep(4)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
            self.ipdu.resume_bus_send("backbonefr") 
            self.ck_no_specific_event_and_GetTelltaleList(hint, 1) 

    @allure.title("EPB指示灯_UsgMod从2/11/13下切至1后再切至非1值_需停掉10s计时器")
    @pytest.mark.full
    def test_caseid_1984284(self): # fr EpbLampReq|EPB Working,state|lastUM|EPBIndicatorLightReqStsValidity,value|wti current mode
        hint = "EPB Working"  
        self.sd_tester.change_usage_mode(2) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',0)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',0) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":1,"validity":0}}, timeout=3)  
        self.sd_tester.change_usage_mode(1) 
        self.partner.empty_all(2)  
        self.sd_tester.change_usage_mode(0)    
        self.ck_TelltaleList_and_GetTelltaleList(hint, 0)  
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq')
            sleep(2)
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":1,"validity":7}})         
            self.ck_no_specific_event_and_GetTelltaleList(hint, 0) 
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq')
        self.ck_no_specific_event_and_GetTelltaleList(hint, 0) 
        
    @allure.title("转向故障信息_SteerErrReq=1_UsgMod遍历")
    @pytest.mark.full
    def test_caseid_1984779(self):
        hint = "Steering Warning"   
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 1)
        self.partner.empty_all(1) 
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            value=1 if UsgMod in [11, 13] else 0
            if UsgMod in [13, 2]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, value, timeout=3.5)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, value)  
                
    @allure.title("转向故障信息_SteerErrReq=2_UsgMod遍历")
    @pytest.mark.sanity
    def test_caseid_1984780(self):
        hint = "Steering Warning"          
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 2)
        self.partner.empty_all(1) 
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            value=2 if UsgMod in [11, 13] else 0
            if UsgMod in [13, 2]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, value, timeout=3.5)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, value)  
        
    @allure.title("转向故障信息_SteerErrReq=3_UsgMod遍历")
    @pytest.mark.full
    def test_caseid_1984781(self):
        hint = "Steering Warning"   
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 3)
        self.partner.empty_all(1) 
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            value=3 if UsgMod in [11, 13] else 0
            if UsgMod in [13, 2]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, value, timeout=3.5)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, value)  
                
    @allure.title("转向故障信息_SteerErrReq=4_UsgMod遍历")
    @pytest.mark.full
    def test_caseid_1984782(self):
        hint = "Steering Warning"          
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 4)
        self.partner.empty_all(1) 
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)
            value=4 if UsgMod in [11, 13] else 0
            if UsgMod in [13, 2]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, value, timeout=3.5)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, value)         

    @allure.title("转向故障信息_UsgMod=11/13_SteerErrReq遍历")
    @pytest.mark.sanity
    def test_caseid_1984785(self):
        hint = "Steering Warning"      
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0) 
        self.sd_tester.change_usage_mode(11)   
        self.partner.empty_all(3.2) 
        for i in range(8):
            self.sd_tester.change_usage_mode(random.choice([11, 13]))
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', i)
            value=i if i<5 else 0
            if i in range(1, 6):
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, value)
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, value) 
         
    @allure.title("转向故障信息_UsgMod=0/1/2_SteerErrReq遍历")
    @pytest.mark.smoke
    def test_caseid_1984786(self):
        hint = "Steering Warning"      
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0) 
        self.partner.empty_all(1) 
        for i in range(8):
            self.sd_tester.change_usage_mode(random.choice([0, 1, 2]))   
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', i)
            self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)       
            
    @allure.title("转向故障信息_UsgMod从0/1/2切换至11/13_debounce确认")
    @pytest.mark.full
    def test_caseid_1984790(self):
        hint = "Steering Warning"  
        for usgMod1 in [0, 1, 2]:             
            for usgMod2 in [11, 13]:  
                signal = random.choice(range(1, 5))  
                self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', signal)                     
                self.sd_tester.change_usage_mode(usgMod1) 
                self.partner.empty_all(1)    
                self.sd_tester.change_usage_mode(usgMod2) 
                self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint, timeout=2.5)
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, signal) # 3s后上报
                
    @allure.title("转向故障信息_UsgMod从0/1/2切换至11/13_debounce内改变信号值")
    @pytest.mark.full
    def test_caseid_1984791(self):
        hint = "Steering Warning"  
        for usgMod1 in [0, 1, 2]:             
            for usgMod2 in [11, 13]: 
                self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 1)                     
                self.sd_tester.change_usage_mode(usgMod1) 
                self.partner.empty_all(1)    
                self.sd_tester.change_usage_mode(usgMod2)
                signal = random.choice(range(1, 5))  
                self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', signal)       
                self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint, timeout=2.5)
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, signal) # 3s后上报

    @allure.title("转向故障信息_UsgMod=11/13_信号丢失")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1984795(self): #  can SteerErrReq|wti current mode|Steering Warning|SteerErrReq_TimeOut
        hint = "Steering Warning"   
        self.sd_tester.change_usage_mode(11)     
        self.partner.empty_all(3.2)             
        for i in range(8):
            self.sd_tester.change_usage_mode(random.choice([11, 13]))   
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', i)            
            value=i if i<5 else 0  
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(value)}]}, timeout=3)
            self.partner.empty_all(0.2)  
            self.ipdu.pause_bus_send("chassiscan1")
            self.ck_no_specific_event_and_GetWarningMsgList(hint, value, timeout=4)
            if value != 4:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 4) # 5s后上报
            else:
                self.ck_no_specific_event_and_GetWarningMsgList(hint, 4)  
            self.ipdu.resume_bus_send("chassiscan1")     
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(value)}]}, timeout=3)           
 
    @allure.title("转向故障信息_UsgMod=0/1/2_信号丢失")
    @pytest.mark.full
    def test_caseid_1984796(self): 
        hint = "Steering Warning"              
        for i in range(8):
            self.sd_tester.change_usage_mode(random.choice([0, 1, 2]))   
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', i)           
            self.ipdu.pause_bus_send("chassiscan1")
            sleep(5.2)  
            self.ipdu.resume_bus_send("chassiscan1")  
            self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)           
            
    @allure.title("EBD警告信息_BrkMsgWarnReq遍历_UsgMod=0/1")
    @pytest.mark.smoke
    def test_caseid_1984816(self): 
        hint = "EBD Warning"      
        self.partner.empty_all()                
        for i in range(8):
            self.sd_tester.change_usage_mode(random.choice([0, 1]))   
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', i)
            # self.ck_no_specific_event_and_GetWarningMsgList(hint, 0)  # UsgMod不变，信号变化时，会重复上报
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '0'}]})

    @allure.title("EBD警告信息_BrkMsgWarnReq遍历_UsgMod=2/11/13")
    @pytest.mark.sanity
    def test_caseid_1984819(self): # BrkMsgWarnReq|EBD Warning|wti current mode
        hint = "EBD Warning"     
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 5) 
        sleep(2)               
        for i in range(8):
            self.partner.empty_all()       
            self.sd_tester.change_usage_mode(random.choice([2, 11, 13]))    
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', i)         
            self.ck_WarningMsgList_and_GetWarningMsgList(hint, i) 
                    
    @allure.title("无动力输出_normal转为warning后维持")
    @pytest.mark.smoke
    def test_caseid_1984820(self): # wti| No Power Output|VehSpdLgt|GearLvrIndcn|TrsmParkLockdTrsmParkLockd
        hint = "No Power Output"  
        self.sd_tester.change_usage_mode(11)  
        self.setNoPowerOutput([0, 2, 1.0, 0], sleeptime=2)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '0'}]})
        self.setNoPowerOutput([0, 2, 1.0, 3], sleeptime=2)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1) 
        self.partner.empty_all() 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0.1)
        self.ck_no_specific_event_and_GetWarningMsgList(hint, 1) 
        
    @allure.title("无动力输出_warning_gear从2切0")
    @pytest.mark.sanity
    def test_caseid_1984821(self): 
        hint = "No Power Output"  
        self.sd_tester.change_usage_mode(11)  
        self.setNoPowerOutput([0, 2, 1.0, 3], sleeptime=2)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1) 
        self.partner.empty_all() 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0) 
        
    @allure.title("无动力输出_warning_gear从2切1")
    @pytest.mark.full
    def test_caseid_1984822(self): 
        hint = "No Power Output"  
        self.sd_tester.change_usage_mode(11)  
        self.setNoPowerOutput([0, 2, 3.0, 3], sleeptime=2)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1) 
        self.partner.empty_all() 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 1)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0) 
        
    @allure.title("无动力输出_warning_gear从2切3")
    @pytest.mark.full
    def test_caseid_1984823(self): 
        hint = "No Power Output"  
        self.sd_tester.change_usage_mode(11)  
        self.setNoPowerOutput([1, 2, 1.0, 3], sleeptime=2)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1) 
        self.partner.empty_all() 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 3)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0) 
        
    @allure.title("无动力输出_warning_gear从2切5")
    @pytest.mark.full
    def test_caseid_1984824(self): 
        hint = "No Power Output"  
        self.sd_tester.change_usage_mode(11)  
        self.setNoPowerOutput([1, 2, 3.0, 3], sleeptime=2)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1) 
        self.partner.empty_all() 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 6)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0) 
        
    @allure.title("无动力输出_warning_UsgMod从11切13")
    @pytest.mark.smoke
    def test_caseid_1984826(self): # UsgMod从11切0/1/2需要车速=0 
        hint = "No Power Output"  
        self.sd_tester.change_usage_mode(11)  
        self.setNoPowerOutput([1, 2, 3.0, 3], sleeptime=2)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1) 
        self.partner.empty_all() 
        self.sd_tester.change_usage_mode(13)  
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0) 
        
    @allure.title("无动力输出_warning_DisplaySpeedChanged.speed切0")
    @pytest.mark.full
    def test_caseid_1984827(self): 
        hint = "No Power Output"  
        self.sd_tester.change_usage_mode(11)  
        self.setNoPowerOutput([1, 2, 3.0, 3], sleeptime=2)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1) 
        self.partner.empty_all() 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0) 

    @allure.title("无动力输出_warning_DisplaySpeedChanged.isvaild切0")
    @pytest.mark.full
    def test_caseid_1984828(self): 
        hint = "No Power Output"  
        self.sd_tester.change_usage_mode(11)  
        self.setNoPowerOutput([1, 2, 3.0, 3], sleeptime=2)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1) 
        self.partner.empty_all() 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 0)
        self.ck_no_specific_event_and_GetWarningMsgList(hint, 1) 

    def set_Shift_Reminder(self, gear=4, pos=0):
        '''换挡提示 默认档位=NA, 加速踏板pos=0'''
        self.sd_tester.change_usage_mode(random.choice([11, 13])) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0) # NA 档位
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', pos) # pos=0
        self.partner.empty_all(0.5) 
        
    @allure.title("换挡提示_进入条件判断_加速踏板位置满足_档位遍历")
    @pytest.mark.sanity
    def test_caseid_1988866(self): # gear change from|AccPedalPosition,oldPosition|Shift Reminder|preHandleAcc,acc
        hint = "Shift Reminder"  
        self.set_Shift_Reminder()
        for gear in range(5): # P R N D NA
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 0) 
            sleep(0.5)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear)            
            sleep(0.5)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 100.0) 
            if gear in [0, 2] :
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)        
                self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.5)
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)

    @allure.title("换挡提示_进入条件判断_档位满足_加速踏板位置遍历")
    @pytest.mark.sanity
    def test_caseid_1988867(self): 
        hint = "Shift Reminder"  
        self.set_Shift_Reminder()     
        for pos in [0, 4.91, 5.0, 5.1, 100.0]:
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 0.0) 
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', random.choice([0, 2]))      
            sleep(0.5)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', pos) 
            if pos > 5.0:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)        
                self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.5)
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)

    @allure.title("换挡提示_进入条件判断_档位满足&加速踏板位置满足_validity=7")
    @pytest.mark.full
    def test_caseid_1987979(self): 
        hint = "Shift Reminder"  
        self.set_Shift_Reminder(gear=random.choice([0, 2]))          
        try:
            self.ipdu.set_no_crc(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat')
            sleep(2)       
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 10.0) 
            self.partner.ck_wti_no_warning_and_ck_resp(hint, 0) 
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat')
        sleep(2)   
        # self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)  # SOA-28359 Validity！=0时认为是不可信，直接丢弃掉
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=2.5) 

    @allure.title("换挡提示_退出条件判断_100ms内切换档位_无响应")
    @pytest.mark.sanity
    def test_caseid_1988889(self): 
        hint = "Shift Reminder"  
        self.set_Shift_Reminder(gear=random.choice([0, 2]))
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 50.0) 
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)
        for gear in [1, 0]: # P R N D NA
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear)
            sleep(0.03)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.1) # 100ms置位
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)     

    @allure.title("换挡提示_退出条件判断_100ms内切换加速踏板位置_无响应")
    @pytest.mark.sanity
    def test_caseid_1988869(self): 
        hint = "Shift Reminder"          
        self.set_Shift_Reminder(gear=random.choice([0, 2]))
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 50.0) 
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)
        for pos in [0.0, 5.0, 5.1]:
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', pos) # pedal有降频处理，50ms上报一次event，该条用例会出现信号=0.0时无event的现象
            sleep(0.02)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.1) # 100ms置位
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)     

    # SOA-28162
    @allure.title("换挡提示_先满足触发条件_再满足前置条件_无响应")
    @pytest.mark.full
    def test_caseid_1988935(self): # gear change from|AccPedalPosition,oldPosition|Shift Reminder|preHandleAcc,acc
        hint = "Shift Reminder" 
        self.set_Shift_Reminder()
        for gear in [0, 2]:
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 4)
            sleep(0.5) 
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 2.0) 
            sleep(0.5)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', random.choice([6.0, 100.0])) # 加速踏板从 ≤5 跳变至 >5
            sleep(0.5)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear) 
            self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)    

    @allure.title("换挡提示_档位遍历_仅档位处于P/N档时满足触发条件后触发告警")
    @pytest.mark.smoke
    def test_caseid_1988932(self): # gear change from|AccPedalPosition,oldPosition|Shift Reminder|preHandleAcc,acc
        hint = "Shift Reminder"  
        self.set_Shift_Reminder()
        for gear in range(5): # P R N D NA
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 5.0) 
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear)
            sleep(0.5)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 50.0)             
            if gear in [0, 2] :
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)        
                self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.5)
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)

    @allure.title("换挡提示_档位处于P/N档_加速踏板位置从>5跳变至其他值_无响应")
    @pytest.mark.sanity
    def test_caseid_1988933(self):
        hint = "Shift Reminder" 
        self.set_Shift_Reminder(pos=6)  
        for gear, pos in {0:100.0, 2:5.0}.items():
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 99.0)    
            sleep(0.5)       
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear) 
            sleep(0.5)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', pos) # 加速踏板从≤5跳变至≤5或>5
            self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)    

    @allure.title("换挡提示_档位处于P/N档_加速踏板位置从≤5跳变至其他值")
    @pytest.mark.smoke
    def test_caseid_1988934(self):
        hint = "Shift Reminder" 
        self.set_Shift_Reminder()  
        for gear in [0, 2]:
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 5.0)     
            sleep(0.5)   
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear) 
            sleep(0.5)            
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 2.0) # 加速踏板从≤5跳变至≤5
            self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)  
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 10.0) # 加速踏板从≤5跳变至>5
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)        
            self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.2) 

    def set_Release_Brake_Reminder(self, UsgMod=1, brk=0, gear=0, sleeptime=1):
        '''换挡刹车释放提示'''
        self.sd_tester.change_usage_mode(UsgMod) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', brk) # 制动踏板未踩下
        self.partner.empty_all(sleeptime)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear)
        
    @allure.title("换挡刹车释放提示_进入条件判断_先满足触发条件_再满足前置条件")
    @pytest.mark.full
    def test_caseid_1987989(self): 
        hint = "Release Brake Reminder" # 结尾有空格
        self.set_Release_Brake_Reminder()
        self.sd_tester.change_usage_mode(2) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1) 
        sleep(50)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 1)
        sleep(100)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0) 
        
    @allure.title("换挡刹车释放提示_进入条件判断_制动踏板踩下时间和触发条件校验")
    @pytest.mark.sanity    
    def test_caseid_1988860(self): # BrakePedalStatus,value|GearLvrIndcn:|wti current mode|Release Brake Reminder
        hint = "Release Brake Reminder" 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0) 
        self.set_Release_Brake_Reminder(UsgMod=2, brk=1) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 1)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0) # 不足150s 
        sleep(150) # 制动踏板踩下时间超过150s才可满足其前置
        for gear in range(1, 8):
            self.sd_tester.change_usage_mode(2) 
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
            sleep(0.5)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear)
            if gear in [1, 3]:# 从0跳变至1/3
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)        
                self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.5)
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)   

    @allure.title("换挡刹车释放提示_进入条件判断_UsgMod满足_制动踏板状态的validity=7")
    @pytest.mark.full    
    def test_caseid_1988001(self): 
        hint = "Release Brake Reminder" 
        self.set_Release_Brake_Reminder(UsgMod=2, brk=1, sleeptime=150) 
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
            sleep(2)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 1)
            self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)   
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)   

    @allure.title("换挡刹车释放提示_进入条件判断_制动踏板状态满足_UsgMod的validity=4")
    @pytest.mark.full
    def test_caseid_1988003(self): 
        hint = "Release Brake Reminder" 
        self.set_Release_Brake_Reminder(UsgMod=2, brk=1, sleeptime=150) 
        self.ipdu.pause_bus_send("backbonefr")
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetUsageModeValidity", {},
                                              {"out": {"value": 2, "validity": 4}}, timeout=5)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 1)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)   
        self.ipdu.resume_bus_send("backbonefr")    
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)              
            
    @allure.title("换挡刹车释放提示_退出条件判断_100ms计时器超时")
    @pytest.mark.sanity
    def test_caseid_1988861(self): 
        hint = "Release Brake Reminder"    
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.set_Release_Brake_Reminder(UsgMod=2, brk=1, gear=3, sleeptime=150)    
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.5) 

    @allure.title("换挡刹车释放提示_退出条件判断_100ms内制动踏板释放后再次踩下_无响应")
    @pytest.mark.full 
    def test_caseid_1988863(self): 
        hint = "Release Brake Reminder"    
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.set_Release_Brake_Reminder(UsgMod=2, brk=1, gear=3, sleeptime=150) 
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)
        for i in [0, 1]:
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', i) 
            sleep(0.02)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.1) # 100ms置位
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)    

    @allure.title("换挡刹车释放提示_退出条件判断_100ms内再次触发GearLvrIndcn跳变_无响应")
    @pytest.mark.full
    def test_caseid_1988004(self): 
        hint = "Release Brake Reminder"    
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.set_Release_Brake_Reminder(UsgMod=2, brk=1, gear=3, sleeptime=150) 
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)
        for i in [0, 3]:
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', i) 
            sleep(0.03)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.1) # 100ms置位
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)   

    @allure.title("换挡刹车释放提示_退出条件判断_计时器开启1s后_切换UsgMod_无响应")
    @pytest.mark.sanity
    def test_caseid_1988864(self): 
        hint = "Release Brake Reminder"      
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.set_Release_Brake_Reminder(UsgMod=2, brk=1, gear=3, sleeptime=150)   
        self.partner.empty_all(1)
        self.sd_tester.change_usage_mode(random.choice([0, 1, 11, 13]))      
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0, timeout=2) 
        
    @allure.title("换挡刹车释放提示_退出条件判断_计时器开启1s后_释放制动踏板_无响应")
    @pytest.mark.full
    def test_caseid_1988865(self): 
        hint = "Release Brake Reminder"    
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.set_Release_Brake_Reminder(UsgMod=2, brk=1, gear=3, sleeptime=150) 
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0) 
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0, timeout=2)   
                                              
    def set_Brake_Overide_Accelerator(self, gear=random.choice([1, 3]), speed=0, brk=1, acc=10.0, status=random.choice([0, 3, 4, 5])):
        '''制动优先BOA'''
        self.sd_tester.change_usage_mode(random.choice([11, 13])) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear) # gear
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3) # 车速有效
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', speed) # DisplaySpeedChanged
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', brk) # 制动踏板
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', acc) # 加速踏板
        dict={0:1, 1:2, 2:3, 3:4, 4:0, 5:5} # status:信号值
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  dict[status]) # LaunchMode.info.status
        self.partner.empty_all(4.5) # 防止进入4s计时器
        
    @allure.title("制动优先BOA_进入条件判断_其他条件满足_档位遍历")
    @pytest.mark.sanity
    def test_caseid_1988937(self): # Brake Overide Accelerator|GearLvrIndcn:|gear change from |LaunchMode,fault:|BrakePedalStatus,value:|AccPedalPosition,position:
        hint = "Brake Overide Accelerator" 
        self.set_Brake_Overide_Accelerator(gear=4)
        for gear in range(5):
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear) # gear
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)          
            sleep(0.2)   
            if gear in [1, 3]:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0) # 防止回idle后再次进入Wanring
                self.partner.ck_wti_no_warning_and_ck_resp(hint, 1, timeout=3)
                self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=1) # 4s置位
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)

    @allure.title("制动优先BOA_进入条件判断_其他条件满足_显示车速isvalid=Flase")
    @pytest.mark.full
    def test_caseid_1988938(self): 
        hint = "Brake Overide Accelerator" 
        self.set_Brake_Overide_Accelerator(gear=4)
        self.ipdu.pause_bus_send("backbonefr") # FR信号丢失后，会使得车速isValid=False，制动踏板不存在信号丢失场景
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetDisplaySpeed", {}, {"out": {"isvalid":False}}, timeout=3)  
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', random.choice([1, 3])) 
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', random.choice([0, 2, 4])) # 防止回idle后再次进入Wanring
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 1, timeout=3.7)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.5) # 4s置位
        self.ipdu.resume_bus_send("backbonefr")
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)
                        
    @allure.title("制动优先BOA_进入条件判断_其他条件满足_制动踏板状态遍历")
    @pytest.mark.full
    def test_caseid_1988939(self): 
        hint = "Brake Overide Accelerator" 
        self.set_Brake_Overide_Accelerator(brk=0)   
        for brk in [1, 0]:
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', brk) 
            sleep(0.5)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', random.choice([1, 3]))
            if brk == 1:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', random.choice([0, 2, 4])) # 防止回idle后再次进入Wanring
                self.partner.ck_wti_no_warning_and_ck_resp(hint, 1, timeout=3)
                self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=1) # 4s置位
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)

    @allure.title("制动优先BOA_进入条件判断_其他条件满足_制动踏板validity=7")
    @pytest.mark.full
    def test_caseid_1988023(self): 
        hint = "Brake Overide Accelerator" 
        self.set_Brake_Overide_Accelerator(brk=0)   
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
            self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatusValidity", {"pedals": [1]},
                                                  {"out": [{"statusValidity": 7}]}, timeout=2.5)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1) 
            self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)   
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=2.5)    

    @allure.title("制动优先BOA_进入条件判断_其他条件满足_加速踏板位置遍历")
    @pytest.mark.full
    def test_caseid_1988940(self): 
        hint = "Brake Overide Accelerator" 
        self.set_Brake_Overide_Accelerator(acc=1.0)   
        for acc in [1.1, 0, 2.0, 99.9, 1.0, 100.0]:
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', acc)
            sleep(0.5)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', random.choice([1, 3]))
            if acc > 1.0:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', random.choice([0, 2, 4])) # 防止回idle后再次进入Wanring
                self.partner.ck_wti_no_warning_and_ck_resp(hint, 1, timeout=3)
                self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=1) # 4s置位
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)

    @allure.title("制动优先BOA_进入条件判断_其他条件满足_加速踏板validity=7")
    @pytest.mark.full
    def test_caseid_1988024(self): 
        hint = "Brake Overide Accelerator" 
        self.set_Brake_Overide_Accelerator(acc=0)   
        try:
            self.ipdu.set_no_crc(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat')
            self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [0]},
                                                {"out": [{"id": 0, "statusValidity": 7}]}, timeout=3)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 50.0)
            self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)   
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat')
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=2.5)    
        
    @allure.title("制动优先BOA_进入条件判断_其他条件满足_弹射起步功能状态遍历")
    @pytest.mark.sanity
    def test_caseid_1988941(self): 
        hint = "Brake Overide Accelerator" 
        self.set_Brake_Overide_Accelerator(status=1)   
        for status in range(6):
            dict={0:1, 1:2, 2:3, 3:4, 4:0, 5:5} # status:信号值
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  dict[status]) # LaunchMode.info.status
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1) 
            if status not in [1, 2]:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0) 
                self.partner.ck_wti_no_warning_and_ck_resp(hint, 1, timeout=3)
                self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=1.5) # 4s置位
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)
        for signal in [6, 7]: # 弹射状态保持last_value
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  signal)
            self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)     

    @allure.title("制动优先BOA_进入条件判断_Warning下4s内未改变触发条件_4s超时回idle后再次上报Wanring")
    @pytest.mark.sanity
    def test_caseid_1988947(self):
        hint = "Brake Overide Accelerator"       
        self.set_Brake_Overide_Accelerator(brk=0)       
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)   
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)    
        for _ in range(2): 
            self.partner.ck_wti_no_warning_and_ck_resp(hint, 1, timeout=3.5)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '0'}]}, timeout=1) # 4s置位
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1) # 置位后判断仍满足条件，再次Wanring 

    @allure.title("制动优先BOA_退出条件判断_4s内切换档位_计时结束时档位仍满足前置条件")
    @pytest.mark.sanity
    def test_caseid_1988948(self):
        hint = "Brake Overide Accelerator"       
        self.set_Brake_Overide_Accelerator(gear=1, brk=0)       
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)   
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)     
        for gear in [random.choice([0, 2, 4]), 3]:               
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear) # gear
            sleep(1.5)
        self.partner.ck_coming_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '0'}]}, timeout=1.5) # 4s置位
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1) # 置位后判断仍满足条件，再次Wanring     
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 1, timeout=3)   

    @allure.title("制动优先BOA_退出条件判断_4s内切换档位_计时结束时档位不满足前置条件")
    @pytest.mark.sanity
    def test_caseid_1988942(self):
        hint = "Brake Overide Accelerator"       
        self.set_Brake_Overide_Accelerator(brk=0)       
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)   
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)     
        for gear in range(5):               
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear) # gear
            sleep(0.7)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.8) # 4s置位
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)    

    @allure.title("制动优先BOA_退出条件判断_4s内切换弹射起步功能状态_计时结束时弹射起步功能状态仍满足前置条件")
    @pytest.mark.full
    def test_caseid_1988949(self):
        hint = "Brake Overide Accelerator"       
        self.set_Brake_Overide_Accelerator(brk=0)       
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)   
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)     
        for status in range(6):
            dict={0:1, 1:2, 2:3, 3:4, 4:0, 5:5} # status:信号值
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  dict[status]) # LaunchMode.info.status
            sleep(0.5)        
        self.partner.ck_coming_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '0'}]}, timeout=1.5) 
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1) # 置位后判断仍满足条件，再次Wanring     
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 1, timeout=3)   

    @allure.title("制动优先BOA_退出条件判断_4s内切换弹射起步功能状态_计时结束时弹射起步功能状态不满足前置条件")
    @pytest.mark.full
    def test_caseid_1988943(self):
        hint = "Brake Overide Accelerator"   
        self.set_Brake_Overide_Accelerator(brk=0)    
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)   
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)  
        for status in [0, 1, 3, 4, 5, 2]:
            dict={0:1, 1:2, 3:4, 4:0, 5:5, 2:3} # status:信号值
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  dict[status]) # LaunchMode.info.status
            sleep(0.5)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=1.5) # 4s置位
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)            

    @allure.title("制动优先BOA_退出条件判断_4s内制动踏板状态变化_计时结束时制动踏板仍满足前置条件")
    @pytest.mark.sanity
    def test_caseid_1988950(self):
        hint = "Brake Overide Accelerator"       
        self.set_Brake_Overide_Accelerator(gear=0)    
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', random.choice([1, 3]))
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)     
        for brk in [0, 1]:
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', brk) 
            sleep(1.5)
        self.partner.ck_coming_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '0'}]}, timeout=1.5) 
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1) # 置位后判断仍满足条件，再次Wanring     
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 1, timeout=3)  

    @allure.title("制动优先BOA_退出条件判断_4s内制动踏板状态变化_计时结束时制动踏板不满足前置条件")
    @pytest.mark.full
    def test_caseid_1988944(self):
        hint = "Brake Overide Accelerator"     
        self.set_Brake_Overide_Accelerator(gear=0)    
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', random.choice([1, 3]))
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)                    
        for brk in [0, 1, 0]:
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', brk) 
            sleep(1)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=1.5) # 100ms置位
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)  

    @allure.title("制动优先BOA_退出条件判断_4s内加速踏板位置变化_计时结束时加速踏板仍满足前置条件")
    @pytest.mark.full
    def test_caseid_1988951(self):
        hint = "Brake Overide Accelerator"       
        self.set_Brake_Overide_Accelerator(gear=0)    
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', random.choice([1, 3]))
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)     
        for acc in [1.0, 1.1, 100.0]:
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', acc)
            sleep(1)
        self.partner.ck_coming_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '0'}]}, timeout=1.5) 
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1) # 置位后判断仍满足条件，再次Wanring     
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 1, timeout=3)  

    @allure.title("制动优先BOA_退出条件判断_4s内加速踏板位置变化_计时结束时加速踏板不满足前置条件")
    @pytest.mark.sanity
    def test_caseid_1988945(self):
        hint = "Brake Overide Accelerator"     
        self.set_Brake_Overide_Accelerator(gear=0)    
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', random.choice([1, 3]))
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)                    
        for acc in [1.0, 1.1, 100.0, 0]:
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', acc)
            sleep(0.8)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=1.5) # 100ms置位
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)    

    @allure.title("制动优先BOA_重启场景_未收到弹射起步功能状态信号")
    @pytest.mark.full
    def test_caseid_1988952(self):
        hint = "Brake Overide Accelerator"   
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg',  0)     
        self.set_Brake_Overide_Accelerator(gear=0)    
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', random.choice([1, 3]))
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)    
        self.ipdu.pause_bus_send("chassiscan1") # 弹射起步状态重启后为默认值255
        sleep(2)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        sleep(2)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '0'}]}, timeout=3) 
        self.ipdu.resume_bus_send("chassiscan1")
        self.partner.ck_wti_warning_and_resp(hint, 1, timeout=3)  

    @allure.title("制动优先BOA_重启场景_LaunchMode.info.status=255")
    @pytest.mark.full
    def test_caseid_1988956(self):
        hint = "Brake Overide Accelerator"   
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg',  0)     
        self.set_Brake_Overide_Accelerator(gear=0)    
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', 7) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', random.choice([1, 3]))
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1) 
        sleep(2)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg',  13)
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"LaunchMode",{"info":{"status":255, "fault":13}})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '0'}]}, timeout=1) 
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', 0)
        self.partner.ck_wti_warning_and_resp(hint, 1, timeout=1)  

    def set_Launch_Mode_Operation_Reminder_pre1(self, bonnet=1, doorsts=[0, 0, 0, 0, 0], angle=0.0, epb=9, bltsts=0, bltst1=1):
        ''' 弹射起步引导提示信息 '''
        self.boon_all_open_close(bonnet) # 1=关闭 status.sts=1; 0=打开 status.sts=0
        self.dk.set_door_sts(doorsts)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3) # SteerWheelInfo.info.isvalid=True
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', angle) # 方向盘转角 SteerWheelInfo.info.angle
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', epb) # EPB功能运行状态 EPBOperationStatu.state
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', bltsts)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', bltst1)

    def set_Launch_Mode_Operation_Reminder_pre2(self, gear=3, status=random.choice([3, 4]), fault=0, brk=11.5, acc=96.0, road=0.0, info=0, sleeptime=1):
        ''' 弹射起步引导提示信息 '''
        self.sd_tester.change_usage_mode(random.choice([11, 13])) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', random.choice([0, 1]))
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear) # gear
        dict={0:1, 1:2, 2:3, 3:4, 4:0, 5:5} # status:信号值
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg', fault)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  dict[status]) # LaunchMode.info.status
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', brk) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', acc) 
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr11, 'RoadInclnRoadIncln', road)
        sleep(sleeptime)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, 
                                              {"out": [{"name": "Launch Mode Operation Reminder" , "info": str(info)}]}, timeout=3)     
        self.partner.empty_all()

    @allure.title("弹射起步引导提示信息_info=1_RoadInclnRoadIncln绝对值>0.05_通过遍历LaunchMode.info.status触发进入&退出")
    @pytest.mark.full
    def test_caseid_1988178(self): # 仅检查故障1 # handleLunchIndicator,status|Launch Mode Operation Reminder|gear change from 
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(road=0.9)   
        for signal_status in range(8): # signal:status={0:4, 1:0, 2:1, 3:2, 4:3, 5:5, 6:5, 7:5}
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', signal_status)
            value=1 if signal_status == 1 else 0
            logger.info(f"打印当前返回值 value={value}, signal_status={signal_status}")
            if signal_status in [1, 2, 4]:  # signal:status={0:4, 1:0, 2:1, 3:2, 4:3, 5:5, 6:5, 7:5}
                self.partner.ck_wti_warning_and_resp(hint, value)  
            elif signal_status == 3: 
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},  
                                                      {"out": [{"name": hint, "info": '0'}]})     
                self.partner.ck_wti_coming_warning_and_resp(hint, 8, timeout=1)
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, value)   
                
    @allure.title("弹射起步引导提示信息_info=1_LaunchMode.info.status=0_通过遍历RoadInclnRoadIncln正负数触发进入&保持&退出")
    @pytest.mark.sanity
    def test_caseid_1988179(self): # 仅检查故障1
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=0) 
        dict={0:[0.98, -0.98],1:[0.04, -0.04], 2:[0.038, -0.038, 0]}
        for i in range(len(dict[0])):
            for j in range(len(dict[1])):
                    for k in range(len(dict[2])):
                        logger.info(f"打印当前值 i={i}, {dict[0][i]}, 触发")
                        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr11, 'RoadInclnRoadIncln', dict[0][i]) 
                        self.partner.ck_wti_warning_and_resp(hint, 1)  
                        logger.info(f"打印当前值 j={j}, {dict[1][j]}, 维持")
                        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr11, 'RoadInclnRoadIncln', dict[1][j]) 
                        self.partner.ck_wti_no_warning_and_ck_resp(hint, 1)   
                        logger.info(f"打印当前值 k={k}, {dict[2][k]}, 退出")
                        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr11, 'RoadInclnRoadIncln', dict[2][k])      
                        self.partner.ck_wti_warning_and_resp(hint, 0)  

    @allure.title("弹射起步引导提示信息_info=2/3/4/5_LaunchMode.info.status=0_通过遍历fault触发进入&退出")
    @pytest.mark.sanity
    def test_caseid_1988193(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=0) 
        res={9:2, 8:3, 7:4, 6:5} # fault与info的映射关系
        last_value=0
        for signal_fault in range(16):
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg', signal_fault)
            value=res[signal_fault] if signal_fault in [6, 7, 8, 9] else 0
            if last_value==value:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, value)     
            else:
                self.partner.ck_wti_warning_and_resp(hint, value)  
            last_value=value

    @allure.title("弹射起步引导提示信息_info=2/3/4/5_LaunchMode.info.fault=9/8/7/6_通过status=0/5保持")
    @pytest.mark.full
    def test_caseid_1988195(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=0) 
        dict1={9:2, 8:3, 7:4, 6:5} # fault与info的映射关系
        for signal_fault, value in dict1.items():
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg', signal_fault)
            self.partner.ck_wti_warning_and_resp(hint, value)  
            for signal_status in [5, 6, 1, 7]: # signal:status={0:4, 1:0, 2:1, 3:2, 4:3, 5:5, 6:5, 7:5}
                self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', signal_status)
                logger.info(f"打印当前返回值:fault={signal_fault}, signal_status={signal_status}, value={value}")
                self.partner.ck_wti_no_warning_and_ck_resp(hint, value)       

    @allure.title("弹射起步引导提示信息_info=2/3/4/5_通过LaunchMode.info.status=5&fault取随机值保持当前info")
    @pytest.mark.full
    def test_caseid_1988199(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=0) 
        dict1={9:2, 8:3, 7:4, 6:5} # fault与info的映射关系
        for signal_fault1, value in dict1.items():
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', 1) # 再次进入
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg', signal_fault1)
            self.partner.ck_wti_warning_and_resp(hint, value)  
            for signal_status in [5, 6, 7]: # signal:status={0:4, 1:0, 2:1, 3:2, 4:3, 5:5, 6:5, 7:5}
                self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', signal_status)
                sleep(0.5)
                self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg', random.choice([0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15]))
                self.partner.ck_wti_no_warning_and_ck_resp(hint, value)       
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', 4) # LaunchMode.info.status=3, 退出使得info=0 
            self.partner.ck_wti_warning_and_resp(hint, 0)  
            
    @allure.title("弹射起步引导提示信息_info=2/3/4/5_LaunchMode.info.fault=9/8/7/6_通过status=1/2/3/4退出")
    @pytest.mark.full
    def test_caseid_1988200(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=0) 
        dict1={9:2, 8:3, 7:4, 6:5} # fault与info的映射关系
        for signal_fault1, value in dict1.items():
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg', signal_fault1)
            self.partner.ck_wti_warning_and_resp(hint, value)  
            for signal_status in [2, 3, 4, 0]: # signal:status={0:4, 1:0, 2:1, 3:2, 4:3, 5:5, 6:5, 7:5}
                self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', signal_status) # 退出
                if signal_fault1 == 7 and signal_status == 2: # info=4时，LaunchMode.info.status=1 不会退出
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, value)   
                else:
                    self.partner.ck_wti_warning_and_resp(hint, 0)  
                    self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', 1) # 再次进入 LaunchMode.info.status=0
                    self.partner.ck_wti_warning_and_resp(hint, value)  
                        
    @allure.title("弹射起步引导提示信息_info=4_LaunchMode.info.status=1_通过遍历fault触发进入&退出")
    @pytest.mark.sanity
    def test_caseid_1988201(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=1) 
        for signal_fault in range(16):
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg', signal_fault)
            value=4 if signal_fault == 7 else 0
            if signal_fault in [7, 8]:
                self.partner.ck_wti_warning_and_resp(hint, value)    
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, value)   
                
    @allure.title("弹射起步引导提示信息_info=2_通过status.sts触发进入&退出")
    @pytest.mark.full
    def test_caseid_1988207(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=0)     
        dict1={0:2, 1:0}
        for key, value in dict1.items():
            self.boon_all_open_close(key)
            self.partner.ck_wti_warning_and_resp(hint, value)    

    @allure.title("弹射起步引导提示信息_info=2_通过DoorSts.openCloseSts.isOpen触发进入和退出_单个门开关状态遍历")
    @pytest.mark.full
    def test_caseid_1988208(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=0)             
        doorsts=[0, 0, 0, 0, 0]
        for i in range(4):
            doorsts[i]=1
            self.dk.set_door_sts(doorsts)
            self.partner.ck_wti_warning_and_resp(hint, 2)   
            self.dk.set_door_sts([0, 0, 0, 0, 0])
            self.partner.ck_wti_warning_and_resp(hint, 0)   

    @allure.title("弹射起步引导提示信息_info=2_通过DoorSts.openCloseSts.isOpen触发进入和退出_四门依次打开&依次关闭")
    @pytest.mark.sanity
    def test_caseid_1988210(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=0)   
        # 四门全关，依次打开
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.partner.ck_wti_warning_and_resp(hint, 2)   
        doorsts=[1, 0, 0, 0, 0]
        for i in range(3):
            doorsts[i+1]=1
            self.dk.set_door_sts(doorsts)
            sleep(0.5)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 2) 
        # 四门全开后，依次关闭
        for i in range(3):
            doorsts[i]=0
            self.dk.set_door_sts(doorsts)
            sleep(0.5)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 2) 
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.partner.ck_wti_warning_and_resp(hint, 0)   
        
    @allure.title("弹射起步引导提示信息_info=2_通过DoorSts.openCloseSts.isOpen触发进入和退出_先开主驾再开副驾,先关副驾再关主驾")
    @pytest.mark.full
    def test_caseid_1988211(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=0)     
        self.dk.set_door_sts([1, 0, 0, 0, 0]) # 先开主驾再开副驾
        self.partner.ck_wti_warning_and_resp(hint, 2)       
        self.dk.set_door_sts([1, 1, 0, 0, 0])     
        sleep(1)
        self.dk.set_door_sts([1, 0, 0, 0, 0]) # 先关副驾再关主驾    
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 2) 
        self.dk.set_door_sts([0, 0, 0, 0, 0])     
        self.partner.ck_wti_warning_and_resp(hint, 0) 
        
    @allure.title("弹射起步引导提示信息_info=2_通过DoorSts.openCloseSts.isOpen触发进入和退出_尾门打开&关闭")
    @pytest.mark.full
    def test_caseid_1988212(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=0)            
        self.dk.set_door_sts([0, 0, 0, 0, 1]) # 仅开尾门 不进入info=2
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0) 
        self.dk.set_door_sts([0, 0, 0, 1, 1])   
        self.partner.ck_wti_warning_and_resp(hint, 2)        
        self.dk.set_door_sts([0, 0, 0, 1, 0])  # 进入info=2后，关尾门不退出  
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 2)   
        self.dk.set_door_sts([0, 0, 0, 0, 0])     
        self.partner.ck_wti_warning_and_resp(hint, 0)  

    @allure.title("弹射起步引导提示信息_info=3_通过遍历BltLockStAtDrvrBltLockSts触发进入&退出")
    @pytest.mark.full
    def test_caseid_1988218(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=0)  
        dict1={1:3, 0:0}  
        for key,value in dict1.items():
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', key)
            self.partner.ck_wti_warning_and_resp(hint, value)  
            
    @allure.title("弹射起步引导提示信息_info=3_通过遍历BltLockStAtDrvrBltLockSt1触发进入&退出")
    @pytest.mark.full
    def test_caseid_1988219(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=0)  
        dict1={0:3, 1:0}  
        for key,value in dict1.items(): 
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', key) 
            self.partner.ck_wti_warning_and_resp(hint, value)  

    @allure.title("弹射起步引导提示信息_info=4_通过遍历Gear.gear触发进入&保持&退出")
    @pytest.mark.sanity
    def test_caseid_1988235(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=0)  
        for gear in range(5):
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear)
            value = 0 if gear == 3 else 4
            if gear in [0, 3, 4]:
                self.partner.ck_wti_warning_and_resp(hint, value)  
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, value) 

    @allure.title("弹射起步引导提示信息_info=4_通过遍历EPBOperationStatu.state触发进入&保持&退出")
    @pytest.mark.full
    def test_caseid_1988240(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=1)  
        for i in range(16):
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', i)
            value = 0 if i == 9 else 4
            if i in [0, 9, 10]:
                self.partner.ck_wti_warning_and_resp(hint, value)  
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, value) 

    @allure.title("弹射起步引导提示信息_info=5_通过遍历SteerWheelInfo.info.angle正负数触发进入&保持&退出")
    @pytest.mark.full
    def test_caseid_1988243(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=0)   
        limit_angle=10*3.1416/180 # 10*math.pi/180=0.174533  已确认Π取3.1416
        for i in [limit_angle+0.1,  -limit_angle-0.1]:
            for j in [limit_angle-0.1, 0,  -limit_angle+0.1]:
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', i)
                self.partner.ck_wti_warning_and_resp(hint, 5)  
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', j)
                self.partner.ck_wti_warning_and_resp(hint, 0)    

    @allure.title("弹射起步引导提示信息_info=6_通过BrkPedlTrvlAct触发进入&保持&退出")
    @pytest.mark.full
    def test_caseid_1988253(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=1)  
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', random.choice([10.49, 0])) # 进入 brk < 10.5, 时间超过0.5s
        self.partner.ck_wti_coming_warning_and_resp(hint, 6) 
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 11.0) # 保持
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 6)  
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 11.5) # 退出 brk >= 11.5, 时间超过0.5s
        self.partner.ck_wti_coming_warning_and_resp(hint, 0)     
        
    @allure.title("弹射起步引导提示信息_info=6_通过LaunchMode.info.status触发进入&退出")
    @pytest.mark.full
    def test_caseid_1988254(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(brk=10.0)  
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', 2) # LaunchMode.info.status=1
        self.partner.ck_wti_warning_and_resp(hint, 6)  
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', 6) # LaunchMode.info.status会保持上一次的值
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 6)  
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', 3) # LaunchMode.info.status=2
        self.partner.ck_wti_coming_warning_and_resp(hint, 8)         
        
    @allure.title("弹射起步引导提示信息_info=6_BrkPedlTrvlAct进入时的持续时间校验")
    @pytest.mark.full
    def test_caseid_1988255(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=1)  
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 0) 
        sleep(0.3)
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 16.0) 
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)   
        
    @allure.title("弹射起步引导提示信息_info=6_BrkPedlTrvlAct退出时的持续时间校验")
    @pytest.mark.full
    def test_caseid_1988256(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=1, brk=0, info=6)  
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 16.0) 
        sleep(0.3)
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 10.0) 
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 6)     
        
    @allure.title("弹射起步引导提示信息_info=7_通过AccrPedlRatAccrPedlRat触发进入&保持&退出")
    @pytest.mark.full
    def test_caseid_1988265(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=1)          
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 11.0)    
        sleep(0.3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 90.0)                           
        self.partner.ck_wti_coming_warning_and_resp(hint, 7) # 进入 信号持续时间超过0.5s     
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 92.0) 
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 7) # 保持    
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 95.01)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0) # 退出 acc > 95.0, 持续时间超过0.5s 
        
    @allure.title("弹射起步引导提示信息_info=7_通过LaunchMode.info.status触发进入&退出")
    @pytest.mark.full
    def test_caseid_1988267(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2()    
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 11.0)    
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 89.9)   
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)        
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  2) # LaunchMode.info.status=1
        self.partner.ck_wti_warning_and_resp(hint, 7)  
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  1) # LaunchMode.info.status=0
        self.partner.ck_wti_warning_and_resp(hint, 0)  

    @allure.title("弹射起步引导提示信息_info=7_通过BrkPedlTrvlAct触发进入&保持&退出")
    @pytest.mark.sanity
    def test_caseid_1988269(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=1, acc=0, info=7)  
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 10.9) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 90.9) # 维持7，防止退出6后再次通过进入条件映射7
        sleep(0.5)
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 10.5) 
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 7)       
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 10.49) # 进6退7
        self.partner.ck_wti_coming_warning_and_resp(hint, 6)
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 11.5) 
        self.partner.ck_wti_warning_and_resp(hint, 0)  # 证明BrkPedlTrvlAct=10.49的时候 退出了7
        
    @allure.title("弹射起步引导提示信息_info=7_BrkPedlTrvlAct进入时的持续时间校验")
    @pytest.mark.full
    def test_caseid_1988270(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=1)       
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 10.5) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 80.0)
        sleep(0.5)        
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 11.0) 
        sleep(0.3)
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 10.5) 
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)   
        
    @allure.title("弹射起步引导提示信息_info=7_AccrPedlRatAccrPedlRat进入时的持续时间校验")
    @pytest.mark.full
    def test_caseid_1988271(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=1)           
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 11.0) 
        sleep(0.5)        
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 90.0)
        sleep(0.3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 92.0)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)   

    @allure.title("弹射起步引导提示信息_info=7_BrkPedlTrvlAct退出时的持续时间校验")
    @pytest.mark.full
    def test_caseid_1988273(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=1)     
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 80.0)      
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 11.0)     
        self.partner.ck_wti_coming_warning_and_resp(hint, 7)
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 10.0) 
        sleep(0.3)
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 10.6)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 7)   

    @allure.title("弹射起步引导提示信息_info=7_AccrPedlRatAccrPedlRat退出时的持续时间校验")
    @pytest.mark.full
    def test_caseid_1988274(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=1)    
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 80.0)      
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 11.0)     
        self.partner.ck_wti_coming_warning_and_resp(hint, 7)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 100.0)      
        sleep(0.3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 92.0)    
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 7) 
        
    @allure.title("弹射起步引导提示信息_info=8_通过遍历LaunchMode.info.status触发进入&退出")
    @pytest.mark.full
    def test_caseid_1988304(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2()  
        for signal_status in range(8): # signal:status={0:4, 1:0, 2:1, 3:2, 4:3, 5:5, 6:5, 7:5}
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', signal_status)
            value=8 if signal_status==3 else 0
            if signal_status in [3, 4]: 
                self.partner.ck_wti_warning_and_resp(hint, value)  
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, value) 

    @allure.title("弹射起步引导提示信息_info=8_通过BrkPedlTrvAct触发进入&保持")
    @pytest.mark.smoke
    def test_caseid_1988327(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2()  
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', 3) # # LaunchMode.info.status=2
        sleep(0.2)
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 0.0) # 物理值=0
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0) 
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 0) # 总线值=0，物理值=-5
        self.partner.ck_wti_warning_and_resp(hint, 8) 
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 0.0)
        sleep(0.5)
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 10.0)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 8) 
        
    @allure.title("弹射起步引导提示信息_info=8_LaunchMode.info.status进入时的持续时间校验")
    @pytest.mark.full
    def test_caseid_1988328(self):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2()  
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  3) # LaunchMode.info.status=2  
        sleep(0.3) 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  1) 
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)  

    @allure.title("弹射起步引导提示信息_优先级_info=1/2/3/4/5_从小到大依次触发")
    @pytest.mark.full
    def test_caseid_1988378(self): # 2＞3＞4＞1＞5＞6＞7＞8＞0
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=0)  
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', random.choice([14.0, -14.0]))
        self.partner.ck_wti_warning_and_resp(hint, 5)  
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr11, 'RoadInclnRoadIncln', 0.06) 
        self.partner.ck_wti_warning_and_resp(hint, 1)  
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr11, 'RoadInclnRoadIncln', 0.04) # 维持info=1
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)       
        self.partner.ck_wti_warning_and_resp(hint, 4) 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 1)
        self.partner.ck_wti_warning_and_resp(hint, 3) 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg', 9)   
        self.partner.ck_wti_warning_and_resp(hint, 2)    
        
    @allure.title("弹射起步引导提示信息_优先级_info=1/2/3/4/5_从大到小依次触发")
    @pytest.mark.smoke
    def test_caseid_1988379(self): # 2＞3＞4＞1＞5＞6＞7＞8＞0
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1(angle=random.choice([14.0, -14.0]), bltsts=1)
        self.set_Launch_Mode_Operation_Reminder_pre2(gear=0, status=0, fault=9, road=0.06, info=2)  
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr11, 'RoadInclnRoadIncln', 0.04) # 维持info=1
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg', 0)   
        self.partner.ck_wti_warning_and_resp(hint, 3) 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
        self.partner.ck_wti_warning_and_resp(hint, 4)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 3)      
        self.partner.ck_wti_warning_and_resp(hint, 1)  
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr11, 'RoadInclnRoadIncln', 0.038) 
        self.partner.ck_wti_warning_and_resp(hint, 5)  
        
    @allure.title("弹射起步引导提示信息_优先级_info=2/3/4/5")
    @pytest.mark.full
    def test_caseid_1988380(self): # 2＞3＞4＞1＞5＞6＞7＞8＞0
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1(bonnet=0)
        self.set_Launch_Mode_Operation_Reminder_pre2(status=0, info=2)  
        for fault in [6, 7, 8, 9]:
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg', fault)   
            self.partner.ck_wti_no_warning_and_ck_resp(hint, 2)  

    @allure.title("弹射起步引导提示信息_优先级_info=4/6/7/8")
    @pytest.mark.full
    def test_caseid_1988381(self): # 2＞3＞4＞1＞5＞6＞7＞8＞0 handleLunchIndicator,status|Launch Mode Operation Reminder|gear change from 
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=1, brk=1.5, acc=89.9, info=6)  
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 11.2) # info=7, 维持6
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 6)  
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg', 7)
        self.partner.ck_wti_warning_and_resp(hint, 4)  
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg', 0)
        self.partner.ck_wti_warning_and_resp(hint, 6)  
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', 3)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                          {"list": [{"name": hint, "info": '0'}]}, timeout=1)
        self.partner.ck_wti_warning_and_resp(hint, 8)  

    @allure.title("弹射起步引导提示信息_重启后未收到所有总线信号")
    @pytest.mark.full
    def test_caseid_1988382(self):  
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1(bltst1=0)
        self.set_Launch_Mode_Operation_Reminder_pre2(gear=0, status=0, fault=9, info=2)  
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT, resume_all_bus=False)
        sleep(2)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '0'}]}, timeout=2)
        self.ipdu.resume_all_bus_send()
        self.partner.ck_wti_warning_and_resp(hint, 2, timeout=3)  

    @allure.title("弹射起步引导提示信息_重启后未收到backbonefr总线信号")
    @pytest.mark.full
    def test_caseid_1988383(self):  # 重启后 前舱盖拿到默认值65535
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1(bltsts=1, bltst1=0)
        self.set_Launch_Mode_Operation_Reminder_pre2(gear=0, status=0, info=3)  
        self.ipdu.pause_bus_send("backbonefr") 
        self.partner.empty_all(3) 
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 65535}, timeout=2)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '2'}]}, timeout=3) # partner会存在收不到通知的情况  
        self.ipdu.resume_bus_send("backbonefr")  
        self.partner.ck_wti_warning_and_resp(hint, 3, timeout=3)  

    @allure.title("弹射起步引导提示信息_重启后未收到propulsioncan总线信号")
    @pytest.mark.full
    def test_caseid_1988384(self):  
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=1, acc=5.1, info=7)          
        sleep(2)
        self.ipdu.pause_bus_send("propulsioncan") # 重启后不会收到 acc + gear 的底层信号
        self.partner.empty_all(3) 
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        sleep(2)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetGear", {}, {"out": 5})

        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '4'}]}, timeout=2) # 重启后拿到的gear=5
        self.ipdu.resume_bus_send("propulsioncan")  
        self.partner.ck_wti_warning_and_resp(hint, 0, timeout=3) # 档位信号上来后映射info=4, acc上来后映射info=7

    @allure.title("弹射起步引导提示信息_重启后未收到chassiscan1总线信号")
    @pytest.mark.full
    def test_caseid_1988385(self):  
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=0, fault=7, road=0.1, info=4)
        self.ipdu.pause_bus_send("chassiscan1") # 重启后不会收到 弹射起步的status和fault 的底层信号
        self.partner.empty_all(3) 
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        sleep(2)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '0'}]}) # 如果启动后上报了LaunchMode的默认值，此时Info=1，否则=0
        self.ipdu.resume_bus_send("chassiscan1")  
        self.partner.ck_wti_warning_and_resp(hint, 4, timeout=3)   

    @allure.title("弹射起步引导提示信息_重启后未收到chassiscan2总线信号")
    @pytest.mark.full
    def test_caseid_1988386(self):  
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=0, road=0.1, info=1)     
        self.ipdu.pause_bus_send("chassiscan2") # 重启后不会收到 brk + road 的底层信号
        self.partner.empty_all(3) 
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        sleep(2)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '0'}]})  # 如果底层road没收到 异常按照默认值映射的话，会映射info=7
        self.ipdu.resume_bus_send("chassiscan2")   
        self.partner.ck_wti_warning_and_resp(hint, 1, timeout=3)      
                                                           
######################################################################################################################################################## 

@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIService_Chassis")
@pytest.mark.aqx    
class TestChassisWTIServiceMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21", enable_inter_service=True)
        self.partner = S2sBaseClass([("WTIService", "client"),
                                     ("ChassisService", "client"),
                                     ("VehicleModeService", "client"),
                                     ("PedalService", "client")
                                     ])
        self.partner.wait_for_service_reconnect(WTI_SERVICE_CLIENT) 
        sleep(15)

    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all(5)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        sleep(5)
        super().after_each_func(ecu)     

    def set_Autohold_Active_Green_and_Standby_Grey(self, hint, Lamp):
        '''Autohold激活指示灯+Autohold待命指示灯 前置设为info=1 '''
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 2) # UsgMod信号
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'AutHldSoftSwtEnaSts', 1) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'LampReqByVehHld', Lamp) # len=2  
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0) # 删除 给一个不满足GearLvrIndcn=2 or 3的值 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'DoorDrvrStsWithFacQlyDoorSts', 2) # len=2
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'DoorDrvrStsWithFacQlyFacQly', 3) # len=2
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', 1) # len=1 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr10, 'SmartAutoHldCtrlSts', 1) # 删除 给一个不满足0的值 len=1 
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, 
                                              {"out": [{"name": hint, "state": "1"}]}, timeout=5)
        self.partner.empty_all()

    @allure.title("获取&通知Autohold激活指示灯_AutHldSoftSwtEnaSts和LampReqByVehHld信号遍历")
    @pytest.mark.sanity
    def test_caseid_1987129(self):   
        hint = "Autohold Active Green"   
        self.set_Autohold_Active_Green_and_Standby_Grey(hint, Lamp=1)  
        last_value=1
        for aut in range(2):
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'AutHldSoftSwtEnaSts', aut) 
            for lamp in range(4):
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', random.choice([2, 11, 13])) # UsgMod信号
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'LampReqByVehHld', lamp) 
                value = 1 if aut == 1 and lamp == 1 else 0
                logger.info(f"打印当前返回值:aut={aut},lamp={lamp},last_value={last_value}, value={value}")
                if last_value == value:
                    self.partner.ck_wti_no_telltale_and_ck_resp(hint, value)
                else:
                    self.partner.ck_wti_telltale_and_resp(hint, value)
                last_value=value
        
    @allure.title("获取&通知Autohold激活指示灯_DoorDrvrSts信号遍历")
    @pytest.mark.sanity
    def test_caseid_1987139(self):   
        hint = "Autohold Active Green"     
        self.set_Autohold_Active_Green_and_Standby_Grey(hint, Lamp=1)  
        last_value=1
        for DoorSts in range(4):
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'DoorDrvrStsWithFacQlyDoorSts', DoorSts) # len=2
            for FacQly in range(4):
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', random.choice([2, 11, 13])) # UsgMod信号
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'DoorDrvrStsWithFacQlyFacQly', FacQly) # len=2
                value = 1 if  DoorSts == 2 and FacQly == 3 else 0
                if last_value == value:
                    self.partner.ck_wti_no_telltale_and_ck_resp(hint, value)
                else:
                    self.partner.ck_wti_telltale_and_resp(hint, value)
                last_value=value
 
    @allure.title("获取&通知Autohold激活指示灯_BltLockStAtDrvrBltLockSt1和UsgMod信号遍历")
    @pytest.mark.sanity
    def test_caseid_1987140(self):   
        hint = "Autohold Active Green"   
        self.set_Autohold_Active_Green_and_Standby_Grey(hint, Lamp=1)  
        last_value=1
        for UsgMod in [13, 11, 2, 1, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', UsgMod) # UsgMod信号
            for Blt in range(2):
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', Blt) # len=1 
                value = 1 if UsgMod in [2, 11, 13] and Blt == 1 else 0
                if last_value == value:
                    # self.partner.ck_wti_no_telltale_and_ck_resp(hint, value) #存在重复上报的情况
                    self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, 
                                                          {"out": [{"name": hint, "state": value}]})
                else:
                    self.partner.ck_wti_telltale_and_resp(hint, value)
                last_value=value

    @allure.title("获取&通知Autohold激活指示灯_GearLvrIndcn和SmartAutoHldCtrlSts信号遍历")
    @pytest.mark.smoke
    def test_caseid_1987141(self):   
        hint = "Autohold Active Green"   
        self.set_Autohold_Active_Green_and_Standby_Grey(hint, Lamp=1)  
        for Gear in range(8):
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', Gear) # 删除 GearLvrIndcn=2 or 3 , len=3             
            for Smart in range(2):
                self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr10, 'SmartAutoHldCtrlSts', Smart) # 删除 len=1 
                self.partner.ck_wti_no_telltale_and_ck_resp(hint, 1)

    @allure.title("获取&通知Autohold激活指示灯_AutHldSoftSwtEnaSts信号丢失")
    @pytest.mark.full
    def test_caseid_1987142(self):   
        hint = "Autohold Active Green"   
        self.set_Autohold_Active_Green_and_Standby_Grey(hint, Lamp=1)  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'AutHldSoftSwtEnaSts', 0) # len=1
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, 
                                              {"out": [{"name": hint, "state": "0"}]}, timeout=3)
        self.ipdu.stop_send_pdu('backbonefr', 3741504) # AutHldSoftSwtEnaSts
        self.partner.ck_wti_telltale_and_resp(hint, 1, timeout=3)
        self.partner.empty_all()
        self.ipdu.resume_bus_send("backbonefr") 
        self.partner.ck_wti_telltale_and_resp(hint, 0, timeout=3)

    @allure.title("获取&通知Autohold激活指示灯_SmartAutoHldCtrlSts信号丢失")
    @pytest.mark.full
    def test_caseid_1987143(self): # 删除 所以丢失无影响
        hint = "Autohold Active Green"   
        self.set_Autohold_Active_Green_and_Standby_Grey(hint, Lamp=1)  
        self.ipdu.stop_send_pdu('backbonefr', 2097928) # SmartAutoHldCtrlSts
        sleep(3)
        self.ipdu.resume_bus_send("backbonefr") 
        self.partner.ck_wti_no_telltale_and_ck_resp(hint, 1, timeout=3)    

    @allure.title("获取&通知Autohold激活指示灯_LampReqByVehHld信号丢失")
    @pytest.mark.full
    def test_caseid_1987144(self):   
        hint = "Autohold Active Green"   
        self.set_Autohold_Active_Green_and_Standby_Grey(hint, Lamp=1)          
        self.ipdu.stop_send_pdu('backbonefr', 3737376) # LampReqByVehHld
        self.partner.ck_wti_telltale_and_resp(hint, 0, timeout=2)
        self.ipdu.resume_bus_send("backbonefr") 
        self.partner.ck_wti_telltale_and_resp(hint, 1, timeout=3)       

    @allure.title("获取&通知Autohold激活指示灯_DoorDrvrStsWithFacQly信号组丢失")
    @pytest.mark.full
    def test_caseid_1987145(self): # DoorDrvrStsWithFacQlyDoorSts 和DoorDrvrStsWithFacQlyFacQly
        hint = "Autohold Active Green"   
        self.set_Autohold_Active_Green_and_Standby_Grey(hint, Lamp=1)          
        self.ipdu.stop_send_pdu('backbonefr', 524548) # DoorDrvrStsWithFacQly
        self.partner.ck_wti_telltale_and_resp(hint, 0, timeout=2)
        self.ipdu.resume_bus_send("backbonefr") 
        self.partner.ck_wti_telltale_and_resp(hint, 1, timeout=3)   

    @allure.title("获取&通知Autohold激活指示灯_BltLockStAtDrvrBltLockSt1信号丢失")
    @pytest.mark.full
    def test_caseid_1987146(self):   
        hint = "Autohold Active Green"   
        self.set_Autohold_Active_Green_and_Standby_Grey(hint, Lamp=1)     
        self.ipdu.stop_send_pdu('backbonefr', 1310721) # BltLockStAtDrvrBltLockSt1
        self.partner.ck_wti_telltale_and_resp(hint, 0, timeout=2)
        self.ipdu.resume_bus_send("backbonefr") 
        self.partner.ck_wti_telltale_and_resp(hint, 1, timeout=3)  
        
    @allure.title("获取&通知Autohold激活指示灯_UsgMod从0/1切换至2/11/13")
    @pytest.mark.sanity
    def test_caseid_1979887(self):  
        hint = "Autohold Active Green"  # AutHldSoftSwtEnaSts|LampReqByVehHld|GearLvrIndcn|BltLockStAtDrvrBltLockSt1|SmartAutoHldCtrlSts|Autohold Active Green|wti current mode|lastUM
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1) # UsgMod信号
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'DoorDrvrStsWithFacQlyDoorSts', 2) # len=2
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'DoorDrvrStsWithFacQlyFacQly', 3) # len=2
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 3) #  GearLvrIndcn=2 or 3 , len=3
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'AutHldSoftSwtEnaSts', 1) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'LampReqByVehHld', 1) # len=2        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', 1) # len=1   
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr10, 'SmartAutoHldCtrlSts', 0)
        sleep(3)
        for UsgMod1 in [0, 1]: 
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', UsgMod1) # UsgMod信号
            for UsgMod2 in [2, 11, 13]:  
                self.partner.empty_all(2)  
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', UsgMod2) # UsgMod信号
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
                self.partner.ck_wti_telltale_and_resp(hint, 1, timeout=1.5) # 1s后
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', UsgMod1) # UsgMod信号
                self.partner.ck_wti_telltale_and_resp(hint, 0)  #立即上报                          

    @allure.title("获取&通知Autohold激活指示灯_信号丢失")
    @pytest.mark.full
    def test_caseid_1979888(self):   
        hint = "Autohold Active Green"  # AutHldSoftSwtEnaSts|LampReqByVehHld|GearLvrIndcn|BltLockStAtDrvrBltLockSt1|SmartAutoHldCtrlSts|Autohold Active Green|wti current mode|lastUM
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1) # UsgMod信号
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'DoorDrvrStsWithFacQlyDoorSts', 2) # len=2
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'DoorDrvrStsWithFacQlyFacQly', 3) # len=2
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 2) #  GearLvrIndcn=2 or 3 , len=3
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'AutHldSoftSwtEnaSts', 1) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'LampReqByVehHld', 1) # len=2        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', 1) # len=1   
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr10, 'SmartAutoHldCtrlSts', 0)
        sleep(3)        
        for UsgMod in [0, 1, 2, 11, 13]:  
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', UsgMod) # UsgMod信号 
            self.partner.empty_all(2) 
            self.ipdu.pause_bus_send("backbonefr") 
            value = 1 if UsgMod in [2, 11, 13] else 0
            if UsgMod in [2, 11, 13]: 
                self.partner.ck_wti_telltale_and_resp(hint, 0, timeout=2) 
            else: 
                # self.ck_no_specific_event_and_GetTelltaleList(hint, 0) # 重复上报
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]}, timeout=2)
            self.ipdu.resume_bus_send("backbonefr")
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": str(value)}]}, timeout=3)

    @allure.title("获取&通知Autohold待命指示灯_UsgMod从0/1切换至2/11/13")
    @pytest.mark.sanity
    def test_caseid_1979891(self):  
        hint = "Autohold Standby Grey"  # AutHldSoftSwtEnaSts|LampReqByVehHld|GearLvrIndcn|BltLockStAtDrvrBltLockSt1|SmartAutoHldCtrlSts|Autohold Standby Grey|wti current mode|lastUM
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1) # UsgMod信号
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'DoorDrvrStsWithFacQlyDoorSts', 2) # len=2
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'DoorDrvrStsWithFacQlyFacQly', 3) # len=2
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 3) #  GearLvrIndcn=2 or 3 , len=3
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'AutHldSoftSwtEnaSts', 1) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'LampReqByVehHld', 0) # len=2        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', 1) # len=1  
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr10, 'SmartAutoHldCtrlSts', 0) 
        sleep(3)
        for UsgMod1 in [0, 1]: 
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', UsgMod1) # UsgMod信号
            for UsgMod2 in [2, 11, 13]:  
                self.partner.empty_all(2)  
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', UsgMod2) # UsgMod信号
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": "0"}]})
                self.partner.ck_wti_telltale_and_resp(hint, 1, timeout=1.5) # 1s后
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', UsgMod1) # UsgMod信号
                self.partner.ck_wti_telltale_and_resp(hint, 0)  #立即上报  
                
    @allure.title("获取&通知Autohold待命指示灯_信号丢失")
    @pytest.mark.full
    def test_caseid_1979892(self):   
        hint = "Autohold Standby Grey"  # AutHldSoftSwtEnaSts|LampReqByVehHld|GearLvrIndcn|BltLockStAtDrvrBltLockSt1|SmartAutoHldCtrlSts|Autohold Standby Grey|wti current mode|lastUM
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1) # UsgMod信号
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'DoorDrvrStsWithFacQlyDoorSts', 2) # len=2
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'DoorDrvrStsWithFacQlyFacQly', 3) # len=2
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 2) #  GearLvrIndcn=2 or 3 , len=3
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'AutHldSoftSwtEnaSts', 1) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'LampReqByVehHld', 0) # len=2        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', 1) # len=1   
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr10, 'SmartAutoHldCtrlSts', 0)
        sleep(3)        
        for UsgMod in [0, 1, 2, 11, 13]:  
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', UsgMod) # UsgMod信号
            self.partner.empty_all(2) 
            self.ipdu.pause_bus_send("backbonefr") 
            value = 1 if UsgMod in [2, 11, 13] else 0
            if UsgMod in [2, 11, 13]: 
                self.partner.ck_wti_telltale_and_resp(hint, 0, timeout=2) 
            else: 
                self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint, timeout=1)
            self.ipdu.resume_bus_send("backbonefr")
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out": [{"name": hint, "state": str(value)}]}, timeout=3)
        
    @allure.title("获取&通知Autohold待命指示灯_AutHldSoftSwtEnaSts和LampReqByVehHld信号遍历")
    @pytest.mark.sanity
    def test_caseid_1987147(self):   
        hint = "Autohold Standby Grey"   
        self.set_Autohold_Active_Green_and_Standby_Grey(hint, Lamp=0)  
        last_value=1
        for aut in range(2):
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'AutHldSoftSwtEnaSts', aut) 
            for lamp in range(4):
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', random.choice([2, 11, 13])) # UsgMod信号
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'LampReqByVehHld', lamp) 
                value = 1 if aut == 1 and lamp == 0 else 0
                logger.info(f"打印当前返回值:aut={aut},lamp={lamp},last_value={last_value}, value={value}")
                if last_value == value:
                    self.partner.ck_wti_no_telltale_and_ck_resp(hint, value)
                else:
                    self.partner.ck_wti_telltale_and_resp(hint, value)
                last_value=value
        
    @allure.title("获取&通知Autohold待命指示灯_DoorDrvrSts信号遍历")
    @pytest.mark.sanity
    def test_caseid_1987148(self):   
        hint = "Autohold Standby Grey"     
        self.set_Autohold_Active_Green_and_Standby_Grey(hint, Lamp=0)  
        last_value=1
        for DoorSts in range(4):
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'DoorDrvrStsWithFacQlyDoorSts', DoorSts) # len=2
            for FacQly in [0, 1, 3, 2]:
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', random.choice([2, 11, 13])) # UsgMod信号
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'DoorDrvrStsWithFacQlyFacQly', FacQly) # len=2
                value = 1 if  DoorSts == 2 and FacQly == 3 else 0
                if last_value == value:
                    self.partner.ck_wti_no_telltale_and_ck_resp(hint, value)
                else:
                    self.partner.ck_wti_telltale_and_resp(hint, value)
                last_value=value
 
    @allure.title("获取&通知Autohold待命指示灯_BltLockStAtDrvrBltLockSt1和UsgMod信号遍历")
    @pytest.mark.sanity
    def test_caseid_1987149(self):   
        hint = "Autohold Standby Grey"    
        self.set_Autohold_Active_Green_and_Standby_Grey(hint, Lamp=0)  
        last_value=1
        for UsgMod in [13, 11, 2, 1, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', UsgMod) # UsgMod信号
            for Blt in range(2):
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', Blt) # len=1 
                value = 1 if UsgMod in [2, 11, 13] and Blt == 1 else 0
                if last_value == value:
                    # self.partner.ck_wti_no_telltale_and_ck_resp(hint, value) #存在重复上报的情况
                    self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, 
                                                          {"out": [{"name": hint, "state": value}]})
                else:
                    self.partner.ck_wti_telltale_and_resp(hint, value)
                last_value=value

    @allure.title("获取&通知Autohold待命指示灯_GearLvrIndcn和SmartAutoHldCtrlSts信号遍历")
    @pytest.mark.smoke
    def test_caseid_1987150(self):   
        hint = "Autohold Standby Grey"      
        self.set_Autohold_Active_Green_and_Standby_Grey(hint, Lamp=0)  
        last_value=1
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', random.choice([2, 11, 13])) # UsgMod信号
        for Gear in range(8):
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', Gear) # 删除 GearLvrIndcn=2 or 3 , len=3             
            for Smart in range(2):
                self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr10, 'SmartAutoHldCtrlSts', Smart) # 删除 len=1 
                self.partner.ck_wti_no_telltale_and_ck_resp(hint, 1)

    @allure.title("获取&通知Autohold待命指示灯_LampReqByVehHld信号丢失")
    @pytest.mark.full
    def test_caseid_1987151(self):   
        hint = "Autohold Standby Grey"    
        self.set_Autohold_Active_Green_and_Standby_Grey(hint, Lamp=0)          
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'LampReqByVehHld', 1) # len=2 
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, 
                                              {"out": [{"name": hint, "state": "0"}]}, timeout=3)
        self.ipdu.stop_send_pdu('backbonefr', 3737376) # LampReqByVehHld
        self.partner.ck_wti_telltale_and_resp(hint, 1, timeout=3)
        self.partner.empty_all()
        self.ipdu.resume_bus_send("backbonefr") 
        self.partner.ck_wti_telltale_and_resp(hint, 0, timeout=3)

    @allure.title("获取&通知Autohold待命指示灯_SmartAutoHldCtrlSts信号丢失")
    @pytest.mark.full
    def test_caseid_1987152(self):   # 信号已删除，丢失应无影响
        hint = "Autohold Standby Grey"    
        self.set_Autohold_Active_Green_and_Standby_Grey(hint, Lamp=0)  
        self.ipdu.stop_send_pdu('backbonefr', 2097928) # SmartAutoHldCtrlSts
        sleep(3)
        self.ipdu.resume_bus_send("backbonefr") 
        self.partner.ck_wti_no_telltale_and_ck_resp(hint, 1, timeout=3)    

    @allure.title("获取&通知Autohold待命指示灯_AutHldSoftSwtEnaSts信号丢失")
    @pytest.mark.full
    def test_caseid_1987153(self):   
        hint = "Autohold Standby Grey"    
        self.set_Autohold_Active_Green_and_Standby_Grey(hint, Lamp=0)       
        self.ipdu.stop_send_pdu('backbonefr', 3741504) # AutHldSoftSwtEnaSts
        self.partner.ck_wti_telltale_and_resp(hint, 0, timeout=3)
        self.ipdu.resume_bus_send("backbonefr") 
        self.partner.ck_wti_telltale_and_resp(hint, 1, timeout=3)     

    @allure.title("获取&通知Autohold待命指示灯_DoorDrvrStsWithFacQly信号组丢失")
    @pytest.mark.full
    def test_caseid_1987154(self): # DoorDrvrStsWithFacQlyDoorSts 和DoorDrvrStsWithFacQlyFacQly
        hint = "Autohold Standby Grey"    
        self.set_Autohold_Active_Green_and_Standby_Grey(hint, Lamp=0)          
        self.ipdu.stop_send_pdu('backbonefr', 524548) # DoorDrvrStsWithFacQly
        self.partner.ck_wti_telltale_and_resp(hint, 0, timeout=2)
        self.ipdu.resume_bus_send("backbonefr") 
        self.partner.ck_wti_telltale_and_resp(hint, 1, timeout=3)   

    @allure.title("获取&通知Autohold待命指示灯_BltLockStAtDrvrBltLockSt1信号丢失")
    @pytest.mark.full    
    def test_caseid_1987155(self):   
        hint = "Autohold Standby Grey"    
        self.set_Autohold_Active_Green_and_Standby_Grey(hint, Lamp=0)     
        self.ipdu.stop_send_pdu('backbonefr', 1310721) # BltLockStAtDrvrBltLockSt1
        self.partner.ck_wti_telltale_and_resp(hint, 0, timeout=2)
        self.ipdu.resume_bus_send("backbonefr") 
        self.partner.ck_wti_telltale_and_resp(hint, 1, timeout=3)  
        
    @allure.title("换挡刹车释放提示_进入条件判断_制动踏板状态满足_UsgMod的validity=7")
    @pytest.mark.full
    def test_caseid_1988002(self): 
        hint = "Release Brake Reminder" 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 2) # UsgMod信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)        
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1) # 制动踏板未踩下
        self.partner.empty_all(150) 
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts')
            self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetUsageModeValidity", {},
                                                  {"out": {"value": 2, "validity": 7}}, timeout=3)
            sleep(1)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 1) 
            self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)                
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts')
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)
        
    @allure.title("换挡刹车释放提示_退出条件判断_100ms内UsgMod切1后再次切2_无响应")
    @pytest.mark.full
    def test_caseid_1988862(self): 
        hint = "Release Brake Reminder"    
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 2) # UsgMod信号        
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1) # 制动踏板未踩下
        self.partner.empty_all(150) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 3)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 2)
        for UsgMod in [1, 2]: 
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', UsgMod)
            sleep(0.03)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.1) # 100ms置位    
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0) 

    def set_Brake_Overide_Accelerator(self, gear=random.choice([1, 3]), speed=0, brk=1, acc=10.0, status=random.choice([0, 3, 4, 5]), info=1):
        '''制动优先BOA'''
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', random.choice([11, 13])) # UsgMod信号 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', random.choice([0, 1]))
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear) # gear
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3) # 车速有效
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', speed) # DisplaySpeedChanged
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', brk) # 制动踏板
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', acc) # 加速踏板
        dict={0:1, 1:2, 2:3, 3:4, 4:0, 5:5} # status:信号值
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  dict[status]) # LaunchMode.info.status
        sleep(3)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": "Brake Overide Accelerator", "info": str(info)}]}, timeout=5)
        self.partner.empty_all() 
                
    @allure.title("制动优先BOA_进入条件判断_其他条件满足_车速单位遍历")
    @pytest.mark.full
    def test_caseid_1988946(self): 
        hint = "Brake Overide Accelerator" 
        self.ipdu.set(self.ipdu.backbonefr.DimBackBoneFr04, 'VehSpdIndcdVeSpdIndcdUnit', 1) # 车速单位不等于Kmph
        self.set_Brake_Overide_Accelerator(info=0)        
        for i in [2, 1, 0]:
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
            self.ipdu.set(self.ipdu.backbonefr.DimBackBoneFr04, 'VehSpdIndcdVeSpdIndcdUnit', i) # 车速单位
            if i == 0:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=1)
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
                self.partner.ck_wti_no_warning_and_ck_resp(hint, 1, timeout=3.7)
                self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.5) # 4s置位
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)          

    @allure.title("制动优先BOA_进入条件判断_其他条件满足_加速踏板validity=4")
    @pytest.mark.full
    def test_caseid_1988025(self): 
        hint = "Brake Overide Accelerator" 
        self.ipdu.set(self.ipdu.backbonefr.DimBackBoneFr04, 'VehSpdIndcdVeSpdIndcdUnit', 0)
        self.set_Brake_Overide_Accelerator(brk=0, info=0) 
        self.ipdu.stop_send_pdu('propulsioncan', 0x04A) # 仅加速踏板信号丢失 
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [0]},
                                              {"out": [{"id": 0, "statusValidity": 4}]}, timeout=5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1) # 制动踏板
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)
        self.ipdu.resume_bus_send("propulsioncan")
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]}, timeout=2.5)    