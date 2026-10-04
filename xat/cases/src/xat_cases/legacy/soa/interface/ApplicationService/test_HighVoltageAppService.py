"""
@File         :test_HighVoltageAppService.py
@Time         :2024/8/2 19:07:31
@Author       :tao.cheng_ext@jiduauto.com
@Description  :Test SOA for HighVoltageAppService
"""

import random
import os
import sys
import pytest
import allure
import datetime
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.driver.ssh_interface import command_send
from xat_ecu.legacy.sdk.sdk_tools import *

def current_time_with_seconds_zero_to_timestamp():
    ''' 获取当前时间时间戳并将秒数置0以便拿到整时整分0秒'''
    now = datetime.datetime.now()
    now_zero_seconds = now.replace(second=0, microsecond=0)
    timestamp = int(now_zero_seconds.timestamp())
    return timestamp

def DisplayStartTime(nowtime1,offset):
    ''' 将获取到的时间戳中的年月日时分 分别提取出来，以便赋值给某个参数''' 
    otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(nowtime1+offset))
    starttime = [int(item) for item in otherStyleTime.split("_")]
    return starttime

def todaymorning8():
    ''' 获取当天早上的8点''' 
    now = datetime.datetime.now()
    todaymorning=now.replace(hour=8, minute=0, second=0, microsecond=0)
    todaymorning8oclock = int(todaymorning.timestamp())
    return todaymorning8oclock

todaymorning8=todaymorning8()

def DisplayEndTime(nowtime1,offset):
    ''' 将获取到的时间戳中的年月日时分 分别提取出来，以便赋值给某个参数''' 
    otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(nowtime1+offset))
    EndTime = [int(item) for item in otherStyleTime.split("_")]
    return EndTime

