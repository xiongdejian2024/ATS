# -*- encoding: utf-8 -*-
"""
@File         :test_ResetSOAConfigService.py
@Time         :2023/04/30 19:07:31
@Author       :tao.cheng_ext@jiduauto.com
@Description  :Test SOA for ResetSOAConfigService
"""

import random
import allure
import math
import pytest
from time import sleep
from xat_ecu.legacy.common.data_type_handing import logger
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
import datetime

def current_time_with_seconds_zero_to_timestamp():
    ''' 获取当前时间时间戳并将秒数置0以便拿到整时整分0秒'''
    now = datetime.datetime.now()
    now_zero_seconds = now.replace(second=0, microsecond=0)
    timestamp = int(now_zero_seconds.timestamp())
    return timestamp

@allure.feature("SOA服务接口")
@allure.story("BGM应用/ResetSOAConfigService")
class TestResetSOAConfigService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("EntryService", "client"),
                                     ("WirelessPhoneChargingService", "client"),
                                     ("SuspensionService", "client"),
                                     ("LightService", "client"),
                                     ("WiperService", "client"),
                                     ("ChassisService", "client"),
                                     ("HighVoltageService", "client"),
                                     ("DoorService", "client"),
                                     ("SeatService", "client"),
                                     ("SteerWheelService", "client"),
                                     ("HighVoltageAppService", "client"),
                                     ("ClimateControlService", "client"),
                                     ("ShieldWindowService", "client"),
                                    ("VehicleModeService", "client"),
                                     ("CentralLockService", "client"),
                                     ("KeyService", "client"),
                                     ("AVPService", "server"),
                                     ("RPAAPAService", "server"),
                                     ("VehicleSetStatusService", "client"),
                                     ("VehicleTimeService", "client"),
                                     ("ConditionCheckService", "client"),
                                     ("HornService", "client"),
                                     ("ResetSOAConfigService", "client"),
                                     ])
        self.partner.method_default_timeout = 3 #resetSOA注册服务多，可以适当放开
        self.sd_tester.tester_present()
        self.io.set_four_door_close()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.sd_tester.stop_tester_present()
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
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe', 1)
        self.ipdu.rx_flag_reset_all()
        self.ipdu.reset_check_results()
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.partner.empty_all(2)#重启的case较多，重启后如果进行ResetAllVehicleSOAConfig会超时，需要加大延时，因为此接口注册服务过多

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def CltcKm(self,cltcfullkm,SOC,SOH):
        '''cltc续航里程  需要输入满电续航值 电量 健康度 '''
        if SOH >= 99:
            return math.floor(cltcfullkm*SOC*100/10000)
        else:
            return math.floor(cltcfullkm*SOC*(SOH+1)/10000)

    def EstimateKm(self,batteryCapacityMax,SOC,SOH,Powerper100km):
        '''实估续航里程  需要输入健康度 电池度数 最大充电电量 百公里电耗'''
        return math.floor(batteryCapacityMax*SOC*SOH*0.01/Powerper100km)

    def ck_CLTCRange_estimatedRange_GetResponse(self, Value1, value2, value3):
        '''校验通知表显续航里程的source和CLTCRange和estimatedRange的值'''
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "NotifyRange", 
                                  {"infos": {"source": Value1,"CLTCRange":value2,"estimatedRange": value3}})
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetRange", {},
                                                 {"out": {"source": Value1,"CLTCRange":value2,"estimatedRange": value3}})

    def check_SetBatteryHeating(self, remReq=0, remTarT=0, remReqFromAC=0, remTarTFromAC=0, localreq=0, localTarT=0, timeout=2):
        ''' 设置电池热管理请求 下行总线信号校验'''
        self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr01, 'RemHvBattHeatgReq', remReq, timeout=timeout)
        self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr01, 'RemHvBattHeatgTarT', remTarT, timeout=timeout)
        self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr09, 'RemHvBattHeatgReqFromAC', remReqFromAC, timeout=timeout)        
        self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr09, 'RemHvBattHeatgTarTFromAC', remTarTFromAC, timeout=timeout)
        self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr01, 'LocalHvBattThermReq', localreq, timeout=timeout)
        self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr01, 'LocalHvBattThermTarT', localTarT, timeout=timeout)

    def five_door_close(self):
        self.io.pass_door_close()
        self.io.drvr_door_close()
        self.io.lere_door_close()
        self.io.rire_door_close()
        self.io.trunk_door_close()
        sleep(1)

    def seat_belt_status(self,A,B,C,D,E):
        """设置主驾 副驾 左后 后中 后右 1代表已系 0 代表未系"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSt1', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSt1', D)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSt1', E)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSts', 0)
        sleep(1)

    def set_four_seat_occupt(self,A,B,C,D):
        """设置副驾 左后 后中 后右 1/2代表占位 0 代表未占位"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts_0_SRSBackBoneSignalIPdu04', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe_0_SRSBackBoneSignalIPdu04', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi_0_SRSBackBoneSignalIPdu04', D)
        sleep(1)

    def set_no_default_config(self):
        """测试前提，先设置配置为非默认配置项"""
        # 设置外灯模式Off
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindMode",{"zoneId":2,"mode":2})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindMode",{"zoneId":3,"mode":2})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindMode",{"zoneId":4,"mode":2})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 0})
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
                                         {"isOpen": False})
        # 设置后雾灯打开
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                         {"lights": [{"light": {"type": 4, "zoneId": 10}, "mode": 1}]})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 1)
        # 设置雨刮档位调节关闭
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": False})
        sleep(0.2)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit", {"wipers": 0, "isOn": False})
        sleep(0.2)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 2}]})
        # 设置雪地模式非关闭
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetTorqueMode", {"mode": 1})
        self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetEnergyRecoveryLevel", {"level": 1})
        # 设置陡坡缓降打开
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetHDC", {"on": True})
        # 校验电动侧门电动开启禁用（手动模式）：手动
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetDoorMode", {"doors": [{"id": 4, "mode": 0}]})
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetDrvrPwrDoorAutOperMode', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetPassPwrDoorAutOperMode', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetLeRePwrDoorAutOperMode', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetRiRePwrDoorAutOperMode', 0, timeout=0.5)
        # 打开离车闭锁，打开近车自动解锁 #key0是离开上锁，key1是靠近解锁，key3是解锁开门
        self.bgm_eth_inter.start_bgm_tcpdump()#偶发0.5S校验不到，采用tcpdump观察15015是否下发
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3},
                                                                                         {"key": 1, "value": 1},{"key": 3, "value": 1}]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(2)
        self.bgm_eth_inter.ck_ordered_array("WalkAwayLockHmi", [3])#周期下发的
        self.bgm_eth_inter.ck_ordered_array("ApproachUnlockHmi", [0])#周期下发的
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr18, "WalkAwayLockHmi", 3, timeout=1) #总线为事件帧，但是PDU下发周期是1S
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr18, "ApproachUnlockHmi", 0, timeout=1)#总线为事件帧，但是PDU下发周期是1S
        # 设置座椅加热1级
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingLevel",
                                         {"params": [{"id": 0, "uint8Info": 1},
                                                     {"id": 1, "uint8Info": 1},
                                                     {"id": 4, "uint8Info": 1},
                                                     {"id": 6, "uint8Info": 1}]})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', 1, timeout=0.5)
        # 设置座椅通风1级
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingLevel",
                                         {"params": [{"id": 0, "uint8Info": 1},
                                                     {"id": 1, "uint8Info": 1},
                                                     {"id": 4, "uint8Info": 1},
                                                     {"id": 6, "uint8Info": 1}]})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstRi', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowSecLe', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowSecRi', 1, timeout=0.5)
        # 设置主副驾座椅按摩
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetMassageConf",
                                         {"params": [{"id": 0, "conf": {"isOn": True, "type": 1, "intensity": 0}},
                                                     {"id": 1, "conf": {"isOn": True, "type": 1, "intensity": 0}}]})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'DrvrSeatDispMassgFctOnOff', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'DrvrSeatDispMassgFctMassgProg', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'DrvrSeatDispMassgFctMassgInten', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'PassSeatDispMassgFctOnOff', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'PassSeatDispMassgFctMassgProg', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'PassSeatDispMassgFctMassgInten', 0, timeout=0.5)
        # 设置方向盘加热打开
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 1})
        # 空调相关的配置项
        # 设置前排空调总开关-关闭
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId": 0})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {},
                                              {"out": {"firstRowPowerStatus": False,"secondRowPowerStatus": False}})
        # 设置AC 关闭
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAC", {}, {"out": False})
        # 设置AUTO zoneid=0, on=False
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetClimateAuto",{"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindSpeed",{"zoneId":1,"speed":14})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindSpeed",{"zoneId":2,"speed":14})
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetClimateAuto",{"zoneId": 0, "on": False})
        # 设置内外循环- 内循环
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 2})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 2})
        # 设置温度同步设置，on=False
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": False})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": False})
        # 设置主驾、副驾、后排温度16摄氏度
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperature", {"zoneId": 3, "value": 16.0})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperature", {"zoneId": 4, "value": 16.0})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperature", {"zoneId": 2, "value": 16.0})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetTargetTemperature", {"zoneId": 3},
                                              {"out": {"zoneId": 3, "value": 16.0, "isValid": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetTargetTemperature", {"zoneId": 4},
                                              {"out": {"zoneId": 4, "value": 16.0, "isValid": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetTargetTemperature", {"zoneId": 2},
                                              {"out": {"zoneId": 2, "value": 16.0, "isValid": True}})
        #风向调节 设置为随机值
        name_to_signal = {"第一排左侧左":["HmiElecAirDirCrtlReqDrvrLePosX","HmiElecAirDirCrtlReqDrvrLePosY"],
                          "第一排左侧右":["HmiElecAirDirCrtlReqDrvrRiPosX","HmiElecAirDirCrtlReqDrvrRiPosY"],
                          "第一排右侧左":["HmiElecAirDirCrtlReqPassLePosX","HmiElecAirDirCrtlReqPassLePosY"],
                          "第一排右侧右":["HmiElecAirDirCrtlReqPassRiPosX","HmiElecAirDirCrtlReqPassRiPosY"],
                          "第二排左":["HmiReElecAirDirCrtlReqSecRowLePosX","HmiReElecAirDirCrtlReqSecRowLePosY"]}
        location_to_number={"第一排左":3,"第一排右":4,"第二排左":2}
        for name,singal_list in name_to_signal.items():
            logger.info(f"设置接口_SetOutletAngle_{name}出风角度")
            X = random.randint(0,100)
            Y = random.randint(0,100)
            side =0 if name[-1]=="左" else 1
            zoneId = location_to_number[name[:4]]
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetOutletAngle",{"outlets":[{"id":zoneId,"side":side,"horizontal":X,"vertical":Y}]})
            logger.info(f"校验信号")
            if "第二排" not in name:
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr49,singal_list[0],X*2)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr49,singal_list[1],Y*2)
            else:
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10,singal_list[0],X*2)
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10,singal_list[1],Y*2)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT,"GetOutletAngle",{"zoneId":zoneId},ck_info={"out":[{"id":zoneId,"side":side,"horizontal":X,"vertical":Y}]}) 
        # 出风口控制 全部关闭
        id_to_signal={8:"HmiAirVentDrvrLeSwtReq",9:"HmiAirVentDrvrRiSwtReq",10:"HmiAirVentPassLeSwtReq",11:"HmiAirVentPassRiSwtReq",12:"HmiAirVentSecLeLeSwtReq"}        
        location_to_number= {"第一排左左":8,"第一排左右":9,"第一排右左":10,"第一排右右":11,"第二排左左":12}
        name_list1 = ["第一排左左","第一排左右","第一排右左","第一排右右","第二排左左"]
        name_list2 = ["关闭"]
        for name_1 in name_list1:
            for name_2 in name_list2: 
                True_or_False = True if name_2 =="开启" else False
                signal_value = 1 if name_2 == "开启" else 0
                logger.info(f"设置接口_SetAirVent_{name_1}{name_2}")
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetAirVent",{"zoneId":location_to_number[name_1],"on":True_or_False})
                logger.info(f"校验总线信号")
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr13,id_to_signal[location_to_number[name_1]],signal_value)
                logger.info(f"获取接口_GetAirVent_{name_1}状态")
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT,"GetAirVent",args={"zoneId":location_to_number[name_1]},ck_info={"out":True_or_False}) 
                         
        # 设置风量
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId": 1, "speed": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1},
                                              {"out": {"zoneId": 1, "speed": 1}})
        # 设置前挡风玻璃除雾_关闭
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFastDefrostMode", {}, {"out": False})
        # 设置后挡风玻璃除雾-Id=@value(2) kShieldWindowRear status=@value(1) kHeatStatusOn
        self.partner.send_method_request(SHIELDWINDOW_SERVICE_CLIENT, "SetHeat", {"heat": {"id": 2, "status": 1}})
        # 设置PM2.5一键过滤 On

    @allure.title("设置随车项恢复出厂设置")
    @pytest.mark.smoke
    def test_caseid_108975(self):
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.set_no_default_config()
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)
        sleep(1)
        # 校验后排空调总开关-开启
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {},
                                              {"out": {"secondRowPowerStatus": True}})
        """校验配置项"""
        # 校验外灯模式：自动
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 1})
        # 校验后雾灯关闭
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 0)
        # 校验雨刮模式：自动
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                              {"out": [{"id": 0, "mode": 6}]})
        # 校验雪地模式：关闭
        # 校验陡坡缓降关闭
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr07, 'EgyRgnLvlSet', 3)
        # self.ipdu.check(self.ipdu.chassiscan1.BgmChas1Fr02, 'TqModReq', 0)
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 0) 
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetDrvrPwrDoorAutOperMode', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetPassPwrDoorAutOperMode', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetLeRePwrDoorAutOperMode', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetRiRePwrDoorAutOperMode', 1, timeout=0.5)
        # 校验离车落锁配置-关五门，近车自动解锁-关闭
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr18, "WalkAwayLockHmi", 0, timeout=0.5)
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr18, "ApproachUnlockHmi", 1, timeout=1.5)#PDU下发周期1S
        # 校验手动闭锁左侧儿童锁-解锁
        # todo: 查看下行pdu 5404 ChdLockReLeCtrlHmiReq=1，pdu_length=1,start_postion=7  先发1帧1，再发1帧0
        # self.ipdu.check(self.ipdu.bodycan.CemBodyFr09, 'ChdLockReLeCtrlHmiReq', 1)  # 估计捕捉不到
        # 校验手动闭锁右侧儿童锁-解锁
        # todo: 查看下行pdu 5405 ChdLockReRiCtrlHmiReq=1，pdu_length=1,start_postion=7  先发1帧1，再发1帧0
        # self.ipdu.check(self.ipdu.bodycan.CemBodyFr09, 'ChdLockReLeCtrlHmiReq', 1)
        # 校验座椅通风开关-关闭
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 0, timeout=0.5) # 事件帧
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', 0, timeout=0.5)
        # 校验座椅加热开关-关闭
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 0, timeout=0.5) # 事件帧
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstRi', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowSecLe', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowSecRi', 0, timeout=0.5)
        # 校验主驾座椅按摩开关-关闭
        # 校验主驾座椅按摩模式-模式1
        # 校验副驾座椅按摩开关-关闭
        # 校验副驾座椅按摩模式-模式1
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'DrvrSeatDispMassgFctOnOff', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'DrvrSeatDispMassgFctMassgProg', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'DrvrSeatDispMassgFctMassgInten', 3, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'PassSeatDispMassgFctOnOff', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'PassSeatDispMassgFctMassgProg', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'PassSeatDispMassgFctMassgInten', 3, timeout=0.5)
        # 校验方向盘加热关闭
        # todo: 查看下行pdu 6151 SteerWhlHeatgOnReq=0
        # 校验前排空调总开关-开启
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {},
                                              {"out": {"firstRowPowerStatus": True}})
        # 校验AC状态-on
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAC", {}, {"out": True})
        # 校验AUTO-zoneid=0-on=true
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateAuto", {"zoneId": 0},
                                              {"out": {"zoneId": 0, "isOn": True}})
        # 校验内外循环Auto-mode=1
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        # 校验温度同步设置，on=True
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        # 校验主驾、副驾、后排温度控制22摄氏度
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetTargetTemperature", {"zoneId": 3},
                                              {"out": {"zoneId": 3, "value": 22.0, "isValid": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetTargetTemperature", {"zoneId": 4},
                                              {"out": {"zoneId": 4, "value": 22.0, "isValid": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetTargetTemperature", {"zoneId": 2},
                                              {"out": {"zoneId": 2, "value": 22.0, "isValid": True}})
        # 校验风量zoneId=@value(1) kFirstRow speed=@value(12) kLvlAutoNormal
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1},
                                              {"out": {"zoneId": 1, "speed": 12}})
        # 校验前挡风玻璃除雾-关闭
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFastDefrostMode", {}, {"out": False})
        # 校验后挡风玻璃除雾-Id=@value(2) kShieldWindowRear status=@value(0) kHeatStatusOff
        self.partner.send_request_and_ck_resp(SHIELDWINDOW_SERVICE_CLIENT, "GetHeat", {"windows": [2]},
                                              {"out": [{"id": 2, "status": 0}]})
        # 校验PM25一键过滤=false
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetPM25", {}, {"out": False})
        # 校验清除异味=false
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCockpitCleanMode", {}, {"out": False})
        # 校验主驾、副驾、后排吹风模式zoneId=3,4,2 mode=7
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr46, 'HmiCmptmtAirDistbnFrntLe', 7, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr46, 'HmiCmptmtAirDistbnFrntRi', 7, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr46, 'HmiCmptmtAirDistbnRe', 7, timeout=0.5)
        
        #检查空调出风口控制
        location_to_number= {"第一排左左":8,"第一排左右":9,"第一排右左":10,"第一排右右":11,"第二排左左":12}
        name_list1 = ["第一排左左","第一排左右","第一排右左","第一排右右","第二排左左"]
        for name_1 in name_list1:
            logger.info(f"获取接口_GetAirVent_{name_1}状态")
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT,"GetAirVent",args={"zoneId":location_to_number[name_1]},ck_info={"out":1}) 
        #检查方向调节各区域
        name_to_signal = {"第一排左侧左":["HmiElecAirDirCrtlReqDrvrLePosX","HmiElecAirDirCrtlReqDrvrLePosY"],
                    "第一排左侧右":["HmiElecAirDirCrtlReqDrvrRiPosX","HmiElecAirDirCrtlReqDrvrRiPosY"],
                    "第一排右侧左":["HmiElecAirDirCrtlReqPassLePosX","HmiElecAirDirCrtlReqPassLePosY"],
                    "第一排右侧右":["HmiElecAirDirCrtlReqPassRiPosX","HmiElecAirDirCrtlReqPassRiPosY"],
                    "第二排左":["HmiReElecAirDirCrtlReqSecRowLePosX","HmiReElecAirDirCrtlReqSecRowLePosY"]}
        location_to_number={"第一排左":3,"第一排右":4,"第二排左":2}
        for name,singal_list in name_to_signal.items():
            side =0 if name[-1]=="左" else 1
            zoneId = location_to_number[name[:4]]
            logger.info(f"校验信号")
            if "第二排" not in name:
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr49,singal_list[0],100)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr49,singal_list[1],100)
            else:
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10,singal_list[0],100)
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10,singal_list[1],100)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT,"GetOutletAngle",{"zoneId":zoneId},ck_info={"out":[{"id":zoneId,"side":side,"horizontal":50,"vertical":50}]}) 
        self.restart_bgm_and_connect_service(RESETSOAVONFIG_SERVICE_CLIENT)
        # 校验后排空调总开关-开启
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {},
                                              {"out": {"secondRowPowerStatus": True}})
        # 校验外灯模式：自动
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 1})
        # 校验后雾灯关闭
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 0)
        # 校验雨刮模式：自动
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                              {"out": [{"id": 0, "mode": 6}]})
        # 校验雪地模式：关闭
        # todo: 查看下行pdu 10011 TqModReqETH=0，pdu_length=1,start_postion=7
        # todo: 查看下行pdu 10003 EgyRgnLvlSetETH=0，pdu_length=1,start_postion=7
        # 校验陡坡缓降关闭
        # todo: 查看下行pdu 10008 HillDwnCtrlStETH=0，pdu_length=1,start_postion=7
        # 校验电动侧门电动开启禁用（手动模式）：电动
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetDrvrPwrDoorAutOperMode', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetPassPwrDoorAutOperMode', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetLeRePwrDoorAutOperMode', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetRiRePwrDoorAutOperMode', 1, timeout=0.5)
        # 校验离车落锁配置-关五门，近车自动解锁-打开
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr18, "WalkAwayLockHmi", 0, timeout=0.5)
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr18, "ApproachUnlockHmi", 1, timeout=1.5)
        # 校验手动闭锁左侧儿童锁-解锁
        # todo: 查看下行pdu 5404 ChdLockReLeCtrlHmiReq=1，pdu_length=1,start_postion=7  先发1帧1，再发1帧0
        # self.ipdu.check(self.ipdu.bodycan.CemBodyFr09, 'ChdLockReLeCtrlHmiReq', 1)  # 估计捕捉不到
        # 校验手动闭锁右侧儿童锁-解锁
        # todo: 查看下行pdu 5405 ChdLockReRiCtrlHmiReq=1，pdu_length=1,start_postion=7  先发1帧1，再发1帧0
        # self.ipdu.check(self.ipdu.bodycan.CemBodyFr09, 'ChdLockReLeCtrlHmiReq', 1)
        # 校验座椅通风开关-关闭
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 0, timeout=0.5) # 事件帧
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', 0, timeout=0.5)
        # 校验座椅加热开关-关闭
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 0, timeout=0.5) # 事件帧
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstRi', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowSecLe', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowSecRi', 0, timeout=0.5)
        # 校验主驾座椅按摩开关-关闭
        # 校验主驾座椅按摩模式-模式1
        # 校验副驾座椅按摩开关-关闭
        # 校验副驾座椅按摩模式-模式1
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'DrvrSeatDispMassgFctOnOff', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'DrvrSeatDispMassgFctMassgProg', 0, timeout=0.5)
        # self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'DrvrSeatDispMassgFctMassgInten', 3)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'PassSeatDispMassgFctOnOff', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'PassSeatDispMassgFctMassgProg', 0, timeout=0.5)
        # self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'PassSeatDispMassgFctMassgInten', 3)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetMassageConf",{"seats": [0,1]},
                                        {"out": [{"id": 0,"conf": {"isOn": False, "type": 0, "intensity": 3}},
                                                    {"id": 1,"conf": {"isOn": False, "type": 0, "intensity": 3}}]})
        # 校验方向盘加热关闭
        # todo: 查看下行pdu 6151 SteerWhlHeatgOnReq=0
        # 校验前排空调总开关-开启
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {},
                                              {"out": {"firstRowPowerStatus": True}})
        # 校验AC状态-on
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAC", {}, {"out": True})
        # 校验AUTO-zoneid=0-on=true
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateAuto", {"zoneId": 0},
                                              {"out": {"zoneId": 0, "isOn": True}})
        # 校验内外循环Auto-mode=1
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        # 校验温度同步设置，on=True
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        # 校验主驾、副驾、后排温度控制22摄氏度
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetTargetTemperature", {"zoneId": 3},
                                              {"out": {"zoneId": 3, "value": 22.0, "isValid": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetTargetTemperature", {"zoneId": 4},
                                              {"out": {"zoneId": 4, "value": 22.0, "isValid": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetTargetTemperature", {"zoneId": 2},
                                              {"out": {"zoneId": 2, "value": 22.0, "isValid": True}})
        # 校验风量zoneId=@value(1) kFirstRow speed=@value(12) kLvlAutoNormal
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1},
                                              {"out": {"zoneId": 1, "speed": 12}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2},
                                              {"out": {"zoneId": 2, "speed": 12}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT,"GetClimateMode",{},{"out": 2})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT,"GetClimateSystemStatus",{},{"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":1,"isWindModeAuto":True},
                                                "airModePassenger":{"mode":1,"isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1,"isWindModeAuto":True},"firstRowPowerStatus": True,"secondRowPowerStatus": True}})
        # 校验前挡风玻璃除雾-关闭
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFastDefrostMode", {}, {"out": False})
        # 校验后挡风玻璃除雾-Id=@value(2) kShieldWindowRear status=@value(0) kHeatStatusOff
        self.partner.send_request_and_ck_resp(SHIELDWINDOW_SERVICE_CLIENT, "GetHeat", {"windows": [2]},
                                              {"out": [{"id": 2, "status": 0}]})
        # 校验PM25一键过滤=false
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetPM25", {}, {"out": False})
        # 校验清除异味=false
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCockpitCleanMode", {}, {"out": False})
        # 校验主驾、副驾、后排吹风模式zoneId=3,4,2 mode=7
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr46, 'HmiCmptmtAirDistbnFrntLe', 7, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr46, 'HmiCmptmtAirDistbnFrntRi', 7, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr46, 'HmiCmptmtAirDistbnRe', 7, timeout=0.5)
        
        #检查空调出风口控制
        location_to_number= {"第一排左左":8,"第一排左右":9,"第一排右左":10,"第一排右右":11,"第二排左左":12}
        name_list1 = ["第一排左左","第一排左右","第一排右左","第一排右右","第二排左左"]
        for name_1 in name_list1:
            logger.info(f"获取接口_GetAirVent_{name_1}状态")
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT,"GetAirVent",args={"zoneId":location_to_number[name_1]},ck_info={"out":1}) 
        #检查方向调节各区域
        name_to_signal = {"第一排左侧左":["HmiElecAirDirCrtlReqDrvrLePosX","HmiElecAirDirCrtlReqDrvrLePosY"],
                    "第一排左侧右":["HmiElecAirDirCrtlReqDrvrRiPosX","HmiElecAirDirCrtlReqDrvrRiPosY"],
                    "第一排右侧左":["HmiElecAirDirCrtlReqPassLePosX","HmiElecAirDirCrtlReqPassLePosY"],
                    "第一排右侧右":["HmiElecAirDirCrtlReqPassRiPosX","HmiElecAirDirCrtlReqPassRiPosY"],
                    "第二排左":["HmiReElecAirDirCrtlReqSecRowLePosX","HmiReElecAirDirCrtlReqSecRowLePosY"]}
        location_to_number={"第一排左":3,"第一排右":4,"第二排左":2}
        for name,singal_list in name_to_signal.items():
            side =0 if name[-1]=="左" else 1
            zoneId = location_to_number[name[:4]]
            logger.info(f"校验信号")
            if "第二排" not in name:
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr49,singal_list[0],100)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr49,singal_list[1],100)
            else:
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10,singal_list[0],100)
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10,singal_list[1],100)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT,"GetOutletAngle",{"zoneId":zoneId},ck_info={"out":[{"id":zoneId,"side":side,"horizontal":50,"vertical":50}]}) 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetClimateAuto",{"zoneId": 0, "on": False})
        sleep(1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT,"GetClimateSystemStatus",{},{"out":{
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":6,"isWindModeAuto":False},
                                                "airModePassenger":{"mode":4,"isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":4,"isWindModeAuto":False},"firstRowPowerStatus": True,"secondRowPowerStatus": True}})

    @allure.title("获取随车项恢复出厂设置执行结果_默认值")
    @pytest.mark.sanity
    @pytest.mark.restart
    def test_caseid_108972(self):
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        sleep(5)
        self.partner.send_request_and_ck_resp(RESETSOAVONFIG_SERVICE_CLIENT, "GetResetAllVehicleSOAConfigResult", {},
                                              {"out": 0})
        
    @allure.title("manual到auto状态机下恢复出厂设置")
    @pytest.mark.sanity
    def test_caseid_1985926(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetClimateAuto",{"zoneId": 0, "on": False})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindMode",{"zoneId":2,"mode":1})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindMode",{"zoneId":3,"mode":1})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindMode",{"zoneId":4,"mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindSpeed",{"zoneId":1,"speed":4})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindSpeed",{"zoneId":2,"speed":4})
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetClimateAuto",{"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindSpeed",{"zoneId":1,"speed":14})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindSpeed",{"zoneId":2,"speed":14})
        sleep(1)
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)
        sleep(1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT,"GetClimateSystemStatus",{},{"out":{
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":2,"isWindModeAuto":True},
                                                "airModePassenger":{"mode":2,"isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2,"isWindModeAuto":True},"firstRowPowerStatus": True,"secondRowPowerStatus": True}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetClimateAuto",{"zoneId": 0, "on": False})
        sleep(0.1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT,"GetClimateSystemStatus",{},{"out":{
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":6,"isWindModeAuto":False},
                                                "airModePassenger":{"mode":4,"isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":4,"isWindModeAuto":False},"firstRowPowerStatus": True,"secondRowPowerStatus": True}})

    @allure.title("设置随车项恢复出厂设置_续航里程&加热优先级")
    @pytest.mark.smoke
    def test_caseid_1988612(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:2,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr04, 'HvBattEgyCdn', 99.0)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 100.0)
        self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetRange",
                                            {"infos": {"type": 1, "CLTCRange": 999, "estimatedRange": 999}})
        self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetAveragePowerConsume", {"power": 50})
        sleep(3)
        self.restart_bgm_and_connect_service(HIGHVOLTAGE_SERVICE_CLIENT)
        sleep(1)
        self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetRange",
                                            {"infos": {"type": 1, "CLTCRange": 500, "estimatedRange": 500}})
        self.ck_CLTCRange_estimatedRange_GetResponse(0,self.CltcKm(880,100,99),500)
        self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetRange",
                                            {"infos": {"type": 1, "CLTCRange": 65535, "estimatedRange": 65535}})
        self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetAveragePowerConsume", {"power": 20})
        sleep(0.5)
        logger.info(f"计算CLTC值为{self.CltcKm(880,100,99)}===估计值{self.EstimateKm(98.7,100,99,20)}")
        self.ck_CLTCRange_estimatedRange_GetResponse(1,self.CltcKm(880,100,99),self.EstimateKm(98.7,100,99,20))
        #前置条件
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetRange",
                                        {"infos": {"type": 1, "CLTCRange": 500, "estimatedRange": 500}})
        sleep(1)
        self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetHeatingPriority", {"req": 2})
        self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr01, 'HvBattClimaPrioReq', 1, timeout=1)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetRange", {},{"out": {"type":1,"CLTCRange":self.CltcKm(880,100,99),"estimatedRange":500}})
        self.partner.empty_all()
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)
        self.partner.ck_s2s_event(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfigResult", {"sts": 2},timeout=4)
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "NotifyRange", 
                                  {"infos": {"source": 1,"type":0,"CLTCRange":self.CltcKm(880,100,99),"estimatedRange": self.EstimateKm(98.7,100,99,20)}})
        self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr01, 'HvBattClimaPrioReq', 0, timeout=1)
        self.restart_bgm_and_connect_service(RESETSOAVONFIG_SERVICE_CLIENT)
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "NotifyRange", 
                                  {"infos": {"source": 1,"type":0,"CLTCRange":self.CltcKm(880,100,99),"estimatedRange": self.EstimateKm(98.7,100,99,20)}},timeout=7)
        self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr01, 'HvBattClimaPrioReq', 0, timeout=1)

    @allure.title("设置随车项恢复出厂设置_充电目标SOC")
    @pytest.mark.sanity
    def test_caseid_1988597(self):
        info={25:1000,24:900,23:1000,16:900}
        for key,value in info.items():
            self.sd_tester.write_single_ccp(566, key)
            sleep(3)
            self.restart_bgm_and_connect_service(HIGHVOLTAGE_SERVICE_CLIENT)
            sleep(10)#重启后就resetSOA会存在服务还没有连上的情况
            logger.info(f"写入CCP566为{key}")
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetChargeSoc", {"soc": 50})
            self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr12, 'LocalBookChrgnTarVal', 500, timeout=3)
            sleep(5)
            self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)
            self.partner.ck_s2s_event(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfigResult", {"sts": 2},timeout=4)
            self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr12, 'LocalBookChrgnTarVal', value, timeout=1)
            self.restart_bgm_and_connect_service(HIGHVOLTAGE_SERVICE_CLIENT)    
            sleep(1)
            self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr12, 'LocalBookChrgnTarVal', value, timeout=1)    

    @allure.title("设置随车项恢复出厂设置_空调_校验周期100ms")
    @pytest.mark.smoke
    def test_caseid_1988618(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)#auto，除霜除雾吹风模式
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode", {"isOpen": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetACInhibit", {"isOn": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":0})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 2})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 22})
        self.partner.empty_all()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":3})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":3})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 3, 
                                                "windSpeedSecRow":3, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 2})
        self.partner.empty_all()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":13})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":13})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 13, 
                                                "windSpeedSecRow":13, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})

        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        self.partner.empty_all()
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4}})
        time1=time.time() #check总线时会存在晚校验到，结果导致差值过小
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12}})
        time2=time.time()
        logger.info(f"差值为{time2-time1}")
        assert 0.05<time2-time1<0.23 #开发这里需要等待第一个操作设置成功后再等100ms

    @allure.title("设置随车项恢复出厂设置_空调")
    @pytest.mark.smoke
    def test_caseid_1988617(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)#auto，除霜除雾吹风模式
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode", {"isOpen": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetACInhibit", {"isOn": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":0})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 2})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 22})
        self.partner.empty_all()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":3})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":3})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 3, 
                                                "windSpeedSecRow":3, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 2})
        self.partner.empty_all()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":13})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":13})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 13, 
                                                "windSpeedSecRow":13, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})

        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        self.partner.empty_all()
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)
        self.partner.ck_s2s_event(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfigResult", {"sts": 2})
        sleep(1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                    "windSpeedSecRow":12, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                    "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                    "airModeSecRow":{"mode":2, "isWindModeAuto":True}, 
                                                    "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.partner.empty_all()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":6, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":4, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":4, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                    "windSpeedSecRow":4, "airModeDriver":{"mode":6, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":4, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":4, "isWindModeAuto":False}, 
                                                    "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
        sleep(2)
        self.restart_bgm_and_connect_service(RESETSOAVONFIG_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":6, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":4, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":4, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}},timeout=5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                    "windSpeedSecRow":4, "airModeDriver":{"mode":6, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":4, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":4, "isWindModeAuto":False}, 
                                                    "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.empty_all()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                    "windSpeedSecRow":12, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                    "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                    "airModeSecRow":{"mode":2, "isWindModeAuto":True}, 
                                                    "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        
    @allure.title("设置随车项恢复出厂设置_高压电池加热_校验周期100ms")
    @pytest.mark.sanity
    def test_caseid_1988614(self):
        self.sd_tester.write_single_ccp(973,2) #交直流都支持
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0) 
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(3)
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        sleep(2)
        self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetBatteryHeating", {"type": 1,  "on":  True , "value": 0})
        sleep(0.2)
        self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetBatteryHeating", {"type": 5,  "on":  True , "value": 0})
        sleep(3)#重启有波动
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(1)
        self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetBatteryHeating", {"type": 5,  "on":  True , "value": 0})
        sleep(1)
        self.check_SetBatteryHeating(remReq=0, remTarT=80, remReqFromAC=1, remTarTFromAC=80, localTarT=80)
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)
        self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr01, 'LocalHvBattThermTarT', 0) #此时远程温度为last value
        time1=time.time()
        self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr01, 'RemHvBattHeatgTarT', 0,timeout=0.5)
        time2=time.time()
        logger.info(f"差值为{time2-time1}")
        assert 0.05<time2-time1<0.21 #总线校验过慢，日志显示在100ms大一点

    @allure.title("设置随车项恢复出厂设置_高压电池加热")
    @pytest.mark.sanity
    def test_caseid_1988577(self):
        self.sd_tester.write_single_ccp(973,2) #交直流都支持
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0) 
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        sleep(3)
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        sleep(2)
        self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetBatteryHeating", {"type": 1,  "on":  True , "value": 0})
        sleep(0.2)
        self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetBatteryHeating", {"type": 5,  "on":  True , "value": 0})
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) 
        sleep(1)
        self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetBatteryHeating", {"type": 5,  "on":  True , "value": 0})
        sleep(1)
        self.check_SetBatteryHeating(remReq=0, remTarT=80, remReqFromAC=1, remTarTFromAC=80, localTarT=80)
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)
        
        self.partner.ck_s2s_event(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfigResult", {"sts": 2})
        self.partner.empty_all()
        self.check_SetBatteryHeating(remReq=0, remTarT=0, remReqFromAC=0, remTarTFromAC=0, localTarT=0)#事件帧过快，直接校验最终状态，校验tcpdump的case观察中间态
        sleep(2)
        self.check_SetBatteryHeating(remReq=0, remTarT=0, remReqFromAC=0, remTarTFromAC=0, localTarT=0)
        self.restart_bgm_and_connect_service(RESETSOAVONFIG_SERVICE_CLIENT)
        self.check_SetBatteryHeating(remReq=0, remTarT=0, remReqFromAC=0, remTarTFromAC=0, localTarT=0)

    @allure.title("设置随车项恢复出厂设置_高压放电&预约充电")
    @pytest.mark.sanity
    def test_caseid_1988575(self):
        self.sd_tester.write_single_ccp(973,2) #交直流都支持
        sleep(3)
        nowtime=current_time_with_seconds_zero_to_timestamp() #去零后最多会少59秒
        logger.info("现在时间是:{}".format(nowtime))
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0) 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr32, 'BookChrgnStsFb', 1) #反馈正常
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 0, "source": 0, "timeInfo": {"startTime": nowtime+120, "endTime": nowtime+360, 
                                                "repeatType": 1},"isToTargetSOCStop": False}},timeout=3)
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', 2) #请求预约充电回馈状态
        sleep(1)
        self.restart_bgm_and_connect_service(HIGHVOLTAGEAPP_SERVICE_CLIENT)
        sleep(2)
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, 
                                              "GetVehicleTimeInfo",{},{"out":{"SynchronizationStatus": 3}},timeout=10)
        sleep(1)
        self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetDischargeLimitSoc", {"soc": 10})
        # self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr07, 'DchaChrgnTarVal', 100, timeout=0.5) #V2.2修复
        self.partner.send_method_request(HIGHVOLTAGEAPP_SERVICE_CLIENT, "SetACBookCharging",
                                          {"cmd": {"type": 1, "source": 0, "timeInfo": {"startTime": nowtime+240, "endTime": nowtime+720, 
                                                "repeatType": 1},"isToTargetSOCStop": False}},timeout=3)
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":1,"workSts":2,
                                                                    "info":{"startTime":nowtime+240,"endTime":nowtime+720,"repeatType":1},
                                                                    "isToTargetSOCStop":False}}})
        self.partner.empty_all()
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)
        
        self.partner.ck_s2s_event(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfigResult", {"sts": 2})
        self.partner.ck_s2s_event(HIGHVOLTAGEAPP_SERVICE_CLIENT, "BookChargingInfo",{"info":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":1609509600,"endTime":1609538400,"repeatType":0},
                                                                    "isToTargetSOCStop":False}}},timeout=7) #需求更改
        self.partner.send_request_and_ck_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT, "GetBookChargingInfo", {},
                                              {"out":{"acInfo":{"source":0,"reqSts":3,"workSts":1,
                                                                    "info":{"startTime":1609509600,"endTime":1609538400,"repeatType":0},
                                                                    "isToTargetSOCStop":False}}},timeout=2)
        sleep(1)
        now = datetime.datetime.now()
        todaymorning=now.replace(hour=8, minute=0, second=0, microsecond=0)
        todaymorning8 = int(todaymorning.timestamp())
        logger.info(f"当天早上8点为{todaymorning8}")
        mark1=todaymorning8+14*60*60
        mark2=todaymorning8+22*60*60
        logger.info(f"通知的当天开始时间为{mark1}且结束时间为{mark2}")
        #时间同步后上报当天的22点到次日6点
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr07, 'DchaChrgnTarVal', 200, timeout=0.5) #V2.2修复
        self.restart_bgm_and_connect_service(RESETSOAVONFIG_SERVICE_CLIENT)
        self.partner.empty_all()    
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",{"info":{"SynchronizationStatus": 3}},timeout=10)
        sleep(0.5)  
        starttime1 = self.partner.return_latest_event(HIGHVOLTAGEAPP_SERVICE_CLIENT,
                                                      "BookChargingInfo")["info"]['acInfo']["info"]['startTime']
        sleep(0.5)
        endtime1 = self.partner.send_request_and_return_resp(HIGHVOLTAGEAPP_SERVICE_CLIENT,
                                                                      "GetBookChargingInfo", {})["out"]['acInfo']["info"]['endTime']
        assert  starttime1== mark1 or mark1 ==starttime1+86400
        assert  endtime1== mark2 or mark2 ==endtime1+86400 #x需求规定只需要校验是否是22:00即可 SOA-29495

    @allure.title("设置随车项恢复出厂设置_空调ECO模式+悬架高度")
    @pytest.mark.smoke
    def test_caseid_1989384(self):
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsModAct', 0)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'StsLvlReqRsn', 0)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetEcoMode', {"on": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'HMIClimaEgySaveReq', 1, timeout=0.5)
        self.partner.send_method_request(SUSPENSION_SERVICE_CLIENT, "SetAirSuspensionHeightConfig",
                                          {"configCmd": {"sourceId":10000,"heightCmd":[{"suspensionId":255,"heightLevelCmd":1}]}})
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, 'HeiReqOfFLHeightLevelReq', 4, timeout=0.5)
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, 'HeiReqOfFRHeightLevelReq', 4, timeout=0.5)
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, 'HeiReqOfRLHeightLevelReq', 4, timeout=0.5)
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, 'HeiReqOfRRHeightLevelReq', 4, timeout=0.5)
        sleep(1)
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, 'HeiReqOfFLHeightLevelReq', 5, timeout=2) #不确定什么时候调用底盘服务
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, 'HeiReqOfFRHeightLevelReq', 5, timeout=2)
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, 'HeiReqOfRLHeightLevelReq', 5, timeout=2)
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr04, 'HeiReqOfRRHeightLevelReq', 5, timeout=2)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'HMIClimaEgySaveReq', 0, timeout=0.5)
        
    @allure.title("设置随车项恢复出厂设置_洗车模式&拖车模式&露营模式")
    @pytest.mark.sanity
    def test_caseid_1988574(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0)        
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)    #拖车模式不能连枪
        sleep(1) 
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_usage_mode(11)
        self.partner.send_method_request(CONDITIONCHECK_SERVICE_CLIENT, "SetTowModeConfirm", {"isOn": False}, timeout=1)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.seat_belt_status(0,0,0,0,0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        sleep(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}, timeout=2)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        sleep(0.2)
        self.partner.send_method_request(CONDITIONCHECK_SERVICE_CLIENT, "SetTowModeConfirm", {"isOn": False}, timeout=1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        sleep(1)
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_internal_has_key()
        sleep(1)
        self.partner.send_method_request(CONDITIONCHECK_SERVICE_CLIENT, "SetTowModeConfirm", {"isOn": True}, timeout=1)
        logger.info(f"2222222")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 9)
        sleep(1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "TowModeStatus", {"info": {"sts": 2}})
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "TowModeStatus", {"info": {"sts": 3}})
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True})
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":1,"reason":0}})
        self.partner.empty_all()
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)
        
        self.partner.ck_s2s_event(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfigResult", {"sts": 2})
        self.partner.empty_all()
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":0,"reason":1}})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT,"GetTowModeStatus", {},  {"out": {"sts": 5}})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        sleep(1)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":0,"reason":1}})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT,"GetTowModeStatus", {},  {"out": {"sts": 1}})#回6后回1

        self.restart_bgm_and_connect_service(RESETSOAVONFIG_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "TowModeStatus", {"info": {"sts": 1}},timeout=5)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT, "NotifyWashModeSts", {"sts": False},timeout=10)
        sleep(1)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":0,"reason":0}})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT,"GetTowModeStatus", {},  {"out": {"sts": 1}})

    @allure.title("设置随车项恢复出厂设置_12V延时")
    @pytest.mark.sanity
    def test_caseid_1988573(self):
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 9.0)
        sleep(2)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        #进入keeping
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"PowerOutletDelayInfo",{"sts": 
                                                {"delaySts":2, "delayTimeLeft":65535 ,"modeStsSet":2 ,"lastSetTime":2 ,"reason":0}})
        self.partner.empty_all()
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)
        
        self.partner.ck_s2s_event(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfigResult", {"sts": 2})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"PowerOutletDelayInfo",{"sts": 
                                                {"delaySts":0, "delayTimeLeft":65535 ,"modeStsSet":0 ,"lastSetTime":2 ,"reason":1}},timeout=3)
        self.restart_bgm_and_connect_service(RESETSOAVONFIG_SERVICE_CLIENT)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"PowerOutletDelayInfo",{"sts": 
                                                {"delaySts":0, "delayTimeLeft":65535 ,"modeStsSet":0 ,"lastSetTime":2 ,"reason":0}},timeout=10)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetPowerOutletDelayInfo", {}, 
                                                {"out": {"delaySts":0, "delayTimeLeft":65535 ,"modeStsSet":0 ,"lastSetTime":2 ,"reason":0}})

    @allure.title("设置随车项恢复出厂设置_内灯恢复自动")
    @pytest.mark.sanity
    def test_caseid_1988572(self):
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "InternalLightMode", {"sts": 1})
        self.partner.empty_all()
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)
        self.partner.ck_s2s_event(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfigResult", {"sts": 2})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "InternalLightMode", {"sts": 2})
        self.restart_bgm_and_connect_service(RESETSOAVONFIG_SERVICE_CLIENT)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "InternalLightMode", {"sts": 2})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 2})


    @allure.title("获取随车项恢复出厂设置执行结果_重置中")
    @pytest.mark.sanity
    def test_caseid_108974(self):
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)
        self.partner.ck_s2s_event(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfigResult", {"sts": 1})
        sleep(2)

    @allure.title("获取随车项恢复出厂设置执行结果_失败")
    @pytest.mark.sanity
    def test_caseid_1988584(self):
        self.kill_bgm_process()
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=5.5) #必然超时
        try:
            self.partner.ck_s2s_event(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfigResult", {"sts": 3},timeout=15)
            self.partner.send_request_and_ck_resp(RESETSOAVONFIG_SERVICE_CLIENT, "GetResetAllVehicleSOAConfigResult", {},
                                                {"out": 3}, timeout=1)
        except Exception as e:
            assert False
        else:
            assert True

    @allure.title("设置随车项恢复出厂设置_近车解锁开门和离车关门落锁设置项默认关闭")
    @pytest.mark.sanity
    @pytest.mark.restart
    def test_caseid_1984723(self):
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 1, "value": 1},
                                                                                         {"key": 3, "value": 1}]})
        sleep(1)
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)#因最近服务注册过多，需要确认超过5S是否可靠
        sleep(1)
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetConfigInfo", {}, {"out": [{"key": 1, "value": 0},
                                                                                                {"key": 3, "value": 0}]})
        self.restart_bgm_and_connect_service(RESETSOAVONFIG_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetConfigInfo", {}, {"out": [{"key": 1, "value": 0},
                                                                                                {"key": 3, "value": 0}]})
        
    @allure.title("首次出厂_恢复出厂设置执行结果的情况")
    @pytest.mark.full
    def test_caseid_1985947(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)#auto，除霜除雾吹风模式
        # 删除数据库
        self.del_s2s_db()
        sleep(2)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        sleep(5) #删除数据库后重启BGM resetSOA因注册服务过多会存在超时4.5的调用
        #获取空调首次下线设置
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {},
                                              {"out":{"acStatus": True, "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22,
                                                       "windSpeedFirRow": 12, "windSpeedSecRow":12,"airModeDriver":{"isWindModeAuto":True}, 
                                                       "airModePassenger":{"isWindModeAuto":True}, 
                                                "airModeSecRow":{"isWindModeAuto":True},"firstRowPowerStatus": True,"secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {},{"out":2})
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)
        self.partner.empty_all(3)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetClimateAuto",{"zoneId": 0, "on": False})
        sleep(1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT,"ClimateSystemStatus", {"status":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":6,"isWindModeAuto":False},
                                                "airModePassenger":{"mode":4,"isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":4,"isWindModeAuto":False},
                                                "firstRowPowerStatus": True,"secondRowPowerStatus": True}})#需求改为False
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT,"GetClimateSystemStatus",{},{"out":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":6,"isWindModeAuto":False},
                                                "airModePassenger":{"mode":4,"isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":4,"isWindModeAuto":False},
                                                "firstRowPowerStatus": True,"secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT,"GetCycleMode",{},{"out": 3})#manual下为3外循环
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {},{"out":1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT,"GetAutoSyncMode",{},{"out": True}) #温度同步
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'HMIClimaEgySaveReq', 0, timeout=0.5) #节能模式关闭
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr46, 'HmiFragraLvlReq', 0, timeout=0.5) #香氛
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'TelmAirFragTasteReq', 0, timeout=0.5) #香氛
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh1', 0, timeout=0.5) #香氛
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh2', 0, timeout=0.5) #香氛
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh3', 0, timeout=0.5) #香氛
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAirVent", {"zoneId":8},{"out":True}) #风口
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAirVent", {"zoneId":9},{"out":True})#风口
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAirVent", {"zoneId":10},{"out":True})#风口
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAirVent", {"zoneId":11},{"out":True})#风口
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAirVent", {"zoneId":12},{"out":True})#风口
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetOutletStatus",{}, {"out":{"driverVentStatus":{"mode":0, "leftHorizontal":50,
                                                                                "leftVertical":50, "rightHorizontal":50,"rightVertical":50},
                                                                               "passVentStatus": {"mode":0, "leftHorizontal":50,"leftVertical":50,"rightHorizontal":50,"rightVertical":50},
                                                                               "secRowVentStatus":{"mode": 0,"leftHorizontal":50,"leftVertical":50,"rightHorizontal":50,"rightVertical":50}}})

    @allure.title("ResetSOAConfigService服务重启默认值")
    @pytest.mark.full
    def test_caseid_1984584(self):
        self.ipdu.pause_all_bus_send()
        self.nucapp.bgm_power_off()
        sleep(2)
        self.nucapp.bgm_power_on()
        sleep(10)
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfigResult", {"sts": 0})

    @allure.title("获取随车项恢复出厂设置执行结果_重置完成")
    @pytest.mark.full
    def test_caseid_108973(self):
        sleep(2)#会收到上个case重启影响，导致接口调用超时
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)
        self.partner.ck_s2s_event(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfigResult", {"sts": 2},timeout=5)#重置完成需要花费时间
        self.partner.send_request_and_ck_resp(RESETSOAVONFIG_SERVICE_CLIENT, "GetResetAllVehicleSOAConfigResult", {},
                                              {"out": 2}, timeout=2)
        
    @allure.title("设置随车项恢复出厂设置_无线充电开关默认打开")
    @pytest.mark.sanity
    def test_caseid_1987967(self):
        self.partner.send_method_request(WIRELESScharging_CLIENT, "SetWirelessCharging", {"req":[{"zone":2 ,"isOn": False}]})
        sleep(1)
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmi', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmiPass', 0, timeout=0.5)
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)
        sleep(1)
        self.partner.ck_s2s_event(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfigResult", {"sts": 2},timeout=4)
        self.partner.send_request_and_ck_resp(RESETSOAVONFIG_SERVICE_CLIENT, "GetResetAllVehicleSOAConfigResult", {},
                                              {"out": 2}, timeout=2)
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmi', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmiPass', 1, timeout=0.5)
        self.restart_bgm_and_connect_service(RESETSOAVONFIG_SERVICE_CLIENT)
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmi', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmiPass', 1, timeout=0.5)

    @allure.title("设置随车项恢复出厂设置_近车解锁开门和离车关门落锁设置项默认关闭")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1960024(self):
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 1},
                                                                                         {"key": 1, "value": 1},
                                                                                         {"key": 3, "value": 1},
                                                                                         {"key": 4, "value": 1},
                                                                                         {"key": 5, "value": 1}]})
        sleep(1)
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetConfigInfo", {}, {"out": [{"key": 0, "value": 1},
                                                                                                {"key": 1, "value": 1},
                                                                                                {"key": 3, "value": 1},
                                                                                                {"key": 4, "value": 1},
                                                                                                {"key": 5, "value": 1}]})
        self.restart_bgm_and_connect_service(RESETSOAVONFIG_SERVICE_CLIENT)
        sleep(3)#重启后如果进行ResetAllVehicleSOAConfig会超时，需要加大延时，因为此接口注册服务过多
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetConfigInfo", {}, {"out": [{"key": 0, "value": 1},
                                                                                                {"key": 1, "value": 1},
                                                                                                {"key": 3, "value": 1},
                                                                                                {"key": 4, "value": 1},
                                                                                                {"key": 5, "value": 1}]})
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)
        sleep(1)
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetConfigInfo", {}, {"out": [{"key": 0, "value": 0},
                                                                                                {"key": 1, "value": 0},
                                                                                                {"key": 3, "value": 0},
                                                                                                {"key": 4, "value": 1},
                                                                                                {"key": 5, "value": 1}]})
        self.restart_bgm_and_connect_service(RESETSOAVONFIG_SERVICE_CLIENT)
        sleep(1)
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetConfigInfo", {}, {"out": [{"key": 0, "value": 0},
                                                                                                {"key": 1, "value": 0},
                                                                                                {"key": 3, "value": 0},
                                                                                                {"key": 4, "value": 1},
                                                                                                {"key": 5, "value": 1}]})
        
