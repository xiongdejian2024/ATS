# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_alm.py
@Time         :2024/03/14 14:20:31
@Author       :xiangyue.li@jiduauto.com
@Description  :BGM车控车设氛围灯
"""
from time import sleep
import pytest
from xat_ecu.legacy.sdk.sdk_tools import *

from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_cases.legacy.soa.case_helper.utils import ck_pdu_period_time, ck_pdu_sporadic
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *

@allure.feature("SOA服务接口")
@allure.story("整车控制/LightService")  # 转向灯
@pytest.mark.peipei
class TestLightServiceTurnLamp(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.diagnostic_client_sim_start()
        self.sd_tester.tester_present()
        self.ipdu.set_vehspd(0)  # 车速
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        # 放在beforecase
        self.bgm_tcpdump = BGM_SSH()
        self.bgm_tcpdump.init_bgm_tcpdump()
        # 启动partner operator
        self.partner = S2sBaseClass([("LightService", "client"),
                                     ("SteerWheelService", "client"),
                                     ("CarConfigService", "client")])
        sleep(5)
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟(数据库周期性报文和调度表)
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        # 检查上位机上是否有其它未关闭的soa_partner进程在运行，如果有，则杀死进程

    def before_each_func(self, ecu):
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 0)
        sleep(0.5)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 255}})
        self.partner.empty_all()
        super().before_each_func(ecu, start=False)

    def after_each_func(self, ecu):
        self.ipdu.set_vehspd(0.0)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "VehMtnStVehMtnSt", 3)
        sleep(0.5)
        self.sd_tester.change_usage_mode(1)
        sleep(0.5)
        self.sd_tester.change_car_mode(0)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 255}})
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        try:
            self.sd_tester.change_usage_mode(1)
            self.sd_tester.change_car_mode(0)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        self.ipdu.time_control_stop()  # 停止数据模拟(数据库周期性报文和调度表)
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，总线开始收发报文
        self.partner.stop_operators()
        self.sd_tester.stop_tester_present()
        sleep(0.5)
        self.sd_tester.diagnostic_client_sim_close()
        sleep(0.5)
        # 检查上位机上是否有其它未关闭的soa_partner进程在运行，如果有，则杀死进程
        partner_process_check()
        super().after_class(self, ecu)

        self.ipdu.set_vehspd(0)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 255}})

    @allure.title("普通氛围灯_Normal_Convenience_Brightness")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1980993(self):
        self.sd_tester.change_car_mode(5)
        self.sd_tester.change_usage_mode(2)
        self.sd_tester.write_single_ccp(950, 1)
        for b, R, G, B in [(1, 1, 0, 1),(99, 0, 1, 0), (100, 0, 0, 1), (50, 1, 0, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals(
                [(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', b),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', R),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', G),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', B)])

    @allure.title("普通氛围灯_Normal_Convenience_Red")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1979645(self):
        self.sd_tester.change_car_mode(5)
        self.sd_tester.change_usage_mode(2)
        for b, R, G, B in [(1, 1, 0, 0),(99, 0, 0, 0), (100, 254, 0, 0), (0, 255, 0, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals(
                [(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', b),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', R),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', G),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', B)])
            
    @allure.title("普通氛围灯_Normal_Convenience_Green")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1979647(self):
        self.sd_tester.change_car_mode(5)
        self.sd_tester.change_usage_mode(2)
        for b, R, G, B in [(1, 0, 100, 0),(99, 0, 255, 0), (100, 0, 1, 0), (0, 0, 254, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals(
                [(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', b),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', R),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', G),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', B)])
            
    @allure.title("普通氛围灯_Normal_Convenience_Blue")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1979646(self):
        self.sd_tester.change_car_mode(5)
        self.sd_tester.change_usage_mode(2)
        for b, R, G, B in [(1, 0, 0, 1),(99, 0, 0, 254), (100, 0, 0, 255), (0, 0, 0, 50)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals(
                [(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', b),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', R),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', G),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', B)])
                        
    @allure.title("普通氛围灯_Dyno_Convenience_Brightness")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1985075(self):
        self.sd_tester.change_car_mode(5)
        self.sd_tester.change_usage_mode(2)
        for b, R, G, B in [(1, 1, 0, 1),(99, 0, 1, 0), (100, 0, 0, 1), (50, 1, 0, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals(
                [(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', b),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', R),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', G),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', B)])

    @allure.title("普通氛围灯_Dyno_Convenience_Red")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1979638(self):
        self.sd_tester.change_car_mode(5)
        self.sd_tester.change_usage_mode(2)
        for b, R, G, B in [(1, 1, 0, 0),(99, 50, 0, 0), (100, 254, 0, 0), (0, 255, 0, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals(
                [(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', b),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', R),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', G),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', B)])
            
    @allure.title("普通氛围灯_Dyno_Convenience_Green")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1979641(self):
        self.sd_tester.change_car_mode(5)
        self.sd_tester.change_usage_mode(2)
        for b, R, G, B in [(1, 0, 100, 0),(99, 0, 255, 0), (100, 0, 1, 0), (0, 0, 254, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals(
                [(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', b),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', R),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', G),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', B)])
            
    @allure.title("普通氛围灯_Dyno_Convenience_Blue")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1979640(self):
        self.sd_tester.change_car_mode(5)
        self.sd_tester.change_usage_mode(2)
        for b, R, G, B in [(1, 0, 0, 1),(99, 0, 0, 254), (100, 0, 0, 255), (0, 0, 0, 50)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals(
                [(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', b),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', R),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', G),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', B)])

    @allure.title("Dyno_Driving_ALM1_Red")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1979642(self):
        self.sd_tester.change_car_mode(5)
        self.sd_tester.change_usage_mode(13)
        for b, R, G, B in [(1, 1, 0, 0),(99, 50, 0, 0), (100, 254, 0, 0), (0, 255, 0, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals(
                [(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', b),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', R),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', G),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', B)])
            
    @allure.title("Dyno_Driving_ALM1_Green")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1979644(self):
        self.sd_tester.change_car_mode(5)
        self.sd_tester.change_usage_mode(13)
        for b, R, G, B in [(1, 0, 100, 0),(99, 0, 255, 0), (100, 0, 1, 0), (0, 0, 254, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals(
                [(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', b),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', R),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', G),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', B)])
            
    @allure.title("Dyno_Driving_ALM1_Blue")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1979643(self):
        self.sd_tester.change_car_mode(5)
        self.sd_tester.change_usage_mode(13)
        for b, R, G, B in [(1, 0, 0, 1),(99, 0, 0, 254), (100, 0, 0, 255), (0, 0, 0, 50)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals(
                [(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', b),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', R),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', G),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', B)])
                        
    @allure.title("Dyno_Driving_ALM1_Brightness")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1982968(self):
        self.sd_tester.change_car_mode(5)
        self.sd_tester.change_usage_mode(13)
        for b, R, G, B in [(1, 1, 0, 1),(99, 0, 1, 0), (100, 0, 0, 1), (50, 1, 0, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals(
                [(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', b),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', R),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', G),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', B)])
            
    # @allure.title("普通氛围灯_Dyno_Active_Brightness")
    # @pytest.mark.full
    # def test_intrlight_ctrl_caseid_1982969(self):
    #     self.sd_tester.change_car_mode(11)
    #     self.sd_tester.change_usage_mode(2)
    #     self.sd_tester.write_single_ccp(950, 1)
    #     for b, R, G, B in [(1, 1, 0, 0),(99, 0, 1, 0), (100, 0, 0, 1), (50, 1, 0, 0)]:
    #         self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
    #             {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
    #                 {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
    #         sleep(0.5)
    #         self.ipdu.check_multiple_signals(
    #             [(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', b),
    #             (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', R),
    #             (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', G),
    #             (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', B)])

    # @allure.title("普通氛围灯_Dyno_Active_Red")
    # @pytest.mark.full
    # def test_intrlight_ctrl_caseid_1980990(self):
    #     self.sd_tester.change_car_mode(11)
    #     self.sd_tester.change_usage_mode(2)
    #     self.sd_tester.write_single_ccp(950, 1)
    #     for b, R, G, B in [(1, 1, 0, 0),(99, 50, 0, 0), (100, 254, 0, 0), (0, 255, 0, 0)]:
    #         self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
    #             {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
    #                 {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
    #         sleep(0.5)
    #         self.ipdu.check_multiple_signals(
    #             [(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', b),
    #             (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', R),
    #             (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', G),
    #             (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', B)])
            
    @allure.title("Normal_Driving_ALM1_Red")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1979637(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.write_single_ccp(950, 1)
        for b, R, G, B in [(1, 1, 0, 0),(99, 50, 0, 0), (100, 254, 0, 0), (0, 255, 0, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals(
                [(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', b),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', R),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', G),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', B)])
            
    @allure.title("Normal_Driving_ALM1_Green")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1979623(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.write_single_ccp(950, 1)
        for b, R, G, B in [(1, 0, 100, 0),(99, 0, 255, 0), (100, 0, 1, 0), (0, 0, 254, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals(
                [(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', b),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', R),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', G),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', B)])
            
    @allure.title("Normal_Driving_ALM1_Blue")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1979624(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.write_single_ccp(950, 1)
        for b, R, G, B in [(1, 0, 0, 1),(99, 0, 0, 254), (100, 0, 0, 255), (0, 0, 0, 50)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals(
                [(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', b),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', R),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', G),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', B)])
            
    @allure.title("Normal_Driving_ALM1_brightness")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1983049(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.write_single_ccp(950, 1)
        for b, R, G, B in [(1, 1, 0, 1),(99, 0, 1, 0), (100, 0, 0, 1), (50, 1, 0, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals(
                [(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', b),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', R),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', G),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', B)])
    
    @allure.title("Venus_普通氛围灯_Normal_Convenience_Brightness1")
    @pytest.mark.sanity
    @pytest.mark.venus
    def test_caseid_1983131(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.write_single_ccp(950, 2)
        for b, R, G, B in [(20, 1, 55, 65),(30, 110, 155, 254), (100, 150, 255, 254), (0, 254, 254, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 25, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(1)
    
    @allure.title("Venus_普通氛围灯_Normal_Convenience_Brightness2")
    @pytest.mark.sanity
    @pytest.mark.venus
    def test_caseid_1983132(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.write_single_ccp(950, 2)
        for b, R, G, B in [(20, 1, 55, 65),(30, 110, 155, 254), (100, 150, 255, 254), (0, 254, 254, 0)]:

            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 25, "zoneId": 16}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
        self.sd_tester.write_single_ccp(950, 1)


    @allure.title("Normal_Convenience_ALM1禁用")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1960166(self):
        with allure.step(f"Step:设置初始条件"):
            # 车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            # 使用模式 Usage Mode=02 convenience
            self.sd_tester.change_usage_mode(2)
            self.partner.send_method_request(
                LIGHT_SERVICE_CLIENT,
                "SetAmbientInhibit",
                {"ambientInhibit": [{"type": 35, "inhibitSts": True}]},
            )
            self.partner.ck_s2s_event(
                LIGHT_SERVICE_CLIENT,
                "LightInhibitSts",
                {"sts": [{"type": 35, "inhibitSts": True}]},
            )
            self.partner.send_request_and_ck_resp(
                LIGHT_SERVICE_CLIENT,
                "GetLightInhibitSts",
                {"type": [35]},
                {"out": [{"type": 35, "inhibitSts": True}]},
            )
            self.ipdu.check(
                self.ipdu.cem_lin5.CemCem_Lin5Fr01,
                "OrdinaryAmbientLightFrontLeftRed",
                0,
            )
            self.ipdu.check(
                self.ipdu.cem_lin5.CemCem_Lin5Fr01,
                "OrdinaryAmbientLightFrontLeftGreen",
                0,
            )
            self.ipdu.check(
                self.ipdu.cem_lin5.CemCem_Lin5Fr01,
                "OrdinaryAmbientLightFrontLeftBrightness",
                0,
            )
            self.ipdu.check(
                self.ipdu.cem_lin5.CemCem_Lin5Fr01,
                "OrdinaryAmbientLightFrontLeftBrightness",
                0,
            )
        with allure.step(f"Step:调用氛围灯接口"):
            # 调取SOApartner
            self.partner.send_method_request(
                LIGHT_SERVICE_CLIENT,
                "LightShowControlWithLightDevice",
                {
                    "lights": [
                        {
                            "light": {"type": 35, "zoneId": 1},
                            "PixelData": [0],
                            "type": 0,
                            "color": [
                                {
                                    "brightness": 100,
                                    "color": {"cRed": 255, "cGreen": 255, "cBlue": 255},
                                }
                            ],
                        }
                    ]
                },
            )
            self.ipdu.check(
                self.ipdu.cem_lin5.CemCem_Lin5Fr01,
                "OrdinaryAmbientLightFrontLeftRed",
                0,
            )
            self.ipdu.check(
                self.ipdu.cem_lin5.CemCem_Lin5Fr01,
                "OrdinaryAmbientLightFrontLeftGreen",
                0,
            )
            self.ipdu.check(
                self.ipdu.cem_lin5.CemCem_Lin5Fr01,
                "OrdinaryAmbientLightFrontLeftBrightness",
                0,
            )
            self.ipdu.check(
                self.ipdu.cem_lin5.CemCem_Lin5Fr01,
                "OrdinaryAmbientLightFrontLeftBrightness",
                0,
            )