@allure.feature("SOA服务接口")
@allure.story("BGM应用/HighVoltageAppService")
class TestHighVoltageAppService400V_2motor(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([
            ("HighVoltageAppService", "client"),
            ("VehicleTimeService", "client"),
            ("HighVoltageService", "client"),
            ("SentryModeService", "server"),
            ("ChassisService", "client")])
        self.partner.method_default_timeout = 3
        self.sd_tester.tester_present()
        self.ipdu.send_pdu('chassiscan1', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('chassiscan2', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('propulsioncan', 0x516, [0x16, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0)  
        self.sd_tester.write_multi_ccp({3: 129, 4: 6,950:1,962:0,973:2}) #400V双电机且支持交直流
        sleep(3)
        self.nucapp.bgm_power_off()
        self.nucapp.bgm_power_on()
        self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        sleep(15)#补电进程过慢，需要等待

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)#放电结束
        sleep(0.1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(0.1)      
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr30, 'TotDchaEgy', 0.0)
        self.sd_tester.change_usage_mode(1)
        sleep(1) #以下为驻车能耗通用信号
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 0)#高压输出能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 0.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 0.0)#座舱消耗能量
        self.partner.empty_all(1) #以下为400V双电机电流电压
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'EngSt1WdStsEngSt1WdSts', 0)#发动机状态
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr05, 'IsgUDc', 400.0)
        self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr02, 'WhlMotSysUdc',400.0)
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr03, 'IsgIDc', 0.0)
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysIdc',0.0)
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr05, 'IsgUDc800', 400.0)
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08,'WhlMotSysUDc800',400.0)
        self.partner.empty_all(3) 
        self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":0,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
        #以下2.2适配
        # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
        #                                {"sentryModeSts":[{"mainSts":0,"workSts":0,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})

    def after_each_func(self, ecu):
        self.ipdu.reset_check_results()
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.dk.stop_listen_dk_bgm_response()
        self.sd_tester.stop_tester_present()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def Shift_Gear(self, X):
        """0代表P挡 2代表N挡 3代表D挡 1代表R挡"""
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', X)
        sleep(1)

    def Base_shaobing_inCreas_200wh(self):
        '''基础设置哨兵模式阶段的消耗量  防止case一开始参数就是0'''
        sleep(1)
        # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
        #                            {"sentryModeSts":[{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
        self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
        sleep(1) 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 10.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 100.0)#高压输出能量    
        sleep(1) 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 20.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 200.0)#高压输出能量  
        sleep(1) 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 30.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 230.0)#高压输出能量  
        sleep(3)    
        # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
        #                            {"sentryModeSts":[{"mainSts":0,"workSts":0,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
        self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":0,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})

    @allure.title("通知驻车能量消耗信息_出厂默认值")
    @pytest.mark.full
    def test_caseid_1989083(self): 
        self.del_SOAAPP_db()
        sleep(1)
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT, resume_all_bus=False)
        sleep(1)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {}, 
                                              {"out":{"totalParkingEnergy":0,"parkingCounter":0,"parkingThermalEnergy":0,
                                                      "parkingCabinEnergy":0,"sentryModeEnergy":0,"sentryModeCounter":0,
                                                      "disChargingEnergy":0,"disChargingCounter":0}})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                              {"info":{"totalParkingEnergy":0,"parkingCounter":0,"parkingThermalEnergy":0,
                                                      "parkingCabinEnergy":0,"sentryModeEnergy":0,"sentryModeCounter":0,
                                                      "disChargingEnergy":0,"disChargingCounter":0}})
        
    @allure.title("通知驻车能量消耗信息_上电P档或者NA档到P档时_parkingCounter不加1")
    @pytest.mark.full
    def test_caseid_1989084(self): 
        parkingCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCounter']
        logger.info("parkingCounter是:{}".format(parkingCounter))
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "Gear", {"gear": 0}, timeout=5)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                              {"info":{"parkingCounter":parkingCounter}}, timeout=5)
        sleep(1)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {}, 
                                              {"out":{"parkingCounter":parkingCounter}})
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 7)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
        self.partner.empty_all(1) #档位N档
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "Gear", {"gear": 5}, timeout=2)
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "Gear", {"gear": 0}, timeout=2)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo",{},{"out":{"parkingCounter":parkingCounter}})

    @allure.title("通知驻车能量消耗信息_充电到非充电时_parkingCounter不加1")
    @pytest.mark.full
    def test_caseid_1989094(self): 
        parkingCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCounter']
        logger.info("parkingCounter是:{}".format(parkingCounter))
        sleep(1)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {}, 
                                              {"out":{"parkingCounter":parkingCounter}})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)#交流充电开始  
        self.partner.ck_no_event_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",{"out":{"parkingCounter":parkingCounter}},timeout=3)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 3)#交流充电结束
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)#交流充电结束
        self.partner.ck_no_event_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",{"out":{"parkingCounter":parkingCounter}},timeout=3)


    @allure.title("通知驻车能量消耗信息_上电P档时totalParkingEnergy通过totalEnergy之outputEnergy和recoveryEnergy触发更新的逻辑")
    @pytest.mark.full
    def test_caseid_1989086(self): 
        totalParkingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['totalParkingEnergy']
        logger.info("totalParkingEnergy:{}".format(totalParkingEnergy))
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "Gear", {"gear": 0}, timeout=5)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                              {"info":{"totalParkingEnergy":totalParkingEnergy}}, timeout=5)
        sleep(1)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {}, 
                                              {"out":{"totalParkingEnergy":totalParkingEnergy}})
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 40.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 80.0)#高压输出能量
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                              {"info":{"totalParkingEnergy":totalParkingEnergy+0.04}}, timeout=3)
        time1=time.time()
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {}, 
                                              {"out":{"totalParkingEnergy":totalParkingEnergy+0.04}})
        self.partner.empty_all() 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 50.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 150.0)#高压输出能量
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                              {"info":{"totalParkingEnergy":totalParkingEnergy+0.1}}, timeout=3)
        time2=time.time()
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {}, 
                                              {"out":{"totalParkingEnergy":totalParkingEnergy+0.1}})
        assert 1.8<time2 -time1<2.1 #2S上报周期

    @allure.title("通知驻车能量消耗信息_充电时到非充电时totalParkingEnergy通过totalEnergy之outputEnergy和recoveryEnergy触发更新的逻辑")
    @pytest.mark.full
    def test_caseid_1989096(self): 
        totalParkingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['totalParkingEnergy']
        parkingCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCounter']
        logger.info("totalParkingEnergy:{}".format(totalParkingEnergy))
        logger.info("parkingCounter:{}".format(parkingCounter))
        sleep(1)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {}, 
                                              {"out":{"totalParkingEnergy":totalParkingEnergy}})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)#充电开始  
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 3)#充电结束
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 10.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 50.0)#高压输出能量
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 40.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 80.0)#高压输出能量
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, 
                                        "ParkingEnergyConsumptionInfo",{"info":{"totalParkingEnergy":totalParkingEnergy+0.04,"parkingCounter":parkingCounter}},timeout=3)
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 50.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 150.0)#高压输出能量
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, 
                                        "ParkingEnergyConsumptionInfo",{"info":{"totalParkingEnergy":totalParkingEnergy+0.1,"parkingCounter":parkingCounter}},timeout=3)

    @allure.title("通知驻车能量消耗信息_双电机400V_断电15S内所有数据被记忆")
    @pytest.mark.full
    def test_caseid_1989100(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 10.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 50.0)#高压输出能量
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 7)  
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 8)#放电开始
        sleep(5)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr30, 'TotDchaEgy', 1000.0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)#放电结束
        sleep(10)
        totalParkingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['totalParkingEnergy']
        parkingCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCounter']
        parkingThermalEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy']
        parkingCabinEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy']
        sentryModeEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeEnergy']
        sentryModeCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeCounter']
        disChargingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['disChargingEnergy']
        disChargingCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['disChargingCounter']
        sleep(5)
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, 
                                        "ParkingEnergyConsumptionInfo",{"info":{"totalParkingEnergy":totalParkingEnergy,"parkingCounter":parkingCounter,
                                                      "parkingCabinEnergy":parkingCabinEnergy,"sentryModeEnergy":sentryModeEnergy,
                                                      "sentryModeCounter":sentryModeCounter,"parkingThermalEnergy":parkingThermalEnergy,
                                                      "disChargingEnergy":disChargingEnergy,"disChargingCounter":disChargingCounter}},timeout=3)
    
    @allure.title("通知驻车能量消耗信息_双电机400V_诊断重启5S内所有数据被记忆")
    @pytest.mark.full
    def test_caseid_1989101(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 10.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 50.0)#高压输出能量
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 7)  
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 8)#放电开始
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)#放电结束
        sleep(6)
        totalParkingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['totalParkingEnergy']
        parkingCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCounter']
        parkingThermalEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy']
        parkingCabinEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy']
        sentryModeEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeEnergy']
        sentryModeCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeCounter']
        disChargingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['disChargingEnergy']
        disChargingCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['disChargingCounter']
        logger.info("totalParkingEnergy:{}".format(totalParkingEnergy))
        self.sd_tester.reset_ecu()#正常下电
        self.partner.wait_for_service_reconnect(HIGHVOLTAGE_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, 
                                        "ParkingEnergyConsumptionInfo",{"info":{"totalParkingEnergy":totalParkingEnergy,"parkingCounter":parkingCounter,
                                                      "parkingCabinEnergy":parkingCabinEnergy,"sentryModeEnergy":sentryModeEnergy,
                                                      "sentryModeCounter":sentryModeCounter,"parkingThermalEnergy":parkingThermalEnergy,
                                                      "disChargingEnergy":disChargingEnergy,"disChargingCounter":disChargingCounter}},timeout=3)
        
    @allure.title("通知驻车能量消耗信息_上电P档时parkingCabinEnergy或者parkingThermalEnergy触发更新的逻辑")
    @pytest.mark.full
    def test_caseid_1989087(self): 
        totalParkingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['totalParkingEnergy'] #总消耗能量
        parkingCabinEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy'] #座舱消耗能量
        parkingThermalEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy'] #热消耗能量
        logger.info(f"当前totalParkingEnergy:{totalParkingEnergy}且当前parkingCabinEnergy:{parkingCabinEnergy}且当前parkingThermalEnergy:{parkingThermalEnergy}")
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "Gear", {"gear": 0}, timeout=5)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                              {"info":{"totalParkingEnergy":totalParkingEnergy,
                                                       "parkingCabinEnergy":parkingCabinEnergy,
                                                       "parkingThermalEnergy":parkingThermalEnergy}}, timeout=5)
        sleep(1)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {}, 
                                              {"out":{"totalParkingEnergy":totalParkingEnergy,
                                                       "parkingCabinEnergy":parkingCabinEnergy,
                                                       "parkingThermalEnergy":parkingThermalEnergy}},timeout=1)
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 18000.0)#热消耗能量
        sleep(20)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 0.0)#热消耗能量
        sleep(1)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                              {"info":{"totalParkingEnergy":totalParkingEnergy,
                                                       "parkingCabinEnergy":parkingCabinEnergy,
                                                       "parkingThermalEnergy":parkingThermalEnergy+0.1}}, timeout=2)
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 18000.0)#座舱消耗能量
        sleep(40)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 0.0)#座舱消耗能量
        sleep(1)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                              {"info":{"totalParkingEnergy":totalParkingEnergy,
                                                       "parkingCabinEnergy":parkingCabinEnergy+0.2,
                                                       "parkingThermalEnergy":parkingThermalEnergy+0.1}}, timeout=2)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {}, 
                                              {"out":{"totalParkingEnergy":totalParkingEnergy,
                                                       "parkingCabinEnergy":parkingCabinEnergy+0.2,
                                                       "parkingThermalEnergy":parkingThermalEnergy+0.1}}, timeout=2)
        
    @allure.title("通知驻车能量消耗信息_充电开始_哨兵到充电结束_sentryModeCounter加1")
    @pytest.mark.sanity
    def test_caseid_1989112(self): 
        parkingCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCounter']
        sentryModeCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeCounter']
        logger.info("parkingCounter是:{}".format(parkingCounter))
        logger.info("sentryModeCounter:{}".format(sentryModeCounter))
        last=0
        for shaobingtime in [0,1]:
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2) #先充电
            sleep(1)
            self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":shaobingtime,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
            # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
            #                            {"sentryModeSts":[{"mainSts":0,"workSts":shaobingtime,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
            sleep(1)
            self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
            # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
            #                            {"sentryModeSts":[{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
            self.partner.ck_no_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo") #此时无event，因为处于充电中
            sleep(1)
            last= last+1
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 3) #每次充电后都有哨兵
            sleep(1)
            self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                      {"info":{"parkingCounter":parkingCounter,"sentryModeCounter":sentryModeCounter+last}})
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {}, 
                                              {"out":{"parkingCounter":parkingCounter,"sentryModeCounter":sentryModeCounter+2}}, timeout=2)

    @allure.title("通知驻车能量消耗信息_充电期间_多次哨兵_sentryModeCounter充电结束时加1")
    @pytest.mark.sanity
    def test_caseid_1989140(self): 
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2) #先充电
        sleep(1)
        parkingCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCounter']
        sentryModeCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeCounter']
        logger.info("parkingCounter是:{}".format(parkingCounter))
        logger.info("sentryModeCounter:{}".format(sentryModeCounter))
        for shaobingtime in [0,1]:
            self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":shaobingtime,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
            # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
            #                            {"sentryModeSts":[{"mainSts":0,"workSts":shaobingtime,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
            sleep(1)
            self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
            # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
            #                            {"sentryModeSts":[{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
            self.partner.ck_no_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo") #此时无event，因为处于充电中
            sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 3) #一个充电周期内多次充哨兵
        sleep(1)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                      {"info":{"parkingCounter":parkingCounter,"sentryModeCounter":sentryModeCounter+1}})
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {}, 
                                              {"out":{"parkingCounter":parkingCounter,"sentryModeCounter":sentryModeCounter+1}}, timeout=2)

    @allure.title("通知驻车能量消耗信息_充电期间__sentryModeCounter哨兵开始到哨兵结束时不+1")
    @pytest.mark.sanity
    def test_caseid_1989143(self): 
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2) 
        sleep(1)
        parkingCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCounter']
        sentryModeCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeCounter']
        logger.info("parkingCounter是:{}".format(parkingCounter))
        logger.info("sentryModeCounter:{}".format(sentryModeCounter))
        for shaobingtime in [0,1]:
            self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":shaobingtime,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
            # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
            #                            {"sentryModeSts":[{"mainSts":0,"workSts":shaobingtime,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
            sleep(1)
            self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
            # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
            #                            {"sentryModeSts":[{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
            sleep(1)
        self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":1,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
        # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
        #                            {"sentryModeSts":[{"mainSts":0,"workSts":1,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 3) 
        sleep(1)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo",{}, 
                                          {"out":{"parkingCounter":parkingCounter,"sentryModeCounter":sentryModeCounter}},timeout=3)

    @allure.title("通知驻车能量消耗信息_哨兵期间充电开始到结束_sentryModeCounter不加1")
    @pytest.mark.sanity
    def test_caseid_1989111(self): 
        parkingCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCounter']
        sentryModeCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeCounter']
        logger.info("parkingCounter是:{}".format(parkingCounter))
        logger.info("sentryModeCounter:{}".format(sentryModeCounter))
        for shaobingtime in [0,1]:
            self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":shaobingtime,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
            # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
            #                            {"sentryModeSts":[{"mainSts":0,"workSts":shaobingtime,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
            sleep(1)
            self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
            # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
            #                            {"sentryModeSts":[{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
            sleep(1)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2) 
            sleep(1)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 3) 
            sleep(1)
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                          {"info":{"parkingCounter":parkingCounter,"sentryModeCounter":sentryModeCounter+2}},timeout=3)

    @allure.title("通知驻车能量消耗信息_哨兵非2到2时sentryModeCounter加1")
    @pytest.mark.sanity
    def test_caseid_1989107(self): 
        parkingCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCounter']
        sentryModeCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeCounter']
        logger.info("parkingCounter是:{}".format(parkingCounter))
        logger.info("sentryModeCounter:{}".format(sentryModeCounter))
        for shaobingtime in [0,1]:
            self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":shaobingtime,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
            # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
            #                            {"sentryModeSts":[{"mainSts":0,"workSts":shaobingtime,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
            sleep(1)
            self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
            # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
            #                            {"sentryModeSts":[{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                          {"info":{"parkingCounter":parkingCounter,"sentryModeCounter":sentryModeCounter+2}},timeout=3)
        
    @allure.title("通知驻车能量消耗信息_sentryModeEnergy非放电时_更新逻辑")
    @pytest.mark.smoke
    def test_caseid_1989108(self): 
        self.Base_shaobing_inCreas_200wh()
        sleep(2)
        totalParkingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['totalParkingEnergy']
        sentryModeEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeEnergy']
        logger.info("totalParkingEnergy:{}".format(totalParkingEnergy))
        logger.info("sentryModeEnergy:{}".format(sentryModeEnergy))
        # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
        #                            {"sentryModeSts":[{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
        self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'EngSt1WdStsEngSt1WdSts', 6)
        sleep(1)#清除之前的高压ConsumptionInfo
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 40.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 80.0)#高压输出能量    
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo", #哨兵增加时total也增加
                                          {"info":{"totalParkingEnergy":totalParkingEnergy+0.04,"sentryModeEnergy":sentryModeEnergy+0.04}},timeout=4)
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 50.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 150.0)#高压输出能量
        sleep(1)
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                          {"info":{"totalParkingEnergy":totalParkingEnergy+0.1,"sentryModeEnergy":sentryModeEnergy+0.1}},timeout=3)
        parkingCabinEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy']
        parkingThermalEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy']
        logger.info("parkingCabinEnergy:{}".format(parkingCabinEnergy))
        logger.info("parkingThermalEnergy:{}".format(parkingThermalEnergy))
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 18000.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 18000.0)#座舱消耗能量
        sleep(20)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 0.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 0.0)#座舱消耗能量
        sleep(1)
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                          {"info":{"totalParkingEnergy":totalParkingEnergy+0.1}},timeout=3)
        parkingCabinEnergy3 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy']
        parkingThermalEnergy3 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy']
        sentryModeEnergy3 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeEnergy']
        assert 0.08<parkingCabinEnergy3-parkingCabinEnergy<0.11 and 0.08<parkingThermalEnergy3-parkingThermalEnergy<0.11
        assert 0.08< sentryModeEnergy-sentryModeEnergy3<0.11
        # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
        #                            {"sentryModeSts":[{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
        self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", #关闭哨兵
                                       {"sentryModeSts":{"mainSts":0,"workSts":1,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 18000.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 18000.0)#座舱消耗能量
        sleep(20)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 0.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 0.0)#座舱消耗能量
        sleep(1)
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                          {"info":{"totalParkingEnergy":totalParkingEnergy+0.1,}},timeout=3)
        sentryModeEnergy4 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeEnergy']
        assert sentryModeEnergy4==sentryModeEnergy3
        parkingCabinEnergy2 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy']
        parkingThermalEnergy2 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy']
        assert 0.08<parkingCabinEnergy2-parkingCabinEnergy3<0.11 and 0.08<parkingThermalEnergy2-parkingThermalEnergy3<0.11

    @allure.title("通知驻车能量消耗信息_sentryModeEnergy开启后并交流放电_更新逻辑（哨兵结束后继续放电）")
    @pytest.mark.sanity
    def test_caseid_1989109(self): 
        self.Base_shaobing_inCreas_200wh()
        sleep(2)
        totalParkingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['totalParkingEnergy']
        sentryModeEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeEnergy']
        logger.info("totalParkingEnergy:{}".format(totalParkingEnergy))
        logger.info("sentryModeEnergy:{}".format(sentryModeEnergy))
        # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
        #                            {"sentryModeSts":[{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
        self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'EngSt1WdStsEngSt1WdSts', 6)
        sleep(1)#清除之前的高压ConsumptionInfo
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 40.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 80.0)#高压输出能量  
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                          {"info":{"totalParkingEnergy":totalParkingEnergy+0.04,"sentryModeEnergy":sentryModeEnergy+0.04}},timeout=3)
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 50.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 150.0)#高压输出能量   
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                          {"info":{"totalParkingEnergy":totalParkingEnergy+0.1,"sentryModeEnergy":sentryModeEnergy+0.1}},timeout=3)
        parkingCabinEnergy1 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy']
        parkingThermalEnergy1 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy']
        logger.info("parkingCabinEnergy1:{}".format(parkingCabinEnergy1))
        logger.info("parkingThermalEnergy1:{}".format(parkingThermalEnergy1))
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 18000.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 18000.0)#座舱消耗能量
        sleep(20)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 0.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 0.0)#座舱消耗能量
        sleep(1)
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                          {"info":{"totalParkingEnergy":totalParkingEnergy+0.1}},timeout=3)
        parkingCabinEnergy3 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy']
        parkingThermalEnergy3 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy']
        sentryModeEnergy3 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeEnergy']
        assert 0.08<parkingCabinEnergy3-parkingCabinEnergy1<0.11 and 0.08<parkingThermalEnergy3-parkingThermalEnergy1<0.11
        assert 0.08< sentryModeEnergy-sentryModeEnergy3<0.11

        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 7)  
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 8) #交流枪开始放电
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr30, 'TotDchaEgy', 101.0) #放电增量0.101kwh
        sleep(2)
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                          {"info":{"totalParkingEnergy":totalParkingEnergy+0.1}},timeout=3)
        sleep(2)
        sentryModeEnergy4 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeEnergy']
        assert 0.15< sentryModeEnergy-sentryModeEnergy4<0.22
        # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
        #                            {"sentryModeSts":[{"mainSts":0,"workSts":0,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
        self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":0,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
        sleep(1)
        parkingCabinEnergy2 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy']
        parkingThermalEnergy2 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy']
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 18000.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 18000.0)#座舱消耗能量
        sleep(20)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 0.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 0.0)#座舱消耗能量
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr30, 'TotDchaEgy', 1000.0) #放电干扰
        sleep(2)
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                          {"info":{"totalParkingEnergy":totalParkingEnergy+0.1,"sentryModeEnergy":sentryModeEnergy4}},timeout=3)
        parkingCabinEnergy3 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy']
        parkingThermalEnergy3 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy']
        assert parkingCabinEnergy2 < parkingCabinEnergy3 and parkingThermalEnergy2 < parkingThermalEnergy3

    @allure.title("通知驻车能量消耗信息_交流放电后sentryModeEnergy_更新逻辑（哨兵结束后继续放电）")
    @pytest.mark.sanity
    def test_caseid_1989110(self): 
        self.Base_shaobing_inCreas_200wh()
        sleep(2)
        totalParkingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['totalParkingEnergy']
        sentryModeEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeEnergy']
        logger.info("totalParkingEnergy:{}".format(totalParkingEnergy))
        logger.info("sentryModeEnergy:{}".format(sentryModeEnergy))
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 7)  
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 8) #交流枪开始放电
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr30, 'TotDchaEgy', 101.0) #放电增量0.101kwh
        sleep(2)
        # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
        #                            {"sentryModeSts":[{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
        self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'EngSt1WdStsEngSt1WdSts', 6)
        sleep(1)#清除之前的高压ConsumptionInfo
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 40.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 80.0)#高压输出能量
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                          {"info":{"totalParkingEnergy":totalParkingEnergy+0.04,"sentryModeEnergy":sentryModeEnergy+0.04}},timeout=4)
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 50.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 150.0)#高压输出能量   
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                          {"info":{"totalParkingEnergy":totalParkingEnergy+0.1,"sentryModeEnergy":sentryModeEnergy+0.1}},timeout=3)
        parkingCabinEnergy1 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy']
        parkingThermalEnergy1 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy']
        logger.info("parkingCabinEnergy1:{}".format(parkingCabinEnergy1))
        logger.info("parkingThermalEnergy1:{}".format(parkingThermalEnergy1))
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 18000.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 18000.0)#座舱消耗能量
        sleep(20)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 0.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 0.0)#座舱消耗能量
        sleep(1)
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                          {"info":{"totalParkingEnergy":totalParkingEnergy+0.1}},timeout=3)
        parkingCabinEnergy3 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy']
        parkingThermalEnergy3 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy']
        sentryModeEnergy3 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeEnergy']
        assert 0.08<parkingCabinEnergy3-parkingCabinEnergy1<0.11 and 0.08<parkingThermalEnergy3-parkingThermalEnergy1<0.11
        assert 0.08< sentryModeEnergy-sentryModeEnergy3<0.11
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr30, 'TotDchaEgy', 1009.0) #放电增量1.009kwh
        sleep(4)
        sentryModeEnergy4 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeEnergy']
        assert 0< sentryModeEnergy3-sentryModeEnergy4
        # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
        #                            {"sentryModeSts":[{"mainSts":0,"workSts":0,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
        self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":0,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
        sleep(1)
        parkingCabinEnergy2 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy']
        parkingThermalEnergy2 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy']
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 18000.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 18000.0)#座舱消耗能量
        sleep(20)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 0.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 0.0)#座舱消耗能量
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr30, 'TotDchaEgy', 2000.0) #放电干扰
        sleep(2)
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                          {"info":{"totalParkingEnergy":totalParkingEnergy+0.1,"sentryModeEnergy":sentryModeEnergy4}},timeout=3)
        parkingCabinEnergy3 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy']
        parkingThermalEnergy3 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy']
        assert parkingCabinEnergy2 < parkingCabinEnergy3 and parkingThermalEnergy2 < parkingThermalEnergy3

    @allure.title("通知驻车能量消耗信息_有效挡位到到P档时_parkingCounter加1")
    @pytest.mark.sanity
    def test_caseid_1989089(self): 
        parkingCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCounter']
        logger.info("parkingCounter是:{}".format(parkingCounter))
        self.sd_tester.change_usage_mode(13)
        for gear in [1,2,3]:
            logger.info(f"切换档位为{gear}")
            self.Shift_Gear(gear)
            self.partner.empty_all(1) 
            self.Shift_Gear(0)
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",{"info":{"parkingCounter":parkingCounter+3}})
        
    @allure.title("通知驻车能量消耗信息_非P到P档时totalParkingEnergy通过totalEnergy之outputEnergy和recoveryEnergy触发更新的逻辑")
    @pytest.mark.sanity
    def test_caseid_1989090(self): 
        self.sd_tester.change_usage_mode(13)
        last_parkingCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['parkingCounter']
        last_totalParkingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['totalParkingEnergy']
        for gear in [1,2,3]:
            logger.info(f"切换档位为{gear}")
            self.Shift_Gear(gear)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'EngSt1WdStsEngSt1WdSts',0)
            parkingCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['parkingCounter']
            totalParkingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['totalParkingEnergy']
            logger.info(f"totalParkingEnergy是:{totalParkingEnergy}且parkingCounter是:{parkingCounter}")
            self.partner.empty_all(1) 
            self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {}, 
                                                {"out":{"totalParkingEnergy":totalParkingEnergy,"parkingCounter":parkingCounter}}, timeout=2)
            self.partner.empty_all(1) 
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 40.0) #高压回收能量
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 50.0)#高压输出能量
            self.partner.empty_all(2) 
            self.partner.ck_no_event_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                                {"out":{"totalParkingEnergy":totalParkingEnergy,"parkingCounter":parkingCounter}})
            self.Shift_Gear(0)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'EngSt1WdStsEngSt1WdSts',6)
            sleep(1)
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 50.0) #高压回收能量
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 70.0)#高压输出能量
            sleep(1)
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 60.0) #高压回收能量
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 100.0)#高压输出能量
            sleep(1)
            self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, 
                                        "ParkingEnergyConsumptionInfo",{"info":{"totalParkingEnergy":totalParkingEnergy+0.04,"parkingCounter":parkingCounter+1}})
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 70.0) #高压回收能量
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 170.0)#高压输出能量
            sleep(1)
            self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, 
                                        "ParkingEnergyConsumptionInfo",{"info":{"totalParkingEnergy":totalParkingEnergy+0.1,"parkingCounter":parkingCounter+1}})
            sleep(1)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {}, 
                                              {"out":{"totalParkingEnergy":last_totalParkingEnergy+0.3,
                                                       "parkingCounter":last_parkingCounter+3}}, timeout=2)

    @allure.title("通知驻车能量消耗信息_非P到P档时parkingCabinEnergy或者parkingThermalEnergy触发更新的逻辑")
    @pytest.mark.full
    def test_caseid_1989091(self): 
        self.sd_tester.change_usage_mode(13)
        last_parkingCabinEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['parkingCabinEnergy'] #初始座舱能量
        last_totalParkingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['totalParkingEnergy']#初始总能量
        last_parkingThermalEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['parkingThermalEnergy']#初始热管理能量
        for gear in [1,2,3]:
            logger.info(f"切换档位为{gear}")
            self.Shift_Gear(gear)
            sleep(1)
            parkingCabinEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['parkingCabinEnergy']
            totalParkingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['totalParkingEnergy']
            parkingThermalEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['parkingThermalEnergy']
            logger.info(f"totalParkingEnergy是:{totalParkingEnergy}parkingCabinEnergy:{parkingCabinEnergy}")
            logger.info(f"parkingThermalEnergy:{parkingThermalEnergy}")
            self.partner.empty_all(1) 
            self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {}, 
                                                {"out":{"totalParkingEnergy":totalParkingEnergy,"parkingCabinEnergy":parkingCabinEnergy,
                                                        "parkingThermalEnergy":parkingThermalEnergy}}, timeout=2)
            self.partner.empty_all(1) 
            self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr03, 'IsgIDc', 100.0) #驱动消耗开始
            self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysIdc',100.0)#驱动消耗开始
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 18000.0)#热消耗能量
            sleep(10)
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 0.0)#热消耗能量
            sleep(1)
            self.partner.ck_no_event_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                                {"out":{"totalParkingEnergy":totalParkingEnergy,"parkingCabinEnergy":parkingCabinEnergy,
                                                        "parkingThermalEnergy":parkingThermalEnergy}}, timeout=2)
            self.Shift_Gear(0) #P档后
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 18000.0)#热消耗能量
            sleep(20)
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 0.0)#热消耗能量
            sleep(1)
            self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, 
                                        "ParkingEnergyConsumptionInfo",{"info":{"totalParkingEnergy":totalParkingEnergy,"parkingCabinEnergy":parkingCabinEnergy}},timeout=2)
            parkingThermalEnergy1 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['parkingThermalEnergy']
            logger.info(f"20S的热消耗增量为{parkingThermalEnergy1-parkingThermalEnergy}")
            assert 0.08 <parkingThermalEnergy1-parkingThermalEnergy <0.11
            self.partner.empty_all(1) 
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 18000.0)#座舱消耗能量
            sleep(20)
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 0.0)#座舱消耗能量
            sleep(1)
            parkingCabinEnergy1 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['parkingCabinEnergy']
            logger.info(f"20S的座舱消耗增量为{parkingCabinEnergy1-parkingCabinEnergy}")
            assert 0.08 <parkingCabinEnergy1-parkingCabinEnergy <0.11
            sleep(1)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {}, 
                                              {"out":{"totalParkingEnergy":last_totalParkingEnergy}}, timeout=2)
        parkingCabinEnergy2 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['parkingCabinEnergy']
        parkingThermalEnergy2 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['parkingThermalEnergy']
        assert 0.24 <parkingCabinEnergy2-last_parkingCabinEnergy <0.33
        assert 0.24 <parkingThermalEnergy2-last_parkingThermalEnergy <0.33
        
    @allure.title("通知驻车能量消耗信息_双电机400V_非P档时所有参数不受干扰")
    @pytest.mark.full
    def test_caseid_1989092(self): 
        self.sd_tester.change_usage_mode(13)
        last_parkingCabinEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['parkingCabinEnergy'] #初始座舱能量
        last_totalParkingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['totalParkingEnergy']#初始总能量
        last_parkingThermalEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['parkingThermalEnergy']#初始热管理能量
        self.Shift_Gear(3)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {}, 
                                                {"out":{"totalParkingEnergy":last_totalParkingEnergy,"parkingCabinEnergy":last_parkingCabinEnergy,
                                                        "parkingThermalEnergy":last_parkingThermalEnergy}}, timeout=2)
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 18000.0)#座舱消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 18000.0)#热消耗能量
        sleep(10)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 0.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 0.0)#座舱消耗能量
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr03, 'IsgIDc', 100.0) #驱动消耗开始
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysIdc',100.0)#驱动消耗开始
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 40.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 80.0)#高压输出能量
        sleep(1)
        self.partner.ck_no_event_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                {"out":{"totalParkingEnergy":last_totalParkingEnergy,"parkingCabinEnergy":last_parkingCabinEnergy,
                                                        "parkingThermalEnergy":last_parkingThermalEnergy}}, timeout=2)
        
    @allure.title("通知驻车能量消耗信息_双电机400V_开始充电时_所有参数不受干扰")
    @pytest.mark.full
    def test_caseid_1989093(self): 
        last_parkingCabinEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['parkingCabinEnergy'] #初始座舱能量
        last_totalParkingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['totalParkingEnergy']#初始总能量
        last_parkingThermalEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                    "out"]['parkingThermalEnergy']#初始热管理能量
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)#充电电开始  
        self.partner.empty_all(1) 
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {}, 
                                                {"out":{"totalParkingEnergy":last_totalParkingEnergy,"parkingCabinEnergy":last_parkingCabinEnergy,
                                                        "parkingThermalEnergy":last_parkingThermalEnergy}}, timeout=2)
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 18000.0)#座舱消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 18000.0)#热消耗能量
        sleep(10)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 0.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 0.0)#座舱消耗能量
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr03, 'IsgIDc', 100.0) #驱动消耗开始
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysIdc',100.0)#驱动消耗开始
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 40.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 80.0)#高压输出能量
        sleep(1)
        self.partner.ck_no_event_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                {"out":{"totalParkingEnergy":last_totalParkingEnergy,"parkingCabinEnergy":last_parkingCabinEnergy,
                                                        "parkingThermalEnergy":last_parkingThermalEnergy}}, timeout=2)

    @allure.title("通知驻车能量消耗信息_sentryModeEnergy_充电时哨兵_哨兵能耗不增加（哨兵开始到哨兵结束一致保持充电）")
    @pytest.mark.full
    def test_caseid_1989113(self): 
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)#充电开始 
        sleep(1)
        totalParkingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['totalParkingEnergy']
        sentryModeEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeEnergy']
        logger.info("totalParkingEnergy:{}".format(totalParkingEnergy))
        logger.info("sentryModeEnergy:{}".format(sentryModeEnergy))
        # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
        #                            {"sentryModeSts":[{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
        self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 40.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 80.0)#高压输出能量
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 50.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 150.0)#高压输出能量     
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 18000.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 18000.0)#座舱消耗能量
        sleep(10)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 0.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 0.0)#座舱消耗能量
        self.partner.ck_no_event_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                             {"out":{"totalParkingEnergy":totalParkingEnergy,"sentryModeEnergy":sentryModeEnergy}})
        # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
        #                            {"sentryModeSts":[{"mainSts":0,"workSts":1,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
        self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":1,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 18000.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 18000.0)#座舱消耗能量
        sleep(10)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 0.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 0.0)#座舱消耗能量
        self.partner.empty_all(1) 
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {}, 
                                                {"out":{"totalParkingEnergy":totalParkingEnergy,"sentryModeEnergy":sentryModeEnergy}})

    @allure.title("通知驻车能量消耗信息_sentryModeEnergy开启后并交流充电_更新逻辑（哨兵结束前结束充电）")
    @pytest.mark.sanity
    def test_caseid_1989114(self): 
        self.Base_shaobing_inCreas_200wh()
        totalParkingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['totalParkingEnergy']
        sentryModeEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeEnergy']
        logger.info("totalParkingEnergy:{}".format(totalParkingEnergy))
        logger.info("sentryModeEnergy:{}".format(sentryModeEnergy))
        # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
        #                            {"sentryModeSts":[{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
        self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'EngSt1WdStsEngSt1WdSts', 6)
        sleep(1)#清除之前的高压ConsumptionInfo
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 40.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 80.0)#高压输出能量
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 50.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 150.0)#高压输出能量     
        sleep(1)
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                          {"info":{"totalParkingEnergy":totalParkingEnergy+0.1,"sentryModeEnergy":sentryModeEnergy+0.1}},timeout=3)
        parkingCabinEnergy1 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy']
        parkingThermalEnergy1 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy']
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 18000.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 18000.0)#座舱消耗能量
        sleep(20)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 0.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 0.0)#座舱消耗能量
        sleep(1)
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                          {"info":{"totalParkingEnergy":totalParkingEnergy+0.1}},timeout=3)
        parkingCabinEnergy3 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy']
        parkingThermalEnergy3 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy']
        sentryModeEnergy3 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeEnergy']
        assert 0.08<parkingCabinEnergy3-parkingCabinEnergy1<0.11 and 0.08<parkingThermalEnergy3-parkingThermalEnergy1<0.11
        assert 0.08< sentryModeEnergy-sentryModeEnergy3<0.11
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1)  
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)#交流充电开始 
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 18000.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 18000.0)#座舱消耗能量
        sleep(20)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 0.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 0.0)#座舱消耗能量
        sleep(1) #无驻车能耗信息
        self.partner.ck_no_event_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                            {"out":{"totalParkingEnergy":totalParkingEnergy+0.1,"sentryModeEnergy":sentryModeEnergy3,
                                    "parkingCabinEnergy":parkingCabinEnergy3,"parkingThermalEnergy":parkingThermalEnergy3}},timeout=3)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 3)#交流充电结束
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 18000.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 18000.0)#座舱消耗能量
        sleep(20)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 0.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 0.0)#座舱消耗能量
        sleep(1) #无驻车能耗信息
        parkingCabinEnergy2 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy']
        parkingThermalEnergy2 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy']
        sentryModeEnergy2 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeEnergy']
        assert parkingCabinEnergy2 >parkingCabinEnergy1 and parkingThermalEnergy2 > parkingThermalEnergy1 
        assert sentryModeEnergy2 != sentryModeEnergy-0.1

    @allure.title("通知驻车能量消耗信息_sentryModeEnergy交流充电后开启哨兵再结束充电_更新逻辑（哨兵结束前结束充电）")
    @pytest.mark.full
    def test_caseid_1989115(self): 
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1)  
        self.Base_shaobing_inCreas_200wh()
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)#交流充电开始 
        self.partner.empty_all(1) 
        totalParkingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['totalParkingEnergy']
        sentryModeEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeEnergy']
        parkingCabinEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy']
        parkingThermalEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy']
        logger.info("totalParkingEnergy:{}".format(totalParkingEnergy))
        logger.info("sentryModeEnergy:{}".format(sentryModeEnergy))
        logger.info("parkingCabinEnergy:{}".format(parkingCabinEnergy))
        logger.info("parkingThermalEnergy:{}".format(parkingThermalEnergy))
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 18000.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 18000.0)#座舱消耗能量
        sleep(20)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 0.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 0.0)#座舱消耗能量
        sleep(1)
        self.partner.ck_no_event_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                            {"out":{"totalParkingEnergy":totalParkingEnergy,"sentryModeEnergy":sentryModeEnergy,
                                    "parkingCabinEnergy":parkingCabinEnergy,"parkingThermalEnergy":parkingThermalEnergy}},timeout=3)

        # self.partner.send_event_notify("SentryModeService_server", "SentryModeStsListInfo", 
        #                            {"sentryModeSts":[{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}]})
        self.partner.send_event_notify("SentryModeService_server", "NotifySentryModeSts", 
                                       {"sentryModeSts":{"mainSts":0,"workSts":2,"perceptionSts":0,"functionErr":0,"timestamp":1728926122362}})
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyIn', 40.0) #高压回收能量
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 80.0)#高压输出能量
        self.partner.ck_no_event_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                            {"out":{"totalParkingEnergy":totalParkingEnergy,"sentryModeEnergy":sentryModeEnergy,
                                    "parkingCabinEnergy":parkingCabinEnergy,"parkingThermalEnergy":parkingThermalEnergy}},timeout=3)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)#交流充电结束
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 18000.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 18000.0)#座舱消耗能量
        sleep(20)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr19, 'HvBattThermPwrCns', 0.0)#热消耗能量
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr41, 'HvCabinThermPwrCns', 0.0)#座舱消耗能量
        sleep(1) #无驻车能耗信息
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {}, 
                                                {"out":{"totalParkingEnergy":totalParkingEnergy}})
        parkingCabinEnergy2 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy']
        parkingThermalEnergy2 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy']
        sentryModeEnergy2 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeEnergy']
        assert parkingCabinEnergy2 >parkingCabinEnergy and parkingThermalEnergy2 > parkingThermalEnergy and 0 <=sentryModeEnergy2<sentryModeEnergy

    @allure.title("通知驻车能量消耗信息_双电机400V_非哨兵直接放电_非放电的其他参数不受干扰")
    @pytest.mark.full
    def test_caseid_1989116(self): 
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 7)  
        sleep(1)
        totalParkingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['totalParkingEnergy']
        sentryModeEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['sentryModeEnergy']
        parkingCabinEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingCabinEnergy']
        parkingThermalEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['parkingThermalEnergy']
        disChargingCounter = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['disChargingCounter']
        disChargingEnergy = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetParkingEnergyConsumptionInfo", {})[
                "out"]['disChargingEnergy']
        logger.info("totalParkingEnergy:{}".format(totalParkingEnergy))
        logger.info("sentryModeEnergy:{}".format(sentryModeEnergy))
        logger.info("parkingCabinEnergy:{}".format(parkingCabinEnergy))
        logger.info("parkingThermalEnergy:{}".format(parkingThermalEnergy))
        logger.info("disChargingEnergy:{}".format(disChargingEnergy))
        logger.info("disChargingCounter:{}".format(disChargingCounter))
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 8)#交流充电开始 
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr30, 'TotDchaEgy', 201.0)
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr30, 'TotDchaEgy', 1010.0)
        sleep(2)
        self.partner.ck_event_and_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "ParkingEnergyConsumptionInfo",
                                       {"info":{"totalParkingEnergy":totalParkingEnergy,"parkingCabinEnergy":parkingCabinEnergy,
                                                "parkingThermalEnergy":parkingThermalEnergy,"disChargingCounter":disChargingCounter+1,
                                                 "disChargingEnergy":disChargingEnergy+1.01,"sentryModeEnergy":sentryModeEnergy}})