@allure.feature("SOA服务接口")
@allure.story("BGM应用/ResetSOAConfigService")
class TestResetSOAConfigServiceAll(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("HighVoltageService", "client"),
                                    ("DoorService", "client"),
                                    ("ChassisService", "client"),
                                    ("EntryService", "client"),
                                     ("WirelessPhoneChargingService", "client"),("ChargeLidService", "client"),
                                     ("LightService", "client"),
                                     ("OuterRearViewService", "client"),
                                     ("WiperService", "client"),
                                     ("WindowAppService", "client"),
                                     ("TailWingService", "client"),
                                     ("SeatService", "client"),
                                     ("SteerWheelService", "client"),
                                     ("HighVoltageAppService", "client"),
                                     ("ClimateControlService", "client"),
                                     ("CentralLockService", "client"),
                                     ("KeyService", "client"),
                                     ("VehicleSetStatusService", "client"),
                                     ("ConditionCheckService", "client"),
                                     ("HornService", "client"),
                                     ("ResetSOAConfigService", "client")])
        self.partner.method_default_timeout = 3 #resetSOA注册服务多，可以适当放开
        self.sd_tester.tester_present()
        self.io.set_four_door_close()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.sd_tester.stop_tester_present()
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
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe', 1)
        self.ipdu.rx_flag_reset_all()
        self.ipdu.reset_check_results()
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(2)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    @allure.title("设置随车项恢复出厂设置_筛查所有服务设置项")
    @pytest.mark.full
    def test_caseid_1988651(self):
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 1,"source": 2})
        self.partner.empty_all(5)
        self.partner.send_method_request(RESETSOAVONFIG_SERVICE_CLIENT, "ResetAllVehicleSOAConfig", {},timeout=4)
        sleep(10)