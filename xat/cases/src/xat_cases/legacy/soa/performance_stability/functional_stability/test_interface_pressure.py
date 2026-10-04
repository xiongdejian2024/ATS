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

TAILGATESERVICE_CLIENT = "TailGateService_client"
WTI_SERVICE_CLIENT = "WTIService_client"
WINDOWS_APP_SERVICE_CLIENT = "WindowAppService_client"
SEAT_SERVICE_CLIENT="SeatService_client"
DOOR_SERVICE_CLIENT="DoorService_client"
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
        self.partner = S2sBaseClass([
                                 ("TailGateService", "client"),
                                     ("SeatService", "client"),
                                     ("ChassisService", "client"),
                                     ("WTIService", "client"),
                                     ("WindowAppService", "client"),
                                     ("EntryService", "client"),
                                     ("DoorService","client"),
                                     ("PedalService","client"),
                                     ("HighVoltageService", "client"),
                                     ("CentralLockService", "client"),
                                     ("InnerRearViewService", "client"),
                                     ("KeyService", "client"),
                                ])

        time.sleep(5)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set_vehspd(0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.io.set_four_door_close()
        sleep(1)
        try:
            self.sd_tester.change_car_mode(0)
            self.sd_tester.change_usage_mode(1)
        except Exception as e:
            logger.error(e)
        sleep(1)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        try:
            self.sd_tester.change_car_mode(0)
            self.sd_tester.change_usage_mode(1)
        except Exception as e:
            logger.error(e)
        super().after_each_func(ecu, start=False)

    @allure.title("str后获取电动门开启模式_压测一百次")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1748251?projectId=46')
    @pytest.mark.full
    def test_caseid_1913719(self):
        for x in range(TIMES):        
            logger.info(f"第{x+1}次")
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetDoorMode", {"doors": [{"id": 4, "mode": 0}]})
            sleep(5)
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetDoorMode", {"doors": [{"id": 4, "mode": 1}]})
            time.sleep(0.5)
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetDrvrPwrDoorAutOperMode', 1)
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetPassPwrDoorAutOperMode', 1)
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetLeRePwrDoorAutOperMode', 1)
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetRiRePwrDoorAutOperMode', 1)
            time.sleep(1)
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetDoorMode",{"doors":[4]},
                                                {"out":[{"id":0,"mode":1},{"id":1,"mode":1},{"id":2,"mode":1},{"id":3,"mode":1}]})
    
    
    def set_drvr_frontheiperc(self, perc):
        """设置主驾腿托位置"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiPerc', perc)

    def set_drvr_sldperc(self, perc):
        """设置主驾前后位置"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc', perc)

    def set_drvr_angelperc(self, perc):
        """设置主驾靠背角度"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'SeatBackAngleRowFirstDrvr_0_SmdBodySignalIPdu01', perc)

    def set_drvr_heiperc(self, perc):
        """设置主驾高度位置"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc', perc)

    def set_drvr_heipercValid(self, QF):
        """设置主驾高度位置有效性"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', QF)

    def set_drvr_frontheipercValid(self, QF):
        """设置主驾腿托位置有效性"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', QF)

    def set_drvr_sldpercValid(self, QF):
        """设置主驾前后位置有效性"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', QF)

    def set_pass_frontheiperc(self, perc):
        """设置副驾腿托位置"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiPerc_0_SmpBodySignalIPdu02', perc)

    def set_pass_sldperc(self, perc):
        """设置副驾前后位置"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldPerc_0_SmpBodySignalIPdu02', perc)

    def set_pass_sldpercValid(self, QF):
        """设置副驾前后位置有效性"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF_0_SmpBodySignalIPdu02', QF)

    def set_pass_angelperc(self, perc):
        """设置副驾靠背角度"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'SeatBackAngleRowFirstPass_0_SmpBodySignalIPdu02', perc)

    def set_pass_heiperc(self, perc):
        """设置副驾高度位置"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc_0_SmpBodySignalIPdu02', perc)

    def set_pass_heipercValid(self, QF):
        """设置副驾高度位置有效性"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF_0_SmpBodySignalIPdu02', QF)

    def set_pass_frontheipercValid(self, QF):
        """设置副驾腿托位置有效性"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiQF_0_SmpBodySignalIPdu02', QF)
        
    def five_door_close(self):
        self.io.pass_door_close()
        self.io.drvr_door_close()
        self.io.lere_door_close()
        self.io.rire_door_close()
        self.io.trunk_door_close()

    @allure.title("高压服务800V_CCP来的晚_信号来的早_压测500次")
    @pytest.mark.full
    @pytest.mark.repeat(500)
    def test_caseid_1989191(self):
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr06, 'IemGenericEMQnty', 2)
        self.sd_tester.write_multi_ccp({3: 129, 4: 6,950:1,962:2}) #4:6代表双电机，962：2代表800V
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HvBattPwrLimDcha1',20.0)
        #
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr31, 'HvBattPwrLimDcha800',10.0) #800V放电
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr13, 'HvBattChrgnPwrCns1', 200.0)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr12, 'HvBattChrgnPwrCns800', 100.0) #800V充电功率

        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr06, 'IsgTqActIsgTqAct', -1000.0)
        self.ipdu.set(self.ipdu.propulsioncan.MgmPropFr06, 'IsgSpdActSgnSafeIsgSpdWSgnTyp', 2000)
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr12, 'WhlMotSysSpdActSafeIsgSpdWSgnTyp', 2000)
        self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr01, 'WhlMotSysTqEstIsgTqAct', -1000.0)
        self.ipdu.set(self.ipdu.propulsioncan.MgmPropFr06, 'IsgSpdActSgnSafe800IsgSpdActSgn800', 10000) #800V转速
        self.ipdu.set(self.ipdu.chassiscan1.IemChas1Fr02, 'WhlMotSysSpdActSafe800IsgSpdActSgn800', 10000)#800V转速

        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr06, 'IsgSpdActSgn', 2000.0)#电机转速
        self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr02, 'WhlMotSysSpdAct',2000.0)
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysSpdAct800', 1000.0)#电机信息里的转速
        self.ipdu.set(self.ipdu.propulsioncan.MgmPropFr05, 'IsgSpdActSgn800', 1000.0) #电机信息里的转速

        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc', 100.0)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc800', 0.0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr25, 'PlsHeatgTarT',40.0)
        sleep(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr22, 'ChrgEquipIDc',0.0) #避免电流先上，电压后来，所以前置都归0
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr05, 'IsgUDc', 100.0)
        self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr02, 'WhlMotSysUdc',100.0)
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr05, 'IsgUDc800', 400.0) #800V
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08,'WhlMotSysUDc800',400.0)#800V
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'PlsHeatgSts',1)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr27, 'ResvFb1',2)
        self.partner.empty_all(3)
        self.restart_bgm_and_connect_service(HIGHVOLTAGE_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(0.5) 
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc800', 400.0)
        sleep(1) #避免电压后来，导致没有上报充电桩信息
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr22, 'ChrgEquipIDc',10.0)
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "ChargingInfo",{"info": {"chargePower": 100.0}},timeout=5)
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "MotorPower",
                                  {'motorsPower': [{'motorId': 0, 'power': -88}, {'motorId': 1, 'power': -88}]})
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "NotifyChargingEquipmentInformation",
                                {"info": {"chargePowerInput": 4000,"actualCurrent":10.0}})
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "MotorInfo",
                                    {"motorsInfo": [{"motorId": 0,"rotationalSpeed": 1000.0,"inputVoltage": 400},
                                                    {"motorId": 1,"rotationalSpeed": 1000.0,"inputVoltage": 400}]})
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "HVBatteryVoltage", {"value": 400})
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "LimitedDischargePower", {"power": 10})
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT,"EnergyRecoveryInfo",{"info":{"value":10}})
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "PulseHeatingInfo", {"sts":{"pulseHeatingSts": 1,"pulseHeatingTargetTemperature": 40.0}})

    @allure.title("高压服务400V_CCP来的晚_信号来的早_压测500次")
    @pytest.mark.full
    @pytest.mark.repeat(500)
    def test_caseid_1989186(self):
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr06, 'IemGenericEMQnty', 2)
        self.sd_tester.write_multi_ccp({3: 129, 4: 6,950:1,962:0}) #4:6代表双电机，962：2代表800V
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HvBattPwrLimDcha1',10.0)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr13, 'HvBattChrgnPwrCns1', 100.0)

        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr06, 'IsgTqActIsgTqAct', -1000.0)
        self.ipdu.set(self.ipdu.propulsioncan.MgmPropFr06, 'IsgSpdActSgnSafeIsgSpdWSgnTyp', 10000)
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr12, 'WhlMotSysSpdActSafeIsgSpdWSgnTyp', 10000)
        self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr01, 'WhlMotSysTqEstIsgTqAct', -1000.0)

        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr06, 'IsgSpdActSgn', 1000.0)#电机转速
        self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr02, 'WhlMotSysSpdAct',1000.0)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc', 0.0) #设置为0 避免重启后电压先到影响校验event
        sleep(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr22, 'ChrgEquipIDc',0.0)
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr05, 'IsgUDc', 400.0)
        self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr02, 'WhlMotSysUdc',400.0)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr27, 'ResvFb1',2)
        self.partner.empty_all(3)
        self.restart_bgm_and_connect_service(HIGHVOLTAGE_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(0.5) 
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc', 400.0)
        sleep(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr22, 'ChrgEquipIDc',10.0)
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "ChargingInfo",{"info": {"chargePower": 100.0}},timeout=5)
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "MotorPower",
                                  {'motorsPower': [{'motorId': 0, 'power': -88}, {'motorId': 1, 'power': -88}]})
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "NotifyChargingEquipmentInformation",
                                {"info": {"chargePowerInput": 4000,"actualCurrent":10.0}})
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "MotorInfo",
                                    {"motorsInfo": [{"motorId": 0,"rotationalSpeed": 1000.0,"inputVoltage": 400},
                                                    {"motorId": 1,"rotationalSpeed": 1000.0,"inputVoltage": 400}]})
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "HVBatteryVoltage", {"value": 400})
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "LimitedDischargePower", {"power": 10})

    @allure.title("高压服务交流CCP_信号来的早_CCP来的晚")
    @pytest.mark.full
    @pytest.mark.repeat(500)
    def test_caseid_1989233(self):
        self.sd_tester.write_single_ccp(973,2) #交直流都支持
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 3)   
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0) #直流枪
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.5)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr03, 'OnBdChrgrUAct', 10.0)
        sleep(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr02, 'OnBdChrgrIAct', 20.0)
        sleep(3)
        self.restart_bgm_and_connect_service(HIGHVOLTAGE_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 3)   
        sleep(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.5)
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "ChargingInfo",{"info": {"isConnect":True,"acdcType":2}},timeout=5)    
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT,"DischargingInfo",{"info":{"isConnect":False,"acdcType":0}})
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "HVSOCInfo", {"info":{"displaySoc":11}})
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "NotifyChargingEquipmentInformation",
                                {"info": {"chargePowerInput": 200,"actualCurrent": 20,'chargeVoltageInput':10}})
        self.partner.empty_all()

    @allure.title("压测CCP无法写入100次")
    @pytest.mark.full
    def test_caseid_1988050(self):
        for times in range(TIMES):
            logger.info(f"第{times}压测")
            self.sd_tester.write_multi_ccp({3: 128, 4: 6,950:2,566:16})
            self.partner.empty_all(2)
            self.sd_tester.enter_default_session()
            sleep(0.1)
            self.sd_tester.write_multi_ccp({3: 129, 566: 16, 950:1, 966:0})
            sleep(3)
            result1 = self.sd_tester.return_udsdata_and_check_and_print_response_result("写入ccp")
            if result1[0] == False:
                sleep(100000)
            else:
                check1 = self.sd_tester.read_ccp()
                logger.info(f"----打印{check1}---")
                sleep(1)
                self.restart_bgm_and_connect_service(HIGHVOLTAGE_SERVICE_CLIENT)
                sleep(5)
                check2 = self.sd_tester.read_ccp()
                logger.info(f"----打印{check2}---")
                #  找出第几位不同
                check1="111"
                check2="111"
                if check1==check2:
                    pass
                else:
                    min_len = min(len(check1), len(check2))
                    diff_index = -1
                    for i in range(min_len):
                        if check1[i]!= check2[i]:
                            diff_index = i
                            break
                    if diff_index == -1 and len(check1)!= len(check2):
                        diff_index = min_len
                    if diff_index!= -1:
                        print(f"在第 {diff_index + 1} 位开始不同，num1的字符为 {check1[diff_index]}, num2的字符为 {check2[diff_index]}")

    @allure.title("压测雨天自动关窗")
    @pytest.mark.full
    def test_caseid_1984546(self):
        self.sd_tester.write_single_ccp(177,1)
        sleep(3)
        for i in range(2):
            logger.info(f"第{i}次压测")
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
            sleep(1)
            cenlock = self.ipdu.get_recent_signal_raw_value(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt')
            if cenlock  == 1:
                self.dk.send_nfc_cmd() #解决刷两次卡，导致不能设防
            self.restart_bgm_and_connect_service(WINDOWS_APP_SERVICE_CLIENT)
            self.ipdu.lin1_wakeup()
            sleep(1)
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'RainDetected', 0)
            sleep(1)
            logger.info(f"=============开始发信号==========")
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'RainDetected', 1)
            sleep(0.1)
            self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1),
                                            (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1),
                                            (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1),
                                            (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 1)])
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'RainDetected', 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
            sleep(1)

    @allure.title("BGM重启后首次远控车窗，尾门，座椅加热通风")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1684857?projectId=46')
    @pytest.mark.full
    def test_caseid_1919282(self):
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr_0_DdmBodySignalIPdu04', 26)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass_0_PdmBodySignalIPdu01', 19)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe_0_RldmBodySignalIPdu01', 19)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi_0_RrdmBodySignalIPdu01', 26)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts_0_PotBodySignalIPdu02', 1)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr03, 'TrOpenPosn', 0)
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetAutoVenting', {"params": [{"id": 1, "isOn": False}]})
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                         {"params": [{"id": 1, "uint8Info": 3}]})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'TelmSeatPassHeatClimaLvl', 3)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "SetPosition", {"pos": 100})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr131, 'TrOpenPosnReqFromHmi', 100)
        self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition",
                                         {"windows": [{"id": 4, "position": 0}]})
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass_0_PdmBodySignalIPdu01', 20)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe_0_RldmBodySignalIPdu01', 20)
        sleep(0.2)
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1),
                                          (self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1),
                                         (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 1),
                                         (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1)])

    @allure.title("JBS-19996尾门已锁，挂D档，弹窗提醒尾门未锁")
    @pytest.mark.full
    def test_caseid_1898488(self):
        for X in range(TIMES):
            logger.info(f"第{X}次压测")
            self.sd_tester.change_usage_mode(11)
            self.io.set_four_door_close()
            self.io.trunk_door_close()
            sleep(1)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 3)
            sleep(1)
            try:
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "WarningMsgList", {},
                                                      {"list": [{"name": "Tail", "info": "1"}]})
            except Exception:
                pass
            else:
                assert False
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
            self.io.trunk_door_open()
            sleep(1)

    @allure.title("JBS-20204主驾占座，大屏无安全带未系指示灯")
    @pytest.mark.full
    def test_caseid_1898351(self):
        for X in range(TIMES):
            logger.info(f"第{X}次压测")
            self.sd_tester.change_usage_mode(2)
            self.io.driver_seat_notpresent()
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts', 0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe', 0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid', 0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi', 0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', 0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                          'BltLockStAtRowSecLeBltLockSts', 0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                          'BltLockStAtRowSecMidBltLockSts', 0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                          'BltLockStAtRowSecRiBltLockSts', 0)
            self.partner.empty_all(1)
            self.io.driver_seat_present()
            A = self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList", {})["list"][0]['sequenceTime'][
                'timestamp']

            B = self.partner.send_request_and_return_resp(WTI_SERVICE_CLIENT,"GetTelltaleList", {})[
                "out"]
            B2 = ""
            for obj in B:
                name = obj["name"]
                if name == "Seat Belt":
                    B2 = obj["sequenceTime"]["timestamp"]
                    break
            else:
                logger.info("not found")
            if A < B2:
                assert True
            else:
                assert False

    # @allure.title("JBS-20100唤醒情况下发关窗指令，指令下发失败，车窗先上升后下降")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1750986?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1892960(self):
    #     for X in range(TIMES):
    #         logger.info(f"第{X}次压测")
    #         self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr_0_DdmBodySignalIPdu04', 26)
    #         self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass_0_PdmBodySignalIPdu01', 19)
    #         self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe_0_RldmBodySignalIPdu01', 19)
    #         self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi_0_RrdmBodySignalIPdu01', 26)
    #         sleep(1)
    #         self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetSpecificWindowPosition",
    #                                          {"windows": [{"id": 4, "position": 0}]})
    #         self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 20)
    #         self.ipdu.check(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 20)
    #         sleep(1)
    #         self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass_0_PdmBodySignalIPdu01', 20)
    #         self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe_0_RldmBodySignalIPdu01', 20)
    #         self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 1),
    #                                           (self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 1),
    #                                           (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 1),
    #                                           (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 1)])
    #         sleep(1)
    # 重复
    # @allure.title("主驾占座，大屏无安全带未系指示灯")
    # @pytest.mark.full
    # def test_caseid_1892956(self):
    #     for X in range(100):
    #         logger.info(f"第{X}次压测")
    #         self.sd_tester.change_usage_mode(2)
    #         self.io.driver_seat_present()
    #         self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts', 0)
    #         self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe', 0)
    #         self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid', 0)
    #         self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi', 0)
    #         self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
    #         self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', 0)
    #         self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04',
    #                       0)
    #         self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04',
    #                       0)
    #         self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
    #                       'BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04', 0)
    #         self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
    #                       'BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04', 0)
    #         self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
    #                       'BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04', 0)
    #         self.partner.empty_all(1)
    #         self.io.driver_seat_notpresent()
    #         self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList", {"list": [{"name": "Seat Belt", "state": "0"}]})
    #         self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
    #                                               {"out": [{"name": "Seat Belt", "state": "0"}]})
    #         SeatId = ['PassSeatSts', 'SeatOccptAtRowSecLe', 'SeatOccptAtRowSecMid', 'SeatOccptAtRowSecRi']
    #         def State(value1):
    #             return "1" if value1 == 1 else "0"
    #         for seat in SeatId:
    #             for value1 in [1, 0]:
    #                 state1 = State(value1)
    #                 self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, seat, value1)
    #                 sleep(1)
    #                 logger.info(f"---send{seat}---{value1}")
    #                 self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
    #                                           {"list": [{"name": "Seat Belt", "state": state1}]})
    #                 self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
    #                                                       {"out": [{"name": "Seat Belt", "state": state1}]})

    @allure.title("安全带时间戳压测")
    @pytest.mark.full
    def test_caseid_1912729(self):
        for X in range(TIMES):
            logger.info(f"第{X}次压测")
            self.io.driver_seat_present()
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', 0)
            self.partner.empty_all(1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', 1)
            sleep(1)
            A = self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts", {})["status"]["sequenceTime"][
                'timestamp']
            logger.info(f"----{A}")
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', 0)
            sleep(1)
            B = self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts", {})["status"]["sequenceTime"][
                "timestamp"]
            if int(B) - int(A) > 0:
                assert True
            else:
                assert False

    @allure.title("座椅、高压、windowapp服务设置项下电重启记忆压测10次")
    @pytest.mark.full
    def test_caseid_1903604(self):
        for X in range(10):
            #setting
            logger.info(f"第{X}次压测")
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetAutoHeating",
                                             {"params": [{"id": 0, "isOn": True}, {"id": 1, "isOn": True},
                                                         {"id": 4, "isOn": True}, {"id": 6, "isOn": True}]})

            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetAutoVenting",
                                             {"params": [{"id": 0, "isOn": True}, {"id": 1, "isOn": True},
                                                         {"id": 4, "isOn": True}, {"id": 6, "isOn": True}]})

            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetMassageConf",
                                             {"params": [{"id": 0, "conf": {"isOn": True, "type": 4, "intensity": 2}}]})
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetMassageConf",
                                             {"params": [{"id": 1, "conf": {"isOn": True, "type": 4, "intensity": 2}}]})
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetRange",
                                             {"infos": {"type": 1, "CLTCRange": 999, "estimatedRange": 999}})
            self.partner.send_method_request(WINDOWS_APP_SERVICE_CLIENT, "SetRainAutoCloseWindow", {"isOn": True})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetDoorMode", 
                                              {"doors": [{"id":0, "mode": 1}]})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT,"SetAutoCloseTrigger",{"trigger":0})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT,'SetStrengthLevel',{"doors": [{"id": 4, "level": 2}]})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT,'SetOpenSpeed',{"doors":[{"id":4,"level":2}]})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT,'SetCloseSpeed',{"doors":[{"id":4,"level":2}]})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT,'SetWindElimination',{"doors":[{"id":4,"on":True}]})
            sleep(1)
            #set and get
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetMassageConf", {"seats": [3]},
                                                  {"out": [
                                                      {"id": 0, "conf": {"isOn": False, "type": 4, "intensity": 2}},
                                                      {"id": 1, "conf": {"isOn": False, "type": 4, "intensity": 2}}]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetAutoHeating", {"seats": [12]},
                                                  {"out": [{"id": 0, "isOn": True}, {"id": 1, "isOn": True},
                                                           {"id": 4, "isOn": True}, {"id": 6, "isOn": True}]})

            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetAutoVenting", {"seats": [12]},
                                                  {"out": [{"id": 0, "isOn": True}, {"id": 1, "isOn": True},
                                                           {"id": 4, "isOn": True}, {"id": 6, "isOn": True}]})
            self.partner.send_request_and_ck_resp(WINDOWS_APP_SERVICE_CLIENT, "GetRainAutoCloseWindowStatus", {},
                                                  {"out": True})

            self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetRange", {},
                                                  {"out": {"type": 1,  "estimatedRange": 999}})
    
            # self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetDrvrPwrDoorAutOperMode', 1)
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetDoorMode",{"doors":0},{"out":[{"id":0,"mode":1}]})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetAutoCloseTrigger",{},{"out":[0]})
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetPwrDoorWindCatch', 1)
            
            self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
            # get
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetMassageConf", {"seats": [3]},
                                                  {"out": [{"id": 0, "conf": {"isOn": False, "type": 4, "intensity": 2}},
                                                           {"id": 1, "conf": {"isOn": False, "type": 4, "intensity": 2}}]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetAutoHeating", {"seats": [12]},
                                                  {"out": [{"id": 0, "isOn": True}, {"id": 1, "isOn": True},
                                                         {"id": 4, "isOn": True}, {"id": 6, "isOn": True}]})

            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetAutoVenting", {"seats": [12]},
                                                  {"out": [{"id": 0, "isOn": True}, {"id": 1, "isOn": True},
                                                           {"id": 4, "isOn": True}, {"id": 6, "isOn": True}]})                                        
            self.partner.send_request_and_ck_resp(WINDOWS_APP_SERVICE_CLIENT, "GetRainAutoCloseWindowStatus", {},{"out": True})
            self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetRange", {},
                                                  {"out": {"type": 1}})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetDoorMode",{"doors":0},{"out":[{"id":0,"mode":1}]})
            # self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetDrvrPwrDoorAutOperMode', 1)
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetAutoCloseTrigger",{},{"out":[0]})
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetPwrDoorWindCatch', 0)
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetWindElimination", {"doors": [4]},
                                                                                             {"out": [{"id": 4, "on": True}]})
            sleep(1)
            #recover
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetAutoHeating",
                                             {"params": [{"id": 0, "isOn": False}, {"id": 1, "isOn": False},
                                                         {"id": 4, "isOn": False}, {"id": 6, "isOn": False}]})
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetAutoVenting",
                                             {"params": [{"id": 0, "isOn": False}, {"id": 1, "isOn": False},
                                                         {"id": 4, "isOn": False}, {"id": 6, "isOn": False}]})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetDoorMode", 
                                               {"doors": [{"id": 4, "mode": 0}]})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, "CancelAutoCloseTrigger", {"trigger": 0})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT,"SetStrengthLevel",{"doors":[{"id":4,"level":0}]})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT,'SetOpenSpeed',{"doors":[{"id":4,"level":0}]})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT,'GetCloseSpeed',{"doors":[{"id":4,"level":0}]}) 
            self.partner.send_method_request(DOOR_SERVICE_CLIENT,'SetWindElimination',{"doors":[{"id":4,"on":False}]})

            sleep(1)

    @allure.title("v1.1_s2s_座椅调节状态机中存在死锁问题，导致s2s运行异常")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1791927?projectId=46')
    @pytest.mark.full
    def test_caseid_1959943(self):
        for i in range(TIMES):
            self.sd_tester.change_car_mode(0)
            self.sd_tester.change_usage_mode(2)
            sleep(1)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',{"params": [{"id": 0, "uint8Info": 2}]})
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 2)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 0)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd_0_SmdBodySignalIPdu05', 1)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
            self.set_drvr_sldperc(20.0)
            self.set_drvr_sldpercValid(3)
            self.set_drvr_angelperc(20.0)
            self.set_drvr_heiperc(20.0)
            self.set_drvr_frontheiperc(20.0)
            sleep(1)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                {"params": {"id": 0,
                                                            "position": {"backAngle": 20, "longitudinalPosition": 100,
                                                                        "verticalPosition": 20,
                                                                        "LegrestVerticalPosition": 20,
                                                                        "backAngleIsValid": True,
                                                                        "longitudinalIsValid": True,
                                                                        "verticalIsValid": True,
                                                                        "legrestVerticalIsValid": True}}},
                                                {"out": 1})
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr', 1)
            self.set_drvr_sldperc(100.0)
            sleep(1)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr', 0)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',{"params": [{"id": 0, "uint8Info": 1}]})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 1)
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingTime",
                                             {"params": [{"id": 0, "uint64Info": 20},{"id": 1, "uint64Info": 20},
                                                         {"id": 4, "uint64Info": 20},{"id": 6, "uint64Info": 20}]})
        sleep(1)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetHeatingTime", {"seats": [12]},
                                            {"out": [{"id": 0, "uint64Info": 20},{"id": 1, "uint64Info": 20},
                                                    {"id": 4, "uint64Info": 20},{"id": 6, "uint64Info": 20}]})
            
        
    # @allure.title("蓝牙解闭锁_压测100次")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683137?projectId=46')
    # @pytest.mark.full   
    # def test_caseid_1913718(self):
    #     self.io.trunk_door_close()
    #     self.io.pass_door_close()
    #     self.io.lere_door_close()
    #     self.io.rire_door_close()
    #     self.io.drvr_door_close()
    #     sleep(1)
    #     self.dk.set_door_opener_sts(1, 1, 1, 1, 1)   
    #     for i in range(TIMES):
    #         logger.info(f"第{i+1}次")
    #         self.io.trunk_door_close()
    #         self.io.pass_door_close()
    #         self.io.lere_door_close()
    #         self.io.rire_door_close()
    #         self.io.drvr_door_close()
    #         sleep(1)
    #         self.dk.send_rke_lock()
    #         self.dk.ck_cenlock_sts(3)
    #         sleep(3)
    #         i += 1

