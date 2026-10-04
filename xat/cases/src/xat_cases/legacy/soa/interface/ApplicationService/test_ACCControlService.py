#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_ReverseProxyService.py
@Time         :2023/04/08 17:20:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import allure
import pytest
import random
from time import sleep
from random import randint
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.digital_key_s2s import DigitalKeyPartner
from xat_cases.legacy.soa.case_helper.gnss_server import *
from xat_ecu.legacy.driver.ssh_interface import command_send


STEERWHEEL_SERVICE_SERVER = "SteerWheelService_server"
CARCONFIG_SERVICE_SERVER = "CarConfigService_server"

@allure.feature("SOA服务接口")
@allure.story("BGM应用/ACCControlService")
@pytest.mark.zjb
class TestACCControlService(TestBase):

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = DigitalKeyPartner([
            RPAAPA_SERVICE_SERVER,
            AVP_SERVICE_SERVER,
            ACC_SERVICE_SERVER,
            INTERACTIVE_SERVICE_SERVER
        ])
        self.partner.register_callback(RPAAPA_SERVICE_SERVER, self.partner.on_GetAPAStatus)
        self.ipdu.send_pdu('chassiscan1', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('chassiscan2', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEKeyPrsntStsZone7', 'Validity_NotValid')
        self.partner.empty_all(0.5)
        self.dk.empty_dk_data_queue()

    def after_each_func(self, ecu):
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 0)
        if ecu.get("testresult") != "Pass":
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER,
                                           "NotifyPASetResponse", {"paSetResponse": 2})
            sleep(1)
        super().after_each_func(ecu, start=False)

    def ck_SetACCSpeedStep(self, value1, value2, value3):
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 0)
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', value1)
        logger.info(f"set信号{value1}")
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', value2)
        logger.info(f"set信号{value2}")
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStep", {"stepValue": value2}, timeout=0.4)
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStep", {"stepValue": value2}, timeout=0.650 + 0.1)  # 第一个偶发timer有偏差，SOA-21169
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStep", {"stepValue": value2}, timeout=0.500 + 0.05)
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStep", {"stepValue": value2}, timeout=0.300 + 0.05)
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStep", {"stepValue": value2}, timeout=0.200 + 0.05)
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStep", {"stepValue": value2}, timeout=0.200 + 0.05)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', value3)
        logger.info(f"set信号{value3}")
        self.partner.empty_all(0.4)
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStep")

    @allure.title("设置自适应巡航速度梯度调节_0->非0")
    @pytest.mark.full
    def test_caseid_105108(self):
        for x in range(1, 6):
            logger.info(x)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 0)
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', x)
            if x in [1, 3]:
                self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStep", {"stepValue": x})
            else:
                self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStep")

    @allure.title("设置自适应巡航速度梯度调节_1->非1")
    @pytest.mark.full
    def test_caseid_105112(self):
        for x in [0, 2, 3, 4, 5]:
            logger.info(x)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 1)
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', x)
            if x == 2:
                self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStep", {"stepValue": x})
            else:
                self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStep")

    @allure.title("设置自适应巡航速度梯度调节_2->非2")
    @pytest.mark.full
    def test_caseid_105114(self):
        for x in [0, 1, 3, 4, 5]:
            logger.info(x)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 2)
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', x)
            self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStep")

    @allure.title("设置自适应巡航速度梯度调节_3->非3")
    @pytest.mark.full
    def test_caseid_105109(self):
        for x in [0, 1, 2, 4, 5]:
            logger.info(x)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 3)
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', x)
            if x in [4]:
                self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStep", {"stepValue": x})
            else:
                self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStep")

    @allure.title("设置自适应巡航速度梯度调节_4->非4")
    @pytest.mark.full
    def test_caseid_105111(self):
        for x in [0, 1, 2, 3, 5]:
            logger.info(x)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 4)
            self.partner.empty_all(0.2)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', x)
            self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStep")

    @allure.title("设置自适应巡航速度梯度调节_5->非5")
    @pytest.mark.full
    def test_caseid_105113(self):
        for x in [0, 1, 2, 3, 4]:
            logger.info(x)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 5)
            self.partner.empty_all(0.2)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', x)
            self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStep")

    @allure.title("设置自适应巡航速度梯度调节_1->2并保持->0")
    @pytest.mark.smoke
    def test_caseid_105123(self):
        self.ck_SetACCSpeedStep(1, 2, 0)

    @allure.title("设置自适应巡航速度梯度调节_1->2并保持->1")
    @pytest.mark.full
    def test_caseid_105096(self):
        self.ck_SetACCSpeedStep(1, 2, 1)

    @allure.title("设置自适应巡航速度梯度调节_1->2并保持->3")
    @pytest.mark.sanity
    def test_caseid_105069(self):
        self.ck_SetACCSpeedStep(1, 2, 3)

    @allure.title("设置自适应巡航速度梯度调节_1->2并保持->4")
    @pytest.mark.full
    def test_caseid_105089(self):
        self.ck_SetACCSpeedStep(1, 2, 4)

    @allure.title("设置自适应巡航速度梯度调节_1->2并保持->5")
    @pytest.mark.full
    def test_caseid_105121(self):
        self.ck_SetACCSpeedStep(1, 2, 5)

    @allure.title("设置自适应巡航速度梯度调节_3->4并保持->0")
    @pytest.mark.full
    def test_caseid_105095(self):
        self.ck_SetACCSpeedStep(3, 4, 0)

    @allure.title("设置自适应巡航速度梯度调节_3->4并保持->1")
    @pytest.mark.full
    def test_caseid_105074(self):
        self.ck_SetACCSpeedStep(3, 4, 1)

    @allure.title("设置自适应巡航速度梯度调节_3->4并保持->2")
    @pytest.mark.sanity
    def test_caseid_105070(self):
        self.ck_SetACCSpeedStep(3, 4, 2)

    @allure.title("设置自适应巡航速度梯度调节_3->4并保持->3")
    @pytest.mark.full
    def test_caseid_105090(self):
        self.ck_SetACCSpeedStep(3, 4, 3)

    @allure.title("设置自适应巡航速度梯度调节_3->4并保持->5")
    @pytest.mark.full
    def test_caseid_105105(self):
        self.ck_SetACCSpeedStep(3, 4, 5)

    @allure.title("设置跟车时距档位_SteerWhlScLeftButtonLe仅0到1调用SetFollowDistanceLevel.AdjusetSet=2")
    @pytest.mark.sanity
    def test_caseid_105119(self):
        for i in range(4):
            for j in range(4):
                logger.info(f"{i}->{j}")
                if i == j:
                    continue
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02,
                              'SteerWhlScLeftButtonLeSteerWhlTouchSwt2_0_SwtlBodySignalIPdu02', i)
                self.partner.empty_all(0.5)
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02,
                              'SteerWhlScLeftButtonLeSteerWhlTouchSwt2_0_SwtlBodySignalIPdu02', j)
                if i == 0 and j == 1:
                    self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetFollowDistanceLevel", {"adjustSet": 2})
                else:
                    self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetFollowDistanceLevel", timeout=0.3)

    @allure.title("设置跟车时距档位_SteerWhlScRightButtonLe仅0到1调用SetFollowDistanceLevel.AdjusetSet=1")
    @pytest.mark.sanity
    def test_caseid_105100(self):
        for i in range(4):
            for j in range(4):
                logger.info(f"{i}->{j}")
                if i == j:
                    continue
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02,
                              'SteerWhlScRightButtonLeSteerWhlTouchSwt2_0_SwtlBodySignalIPdu02', i)
                self.partner.empty_all(0.5)
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02,
                              'SteerWhlScRightButtonLeSteerWhlTouchSwt2_0_SwtlBodySignalIPdu02', j)
                if i == 0 and j == 1:
                    self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetFollowDistanceLevel", {"adjustSet": 1})
                else:
                    self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetFollowDistanceLevel", timeout=0.3)
    
    @allure.title("设置自适应巡航速度梯度调节_冷启15s内可用")
    @pytest.mark.full
    def test_caseid_1983942(self):
        self.ipdu.pause_all_bus_send()
        sleep(1)
        self.bgm_power_off_and_on(timeout=0)
        self.partner.empty_all()
        self.ipdu.resume_all_bus_send()
        t1 = time.time()
        self.partner.wait_for_service_reconnect(ACC_SERVICE_SERVER)
        for _ in range(10):
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 0)
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 1)
            try:
                self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStep", {"stepValue": 1})
            except Exception as e:
                pass
            else:
                break
        assert time.time() - t1 < 15, "启动后15s内可用"

    @allure.title("设置跟车时距档位_冷启15s内可用")
    @pytest.mark.full
    def test_caseid_1983947(self):
        self.ipdu.pause_all_bus_send()
        sleep(1)
        self.bgm_power_off_and_on(timeout=0)
        self.partner.empty_all()
        self.ipdu.resume_all_bus_send()
        t1 = time.time()
        self.partner.wait_for_service_reconnect(ACC_SERVICE_SERVER)
        for _ in range(20):  # 20 * 0.5 = 10s, 加上上电到服务连接肯定超过15s了
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2', 0)
            self.partner.empty_all(0.2)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScRightButtonLeSteerWhlTouchSwt2', 1)
            try:
                self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetFollowDistanceLevel", {"adjustSet": 1}, timeout=0.3)
            except Exception as e:
                pass
            else:
                break
        assert time.time() - t1 < 15, "启动后15s内可用"


