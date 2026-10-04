#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_WTIService_Climate.py
@Time         :2023/04/08 17:20:31
@Author       :tao.cheng_ext@jiduauto.com
@Description : Test SOA for WTIService_Climate
"""

import random
import allure
import pytest
import copy
from time import sleep
from random import randint
from xat_ecu.legacy.common.data_type_handing import logger
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.soa.case_helper.test_base import TestBase


@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIService_Climate")
class TestWTIService_Climate(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("WTIService", "client"),("ClimateControlService", "client"),])
        self.partner.method_default_timeout = 0.1
        self.sd_tester.tester_present()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.partner.stop_operators()
        self.sd_tester.stop_tester_present()
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
        sleep(1)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.airvent_no_fault()
        self.partner.empty_all(0.5)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def airvent_no_fault(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr62, 'VentnActr01BlckSts_1_CcmBodySignalIPdu62',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr62, 'VentnActr01ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr62, 'VentnActr02BlckSts',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr62, 'VentnActr02ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr63, 'VentnActr03BlckSts_1_CcmBodySignalIPdu63',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr63, 'VentnActr03ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr63, 'VentnActr04BlckSts',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr63, 'VentnActr04ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr64, 'VentnActr05BlckSts_1_CcmBodySignalIPdu64',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr64, 'VentnActr05ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr64, 'VentnActr06BlckSts',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr64, 'VentnActr06ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr65, 'VentnActr07BlckSts_1_CcmBodySignalIPdu65',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr65, 'VentnActr07ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr65, 'VentnActr08BlckSts',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr65, 'VentnActr08ElecErr',0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05,'BltLockStAtDrvrBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtPassBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 0)
        sleep(1)
        
    @allure.title("前排出风口调节故障") 
    @pytest.mark.sanity
    def test_caseid_1979976(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr63, 'VentnActr04BlckSts',1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr65, 'VentnActr08BlckSts',1)
        sleep(20)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Front Vent Adjustment Error", "info": "0"}]})
        sleep(20)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Front Vent Adjustment Error", "info": "0"}]})
        sleep(21)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Front Vent Adjustment Error", "info": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Front Vent Adjustment Error", "info": "1"}]})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr63, 'VentnActr04BlckSts',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr65, 'VentnActr08BlckSts',0)
        sleep(1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Front Vent Adjustment Error", "info": "0"}]})
        #其他信号造故障
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr64, 'VentnActr06BlckSts',1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr63, 'VentnActr04BlckSts',1)
        sleep(20)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Front Vent Adjustment Error", "info": "0"}]})
        sleep(20)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Front Vent Adjustment Error", "info": "0"}]})
        sleep(21)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Front Vent Adjustment Error", "info": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Front Vent Adjustment Error", "info": "1"}]})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr64, 'VentnActr06BlckSts',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr63, 'VentnActr04BlckSts',0)
        sleep(1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Front Vent Adjustment Error", "info": "0"}]})

    @allure.title("前排出风口调节产生故障恢复故障") 
    @pytest.mark.full
    def test_caseid_1987930(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr63, 'VentnActr04BlckSts',1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr64, 'VentnActr06BlckSts',1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr65, 'VentnActr08BlckSts',1)
        sleep(40)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr64, 'VentnActr05BlckSts',1)
        sleep(20)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Front Vent Adjustment Error", "info": "1"}]})
        sleep(40)
        self.partner.ck_no_event(WTI_SERVICE_CLIENT, "WarningMsgList")
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr64, 'VentnActr05BlckSts',0)
        self.partner.ck_no_event(WTI_SERVICE_CLIENT, "WarningMsgList")
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Front Vent Adjustment Error", "info": "1"}]})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr63, 'VentnActr04BlckSts',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr64, 'VentnActr06BlckSts',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr65, 'VentnActr08BlckSts',0)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Front Vent Adjustment Error", "info": "0"}]})
 
    @allure.title("后排出风口调节故障") 
    @pytest.mark.sanity
    def test_caseid_1979977(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr66, "VentnActr09BlckSts",0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr66, "VentnActr09ElecErr",0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr66, "VentnActr10BlckSts",0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr66, "VentnActr10ElecErr",0)
        self.partner.empty_all(1)
        for siginal in ["VentnActr09BlckSts","VentnActr09ElecErr","VentnActr10BlckSts","VentnActr10ElecErr"]:
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr66, siginal,1)
            sleep(20)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Rear Vent Adjustment Error", "info": "0"}]})
            sleep(20)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Rear Vent Adjustment Error", "info": "0"}]})
            sleep(21)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Rear Vent Adjustment Error", "info": "1"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Rear Vent Adjustment Error", "info": "1"}]})
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr66, siginal,0)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Rear Vent Adjustment Error", "info": "0"}]})

    @allure.title("遍历_内外循环风门故障") 
    @pytest.mark.sanity
    def test_caseid_1979978(self):
        info = {1:"1",0:"0"}
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr61, 'HvacRecFlapActrErr', 0)
        self.partner.empty_all(0.5)
        for key,value in info.items():
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr61, 'HvacRecFlapActrErr', key)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Circulation Motor Error", "info": value}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Circulation Motor Error", "info": value}]})

    @allure.title("遍历_前排吹风模式故障") 
    @pytest.mark.sanity
    def test_caseid_1979979(self):
        info = {1:"1",0:"0"}
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr61, 'HvacModFlapActrErrFrstRowLe', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr61, 'HvacModFlapActrErrFrstRowRi', 0)
        self.partner.empty_all(0.5)
        for key,value in info.items():
            logger.info(f"----发送HvacModFlapActrErrFrstRowRi为{key}")
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr61, 'HvacModFlapActrErrFrstRowRi', key)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Front Mode Motor Error", "info": value}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Front Mode Motor Error", "info": value}]})
        for key,value in info.items():
            logger.info(f"----发送HvacModFlapActrErrFrstRowLe为{key}")
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr61, 'HvacModFlapActrErrFrstRowLe', key)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Front Mode Motor Error", "info": value}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Front Mode Motor Error", "info": value}]})
        for key,value in info.items():
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr61, 'HvacModFlapActrErrFrstRowRi', key)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr61, 'HvacModFlapActrErrFrstRowLe', key)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Front Mode Motor Error", "info": value}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Front Mode Motor Error", "info": value}]})

    @allure.title("遍历_PM2.5系统故障") 
    @pytest.mark.sanity
    def test_caseid_1979980(self):
        info = [(3,"1"),(0,"0"),(3,"1"), (1,"0"), (3,"1"), (2,"0")]
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'IntPm25StsFrmClima', 0)
        self.partner.empty_all(0.5)
        for item in info:
            logger.info(f"-----发送信号值{item[0]}")
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'IntPm25StsFrmClima', item[0])
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"PM2.5 System Error", "info": item[1]}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"PM2.5 System Error", "info": item[1]}]})

    @allure.title("遍历_空气质量管理系统故障") 
    @pytest.mark.sanity
    def test_caseid_1979981(self):
        def info(input):
            return "0" if input == 0 else "1"
        def info2(input2):
            return "0" if input2 == 0 or input2 == 1 else "1"
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetClimateAuto",{"zoneId": 0, "on": False})
        for Y in [2,11,13]:
            self.sd_tester.change_usage_mode(Y)
            for X in range(1,10):
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyQf', 0)
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"Off",{"zoneId":0})
                self.partner.empty_all(0.5)
                logger.info(f"-----发送信号值{X}")
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindSpeed",{"zoneId":1,"speed":X})
                #以上接口代替信号self.ipdu.set(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', X)
                sleep(2)
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"AQS System Error", "info": "0"}]})
                sleep(3)
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"AQS System Error", "info": info(X)}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"AQS System Error", "info": info(X)}]})
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"Off",{"zoneId":0})
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"AQS System Error", "info": "0"}]})
            for X in range(1,10):
                logger.info(f"-----发送信号值{X}")
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyQf', 0)
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindSpeed",{"zoneId":1,"speed":X})
                sleep(2)
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"AQS System Error", "info": "0"}]})
                sleep(3)
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"AQS System Error", "info": info(X)}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"AQS System Error", "info": info(X)}]})
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyQf', 1)
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"AQS System Error", "info": "0"}]})
        for Z in [2,1,2,0,11,1,11,0,13,1,13,0]:
            logger.info(f"-----切换使用者模式为{X}")
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindSpeed",{"zoneId":1,"speed":1})
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyQf', 0)
            self.sd_tester.change_usage_mode(Z)
            sleep(5)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"AQS System Error", "info": info2(Z)}]})

    @allure.title("WarningMsgList_空调系统故障") 
    @pytest.mark.sanity
    def test_caseid_1980108(self):
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'HvCooltHeatrWarnSigFltPrsnt', 1)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr07, 'CmprFbCmprSts2', 2)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'HvCooltHeatrWarnSigFltInCom', 1)
        self.partner.ck_no_event(WTI_SERVICE_CLIENT,"WarningMsgList")
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Climate System Error", "info": "0"}]})    
     
    @allure.title("遍历_香氛系统故障") 
    @pytest.mark.sanity
    def test_caseid_1980109(self):
        info = [(3,"1"),(0,"0"),(3,"1"), (1,"0"), (3,"1"), (2,"0")]
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragStsFrmClima', 0)
        self.partner.empty_all(0.5)
        for item in info:
            logger.info(f"-----发送信号值{item[0]}")
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragStsFrmClima', item[0])
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Fragrance System Error", "info": item[1]}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Fragrance System Error", "info": item[1]}]})


    @allure.title("WTI_空气质量管理系统故障_400v车型5s内改变条件在恢复条件") 
    @pytest.mark.smoke
    @pytest.mark.jishu3
    def test_caseid_1989674(self):  
        self.airvent_no_fault()
        self.sd_tester.write_single_ccp(962,0)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindSpeed",{"zoneId":1,"speed":1})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyQf', 0)
        self.sd_tester.change_usage_mode(2)
        self.partner.empty_all(0.5)
        sleep(3)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyQf', 1)
        self.partner.ck_no_event_and_ck_resp(WTI_SERVICE_CLIENT,"WarningMsgList",{"out":[{"name":"AQS System Error", "info": 0}]})
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyQf', 0)
        sleep(2)
        self.partner.ck_no_event_and_ck_resp(WTI_SERVICE_CLIENT,"WarningMsgList",{"out":[{"name":"AQS System Error", "info": 0}]})
        self.partner.empty_all(0.5)
        sleep(3)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"AQS System Error", "info": 1}]})

    @allure.title("WTI_空气质量管理系统故障_车型错5s内400V车型上报") 
    @pytest.mark.full
    @pytest.mark.jishu3
    def test_caseid_1989675(self):  
        self.airvent_no_fault()
        self.sd_tester.write_single_ccp(962,3)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindSpeed",{"zoneId":1,"speed":1})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyQf', 0)
        self.sd_tester.change_usage_mode(2)
        self.partner.empty_all(0.5)
        sleep(5)
        self.partner.ck_no_event_and_ck_resp(WTI_SERVICE_CLIENT,"WarningMsgList",{"out":[{"name":"AQS System Error", "info": 0}]})
        self.sd_tester.write_single_ccp(962,0)
        self.sd_tester.change_usage_mode(2)
        sleep(4)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"AQS System Error", "info": 1}]})
                
    @allure.title("WTI_空气质量管理系统故障_400v车型5s内usage跳变") 
    @pytest.mark.sanity
    @pytest.mark.jishu3
    def test_caseid_1989676(self): 
        self.airvent_no_fault() 
        self.sd_tester.write_single_ccp(962,0)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindSpeed",{"zoneId":1,"speed":1})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyQf', 0)
        self.sd_tester.change_usage_mode(2)
        self.partner.empty_all()
        self.partner.ck_no_event_and_ck_resp(WTI_SERVICE_CLIENT,"WarningMsgList",{"out":[{"name":"AQS System Error", "info": 0}]})
        self.sd_tester.change_usage_mode(0)
        self.partner.empty_all()
        sleep(2)
        self.partner.ck_no_event_and_ck_resp(WTI_SERVICE_CLIENT,"WarningMsgList",{"out":[{"name":"AQS System Error", "info": 0}]})
        self.sd_tester.change_usage_mode(11)
        self.partner.empty_all()
        sleep(2)
        self.partner.ck_no_event_and_ck_resp(WTI_SERVICE_CLIENT,"WarningMsgList",{"out":[{"name":"AQS System Error", "info": 0}]})
        sleep(3)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"AQS System Error", "info": 1}]},timeout=2)
        
    @allure.title("WTI_空气质量管理系统故障_400v车型5s内usage从满足跳变满足") 
    @pytest.mark.full
    @pytest.mark.jishu3
    def test_caseid_1989679(self): 
        self.airvent_no_fault() 
        self.sd_tester.change_usage_mode(0)
        self.sd_tester.write_single_ccp(962,0)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindSpeed",{"zoneId":1,"speed":1})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyQf', 0)
        self.partner.empty_all(1)
        self.sd_tester.change_usage_mode(2)
        self.partner.empty_all()
        sleep(1)
        self.partner.ck_no_event_and_ck_resp(WTI_SERVICE_CLIENT,"WarningMsgList",{"out":[{"name":"AQS System Error", "info": 0}]})
        sleep(2)
        self.sd_tester.change_usage_mode(11)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"AQS System Error", "info": 1}]},timeout=2)
        
    @allure.title("WTI_空气质量管理系统故障_800v车型不上报") 
    @pytest.mark.full
    @pytest.mark.jishu3
    def test_caseid_1989677(self):  
        self.airvent_no_fault()
        self.sd_tester.change_usage_mode(2)
        self.sd_tester.write_single_ccp(962,1)
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindSpeed",{"zoneId":1,"speed":1})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyQf', 0)
        sleep(5)
        self.partner.ck_no_event(WTI_SERVICE_CLIENT,"WarningMsgList")
        
    @allure.title("WTI_空气质量管理系统故障_错误车型5s内上报800v车型") 
    @pytest.mark.full
    @pytest.mark.jishu3
    def test_caseid_1989678(self):  
        self.airvent_no_fault()
        self.sd_tester.change_usage_mode(2)
        self.sd_tester.write_single_ccp(962,6)
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindSpeed",{"zoneId":1,"speed":1})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyQf', 0)
        sleep(1)
        self.sd_tester.write_single_ccp(962,1)
        sleep(5)
        self.partner.ck_no_event(WTI_SERVICE_CLIENT,"WarningMsgList")