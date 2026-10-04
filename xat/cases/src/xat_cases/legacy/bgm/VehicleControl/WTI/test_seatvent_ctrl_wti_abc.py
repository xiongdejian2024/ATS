#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_seat_ctrl_abc.py
@Author      : liqi.yin_ext@jiduauto.com
@Time        : 2024/1/24 11:30
@Description: BGM车控车设空调
"""
import os
import sys
import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.soa_partner.src.partner_const import *






@allure.feature("SOA服务接口")
@allure.story("WTI通知")
class TestWTIServiceChargeLid(TestABCBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        self.soa.update(["SeatService_client", "WTIService_client"])
        sleep(2)
    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)

    def after_class(self, ecu):
        pass


    @allure.title("副驾座椅通风无报警PassSeatVentAvlSts:7")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339556?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1981263(self):
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatVentAvlSts",5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatVentAvlSts",7)
        self.soa.get_and_event_check_warning_info_list(name="Passenger Seat Wind Warning",info="0")


    @allure.title("副驾座椅通风无报警PassSeatVentAvlSts:6")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339555?projectId=46"
    )
    def test_caseid_1981262(self):
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatVentAvlSts",5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatVentAvlSts",6)
        self.soa.get_and_event_check_warning_info_list(name="Passenger Seat Wind Warning",info="0")


    @allure.title("副驾座椅通风报警PassSeatVentAvlSts:5")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339554?projectId=46"
    )
    def test_caseid_1981261(self):
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatVentAvlSts",7)
        sleep(1)
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatVentAvlSts",5)
        self.soa.get_and_event_check_warning_info_list(name="Passenger Seat Wind Warning",info="1")


    @allure.title("副驾座椅通风无报警PassSeatVentAvlSts:4")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339553?projectId=46"
    )
    def test_caseid_1981260(self):
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatVentAvlSts",3)
        sleep(1)
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatVentAvlSts",4)
        self.soa.get_and_event_check_warning_info_list(name="Passenger Seat Wind Warning",info="0")


    @allure.title("副驾座椅通风报警PassSeatVentAvlSts:3")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339552?projectId=46"
    )
    def test_caseid_1981259(self):
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatVentAvlSts",7)
        sleep(1)
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatVentAvlSts",3)
        self.soa.get_and_event_check_warning_info_list(name="Passenger Seat Wind Warning",info="1")


    @allure.title("副驾座椅通风无报警PassSeatVentAvlSts:2")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339551?projectId=46"
    )
    def test_caseid_1981258(self):
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatVentAvlSts",3)
        sleep(1)
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatVentAvlSts",2)
        self.soa.get_and_event_check_warning_info_list(name="Passenger Seat Wind Warning",info="0")


    @allure.title("副驾座椅通风无报警PassSeatVentAvlSts:1")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339550?projectId=46"
    )
    def test_caseid_1981257(self):
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatVentAvlSts",3)
        sleep(1)
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatVentAvlSts",1)
        self.soa.get_and_event_check_warning_info_list(name="Passenger Seat Wind Warning",info="0")


    @allure.title("副驾座椅通风无报警PassSeatVentAvlSts:0")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339549?projectId=46"
    )
    def test_caseid_1981256(self):
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatVentAvlSts",3)
        sleep(1)
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatVentAvlSts",0)
        self.soa.get_and_event_check_warning_info_list(name="Passenger Seat Wind Warning",info="0")


    @allure.title("主椅通风无报警DrvrSeatVentAvlSts:7")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339548?projectId=46"
    )
    def test_caseid_1981248(self):
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatVentAvlSts",5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatVentAvlSts",7)
        self.soa.get_and_event_check_warning_info_list(name="Driver Seat Wind Warning",info="0")

    @allure.title("主椅通风无报警DrvrSeatVentAvlSts:6")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339547?projectId=46"
    )
    def test_caseid_1981247(self):
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatVentAvlSts",5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatVentAvlSts",6)
        self.soa.get_and_event_check_warning_info_list(name="Driver Seat Wind Warning",info="0")

    @allure.title("主椅通风报警DrvrSeatVentAvlSts:5")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339546?projectId=46"
    )
    def test_caseid_1981246(self):
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatVentAvlSts",2)
        sleep(1)
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatVentAvlSts",5)
        self.soa.get_and_event_check_warning_info_list(name="Driver Seat Wind Warning",info="1")

    @allure.title("主椅通风无报警DrvrSeatVentAvlSts:4")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339545?projectId=46"
    )
    def test_caseid_1981245(self):
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatVentAvlSts",5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatVentAvlSts",4)
        self.soa.get_and_event_check_warning_info_list(name="Driver Seat Wind Warning",info="0")

    @allure.title("主椅通风报警DrvrSeatVentAvlSts:3")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339544?projectId=46"
    )
    def test_caseid_1981244(self):
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatVentAvlSts",6)
        sleep(1)
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatVentAvlSts",3)
        self.soa.get_and_event_check_warning_info_list(name="Driver Seat Wind Warning",info="1")

    @allure.title("主椅通风无报警DrvrSeatVentAvlSts:2")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339543?projectId=46"
    )
    def test_caseid_1981243(self):
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatVentAvlSts",5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatVentAvlSts",2)
        self.soa.get_and_event_check_warning_info_list(name="Driver Seat Wind Warning",info="0")

    @allure.title("主椅通风无报警DrvrSeatVentAvlSts:1")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339542?projectId=46"
    )
    def test_caseid_1981242(self):
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatVentAvlSts",5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatVentAvlSts",1)
        self.soa.get_and_event_check_warning_info_list(name="Driver Seat Wind Warning",info="0")

    @allure.title("主椅通风无报警DrvrSeatVentAvlSts:0")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339541?projectId=46"
    )
    def test_caseid_1981196(self):
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatVentAvlSts",5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatVentAvlSts",0)
        self.soa.get_and_event_check_warning_info_list(name="Driver Seat Wind Warning",info="0")


    @allure.title("后排左侧通风无报警SeatVentAvlStsRowSecLe:0")
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518698?projectId=46"
    )
    def test_caseid_1984999(self):
        self.bus_comm.set("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecLe",3)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecLe",0)
        self.soa.get_and_event_check_warning_info_list(name="Rear Left Seat Vent Warning", info="0")


    @allure.title("后排左侧通风无报警SeatVentAvlStsRowSecLe:1")
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518693?projectId=46"
    )
    def test_caseid_1984998(self):
        self.bus_comm.set("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecLe",3)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecLe",1)
        self.soa.get_and_event_check_warning_info_list(name="Rear Left Seat Vent Warning", info="0")


    @allure.title("后排左侧通风无报警SeatVentAvlStsRowSecLe:2")
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518691?projectId=46"
    )
    def test_caseid_1984997(self):
        self.bus_comm.set("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecLe",3)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecLe",2)
        self.soa.get_and_event_check_warning_info_list(name="Rear Left Seat Vent Warning", info="0")


    @allure.title("后排左侧通风报警SeatVentAvlStsRowSecLe:3")
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518690?projectId=46"
    )
    def test_caseid_1984996(self):
        self.bus_comm.set("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecLe",2)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecLe",3)
        self.soa.get_and_event_check_warning_info_list(name="Rear Left Seat Vent Warning", info="1")


    @allure.title("后排左侧通风无报警SeatVentAvlStsRowSecLe:4")
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518687?projectId=46"
    )
    def test_caseid_1984995(self):
        self.bus_comm.set("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecLe",3)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecLe",4)
        self.soa.get_and_event_check_warning_info_list(name="Rear Left Seat Vent Warning", info="0")


    @allure.title("后排左侧通风报警SeatVentAvlStsRowSecLe:5")
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518686?projectId=46"
    )
    def test_caseid_1984994(self):
        self.bus_comm.set("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecLe",2)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecLe",5)
        self.soa.get_and_event_check_warning_info_list(name="Rear Left Seat Vent Warning", info="1")


    @allure.title("后排左侧通风无报警SeatVentAvlStsRowSecLe:6")
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518685?projectId=46"
    )
    def test_caseid_1984993(self):
        self.bus_comm.set("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecLe",3)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecLe",6)
        self.soa.get_and_event_check_warning_info_list(name="Rear Left Seat Vent Warning", info="0")


    @allure.title("后排左侧通风无报警SeatVentAvlStsRowSecLe:7")
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518683?projectId=46"
    )
    def test_caseid_1984992(self):
        self.bus_comm.set("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecLe",3)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecLe",7)
        self.soa.get_and_event_check_warning_info_list(name="Rear Left Seat Vent Warning", info="0")


    @allure.title("后排右侧通风无报警SeatVentAvlStsRowSecRi:0")
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518712?projectId=46"
    )
    def test_caseid_1985007(self):
        self.bus_comm.set("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecRi",3)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecRi",7)
        self.soa.get_and_event_check_warning_info_list(name="Rear Right Seat Vent Warning", info="0")


    @allure.title("后排右侧通风无报警SeatVentAvlStsRowSecRi:1")
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518710?projectId=46"
    )
    def test_caseid_1985006(self):
        self.bus_comm.set_wti_signal(func=WTI_Func.ReRiSeatVentWarning,value=3)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ReRiSeatVentWarning,sig_value=1,prom_name="Rear Right Seat Vent Warning",prom_state="0")


    @allure.title("后排右侧通风无报警SeatVentAvlStsRowSecRi:2")
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518709?projectId=46"
    )
    def test_caseid_1985005(self):
        self.bus_comm.set_wti_signal(func=WTI_Func.ReRiSeatVentWarning,value=3)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ReRiSeatVentWarning,sig_value=2,prom_name="Rear Right Seat Vent Warning",prom_state="0")


    @allure.title("后排右侧通风报警SeatVentAvlStsRowSecRi:3")
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518707?projectId=46"
    )
    def test_caseid_1985004(self):
        self.bus_comm.set_wti_signal(func=WTI_Func.ReRiSeatVentWarning,value=1)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ReRiSeatVentWarning,sig_value=3,prom_name="Rear Right Seat Vent Warning",prom_state="1")


    @allure.title("后排右侧通风无报警SeatVentAvlStsRowSecRi:4")
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518706?projectId=46"
    )
    def test_caseid_1985003(self):
        self.bus_comm.set_wti_signal(func=WTI_Func.ReRiSeatVentWarning,value=3)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ReRiSeatVentWarning,sig_value=4,prom_name="Rear Right Seat Vent Warning",prom_state="0")


    @allure.title("后排右侧通风报警SeatVentAvlStsRowSecRi:5")
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518704?projectId=46"
    )
    def test_caseid_1985002(self):
        self.bus_comm.set_wti_signal(func=WTI_Func.ReRiSeatVentWarning,value=1)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ReRiSeatVentWarning,sig_value=5,prom_name="Rear Right Seat Vent Warning",prom_state="1")


    @allure.title("后排右侧通风无报警SeatVentAvlStsRowSecRi:6")
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518703?projectId=46"
    )
    def test_caseid_1985001(self):
        self.bus_comm.set_wti_signal(func=WTI_Func.ReRiSeatVentWarning,value=3)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ReRiSeatVentWarning,sig_value=6,prom_name="Rear Right Seat Vent Warning",prom_state="0")


    @allure.title("后排右侧通风无报警SeatVentAvlStsRowSecRi:7")
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518702?projectId=46"
    )
    def test_caseid_1985000(self):
        self.bus_comm.set_wti_signal(func=WTI_Func.ReRiSeatVentWarning,value=3)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ReRiSeatVentWarning,sig_value=7,prom_name="Rear Right Seat Vent Warning",prom_state="0")
