# -*- coding: utf-8 -*-
"""
@File        : test_daily.py
@Author      : jiahong.wang_ext
@Time        : 2024/6/14 16:00 PM
@Description : Test SOA for DoorService
"""
import pytest
import allure
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.common.data_type_handing import logger
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_cases.legacy.soa.case_helper.utils import *

LOWVOLTAGE_SERVICE = "LowVoltageService_client"


@allure.feature("daily")                                  
@allure.story("停发总线和E2E故障的注入及恢复接口，信号，预期加入框架的daily验证")
@pytest.mark.mockmcu
class TestDoorServiceMockMcu(TestBase):

    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("ChassisService", "client"),
                                     ("DoorService", "client"),
                                     ("LowVoltageService", "client"),
                                     ("SteerWheelService", "client"),
                                     ("DrivingAssistService", "client"),
                                     ("GB32960Service", "client")])
        sleep(5)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)            
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu)
        sleep(10)

    def ck_GB32960Data_and_GetGB32960Data(self, ck_dict):
        """校验指定GB32960Data事件，并请求GetGB32960Data获取结果"""
        self.partner.ck_s2s_event(GB32960_SERVICE_CLIENT, "GB32960Data",
                                  {"info": ck_dict})
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": ck_dict})

    @allure.title("单独停止和恢复bodycan")
    @pytest.mark.full
    def test_daily_1(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 2)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorOpenerPassSts", 0)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorPassAntiPnch", 0)
        sleep(1)
        logger.info(f"开始停发总线*****************************")
        self.ipdu.pause_bus_send("bodycan")
        sleep(1.5)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorSts", {"sts":{"openCloseSts":{"isOpen": False, "isOpenValidity": 4}, "sts": 7, "isAntiPinch": False}}, timeout= 20)
        self.ipdu.resume_bus_send("bodycan")
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorSts", {"sts":{"openCloseSts":{"isOpen": False, "isOpenValidity": 0}, "sts": 7, "isAntiPinch": False}}, timeout= 20)

    @allure.title("停止所有总线和恢复查看can预期")
    @pytest.mark.full
    def test_daily_2(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 2)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorOpenerPassSts", 0)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorPassAntiPnch", 0)
        sleep(1)
        logger.info(f"开始停发总线*****************************")
        self.ipdu.pause_all_bus_send()
        sleep(1.5)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorSts", {"sts":{"openCloseSts":{"isOpen": False, "isOpenValidity": 4}, "sts": 7, "isAntiPinch": False}}, timeout= 20)
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorSts", {"sts":{"openCloseSts":{"isOpen": False, "isOpenValidity": 0}, "sts": 7, "isAntiPinch": False}}, timeout= 20)

    @allure.title("单独停止和恢复cem_lin4")
    @pytest.mark.sanity
    def test_daily_3(self):
        self.ipdu.set(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionHandsOnStatus', 1)
        self.ipdu.set(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionErrorStatus', 1)
        self.partner.empty_all(0.5)
        self.ipdu.pause_ecu_send("cem_lin4","HOD")
        sleep(1)
        self.partner.ck_s2s_event(DRIVINGASSIST_SERVICE_CLIENT, "handOFFSts",
                                  {"sts": {"onSts": 1, "errSts": 3}})
        self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "getHandOFFSts", {},
                                              {"out": {"onSts": 1, "errSts": 3}})
        self.ipdu.resume_ecu_send("cem_lin4","HOD")
        self.partner.ck_s2s_event(DRIVINGASSIST_SERVICE_CLIENT, "handOFFSts",
                                  {"sts": {"onSts": 1, "errSts": 1}}, timeout=1)
        self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "getHandOFFSts", {},
                                              {"out": {"onSts": 1, "errSts": 1}}, timeout=1)

    @allure.title("停止所有总线和恢复查看cem_lin4预期")
    @pytest.mark.sanity
    def test_daily_4(self):
        self.ipdu.set(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionHandsOnStatus', 1)
        self.ipdu.set(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionErrorStatus', 1)
        self.partner.empty_all(0.5)
        self.ipdu.pause_all_bus_send()
        sleep(1)
        self.partner.ck_s2s_event(DRIVINGASSIST_SERVICE_CLIENT, "handOFFSts",
                                  {"sts": {"onSts": 1, "errSts": 3}})
        self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "getHandOFFSts", {},
                                              {"out": {"onSts": 1, "errSts": 3}})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(DRIVINGASSIST_SERVICE_CLIENT, "handOFFSts",
                                  {"sts": {"onSts": 1, "errSts": 1}}, timeout=1)
        self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "getHandOFFSts", {},
                                              {"out": {"onSts": 1, "errSts": 1}}, timeout=1)

    @allure.title("单独停止和恢复backbonefr")
    @pytest.mark.full
    def test_daily_5(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',1)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',1) 
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',0)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',0) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":1,"validity":0}}, timeout=3)  
        self.partner.empty_all(2)    
        self.ipdu.pause_bus_send("backbonefr")   
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":1,"validity":4}}, timeout=2.5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":1,"validity":4}}) 
        self.ipdu.resume_bus_send("backbonefr") 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":1,"validity":0}})
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":1,"validity":0}})

    @allure.title("停止所有总线和恢复查看backbonefr预期")
    @pytest.mark.full
    def test_daily_6(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',1)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',1) 
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',0)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',0) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":1,"validity":0}}, timeout=3)  
        self.partner.empty_all(2)    
        self.ipdu.pause_all_bus_send()   
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":1,"validity":4}}, timeout=2.5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":1,"validity":4}}) 
        self.ipdu.resume_all_bus_send() 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":1,"validity":0}})
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":1,"validity":0}})

    @allure.title("E2E故障 backbonefr") 
    @pytest.mark.full
    def test_daily_7(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn', 1)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,"GetLowWarn",{},{"out":1})
        self.ipdu.set_no_crc(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn')
        sleep(0.5)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"LowWarn",{"warn":3})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn', 2)
        sleep(1)
        self.partner.ck_no_event(LOWVOLTAGE_SERVICE,"LowWarn")
        self.ipdu.restore_crc(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn')
        sleep(1)
        self.partner.ck_s2s_event(LOWVOLTAGE_SERVICE,"LowWarn",{"warn":2})
        self.partner.send_request_and_ck_resp(LOWVOLTAGE_SERVICE,"GetLowWarn",{},{"out":2})

    @pytest.mark.full
    @allure.title("E2E故障 bodycan")
    def test_daily_8(self):
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

    @allure.title("E2E故障 cem_lin4")
    @pytest.mark.full
    def test_daily_9(self):
        self.ipdu.set(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionHandsOnStatus', 1)
        self.ipdu.set(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionErrorStatus', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set_no_crc(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionHandsOnStatus')
        self.partner.ck_s2s_event(DRIVINGASSIST_SERVICE_CLIENT, "handOFFSts",
                                  {"sts": {"onSts": 1, "errSts": 3}})
        self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "getHandOFFSts", {},
                                              {"out": {"onSts": 1, "errSts": 3}})
        self.ipdu.restore_crc(self.ipdu.cem_lin4.HodDim_Lin1Fr04, 'HandsOnDetectionHandsOnStatus')
        self.partner.ck_s2s_event(DRIVINGASSIST_SERVICE_CLIENT, "handOFFSts",
                                  {"sts": {"onSts": 1, "errSts": 1}}, timeout=1)
        self.partner.send_request_and_ck_resp(DRIVINGASSIST_SERVICE_CLIENT, "getHandOFFSts", {},
                                              {"out": {"onSts": 1, "errSts": 1}}, timeout=1)
