#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_seat_ctrl_abc.py
@Author      : liqi.yin_ext@jiduauto.com
@Time        : 2024/1/24 11:30
@Description: BGM车控车设座椅
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


    @allure.title("副驾座椅加热无报警PassSeatHeatgAvlSts:7")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339540?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1981057(self):
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatHeatgAvlSts", 5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatHeatgAvlSts", 7)
        self.soa.get_and_event_check_warning_info_list(name="Passenger Seat Heat Warning", info="0")


    @allure.title("副驾座椅加热无报警PassSeatHeatgAvlSts:6")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339539?projectId=46"
    )
    def test_caseid_1981056(self):
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatHeatgAvlSts",5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatHeatgAvlSts",6)
        self.soa.get_and_event_check_warning_info_list(name="Passenger Seat Heat Warning",info="0")

    @allure.title("副驾座椅加热无报警PassSeatHeatgAvlSts:5")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339538?projectId=46"
    )
    def test_caseid_1981055(self):
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatHeatgAvlSts",2)
        sleep(1)
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatHeatgAvlSts",5)
        self.soa.get_and_event_check_warning_info_list(name="Passenger Seat Heat Warning",info="1")
    @allure.title("副驾座椅加热无报警PassSeatHeatgAvlSts:4")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339537?projectId=46"
    )
    def test_caseid_1981054(self):
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatHeatgAvlSts",5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatHeatgAvlSts",4)
        self.soa.get_and_event_check_warning_info_list(name="Passenger Seat Heat Warning",info="0")

    @allure.title("副驾座椅加热无报警PassSeatHeatgAvlSts:3")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339536?projectId=46"
    )
    def test_caseid_1981053(self):
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatHeatgAvlSts",1)
        sleep(1)
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatHeatgAvlSts",3)
        self.soa.get_and_event_check_warning_info_list(name="Passenger Seat Heat Warning",info="1")

    @allure.title("副驾座椅加热无报警PassSeatHeatgAvlSts:2")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339535?projectId=46"
    )
    def test_caseid_1981052(self):
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatHeatgAvlSts",5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatHeatgAvlSts",2)
        self.soa.get_and_event_check_warning_info_list(name="Passenger Seat Heat Warning",info="0")

    @allure.title("副驾座椅加热无报警PassSeatHeatgAvlSts:1")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339534?projectId=46"
    )
    def test_caseid_1981051(self):
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatHeatgAvlSts",5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatHeatgAvlSts",1)
        self.soa.get_and_event_check_warning_info_list(name="Passenger Seat Heat Warning",info="0")

    @allure.title("副驾座椅加热无报警PassSeatHeatgAvlSts:0")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339533?projectId=46"
    )
    def test_caseid_1981050(self):
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatHeatgAvlSts",5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmpBodyFr03", "PassSeatHeatgAvlSts",0)
        self.soa.get_and_event_check_warning_info_list(name="Passenger Seat Heat Warning",info="0")



    @allure.title("主椅加热无报警DrvrSeatHeatgAvlSts:7")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339532?projectId=46"
    )
    def test_caseid_1981049(self):
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatHeatgAvlSts",5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatHeatgAvlSts",7)
        self.soa.get_and_event_check_warning_info_list(name="Driver Seat Heat Warning",info="0")

    @allure.title("主椅加热无报警DrvrSeatHeatgAvlSts:6")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339531?projectId=46"
    )
    def test_caseid_1981048(self):
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatHeatgAvlSts",5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatHeatgAvlSts",6)
        self.soa.get_and_event_check_warning_info_list(name="Driver Seat Heat Warning",info="0")

    @allure.title("主椅加热无报警DrvrSeatHeatgAvlSts:5")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339530?projectId=46"
    )
    def test_caseid_1981047(self):
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatHeatgAvlSts",1)
        sleep(1)
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatHeatgAvlSts",5)
        self.soa.get_and_event_check_warning_info_list(name="Driver Seat Heat Warning",info="1")

    @allure.title("主椅加热无报警DrvrSeatHeatgAvlSts:4")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339529?projectId=46"
    )
    def test_caseid_1981045(self):
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatHeatgAvlSts",5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatHeatgAvlSts",4)
        self.soa.get_and_event_check_warning_info_list(name="Driver Seat Heat Warning",info="0")

    @allure.title("主椅加热无报警DrvrSeatHeatgAvlSts:3")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339528?projectId=46"
    )
    def test_caseid_1981044(self):
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatHeatgAvlSts",1)
        sleep(1)
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatHeatgAvlSts",3)
        self.soa.get_and_event_check_warning_info_list(name="Driver Seat Heat Warning",info="1")

    @allure.title("主椅加热无报警DrvrSeatHeatgAvlSts:2")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339527?projectId=46"
    )
    def test_caseid_1981043(self):
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatHeatgAvlSts",5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatHeatgAvlSts",2)
        self.soa.get_and_event_check_warning_info_list(name="Driver Seat Heat Warning",info="0")

    @allure.title("主椅加热无报警DrvrSeatHeatgAvlSts:1")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339526?projectId=46"
    )
    def test_caseid_1981042(self):
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatHeatgAvlSts",5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatHeatgAvlSts",1)
        self.soa.get_and_event_check_warning_info_list(name="Driver Seat Heat Warning",info="0")

    @allure.title("主椅加热无报警DrvrSeatHeatgAvlSts:0")                       #pass
    @pytest.mark.sanity
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339523?projectId=46"
    )
    def test_caseid_1981033(self):
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatHeatgAvlSts",5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmdBodyFr04", "DrvrSeatHeatgAvlSts",0)
        self.soa.get_and_event_check_warning_info_list(name="Driver Seat Heat Warning",info="0")


    @allure.title("后排右侧座椅加热无报警SeatHeatgAvlStsRowSecRi:0")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518663?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1984991(self):
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecRi", 5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecRi", 7)
        self.soa.get_and_event_check_warning_info_list(name="Rear Right Seat Heat Warning", info="0")


    @allure.title("后排右侧座椅加热无报警SeatHeatgAvlStsRowSecRi:1")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518660?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1984990(self):
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecRi", 5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecRi", 1)
        self.soa.get_and_event_check_warning_info_list(name="Rear Right Seat Heat Warning", info="0")


    @allure.title("后排右侧座椅加热无报警SeatHeatgAvlStsRowSecRi:2")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518658?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1984989(self):
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecRi", 5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecRi", 1)
        self.soa.get_and_event_check_warning_info_list(name="Rear Right Seat Heat Warning", info="0")


    @allure.title("后排右侧座椅加热报警SeatHeatgAvlStsRowSecRi:3")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518654?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1984988(self):
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecRi", 1)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecRi", 3)
        self.soa.get_and_event_check_warning_info_list(name="Rear Right Seat Heat Warning", info="1")


    @allure.title("后排右侧座椅加热无报警SeatHeatgAvlStsRowSecRi:4")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518653?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1984987(self):
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecRi", 3)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecRi", 4)
        self.soa.get_and_event_check_warning_info_list(name="Rear Right Seat Heat Warning", info="0")


    @allure.title("后排右侧座椅加热报警SeatHeatgAvlStsRowSecRi:5")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518652?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1984986(self):
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecRi", 4)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecRi", 5)
        self.soa.get_and_event_check_warning_info_list(name="Rear Right Seat Heat Warning", info="1")


    @allure.title("后排右侧座椅加热无报警SeatHeatgAvlStsRowSecRi:6")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518651?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1984985(self):
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecRi", 5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecRi", 6)
        self.soa.get_and_event_check_warning_info_list(name="Rear Right Seat Heat Warning", info="0")


    @allure.title("后排右侧座椅加热无报警SeatHeatgAvlStsRowSecRi:7")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518647?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1984984(self):
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecRi", 5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecRi", 7)
        self.soa.get_and_event_check_warning_info_list(name="Rear Right Seat Heat Warning", info="0")


    @allure.title("后排左侧座椅加热无报警SeatHeatgAvlStsRowSecLe:0")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518638?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1984983(self):
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecLe", 5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecLe", 0)
        self.soa.get_and_event_check_warning_info_list(name="Rear Left Seat Heat Warning", info="0")


    @allure.title("后排左侧座椅加热无报警SeatHeatgAvlStsRowSecLe:1")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518637?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1984982(self):
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecLe", 5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecLe", 1)
        self.soa.get_and_event_check_warning_info_list(name="Rear Left Seat Heat Warning", info="0")


    @allure.title("后排左侧座椅加热无报警SeatHeatgAvlStsRowSecLe:2")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518636?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1984981(self):
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecLe", 3)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecLe", 2)
        self.soa.get_and_event_check_warning_info_list(name="Rear Left Seat Heat Warning", info="0")


    @allure.title("后排左侧座椅加热报警SeatHeatgAvlStsRowSecLe:3")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518635?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1984980(self):
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecLe", 1)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecLe", 3)
        self.soa.get_and_event_check_warning_info_list(name="Rear Left Seat Heat Warning", info="1")


    @allure.title("后排左侧座椅加热无报警SeatHeatgAvlStsRowSecLe:4")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518633?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1984979(self):
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecLe", 3)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecLe", 4)
        self.soa.get_and_event_check_warning_info_list(name="Rear Left Seat Heat Warning", info="0")


    @allure.title("后排左侧座椅加热报警SeatHeatgAvlStsRowSecLe:5")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518628?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1984978(self):
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecLe", 1)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecLe", 5)
        self.soa.get_and_event_check_warning_info_list(name="Rear Left Seat Heat Warning", info="1")


    @allure.title("后排左侧座椅加热无报警SeatHeatgAvlStsRowSecLe:6")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518625?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1984977(self):
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecLe", 5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecLe", 6)
        self.soa.get_and_event_check_warning_info_list(name="Rear Left Seat Heat Warning", info="0")


    @allure.title("后排左侧座椅加热无报警SeatHeatgAvlStsRowSecLe:7")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2518624?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1984976(self):
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecLe", 5)
        sleep(1)
        self.bus_comm.set("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecLe", 7)
        self.soa.get_and_event_check_warning_info_list(name="Rear Left Seat Heat Warning", info="0")
