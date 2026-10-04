#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_wirelesscharge_abc.py
@Author      : xiangyue.li@jiduauto.com
@Time        : 2024/2/29 15:30
@Description : BGM车控车设无线充电
"""

import os
import sys
import pytest
import allure
from time import sleep
import copy

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("车控车设")
@allure.story("无线充电")
class TestWirelessChargeCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["WirelessPhoneChargingService_client", "ResetSOAConfigService_client",
                         "CentralLockService_client", "DoorService_client", "LightService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.RKE)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL,
            vehmtnst=VehMtnSts.StandStillVal3
        )
        self.io.set_five_door_sts(Door.close)
        sleep(1)

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    @allure.title("Mars1诊断复位_无线充电On_记忆")
    @pytest.mark.full
    def test_wireless_charge_caseid_1985358(self):
        self.sd_tester.write_ccp({950: 0x1, 962: 0x00})
        sleep(2)
        self.soa.ctrl_wireless_charge(WPCZoneId.FrontLeft, isOn.On)
        self.bus_comm.check_wireless_charge_drv(OnOff.On)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(20)
        self.bus_comm.check_wireless_charge_drv(OnOff.On)

    @allure.title("Mars1诊断复位_无线充电Off_记忆")
    @pytest.mark.full
    def test_wireless_charge_caseid_1995296(self):
        self.sd_tester.write_ccp({950: 0x1, 962: 0x00})
        sleep(2)
        self.soa.ctrl_wireless_charge(WPCZoneId.FrontLeft, isOn.Off)
        self.bus_comm.check_wireless_charge_drv(OnOff.Off)
        self.sd_tester.send_data([0x10, 0x01])
        sleep(20)
        self.bus_comm.check_wireless_charge_drv(OnOff.Off)

    @allure.title("MarsMca掉电重启_无线充电On_记忆")
    @pytest.mark.full
    def test_wireless_charge_caseid_1985355(self):
        self.sd_tester.write_ccp(ccp={950: 0x01, 962: 0x02})
        sleep(2)
        self.soa.ctrl_wireless_charge(zone=WPCZoneId.All, sts=isOn.On)
        sleep(1)
        self.bus_comm.check_wireless_charge_drv(OnOff.On)
        self.bus_comm.check_wireless_charge_pass(OnOff.On)
        with allure.step("掉电重启"):
            self.io.io_reset_bgm(times=10)
            sleep(5)
        self.bus_comm.check_wireless_charge_drv(OnOff.On)
        self.bus_comm.check_wireless_charge_pass(OnOff.On)

    @allure.title("MarsMca掉电重启_无线充电Off_记忆")
    @pytest.mark.full
    def test_wireless_charge_caseid_1995297(self):
        self.sd_tester.write_ccp(ccp={950: 0x01, 962: 0x02})
        sleep(2)
        self.soa.ctrl_wireless_charge(zone=WPCZoneId.All, sts=isOn.Off)
        sleep(1)
        self.bus_comm.check_wireless_charge_drv(OnOff.Off)
        self.bus_comm.check_wireless_charge_pass(OnOff.Off)
        with allure.step("掉电重启"):
            self.io.io_reset_bgm(times=10)
            sleep(5)
        self.bus_comm.check_wireless_charge_drv(OnOff.Off)
        self.bus_comm.check_wireless_charge_pass(OnOff.Off)

    @pytest.mark.full
    @pytest.mark.parametrize(
        "sts, inform, title",
        [[WPCFailureSts.NoFailure, WPCFaultsId.Ok, "MarsOne_无线充电故障提示(WPCFailureSts:0)"],
         [WPCFailureSts.Reserved3, WPCFaultsId.WPCFailureSignalInvalid, "MarsOne_无线充电故障提示(WPCFailureSts:1)"],
         [WPCFailureSts.OverTemperature, WPCFaultsId.OverTemperature, "MarsOne无线充电故障提示(WPCFailureSts:2)"],
         [WPCFailureSts.Reserved4, WPCFaultsId.WPCFailureSignalInvalid, "Mars单无线充电_充电故障提示(WPCFailureSts:3)"],
         [WPCFailureSts.RFOD, WPCFaultsId.RFOD,"Mars单无线充电_充电故障提示(WPCFailureSts:4)"],
         [WPCFailureSts.Reserved5, WPCFaultsId.WPCFailureSignalInvalid,"Mars单无线充电_充电故障提示(WPCFailureSts:5)"],
         [WPCFailureSts.VoltageProtected, WPCFaultsId.VoltageProtected,"Mars单无线充电_充电故障提示(WPCFailureSts:7)"],
         [WPCFailureSts.Reserved6, WPCFaultsId.WPCFailureSignalInvalid,"Mars无线充电_充电故障提示(WPCFailureSts:8)"],
         [WPCFailureSts.OverPowerProtected, WPCFaultsId.OverPowerProtected,"Mars无线充电_充电故障提示(WPCFailureSts:9)"],
         [WPCFailureSts.Reserved7, WPCFaultsId.WPCFailureSignalInvalid,"Mars无线充电_充电故障提示(WPCFailureSts:10)"],
         [WPCFailureSts.InternalFailure, WPCFaultsId.InternalError,"Mars无线充电_充电故障提示(WPCFailureSts:11)"],
         [WPCFailureSts.Reserved2, WPCFaultsId.WPCFailureSignalInvalid,"Mars无线充电_充电故障提示(WPCFailureSts:12)"],
         [WPCFailureSts.OFOD, WPCFaultsId.OFOD,"Mars无线充电_充电故障提示(WPCFailureSts:13)"],
         [WPCFailureSts.Invalid, WPCFaultsId.WPCFailureSignalInvalid,"Mars无线充电_充电故障提示(WPCFailureSts:14)"],
         [WPCFailureSts.NFCCardProtect, WPCFaultsId.NFCCardProtect,"Mars单无线充电_充电故障提示(WPCFailureSts:15)"]],
        ids=["1995443","1989752","1989707","1989753","1989754","1989755","1989756","1989757","1992470","1992473",
             "1992475","1992468","1992482","1992477","1989782"]
    )
    def test_wireless_charge_mars_fail_caseid_(self, sts, inform, title):
        allure.dynamic.title(title)
        self.sd_tester.write_ccp(ccp={950: 0x01, 962: 0x00})
        sleep(2)
        self.bus_comm.set_WPCModuleSts(WPCModuleSts.Standby)
        self.bus_comm.set_WPCCtrlRes(WPCCtrlRes.enabled)
        self.bus_comm.set_PhoneForgottenRmn(OnOff.Off)
        self.bus_comm.set_WPCFailureSts(sts)
        sleep(0.5)
        self.soa.check_wireless_inform(faultid=inform)

    @allure.title("Mars休眠唤醒_无线充电On_记忆")
    @pytest.mark.full
    def test_wireless_charge_caseid_1995453(self):
        """
        单独运行可以，全部运行容易失败，休眠唤醒用例都有这个问题
        @return:
        """
        self.sd_tester.write_ccp(ccp={950: 0x01, 962: 0x00})
        sleep(1)
        sts_dic = {OnOff.On: isOn.On, OnOff.Off: isOn.Off}
        for sig, sts in sts_dic.items():
            self.soa.ctrl_wireless_charge(zone=WPCZoneId.FrontRow, sts=sts)
            sleep(1)
            self.bus_comm.check_wireless_charge_drv(sig)
            sleep(2)
            self.mix.network_sleep()
            sleep(5)
            self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
            sleep(5)
            self.bus_comm.check_wireless_charge_drv(sig)

    @allure.title("Mars单无线充电_CDC设置前排所有区域无线充电关闭")
    @pytest.mark.sanity
    def test_wireless_charge_caseid_1989760(self):
        self.sd_tester.write_ccp(ccp={950: 0x1, 962: 0x00})
        sleep(2)
        self.soa.ctrl_wireless_charge(zone=WPCZoneId.All, sts=isOn.Off)
        self.bus_comm.check_wireless_charge_drv(OnOff.Off)

    @allure.title("Mars单无线充电_CDC设置前排所有区域无线充电开启")
    @pytest.mark.sanity
    def test_wireless_charge_caseid_1989685(self):
        self.sd_tester.write_ccp(ccp={950: 0x1, 962: 0x00})
        sleep(2)
        self.soa.ctrl_wireless_charge(zone=WPCZoneId.All, sts=isOn.On)
        self.bus_comm.check_wireless_charge_drv(OnOff.On)

    @allure.title("Mars单无线充电_多充电故障提示")
    @pytest.mark.full
    def test_wireless_charge_caseid_1989788(self):
        self.sd_tester.write_ccp(ccp={950: 0x01, 962: 0x00})
        sleep(2)
        self.bus_comm.set_WPCModuleSts(WPCModuleSts.Standby)
        self.bus_comm.set_WPCCtrlRes(WPCCtrlRes.enabled)
        self.bus_comm.set_PhoneForgottenRmn(OnOff.Off)
        self.bus_comm.set_WPCFailureSts(WPCFailureSts.OverTemperature)
        self.bus_comm.set_WPCFailureSts(WPCFailureSts.OverPowerProtected)
        sleep(0.5)
        self.soa.check_wireless_inform(faultid=WPCFaultsId.OverPowerProtected)

    @allure.title("mars手机遗留WPC提醒")
    @pytest.mark.full
    def test_wireless_charge_caseid_1985348(self):
        self.sd_tester.write_ccp(ccp={950: 0x01, 962: 0x00})
        sleep(2)
        self.soa.ctrl_wireless_charge(zone=WPCZoneId.FrontLeft, sts=isOn.On)
        self.bus_comm.set_WPCModuleSts()
        self.bus_comm.set_WPCCtrlRes()
        self.bus_comm.set_WPCFailureSts()
        self.bus_comm.set_PhoneForgottenRmn(OnOff.On)
        sleep(0.1)
        self.soa.check_wireless_inform(isforgotten=WPCIsForgotten.Forgotten)

    @pytest.mark.sanity
    @pytest.mark.parametrize(
        'sts, inform, title',
        [[WPCModuleSts.Standby, WPCChargingSts.Standby, "mars无线充电状态提示(WPCModuleSts:1)"],
         [WPCModuleSts.OverTemperatureProtected, WPCChargingSts.Fault,"mars无线充电状态提示(WPCModuleSts:0)"],
         [WPCModuleSts.Invalid, WPCChargingSts.Invalid,"mars无线充电状态提示(WPCModuleSts:15)"],
         [WPCModuleSts.VoltageProtected, WPCChargingSts.Fault,"mars无线充电状态提示无线充电异常(WPCModuleSts:4)"],
         [WPCModuleSts.Charging, WPCChargingSts.Charging,"mars无线充电状态提示无线充电中(WPCModuleSts:2)"],
         [WPCModuleSts.FOD, WPCChargingSts.Fault,"mars无线充电状态提示无线充电异常(WPCModuleSts:3)"],
         [WPCModuleSts.OFF, WPCChargingSts.ModuleOFF,"mars无线充电状态提示(WPCModuleSts:7)"],
         [WPCModuleSts.OverPowerProtected, WPCChargingSts.Fault,"mars无线充电状态提示无线充电异常(WPCModuleSts:5)"],
         [WPCModuleSts.Resvd5, WPCChargingSts.Invalid,"mars无线充电状态提示(WPCModuleSts:13)"],
         [WPCModuleSts.InternalFailure, WPCChargingSts.Fault,"mars无线充电状态提示无线充电模块内部故障(WPCModuleSts:10)"],
         [WPCModuleSts.Resvd6, WPCChargingSts.Invalid,"mars无线充电状态提示(WPCModuleSts:14)"],
         [WPCModuleSts.NFCCardFailure, WPCChargingSts.Fault,"mars无线充电状态提示(WPCModuleSts:12)"]],
        ids=["1985170","1985169","1991964","1985173","1985171","1985172","1985175","1985174","1985178","1985176",
             "1985179","1985177"]
    )
    def test_wireless_charge_mars_sts_caseid_(self, sts, inform, title):
        allure.dynamic.title(title)
        self.sd_tester.write_ccp(ccp={950: 0x01, 962: 0x00})
        sleep(2)
        self.soa.ctrl_wireless_charge(zone=WPCZoneId.All, sts=isOn.On)
        sleep(0.5)
        self.bus_comm.set_WPCModuleSts(sts=sts)
        self.bus_comm.set_WPCCtrlRes(WPCCtrlRes.enabled)
        self.bus_comm.set_PhoneForgottenRmn(OnOff.Off)
        self.bus_comm.set_WPCFailureSts(WPCFailureSts.NoFailure)
        self.soa.check_wireless_inform(chargingsts=inform)

    @allure.title("venus_CDC设置无线充电关闭")
    @pytest.mark.sanity
    def test_wireless_charge_caseid_1989684(self):
        self.sd_tester.write_ccp(ccp={950: 0x2})
        sleep(2)
        self.soa.ctrl_wireless_charge(zone=WPCZoneId.All, sts=isOn.Off)
        self.bus_comm.check_wireless_charge_drv(OnOff.Off)
        self.bus_comm.check_wireless_charge_pass(OnOff.Off)

    @allure.title("venus_CDC设置无线充电开启")
    @pytest.mark.sanity
    def test_wireless_charge_caseid_1985335(self):
        self.sd_tester.write_ccp(ccp={950: 0x2})
        sleep(2)
        self.soa.ctrl_wireless_charge(zone=WPCZoneId.All, sts=isOn.On)
        sleep(.1)
        self.bus_comm.check_wireless_charge_drv(OnOff.On)
        self.bus_comm.check_wireless_charge_pass(OnOff.On)

    @allure.title("venus_WPC与CDC交互_手机遗留WPC状态提醒")
    @pytest.mark.sanity
    def test_wireless_charge_caseid_1985336(self):
        self.sd_tester.write_ccp(ccp={950: 0x02})
        sleep(2)
        self.soa.ctrl_wireless_charge(zone=WPCZoneId.FrontRow, sts=isOn.On)
        self.bus_comm.set_WPCModuleSts()
        self.bus_comm.set_WPCCtrlRes()
        self.bus_comm.set_WPCFailureSts()
        self.bus_comm.set_PhoneForgottenRmn(OnOff.On)
        self.bus_comm.set_PhoneForgottenRmnPass(OnOff.On)
        self.soa.check_two_wireless_inform(
            isforgotten=WPCIsForgotten.Forgotten, isforgotten_pass=WPCIsForgotten.Forgotten)
        sleep(.1)
        self.bus_comm.set_PhoneForgottenRmn(OnOff.Off)
        self.bus_comm.set_PhoneForgottenRmnPass(OnOff.Off)
        self.soa.check_two_wireless_inform(
            isforgotten=WPCIsForgotten.NotForgotten, isforgotten_pass=WPCIsForgotten.NotForgotten)
        sleep(.1)
        self.bus_comm.set_PhoneForgottenRmn(OnOff.Off)
        self.bus_comm.set_PhoneForgottenRmnPass(OnOff.On)
        self.soa.check_two_wireless_inform(
            isforgotten=WPCIsForgotten.NotForgotten, isforgotten_pass=WPCIsForgotten.Forgotten)

    @allure.title("venus_多无线充电故障提示")
    @pytest.mark.full
    def test_wireless_charge_caseid_1989789(self):
        self.sd_tester.write_ccp(ccp={950: 0x02})
        sleep(2)
        self.bus_comm.set_WPCModuleSts(WPCModuleSts.Standby)
        self.bus_comm.set_WPCCtrlRes(WPCCtrlRes.enabled)
        self.bus_comm.set_PhoneForgottenRmn(OnOff.Off)
        self.bus_comm.set_WPCFailureSts(WPCFailureSts.OverTemperature)
        self.bus_comm.set_WPCFailureSts(WPCFailureSts.OverPowerProtected)
        sleep(0.5)
        self.soa.check_wireless_inform(faultid=WPCFaultsId.OverPowerProtected)

    @pytest.mark.full
    @pytest.mark.parametrize(
        "sts, inform, title",
        [[WPCFailureSts.NoFailure, WPCFaultsId.Ok, "venus_无线充电故障状态提示(WPCFailureSts:0)"],
         [WPCFailureSts.Reserved3, WPCFaultsId.WPCFailureSignalInvalid, "venus_无线充电故障状态提示(WPCFailureSts:1)"],
         [WPCFailureSts.OverTemperature, WPCFaultsId.OverTemperature, "venus_无线充电故障状态提示_(WPCFailureSts:2)"],
         [WPCFailureSts.Reserved4, WPCFaultsId.WPCFailureSignalInvalid, "venus_无线充电故障提示(WPCFailureSts:3)"],
         [WPCFailureSts.RFOD, WPCFaultsId.RFOD, "venus_无线充电故障提示(WPCFailureSts:4)"],
         [WPCFailureSts.Reserved5, WPCFaultsId.WPCFailureSignalInvalid, "venus_无线充电故障提示(WPCFailureSts:5)"],
         [WPCFailureSts.VoltageProtected, WPCFaultsId.VoltageProtected, "venus_无线充电故障提示(WPCFailureSts:7)"],
         [WPCFailureSts.Reserved6, WPCFaultsId.WPCFailureSignalInvalid, "venus_无线充电故障提示(WPCFailureSts:8)"],
         [WPCFailureSts.OverPowerProtected, WPCFaultsId.OverPowerProtected,
          "venus_无线充电故障提示(WPCFailureSts:9)"],
         [WPCFailureSts.Reserved7, WPCFaultsId.WPCFailureSignalInvalid, "venus_无线充电故障提示(WPCFailureSts:10)"],
         [WPCFailureSts.InternalFailure, WPCFaultsId.InternalError, "venus_无线充电故障提示(WPCFailureSts:11)"],
         [WPCFailureSts.Reserved2, WPCFaultsId.WPCFailureSignalInvalid, "venus_无线充电故障提示(WPCFailureSts:12)"],
         [WPCFailureSts.OFOD, WPCFaultsId.OFOD, "venus_无线充电故障提示(WPCFailureSts:13)"],
         [WPCFailureSts.Invalid, WPCFaultsId.WPCFailureSignalInvalid, "venus_无线充电故障提示(WPCFailureSts:14)"],
         [WPCFailureSts.NFCCardProtect, WPCFaultsId.NFCCardProtect, "venus_无线充电故障提示(WPCFailureSts:15)"]],
        ids=["1995444", "1986082", "1986080", "1986081", "1985184", "1989736", "1989741", "1989737", "1992483",
             "1992476","1992490", "1992430", "1992439", "1992485", "1989781"]
    )
    def test_wireless_charge_venus_fail_caseid_(self, sts, inform, title):
        allure.dynamic.title(title)
        self.sd_tester.write_ccp(ccp={950: 0x02, 962: 0x00})
        sleep(2)
        self.soa.ctrl_wireless_charge(zone=WPCZoneId.All, sts=isOn.On)
        sleep(0.1)
        self.bus_comm.set_WPCModuleSts(WPCModuleSts.Standby)
        self.bus_comm.set_WPCCtrlRes(WPCCtrlRes.enabled)
        self.bus_comm.set_PhoneForgottenRmn(OnOff.Off)
        self.bus_comm.set_WPCFailureSts(sts)
        self.bus_comm.set_WPCModuleStsPass(WPCModuleSts.Standby)
        self.bus_comm.set_WPCCtrlResPass(WPCCtrlRes.enabled)
        self.bus_comm.set_PhoneForgottenRmnPass(OnOff.Off)
        self.bus_comm.set_WPCFailureStsPass(sts)
        self.soa.check_two_wireless_inform(faultid=inform, faultid_pass=inform)
        sleep(.1)

    @pytest.mark.full
    @pytest.mark.parametrize(
        'sts, inform, title',
        [[WPCModuleSts.Standby, WPCChargingSts.Standby, "venus无线充电状态提示(WPCModuleSts:1)"],
         [WPCModuleSts.OverTemperatureProtected, WPCChargingSts.Fault, "venus无线充电状态无提示(WPCModuleSts:0)"],
         [WPCModuleSts.Invalid, WPCChargingSts.Invalid, "venus无线充电状态提示(WPCModuleSts:15)"],
         [WPCModuleSts.VoltageProtected, WPCChargingSts.Fault, "venus无线充电状态提示(WPCModuleSts:4)"],
         [WPCModuleSts.Charging, WPCChargingSts.Charging, "venus无线充电状态提示(WPCModuleSts:2)"],
         [WPCModuleSts.FOD, WPCChargingSts.Fault, "venus无线充电状态提示(WPCModuleSts:3)"],
         [WPCModuleSts.OFF, WPCChargingSts.ModuleOFF, "venus_无线充电状态提示(WPCModuleSts:7)"],
         [WPCModuleSts.OverPowerProtected, WPCChargingSts.Fault, "venus_无线充电状态提示(WPCModuleSts:5)"],
         [WPCModuleSts.Resvd5, WPCChargingSts.Invalid, "venus_无线充电状态提示(WPCModuleSts:13)"],
         [WPCModuleSts.InternalFailure, WPCChargingSts.Fault, "venus_无线充电状态提示(WPCModuleSts:10)"],
         [WPCModuleSts.Resvd6, WPCChargingSts.Invalid, "venus_无线充电状态提示(WPCModuleSts:14)"],
         [WPCModuleSts.NFCCardFailure, WPCChargingSts.Fault, "venus_无线充电状态提示(WPCModuleSts:12)"]],
        ids=["1985181", "1985182", "1986083", "1989739", "1985183", "1989738", "1989740", "1985372", "1995294",
             "1989774","1995295", "1985373"]
    )
    def test_wireless_charge_venus_sts_caseid_(self, sts, inform, title):
        allure.dynamic.title(title)
        self.mix.set_common_precontion(ccp={950: 0x02, 636: 0x0})
        self.soa.ctrl_wireless_charge(zone=WPCZoneId.All, sts=isOn.On)
        sleep(0.1)
        self.bus_comm.set_WPCModuleSts(sts)
        self.bus_comm.set_WPCCtrlRes(WPCCtrlRes.enabled)
        self.bus_comm.set_PhoneForgottenRmn(OnOff.Off)
        self.bus_comm.set_WPCFailureSts(WPCFailureSts.NoFailure)
        self.bus_comm.set_WPCModuleStsPass(sts)
        self.bus_comm.set_WPCCtrlResPass(WPCCtrlRes.enabled)
        self.bus_comm.set_PhoneForgottenRmnPass(OnOff.Off)
        self.bus_comm.set_WPCFailureStsPass(WPCFailureSts.NoFailure)
        self.soa.check_two_wireless_inform(chargingsts=inform, chargingsts_pass=inform)
        sleep(.1)

    @allure.title("venus掉电重启_无线充电Off_记忆")
    @pytest.mark.full
    def test_wireless_charge_caseid_1992484(self):
        self.sd_tester.write_ccp(ccp={950: 0x02, 962: 0x02})
        sleep(1)
        self.soa.ctrl_wireless_charge(zone=WPCZoneId.FrontRow, sts=isOn.Off)
        sleep(1)
        self.bus_comm.check_wireless_charge_drv(OnOff.Off)
        self.bus_comm.check_wireless_charge_pass(OnOff.Off)
        with allure.step("掉电重启"):
            self.io.io_reset_bgm(times=10)
            sleep(5)
        self.bus_comm.check_wireless_charge_drv(OnOff.Off)
        self.bus_comm.check_wireless_charge_pass(OnOff.Off)

    @allure.title("venus掉电重启_无线充电On_记忆")
    @pytest.mark.full
    def test_wireless_charge_caseid_1918839(self):
        self.sd_tester.write_ccp(ccp={950: 0x02, 962: 0x00})
        sleep(1)
        self.soa.ctrl_wireless_charge(zone=WPCZoneId.FrontRow, sts=isOn.On)
        sleep(1)
        self.bus_comm.check_wireless_charge_drv(OnOff.On)
        self.bus_comm.check_wireless_charge_pass(OnOff.On)
        with allure.step("掉电重启"):
            self.io.io_reset_bgm(times=10)
            sleep(5)
        self.bus_comm.check_wireless_charge_drv(OnOff.On)
        self.bus_comm.check_wireless_charge_pass(OnOff.On)

    @allure.title("Venus休眠唤醒_无线充电Off_记忆")
    @pytest.mark.full
    def test_wireless_charge_caseid_118902(self):
        self.sd_tester.write_ccp(ccp={950: 0x02, 962: 0x00})
        sleep(2)
        self.soa.ctrl_wireless_charge(zone=WPCZoneId.FrontRow, sts=isOn.Off)
        sleep(.1)
        self.bus_comm.check_wireless_charge_drv(OnOff.Off)
        self.bus_comm.check_wireless_charge_pass(OnOff.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        sleep(1)
        with allure.step("休眠唤醒"):
            self.mix.network_sleep()
            sleep(5)
            self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
            sleep(5)
        self.bus_comm.check_wireless_charge_drv(OnOff.Off)
        self.bus_comm.check_wireless_charge_pass(OnOff.Off)

    @allure.title("Venus休眠唤醒_无线充电On_记忆")
    @pytest.mark.full
    def test_wireless_charge_caseid_1985351(self):
        self.sd_tester.write_ccp(ccp={950: 0x02, 962: 0x02})
        sleep(2)
        self.soa.ctrl_wireless_charge(zone=WPCZoneId.FrontRow, sts=isOn.On)
        sleep(1)
        self.bus_comm.check_wireless_charge_drv(OnOff.On)
        self.bus_comm.check_wireless_charge_pass(OnOff.On)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        sleep(2)
        with allure.step("休眠唤醒"):
            self.mix.network_sleep()
            sleep(5)
            self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
            sleep(5)
        self.bus_comm.check_wireless_charge_drv(OnOff.On)
        self.bus_comm.check_wireless_charge_pass(OnOff.On)

    @pytest.mark.full
    @pytest.mark.parametrize(
        'ccp, title',
        [[{950: 0x01, 962: 0x00}, "mars恢复出厂设置_WPC状态"],
         [{950: 0x02, 962: 0x00}, "venus恢复出厂设置_WPC状态"]],
        ids=["1991404", "118904"]
    )
    def test_reset_wireless_charge_caseid_(self, ccp, title):
        allure.dynamic.title(title)
        self.sd_tester.write_ccp(ccp)
        sleep(2)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        sleep(2)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(.1)
        self.soa.ctrl_wireless_charge(WPCZoneId.FrontLeft, isOn.Off)
        self.soa.ctrl_wireless_charge(WPCZoneId.FrontRight, isOn.Off)
        sleep(0.5)
        self.bus_comm.check_wireless_charge_drv(OnOff.Off)
        self.bus_comm.check_wireless_charge_pass(OnOff.Off)
        sleep(1)
        self.soa.send_method_request(
            partner_key="ResetSOAConfigService_client",
            method_name="ResetAllVehicleSOAConfig",
            args={}
        )
        sleep(30)
        self.soa.send_request_and_ck_resp(
            partner_key="ResetSOAConfigService_client",
            method_name="GetResetAllVehicleSOAConfigResult",
            args={},
            ck_info={"out": 2}
        )
        self.bus_comm.check_wireless_charge_drv(OnOff.On)
        self.bus_comm.check_wireless_charge_pass(OnOff.On)
        self.soa.get_internal_light_mode(LightMode.Auto)
