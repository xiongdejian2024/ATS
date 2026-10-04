#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: test_NetWorkService.py
@Time: 2023/02/04 08:00
@Author: jingjing.wang
@Description: Test SOA service about NetStatService
"""
import os
import sys

import allure
import pytest

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
print(project_root)
sys.path.append(project_root)
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.common.logmanagment.logmanager import *
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.api.abc_interface import *
from xat_ecu.api.interfaces.dp1.ssh import Ssh

iccid = ""


@allure.feature("SOA服务接口")
@allure.story("互联服务/NetWorkService")
@pytest.mark.tcam
class TestNetStatService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.nucapp = NucApp(self.tc_config)
        self.tcam_ssh = TCAM_SSH()
        sleep(0.5)

        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        sleep(1)

        # 启动partner operator
        self.partner = S2sBaseClass([("NetStatService", "client")])
        self.partner.method_default_timeout = 0.1
        sleep(1)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.sd_tester.change_car_mode(0, do_assert=1)
        sleep(1)
        self.sd_tester.change_usage_mode(1, do_assert=1)
        sleep(2)
        Ssh("single_tcam").set_cell_band(Cell_band.SA)
        sleep(5)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def git_iccid_info(self):
        global iccid
        if self.tc_config["wifi_localhost"] == "172.18.128.71":
            iccid = "89860808092290006119"
        elif self.tc_config["wifi_localhost"] == "172.18.128.72":
            iccid = "89860808092290006063"

    @allure.title("SetNetResidentSts(bool is_5G) 开启5G功能")
    @pytest.mark.sanity
    def test_caseid_108875(self):
        with allure.step(f"Step:通过CDC打开5G开关:(服务:NetStatService;函数名:SetNetResidentSts)"):
            logger.info("通过CDC打开5G开关:(服务:NetStatService;函数名:SetNetResidentSts)")
            self.partner.send_request_and_ck_resp(
                'NetStatService_client',
                'SetNetResidentSts',
                args={"is_5G": True},
                ck_info={"out": True},
                timeout=3,
                cycle_time=1,
            )

    @allure.title("SetNetResidentSts(bool is_5G) 关闭5G功能")
    @pytest.mark.full
    def test_caseid_108876(self):
        with allure.step(f"Step:通过CDC关闭5G开关:(服务:NetStatService;函数名:SetNetResidentSts)"):
            logger.info("通过CDC关闭5G开关:(服务:NetStatService;函数名:SetNetResidentSts)")
            self.partner.send_request_and_ck_resp(
                'NetStatService_client',
                'SetNetResidentSts',
                args={"is_5G": False},
                ck_info={"out": True},
                timeout=3,
                cycle_time=1,
            )

    @allure.title("获取ICCID")  # 一个tcam有一个唯一的识别码直接获取即可
    @pytest.mark.full
    def test_caseid_108878(self):
        data=TCAM_SSH().get_ICCID()
        logger.info({f'iccid是{data}'})
        self.partner.send_request_and_ck_resp('NetStatService_client', 'GetIccid', {},
                                              {"out": data})

    @allure.title("获取蜂窝网络状态")
    @pytest.mark.sanity
    def test_caseid_108881(self):
        with allure.step(f"Step:通过SOApartner调用GetNetSts()获取蜂窝网络状态"):
            self.partner.send_request_and_ck_resp("NetStatService_client", "GetNetSts", {}, {"out": [
                {"ApnName": 1, "ApnSts": 0}]})

    @allure.title("获取基站辅助定位信息")
    @pytest.mark.smoke
    def test_caseid_108874(self):
        self.partner.send_request_and_ck_resp('NetStatService_client', 'GetNodeBInfo', {},
                                              {"out": {"mcc": 460, "mnc": 0}})  # ,"lac":6183,"cid":142709458

    @allure.title("通知基站辅助定位信息")
    @pytest.mark.full
    def test_caseid_110849(self):
        self.partner.ck_s2s_event("NetStatService_client", "NodeBInfo", {"info": {"mcc": 460, "mnc": 0}})

    @allure.title("通知蜂窝网络状态")
    @pytest.mark.sanity
    def test_caseid_110848(self):
        self.partner.ck_s2s_event("NetStatService_client", "NetWorkSts", {"NetStsArr": [{"ApnName": 1, "ApnSts": 0},
                                                                                        {"ApnName": 4, "ApnSts": 0}]})

    @allure.title("获取5G开关状态-5G开启")
    @pytest.mark.full
    def test_caseid_1918816(self):
        self.partner.send_method_request("NetStatService_client", "SetNetResidentSts", {"is_5G": True})
        self.partner.send_request_and_ck_resp('NetStatService_client', 'GetSwitch5GNet', {}, {"out": 1})

    @allure.title("获取5G开关状态-当前为4G状态")
    @pytest.mark.full
    def test_caseid_1918815(self):
        Ssh("single_tcam").set_cell_band(Cell_band.LTE)# 优先使用4G网络
        self.partner.send_request_and_ck_resp('NetStatService_client', 'GetSwitch5GNet', {}, {"out": 2},timeout=20)
        Ssh("single_tcam").set_cell_band(Cell_band.SA)# 优先使用5G网络
        self.partner.send_request_and_ck_resp('NetStatService_client', 'GetSwitch5GNet', {}, {"out": 1},timeout=20)
        
    @allure.title("获取/通知5G网络状态")
    @pytest.mark.sanity
    def test_caseid_1984307(self):
        Ssh("single_tcam").set_cell_band(Cell_band.SA)# 优先使用5G网络
        info = self.partner.return_latest_event("NetStatService_client", "NetworkStatus5G")
        assert info["info"]["networkStatus"] in [0, 1]
        self.partner.send_request_and_ck_resp('NetStatService_client', 'Get5GNetworkStatus', {}, 
                                              {"out": {"networkStatus":info["info"]["networkStatus"]}})