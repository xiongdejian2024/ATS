
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_WTIService.py
@Time         :2023/10/26 17:20:31
@Author       :peipei.yang_ext@jiduauto.com
@Description  :
"""
import os
import sys

from xat_ecu.legacy.sdk.sdk_tools import check_pdu, get_pdu_value_and_time
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.soa.case_helper.utils import ck_pdu_period_time


@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIService_Wiper")
@pytest.mark.wtiwiper
class TestWiperWTIService(TestBase):
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
                                     ("VehicleModeService", "client"),
                                     ("InterCommService", "client", "BGM_InterCommService")
                                     ])
        self.partner.method_default_timeout = 0.1
        self.ipdu.send_pdu('chassiscan1', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('chassiscan2', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('propulsioncan', 0x516, [0x16, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
    
        self.coolant2 = 'Coolant2'

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 0)
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
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 3)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 0)
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        # self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.ipdu.set_vehspd(0)
        sleep(0.5)
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 0)
        self.sd_tester.stop_tester_present()
        self.ipdu.resume_all_bus_send()  # 恢复所有总线
        super().after_each_func(ecu, start=False)

    def ck_no_specific_event_and_GetWarningMsgList(self, hint, info, timeout=1):
        """校验无指定warningMsgList事件,并请求WarningMsgList获取结果"""
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})

    def ck_WarningMsgList_and_GetWarningMsgList(self, hint, info, timeout=3):
        """校验指定warningMsgList事件,并请求WarningMsgList获取结果"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint, "info": str(info)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})

    def ck_no_specific_event_and_GetTelltaleList(self, hint, state, timeout=1):
        """校验无指定warningMsgList事件,并请求WarningMsgList获取结果"""
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "TelltaleList", hint, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": hint, "state": str(state)}]})

    def ck_TelltaleList_and_GetTelltaleList(self, hint, state, timeout=3):
        """校验指定TelltaleList事件,并请求TelltaleList获取结果"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                  {"list": [{"name": hint, "state": str(state)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": hint, "state": str(state)}]})
    def set_wiper_switch_use_prompt(self, by, status, recovery):
        """
        触发雨刮开关使用提示的条件及恢复方式
        by (str):按键steer或拨杆lever
        status (int): 雨刮开关切换到的状态1或2
        recovery (str): 提示消失的方式，未处于维修模式maintaince_off或者超时恢复timeout
        """
        hint = "Wiper Switch Use Prompt"
        self.partner.send_method_request("WiperService_client", "SetWiperMaintainceMode", {'on': True})  
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        self.partner.send_request_and_ck_resp("WiperService_client", "GetWiperMaintainceMode", {}, {"out": True}, timeout=3) 
        self.partner.send_request_and_ck_resp("WiperService_client", "GetSwitchStatus", {"wipers": 0}, {"out": 0}, timeout=2)
        
        if by == "steer":
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', status)
        elif by == "lever":
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 0)
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', status)
            
        # 检查有提示
        self.partner.send_request_and_ck_resp("WiperService_client", "GetSwitchStatus", {"wipers": 0}, {"out": status}, timeout=2)
        self.partner.ck_event_and_resp(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]})
        
        if recovery == 'maintaince_off':
            # 设置雨刮退出维修，检查无提示
            self.partner.send_method_request("WiperService_client", "SetWiperMaintainceMode", {'on': False})  
            self.partner.ck_coming_event_and_resp(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '0'}]}, timeout=1, deviation=0.5)
        elif recovery == 'timeout':
            # 超时后无提示
            self.partner.ck_coming_event_and_resp(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '0'}]}, timeout=4, deviation=0.5)
    
    @allure.title("雨刮开关使用提示_按键状态从0到1退出维修后无提示_按键状态从0到1超时后无提示")
    @pytest.mark.full
    def test_caseid_1989611(self):
        self.sd_tester.change_car_mode(0)  
        self.sd_tester.change_usage_mode(11)

        self.set_wiper_switch_use_prompt("steer", 1, "maintaince_off")
        # 开关状态为0
        sleep(5)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 0)
        self.partner.empty_all(2)
        self.set_wiper_switch_use_prompt("steer", 1, "timeout")

    @allure.title("雨刮开关使用提示_拨杆状态从0到1退出维修后无提示_拨杆状态从0到1超时后无提示")
    @pytest.mark.full
    def test_caseid_1989612(self):
        self.sd_tester.change_car_mode(0)  
        self.sd_tester.change_usage_mode(11)

        self.set_wiper_switch_use_prompt("lever", 1, "maintaince_off")
        # 开关状态为0
        sleep(5)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 0)
        self.partner.empty_all(2)
        self.set_wiper_switch_use_prompt("lever", 1, "timeout")

    @allure.title("雨刮开关使用提示_拨杆状态从0到2退出维修后无提示_拨杆状态从0到2超时后无提示")
    @pytest.mark.full
    def test_caseid_1989613(self):
        self.set_wiper_switch_use_prompt("lever", 2, "maintaince_off")
        # 开关状态为0
        sleep(5)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 0)
        self.partner.empty_all(2)
        self.set_wiper_switch_use_prompt("lever", 2, "timeout")
        
    @allure.title("雨刮开关使用提示_按键状态从0到2退出维修后无提示_按键状态从0到2超时后无提示")
    @pytest.mark.full
    def test_caseid_1989614(self):
        self.set_wiper_switch_use_prompt("steer", 2, "maintaince_off")
        # 开关状态为0
        sleep(5)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 0)
        self.partner.empty_all(2)
        self.set_wiper_switch_use_prompt("steer", 2, "timeout")

    @allure.title("雨刮开关使用提示_处于维修短按有提示_未处于维修无提示")
    @pytest.mark.smoke
    def test_caseid_1943263(self):
        hint = "Wiper Switch Use Prompt"
        self.sd_tester.change_car_mode(0)  # 0|5#2
        self.sd_tester.change_usage_mode(11)
        self.partner.send_method_request("WiperService_client", "SetWiperMaintainceMode", {'on': True})  # 设置雨刮维修模式
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        self.partner.send_request_and_ck_resp("WiperService_client", "GetWiperMaintainceMode", {}, {"out": True}, timeout=3)  
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1)
        sleep(0.5)
        self.partner.send_request_and_ck_resp("WiperService_client", "GetSwitchStatus", {"wipers": 0}, {"out": 1})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": "Wiper Switch Use Prompt", "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": "Wiper Switch Use Prompt", "info": '1'}]})

        sleep(2)        
        self.partner.send_method_request("WiperService_client", "SetWiperMaintainceMode", {'on': False})  
        self.partner.ck_coming_event_and_resp(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '0'}]}, timeout=1, deviation=0.5)

    @allure.title("雨刮开关使用提示_处于维修短按有提示_超时无提示")
    @pytest.mark.sanity
    def test_caseid_1943269(self):
        hint = "Wiper Switch Use Prompt"
        self.sd_tester.change_car_mode(0)  # 0|5#2
        self.sd_tester.change_usage_mode(11)
        self.partner.send_method_request("WiperService_client", "SetWiperMaintainceMode", {'on': True})  # 设置雨刮维修模式
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        self.partner.send_request_and_ck_resp("WiperService_client", "GetWiperMaintainceMode", {}, {"out": True}, timeout=3) 
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1)
        sleep(0.1)
        self.partner.send_request_and_ck_resp("WiperService_client", "GetSwitchStatus", {"wipers": 0}, {"out": 1})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": "Wiper Switch Use Prompt", "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": "Wiper Switch Use Prompt", "info": '1'}]})
        # 超时无提示
        self.partner.ck_coming_event_and_resp(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '0'}]}, timeout=4, deviation=0.5)

    @allure.title("雨刮开关使用提示_处于维修长按有提示_未处于维修无提示")
    @pytest.mark.sanity
    def test_caseid_1979758(self):
        hint = "Wiper Switch Use Prompt"
        self.partner.send_method_request("WiperService_client", "SetWiperMaintainceMode", {'on': True})  # 设置雨刮维修模式
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        self.partner.send_request_and_ck_resp("WiperService_client", "GetWiperMaintainceMode", {}, {"out": True}, timeout=3)  
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 2)
        sleep(0.5)
        self.partner.send_request_and_ck_resp("WiperService_client", "GetSwitchStatus", {"wipers": 0}, {"out": 2})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": "Wiper Switch Use Prompt", "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": "Wiper Switch Use Prompt", "info": '1'}]})

        sleep(2)        
        self.partner.send_method_request("WiperService_client", "SetWiperMaintainceMode", {'on': False})  
        self.partner.ck_coming_event_and_resp(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '0'}]}, timeout=1, deviation=0.5)

    @allure.title("雨刮开关使用提示_处于维修长按有提示_超时无提示")
    @pytest.mark.sanity
    def test_caseid_1989635(self):
        hint = "Wiper Switch Use Prompt"
        self.partner.send_method_request("WiperService_client", "SetWiperMaintainceMode", {'on': True})  # 设置雨刮维修模式
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        self.partner.send_request_and_ck_resp("WiperService_client", "GetWiperMaintainceMode", {}, {"out": True}, timeout=3) 
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 2)
        sleep(0.1)
        self.partner.send_request_and_ck_resp("WiperService_client", "GetSwitchStatus", {"wipers": 0}, {"out": 2})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": "Wiper Switch Use Prompt", "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": "Wiper Switch Use Prompt", "info": '1'}]})
        # 超时无提示
        self.partner.ck_coming_event_and_resp(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '0'}]}, timeout=4, deviation=0.5)
        
    @allure.title("雨刮开关使用有提示_开关从1到0不满足退出仍有提示_超时无提示")
    @pytest.mark.full
    def test_caseid_1979756(self):
        hint = "Wiper Switch Use Prompt"
        self.sd_tester.change_car_mode(0)  # 0|5#2
        self.sd_tester.change_usage_mode(11)
        self.partner.send_method_request("WiperService_client", "SetWiperMaintainceMode", {'on': True})  # 设置雨刮维修模式
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        self.partner.send_request_and_ck_resp("WiperService_client", "GetWiperMaintainceMode", {}, {"out": True}, timeout=3)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1)
        sleep(0.3)
        # 信号从0到1有提示
        self.partner.send_request_and_ck_resp("WiperService_client", "GetSwitchStatus", {"wipers": 0}, {"out": 1})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": "Wiper Switch Use Prompt", "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": "Wiper Switch Use Prompt", "info": '1'}]})
        
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})
        # 信号从1到0不满足退出条件，仍有提示
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        sleep(2)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": "Wiper Switch Use Prompt", "info": '1'}]})
        # 超时无提示
        self.partner.ck_coming_event_and_resp(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '0'}]}, timeout=2, deviation=0.5)
        
    @allure.title("雨刮开关使用有提示_开关故障不满足退出仍有提示_超时无提示")
    @pytest.mark.full
    def test_caseid_1979757(self):
        hint = "Wiper Switch Use Prompt"
        self.sd_tester.change_car_mode(0)  # 0|5#2
        self.sd_tester.change_usage_mode(11)
        self.partner.send_method_request("WiperService_client", "SetWiperMaintainceMode", {'on': True})  # 设置雨刮维修模式
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        self.partner.send_request_and_ck_resp("WiperService_client", "GetWiperMaintainceMode", {}, {"out": True}, timeout=3)  # 雨刮处于维修位置
        self.partner.empty_all(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1)
        sleep(0.3)
        # 信号从0到1有提示
        self.partner.send_request_and_ck_resp("WiperService_client", "GetSwitchStatus", {"wipers": 0}, {"out": 1})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": "Wiper Switch Use Prompt", "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": "Wiper Switch Use Prompt", "info": '1'}]})
        
        # 开关信号故障，仍有提示
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 3)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 3)
        self.partner.send_request_and_ck_resp("WiperService_client", "GetSwitchStatus", {"wipers": 0}, {"out": 3})
        sleep(2)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": "Wiper Switch Use Prompt", "info": '1'}]})
        
        # 超时无提示
        self.partner.ck_coming_event_and_resp(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '0'}]}, timeout=2, deviation=0.5)

    @allure.title("雨刮开关使用有提示_开关从0到1重置计时器")
    @pytest.mark.full
    def test_caseid_1989636(self):
        hint = "Wiper Switch Use Prompt"
        self.sd_tester.change_car_mode(0)  # 0|5#2
        self.sd_tester.change_usage_mode(11)
        self.partner.send_method_request("WiperService_client", "SetWiperMaintainceMode", {'on': True})  # 设置雨刮维修模式
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        self.partner.send_request_and_ck_resp("WiperService_client", "GetWiperMaintainceMode", {}, {"out": True}, timeout=3)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1)
        sleep(0.2)
        # 信号从0到1有提示
        self.partner.send_request_and_ck_resp("WiperService_client", "GetSwitchStatus", {"wipers": 0}, {"out": 1})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": '1'}]})
        sleep(2)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})
        
        # 信号从0到1，重置计时器，仍然需要4秒超时后提示消失
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1)
        sleep(0.1)
        self.partner.send_request_and_ck_resp("WiperService_client", "GetSwitchStatus", {"wipers": 0}, {"out": 1})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": '1'}]})
        self.partner.ck_coming_event_and_resp(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '0'}]}, timeout=4, deviation=0.5)

    @allure.title("雨刮开关使用有提示_开关从0到2重置计时器")
    @pytest.mark.full
    def test_caseid_1989637(self):
        hint = "Wiper Switch Use Prompt"
        self.partner.send_method_request("WiperService_client", "SetWiperMaintainceMode", {'on': True})  # 设置雨刮维修模式
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        self.partner.send_request_and_ck_resp("WiperService_client", "GetWiperMaintainceMode", {}, {"out": True}, timeout=3)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 2)
        sleep(0.2)
        # 信号从0到2有提示
        self.partner.send_request_and_ck_resp("WiperService_client", "GetSwitchStatus", {"wipers": 0}, {"out": 2})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": '1'}]})
        sleep(2)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit", {"wipers": 0, "isOn": True})

        # 信号从0到2，重置计时器，仍然需要4秒超时后提示消失
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 2)
        sleep(0.1)
        self.partner.send_request_and_ck_resp("WiperService_client", "GetSwitchStatus", {"wipers": 0}, {"out": 2})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": hint, "info": '1'}]})
        self.partner.ck_coming_event_and_resp(WTI_SERVICE_CLIENT, "WarningMsgList", {"list": [{"name": hint, "info": '0'}]}, timeout=4, deviation=0.5)
        
    @allure.title("雨刮开关使用提示_前提不满足无提示")
    @pytest.mark.full
    def test_caseid_1989638(self):
        self.sd_tester.change_car_mode(0)  # 0|5#2
        self.sd_tester.change_usage_mode(11)
        self.partner.send_method_request("WiperService_client", "SetWiperMaintainceMode", {'on': False})  # 设置雨刮退出维修
        self.partner.send_request_and_ck_resp("WiperService_client", "GetWiperMaintainceMode", {}, {"out": False}, timeout=3)  
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1)
        sleep(0.5)
        self.partner.send_request_and_ck_resp("WiperService_client", "GetSwitchStatus", {"wipers": 0}, {"out": 1})
        sleep(1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": "Wiper Switch Use Prompt", "info": '0'}]})

    @allure.title("雨刮开关使用提示_触发不满足无提示")
    @pytest.mark.full
    def test_caseid_1989639(self):
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1)
        self.partner.empty_all(1) 
        self.partner.send_method_request("WiperService_client", "SetWiperMaintainceMode", {'on': True})  # 设置雨刮维修模式
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        self.partner.send_request_and_ck_resp("WiperService_client", "GetWiperMaintainceMode", {}, {"out": True}, timeout=3)  
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 2)
        sleep(0.5)
        self.partner.send_request_and_ck_resp("WiperService_client", "GetSwitchStatus", {"wipers": 0}, {"out": 2})
        sleep(1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out": [{"name": "Wiper Switch Use Prompt", "info": '0'}]})

    @allure.title("液位信息1(MsgCoolantDriveSys)")
    @pytest.mark.sanity
    def test_caseid_107389(self):
        hint = "Coolant1"
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr09, 'EmotCooltIndcnReq', 1)
        sleep(1)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr09, 'EmotCooltIndcnReq', 0)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @allure.title("液位信息2BattCooltIndcnReq为1_持续60秒")
    @pytest.mark.sanity
    def test_caseid_1988995(self):
        # 前提没有提示信息
        msg = self.partner.send_request_and_return_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {})['out']
        info = int([i for i in msg if i['name'] == self.coolant2][0]['info'])
        if info == 1:
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 0)
            self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
            
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 1)
        sleep(30)
        self.partner.ck_wti_no_warning_and_ck_resp(self.coolant2, 0)
        sleep(30)
        self.partner.ck_wti_warning_and_resp(self.coolant2, 1)

    @allure.title("液位信息2BattCooltIndcnReq为0_持续60秒")
    @pytest.mark.sanity
    def test_caseid_1988996(self):
        # 前提已有提示信息
        msg = self.partner.send_request_and_return_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {})['out']
        info = int([i for i in msg if i['name'] == self.coolant2][0]['info'])
        if info == 0:      
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 1)
            sleep(60)
            self.partner.ck_wti_warning_and_resp(self.coolant2, 1)

        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 0)
        sleep(30)
        self.partner.ck_wti_no_warning_and_ck_resp(self.coolant2, 1)        
        sleep(30)
        self.partner.ck_wti_warning_and_resp(self.coolant2, 0)

    @allure.title("液位信息2BattCooltIndcnReq为1_60秒内打断")
    @pytest.mark.full
    def test_caseid_1988997(self):
        # 前提没有提示信息
        msg = self.partner.send_request_and_return_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {})['out']
        info = int([i for i in msg if i['name'] == self.coolant2][0]['info'])
        if info == 1:
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 0)
            self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
            
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 1)
        sleep(30)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 0)
        sleep(0.1)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 1)
        self.partner.ck_wti_no_warning_and_ck_resp(self.coolant2, 0)
        sleep(30)
        self.partner.ck_wti_no_warning_and_ck_resp(self.coolant2, 0)
        sleep(30)
        self.partner.ck_wti_warning_and_resp(self.coolant2, 1)

    @allure.title("液位信息2BattCooltIndcnReq为0_60秒内打断")
    @pytest.mark.full
    def test_caseid_1988998(self):
        # 前提已有提示信息
        msg = self.partner.send_request_and_return_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {})['out']
        info = int([i for i in msg if i['name'] == self.coolant2][0]['info'])
        if info == 0:    
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 1)
            sleep(60)
            self.partner.ck_wti_warning_and_resp(self.coolant2, 1)
            
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 0)
        sleep(30)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 1)
        sleep(0.1)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 0)
        self.partner.ck_wti_no_warning_and_ck_resp(self.coolant2, 1)
        sleep(30)
        self.partner.ck_wti_no_warning_and_ck_resp(self.coolant2, 1)
        sleep(30)
        self.partner.ck_wti_warning_and_resp(self.coolant2, 0)

    @allure.title("液位信息2BattCooltIndcnReq值改变")
    @pytest.mark.full
    def test_caseid_1988999(self):    
        # 前提没有提示信息
        msg = self.partner.send_request_and_return_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {})['out']
        info = int([i for i in msg if i['name'] == self.coolant2][0]['info'])
        if info == 1:
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 0)
            self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
                    
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 1)
        self.partner.ck_wti_no_warning_and_ck_resp(self.coolant2, 0)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 0)
        self.partner.ck_wti_no_warning_and_ck_resp(self.coolant2, 0)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 1)
        self.partner.ck_wti_no_warning_and_ck_resp(self.coolant2, 0)
        
    @allure.title("液位信息2BattCooltIndcnReq为1_重启场景")
    @pytest.mark.full
    def test_caseid_1989000(self):    
        # 前提没有提示信息
        msg = self.partner.send_request_and_return_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {})['out']
        info = int([i for i in msg if i['name'] == self.coolant2][0]['info'])
        if info == 1:
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 0)
            self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
                    
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 1)
        sleep(30)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)        
        sleep(30)
        self.partner.ck_wti_no_warning_and_ck_resp(self.coolant2, 0)
        sleep(30)
        self.partner.ck_wti_warning_and_resp(self.coolant2, 1)

    @allure.title("获取气格栅异常&通知进气格栅异常_故障产生到恢复")
    @pytest.mark.sanity
    def test_caseid_1919376(self):
        hint = "Air Grille Abnormal"
        for usage_mode in [2, 11, 13]:
            logger.info(f"设置模式---{usage_mode}")
            self.sd_tester.change_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr29, 'GrlShttrStsShttrBlkd', 0)
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr29, 'GrlShttrStsShttrBlkd', 1)
            sleep(64)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": "Air Grille Abnormal", "info": '0'}]})
            sleep(106)
            self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr29, 'GrlShttrStsShttrBlkd', 0)
            sleep(1)
            self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @allure.title("获取进气格栅异常&通知进气格栅异常_模式不不满足停止计时不上报")
    @pytest.mark.full
    def test_caseid_1943381(self):
        hint = "Air Grille Abnormal"
        for usage_mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr29, 'GrlShttrStsShttrBlkd', 0)
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr29, 'GrlShttrStsShttrBlkd', 1)
            sleep(50)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": "Air Grille Abnormal", "info": '0'}]})
            sleep(110)
            self.sd_tester.change_usage_mode(0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": "Air Grille Abnormal", "info": '0'}]})
            self.sd_tester.change_usage_mode(1)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": "Air Grille Abnormal", "info": '0'}]})
    
    @allure.title("获取进气格栅异常&通知进气格栅异常_故障产生到恢复_信号不满足")
    @pytest.mark.full
    def test_caseid_1943382(self):
        hint = "Air Grille Abnormal"
        for usage_mode in [2, 11, 13]:
            logger.info(f"设置模式---{usage_mode}")
            self.sd_tester.change_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr29, 'GrlShttrStsShttrBlkd', 0)
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr29, 'GrlShttrStsShttrBlkd', 1)
            sleep(106)
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr29, 'GrlShttrStsShttrBlkd', 0)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": "Air Grille Abnormal", "info": '0'}]})
            sleep(60)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": "Air Grille Abnormal", "info": '0'}]})
    
    @allure.title("获取进气格栅异常&通知进气格栅异常_模式切换场景")
    @pytest.mark.sanity
    def test_caseid_1984322(self):
        hint = "Air Grille Abnormal"
        self.sd_tester.change_usage_mode(0)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr29, 'GrlShttrStsShttrBlkd', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr29, 'GrlShttrStsShttrBlkd', 1)
        sleep(20)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{"name": "Air Grille Abnormal", "info": '0'}]})
        self.sd_tester.change_usage_mode(2)
        sleep(150)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{"name": "Air Grille Abnormal", "info": '0'}]})
        sleep(20)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        self.sd_tester.change_usage_mode(1)
        sleep(1)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)
        self.sd_tester.change_usage_mode(11)
        sleep(170)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        sleep(1)
        self.sd_tester.change_usage_mode(0)
        self.sd_tester.change_usage_mode(13)
        sleep(170)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr29, 'GrlShttrStsShttrBlkd', 0)
            

@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIService_Wiper")
@pytest.mark.wtiwipermock
class TestWiperWTIServiceMockMcu(TestBase):

    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([WTI_SERVICE_CLIENT, WIPER_SERVICE_CLIENT])
        self.wti_wiperliquid = "Wiper Liquid"
        
    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.ipdu.set_vehspd(0)
        sleep(0.5)
        self.partner.empty_all(1)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def set_usage_mode(self, mode):
        """通过模拟mcu cdd打包总线数据来输入usage mode给到S2S"""
        logger.info(f"设置usage mode: {mode}")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', mode)
    
    def ck_no_specific_event_and_GetWarningMsgList(self, hint, info, timeout=1):
        """校验无指定warningMsgList事件,并请求WarningMsgList获取结果"""
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})

    def ck_WarningMsgList_and_GetWarningMsgList(self, hint, info, timeout=3):
        """校验指定warningMsgList事件,并请求WarningMsgList获取结果"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint, "info": str(info)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})

    @allure.title("雨刮系统故障信息(MsgWiperSysFailure)")
    @pytest.mark.smoke
    def test_caseid_108527(self):
        hint = "Wiper System Failure"
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WiprSysFailrDetdSafe', 0)
        self.partner.empty_all(0.5)
        for safe in [2, 1, 2, 3, 2, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WiprSysFailrDetdSafe', safe)
            if safe in [2]:
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
            else :
                self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)
    

    @allure.title("雨刮退出维修位置提醒_检查WarningMsgList")
    @pytest.mark.sanity
    def test_caseid_1987995(self):
        hint = "Wiper Exit Repair Position"
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 0)
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "MaintainceMode", {"on": 0})

        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        self.partner.ck_wti_warning_and_resp(hint, 0)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "MaintainceMode", {"on": 1})

    @allure.title("雨刮退出维修位置提醒_雨刮维修模式关闭")
    @pytest.mark.full
    def test_caseid_1987996(self):
        hint = "Wiper Exit Repair Position"
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMaintainceMode", {'on': False})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=1)
        self.bgm_eth_inter.ck_signal_values("WiprFrntSrvModReq", [2, 2, 2, 0])
        
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        self.partner.empty_all(0.2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 0)
        self.partner.ck_wti_warning_and_resp(hint, 1)

        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        self.partner.ck_wti_warning_and_resp(hint, 0)

    @allure.title("雨刮退出维修位置提醒_设置WiprInPosnForSrv为1_雨刮维修模式关闭")
    @pytest.mark.full
    def test_caseid_1987997(self):
        hint = "Wiper Exit Repair Position"
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMaintainceMode", {'on': False})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=1)
        self.bgm_eth_inter.ck_signal_values("WiprFrntSrvModReq", [2, 2, 2, 0])
        
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 0)
        sleep(0.2)
        self.partner.ck_wti_warning_and_resp(hint, 1)

    @allure.title("雨刮退出维修位置提醒_设置WiprInPosnForSrv为0_雨刮维修模式开启")
    @pytest.mark.full
    def test_caseid_1987998(self):
        hint = "Wiper Exit Repair Position"
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 0)
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMaintainceMode", {'on': True})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=1)
        self.bgm_eth_inter.ck_signal_values("WiprFrntSrvModReq", [1, 1, 1, 0])

        self.partner.empty_all()
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        sleep(0.2)
        self.partner.ck_wti_warning_and_resp(hint, 0)

    @allure.title("雨刮退出维修位置提醒_与雨刮系统故障信息、雨量传感器故障信息组合测试")
    @pytest.mark.full
    def test_caseid_1987999(self):
        repair_hint = "Wiper Exit Repair Position"
        sensor_hint = "Wiper Sensor Failure"
        system_hint = "Wiper System Failure"
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'RainSnsrActvnErrToHmi', 1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WiprSysFailrDetdSafe', 2)
        
        self.partner.ck_wti_warning_and_resp(repair_hint, 1)
        self.partner.ck_wti_warning_and_resp(sensor_hint, 1)
        self.partner.ck_wti_warning_and_resp(system_hint, 1)

        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'RainSnsrActvnErrToHmi', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WiprSysFailrDetdSafe', 0)
        
        self.partner.ck_wti_warning_and_resp(repair_hint, 0)
        self.partner.ck_wti_warning_and_resp(sensor_hint, 0)
        self.partner.ck_wti_warning_and_resp(system_hint, 0)

    @allure.title("雨刮退出维修位置提醒_与洗涤液不足、舱外光亮度原始数据传感器故障、雨刮开关/按键故障组合测试")
    @pytest.mark.full
    def test_caseid_1988000(self):
        hint = "Wiper Exit Repair Position"
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'RainSnsrActvnErrToHmi', 1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 3)
        
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault", {"faults": 
                                [{"fault":1, "faultMsg":"", "wiper":0}, 
                                 {"fault":2, "faultMsg":"", "wiper":0}, 
                                 {"fault":5, "faultMsg":"", "wiper":0}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": 
                                [{"fault":1, "faultMsg":"", "wiper":0}, 
                                 {"fault":2, "faultMsg":"", "wiper":0}, 
                                 {"fault":5, "faultMsg":"", "wiper":0}]})

        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'RainSnsrActvnErrToHmi', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 2)
        
        self.partner.ck_wti_warning_and_resp(hint, 0)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault", {"faults": 
                                [{"fault":0, "faultMsg":"OK", "wiper":2}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": 
                                [{"fault":0, "faultMsg":"OK", "wiper":2}]})

    @allure.title("雨刮退出维修位置提醒_启动场景初始值")
    @pytest.mark.full
    def test_caseid_1988014(self):
        hint = "Wiper Exit Repair Position"
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0, timeout=10)

        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 0)
        self.partner.ck_wti_warning_and_resp(hint, 1, timeout=10)
                
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0, timeout=5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0, timeout=5)
        
    @allure.title("雨量传感器故障信息(MsgWiperSensorFailure)")
    @pytest.mark.sanity
    def test_caseid_108528(self):
        hint = "Wiper Sensor Failure"
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'RainSnsrActvnErrToHmi', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'RainSnsrActvnErrToHmi', 1)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'RainSnsrActvnErrToHmi', 0)
        self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @pytest.mark.wiperliquid
    @allure.title("雨刮洗涤液信息_条件1触发_退出")
    @pytest.mark.sanity
    def test_caseid_1988429(self):
        # WshrFldTankStsToHMI从0到1，有提示
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 0) 
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperWashFluidLow", {}, {"out": 0})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 1) 
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperWashFluidLow", {}, {"out": 1})
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperWashFluidLowStatus", {"isWashFluidLow": 1})
        self.partner.ck_wti_warning_and_resp(self.wti_wiperliquid, 1)
        
        # 无提示
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 0)        
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperWashFluidLowStatus", {"isWashFluidLow": 0})
        self.partner.ck_wti_warning_and_resp(self.wti_wiperliquid, 0)
        
    @pytest.mark.wiperliquid
    @allure.title("雨刮洗涤液信息_条件2液位低&&启动洗涤(触发)_退出")
    @pytest.mark.sanity
    def test_caseid_1988430(self):
        # WshrFldTankStsToHMI为1
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 1) 
        sleep(0.1)
        self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT)
        sleep(3)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperWashFluidLow", {}, {"out": 1}, timeout=15)
        self.partner.empty_all(0.2)
        
        # 启动洗涤，有提示
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit", {"wipers": 0, "isOn": False})        
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', 0)
        sleep(0.1)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', 2)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SparyWashing", {"info": {"id": 0, "on": True}})
        self.partner.ck_wti_warning_and_resp(self.wti_wiperliquid, 1)
        
        # 退出 无提示
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 0)        
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperWashFluidLowStatus", {"isWashFluidLow": 0})
        self.partner.ck_wti_warning_and_resp(self.wti_wiperliquid, 0)
        
    @pytest.mark.wiperliquid        
    @allure.title("雨刮洗涤液信息_条件2液位低&&停止洗涤(不触发)")
    @pytest.mark.full
    def test_caseid_1988431(self):
        # WshrFldTankStsToHMI为1
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 1) 
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', 2)
        sleep(0.1)
        self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT)
        sleep(3)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperWashFluidLow", {}, {"out": 1}, timeout=15)
        self.partner.empty_all(0.2)

        # 停止洗涤，无提示
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit", {"wipers": 0, "isOn": False})        
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', 0)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SparyWashing", {"info": {"id": 0, "on": False}})
        self.partner.ck_wti_no_warning_and_ck_resp(self.wti_wiperliquid, 0)
        
    @pytest.mark.wiperliquid        
    @allure.title("雨刮洗涤液信息_条件2液位不低&&启动洗涤(不触发)")
    @pytest.mark.full
    def test_caseid_1988432(self):
        # WshrFldTankStsToHMI为0
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 0) 
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperWashFluidLow", {}, {"out": 0})
        self.partner.empty_all(0.2)

        # 启动洗涤，无提示
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit", {"wipers": 0, "isOn": False})        
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', 0)
        sleep(0.1)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', 2)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SparyWashing", {"info": {"id": 0, "on": True}})        
        self.partner.ck_wti_no_warning_and_ck_resp(self.wti_wiperliquid, 0)
        
    @pytest.mark.wiperliquid
    @allure.title("雨刮洗涤液信息_条件2液位低&&启动洗涤(触发)_停止洗涤(不退出)")
    @pytest.mark.full
    def test_caseid_1988433(self):
        # WshrFldTankStsToHMI为1
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 1) 
        sleep(0.1)
        self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT)
        sleep(3)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperWashFluidLow", {}, {"out": 1}, timeout=15)
        self.partner.empty_all(0.2)

        # 启动洗涤，有提示
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit", {"wipers": 0, "isOn": False})        
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', 0)
        sleep(0.1)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', 2)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SparyWashing", {"info": {"id": 0, "on": True}})
        self.partner.ck_wti_warning_and_resp(self.wti_wiperliquid, 1)

        # 停止洗涤，不退出
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', 0)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SparyWashing", {"info": {"id": 0, "on": False}})
        self.partner.ck_wti_no_warning_and_ck_resp(self.wti_wiperliquid, 1)
        
    @pytest.mark.wiperliquid        
    @allure.title("雨刮洗涤液信息_条件1&&条件2都满足(触发)_退出")
    @pytest.mark.sanity
    def test_caseid_1988434(self):
        # WshrFldTankStsToHMI从0到1
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 0) 
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperWashFluidLow", {}, {"out": 0})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 1) 
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperWashFluidLow", {}, {"out": 1})
        self.partner.ck_wti_warning_and_resp(self.wti_wiperliquid, 1)
        self.partner.empty_all(0.2)
        
        # 启动洗涤，有提示
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit", {"wipers": 0, "isOn": False})        
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', 0)
        sleep(0.1)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', 2)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SparyWashing", {"info": {"id": 0, "on": True}})
        self.partner.ck_wti_warning_and_resp(self.wti_wiperliquid, 1)

        # 退出，无提示
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 0)        
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperWashFluidLowStatus", {"isWashFluidLow": 0})
        self.partner.ck_wti_warning_and_resp(self.wti_wiperliquid, 0)
        
    @pytest.mark.wiperliquid
    @allure.title("雨刮洗涤液信息_条件2触发_退出_条件1触发_退出")
    @pytest.mark.sanity
    def test_caseid_1988436(self):
        # WshrFldTankStsToHMI为1
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 1) 
        sleep(0.1)
        self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT)
        sleep(3)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperWashFluidLow", {}, {"out": 1}, timeout=15)
        self.partner.empty_all(0.2)
        
        # 启动洗涤，有提示
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit", {"wipers": 0, "isOn": False})        
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', 0)
        sleep(0.1)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', 2)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SparyWashing", {"info": {"id": 0, "on": True}})
        self.partner.ck_wti_warning_and_resp(self.wti_wiperliquid, 1)
        
        # 退出，无提示
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 0)        
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperWashFluidLowStatus", {"isWashFluidLow": 0})
        self.partner.ck_wti_warning_and_resp(self.wti_wiperliquid, 0)
        
        # WshrFldTankStsToHMI从0到1，有提示
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 1) 
        self.partner.ck_wti_warning_and_resp(self.wti_wiperliquid, 1)
        
        # 退出，无提示
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 0)        
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperWashFluidLowStatus", {"isWashFluidLow": 0})
        self.partner.ck_wti_warning_and_resp(self.wti_wiperliquid, 0)
        
    @pytest.mark.wiperliquid        
    @allure.title("雨刮洗涤液信息_重启场景_isWashFluidLow为1后重启bgm_再启动洗涤")
    @pytest.mark.full
    def test_caseid_1988437(self):
        # WshrFldTankStsToHMI为1，重启bgm, 无提示
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 1) 
        sleep(0.1)
        self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT)
        sleep(3)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperWashFluidLow", {}, {"out": 1}, timeout=15)
        self.partner.ck_wti_no_warning_and_ck_resp(self.wti_wiperliquid, 0)
        self.partner.empty_all(0.2)
        
        # 启动洗涤，有提示
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit", {"wipers": 0, "isOn": False})        
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', 0)
        sleep(0.1)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', 2)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SparyWashing", {"info": {"id": 0, "on": True}})
        self.partner.ck_wti_warning_and_resp(self.wti_wiperliquid, 1)

        # 退出，无提示
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 0)        
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperWashFluidLowStatus", {"isWashFluidLow": 0})
        self.partner.ck_wti_warning_and_resp(self.wti_wiperliquid, 0)
        
    @pytest.mark.wiperliquid
    @allure.title("雨刮洗涤液信息_重启场景_isWashFluidLow为0后重启bgm_再isWashFluidLow为1")
    @pytest.mark.full
    def test_caseid_1988438(self):
        # WshrFldTankStsToHMI为0，重启bgm, 无提示
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 0) 
        sleep(0.1)
        self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT)
        sleep(3)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperWashFluidLow", {}, {"out": 0}, timeout=15)
        self.partner.ck_wti_no_warning_and_ck_resp(self.wti_wiperliquid, 0)
        self.partner.empty_all(0.2)
                
        # WshrFldTankStsToHMI为1，有提示
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 1) 
        self.partner.ck_wti_warning_and_resp(self.wti_wiperliquid, 1)
        
        # 退出，无提示
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 0)        
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperWashFluidLowStatus", {"isWashFluidLow": 0})
        self.partner.ck_wti_warning_and_resp(self.wti_wiperliquid, 0)
        
    @pytest.mark.wiperliquid        
    @allure.title("雨刮洗涤液信息_重启场景_检查isWashFluidLow值")
    @pytest.mark.full
    def test_caseid_1988439(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 1) 
        sleep(0.1)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT, resume_all_bus=False)
        sleep(3)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperWashFluidLow", {}, {"out": 0}, timeout=15)
        self.ipdu.resume_all_bus_send()
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperWashFluidLow", {}, {"out": 1}, timeout=3)
        
    @pytest.mark.wiperliquid
    @allure.title("雨刮洗涤液信息_与无WTI信息的洗涤液不足、舱外光亮度原始数据传感器故障、雨刮开关/按键故障组合测试")
    @pytest.mark.full
    def test_caseid_1988440(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 0)
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'RainSnsrActvnErrToHmi', 1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 3)
        
        self.partner.ck_wti_warning_and_resp(self.wti_wiperliquid, 1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault", {"faults": 
                                [{"fault":1, "faultMsg":"", "wiper":0}, 
                                 {"fault":2, "faultMsg":"", "wiper":0}, 
                                 {"fault":5, "faultMsg":"", "wiper":0}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": 
                                [{"fault":1, "faultMsg":"", "wiper":0}, 
                                 {"fault":2, "faultMsg":"", "wiper":0}, 
                                 {"fault":5, "faultMsg":"", "wiper":0}]})

        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'RainSnsrActvnErrToHmi', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 2)
        
        self.partner.ck_wti_warning_and_resp(self.wti_wiperliquid, 0)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault", {"faults": 
                                [{"fault":0, "faultMsg":"OK", "wiper":2}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": 
                                [{"fault":0, "faultMsg":"OK", "wiper":2}]})