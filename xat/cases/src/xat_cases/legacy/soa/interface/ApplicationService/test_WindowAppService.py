"""
@File         :test_WindowAppService.py
@Time         :2023/04/30 19:07:31
@Author       :tao.cheng_ext@jiduauto.com
@Description  :Test SOA for WindowAppService
"""

import os
import sys
import pytest
import allure
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *


@allure.feature("SOA服务接口")
@allure.story("BGM应用/WindowAppService")
class TestWindowAppService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([
            ("WindowAppService", "client"),
            ("WindowService", "client"),])
        self.partner.method_default_timeout = 2
        self.sd_tester.tester_present()
        self.ipdu.send_pdu('chassiscan1', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('chassiscan2', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('propulsioncan', 0x516, [0x16, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.sd_tester.change_usage_mode(1)
        self.partner.empty_all(2)

    def after_each_func(self, ecu):
        self.ipdu.reset_check_results()
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.dk.stop_listen_dk_bgm_response()
        self.sd_tester.stop_tester_present()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    @pytest.mark.smoke
    @allure.title("车窗远控位置控制_副驾车窗打开")
    def test_caseid_105764(self):
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 20)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition",
                                         {"windows": [{"id": 1, "position": 100}]})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 26, timeout=0.5)

    @pytest.mark.sanity
    @allure.title("车窗远控位置控制_车窗全关（左后不处于全开）")
    def test_caseid_105716(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 26)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 26)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 20)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 26)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition",
                                         {"windows": [{"id": 4, "position": 0}]})
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 21)
        sleep(0.2)
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 1),
                                         (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1)])
        
    @pytest.mark.full
    @allure.title("车窗远控位置控制_全关scene2")
    def test_caseid_105719(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 20)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 20)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 20)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 20)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition",
                                         {"windows": [{"id": 4, "position": 0}]})
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 21)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 21)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 21)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 21)
        sleep(0.5)
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 1),
                                         (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1)])

    @pytest.mark.sanity
    @allure.title("车窗远控位置控制_副驾车窗关闭scene1")
    def test_caseid_105780(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 26)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 20)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 26)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 26)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition",
                                         {"windows": [{"id": 1, "position": 0}]})
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 21)
        sleep(0.2)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 0, timeout=0.5)

    @allure.title("车窗远控位置控制_车窗全关（副驾、左后不处于全开）")
    @pytest.mark.full
    def test_caseid_105705(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 26)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 19)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 19)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 26)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition",
                                         {"windows": [{"id": 4, "position": 0}]})
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 20)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 20)
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1)])
        
    @allure.title("车窗远控位置控制_车窗全关（主驾不处于全开）")
    @pytest.mark.full
    def test_caseid_105703(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 18)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 26)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 26)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 26)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition",
                                         {"windows": [{"id": 4, "position": 0}]})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 19, timeout=0.5)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 19)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1, timeout=0.5)
        
    @allure.title("车窗远控位置控制_车窗全关（主副驾不处于全开）")
    @pytest.mark.full
    def test_caseid_105715(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 17)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 17)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 26)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 26)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition",
                                         {"windows": [{"id": 4, "position": 0}]})
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 18)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 18)
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1)])
        
    @allure.title("车窗远控位置控制_右后车窗打开")
    @pytest.mark.sanity
    def test_caseid_105743(self):
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 20)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition",
                                         {"windows": [{"id": 3, "position": 100}]})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 26, timeout=0.5)

    @allure.title("车窗远控位置控制_左后车窗打开")
    @pytest.mark.full
    def test_caseid_105788(self):
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 20)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition",
                                         {"windows": [{"id": 2, "position": 100}]})
        sleep(0.2)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 26, timeout=0.5)

    @allure.title("车窗远控位置控制_主驾车窗打开")
    @pytest.mark.full
    def test_caseid_105749(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 20)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition",
                                         {"windows": [{"id": 0, "position": 100}]})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 26, timeout=0.5)

    @allure.title("车窗远控位置控制_打开全部车窗")
    @pytest.mark.smoke
    def test_caseid_105707(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 19)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 19)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 19)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 19)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition",
                                         {"windows": [{"id": 4, "position": 100}]})
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 26),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 26),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 26),
                                         (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 26)])
        
    @allure.title("车窗远控位置控制_主驾车窗关闭scene1")
    @pytest.mark.full
    def test_caseid_105761(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 19)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 26)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 26)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 26)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition",
                                         {"windows": [{"id": 0, "position": 0}]})
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 20)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1, timeout=0.5)
        
    @allure.title("车窗远控位置控制_车窗全关（副驾、右后不处于全开）")
    @pytest.mark.sanity
    def test_caseid_105732(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 26)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 19)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 26)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 19)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition",
                                         {"windows": [{"id": 4, "position": 0}]})
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 20),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 20)])
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 20)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 20)
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 1),
                                         (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1)])
        
    @allure.title("车窗远控位置控制_车窗全关（主驾、左后不处于全开）")
    @pytest.mark.sanity
    def test_caseid_105729(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 15)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 26)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 15)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 26)
        sleep(1)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition",
                                         {"windows": [{"id": 4, "position": 0}]})
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 16)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 16)
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1)])
        
    @allure.title("遍历设置雨天自动关窗_打开或关闭")
    @pytest.mark.sanity
    def test_caseid_105723(self):
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetRainAutoCloseWindow", {"isOn": True})
        self.partner.empty_all(0.5)
        for state in [False, True]:
            self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, 
                                             "SetRainAutoCloseWindow", {"isOn": state})
            self.partner.ck_s2s_event(WINDOWS_APP_SERVICE_CLIENT, "RainAutoCloseWindowStatus", {"sts": state})
            self.partner.send_request_and_ck_resp(WINDOWS_APP_SERVICE_CLIENT, 
                                                  "GetRainAutoCloseWindowStatus", {}, {"out": state})
            
    @allure.title("WindowAppService重启上电默认值")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1984587(self):
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetRainAutoCloseWindow", {"isOn": False})
        self.restart_bgm_and_connect_service(WINDOWS_APP_SERVICE_CLIENT)
        self.partner.ck_s2s_event(WINDOWS_APP_SERVICE_CLIENT, "RainAutoCloseWindowStatus", {"sts": False})

    @allure.title("设置雨天自动关窗_断电记忆打开")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_105702(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetRainAutoCloseWindow", {"isOn": True})
        sleep(1)
        self.restart_bgm_and_connect_service(WINDOWS_APP_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(WINDOWS_APP_SERVICE_CLIENT, "GetRainAutoCloseWindowStatus", {},  {"out": True})

    @allure.title("第一次远控车窗_5S内恢复总线_应该立即发出请求")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1903646(self):
        self.ipdu.pause_all_bus_send()
        self.nucapp.bgm_power_off()
        sleep(3)
        self.nucapp.bgm_power_on()
        sleep(15)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition",
                                         {"windows": [{"id": 4, "position": 100}]})
        self.ipdu.resume_all_bus_send()
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 1)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 1)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 1)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 1)
        sleep(0.5)
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 26),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 26),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 26),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 26)])
        
    @allure.title("压测重启远控车窗_10次")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1984666(self):
        for i in range(10):
            logger.info(f"第{i}次压测")
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 15)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 26)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 15)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 26)
            sleep(1)
            self.restart_bgm_and_connect_service(WINDOWS_APP_SERVICE_CLIENT)
            self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition",
                                            {"windows": [{"id": 4, "position": 0}]},timeout=1)
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 16)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 16)
            sleep(0.5)
            self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1),
                                            (self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1),
                                            (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 1),
                                            (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1)])