#================================================================================

# @allure.feature("性能稳定性")
# @allure.story("业务稳定性/接口压测")
# @pytest.mark.soa
# class TestClimateControlService(TestBase):
#     def before_class(self, ecu):
#         super().before_class(self, ecu)
#         service_name_type = [("ClimateControlService", "client"),("VehicleModeService","client")]
#         # 为了防止诊断反馈NRC22,需要发送FlexRay报文
#         self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#         # 检查上位机上是否有其它未关闭的soa_partner进程在运行，如果有，则杀死进程
#         partner_process_check()
#         self.bgm_ssh=BGM_SSH()
#         # 启动partner operator
#         self.partner = S2sBaseClass(service_name_type)

#     def before_each_func(self, ecu):
#         super().before_each_func(ecu)
#         self.partner.empty_all()

#     def after_each_func(self, ecu):
#         self.ipdu.reset_check_results()
#         super().after_each_func(ecu)

#     def after_class(self, ecu):    
#         self.partner.stop_operators()
#         super().after_class(self, ecu)

#     @pytest.mark.full
#     @allure.title("展车模式下BGM休眠唤醒后空调服务成功接收展车模式开启通知")
#     def test_climate_caseid_1919279(self):
#         for i in range(TIMES):
#             logger.info(f"第{i}次压测")   
#             logger.info("展车模式后climateservice初始化落后于展车模式通知https://jira.jiduauto.com/browse/JBS-19916")
#             self.sd_tester.write_single_ccp(502, 2)
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
#             self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
#                                             {"isOpen": True})
#             self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr01,
#                             'ExhibitionModeStsExhibitionModeSts', 1) 
#             try:
#                 self.sd_tester.send_data([0x11, 0x81])
#                 time.sleep(0.5)
#             except Exception as e:
#                 logger.warning(f"重启失败==》》{str(e)}")
#             logger.info("休眠唤醒后，查看空调初始化")
#             self.partner.wait_for_service_reconnect("ClimateControlService_client")
#             #由于partner重连是起线程，所以等待20s
#             time.sleep(20)
#             logger.info("校验climateservice客户端服务上线是否早于展车模式的通知")
#             logger.info(f"设置接口_SetClimateAuto_所有区域_打开")
#             self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetClimateAuto",{"zoneId": 0, "on": True})
#             self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT,"GetClimateAuto",{'zoneId':0},{'out':{'zoneId':0,'isOn':True}})
#             check_value =[[True,{"acStatus":True}],{"acStatus":True},1]
#             get_check,notify_check,signal_check = check_value
#             logger.info(f"校验信号HmiCmptmtCoolgReq_0_CEMBodySignalIPdu15_是否为{signal_check}")
#             self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15,"HmiCmptmtCoolgReq",signal_check,timeout=3)
#             logger.info(f"获取接口_GetAC_开关状态_是否为{get_check[0]}")
#             self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT,"GetAC",args={},ck_info={"out":get_check[0]})
#             logger.info(f"获取接口_GetClimateSystemStatus_acStatus_是否为{get_check[1]}")
#             self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT,'GetClimateSystemStatus',args={},ck_info={"out":get_check[1]})
#             logger.info(f"通知接口_ClimateSystemStatus_acStatus_是否为{notify_check}")
#             self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT,'ClimateSystemStatus',ck_info={"status":notify_check})   
#             logger.info("关闭展车模式，防止影响其他case")
#             sleep(0.5)
#             self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
#                                             {"isOpen": False})
#             self.partner.send_event_notify(VEHICLEMODESERVICE_CLIENT, "NotifyExhibitionModeSts",
#                                         {"sts": {"isOpen": False, "isValid": False}})
            
@allure.feature("SOA服务性能稳定性")
@allure.story("S2S稳定性需求")
class TestCentralLockService(TestBase):

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("CentralLockService", "client")])

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')        
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set_vehspd(0)
        self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4})
        self.partner.empty_all(1)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    @allure.title("启动下行接口调用_服务启动需在与MCU建tcp立连接之后")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1903443(self):
        test_times = 2
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.set_nopeople_incar()
        for number in range(test_times):
            self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 0})
            sleep(1)
            self.dk.ck_cenlock_sts(1)
            self.ipdu.pause_all_bus_send()
            self.sd_tester.send_data([0x11, 0x01])
            self.partner.empty_all(2)
            logger.info(f"BGM诊断重启第{number}次")
            self.ipdu.resume_all_bus_send()
            self.partner.wait_for_service_reconnect(CENTRALLOCK_SERVICE_CLIENT)
            self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 0})
            sleep(1)
            self.dk.ck_cenlock_sts(3)
