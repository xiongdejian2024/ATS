#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_light_did.py
@Author      : xiangyue.li@jiduauto.com
@Time        : 2024/4/19 11:30
@Description : 内灯DID
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
from xat_ecu.legacy.common.data_handle import *
import random


@allure.feature("车控车设")
@allure.story("内灯DID")
class TestLightCtrl(TestABCBase):
    def before_class(self, ecu):
        # self.soa.update(["HighVoltageService_client","CentralLockService_client","WTIService_client","LightService_client","CentralLockService_client","DoorService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        # self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3)
        self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
        pass

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    # @allure.title("DID_阅读灯按钮")
    # @pytest.mark.smoke
    # def test_HvActive_caseid_23981(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,vehmtnst=VehMtnSts.StandStillVal3)
    #     self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])    
    #     self.bus_comm.set_singal("cem_lin3","OhcCem_Lin3Fr04","BtnStsOHCLiBtnReadingLe", 1)
    #     self.bus_comm.set_singal("cem_lin3","OhcCem_Lin3Fr04","BtnStsOHCLiBtnReadingRi", 1)
    #     self.bus_comm.set_singal("cem_lin3","OhcCem_Lin3Fr04","BtnStsOHCIntrLiSwtAutOnSts", 1)
    #     self.bus_comm.set_singal("cem_lin3","OhcCem_Lin3Fr04","BtnStsOHCIntrLiSwtAllOnSts", 1)
    #     sleep(2)
    #     self.sd_tester.send_request_and_recv_response([0x22,0x42,0x2F],recv=[0x62,0x42,0x2F,
    #                                                                              0x01])

    @allure.title("458737_DID_410B")
    @pytest.mark.smoke
    def test_caseid_1986969(self):
        # self.bus_comm.set_twilight_sensor_sts(OutdBri=OutdBriSts.Day,BtnStsOHC=BtnStsSngTyp.BtnPsd,TwliBriRaw=TwliBriRaw.Day)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.bus_comm.set_day_mode()
        sleep(2)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0x0B], recv=[0x62, 0x41, 0x0B, 0x02])
        self.bus_comm.set_night_mode()
        sleep(2)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0x0B], recv=[0x62, 0x41, 0x0B, 0x01])

    @allure.title("452806_DID_416D")
    @pytest.mark.smoke
    def test_caseid_1986975(self):
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0x6D], recv=[0x62, 0x41, 0x6D, 0x07, 0xD0])

    @allure.title("452806_DID_416E")
    @pytest.mark.smoke
    def test_caseid_1986976(self):
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0x6E], recv=[0x62, 0x41, 0x6E, 0x07, 0xD0])

    @allure.title("452806_DID_41E5")
    @pytest.mark.smoke
    def test_caseid_1987011(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        self.sd_tester.send_data([0x22, 0x41, 0xE5])
        sleep(2)
        self.sd_tester.send_data([0x2F, 0x41, 0xE5, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFC])
        self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0xE5],
            recv=[0x62, 0x41, 0xE5, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        )
        sleep(1)
        self.sd_tester.send_data([0x2F, 0x41, 0xE5, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x64, 0xFC])
        self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0xE5],
            recv=[0x62, 0x41, 0xE5, 0x00, 0x00, 0x00, 0x00, 0x00, 0x64]
        )
        sleep(1)
        self.sd_tester.send_data([0x2F, 0x41, 0xE5, 0x03, 0x00, 0x00, 0x00, 0x00, 0x64, 0x00, 0xFC])
        self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0xE5],
            recv=[0x62, 0x41, 0xE5, 0x00, 0x00, 0x00, 0x00, 0x64, 0x00]
        )
        sleep(1)
        self.sd_tester.send_data([0x2F, 0x41, 0xE5, 0x03, 0x00, 0x00, 0x00, 0x64, 0x00, 0x00, 0xFC])
        self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0xE5],
            recv=[0x62, 0x41, 0xE5, 0x00, 0x00, 0x00, 0x64, 0x00, 0x00]
        )
        sleep(1)
        self.sd_tester.send_data([0x2F, 0x41, 0xE5, 0x03, 0x00, 0x00, 0x64, 0x00, 0x00, 0x00, 0xFC])
        self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0xE5],
            recv=[0x62, 0x41, 0xE5, 0x00, 0x00, 0x64, 0x00, 0x00, 0x00]
        )
        sleep(1)
        self.sd_tester.send_data([0x2F, 0x41, 0xE5, 0x03, 0x00, 0x64, 0x00, 0x00, 0x00, 0x00, 0xFC])
        self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0xE5],
            recv=[0x62, 0x41, 0xE5, 0x00, 0x64, 0x00, 0x00, 0x00, 0x00]
        )
        sleep(1)
        self.sd_tester.send_data([0x2F, 0x41, 0xE5, 0x03, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFC])
        self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0xE5],
            recv=[0x62, 0x41, 0xE5, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00]
        )
        sleep(1)
        self.sd_tester.send_data([0x2F, 0x41, 0xE5, 0x03, 0x64, 0x64, 0x64, 0x64, 0x64, 0x64, 0xFC])
        self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0xE5],
            recv=[0x62, 0x41, 0xE5, 0x64, 0x64, 0x64, 0x64, 0x64, 0x64]
        )
        sleep(2)
        self.sd_tester.send_data([0x2F, 0x41, 0xE5, 0x00, 0xFC])
        self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0xE5],
            recv=[0x62, 0x41, 0xE5, 0x64, 0x64, 0x64, 0x64, 0x64, 0x64]
        )

    @allure.title("476548_DID_422F")
    @pytest.mark.smoke
    def test_caseid_1987091(self):
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0x2F], recv=[0x62, 0x42, 0x2F, 0x00])
        self.bus_comm.set_singal("cem_lin3", "OhcCem_Lin3Fr01", "BtnStsOHCRLiBtnReadingLe", 1)
        sleep(1)
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0x2F], recv=[0x62, 0x42, 0x2F, 0x01])
        self.bus_comm.set_singal("cem_lin3", "OhcCem_Lin3Fr01", "BtnStsOHCRLiBtnReadingRi", 1)
        sleep(1)
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0x2F], recv=[0x62, 0x42, 0x2F, 0x03])
        self.bus_comm.set_singal("cem_lin3", "OhcCem_Lin3Fr01", "BtnStsOHCRLiBtnReadingLe", 0)
        sleep(1)
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0x2F], recv=[0x62, 0x42, 0x2F, 0x02])

    @allure.title("476548_DID_4230")
    @pytest.mark.smoke
    def test_caseid_1987092(self):
        # self.sd_tester.send_request_and_recv_response([0x22,0x42,0x30],recv=[0x62,0x42,0x30,0x00])
        self.bus_comm.set_singal("cem_lin3", "OhcCem_Lin3Fr04", "BtnStsOHCLiBtnReadingLe", 1)
        self.bus_comm.set_singal("cem_lin3", "OhcCem_Lin3Fr04", "BtnStsOHCLiBtnReadingRi", 1)
        self.bus_comm.set_singal("cem_lin3", "OhcCem_Lin3Fr04", "BtnStsOHCIntrLiSwtAutOnSts", 1)
        self.bus_comm.set_singal("cem_lin3", "OhcCem_Lin3Fr04", "BtnStsOHCIntrLiSwtAllOnSts", 1)
        sleep(1)
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0x30], recv=[0x62, 0x42, 0x30, 0x0F])

    @allure.title("452806_DID_416F")
    @pytest.mark.smoke
    def test_caseid_1987012(self):
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0x6F], recv=[0x62, 0x41, 0x6F, 0x01, 0xF4])

    @allure.title("452806_DID_4170")
    @pytest.mark.smoke
    def test_caseid_1987013(self):
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0x70], recv=[0x62, 0x41, 0x70, 0x03, 0xE8])

    @allure.title("476557_20EB_Mars1_不含console下方灯带_无头枕音响_DID氛围灯自动寻址")
    @pytest.mark.full
    def test_alm_auto_address_v210_caseid_1989821(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x1, 964: 0x0}
        )
        sleep(2)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        sleep(2)
        self.sd_tester.send_data([0x31, 0x01, 0x20, 0xEB])
        sleep(20)
        self.sd_tester.send_request_and_recv_response(
            msg=[0x31, 0x03, 0x20, 0xEB],
            recv=[0x71, 0x03, 0x20, 0xEB, 0x20, 0x22, 0x22, 0x22, 0x00, 0x00]
        )

    @allure.title("476557_20EB_Mars1_不含console下方灯带_含头枕音响_DID氛围灯自动寻址")
    @pytest.mark.full
    def test_alm_auto_address_v210_caseid_1989823(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x2, 964: 0x0}
        )
        sleep(2)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        sleep(2)
        self.sd_tester.send_data([0x31, 0x01, 0x20, 0xEB])
        sleep(20)
        self.sd_tester.send_request_and_recv_response(
            msg=[0x31, 0x03, 0x20, 0xEB],
            recv=[0x71, 0x03, 0x20, 0xEB, 0x20, 0x22, 0x22, 0x22, 0x22, 0x00]
        )

    @allure.title("476557_20EB_Mars1_含console下方灯带_不含头枕音响_DID氛围灯自动寻址")
    @pytest.mark.full
    def test_alm_auto_address_v210_caseid_1989822(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x1, 964: 0x1}
        )
        sleep(2)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        sleep(2)
        self.sd_tester.send_data([0x31, 0x01, 0x20, 0xEB])
        sleep(20)
        self.sd_tester.send_request_and_recv_response(
            msg=[0x31, 0x03, 0x20, 0xEB],
            recv=[0x71, 0x03, 0x20, 0xEB, 0x20, 0x22, 0x22, 0x22, 0x02, 0x00]
        )

    @allure.title("476557_20EB_Mars1_含console下方灯带_含头枕音响_DID氛围灯自动寻址")
    @pytest.mark.sanity
    def test_alm_auto_address_v210_caseid_1989824(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x2, 964: 0x1}
        )
        sleep(2)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        sleep(2)
        self.sd_tester.send_data([0x31, 0x01, 0x20, 0xEB])
        sleep(20)
        self.sd_tester.send_request_and_recv_response(
            msg=[0x31, 0x03, 0x20, 0xEB],
            recv=[0x71, 0x03, 0x20, 0xEB, 0x20, 0x22, 0x22, 0x22, 0x22, 0x02]
        )

    @allure.title("476557_20EB_venus_DID氛围灯自动寻址")
    @pytest.mark.full
    def test_alm_auto_address_caseid_1991568(self):
        ccp_lst = {
            "venus01": {950: 0x2, 636: 0x1, 964: 0x1},
            # "venus00": {950: 0x2, 636: 0x1, 964: 0x0}
        }
        for car_type, ccp in ccp_lst.items():
            with allure.step("车型：" + car_type):
                sleep(0.1)
            self.mix.set_common_precontion(
                usage_mode=UsageMode.CONVENIENCE,
                car_mode=CarMode.NORMAL,
                ccp=ccp
            )
            sleep(2)
            self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
            self.sd_tester.send_data([0x31, 0x01, 0x20, 0xEB])
            sleep(10)
            self.sd_tester.send_request_and_recv_response(
                msg=[0x31, 0x03, 0x20, 0xEB],
                recv=[0x71, 0x03, 0x20, 0xEB, 0x20, 0x22, 0x22, 0x22, 0x22, 0x00]
            )

    @allure.title("476557_20EB_venus800_DID氛围灯自动寻址")
    @pytest.mark.sanity
    def test_alm_auto_address_caseid_1991569(self):
        ccp_lst = {
            "venus80001": {950: 0x2, 636: 0x2, 964: 0x1},
            "venus80000": {950: 0x2, 636: 0x2, 964: 0x0}
        }
        for car_type, ccp in ccp_lst.items():
            with allure.step("车型：" + car_type):
                sleep(0.1)
            self.mix.set_common_precontion(
                usage_mode=UsageMode.CONVENIENCE,
                car_mode=CarMode.NORMAL,
                ccp={950: 0x2, 636: 0x2, 964: 0x1}
            )
            sleep(2)
            self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
            self.sd_tester.send_data([0x31, 0x01, 0x20, 0xEB])
            sleep(10)
            self.sd_tester.send_request_and_recv_response(
                msg=[0x31, 0x03, 0x20, 0xEB],
                recv=[0x71, 0x03, 0x20, 0xEB, 0x20, 0x22, 0x22, 0x22, 0x22, 0x22]
            )

    @allure.title("496994_20F1_Mars1_不含console下方灯带_无头枕音响_DID亮度进入配置模式")
    @pytest.mark.full
    def test_20F1_v210_caseid_1989997(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x1, 964: 0x0}
        )
        sleep(2)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        sleep(2)
        self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF1, 0xB2, 0x21])
        sleep(20)
        self.sd_tester.send_request_and_recv_response(
            msg=[0x31, 0x03, 0x20, 0xF1],
            recv=[0x71, 0x03, 0x20, 0xF1, 0x20, 0xFF, 0xFF, 0x11, 0x11, 0x11, 0x00, 0x00]
        )
        sleep(2)

    @allure.title("496994_20F1_Mars1_不含console下方灯带_含头枕音响_DID亮度进入配置模式")
    @pytest.mark.full
    def test_20F1_caseid_1989998(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x2, 964: 0x0}
        )
        sleep(2)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        sleep(2)
        self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF1, 0xB2, 0x21])
        sleep(20)
        self.sd_tester.send_request_and_recv_response(
            msg=[0x31, 0x03, 0x20, 0xF1],
            recv=[0x71, 0x03, 0x20, 0xF1, 0x20, 0xFF, 0xFF, 0x11, 0x11, 0x11, 0x11, 0x00]
        )
        sleep(2)

    @allure.title("496994_20F1_Mars1_含console下方灯带_无头枕音响_DID亮度进入配置模式")
    @pytest.mark.full
    def test_20F1_v210_caseid_1989995(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x1, 964: 0x1}
        )
        sleep(2)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        sleep(2)
        self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF1, 0xB2, 0x21])
        sleep(20)
        self.sd_tester.send_request_and_recv_response(
            msg=[0x31, 0x03, 0x20, 0xF1],
            recv=[0x71, 0x03, 0x20, 0xF1, 0x20, 0xFF, 0xFF, 0x11, 0x11, 0x11, 0x01, 0x00]
        )
        sleep(2)

    @allure.title("496994_20F1_Mars1_含console下方灯带_含头枕音响_DID亮度进入配置模式")
    @pytest.mark.sanity
    def test_20F1_v210_caseid_1989996(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x2, 964: 0x1}
        )
        sleep(2)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        sleep(2)
        self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF1, 0xB2, 0x21])
        sleep(20)
        self.sd_tester.send_request_and_recv_response(
            msg=[0x31, 0x03, 0x20, 0xF1],
            recv=[0x71, 0x03, 0x20, 0xF1, 0x20, 0xFF, 0xFF, 0x11, 0x11, 0x11, 0x11, 0x01]
        )
        sleep(2)

    @allure.title("496994_20F1_venus_DID20F1亮度进入配置模式")
    @pytest.mark.full
    def test_20F1_caseid_1992519(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x2, 636: 0x1}
        )
        sleep(2)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        sleep(2)
        self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF1, 0xB2, 0x21])
        sleep(20)
        self.sd_tester.send_request_and_recv_response(
            msg=[0x31, 0x03, 0x20, 0xF1],
            recv=[0x71, 0x03, 0x20, 0xF1, 0x20, 0xFF, 0xFF, 0x11, 0x11, 0x11, 0x11, 0x00]
        )
        sleep(2)

    @allure.title("496994_20F1_venus800_DID20F1亮度进入配置模式")
    @pytest.mark.sanity
    def test_20F1_caseid_1992520(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x2, 636: 0x2}
        )
        sleep(2)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        sleep(2)
        self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF1, 0xB2, 0x21])
        sleep(20)
        self.sd_tester.send_request_and_recv_response(
            msg=[0x31, 0x03, 0x20, 0xF1],
            recv=[0x71, 0x03, 0x20, 0xF1, 0x20, 0xFF, 0xFF, 0x11, 0x11, 0x11, 0x11, 0x11]
        )
        sleep(2)

    # @allure.title("496994_20F2_Mars1_不含console下方灯带_无头枕音响_DID亮度退出配置模式")
    # @pytest.mark.full
    # def test_20F2_v210_caseid_1990000(self):
    #     self.mix.set_common_precontion(
    #         usage_mode=UsageMode.CONVENIENCE,
    #         car_mode=CarMode.NORMAL,
    #         ccp={950: 0x1, 636: 0x1, 964: 0x0}
    #     )
    #     sleep(2)
    #     self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
    #     sleep(2)
    #     self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF2, 0xFF, 0xFF])
    #     sleep(20)
    #     self.sd_tester.send_data([0x31, 0x03, 0x20, 0xF2])
    #     sleep(2)
    #
    # @allure.title("496994_20F2_Mars1_不含console下方灯带_含头枕音响_DID亮度退出配置模式")
    # @pytest.mark.full
    # def test_20F2_v210_caseid_1989999(self):
    #     self.mix.set_common_precontion(
    #         usage_mode=UsageMode.CONVENIENCE,
    #         car_mode=CarMode.NORMAL,
    #         ccp={950: 0x1, 636: 0x2, 964: 0x0}
    #     )
    #     sleep(2)
    #     self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
    #     sleep(2)
    #     self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF2, 0xFF, 0xFF])
    #     sleep(20)
    #     self.sd_tester.send_data([0x31, 0x03, 0x20, 0xF2])
    #     sleep(2)
    #
    # @allure.title("496994_20F2_Mars1_含console下方灯带_无头枕音响_DID亮度退出配置模式")
    # @pytest.mark.full
    # def test_20F2_v210_caseid_1990002(self):
    #     self.mix.set_common_precontion(
    #         usage_mode=UsageMode.CONVENIENCE,
    #         car_mode=CarMode.NORMAL,
    #         ccp={950: 0x1, 636: 0x2, 964: 0x1}
    #     )
    #     sleep(2)
    #     self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
    #     sleep(2)
    #     self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF2, 0xFF, 0xFF])
    #     sleep(20)
    #     self.sd_tester.send_data([0x31, 0x03, 0x20, 0xF2])
    #     sleep(2)

    # @allure.title("Mars1_含console下方灯带_无头枕音响_DID亮度退出配置模式")
    # def test_20F2_caseid_1990002(self):
    #     self.mix.set_common_precontion(
    #         usage_mode=UsageMode.CONVENIENCE,
    #         car_mode=CarMode.NORMAL,
    #         ccp={950: 0x1, 636: 0x1, 964: 0x1}
    #     )
    #     sleep(2)
    #     self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
    #     sleep(2)
    #     for i in range(0, 0x0F + 1):
    #         for j in range(0, 0x0F + 1):
    #             self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF1, i, j])
    #             sleep(20)
    #             self.sd_tester.send_data([0x31, 0x03, 0x20, 0xF1])
    #             sleep(2)
    #             self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF2, 0xFF, 0xFF])
    #             sleep(20)
    #             # self.sd_tester.send_data([0x31, 0x03, 0x20, 0xF2])
    #             code, resp = self.sd_tester.send_request_and_recv_response(
    #                 msg=[0x31, 0x03, 0x20, 0xF2],
    #                 recv=[0x71, 0x03, 0x20, 0xF2, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00],
    #                 do_assert=False
    #             )
    #             with allure.step(f"20F2返回值为{resp}"):
    #                 logger.info(f"20F2返回值为{resp}")
    #             sleep(2)

    # @allure.title("496994_20F2_Mars1_含console下方灯带_含头枕音响_DID亮度退出配置模式")
    # @pytest.mark.sanity
    # def test_20F2_v210_caseid_1990001(self):
    #     self.mix.set_common_precontion(
    #         usage_mode=UsageMode.CONVENIENCE,
    #         car_mode=CarMode.NORMAL,
    #         ccp={950: 0x1, 636: 0x2, 964: 0x1}
    #     )
    #     sleep(2)
    #     self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
    #     sleep(2)
    #     self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF1, 0x11, 0x11])
    #     sleep(20)
    #     self.sd_tester.send_data([0x31, 0x03, 0x20, 0xF1])
    #     sleep(2)
    #     self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF2, 0xFF, 0xFF])
    #     sleep(20)
    #     self.sd_tester.send_data([0x31, 0x03, 0x20, 0xF2])
    #     sleep(2)
    #
    # @allure.title("496994_20F2_venus_DID20F2亮度退出配置模式")
    # @pytest.mark.full
    # def test_20F2_caseid_1992523(self):
    #     self.mix.set_common_precontion(
    #         usage_mode=UsageMode.CONVENIENCE,
    #         car_mode=CarMode.NORMAL,
    #         ccp={950: 0x2, 636: 0x1}
    #     )
    #     sleep(2)
    #     self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
    #     sleep(2)
    #     self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF1, 0xB2, 0x21])
    #     sleep(20)
    #     self.sd_tester.send_data([0x31, 0x03, 0x20, 0xF1])
    #     sleep(2)
    #     self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF2, 0xB2, 0x22])
    #     sleep(20)
    #     self.sd_tester.send_data([0x31, 0x03, 0x20, 0xF2])
    #     sleep(2)

    @allure.title("496994_20F2_venus800_DID20F2亮度退出配置模式")
    @pytest.mark.sanity
    def test_20F2_caseid_1992524(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x2, 636: 0x2}
        )
        sleep(2)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        sleep(1)
        self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF1, 0x11, 0x11])
        sleep(20)
        self.sd_tester.send_data([0x31, 0x03, 0x20, 0xF1])
        sleep(2)
        self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF2, 0xFF, 0xFF])
        sleep(20)
        self.sd_tester.send_data([0x31, 0x03, 0x20, 0xF2])
        sleep(2)

    @allure.title("496994_20F3_Mars1_不含console下方灯带_无头枕音响_DID亮度调节配置模式")
    @pytest.mark.full
    def test_20F3_v210_caseid_1990005(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x1, 964: 0x0}
        )
        sleep(2)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        sleep(1)
        self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF3, 0x01, 0x20])
        sleep(20)
        self.sd_tester.send_request_and_recv_response(
            msg=[0x31, 0x03, 0x20, 0xF3],
            recv=[0x71, 0x03, 0x20, 0xF3, 0x10, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, 0x00, 0x00, 0x00, 0x00]
        )
        sleep(2)

    @allure.title("496994_20F3_Mars1_不含console下方灯带_含头枕音响_DID亮度调节配置模式")
    @pytest.mark.full
    def test_20F3_v210_caseid_1990006(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x2, 964: 0x0}
        )
        sleep(2)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        sleep(1)
        self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF3, 0x01, 0x20])
        sleep(20)
        self.sd_tester.send_request_and_recv_response(
            msg=[0x31, 0x03, 0x20, 0xF3],
            recv=[0x71, 0x03, 0x20, 0xF3, 0x10, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, 0x00, 0x00]
        )
        sleep(2)

    @allure.title("496994_20F3_Mars1_含console下方灯带_无头枕音响_DID亮度调节配置模式")
    @pytest.mark.full
    def test_20F3_v210_caseid_1990003(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x1, 964: 0x1}
        )
        sleep(2)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        sleep(1)
        self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF3, 0x01, 0x20])
        sleep(20)
        self.sd_tester.send_request_and_recv_response(
            msg=[0x31, 0x03, 0x20, 0xF3],
            recv=[0x71, 0x03, 0x20, 0xF3, 0x10, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, 0x00, 0x00, 0x00]
        )
        sleep(2)

    @allure.title("496994_20F3_Mars1_含console下方灯带_含头枕音响_DID亮度调节配置模式")
    @pytest.mark.sanity
    def test_20F3_v210_caseid_1990004(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x2, 964: 0x1}
        )
        sleep(2)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        sleep(1)
        self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF3, 0x01, 0x20])
        sleep(20)
        self.sd_tester.send_request_and_recv_response(
            msg=[0x31, 0x03, 0x20, 0xF3],
            recv=[0x71, 0x03, 0x20, 0xF3, 0x10, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, 0x00]
        )
        sleep(2)

    @allure.title("496994_20F3_venus_DID20F3亮度调节配置模式")
    @pytest.mark.full
    def test_20F3_caseid_1992521(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x2, 636: 0x1}
        )
        sleep(2)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        sleep(1)
        self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF3, 0x01, 0x20])
        sleep(20)
        self.sd_tester.send_request_and_recv_response(
            msg=[0x31, 0x03, 0x20, 0xF3],
            recv=[0x71, 0x03, 0x20, 0xF3, 0x10, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, 0x00, 0x00]
        )
        sleep(2)

    @allure.title("496994_20F3_venus800_DID20F3亮度调节配置模式")
    @pytest.mark.sanity
    def test_20F3_caseid_1992522(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x2, 636: 0x2}
        )
        sleep(2)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        sleep(1)
        self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF3, 0x01, 0x20])
        sleep(20)
        self.sd_tester.send_request_and_recv_response(
            msg=[0x31, 0x03, 0x20, 0xF3],
            recv=[0x71, 0x03, 0x20, 0xF3, 0x10, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65]
        )
        sleep(2)

    # @allure.title("478644_4600_调节内灯目标亮度值的系统状态")
    # @pytest.mark.smoke
    # def test_4600_caseid_1989416(self):
    #     self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
    #     sleep(2)
    #     self.sd_tester.send_request_and_recv_response(
    #         [0x22, 0x46, 0x00],
    #         recv=[0x62, 0x46, 0x00, 0x00, 0x64, 0x32, 0x3C, 0x64]
    #     )
    #     sleep(20)

    @allure.title("4600_KL30重启BGM内灯亮度值调节")
    @pytest.mark.add
    @pytest.mark.sanity
    def test_4600_caseid_1993290(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        sleep(1)
        num_lst = [hex(random.randint(0, 100))[2:] for _ in range(5)]
        for i in range(len(num_lst)):
            if len(num_lst[i]) < 2:
                num_lst[i] = "0" + num_lst[i]
            else:
                num_lst[i] = num_lst[i]
        self.sd_tester.send_data("2E4600"+num_lst[0]+num_lst[1]+num_lst[2]+num_lst[3]+num_lst[4])
        sleep(10)
        self.io.io_reset_bgm(times=10)
        sleep(15)
        # 生成随机数
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        self.sd_tester.send_request_and_recv_response(
            [0x22, 0x46, 0x00],
            recv="624600"+num_lst[0]+num_lst[1]+num_lst[2]+num_lst[3]+num_lst[4]
        )
        self.sd_tester.send_data([0x2E, 0x46, 0x00, 0x00, 0x64, 0x32, 0x3C, 0x64])
        sleep(10)

    @allure.title("4600_内灯亮度值调节")
    @pytest.mark.add
    @pytest.mark.sanity
    def test_4600_caseid_1984459(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        sleep(1)
        num_lst = [hex(random.randint(0, 100))[2:] for _ in range(5)]
        for i in range(len(num_lst)):
            if len(num_lst[i]) < 2:
                num_lst[i] = "0" + num_lst[i]
            else:
                num_lst[i] = num_lst[i]
        self.sd_tester.send_data("2E4600" + num_lst[0] + num_lst[1] + num_lst[2] + num_lst[3] + num_lst[4])
        sleep(5)
        self.sd_tester.send_data("1181")
        sleep(25)
        # 生成随机数
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        self.sd_tester.send_request_and_recv_response(
            [0x22, 0x46, 0x00],
            recv="624600" + num_lst[0] + num_lst[1] + num_lst[2] + num_lst[3] + num_lst[4]
        )
        self.sd_tester.send_data([0x2E, 0x46, 0x00, 0x00, 0x64, 0x32, 0x3C, 0x64])
        sleep(10)

    @allure.title("434759_4260_手套箱解锁供电控制")
    @pytest.mark.sanity
    def test_4260_caseid_1992563(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        sleep(1)
        self.sd_tester.send_request_and_recv_response(
            [0x2F, 0x42, 0x60, 0x03, 0x00],
            recv=[0x6F, 0x42, 0x60, 0x03, 0x0]
        )
        sleep(2)
        self.sd_tester.send_request_and_recv_response(
            [0x2F, 0x42, 0x60, 0x03, 0x01],
            recv=[0x6F, 0x42, 0x60, 0x03, 0x01]
        )
        sleep(2)
        self.sd_tester.send_request_and_recv_response(
            [0x2F, 0x42, 0x60, 0x00],
            recv=[0x6F, 0x42, 0x60, 0x00, 0x01]
        )
        sleep(2)

    # def test_22F186(self):
    #     self.sd_tester.send_data([0x22, 0xF1, 0x86])
    #     sleep(5)

    @allure.title("680079_D136_SALM休眠唤醒控制")
    @pytest.mark.sanity
    def test_D136_caseid_1992564(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        self.sd_tester.send_data([0x2F, 0xD1, 0x36, 0x03, 0x01])
        sleep(2)
        self.sd_tester.send_request_and_recv_response(
            [0x22, 0xD1, 0x36],
            recv=[0x62, 0xD1, 0x36, 0x01]
        )
        self.sd_tester.send_data([0x2F, 0xD1, 0x36, 0x03, 0x00])
        sleep(2)
        self.sd_tester.send_request_and_recv_response(
            [0x22, 0xD1, 0x36],
            recv=[0x62, 0xD1, 0x36, 0x00]
        )
        sleep(2)

    @allure.title("434336_2015_私有锁禁用")
    @pytest.mark.full
    def test_2015_caseid_1992565(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
        self.sd_tester.send_request_and_recv_response(
            [0x31, 0x01, 0x20, 0x15, 0x00],
            recv=[0x71, 0x01, 0x20, 0x15, 0x22]
        )
        sleep(20)
        self.sd_tester.send_request_and_recv_response(
            [0x31, 0x03, 0x20, 0x15],
            recv=[0x71, 0x03, 0x20, 0x15, 0x20]
        )
        sleep(5)
        self.sd_tester.send_request_and_recv_response(
            [0x31, 0x01, 0x20, 0x15, 0x01],
            recv=[0x71, 0x01, 0x20, 0x15, 0x22]
        )
        sleep(20)
        self.sd_tester.send_request_and_recv_response(
            [0x31, 0x03, 0x20, 0x15],
            recv=[0x71, 0x03, 0x20, 0x15, 0x20]
        )

    @pytest.mark.full
    @allure.title("KL30重启BGM416F内灯白天至黑夜值存储")
    @pytest.mark.add
    def test_caseid_1993311(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        # 将范围转换为16进制
        num = random.randint(400, 700)
        # 生成随机数
        random_hex = hex(num)[2:]
        self.sd_tester.send_data("2E416F0"+random_hex)
        sleep(10)
        self.io.io_reset_bgm(times=10)
        sleep(15)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        self.sd_tester.send_request_and_recv_response(msg="22416F", recv="62416F0"+random_hex)
        self.sd_tester.send_data([0x2E, 0x41, 0x6F, 0x01, 0xF4])
        sleep(10)

    @pytest.mark.full
    @allure.title("KL30重启BGM4170内灯黑夜至白天值存储")
    @pytest.mark.add
    def test_caseid_1993312(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        # 将范围转换为16进制
        num = random.randint(800, 1300)
        # 生成随机数
        random_hex = hex(num)[2:]
        self.sd_tester.send_data("2E41700" + random_hex)
        sleep(10)
        self.io.io_reset_bgm(times=10)
        sleep(15)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        self.sd_tester.send_request_and_recv_response(msg="224170", recv="6241700" + random_hex)
        self.sd_tester.send_data([0x2E, 0x41, 0x70, 0x03, 0xE8])
        sleep(10)

    @pytest.mark.full
    @allure.title("4170_1181重启内灯黑夜至白天值存储")
    @pytest.mark.add
    def test_caseid_1984492(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        # 将范围转换为16进制
        num = random.randint(800, 1300)
        # 生成随机数
        random_hex = hex(num)[2:]
        self.sd_tester.send_data("2E41700" + random_hex)
        sleep(5)
        self.sd_tester.send_data("1181")
        sleep(25)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        self.sd_tester.send_request_and_recv_response(msg="224170", recv="6241700" + random_hex)
        self.sd_tester.send_data([0x2E, 0x41, 0x70, 0x03, 0xE8])
        sleep(10)

    @pytest.mark.full
    @allure.title("KL30重启BGM416D室内灯光白天至黑夜计时器存储")
    @pytest.mark.add
    def test_caseid_1993313(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        # 将范围转换为16进制
        num = random.randint(0, 10000)
        # 生成随机数
        random_hex = hex(num)[2:]
        if len(random_hex) < 4:
            if len(random_hex) == 3:
                random_hex = "0" + random_hex
            elif len(random_hex) == 2:
                random_hex = "00" + random_hex
            else:
                random_hex = "000" + random_hex
        self.sd_tester.send_data("2E416D" + random_hex)
        sleep(10)
        self.io.io_reset_bgm(times=10)
        sleep(15)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        self.sd_tester.send_request_and_recv_response(msg="22416D", recv="62416D" + random_hex)
        self.sd_tester.send_data([0x2E, 0x41, 0x6D, 0x07, 0xD0])
        sleep(10)

    @pytest.mark.full
    @allure.title("416D_1181室内灯光白天至黑夜计时器存储")
    @pytest.mark.add
    def test_caseid_1984493(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        # 将范围转换为16进制
        num = random.randint(0, 10000)
        # 生成随机数
        random_hex = hex(num)[2:]
        if len(random_hex) < 4:
            if len(random_hex) == 3:
                random_hex = "0" + random_hex
            elif len(random_hex) == 2:
                random_hex = "00" + random_hex
            else:
                random_hex = "000" + random_hex
        self.sd_tester.send_data("2E416D" + random_hex)
        sleep(5)
        self.sd_tester.send_data("1181")
        sleep(25)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        self.sd_tester.send_request_and_recv_response(msg="22416D", recv="62416D" + random_hex)
        self.sd_tester.send_data([0x2E, 0x41, 0x6D, 0x07, 0xD0])
        sleep(10)

    @pytest.mark.full
    @allure.title("KL30重启BGM416E室内灯光黑夜至白天计时器存储")
    @pytest.mark.add
    def test_caseid_1993314(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        # 将范围转换为16进制
        num = random.randint(0, 10000)
        # 生成随机数
        random_hex = hex(num)[2:]
        if len(random_hex) < 4:
            if len(random_hex) == 3:
                random_hex = "0" + random_hex
            elif len(random_hex) == 2:
                random_hex = "00" + random_hex
            else:
                random_hex = "000" + random_hex
        self.sd_tester.send_data("2E416E" + random_hex)
        sleep(10)
        self.io.io_reset_bgm(times=10)
        sleep(15)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        self.sd_tester.send_request_and_recv_response(msg="22416E", recv="62416E" + random_hex)
        self.sd_tester.send_data([0x2E, 0x41, 0x6E, 0x07, 0xD0])
        sleep(10)

    @pytest.mark.full
    @allure.title("416E_1181室内灯光黑夜至白天计时器存储")
    @pytest.mark.add
    def test_caseid_1984494(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        # 将范围转换为16进制
        num = random.randint(0, 10000)
        # 生成随机数
        random_hex = hex(num)[2:]
        if len(random_hex) < 4:
            if len(random_hex) == 3:
                random_hex = "0" + random_hex
            elif len(random_hex) == 2:
                random_hex = "00" + random_hex
            else:
                random_hex = "000" + random_hex
        self.sd_tester.send_data("2E416E" + random_hex)
        sleep(10)
        self.sd_tester.send_data("1181")
        sleep(25)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        self.sd_tester.send_request_and_recv_response(msg="22416E", recv="62416E" + random_hex)
        self.sd_tester.send_data([0x2E, 0x41, 0x6E, 0x07, 0xD0])
        sleep(10)

    @pytest.mark.full
    @allure.title("416F_1181重启内灯白天至黑夜值存储")
    @pytest.mark.add
    def test_caseid_1984491(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        # 将范围转换为16进制
        num = random.randint(0, 10000)
        # 生成随机数
        random_hex = hex(num)[2:]
        if len(random_hex) < 4:
            if len(random_hex) == 3:
                random_hex = "0" + random_hex
            elif len(random_hex) == 2:
                random_hex = "00" + random_hex
            else:
                random_hex = "000" + random_hex
        self.sd_tester.send_data("2E416E" + random_hex)
        sleep(5)
        self.sd_tester.send_data("1181")
        sleep(25)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5)
        self.sd_tester.send_request_and_recv_response(msg="22416E", recv="62416E" + random_hex)
        self.sd_tester.send_data([0x2E, 0x41, 0x6E, 0x07, 0xD0])
        sleep(10)

    # def test_alm_auto_address_caseid_abc(self):
    #     ccp_lst = {
    #         "venus01": {950: 0x2, 636: 0x2, 964: 0x0},
    #         # "venus00": {950: 0x2, 636: 0x1, 964: 0x0}
    #     }
    #     for car_type, ccp in ccp_lst.items():
    #         with allure.step("车型：" + car_type):
    #             sleep(0.1)
    #         self.mix.set_common_precontion(
    #             usage_mode=UsageMode.CONVENIENCE,
    #             car_mode=CarMode.NORMAL,
    #             ccp=ccp
    #         )
    #         sleep(2)
    #         self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
    #         self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF1, 0x00, 0x00])
    #         sleep(10)
    #         self.sd_tester.send_data([0x31, 0x03, 0x20, 0xF1])
    #         sleep(10)
    #         self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF3, 0x01, 0x10])
    #         sleep(20)
    #         self.sd_tester.send_data([0x31, 0x03, 0x20, 0xF3])
    #         sleep(10)
    #         self.sd_tester.send_data([0x31, 0x01, 0x20, 0xF2, 0x00, 0x00])
    #         sleep(10)
    #         self.sd_tester.send_data([0x31, 0x03, 0x20, 0xF2])
    #         sleep(10)

    # @allure.title("诊断控制SALM点亮、熄灭D136")
    # def test_caseid_1991477(self):
    #     self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L0)
    #     self.sd_tester.send_request_and_recv_response(msg="22D136", recv="62D13600")
    #     self.mix.set_usage_mode(UsageMode.ABANDONED)
    #     sleep(2)
    #     self.sd_tester.send_data([0x22, 0xD1, 0x36])
    #     sleep(2)





