# -*- coding: utf-8 -*-
"""
@File        : test_service.py
@Author      : tao.cheng_ext@jiduatuo.com
@Time        : 2023/06/5 18:00 PM
@Description : Test SOA for ConditionCheckService
"""

import os
import sys
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
sys.path.append(os.path.join(os.getcwd(), "../../../.."))
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_cases.legacy.soa.case_helper.parse_excel import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.driver.ssh_interface import command_send

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path.split("sat")[0], "sat"))
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.common.logger import logger

@allure.feature("SOA服务性能稳定性")
@allure.story("S2S稳定性需求")
@pytest.mark.soa
class Testperfomance(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([ ("ConditionCheckService", "client"),
                                     ("VehicleModeService", "client"),
                                     ("VehicleSetStatusService", "client"),
                                     ("ChassisService", "client"),
                                     ("CarConfigService", "client"),
                                     ("HighVoltageService", "client")])
        self.sd_tester.tester_present()
        self.ipdu.send_pdu('chassiscan1', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('chassiscan2', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('propulsioncan', 0x516, [0x16, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        sleep(1)
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
                                             {"isOpen": False})
        self.partner.empty_all(1)

    def after_each_func(self, ecu):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.sd_tester.stop_tester_present()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def BGM_down_up(self,X,Y,Z):
        """X代表总线停后等待时间 Y代表下电后电等待时间 Z代表上电后电等待时间"""
        self.ipdu.pause_all_bus_send()
        sleep(X)
        self.nucapp.bgm_power_off()
        sleep(Y)
        self.nucapp.bgm_power_on()
        sleep(Z)

    def five_door_close(self):
        self.io.pass_door_close()
        self.io.drvr_door_close()
        self.io.lere_door_close()
        self.io.rire_door_close()
        self.io.trunk_door_close()

    @allure.title("压测_BGM重启设置维持上电模式")
    @pytest.mark.sanity
    @pytest.mark.repeat(1)
    def test_caseid_1984523(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        sleep(1)
        self.dk.set_cenlock_sts(1)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        sleep(6) #SOA-23216
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(1)

    @allure.title("压测拖车模式重启后能进入")
    @pytest.mark.full
    @pytest.mark.repeat(10)
    @pytest.mark.restart
    def test_caseid_1984498(self):
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd',  0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn',  0)
        self.sd_tester.change_usage_mode(11)
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_internal_has_key()
        sleep(2)
        self.partner.send_method_request(CONDITIONCHECK_SERVICE_CLIENT, "SetTowModeConfirm", {"isOn": True})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 9)
        sleep(1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "TowModeStatus", {"info": {"sts": 2}})
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "TowModeStatus", {"info": {"sts": 3}})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.restart_bgm_and_connect_service(CONDITIONCHECK_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT,
                                              "GetTowModeStatus", {},  {"out": {"sts": 3}},timeout=10)
        self.partner.send_method_request(CONDITIONCHECK_SERVICE_CLIENT, "SetTowModeConfirm", {"isOn": False})
        sleep(1)

    @allure.title("BGM重启后恢复总线_75度电池包压测充电速度显示正常")#140
    @pytest.mark.sanity
    @pytest.mark.restart
    def test_caseid_1984181(self):
       # 13.5kWh/100km
        self.sd_tester.write_multi_ccp({3: 129, 566: 23,950:1,962:0})
        sleep(3)
        self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetRange",
                                            {"infos": {"type": 0, "CLTCRange": 999, "estimatedRange": 999}})
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                                {"out": {"cltcEnergyComsumption":13.5}})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr13, 'HvBattChrgnPwrCns1', 100000.0)
        sleep(1)
        for i in range(1):
            logger.info(f"第{i}次压测")
            self.BGM_down_up(1,1,1)
            self.ipdu.resume_all_bus_send()
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr13, 'HvBattChrgnPwrCns1', 100000.0)
            sleep(1)
            self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "ChargingInfo", {"info": {"chargeSpeedCalculate": 740}},timeout=10)
            
    @allure.title("75度电池包压测_来回切换工况类型_充电速度显示正常")#140
    @pytest.mark.sanity
    def test_caseid_1984184(self):
       # 13.5kWh/100km
        self.sd_tester.write_multi_ccp({3: 129, 566: 23,950:1})
        sleep(3)
        self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetAveragePowerConsume", {"power": 50})
        for i in range(100):
            logger.info(f"第{i}次压测")
            sleep(1)
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetRange",
                                            {"infos": {"type": 0, "CLTCRange": 999, "estimatedRange": 999}})
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr13, 'HvBattChrgnPwrCns1', 0)
            self.partner.empty_all(0.5)
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                                {"out": {"cltcEnergyComsumption":13.5}})
            sleep(1)
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr13, 'HvBattChrgnPwrCns1', 10000.0)
            sleep(1)
            self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "ChargingInfo", {"info": {"chargeSpeedCalculate": 74}})
            self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {},
                                                {"out": {"chargeSpeedCalculate": 74}})
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetRange",#切换类型
                                            {"infos": {"type": 1, "CLTCRange": 999, "estimatedRange": 999}})
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr13, 'HvBattChrgnPwrCns1', 1000.0)
            sleep(1)
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr13, 'HvBattChrgnPwrCns1', 100000.0)
            sleep(1)
            self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "ChargingInfo", {"info": {"chargeSpeedCalculate": 200}})
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr13, 'HvBattChrgnPwrCns1', 0.0)
            sleep(1)
            self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "ChargingInfo", {"info": {"chargeSpeedCalculate": 0}})