@allure.feature("SOA服务接口")
@allure.story("BGM应用/ACCControlService")
@pytest.mark.ypp
class TestACCCService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        for process_name in ["monitor_em2.sh", "em2", "s2s_service", "service_monitor"]:
            res = command_send(
                device_name="BGM",
                cmd=f"ps -ef |grep app |grep {process_name} |grep -v grep",
                timeout=60,
            )[1]
            pid = res.split()[1]
            command_send(device_name="BGM", cmd=f"kill -9 {pid}")
        sleep(10)
        command_send(device_name="BGM", cmd='su - service_monitor -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;/app/bin/service_monitor  -c /app/etc/service_monitor.json &"', timeout=5)
        
        self.partner = S2sBaseClass([ACC_SERVICE_SERVER,
                                     STEERWHEEL_SERVICE_SERVER,
                                     CARCONFIG_SERVICE_SERVER])
        self.partner.method_default_timeout = 0.1
        self.partner.wait_for_service_reconnect(ACC_SERVICE_SERVER)
        sleep(10)
        
    def after_class(self, ecu):
        self.partner.stop_operators()
        sleep(4)
        self.bgm_power_off_and_on(self, timeout=1)
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.send_event_notify(CARCONFIG_SERVICE_SERVER, "NotifyConfigList",
                                           {"list": [{"name": 970, "value": 1}]})
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelButtonInhibit", {"opts": 0})
        self.partner.empty_all(1)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)
    
    
    @allure.title("滚轮调速方案_前置条件不满足(ccp=0)")
    @pytest.mark.full
    def test_caseid_1985790(self):
        self.partner.send_event_notify(CARCONFIG_SERVICE_SERVER, "NotifyConfigList",
                                           {"list": [{"name": 970, "value": 0}]})
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelButtonInhibit", {"opts": 0})
        self.partner.empty_all(1)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        sleep(0.1)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller")
    
    @allure.title("滚轮调速方案_前置条件不满足(R2按键发送信号)")
    @pytest.mark.full
    def test_caseid_1985843(self):
        self.partner.send_event_notify(CARCONFIG_SERVICE_SERVER, "NotifyConfigList",
                                           {"list": [{"name": 970, "value": 1}]})
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelR2ButtonSts", {"opts": 0})
        self.partner.empty_all(1)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelR2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        sleep(0.1)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelR2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller")
    
    @allure.title("滚轮调速方案_方向盘按键抑制激活-未激活")
    @pytest.mark.full
    def test_caseid_1985791(self):
        self.partner.send_event_notify(CARCONFIG_SERVICE_SERVER, "NotifyConfigList",
                                           {"list": [{"name": 970, "value": 1}]})
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelButtonInhibit", {"opts": 1})
        self.partner.empty_all(1)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        sleep(0.1)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller")
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelButtonInhibit", {"opts": 2})
        sleep(1)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts":{"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        sleep(0.1)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-1})#M=1/N=0.1 
    
    @allure.title("滚轮调速方案_方向盘按键抑制未激活-激活")
    @pytest.mark.sanity
    def test_caseid_1985796(self):
        self.partner.send_event_notify(CARCONFIG_SERVICE_SERVER, "NotifyConfigList",
                                           {"list": [{"name": 970, "value": 1}]})
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelButtonInhibit", {"opts": 0})
        self.partner.empty_all(1)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        sleep(0.1)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {}, timeout=0.1)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelButtonInhibit", {"opts": 3})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.5)
    
    @allure.title("滚轮调速方案_绝对值<12(由正变负)")
    @pytest.mark.smoke
    def test_caseid_1985793(self):
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.0125)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.0125)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2, "step":3},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":2}, timeout=0.1)#2/0.233=8.583(<12,所以k*m)
        sleep(0.125)
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-5})#3/0.125=24(>12,所以取值为-5)
    
    @allure.title("滚轮调速方案_绝对值<12(由负变正)")
    @pytest.mark.full
    def test_caseid_1985807(self):
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.0125)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.0125)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1, "step":3},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-2}, timeout=0.1)
        sleep(0.125)
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":5})
    
    @allure.title("滚轮调速方案_绝对值>12(由正变负)")
    @pytest.mark.sanity
    def test_caseid_1985801(self):
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":3},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":5}, timeout=0.1)
        sleep(0.125)
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-1})
    
    @allure.title("滚轮调速方案_绝对值>12(由负变正)")
    @pytest.mark.smoke
    def test_caseid_1985802(self):
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":3},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-5}, timeout=0.1)
        sleep(0.125)
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":1})
        
    @allure.title("模拟服务端发送通知设置滚轮调速方案_快速(由正变负)")
    @pytest.mark.sanity
    def test_caseid_1988194(self):
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.0125)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.0125)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2, "step":3},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":2,"rollSpeed":1}, timeout=0.1)#2/0.233=8.583(<12,所以k*m)
        sleep(0.125)
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-5,"rollSpeed":0})#3/0.125=24(>12,所以取值为-5)
    
    @allure.title("模拟服务端发送通知设置滚轮调速方案_快速(由负变正)")
    @pytest.mark.full
    def test_caseid_1988196(self):
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.0125)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.0125)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1, "step":3},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-2,"rollSpeed":1}, timeout=0.1)
        sleep(0.125)
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":5,"rollSpeed":0})
    
    @allure.title("模拟服务端发送通知设置滚轮调速方案_慢速(由正变负)")
    @pytest.mark.full
    def test_caseid_1988197(self):
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":3},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":5,"rollSpeed":0}, timeout=0.1)
        sleep(0.125)
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-1,"rollSpeed":1})
    
    @allure.title("模拟服务端发送通知设置滚轮调速方案_慢速(由负变正)")
    @pytest.mark.full
    def test_caseid_1988198(self):
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":3},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-5,"rollSpeed":0}, timeout=0.1)
        sleep(0.125)
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":1,"rollSpeed":1})
    
    @allure.title("滚轮调速方案_R/200ms前的累计时间|>12(由正变0)")
    @pytest.mark.full
    def test_caseid_1985804(self):
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":5}, timeout=0.125)
    
    @allure.title("滚轮调速方案_R/200ms前的累计时间|>12(由负变0)")
    @pytest.mark.full
    def test_caseid_1985806(self):
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.1)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.1)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-5}, timeout=0.125)
    
    @allure.title("滚轮调速方案_R/200ms前的累计时间|<12(由正到0)")
    @pytest.mark.full
    def test_caseid_1985808(self):
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        sleep(0.125)
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":4})#1/0.2=5<8 k*m=1
    
    @allure.title("滚轮调速方案_R/200ms前的累计时间|<12(由负到0)")
    @pytest.mark.sanity
    def test_caseid_1985809(self):
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.09)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":0,"step":0},"faultInfo":{"isFault":False,"fault":[0]}}})
        sleep(0.125)
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-4})#1/0.2=5<8 k*m=1
    
    @allure.title("滚轮调速方案_绝对值<12(有故障时)")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1985812(self):
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.05)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.05)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":True,"fault":[1]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.05)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":5}, timeout=0.05)#2/0.15=13.3333>8  +5
        
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":True,"fault":[1]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.05)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":True,"fault":[1]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.05)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":2},"faultInfo":{"isFault":False,"fault":[0]}}})
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue":-1}, timeout=0.012)#1/0.116=8.11>8 -5

        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":True,"fault":[1]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.05)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":1,"step":1},"faultInfo":{"isFault":True,"fault":[1]}}})
        self.partner.ck_no_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", timeout=0.05)
        self.partner.send_event_notify(STEERWHEEL_SERVICE_SERVER, "SteerWheelL2ButtonSts",
                                       {"buttonSts": {"stsInfo":{"sts":2,"step":1},"faultInfo":{"isFault":True,"fault":[1]}}})
        self.partner.ck_s2s_req(ACC_SERVICE_SERVER, "SetACCSpeedStepWithRoller", {"rollerStepValue": 5}, timeout=0.1)#2/0.15>8
    