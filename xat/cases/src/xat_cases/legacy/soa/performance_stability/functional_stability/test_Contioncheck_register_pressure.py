import os
import sys
import random
import allure
import pytest
import copy
import uuid
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
sys.path.append(os.path.join(os.getcwd(), "../../../.."))

from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_cases.legacy.soa.case_helper.parse_excel import *
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_ecu.legacy.sdk.digital_key.RVCTSPMessage_pb2 import *
from xat_ecu.legacy.sdk.sdk_tools import check_pdu
from xat_ecu.legacy.common.data_type_handing import logger, DataTypeHanding
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.bgm.bgm_ssh import *

global TIMES
TIMES = 100

@allure.feature("性能稳定性")
@allure.story("业务稳定性/接口压测")
@pytest.mark.soa
class Test_Interface(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("ChassisService", "client"),
                                     ("ConditionCheckService", "client"),
                                     ("HighVoltageService", "client")])
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.io.set_four_door_close()
        sleep(1)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)
    
    def set_futionID35_true(self):
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 2)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 0)
        self.partner.empty_all(1)

    @allure.title("Condioncheck服务_SOAPP服务注册S2S服务压测100次")
    @pytest.mark.full
    @pytest.mark.repeat(TIMES)
    def test_caseid_1985866(self):
        self.set_futionID35_true()
        self.ipdu.pause_all_bus_send()
        logger.info(f"开始杀SOAAPP")
        self.kill_bgm_process('SOAApp')
        sleep(2)
        logger.info(f"开始杀S2S")
        self.kill_bgm_process()
        self.partner.wait_for_service_reconnect(CONDITIONCHECK_SERVICE_CLIENT)
        self.ipdu.resume_all_bus_send() #停掉恢复总线，防止信号发不处来
        self.partner.empty_all(5) #避免启动性能差
        self.set_futionID35_true()
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 1)
        sleep(1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                  {"infos": [{'functionId': 35, 'state': True,'failedKeys': ['']},
                                             {'functionId': 29, 'state': True,'failedKeys': ['']}]})
    
 