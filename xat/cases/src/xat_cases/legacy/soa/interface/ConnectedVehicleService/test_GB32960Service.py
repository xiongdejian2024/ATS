#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: test_GB32960Service.py
@Time: 2023/11/4 18:00
@Author: jingjing.wang
@Description: Test SOA service about GB32960Service
"""
import pytest
import allure
from time import sleep
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.soa.case_helper.gnss_server import GNSSServiceServer


@allure.feature("SOA服务接口")
@allure.story("互联服务/GB32960Service")
@pytest.mark.wjj
class TestGB32960_TCAM(TestBase):
    '''重启tcam'''
    def before_class(self, ecu):  # 用例执行前处理
        super().before_class(self, ecu)
        logger.info("TCAM下电")
        self.nucapp.tcam_power_off()
        sleep(30)
        self.sd_tester.tester_present()
        self.sd_tester.write_single_ccp(962, 0)
        sleep(1)
        self.partner = GNSSServiceServer(
            [("GB32960Service", "client"), ("GNSSService", "server"), ("VehicleTimeService", "client")])
        self.partner.register_callback("GNSSService_server", self.partner.on_GetGNSSInformation)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.partner.empty_all(1)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        sleep(1)
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):  # 用例执行后处理
        self.sd_tester.stop_tester_present()
        self.partner.stop_operators()
        self.nucapp.tcam_power_on()
        sleep(180)
        super().after_class(self, ecu)

    def ck_GB32960Data_and_GetGB32960Data(self, ck_dict):
        """校验指定GB32960Data事件，并请求GetGB32960Data获取结果"""
        self.partner.ck_s2s_event(GB32960_SERVICE_CLIENT, "GB32960Data",
                                  {"info": ck_dict})
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": ck_dict})

    @allure.title("获取|通知GB32960数据_Vehpositiondata_初始值")
    @pytest.mark.full
    def test_caseid_1982933(self):
        self.partner.GNSSStatus = 2
        self.partner.longitude = 2  # 上海的位置
        self.partner.latitude = 2
        self.ck_GB32960Data_and_GetGB32960Data(
            {"VehPositionData": {"LocationSts": 0, "Longitude": 2 * (10 ** 6), "Latitude": 2 * (10 ** 6)}})
        self.partner.unregister_callback("GNSSService_server", self.partner.on_GetGNSSInformation)
        try:
            self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
            self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                                  {"out":
                                                       {"VehPositionData": {"LocationSts": 1, "Longitude": 0,
                                                                            "Latitude": 0}}})
        except Exception as e:
            self.partner.register_callback("GNSSService_server", self.partner.on_GetGNSSInformation)
            assert False, e
        else:
            self.partner.register_callback("GNSSService_server", self.partner.on_GetGNSSInformation)

    @allure.title("获取|通知GB32960数据_LocationSts0/1")
    @pytest.mark.smoke
    def test_caseid_1982932(self):
        for GNSSStatus in range(2):
            self.partner.empty_all(0.2)
            self.partner.GNSSStatus = GNSSStatus
            for longitude in range(2):
                self.partner.empty_all(0.2)
                self.partner.longitude = longitude
                for latitude in range(2):
                    self.partner.empty_all(0.2)
                    self.partner.latitude = latitude
                    if self.partner.GNSSStatus == 0 or self.partner.longitude == 0 or self.partner.latitude == 0:
                            self.ck_GB32960Data_and_GetGB32960Data({"VehPositionData": {"LocationSts": 1}})
                    else:
                            self.ck_GB32960Data_and_GetGB32960Data({"VehPositionData": {"LocationSts": 0}})

    @allure.title("获取|通知GB32960数据_Longitude正常值")
    @pytest.mark.sanity
    def test_caseid_1982934(self):
        self.partner.longitude = 2  # 上海的位置
        self.ck_GB32960Data_and_GetGB32960Data({"VehPositionData": {"Longitude": 2 * (10 ** 6)}})
        sleep(1)
        self.partner.longitude = 3.141592653589793238  # 上海的位置
        self.ck_GB32960Data_and_GetGB32960Data(
            {"VehPositionData": {"Longitude": round(3.141592653589793238, 6) * (10 ** 6)}})

    @allure.title("获取|通知GB32960数据_Latitude正常值")
    @pytest.mark.sanity
    def test_caseid_1982935(self):
        self.partner.latitude = 2
        self.ck_GB32960Data_and_GetGB32960Data({"VehPositionData": {"Latitude": 2 * (10 ** 6)}})
        sleep(1)
        self.partner.latitude = 3.141592653589793238
        self.ck_GB32960Data_and_GetGB32960Data(
            {"VehPositionData": {"Latitude": round(3.141592653589793238, 6) * (10 ** 6)}})


@allure.feature("SOA服务接口")
@allure.story("互联服务/GB32960")
@pytest.mark.wjj
class TestGB32960(TestBase):
    '''常规GB32960'''
    def before_class(self, ecu):  # 用例执行前处理
        super().before_class(self, ecu)
        self.sd_tester.tester_present()
        self.sd_tester.write_single_ccp(962, 0)
        sleep(1)
        self.partner = GNSSServiceServer([("GB32960Service", "client")])

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.partner.empty_all(1)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        sleep(1)
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):  # 用例执行后处理
        self.sd_tester.stop_tester_present()
        self.partner.stop_operators()
        sleep(5)
        super().after_class(self, ecu)

    def ck_GB32960Data_and_GetGB32960Data(self, ck_dict):
        """校验指定GB32960Data事件，并请求GetGB32960Data获取结果"""
        self.partner.ck_s2s_event(GB32960_SERVICE_CLIENT, "GB32960Data",
                                  {"info": ck_dict})
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": ck_dict})

    def SetExtremeData(self, value1, value2, value3, value4, value5, value6, value7, value8, value9, value10,
                       value11,
                       value12):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr25, 'HvBattVoltMaxSerlNr', value1)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr23, 'HvBattCellUInfoU3', value2)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr23, 'HvBattCellUInfoU4', value3)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr25, 'HvBattVoltMinSerlNr', value4)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr23, 'HvBattCellUInfoU3', value5)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr23, 'HvBattCellUInfoU4', value6)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr25, 'HvBattTMaxSerlNr', value7)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattTSnsrNr', value8)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattSnsrT', value9)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr25, 'HvBattTMinSerlNr', value10)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattTSnsrNr', value11)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattSnsrT', value12)
        sleep(0.5)

    def Warning(self, HvCellTDifFltPrm, HvCellTOverFltPrm, HvPackUUnderFltPrm, HvSocLoFltPrm, HvCellUOverFltPrm,
                HvCellUUnderFltPrm, HvSocHiFltPrm, HvSocHopFltPrm, HvCellUDifFltPrm, HvlsoFltPrm, EscWarnIndcnReqPrm,
                AbsWarnIndcnReqPrm, HvPackOverChrgFltPrm):
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr08, 'HvCellTDifFlt', HvCellTDifFltPrm)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr08, 'HvCellTOverFlt', HvCellTOverFltPrm)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr08, 'HvPackUUnderFlt', HvPackUUnderFltPrm)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr08, 'HvSocLoFlt', HvSocLoFltPrm)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr08, 'HvCellUOverFlt', HvCellUOverFltPrm)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr08, 'HvCellUUnderFlt', HvCellUUnderFltPrm)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr08, 'HvSocHiFlt', HvSocHiFltPrm)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr08, 'HvSocHopFlt', HvSocHopFltPrm)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr08, 'HvCellUDifFlt', HvCellUDifFltPrm)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr08, 'HvIsoFlt', HvlsoFltPrm)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', EscWarnIndcnReqPrm)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq',
                      AbsWarnIndcnReqPrm)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr08, 'HvPackOverChrgFlt', HvPackOverChrgFltPrm)
        sleep(0.5)

    def Warning01(self, HvBattMismatchFltPrm, FltTDcDcPrm, BrkWarnIndcnReqPrm, BrkSysWarnIndcnReqPrm,
                  BrkSysWarnIndcnReqSecPrm, FltElecDcDcPrm, HvilFltPrm):
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr08, 'HvBattMismatchFlt', HvBattMismatchFltPrm)  # 01
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'FltTDcDc', FltTDcDcPrm)  # 01
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', BrkSysWarnIndcnReqPrm)  # 01
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', BrkSysWarnIndcnReqSecPrm)  # 01
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'FltElecDcDc', FltElecDcDcPrm)  # 01
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq',
                      BrkWarnIndcnReqPrm)  # 01
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr08, 'HvilFlt', HvilFltPrm)  # 01

    def Warning012(self, IemGenericInvrtTAlrmStPrm, IgmGenericInvrtTAlrmStPrm, IemGenericMotTAlrmStPrm,
                   IgmGenericMotTAlrmStPrm):
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr06, 'IemGenericInvrtTAlrmSt', IemGenericInvrtTAlrmStPrm)  # 012
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr07, 'IgmGenericInvrtTAlrmSt',
                      IgmGenericInvrtTAlrmStPrm)  # 012
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr06, 'IemGenericMotTAlrmSt', IemGenericMotTAlrmStPrm)  # 012
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr07, 'IgmGenericMotTAlrmSt', IgmGenericMotTAlrmStPrm)  # 012

    def CellUVal(self, HvBattCellUInfoU1, HvBattCellUInfoU3, HvBattCellUInfoU4):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackboneNmFr01, 'HvBattCellUInfoU1', HvBattCellUInfoU1)  # 有效值>=3
        self.ipdu.set(self.ipdu.backbonefr.VddmBackboneNmFr01, 'HvBattCellUInfoU3', HvBattCellUInfoU3)  # 电池电压编号
        self.ipdu.set(self.ipdu.backbonefr.VddmBackboneNmFr01, 'HvBattCellUInfoU4', HvBattCellUInfoU4)  # 电压

    @allure.title("重启evnet")
    @pytest.mark.full
    def test_caseid_1984543(self):
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT)
        self.ck_GB32960Data_and_GetGB32960Data({})

    @allure.title("获取|通知GB32960数据_ChrgnStsInfo_1_5")
    @pytest.mark.smoke
    def test_caseid_1979947(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr09, 'ChrgnSts', 0)
        for i in range(1, 5):
            logger.info(f"现在是{i}")
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr09, 'ChrgnSts', i)
            self.partner.empty_all(0.5)
            self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"ChrgnStsInfo": i}})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr09, 'ChrgnSts', 5)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"ChrgnStsInfo": 255}})

    @allure.title("获取|通知GB32960数据_ChrgnStsInfo信号丢失/初始值")  # todo 初始值错误254
    @pytest.mark.full
    def test_caseid_1979948(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr09, 'ChrgnSts', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr09, 'ChrgnSts', 0)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"ChrgnStsInfo": 254}})
        self.ipdu.pause_bus_send("backbonefr")
        sleep(2)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"ChrgnStsInfo": 254}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"ChrgnStsInfo": 3}}})
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"ChrgnStsInfo": 254}})

    @allure.title("获取|通知GB32960数据_HvBattSocToltalU_0_511")
    @pytest.mark.sanity
    def test_caseid_1979950(self):
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc', 1.0)
        for i in (0.0, 10.0, 199.0, 510.0, 511.0):
            logger.info(f"现在是{i}")
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc', i)
            self.partner.empty_all(0.5)
            self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"HvBattSocToltalU": i * 10}})

    @allure.title("获取|通知GB32960数据_HvBattSocToltalU信号丢失_初始值")  # liugao:超范围值暂时不测
    @pytest.mark.full
    def test_caseid_1979999(self):
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc', 0)
        sleep(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc', 1.0)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"HvBattSocToltalU": 10}})
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"HvBattSocToltalU": 10}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"HvBattSocToltalU": 0}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"HvBattSocToltalU": 10}})

    @allure.title("获取|通知GB32960数据_HvBattSocToltalI_0_1000")
    @pytest.mark.smoke
    def test_caseid_1980000(self):
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HvBattIDc1', 1.0)
        self.partner.empty_all(0.5)
        for i in (0.0, 20.0, 103.0, 999.0, 1000.0):  # 16380,16390,16580,17410,26370,26380
            logger.info(f"现在是{i}")
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HvBattIDc1', i)
            self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"HvBattSocToltalI": ((i + 1000) * 10)}})

    @allure.title("获取|通知GB32960数据_HvBattSocToltalI超范围值/信号丢失/初始值")
    @pytest.mark.full
    def test_caseid_1980001(self):
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HvBattIDc1', 0)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HvBattIDc1', 10.0)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"HvBattSocToltalI": 10100}})
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {
                                                  "HvBattSocToltalI": 10100}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"HvBattSocToltalI": 0}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HvBattIDc1', 1001.0)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"HvBattSocToltalI": 65535}})

    @allure.title("获取|通知GB32960数据_HvBattSocInfo_0_100/超范围值/信号丢失/初始值")
    @pytest.mark.full
    def test_caseid_1980398(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10)
        self.partner.empty_all(0.5)
        for i in (0, 100, 888, 1000):
            logger.info(f"现在是{i}")
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', i)
            sleep(0.2)
            self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"HvBattSocInfo": int(i * 0.1)}})
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {
                                                  "HvBattSocInfo": 100}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"HvBattSocInfo": 50}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 1023)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"HvBattSocInfo": 255}})

    @allure.title("获取|通知GB32960数据_DcDcSts_0_1_初始值")  # todo 初始值为2
    @pytest.mark.sanity
    def test_caseid_1980003(self):
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"DcDcSts": 2}})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"DcDcSts": 1}}) 
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"DcDcSts": 2}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"DcDcSts": 1}})

    @allure.title("获取|通知GB32960数据_DcDcSts_超范围值/信号丢失")
    @pytest.mark.full
    def test_caseid_1980004(self):
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"DcDcSts": 1}})
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"DcDcSts": 1}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"DcDcSts": 1}})

    @allure.title("获取|通知GB32960数据_GearLvrIndcn_Bit0_Bit3_p档_有无制动驱动信号丢失_初始值")
    @pytest.mark.full
    def test_caseid_1980005(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 1)
        self.partner.empty_all(0.5)
        for i in [0, 4, 5, 6, 7]:
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', i)
            for a in range(2):
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr39, 'VehPropSts', a)
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'BrkFricTqTotAtWhlsActBrkFricTqTotAtWhlsAct', a)
                if a == 1:
                    sts = 63
                else:
                    sts = 15
                self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": sts}})
        self.ipdu.pause_all_bus_send()
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"GearSts": 63}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": 15}})
        self.ipdu.resume_all_bus_send()
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": 63}})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr39, 'VehPropSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'BrkFricTqTotAtWhlsActBrkFricTqTotAtWhlsAct', 0)

    @allure.title("获取|通知GB32960数据_GearLvrIndcn_Bit0_Bit3_R档_信号丢失_初始值")
    @pytest.mark.full
    def test_caseid_1980045(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 1)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": 13}})
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"GearSts": 13}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": 15}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": 13}})

    @allure.title("获取|通知GB32960数据_GearLvrIndcn_Bit0_Bit3_空档_超范围值_信号丢失_初始值")
    @pytest.mark.full
    def test_caseid_1980402(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 2)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": 0}})
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"GearSts": 0}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": 15}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": 0}})

    @allure.title("获取|通知GB32960数据_GearLvrIndcn_Bit0_Bit3_D档_信号丢失_初始值")
    @pytest.mark.sanity
    def test_caseid_1980404(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 3)
        sleep(0.2)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": 14}})
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"GearSts": 14}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": 15}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": 14}})
    
    @allure.title("获取|通知GB32960数据_GearLvrIndcn_Bit4有无制动_信号丢失_初始值")
    @pytest.mark.full
    def test_caseid_1980046(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr39, 'VehPropSts', 0)#bit5置为0
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'BrkFricTqTotAtWhlsActBrkFricTqTotAtWhlsAct', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 2)
        for i in [267, 20000]:
            logger.info(f"信号是{i}")
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'BrkFricTqTotAtWhlsActBrkFricTqTotAtWhlsAct', i)
            sleep(0.5)
            self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": 16}})
        self.ipdu.pause_bus_send("backbonefr")
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"GearSts": 16}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": 15}})
        self.ipdu.resume_bus_send("backbonefr")
        self.ipdu.resume_bus_send("propulsioncan")
        sleep(0.2)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": 16}})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'BrkFricTqTotAtWhlsActBrkFricTqTotAtWhlsAct', 0)
        sleep(0.1)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": 0}})

    @allure.title("获取|通知GB32960数据_GearLvrIndcn_Bit5有无驱动_信号丢失_初始值")
    @pytest.mark.full
    def test_caseid_1980044(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'BrkFricTqTotAtWhlsActBrkFricTqTotAtWhlsAct', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr39, 'VehPropSts', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 2)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr39, 'VehPropSts', 1)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": 32}})
        self.ipdu.pause_bus_send("backbonefr")
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"GearSts": 32}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": 15}})
        self.ipdu.resume_bus_send("backbonefr")
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": 32}})
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr39, 'VehPropSts', 0)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"GearSts": 0}})

    @allure.title("获取|通知GB32960数据_InsulationR0_60000_超范围值_信号丢失_初始值")
    @pytest.mark.full
    def test_caseid_1980111(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr09, 'HvIsoR', 1)
        for i in [0, 29, 498, 9999, 59999, 60000, 27]:
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr09, 'HvIsoR', i)
            self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"InsulationR": i}})
        self.ipdu.pause_bus_send("backbonefr")
        sleep(2)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"InsulationR": 27}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"InsulationR": 60000}})
        self.ipdu.resume_bus_send("backbonefr")
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr39, 'VehPropSts', 60001)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"InsulationR": 27}}},timeout=3)

    @allure.title("获取|通知GB32960数据_AccPedlTrvlVal0_100_超范围值_信号丢失_初始值")
    @pytest.mark.full
    def test_caseid_1980112(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat_0_EcmPropSignalIPdu00', 1)
        for i in [2576, 9999, 10000, 22789, 24897, 25600]:
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat_0_EcmPropSignalIPdu00', i)
            self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"AccPedlTrvlVal": int(i * 0.00390625)}})
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"AccPedlTrvlVal": 100}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"AccPedlTrvlVal": 0}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"AccPedlTrvlVal": 100}})
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat_0_EcmPropSignalIPdu00', 25900)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"AccPedlTrvlVal": 255}})

    @allure.title("获取|通知GB32960数据_BrkPedlSts0_100_超范围值_信号丢失_初始值")
    @pytest.mark.full
    def test_caseid_1980114(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatPerc', 1)
        for i in [2576, 9999, 10000, 22789, 24897, 25600]:
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatPerc', i)
            self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"BrkPedlStsInfo": (int(i * 0.00390625))}})
        self.ipdu.pause_bus_send("backbonefr")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"BrkPedlStsInfo": 100}}})
        sleep(1)  # 停propulsioncan等待1s，如果不等待可能直接杀s2s导致总线还没有停掉
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatPerc', 0)
        self.ipdu.resume_bus_send("backbonefr")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatPerc', 25900)  # 全哥那边超过100的信号发出去
        sleep(2.5)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"BrkPedlStsInfo": 255}}})

        '''---------------------DrvMotList结构体--------------------'''

    @allure.title(
        "获取|通知GB32960数据_VehPositionData_ExtremeDataInfoTyp_WarningDataInfoTyp_HVBatteryVoltageDataInfoTyp_HVBatteryTemperatureData_正常_初始值")
    @pytest.mark.smoke
    def test_caseid_1980266(self):
        self.ck_GB32960Data_and_GetGB32960Data(
            {"VehPositionData": {"InfoTyp": 5}, "ExtremeData": {"InfoTyp": 6}, "WarningData": {"InfoTyp": 7},
             "HVBatteryVoltageData": {"InfoTyp": 8}, "HVBatteryTemperatureData": {"InfoTyp": 9}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data(
            {"VehPositionData": {"InfoTyp": 5}, "ExtremeData": {"InfoTyp": 6}, "WarningData": {"InfoTyp": 7},
             "HVBatteryVoltageData": {"InfoTyp": 8}, "HVBatteryTemperatureData": {"InfoTyp": 9}})

    @allure.title("获取|通知GB32960数据_Extreme_正常值_初始值")
    @pytest.mark.full
    def test_caseid_1980282(self):
        self.SetExtremeData(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        for i in [0, 72, 245]:
            logger.info(f'信号{i}')
            self.SetExtremeData(i, i, i, i, i, i, i, i, i, i, i, i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"ExtremeData": {"MaxHvBattUSubSysNr": 1, "MaxHvBattCellUCod": 1, "MaxHvBattCellUVal": 1,
                                 "MinHvBattUSubSysNr": 1, "MinHvBattCellUCod": 1, "MinHvBattCellUVal": 1,
                                 "MaxHvBattTSubSysNr": 1, "MaxHvBattCellTCod": 1, "MaxHvBattCellTVal": 1,
                                 "MinHvBattTSubSysNr": 1, "MinHvBattCellTCod": 1, "MinHvBattCellTVal": 1}})
        self.ipdu.pause_bus_send("propulsioncan")
        self.ipdu.pause_bus_send("backbonefr")
        sleep(2)
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data(
            {"ExtremeData": {"MaxHvBattUSubSysNr": 1, "MaxHvBattCellUCod": 1, "MaxHvBattCellUVal": 1,
                             "MinHvBattUSubSysNr": 1, "MinHvBattCellUCod": 1, "MinHvBattCellUVal": 1,
                             "MaxHvBattTSubSysNr": 1, "MaxHvBattCellTCod": 1, "MaxHvBattCellTVal": 1,
                             "MinHvBattTSubSysNr": 1, "MinHvBattCellTCod": 1, "MinHvBattCellTVal": 1}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_GB32960Data_and_GetGB32960Data(
            {"ExtremeData": {"MaxHvBattUSubSysNr": 1, "MaxHvBattCellUCod": 1, "MaxHvBattCellUVal": 1,
                             "MinHvBattUSubSysNr": 1, "MinHvBattCellUCod": 1, "MinHvBattCellUVal": 1,
                             "MaxHvBattTSubSysNr": 1, "MaxHvBattCellTCod": 1, "MaxHvBattCellTVal": 1,
                             "MinHvBattTSubSysNr": 1, "MinHvBattCellTCod": 1, "MinHvBattCellTVal": 1}})

    @allure.title(
        "获取|通知GB32960数据_ReChrglEgyStorgSubSysQnty正常值_初始值")
    @pytest.mark.sanity
    def test_caseid_1980296(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr23, 'HvBattNr', 2)
        for i in [0, 72, 245]:
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr23, 'HvBattNr', i)
            self.ck_GB32960Data_and_GetGB32960Data({"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysQnty": 1},
                                                    "HVBatteryTemperatureData": {"ReChrglEgyStorgSubSysQnty": 1}})
        self.ipdu.pause_bus_send("backbonefr")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysQnty": 1},
                                                       "HVBatteryTemperatureData": {"ReChrglEgyStorgSubSysQnty": 1}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysQnty": 1},
                                                       "HVBatteryTemperatureData": {"ReChrglEgyStorgSubSysQnty": 1}}})
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_GB32960Data_and_GetGB32960Data({"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysQnty": 1},
                                                "HVBatteryTemperatureData": {"ReChrglEgyStorgSubSysQnty": 1}})

    @allure.title(
        "获取|通知GB32960数据_HVBatteryVoltageData_ReChrglEgyStorgSubSysSeqNr_HVBatteryTemperatureData_ReChrglEgyStorgSubSysSeqNr_正常值_初始值")
    @pytest.mark.sanity
    def test_caseid_1980297(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'PackNr', 2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr14, 'IgmGenericEMSeqNr', 2)
        for i in [0, 72, 245]:
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'PackNr', i)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr14, 'IgmGenericEMSeqNr', i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysList": [{"ReChrglEgyStorgSubSysSeqNr": 1}]},
                 "HVBatteryTemperatureData": {"ReChrglEgyStorgSubSysList": [{"ReChrglEgyStorgSubSysSeqNr": 1}]}})
        self.ipdu.pause_bus_send("backbonefr")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out":
                                                  {"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysList": [
                                                      {"ReChrglEgyStorgSubSysSeqNr": 1}]}, "HVBatteryTemperatureData": {
                                                      "ReChrglEgyStorgSubSysList": [
                                                          {"ReChrglEgyStorgSubSysSeqNr": 1}]}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out":
                                                  {"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysList": [
                                                      {"ReChrglEgyStorgSubSysSeqNr": 1}]}, "HVBatteryTemperatureData": {
                                                      "ReChrglEgyStorgSubSysList": [
                                                          {"ReChrglEgyStorgSubSysSeqNr": 1}]}}})
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_GB32960Data_and_GetGB32960Data(
            {"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysList": [{"ReChrglEgyStorgSubSysSeqNr": 1}]},
             "HVBatteryTemperatureData": {"ReChrglEgyStorgSubSysList": [{"ReChrglEgyStorgSubSysSeqNr": 1}]}})

    @allure.title(
        "获取|通知GB32960数据_ReChrglEgyStorgU_正常值_初始值")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1980298?projectId=46')
    @pytest.mark.full
    def test_caseid_1980298(self):
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc', 2)
        for i in [0, 72, 245, 511, 2046, 2047]:
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc', i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysList": [{"ReChrglEgyStorgU": int(i * 0.25 * 10)}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out":
                                                  {"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysList": [
                                                      {"ReChrglEgyStorgU": 5117}]}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"HVBatteryVoltageData": {
                                                  "ReChrglEgyStorgSubSysList": [{"ReChrglEgyStorgU": 0}]}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
            {"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysList": [{"ReChrglEgyStorgU": 5117}]}})

    @allure.title(
        "获取|通知GB32960数据_BattCellesTotNr_正常值_初始值")  
    @pytest.mark.sanity
    def test_caseid_1980303(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackboneNmFr01, 'HvBattCellUInfoU2', 10)
        for i in [72, 245, 255]:
            logger.info(f'信号{i}')
            sleep(0.2)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackboneNmFr01, 'HvBattCellUInfoU2', i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"HVBatteryVoltageData": {
                    "ReChrglEgyStorgSubSysList": [{"BattCellesTotNr": i - 3}]}})
        self.ipdu.pause_bus_send("backbonefr")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out":
                                                  {"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysList": [
                                                      {"BattCellesTotNr": 252}]}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"HVBatteryVoltageData": {
                                                  "ReChrglEgyStorgSubSysList": [
                                                      {"BattCellesTotNr": 1}]}}})
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_GB32960Data_and_GetGB32960Data(
            {"HVBatteryVoltageData": {
                "ReChrglEgyStorgSubSysList": [{"BattCellesTotNr": 252}]}})
        
    @allure.title(
        "获取|通知GB32960数据_TotCellNrofThisFrm_正常值_初始值_超范围值")  
    @pytest.mark.full
    def test_caseid_1985116(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackboneNmFr01, 'HvBattCellUInfoU2', 10)
        for i in [72, 100 ,203]:
            logger.info(f'信号{i}')
            sleep(0.2)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackboneNmFr01, 'HvBattCellUInfoU2', i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"HVBatteryVoltageData": {
                    "ReChrglEgyStorgSubSysList": [{"TotCellNrofThisFrm": i - 3}]}})
        self.ipdu.pause_bus_send("backbonefr")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out":
                                                  {"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysList": [
                                                      { "TotCellNrofThisFrm": 200}]}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"HVBatteryVoltageData": {
                                                  "ReChrglEgyStorgSubSysList": [
                                                      {"TotCellNrofThisFrm": 1}]}}})
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_GB32960Data_and_GetGB32960Data(
            {"HVBatteryVoltageData": {
                "ReChrglEgyStorgSubSysList": [{"TotCellNrofThisFrm": 200}]}})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackboneNmFr01, 'HvBattCellUInfoU2', 255)
        self.ck_GB32960Data_and_GetGB32960Data(
                {"HVBatteryVoltageData": {
                    "ReChrglEgyStorgSubSysList": [{"TotCellNrofThisFrm": 200}]}})

    @allure.title(
        "获取|通知GB32960数据_BgngCellSeqNrofThisFrm_正常值_初始值")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1980302?projectId=46')
    @pytest.mark.full
    def test_caseid_1980302(self):
        self.ck_GB32960Data_and_GetGB32960Data(
            {"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysList": [{"BgngCellSeqNrofThisFrm": 1}]}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out":
                                                  {"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysList": [
                                                      {"BgngCellSeqNrofThisFrm": 1}]}}})

    @allure.title("获取|通知GB32960数据_TotTProbeNr_正常值_初始值")
    @pytest.mark.sanity
    def test_caseid_1980307(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr21, 'HvBattCellTNr', 2)
        for i in [1, 275, 65530, 65531]:
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr21, 'HvBattCellTNr', i)
            sleep(0.5)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"HVBatteryTemperatureData": {"ReChrglEgyStorgSubSysList": [{"TotTProbeNr": i}]}})
        self.ipdu.pause_bus_send("backbonefr")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out":
                                                  {"HVBatteryTemperatureData": {
                                                      "ReChrglEgyStorgSubSysList": [{"TotTProbeNr": 65531}]}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"HVBatteryTemperatureData": {
                                                  "ReChrglEgyStorgSubSysList": [{"TotTProbeNr": 1}]}}})
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_GB32960Data_and_GetGB32960Data(
            {"HVBatteryTemperatureData": {"ReChrglEgyStorgSubSysList": [{"TotTProbeNr": 65531}]}})

    @allure.title("获取|通知GB32960数据_CellUVal_正常值")
    @pytest.mark.smoke
    def test_caseid_1980304(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackboneNmFr01, 'HvBattCellUInfoU2', 13)  # CellUVal的长度控制信号-3
        self.CellUVal(3, 1, 2)
        self.partner.empty_all(0.5)
        for i in [0, 254, 6000, 8191]:
            logger.info(f'电池电压是{i}')
            self.CellUVal(3, 1, i)
            sleep(0.1)
            self.CellUVal(3, 3, i)
            sleep(0.1)
            self.CellUVal(6, 7, i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"HVBatteryVoltageData":{"ReChrglEgyStorgSubSysList": [{
                    "CellUVal":  [i, 0, i, 0, 0, 0, i, 0, 0, 0]}]}})
        self.CellUVal(3, 1, 0)
        sleep(0.1)
        self.CellUVal(3, 3, 0)
        sleep(0.1)
        self.CellUVal(3, 7, 0)
        
    @allure.title("获取|通知GB32960数据_CellUVal_初始值")
    @pytest.mark.full
    def test_caseid_1985266(self):
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackboneNmFr01, 'HvBattCellUInfoU2', 13)  # CellUVal的长度控制信号-3
        self.CellUVal(3, 1, 6000)
        sleep(0.1)
        self.CellUVal(3, 3, 6000)
        sleep(0.1)
        self.CellUVal(6, 7, 6000)
        sleep(0.1)
        self.ck_GB32960Data_and_GetGB32960Data(
                {"HVBatteryVoltageData":{"ReChrglEgyStorgSubSysList": [{
                    "CellUVal": [6000,0,6000,0,0,0,6000,0,0,0]}]}})
        self.ipdu.pause_bus_send("backbonefr")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out":{"HVBatteryVoltageData":{"ReChrglEgyStorgSubSysList": [{
                    "CellUVal": [6000,0,6000,0,0,0,6000,0,0,0]}]}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data(
            {"HVBatteryVoltageData":{"ReChrglEgyStorgSubSysList": [{"CellUVal": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}]}})
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_GB32960Data_and_GetGB32960Data(
            {"HVBatteryVoltageData":{"ReChrglEgyStorgSubSysList": [{
                "CellUVal": [6000,0,6000,0,0,0,6000,0,0,0]}]}})
        self.CellUVal(3, 1, 0)
        self.CellUVal(3, 3, 0)
        self.CellUVal(3, 7, 0)

    @allure.title(
        "获取|通知GB32960数据_PrpnMode_正常值_初始值")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1980433?projectId=46')
    @pytest.mark.full
    def test_caseid_1980433(self):
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"PrpnMode": 1}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"PrpnMode": 1}})

    @allure.title(
        "获取|通知GB32960数据_ProbeTVal_正常值_初始值_超范围")  # todo 超范围值是255
    @pytest.mark.sanity
    def test_caseid_1980330(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr21, 'HvBattCellTNr', 48)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattTSnsrNr', 2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattSnsrT', 1)
        for i in [0, 40, 250,254]:
            logger.info(f'电池温度是{i}')
            if i in [254]:
                sts = 255
            else:
                sts = i
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattTSnsrNr', 22)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattSnsrT', i)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattTSnsrNr', 33)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattSnsrT', i)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattTSnsrNr', 48)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattSnsrT', i)
                sleep(1)
                self.ck_GB32960Data_and_GetGB32960Data(
                    {"HVBatteryTemperatureData": {"ReChrglEgyStorgSubSysList": [{"TotTProbeNr": 48,
                                                                                 "ProbeTVal": [0, 0, 0, 0, 0, 0, 0, 0,
                                                                                               0, 0,
                                                                                               0,
                                                                                               0, 0, 0, 0, 0, 0, 0, 0,
                                                                                               0, 0,
                                                                                               sts,
                                                                                               0, 0, 0, 0, 0, 0, 0, 0,
                                                                                               0, 0,
                                                                                               sts,
                                                                                               0, 0, 0, 0, 0, 0, 0, 0,
                                                                                               0, 0,
                                                                                               0,
                                                                                               0, 0, 0, sts]}]}})
        self.ipdu.pause_bus_send("backbonefr")
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"HVBatteryTemperatureData": {"ReChrglEgyStorgSubSysList": [
                                                  {"TotTProbeNr": 48,
                                                   "ProbeTVal": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                 0,
                                                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                 250,
                                                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                 250,
                                                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                 0,
                                                                 0, 0, 0, 250]}]}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"HVBatteryTemperatureData": {"ReChrglEgyStorgSubSysList": [
                                                  {"TotTProbeNr": 1,
                                                   "ProbeTVal": [0]}]}}})
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_GB32960Data_and_GetGB32960Data(
                    {"HVBatteryTemperatureData": {"ReChrglEgyStorgSubSysList": [{"TotTProbeNr": 48,
                                                                                 "ProbeTVal": [0, 0, 0, 0, 0, 0, 0, 0,
                                                                                               0, 0,
                                                                                               0,
                                                                                               0, 0, 0, 0, 0, 0, 0, 0,
                                                                                               0, 0,
                                                                                               250,
                                                                                               0, 0, 0, 0, 0, 0, 0, 0,
                                                                                               0, 0,
                                                                                               250,
                                                                                               0, 0, 0, 0, 0, 0, 0, 0,
                                                                                               0, 0,
                                                                                               0,
                                                                                               0, 0, 0, 250]}]}})

    @allure.title(
        "获取|通知GB32960数据_WarningData0123_正常值_初始值")
    @pytest.mark.smoke
    def test_caseid_1980374(self):
        self.Warning(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        for i in range(4):
            logger.info(f'报警信息是{i}')
            self.Warning(i, i, i, i, i, i, i, i, i, i, i, i, i)
            self.partner.empty_all(0.5)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"WarningData": {"HvCellTDifFltPrm": i, "HvCellTOverFltPrm": i, "HvPackUUnderFltPrm": i,
                                 "HvSocLoFltPrm": i, "HvCellUOverFltPrm": i, "HvCellUUnderFltPrm": i,
                                 "HvSocHiFltPrm": i, "HvSocHopFltPrm": i, "HvCellUDifFltPrm": i, "HvlsoFltPrm": i,
                                 "EscWarnIndcnReqPrm": i, "AbsWarnIndcnReqPrm": i, "HvPackOverChrgFltPrm": i}})
        self.ipdu.pause_bus_send("backbonefr")
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {
                                                  "WarningData": {"HvCellTDifFltPrm": 3, "HvCellTOverFltPrm": 3,
                                                                  "HvPackUUnderFltPrm": 3,
                                                                  "HvSocLoFltPrm": 3, "HvCellUOverFltPrm": 3,
                                                                  "HvCellUUnderFltPrm": 3,
                                                                  "HvSocHiFltPrm": 3, "HvSocHopFltPrm": 3,
                                                                  "HvCellUDifFltPrm": 3, "HvlsoFltPrm": 3,
                                                                  "EscWarnIndcnReqPrm": 3, "AbsWarnIndcnReqPrm": 3,
                                                                  "HvPackOverChrgFltPrm": 3}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data({"WarningData": {"HvCellTDifFltPrm": 0, "HvCellTOverFltPrm": 0,
                                                                  "HvPackUUnderFltPrm": 0,
                                                                  "HvSocLoFltPrm": 0, "HvCellUOverFltPrm": 0,
                                                                  "HvCellUUnderFltPrm": 0,
                                                                  "HvSocHiFltPrm": 0, "HvSocHopFltPrm": 0,
                                                                  "HvCellUDifFltPrm": 0, "HvlsoFltPrm": 0,
                                                                  "EscWarnIndcnReqPrm": 3, "AbsWarnIndcnReqPrm": 3,
                                                                  "HvPackOverChrgFltPrm": 0}})
        self.ipdu.resume_bus_send("backbonefr")
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
            {"WarningData": {"HvCellTDifFltPrm": 3, "HvCellTOverFltPrm": 3, "HvPackUUnderFltPrm": 3,
                             "HvSocLoFltPrm": 3, "HvCellUOverFltPrm": 3, "HvCellUUnderFltPrm": 3,
                             "HvSocHiFltPrm": 3, "HvSocHopFltPrm": 3, "HvCellUDifFltPrm": 3, "HvlsoFltPrm": 3,
                             "EscWarnIndcnReqPrm": 3, "AbsWarnIndcnReqPrm": 3, "HvPackOverChrgFltPrm": 3}})

    @allure.title(
        "获取|通知GB32960数据_WarningData01_正常值_初始值")
    @pytest.mark.sanity
    def test_caseid_1980377(self):
        self.Warning01(1, 1, 1, 1, 1, 1, 1)
        for i in range(2):
            logger.info(f'报警信息是{i}')
            self.Warning01(i, i, i, i, i, i, i)
            self.partner.empty_all(0.5)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"WarningData": {"HvBattMismatchFltPrm": i, "FltTDcDcPrm": i, "BrkWarnIndcnReqPrm": i,
                                 "BrkSysWarnIndcnReqPrm": i, "BrkSysWarnIndcnReqSecPrm": i, "FltElecDcDcPrm": i,
                                 "HvilFltPrm": i}})
        self.ipdu.pause_bus_send("backbonefr")
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {
                                                  "WarningData": {"HvBattMismatchFltPrm": 1, "FltTDcDcPrm": 1,
                                                                  "BrkWarnIndcnReqPrm": 1,
                                                                  "BrkSysWarnIndcnReqPrm": 1,
                                                                  "BrkSysWarnIndcnReqSecPrm": 1,
                                                                  "FltElecDcDcPrm": 1,
                                                                  "HvilFltPrm": 1}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {
                                                  "WarningData": {"HvBattMismatchFltPrm": 0, "FltTDcDcPrm": 0,
                                                                  "BrkWarnIndcnReqPrm": 1,
                                                                  "BrkSysWarnIndcnReqPrm": 1,
                                                                  "BrkSysWarnIndcnReqSecPrm": 1,
                                                                  "FltElecDcDcPrm": 0,
                                                                  "HvilFltPrm": 0}}})
        self.ipdu.resume_bus_send("backbonefr")
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
            {"WarningData": {"HvBattMismatchFltPrm": 1, "FltTDcDcPrm": 1,
                             "BrkWarnIndcnReqPrm": 1,
                             "BrkSysWarnIndcnReqPrm": 1,
                             "BrkSysWarnIndcnReqSecPrm": 1,
                             "FltElecDcDcPrm": 1,
                             "HvilFltPrm": 1}})

    @allure.title(
        "获取|通知GB32960数据_WarningData012_正常值_初始值")
    @pytest.mark.sanity
    def test_caseid_1980376(self):
        self.Warning012(1, 1, 1, 1)
        for i in range(3):
            logger.info(f'报警信息是{i}')
            self.Warning012(i, i, i, i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"WarningData": {"IemGenericInvrtTAlrmStPrm": i, "IgmGenericInvrtTAlrmStPrm": i,
                                 "IemGenericMotTAlrmStPrm": i,
                                 "IgmGenericMotTAlrmStPrm": i}})
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {
                                                  "WarningData": {"IemGenericInvrtTAlrmStPrm": 2,
                                                                  "IgmGenericInvrtTAlrmStPrm": 2,
                                                                  "IemGenericMotTAlrmStPrm": 2,
                                                                  "IgmGenericMotTAlrmStPrm": 2}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {
                                                  "WarningData": {"IemGenericInvrtTAlrmStPrm": 0,
                                                                  "IgmGenericInvrtTAlrmStPrm": 0,
                                                                  "IemGenericMotTAlrmStPrm": 0,
                                                                  "IgmGenericMotTAlrmStPrm": 0}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
                {"WarningData": {"IemGenericInvrtTAlrmStPrm": 2, "IgmGenericInvrtTAlrmStPrm": 2,
                                 "IemGenericMotTAlrmStPrm": 2,
                                 "IgmGenericMotTAlrmStPrm": 2}})
        
    @allure.title("获取|通知GB32960数据_DrvMotSts_0_16_信号丢失_初始值_电机2")  #v2.1需求
    @pytest.mark.sanity
    def test_caseid_1987253(self):
        self.sd_tester.write_multi_ccp({4:6,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr06, 'IemGenericModStatusRms', 1)
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr07, 'IgmGenericModStatusRms', 1)
        for i in list(range(16)) + [5]:
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr07, 'IgmGenericModStatusRms', i)
            if i in [1, 2, 4]:
                sts = i
            elif i == 0:
                sts = 255
            elif i == 5:
                sts = 254
            else:
                sts = 3
            self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSts": 1}, {"DrvMotSeqNr": 2,"DrvMotSts": sts}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 2,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSts": 1},
                                                                                         {"DrvMotSeqNr": 2,"DrvMotSts": 254}]}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data(
            {"DriveMotorData": {"DrvMotQnty": 2, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSts": 3}, {"DrvMotSeqNr": 2,"DrvMotSts": 3}]}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
            {"DriveMotorData": {"DrvMotQnty": 2, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSts": 1}, {"DrvMotSeqNr": 2,"DrvMotSts": 254}]}})
        
    @allure.title("获取|通知GB32960数据_DrvMotSts_电机1设置第二个电机信号无变化")#v2.1需求
    @pytest.mark.full
    def test_caseid_1987481(self):
        self.sd_tester.write_multi_ccp({4:8,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr06, 'IemGenericModStatusRms', 1)
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr07, 'IgmGenericModStatusRms', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr07, 'IgmGenericModStatusRms', 2)
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSts": 1}]}})
        
    @allure.title("获取|通知GB32960数据_DrvMotCtrlrT_信号丢失_初始值_电机2")#v2.1需求
    @pytest.mark.full
    def test_caseid_1987254(self):
        self.sd_tester.write_multi_ccp({4:6,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr03, 'WhlMotSysInvrT', 1)
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr02, 'IsgInvrT', 1)
        for i in [0, 10, 87, 178, 254, 255]:
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr02, 'IsgInvrT', i)
            if i - 50 >= -40:
                sts = i - 50 + 40
            elif i - 50 < -40:
                sts = 0
            else:
                sts = False
            self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotCtrlrT": 0}, {"DrvMotSeqNr": 2,"DrvMotCtrlrT": sts}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(1)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 2,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotCtrlrT": 0},
                                                                                         {"DrvMotSeqNr": 2,"DrvMotCtrlrT": 245}]}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 2,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotCtrlrT": 0},
                                                                                         {"DrvMotSeqNr": 2,"DrvMotCtrlrT": 0}]}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotCtrlrT": 0}, {"DrvMotSeqNr": 2,"DrvMotCtrlrT": 245}]}})
        
    @allure.title("获取|通知GB32960数据_DrvMotSpeed_信号丢失_初始值_电机2_400v") #2.1需求
    @pytest.mark.full
    def test_caseid_1987319(self):
        self.sd_tester.write_multi_ccp({4:6,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr02, 'WhlMotSysSpdAct', 1)
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr06, 'IsgSpdActSgn', 1)
        for i in [0, 7999, 16383]:  # 信号最大只能到16383
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr06, 'IsgSpdActSgn', i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2,
                                    "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": 1 + 20000}, {"DrvMotSeqNr": 2,"DrvMotSpeed": i + 20000}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(1)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 2,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": 1 + 20000},
                                                                                         {"DrvMotSeqNr": 2,"DrvMotSpeed": 36383}]}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 2,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": 0},
                                                                                         {"DrvMotSeqNr": 2,"DrvMotSpeed": 0}]}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2,
                                    "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": 1 + 20000}, {"DrvMotSeqNr": 2,"DrvMotSpeed": 36383}]}})

    @allure.title(
        "获取|通知GB32960数据_DrvMotTorque_信号丢失_初始值_超范围值_电机2") #v2.1需求
    @pytest.mark.sanity
    def test_caseid_1987449(self):
        self.sd_tester.write_multi_ccp({4:6,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr01, 'WhlMotSysTqEstIsgTqAct', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr06, 'IsgTqActIsgTqAct', 20.0)
        for i in [0.0, 10.0, 2652.0, 4553.0]:  # 信号最大只能到16383
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr06, 'IsgTqActIsgTqAct', i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2,
                                    "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotTorque": 1 * 10 + 20000},
                                                   {"DrvMotSeqNr": 2,"DrvMotTorque": i * 10 + 20000}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 2,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotTorque": 1 * 10 + 20000},
                                                                                         {"DrvMotSeqNr": 2,"DrvMotTorque": 65530}]}}},timeout=2)
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 2,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotTorque": 0},
                                                                                         {"DrvMotSeqNr": 2,"DrvMotTorque": 0}]}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2,
                                    "DrvMotList": [{"DrvMotTorque": 1 * 10 + 20000},
                                                   {"DrvMotTorque": 65530}]}})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr06, 'IsgTqActIsgTqAct', 4554.0)
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2,
                                    "DrvMotList": [{"DrvMotTorque": 1 * 10 + 20000},
                                                   {"DrvMotTorque": 65535}]}})

    @allure.title("获取|通知GB32960数据_DrvMotT_信号丢失_初始值_电机2")#2.1需求
    @pytest.mark.full
    def test_caseid_1987450(self):
        self.sd_tester.write_multi_ccp({4:6,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr03, 'WhlMotSysMotT', 0)
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr03, 'IsgMotT', 20)
        for i in [0, 87, 178, 254, 255]:
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr03, 'IsgMotT', i)
            if i - 50 >= -40:
                sts = i - 50 + 40
            elif i - 50 < -40:
                sts = 0
            else:
                sts = False
            self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotT": 0}, {"DrvMotSeqNr": 2,"DrvMotT": sts}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 2,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotT": 0},
                                                                                         {"DrvMotSeqNr": 2,"DrvMotT": 245}]}}},timeout=2)
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 2,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotT": 0},
                                                                                         {"DrvMotSeqNr": 2,"DrvMotT": 0}]}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotT": 0}, {"DrvMotSeqNr": 2,"DrvMotT": 245}]}})

    @allure.title("获取|通知GB32960数据_MotCtrlrInpUDc_信号丢失_初始值_电机2")#2.1需求
    @pytest.mark.full
    def test_caseid_1987451(self):
        self.sd_tester.write_multi_ccp({4:6,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr02, 'WhlMotSysUdc', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr05, 'IsgUDc', 20.0)
        sleep(0.5)
        for i in [0.0, 200.0, 178.0, 255.0, 365.0, 511.0]:
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr05, 'IsgUDc', i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2,
                                    "DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrInpUDc": 1 * 10}, {"DrvMotSeqNr": 2,"MotCtrlrInpUDc": i * 10}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 2,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrInpUDc": 1 * 10},
                                                                                         {"DrvMotSeqNr": 2,"MotCtrlrInpUDc": 5110}]}}},timeout=2)
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 2,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrInpUDc": 0},
                                                                                         {"DrvMotSeqNr": 2,"MotCtrlrInpUDc": 0}]}}},timeout=2)
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2,
                                    "DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrInpUDc": 1 * 10}, {"DrvMotSeqNr": 2,"MotCtrlrInpUDc": 5110}]}})
        
    @allure.title("获取|通知GB32960数据_MotCtrlrIDc_信号丢失_初始值_电机2") #v2.1需求
    @pytest.mark.sanity
    def test_caseid_1987455(self):
        self.sd_tester.write_multi_ccp({4:6,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysIdc', 1)
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr03, 'IsgIDc', 20)
        sleep(0.5)
        for i in [0, 278, 9999, 16382, 16383]:#信号最大值为16383
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr03, 'IsgIDc', i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2,
                                    "DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrIDc": 1813},
                                                   {"DrvMotSeqNr": 2,"MotCtrlrIDc": int((i * 0.1 - 818.8 + 1000) * 10)}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 2,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrIDc": 1813},
                                                                                         {"DrvMotSeqNr": 2,"MotCtrlrIDc": int((i * 0.1 - 818.8 + 1000) * 10)}]}}},timeout=2)
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 2,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrIDc": 0},
                                                                                         {"DrvMotSeqNr": 2,"MotCtrlrIDc": 0}]}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2,
                                    "DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrIDc": 1813},
                                                   {"DrvMotSeqNr": 2,"MotCtrlrIDc": int((i * 0.1 - 818.8 + 1000) * 10)}]}})

    @allure.title("获取|通知GB32960数据_DrvMotSts_0_16_信号丢失_初始值_电机1")#2.1需求
    @pytest.mark.smoke
    def test_caseid_1987466(self):
        self.sd_tester.write_multi_ccp({4:8,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr06, 'IemGenericModStatusRms', 1)
        for i in list(range(16)) + [5]:
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.IemPropFr06, 'IemGenericModStatusRms', i)
            sleep(0.5)
            if i in [1, 2, 4]:
                sts = i
            elif i == 0:
                sts = 255
            elif i == 5:
                sts = 254
            else:
                sts = 3
            self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSts": sts}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSts": 254}]}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSts": 3}]}}},timeout=2)
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSts": 254}]}})

    @allure.title("获取|通知GB32960数据_DrvMotCtrlrT_信号丢失_初始值_电机1")#2.1需求
    @pytest.mark.full
    def test_caseid_1987467(self):
        self.sd_tester.write_multi_ccp({4:8,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr03, 'WhlMotSysInvrT', 1)
        for i in [0, 10, 87, 178, 254, 255]:
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.IemPropFr03, 'WhlMotSysInvrT', i)
            if i - 50 >= -40:
                sts = i - 50 + 40
            elif i - 50 < -40:
                sts = 0
            else:
                sts = False
            self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotCtrlrT": sts}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotCtrlrT": 245}]}}},timeout=2)
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotCtrlrT": 0}]}}},timeout=2)
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotCtrlrT": 245}]}})

    @allure.title("获取|通知GB32960数据_DrvMotSpeed_信号丢失_初始值_电机1_400v") #2.1需求
    @pytest.mark.full
    def test_caseid_1987468(self):
        self.sd_tester.write_multi_ccp({4:8,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr02, 'WhlMotSysSpdAct', 1)
        for i in [0, 7999, 16383]:  # 信号最大只能到16383
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr02, 'WhlMotSysSpdAct', i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSpeed": i + 20000}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"DrvMotSpeed": 36383}]}}},timeout=2)
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": 0}]}}},timeout=2)
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSpeed": 36383}]}})

    @allure.title(
        "获取|通知GB32960数据_DrvMotTorque_超范围值_信号丢失_初始值_电机1")#v2.1需求
    @pytest.mark.full
    def test_caseid_1987471(self):
        self.sd_tester.write_multi_ccp({4:8,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr01, 'WhlMotSysTqEstIsgTqAct', 100.0)
        for i in [0.0, 10.0, 2652.0, 4553.0]:
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr01, 'WhlMotSysTqEstIsgTqAct', i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotTorque": i * 10 + 20000}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotTorque": 65530}]}}},timeout=2)
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotTorque": 0}]}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotTorque": 65530}]}})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr01, 'WhlMotSysTqEstIsgTqAct', 4554.0)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotTorque": 65535}]}}})

    @allure.title("获取|通知GB32960数据_DrvMotT_信号丢失_初始值_电机1")#2.1需求
    @pytest.mark.sanity
    def test_caseid_1987474(self):
        self.sd_tester.write_multi_ccp({4:8,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr03, 'WhlMotSysMotT', 1)
        for i in [0, 87, 178, 254, 255]:
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.IemPropFr03, 'WhlMotSysMotT', i)
            if i - 50 >= -40:
                sts = i - 50 + 40
            elif i - 50 < -40:
                sts = 0
            else:
                sts = False
            self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotT": sts}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotT": 245}]}}},timeout=2)
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotT": 0}]}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotT": 245}]}})

    @allure.title("获取|通知GB32960数据_MotCtrlrInpUDc_信号丢失_初始值_电机1")#2.1需求
    @pytest.mark.sanity
    def test_caseid_1987475(self):
        self.sd_tester.write_multi_ccp({4:8,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr02, 'WhlMotSysUdc', 1.0)
        for i in [0.0, 200.0, 178.0, 255.0, 365.0, 511.0]:#信号最大值为2044
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr02, 'WhlMotSysUdc', i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"MotCtrlrInpUDc": i * 10}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"MotCtrlrInpUDc": 5110}]}}},timeout=2)
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrInpUDc": 0}]}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"MotCtrlrInpUDc": 5110}]}})
     
    @allure.title(
        "获取|通知GB32960数据_MotCtrlrIDc_信号丢失_初始值_电机1")#2.1需求
    @pytest.mark.full
    def test_caseid_1987478(self):
        self.sd_tester.write_multi_ccp({4:8,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysIdc', 1)
        for i in [0, 278, 9999, 16382, 16383]:
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysIdc', i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1,
                                    "DrvMotList": [{"DrvMotSeqNr": 1, "MotCtrlrIDc": int((i * 0.1 - 818.8 + 1000) * 10)}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrIDc": 18195}]}}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrIDc": 0}]}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data({"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrIDc": 18195}]}})
        
    @allure.title("获取|通知GB32960数据_DrvMotQnty_400v_正常值_默认值")#v2.1 需求
    @pytest.mark.smoke
    def test_caseid_1987622(self):
        self.sd_tester.write_multi_ccp({4:8,962:0})#一个电机
        self.ck_GB32960Data_and_GetGB32960Data({"DriveMotorData": {"DrvMotQnty": 1,"DrvMotList": [{"DrvMotSeqNr": 1}]}})
        self.del_s2s_db()#删除数据库
        sleep(2)
        self.sd_tester.write_multi_ccp({4:255,962:0})#一个电机
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data({"DriveMotorData": {"DrvMotQnty": 2,"DrvMotList": [{"DrvMotSeqNr": 1},{"DrvMotSeqNr": 2}]}})
        self.sd_tester.write_multi_ccp({4:6,962:0})#两个电机
        self.ck_GB32960Data_and_GetGB32960Data({"DriveMotorData": {"DrvMotQnty": 2,"DrvMotList": [{"DrvMotSeqNr": 1},{"DrvMotSeqNr": 2}]}})
        self.del_s2s_db()#删除数据库
        sleep(2)
        self.sd_tester.write_multi_ccp({4:255,962:0})#两个电机
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data({"DriveMotorData": {"DrvMotQnty": 2,"DrvMotList": [{"DrvMotSeqNr": 1},{"DrvMotSeqNr": 2}]}})


@allure.feature("SOA服务接口")
@allure.story("互联服务/GB32960")
@pytest.mark.wjj
class TestGB32960ServiceSetup(TestBase):
    '''MOCKMCU'''

    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.sd_tester.write_single_ccp(962, 0)
        sleep(1)
        self.partner = S2sBaseClass([("GB32960Service", "client")])
        self.partner.method_default_timeout = 0.1

    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.partner.empty_all(1)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)    
        
    def ck_GB32960Data_and_GetGB32960Data(self, ck_dict):
        """校验指定GB32960Data事件，并请求GetGB32960Data获取结果"""
        self.partner.ck_s2s_event(GB32960_SERVICE_CLIENT, "GB32960Data",
                                  {"info": ck_dict})
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": ck_dict})

    @allure.title("获取|通知GB32960数据_VehSpeed信号丢失_超范围值")
    @pytest.mark.full
    def test_caseid_1980428(self):
        self.ipdu.set(self.ipdu.backbonefr.DimBackBoneFr04, 'VehSpdIndcdVeSpdIndcdUnit', 0)
        self.ipdu.set(self.ipdu.backbonefr.DimBackBoneFr04, 'VehSpdIndcdVehSpdIndcd', 1)
        for i in (0, 100, 125, 220):
            logger.info(f"现在是{i}")
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.backbonefr.DimBackBoneFr04, 'VehSpdIndcdVehSpdIndcd', i)
            self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"VehSpeed": i * 10}})
        self.ipdu.pause_bus_send("backbonefr")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"VehSpeed": 2200}}})
        self.ipdu.resume_bus_send("backbonefr")
        self.ipdu.set(self.ipdu.backbonefr.DimBackBoneFr04, 'VehSpdIndcdVehSpdIndcd', 221)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"VehSpeed": 65535}})

    @allure.title("获取|通知GB32960数据_AccumMilg_正常值_信号丢失_超范围值")
    @pytest.mark.full
    def test_caseid_1980429(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr10, 'TotDstTrvldHiResl', 1)
        for i in (0, 1000, 3564324,999999999,999999999):
            logger.info(f"现在是{i}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr10, 'TotDstTrvldHiResl', i)
            sleep(0.2)
            self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"AccumMilg":int(i/100)}})
        self.ipdu.pause_bus_send("backbonefr")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"AccumMilg": 9999999}}})
        self.ipdu.resume_bus_send("backbonefr")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr10, 'TotDstTrvldHiResl', 1999999999)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"AccumMilg": 16777215}})

    @allure.title("获取|通知GB32960数据_VehSts信号丢失_超范围值")
    @pytest.mark.full
    def test_caseid_1980431(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 13)
        for i in (0, 1, 2, 11):
            logger.info(f"现在是{i}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', i)
            sleep(0.2)
            self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"VehSts": 2}})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 13)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"VehSts": 1}})
        self.ipdu.pause_bus_send("backbonefr")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"VehSts": 1}}})
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"VehSts": 1}})


@allure.feature("SOA服务接口")
@allure.story("互联服务/GB32960")
@pytest.mark.wjj
@pytest.mark.babai
class TestGB32960_800v(TestBase):
    '''800V车GB32960'''
    def before_class(self, ecu):  # 用例执行前处理
        super().before_class(self, ecu)
        self.sd_tester.tester_present()
        self.sd_tester.write_single_ccp(962, 2)
        sleep(1)
        self.partner = GNSSServiceServer([("GB32960Service", "client")])

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.partner.empty_all(1)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        sleep(1)
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):  # 用例执行后处理
        self.sd_tester.stop_tester_present()
        self.partner.stop_operators()
        super().after_class(self, ecu)
        
    def ck_GB32960Data_and_GetGB32960Data(self, ck_dict):
        """校验指定GB32960Data事件，并请求GetGB32960Data获取结果"""
        self.partner.ck_s2s_event(GB32960_SERVICE_CLIENT, "GB32960Data",
                                  {"info": ck_dict})
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": ck_dict})

    @allure.title("获取|通知GB32960数据_HvBattSocToltalU800_0_511")#800v车 2.0需求
    @pytest.mark.smoke
    def test_caseid_1984783(self):
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc800', 1.0)
        for i in (0.0, 10.0, 199.0, 510.0, 511.0):
            logger.info(f"现在是{i}")
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc800', i)
            self.partner.empty_all(0.5)
            self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"HvBattSocToltalU": i * 10}})

    @allure.title("获取|通知GB32960数据_HvBattSocToltalU800信号丢失")#800v车 2.0需求
    @pytest.mark.full
    def test_caseid_1984788(self):
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc800', 1.0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc800', 10.0)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"HvBattSocToltalU": 100}})
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(2)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"HvBattSocToltalU": 100}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"HvBattSocToltalU": 100}})

    @allure.title("获取|通知GB32960数据_HvBattSocToltalU800信号初始值")#800v车 2.0需求
    @pytest.mark.full
    def test_caseid_1984789(self):
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc800', 1.0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc800', 10.0)
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"HvBattSocToltalU": 100}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"VehStatus": {"HvBattSocToltalU": 0}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data({"VehStatus": {"HvBattSocToltalU": 100}})

    @allure.title("获取|通知GB32960数据_ReChrglEgyStorgU800_正常值")#v2.0需求
    @pytest.mark.full
    def test_caseid_1984811(self):
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc800', 2)
        for i in [0, 72, 245, 511, 2046, 2047]:
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc800', i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysList": [{"ReChrglEgyStorgU": int(i * 0.25 * 10)}]}})

    @allure.title("获取|通知GB32960数据_ReChrglEgyStorgU800_初始值")#v2.0需求
    @pytest.mark.full
    def test_caseid_1984812(self):
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc800', 2)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc800', 72)
        self.ck_GB32960Data_and_GetGB32960Data(
            {"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysList": [{"ReChrglEgyStorgU": 180}]}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"HVBatteryVoltageData": {
                                                  "ReChrglEgyStorgSubSysList": [{"ReChrglEgyStorgU": 0}]}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
            {"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysList": [{"ReChrglEgyStorgU": 180}]}})

    @allure.title("获取|通知GB32960数据_ReChrglEgyStorgU800_初始值")#v2.0需求
    @pytest.mark.full
    def test_caseid_1984813(self):
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc800', 2)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc800', 72)
        self.ck_GB32960Data_and_GetGB32960Data(
            {"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysList": [{"ReChrglEgyStorgU": 180}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"HVBatteryVoltageData": {
                                                  "ReChrglEgyStorgSubSysList": [{"ReChrglEgyStorgU": 180}]}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
            {"HVBatteryVoltageData": {"ReChrglEgyStorgSubSysList": [{"ReChrglEgyStorgU": 180}]}})
        
    @allure.title("获取|通知GB32960数据_MotCtrlrInpUDc800_电机1_800v")#2.1需求
    @pytest.mark.smoke
    def test_caseid_1987486(self):
        self.sd_tester.write_multi_ccp({4:8,962:2})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysUDc800', 1.0)
        for i in [0.0, 200.0, 178.0, 255.0, 365.0, 511.0]:#信号最大值为4095
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysUDc800', i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSeqNr":1,"MotCtrlrInpUDc": i * 10}]}})

    @allure.title("获取|通知GB32960数据_MotCtrlrInpUDc800_信号丢失_电机1_800v")#2.1需求
    @pytest.mark.full
    def test_caseid_1987487(self):
        self.sd_tester.write_multi_ccp({4:8,962:2})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysUDc800', 1.0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysUDc800', 200.0)
        self.ck_GB32960Data_and_GetGB32960Data(
            {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrInpUDc": 2000}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrInpUDc": 2000}]}}},timeout=2)
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
            {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrInpUDc": 2000}]}})

    @allure.title("获取|通知GB32960数据_MotCtrlrInpUDc800_初始值_电机1_800v")#2.1需求
    @pytest.mark.full
    def test_caseid_1987488(self):
        self.sd_tester.write_multi_ccp({4:8,962:2})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysUDc800', 1.0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysUDc800', 200.0)
        self.ck_GB32960Data_and_GetGB32960Data(
            {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"MotCtrlrInpUDc": 2000}]}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrInpUDc": 0}]}}},timeout=2)
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
            {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"MotCtrlrInpUDc": 2000}]}})

    @allure.title("获取|通知GB32960数据_DrvMotSpeed800_电机1_800v")  # v2.1需求
    @pytest.mark.sanity
    def test_caseid_1987489(self):
        self.sd_tester.write_multi_ccp({4:8,962:2})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysSpdAct800', 1)
        for i in [0, 7999, 16383]:  # 信号最大只能到16383
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysSpdAct800', i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSpeed": i + 20000}]}})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysSpdAct800', -20001)
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSpeed": 0}]}})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysSpdAct800', -20000)
        logger.info(f'信号是')
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSpeed": 0}]}})

    @allure.title("获取|通知GB32960数据_DrvMotSpeed800_信号丢失_电机1_800v")  # v2.1需求
    @pytest.mark.full
    def test_caseid_1987493(self):
        self.sd_tester.write_multi_ccp({4:8,962:2})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysSpdAct800', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysSpdAct800', 7999)
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": 27999}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": 27999}]}}},timeout=2)
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": 27999}]}})

    @allure.title("获取|通知GB32960数据_DrvMotSpeed800_初始值_电机1_800v")  # v2.1需求
    @pytest.mark.full
    def test_caseid_1987494(self):
        self.sd_tester.write_multi_ccp({4:8,962:2})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysSpdAct800', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysSpdAct800', 7999)
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": 27999}]}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 1,
                                                                          "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": 0}]}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": 27999}]}})

    @allure.title("获取|通知GB32960数据_MotCtrlrInpUDc_电机2_800v")#2.1需求
    @pytest.mark.sanity
    def test_caseid_1987496(self):
        self.sd_tester.write_multi_ccp({4:6,962:2})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysUDc800', 0.0)
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr05, 'IsgUDc800', 20.0)
        self.partner.empty_all()
        for i in [0, 10, 4095]:#信号最大值为4095
            logger.info(f'信号{i}')
            self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr05, 'IsgUDc800', i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2,
                                    "DrvMotList": [{"DrvMotSeqNr":1,"MotCtrlrInpUDc": 0}, {"DrvMotSeqNr":2,"MotCtrlrInpUDc": int( i * 0.25 * 10)}]}})

    @allure.title("获取|通知GB32960数据_MotCtrlrInpUDc800_信号丢失_电机2_800v")#2.1需求
    @pytest.mark.full
    def test_caseid_1987498(self):
        self.sd_tester.write_multi_ccp({4:6,962:2})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysUDc800', 0.0)
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr05, 'IsgUDc800', 20.0)
        self.partner.empty_all(0.2)
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr05, 'IsgUDc800', 200.0)
        self.ck_GB32960Data_and_GetGB32960Data(
            {"DriveMotorData": {"DrvMotQnty": 2,
                                "DrvMotList": [{"DrvMotSeqNr":1,"MotCtrlrInpUDc": 0}, {"DrvMotSeqNr":2,"MotCtrlrInpUDc": 2000}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 2,
                                                                          "DrvMotList": [{"DrvMotSeqNr":1,"MotCtrlrInpUDc": 0},
                                                                                         {"DrvMotSeqNr":2,"MotCtrlrInpUDc": 2000}]}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2,
                                    "DrvMotList": [{"DrvMotSeqNr":1,"MotCtrlrInpUDc": 0}, {"DrvMotSeqNr":2,"MotCtrlrInpUDc": 2000}]}})

    @allure.title("获取|通知GB32960数据_MotCtrlrInpUDc800_初始值_电机2_800v")#2.1需求
    @pytest.mark.full
    def test_caseid_1987500(self):
        self.sd_tester.write_multi_ccp({4:6,962:2})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysUDc800', 0.0)
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr05, 'IsgUDc800', 20.0)
        self.partner.empty_all(0.2)
        self.ipdu.set(self.ipdu.propulsioncan.IgmMgmPropFr05, 'IsgUDc800', 200.0)
        self.ck_GB32960Data_and_GetGB32960Data(
            {"DriveMotorData": {"DrvMotQnty": 2,
                                "DrvMotList": [{"DrvMotSeqNr":1,"MotCtrlrInpUDc": 0}, {"DrvMotSeqNr":2,"MotCtrlrInpUDc": 2000}]}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 2,
                                                                          "DrvMotList": [{"DrvMotSeqNr":1,"MotCtrlrInpUDc": 0},
                                                                                         {"DrvMotSeqNr":2,"MotCtrlrInpUDc": 0}]}}},timeout=2)
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2,
                                    "DrvMotList": [{"DrvMotSeqNr":1,"MotCtrlrInpUDc": 0}, {"DrvMotSeqNr":2,"MotCtrlrInpUDc": 2000}]}})

    @allure.title("获取|通知GB32960数据_DrvMotSpeed_电机2_800v") #2.1需求
    @pytest.mark.smoke
    def test_caseid_1987502(self):
        self.sd_tester.write_multi_ccp({4:6,962:2})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysSpdAct800', 0)
        self.ipdu.set(self.ipdu.propulsioncan.MgmPropFr05, 'IsgSpdActSgn800', 1)
        for i in [0, 7999, 16383]:  # 信号最大只能到16383
            logger.info(f'信号{i}')
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.propulsioncan.MgmPropFr05, 'IsgSpdActSgn800', i)
            self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2,
                                    "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": 20000}, {"DrvMotSeqNr":2,"DrvMotSpeed": i + 20000}]}})
        self.ipdu.set(self.ipdu.propulsioncan.MgmPropFr05, 'IsgSpdActSgn800', -20001)
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2,
                                    "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": 20000}, {"DrvMotSeqNr":2,"DrvMotSpeed": 0}]}})

    @allure.title("获取|通知GB32960数据_DrvMotSpeed_信号丢失_电机2_800v") #2.1需求
    @pytest.mark.full
    def test_caseid_1987504(self):
        self.sd_tester.write_multi_ccp({4:6,962:2})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysSpdAct800', 0)
        self.ipdu.set(self.ipdu.propulsioncan.MgmPropFr05, 'IsgSpdActSgn800', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.MgmPropFr05, 'IsgSpdActSgn800', 10)
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2,
                                    "DrvMotList": [{"DrvMotSeqNr":1,"DrvMotSpeed": 20000}, {"DrvMotSeqNr":2,"DrvMotSpeed": 20010}]}})
        self.ipdu.pause_bus_send("propulsioncan")
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 2,
                                                                          "DrvMotList": [{"DrvMotSeqNr":1,"DrvMotSpeed": 20000},
                                                                                         {"DrvMotSeqNr":2,"DrvMotSpeed": 20010}]}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2,
                                    "DrvMotList": [{"DrvMotSeqNr":1,"DrvMotSpeed": 20000}, {"DrvMotSeqNr":2,"DrvMotSpeed": 20010}]}})

    @allure.title("获取|通知GB32960数据_DrvMotSpeed_初始值_电机2_800v") #2.1需求
    @pytest.mark.full
    def test_caseid_1987505(self):
        self.sd_tester.write_multi_ccp({4:6,962:2})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysSpdAct800', 0)
        self.ipdu.set(self.ipdu.propulsioncan.MgmPropFr05, 'IsgSpdActSgn800', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.MgmPropFr05, 'IsgSpdActSgn800', 10)
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2,
                                    "DrvMotList": [{"DrvMotSeqNr":1,"DrvMotSpeed": 20000}, {"DrvMotSeqNr":2,"DrvMotSpeed": 20010}]}})
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(GB32960_SERVICE_CLIENT, "GetGB32960Data", {},
                                              {"out": {"DriveMotorData": {"DrvMotQnty": 2,
                                                                          "DrvMotList": [{"DrvMotSeqNr":1,"DrvMotSpeed": 0},
                                                                                         {"DrvMotSeqNr":2,"DrvMotSpeed": 0}]}}})
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 2,
                                    "DrvMotList": [{"DrvMotSeqNr":1,"DrvMotSpeed": 20000}, {"DrvMotSeqNr":2,"DrvMotSpeed": 20010}]}})
        
    @allure.title("获取|通知GB32960数据_DrvMotSpeed_电机1设置第二个电机信号无变化800v") #2.1需求
    @pytest.mark.sanity
    def test_caseid_1987506(self):
        self.sd_tester.write_multi_ccp({4:8,962:2})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysSpdAct800', 0)
        self.ipdu.set(self.ipdu.propulsioncan.MgmPropFr05, 'IsgSpdActSgn800', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.MgmPropFr05, 'IsgSpdActSgn800', 1)
        self.ck_GB32960Data_and_GetGB32960Data(
                {"DriveMotorData": {"DrvMotQnty": 1,
                                    "DrvMotList": [{"DrvMotSeqNr":1,"DrvMotSpeed": 20000}]}})
        
    @allure.title("获取|通知GB32960数据_DrvMotQnty_800v_正常值_默认值")#v2.1 需求
    @pytest.mark.sanity
    def test_caseid_1987623(self):
        self.sd_tester.write_multi_ccp({4:8,962:2})#一个电机
        self.ck_GB32960Data_and_GetGB32960Data({"DriveMotorData": {"DrvMotQnty": 1,"DrvMotList": [{"DrvMotSeqNr": 1}]}})
        self.del_s2s_db()#删除数据库
        sleep(2)
        self.sd_tester.write_multi_ccp({4:255,962:2})#一个电机
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data({"DriveMotorData": {"DrvMotQnty": 2,"DrvMotList": [{"DrvMotSeqNr": 1},{"DrvMotSeqNr": 2}]}})
        self.sd_tester.write_multi_ccp({4:6,962:2})#两个电机
        self.ck_GB32960Data_and_GetGB32960Data({"DriveMotorData": {"DrvMotQnty": 2,"DrvMotList": [{"DrvMotSeqNr": 1},{"DrvMotSeqNr": 2}]}})
        self.del_s2s_db()#删除数据库
        sleep(2)
        self.sd_tester.write_multi_ccp({4:7,962:2})#两个电机
        self.restart_bgm_and_connect_service(GB32960_SERVICE_CLIENT,resume_all_bus=False)
        self.ck_GB32960Data_and_GetGB32960Data({"DriveMotorData": {"DrvMotQnty": 2,"DrvMotList": [{"DrvMotSeqNr": 1},{"DrvMotSeqNr": 2}]}})