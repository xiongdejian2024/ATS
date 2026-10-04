#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_EntryService.py
@Time         :2023/04/30 19:07:31
@Author       :peipei.yang_ext@jiduauto.com
@Description  :
"""
import allure
import pytest
import os
import sys
from time import sleep

from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_ecu.legacy.sdk.driver.jidutest_io.io.io_system import IOSystem
from xat_ecu.legacy.interface.nuc_app import get_obd_ip

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
sys.path.append(os.path.join(os.getcwd(), "../../../.."))
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.ecu_sim.sd_tester import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *

NotifyTi = 1
ENTRY_SERVICE_CLIENT = "EntryService_client"
CENTRALLOCK_SERVICE_CLIENT = STEERWHEEL_SERVICE_CLIENT


@allure.feature("SOA服务接口")
@allure.story("整车控制/SteerWheelService")
@pytest.mark.ypp1
class TestSteerWheelService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("SteerWheelService", "client"),
                                     ("CarConfigService", "client"),
                                     ("ACCService", "server")])
        self.partner.method_default_timeout = 0.1
        time.sleep(5)
        self.curr_steer_angle = 0.0  # -3~3
        self.curr_steer_length = 0.0  # -25~30
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
        self.ipdu.rx_flag_reset_all()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTqQf', 3)  # 清除故障18
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3)  # 清除故障19
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 0},timeout = 2) 
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2')#L2长按短按按键故障
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2')
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2')
        self.ipdu.restore_crc(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTq')
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2')  # 1
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2')  # 1
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1')
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2')
        self.ipdu.lin1_wakeup()#唤醒lin1
        sleep(1)
        self.ipdu.set_vehspd(0)
        sleep(0.5)
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        self.set_steer_position(0.0, 0.0)  # 方向盘角度和长度是一个电机，先角度，再高度
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelButtonInhibit", {"opts": 0},timeout=2)
        self.partner.empty_all(0.5)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        self.ipdu.lin1_reset_wakeup()#停止唤醒
        time.sleep(1)
        super().after_each_func(ecu, start=False)

    def set_button_signal(self, ButtonMidRi1=None, ButtonMidRi2=None, LeftButtonRi=None, RightButtonRi=None,
                          ButtonMidLe1SteerWhlTouchSwt1=None, ButtonMidLe2SteerWhlTouchSwt2=None,
                          LeftButtonLeSteerWhlTouchSwt2=None, RightButtonLeSteerWhlTouchSwt2=None):
        if ButtonMidRi1 is not None:
            logger.info(f"设置ButtonMidRi1--{ButtonMidRi1}")
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', ButtonMidRi1)
        if ButtonMidRi2 is not None:
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi2', ButtonMidRi2)
        if LeftButtonRi is not None:
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScLeftButtonRi', LeftButtonRi)
        if RightButtonRi is not None:
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScRightButtonRi', RightButtonRi)
        if ButtonMidLe1SteerWhlTouchSwt1 is not None:
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1',
                          ButtonMidLe1SteerWhlTouchSwt1)
        if ButtonMidLe2SteerWhlTouchSwt2 is not None:
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2',
                          ButtonMidLe2SteerWhlTouchSwt2)
        if LeftButtonLeSteerWhlTouchSwt2 is not None:
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2',
                          LeftButtonLeSteerWhlTouchSwt2)
        if RightButtonLeSteerWhlTouchSwt2 is not None:
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2',
                          RightButtonLeSteerWhlTouchSwt2)

    def ck_steer_angle_control(self, exp_angle, pre_check=True):
        """
        校验方向盘角度控制
        @param exp_angle: 预期控制角度，float
        @param pre_check: 前提条件是否满足
        """
        logger.info(f"curr_steer_angle={self.curr_steer_angle}")
        if abs(self.curr_steer_angle - exp_angle) > 0.13 and pre_check:  # 至少差0.13(对应总线值13)才会触发控制
            if self.curr_steer_angle > exp_angle:  # 角度增加>>-3，Up
                self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtUpSts', 1, timeout=1)    
            else:
                self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtDwnSts', 1, timeout=1)
            # self.set_steer_position(angle=exp_angle)

        else:
            sleep(0.2)

    def ck_angle_idle(self, timeout=1.5):
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtUpSts', 0, timeout=timeout)
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtDwnSts', 0, timeout=1)

    def ck_steer_length_control(self, exp_length, pre_check=True):
        """
        校验方向盘长度控制
        @param exp_length: 预期控制长度，float
        @param pre_check: 前提条件是否满足
        """
        if abs(self.curr_steer_length - exp_length) > 1.3 and pre_check:  # 应该至少差1.3(对应总线值差13)才会触发控制
            if self.curr_steer_length < exp_length:  # 长度增加>>30，Backward
                self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 1, timeout=1)
            else:
                self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 1, timeout=1)
            self.set_steer_position(length=exp_length)
        else:
            sleep(0.2)

    def ck_length_idle(self, BackSts, FwdSts, UpSts, DwnSts, timeout=1.5):
        self.ipdu.check_multiple_signals([(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', BackSts),
                                          (self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', FwdSts),
                                           (self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtUpSts', UpSts),
                                            (self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtDwnSts', DwnSts)])
    
    def set_steer_position(self, angle: float = None, length: float = None):
        """
        设置方向盘角度和长度, 根据SteerWheelPositionChanged接口定义的转换为int类型给到总线上
        @param angle: 方向盘角度
        @param length: 方向盘长度
        """
        hint = ''
        if angle is not None:
            self.angle_can_signal = round((angle + 3.3375) / 0.0125)
            self.ipdu.set(self.ipdu.cem_lin4.AswmCem_Lin4Fr02, 'SteerWhlPosnAng', self.angle_can_signal)
            self.curr_steer_angle = angle
            hint += f"设置方向盘角度{angle}--总线值{self.angle_can_signal}"
        if length is not None:
            self.length_can_signal = round((length + 27.8) / 0.1)
            self.ipdu.set(self.ipdu.cem_lin4.AswmCem_Lin4Fr02, 'SteerWhlPosnX', self.length_can_signal)
            self.curr_steer_length = length
            hint += f" 设置方向盘长度{length}--总线值{self.length_can_signal}"
        logger.info(hint)
    
    def set_steer_position_venus(self, angle: float = None, length: float = None):
        """
        设置方向盘角度和长度, 根据SteerWheelPositionChanged接口定义的转换为int类型给到总线上
        @param angle: 方向盘角度
        @param length: 方向盘长度
        """
        hint = ''
        if angle is not None:
            self.angle_can_signal = round((angle + 3.3664) / 0.0229)
            self.ipdu.set(self.ipdu.cem_lin4.AswmCem_Lin4Fr02, 'SteerWhlPosnAng', self.angle_can_signal)
            self.curr_steer_angle = angle
            hint += f"设置方向盘角度{angle}--总线值{self.angle_can_signal}"
        if length is not None:
            self.length_can_signal = round((length + 28) / 0.2)
            self.ipdu.set(self.ipdu.cem_lin4.AswmCem_Lin4Fr02, 'SteerWhlPosnX', self.length_can_signal)
            self.curr_steer_length = length
            hint += f" 设置方向盘长度{length}--总线值{self.length_can_signal}"
        logger.info(hint)
        
    def set_stalk_status_init(self):
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2')
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2')
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 0)
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2') 
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 0)
        self.ipdu.restore_crc(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1')
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 0)
        self.partner.empty_all(1)
        
    def set_no_SteerWheelFault(self):
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1')
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 0)
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2')
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2', 0)
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2')
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2', 0)
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2')
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2', 0)
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2')
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2')
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 0)
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2')
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 0)
        self.ipdu.restore_crc(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1')
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 0)
        
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi2', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScRightButtonRi', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScLeftButtonRi', 0)
        sleep(1)

    @pytest.mark.sanity
    @allure.title("设置方向盘按键抑制&获取方向盘按键抑制&通知方向盘按键抑制")
    def test_caseid_108631(self):
        for x in list(range(4)) + [0]:
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelButtonInhibit", {"opts": x},timeout=1)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelButtonInhibit", {"opts": x})
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetSteerWheelButtonInhibit", {},
                                                  {"out": x}, timeout=2)

    @pytest.mark.full
    @allure.title("设置方向盘按键抑制&获取方向盘按键抑制_下电不记忆")
    def test_caseid_1980713(self):
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelButtonInhibit", {"opts": 1},timeout=1)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetSteerWheelButtonInhibit", {},
                                              {"out": 0}, timeout=2)

    @pytest.mark.full
    @allure.title("设置方向盘按键抑制_控制别的接口@value(1)kAdasInhibit")
    def test_caseid_1980299(self):
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelButtonInhibit", {"opts": 1},timeout=2)
        sleep(1)
        self.set_button_signal(ButtonMidRi1=0, ButtonMidRi2=0, ButtonMidLe2SteerWhlTouchSwt2=0)
        sleep(0.5)
        self.set_button_signal(ButtonMidRi1=1, ButtonMidRi2=1, ButtonMidLe2SteerWhlTouchSwt2=1)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "ADASButtonChanged")
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "ADASComplexButtonChanged")
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "NotifyADActivationButttonState")
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SimpleButtonChanged",
                                  {"infos": [{"buttonId": 1, "state": 1}]})
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', 1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ComplexButtonChanged",
                                  {"infos": [{"buttonId": 0, "state": 1}]})

    @pytest.mark.full
    @allure.title("设置方向盘按键抑制_控制别的接口@value(2)kNoneAdasInhibit ")
    def test_caseid_1980300(self):
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelButtonInhibit", {"opts": 2},timeout=1)
        sleep(1)
        self.set_button_signal(ButtonMidRi1=0, ButtonMidRi2=0, ButtonMidLe2SteerWhlTouchSwt2=0)
        sleep(0.5)
        self.set_button_signal(ButtonMidRi1=1, ButtonMidRi2=1, ButtonMidLe2SteerWhlTouchSwt2=1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ADASButtonChanged",
                                  {"infos": [{"buttonId": 1, "state": 1}]})
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ADASComplexButtonChanged",
                                  {"infos": [{"buttonId": 0, "state": 1}]})
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "NotifyADActivationButttonState", {"pressState": 1})
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SimpleButtonChanged")
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "ComplexButtonChanged")

    @pytest.mark.full
    @allure.title("设置方向盘按键抑制_控制别的接口@value(3)kAllInhibits")
    def test_caseid_1980301(self):
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelButtonInhibit", {"opts": 3},timeout=1)
        self.set_button_signal(ButtonMidRi1=0, ButtonMidRi2=0, ButtonMidLe2SteerWhlTouchSwt2=0)
        sleep(0.5)
        self.set_button_signal(ButtonMidRi1=1, ButtonMidRi2=1, ButtonMidLe2SteerWhlTouchSwt2=1)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "ADASButtonChanged")
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "ADASComplexButtonChanged")
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "NotifyADActivationButttonState")
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SimpleButtonChanged")
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "ComplexButtonChanged")

    @pytest.mark.sanity
    @allure.title("通知方向盘ADAS简单按键变化 测试")  
    def test_caseid_108585(self):
        self.set_button_signal(ButtonMidRi2=0, LeftButtonRi=0, RightButtonRi=0)
        sleep(0.1)
        for buttonId in [1, 2, 3]:
            for i in [1, 2, 3, 0]:
                self.set_button_signal(ButtonMidRi2=i if buttonId == 1 else None,
                                       LeftButtonRi=i if buttonId == 2 else None,
                                       RightButtonRi=i if buttonId == 3 else None)
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ADASButtonChanged",
                                          {"infos": [{"buttonId": buttonId, "state": i}]})

    @pytest.mark.smoke
    @allure.title("通知方向盘ADAS简单按键变化_驾驶辅助进入退出_E2E")  
    def test_caseid_1980260(self):
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2', 0)
        self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ADASButtonChanged",
                                  {"infos": [{"buttonId": 5, "state": 4}]})
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ADASButtonChanged",
                                  {"infos": [{"buttonId": 5, "state": 0}]})
        for i in [1, 2, 3, 0]:
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2', i)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ADASButtonChanged",
                                      {"infos": [{"buttonId": 5, "state": i}]})

    @pytest.mark.full
    @allure.title("通知方向盘ADAS简单按键变化_跟车距离调节-左_E2E")  
    def test_caseid_1980261(self):
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2', 0)
        self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ADASButtonChanged",
                                  {"infos": [{"buttonId": 6, "state": 4}]})
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ADASButtonChanged",
                                  {"infos": [{"buttonId": 6, "state": 0}]})
        for i in [1, 2, 3, 0]:
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2', i)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ADASButtonChanged",
                                      {"infos": [{"buttonId": 6, "state": i}]})

    @pytest.mark.full
    @allure.title("通知方向盘ADAS简单按键变化_跟车距离调节-右_E2E")  
    def test_caseid_1980262(self):
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2', 0)
        self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ADASButtonChanged",
                                  {"infos": [{"buttonId": 7, "state": 4}]})
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ADASButtonChanged",
                                  {"infos": [{"buttonId": 7, "state": 0}]})
        for i in [1, 2, 3, 0]:
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2', i)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ADASButtonChanged",
                                      {"infos": [{"buttonId": 7, "state": i}]})

    @pytest.mark.sanity
    @allure.title("通知方向盘ADAS复杂按键变化 测试") 
    def test_caseid_108582(self):
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', 0)
        self.partner.empty_all(0.5)
        for i in [1, 2, 3, 4, 5]:
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', i)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ADASComplexButtonChanged",
                                      {"infos": [{"buttonId": 0, "state": i}]})
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', 6)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "ADASComplexButtonChanged")
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', 7)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "ADASComplexButtonChanged")
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', 0)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ADASComplexButtonChanged",
                                  {"infos": [{"buttonId": 0, "state": 0}]})

    @pytest.mark.full
    @allure.title("通知方向盘ADAS复杂按键变化 测试_E2E") 
    def test_caseid_1980272(self):
        for i in [1, 2, 3, 4, 5]:
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', i)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ADASComplexButtonChanged",
                                      {"infos": [{"buttonId": 4, "state": i}]})
        self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ADASComplexButtonChanged",
                                  {"infos": [{"buttonId": 4, "state": 6}]})
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1')
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 6)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "ADASComplexButtonChanged")
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 7)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "ADASComplexButtonChanged")
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 0)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ADASComplexButtonChanged",
                                  {"infos": [{"buttonId": 4, "state": 0}]})

    @pytest.mark.sanity
    @allure.title("通知方向盘简单按键变化_ButtonId(1&2&3)")
    def test_caseid_108591(self):
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi2', 0)
        sleep(0.1)
        for i in [1, 2, 0]:
            logger.info(f"打印{i}")
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi2', i)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SimpleButtonChanged",
                                      {"infos": [{"buttonId": 1, "state": i}]})
        for x in [1, 2, 0]:
            logger.info(f"打印{x}")
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScLeftButtonRi', x)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SimpleButtonChanged",
                                      {"infos": [{"buttonId": 2, "state": x}]})
        for y in [1, 2, 0]:
            logger.info(f"打印{y}")
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScRightButtonRi', y)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SimpleButtonChanged",
                                      {"infos": [{"buttonId": 3, "state": y}]})

    @pytest.mark.smoke
    @allure.title("通知方向盘简单按键变化_ButtonId(5&6&7)")
    def test_caseid_1980281(self):
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi2', 0)
        sleep(0.1)
        for i in [1, 2, 0]:
            logger.info(f"打印{i}")
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2', i)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SimpleButtonChanged",
                                      {"infos": [{"buttonId": 5, "state": i}]})
        for x in [1, 2, 0]:
            logger.info(f"打印{x}")
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2', x)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SimpleButtonChanged",
                                      {"infos": [{"buttonId": 6, "state": x}]})
        for y in [1, 2, 0]:
            logger.info(f"打印{y}")
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2', y)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SimpleButtonChanged",
                                      {"infos": [{"buttonId": 7, "state": y}]})

    @pytest.mark.sanity
    @allure.title("通知方向盘复杂按键变化")
    def test_caseid_108648(self):
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', 0)
        self.partner.empty_all(0.5)
        for i in [1, 2, 3, 4, 0]:
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', i)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ComplexButtonChanged",
                                      {"infos": [{"buttonId": 0, "state": i}]})
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 0)
        for i in [1, 2, 3, 4, 0]:
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', i)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ComplexButtonChanged",
                                      {"infos": [{"buttonId": 4, "state": i}]})

    @pytest.mark.smoke
    @allure.title("方向盘位置调节&停止方向盘调节_条件满足可以调节")
    def test_caseid_1980292(self):
        def inner_test():
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection",
                                             {"direction": 0})  # 设置方向盘位置方向向前
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 1, timeout=0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StopMoveDirection",
                                             {"direction": 0})  # 停止方向盘位置方向向前
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 0, timeout=0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection",
                                             {"direction": 2})  # with allure.step("设置方向盘位置方向向上"):
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtUpSts', 1, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtDwnSts', 0, timeout=0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StopMoveDirection",
                                             {"direction": 2})  # 停止方向盘位置方向向上
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtUpSts', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtDwnSts', 0, timeout=0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection", {"direction": 3})  # 向后
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 1, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 0, timeout=0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StopMoveDirection",
                                             {"direction": 3})  # 停止方向盘位置方向向后
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 0, timeout=0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection",
                                             {"direction": 5})  # 设置方向盘位置向下
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtUpSts', 0, timeout=0.5) # 检查信号SteerAdjSwtUpSts值
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtDwnSts', 1, timeout=0.5) # 检查信号SteerAdjSwtDwnSts值"
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StopMoveDirection",
                                             {"direction": 5})  # 停止方向盘位置方向向下
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtUpSts', 0, timeout=0.5) # 检查信号SteerAdjSwtUpSts值
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtDwnSts', 0, timeout=0.5)
            self.ipdu.set_vehspd(0)

        self.ipdu.set_vehspd(0)  # with allure.step("设置车速小于1.994m/s")
        for car_mode in [0, 1, 2, 5]:
            self.sd_tester.change_car_mode(car_mode)
            inner_test()
        for usage_mode in [1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            inner_test()

    @pytest.mark.sanity
    @allure.title("方向盘位置调节_条件满足可以调节(先前再后)")#pass
    def test_caseid_1980447(self):
        self.ipdu.set_vehspd(0)  # with allure.step("设置车速小于1.994m/s")
        for car_mode in [0, 1, 2, 5]:
            self.sd_tester.change_car_mode(car_mode)
            logger.info(f"carmode模式为{car_mode}")
            for usage_mode in [1, 2, 11]:
                self.sd_tester.change_usage_mode(usage_mode)
                logger.info(f"usagemode模式为{usage_mode}")
                self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection",
                                                {"direction": 0})  # 设置方向盘位置方向向前
                sleep(1)
                self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 0, timeout=0.5)
                self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 1, timeout=0.5)
                self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection", {"direction": 3})  # 向后
                sleep(1)
                self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 1, timeout=0.5)
                self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 0, timeout=0.5)

    @pytest.mark.smoke
    @allure.title("方向盘位置调节_条件满足可以调节(先前再上)")#pass
    def test_caseid_1980452(self):
        def inner_test():
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection",
                                             {"direction": 0})  # 设置方向盘位置方向向前
            sleep(1)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 1, timeout=0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection", {"direction": 2})  # 向上
            sleep(1)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtUpSts', 1, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtDwnSts', 0, timeout=0.5)

        self.ipdu.set_vehspd(0)  # with allure.step("设置车速小于1.994m/s")
        for car_mode in [0, 1, 2, 5]:
            self.sd_tester.change_car_mode(car_mode)
            inner_test()
        for usage_mode in [1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            inner_test()

    @pytest.mark.smoke
    @allure.title("方向盘位置调节_方向盘位置调节&设置目标位置&停止方向盘")#pass
    def test_caseid_1980449(self):
        def inner_test():
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection",
                                             {"direction": 0})  # 设置方向盘位置方向向前
            sleep(1)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 1, timeout=0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                             {"position": {"angle": -3, "length": -25}})  # 设置方向盘目标位置
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StopMoveDirection",
                                             {"direction": 0})  # 停止方向盘位置方向向前
            sleep(1)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 0, timeout=0.5)

        self.ipdu.set_vehspd(0)  # with allure.step("设置车速小于1.994m/s")
        for car_mode in [0, 1, 2, 5]:
            self.sd_tester.change_car_mode(car_mode)
            inner_test()
        for usage_mode in [1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            inner_test()

    @pytest.mark.full
    @allure.title("方向盘位置调节_方向盘位置调节&设置目标位置&停止方向盘(所有方向)")#pass
    def test_caseid_1980450(self):
        def inner_test():
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection",
                                             {"direction": 0})  # 设置方向盘位置方向向前
            sleep(1)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 1, timeout=0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                             {"position": {"angle": -3, "length": -25}})  # 设置方向盘目标位置
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection",
                                             {"direction": 3})  # 设置方向盘位置方向向前
            sleep(1)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 1, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 0, timeout=0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StopMove", {})
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 0, timeout=0.5)

        self.ipdu.set_vehspd(0)  # with allure.step("设置车速小于1.994m/s")
        for car_mode in [0, 1, 2, 5]:
            self.sd_tester.change_car_mode(car_mode)
            inner_test()
        for usage_mode in [1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            inner_test()

    @pytest.mark.full
    @allure.title("方向盘位置调节_打断逻辑(前置条件不满足(carmode模式))")# PASS
    def test_caseid_1980463(self):
        self.sd_tester.change_car_mode(3)  # "设置前提条件:CarMode == Dynamometer"
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set_vehspd(0)  # with allure.step("设置车速小于1.994m/s"):
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection",
                                         {"direction": 0})
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtUpSts', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtDwnSts', 0, timeout=0.5)

    @pytest.mark.full
    @allure.title("方向盘位置调节_打断逻辑(usagemode模式不满足)")  # PASS
    def test_caseid_1913752(self):
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.change_car_mode(1)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(0)  # with allure.step("设置车速小于1.994m/s"):
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection",
                                         {"direction": 2})  # with allure.step("设置方向盘位置方向向上"):

        self.sd_tester.change_usage_mode(0)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("SteerAdjSwtBackSts", [0])
        self.bgm_eth_inter.ck_ordered_array("SteerAdjSwtBackSts", [0])
        self.bgm_eth_inter.ck_ordered_array("SteerAdjSwtFwdSts", [0])
        self.bgm_eth_inter.ck_ordered_array("SteerAdjSwtDwnSts", [0])

    @pytest.mark.full
    @allure.title("方向盘位置调节_打断逻辑(前置条件(usagemode模式不满足))")
    def test_caseid_1980467(self):
        info = ["SteerAdjSwtBackSts","SteerAdjSwtFwdSts","SteerAdjSwtUpSts","SteerAdjSwtDwnSts"]
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection",
                                         {"direction": 2})#向上调节
        self.sd_tester.change_usage_mode(0)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        for i in range(4):
            assert self.bgm_eth_inter.get_signal_values(info[i])[-1] == 0

    @pytest.mark.full
    @allure.title("方向盘位置调节_打断逻辑(先设置位置调节_车速不满足)")#pass
    def test_caseid_1980446(self):
        info = ["SteerAdjSwtBackSts","SteerAdjSwtFwdSts","SteerAdjSwtUpSts","SteerAdjSwtDwnSts"]
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(0)  # with allure.step("设置车速小于1.994m/s"):
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection",
                                         {"direction": 2})  # with allure.step("设置方向盘位置方向向上"):
        self.ipdu.set_vehspd(1.4)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        for i in range(4):
            assert self.bgm_eth_inter.get_signal_values(info[i])[-1] == 0

    @pytest.mark.full
    @allure.title("方向盘位置调节_前置条件不满足(车速)")#pass
    def test_caseid_1980468(self):
        self.sd_tester.change_car_mode(1)
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set_vehspd(1.4)
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection",
                                         {"direction": 3})
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtUpSts', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtDwnSts', 0, timeout=0.5)

    @pytest.mark.smoke
    @allure.title("方向盘位置调节&停止方向盘调节(所有方向)_条件满足可以调节")  # pass
    def test_caseid_1980294(self):
        # todo 开始抓包
        file_path, save_name = self.bgmcli.start_bgm_tcpdump()

        def inner_test():
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection",
                                             {"direction": 0})  # 设置方向盘位置方向向前
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 1, timeout=0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection",
                                             {"direction": 2})  # with allure.step("设置方向盘位置方向向上"):
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtUpSts', 1, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtDwnSts', 0, timeout=0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection", {"direction": 3})  # 向后
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 1, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 0, timeout=0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection",
                                             {"direction": 5})  # 设置方向盘位置向下
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtUpSts', 0, timeout=0.5) # 检查信号SteerAdjSwtUpSts值
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtDwnSts', 1, timeout=0.5) # 检查信号SteerAdjSwtDwnSts值"
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StopMove", {})
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtUpSts', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtDwnSts', 0, timeout=0.5)

        self.ipdu.set_vehspd(0)  # with allure.step("设置车速小于1.994m/s")
        sleep(0.2)
        for car_mode in [0, 1, 2, 5]:
            self.sd_tester.change_car_mode(car_mode)
            inner_test()
        for usage_mode in [1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            inner_test()
        sleep(2)
        data_list = [(6001, 2, 0, 1), (6001, 2, 8, 1), (6002, 2, 0, 1), (6002, 2, 8, 1)]
        res_dict = self.stop_tcpdump_and_copy_and_calculate(save_name, data_list)#停止抓包

    @pytest.mark.sanity
    @allure.title("设置方向盘目标位置_角度|长度由小变大_Mars1")
    def test_caseid_111333(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.ipdu.set_vehspd(0)  
        for car_mode in [0, 1, 2, 5]:
            self.sd_tester.change_car_mode(car_mode)
            logger.info(f"carmode模式为{car_mode}")
            for usage_mode in [1, 2, 11]:
                self.sd_tester.change_usage_mode(usage_mode)
                logger.info(f"usagemode模式为{usage_mode}")
                self.set_steer_position(2.0, 0.0)
                self.partner.empty_all(1)
                self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                                    {"position": {"angle": 3.0, "length": 25.0}},{"out":1}) 
                sleep(1)
                self.ck_length_idle(0, 0, 0, 1)
                self.set_steer_position(angle=3)
                self.ck_length_idle(1, 0, 0, 0)
                self.set_steer_position(length=25)
    
    @pytest.mark.full
    @allure.title("设置方向盘目标位置_角度|长度由大变小_Mars1")
    def test_caseid_1987246(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.ipdu.set_vehspd(0)  
        for car_mode in [0, 1, 2, 5]:
            self.sd_tester.change_car_mode(car_mode)
            logger.info(f"模式为{car_mode}")
            self.sd_tester.change_usage_mode(13)
            self.set_steer_position(3.0, 25.0)
            self.partner.empty_all(1)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                                {"position": {"angle": -3.0, "length": -1.0}},{"out":1}) 
            sleep(1)
            self.ck_length_idle(0, 0, 1, 0)
            self.set_steer_position(angle=-3)
            self.ck_length_idle(0, 1, 0, 0)
            self.set_steer_position(length=-25)
            self.sd_tester.change_usage_mode(1)
    
    @pytest.mark.smoke
    @allure.title("设置方向盘目标位置_打断逻辑(carmode从满足到不满足)_Mars1")
    def test_caseid_1980416(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.ipdu.set_vehspd(0) 
        for usage_mode in [1, 2, 11]:
            self.sd_tester.change_usage_mode(usage_mode)
            logger.info(f"模式为{usage_mode}")
            self.sd_tester.change_car_mode(0)
            self.set_steer_position(2.0, 0.0)
            self.partner.empty_all(1)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                                {"position": {"angle": 3.0, "length": 25.0}},{"out":1}) 
            sleep(1)
            self.ck_length_idle(0, 0, 0, 1)
            self.sd_tester.change_car_mode(3)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                                {"position": {"angle": 0.0, "length": 0.0}},{"out":0})
            self.ck_length_idle(0, 0, 0, 0)
    
    @pytest.mark.full
    @allure.title("设置方向盘目标位置_打断逻辑(usagemode从满足到不满足)_Mars1")
    def test_caseid_1980417(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.sd_tester.change_car_mode(1)
        self.ipdu.set_vehspd(0) 
        for usage_mode in [1, 2, 11]:
            logger.info(f"模式为{usage_mode}")
            self.sd_tester.change_usage_mode(usage_mode)
            self.set_steer_position(2.0, 0.0)
            self.partner.empty_all(1)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                                {"position": {"angle": 3.0, "length": 25.0}},{"out":1}) 
            sleep(1)
            self.ck_length_idle(0, 0, 0, 1)
            self.set_steer_position(3.0, 25.0)
            sleep(1)
            self.sd_tester.change_usage_mode(0)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                                {"position": {"angle": 0.0, "length": 0.0}},{"out":0})
            self.ck_length_idle(0, 0, 0, 0)
    
    @pytest.mark.full
    @allure.title("设置方向盘目标位置_打断逻辑(车速从满足到不满足)_Mars1")
    def test_caseid_1980418(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set_vehspd(0) 
        self.set_steer_position(2.0, 0.0)
        self.partner.empty_all(1)
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                            {"position": {"angle": 3.0, "length": 25.0}},{"out":1}) 
        sleep(1)
        self.ck_length_idle(0, 0, 0, 1)
        self.ipdu.set_vehspd(3.0)
        sleep(1)
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                            {"position": {"angle": 0.0, "length": 0.0}},{"out":0})
        self.ck_length_idle(0, 0, 0, 0)
    
    @pytest.mark.full
    @allure.title("设置方向盘目标位置_打断逻辑(前置条件(carmode不满足))_Mars1")
    def test_caseid_1980473(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.ipdu.set_vehspd(0) 
        self.sd_tester.change_car_mode(3)
        for usage_mode in [1, 2, 11]:
            self.sd_tester.change_usage_mode(usage_mode)
            logger.info(f"usagemode模式为{usage_mode}")
            self.set_steer_position(2.0, 0.0)
            self.partner.empty_all(1)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                                {"position": {"angle": 3.0, "length": 25.0}},{"out":0}) 
            sleep(1)
            self.ck_length_idle(0, 0, 0, 0)
    
    @pytest.mark.full
    @allure.title("设置方向盘目标位置_打断逻辑(前置条件(usagemode不满足))_Mars1")
    def test_caseid_1980474(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.ipdu.set_vehspd(0) 
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(0)
        self.set_steer_position(2.0, 0.0)
        self.partner.empty_all(1)
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                            {"position": {"angle": 3.0, "length": 25.0}},{"out":0}) 
        sleep(1)
        self.ck_length_idle(0, 0, 0, 0)
    
    @pytest.mark.full
    @allure.title("设置方向盘目标位置_打断逻辑(前置条件(车速不满足))_Mars1")
    def test_caseid_1980475(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.ipdu.set_vehspd(3.0) 
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.set_steer_position(2.0, 0.0)
        self.partner.empty_all(1)
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                            {"position": {"angle": 3.0, "length": 25.0}},{"out":0}) 
        sleep(1)
        self.ck_length_idle(0, 0, 0, 0)
    
    @pytest.mark.full
    @allure.title("设置方向盘目标位置_差值范围_10s可控_Mars1")
    def test_caseid_1980457(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.ipdu.set_vehspd(0) 
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.set_steer_position(2.0, 0.0)
        self.partner.empty_all(1)
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                            {"position": {"angle": 3.0, "length": 25.0}},{"out":1}) 
        sleep(7)
        self.ck_length_idle(0, 0, 0, 1)
        sleep(4)
        self.ck_length_idle(0, 0, 0, 0)
    
    @pytest.mark.full
    @allure.title("设置方向盘目标位置_差值范围无需控制_Mars1")
    def test_caseid_1980454(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.ipdu.set_vehspd(0) 
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.set_steer_position(2.0, 0.0)
        self.partner.empty_all(1)
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                            {"position": {"angle": 2.01, "length": 0.005}},{"out":1}) 
        sleep(1)
        self.ck_length_idle(0, 0, 0, 0)
    
    @pytest.mark.full
    @allure.title("设置方向盘目标位置_打断逻辑(方向盘位置调节接口调用不控制)_Mars1")
    def test_caseid_1980419(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.ipdu.set_vehspd(0) 
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.set_steer_position(2.0, 0.0)
        self.partner.empty_all(1)
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                            {"position": {"angle": 2.5, "length": 0.5}},{"out":1}) 
        sleep(1)
        self.ck_length_idle(0, 0, 0, 1)
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StopMoveDirection",
                                             {"direction": 2})
        self.ck_length_idle(0, 0, 0, 0)
    
    @pytest.mark.full
    @allure.title("设置方向盘目标位置_打断逻辑(停止方向盘调节(所有方向) 接口调用不控制)_Mars1")
    def test_caseid_1987247(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.ipdu.set_vehspd(0) 
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.set_steer_position(2.0, 0.0)
        self.partner.empty_all(1)
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                            {"position": {"angle": 2.5, "length": 0.5}},{"out":1}) 
        sleep(1)
        self.ck_length_idle(0, 0, 0, 1)
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StopMove", {})
        self.ck_length_idle(0, 0, 0, 0)
    
    @pytest.mark.full
    @allure.title("启动场景_设置方向盘目标位置_前置条件不满足_2s超时条件满足_能立马返回Fasle_Mars1")
    def test_caseid_1987198(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(1.5)
        sleep(0.5)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        t1 = time.time()
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                             {"position": {"angle": 0, "length": 0}},{"out":0}, timeout=2) 
        t2 = time.time()
        assert abs(float(t2) - float(t1) ) < 0.5
    
    @pytest.mark.full
    @allure.title("启动场景_设置方向盘目标位置_前置条件不满足_2s超时条件满足_能立马返回True_Mars1")
    def test_caseid_1987199(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(1.3)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        t1 = time.time()
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                             {"position": {"angle": 0, "length": 0}},{"out":1}, timeout=2) 
        t2 = time.time()
        assert abs(float(t2) - float(t1) ) < 1
    
    @pytest.mark.smoke
    @allure.title("启动场景_设置方向盘目标位置_2s内超时内条件满足_立马进行控制_Mars1")#
    def test_caseid_1987183(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(0)
        self.set_steer_position(0.0, 0.0)
        self.partner.empty_all(1)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(2)
        time1 = time.time()
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                                    {"position": {"angle": 3, "length": 25}},{"out":1}, timeout=2) 
        self.ck_length_idle(0, 0, 0, 1)
        self.set_steer_position(angle=3)
        self.ck_length_idle(1, 0, 0, 0)
    
    @pytest.mark.full
    @allure.title("设置方向盘目标位置2s内超时内不满足_重启后信号没来场景_不进行控制_Mars1")#条件不满足场景
    def test_caseid_1987184(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(1.3)
        self.ipdu.pause_ecu_send("cem_lin4","ASWM")
        sleep(1)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT, resume_all_bus=False)
        sleep(2)
        self.partner.empty_all()
        self.ipdu.resume_ecu_send("cem_lin4","ASWM")
        sleep(1)
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                                    {"position": {"angle": 3, "length": 25}},{"out":1}, timeout=2) 
        self.ck_length_idle(0, 0, 0, 0)
    
    @pytest.mark.full
    @allure.title("设置方向盘目标位置_重启后仅单个信号来场景_Mars1")#信号恢复后只有角度发生变化
    def test_caseid_1987224(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(1.3)
        self.set_steer_position(angle=3)
        self.ipdu.pause_ecu_send("cem_lin4","ASWM")
        sleep(1)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                             {"position": {"angle": 1.0, "length": 0}},{"out":1},timeout=1) 
        self.ck_length_idle(0, 0, 0, 0)
        self.ipdu.resume_all_bus_send()
        sleep(1)
        self.ck_length_idle(0, 0, 1, 0)
    
    @pytest.mark.full
    @allure.title("设置方向盘目标位置_SteerWhlPosnAng角度不在范围内_不进行控制_Mars1")
    def test_caseid_1987225(self):
        self.sd_tester.write_single_ccp(950, 1)
        sleep(2)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(1.3)
        for i in [0,1,540,541]:
            logger.info(f"i={i}")
            self.set_steer_position(length=0)
            self.ipdu.set(self.ipdu.cem_lin4.AswmCem_Lin4Fr02, 'SteerWhlPosnAng',i)
            sleep(0.5)
            #angle 相当于信号值267
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                                    {"position": {"angle": 0, "length": 0}},{"out":1},timeout=1) 
            #保证下行信号已变化
            sleep(2)
            if i in [0,1]:
                self.ck_length_idle(0, 0, 0, 1)
            elif i == 540:
                self.ck_length_idle(0, 0, 1, 0)
            else:
                self.ck_length_idle(0, 0, 0, 0)
            self.set_steer_position(length=0)
            sleep(1)     
             
    @pytest.mark.full
    @allure.title("设置方向盘目标位置_SteerWhlPosnX长度不在范围内_不进行控制_Mars1")
    def test_caseid_1987226(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(1.3)
        for i in [0,1,615,616]:
            logger.info(f"i={i}")
            self.set_steer_position(angle=2) 
            sleep(0.5)
            self.ipdu.set(self.ipdu.cem_lin4.AswmCem_Lin4Fr02, 'SteerWhlPosnX',i)
            sleep(0.5)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                                    {"position": {"angle": 3, "length": 0}},{"out":1})
            self.ck_length_idle(0, 0, 0, 1)
            self.set_steer_position(angle=3) 
            sleep(2)
            if i in [0,1]:
                self.ck_length_idle(1, 0, 0, 0)
            elif i == 615:
                self.ck_length_idle(0, 1, 0, 0)
            else:
                self.ck_length_idle(0, 0, 0, 0)
            self.set_steer_position(length=0)
            sleep(0.5)
           
    @allure.title("非启动场景_设置方向盘目标位置长度信号没来_无需阻塞2s进行控制_Mars1")
    @pytest.mark.full
    def test_caseid_1987227(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(1.3)
        self.set_steer_position(angle=2.8)
        sleep(0.5)
        self.ipdu.pause_ecu_send("cem_lin4","ASWM")
        sleep(1)
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                             {"position": {"angle": 1.0, "length": 0}},{"out":1}) 
        self.ck_length_idle(0, 0, 1, 0)
        self.ipdu.resume_all_bus_send()
    
    @pytest.mark.full
    @allure.title("启动场景_设置方向盘目标位置_前置条件不满足_2s超时条件满足_能立马返回Fasle_Venus")
    def test_caseid_1987234(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(1.5)
        sleep(0.5)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        t1 = time.time()
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                             {"position": {"angle": 0, "length": 0}},{"out":0}, timeout=2) 
        t2 = time.time()
        assert abs(float(t2) - float(t1) ) < 0.5
    
    @pytest.mark.full
    @allure.title("启动场景_设置方向盘目标位置_前置条件不满足_2s超时条件满足_能立马返回True_Venus")
    def test_caseid_1987232(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(1.3)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        t1 = time.time()
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                             {"position": {"angle": 0, "length": 0}},{"out":1}, timeout=2) 
        t2 = time.time()
        assert abs(float(t2) - float(t1) ) < 0.5
    
    @pytest.mark.smoke
    @allure.title("启动场景_设置方向盘目标位置_2s内超时内条件满足_立马进行控制_Venus")#
    def test_caseid_1987228(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(0)
        self.set_steer_position_venus(0.0, 0.0)
        self.partner.empty_all(1)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(2)
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                                    {"position": {"angle": 3, "length": 25}},{"out":1}, timeout=2) 
        self.ck_length_idle(0, 0, 0, 1)
        self.set_steer_position_venus(angle=3)
        sleep(0.5)
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtUpSts', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtDwnSts', 0, timeout=0.5)
        # self.ck_length_idle(1, 0, 0, 0)
    
    @pytest.mark.full
    @allure.title("设置方向盘目标位置2s内超时内不满足_重启后信号没来场景_不进行控制_Venus")#条件不满足场景
    def test_caseid_1987231(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(1.3)
        self.ipdu.pause_ecu_send("cem_lin4","ASWM")
        sleep(1)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT, resume_all_bus=False)
        sleep(2)
        self.partner.empty_all()
        self.ipdu.resume_ecu_send("cem_lin4","ASWM")
        sleep(1)
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                                    {"position": {"angle": 3, "length": 25}},{"out":1}, timeout=2) 
        self.ck_length_idle(0, 0, 0, 0)
    
    @pytest.mark.full
    @allure.title("设置方向盘目标位置_重启后仅单个信号来场景_Venus")#信号恢复后只有角度发生变化
    def test_caseid_1987233(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(1.3)
        self.set_steer_position_venus(angle=3)
        sleep(0.5)
        self.ipdu.pause_ecu_send("cem_lin4","ASWM")
        sleep(1)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT,pause_all_bus=True, resume_all_bus=False)
        sleep(2)
        self.partner.empty_all()
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                             {"position": {"angle": 1.0, "length": 0}},{"out":1}) 
        self.ck_length_idle(0, 0, 0, 0)
        self.ipdu.resume_all_bus_send()
        sleep(1)
        self.ck_length_idle(0, 0, 1, 0)
    
    @pytest.mark.full
    @allure.title("设置方向盘目标位置_SteerWhlPosnAng角度不在范围内_不进行控制_Venus")
    def test_caseid_1987230(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(1.3)
        for i in [0,1,310,311]:
            logger.info(f"i={i}")
            self.set_steer_position_venus(length=0)
            self.ipdu.set(self.ipdu.cem_lin4.AswmCem_Lin4Fr02, 'SteerWhlPosnAng',i)
            sleep(0.5)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                                    {"position": {"angle": 0, "length": 0}},{"out":1}) 
            sleep(2)
            if i in [0,1]:
                self.ck_length_idle(0, 0, 0, 1)
            elif i == 310:
                self.ck_length_idle(0, 0, 1, 0)
            else:
                self.ck_length_idle(0, 0, 0, 0)
            self.set_steer_position_venus(length=0)
            sleep(1)
    
    @pytest.mark.full
    @allure.title("设置方向盘目标位置_SteerWhlPosnX长度不在范围内_不进行控制_Venus")
    def test_caseid_1987235(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(1.3)
        for i in [0,1,317,318]:
            logger.info(f"i={i}")
            self.set_steer_position_venus(angle=2) 
            self.ipdu.set(self.ipdu.cem_lin4.AswmCem_Lin4Fr02, 'SteerWhlPosnX',i)
            #框架发送lin信号偶尔会晚一点，这里等待时间加长
            sleep(2)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                                    {"position": {"angle": 3, "length": 0}},{"out":1})
            self.ck_length_idle(0, 0, 0, 1)
            self.set_steer_position_venus(angle=3) 
            sleep(2)
            if i in [0,1]:
                self.ck_length_idle(1, 0, 0, 0)
            elif i == 317:
                self.ck_length_idle(0, 1, 0, 0)
            else:
                self.ck_length_idle(0, 0, 0, 0)
            self.set_steer_position_venus(length=0)
            # self.set_steer_position_venus(angle=2) 
            # self.ipdu.set(self.ipdu.cem_lin4.AswmCem_Lin4Fr02, 'SteerWhlPosnX',i)
            sleep(0.5)
            
    @allure.title("非启动场景_设置方向盘目标位置长度信号没来_无需阻塞2s进行控制_Venus")
    @pytest.mark.full
    def test_caseid_1987229(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(1.3)
        self.set_steer_position_venus(angle=3)
        sleep(0.5)
        self.ipdu.pause_ecu_send("cem_lin4","ASWM")
        sleep(1)
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                             {"position": {"angle": 1.0, "length": 0}},{"out":1}) 
        self.ck_length_idle(0, 0, 1, 0)
        self.ipdu.resume_all_bus_send()
    
    @pytest.mark.full
    @allure.title("启动场景_设置方向盘目标位置_配置字不满足条件_不进行控制")#
    def test_caseid_1987236(self):
        self.sd_tester.write_single_ccp(950, 3)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(0)
        self.set_steer_position_venus(0.0, 0.0)
        self.partner.empty_all(1)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(2)
        time1 = time.time()
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelPositionTarget",
                                                    {"position": {"angle": 3, "length": 25}},{"out":1}, timeout=2) 
        self.ck_length_idle(0, 0, 0, 0)

    @pytest.mark.smoke
    @allure.title("获取通知方向盘位置&通知方向盘位置_角度+长度")#Mars1
    def test_caseid_1980413(self):
        self.sd_tester.write_single_ccp(950, 1)
        sleep(1)
        for angle in [-2.9, 1.8, -1.7, 3]:
            self.set_steer_position(angle=angle)
            sleep(0.5)
            logger.info(f"信号为{angle}")
            for length in [-25.0, 29.9, 0]:
                logger.info(f"信号为{length}")
                self.set_steer_position(length=length)
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelPositionChanged",
                                          {"position": {"angle": angle, "length": length}})
                self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetSteerWheelPosition", {},
                                                 {"out": {"angle": angle, "length": length}})
    
    @pytest.mark.full
    @allure.title("获取通知方向盘位置&通知方向盘位置_角度+长度")#Venus
    def test_caseid_1984527(self):
        self.sd_tester.write_single_ccp(950, 2)
        sleep(1)
        for angle in [-2.9, 1.79, -1.7, 3]:
            self.set_steer_position(angle=angle)
            logger.info(f"信号为{angle}")
            for length in [-25.0, 29.9, 0]:
                logger.info(f"信号为{length}")
                self.set_steer_position(length=length)
                exp_angle = self.angle_can_signal * 0.0229 - 3.3664
                exp_length = self.length_can_signal * 0.2-28
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelPositionChanged",
                                          {"position": {"angle": exp_angle, "length": exp_length}})
                self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetSteerWheelPosition", {},
                                                 {"out": {"angle": exp_angle, "length": exp_length}})
                
    @pytest.mark.full
    @allure.title("获取通知方向盘位置&通知方向盘位置_角度+长度_默认值")#Venus
    def test_caseid_1985546(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_steer_position(angle=0)
        self.set_steer_position(length=0)
        self.partner.empty_all(0.5)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetSteerWheelPosition", {}, {"out": {"angle": 0, "length": 0}},timeout = 2)
        self.ipdu.resume_all_bus_send()
        exp_angle = self.angle_can_signal * 0.0229 - 3.3664
        exp_length = self.length_can_signal * 0.2-28
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelPositionChanged",
                                    {"position": {"angle": exp_angle, "length": exp_length}})
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetSteerWheelPosition", {},
                                            {"out": {"angle": exp_angle, "length": exp_length}})

    @pytest.mark.sanity
    @allure.title("设置方向盘加热等级_远程方向盘加热")
    def test_caseid_1980309(self):
        for usage_mode in [0, 1]:
            self.sd_tester.change_usage_mode(usage_mode)
            for Y in range(4):
                # todo 开始抓包
                self.bgm_eth_inter.start_bgm_tcpdump()
                logger.info(f"加热等级为{Y}")
                self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": Y})  # 设置方向盘加热等级一档
                sleep(2)
                self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
                self.bgm_eth_inter.ck_signal_values("TelmSteerWhlHeatgReqLvl", [Y, Y, Y, Y, Y])
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr36, 'TelmSteerWhlHeatgReqLvl', Y)
                
    @pytest.mark.full
    @allure.title("设置方向盘加热等级_远程方向盘加热_打断")
    def test_caseid_1980310(self):
        for usage_mode in [0, 1]:
            self.sd_tester.change_usage_mode(usage_mode)
            # todo 开始抓包
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 1})  # 设置方向盘加热等级一档
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 2})
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 3})
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_signal_values("TelmSteerWhlHeatgReqLvl", [1, 2, 3, 3, 3, 3, 3])

    @pytest.mark.smoke
    @allure.title("设置方向盘加热等级_本地方向盘加热")
    def test_caseid_1980311(self):
        for usage_mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            for Y in range(4):
                # todo 开始抓包
                self.bgm_eth_inter.start_bgm_tcpdump()
                logger.info(f"加热等级为{Y}")
                self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": Y})  # 设置方向盘加热等级一档
                sleep(2)
                self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
                self.bgm_eth_inter.ck_signal_values("SteerWhlHeatgOnReq", [Y])

    @pytest.mark.full
    @allure.title("设置方向盘加热等级_本地方向盘加热")
    def test_caseid_1980312(self):
        self.sd_tester.write_single_ccp(186, 2)
        for usage_mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            # todo 开始抓包
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 1}) 
            sleep(0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 0})  
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_signal_values("SteerWhlHeatgOnReq", [1, 0])

    @pytest.mark.full
    @allure.title("设置方向盘加热等级_本地方向盘加热_UsageMode从convenience以上→Abandoned/inactive时")#对应需求3. 当UsageMode从convenience及以上→Abandoned/inactive时，需要增加以下处理逻辑
    def test_caseid_1980313(self):
        self.sd_tester.write_single_ccp(186, 2)
        for usage_mode in [2, 11, 13]:
            logger.info(f"模式为{usage_mode}")
            self.sd_tester.change_usage_mode(usage_mode)
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 0})  # 设置方向盘加热等级一档
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', 0)
            self.sd_tester.change_usage_mode(1)
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_signal_values("SteerWhlHeatgOnReq", [0, 0])

    @pytest.mark.full
    @allure.title("设置方向盘加热等级_本地方向盘加热")  # Mcu逻辑10s后自动关闭
    def test_caseid_1981114(self):
        self.sd_tester.change_usage_mode(2)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 1})  # 设置方向盘加热等级一档
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SteerWhlHeatgOnReq", [1])

    @pytest.mark.full
    @allure.title("设置方向盘加热等级_本地方向盘加热_UsageMode为Convenience及以上时")  # v1.4
    def test_caseid_1981115(self):
        self.sd_tester.write_single_ccp(186, 2)
        for usage_mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            # todo 开始抓包
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 1})  # 设置方向盘加热等级一档
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_signal_values("SteerWhlHeatgOnReq", [1])

    @pytest.mark.smoke
    @allure.title("获取|通知方向盘加热等级_远程方向盘加热")
    def test_caseid_1980314(self):
        self.sd_tester.write_single_ccp(186, 2)
        self.bgm_eth_inter.start_bgm_tcpdump()
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            logger.info(f"使用者模式为{X}")
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 0,"source": 1})
            sleep(0.5)
            for Y in range(1, 4):
                logger.info(f"加热等级为{Y}")
                self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": Y,"source": 1})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SteerWhlHeatgOnReq", [0,1,2,3,0,1,2,3,0,1,2,3])      
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 0})
     
    @pytest.mark.sanity
    @allure.title("获取|通知转向扭矩状态")
    def test_caseid_108587(self):
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTq', 0)
        self.partner.empty_all(0.5)
        for X in [0, 1, 2, 3]:
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTqQf',
                          X)
            if X in [1, 2, 0]:
                X = False
            else:
                X = True
            for Y in [-30.0, 30.0, -10.0, 0.0]:
                logger.info(f'发到{Y}')
                self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTq', Y)
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Torque",
                                          {"fTorque": {"torque": Y, "isvalid": X}})
                self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetTorqueInfo", {},
                                                      {"out": {"torque": Y, "isvalid": X}})

    @pytest.mark.full
    @allure.title("获取|通知转向扭矩状态_通讯故障_UsgModSts = 0/1/2_默认值")
    def test_caseid_1980322(self):
        for X in range(3):
            self.sd_tester.change_usage_mode(X)
            logger.info(f'发到{X}')
            self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetTorqueInfo", {},
                                                  {"out": {"torque": 0.0, "isvalid": False}},timeout = 0.5)
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Torque",
                                          {"fTorque": {"torque": 0.0, "isvalid": True}})
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetTorqueInfo", {},
                                                  {"out": {"torque": 0.0, "isvalid": True}},timeout = 2)

    @pytest.mark.full
    @allure.title("获取|通知转向扭矩状态_通讯故障_UsgModSts = 0/1/2_记忆值")
    def test_caseid_1980323(self):
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTqQf',
                      3)
        sleep(0.2)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTq', 30.0)
        sleep(0.2)
        for X in [0, 1, 2]:
            self.sd_tester.change_usage_mode(X)
            logger.info(f"usgmode={X}")
            self.ipdu.pause_bus_send("chassiscan1")
            sleep(0.2)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetTorqueInfo", {},
                                                  {"out": {"torque": 30.0, "isvalid": True}}, timeout=2)
            self.ipdu.resume_bus_send("chassiscan1")
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetTorqueInfo", {},
                                                  {"out": {"torque": 30.0, "isvalid": True}}, timeout=2)

    @pytest.mark.full
    @allure.title("获取|通知转向扭矩状态_通讯故障_UsgModSts = 11/13_默认值")
    def test_caseid_1980325(self):
        for X in [11, 13]:
            self.sd_tester.change_usage_mode(X)
            logger.info(f"usgmode={X}")
            self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetTorqueInfo", {},
                                                  {"out": {"torque": 0.0, "isvalid": False}},timeout = 0.5)
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Torque",
                                          {"fTorque": {"torque": 30.0, "isvalid": True}})
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetTorqueInfo", {},
                                                  {"out": {"torque": 30.0, "isvalid": True}},timeout = 0.5)

    @pytest.mark.full
    @allure.title("获取|通知转向扭矩状态_通讯故障_UsgModSts = 11/13_记忆值")
    def test_caseid_1980326(self):
        #重启后15s 不需要检测超时，否则会因为性能问题，导致校验失效
        sleep(10)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTqQf',
                      3)
        sleep(0.2)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTq', 30.0)
        sleep(0.2)
        for Y in [11, 13]:
            self.sd_tester.change_usage_mode(Y)
            sleep(0.5)
            logger.info(f"usgmode={Y}")
            self.ipdu.pause_all_bus_send()
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Torque",
                                          {"fTorque": {"torque": 30.0, "isvalid": False}})
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetTorqueInfo", {},
                                                  {"out": {"torque": 30.0, "isvalid": False}}, timeout=2.5)
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Torque",
                                          {"fTorque": {"torque": 30.0, "isvalid": True}})
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetTorqueInfo", {},
                                                  {"out": {"torque": 30.0, "isvalid": True}}, timeout=2)

    @pytest.mark.full
    @allure.title("获取|通知转向扭矩状态_通讯故障_E2E故障")#pass
    def test_caseid_1980327(self):
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTqQf',
                      3)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTq', 0.0)
        self.partner.empty_all(0.5)
        for SteerWhlTq in [30.0, -30.0]:
            logger.info(f'发到{SteerWhlTq}')
            self.ipdu.set_no_crc(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTq')
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTq', SteerWhlTq)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Torque",
                                      {"fTorque": {"torque": SteerWhlTq, "isvalid": False}})
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetTorqueInfo", {},
                                                  {"out": {"torque": SteerWhlTq, "isvalid": False}})
            self.ipdu.restore_crc(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTq')
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Torque",
                                      {"fTorque": {"torque": SteerWhlTq, "isvalid": True}}, timeout=2)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetTorqueInfo", {},
                                                  {"out": {"torque": SteerWhlTq, "isvalid": True}}, timeout=2)

    @pytest.mark.smoke
    @allure.title("获取|通知方向盘转角状态")
    def test_caseid_108593(self):
        for Qf in [0, 1, 2, 3]:
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf',
                          Qf)
            sleep(0.5)
            if Qf in [1, 2, 0]:
                Qf = False
            else:
                Qf = True
            for Ag in [-14.5, 14.5, -10.0, 0.0]:
                logger.info(f'发到{Ag}')
                for Spd in [-50.0, 50.0, -10.0, 0.0]:
                    self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', Ag)
                    self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAgSpd', Spd)
                    sleep(1)
                    self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelInfo",
                                            {"info": {"angle": Ag, "speed": Spd, "isvalid": Qf}}, timeout=2)
                    self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetSteerWheelInfo", {},
                                                        {"out": {"angle": Ag, "speed": Spd, "isvalid": Qf}},
                                                        timeout=2)
    
    @pytest.mark.full
    @allure.title("获取|通知方向盘转角状态_默认值")
    def test_caseid_1985479(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAgSpd', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3)
        sleep(1)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetSteerWheelInfo", {},
                                              {"out": {"angle": 0, "speed": 0, "isvalid": 0}},timeout = 0.5)
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelInfo",
                                            {"info": {"angle": 0, "speed": 0, "isvalid": 1}})
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetSteerWheelInfo", {},
                                                        {"out": {"angle": 0, "speed": 0, "isvalid": 1}},timeout = 2)

    @pytest.mark.full
    @allure.title("设置转向强度等级")
    def test_caseid_1980368(self):
        for X in range(8):
            logger.info(f"level_set为{X}")
            # todo 开始抓包
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerStrengthLevel", {"level": X})
            self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr16, 'SteerAsscLvl', X)
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_signal_values("SteerAsscLvlETH", [X])

    @pytest.mark.full
    @allure.title("获取|通知转向强度等级")
    def test_caseid_108592(self):
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr06, 'SteerAsscLvlCfmd', 0)
        for i in range(1, 8):
            logger.info(f"LvlCfmd为{i}")
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr06, 'SteerAsscLvlCfmd', i)
            sleep(0.5)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StrengthLevel", {"level": i})
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetSteerStrengthLevel", {},
                                                  {"out": i})
    
    @pytest.mark.full
    @allure.title("获取|通知转向强度等级_默认值")
    def test_caseid_1985480(self):
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr06, 'SteerAsscLvlCfmd', 0)
        sleep(0.5)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetSteerStrengthLevel", {},
                                                  {"out": 0},timeout=2)
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StrengthLevel", {"level": 0})
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetSteerStrengthLevel", {},
                                                  {"out": 0},timeout=2)

    @pytest.mark.sanity
    @allure.title("通知AD激活退出按键状态变化")
    def test_caseid_108630(self):
        for i in list(range(1, 4)) + [0]:
            logger.info(f"信号为{i}")
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2', i)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "NotifyADActivationButttonState", {"pressState": i},
                                      timeout=2)
    
    @pytest.mark.full
    @allure.title("通知AD激活退出按键状态变化_重启event")
    def test_caseid_1984553(self):
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2', 1)
        sleep(0.5)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "NotifyADActivationButttonState", {"pressState": 1},
                                    timeout=2)

    @pytest.mark.full
    @allure.title("通知AD激活退出按键状态变化_E2E故障")
    def test_caseid_1980375(self):
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2', 1)
        self.partner.empty_all(2)
        self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "NotifyADActivationButttonState", {"pressState": 4},
                                  timeout=2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2', 2)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "NotifyADActivationButttonState")
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2', 3)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "NotifyADActivationButttonState")
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "NotifyADActivationButttonState", {"pressState": 3},
                                  timeout=2)

    @pytest.mark.full
    @allure.title("通知转向开关状态_重启event")
    def test_caseid_1984552(self):
        self.sd_tester.write_single_ccp(629, 4)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 1)
        sleep(0.5)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",{})

    @pytest.mark.full
    @allure.title("获取|通知方向盘故障状态_方向盘系统故障")
    def test_caseid_1939939(self):
        #规避 = 3时，上报fault = 13
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2', 0)
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2')
        self.sd_tester.write_single_ccp(186, 2)
        self.ipdu.set(self.ipdu.cem_lin4.AswmCem_Lin4Fr01, 'WhlFailrSts', 0)
        self.partner.empty_all(0.5)
        for value in [1, 0, 2, 0, 4, 0, 8, 0, 16, 0, 32, 0, 64, 0, 6, 4, 0]:
            logger.info(f"Singal_set为{value}")
            self.ipdu.set(self.ipdu.cem_lin4.AswmCem_Lin4Fr01, 'WhlFailrSts', value)
            for fault in range(1, 8):
                if (1 << (fault - 1)) == value:  # 往前移一位
                    break
            if value == 6:
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
                                          {"faults": [{"fault": 2, "faultMsg": ""}, {"fault": 3, "faultMsg": ""}]})
                self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                                      {"out": [{"fault": 2, "faultMsg": ""},
                                                               {"fault": 3, "faultMsg": ""}]})
            else:
                if value == 0:
                    fault = 0
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
                                          {"faults": [{"fault": fault, "faultMsg": ""}]})
                self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                                      {"out": [{"fault": fault, "faultMsg": ""}]})

    @pytest.mark.sanity
    @allure.title("获取|通知方向盘故障状态_L2上拨下拨按键故障 ")#pass
    def test_caseid_1939938(self):
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 1)
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})
        self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
                                  {"faults": [{"fault": 12, "faultMsg": ""}]})
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 12, "faultMsg": ""}]})
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1')
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})

    @pytest.mark.sanity
    @allure.title("获取|通知方向盘故障状态_L2长按短按按键故障")#pass
    def test_caseid_1939940(self):
        self.sd_tester.write_single_ccp(186, 2)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2', 1)
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})
        self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
                                  {"faults": [{"fault": 13, "faultMsg": ""}]})
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 13, "faultMsg": ""}]})
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2')
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})

    @pytest.mark.sanity
    @allure.title("获取|通知方向盘故障状态_L3长按短按按键故障")#pass
    def test_caseid_1980391(self):
        self.sd_tester.write_single_ccp(186, 2)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2', 1)
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})
        self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
                                  {"faults": [{"fault": 14, "faultMsg": ""}]})
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 14, "faultMsg": ""}]})
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2')
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})

    @pytest.mark.sanity
    @allure.title("获取|通知方向盘故障状态_L4长按短按按键故障")#pass
    def test_caseid_1980393(self):
        self.sd_tester.write_single_ccp(186, 2)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2', 1)
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})
        self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
                                  {"faults": [{"fault": 15, "faultMsg": ""}]})
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 15, "faultMsg": ""}]})
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2')
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})

    @pytest.mark.full
    @allure.title("获取和通知方向盘故障状态_转向扭矩故障_QF!=3时故障")#pass
    def test_caseid_1939944(self):
        for usage_mode in [11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                             {"out": [{"fault": 0, "faultMsg": ""}]})
            for value in [1, 3, 2, 3, 0, 3]:
                logger.info(f"信号为{value}")
                self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTqQf',
                              value)  # 故障18
                for fault in [0, 18]:
                    if value == [0, 1, 2]:
                        fault = 18
                        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
                                                  {"faults": [{"fault": fault, "faultMsg": ""}]})
                        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                                         {"out": [{"fault": fault, "faultMsg": ""}]})
                else:
                    if value == 3:
                        fault = 0
                        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                                         {"out": [{"fault": fault, "faultMsg": ""}]})

    @pytest.mark.sanity
    @allure.title("获取和通知方向盘故障状态_转向扭矩故障_E2E故障")#pass
    def test_caseid_1980400(self):
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})
        self.ipdu.set_no_crc(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTq')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
                                  {"faults": [{"fault": 18, "faultMsg": ""}]})
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 18, "faultMsg": ""}]})
        self.ipdu.restore_crc(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTq')
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})

    @pytest.mark.full
    @allure.title("获取和通知方向盘故障状态_转向扭矩故障_信号丢失(11/13)")#pass
    def test_caseid_1980403(self):
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})
        for usage_mode in [11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            self.ipdu.pause_bus_send("chassiscan1")
            sleep(2)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
                                      {"faults": [{"fault": 18, "faultMsg": ""}]})
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                             {"out": [{"fault": 18, "faultMsg": ""}]})
            self.ipdu.resume_bus_send("chassiscan1")
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                             {"out": [{"fault": 0, "faultMsg": ""}]})

    @pytest.mark.sanity
    @allure.title("获取和通知方向盘故障状态_转角故障")#pass
    def test_caseid_1939937(self):
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})
        for value in [1, 3, 2, 3, 0, 3]:
            logger.info(f"信号为{value}")
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTqQf',
                          value)  # 故障18
            for fault in [0, 19]:
                if value == [0, 1, 2]:
                    fault = 19
                    self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
                                              {"faults": [{"fault": fault, "faultMsg": ""}]})
                    self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                                     {"out": [{"fault": fault, "faultMsg": ""}]})
            else:
                if value == 3:
                    fault = 0
                    self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                                     {"out": [{"fault": fault, "faultMsg": ""}]})
    
    @pytest.mark.sanity
    @allure.title("方向盘加热等级_请求源赋值逻辑测试")
    def test_caseid_1985597(self):
        for i in [2,0,11,1,13]:
            logger.info(f"i=={i}")
            self.sd_tester.change_usage_mode(i)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 0,"source": 0})
            sleep(0.5)
            for j in [1,2,0]:
                logger.info(f"j=={j}")
                self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 0,"source": j})
                sleep(0.5)
                if i in [2,11,13]:
                    self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Heat", {"sts": {"source":j}})
                    self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"source":j}})
                else:
                    self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "Heat")
                    self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"source":0}})
                    
    @pytest.mark.full
    @allure.title("方向盘加热等级_请求源赋值逻辑测试_BGM重启")
    def test_caseid_1985598(self):
            self.sd_tester.change_usage_mode(2)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 0,"source": 0})
            sleep(0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 0,"source": 1})
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Heat", {"sts": {"source":1}})
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"source":1}})
            
            self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
            sleep(2)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Heat", {"sts": {"source":0}})
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"source":0}})
            
    @pytest.mark.full
    @allure.title("方向盘加热等级_请求源赋值逻辑测试_默认值")
    def test_caseid_1985599(self):
            self.sd_tester.change_usage_mode(2)
            #不加等待可能导致接口调用之后 usagemode才切成功
            sleep(0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 0,"source": 0}, timeout = 0.5)
            sleep(0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 0})
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Heat", {"sts": {"source":1}})
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"source":1}})
            
    @allure.title("座椅通风加热请求源_usagemode_下切上切")
    @pytest.mark.sanity
    def test_caseid_1985797(self):
        for i in [2,11,13]:
            for j in [0,1]:
                for k in [2,11,13]:
                    self.sd_tester.change_usage_mode(i)  
                    self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 0,"source": 0})
                    sleep(0.5)
                    self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 0,"source": 2})
                    self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Heat", {"sts": {"source":2}})
                    self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"source":2}})
                    
                    self.sd_tester.change_usage_mode(j) 
                    self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Heat", {"sts": {"source":0}})
                    self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"source":0}}) 
                    
                    self.sd_tester.change_usage_mode(k) 
                    self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "Heat")
                    self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"source":0}})
                    
    @pytest.mark.sanity
    @allure.title("方向盘L2按键状态_拨扭开关_变化上报")
    def test_caseid_1985539(self):
        list1 = [[0,0],[1,1],[3,2],[5,2],[2,1],[4,2]]
        self.sd_tester.write_single_ccp(970, 0)
        logger.info("写ccp：{}".format({970: 0}))
        # self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [970]},
        #                                       {"out": [{"name": 970, "value": 0}]})
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 1)
        self.partner.empty_all(1)
        for i in range(6):  
            logger.info(f"i=={i}")
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', list1[i][0])
            if i == 3:
                self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts")
            else:
                self.partner.ck_coming_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                                {"buttonSts":{"stsInfo":{"sts":list1[i][1],"step":-1},"faultInfo":{"isFault":False,"fault":[0]}}})
                   
    @pytest.mark.sanity
    @allure.title("方向盘L2按键状态_拨扭开关_变化上报_多次调节")
    def test_caseid_1985541(self):
        list1 = [[0,0],[1,1],[3,2]]
        self.sd_tester.write_single_ccp(970, 0)
        logger.info("写ccp：{}".format({970: 0}))
        # self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [970]},
        #                                       {"out": [{"name": 970, "value": 0}]})
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 1)
        self.partner.empty_all(1)
        for i in range(20):
            for j in range(3):
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', list1[j][0])
                self.partner.ck_coming_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                                {"buttonSts":{"stsInfo":{"sts":list1[j][1],"step":-1},"faultInfo":{"isFault":False,"fault":[0]}}})
    
    @pytest.mark.sanity
    @allure.title("方向盘R2按键状态_拨扭开关_变化上报")
    def test_caseid_1985637(self):
        list1 = [[0,0],[1,1],[3,2],[5,2],[2,1],[4,2]]
        self.sd_tester.write_single_ccp(970, 0)
        logger.info("写ccp：{}".format({970: 0}))
        # self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [970]},
        #                                       {"out": [{"name": 970, "value": 0}]})
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', 1)
        self.partner.empty_all(1)
        for i in range(6):  
            logger.info(f"i=={i}")
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', list1[i][0])
            if i == 3:
                self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts")
            else:
                self.partner.ck_coming_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                                {"buttonSts":{"stsInfo":{"sts":list1[i][1],"step":-1},"faultInfo":{"isFault":False,"fault":[0]}}})
              
    @pytest.mark.sanity
    @allure.title("方向盘R2按键状态_拨扭开关_变化上报_多次调节")
    def test_caseid_1985638(self):
        list1 = [[0,0],[1,1],[3,2]]
        self.sd_tester.write_single_ccp(970, 0)
        logger.info("写ccp：{}".format({970: 0}))
        # self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [970]},
        #                                       {"out": [{"name": 970, "value": 0}]})
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', 1)
        self.partner.empty_all(1)
        for i in range(20):
            for j in range(3):
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', list1[j][0])
                self.partner.ck_coming_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                                {"buttonSts":{"stsInfo":{"sts":list1[j][1],"step":-1},"faultInfo":{"isFault":False,"fault":[0]}}})    
    
    @allure.title("方向盘拨钮按键状态_配置字不满足")
    @pytest.mark.full
    def test_caseid_1985647(self):
        self.partner.empty_all(1) 
        self.sd_tester.write_single_ccp(970, 2)
        # self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [970]},
        #                                       {"out": [{"name": 970, "value": 2}]})
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 5)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', 5)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 5)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', 0)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts")
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts") 
        
    @allure.title("滚轮调速方案_15s内Acc服务可用")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1985962(self):
        self.sd_tester.write_single_ccp(970, 1)
        self.ipdu.pause_all_bus_send()
        sleep(1)
        self.bgm_power_off_and_on(timeout=0)
        self.partner.empty_all()
        self.ipdu.resume_all_bus_send()
        t1 = time.time()
        self.partner.wait_for_service_reconnect(ACC_SERVICE_SERVER)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr03, 'ScButtUpDnStpMidLe1UpDnSts', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr03, 'ScButtUpDnStpMidLe1ScButtUpDnStp', 0)
        sleep(0.5)
        for _ in range(120):
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr03, 'ScButtUpDnStpMidLe1UpDnSts', 1)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr03, 'ScButtUpDnStpMidLe1ScButtUpDnStp', 1)
            sleep(0.1)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr03, 'ScButtUpDnStpMidLe1UpDnSts', 2)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr03, 'ScButtUpDnStpMidLe1ScButtUpDnStp', 1)
            sleep(0.1)
            try:
                self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":5}, timeout=0.03)
            except Exception as e:
                pass
            else:
                break
        assert time.time() - t1 < 15, "启动后15s内可用"   
    
    @allure.title("L2上拨下拨按键故障")
    @pytest.mark.sanity
    def test_caseid_1987677(self):
        self.set_no_SteerWheelFault()
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})
        self.partner.empty_all(1)
        for opts in [0,1,2,3]:
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelButtonInhibit", {"opts": opts},timeout=1)
            for j in [1,2,3,4,5,0,6,0]:
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', j) 
                if j == 5 or j == 6:
                    self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 12, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
                elif j == 0:
                    self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 0, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
                else:
                    self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault")
                    
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 0)
            sleep(0.5)
            self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1')
            self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 12, "faultMsg": ""}]},
                                    "GetFaultInfo", {}) 
            #e2e故障时，服务不处理对应的信号     
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 5)
            sleep(0.5)  
            self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault") 
            #e2e故障时，服务处理对应的信号
            self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1')
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
                                    {"faults": [{"fault": 0, "faultMsg": ""}]})   
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
                                    {"faults": [{"fault": 12, "faultMsg": ""}]})
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 0)
            sleep(0.5)      
            self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 0, "faultMsg": ""}]},
                                    "GetFaultInfo", {})    
            
    @allure.title("L2长按短按按键故障")
    @pytest.mark.sanity
    def test_caseid_1987678(self):
        self.set_no_SteerWheelFault()
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})
        self.partner.empty_all(1)
        for opts in [0,1,2,3]:
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelButtonInhibit", {"opts": opts},timeout=1)
            for j in [1,2,3,0,4]:
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2', j)
                if j == 3:
                    self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 13, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
                elif j == 0:
                    self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 0, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
                else:
                    self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault") 
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2', 0)
            sleep(0.5)
            self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2')
            self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 13, "faultMsg": ""}]},
                                    "GetFaultInfo", {}) 
            #e2e故障时，服务不处理对应的信号     
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2', 3)
            sleep(0.5)  
            self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault") 
            #e2e故障时，服务处理对应的信号
            self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2')
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
                                    {"faults": [{"fault": 0, "faultMsg": ""}]})   
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
                                    {"faults": [{"fault": 13, "faultMsg": ""}]})
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2', 0)
            sleep(0.5)      
            self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 0, "faultMsg": ""}]},
                                    "GetFaultInfo", {}) 
    
    @allure.title("L3长按短按按键故障")
    @pytest.mark.sanity
    def test_caseid_1987679(self):
        self.set_no_SteerWheelFault()
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})
        self.partner.empty_all(1)
        for opts in [0,1,2,3]:
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelButtonInhibit", {"opts": opts},timeout=1)
            for j in [1,2,3,0,4]:
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2', j)
                if j == 3:
                    self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 14, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
                elif j == 0:
                    self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 0, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
                else:
                    self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault")
                    
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2', 0)
            sleep(0.5)
            self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2')
            self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 14, "faultMsg": ""}]},
                                    "GetFaultInfo", {}) 
            #e2e故障时，服务不处理对应的信号     
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2', 3)
            sleep(0.5)  
            self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault") 
            #e2e故障时，服务处理对应的信号
            self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2')
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
                                    {"faults": [{"fault": 0, "faultMsg": ""}]})   
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
                                    {"faults": [{"fault": 14, "faultMsg": ""}]})
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2', 0)
            sleep(0.5)      
            self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 0, "faultMsg": ""}]},
                                    "GetFaultInfo", {})   
            
    @allure.title("L4长按短按按键故障")
    @pytest.mark.sanity
    def test_caseid_1987680(self):
        self.set_no_SteerWheelFault()
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})
        self.partner.empty_all(1)
        for opts in [0,1,2,3]:
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelButtonInhibit", {"opts": opts},timeout=1)
            for j in [1,2,3,0,4]:
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2', j)
                if j == 3:
                    self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 15, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
                elif j == 0:
                    self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 0, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
                else:
                    self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault")
                    
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2', 0)
            sleep(0.5)
            self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2')
            self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 15, "faultMsg": ""}]},
                                    "GetFaultInfo", {}) 
            #e2e故障时，服务不处理对应的信号     
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2', 3)
            sleep(0.5)  
            self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault") 
            #e2e故障时，服务处理对应的信号
            self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2')
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
                                    {"faults": [{"fault": 0, "faultMsg": ""}]})   
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
                                    {"faults": [{"fault": 15, "faultMsg": ""}]})
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2', 0)
            sleep(0.5)      
            self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 0, "faultMsg": ""}]},
                                    "GetFaultInfo", {}) 
   
    @allure.title("左转向灯开关故障")
    @pytest.mark.sanity
    def test_caseid_1987604(self):
        self.set_no_SteerWheelFault()
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})
        self.partner.empty_all(1)
        for i in range(3):
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelButtonInhibit", {"opts": i},timeout=1)
            for j in [1,2,3,0,4]:
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', j)
                if j == 3 :
                    self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 16, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
                elif j == 0:
                    self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 0, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
                else:
                    self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault")
                    
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
            self.partner.empty_all(0.5)
            self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2')
            self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 16, "faultMsg": ""}]},
                                    "GetFaultInfo", {}) 
            #e2e故障时，服务不处理对应的信号     
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 3)
            self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault") 
            
            #e2e非故障时，服务处理对应的信号
            self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2')
            self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault") 
            # self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
            #                         {"faults": [{"fault": 0, "faultMsg": ""}]})   
            # self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
            #                         {"faults": [{"fault": 16, "faultMsg": ""}]})
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
            sleep(0.5)      
            self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 0, "faultMsg": ""}]},
                                    "GetFaultInfo", {})   
            
    @allure.title("右转向灯开关故障")
    @pytest.mark.sanity
    def test_caseid_1987605(self):
        self.set_no_SteerWheelFault()
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})
        self.partner.empty_all(1)
        #老方向盘
        self.sd_tester.write_single_ccp(629, 4)
        for j in [1,2,3,0,4]:
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', j)
            if j == 3 :
                self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                {"faults": [{"fault": 17, "faultMsg": ""}]},
                                "GetFaultInfo", {})
            elif j == 0:
                self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                {"faults": [{"fault": 0, "faultMsg": ""}]},
                                "GetFaultInfo", {})
            else:
                self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault")
                
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set_no_crc(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2')
        self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                {"faults": [{"fault": 17, "faultMsg": ""}]},
                                "GetFaultInfo", {}) 
   
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 3)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault") 

        self.ipdu.restore_crc(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2')
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault") 
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 0)
        sleep(0.5)      
        self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                {"faults": [{"fault": 0, "faultMsg": ""}]},
                                "GetFaultInfo", {})   
        
        #新方向盘
        self.sd_tester.write_single_ccp(629, 6)
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2')
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 0)
        for j in [1,2,3,0,4]:
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', j)
            if j == 3 :
                self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                {"faults": [{"fault": 17, "faultMsg": ""}]},
                                "GetFaultInfo", {})
            elif j == 0:
                self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                {"faults": [{"fault": 0, "faultMsg": ""}]},
                                "GetFaultInfo", {})
            else:
                self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault")
                
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2')
        self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                {"faults": [{"fault": 17, "faultMsg": ""}]},
                                "GetFaultInfo", {}) 
   
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 3)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault") 

        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2')
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault") 
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 0)
        sleep(0.5)      
        self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                {"faults": [{"fault": 0, "faultMsg": ""}]},
                                "GetFaultInfo", {})   
                
    @allure.title("R2上拨下拨按键故障")
    @pytest.mark.sanity
    def test_caseid_1987681(self):
        #本信号无e2e校验
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', 0)
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})
        self.partner.empty_all(1)
        for i in [0,1,2,3]:
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelButtonInhibit", {"opts": i},timeout=1)
            for j in [1,2,3,4,5,0,6,0]:
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', j)
                if j == 5 or j == 6:
                    self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 8, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
                elif j == 0:
                    self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 0, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
                else:
                    self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault")
                      
    @allure.title("R2长按短按按键故障")
    @pytest.mark.sanity
    def test_caseid_1987687(self):
        #本信号无e2e校验
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', 0)
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})
        self.partner.empty_all(1)
        for i in [0,1,2,3]:
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelButtonInhibit", {"opts": i},timeout=1)
            for j in [1,2,3,0,4]:
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi2', j)
                
                if j == 3 :
                    self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 9, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
                elif j == 0:
                    self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 0, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
                else:
                    self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault")
            
    @allure.title("R3按键故障")
    @pytest.mark.sanity
    def test_caseid_1987688(self):
        #本信号无e2e校验
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScRightButtonRi', 0)
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})
        self.partner.empty_all(1)
        for i in [0,1,2,3]:
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelButtonInhibit", {"opts": i},timeout=1)
            for j in [1,2,3,0,4]:
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScRightButtonRi', j)
                if j == 3 :
                    self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 11, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
                elif j == 0:
                    self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 0, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
                else:
                    self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault")
                                
    @allure.title("R4按键故障")
    @pytest.mark.sanity
    def test_caseid_1987689(self):
        #本信号无e2e校验
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScLeftButtonRi', 0)
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]})
        self.partner.empty_all(1)
        for i in [0,1,2]:
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelButtonInhibit", {"opts": i},timeout=1)
            for j in [1,2,3,0,4]:
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScLeftButtonRi', j)
                if j == 3 :
                    self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 10, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
                elif j == 0:
                    self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 0, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
                else:
                    self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault")
                    
    @allure.title("转向灯拨杆开关故障")
    @pytest.mark.smoke
    def test_caseid_1989192(self):
        self.set_no_SteerWheelFault()
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                         {"out": [{"fault": 0, "faultMsg": ""}]}) 
        self.partner.empty_all(1)
        for i in [1,2,3,4,5,0]:
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', i)
            if i == 5:
                self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 21, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
            elif i == 0:
                self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 0, "faultMsg": ""}]},
                                    "GetFaultInfo", {})
            else:self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault")
            
        self.ipdu.set_no_crc(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1')
        self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                {"faults": [{"fault": 21, "faultMsg": ""}]},
                                "GetFaultInfo", {})
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 5) 
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault")
        self.ipdu.restore_crc(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1')  
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault")
        
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 1)
        self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                {"faults": [{"fault": 0, "faultMsg": ""}]},
                                "GetFaultInfo", {}) 
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 5) 
        self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                {"faults": [{"fault": 21, "faultMsg": ""}]},
                                "GetFaultInfo", {}) 
        self.ipdu.set_no_crc(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1')
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault")
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 0) 
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault")
        self.ipdu.restore_crc(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1')  
        self.partner.ck_event_and_resp(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                {"faults": [{"fault": 0, "faultMsg": ""}]},
                                "GetFaultInfo", {}) 
              
    @allure.title("启动场景_通知方向盘ADAS简单按键变化_默认值")
    @pytest.mark.full
    def test_caseid_1988619(self): 
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2',0)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2',0)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2',0)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi2', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScLeftButtonRi', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScRightButtonRi', 0)
        
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "ADASButtonChanged")
        
    @allure.title("启动场景_通知方向盘ADAS简单按键变化_非默认值")
    @pytest.mark.full
    def test_caseid_1988620(self): 
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2',1)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2',1)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2',1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi2', 1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScLeftButtonRi', 1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScRightButtonRi', 1)

        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ADASButtonChanged",{})
              
    @allure.title("启动场景_通知方向盘ADAS复杂按键变化_默认值")
    @pytest.mark.full
    def test_caseid_1988621(self): 
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1',0)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', 0)

        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "ADASComplexButtonChanged")
        
    @allure.title("启动场景_通知方向盘ADAS复杂按键变化_非默认值")
    @pytest.mark.full
    def test_caseid_1988622(self): 
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1',1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', 1)

        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ADASComplexButtonChanged",{})
    
       
    @allure.title("启动场景_通知方向盘简单按键变化_默认值")
    @pytest.mark.full
    def test_caseid_1988623(self): 
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2',0)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2',0)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2',0)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi2', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScLeftButtonRi', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScRightButtonRi', 0)
        
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SimpleButtonChanged")
        
    @allure.title("启动场景_通知方向盘简单按键变化_非默认值")
    @pytest.mark.full
    def test_caseid_1988624(self): 
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2',1)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2',1)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2',1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi2', 1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScLeftButtonRi', 1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScRightButtonRi', 1)
        
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SimpleButtonChanged",
                                  {"infos": [{"buttonId": 1, "state": 1},
                                             {"buttonId": 2, "state": 1},
                                             {"buttonId": 3, "state": 1},
                                            ]})
        # self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SimpleButtonChanged",
        #                           {"infos": [{"buttonId": 5, "state": 1},
        #                                     ]})
        # self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SimpleButtonChanged",
        #                           {"infos": [{"buttonId": 6, "state": 1},
        #                                      {"buttonId": 7, "state": 1},
        #                                     ]})
             
    @allure.title("启动场景_通知方向盘复杂按键变化_默认值")
    @pytest.mark.full
    def test_caseid_1988625(self): 
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1',0)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', 0)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "ComplexButtonChanged")
        
    @allure.title("启动场景_通知方向盘复杂按键变化_非默认值")
    @pytest.mark.full
    def test_caseid_1988626(self): 
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1',1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', 1)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "ComplexButtonChanged",{})
        
    @allure.title("启动场景_通知方向盘位置_默认值")
    @pytest.mark.full
    def test_caseid_1988627(self): 
        self.sd_tester.write_single_ccp(950, 1)
        sleep(2)
        self.set_steer_position(0.0, 0.0)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelPositionChanged",
                                          {"position": {"angle": 0, "length": 0}})
        
    @allure.title("启动场景_通知方向盘位置_非默认值")
    @pytest.mark.full
    def test_caseid_1988628(self): 
        self.sd_tester.write_single_ccp(950, 1)
        sleep(2)
        self.set_steer_position(1.0, 1.0)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelPositionChanged",
                                          {"position": {"angle": 1.0, "length": 1.0}})
        
    @allure.title("启动场景_通知转向扭矩状态_默认值")
    @pytest.mark.full
    def test_caseid_1988629(self): 
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTq', 0)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTqQf', 1)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Torque",
                                          {"fTorque": {"torque": 0, "isvalid": 0}})
        
    @allure.title("启动场景_通知转向扭矩状态_非默认值")
    @pytest.mark.full
    def test_caseid_1988630(self): 
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTq', 1)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTqQf', 3)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Torque",
                                          {"fTorque": {"torque": 0.00390625, "isvalid": 1}})
    
    @allure.title("启动场景_通知方向盘转角状态_默认值")
    @pytest.mark.full
    def test_caseid_1988631(self): 
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAgSpd', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 0)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(2)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelInfo",
                                            {"info": {"angle": 0, "speed": 0, "isvalid": 0}})
        
    @allure.title("启动场景_通知方向盘转角状态_非默认值")
    @pytest.mark.full
    def test_caseid_1988632(self): 
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAgSpd', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelInfo",
                                            {"info": {"angle": 0.0009765625, "speed": 0.0078125, "isvalid": 1}})
    
    @allure.title("启动场景_通知转向强度等级状态_默认值")
    @pytest.mark.full
    def test_caseid_1988633(self):
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr06, 'SteerAsscLvlCfmd', 0)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StrengthLevel", {"level": 0})
        
    @allure.title("启动场景_通知转向强度等级状态_默认值")
    @pytest.mark.full
    def test_caseid_1988634(self):
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr06, 'SteerAsscLvlCfmd', 1)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StrengthLevel", {"level": 1})
        
    @allure.title("启动场景_通知AD激活退出按键状态变化_默认值")
    @pytest.mark.full
    def test_caseid_1988635(self):
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2',0)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "NotifyADActivationButttonState", {"pressState": 0})
        
    @allure.title("启动场景_通知AD激活退出按键状态变化_非默认值")
    @pytest.mark.full
    def test_caseid_1988636(self):
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2',1)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "NotifyADActivationButttonState", {"pressState": 1})
        
    @allure.title("启动场景_通知转向开关状态_默认值")
    @pytest.mark.full
    def test_caseid_1988637(self):
        self.sd_tester.write_single_ccp(629, 4)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 0)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 0)
        self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2')
        self.ipdu.set_no_crc(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2')
        self.ipdu.set_no_crc(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1') 
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                    {"infos": [{"stalkId": 0, "state": 4, "isValid": 0}]})
        
    @allure.title("启动场景_通知转向开关状态_非默认值")
    @pytest.mark.full
    def test_caseid_1988638(self):
        self.sd_tester.write_single_ccp(629, 4)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 1)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",{})

    @pytest.mark.smoke
    @allure.title("左转向开关状态")
    def test_caseid_1989005(self):
        #左转向灯与CCP无关
        self.sd_tester.write_single_ccp(629, 4)
        self.set_stalk_status_init()
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 1, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 1)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 2)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 2)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 2, "isValid": True}]})
       
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 3)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 1, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 3)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")

        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 4)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 5)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 3, "isValid": True}]})
        self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2')
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set_no_crc(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 4, "isValid": False}]})
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2')
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.restore_crc(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 3, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 0, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 0)
        #前状态右转向灯state不为0
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 0, "isValid": True}]})
    
    @pytest.mark.full
    @allure.title("左转向开关状态_参数state同时满足赋多个值")
    def test_caseid_1989006(self):  
        self.sd_tester.write_single_ccp(629, 6)  
        self.set_stalk_status_init()
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 2)    
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 1, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 1)  
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 2)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 2, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 0)    
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 0, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 1, "isValid": True}]})
        
    @pytest.mark.full
    @allure.title("左转向开关状态_E2E故障到恢复")
    def test_caseid_1989007(self):    
        self.set_stalk_status_init()
        self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2')
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 1, "isValid": True}]})
        
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 1)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set_no_crc(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1')
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 0)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.restore_crc(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 0, "isValid": True}]})
        
    @pytest.mark.full
    @allure.title("左转向开关状态_启动场景_LeverSwtLe未跳变")
    def test_caseid_1989008(self):    
        self.set_stalk_status_init()
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 1, "isValid": True}]})
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 0, "isValid": True}]})
        
    @pytest.mark.full
    @allure.title("左转向开关状态_条件other")
    def test_caseid_1989009(self):    
        self.set_stalk_status_init()
        for i in [0,3]:
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', i)
            sleep(0.5)
            for j in [3,5,4]:
                logger.info(f"i={i},j={j}")
                self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', j)
                if i == 0 and j == 3:
                    self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 1, "isValid": True}]})
                elif i == 3 and j == 5 :
                    self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 3, "isValid": True}]})
                else : self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus") 

    @pytest.mark.full
    @allure.title("左转向开关状态_启动场景_当前other状态")
    def test_caseid_1989037(self):    
        self.set_stalk_status_init()
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)
        sleep(1)
        self.ipdu.stop_send_pdu('bodycan', 0x268)
        self.ipdu.stop_send_pdu('bodycan', 0x269)
        self.ipdu.stop_send_pdu('bodycan', 0x271)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT,pause_all_bus=False,resume_all_bus=False)
        #停止 左右方向盘转向开关信号，即不满足所有 通知转向开关状态
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 0, "isValid": False},
                                                 {"stalkId":0,"state":0,"isValid":False}]})
        self.ipdu.resume_bus_send("bodycan")
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 1, "isValid": True}]})
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 0, "isValid": True}]})
        
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 3)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 4)
        sleep(1)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        #重启后第一次来的哪个信号，若是按键信号，则只上报 按键信号对应的值，若是拨杆信号,两边发送false
        #不满足左方向盘 所有通知转向开关状态，但是右方向盘任然满足
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId":0,"state":0,"isValid":True}]})
    
    @pytest.mark.sanity
    @allure.title("右转向开关状态_老方向盘")
    def test_caseid_1989010(self):
        self.sd_tester.write_single_ccp(629, 4)  
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [629]},
                                              {"out": [{"name": 629, "value": 4}]})
        sleep(2)  
        self.set_stalk_status_init()
        #老方向盘时 设置新方向盘对应的信号无效
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 1)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 1, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 3)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 4)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 2)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 2, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 1, "isValid": True}]})
        
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 3)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 2)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 5)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 3, "isValid": True}]})
        
        self.ipdu.set_no_crc(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2')
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set_no_crc(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 4, "isValid": False}]})
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2')
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.restore_crc(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 3, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 0)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 0, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 0)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 0, "isValid": True}]})
        
    @pytest.mark.full
    @allure.title("右转向开关状态_老方向盘_参数state同时满足赋多个值")
    def test_caseid_1989011(self):  
        self.sd_tester.write_single_ccp(629, 4)  
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [629]},
                                              {"out": [{"name": 629, "value": 4}]})
        sleep(2)  
        self.set_stalk_status_init()
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 4)    
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 1, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 5)   
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 2)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 2, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 0)    
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 0, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 1, "isValid": True}]})
    
    @pytest.mark.full
    @allure.title("右转向开关状态_老方向盘_E2E故障到恢复")
    def test_caseid_1989012(self):  
        self.sd_tester.write_single_ccp(629, 4)  
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [629]},
                                              {"out": [{"name": 629, "value": 4}]})
        sleep(2)  
        self.set_stalk_status_init()
        self.ipdu.set_no_crc(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2')
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 1)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 1, "isValid": True}]})
        
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 3)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set_no_crc(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1')
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 0)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.restore_crc(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 0, "isValid": True}]})
        
    @pytest.mark.full
    @allure.title("右转向开关状态_老方向盘_启动场景_LeverSwtLe未跳变")
    def test_caseid_1989013(self):   
        self.sd_tester.write_single_ccp(629, 4)  
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [629]},
                                              {"out": [{"name": 629, "value": 4}]})
        sleep(2)  
        self.set_stalk_status_init()
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 3)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 1, "isValid": True}]})
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 0, "isValid": True}]})
        
    @pytest.mark.full
    @allure.title("右转向开关状态_老方向盘_条件other")
    def test_caseid_1989014(self):  
        self.sd_tester.write_single_ccp(629, 4)  
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [629]},
                                              {"out": [{"name": 629, "value": 4}]})
        sleep(2)  
        self.set_stalk_status_init()
        for i in [0,3]:
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', i)
            sleep(0.5)
            for j in [3,5,4]:
                logger.info(f"i={i},j={j}")
                self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', j)
                if (i == 0 and j == 3) or (i == 3 and j == 4):
                    self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 1, "isValid": True}]})
                elif i == 3 and j == 5 :
                    self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 3, "isValid": True}]})
                else : self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus") 

    @pytest.mark.full
    @allure.title("右转向开关状态_启动场景_当前other状态_老方向盘")
    def test_caseid_1989038(self):    
        self.sd_tester.write_single_ccp(629, 4)  
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [629]},
                                              {"out": [{"name": 629, "value": 4}]})
        sleep(2)   
        self.set_stalk_status_init()
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 1)
        sleep(1)
        self.ipdu.stop_send_pdu('bodycan', 0x268)
        self.ipdu.stop_send_pdu('bodycan', 0x269)
        self.ipdu.stop_send_pdu('bodycan', 0x271)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT,pause_all_bus=False,resume_all_bus=False)
        #停止 左右方向盘转向开关信号，即不满足所有 通知转向开关状态
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 0, "isValid": False},
                                                 {"stalkId":0,"state":0,"isValid":False}]})
        self.ipdu.resume_bus_send("bodycan")
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 0, "isValid": True}]})
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 1, "isValid": True}]})
        
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 3)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 4)
        sleep(1)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId":1,"state":0,"isValid":True}]})
    
    @pytest.mark.sanity
    @allure.title("右转向开关状态_新方向盘")
    def test_caseid_1989015(self):
        self.sd_tester.write_single_ccp(629, 6)  
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [629]},
                                              {"out": [{"name": 629, "value": 6}]})
        sleep(2)   
        self.set_stalk_status_init()
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 1)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 1, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 3)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 4)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 2)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 2, "isValid": True}]})

        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 1, "isValid": True}]})
        
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 3)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 2)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 5)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 3, "isValid": True}]})
        
        self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2')
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set_no_crc(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 4, "isValid": False}]})
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2')
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.restore_crc(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 3, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 0)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 0, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 0)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 0, "isValid": True}]})
    
    @pytest.mark.full
    @allure.title("右转向开关状态_新方向盘_参数state同时满足赋多个值")
    def test_caseid_1989016(self):  
        self.sd_tester.write_single_ccp(629, 6)  
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [629]},
                                              {"out": [{"name": 629, "value": 6}]})
        sleep(2)   
        self.set_stalk_status_init()
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 4)    
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 1, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 5)   
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 2)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 2, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 0)    
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 0, "isValid": True}]})
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 1, "isValid": True}]})
    
    @pytest.mark.full
    @allure.title("右转向开关状态_新方向盘_E2E故障到恢复")
    def test_caseid_1989017(self):  
        self.sd_tester.write_single_ccp(629, 6)  
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [629]},
                                              {"out": [{"name": 629, "value": 6}]})
        sleep(2)   
        self.set_stalk_status_init()
        self.ipdu.set_no_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2')
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 1)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.restore_crc(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 1, "isValid": True}]})
        
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 3)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set_no_crc(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1')
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 0)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus")
        self.ipdu.restore_crc(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1')
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 0, "isValid": True}]})
        
    @pytest.mark.full
    @allure.title("右转向开关状态_新方向盘_启动场景_LeverSwtLe未跳变")
    def test_caseid_1989018(self):   
        self.sd_tester.write_single_ccp(629, 6)  
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [629]},
                                              {"out": [{"name": 629, "value": 6}]})
        sleep(2)   
        self.set_stalk_status_init()
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 4)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 1, "isValid": True}]})
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 0, "isValid": True}]})
        
    @pytest.mark.full
    @allure.title("右转向开关状态_新方向盘_条件other")
    def test_caseid_1989019(self):   
        self.sd_tester.write_single_ccp(629, 6)  
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [629]},
                                              {"out": [{"name": 629, "value": 6}]})
        sleep(2)   
        self.set_stalk_status_init()
        for i in [0,3]:
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', i)
            sleep(0.5)
            for j in [3,5,4]:
                logger.info(f"i={i},j={j}")
                self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', j)
                if (i == 0 and j == 3) or (i == 3 and j == 4):
                    self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 1, "isValid": True}]})
                elif i == 3 and j == 5 :
                    self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 3, "isValid": True}]})
                else : self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus") 

    @pytest.mark.full
    @allure.title("右转向开关状态_启动场景_当前other状态_新方向盘")
    def test_caseid_1989039(self):  
        self.sd_tester.write_single_ccp(629, 6)  
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [629]},
                                              {"out": [{"name": 629, "value": 6}]})
        sleep(2)   
        self.set_stalk_status_init()  
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 1)
        sleep(1)
        self.ipdu.stop_send_pdu('bodycan', 0x268)
        self.ipdu.stop_send_pdu('bodycan', 0x269)
        self.ipdu.stop_send_pdu('bodycan', 0x271)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT,pause_all_bus=False,resume_all_bus=False)
        #停止 左右方向盘转向开关信号，即不满足所有 通知转向开关状态
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 0, "isValid": False},
                                                 {"stalkId":0,"state":0,"isValid":False}]})
        self.ipdu.resume_bus_send("bodycan")
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 1, "state": 0, "isValid": True}]})
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId": 0, "state": 1, "isValid": True}]})
        
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 3)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 4)
        sleep(1)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "StalkStatus",
                                      {"infos": [{"stalkId":1,"state":0,"isValid":True}]})
        
            
@allure.feature("SOA服务接口")
@allure.story("整车控制/SteerWheelService")
@pytest.mark.ypp
class TestSteerWheelServiceMockMcu(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([STEERWHEEL_SERVICE_CLIENT])
        self.partner.method_default_timeout = 5
        
    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr07, 'PinionSteerAgGroupSteerWhlTqQf', 3)  # 清除故障18
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3)  # 清除故障19
        self.ipdu.resume_all_bus_send()
        self.partner.empty_all(1)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def set_usage_mode(self, mode):
        """通过模拟mcu cdd打包总线数据来输入usage mode给到S2S"""
        logger.info(f"设置usage mode: {mode}")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', mode)

    @pytest.mark.full
    @allure.title("获取|通知方向盘加热实际温度_最小|大值")
    def test_caseid_1939967(self):
        for send_value in [-70.0, 134.7, 120.0, 0.0]:
            logger.info(f'发到{send_value}')
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr38, "HSWTRaw", send_value)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "NotifySteerWheelHeatTemperature",
                                      {"temperature": send_value})
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetSteerWheelHeatTemperature", {},
                                                  {"out": send_value})
    
    @pytest.mark.full
    @allure.title("获取|通知方向盘加热实际温度_默认值")
    def test_caseid_1985478(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr38, "HSWTRaw", 0)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetSteerWheelHeatTemperature", {},
                                                  {"out": 0})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "NotifySteerWheelHeatTemperature",
                                      {"temperature": -70.0})
        self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetSteerWheelHeatTemperature", {},
                                                  {"out": -70.0})

    @pytest.mark.smoke
    @allure.title("获取|通知方向盘加热可用状态")
    def test_caseid_1980373(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr03, 'SteerWhlHeatgAvlSts', 0)
        last_value = 0
        #上一条case是启动场景，会导致信号收到的慢（mockmcu）
        self.partner.empty_all(5)
        for send_value in [1, 2, 3, 4, 5, 6, 7, 0]:
            logger.info(f'发到{send_value}')
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr03, 'SteerWhlHeatgAvlSts', send_value)
            if send_value in [0, 1, 2, 3, 4, 5]:
                new_value = send_value
            else:
                new_value = last_value
            if new_value == last_value:
                self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerHeatAvailiable")
            else:
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerHeatAvailiable",
                                          {"status": new_value})
                self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetSteerHeatAvailiable", {},
                                                  {"out": new_value})
            last_value = new_value
    
    @pytest.mark.full
    @pytest.mark.defaultEvent
    @allure.title("获取|通知方向盘加热可用状态_默认值")
    def test_caseid_1984310(self):
        for sts in [1, 0]:
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr03, 'SteerWhlHeatgAvlSts', sts)
            logger.info(f"sts={sts}")
            sleep(1)
            self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT, resume_all_bus=False)
            #启动场景信号丢失恢复无性能要求，这里等待保证后续操作正常进行
            sleep(10)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetSteerHeatAvailiable", {},
                                                    {"out": 0})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerHeatAvailiable",
                                            {"status": sts})
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetSteerHeatAvailiable", {},
                                                    {"out": sts})
    
    @pytest.mark.full
    @allure.title("获取和通知方向盘故障状态_方向盘加热不可用故障")#全哥这边暂时未实现mockmcuE2E校验
    def test_caseid_1980406(self):
        for value in [3, 1, 4, 2, 5, 6, 3, 7, 4, 0]:
            logger.info(f"信号为{value}")
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr03, 'SteerWhlHeatgAvlSts',
                          value)
            for fault in [0, 20]:
                if value == [3, 4, 5]:
                    fault = 19
                    self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault",
                                              {"faults": [{"fault": fault, "faultMsg": ""}]})
                    self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                                     {"out": [{"fault": fault, "faultMsg": ""}]})
            else:
                if value == [1, 2, 6, 7, 0]:
                    fault = 0
                    self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "GetFaultInfo", {},
                                                     {"out": [{"fault": fault, "faultMsg": ""}]})
    
    @pytest.mark.full
    @allure.title("方向盘位置调节_打断逻辑(carmode不满足)")  # pass
    def test_caseid_1980291(self):
        info = ["SteerAdjSwtBackSts","SteerAdjSwtFwdSts","SteerAdjSwtUpSts","SteerAdjSwtDwnSts"]
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', 1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 13)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', 0)  # with allure.step("设置车速小于1.994m/s"):
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "StartMoveDirection",
                                         {"direction": 0})  # 设置方向盘位置方向向前
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', 3)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        for i in range(4):
            assert self.bgm_eth_inter.get_signal_values(info[i])[-1] == 0
                
    @allure.title("设置远程方向盘加热等级_信号重置")
    @pytest.mark.sanity
    def test_caseid_1986007(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [1,0]:
            self.set_usage_mode(mode)
            for i in [1,2,3]:
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', i)
                sleep(0.5)
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', 0)
                sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        result = self.bgm_eth_inter.get_signal_values("TelmSteerWhlHeatgReqLvl")
        assert result.count(0) == 30
        
    @allure.title("方向盘加热的功能延续_先设置的方向盘加热挡位为非0_后调节状态值为非0到0_500ms内状态不变")
    @pytest.mark.sanity
    def test_caseid_1986003(self):
        for i in [1,2,3]:
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": i})
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', i)
            sleep(0.5)

            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', 0)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"level":i}},timeout=0.3)
            
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Heat", {"sts": {"level":0}},timeout=1)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"level":0}})
            
    @allure.title("方向盘加热的功能延续_先设置的方向盘加热挡位为非0_后调节状态值为非0到0_500ms内状态有变化")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1986004(self):
        for i in [1,2,3]:
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 1})
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', i)
            sleep(1)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', 0)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"level":i}},timeout=0.3)
            self.partner.empty_all()
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', i)
            self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "Heat")
            
        for i in [1,2,3]:
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 1})
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', i)
            sleep(1)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', 0)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"level":i}},timeout=0.3)
            self.partner.empty_all()
            if i != 3: 
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', i+1)
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Heat", {"sts": {"level":i+1}},timeout = 1)
            else :
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', 1)
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Heat", {"sts": {"level":1}},timeout = 1)
            
    @allure.title("方向盘加热的功能延续_先设置加热状态值为非0_后设置挡位值为非0_500ms内状态不变")
    @pytest.mark.full
    def test_caseid_1986005(self):
        for i in [1,2,3]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', i)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 1})
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', 0)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"level":i}},timeout = 0.3)
            
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Heat", {"sts": {"level":0}},timeout = 1)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"level":0}})
            
    @allure.title("方向盘加热的功能延续_先设置的方向盘加热挡位为非0_后调节状态值为非0到0_500ms内状态有变化")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1986006(self):
        for i in [1,2,3]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', i)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 1})
            sleep(1)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', 0)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"level":i}},timeout = 0.3)
            self.partner.empty_all()
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', i)
            self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "Heat")
            
        for i in [1,2,3]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', i)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 1})
            sleep(1)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', 0)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"level":i}},timeout = 0.3)
            self.partner.empty_all()
            if i != 3: 
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', i+1)
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Heat", {"sts": {"level":i+1}},timeout = 1)
            else :
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', 1)
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Heat", {"sts": {"level":1}},timeout = 1)        
       
    @allure.title("设置远程方向盘加热等级_信号重置_usagemode上切时")
    @pytest.mark.full
    def test_caseid_1986008(self):
        self.set_usage_mode(1)
        #当UsageMode从Inactive上切Convenience/active/driving且当前加热挡位（设置值）为低/中/高时
        self.bgm_eth_inter.start_bgm_tcpdump()
        for lastmode in [2,11,13]: 
            for i in [1,2,3]:
                self.set_usage_mode(1)
                sleep(0.5)
                self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": i})
                sleep(0.5)
                self.set_usage_mode(lastmode)
                sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        # 本处的0是因为当UsageMode从convenience及以上→Abandoned/inactive时下发
        self.bgm_eth_inter.ck_signal_values("SteerWhlHeatgOnReq",  [1, 0, 2, 0, 3, 0, 1, 0, 2, 0, 3, 0, 1, 0, 2, 0, 3])
        self.set_usage_mode(1)
        #等级为0时上切不会下发PDU
        self.bgm_eth_inter.start_bgm_tcpdump()
        for lastmode in [2,11,13]:   
            self.set_usage_mode(1)
            sleep(0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 0})
            sleep(0.5)
            self.set_usage_mode(lastmode)
            sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        #本处的0是因为当UsageMode从convenience及以上→Abandoned/inactive时下发
        self.bgm_eth_inter.ck_signal_values("SteerWhlHeatgOnReq",  [0,0])
            
    @allure.title("设置远程方向盘加热等级_信号重置_usagemode上切时_开始状态为abandoned")
    @pytest.mark.full
    def test_caseid_1986118(self):
        self.set_usage_mode(0)
        self.bgm_eth_inter.start_bgm_tcpdump()
        for lastmode in [2,11,13]: 
            for i in [0,1,2,3]:
                self.set_usage_mode(0)
                sleep(0.5)
                self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": i})
                sleep(0.5)
                self.set_usage_mode(lastmode)
                sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        #本处的0是因为当UsageMode从convenience及以上→Abandoned/inactive时下发
        self.bgm_eth_inter.ck_signal_values("SteerWhlHeatgOnReq", [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        
    @allure.title("远程方向盘_5帧下发周期内_加热的信号重置_最新值与当前值相同_信号跳变打断接口调用")
    @pytest.mark.full
    def test_caseid_1986123(self):
        self.set_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        for i in [1,2,3]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', i)
            sleep(0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 0})
            #下发5帧期间被打断
            sleep(0.2)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', 0)
            sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        result = self.bgm_eth_inter.get_signal_values("TelmSteerWhlHeatgReqLvl")
        assert result.count(0) == 15
        
    @allure.title("远程方向盘_5帧下发周期内_加热的信号重置_最新值与当前值不同_信号跳变打断接口调用")
    @pytest.mark.full
    def test_caseid_1986124(self):
        self.set_usage_mode(0)
        self.bgm_eth_inter.start_bgm_tcpdump()
        for i in [1,2,3]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', i)
            sleep(0.5)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 1})
            #下发5帧期间被打断
            t1 = time.time()
            logger.info(f"t1={t1}")
            sleep(0.2)
            t2 = time.time()
            logger.info(f"t2={t2}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', 0)
            sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        result = self.bgm_eth_inter.get_signal_values("TelmSteerWhlHeatgReqLvl")
        assert result.count(1) <= 15
        assert result.count(0) == 15
        
    @allure.title("远程方向盘_5帧下发周期内_加热的信号重置_最新值与当前值相同_接口调用打断信号跳变")
    @pytest.mark.full
    def test_caseid_1986192(self):
        self.set_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        for i in [1,2,3]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', i)
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', 0)
            #下发5帧期间被打断
            sleep(0.2)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 0})
            sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        result = self.bgm_eth_inter.get_signal_values("TelmSteerWhlHeatgReqLvl")
        assert result.count(0) == 15

    @allure.title("远程方向盘_5帧下发周期内_加热的信号重置_最新值与当前值不同_接口调用打断信号跳变")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1986193(self):
        self.set_usage_mode(0)
        self.bgm_eth_inter.start_bgm_tcpdump()
        for i in [1,2,3]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', i)
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', 0)
            #下发5帧期间被打断
            sleep(0.2)
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 1})
            sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        result = self.bgm_eth_inter.get_signal_values("TelmSteerWhlHeatgReqLvl")
        # assert result.count(1) == 15
        assert result.count(1) <= 15
        assert result.count(0) <= 15
        
    #JBS-43252   
    @allure.title("方向盘加热_等级非0到0_500ms内请求源变化")
    @pytest.mark.full
    def test_caseid_1988608(self): 
        self.set_usage_mode(2)
        for LvlSts in [1,2,3]:
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": LvlSts,"source": 0})
            for source in [1,2,0]:
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', LvlSts)
                sleep(0.5)
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', 0)
                self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": LvlSts,"source": source})
                
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Heat", {"sts": {"source":source}})
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Heat", {"sts": {"level":0}})
                self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"level":0,"source":source}})
                
    @allure.title("方向盘加热_等级非0到0_500ms内不会触发多余event")
    @pytest.mark.full
    def test_caseid_1988609(self): 
        for LvlSts in [1,2,3]:
            self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": LvlSts})
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', LvlSts)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"level":LvlSts}})
            self.partner.empty_all(1)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', 0)
            #必须加等待
            sleep(0.2)
            self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "Heat",timeout = 0.2)
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"level":LvlSts}},timeout=0.2)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Heat", {"sts": {"level":0}})
            self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetHeat", {}, {"out": {"level":0}})
            
    @pytest.mark.full
    @allure.title("启动场景_通知方向盘加热实际温度_非默认值")
    def test_caseid_1988642(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr38, "HSWTRaw", 0)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "NotifySteerWheelHeatTemperature",
                                      {"temperature": -70.0}, timeout = 10)  
    @pytest.mark.full
    @allure.title("启动场景_通知方向盘加热实际温度_默认值")
    def test_caseid_1988641(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr38, "HSWTRaw", 0.0)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "NotifySteerWheelHeatTemperature",
                                      {"temperature": 0}, timeout = 10)
       
    @allure.title("启动场景_通知方向盘故障状态_默认值")
    @pytest.mark.full
    def test_caseid_1988643(self):
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 0, "faultMsg": ""}]}, timeout = 10)
        
    @allure.title("启动场景_通知方向盘故障状态_非默认值")
    @pytest.mark.full
    def test_caseid_1988644(self):
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScLeftButtonRi', 3)
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelFault", 
                                    {"faults": [{"fault": 10, "faultMsg": ""}]}, timeout = 10)
        
    @allure.title("启动场景_通知方向加热等级_默认值")
    @pytest.mark.full
    def test_caseid_1988639(self): 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', 0)
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"source": 0})
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Heat", {"sts": {"level":0, "source":0}}, timeout = 10)
        
    @allure.title("启动场景_通知方向加热等级_非默认值")
    @pytest.mark.full
    def test_caseid_1988640(self): 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'SteerWhlHeatgLvlSts', 1)
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"source": 1})
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(1)
        #休眠或下电后，再次唤醒时，当服务代理S2S没有接收到SteerWheelService服务中void SetHeat(HeatLevel status,SourceId source = @value(1) 
        # kHMI)接口的调用时，服务代理S2S的该接口参数source为@value(0) kIdle
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "Heat", {"sts": {"level":1, "source":0}}, timeout = 10)
                
                             
@pytest.mark.lg
@allure.feature("SOA服务接口")
@allure.story("整车控制/SteerWheelService")
class TestTailWingServiceMockTCP(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu, tcp_down_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("SteerWheelService", "client"),
                                     ("CarConfigService", "client"),
                                     ("ACCService","server")])
        self.partner.method_default_timeout = 5
        self.partner.wait_for_service_reconnect(STEERWHEEL_SERVICE_CLIENT)
    
    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
    
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.write_ccp_by_tcp({970:1})
        #ccp写完 需要保证生效
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [970]},
                                              {"out": [{"name": 970, "value": 1}]}, timeout = 3)
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelButtonInhibit", {"opts": 0},timeout=1)
        self.partner.empty_all()
        
    def after_each_func(self, ecu):
        self.set_L2roller_stop()
        self.set_R2roller_stop()
        super().after_each_func(ecu)
        
    def set_L2roller_stop(self):
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 0)  
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 0, send_pdu_immediately=True) 
        self.partner.empty_all(0.3)
        
    def set_R2roller_stop(self):
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 0)  
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHScButtUpDnStp", 0, send_pdu_immediately=True) 
        self.partner.empty_all(0.3)
        
    def set_L2roller_signal(self,signal1,signal2,time):
        for num in range(len(signal1)):
            self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", signal1[num])  
            self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", signal2[num], send_pdu_immediately=True)
            sleep(time)
            
    def set_R2roller_signal(self,signal1,signal2,time):
        for num in range(len(signal1)):
            self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", signal1[num])  
            self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHScButtUpDnStp", signal2[num], send_pdu_immediately=True)
            sleep(time)
            
    def get_sum(self,sts,step):
        def return_info(value):
            if value == 1:
                return 1 
            elif value == 2:
                return -1
            else:
                return 0
        sum = 0
        for i in range(len(sts)):
            sum += step[i]*(return_info(sts[i]))
        return sum
    
    @allure.title("方向盘L2按键状态_滚轮开关_服务启动_状态信号为0")
    @pytest.mark.full
    def test_caseid_1985542(self): # 
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(5)
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 0, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.5)   
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 0, send_pdu_immediately=True) 
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts")
    
    @allure.title("方向盘L2按键状态_滚轮开关_服务启动_状态信号为非0_不满足滚动开始条件")
    @pytest.mark.full
    def test_caseid_1985543(self):  
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(5)
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 0, send_pdu_immediately=True) 
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts")
        
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(5)
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 2) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 0, send_pdu_immediately=True) 
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts")
        
    @allure.title("方向盘L2按键状态_滚轮开关_100ms计时器开启时动作")
    @pytest.mark.full
    def test_caseid_1985545(self): 
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)   
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 2) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)     
 
    @allure.title("方向盘L2按键状态_滚轮开关_滚轮向上向下滚动")
    @pytest.mark.sanity
    def test_caseid_1985548(self): 
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)   
        self.set_L2roller_signal([1,1,1,1], [20,35,50,63], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":168},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        
        self.set_L2roller_stop()  
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 2) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02) 
        self.set_L2roller_signal([2,2,2,2], [20,35,50,63], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":168},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        #测试sts = 0，或3
        self.set_L2roller_stop()  
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)   
        self.set_L2roller_signal([1,0,2,3], [10,20,40,20], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":30},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        
    @allure.title("方向盘L2按键状态_滚轮开关_sum为0")
    @pytest.mark.sanity
    def test_caseid_1985550(self): 
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02) 
        #为0可上报
        self.set_L2roller_signal([1,2,1,2], [10,20,10,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        #为0可上报
        self.set_L2roller_signal([1,2,1,2], [10,20,10,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        #停止滚动条件满足报一次0
        self.set_L2roller_signal([0,0,0,0], [0,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        #滚动条件满足后为0 不报
        self.set_L2roller_signal([0,0,0,0], [0,0,0,0], 0.015)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts")
     
    @allure.title("方向盘L2按键状态_滚轮开关_多次滚动")
    @pytest.mark.full
    def test_caseid_1985551(self): 
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02) 
        for i in range(100):
            sts = [random.randint(0, 2) for _ in range(4)]
            stp = [random.randint(0, 63) for _ in range(4)]
            sum = self.get_sum(sts,stp)
            logger.info(f"i={i},sts={sts},stp={stp},sum={sum}")
            self.set_L2roller_signal(sts, stp, 0.015)
            if sum == 0 :
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":sum},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.08) 
            elif sum > 0:
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":sum},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.08) 
            else:
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":abs(sum)},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.08) 
    
    @allure.title("方向盘L2按键状态_滚轮开关_step最大值测试")
    @pytest.mark.full
    def test_caseid_1985552(self): 
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02) 
        self.set_L2roller_signal([1,1,1,1,1,1], [63,63,63,63,63,63], 0.01)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":315},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 2) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)   

        self.set_L2roller_signal([2,2,2,2,2,2], [63,63,63,63,63,63], 0.01)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":315},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06)     
    
    @allure.title("方向盘L2按键状态_滚轮开关_isFault&fault赋值逻辑")
    @pytest.mark.smoke
    def test_caseid_1985553(self): 
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)     
        sleep(0.01)#保证插帧那次能验证到
        self.set_L2roller_signal([3,3,3,3], [1,2,3,4], 0.01)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)     
        #fault上报是插帧
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":True,"fault":[1]}}},timeout=0.05) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":True,"fault":[1]}}},timeout=0.12) 
        #falut后直接停止
        self.set_L2roller_signal([3,3,3,3], [1,2,3,4], 0.015)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts")
        sleep(2)   
        #非同一个100ms周期 变为falut
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 2) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        self.set_L2roller_signal([1,2,3,3], [1,2,1,1], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        self.set_L2roller_signal([3,3], [1,1], 0.01)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":True,"fault":[1]}}},timeout=0.07)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":True,"fault":[1]}}},timeout=0.09)  
        self.set_L2roller_signal([3,3,3,3], [1,2,3,4], 0.015)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts")
        
    @allure.title("方向盘滚轮按键状态_配置字不满足")
    @pytest.mark.sanity
    def test_caseid_1985554(self): 
        self.write_ccp_by_tcp({970:2})
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts")
        
        self.set_R2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts")
        
    @allure.title("方向盘L2按键状态_滚轮开关_停止滚动到重新滚动")
    @pytest.mark.sanity
    def test_caseid_1985727(self): 
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)
        self.set_L2roller_signal([1,1,1,1], [20,35,50,63], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":168},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06)
        self.set_L2roller_signal([1,2,0,0], [10,20,0,0], 0.015)     
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":10},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06)
        self.set_L2roller_signal([0,0,2,1], [0,0,10,20], 0.015)   
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":10},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06)
        self.set_L2roller_signal([1,2,0,0], [10,20,0,0], 0.015)     
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":10},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06)
        self.set_L2roller_signal([0,0,0,0], [0,0,0,0], 0.015) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06)
        self.set_L2roller_signal([0,0,0,0], [0,0,0,0], 0.015) 
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts")
        #后一个滚动周期
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)
        self.set_L2roller_signal([1,1,1,1], [20,35,50,63], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":168},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06)
    #R2    
    @allure.title("方向盘R2按键状态_滚轮开关_服务启动_状态信号为0")
    @pytest.mark.full
    def test_caseid_1985639(self): 
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(5)
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 0, send_pdu_immediately=True)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        a = self.bgm_eth_inter.get_signal_values("ScButtUpDnStpMidRi1ETHUpDnSts")
        logger.info(f"a={a}")
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.5)   
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 0, send_pdu_immediately=True) 
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts")
    
    @allure.title("方向盘R2按键状态_滚轮开关_服务启动_状态信号为非0_不满足滚动开始条件")
    @pytest.mark.full
    def test_caseid_1985640(self): 
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(5)
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHScButtUpDnStp", 0, send_pdu_immediately=True) 
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts")
        
        self.restart_bgm_and_connect_service(STEERWHEEL_SERVICE_CLIENT)
        sleep(5)
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 2) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHScButtUpDnStp", 0, send_pdu_immediately=True) 
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts")
        
    @allure.title("方向盘R2按键状态_滚轮开关_100ms计时器开启时动作")
    @pytest.mark.full
    def test_caseid_1985641(self): 
        self.write_ccp_by_tcp({970:1})
        self.set_R2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)   
        self.set_R2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 2) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)     
 
    @allure.title("方向盘R2按键状态_滚轮开关_滚轮向上向下滚动")
    @pytest.mark.sanity
    def test_caseid_1985642(self): 
        self.set_R2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)   
        self.set_R2roller_signal([1,1,1,1], [20,35,50,63], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":168},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        
        self.set_R2roller_stop()  
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 2) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02) 
        self.set_R2roller_signal([2,2,2,2], [20,35,50,63], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":168},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        #测试sts = 0，或3
        self.set_R2roller_stop()  
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHScButtUpDnStp", 1, send_pdu_immediately=True)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)   
        self.set_R2roller_signal([1,0,2,3], [10,20,40,20], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":30},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        
    @allure.title("方向盘R2按键状态_滚轮开关_sum为0")
    @pytest.mark.smoke
    def test_caseid_1985643(self): 
        self.set_R2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02) 
        #为0可上报
        self.set_R2roller_signal([1,2,1,2], [10,20,10,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        #为0可上报
        self.set_R2roller_signal([1,2,1,2], [10,20,10,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        #停止滚动条件满足报一次0
        self.set_R2roller_signal([0,0,0,0], [0,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        #滚动条件满足后为0 不报
        self.set_R2roller_signal([0,0,0,0], [0,0,0,0], 0.015)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts")
     
    @allure.title("方向盘R2按键状态_滚轮开关_多次滚动")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1985644(self): 
        self.set_R2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02) 
        for i in range(100):
            sts = [random.randint(0, 2) for _ in range(4)]
            stp = [random.randint(0, 63) for _ in range(4)]
            sum = self.get_sum(sts,stp)
            logger.info(f"i={i},sts={sts},stp={stp},sum={sum}")
            self.set_R2roller_signal(sts, stp, 0.015)
            if sum == 0 :
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":sum},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.08) 
            elif sum > 0:
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":sum},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.08) 
            else:
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":abs(sum)},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.08) 
    
    @allure.title("方向盘R2按键状态_滚轮开关_step最大值测试")
    @pytest.mark.full
    def test_caseid_1985645(self): 
        self.set_R2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02) 
        self.set_R2roller_signal([1,1,1,1,1,1], [63,63,63,63,63,63], 0.01)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":315},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        
        self.set_R2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 2) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)   

        self.set_R2roller_signal([2,2,2,2,2,2], [63,63,63,63,63,63], 0.01)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":315},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06)     
 
    @allure.title("方向盘R2按键状态_滚轮开关_isFault&fault赋值逻辑")
    @pytest.mark.full
    def test_caseid_1985646(self): 
        self.set_R2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)     
        sleep(0.01)#保证插帧那次能验证到
        self.set_R2roller_signal([3,3,3,3], [1,2,3,4], 0.01)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)     
        #fault上报是插帧
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":True,"fault":[1]}}},timeout=0.05) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":True,"fault":[1]}}},timeout=0.12) 
        #falut后直接停止
        self.set_R2roller_signal([3,3,3,3], [1,2,3,4], 0.015)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts")
        sleep(2)   
        #非同一个100ms周期 变为falut
        self.set_R2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 2) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        self.set_R2roller_signal([1,2,3,3], [1,2,1,1], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        self.set_R2roller_signal([3,3], [1,1], 0.01)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":True,"fault":[1]}}},timeout=0.07)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":True,"fault":[1]}}},timeout=0.09)  
        self.set_R2roller_signal([3,3,3,3], [1,2,3,4], 0.015)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts")
        
    @allure.title("方向盘R2按键状态_滚轮开关_停止滚动到重新滚动")
    @pytest.mark.sanity
    def test_caseid_1985766(self): 
        self.set_R2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHScButtUpDnStp", 1, send_pdu_immediately=True)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)
        self.set_R2roller_signal([1,1,1,1], [20,35,50,63], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":168},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06)
        self.set_R2roller_signal([1,2,0,0], [10,20,0,0], 0.015)     
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":10},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06)
        self.set_R2roller_signal([0,0,2,1], [0,0,10,20], 0.015)   
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":10},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06)
        self.set_R2roller_signal([1,2,0,0], [10,20,0,0], 0.015)     
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":10},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06)
        self.set_R2roller_signal([0,0,0,0], [0,0,0,0], 0.015) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06)
        self.set_R2roller_signal([0,0,0,0], [0,0,0,0], 0.015) 
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts")
        #后一个滚动周期
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHScButtUpDnStp", 1, send_pdu_immediately=True)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)
        self.set_R2roller_signal([1,1,1,1], [20,35,50,63], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":168},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06)
    
    @allure.title("方向盘L2按键状态_滚轮开关_isFault&fault赋值逻辑_idle状态下")
    @pytest.mark.full
    def test_caseid_1985869(self): 
        self.set_L2roller_stop()
        self.set_L2roller_signal([3,3,3,3], [1,2,3,4], 0.02)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":True,"fault":[1]}}},timeout=0.06)
        self.set_L2roller_signal([1], [1], 0.02)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06)
        
    @allure.title("方向盘R2按键状态_滚轮开关_isFault&fault赋值逻辑_idle状态下")
    @pytest.mark.full
    def test_caseid_1985870(self): 
        self.set_R2roller_stop()
        self.set_R2roller_signal([3,3,3,3], [1,2,3,4], 0.02)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":True,"fault":[1]}}},timeout=0.06)
        self.set_R2roller_signal([1], [1], 0.02)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06)
        
    #acc     SWR
    @allure.title("滚轮调速方案_前置条件不满足(ccp=0)")
    @pytest.mark.full
    def test_caseid_1985931(self):
        self.write_ccp_by_tcp({970:0})
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelButtonInhibit", {"opts": 0},timeout=1)
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts")
                                           
        self.set_L2roller_signal([1,1,1,1], [20,35,50,63], 0.015)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts")
                                            
        self.set_L2roller_signal([2,2,2,2], [20,35,50,63], 0.015)
        self.partner.ck_no_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts")
                                          
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller")
    
    @allure.title("滚轮调速方案_前置条件不满足(方向盘按键抑制激活opts: 1)")
    @pytest.mark.full
    def test_caseid_1985932(self):
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelButtonInhibit", {"opts": 1},timeout=1)
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)                                      
        self.set_L2roller_signal([1,1,1,1], [20,35,50,63], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":168},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)   
        self.set_L2roller_signal([2,2,2,2], [20,35,50,63], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":168},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)   
        
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller")   
        
    @allure.title("滚轮调速方案_前置条件不满足(方向盘按键抑制激活opts: 3)")
    @pytest.mark.full
    def test_caseid_1985933(self):
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetSteerWheelButtonInhibit", {"opts": 1},timeout=1)
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)                                      
        self.set_L2roller_signal([1,1,1,1], [20,35,50,63], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":168},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)   
        self.set_L2roller_signal([2,2,2,2], [20,35,50,63], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":168},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)   
        
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller")   
    
    @allure.title("滚轮调速方案_绝对值>12(由正变负)")
    @pytest.mark.sanity
    def test_caseid_1985934(self):
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 2, send_pdu_immediately=True) 
        self.partner.ck_coming_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)                                      
        self.set_L2roller_signal([1,1,1,1], [1,1,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)  
        self.set_L2roller_signal([0,0,0,0], [0,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07) 
        self.set_L2roller_signal([2,2,2,2], [2,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)       
        #M=4, N=200+ms,rollerStepValue=+5
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":5}, timeout=0.2)
        sleep(0.125)
        # #R=2,200ms前的累计时间=0.1,rollerStepValue=-5
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-5}, timeout=0.25)
        
    @allure.title("滚轮调速方案_绝对值<12(由正变负)")
    @pytest.mark.sanity
    def test_caseid_1987104(self):
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)                                      
        self.set_L2roller_signal([1,1,1,1], [1,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                  {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)  
        self.set_L2roller_signal([0,0,0,0], [0,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                  {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07) 
        self.set_L2roller_signal([2,2,2,2], [1,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts", 
                                  {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)       
        #M=2, N=200+ms,rollerStepValue=+5
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":2}, timeout=0.2)
        sleep(0.125)
        # #R=1,200ms前的累计时间=0.1,rollerStepValue=-1
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-1}, timeout=0.25)
        
    @allure.title("滚轮调速方案_绝对值>12(由负变正)")
    @pytest.mark.full
    def test_caseid_1985935(self):
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 2) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 2, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)                                      
        self.set_L2roller_signal([2,2,2,2], [1,1,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)   
        self.set_L2roller_signal([0,0,0,0], [0,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07) 
        self.set_L2roller_signal([1,1,1,1], [2,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)     
        
        #M=4, N=200+ms,rollerStepValue=-5
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-5}, timeout=0.1)
        sleep(0.125)
        # #R=2,200ms前的累计时间=0.1,rollerStepValue=5
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":5}, timeout=0.25)
        
    @allure.title("滚轮调速方案_绝对值<12(由负变正)")
    @pytest.mark.full
    def test_caseid_1987105(self):
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 2) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)                                      
        self.set_L2roller_signal([2,2,2,2], [1,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)   
        self.set_L2roller_signal([0,0,0,0], [0,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07) 
        self.set_L2roller_signal([1,1,1,1], [1,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)     
        
        #M=2, N=200+ms,rollerStepValue=-2
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-2}, timeout=0.1)
        sleep(0.125)
        # #R=1,200ms前的累计时间=0.1,rollerStepValue=1
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":1}, timeout=0.25)
        
    @allure.title("滚轮调速方案_快滚(由正变负)")
    @pytest.mark.sanity
    def test_caseid_1988189(self):
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 2, send_pdu_immediately=True) 
        self.partner.ck_coming_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)                                      
        self.set_L2roller_signal([1,1,1,1], [1,1,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)  
        self.set_L2roller_signal([0,0,0,0], [0,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07) 
        self.set_L2roller_signal([2,2,2,2], [2,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)       

        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":5,"rollSpeed":0}, timeout=0.2)
        sleep(0.125)
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-5,"rollSpeed":0}, timeout=0.25)
        
    @allure.title("滚轮调速方案_慢速(由正变负)")
    @pytest.mark.full
    def test_caseid_1988190(self):
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_coming_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)                                      
        self.set_L2roller_signal([1,1,1,1], [1,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)  
        self.set_L2roller_signal([0,0,0,0], [0,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07) 
        self.set_L2roller_signal([2,2,2,2], [1,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)       

        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":2,"rollSpeed":1}, timeout=0.2)
        sleep(0.125)
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-1,"rollSpeed":1}, timeout=0.25)
        
    @allure.title("滚轮调速方案_快滚(由负变正)")
    @pytest.mark.full
    def test_caseid_1988191(self):
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 2) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 2, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)                                      
        self.set_L2roller_signal([2,2,2,2], [1,1,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)   
        self.set_L2roller_signal([0,0,0,0], [0,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07) 
        self.set_L2roller_signal([1,1,1,1], [2,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)     
        
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-5,"rollSpeed":0}, timeout=0.1)
        sleep(0.125)
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":5,"rollSpeed":0}, timeout=0.25)
        
    @allure.title("滚轮调速方案_慢速(由负变正)")
    @pytest.mark.full
    def test_caseid_1988192(self):
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 2) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)                                      
        self.set_L2roller_signal([2,2,2,2], [1,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)   
        self.set_L2roller_signal([0,0,0,0], [0,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07) 
        self.set_L2roller_signal([1,1,1,1], [1,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)     
        
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-2,"rollSpeed":1}, timeout=0.1)
        sleep(0.125)
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":1,"rollSpeed":1}, timeout=0.25)
        
    @allure.title("滚轮调速方案_200ms前的累计时间|>12(由正变0)")
    @pytest.mark.sanity
    def test_caseid_1985937(self):
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)                                      
        self.set_L2roller_signal([1,1,1,1], [1,1,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)   
        self.set_L2roller_signal([1,1,1,1], [1,1,1,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":3},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07) 
        sleep(0.2)
        # #R=6,200ms前的累计时间=200ms+,rollerStepValue=5
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":5}, timeout=0.25)
        
    @allure.title("滚轮调速方案_200ms前的累计时间|<12(由正变0)")
    @pytest.mark.smoke
    def test_caseid_1987106(self):
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)   
        for i in range(5):                                 
            self.set_L2roller_signal([1,1,1,1], [1,0,0,0], 0.015)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                                {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)   
        sleep(0.125)
        # #R=6,200ms前的累计时间=600ms+,rollerStepValue=5
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":6}, timeout=0.25)
        
    @allure.title("滚轮调速方案_200ms前的累计时间|>12(由负变0)")
    @pytest.mark.smoke
    def test_caseid_1985938(self):
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 2) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)                                      
        self.set_L2roller_signal([2,2,2,2], [1,1,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)   
        self.set_L2roller_signal([2,2,2,2], [1,1,1,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":3},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07) 
        sleep(0.2)
        # #R=-6,200ms前的累计时间=200ms+,rollerStepValue=5
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-5}, timeout=0.25)
        
    @allure.title("滚轮调速方案_200ms前的累计时间|<12(由负变0)")
    @pytest.mark.full
    def test_caseid_1987107(self):
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 2) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)  
        for i in range(5):                                 
            self.set_L2roller_signal([2,2,2,2], [1,0,0,0], 0.015)
            self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                                {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)   
        sleep(0.125)
        # #R=-6,200ms前的累计时间=500ms+,rollerStepValue=5
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-6}, timeout=0.25)
    
    @allure.title("滚轮调速方案_isFault&fault赋值逻辑_方向由正到负")
    @pytest.mark.full
    def test_caseid_1985940(self): 
        #只能在非造一个100ms周期 变为falut
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        self.set_L2roller_signal([2,1,3,3], [1,5,1,1], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":4},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        self.set_L2roller_signal([3,3,2,2], [1,1,1,0], 0.02)
        #fault即时到期
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":True,"fault":[1]}}},timeout=0.07)
        #滚动100ms记时到期
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)  
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":5}, timeout=0.25)
        
    @allure.title("滚轮调速方案_isFault&fault赋值逻辑_方向由负到正")
    @pytest.mark.full
    def test_caseid_1985941(self): 
        #只能在非造一个100ms周期 变为falut
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 2) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        self.set_L2roller_signal([1,2,3,3], [1,5,1,1], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":4},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.06) 
        self.set_L2roller_signal([3,3,1,1], [1,1,1,0], 0.02)
        #fault即时到期
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":True,"fault":[1]}}},timeout=0.07)
        #滚动100ms记时到期
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)  
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-5}, timeout=0.25)

    @allure.title("滚轮调速方案_前置条件不满足(R2按键发送信号)")
    @pytest.mark.full
    def test_caseid_1985946(self):
        self.write_ccp_by_tcp({970:1})
        self.set_R2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidRi1ETHScButtUpDnStp", 1, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02)                                      
        self.set_R2roller_signal([1,1,1,1], [1,1,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)  
        self.set_R2roller_signal([2,2,2,2], [1,0,0,0], 0.015)
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelR2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.07)       
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller")   
        
    @allure.title("滚轮调速方案_多次随机滚动")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1985948(self): 
        self.set_L2roller_stop()
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHUpDnSts", 1) 
        self.bgm_eth_inter.set_signal("ScButtUpDnStpMidLe1ETHScButtUpDnStp", 5, send_pdu_immediately=True) 
        self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":5},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.02) 
        last_flag = 1
        current_flag = 0
        for i in range(100):
            logger.info(f"i={i}")
            sum = 0
            while sum == 0:
                sts = [random.randint(1, 2) for _ in range(4)]
                stp = [random.randint(2, 63) for _ in range(4)]
                sum = self.get_sum(sts,stp)
            self.set_L2roller_signal(sts, stp, 0.015)
            if sum > 0:
                current_flag = 1
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":1,"step":sum},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.08)      
            else:
                current_flag = 2
                self.partner.ck_s2s_event(STEERWHEEL_SERVICE_CLIENT, "SteerWheelL2ButtonSts",
                                            {"buttonSts":{"stsInfo":{"sts":2,"step":abs(sum)},"faultInfo":{"isFault":False,"fault":[0]}}},timeout=0.08) 
            
            logger.info(f"last_flag={last_flag},current_flag={current_flag}")
            if last_flag == current_flag :
                self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller",0.01)
            elif last_flag > current_flag:
                self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-5}, timeout=0.03)
            elif last_flag < current_flag:          
                self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":5}, timeout=0.03)
            last_flag = current_flag
            

    