#========================================================================================================================

@allure.feature("SOA服务接口")
@allure.story("BGM应用/HighVoltageAppService")
class TestHighVoltageAppService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([
            ("HighVoltageAppService", "client"),
            ("VehicleTimeService", "client"),
            ("HighVoltageService", "client")])
        self.partner.method_default_timeout = 3
        self.sd_tester.tester_present()
        self.ipdu.send_pdu('chassiscan1', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('chassiscan2', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('propulsioncan', 0x516, [0x16, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.sd_tester.write_single_ccp(973,2) #交直流都支持
        sleep(3)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.sd_tester.change_usage_mode(1)
        self.partner.empty_all(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消tcam的闹钟
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #请求预约充电回馈状态

    def after_each_func(self, ecu):
        self.ipdu.reset_check_results()
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.dk.stop_listen_dk_bgm_response()
        self.sd_tester.stop_tester_present()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    @allure.title("控制充电_遍历")
    @pytest.mark.smoke
    def test_caseid_1988406(self): 
        for cmd1 in [0,1,2]:
            for source1 in range(6):
                self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetChargingControl", {"cmd":{"type":cmd1,"source":source1}})
                if cmd1 ==0:
                    self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr08, 'ChrgSoftSwCtrlSt', 0, timeout=0.5)
                elif cmd1 ==1:
                    self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr08, 'ChrgSoftSwCtrlSt', 1, timeout=0.5)
                    self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr08, 'ChrgSoftSwCtrlSt', 0, timeout=0.5)
                else:
                    self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr08, 'ChrgSoftSwCtrlSt', 2, timeout=0.5)
                    self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr08, 'ChrgSoftSwCtrlSt', 0, timeout=0.5)
                sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        for source2 in range(6):
            self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetChargingControl", {"cmd":{"type":0,"source":source2}})
            sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(2)
        self.bgm_eth_inter.ck_signal_values("ChrgSoftSwCtrlSt", [])

    @allure.title("控制放电_遍历")
    @pytest.mark.smoke
    def test_caseid_1988407(self): 
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetDischargingControl", {"cmd":{"type":2,"source":1}})
        sleep(1)
        for source1 in range(6):
            for cmd1 in [0,1,2]:
                self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetDischargingControl", {"cmd":{"type":cmd1,"source":source1}})
                if cmd1 ==1:
                    self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr07, 'V2XDchaSwt', 2, timeout=0.5)
                else:
                    self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr07, 'V2XDchaSwt', 0, timeout=0.5)
                sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        for source2 in range(6):
            self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetDischargingControl", {"cmd":{"type":0,"source":source2}})
            sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(2)
        self.bgm_eth_inter.ck_ordered_array("V2XDchaSwt", [0])

    @allure.title("通知预约充电信息_出厂默认值")
    @pytest.mark.full
    def test_caseid_1988222(self): 
        self.del_SOAAPP_db()
        sleep(1)
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT) #会出现时间先同步后再上线高压APP服务，所以不校验固定默认值
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)
        now = datetime.datetime.now()
        todaymorning=now.replace(hour=8, minute=0, second=0, microsecond=0)
        todaymorning8 = int(todaymorning.timestamp())
        logger.info(f"当天早上8点为{todaymorning8}")
        mark1=todaymorning8+14*60*60
        mark2=todaymorning8+22*60*60
        logger.info(f"通知的当天开始时间为{mark1}且结束时间为{mark2}")
        #时间同步后上报当天的22点到次日6点
        sleep(0.5)  
        starttime1 = self.partner.return_latest_event(HIGHVOLTAGEAPP_SERVICE_CLIENT,
                                                      "BookChargingInfo")["info"]['acInfo']["info"]['startTime']
        sleep(0.5)
        endtime1 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT,
                                                                      "GetBookChargingInfo", {})["out"]['acInfo']["info"]['endTime']
        assert  starttime1== mark1 or mark1 ==starttime1+86400
        assert  endtime1== mark2 or mark2 ==endtime1+86400 #x需求规定只需要校验是否是22:00即可 SOA-29495

    @allure.title("通知预约充电显示信息_出厂默认值")
    @pytest.mark.full
    def test_caseid_1988547(self): 
        self.del_SOAAPP_db()
        sleep(1)
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT,pause_all_bus=True, resume_all_bus=False)
        sleep(1)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetDisplayBookChargingInfo", {},
                                             {"out": {"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60,"kSecond":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60,"kSecond":60}}},timeout=3)
        
#=============================================================================================

@allure.feature("SOA服务接口")
@allure.story("BGM应用/HighVoltageAppService")
class TestHighVoltageAppService_TimeNotSync(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([
            ("HighVoltageAppService", "client"),
            ("HighVoltageService", "client"),
            ("VehicleTimeService", "client")])
        self.partner.method_default_timeout = 3
        self.sd_tester.tester_present()
        self.ipdu.send_pdu('chassiscan1', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('chassiscan2', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('propulsioncan', 0x516, [0x16, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.sd_tester.write_single_ccp(973,2) #交直流都支持
        sleep(3)
        self.nucapp.tcam_power_off()
        sleep(25) #制造时间不同步

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.sd_tester.change_usage_mode(1)
        self.partner.empty_all(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #请求预约充电回馈状态成功

    def after_each_func(self, ecu):
        self.ipdu.reset_check_results()
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        try:
            self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        except Exception as err:
            self.nucapp.tcam_power_off()
            sleep(25)
            self.nucapp.bgm_power_off()
            sleep(2)
            self.nucapp.bgm_power_on()
            self.nucapp.tcam_power_on()
            self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
            self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=300)
        else:
            assert True
        self.dk.stop_listen_dk_bgm_response()
        self.sd_tester.stop_tester_present()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    @allure.title("通知预约充电信息_kBookStsDefault →kBookStsFailed_off_时间未同步情况下新建")
    @pytest.mark.full
    def test_caseid_1988227(self): 
        self.del_SOAAPP_db()
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #反馈正常
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        sleep(1)
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        sleep(2)
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 0}})
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+60, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}})
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 0, timeout=0.5)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":5,
                                                                    "info":{"startTime":1609509600,"endTime":1609538400,"repeatType":0},
                                                                    "isToTargetSOCStop":False}}})
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":1609509600,"endTime":1609538400,"repeatType":0},
                                                                    "isToTargetSOCStop":False}}},timeout=3)#会跳到3,1
        
    @allure.title("通知预约充电信息_kBookStsDefault →kBookStsFailed_off_时间不同步情况下取消")
    @pytest.mark.full
    def test_caseid_1988230(self): 
        self.del_SOAAPP_db()
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #反馈正常
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        sleep(1)
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        sleep(2)
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 0}})
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}})
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 0, timeout=0.5)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":5,
                                                                    "info":{"startTime":1609509600,"endTime":1609538400,"repeatType":0},
                                                                    "isToTargetSOCStop":False}}})
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":1609509600,"endTime":1609538400,"repeatType":0},
                                                                    "isToTargetSOCStop":False}}},timeout=3)#会跳到3,1
        
    @allure.title("通知预约充电信息_kBookStsDefault →kBookStsFailed_off_时间不同步情况下更新")
    @pytest.mark.full
    def test_caseid_1988231(self): 
        self.del_SOAAPP_db()
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #反馈正常
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        sleep(2)
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 0}})
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 2, "source": 0, "timeInfo": {"startTime": nowtime+60, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}})
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 0, timeout=0.5)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":5,
                                                                    "info":{"startTime":1609509600,"endTime":1609538400,"repeatType":0},
                                                                    "isToTargetSOCStop":False}}})
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":1609509600,"endTime":1609538400,"repeatType":0},
                                                                    "isToTargetSOCStop":False}}},timeout=3)

#=============================================================================================

