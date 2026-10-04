#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File        : test_WindowService.py
@Author      : tao.cheng_ext@jiduatuo.com
@Time        : 2023/06/08 15:00 PM
@Description : Test SOA for WindowService
"""

import os
import sys
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *


class MoveSts:
    moving = 0
    stop = 1
    unknown = 255


@allure.feature("SOA服务接口")
@allure.story("整车控制/WindowService")
@pytest.mark.window
class TestWindowService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("WindowService", "client"),
                                     ("WindowAppService", "client"),
                                     ("KeyService", "client")])
        self.partner.method_default_timeout = 0.1
        self.sd_tester.tester_present()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        self.sd_tester.stop_tester_present()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.set_nopeople_incar()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqFrntLe', 0)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqFrntRi', 0)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqReLe', 0)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqReRi', 0)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinSwtStsAtPass', 0)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'WinSwtStsAtReLe', 0)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'WinSwtStsAtReRi', 0)
        self.set_WinPosnSts(1)
        self.ck_moveinfo_event_and_resp(MoveSts.stop, check_event=False)
        self.io.set_four_door_close()
        sleep(1)
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        self.partner.empty_all(0.5)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def five_door_close(self):
        self.io.pass_door_close()
        self.io.drvr_door_close()
        self.io.lere_door_close()
        self.io.rire_door_close()
        self.io.trunk_door_close()

    def BGM_down_up(self,X,Y,Z):
        """X代表总线停后等待时间 Y代表下电后电等待时间 Z代表上电后电等待时间"""
        self.ipdu.pause_all_bus_send()
        sleep(X)
        self.nucapp.bgm_power_off()
        sleep(Y)
        self.nucapp.bgm_power_on()
        sleep(Z)

    @allure.title("1.3.1版本_锁车自动关窗新CR")
    @pytest.mark.full
    def test_caseid_1981298(self):
        self.sd_tester.enter_default_session()
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        sleep(1)
        self.dk.set_cenlock_sts(0x1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 4, "value": 0}]})
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 26)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 6)
        sleep(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 4, "value": 1}]})
        sleep(1)
        self.dk.send_nfc_cmd()
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 7, timeout=0.5)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 7)
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1),
                                         (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 1)])

    @allure.title("1.3.1版本_锁车自动关窗新CR_短降后超时判断")
    @pytest.mark.full
    def test_caseid_1981301(self):
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 4, "value": 0}]})
        sleep(2)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 4, "value": 1}]})
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        sleep(1)
        self.dk.set_cenlock_sts(0x1)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 26)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 26)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 6)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 26)
        sleep(1)
        self.sd_tester.change_usage_mode(1)
        self.dk.send_nfc_cmd()
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 7, timeout=1)#刷卡后window需要根据windglb信号做判断
        sleep(1.5)
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1),
                                         (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 1)])
        
    @allure.title("1.3.1版本_自动关窗提醒_远控车窗关闭_某车窗不处于全开状态")
    @pytest.mark.full
    def test_caseid_1981306(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 4)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 20)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 20)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 5)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition", 
                                         {"windows": [{"id": 4, "position": 0}]})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 21)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 21)
        sleep(0.1)
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 1)])
        
    @allure.title("1.3.1版本_自动关窗提醒_远控车窗关闭_车窗处于全开状态")
    @pytest.mark.full
    def test_caseid_1981308(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 2)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 2)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 2)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 2)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition", 
                                         {"windows": [{"id": 4, "position": 0}]})
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 1)])

    @allure.title("打开")
    @pytest.mark.smoke
    def test_caseid_107062(self):
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "Open", {"windows": [0, 1, 2, 3]})
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 26),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 26),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 26),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 26)])

    @allure.title("车窗设置打开或关闭_下行PDU")
    @pytest.mark.smoke
    def test_caseid_1903494(self):
        def info(input):
            return 26 if input == "Open" else 1
        for req in ["Open","Close"]:
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, req, {"windows": [0, 1, 2, 3]})
            sleep(3)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
                self.bgm_eth_inter.ck_signal_values(signal, [0, info(req), info(req), info(req), 0, 0, info(req), info(req), info (req), 0])
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
            self.bgm_eth_inter.ck_period_time(signal, 0.04, 0.4, permit_fail_times=2)

    @allure.title("车窗服务上电event") # 通知车窗故障信息/通知车窗按键开关状态/通知车窗位置 
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1984312(self):
        for sts in [0, 1]:
            logger.info(f"sts:{sts}")
            faults = [{"fault": 3, "faultMsg": "", "window": 0},
                      {"fault": 3, "faultMsg": "", "window": 1},
                      {"fault": 3, "faultMsg": "", "window": 2},
                      {"fault": 3, "faultMsg": "", "window": 3},
                      {"fault": 4, "faultMsg": "", "window": 0},
                      {"fault": 4, "faultMsg": "", "window": 1},
                      {"fault": 4, "faultMsg": "", "window": 2},
                      {"fault": 4, "faultMsg": "", "window": 3}] if sts == 1 else [{"fault":0,"faultMsg":"","window":4}]
            pos = 255 if sts == 0 else 0
            val = 1 if sts == 0 else 0
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'WinFailrStsAtDrvr', sts)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'WinFailrStsAtPass', sts)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinFailrStsAtReLe', sts)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinFailrStsAtReRi', sts)
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, 'WinThermlStsAtDrvr', sts)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'WinThermlStsAtPass', sts)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'WinThermlStsAtReLe', sts)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'WinThermlStsAtReRi', sts)
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqFrntLe', sts)
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqFrntRi', sts)
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqReLe', sts)
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqReRi', sts)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinSwtStsAtPass', sts)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'WinSwtStsAtReLe', sts)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'WinSwtStsAtReRi', sts)
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', sts)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', sts)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', sts)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', sts)
            sleep(0.2)
            self.restart_bgm_and_connect_service(WINDOW_SERVICE_CLIENT)
            sleep(5)
            self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "WindowFault", {"faults":faults})
            self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT,"WindowPosition",{"position": 
                                                                [{"id": 0,"position": pos,"validity": val}, {"id": 1,"position": pos,"validity": val}, 
                                                                 {"id": 2,"position": pos,"validity": val}, {"id": 3,"position": pos,"validity": val}]})
            self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "NotifyWindowSwitchStatus", {"info":{"zone": 6, "sts":sts}}, timeout=15)

    @allure.title("获取车窗位置/下雨自动关窗/按键状态/车窗故障信息_默认值")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_1960070(self):
        try:
            self.ipdu.pause_bus_send("bodycan")
            self.ipdu.pause_bus_send("infocanfd")
            self.nucapp.bgm_power_off()
            sleep(3)
            self.nucapp.bgm_power_on()
            sleep(10)
            self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetWindowSwitchStatus", {"zone": [0,1,2,3,4,5,6]},
                                              {"out":[{"zone":0,"sts":0},{"zone":1,"sts":0},{"zone":2,"sts":0},{"zone":3,"sts":0},
                                                      {"zone":4,"sts":0},{"zone":5,"sts":0},{"zone":6,"sts":0}]})
            self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetRainWinAutoCloseReqSts", {}, {"out": 0})
            self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetPosition", {"windows":[0,1,2,3]}, 
                                                  {"out": [{"id": 0, "position": 255}, {"id": 1, "position": 255}, 
                                                           {"id": 2, "position": 255}, {"id": 3, "position": 255}]})
            self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": [{"fault":0,"faultMsg":"","window":4}]})
        except Exception as err:
            assert False
            self.ipdu.resume_bus_send("bodycan")
            self.ipdu.resume_bus_send("infocanfd")
        else:
            self.ipdu.resume_bus_send("bodycan")
            self.ipdu.resume_bus_send("infocanfd")

    @allure.title("遍历_获取和通知车窗按键开关状态")
    @pytest.mark.smoke
    def test_caseid_1979603(self):
        info ={'WinSwtReqFrntLe':0,'WinSwtReqFrntRi':1,'WinSwtReqReLe':2,'WinSwtReqReRi':3}
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqFrntLe', 0)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqFrntRi', 0)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqReLe', 0)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqReRi', 0)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinSwtStsAtPass', 0)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'WinSwtStsAtReLe', 0)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'WinSwtStsAtReRi', 0)
        self.partner.empty_all(0.5)
        for X in range(1,6):
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqFrntLe', X)
            sleep(0.5)
            self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "NotifyWindowSwitchStatus", {"info":{"zone": 0, "sts":X}})
            self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetWindowSwitchStatus", {"zone": [0]},
                                              {"out":[{"zone":0,"sts":X}]})
        for Y in range(1,6):
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqFrntRi', Y)
            sleep(0.5)
            self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "NotifyWindowSwitchStatus", {"info":{"zone": 1, "sts":Y}})
            self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetWindowSwitchStatus", {"zone": [1]},
                                              {"out":[{"zone":1,"sts":Y}]})
        for Z in range(1,6):
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqReLe', Z)
            sleep(0.5)
            self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "NotifyWindowSwitchStatus", {"info":{"zone": 2, "sts":Z}})
            self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetWindowSwitchStatus", {"zone": [2]},
                                              {"out":[{"zone":2,"sts":Z}]})
        for A in range(1,6):
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqReRi', A)
            sleep(0.5)
            self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "NotifyWindowSwitchStatus", {"info":{"zone": 3, "sts":A}})
            self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetWindowSwitchStatus", {"zone": [3]},
                                              {"out":[{"zone":3,"sts":A}]})
        for B in range(1,6):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinSwtStsAtPass', B)
            sleep(0.5)
            self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "NotifyWindowSwitchStatus", {"info":{"zone": 4, "sts":B}})
            self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetWindowSwitchStatus", {"zone": [4]},
                                              {"out":[{"zone":4,"sts":B}]})
        for C in range(1,6):
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'WinSwtStsAtReLe', C)
            sleep(0.5)
            self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "NotifyWindowSwitchStatus", {"info":{"zone": 5, "sts":C}})
            self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetWindowSwitchStatus", {"zone": [5]},
                                              {"out":[{"zone":5,"sts":C}]})
        for D in range(1,6):
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'WinSwtStsAtReRi', D)
            sleep(0.5)
            self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "NotifyWindowSwitchStatus", {"info":{"zone": 6, "sts":D}})
            self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetWindowSwitchStatus", {"zone": [6]},
                                              {"out":[{"zone":6,"sts":D}]})
        for key,value in info.items():
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, key, 0)
            sleep(0.5)
            self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "NotifyWindowSwitchStatus", {"info":{"zone": value, "sts":0}})
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinSwtStsAtPass', 0)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'WinSwtStsAtReLe', 0)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'WinSwtStsAtReRi', 0)
        sleep(0.5)
        self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "NotifyWindowSwitchStatus", {"info":{"zone": 4, "sts":0}})
        self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "NotifyWindowSwitchStatus", {"info":{"zone": 5, "sts":0}})
        self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "NotifyWindowSwitchStatus", {"info":{"zone": 6, "sts":0}})
        self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetWindowSwitchStatus", {"zone": [0,1,2,3,4,5,6]},
                                              {"out":[{"zone":0,"sts":0},{"zone":1,"sts":0},{"zone":2,"sts":0},{"zone":3,"sts":0},
                                                      {"zone":4,"sts":0},{"zone":5,"sts":0},{"zone":6,"sts":0}]})

    @allure.title("1.3.1版本_自动关窗提醒_远控车窗关闭_BGM上电后无法获取位置")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1981303(self):
        try:
            self.ipdu.pause_bus_send("bodycan")
            self.nucapp.bgm_power_off()
            time.sleep(1)
            self.nucapp.bgm_power_on()
            sleep(10)
            self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition", {"windows": [{"id": 4, "position": 0}]})
            self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 1),
                                         (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1)])
            sleep(2)
            self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition", {"windows": [{"id": 2, "position": 0}]})
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 0, timeout=0.5)
        except Exception as error:
            self.ipdu.resume_bus_send("bodycan")
            assert False, error
        else:
            self.ipdu.resume_bus_send("bodycan")

    @allure.title("1.3.1版本_自动关窗提醒_远控车窗关闭_超时处理")
    @pytest.mark.full
    def test_caseid_1981305(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 5)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 5)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 6)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 6)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition", {"windows": [{"id": 4, "position": 0}]})
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 6),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 6),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 7),
                                         (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 7)])
        sleep(1)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 0, timeout=0.5)
        sleep(0.4) #2S后未获取到位置
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1),
                                         (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 1)])

    @allure.title("1.3.1版本_自动关窗提醒_远控车窗关闭_BGM上电后远控单个车窗")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1981304(self):
        self.ipdu.pause_bus_send("bodycan")
        self.nucapp.bgm_power_off()
        time.sleep(1)
        self.nucapp.bgm_power_on()
        sleep(5)
        self.ipdu.resume_bus_send("bodycan")
        sleep(5)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 5)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 5)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 6)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 6)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition", {"windows": [{"id": 3, "position": 0}]})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 7, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 0, timeout=0.5)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 7)
        sleep(0.1)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 0, timeout=0.5)

    @allure.title("遍历_获取和通知车窗故障信息_所有车窗故障")
    @pytest.mark.smoke
    def test_caseid_1978249(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'WinFailrStsAtDrvr', 0)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'WinFailrStsAtPass', 0)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinFailrStsAtReLe', 0)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinFailrStsAtReRi', 0)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, 'WinThermlStsAtDrvr', 0)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'WinThermlStsAtPass', 0)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'WinThermlStsAtReLe', 0)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'WinThermlStsAtReRi', 0)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'WinFailrStsAtDrvr', 1)
        sleep(0.2)
        self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "WindowFault", {"faults":[{"fault":3,"faultMsg":"","window":0}]})
        self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": [{"fault":3,"faultMsg":"","window":0}]})

        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'WinFailrStsAtPass', 1)
        sleep(0.2)
        self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "WindowFault",{"faults": [{"fault": 3, "faultMsg": "", "window": 0},
                                                                                   {"fault": 3, "faultMsg": "", "window": 1}]})
        self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": [{"fault":3,"faultMsg":"","window":0},
                                                                                                  {"fault": 3, "faultMsg": "", "window": 1}]})
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinFailrStsAtReLe', 1)
        sleep(0.2)
        self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "WindowFault", {"faults": [{"fault": 3, "faultMsg": "", "window": 0},
                                                                                    {"fault": 3, "faultMsg": "", "window": 1},
                                                                                    {"fault": 3, "faultMsg": "", "window": 2}]})
        self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": [{"fault": 3, "faultMsg": "", "window": 0},
                                                                                         {"fault": 3, "faultMsg": "", "window": 1},
                                                                                        {"fault": 3, "faultMsg": "", "window": 2}]})
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinFailrStsAtReRi', 1)
        sleep(0.1)
        self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "WindowFault",
                                  {"faults": [{"fault": 3, "faultMsg": "", "window": 0},
                                              {"fault": 3, "faultMsg": "", "window": 1},
                                              {"fault": 3, "faultMsg": "", "window": 2},
                                              {"fault": 3, "faultMsg": "", "window": 3}]})
        self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 3, "faultMsg": "", "window": 0},
                                                       {"fault": 3, "faultMsg": "", "window": 1},
                                                       {"fault": 3, "faultMsg": "", "window": 2},
                                                       {"fault": 3, "faultMsg": "", "window": 3}]})

        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, 'WinThermlStsAtDrvr', 1)
        sleep(0.1)
        self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "WindowFault",
                                  {"faults": [{"fault": 3, "faultMsg": "", "window": 0},
                                              {"fault": 3, "faultMsg": "", "window": 1},
                                              {"fault": 3, "faultMsg": "", "window": 2},
                                              {"fault": 3, "faultMsg": "", "window": 3},
                                              {"fault": 4, "faultMsg": "", "window": 0}]})
        self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 3, "faultMsg": "", "window": 0},
                                                       {"fault": 3, "faultMsg": "", "window": 1},
                                                       {"fault": 3, "faultMsg": "", "window": 2},
                                                       {"fault": 3, "faultMsg": "", "window": 3},
                                                       {"fault": 4, "faultMsg": "", "window": 0}]})

        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'WinThermlStsAtPass', 1)
        sleep(0.1)
        self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "WindowFault",
                                  {"faults": [{"fault": 3, "faultMsg": "", "window": 0},
                                              {"fault": 3, "faultMsg": "", "window": 1},
                                              {"fault": 3, "faultMsg": "", "window": 2},
                                              {"fault": 3, "faultMsg": "", "window": 3},
                                              {"fault": 4, "faultMsg": "", "window": 0},
                                              {"fault": 4, "faultMsg": "", "window": 1}]})
        self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 3, "faultMsg": "", "window": 0},
                                                       {"fault": 3, "faultMsg": "", "window": 1},
                                                       {"fault": 3, "faultMsg": "", "window": 2},
                                                       {"fault": 3, "faultMsg": "", "window": 3},
                                                       {"fault": 4, "faultMsg": "", "window": 0},
                                                       {"fault": 4, "faultMsg": "", "window": 1}]})

        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'WinThermlStsAtReLe', 1)
        sleep(0.1)
        self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "WindowFault",
                                  {"faults": [{"fault": 3, "faultMsg": "", "window": 0},
                                              {"fault": 3, "faultMsg": "", "window": 1},
                                              {"fault": 3, "faultMsg": "", "window": 2},
                                              {"fault": 3, "faultMsg": "", "window": 3},
                                              {"fault": 4, "faultMsg": "", "window": 0},
                                              {"fault": 4, "faultMsg": "", "window": 1},
                                              {"fault": 4, "faultMsg": "", "window": 2}]})
        self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 3, "faultMsg": "", "window": 0},
                                                       {"fault": 3, "faultMsg": "", "window": 1},
                                                       {"fault": 3, "faultMsg": "", "window": 2},
                                                       {"fault": 3, "faultMsg": "", "window": 3},
                                                       {"fault": 4, "faultMsg": "", "window": 0},
                                                       {"fault": 4, "faultMsg": "", "window": 1},
                                                       {"fault": 4, "faultMsg": "", "window": 2}]})

        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'WinThermlStsAtReRi', 1)
        sleep(0.1)
        self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "WindowFault",
                                  {"faults": [{"fault": 3, "faultMsg": "", "window": 0},
                                              {"fault": 3, "faultMsg": "", "window": 1},
                                              {"fault": 3, "faultMsg": "", "window": 2},
                                              {"fault": 3, "faultMsg": "", "window": 3},
                                              {"fault": 4, "faultMsg": "", "window": 0},
                                              {"fault": 4, "faultMsg": "", "window": 1},
                                              {"fault": 4, "faultMsg": "", "window": 2},
                                              {"fault": 4, "faultMsg": "", "window": 3}]})
        self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 3, "faultMsg": "", "window": 0},
                                                       {"fault": 3, "faultMsg": "", "window": 1},
                                                       {"fault": 3, "faultMsg": "", "window": 2},
                                                       {"fault": 3, "faultMsg": "", "window": 3},
                                                       {"fault": 4, "faultMsg": "", "window": 0},
                                                       {"fault": 4, "faultMsg": "", "window": 1},
                                                       {"fault": 4, "faultMsg": "", "window": 2},
                                                       {"fault": 4, "faultMsg": "", "window": 3}]})

        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'WinFailrStsAtDrvr', 0)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'WinFailrStsAtPass', 0)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinFailrStsAtReLe', 0)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinFailrStsAtReRi', 0)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, 'WinThermlStsAtDrvr', 0)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'WinThermlStsAtPass', 0)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'WinThermlStsAtReLe', 0)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'WinThermlStsAtReRi', 0)
        time.sleep(1)
        self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "WindowFault",   {"faults": [{"fault": 0, "faultMsg": "", "window": 4}]})
        self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": [{"fault": 0, "faultMsg": "", "window": 4}]})

    @allure.title("关闭")
    @pytest.mark.sanity
    def test_caseid_107060(self):
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "Close", {"windows": [0, 1, 2, 3]})

        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 1)])

    @allure.title("设置所有车窗位置_打断逻辑")
    @pytest.mark.full
    def test_caseid_107055(self):
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 0, "position": 20},
                                                                                            {"id": 1, "position": 20},
                                                                                            {"id": 2, "position": 20},
                                                                                            {"id": 3, "position": 20}]})
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 0, "position": 100},
                                                                                            {"id": 1, "position": 100},
                                                                                            {"id": 2, "position": 100},
                                                                                            {"id": 3,
                                                                                             "position": 100}]})
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 26),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 26),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 26),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 26)])

    @allure.title("遍历使用者模式_0和1_设置所有车窗位置_开度0")
    @pytest.mark.full
    def test_caseid_107059(self):
        for usgmode in [0,1]:
            self.sd_tester.change_usage_mode(usgmode)
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": 0}]})
            self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1),
                                            (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1),
                                            (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1),
                                            (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 1)])
        
    @allure.title("遍历使用者模式_0和1_设置所有车窗位置_开度100")
    @pytest.mark.full
    def test_caseid_107064(self):
        for usgmode in [0,1]:
            self.sd_tester.change_usage_mode(usgmode)
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 0, "position": 100},
                                                                                                {"id": 1, "position": 100},
                                                                                                {"id": 2, "position": 100},
                                                                                                {"id": 3, "position": 100}]})
            self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 26),
                                            (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 26),
                                            (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 26),
                                            (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 26)])

    @allure.title("打开_打断逻辑")
    @pytest.mark.sanity
    def test_caseid_107065(self):
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "Open", {"windows": [0, 1, 2, 3]})

        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 26),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 26),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 26),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 26)])
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 0, "position": 20},
                                                                                            {"id": 1, "position": 20},
                                                                                            {"id": 2, "position": 20},
                                                                                            {"id": 3, "position": 20}]})
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 6),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 6),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 6),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 6)])

    @allure.title("关闭_打断逻辑")
    @pytest.mark.full
    def test_caseid_107054(self):
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "Close", {"windows": [0, 1, 2, 3]})

        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 1)])
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "Open", {"windows": [0, 1, 2, 3]})

        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 26),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 26),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 26),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 26)])

    @allure.title("遍历_通知和获取下雨自动关窗请求状态_关和无请求")
    @pytest.mark.sanity
    def test_caseid_107058(self):
        self.sd_tester.write_single_ccp(177,1)
        sleep(3)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 4, "value": 0}]})
        self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetRainWinAutoCloseReqSts", {}, {"out": 0})
        self.sd_tester.enter_default_session()
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 26)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 5)
        sleep(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 4, "value": 1}]})
        self.dk.set_cenlock_sts(0x1)
        sleep(1)
        self.dk.send_nfc_cmd()
        self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT,"NotifyRainWinAutoCloseReqSts", {"reqSts": 3})
        self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetRainWinAutoCloseReqSts", {}, {"out": 3})
        
    @allure.title("1.3.1版本_自动关窗提醒_雨天自动关窗_超时处理")
    @pytest.mark.full
    def test_caseid_1981302(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetRainAutoCloseWindow", {"isOn": False})
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 5)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 5)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 6)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 6)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetRainAutoCloseWindow", {"isOn": True})
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        sleep(1)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.dk.set_cenlock_sts(3)
        self.ipdu.lin1_wakeup()
        sleep(1)
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'RainDetected', 0)
        sleep(1)
        self.ipdu.check_multiple_signals_thread_start([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 6),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 6),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 7),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 7)],do_print=True)
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'RainDetected', 1)
        result = self.ipdu.check_multiple_signals_thread_stop(message_name="CemBodyFr68")
        assert result
        sleep(1.5)
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 1)])

        
    @allure.title("1.3.1版本_自动关窗提醒_雨天自动关窗_车窗不处于短降状态")
    @pytest.mark.full
    def test_caseid_1981353(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetRainAutoCloseWindow", {"isOn": False})
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 2)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 2)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 2)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 2)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetRainAutoCloseWindow", {"isOn": True})
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.dk.set_cenlock_sts(3)
        self.ipdu.lin1_wakeup()
        sleep(1)
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'RainDetected', 0)
        sleep(1)
        self.ipdu.check_multiple_signals_thread_start([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 1)],do_print=True)
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'RainDetected', 1)
        result = self.ipdu.check_multiple_signals_thread_stop(message_name="CemBodyFr68")
        assert result
            
    @allure.title("通知获取车窗位置_全部车窗位置(包含置信度)_上电默认值")
    @pytest.mark.full
    def test_caseid_1985230(self):
        for sts in [0, 1]:
            logger.info(f"sts:{sts}")
            pos = 255 if sts == 0 else 0
            val = 1 if sts == 0 else 0
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', sts)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', sts)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', sts)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', sts)
            sleep(0.1)
            self.restart_bgm_and_connect_service(WINDOW_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetPosition", {"windows":[4]},
                                                    {"out":[{"id":0,"position":255,"validity": 0}, {"id":1,"position":255,"validity": 0},
                                                            {"id":2,"position":255,"validity": 0}, {"id":3,"position":255,"validity": 0}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT,"WindowPosition",{"position": 
                                                            [{"id": 0,"position":pos,"validity": val}, {"id": 1,"position":pos,"validity": val},
                                                             {"id": 2,"position":pos,"validity": val}, {"id": 3,"position":pos,"validity": val}]})
            self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetPosition", {"windows":[4]},
                                                     {"out":[{"id":0,"position":pos,"validity": val}, {"id":1,"position":pos,"validity": val},
                                                             {"id":2,"position":pos,"validity": val}, {"id":3,"position":pos,"validity": val}]})

    @allure.title("遍历_通知获取车窗位置_全部车窗位置(包含置信度)_无效到有有效位置1")
    @pytest.mark.full
    def test_caseid_1985231(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 1)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 1)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 1)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 1)
        self.partner.empty_all(0.5)
        for X in [0,27,28,29,30,31]:
            logger.info(f"---发送信号{X}")
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', X)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', X)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', X)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', X)
            sleep(0.5)
            self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT,"WindowPosition",{"position": [{"id": 0,"position": 0,"validity": 1},
                                                             {"id": 1,"position": 0,"validity": 1},{"id": 2,"position": 0,"validity": 1},
                                                             {"id": 3,"position": 0,"validity": 1}]})
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 1)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 1)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 1)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 1)
            sleep(0.5)
            self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT,"WindowPosition",{"position": [{"id": 0,"position": 0,"validity": 0},
                                                             {"id": 1,"position": 0,"validity": 0},{"id": 2,"position": 0,"validity": 0},
                                                             {"id": 3,"position": 0,"validity": 0}]})
            
    @allure.title("遍历_通知获取车窗位置_全部车窗位置(包含置信度)_无效到有有效位置10")
    @pytest.mark.sanity
    def test_caseid_1985232(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 26)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 26)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 26)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 26)
        self.partner.empty_all(0.5)
        for X in [0,27,28,29,30,31]:
            logger.info(f"---发送信号{X}")
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', X)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', X)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', X)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', X)
            sleep(0.5)
            self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT,"WindowPosition",{"position": [{"id": 0,"position": 100,"validity": 1},
                                                             {"id": 1,"position": 100,"validity": 1},{"id": 2,"position": 100,"validity": 1},
                                                             {"id": 3,"position": 100,"validity": 1}]})
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 26)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 26)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 26)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 26)
            sleep(0.5)
            self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT,"WindowPosition",{"position": [{"id": 0,"position": 100,"validity": 0},
                                                             {"id": 1,"position": 100,"validity": 0},{"id": 2,"position": 100,"validity": 0},
                                                             {"id": 3,"position": 100,"validity": 0}]})

    @allure.title("设置车窗位置_车窗位置为非预期取值")
    @pytest.mark.full
    def test_caseid_1988649(self):
        for pos in [5, 6, 7]:
            exp = pos//4 + 1
            logger.info(f"position:{pos}, expect:{exp}")
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": pos}]})
            self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', exp),
                                              (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', exp),
                                              (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', exp),
                                              (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', exp)], timeout=0.5)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
            for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
                self.bgm_eth_inter.ck_signal_values(signal, [0, exp, exp, exp, 0, 0, exp, exp, exp, 0])


    def set_WinPosnSts(self, pos, sleep_time=0.1):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', pos)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', pos)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', pos)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', pos)
        sleep(sleep_time)
    
    def ck_moveinfo_event_and_resp(self, sts, check_event=True, timeout=3):
        if check_event:
            self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT,"WindowMoveInfo", {"moveInfo":
                                                {"frontLeftMoveSts": sts, "frontRightMoveSts": sts, 
                                                "rearLeftMoveSts": sts, "rearRightMoveSts": sts}}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetWindowMoveInfo", {}, {"out": 
                                            {"frontLeftMoveSts": sts, "frontRightMoveSts": sts, 
                                             "rearLeftMoveSts": sts, "rearRightMoveSts": sts}})
    
    @allure.title("通知/获取车窗运动信息_idle状态")
    @pytest.mark.full
    def test_caseid_1988991(self):
        for i in [0, 20]:
            logger.info(f"WinPosnStsAtDrvr:{i}") 
            self.set_WinPosnSts(i, sleep_time=0.2)
            self.restart_bgm_and_connect_service(WINDOW_SERVICE_CLIENT, resume_all_bus=False)
            logger.info(f"restart success.") 
            
            self.ck_moveinfo_event_and_resp(MoveSts.unknown, check_event=False, timeout=20)
            
            self.ipdu.resume_all_bus_send()
            check_event = True if i == 20 else False
            sts = MoveSts.stop if i == 20 else MoveSts.unknown
            self.ck_moveinfo_event_and_resp(sts, check_event=check_event)
            
    @allure.title("通知/获取车窗运动信息_运动到停止循环")
    @pytest.mark.smoke
    def test_caseid_1988992(self):
        for i in [2, 26, 25, 1]:
            logger.info(f"WinPosnStsAtDrvr:{i}") 
            self.set_WinPosnSts(i)
            self.ck_moveinfo_event_and_resp(MoveSts.moving)
            self.ck_moveinfo_event_and_resp(MoveSts.stop, timeout=0.6)
        
    @allure.title("通知/获取车窗运动信息_保持运动")
    @pytest.mark.full
    def test_caseid_1988993(self):
        for i in [10, 26, 2, 1]:
            logger.info(f"WinPosnStsAtDrvr:{i}") 
            self.set_WinPosnSts(i)

            check_evnet = True if i == 1 else False
            self.ck_moveinfo_event_and_resp(MoveSts.moving, check_evnet)
            sleep(0.1)
            self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetWindowMoveInfo", {}, {"out": 
                                                {"frontLeftMoveSts": MoveSts.moving, "frontRightMoveSts": MoveSts.moving, 
                                                 "rearLeftMoveSts": MoveSts.moving, "rearRightMoveSts": MoveSts.moving}})
            
    @allure.title("通知/获取车窗运动信息_信号无效值(保持lastvalue)")
    @pytest.mark.full
    def test_caseid_1988994(self):
        # idle状态收到无效值
        self.set_WinPosnSts(0)
        self.restart_bgm_and_connect_service(WINDOW_SERVICE_CLIENT)
        self.ck_moveinfo_event_and_resp(MoveSts.unknown, check_event=False, timeout=20)

        for i in [27, 28, 29, 30, 31]:
            logger.info(f"in idle set WinPosnStsAtDrvr:{i}") 
            self.set_WinPosnSts(i)
            self.ck_moveinfo_event_and_resp(MoveSts.unknown, check_event=False)
    
        # moving状态收到无效值
        for index, value in enumerate([0, 27, 28, 29, 30, 31]):
            logger.info(f"in moving set WinPosnStsAtDrvr:{value}") 
            self.set_WinPosnSts(10 + index)
            self.ck_moveinfo_event_and_resp(MoveSts.moving)
            self.set_WinPosnSts(value)
            self.ck_moveinfo_event_and_resp(MoveSts.moving, check_event=False)
            self.ck_moveinfo_event_and_resp(MoveSts.stop)
    
        # stop状态收到无效值
        self.set_WinPosnSts(10)
        self.partner.empty_all(0.5)
        for i in [0, 27, 28, 29, 30, 31]:
            logger.info(f"in stop set WinPosnStsAtDrvr:{i}") 
            self.set_WinPosnSts(i)
            self.ck_moveinfo_event_and_resp(MoveSts.stop, check_event=False)
            
    @allure.title("设置车窗位置_正常发送报文")
    @pytest.mark.smoke
    def test_caseid_1989198(self):
        for pos in [20, 80]:
            logger.info(f"position:{pos}") 
            sig = pos//4 + 1
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": pos}]})
            sleep(1)
            self.ck_moveinfo_event_and_resp(MoveSts.stop, check_event=False)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
            
            for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
                self.bgm_eth_inter.ck_signal_values(signal, [0, sig, sig, sig, 0, 0, sig, sig, sig, 0])
                self.bgm_eth_inter.ck_period_time(signal, 0.04, 0.4, permit_fail_times=2)
            
                signal_items = self.bgm_eth_inter.get_signal_items(signal)
                assert 0.95 <= signal_items[5][1] - signal_items[0][1] <= 1.05    

    @allure.title("设置车窗位置_打断_1秒内车窗处于运动_再设置位置")
    @pytest.mark.sanity
    def test_caseid_1989200(self):
        sig1 = 40//4 + 1
        sig2 = 20//4 + 1

        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": 40}]})
        self.set_WinPosnSts(11, sleep_time=0.05)
        self.ck_moveinfo_event_and_resp(MoveSts.moving)
        
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": 20}]})
        self.set_WinPosnSts(12, sleep_time=0.05)
        self.ck_moveinfo_event_and_resp(MoveSts.moving, check_event=False)
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": 20}]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        
        for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
            self.bgm_eth_inter.ck_signal_values(signal, [0, sig1, 0, sig2, 0, sig2, sig2, sig2, 0, 0, sig2, sig2, sig2, 0])

    @allure.title("设置车窗位置_打断_1秒内车窗处于停止_再设置位置")
    @pytest.mark.full
    def test_caseid_1989201(self):
        sig1 = 1//4 + 1
        sig2 = 20//4 + 1

        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": 1}]})
        self.set_WinPosnSts(21)
        self.ck_moveinfo_event_and_resp(MoveSts.stop)
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": 20}]})
        self.set_WinPosnSts(20)
        self.ck_moveinfo_event_and_resp(MoveSts.stop)
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": 20}]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        
        for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
            self.bgm_eth_inter.ck_signal_values(signal, [0, sig1, sig1, sig1, 0, 0, sig2, sig2, sig2, 0, 0, sig2, sig2, sig2, 0, 0, sig2, sig2, sig2, 0])

    @allure.title("设置车窗位置_打断_1秒后车窗处于运动_再设置位置")
    @pytest.mark.full
    def test_caseid_1989203(self):
        sig1 = 100//4 + 1
        sig2 = 20//4 + 1
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": 100}]})
        sleep(0.8) 
        self.set_WinPosnSts(11, sleep_time=0.2)
        self.ck_moveinfo_event_and_resp(MoveSts.moving)  # 1秒钟后车窗处于运动，则不会再发第二次报文
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": 20}]})

        sleep(0.8) 
        self.set_WinPosnSts(12, sleep_time=0.2)
        self.ck_moveinfo_event_and_resp(MoveSts.moving)  # 1秒钟后车窗处于运动，则不会再发第二次报文
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": 20}]})
        
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        
        for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
            self.bgm_eth_inter.ck_signal_values(signal, [0, sig1, sig1, sig1, 0, 0, sig2, sig2, sig2, 0, 0, sig2, sig2, sig2, 0, 0, sig2, sig2, sig2, 0])

    @allure.title("设置车窗位置_打断_1秒内车窗处于运动_收到主驾侧车窗有效按键")
    @pytest.mark.sanity
    def test_caseid_1989204(self):
        for btn in [1, 2, 3, 4]:
            position = 40 + btn * 4
            sig = position//4 + 1
            logger.info(f"button: {btn}, position:{position} sig:{sig}")
            
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": position}]})
            self.set_WinPosnSts(10 + btn)
            self.ck_moveinfo_event_and_resp(MoveSts.moving)

            for signal in ['WinSwtReqFrntLe', 'WinSwtReqFrntRi', 'WinSwtReqReLe', 'WinSwtReqReRi']:
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, signal, btn)
                sleep(0.1)
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, signal, 0)
                    
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
            
            for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
                sig_list = self.bgm_eth_inter.get_signal_values(signal)
                assert sig_list != []
                assert str(sig_list)[:-1] in str([0, sig, sig, sig, 0])

    @allure.title("设置车窗位置_不打断_1秒内车窗处于运动_收到主驾侧车窗无效按键")
    @pytest.mark.full
    def test_caseid_1989205(self):
        for btn in [0, 5]:
            position = 40 + btn * 4
            sig = position//4 + 1
            logger.info(f"button: {btn}, position:{position} sig:{sig}")
            
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": position}]})
            self.set_WinPosnSts(10 + btn)
            self.ck_moveinfo_event_and_resp(MoveSts.moving)

            for signal in ['WinSwtReqFrntLe', 'WinSwtReqFrntRi', 'WinSwtReqReLe', 'WinSwtReqReRi']:
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, signal, btn)
                sleep(0.02)
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, signal, 0)
                    
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
            
            for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
                self.bgm_eth_inter.ck_signal_values(signal, [0, sig, sig, sig, 0, 0, sig, sig, sig, 0])
            
    @allure.title("设置车窗位置_打断_1秒内车窗处于运动_收到非主驾侧车窗有效按键")
    @pytest.mark.full
    def test_caseid_1989206(self):
        for btn in [1, 2, 3, 4]:
            position = 40 + btn * 4
            sig = position//4 + 1
            logger.info(f"button: {btn}, position:{position} sig:{sig}")
            
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": position}]})
            self.set_WinPosnSts(10 + btn)
            self.ck_moveinfo_event_and_resp(MoveSts.moving)

            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinSwtStsAtPass', btn)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'WinSwtStsAtReLe', btn)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'WinSwtStsAtReRi', btn)
            sleep(0.1)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinSwtStsAtPass', 0)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'WinSwtStsAtReLe', 0)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'WinSwtStsAtReRi', 0)
            
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
            
            for signal in ['WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
                sig_list = self.bgm_eth_inter.get_signal_values(signal)
                assert sig_list != []
                assert str(sig_list)[:-1] in str([0, sig, sig, sig, 0])

    @allure.title("设置车窗位置_不打断_1秒内车窗处于运动_收到非主驾侧车窗无效按键")
    @pytest.mark.full
    def test_caseid_1989207(self):
        for btn in [0, 5]:
            position = 40 + btn * 4
            sig = position//4 + 1
            logger.info(f"button: {btn}, position:{position} sig:{sig}")
            
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": position}]})
            self.set_WinPosnSts(10 + btn)
            self.ck_moveinfo_event_and_resp(MoveSts.moving)

            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinSwtStsAtPass', btn)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'WinSwtStsAtReLe', btn)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'WinSwtStsAtReRi', btn)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinSwtStsAtPass', 0)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'WinSwtStsAtReLe', 0)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'WinSwtStsAtReRi', 0)
            
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
            
            for signal in ['WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
                self.bgm_eth_inter.ck_signal_values(signal, [0, sig, sig, sig, 0, 0, sig, sig, sig, 0])
            
    @allure.title("设置车窗位置_打断_1秒内车窗处于停止_收到主驾侧车窗有效按键")
    @pytest.mark.full
    def test_caseid_1989208(self):
        for btn in [1, 2, 3, 4]:
            position = 40 + btn * 4
            sig = position//4 + 1
            logger.info(f"button: {btn}, position:{position} sig:{sig}")
            
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": position}]})
            self.set_WinPosnSts(10 + btn)
            self.ck_moveinfo_event_and_resp(MoveSts.stop)

            for signal in ['WinSwtReqFrntLe', 'WinSwtReqFrntRi', 'WinSwtReqReLe', 'WinSwtReqReRi']:
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, signal, btn)
                sleep(0.1)
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, signal, 0)
                    
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
            
            for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
                sig_list = self.bgm_eth_inter.get_signal_values(signal)
                assert sig_list != []
                assert str(sig_list)[:-1] in str([0, sig, sig, sig, 0])

    @allure.title("设置车窗位置_不打断_1秒内车窗处于停止_收到主驾侧车窗无效按键")
    @pytest.mark.full
    def test_caseid_1989209(self):
        for btn in [0, 5]:
            position = 40 + btn * 4
            sig = position//4 + 1
            logger.info(f"button: {btn}, position:{position} sig:{sig}")
            
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": position}]})
            self.set_WinPosnSts(10 + btn)
            self.ck_moveinfo_event_and_resp(MoveSts.stop)

            for signal in ['WinSwtReqFrntLe', 'WinSwtReqFrntRi', 'WinSwtReqReLe', 'WinSwtReqReRi']:
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, signal, btn)
                sleep(0.02)
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, signal, 0)
                    
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
            
            for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
                self.bgm_eth_inter.ck_signal_values(signal, [0, sig, sig, sig, 0, 0, sig, sig, sig, 0])
                
    @allure.title("设置车窗位置_打断_1秒内车窗处于停止_收到非主驾侧车窗有效按键")
    @pytest.mark.full
    def test_caseid_1989210(self):
        for btn in [1, 2, 3, 4]:
            position = 40 + btn * 4
            sig = position//4 + 1
            logger.info(f"button: {btn}, position:{position} sig:{sig}")
            
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": position}]})
            self.set_WinPosnSts(10 + btn)
            self.ck_moveinfo_event_and_resp(MoveSts.stop)

            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinSwtStsAtPass', btn)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'WinSwtStsAtReLe', btn)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'WinSwtStsAtReRi', btn)
            sleep(0.1)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinSwtStsAtPass', 0)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'WinSwtStsAtReLe', 0)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'WinSwtStsAtReRi', 0)
            
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
            
            for signal in ['WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
                sig_list = self.bgm_eth_inter.get_signal_values(signal)
                assert sig_list != []
                assert str(sig_list)[:-1] in str([0, sig, sig, sig, 0])

    @allure.title("设置车窗位置_不打断_1秒内车窗处于停止_收到非主驾侧车窗无效按键")
    @pytest.mark.full
    def test_caseid_1989211(self):
        for btn in [0, 5]:
            position = 40 + btn * 4
            sig = position//4 + 1
            logger.info(f"button: {btn}, position:{position} sig:{sig}")
            
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": position}]})
            self.set_WinPosnSts(10 + btn)
            self.ck_moveinfo_event_and_resp(MoveSts.stop)

            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinSwtStsAtPass', btn)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'WinSwtStsAtReLe', btn)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'WinSwtStsAtReRi', btn)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinSwtStsAtPass', 0)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'WinSwtStsAtReLe', 0)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'WinSwtStsAtReRi', 0)
            
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
            
            for signal in ['WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
                self.bgm_eth_inter.ck_signal_values(signal, [0, sig, sig, sig, 0, 0, sig, sig, sig, 0])
            
    @allure.title("设置车窗位置_收到车窗按键后设置车窗位置")
    @pytest.mark.full
    def test_caseid_1989216(self):
        for signal in ['WinSwtReqFrntLe', 'WinSwtReqFrntRi', 'WinSwtReqReLe', 'WinSwtReqReRi']:
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, signal, 1)
            sleep(0.1)
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, signal, 0)
            
        for pos in [20, 80]:
            sig = pos//4 + 1
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": pos}]})
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=3)
            
            for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
                self.bgm_eth_inter.ck_signal_values(signal, [0, sig, sig, sig, 0, 0, sig, sig, sig, 0])

    @allure.title("设置车窗全开_当前为idle状态")
    @pytest.mark.full
    def test_caseid_1989217(self):
        sig = 26
        self.set_WinPosnSts(0)
        self.restart_bgm_and_connect_service(WINDOW_SERVICE_CLIENT)
        sleep(10)
        self.ck_moveinfo_event_and_resp(MoveSts.unknown, check_event=False, timeout=20)

        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "Open", {"windows": [0, 1, 2, 3]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(3)
        
        for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
            self.bgm_eth_inter.ck_signal_values(signal, [0, sig, sig, sig, 0, 0, sig, sig, sig, 0])

    @allure.title("设置车窗全开_当前为停止状态")
    @pytest.mark.smoke
    def test_caseid_1989218(self):
        sig = 26
        self.set_WinPosnSts(10)
        self.ck_moveinfo_event_and_resp(MoveSts.stop)

        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "Open", {"windows": [0, 1, 2, 3]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(3)
        
        for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
            self.bgm_eth_inter.ck_signal_values(signal, [0, sig, sig, sig, 0, 0, sig, sig, sig, 0])
        
        # 无效信号时
        self.set_WinPosnSts(27)
        self.ck_moveinfo_event_and_resp(MoveSts.stop, check_event=False)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "Open", {"windows": [4]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(3)
        
        for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
            self.bgm_eth_inter.ck_signal_values(signal, [0, sig, sig, sig, 0, 0, sig, sig, sig, 0])
        
    @allure.title("设置车窗全开_当前为运动状态")
    @pytest.mark.sanity
    def test_caseid_1989219(self):
        sig = 26

        self.bgm_eth_inter.start_bgm_tcpdump()
        self.set_WinPosnSts(10)
        self.ck_moveinfo_event_and_resp(MoveSts.moving)
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "Open", {"windows": [0, 1, 2, 3]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(2)
        
        for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
            self.bgm_eth_inter.ck_signal_values(signal, [0, sig, sig, sig, 0, 0, sig, sig, sig, 0])
        

        self.set_WinPosnSts(11)
        self.ck_moveinfo_event_and_resp(MoveSts.moving)
        # 无效信号时
        self.set_WinPosnSts(27)
        self.ck_moveinfo_event_and_resp(MoveSts.moving, check_event=False)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "Open", {"windows": [4]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(2)
        
        for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
            self.bgm_eth_inter.ck_signal_values(signal, [0, sig, sig, sig, 0, 0, sig, sig, sig, 0])
              
    @allure.title("设置车窗全关_当前为idle状态")
    @pytest.mark.full
    def test_caseid_1989220(self):
        sig = 1
        self.set_WinPosnSts(0)
        self.restart_bgm_and_connect_service(WINDOW_SERVICE_CLIENT)
        sleep(10)
        self.ck_moveinfo_event_and_resp(MoveSts.unknown, check_event=False, timeout=20)
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "Close", {"windows": [0, 1, 2, 3]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(3)
        
        for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
            self.bgm_eth_inter.ck_signal_values(signal, [0, sig, sig, sig, 0, 0, sig, sig, sig, 0])

    @allure.title("设置车窗全关_当前为停止状态")
    @pytest.mark.smoke
    def test_caseid_1989221(self):
        sig = 1
        self.set_WinPosnSts(10)
        self.ck_moveinfo_event_and_resp(MoveSts.stop)

        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "Close", {"windows": [0, 1, 2, 3]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(3)
        
        for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
            self.bgm_eth_inter.ck_signal_values(signal, [0, sig, sig, sig, 0, 0, sig, sig, sig, 0])
        
        # 无效信号时
        self.set_WinPosnSts(27)
        self.ck_moveinfo_event_and_resp(MoveSts.stop, check_event=False)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "Close", {"windows": [4]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(3)
        
        for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
            self.bgm_eth_inter.ck_signal_values(signal, [0, sig, sig, sig, 0, 0, sig, sig, sig, 0])
        
    @allure.title("设置车窗全关_当前为运动状态")
    @pytest.mark.sanity
    def test_caseid_1989222(self):
        sig = 1

        self.bgm_eth_inter.start_bgm_tcpdump()
        self.set_WinPosnSts(10)
        self.ck_moveinfo_event_and_resp(MoveSts.moving)
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "Close", {"windows": [0, 1, 2, 3]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(2)
        
        for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
            self.bgm_eth_inter.ck_signal_values(signal, [0, sig, sig, sig, 0, 0, sig, sig, sig, 0])
        

        self.set_WinPosnSts(11)
        self.ck_moveinfo_event_and_resp(MoveSts.moving)
        # 无效信号时
        self.set_WinPosnSts(27)
        self.ck_moveinfo_event_and_resp(MoveSts.moving, check_event=False)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "Close", {"windows": [4]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(2)
        
        for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
            self.bgm_eth_inter.ck_signal_values(signal, [0, sig, sig, sig, 0, 0, sig, sig, sig, 0])
              
    @allure.title("设置车窗停止_当前为idle状态")
    @pytest.mark.full
    def test_caseid_1989224(self): 
        sig = 26
        self.set_WinPosnSts(0)
        self.restart_bgm_and_connect_service(WINDOW_SERVICE_CLIENT)
        sleep(10)
        self.ck_moveinfo_event_and_resp(MoveSts.unknown, check_event=False, timeout=20)

        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetWindowStopCrtl", {"stopCmd": {"windowId":[0, 1, 2, 3]}})
        sleep(2)
        self.set_WinPosnSts(27)
        self.ck_moveinfo_event_and_resp(MoveSts.unknown, check_event=False)
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetWindowStopCrtl", {"stopCmd": {"windowId":[4]}})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(2)
        
        for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
            self.bgm_eth_inter.ck_signal_values(signal, [0, sig, sig, sig, 0, 0, sig, sig, sig, 0])
            
    @allure.title("设置车窗停止_当前为停止状态")
    @pytest.mark.sanity
    def test_caseid_1989226(self):
        self.set_WinPosnSts(10)
        self.ck_moveinfo_event_and_resp(MoveSts.stop)

        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetWindowStopCrtl", {"stopCmd": {"windowId":[0, 1, 2, 3]}})
        sleep(1)
        self.set_WinPosnSts(27)
        self.ck_moveinfo_event_and_resp(MoveSts.stop, check_event=False)
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetWindowStopCrtl", {"stopCmd": {"windowId":[4]}})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(2)
        
        for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
            self.bgm_eth_inter.ck_signal_values(signal, [])

    @allure.title("设置车窗停止_当前为运动状态")
    @pytest.mark.smoke
    def test_caseid_1989227(self):
        sig1 = 16
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.set_WinPosnSts(sig1)
        self.ck_moveinfo_event_and_resp(MoveSts.moving)
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetWindowStopCrtl",  {"stopCmd": {"windowId":[0, 1, 2, 3]}})
        sleep(2)
        
        sig2 = 1
        self.set_WinPosnSts(sig2)
        self.ck_moveinfo_event_and_resp(MoveSts.moving)
        # 无效信号时
        self.set_WinPosnSts(27)
        self.ck_moveinfo_event_and_resp(MoveSts.moving, check_event=False)
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetWindowStopCrtl", {"stopCmd": {"windowId":[4]}})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(2)
        
        for signal in ['WinOpenDrvrReq', 'WinOpenPassReq', 'WinOpenReLeReq', 'WinOpenReRiReq']:
            self.bgm_eth_inter.ck_signal_values(signal, [0, sig1, sig1, sig1, 0, 0, sig2, sig2, sig2, 0])
           

@allure.feature("SOA服务接口")
@allure.story("整车控制/WindowService")
class TestWindowServiceMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("WindowService", "client")])
        self.partner.wait_for_service_reconnect(WINDOW_SERVICE_CLIENT, timeout=30)    

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
    
    @allure.title("通知和获取下雨自动关窗请求状态_通过mockmcu遍历信号值0-3")
    @pytest.mark.full
    def test_caseid_1983479(self):
        sleep(5)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'WinGlbCmd1',0)
        sleep(1)
        for sigin in range(1,5):
            logger.info(f"--发送信号{sigin}")
            self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'WinGlbCmd1',sigin)
            sleep(0.5)
            self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT,
                                      "NotifyRainWinAutoCloseReqSts", {"reqSts": sigin})
            self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT,
                                      "GetRainWinAutoCloseReqSts", {},{"out": sigin})
    
    @pytest.mark.full
    @allure.title("通知下雨自动关窗请求状态重启场景_默认值和非默认值") 
    def test_caseid_1988822(self):
        for sts in [1, 0]:
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'WinGlbCmd1', sts)
            sleep(0.1)
            self.restart_bgm_and_connect_service(WINDOW_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT,"GetRainWinAutoCloseReqSts", {}, {"out": 0})            
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(WINDOW_SERVICE_CLIENT, "NotifyRainWinAutoCloseReqSts", {"reqSts": sts})
            self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT, "GetRainWinAutoCloseReqSts", {},{"out": sts})
