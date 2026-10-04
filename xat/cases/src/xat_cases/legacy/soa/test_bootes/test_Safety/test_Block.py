#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_safety.py
@Time         :2023/08/08 14:37:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import os

import allure
import pytest
from time import sleep

from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *


@allure.feature("SOA中间件测试")
@allure.story("功能安全/通道阻塞")
@pytest.mark.wjj
class TestSafety(TestBase):

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.domin = self.tc_config.get('partner_domin', 'acu')

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        super().after_class(self, ecu)
        os.system("ps -ef | grep tcpreplay| awk '{print $2}' | xargs kill -9")

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkNotEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')

    def after_each_func(self, ecu):
        try:
            self.sd_tester.stop_tester_present()
            self.partner.stop_operators()
        except Exception:
            pass
        super().after_each_func(ecu, start=False)

    @allure.title("通道阻塞_partner服务端心跳2.4s周期BGM不会触发功能安全故障")
    @pytest.mark.smoke
    def test_caseid_1886106(self):
        self.partner = S2sBaseClass([("ANPMRCService", "server", "ANPMRCService", 2400)], domin=self.domin)
        sleep(40)
        # todo: 1.BGM中bootes日志未打印SafetyBlock

    @allure.title("通道阻塞_partner客户端心跳2.4s周期BGM不会触发功能安全故障")
    @pytest.mark.full
    def test_caseid_1886104(self):
        self.partner = S2sBaseClass([("VehicleModeService", "client", "VehicleModeService", 2400)], domin=self.domin)
        sleep(40)
        # todo: 1.BGM中bootes日志未打印SafetyBlock

    @allure.title("通道阻塞_partner服务端心跳2.4s周期CDCQ不会触发功能安全故障")
    @allure.title("通道阻塞_partner服务端心跳2.4s周期CDCA不会触发功能安全故障")
    @allure.title("通道阻塞_partner服务端心跳2.4s周期ACU主板会触发功能安全故障")
    @allure.title("通道阻塞_partner服务端心跳2.4s周期ACU从板会触发功能安全故障")
    @pytest.mark.sanity
    def test_caseid_1886072_1886068_1886061_1886053(self):
        self.partner = S2sBaseClass([("VehicleModeService", "server", "VehicleModeService", 2400)], domin=self.domin)
        sleep(40)
        # todo: 1.CDC中bootes日志一直未打印SafetyBlock
        # todo: 1.ACU主板中bootes日志打印reportSafetyBlock--2，过2.4s后打印恢SafetyBlockRecovery--1

    @allure.title("通道阻塞_partner服务端心跳1.2s周期ACU主板不会触发功能安全故障")
    @allure.title("通道阻塞_partner服务端心跳1.2s周期ACU从板不会触发功能安全故障")
    @pytest.mark.full
    def test_caseid_1886060_1886052(self):
        self.partner = S2sBaseClass([("VehicleModeService", "server", "VehicleModeService", 1200)], domin=self.domin)
        sleep(40)
        # todo: 1.ACU主板中bootes日志未打印reportSafetyBlock--2

    @allure.title("通道阻塞_partner客户端心跳2.4s周期ACU主板会触发功能安全故障")
    @pytest.mark.full
    def test_caseid_1886059(self):
        self.partner = S2sBaseClass([("ANPMRCService", "client", "ANPMRCService", 2400)], domin=self.domin)
        sleep(40)
        # todo: 1.ACU主板中bootes日志打印reportSafetyBlock--2，过2.4s后打印恢SafetyBlockRecovery--1

    @allure.title("通道阻塞_partner客户端心跳1.2s周期ACU主板不会触发功能安全故障")
    @pytest.mark.sanity
    def test_caseid_1886058(self):
        self.partner = S2sBaseClass([("ANPMRCService", "client", "ANPMRCService", 1200)], domin=self.domin)
        sleep(40)
        # todo: 1.ACU主板中bootes日志未打印reportSafetyBlock--2

    @allure.title("通道阻塞_partner客户端心跳2.4s周期ACU从板会触发功能安全故障")
    @pytest.mark.sanity
    def test_caseid_1886051(self):
        self.partner = S2sBaseClass([("IMUService", "client", "IMUService", 2400)], domin=self.domin)
        sleep(35)
        # todo: 1.ACU从板中bootes日志打印reportSafetyBlock--2，过2.4s后打印恢SafetyBlockRecovery--1

    @allure.title("通道阻塞_partner客户端心跳1.2s周期ACU从板不会触发功能安全故障")
    @pytest.mark.full
    def test_caseid_1886050(self):
        self.partner = S2sBaseClass([("IMUService", "client", "IMUService", 1200)], domin=self.domin)
        sleep(35)
        # todo: 1.ACU从板中bootes日志未打印reportSafetyBlock--2