@allure.feature("SOA服务接口")
@allure.story("BGM应用/HighVoltageAppService")
class TestHighVoltageAppService_TimeSync(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([
            ("HighVoltageAppService", "client"),
            ("HighVoltageService", "client"),
            ("VehicleTimeService", "client")])
        self.partner.method_default_timeout = 3
        self.sd_tester.tester_present()
        self.ipdu.send_pdu('chassiscan1', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('chassiscan2', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('propulsioncan', 0x516, [0x16, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.partner.unregister_event(VEHICLETIME_SERVICE_CLIENT)
        self.partner.register_event(VEHICLETIME_SERVICE_CLIENT,[{"VehicleTimeInfo":{"history_config": 1}}])
        self.sd_tester.write_single_ccp(973,2) #交直流都支持
        sleep(3)
        self.nucapp.bgm_power_off()
        self.nucapp.bgm_power_on()
        self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        sleep(5)#防止第一个case不稳定

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.sd_tester.change_usage_mode(1)
        self.partner.empty_all(1)
        try:
            self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        except Exception as err:
            self.nucapp.tcam_power_off()
            sleep(25)
            self.nucapp.bgm_power_off()
            sleep(2)
            self.nucapp.bgm_power_on()
            self.nucapp.tcam_power_on()
            self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
            self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=300)
        else:
            assert True
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消tcam的闹钟防止紊乱
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #请求预约充电回馈状态 枚举值取消

    def after_each_func(self, ecu):
        self.ipdu.reset_check_results()
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        try:
            self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        except Exception as err:
            self.nucapp.tcam_power_off()
            sleep(25)
            self.nucapp.bgm_power_off()
            sleep(2)
            self.nucapp.bgm_power_on()
            self.nucapp.tcam_power_on()
            self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
            self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=300)
        else:
            assert True
        self.dk.stop_listen_dk_bgm_response()
        self.sd_tester.stop_tester_present()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def set_BookChargingTime_Remote(self, startTime_hour, startTime_min, stopTime_hour, stopTime_min, sleeptime=1):
        '''预约充电时间 远控 开始和结束时间 '''
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr33, 'RemoteBookStrtTiChrgnTmrChrgnTmrhour', startTime_hour)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr33, 'RemoteBookStrtTiChrgnTmrChrgnTmrmin', startTime_min)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr33, 'RemoteBookStopTiChrgnTmrChrgnTmrhour', stopTime_hour)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr33, 'RemoteBookStopTiChrgnTmrChrgnTmrmin', stopTime_min)
        sleep(sleeptime)

    def set_BookChargingTime_Bluetooth(self, startTime_hour, startTime_min, stopTime_hour, stopTime_min, sleeptime=1):
        '''预约充电时间 蓝牙 开始和结束时间 '''
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr32, 'BthBookStrtTiChrgnTmrChrgnTmrhour', startTime_hour)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr32, 'BthBookStrtTiChrgnTmrChrgnTmrmin', startTime_min)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr32, 'BthBookStopTiChrgnTmrChrgnTmrhour', stopTime_hour)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr32, 'BthBookStopTiChrgnTmrChrgnTmrmin', stopTime_min)
        sleep(sleeptime)
        
    @allure.title("通知预约充电信息_kBookStsOff →kBookStsFailed_off_调用ALRAM服务失败")
    @pytest.mark.full
    def test_caseid_1988718(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #反馈正常
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}},timeout=3) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.partner.empty_all()
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}},timeout=3) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #请求预约充电回馈状态 枚举值取消
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}})
        self.nucapp.tcam_power_off() #制造tcam下线ALRAM服务断开
        sleep(31)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+240, "endTime": nowtime+600, 
                                                "repeatType": 1},"isToTargetSOCStop": False}},timeout=6) #tcam下电后会调用超时是正常的
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 0, timeout=0.5) #设置预约充电信号
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":5,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=6)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3) #会跳到3 1状态
        self.nucapp.tcam_power_on()
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)#恢复上电
        sleep(2)#重启不稳定

    @allure.title("通知预约充电信息_kBookStsDefault →kBookStsFailed_off_调用ALRAM服务失败")
    @pytest.mark.full
    def test_caseid_1988232(self): 
        self.del_SOAAPP_db()
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #反馈正常
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        sleep(2)
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info(f"当天早上8点为{todaymorning8}")
        mark1=todaymorning8+14*60*60
        mark2=todaymorning8+22*60*60
        logger.info(f"通知的当天开始时间为{mark1}且结束时间为{mark2}")
        logger.info("现在时间是:{}".format(nowtime))
        self.nucapp.tcam_power_off() #制造tcam下线ALRAM服务断开
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+60, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}},timeout=6) #tcam下电后会调用超时是正常的
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 0, timeout=0.5) #设置预约充电信号
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":5,
                                                                    "info":{"startTime":mark1,"endTime":mark2,"repeatType":0},
                                                                    "isToTargetSOCStop":False}}},timeout=6)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":mark1,"endTime":mark2,"repeatType":0},
                                                                    "isToTargetSOCStop":False}}},timeout=3) #会跳到3 1状态
        self.nucapp.tcam_power_on()
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)#恢复上电
        sleep(2)#重启不稳定
        
    @allure.title("通知预约充电信息_kBookStsDefault →kBookStsWait_没插枪再预约")
    @pytest.mark.full
    def test_caseid_1988233(self): 
        self.del_SOAAPP_db()
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #反馈正常
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        sleep(1)
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        sleep(2)
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+60, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}},timeout=6) #tcam下电后会调用超时是正常的
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}})
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3)
        
    @allure.title("通知预约充电信息_kBookStsDefault →kBookStsFailed_off新建endtime小于NOWTIME+300")
    @pytest.mark.full
    def test_caseid_1988228(self): 
        self.del_SOAAPP_db()
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #反馈正常
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        sleep(2)
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-120, "endTime": nowtime+240, 
                                                "repeatType": 1},"isToTargetSOCStop": False}})
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 0, timeout=0.5) #设置预约充电信号
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86280,"endTime":nowtime+86640,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}})
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86280,"endTime":nowtime+86640,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3) #结束时间5min内的推明天
        
    @allure.title("通知预约充电信息_kBookStsDefault →kBookStsWait_没插枪再预约_设置starttime早于now")
    @pytest.mark.full
    def test_caseid_1988234(self): 
        self.del_SOAAPP_db()
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #反馈正常
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        sleep(2)
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp()
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}},timeout=6) #tcam下电后会调用超时是正常的
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86820,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}})
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86820,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3) #推到明天
        
    @allure.title("通知预约充电信息_kBookStsDefault →kBookStsWait_插枪没充电再预约_设置starttime早于now且endtime晚于now")
    @pytest.mark.full
    def test_caseid_1988236(self): 
        self.del_SOAAPP_db()
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(5)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        sleep(2)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) 
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #回复成功
        logger.info(f"通知的开始时间{nowtime+86340}和结束时间{nowtime+360}")
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging
        
    @allure.title("通知预约充电信息_kBookStsDefault →kBookStsWait_插枪没充电再预约_设置starttime和endtime都早于now")
    @pytest.mark.full
    def test_caseid_1988237(self): 
        self.del_SOAAPP_db()
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(5)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        sleep(2)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-420, "endTime": nowtime-60, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) 
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号状态机需要判断
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #回复成功
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        logger.info(f"通知的开始时间{nowtime+86040}和结束时间{nowtime+86340}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+85980,"endTime":nowtime+86340,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging
        
    @allure.title("通知预约充电信息_kBookStsDefault →kBookStsWait_插枪没充电再预约_设置starttime和endtime都晚于now")
    @pytest.mark.full
    def test_caseid_1988238(self): 
        self.del_SOAAPP_db()
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(5)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=10)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        sleep(2)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) 
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #回复成功
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging
        
    @allure.title("通知预约充电信息_满充和有效结束时间来回切换")
    @pytest.mark.full
    def test_caseid_1989596(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                            {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-28680, "endTime": nowtime+600, 
                                                    "repeatType": 1},"isToTargetSOCStop": False}}) #先打开 #7h58min
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.partner.empty_all(2)
        for i in range(10):
            logger.info(f"第{i}次修改")
            self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                            {"cmd": {"type": 2, "source": 0, "timeInfo": {"startTime": nowtime-28680, "endTime": nowtime+600, 
                                                    "repeatType": 1},"isToTargetSOCStop": True}}) #先打开 #7h58min
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #请求预约充电回馈状态
            sleep(1)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
            self.partner.empty_all(0.5)
            self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                            {"cmd": {"type": 2, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+600, 
                                                    "repeatType": 1},"isToTargetSOCStop": False}}) 
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #请求预约充电回馈状态
            sleep(1)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
            sleep(1)
            self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                        "info":{"startTime":nowtime+120,"endTime":nowtime+600,"repeatType":1},
                                                                        "isToTargetSOCStop":False}}}) #进入wait
        self.partner.empty_all(2)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo",{},{"out":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                        "info":{"startTime":nowtime+120,"endTime":nowtime+600,"repeatType":1},
                                                                        "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=4) 
        except Exception:
            assert True
        else:
            assert False
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=1)#校验休眠后拔枪置0 
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                        "info":{"startTime":nowtime+120,"endTime":nowtime+600,"repeatType":1},
                                                                        "isToTargetSOCStop":False}}}) #进入wait

    @allure.title("通知预约充电信息_设置当前时间-开始时间小于8h并且endtime无效再插枪_结束继续充电不停止的情况")
    @pytest.mark.full
    def test_caseid_1989523(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-28680, "endTime": nowtime+600, 
                                                "repeatType": 1},"isToTargetSOCStop": True}}) #先打开 #7h58min
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+57720,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入wait
        self.partner.empty_all(60)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) 
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+57720,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入charging后时间更新
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookStopTiAchieved", 1,timeout=100) #停止充电
        except Exception:
            assert True
        else:
            assert False
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookStopTiAchieved", 0,timeout=1)

    @allure.title("通知预约充电信息_设置当前时间-开始时间小于8h但是过了8h并且endtime无效再插枪的情况")
    @pytest.mark.full
    def test_caseid_1989521(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-28680, "endTime": nowtime+600, 
                                                "repeatType": 1},"isToTargetSOCStop": True}}) #先打开 #7h58min
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+57720,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入wait
        sleep(180)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #请求充电#状态机需要判断
        except Exception:
            assert True
        else:
            assert False
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=1) #请求充电#状态机需要判断
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+57720,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入charging后时间更新

    @allure.title("通知预约充电信息_设置当前时间-开始时间小于8h但是过了8h并且endtime有效再插枪的情况")
    @pytest.mark.full
    def test_caseid_1989519(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-28680, "endTime": nowtime+600, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开 #7h58min
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+57720,"endTime":nowtime+87000,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(180)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #请求充电#状态机需要判断
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+57720,"endTime":nowtime+87000,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间更新
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈

    @allure.title("通知预约充电信息_当前时间-开始时间大于8h并且endtime无效的情况")
    @pytest.mark.sanity
    def test_caseid_1989518(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-8*3600, "endTime": nowtime+600, 
                                                "repeatType": 1},"isToTargetSOCStop": True}}) #先打开
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        logger.info(f"通知的开始时间{nowtime+240}和结束时间{nowtime+86760060}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+57600,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #请求充电#状态机需要判断
        except Exception:
            assert True
        else:
            assert False
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=1) #请求充电#状态机需要判断
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+57600,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入charging后时间更新

    @allure.title("通知预约充电信息_当前时间-开始时间大于8h并且endtime有效的情况")
    @pytest.mark.full
    def test_caseid_1989517(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-9*3600, "endTime": nowtime+600, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        logger.info(f"通知的开始时间{nowtime+240}和结束时间{nowtime+86760060}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+54000,"endTime":nowtime+87000,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #请求充电#状态机需要判断
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+54000,"endTime":nowtime+87000,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间更新
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈

    @allure.title("通知预约充电信息stanby下_休眠下拔枪")
    @pytest.mark.full
    def test_caseid_1989152(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+240, "endTime": nowtime+600, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        logger.info(f"通知的开始时间{nowtime+240}和结束时间{nowtime+86760060}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+240,"endTime":nowtime+600,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+240,"endTime":nowtime+600,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间更新
        self.nucapp.bgm_power_off()
        sleep(3)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) #插枪
        self.partner.empty_all(1)
        self.nucapp.bgm_power_on()
        self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo",{},{"out":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+240,"endTime":nowtime+600,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=4) 
        sleep(3)
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=0.5)#校验休眠后拔枪置0 

    @allure.title("通知预约充电信息_kBookStsDefault →kBookStsWait_插枪没充电再预约_设置starttime早于now且endtime=now")
    @pytest.mark.full
    def test_caseid_1988239(self): 
        self.del_SOAAPP_db()
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(5)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        sleep(2)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-420, "endTime": nowtime, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) 
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号，状态机需要判断
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #回复成功
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=3) #请求充电#状态机需要判断
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+85980,"endTime":nowtime+86400,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        
    @allure.title("通知预约充电信息_kBookStsDefault →kBookStsWait_插枪没充电再预约_设置starttime=now且endtime晚于now")
    @pytest.mark.full
    def test_caseid_1988241(self): 
        self.del_SOAAPP_db()
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(5)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        sleep(2)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #避免与当前时间相差不足5min
        # self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #回复成功
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #请求充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        logger.info(f"通知的开始时间{nowtime+86400}和结束时间{nowtime+86760}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86400,"endTime":nowtime+86820,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging
        
    @allure.title("通知预约充电信息_kBookStsDefault →kBookStsWait_插枪充电预约后负响应")
    @pytest.mark.full
    def test_caseid_1988245(self): 
        self.del_SOAAPP_db()
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(5)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        sleep(2)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-360, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #避免与当前时间相差不足5min
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 3) #回复失败
        logger.info(f"通知的开始时间应该为{nowtime+86040}和结束时间{nowtime+86760}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":1,
                                                                    "info":{"startTime":nowtime+86040,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入失效
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 1)
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86040,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #回复

    @allure.title("通知预约充电信息_kBookStsDefault →kBookStsWait_插枪未充电再预约后回复负响应")
    @pytest.mark.full
    def test_caseid_1988246(self): 
        self.del_SOAAPP_db()
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(5)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-360, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #避免与当前时间相差不足5min
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 3) #回复失败
        logger.info(f"通知的开始时间应该为{nowtime+86040}和结束时间{nowtime+86760}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":1,
                                                                    "info":{"startTime":nowtime+86040,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入alreadycharging
        
    @allure.title("通知预约充电信息kBookStsOff→kBookStsFailed_off _时间不同步下设置")
    @pytest.mark.full
    def test_caseid_1988247(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)                                
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        starttime =self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},timeout=3)[
                "out"]['acInfo']['info']['startTime']
        endtime =self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},timeout=3)[
                "out"]['acInfo']['info']['endTime']
        self.nucapp.tcam_power_off()
        sleep(25)
        self.nucapp.bgm_power_off()
        sleep(2)
        self.nucapp.bgm_power_on()
        self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        sleep(10)
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 0}})
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-360, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #取消
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #回复成功
        logger.info(f"通知的开始时间应该为{starttime}和结束时间{endtime}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":5,
                                                                    "info":{"startTime":starttime,"endTime":endtime,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入失效
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":starttime,"endTime":endtime,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入STS off

    @allure.title("通知预约充电信息_kBookStsDefault →kBookStsOff新建endtime小于starttime+300")#需求更改，此case现实不存在，更改时间范围
    @pytest.mark.full
    def test_caseid_1988249(self): 
        self.del_SOAAPP_db()
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        sleep(5)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-120, "endTime": nowtime+240, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) 
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) 
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #回复成功
        logger.info(f"通知的开始时间应该为{nowtime-120}和结束时间{nowtime+240}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86280,"endTime":nowtime+86640,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait,不限制时间

    @allure.title("通知预约充电信息kBookStsWait_noconnect→压测修改时间")
    @pytest.mark.full
    def test_caseid_1988719(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #避免与当前时间相差不足5min
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #回复成功
        self.partner.empty_all(1)
        for starttime1 in [120,60,180,240]:
            for endtime1 in [360,720,1200]:
                logger.info(f"通知的开始时间应该为{nowtime+starttime1}和结束时间{nowtime+endtime1}")
                self.partner.empty_all()
                self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                                {"cmd": {"type": 2, "source": 0, "timeInfo": {"startTime": nowtime+starttime1, "endTime": nowtime+endtime1, 
                                                        "repeatType": 1},"isToTargetSOCStop": False}}) #取消后新建
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #回复取消
                sleep(0.5)
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #回复成功
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+240,"endTime":nowtime+1200,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(2)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+240,"endTime":nowtime+1200,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait

    @allure.title("通知预约充电信息kBookStsOff→kBookStsOff_修改时间")
    @pytest.mark.full
    def test_caseid_1988263(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+60, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #避免与当前时间相差不足5min
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #回复成功
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+180, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #避免与当前时间相差不足5min
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr03, "StopBookChrgnReq", 1, timeout=3) #取消预约充电
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 0, timeout=0.5) #设置预约充电信号
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #回复默认
        logger.info(f"通知的开始时间应该为{nowtime+180}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) 
        self.partner.empty_all(2)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 2, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+540, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #取消后新建
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #回复成功
        logger.info(f"通知的开始时间应该为{nowtime+120}和结束时间{nowtime+540}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+540,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) 

    @allure.title("通知预约充电显示信息→standby到cancel时type置0")
    @pytest.mark.sanity
    def test_caseid_1988988(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        DisplayStartTime1=DisplayStartTime(nowtime,120)
        DisplayEndTime1=DisplayEndTime(nowtime,420)
        logger.info(f"现在时间是{nowtime}并且显示开始时间为{DisplayStartTime1}=显示结束时间为{DisplayEndTime1}")
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #避免与当前时间相差不足5min
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) 
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(1)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":1,"startTime":{"kYear":DisplayStartTime1[0],"kMonth":DisplayStartTime1[1],
                                                                 "kDay":DisplayStartTime1[2],"kHour":DisplayStartTime1[3],"kMinute":DisplayStartTime1[4]},
                                           "endTime":{"kYear":DisplayEndTime1[0],"kMonth":DisplayEndTime1[1],
                                                      "kDay":DisplayEndTime1[2],"kHour":DisplayEndTime1[3],"kMinute":DisplayEndTime1[4]}}}) #显示时间

        logger.info(f"通知的开始时间应该为{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) 
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":6,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) 
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}},timeout=3)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetDisplayBookChargingInfo", {},
                                             {"out": {"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}})

    @allure.title("通知预约充电信息kBookStsCharging→取消预约充电")
    @pytest.mark.full
    def test_caseid_1988987(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        DisplayStartTime1=DisplayStartTime(nowtime,86280)
        DisplayEndTime1=DisplayEndTime(nowtime,86760)
        logger.info(f"现在时间是{nowtime}并且显示开始时间为{DisplayStartTime1}=显示结束时间为{DisplayEndTime1}")
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-120, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #避免与当前时间相差不足5min
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) 
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":1,"startTime":{"kYear":DisplayStartTime1[0],"kMonth":DisplayStartTime1[1],
                                                                 "kDay":DisplayStartTime1[2],"kHour":DisplayStartTime1[3],"kMinute":DisplayStartTime1[4]},
                                           "endTime":{"kYear":DisplayEndTime1[0],"kMonth":DisplayEndTime1[1],
                                                      "kDay":DisplayEndTime1[2],"kHour":DisplayEndTime1[3],"kMinute":DisplayEndTime1[4]}}}) #显示时间
        logger.info(f"通知的开始时间应该为{nowtime+86280}和结束时间{nowtime+86760}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86280,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) 
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)#AC充电
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) 
        sleep(1)
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=0.5) #设置预约充电信号
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr03, "StopBookChrgnReq", 0,timeout=0.5)#当前内不回取消预约充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":nowtime+86280,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=360) 
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 1)#停止充电
        sleep(1)
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 0, timeout=0.5) #设置预约充电信号
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}},timeout=3)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetDisplayBookChargingInfo", {},
                                             {"out": {"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}})

    @allure.title("通知预约充电显示信息→charging到Deactive时type置0")
    @pytest.mark.sanity
    def test_caseid_1988989(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        DisplayStartTime1=DisplayStartTime(nowtime,86280)
        DisplayEndTime1=DisplayEndTime(nowtime,86820)
        logger.info(f"现在时间是{nowtime}并且显示开始时间为{DisplayStartTime1}=显示结束时间为{DisplayEndTime1}")
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #避免与当前时间相差不足5min
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) 
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(1)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":1,"startTime":{"kYear":DisplayStartTime1[0],"kMonth":DisplayStartTime1[1],
                                                                 "kDay":DisplayStartTime1[2],"kHour":DisplayStartTime1[3],"kMinute":DisplayStartTime1[4]},
                                           "endTime":{"kYear":DisplayEndTime1[0],"kMonth":DisplayEndTime1[1],
                                                      "kDay":DisplayEndTime1[2],"kHour":DisplayEndTime1[3],"kMinute":DisplayEndTime1[4]}}}) #显示时间

        logger.info(f"通知的开始时间应该为{nowtime+86280}和结束时间{nowtime+86820}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86280,"endTime":nowtime+86820,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) 
        sleep(30)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":5,
                                                                    "info":{"startTime":nowtime+86280,"endTime":nowtime+86820,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) 
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}},timeout=3)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetDisplayBookChargingInfo", {},
                                             {"out": {"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}})

    @allure.title("通知预约充电显示信息_AlreadyCharging时type置0")
    @pytest.mark.full
    def test_caseid_1988990(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        DisplayStartTime1=DisplayStartTime(nowtime,120)
        DisplayEndTime1=DisplayEndTime(nowtime,420)
        logger.info(f"现在时间是{nowtime}并且显示开始时间为{DisplayStartTime1}=显示结束时间为{DisplayEndTime1}")
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #避免与当前时间相差不足5min
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1)  
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":1,"startTime":{"kYear":DisplayStartTime1[0],"kMonth":DisplayStartTime1[1],
                                                                 "kDay":DisplayStartTime1[2],"kHour":DisplayStartTime1[3],"kMinute":DisplayStartTime1[4]},
                                           "endTime":{"kYear":DisplayEndTime1[0],"kMonth":DisplayEndTime1[1],
                                                      "kDay":DisplayEndTime1[2],"kHour":DisplayEndTime1[3],"kMinute":DisplayEndTime1[4]}}}) #显示时间
        logger.info(f"通知的开始时间应该为{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) 
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)#AC充电开始
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":5,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) 
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}},timeout=3)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetDisplayBookChargingInfo", {},
                                             {"out": {"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}})

    @allure.title("通知预约充电信息kBookStsWait_AlreadyCharging→kBookStsWait")
    @pytest.mark.full
    def test_caseid_1988268(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)#AC充电中
        sleep(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+180, "endTime": nowtime+540, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #避免与当前时间相差不足5min
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 0, timeout=0.5) #设置预约充电信号
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 3) #回复失败
        logger.info(f"通知的开始时间应该为{nowtime+180}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":1,
                                                                    "info":{"startTime":nowtime+180,"endTime":nowtime+540,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入失效 
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 1)#AC充电结束
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #回复默认
        self.partner.ck_no_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo")
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) #拔枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=3) #设置预约充电信号
        sleep(1)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+180,"endTime":nowtime+540,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入等待

    @allure.title("通知预约充电信息kBookStsWait_AlreadyCharging→kBookStsWait_noconnect_拔枪")
    @pytest.mark.full
    def test_caseid_1988278(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)#AC充电中
        sleep(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #避免与当前时间相差不足5min
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 0, timeout=0.5) #设置预约充电信号
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 3) #回复失败
        logger.info(f"通知的开始时间应该为{nowtime+180}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":1,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入失效 
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 1)#AC充电结束
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #回复默认
        self.partner.ck_no_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo")
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) #拔枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=3) #设置预约充电信号
        sleep(1)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入等待

    @allure.title("通知预约充电信息kBookStsWait_AlreadyCharging→kBookStsWait_AlreadyCharging")
    @pytest.mark.full
    def test_caseid_1988508(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)#AC充电中
        sleep(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+60, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #避免与当前时间相差不足5min
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 3) #回复失败
        logger.info(f"通知的开始时间应该为{nowtime+180}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":1,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入失效 
        self.partner.empty_all(2)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 2, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #避免与当前时间相差不足5min
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 0, timeout=0.5) #设置预约充电信号
        sleep(1)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":1,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入等待

    @allure.title("通知预约充电信息kBookStsWait_AlreadyCharging→kBookStsCanceled")
    @pytest.mark.full
    def test_caseid_1988272(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)#AC充电中
        sleep(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #避免与当前时间相差不足5min
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 0, timeout=0.5) #设置预约充电信号
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 3) #回复失败
        logger.info(f"通知的开始时间应该为{nowtime+180}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":1,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入失效 
        self.partner.empty_all(2)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #避免与当前时间相差不足5min
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr03, "StopBookChrgnReq", 1, timeout=3) #取消预约充电
        sleep(1)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入等待
        
    @allure.title("通知预约充电信息kBookStsWait_AlreadyCharging持久化")
    @pytest.mark.sanity
    def test_caseid_1988279(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)#AC充电中
        sleep(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #避免与当前时间相差不足5min
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 0, timeout=0.5) #设置预约充电信号
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 3) #回复失败
        logger.info(f"通知的开始时间应该为{nowtime+180}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":1,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入失效 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #回到默认
        sleep(1)#数据库延时
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":1,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=10) #进入ALREDY
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":2,"workSts":1,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3)
        
    @allure.title("通知预约充电信息kBookStsOff持久化")
    @pytest.mark.full
    def test_caseid_1988281(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入sts_off 
        sleep(1)#数据库延时
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=7) #进入sts_off 
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3)

    @allure.title("通知预约充电信息kBookStsOff→kBookStsWait_noconnect到standby_开始时间在现在结束时间在明天")
    @pytest.mark.full
    def test_caseid_1988571(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+240, "endTime": nowtime+86580, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #设置预约充电信号
        logger.info(f"通知的开始时间{nowtime+240}和结束时间{nowtime+86580}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+240,"endTime":nowtime+86580,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #回复
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+240,"endTime":nowtime+86580,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging
        
    @allure.title("通知预约充电信息kBookStsWait_noconnect→kBookStsCanceled→kBookStsOff")
    @pytest.mark.full
    def test_caseid_1988283(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #回复
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr03, "StopBookChrgnReq", 1, timeout=3) #取消预约充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":6,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},) #进入cancel
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},) #进入sts_off 
           
    @allure.title("通知预约充电信息_更新时间校验不下发cancel信号")
    @pytest.mark.full
    def test_caseid_1988986(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #回复
        sleep(3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #回复
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 2, "source": 0, "timeInfo": {"startTime": nowtime+180, "endTime": nowtime+540, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #回复成功
        sleep(1)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+180,"endTime":nowtime+540,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},) #进入wait
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(1)
        self.bgm_eth_inter.ck_signal_values("StopBookChrgnReq", [])
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=0.5) #设置预约充电信号


    @allure.title("通知预约充电信息kBookStsWait_noconnect→kBookStsWait_noconnect")
    @pytest.mark.full
    def test_caseid_1988286(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #回复
        sleep(3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #回复
        sleep(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 2, "source": 0, "timeInfo": {"startTime": nowtime+180, "endTime": nowtime+540, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #回复成功
        sleep(1)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+180,"endTime":nowtime+540,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},) #进入wait
        
    @allure.title("通知预约充电信息kBookStsWait_noconnect→kBookStsWait_noconnect过时后插枪")
    @pytest.mark.full
    def test_caseid_1988708(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+60, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=2) #设置预约充电信号，需要状态机判断延时正常
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #回复
        sleep(420)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+86460,"endTime":nowtime+86820,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby 明天

    @allure.title("通知预约充电信息_明天的kBookStsWait_noconnect过时后插枪")
    @pytest.mark.full
    def test_caseid_1988837(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-120, "endTime": nowtime+240, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号，需要状态机判断延时正常
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime+86280}和结束时间{nowtime+86640}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86280,"endTime":nowtime+86640,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(420)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+86280,"endTime":nowtime+86640,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait

    @allure.title("通知预约充电信息kBookStsWait_noconnect→kBookStsStandby")
    @pytest.mark.full
    def test_caseid_1988287(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(2)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},) #进入stdanby

    @allure.title("通知预约充电信息kBookStsWait_noconnect→插入交流枪非1/2/3时不影响状态机") #1024新需求
    @pytest.mark.full
    def test_caseid_1989182(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(2)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+240, "endTime": nowtime+600, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+240,"endTime":nowtime+600,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.empty_all()
        for sts in [1,2,3]:
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', sts) 
            sleep(1)
            self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+240,"endTime":nowtime+600,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) 
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
            sleep(1)
        self.partner.empty_all()
        for sts2 in range(4,14):
            logger.info(f"发送枪状态{sts2}")
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', sts2) 
            sleep(1)
            self.partner.ck_no_event_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",
                                    {"out":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+240,"endTime":nowtime+600,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
            self.partner.ck_no_event_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                             {"out": {"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}})

    @allure.title("通知预约充电信息kBookStsWait_noconnect→插入放电枪不影响状态机")
    @pytest.mark.full
    def test_caseid_1988968(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(2)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 7) 
        self.partner.ck_no_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo")
        self.partner.ck_no_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo")
        self.partner.empty_all(1)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                    {"out":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 5) 
        self.partner.ck_no_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo")
        self.partner.ck_no_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo")
        self.partner.empty_all(1)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                    {"out":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.empty_all(1)
        self.partner.ck_no_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",timeout=120)
        self.partner.ck_no_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",timeout=120)
        
    @allure.title("通知预约充电信息kBookStsWait_noconnect→kBookStsCharging")
    @pytest.mark.full
    def test_caseid_1988288(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime-60}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86820,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #请求充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈成功
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86820,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},) #进入charging
        self.partner.empty_all(2)
        self.partner.ck_no_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo")

    @allure.title("通知预约充电信息kBookStsWait_noconnect持久化")
    @pytest.mark.full
    def test_caseid_1988289(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime-60}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86820,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86820,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86820,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3)
        
    @allure.title("通知预约充电信息kBookStsStandby→kBookStsWait")
    @pytest.mark.full
    def test_caseid_1988291(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(1)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) #拔枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        
    @allure.title("通知预约充电信息kBookStsStandby→kBookStsCanceled→kBookStsOff")
    @pytest.mark.full
    def test_caseid_1988292(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(1)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+180, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr03, "StopBookChrgnReq", 1, timeout=3) #取消预约充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":6,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入cancel，取消时时间保持跟上次打开的一样，仿照闹钟规则
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入off
        
    @allure.title("通知预约充电信息kBookStsStandby→kBookStsCharging")
    @pytest.mark.sanity
    def test_caseid_1988293(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(1)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.partner.empty_all(1)
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=120) #时间到点请求充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间不更新
        
    @allure.title("通知预约充电信息kBookStsStandby→中途重启再到kBookStsCharging")
    @pytest.mark.sanity
    def test_caseid_1988513(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+300, "endTime": nowtime+660, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #3min以内闹钟不会更新成功，所以加大开始时间
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime+300}和结束时间{nowtime+660}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+300,"endTime":nowtime+660,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(1)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+300,"endTime":nowtime+660,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.partner.empty_all(1)
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=310) #时间到点请求充电 #3min内的计时器在重启后不生效，所以采取订阅闹钟
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈 成功
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+300,"endTime":nowtime+660,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间不更新
        
    @allure.title("通知预约充电信息kBookStsCharging→kBookStsWait_noconnect")
    @pytest.mark.sanity
    def test_caseid_1988319(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime+86340}和结束时间{nowtime+86760}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间更新
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) #插枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间更新
        
    @allure.title("通知预约充电信息kBookStsCharging→kBookStsCharging调用cancel")
    @pytest.mark.full
    def test_caseid_1988330(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime+86340}和结束时间{nowtime+86760}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #时间到点请求充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间更新
        self.partner.empty_all(4)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)
        sleep(1)
        self.partner.ck_no_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo")
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":6,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入cancel但是等待finsh后补发信号
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 1)
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr03, "StopBookChrgnReq", 1,timeout=3)#取消预约充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入sts_off


    @allure.title("通知预约充电信息kBookStsCharging→kBookStsFailed_Deactive持久化")
    @pytest.mark.full
    def test_caseid_1988687(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime+86340}和结束时间{nowtime+86760}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #时间到点请求充电 
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间更新
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', random.choice([0,2,3])) #请求充电反馈非成功
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":5,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=31) #进入fail_deactive后时间已到推到明天
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":5,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=10) #进入fail_deactive后时间已到推到明天

    @allure.title("通知预约充电信息kBookStsCharging→kBookStsFailed_Deactive通过信号反馈失败")
    @pytest.mark.full
    def test_caseid_1988535(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime+86340}和结束时间{nowtime+86760}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #时间到点请求充电 #有时候丢帧捕获不到
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间更新
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', random.choice([0,2,3])) #请求充电反馈非成功
        self.partner.empty_all(25)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":5,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=6) #有一个30S判断，进入fail_deactive后时间已到推到明天
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) #拔枪
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait后时间已到推到明天

    @allure.title("通知预约充电信息kBookStsCharging→kBookStsFailed_Deactive通过信号反馈失败")
    @pytest.mark.full
    def test_caseid_1989647(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime+86340}和结束时间{nowtime+86760}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #时间到点请求充电 #有时候丢帧捕获不到
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间更新
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', random.choice([0,2,3])) #请求充电反馈非成功
        self.partner.empty_all(25)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":5,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=6) #有一个30S判断，进入fail_deactive后时间已到推到明天
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 2, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse',1) #请求预约充电回馈状态
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) #拔枪
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait后时间已到推到明天
        
    @allure.title("通知预约充电信息kBookStsCharging→kBookStsFailed_Deactive通过立即充电")
    @pytest.mark.full
    def test_caseid_1988534(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime+86340}和结束时间{nowtime+86760}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #时间到点请求充电 #有时候丢帧捕获不到
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间更新
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetChargingControl", {"cmd":{"type":1,"source":0}})
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":5,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入fail_deactive后时间已到推到明天
        
    @allure.title("通知预约充电信息_插直流枪不能进入到预约充电")
    @pytest.mark.full
    def test_caseid_1988554(self): 
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+86340}和结束时间{nowtime+86760}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1) #插直流
        self.partner.ck_no_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo")
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0) #插直流
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插交流
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #时间到点请求充电 #有时候丢帧捕获不到
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间更新

    @allure.title("通知预约充电信息_枪类型跳为直流枪_但是plugger非1/2/3时不上报") #1024新需求
    @pytest.mark.full
    def test_caseid_1989181(self): 
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+360}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.set_BookChargingTime_Bluetooth(24, 60, 24, 60)
        self.set_BookChargingTime_Remote(10, 10, 15, 10)
        self.partner.empty_all(2)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetDisplayBookChargingInfo", {},
                                             {"out": {"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}})
        self.partner.empty_all(1)
        for sts in [0,4,5]:
            logger.info(f"发送枪连接状态为{sts}")
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', sts) #插直流
            sleep(1)
            self.partner.ck_no_event_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                             {"out": {"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}})

    @allure.title("通知预约充电信息_枪类型跳为直流枪_拔枪")
    @pytest.mark.full
    def test_caseid_1988570(self): 
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1, timeout=3) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0, timeout=3) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+360}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.set_BookChargingTime_Bluetooth(24, 60, 24, 60)
        self.set_BookChargingTime_Remote(10, 10, 15, 10)
        self.partner.empty_all(2)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetDisplayBookChargingInfo", {},
                                             {"out": {"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1) #插直流
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr32, 'ChrgPilBookChrgn', 1) 
        self.partner.ck_no_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":2,"startTime":{"kHour":10,"kMinute":10}, "endTime":{"kHour":15,"kMinute":10}}},timeout=3)
        self.set_BookChargingTime_Remote(11, 22, 11, 22)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":2,"startTime":{"kHour":11,"kMinute":22}, "endTime":{"kHour":11,"kMinute":22}}},timeout=3)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0) #插直流
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr32, 'ChrgPilBookChrgn', 0) 
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}},timeout=3)
        self.partner.empty_all(1)
        self.set_BookChargingTime_Bluetooth(23, 59, 12, 0)
        self.set_BookChargingTime_Remote(24, 60, 24, 60)
        self.partner.empty_all(1)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetDisplayBookChargingInfo", {},
                                             {"out": {"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', random.choice([2, 3])) #随机插直流
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr32, 'ChrgPilBookChrgn', 1) 
        self.partner.ck_no_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":2,"startTime":{"kHour":23,"kMinute":59}, "endTime":{"kHour":12,"kMinute":0}}},timeout=3)
        self.partner.empty_all(1)
        self.set_BookChargingTime_Bluetooth(11, 22, 11, 22)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":2,"startTime":{"kHour":11,"kMinute":22}, "endTime":{"kHour":11,"kMinute":22}}},timeout=3)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0) #插直流
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}},timeout=3)
        
    @allure.title("通知预约充电信息kBookStsFinish→kBookStsCanceled")
    @pytest.mark.full
    def test_caseid_1988346(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+86340}和结束时间{nowtime+86760}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(1)#每个case都重复校验，加上本来事件帧就不容易获取到，这里取消校验请求充电，一个case校验一个请求充电就行
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间更新
        self.partner.empty_all(2)
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookStopTiAchieved", 1,timeout=360) #停止充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 3) #预约充电完成
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":7,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入finsh
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":6,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入finsh
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入finsh

    @allure.title("通知预约充电信息kBookStsCharging→kBookStsFinish_endtime到时情况1")
    @pytest.mark.full
    def test_caseid_1988334(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+86340}和结束时间{nowtime+86760}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #时间到点请求充电 #有时候丢帧捕获不到
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间更新
        self.partner.empty_all(2)
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookStopTiAchieved", 1,timeout=360) #停止充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 3) #预约充电完成
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":7,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入finsh

    @allure.title("通知预约充电信息_目标SOC和时间的优先级")
    @pytest.mark.full
    def test_caseid_1988366(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 50.0)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 100.0)
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": True}}) #先打开
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入wait
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        logger.info(f"通知的开始时间{nowtime+86340}和结束时间0")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86340,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入charging后时间更新
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 1)  
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 3) #预约充电完成
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":7,
                                                                    "info":{"startTime":nowtime+86340,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入finsh
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(2)
        self.bgm_eth_inter.ck_signal_values("BookChrgnActvdReq", [1,1,1,1,1,0]) #新需求
        self.bgm_eth_inter.ck_signal_values("BookStopTiAchieved", [1,1,1,1,1,0])#新需求

    @allure.title("通知预约充电信息_目标SOC未满但是endtime到了的情况")
    @pytest.mark.full
    def test_caseid_1988368(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 50.0)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 100.0)
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": True}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=1) #时间到点请求充电 #有时候丢帧捕获不到
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        logger.info(f"通知的开始时间{nowtime+86340}和结束时间0")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86340,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入charging后时间更新
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookStopTiAchieved", 1,timeout=360) #停止充电
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 3) #预约充电完成
            self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":7,
                                                                        "info":{"startTime":nowtime+86340,"endTime":0,"repeatType":1},
                                                                        "isToTargetSOCStop":True}}}) #进入finsh
        except Exception:
            assert True
        else:
            assert False
        self.bgm_eth_inter.start_bgm_tcpdump()#采用tcpdump拿到停止充电的
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 3) #预约充电完成
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":7,
                                                                    "info":{"startTime":nowtime+86340,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入finsh
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(2)
        self.bgm_eth_inter.ck_signal_values("BookStopTiAchieved", [1,1,1,1,1,0])
        
    @allure.title("通知预约充电信息kBookStsCharging→kBookStsFinish_endtime到时情况2")
    @pytest.mark.full
    def test_caseid_1988335(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=3) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=120) #时间到点请求充电 #有时候丢帧捕获不到
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间更新
        self.partner.empty_all(2)
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookStopTiAchieved", 1,timeout=420) #停止充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 3) #预约充电完成
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":7,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入finsh
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 1)
        self.partner.ck_no_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo")

    @allure.title("通知预约充电信息kBookStsFinish→kBookStsCharging")
    @pytest.mark.full
    def test_caseid_1988349(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #设置预约充电信号
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #时间到点请求充电 #有时候丢帧捕获不到
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间更新
        self.partner.empty_all(2)
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookStopTiAchieved", 1,timeout=360) #停止充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 3) #预约充电完成
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":7,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入finsh

    @allure.title("通知预约充电显示信息_entime为充到目标SOC的表现")
    @pytest.mark.smoke
    def test_caseid_1988569(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 50.0)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 100.0)
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        DisplayStartTime1=DisplayStartTime(nowtime,86340)
        DisplayEndTime1=DisplayEndTime(nowtime,86760)
        logger.info(f"现在时间是{nowtime}并且显示开始时间为{DisplayStartTime1}=显示结束时间为{DisplayEndTime1}")
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": True}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=3) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #时间到点请求充电 #有时候丢帧捕获不到
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        logger.info(f"通知的开始时间{nowtime+86340}和结束时间0")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86340,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入charging后时间更新
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":1,"startTime":{"kYear":DisplayStartTime1[0],"kMonth":DisplayStartTime1[1],
                                                                 "kDay":DisplayStartTime1[2],"kHour":DisplayStartTime1[3],"kMinute":DisplayStartTime1[4]},
                                           "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}}) #显示时间
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 1)  
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookStopTiAchieved", 1,timeout=3) #停止充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 3) #预约充电完成
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":7,
                                                                    "info":{"startTime":nowtime+86340,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入finsh
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":1,"startTime":{"kYear":DisplayStartTime1[0],"kMonth":DisplayStartTime1[1],
                                                                 "kDay":DisplayStartTime1[2],"kHour":DisplayStartTime1[3],"kMinute":DisplayStartTime1[4]},
                                           "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}}) #显示时间
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) #插枪
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}},timeout=3)

    @allure.title("通知预约充电信息kBookStsFinish持久化")
    @pytest.mark.full
    def test_caseid_1988348(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+60, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=65) #时间到点请求充电 #有时候丢帧捕获不到
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        logger.info(f"通知的开始时间{nowtime+60}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间更新
        self.partner.empty_all(2)
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookStopTiAchieved", 1,timeout=420) #停止充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 3) #预约充电完成
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":7,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入finsh
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":7,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=10) #进入finsh

    @allure.title("通知预约充电信息kBookStsFinish→kBookStsWait_noconnect")
    @pytest.mark.full
    def test_caseid_1988347(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+60, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电

        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=65) #时间到点请求充电 #有时候丢帧捕获不到
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        logger.info(f"通知的开始时间{nowtime+60}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间更新
        self.partner.empty_all(2)
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookStopTiAchieved", 1,timeout=420) #停止充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 3) #预约充电完成
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":7,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入finsh
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 1)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) #插枪
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86460,"endTime":nowtime+86820,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入finsh
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #设置预约充电信号

    @allure.title("通知预约充电显示信息→交流枪下stabndby到standby")
    @pytest.mark.sanity
    def test_caseid_1988562(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        DisplayStartTime1=DisplayStartTime(nowtime,120)
        DisplayEndTime1=DisplayEndTime(nowtime,480)
        logger.info(f"现在时间是{nowtime}并且显示开始时间为{DisplayStartTime1}=显示结束时间为{DisplayEndTime1}")
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.ck_no_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo") #无显示信息
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        logger.info(f"通知的开始时间{nowtime+60}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间更新
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":1,"startTime":{"kYear":DisplayStartTime1[0],"kMonth":DisplayStartTime1[1],
                                                                 "kDay":DisplayStartTime1[2],"kHour":DisplayStartTime1[3],"kMinute":DisplayStartTime1[4]},
                                           "endTime":{"kYear":DisplayEndTime1[0],"kMonth":DisplayEndTime1[1],
                                                      "kDay":DisplayEndTime1[2],"kHour":DisplayEndTime1[3],"kMinute":DisplayEndTime1[4]}}}) #显示时间
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        sleep(1)
        DisplayStartTime2=DisplayStartTime(nowtime,120)
        DisplayEndTime2=DisplayEndTime(nowtime,540)
        logger.info(f"更新后的时间是{nowtime}并且显示开始时间为{DisplayStartTime2}=显示结束时间为{DisplayEndTime2}")
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 2, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+540, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":1,"startTime":{"kYear":DisplayStartTime2[0],"kMonth":DisplayStartTime2[1],
                                                                 "kDay":DisplayStartTime2[2],"kHour":DisplayStartTime2[3],"kMinute":DisplayStartTime2[4]},
                                           "endTime":{"kYear":DisplayEndTime1[0],"kMonth":DisplayEndTime1[1],
                                                "kDay":DisplayEndTime2[2],"kHour":DisplayEndTime2[3],"kMinute":DisplayEndTime2[4]}}}) #显示时间
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetDisplayBookChargingInfo", {},
                                             {"out": {"type":1,"startTime":{"kYear":DisplayStartTime2[0],"kMonth":DisplayStartTime2[1],
                                                                 "kDay":DisplayStartTime2[2],"kHour":DisplayStartTime2[3],"kMinute":DisplayStartTime2[4]},
                                           "endTime":{"kYear":DisplayEndTime1[0],"kMonth":DisplayEndTime1[1],
                                                "kDay":DisplayEndTime2[2],"kHour":DisplayEndTime2[3],"kMinute":DisplayEndTime2[4]}}}) #显示时间

    @allure.title("通知预约充电显示信息→交流枪下wait到standby到charging到finish到wait")
    @pytest.mark.sanity
    def test_caseid_1988551(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        DisplayStartTime1=DisplayStartTime(nowtime,60)
        DisplayEndTime1=DisplayEndTime(nowtime,420)
        logger.info(f"现在时间是{nowtime}并且显示开始时间为{DisplayStartTime1}=显示结束时间为{DisplayEndTime1}")
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+60, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.ck_no_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo") #无显示信息
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=65) #时间到点请求充电 #有时候丢帧捕获不到
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        logger.info(f"通知的开始时间{nowtime+60}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging后时间更新
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":1,"startTime":{"kYear":DisplayStartTime1[0],"kMonth":DisplayStartTime1[1],
                                                                 "kDay":DisplayStartTime1[2],"kHour":DisplayStartTime1[3],"kMinute":DisplayStartTime1[4]},
                                           "endTime":{"kYear":DisplayEndTime1[0],"kMonth":DisplayEndTime1[1],
                                                      "kDay":DisplayEndTime1[2],"kHour":DisplayEndTime1[3],"kMinute":DisplayEndTime1[4]}}}) #显示时间
        self.partner.empty_all(2)
        sleep(8)
        self.partner.ck_no_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo")#防止闹钟紊乱
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookStopTiAchieved", 1,timeout=420) #停止充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 3) #预约充电完成
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":7,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入finsh
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":1,"startTime":{"kYear":DisplayStartTime1[0],"kMonth":DisplayStartTime1[1],
                                                                 "kDay":DisplayStartTime1[2],"kHour":DisplayStartTime1[3],"kMinute":DisplayStartTime1[4]},
                                           "endTime":{"kYear":DisplayEndTime1[0],"kMonth":DisplayEndTime1[1],
                                                      "kDay":DisplayEndTime1[2],"kHour":DisplayEndTime1[3],"kMinute":DisplayEndTime1[4]}}}) #显示时间
        self.partner.empty_all(1)
        DisplayStartTime2=DisplayStartTime(nowtime,86460)
        DisplayEndTime2=DisplayEndTime(nowtime,86820)
        logger.info(f"拔枪后的时显示开始时间为{DisplayStartTime2}=显示结束时间为{DisplayEndTime2}")
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) #插枪
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86460,"endTime":nowtime+86820,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入finsh
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}},timeout=3)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetDisplayBookChargingInfo", {},
                                             {"out": {"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}},timeout=3)

    @allure.title("通知预约充电信息kBookStsCharging_持久化")
    @pytest.mark.full
    def test_caseid_1988338(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+60, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电

        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=65) #时间到点请求充电 #有时候丢帧捕获不到
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        logger.info(f"通知的开始时间{nowtime+60}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) 
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈回默认值
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT) #理论上charging不重启
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=15) #时间同步后进入charging
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈成功
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)#时间同步后继续进入charging
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈回到默认值
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈成功
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookStopTiAchieved", 1,timeout=420) #停止充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":7,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 3) #请求充电反馈finish

    @allure.title("通知预约充电信息_source和repeat遍历")
    @pytest.mark.full
    def test_caseid_1988373(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        for source in range(6):
            for repeattype in range(3):
                self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                                {"cmd": {"type": 0, "source": source, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                        "repeatType": repeattype},"isToTargetSOCStop": False}}) #先取消
                self.partner.empty_all(1)
                self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                                {"cmd": {"type": 1, "source": source, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": repeattype},"isToTargetSOCStop": False}}) #先打开
                self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":source,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":repeattype},
                                                                    "isToTargetSOCStop":False}}}) #进入wait

    @allure.title("通知预约充电信息_重启后第一次设置预约充电")
    @pytest.mark.full
    def test_caseid_1989683(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=15)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": True}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #没插枪时不用设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86280,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入wait
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #请求充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                "info":{"startTime":nowtime+86280,"endTime":0,"repeatType":1},
                                                                "isToTargetSOCStop":True}}}) #进入wait
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)
        self.partner.empty_all(1)

    @allure.title("通知预约充电信息_预约充电中取消再新建上报最新的event&下次拔枪执行最新的动作")
    @pytest.mark.full
    def test_caseid_1989684(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": True}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86280,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入wait
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #请求充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86280,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入wait
        sleep(2)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)
        sleep(3)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime-120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": True}}) #先打开
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) 
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":6,
                                                                    "info":{"startTime":nowtime+86280,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入wait
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        sleep(3) #再新建
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) 
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 3) #充电结束
        sleep(3)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) #充电结束
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) #拔枪
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        sleep(2)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(10)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo",{},{"out":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=120) #请求充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)

    @allure.title("通知预约充电信息_预约充电中modify上报最新的event&下次拔枪执行最新的动作")
    @pytest.mark.full
    def test_caseid_1989685(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": True}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86280,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入wait
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #请求充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86280,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入wait
        sleep(2)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)
        sleep(3)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 2, "source": 0, "timeInfo": {"startTime": nowtime+180, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) 
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) 
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+180,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 3) #充电结束
        sleep(3)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) #充电结束
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) #拔枪
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        sleep(2)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+180,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(10)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo",{},{"out":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+180,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=180) #请求充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+180,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)

    @allure.title("通知预约充电信息charging状态_充满为止连续插拔枪5次")
    @pytest.mark.full
    def test_caseid_1989680(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": True}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86280,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入wait
        for plugger in range(5):
            logger.info(f"第{plugger}次压测")
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
            sleep(1)
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
            sleep(1)
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #请求充电
            self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86280,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入wait
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
            sleep(3)

    @allure.title("通知预约充电信息charging状态_有效时间连续插拔枪5次")
    @pytest.mark.full
    def test_caseid_1989681(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86280,"endTime":nowtime+86820,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        for plugger in range(5):
            logger.info(f"第{plugger}次压测")
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
            sleep(1)
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
            self.partner.empty_all(1)
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #请求充电
            self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86280,"endTime":nowtime+86820,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
            sleep(3)

    @allure.title("通知预约充电信息charging状态_starttime到点后有效时间连续插拔枪2次")
    @pytest.mark.full
    def test_caseid_1989682(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.partner.empty_all(4)
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=120) #请求充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        sleep(10)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        sleep(5)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=4) #请求充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈

    @allure.title("通知预约充电信息standby状态连续插拔枪10次")
    @pytest.mark.full
    def test_caseid_1989602(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": True}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入wait
        for plugger in range(10):
            logger.info(f"第{plugger}次压测")
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
            sleep(1)
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
            sleep(1)
            self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入wait
        self.partner.empty_all(2)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo",{},{"out":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入standby
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=120) #请求充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2) #假设在充电
        sleep(1)

    @allure.title("通知预约充电信息kBookStsStandby中修改到充电中")
    @pytest.mark.full
    def test_caseid_1989601(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+60, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": True}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+60,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入wait
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        sleep(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 2, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #请求充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2) #假设在充电
        sleep(1)

    @allure.title("通知预约充电信息kBookStsStandby中修改结束时间为充满为止")
    @pytest.mark.full
    def test_caseid_1989600(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+60, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": True}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+60,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入wait
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        sleep(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 2, "source": 0, "timeInfo": {"startTime": nowtime+60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+360,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=63) #请求充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)#AC充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+360,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}})
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookStopTiAchieved", 1,timeout=305) #停止充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":7,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+360,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}})

    @allure.title("通知预约充电信息kBookStsStandby中修改结束时间为充满为止")
    @pytest.mark.full
    def test_caseid_1989597(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+420}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #插枪时设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        sleep(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 2, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": True}}) #先打开
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入standby
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=125) #请求充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)#AC充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+120,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}})
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookStopTiAchieved", 1,timeout=305) #停止充电
        except Exception:
            assert True
        else:
            assert False
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 3)#AC充电
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":7,
                                                                    "info":{"startTime":nowtime+120,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}},timeout=2) #进入finsh

    @allure.title("通知预约充电信息kBookStsStandby→kBookStsStandby")
    @pytest.mark.full
    def test_caseid_1988372(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+360}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #插枪时设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        sleep(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 2, "source": 0, "timeInfo": {"startTime": nowtime+180, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+180,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=180) #请求充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+180,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2) #假设在充电
        sleep(1)

    @allure.title("通知预约充电信息kBookStsStandby→kBookStsFailed_Deactive情况1")
    @pytest.mark.full
    def test_caseid_1988294(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #插枪时设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.partner.empty_all(1)
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+480}")
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetChargingControl", {"cmd":{"type":1,"source":0}})
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":5,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入fail_deactive后时间未到不推迟      
        
    @allure.title("通知预约充电信息kBookStsFailed_Deactive→kBookStsWait_noconnect")
    @pytest.mark.full
    def test_caseid_1988341(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #插枪时设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.partner.empty_all(1)
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+480}")
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetChargingControl", {"cmd":{"type":1,"source":0}})
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":5,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入fail_deactive后时间未到不推迟
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 1)
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) #拔枪
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=3) #预约充电信号
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait后时间未到不推迟

    @allure.title("通知预约充电信息kBookStsFailed_Deactive→kBookStsCanceled")
    @pytest.mark.full
    def test_caseid_1988345(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #插枪时设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.partner.empty_all(1)
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+480}")
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetChargingControl", {"cmd":{"type":1,"source":0}})
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":5,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入fail_deactive后时间未到不推迟
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+240, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #修改时间
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr03, "StopBookChrgnReq", 1,timeout=1)#取消预约充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":6,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) 
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) 

    @allure.title("通知预约充电信息kBookStsFailed_Deactive→kBookStsWait_noconnect_修改时间后拔枪")
    @pytest.mark.full
    def test_caseid_1988343(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #插枪时设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.partner.empty_all(1)
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+480}")
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetChargingControl", {"cmd":{"type":1,"source":0}})
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":5,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入fail_deactive后时间未到不推迟
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 2, "source": 0, "timeInfo": {"startTime": nowtime+240, "endTime": nowtime+540, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #修改时间
        logger.info(f"通知的开始时间{nowtime+240}和结束时间{nowtime+540}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":1,
                                                                    "info":{"startTime":nowtime+240,"endTime":nowtime+540,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入fail_deactive后时间未到不推迟
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 1)
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) #拔枪
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+240,"endTime":nowtime+540,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait后时间未到不推迟

    @allure.title("通知预约充电信息kBookStsStandby持久化")
    @pytest.mark.full
    def test_caseid_1988301(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #插枪时设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=10) #进入standby
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3)

    @allure.title("通知预约充电信息kBookStsStandby→kBookStsFailed_Deactive情况2")
    @pytest.mark.full
    def test_caseid_1988509(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+360}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #插枪时设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.partner.empty_all(1)
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+360}")
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":5,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入fail_deactive后时间未到不推移
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=120) #请求充电
        except Exception:
            assert True
        else:
            assert False

    @allure.title("通知预约充电信息入参当前时间")
    @pytest.mark.full
    def test_caseid_1988824(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        nowtime2 = time.time()
        nowtime1 = int(nowtime2)
        logger.info("现在时间是:{}".format(nowtime1))
        now_zero_seconds = nowtime1-nowtime1 % 60
        logger.info("秒数归0时间是:{}".format(now_zero_seconds))
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime1+120, "endTime": nowtime1+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        logger.info(f"通知的开始时间{now_zero_seconds+120}和结束时间{now_zero_seconds+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":now_zero_seconds+120,"endTime":now_zero_seconds+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait

    @allure.title("通知预约充电信息kBookStsWait_noconnect→kBookStsFailed_deactive")
    @pytest.mark.full
    def test_caseid_1988507(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 3) #回复失败
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":2,"workSts":5,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=4) #进入fail_deactive

#========================================================================================================================================

@allure.feature("SOA服务接口")
@allure.story("架构基础/HighVoltageAppService")
class TestHighVoltageAppServiceFota_FOTA(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.sd_tester.write_single_ccp(973,2) #AC
        sleep(2)
        self.nucapp.bgm_power_off()
        sleep(3)
        self.nucapp.bgm_power_on()
        sleep(30)
        for process_name in ["monitor_em2.sh", "em2", "fota/fota", "service_monitor"]:
            res = command_send(
                device_name="BGM",
                cmd=f"ps -ef |grep app |grep {process_name} |grep -v grep",
                timeout=60,
            )[1]
            pid = res.split()[1]
            command_send(device_name="BGM", cmd=f"kill -9 {pid}")
        sleep(2)
        command_send(device_name="BGM", cmd='su - service_monitor -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;/app/bin/service_monitor  -c /app/etc/service_monitor.json &"', timeout=15)
        self.partner = S2sBaseClass([
            ("HighVoltageAppService", "client"),
            ("HighVoltageService", "client"),
            ("FotaMasterService", "server"),
            ("VehicleTimeService", "client"),
            ("VehicleSetStatusService", "client")])
        self.sd_tester.tester_present()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        self.nucapp.bgm_power_off()
        sleep(3)
        self.nucapp.bgm_power_on()
        sleep(10)
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=True)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetMaintenanceMode", {"isOn": False},timeout=3)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) #没有开始充电
        sleep(0.5)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":0, "errorCode":0}})
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0)   #交流枪 
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0) #直流枪
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 20.0) #电量20
 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.partner.empty_all(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1) #新增恢复时间同步
        try:
            self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        except Exception as err:
            self.nucapp.tcam_power_off()
            sleep(25)
            self.nucapp.bgm_power_off()
            sleep(2)
            self.nucapp.bgm_power_on()
            self.nucapp.tcam_power_on()
            self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
            self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=300)
        else:
            assert True
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消tcam的闹钟
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #请求预约充电回馈状态

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    @allure.title("通知预约充电信息kBookStsStandby→kBookStsStandby_OTA_开始时间到但是OTA中")
    @pytest.mark.full
    def test_caseid_1988297(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #插枪时设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.partner.empty_all(1)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":5, "errorCode":0}})
        sleep(3)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3)
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=120) #请求充电
        except Exception:
            assert True
        else:
            assert False
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3)

    @allure.title("通知预约充电信息kBookStsStandby→kBookStsStandby_OTA_开始时间未到但是中途OTA过")
    @pytest.mark.full
    def test_caseid_1988512(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #请求预约充电回馈状态
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #插枪时设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.partner.empty_all(1)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":5, "errorCode":0}})
        sleep(3)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":0, "errorCode":0}})
        sleep(1)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3)
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=120) #请求充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入charging
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2) #假设在充电
        sleep(1)
        
    @allure.title("通知预约充电信息kBookStsStandby_OTA中endtime过时")
    @pytest.mark.full
    def test_caseid_1988350(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+60, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电

        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(3)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":5, "errorCode":0}})
        sleep(3)
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=65) #时间到点请求充电 #有时候丢帧捕获不到
        except Exception:
            assert True
        else:
            assert False
        self.partner.empty_all(2)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":7,
                                                                    "info":{"startTime":nowtime+60,"endTime":nowtime+420,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=360) #进入finsh

    @allure.title("通知预约充电显示信息_kBookStsStandby_到OTA到充电结束到拔枪")
    @pytest.mark.full
    def test_caseid_1988568(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        DisplayStartTime1=DisplayStartTime(nowtime,120)
        DisplayEndTime1=DisplayEndTime(nowtime,480)
        logger.info(f"现在时间是{nowtime}并且显示开始时间为{DisplayStartTime1}=显示结束时间为{DisplayEndTime1}")
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #请求预约充电回馈状态
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+360}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #插枪时设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":1,"startTime":{"kYear":DisplayStartTime1[0],"kMonth":DisplayStartTime1[1],
                                                                 "kDay":DisplayStartTime1[2],"kHour":DisplayStartTime1[3],"kMinute":DisplayStartTime1[4]},
                                           "endTime":{"kYear":DisplayEndTime1[0],"kMonth":DisplayEndTime1[1],
                                                      "kDay":DisplayEndTime1[2],"kHour":DisplayEndTime1[3],"kMinute":DisplayEndTime1[4]}}}) #显示时间
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.partner.empty_all(1)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":5, "errorCode":0}})
        sleep(3)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3)
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=120) #请求充电
        except Exception:
            assert True
        else:
            assert False
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetDisplayBookChargingInfo", {},
                                             {"out": {"type":1,"startTime":{"kYear":DisplayStartTime1[0],"kMonth":DisplayStartTime1[1],
                                                                 "kDay":DisplayStartTime1[2],"kHour":DisplayStartTime1[3],"kMinute":DisplayStartTime1[4]},
                                           "endTime":{"kYear":DisplayEndTime1[0],"kMonth":DisplayEndTime1[1],
                                                      "kDay":DisplayEndTime1[2],"kHour":DisplayEndTime1[3],"kMinute":DisplayEndTime1[4]}}}) #显示时间
        self.partner.empty_all()
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":0, "errorCode":0}})
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookStopTiAchieved", 1,timeout=360) #停止充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 3) #请求充电反馈    
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":7,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #这里AK版本有bug需要更新时间到明天
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetDisplayBookChargingInfo", {},
                                             {"out": {"type":1,"startTime":{"kYear":DisplayStartTime1[0],"kMonth":DisplayStartTime1[1],
                                                                 "kDay":DisplayStartTime1[2],"kHour":DisplayStartTime1[3],"kMinute":DisplayStartTime1[4]},
                                           "endTime":{"kYear":DisplayEndTime1[0],"kMonth":DisplayEndTime1[1],
                                                      "kDay":DisplayEndTime1[2],"kHour":DisplayEndTime1[3],"kMinute":DisplayEndTime1[4]}}}) #显示时间
        DisplayStartTime2=DisplayStartTime(nowtime,86520)
        DisplayEndTime2=DisplayEndTime(nowtime,86880)
        logger.info(f"更新后的时间是{nowtime}并且显示开始时间为{DisplayStartTime2}=显示结束时间为{DisplayEndTime2}")
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) #拔枪
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "DisplayBookChargingInfo",
                                  {"info":{"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}},timeout=3)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetDisplayBookChargingInfo", {},
                                             {"out": {"type":0,"startTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60},
                                               "endTime":{"kYear":2236,"kMonth":13,"kDay":32,"kHour":24,"kMinute":60}}},timeout=3)

    @allure.title("通知预约充电信息kBookStsStandby_endtime未过时OTA结束")
    @pytest.mark.full
    def test_caseid_1988541(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #请求预约充电回馈状态
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+120}和结束时间{nowtime+480}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #插枪时设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.partner.empty_all(1)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":5, "errorCode":0}})
        sleep(3)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3)
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=120) #请求充电
        except Exception:
            assert True
        else:
            assert False
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3)
        self.partner.empty_all()
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":0, "errorCode":0}})
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookStopTiAchieved", 1,timeout=360) #停止充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 3) #请求充电反馈    
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":7,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #这里AK版本有bug需要更新时间到明天
                                                                
    @allure.title("通知预约充电信息kBookStsStandby_OTA→kBookStsCanceled")
    @pytest.mark.full
    def test_caseid_1988360(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":5, "errorCode":0}})
        self.partner.empty_all(3)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+86340}和结束时间{nowtime+86760}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86880,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #插枪时设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86880,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入OTA_standby
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+86340, "endTime": nowtime+86880, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #取消
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr03, "StopBookChrgnReq", 1)#取消预约充电
        self.partner.empty_all(2)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":0, "errorCode":0}}) #取消OTA
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #不请求充电
        sleep(2)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86880,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3)

    @allure.title("通知预约充电信息_fota状态非5/6/7/21且处于时间段内需要下发充电请求")
    @pytest.mark.full
    def test_caseid_1989691(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(4)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        for fotastatus in [0,1,2,3,4,8,9,10,11,20,22,23]:
            logger.info(f"fota状态处于{fotastatus}")
            self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":fotastatus, "errorCode":0}})
            self.partner.empty_all(3)
            self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                            {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+480, 
                                                    "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #没插枪时不用设置
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
            logger.info(f"通知的开始时间{nowtime+86340}和结束时间{nowtime+86760}")
            self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                        "info":{"startTime":nowtime+86340,"endTime":nowtime+86880,"repeatType":1},
                                                                        "isToTargetSOCStop":False}}}) #进入wait
            sleep(3)
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #插枪时设置
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #不请求充电

            self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                        "info":{"startTime":nowtime+86340,"endTime":nowtime+86880,"repeatType":1},
                                                                        "isToTargetSOCStop":False}}}) #进入OTA_standby
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2)
            self.partner.empty_all(3)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
            sleep(2)
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) #拔枪
            self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                        "info":{"startTime":nowtime+86340,"endTime":nowtime+86880,"repeatType":1},
                                                                        "isToTargetSOCStop":False}}}) #进入到wait    
            self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                            {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                    "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 0) #预约充电信号
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #没插枪时不用设置
            self.partner.empty_all(3)

    @allure.title("通知预约充电信息_fota状态处于5/6/7/21不能下发充电请求")
    @pytest.mark.full
    def test_caseid_1989692(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(4)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        for fotastatus in [5,6,7,21]:
            logger.info(f"fota状态处于{fotastatus}")
            self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":fotastatus, "errorCode":0}})
            self.partner.empty_all(3)
            self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                            {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+480, 
                                                    "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #没插枪时不用设置
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
            logger.info(f"通知的开始时间{nowtime+86340}和结束时间{nowtime+86760}")
            self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                        "info":{"startTime":nowtime+86340,"endTime":nowtime+86880,"repeatType":1},
                                                                        "isToTargetSOCStop":False}}}) #进入wait
            sleep(3)
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #插枪时设置
            try:
                self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #不请求充电
                self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                        "info":{"startTime":nowtime+86340,"endTime":nowtime+86880,"repeatType":1},
                                                                        "isToTargetSOCStop":False}}}) #进入OTA_standby
            except Exception:
                assert True
            else:
                assert False
            self.partner.empty_all(3)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
            sleep(2)
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) #拔枪
            self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                        "info":{"startTime":nowtime+86340,"endTime":nowtime+86880,"repeatType":1},
                                                                        "isToTargetSOCStop":False}}}) #进入到wait    
            self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                            {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                    "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 0) #预约充电信号
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #没插枪时不用设置
        
    @allure.title("通知预约充电信息kBookStsStandby_OTA→kBookStsWait_noconnect")
    @pytest.mark.full
    def test_caseid_1988362(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":5, "errorCode":0}})
        self.partner.empty_all(3)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #没插枪时不用设置
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0) #请求充电
        logger.info(f"通知的开始时间{nowtime+86340}和结束时间{nowtime+86760}")
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) #插枪
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #插枪时设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入OTA_standby
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) #拔枪
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入到wait
        self.partner.empty_all(2)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":0, "errorCode":0}}) #取消OTA
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #不请求充电
        sleep(2)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+86340,"endTime":nowtime+86760,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3)

