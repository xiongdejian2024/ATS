# -*- coding: utf-8 -*-

"""
@Time    : 2024/07/25 23:56
@Author  : lei.tao
@Email   : lei.tao@jiduauto.com
"""
import time
import pytest
import allure
from xat_ecu.legacy.common.data_type_handing import logger
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import S2sBaseClass
from xat_ecu.legacy.soa_partner.src.partner_const import *


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号组包含负数的场景")
class TestGB32960ServiceSignalNegativeCheck(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("GB32960Service", 'client')])
        self.partner_key = "GB32960Service" + '_client'
        time.sleep(15)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 

    def after_each_func(self, ecu):
        self.partner.empty_all()
        super().after_each_func(ecu)

    @allure.title("GB32960Service::GB32960Data_IsgIDc::PropulsionCAN::0x13A信号为负值时无异常")
    def test_caseid_1988106(self):
        self.sd_tester.write_multi_ccp({4:6,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysIdc', 1)
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x13A")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgIDc", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgIDc", -1.0)
        self.partner.ck_s2s_event(self.partner_key, "GB32960Data", {"info":{"DriveMotorData": {"DrvMotQnty": 2,"DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrIDc": 1813}, {"DrvMotSeqNr": 2,"MotCtrlrIDc":int((-1.0 + 1000) * 10)}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgIDc", 0.0)

    @allure.title("GB32960Service::GB32960Data_IsgInvrT::PropulsionCAN::0x275信号为负值时无异常")
    def test_caseid_1988110(self):
        self.sd_tester.write_multi_ccp({4:6,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr03, 'WhlMotSysInvrT', 1)
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x275")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgInvrT", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgInvrT", -1.0)
        self.partner.ck_s2s_event(self.partner_key, "GB32960Data", {"info":{"DriveMotorData": {"DrvMotQnty": 2,"DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotCtrlrT": 0}, {"DrvMotSeqNr": 2,"DrvMotCtrlrT": 39}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgInvrT", 0.0)

    @allure.title("GB32960Service::GB32960Data_IsgMotT::PropulsionCAN::0x13A信号为负值时无异常")
    def test_caseid_1988107(self):
        self.sd_tester.write_multi_ccp({4:6,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr03, 'WhlMotSysMotT', 0)
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x13A")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgMotT", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgMotT", -1.0)
        self.partner.ck_s2s_event(self.partner_key, "GB32960Data", {"info":{"DriveMotorData": {"DrvMotQnty": 2,"DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotT": 0}, {"DrvMotSeqNr": 2,"DrvMotT": 39}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgMotT", 0.0)

    @allure.title("GB32960Service::GB32960Data_IsgSpdActSgn::PropulsionCAN::0x095信号为负值时无异常")
    def test_caseid_1988109(self):
        self.sd_tester.write_multi_ccp({4:6,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr02, 'WhlMotSysSpdAct', 1)
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x095")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgSpdActSgn", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgSpdActSgn", -1.0)
        self.partner.ck_s2s_event(self.partner_key, "GB32960Data", {"info":{"DriveMotorData": {"DrvMotQnty": 2,"DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": 1 + 20000}, {"DrvMotSeqNr": 2,"DrvMotSpeed": 19999}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgSpdActSgn", 0.0)

    @allure.title("GB32960Service::GB32960Data_IsgSpdActSgn800::PropulsionCAN::0x094信号为负值时无异常")
    def test_caseid_1988105(self):
        self.sd_tester.write_multi_ccp({4:6,962:2})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysSpdAct800', 0)
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x094")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgSpdActSgn800", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgSpdActSgn800", -1.0)
        self.partner.ck_s2s_event(self.partner_key, "GB32960Data", {"info":{"DriveMotorData": {"DrvMotQnty": 2,"DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": 20000}, {"DrvMotSeqNr":2,"DrvMotSpeed": -1.0 + 20000}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgSpdActSgn800", 0.0)

    @allure.title("GB32960Service::GB32960Data_IsgTqActIsgTqAct::PropulsionCAN::0x095信号为负值时无异常")
    def test_caseid_1988108(self):
        self.sd_tester.write_multi_ccp({4:6,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr01, 'WhlMotSysTqEstIsgTqAct', 1.0)
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x095")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgTqActIsgTqAct", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgTqActIsgTqAct", -1.0)
        self.partner.ck_s2s_event(self.partner_key, "GB32960Data", {"info":{"DriveMotorData": {"DrvMotQnty": 2,"DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotTorque": 1 * 10 + 20000},{"DrvMotSeqNr": 2,"DrvMotTorque": -1.0 * 10 + 20000}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgTqActIsgTqAct", 0.0)

    @allure.title("GB32960Service::GB32960Data_WhlMotSysIdc::PropulsionCAN::0x063信号为负值时无异常")
    def test_caseid_1988111(self):
        self.sd_tester.write_multi_ccp({4:8,962:0})
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x063")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysIdc", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysIdc", -1.0)
        self.partner.ck_s2s_event(self.partner_key, "GB32960Data", {"info":{"DriveMotorData": {"DrvMotQnty": 1,"DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrIDc":int((-1.0 + 1000) * 10)}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysIdc", 0.0)

    @allure.title("GB32960Service::GB32960Data_WhlMotSysInvrT::PropulsionCAN::0x305信号为负值时无异常")
    def test_caseid_1988115(self):
        self.sd_tester.write_multi_ccp({4:8,962:0})
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x305")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysInvrT", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysInvrT", -1.0)
        self.partner.ck_s2s_event(self.partner_key, "GB32960Data", {"info":{"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotCtrlrT": 39}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysInvrT", 0.0)

    @allure.title("GB32960Service::GB32960Data_WhlMotSysMotT::PropulsionCAN::0x305信号为负值时无异常")
    def test_caseid_1988112(self):
        self.sd_tester.write_multi_ccp({4:8,962:0})
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x305")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysMotT", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysMotT", -1.0)
        self.partner.ck_s2s_event(self.partner_key, "GB32960Data", {"info":{"DriveMotorData": {"DrvMotQnty": 1,"DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotT": 0}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysMotT", 0.0)

    @allure.title("GB32960Service::GB32960Data_WhlMotSysSpdAct::PropulsionCAN::0x060信号为负值时无异常")
    def test_caseid_1988114(self):
        self.sd_tester.write_multi_ccp({4:8,962:0})
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x060")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysSpdAct", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysSpdAct", -1.0)
        self.partner.ck_s2s_event(self.partner_key, "GB32960Data", {"info":{"DriveMotorData": {"DrvMotQnty": 1,"DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": 19999}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysSpdAct", 0.0)

    @allure.title("GB32960Service::GB32960Data_WhlMotSysTqEstIsgTqAct::PropulsionCAN::0x04C信号为负值时无异常")
    def test_caseid_1988113(self):
        self.sd_tester.write_multi_ccp({4:8,962:0})
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x04C")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysTqEstIsgTqAct", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysTqEstIsgTqAct", -1.0)
        self.partner.ck_s2s_event(self.partner_key, "GB32960Data", {"info":{"DriveMotorData": {"DrvMotQnty": 1,"DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotTorque": 19990}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysTqEstIsgTqAct", 0.0)

    @allure.title("GB32960Service::GetGB32960Data_HvBattIDc1::PropulsionCAN::0x143信号为负值时无异常")
    def test_caseid_1988118(self):
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x143")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "HvBattIDc1", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "HvBattIDc1", -1.0)
        self.partner.send_request_and_ck_resp(self.partner_key, "GetGB32960Data", {}, {"out":{"VehStatus": {"HvBattSocToltalI": ((-1.0 + 1000) * 10)}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "HvBattIDc1", 0.0)

    @allure.title("GB32960Service::GetGB32960Data_IsgIDc::PropulsionCAN::0x13A信号为负值时无异常")
    def test_caseid_1988119(self):
        self.sd_tester.write_multi_ccp({4:6,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysIdc', 1)
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x13A")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgIDc", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgIDc", -1.0)
        self.partner.send_request_and_ck_resp(self.partner_key, "GetGB32960Data", {}, {"out":{"DriveMotorData": {"DrvMotQnty": 2,"DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrIDc": 1813}, {"DrvMotSeqNr": 2,"MotCtrlrIDc":int((-1.0 + 1000) * 10)}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgIDc", 0.0)

    @allure.title("GB32960Service::GetGB32960Data_IsgInvrT::PropulsionCAN::0x275信号为负值时无异常")
    def test_caseid_1988123(self):
        self.sd_tester.write_multi_ccp({4:6,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr03, 'WhlMotSysInvrT', 1)
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x275")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgInvrT", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgInvrT", -1.0)
        self.partner.send_request_and_ck_resp(self.partner_key, "GetGB32960Data", {}, {"out":{"DriveMotorData": {"DrvMotQnty": 2,"DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotCtrlrT": 0}, {"DrvMotSeqNr": 2,"DrvMotCtrlrT": 39}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgInvrT", 0.0)

    @allure.title("GB32960Service::GetGB32960Data_IsgMotT::PropulsionCAN::0x13A信号为负值时无异常")
    def test_caseid_1988120(self):
        self.sd_tester.write_multi_ccp({4:6,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr03, 'WhlMotSysMotT', 0)
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x13A")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgMotT", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgMotT", -1.0)
        self.partner.send_request_and_ck_resp(self.partner_key, "GetGB32960Data", {}, {"out":{"DriveMotorData": {"DrvMotQnty": 2,"DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotT": 0}, {"DrvMotSeqNr": 2,"DrvMotT": 39}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgMotT", 0.0)

    @allure.title("GB32960Service::GetGB32960Data_IsgSpdActSgn::PropulsionCAN::0x095信号为负值时无异常")
    def test_caseid_1988122(self):
        self.sd_tester.write_multi_ccp({4:6,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr02, 'WhlMotSysSpdAct', 1)
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x095")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgSpdActSgn", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgSpdActSgn", -1.0)
        self.partner.send_request_and_ck_resp(self.partner_key, "GetGB32960Data", {}, {"out":{"DriveMotorData": {"DrvMotQnty": 2,"DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": 1 + 20000}, {"DrvMotSeqNr": 2,"DrvMotSpeed": 19999}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgSpdActSgn", 0.0)

    @allure.title("GB32960Service::GetGB32960Data_IsgSpdActSgn800::PropulsionCAN::0x094信号为负值时无异常")
    def test_caseid_1988117(self):
        self.sd_tester.write_multi_ccp({4:6,962:2})
        self.ipdu.set(self.ipdu.propulsioncan.IemPropFr08, 'WhlMotSysSpdAct800', 0)
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x094")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgSpdActSgn800", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgSpdActSgn800", -1.0)
        self.partner.send_request_and_ck_resp(self.partner_key, "GetGB32960Data", {}, {"out":{"DriveMotorData": {"DrvMotQnty": 2,"DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": 20000}, {"DrvMotSeqNr":2,"DrvMotSpeed": -1.0 + 20000}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgSpdActSgn800", 0.0)

    @allure.title("GB32960Service::GetGB32960Data_IsgTqActIsgTqAct::PropulsionCAN::0x095信号为负值时无异常")
    def test_caseid_1988121(self):
        self.sd_tester.write_multi_ccp({4:6,962:0})
        self.ipdu.set(self.ipdu.propulsioncan.IemEduPropFr01, 'WhlMotSysTqEstIsgTqAct', 1.0)
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x095")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgTqActIsgTqAct", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgTqActIsgTqAct", -1.0)
        self.partner.send_request_and_ck_resp(self.partner_key, "GetGB32960Data", {}, {"out":{"DriveMotorData": {"DrvMotQnty": 2,"DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotTorque": 1 * 10 + 20000},{"DrvMotSeqNr": 2,"DrvMotTorque": -1.0 * 10 + 20000}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "IsgTqActIsgTqAct", 0.0)

    @allure.title("GB32960Service::GetGB32960Data_WhlMotSysIdc::PropulsionCAN::0x063信号为负值时无异常")
    def test_caseid_1988124(self):
        self.sd_tester.write_multi_ccp({4:8,962:0})
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x063")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysIdc", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysIdc", -1.0)
        self.partner.send_request_and_ck_resp(self.partner_key, "GetGB32960Data", {}, {"out":{"DriveMotorData": {"DrvMotQnty": 1,"DrvMotList": [{"DrvMotSeqNr": 1,"MotCtrlrIDc":int((-1.0 + 1000) * 10)}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysIdc", 0.0)

    @allure.title("GB32960Service::GetGB32960Data_WhlMotSysInvrT::PropulsionCAN::0x305信号为负值时无异常")
    def test_caseid_1988128(self):
        self.sd_tester.write_multi_ccp({4:8,962:0})
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x305")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysInvrT", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysInvrT", -1.0)
        self.partner.send_request_and_ck_resp(self.partner_key, "GetGB32960Data", {}, {"out": {"DriveMotorData": {"DrvMotQnty": 1, "DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotCtrlrT":39}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysInvrT", 0.0)

    @allure.title("GB32960Service::GetGB32960Data_WhlMotSysMotT::PropulsionCAN::0x305信号为负值时无异常")
    def test_caseid_1988125(self):
        self.sd_tester.write_multi_ccp({4:8,962:0})
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x305")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysMotT", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysMotT", -1.0)
        self.partner.send_request_and_ck_resp(self.partner_key, "GetGB32960Data", {}, {"out":{"DriveMotorData": {"DrvMotQnty": 1,"DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotT": 0}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysMotT", 0.0)

    @allure.title("GB32960Service::GetGB32960Data_WhlMotSysSpdAct::PropulsionCAN::0x060信号为负值时无异常")
    def test_caseid_1988127(self):
        self.sd_tester.write_multi_ccp({4:8,962:0})
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x060")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysSpdAct", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysSpdAct", -1.0)
        self.partner.send_request_and_ck_resp(self.partner_key, "GetGB32960Data", {}, {"out":{"DriveMotorData": {"DrvMotQnty": 1,"DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": 19999}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysSpdAct", 0.0)

    @allure.title("GB32960Service::GetGB32960Data_WhlMotSysSpdAct800::PropulsionCAN::0x063信号为负值时无异常")
    def test_caseid_1988116(self):
        self.sd_tester.write_multi_ccp({4:8,962:2})
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x063")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysSpdAct800", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysSpdAct800", -1.0)
        self.partner.send_request_and_ck_resp(self.partner_key, "GetGB32960Data", {}, {"out":{"DriveMotorData": {"DrvMotQnty": 1,"DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotSpeed": -1.0 + 20000}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysSpdAct800", 0.0)

    @allure.title("GB32960Service::GetGB32960Data_WhlMotSysTqEstIsgTqAct::PropulsionCAN::0x04C信号为负值时无异常")
    def test_caseid_1988126(self):
        self.sd_tester.write_multi_ccp({4:8,962:0})
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x04C")
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysTqEstIsgTqAct", 0.0)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysTqEstIsgTqAct", -1.0)
        self.partner.send_request_and_ck_resp(self.partner_key, "GetGB32960Data", {}, {"out":{"DriveMotorData": {"DrvMotQnty": 1,"DrvMotList": [{"DrvMotSeqNr": 1,"DrvMotTorque": 19990}]}}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.propulsioncan.{msg_id}"), "WhlMotSysTqEstIsgTqAct", 0.0)



@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号组包含负数的场景")
class TestPedalServiceSignalNegativeCheck(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("PedalService", 'client')])
        self.partner_key = "PedalService" + '_client'
        time.sleep(15)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 

    def after_each_func(self, ecu):
        self.partner.empty_all()
        super().after_each_func(ecu)

    @allure.title("PedalService::BrakePedalTravel_BrkPedlTrvlAct::ChassisCAN2::0x102信号为负值时无异常")
    def test_caseid_1988103(self):
        msg_id = self.ipdu.get_signal_message("chassiscan2", "0x102")
        self.ipdu.set(eval(f"self.ipdu.chassiscan2.{msg_id}"), "BrkPedlTrvlAct", 0.0)
        self.ipdu.set(eval(f"self.ipdu.chassiscan2.{msg_id}"), "BrkPedlTrvlAct", -1.0)
        self.partner.ck_s2s_event(self.partner_key, "BrakePedalTravel", {"travel": {"travel": -1}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.chassiscan2.{msg_id}"), "BrkPedlTrvlAct", 0.0)

    @allure.title("PedalService::GetBrakePedalTravel_BrkPedlTrvlAct::ChassisCAN2::0x102信号为负值时无异常")
    def test_caseid_1988104(self):
        msg_id = self.ipdu.get_signal_message("chassiscan2", "0x102")
        self.ipdu.set(eval(f"self.ipdu.chassiscan2.{msg_id}"), "BrkPedlTrvlAct", 0.0)
        self.ipdu.set(eval(f"self.ipdu.chassiscan2.{msg_id}"), "BrkPedlTrvlAct", -1.0)
        self.partner.send_request_and_ck_resp(self.partner_key, "GetBrakePedalTravel", {"pedals": [1]}, {"out": {"travel":-1}}, timeout=3)
        self.ipdu.set(eval(f"self.ipdu.chassiscan2.{msg_id}"), "BrkPedlTrvlAct", 0.0)

