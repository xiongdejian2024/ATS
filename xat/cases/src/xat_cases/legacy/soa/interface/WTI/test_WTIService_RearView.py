
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_WTIService.py
@Time         :2023/04/08 17:20:31
@Author       :jiabin.zhu@jiduauto.com
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
NFC_UWB_Key_Legacy_On_Passenger_Reminder = __import__("os").environ.get('XAT_CREDENTIAL____SOA_INTERFACE_WTI_TEST_WTISERVICE_REARVIEW_PY_NFC_UWB_KEY_LEGACY_ON_PASSENGER_REMINDER', "")

@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIService_RearView")
@pytest.mark.aqx
class TestRearViewWTIService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("WTIService", "client"),
                                     ("LightService", "client"),
                                     ("WiperService", "client"),
                                     ("AutoHighBeamControlService", "server"),
                                     ("ChassisService", "client"),
                                     ("ClimateControlService", "client"),
                                     ("PedalService", "client"),
                                     ("VehicleModeService", "client")
                                     ])
        self.partner.method_default_timeout = 0.1
        self.ipdu.send_pdu('chassiscan1', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('chassiscan2', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('propulsioncan', 0x516, [0x16, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)

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
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr29, 'DCChrgnHndlSts', 'OnBdChrgrHndlSts_ConnectedWithPower') # lin唤醒
        self.ipdu.set(self.ipdu.connectivitycanfd.TcamConnectivityFr12, 'RemHvStrtActvReq', 'OnOffNoReq_On')
        self.ipdu.set(self.ipdu.connectivitycanfd.TcamConnectivityFr12, 'RemDCChrgLidTelmReq', 'OnOffNoReq_On')
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.sd_tester.stop_tester_present()
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
        """校验无指定warningMsgList事件，并请求WarningMsgList获取结果"""
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "TelltaleList", hint, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": hint, "state": str(state)}]})

    def ck_TelltaleList_and_GetTelltaleList(self, hint, state, timeout=3):
        """校验指定TelltaleList事件，并请求TelltaleList获取结果"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                  {"list": [{"name": hint, "state": str(state)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": hint, "state": str(state)}]})
      
    @allure.title("获取&通知主驾后视镜展开回收故障_取值遍历")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1764359?projectId=46')
    @pytest.mark.sanity
    def test_caseid_107399(self):
        hint = "Driver Mirror Fold Error"
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, 'DrvrMirrorFoldErrorFb', 0)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, 'DrvrMirrorFoldErrorFb', 1)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, 'DrvrMirrorFoldErrorFb', 0)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)
          
    @allure.title("获取&通知副驾后视镜展开回收故障_取值遍历")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1764940?projectId=46')
    @pytest.mark.sanity
    def test_caseid_107658(self):
        hint = "Passenger Mirror Fold Error"
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'PassMirrorFoldErrorFb', 0)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'PassMirrorFoldErrorFb', 1)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'PassMirrorFoldErrorFb', 0)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @allure.title("获取&通知主驾后视镜镜面调节故障_取值遍历")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1764363?projectId=46')
    @pytest.mark.sanity
    def test_caseid_107411(self):
        hint = "Driver Mirror Adjustment Error"
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, 'DrvrMirrorAdjErrorFb', 0)
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, 'DrvrMirrorAdjErrorFb', 1)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, 'DrvrMirrorAdjErrorFb', 0)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @allure.title("获取&通知副驾后视镜镜面调节故障_取值遍历")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1763995?projectId=46')
    @pytest.mark.sanity
    def test_caseid_107642(self):
        hint = "Passenger Mirror Adjustment Error "
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'PassMirrorAdjErrorFb', 0)
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'PassMirrorAdjErrorFb', 1)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'PassMirrorAdjErrorFb', 0)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)