#=======================================================================================

@allure.feature("SOA服务接口")
@allure.story("BGM应用/HighVoltageAppService")
class TestHighVoltageAppService_NetworkSleep(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([
            ("HighVoltageAppService", "client"),
            ("HighVoltageService", "client"),
            ("VehicleTimeService", "client")])
        self.partner.method_default_timeout = 3
        self.sd_tester.tester_present()
        self.ipdu.send_pdu('chassiscan1', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('chassiscan2', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('propulsioncan', 0x516, [0x16, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.sd_tester.write_single_ccp(973,2) #交直流都支持
        sleep(3)
        self.nucapp.bgm_power_off()
        self.nucapp.bgm_power_on()
        self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        sleep(5)#防止第一个case不稳定

    def network_sleep(self):
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.stop_tester_present()
        sleep(2)
        self.nucapp.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.nucapp.tcam_kl15_down()
        self.nucapp.bgm_power_off()
        time.sleep(5)
        self.nucapp.bgm_power_on()
        sleep(20)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr20, 'DiagcComActv', 0)
        # 关闭四门两盖、座椅不占座、门外开关不按、没有踩刹车、危险报警灯不亮
        # 发送lin补电
        self.ipdu.set(self.ipdu.cem_lin6.CemCem_Lin6Fr02, "BattSnsrStReq", 1)
        self.ipdu.send_pdu('cem_lin6', 0x06, data=[0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
        time.sleep(10)
        # 设置NFC锁车
        self.dk.set_cenlock_sts(3)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'ChrgnUReq', 116)#物理值13.5
        self.ipdu.check_PNC("connectivitycanfd", 0x533, 'PNC25_BGM', 0, timeout=1)
        self.ipdu.check_PNC("connectivitycanfd", 0x533, 'PNC29_BGM', 0, timeout=60)
        logger.info(f"111111111")
        self.dk.stop_listen_dk_bgm_response()
        # 清除缓存
        time.sleep(5)
        # 判断车辆模式是否是ABANDONED
        start_time = time.time()
        while time.time() - start_time < 60 * 7:
            try:
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 0,timeout=0.2)
            except Exception:
                logger.info(f'当前不为ABANDONED状态')
            else:
                break
            sleep(1)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 0,timeout=0.2)
        time.sleep(20)
        self.ipdu.pause_all_bus_send()
        self.ipdu.send_pdu('cem_lin6', 0x06, data=[0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
        time.sleep(40)
        # 检查CAN LIN FR是否有报文发出

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.sd_tester.change_usage_mode(1)
        self.partner.empty_all(1)
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.io.set_four_door_close()
        try:
            self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=10)
        except Exception as err:
            self.nucapp.tcam_power_off()
            sleep(25)
            self.nucapp.bgm_power_off()
            sleep(2)
            self.nucapp.bgm_power_on()
            self.nucapp.tcam_power_on()
            self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
            self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=300)
        else:
            assert True
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消tcam的闹钟防止紊乱
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #请求预约充电回馈状态 枚举值取消

    def after_each_func(self, ecu):
        self.nucapp.bgm_diag_line_up()#诊断恢复
        self.ipdu.reset_check_results()
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        try:
            self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        except Exception as err:
            self.nucapp.tcam_power_off()
            sleep(25)
            self.nucapp.bgm_power_off()
            sleep(2)
            self.nucapp.bgm_power_on()
            self.nucapp.tcam_power_on()
            self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
            self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=300)
        else:
            assert True
        self.dk.stop_listen_dk_bgm_response()
        self.sd_tester.stop_tester_present()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    @allure.title("通知预约充电信息通过诊断唤醒BGM进行充电")
    @pytest.mark.full
    def test_caseid_1988801(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+60, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #请求预约充电回馈状态
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+600, "endTime": nowtime+960, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1) #设置预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态

        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+600,"endTime":nowtime+960,"repeatType":1},  
                                                                    "isToTargetSOCStop":False}}}) #进入standby
        sleep(1)
        self.network_sleep() #最快3min休眠
        self.partner.wait_for_service_reconnect(HIGHVOLTAGE_SERVICE_CLIENT) #等待高压上线后恢复总线，避免上电不来枪的信号，无法进入charging
        self.ipdu.resume_all_bus_send()
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":4,
                                                                    "info":{"startTime":nowtime+600,"endTime":nowtime+960,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=430) #进入charging后时间更新
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=3) #时间到点请求充电
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 2) #假设在充电
        sleep(1)
        logger.info(f"通知的开始时间{nowtime+600}和结束时间{nowtime+960}")
        self.partner.empty_all(2)
        self.nucapp.bgm_diag_line_up()
        logger.info(f'打开诊断激活线和tcam激活线方便下发停止指令') #停止充电按tcam给的闹钟事件触发，和正常流程一样所以这里不校验停止了

#============================================================================================================================

@allure.feature("SOA服务接口")
@allure.story("架构基础/HighVoltageAppService")
class TestHighVoltageAppServiceFota_FOTA_restart(TestBase): #每个case都要杀SOAAPP进程
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.sd_tester.write_single_ccp(973,2) #AC
        sleep(3)
        for process_name in ["monitor_em2.sh", "em2", "fota/fota", "service_monitor"]:
            res = command_send(
                device_name="BGM",
                cmd=f"ps -ef |grep app |grep {process_name} |grep -v grep",
                timeout=60,
            )[1]
            pid = res.split()[1]
            command_send(device_name="BGM", cmd=f"kill -9 {pid}")
        sleep(2)
        command_send(device_name="BGM", cmd='su - service_monitor -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;/app/bin/service_monitor  -c /app/etc/service_monitor.json &"', timeout=15)
        self.partner = S2sBaseClass([
            ("HighVoltageAppService", "client"),
            ("HighVoltageService", "client"),
            ("FotaMasterService", "server"),
            ("VehicleTimeService", "client"),
            ("VehicleSetStatusService", "client")]) 
        self.sd_tester.tester_present()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        self.nucapp.bgm_power_off()
        sleep(3)
        self.nucapp.bgm_power_on()
        sleep(10)
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=True)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetMaintenanceMode", {"isOn": False},timeout=3)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) #没有开始充电
        sleep(0.5)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":0, "errorCode":0}})
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0)   #交流枪 
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0) #直流枪
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 20.0) #电量20
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.partner.empty_all(1) #不能用restart接口
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+420, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先取消tcam的闹钟
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #请求预约充电回馈状态
        sleep(1)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def start_BGM_Process(self,process_name):
        '''启动BGM的某一个进程'''
        command_send(device_name="BGM", cmd=f'su - {process_name} -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;/app/bin/{process_name}  -c /app/etc/{process_name}.json &"', timeout=15)

    def kill_SOAapp_keep_mockFota_connect(self):
        '''kill掉SOAApp后仍然保持仿真的fota服务端连接'''
        self.kill_bgm_process("vehicle_time")
        self.kill_bgm_process("SOAApp")
        self.start_BGM_Process("SOAApp")
        self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.empty_all(3)#时间同步 
        self.start_BGM_Process("vehicle_time")
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)#时间同步后继续进入charging
        sleep(2)

    def kill_SOAapp_em2_Fota_service_monitor(self):
        '''kill掉SOAApp em2 fota service_monitor等'''
        for process_name in ["monitor_em2.sh", "em2", "fota/fota"]:
            res = command_send(
                device_name="BGM",
                cmd=f"ps -ef |grep app |grep {process_name} |grep -v grep",
                timeout=60,
            )[1]
            pid = res.split()[1]
            command_send(device_name="BGM", cmd=f"kill -9 {pid}")
        sleep(3)

    @allure.title("通知预约充电信息_不处于时间段内_fota7跳idle_不下发请求充电")
    @pytest.mark.full
    def test_caseid_1989466(self): 
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                        {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+300, "endTime": nowtime+600, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+300,"endTime":nowtime+600,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.empty_all(2) #防止数据没落盘
        self.kill_SOAapp_keep_mockFota_connect()
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                        {"taskId":0, "state":7, "errorCode":0}})   
        sleep(1)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                        {"taskId":0, "state":0, "errorCode":0}})   
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=2) #请求充电
        except Exception:
            assert True
        else:
            assert False
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号

    @allure.title("通知预约充电信息_不处于时间段内_fota8跳idle_不下发请求充电")
    @pytest.mark.full
    def test_caseid_1989622(self): 
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                        {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+300, "endTime": nowtime+600, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+300,"endTime":nowtime+600,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.empty_all(2) #防止数据没落盘
        self.kill_bgm_process("vehicle_time") 
        self.kill_bgm_process("SOAApp")
        self.start_BGM_Process("SOAApp")
        self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        sleep(3)
        self.start_BGM_Process("vehicle_time")
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)#时间同步后继续进入charging
        sleep(2)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                        {"taskId":0, "state":8, "errorCode":0}})   
        sleep(1)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                        {"taskId":0, "state":0, "errorCode":0}})   
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=2) #请求充电
        except Exception:
            assert True
        else:
            assert False
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号

    @allure.title("通知预约充电信息_不处于时间段内_fota9跳idle_不下发请求充电")
    @pytest.mark.full
    def test_caseid_1989623(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                        {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+300, "endTime": nowtime+600, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+300,"endTime":nowtime+600,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.empty_all(2) #防止数据没落盘
        self.kill_SOAapp_keep_mockFota_connect()
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                        {"taskId":0, "state":9, "errorCode":0}})   
        sleep(1)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                        {"taskId":0, "state":0, "errorCode":0}})   
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=2) #请求充电
        except Exception:
            assert True
        else:
            assert False
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号

    @allure.title("通知预约充电信息_endtime无效且当前时间大于starttime+8_fota跳idle_不下发请求充电")
    @pytest.mark.full
    def test_caseid_1989598(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                        {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime-32400, "endTime": nowtime+600, 
                                                "repeatType": 1},"isToTargetSOCStop": True}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #请求预约充电回馈状态
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+54000,"endTime":0,"repeatType":1},
                                                                    "isToTargetSOCStop":True}}}) #进入wait
        self.partner.empty_all(2) #防止数据没落盘
        self.kill_bgm_process("vehicle_time")
        self.kill_bgm_process("SOAApp")
        self.start_BGM_Process("SOAApp")
        self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        sleep(3)
        self.start_BGM_Process("vehicle_time")
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)#
        sleep(2)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                        {"taskId":0, "state":8, "errorCode":0}})   
        sleep(1)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                        {"taskId":0, "state":0, "errorCode":0}})   
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=2) #请求充电
        except Exception:
            assert True
        else:
            assert False
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号

    @allure.title("通知预约充电信息_处于时间段内_非kBookActive和kBookDeactive_不下发请求充电")
    @pytest.mark.full
    def test_caseid_1989404(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                        {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime-120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 0,timeout=0.5) #预约充电信号
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #请求预约充电回馈状态
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"repeatType":1},"isToTargetSOCStop":False}}}) #进入wait
        for fotasts in [8,9,10]:
            self.kill_bgm_process("vehicle_time")
            self.kill_bgm_process("SOAApp")
            self.start_BGM_Process("SOAApp")
            self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
            sleep(3)
            self.start_BGM_Process("vehicle_time")
            self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)#时间同步后继续进入charging
            sleep(2)
            self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                           {"taskId":0, "state":fotasts, "errorCode":0}})  
            sleep(1) 
            self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                           {"taskId":0, "state":0, "errorCode":0}})   
            try:
                self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=2) #请求充电
            except Exception:
                assert True
            else:
                assert False
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 0,timeout=0.5) #预约充电信号

    @allure.title("通知预约充电信息_entime已过时_fota跳idle_不下发请求充电")
    @pytest.mark.full
    def test_caseid_1989467(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #没插枪时不用设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        sleep(2) #没有被持久化
        self.kill_bgm_process("vehicle_time")
        self.kill_bgm_process("SOAApp")
        sleep(480) #模拟480S后进入开始充电的时间
        self.start_BGM_Process("SOAApp")
        self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.empty_all(3)#时间同步 
        self.start_BGM_Process("vehicle_time")
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)#时间同步后继续进入charging
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3) #进入wait
        self.kill_SOAapp_keep_mockFota_connect()
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":7, "errorCode":0}})
        sleep(1)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                           {"taskId":0, "state":0, "errorCode":0}})   
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=2) #请求充电
        except Exception:
            assert True
        else:
            assert False
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号

    @allure.title("通知预约充电信息_处于时间段内_非AC交流枪_不下发请求充电")
    @pytest.mark.full
    def test_caseid_1989405(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #没插枪时不用设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.empty_all(2)#防止数据没落盘
        self.kill_bgm_process("vehicle_time")
        self.kill_bgm_process("SOAApp")
        sleep(120) #模拟120S后进入开始充电的时间
        self.start_BGM_Process("SOAApp")
        self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.empty_all(3)#时间同步 
        self.start_BGM_Process("vehicle_time")
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)#时间同步后继续进入charging
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3) #进入wait
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":7, "errorCode":0}})
        sleep(1)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                           {"taskId":0, "state":0, "errorCode":0}})   
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=2) #请求充电
        except Exception:
            assert True
        else:
            assert False
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 5) 
        sleep(2)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":9, "errorCode":0}})
        sleep(1)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                           {"taskId":0, "state":0, "errorCode":0}})   
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=2) #请求充电
        except Exception:
            assert True
        else:
            assert False
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号

    @allure.title("通知预约充电信息_处于时间段内_fota跳idle_一个周期只补发一次")
    @pytest.mark.sanity
    def test_caseid_1989469(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #没插枪时不用设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.empty_all(2)#防止数据没落盘
        self.kill_bgm_process("vehicle_time")
        self.kill_bgm_process("SOAApp")
        sleep(120) #模拟120S后进入开始充电的时间
        self.start_BGM_Process("SOAApp")
        self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.empty_all(3)#时间同步 
        self.start_BGM_Process("vehicle_time")
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)#时间同步后继续进入charging
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3) #进入wait
        sleep(2)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":7, "errorCode":0}})
        sleep(1)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                           {"taskId":0, "state":0, "errorCode":0}})   
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=2) #请求充电
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":8, "errorCode":0}})
        sleep(1)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":0, "errorCode":0}})
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=2) #请求充电
        except Exception:
            assert True
        else:
            assert False
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号

    @allure.title("通知预约充电信息_处于时间段内_fota状态9跳idle_下发请求充电")
    @pytest.mark.sanity
    def test_caseid_1989610(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #没插枪时不用设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.empty_all(2)#防止数据没落盘
        self.kill_bgm_process("vehicle_time")
        self.kill_bgm_process("SOAApp")
        sleep(120) #模拟120S后进入开始充电的时间
        self.start_BGM_Process("SOAApp")
        self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.empty_all(3)#时间同步 
        self.start_BGM_Process("vehicle_time")
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)#时间同步后继续进入charging
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3) #进入wait
        self.kill_SOAapp_keep_mockFota_connect()
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":9, "errorCode":0}})
        sleep(1)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                           {"taskId":0, "state":0, "errorCode":0}})   
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=2) #请求充电
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号

    @allure.title("通知预约充电信息_处于时间段内_fota状态8跳idle_下发请求充电")
    @pytest.mark.sanity
    def test_caseid_1989609(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #没插枪时不用设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.empty_all(2)#防止数据没落盘
        self.kill_bgm_process("vehicle_time")
        self.kill_bgm_process("SOAApp")
        sleep(120) #模拟120S后进入开始充电的时间
        self.start_BGM_Process("SOAApp")
        self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.empty_all(3)#时间同步 
        self.start_BGM_Process("vehicle_time")
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)#时间同步后继续进入charging
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3) #进入wait
        self.kill_SOAapp_keep_mockFota_connect()
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":8, "errorCode":0}})
        sleep(1)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                           {"taskId":0, "state":0, "errorCode":0}})   
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=2) #请求充电
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号

    @allure.title("通知预约充电信息_处于时间段内_fota状态7跳idle_下发请求充电")
    @pytest.mark.smoke
    def test_caseid_1989468(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #没插枪时不用设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.empty_all(2)#防止数据没落盘
        self.nucapp.bgm_power_off()
        sleep(3)
        self.ipdu.pause_all_bus_send()
        sleep(120)
        self.ipdu.resume_all_bus_send()
        self.nucapp.bgm_power_on()
        self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)#时间同步后继续进入charging
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3) #进入wait
        self.kill_SOAapp_keep_mockFota_connect()
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":7, "errorCode":0}})
        sleep(1)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                           {"taskId":0, "state":0, "errorCode":0}})   
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=2) #请求充电
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号

    @allure.title("通知预约充电信息_处于时间段内_遍历fotaStatus从非789跳0_不下发请求充电")
    @pytest.mark.sanity
    def test_caseid_1989403(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #没插枪时不用设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.empty_all(2)#防止数据没落盘
        self.kill_bgm_process("vehicle_time")
        self.kill_bgm_process("SOAApp")
        sleep(120) #模拟120S后进入开始充电的时间
        self.start_BGM_Process("SOAApp")
        self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.empty_all(3)#时间同步 
        self.start_BGM_Process("vehicle_time")
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)#时间同步后继续进入charging
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3) #进入wait
        self.kill_SOAapp_keep_mockFota_connect()
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":random.choice([1,2,3,4,5,6,10,11,20,21,22,23]), "errorCode":0}})
        sleep(1)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                           {"taskId":0, "state":0, "errorCode":0}})   
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=2) #请求充电
        except Exception:
            assert True
        else:
            assert False
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号

    @allure.title("通知预约充电信息_处于时间段内_fota状态直接为0_不下发请求充电")
    @pytest.mark.sanity
    def test_caseid_1989487(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}},timeout=0.1) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #没插枪时不用设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.empty_all(2)#防止数据没落盘
        self.kill_bgm_process("vehicle_time")
        self.kill_bgm_process("SOAApp")
        sleep(120) #模拟120S后进入开始充电的时间
        self.start_BGM_Process("SOAApp")
        self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.empty_all(3)#时间同步 
        self.start_BGM_Process("vehicle_time")
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)#时间同步后继续进入charging
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3) #进入wait
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                           {"taskId":0, "state":0, "errorCode":0}})   
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=2) #请求充电
        except Exception:
            assert True
        else:
            assert False
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号

    @allure.title("通知预约充电信息_处于时间段内_遍历fotaStatus从789跳非0_不下发请求充电")
    @pytest.mark.sanity
    def test_caseid_1989402(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 0) #请求充电反馈
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 0) #请求预约充电回馈状态
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(1)#防止状态反馈0去干扰
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=5)
        sleep(1)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        self.partner.empty_all(1)
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+480, 
                                                "repeatType": 1},"isToTargetSOCStop": False}}) #先打开
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 1) #没插枪时不用设置
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}}) #进入wait
        self.partner.empty_all(2)#防止数据没落盘
        self.kill_bgm_process("vehicle_time")
        self.kill_bgm_process("SOAApp")
        sleep(120) #模拟120S后进入开始充电的时间
        self.start_BGM_Process("SOAApp")
        self.partner.wait_for_service_reconnect(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        self.partner.empty_all(3)#时间同步 
        self.start_BGM_Process("vehicle_time")
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)#时间同步后继续进入charging
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":3,
                                                                    "info":{"startTime":nowtime+120,"endTime":nowtime+480,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}},timeout=3) #进入wait
        sleep(1)
        self.kill_SOAapp_keep_mockFota_connect()
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": {"taskId":0, "state":7, "errorCode":0}})
        sleep(1)
        self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER,"Status",{"status": 
                                                                           {"taskId":0, "state":random.choice([1,2,3,4,5,6,7,10,11,20,21,22,23]), "errorCode":0}})   
        try:
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 1,timeout=2) #请求充电
        except Exception:
            assert True
        else:
            assert False
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgnActvdReq", 0,timeout=0.5) #请求充电
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, "BookChrgSetReq", 1,timeout=0.5) #预约充电信号